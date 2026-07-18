"""Zender, ontvanger en veilige afzonderlijke checkpoints voor ECP-0."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from itertools import permutations
from pathlib import Path
from typing import Any

import torch
from torch import Tensor, nn
from torch.nn import functional as F


@dataclass(frozen=True, slots=True)
class ModelSpec:
    factor_sizes: tuple[int, ...]
    factor_embedding_dim: int
    symbol_embedding_dim: int
    hidden_dim: int
    vocabulary_size: int
    message_length: int
    sender_family: str = "categorical_encoder_autoregressive_sender"
    receiver_family: str = "sequence_encoder_multihead_classifier"

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> "ModelSpec":
        factors = config["world"]["factors"]
        training = config["training"]
        channel = config["channel"]
        return cls(
            factor_sizes=tuple(len(spec["values"]) for spec in factors.values()),
            factor_embedding_dim=training["factor_embedding_dim"],
            symbol_embedding_dim=training["symbol_embedding_dim"],
            hidden_dim=training["hidden_dim"],
            vocabulary_size=channel["vocabulary_size"],
            message_length=channel["message_length"],
            sender_family=config["agents"]["sender"].get(
                "family", "categorical_encoder_autoregressive_sender"
            ),
            receiver_family=config["agents"]["receiver"].get(
                "family", "sequence_encoder_multihead_classifier"
            ),
        )

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "ModelSpec":
        return cls(
            factor_sizes=tuple(value["factor_sizes"]),
            factor_embedding_dim=value["factor_embedding_dim"],
            symbol_embedding_dim=value["symbol_embedding_dim"],
            hidden_dim=value["hidden_dim"],
            vocabulary_size=value["vocabulary_size"],
            message_length=value["message_length"],
            sender_family=value.get(
                "sender_family", "categorical_encoder_autoregressive_sender"
            ),
            receiver_family=value.get(
                "receiver_family", "sequence_encoder_multihead_classifier"
            ),
        )


class Sender(nn.Module):
    """Autoregressieve zender die factorcategorieën naar discrete symbolen omzet."""

    def __init__(self, spec: ModelSpec) -> None:
        super().__init__()
        self.spec = spec
        self.factor_embeddings = nn.ModuleList(
            nn.Embedding(size, spec.factor_embedding_dim) for size in spec.factor_sizes
        )
        combined_dim = len(spec.factor_sizes) * spec.factor_embedding_dim
        self.context_projection = nn.Linear(combined_dim, spec.hidden_dim)
        self.symbol_embedding = nn.Embedding(
            spec.vocabulary_size, spec.symbol_embedding_dim
        )
        self.start_embedding = nn.Parameter(torch.empty(spec.symbol_embedding_dim))
        self.recurrent = nn.GRUCell(
            spec.symbol_embedding_dim + spec.hidden_dim, spec.hidden_dim
        )
        self.symbol_head = nn.Linear(spec.hidden_dim, spec.vocabulary_size)
        nn.init.normal_(self.start_embedding, mean=0.0, std=0.02)

    def forward(
        self,
        meanings: Tensor,
        *,
        temperature: float = 1.0,
        sample: bool = True,
    ) -> tuple[Tensor, Tensor]:
        embedded_factors = [
            embedding(meanings[:, index])
            for index, embedding in enumerate(self.factor_embeddings)
        ]
        context = torch.tanh(self.context_projection(torch.cat(embedded_factors, dim=-1)))
        hidden = context
        previous = self.start_embedding.unsqueeze(0).expand(meanings.shape[0], -1)
        one_hot_messages: list[Tensor] = []
        tokens: list[Tensor] = []

        for _ in range(self.spec.message_length):
            hidden = self.recurrent(torch.cat((previous, context), dim=-1), hidden)
            logits = self.symbol_head(hidden)
            if sample:
                symbol = F.gumbel_softmax(logits, tau=temperature, hard=True, dim=-1)
            else:
                token = logits.argmax(dim=-1)
                symbol = F.one_hot(token, self.spec.vocabulary_size).to(logits.dtype)
            token = symbol.argmax(dim=-1)
            one_hot_messages.append(symbol)
            tokens.append(token)
            previous = symbol @ self.symbol_embedding.weight

        return torch.stack(one_hot_messages, dim=1), torch.stack(tokens, dim=1)

    def relaxed_message(self, meanings: Tensor, *, temperature: float = 1.0) -> Tensor:
        """Deterministische symboolverdelingen voor structurele trainingsdruk.

        Dit pad verzendt niets tijdens evaluatie. Het maakt uitsluitend zichtbaar
        hoe de zender zijn waarschijnlijkheidsmassa over het bestaande discrete
        kanaal verdeelt, zonder Gumbelruis of vooraf toegewezen symboolbetekenis.
        """
        if temperature <= 0:
            raise ValueError("Temperatuur moet positief zijn.")
        embedded_factors = [
            embedding(meanings[:, index])
            for index, embedding in enumerate(self.factor_embeddings)
        ]
        context = torch.tanh(self.context_projection(torch.cat(embedded_factors, dim=-1)))
        hidden = context
        previous = self.start_embedding.unsqueeze(0).expand(meanings.shape[0], -1)
        distributions: list[Tensor] = []
        for _ in range(self.spec.message_length):
            hidden = self.recurrent(torch.cat((previous, context), dim=-1), hidden)
            distribution = torch.softmax(
                self.symbol_head(hidden) / temperature, dim=-1
            )
            distributions.append(distribution)
            previous = distribution @ self.symbol_embedding.weight
        return torch.stack(distributions, dim=1)


class LearnedPermutationSlotSender(nn.Module):
    """Compositionele slots waarvan de factor-slotkoppeling intern wordt gekozen."""

    def __init__(self, spec: ModelSpec) -> None:
        super().__init__()
        if spec.message_length != len(spec.factor_sizes):
            raise ValueError(
                "Een permutationslotzender vereist één slot per betekenisfactor."
            )
        self.spec = spec
        self.factor_embeddings = nn.ModuleList(
            nn.Embedding(size, spec.factor_embedding_dim) for size in spec.factor_sizes
        )
        self.factor_projections = nn.ModuleList(
            nn.Linear(spec.factor_embedding_dim, spec.hidden_dim)
            for _ in spec.factor_sizes
        )
        self.binding_logits = nn.Parameter(
            torch.empty(spec.message_length, len(spec.factor_sizes))
        )
        self.slot_heads = nn.ModuleList(
            nn.Linear(spec.hidden_dim, spec.vocabulary_size)
            for _ in range(spec.message_length)
        )
        nn.init.normal_(self.binding_logits, mean=0.0, std=0.05)
        matrices = []
        for permutation in permutations(range(len(spec.factor_sizes))):
            matrix = torch.zeros(spec.message_length, len(spec.factor_sizes))
            matrix[torch.arange(spec.message_length), torch.tensor(permutation)] = 1.0
            matrices.append(matrix)
        self.register_buffer("permutation_matrices", torch.stack(matrices))

    def forward(
        self,
        meanings: Tensor,
        *,
        temperature: float = 1.0,
        sample: bool = True,
    ) -> tuple[Tensor, Tensor]:
        logits = self._message_logits(meanings)
        if sample:
            symbols = F.gumbel_softmax(logits, tau=temperature, hard=True, dim=-1)
        else:
            tokens = logits.argmax(dim=-1)
            symbols = F.one_hot(tokens, self.spec.vocabulary_size).to(logits.dtype)
        return symbols, symbols.argmax(dim=-1)

    def relaxed_message(self, meanings: Tensor, *, temperature: float = 1.0) -> Tensor:
        if temperature <= 0:
            raise ValueError("Temperatuur moet positief zijn.")
        return torch.softmax(self._message_logits(meanings) / temperature, dim=-1)

    def binding_matrix(self, *, straight_through: bool = True) -> Tensor:
        soft = self.soft_binding_matrix()
        permutation_scores = torch.einsum(
            "psf,sf->p", self.permutation_matrices, self.binding_logits
        )
        hard = self.permutation_matrices[permutation_scores.argmax()]
        if straight_through:
            return hard - soft.detach() + soft
        return hard

    def soft_binding_matrix(self) -> Tensor:
        shifted = self.binding_logits - self.binding_logits.max()
        soft = torch.exp(shifted)
        for _ in range(8):
            soft = soft / soft.sum(dim=1, keepdim=True)
            soft = soft / soft.sum(dim=0, keepdim=True)
        return soft

    def _message_logits(self, meanings: Tensor) -> Tensor:
        factors = torch.stack(
            [
                torch.tanh(projection(embedding(meanings[:, index])))
                for index, (embedding, projection) in enumerate(
                    zip(
                        self.factor_embeddings,
                        self.factor_projections,
                        strict=True,
                    )
                )
            ],
            dim=1,
        )
        slots = torch.einsum("sf,bfh->bsh", self.binding_matrix(), factors)
        return torch.stack(
            [
                head(slots[:, index])
                for index, head in enumerate(self.slot_heads)
            ],
            dim=1,
        )


class InjectivePermutationSlotSender(nn.Module):
    """Vrij geleerde slots en injectieve atoomcodes zonder semantische labels.

    Iedere factor kiest exact één slot. Binnen een factor krijgt iedere waarde
    exact één ander symbool. De harde toewijzingen worden alleen structureel
    begrensd; geen slot of symbool krijgt vooraf een menselijke betekenis.
    """

    def __init__(self, spec: ModelSpec) -> None:
        super().__init__()
        if spec.message_length != len(spec.factor_sizes):
            raise ValueError(
                "Een injectieve permutationslotzender vereist één slot per factor."
            )
        if any(size > spec.vocabulary_size for size in spec.factor_sizes):
            raise ValueError(
                "Injectieve atoomcodes vereisen minstens zoveel symbolen als waarden."
            )
        self.spec = spec
        self.binding_logits = nn.Parameter(
            torch.empty(spec.message_length, len(spec.factor_sizes))
        )
        # Vierkante matrices bevatten naast echte factorwaarden ook dummy-rijen.
        # Daardoor kan Sinkhorn een volledige permutatie leren, terwijl alleen de
        # eerste `factor_size` rijen daadwerkelijk worden uitgezonden.
        self.codebook_logits = nn.ParameterList(
            [
                nn.Parameter(
                    torch.empty(spec.vocabulary_size, spec.vocabulary_size)
                )
                for _ in spec.factor_sizes
            ]
        )
        nn.init.normal_(self.binding_logits, mean=0.0, std=0.05)
        for logits in self.codebook_logits:
            nn.init.normal_(logits, mean=0.0, std=0.05)

        matrices = []
        for permutation in permutations(range(len(spec.factor_sizes))):
            matrix = torch.zeros(spec.message_length, len(spec.factor_sizes))
            matrix[torch.arange(spec.message_length), torch.tensor(permutation)] = 1.0
            matrices.append(matrix)
        self.register_buffer("permutation_matrices", torch.stack(matrices))

    def forward(
        self,
        meanings: Tensor,
        *,
        temperature: float = 1.0,
        sample: bool = True,
    ) -> tuple[Tensor, Tensor]:
        del temperature, sample
        factor_codes = torch.stack(
            [
                self.codebook_matrix(index)[meanings[:, index]]
                for index in range(len(self.spec.factor_sizes))
            ],
            dim=1,
        )
        symbols = torch.einsum(
            "sf,bfv->bsv", self.binding_matrix(), factor_codes
        )
        return symbols, symbols.argmax(dim=-1)

    def relaxed_message(self, meanings: Tensor, *, temperature: float = 1.0) -> Tensor:
        if temperature <= 0:
            raise ValueError("Temperatuur moet positief zijn.")
        factor_codes = torch.stack(
            [
                self.soft_codebook_matrix(index, temperature=temperature)[
                    meanings[:, index]
                ]
                for index in range(len(self.spec.factor_sizes))
            ],
            dim=1,
        )
        return torch.einsum(
            "sf,bfv->bsv", self.soft_binding_matrix(), factor_codes
        )

    def binding_matrix(self, *, straight_through: bool = True) -> Tensor:
        soft = self.soft_binding_matrix()
        permutation_scores = torch.einsum(
            "psf,sf->p", self.permutation_matrices, self.binding_logits
        )
        hard = self.permutation_matrices[permutation_scores.argmax()]
        if straight_through:
            return hard - soft.detach() + soft
        return hard

    def soft_binding_matrix(self) -> Tensor:
        return self._sinkhorn(self.binding_logits)

    def codebook_matrix(
        self, factor_index: int, *, straight_through: bool = True
    ) -> Tensor:
        """Geef de echte waarderijen van een harde één-op-één-symboolcode."""
        soft_full = self.soft_codebook_matrix(factor_index)
        hard_full = self._greedy_permutation(soft_full.detach())
        factor_size = self.spec.factor_sizes[factor_index]
        hard = hard_full[:factor_size]
        soft = soft_full[:factor_size]
        if straight_through:
            return hard - soft.detach() + soft
        return hard

    def soft_codebook_matrix(
        self, factor_index: int, *, temperature: float = 1.0
    ) -> Tensor:
        if temperature <= 0:
            raise ValueError("Temperatuur moet positief zijn.")
        return self._sinkhorn(self.codebook_logits[factor_index] / temperature)

    def soft_codebook_matrices(self) -> tuple[Tensor, ...]:
        return tuple(
            self.soft_codebook_matrix(index)
            for index in range(len(self.spec.factor_sizes))
        )

    @staticmethod
    def _sinkhorn(logits: Tensor) -> Tensor:
        shifted = logits - logits.max()
        soft = torch.exp(shifted)
        for _ in range(12):
            soft = soft / soft.sum(dim=1, keepdim=True)
            soft = soft / soft.sum(dim=0, keepdim=True)
        return soft

    @staticmethod
    def _greedy_permutation(scores: Tensor) -> Tensor:
        """Deterministische harde permutatie; gradiënten lopen via Sinkhorn."""
        size = scores.shape[0]
        hard = torch.zeros_like(scores)
        used_rows: set[int] = set()
        used_columns: set[int] = set()
        for flat_index in scores.flatten().argsort(descending=True).tolist():
            row, column = divmod(flat_index, size)
            if row in used_rows or column in used_columns:
                continue
            hard[row, column] = 1.0
            used_rows.add(row)
            used_columns.add(column)
            if len(used_rows) == size:
                break
        if len(used_rows) != size:
            raise RuntimeError("Kon geen volledige injectieve symboolcode construeren.")
        return hard


class MinimalPermutationSlotSender(InjectivePermutationSlotSender):
    """Injectieve lokale factoralfabetten op de exacte bronondergrens."""

    def __init__(self, spec: ModelSpec) -> None:
        nn.Module.__init__(self)
        if spec.message_length != len(spec.factor_sizes):
            raise ValueError(
                "Een minimale permutationslotzender vereist één slot per factor."
            )
        if spec.vocabulary_size < max(spec.factor_sizes):
            raise ValueError("Globale tokenruimte is kleiner dan een factoralfabet.")
        self.spec = spec
        self.binding_logits = nn.Parameter(
            torch.empty(spec.message_length, len(spec.factor_sizes))
        )
        self.codebook_logits = nn.ParameterList(
            [nn.Parameter(torch.empty(size, size)) for size in spec.factor_sizes]
        )
        nn.init.normal_(self.binding_logits, mean=0.0, std=0.05)
        for logits in self.codebook_logits:
            nn.init.normal_(logits, mean=0.0, std=0.05)
        matrices = []
        for permutation in permutations(range(len(spec.factor_sizes))):
            matrix = torch.zeros(spec.message_length, len(spec.factor_sizes))
            matrix[torch.arange(spec.message_length), torch.tensor(permutation)] = 1.0
            matrices.append(matrix)
        self.register_buffer("permutation_matrices", torch.stack(matrices))

    def forward(
        self,
        meanings: Tensor,
        *,
        temperature: float = 1.0,
        sample: bool = True,
    ) -> tuple[Tensor, Tensor]:
        del temperature, sample
        factor_codes = self._padded_factor_codes(meanings, relaxed=False)
        symbols = torch.einsum(
            "sf,bfv->bsv", self.binding_matrix(), factor_codes
        )
        return symbols, symbols.argmax(dim=-1)

    def relaxed_message(self, meanings: Tensor, *, temperature: float = 1.0) -> Tensor:
        if temperature <= 0:
            raise ValueError("Temperatuur moet positief zijn.")
        factor_codes = self._padded_factor_codes(
            meanings, relaxed=True, temperature=temperature
        )
        return torch.einsum(
            "sf,bfv->bsv", self.soft_binding_matrix(), factor_codes
        )

    def _padded_factor_codes(
        self,
        meanings: Tensor,
        *,
        relaxed: bool,
        temperature: float = 1.0,
    ) -> Tensor:
        codes = []
        for index, size in enumerate(self.spec.factor_sizes):
            matrix = (
                self.soft_codebook_matrix(index, temperature=temperature)
                if relaxed
                else self.codebook_matrix(index)
            )
            selected = matrix[meanings[:, index]]
            codes.append(F.pad(selected, (0, self.spec.vocabulary_size - size)))
        return torch.stack(codes, dim=1)

    def codebook_matrix(
        self, factor_index: int, *, straight_through: bool = True
    ) -> Tensor:
        soft = self.soft_codebook_matrix(factor_index)
        hard = self._greedy_permutation(soft.detach())
        if straight_through:
            return hard - soft.detach() + soft
        return hard


SenderModel = (
    Sender
    | LearnedPermutationSlotSender
    | InjectivePermutationSlotSender
    | MinimalPermutationSlotSender
)


def make_sender(spec: ModelSpec) -> SenderModel:
    if spec.sender_family == "categorical_encoder_autoregressive_sender":
        return Sender(spec)
    if spec.sender_family == "learned_permutation_slot_sender":
        return LearnedPermutationSlotSender(spec)
    if spec.sender_family == "injective_permutation_slot_sender":
        return InjectivePermutationSlotSender(spec)
    if spec.sender_family == "minimal_permutation_slot_sender":
        return MinimalPermutationSlotSender(spec)
    raise ValueError(f"Onbekende zenderarchitectuur: {spec.sender_family}")


class Receiver(nn.Module):
    """Ontvanger die uitsluitend een discrete symboolreeks naar factoren decodeert."""

    def __init__(self, spec: ModelSpec) -> None:
        super().__init__()
        self.spec = spec
        self.symbol_embedding = nn.Embedding(
            spec.vocabulary_size, spec.symbol_embedding_dim
        )
        self.recurrent = nn.GRU(
            input_size=spec.symbol_embedding_dim,
            hidden_size=spec.hidden_dim,
            batch_first=True,
        )
        self.factor_heads = nn.ModuleList(
            nn.Linear(spec.hidden_dim, size) for size in spec.factor_sizes
        )

    def forward(self, message: Tensor) -> tuple[Tensor, ...]:
        if message.ndim == 2:
            embedded = self.symbol_embedding(message)
        elif message.ndim == 3:
            embedded = message @ self.symbol_embedding.weight
        else:
            raise ValueError("Bericht moet [batch,lengte] of [batch,lengte,vocab] zijn.")
        _, hidden = self.recurrent(embedded)
        representation = hidden[-1]
        return tuple(head(representation) for head in self.factor_heads)


class FactorizedPermutationSlotReceiver(nn.Module):
    """Decodeert iedere factor uit exact één vrij gekozen berichtslot."""

    def __init__(self, spec: ModelSpec) -> None:
        super().__init__()
        if spec.message_length != len(spec.factor_sizes):
            raise ValueError(
                "Een factorontvanger vereist één berichtslot per factor."
            )
        self.spec = spec
        self.symbol_embedding = nn.Embedding(
            spec.vocabulary_size, spec.symbol_embedding_dim
        )
        self.binding_logits = nn.Parameter(
            torch.empty(len(spec.factor_sizes), spec.message_length)
        )
        self.factor_heads = nn.ModuleList(
            nn.Linear(spec.symbol_embedding_dim, size)
            for size in spec.factor_sizes
        )
        nn.init.normal_(self.binding_logits, mean=0.0, std=0.05)
        matrices = []
        for permutation in permutations(range(spec.message_length)):
            matrix = torch.zeros(len(spec.factor_sizes), spec.message_length)
            matrix[torch.arange(len(spec.factor_sizes)), torch.tensor(permutation)] = 1.0
            matrices.append(matrix)
        self.register_buffer("permutation_matrices", torch.stack(matrices))

    def forward(self, message: Tensor) -> tuple[Tensor, ...]:
        if message.ndim == 2:
            embedded = self.symbol_embedding(message)
        elif message.ndim == 3:
            embedded = message @ self.symbol_embedding.weight
        else:
            raise ValueError("Bericht moet [batch,lengte] of [batch,lengte,vocab] zijn.")
        factors = torch.einsum("fs,bse->bfe", self.binding_matrix(), embedded)
        return tuple(
            head(factors[:, index])
            for index, head in enumerate(self.factor_heads)
        )

    def binding_matrix(self, *, straight_through: bool = True) -> Tensor:
        soft = self.soft_binding_matrix()
        scores = torch.einsum(
            "pfs,fs->p", self.permutation_matrices, self.binding_logits
        )
        hard = self.permutation_matrices[scores.argmax()]
        if straight_through:
            return hard - soft.detach() + soft
        return hard

    def soft_binding_matrix(self) -> Tensor:
        return InjectivePermutationSlotSender._sinkhorn(self.binding_logits)


ReceiverModel = Receiver | FactorizedPermutationSlotReceiver


def make_receiver(spec: ModelSpec) -> ReceiverModel:
    if spec.receiver_family == "sequence_encoder_multihead_classifier":
        return Receiver(spec)
    if spec.receiver_family == "factorized_permutation_slot_receiver":
        return FactorizedPermutationSlotReceiver(spec)
    raise ValueError(f"Onbekende ontvangerarchitectuur: {spec.receiver_family}")


class CommunicationSystem(nn.Module):
    def __init__(self, spec: ModelSpec) -> None:
        super().__init__()
        self.sender = make_sender(spec)
        self.receiver = make_receiver(spec)

    def forward(
        self, meanings: Tensor, *, temperature: float
    ) -> tuple[tuple[Tensor, ...], Tensor]:
        message, tokens = self.sender(meanings, temperature=temperature, sample=True)
        return self.receiver(message), tokens


class PopulationSystem(nn.Module):
    """Volledig onafhankelijke zenders en ontvangers met één gedeeld kanaal."""

    def __init__(self, spec: ModelSpec, *, sender_count: int, receiver_count: int) -> None:
        super().__init__()
        if sender_count < 2 or receiver_count < 2:
            raise ValueError("Een populatie vereist minstens twee zenders en ontvangers.")
        self.spec = spec
        self.senders = nn.ModuleList(make_sender(spec) for _ in range(sender_count))
        self.receivers = nn.ModuleList(
            make_receiver(spec) for _ in range(receiver_count)
        )

    def forward_pair(
        self,
        meanings: Tensor,
        *,
        sender_index: int,
        receiver_index: int,
        temperature: float,
    ) -> tuple[tuple[Tensor, ...], Tensor]:
        message, tokens = self.senders[sender_index](
            meanings, temperature=temperature, sample=True
        )
        return self.receivers[receiver_index](message), tokens


def save_agent_checkpoint(
    path: str | Path,
    agent: SenderModel | ReceiverModel,
    *,
    kind: str,
) -> None:
    if kind not in {"sender", "receiver", "translator"}:
        raise ValueError(f"Onbekend agenttype: {kind}")
    payload = {
        "format_version": 1,
        "kind": kind,
        "model_spec": asdict(agent.spec),
        "state_dict": {key: value.detach().cpu() for key, value in agent.state_dict().items()},
    }
    torch.save(payload, Path(path))


def load_agent_checkpoint(
    path: str | Path, *, expected_kind: str | None = None, device: str = "cpu"
) -> SenderModel | ReceiverModel:
    payload = torch.load(Path(path), map_location=device, weights_only=True)
    kind = payload["kind"]
    if expected_kind is not None and kind != expected_kind:
        raise ValueError(f"Checkpoint bevat {kind}, verwacht {expected_kind}.")
    spec = ModelSpec.from_dict(payload["model_spec"])
    agent: SenderModel | ReceiverModel
    if kind == "sender":
        agent = make_sender(spec)
    elif kind in {"receiver", "translator"}:
        agent = make_receiver(spec)
    else:
        raise ValueError(f"Checkpoint bevat onbekend agenttype: {kind}")
    agent.load_state_dict(payload["state_dict"])
    agent.to(device)
    agent.eval()
    return agent
