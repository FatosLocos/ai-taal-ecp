"""Sender, receiver, and safe independent checkpoints for ECP."""

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
    slot_alphabet_sizes: tuple[int, ...] = ()
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
            slot_alphabet_sizes=tuple(
                channel.get("slot_alphabet_sizes")
                or channel.get("factor_alphabet_sizes")
                or [channel["vocabulary_size"]] * channel["message_length"]
            ),
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
            slot_alphabet_sizes=tuple(
                value.get("slot_alphabet_sizes")
                or [value["vocabulary_size"]] * value["message_length"]
            ),
            sender_family=value.get(
                "sender_family", "categorical_encoder_autoregressive_sender"
            ),
            receiver_family=value.get(
                "receiver_family", "sequence_encoder_multihead_classifier"
            ),
        )


class Sender(nn.Module):
    """Autoregressive sender that maps factor categories to discrete symbols."""

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
        """Return deterministic symbol distributions for structural training pressure.

        This path transmits nothing during evaluation. It only exposes how the
        sender distributes probability mass over the existing discrete channel,
        without Gumbel noise or preassigned symbol semantics.
        """
        if temperature <= 0:
            raise ValueError("Temperature must be positive.")
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


class BoundedAutoregressiveSender(nn.Module):
    """Joint sender constrained only by each message slot's symbol capacity.

    Every slot is generated from a shared representation of all meaning factors.
    Unlike the permutation-slot senders, this architecture has no factor-slot
    binding, factor-specific message head, or factor-local codebook.
    """

    def __init__(self, spec: ModelSpec) -> None:
        super().__init__()
        if len(spec.slot_alphabet_sizes) != spec.message_length:
            raise ValueError(
                "A bounded autoregressive sender requires one alphabet size per slot."
            )
        if any(
            size < 2 or size > spec.vocabulary_size
            for size in spec.slot_alphabet_sizes
        ):
            raise ValueError(
                "Every slot alphabet must fit within the global token space."
            )
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
        self.slot_heads = nn.ModuleList(
            nn.Linear(spec.hidden_dim, alphabet_size)
            for alphabet_size in spec.slot_alphabet_sizes
        )
        nn.init.normal_(self.start_embedding, mean=0.0, std=0.02)

    def _context(self, meanings: Tensor) -> Tensor:
        embedded_factors = [
            embedding(meanings[:, index])
            for index, embedding in enumerate(self.factor_embeddings)
        ]
        return torch.tanh(
            self.context_projection(torch.cat(embedded_factors, dim=-1))
        )

    def forward(
        self,
        meanings: Tensor,
        *,
        temperature: float = 1.0,
        sample: bool = True,
    ) -> tuple[Tensor, Tensor]:
        if temperature <= 0:
            raise ValueError("Temperature must be positive.")
        context = self._context(meanings)
        hidden = context
        previous = self.start_embedding.unsqueeze(0).expand(meanings.shape[0], -1)
        padded_symbols: list[Tensor] = []
        tokens: list[Tensor] = []
        for head, alphabet_size in zip(
            self.slot_heads, self.spec.slot_alphabet_sizes, strict=True
        ):
            hidden = self.recurrent(torch.cat((previous, context), dim=-1), hidden)
            logits = head(hidden)
            if sample:
                local_symbol = F.gumbel_softmax(
                    logits, tau=temperature, hard=True, dim=-1
                )
            else:
                token = logits.argmax(dim=-1)
                local_symbol = F.one_hot(token, alphabet_size).to(logits.dtype)
            token = local_symbol.argmax(dim=-1)
            symbol = F.pad(
                local_symbol, (0, self.spec.vocabulary_size - alphabet_size)
            )
            padded_symbols.append(symbol)
            tokens.append(token)
            previous = symbol @ self.symbol_embedding.weight
        return torch.stack(padded_symbols, dim=1), torch.stack(tokens, dim=1)

    def relaxed_message(self, meanings: Tensor, *, temperature: float = 1.0) -> Tensor:
        if temperature <= 0:
            raise ValueError("Temperature must be positive.")
        context = self._context(meanings)
        hidden = context
        previous = self.start_embedding.unsqueeze(0).expand(meanings.shape[0], -1)
        distributions: list[Tensor] = []
        for head, alphabet_size in zip(
            self.slot_heads, self.spec.slot_alphabet_sizes, strict=True
        ):
            hidden = self.recurrent(torch.cat((previous, context), dim=-1), hidden)
            local_distribution = torch.softmax(head(hidden) / temperature, dim=-1)
            distribution = F.pad(
                local_distribution,
                (0, self.spec.vocabulary_size - alphabet_size),
            )
            distributions.append(distribution)
            previous = distribution @ self.symbol_embedding.weight
        return torch.stack(distributions, dim=1)


class LearnedPermutationSlotSender(nn.Module):
    """Compositional slots whose factor-slot binding is selected internally."""

    def __init__(self, spec: ModelSpec) -> None:
        super().__init__()
        if spec.message_length != len(spec.factor_sizes):
            raise ValueError(
                "A permutation-slot sender requires one slot per meaning factor."
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
            raise ValueError("Temperature must be positive.")
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
    """Freely learned slots and injective atomic codes without semantic labels.

    Every factor selects exactly one slot. Within a factor, every value receives
    a distinct symbol. The hard assignments are constrained structurally only;
    no slot or symbol receives a human meaning in advance.
    """

    def __init__(self, spec: ModelSpec) -> None:
        super().__init__()
        if spec.message_length != len(spec.factor_sizes):
            raise ValueError(
                "An injective permutation-slot sender requires one slot per factor."
            )
        if any(size > spec.vocabulary_size for size in spec.factor_sizes):
            raise ValueError(
                "Injective atomic codes require at least as many symbols as values."
            )
        self.spec = spec
        self.binding_logits = nn.Parameter(
            torch.empty(spec.message_length, len(spec.factor_sizes))
        )
        # Square matrices contain dummy rows in addition to real factor values.
        # This lets Sinkhorn learn a complete permutation while only the first
        # `factor_size` rows are actually transmitted.
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
            raise ValueError("Temperature must be positive.")
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
        """Return the real value rows of a hard one-to-one symbol code."""
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
            raise ValueError("Temperature must be positive.")
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
        """Deterministic hard permutation; gradients flow through Sinkhorn."""
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
            raise RuntimeError("Could not construct a complete injective symbol code.")
        return hard


class MinimalPermutationSlotSender(InjectivePermutationSlotSender):
    """Injective factor-local alphabets at the exact source lower bound."""

    def __init__(self, spec: ModelSpec) -> None:
        nn.Module.__init__(self)
        if spec.message_length != len(spec.factor_sizes):
            raise ValueError(
                "A minimal permutation-slot sender requires one slot per factor."
            )
        if spec.vocabulary_size < max(spec.factor_sizes):
            raise ValueError("Global token space is smaller than a factor alphabet.")
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
            raise ValueError("Temperature must be positive.")
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
    | BoundedAutoregressiveSender
    | LearnedPermutationSlotSender
    | InjectivePermutationSlotSender
    | MinimalPermutationSlotSender
)


def make_sender(spec: ModelSpec) -> SenderModel:
    if spec.sender_family == "categorical_encoder_autoregressive_sender":
        return Sender(spec)
    if spec.sender_family == "bounded_autoregressive_sender":
        return BoundedAutoregressiveSender(spec)
    if spec.sender_family == "learned_permutation_slot_sender":
        return LearnedPermutationSlotSender(spec)
    if spec.sender_family == "injective_permutation_slot_sender":
        return InjectivePermutationSlotSender(spec)
    if spec.sender_family == "minimal_permutation_slot_sender":
        return MinimalPermutationSlotSender(spec)
    raise ValueError(f"Unknown sender architecture: {spec.sender_family}")


class Receiver(nn.Module):
    """Receiver that decodes only a discrete symbol sequence into factors."""

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
            raise ValueError("Message must have shape [batch,length] or [batch,length,vocab].")
        _, hidden = self.recurrent(embedded)
        representation = hidden[-1]
        return tuple(head(representation) for head in self.factor_heads)


class FactorizedPermutationSlotReceiver(nn.Module):
    """Decode each factor from exactly one freely selected message slot."""

    def __init__(self, spec: ModelSpec) -> None:
        super().__init__()
        if spec.message_length != len(spec.factor_sizes):
            raise ValueError(
                "A factorized receiver requires one message slot per factor."
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
            raise ValueError("Message must have shape [batch,length] or [batch,length,vocab].")
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
    raise ValueError(f"Unknown receiver architecture: {spec.receiver_family}")


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
    """Fully independent senders and receivers with one shared channel."""

    def __init__(self, spec: ModelSpec, *, sender_count: int, receiver_count: int) -> None:
        super().__init__()
        if sender_count < 2 or receiver_count < 2:
            raise ValueError("A population requires at least two senders and two receivers.")
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
        raise ValueError(f"Unknown agent type: {kind}")
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
        raise ValueError(f"Checkpoint contains {kind}; expected {expected_kind}.")
    spec = ModelSpec.from_dict(payload["model_spec"])
    agent: SenderModel | ReceiverModel
    if kind == "sender":
        agent = make_sender(spec)
    elif kind in {"receiver", "translator"}:
        agent = make_receiver(spec)
    else:
        raise ValueError(f"Checkpoint contains unknown agent type: {kind}")
    agent.load_state_dict(payload["state_dict"])
    agent.to(device)
    agent.eval()
    return agent
