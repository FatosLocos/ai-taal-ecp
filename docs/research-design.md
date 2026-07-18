# Research design: emergent AI communication

Version: 0.2<br>
Date: July 17, 2026<br>
First experiment: ECP-0

## 1. Goal

This research tests whether AI agents can develop a communication protocol under controlled conditions that:

- transmits information reliably;
- is more compact than human text representations;
- can describe new combinations;
- can be reconstructed by an independent translator;
- can be learned by agents outside the original training pair;
- remains controllable because all communication runs through one measurable channel.

The research distinguishes between a **code** and a **language-like protocol**. A code can give any complete meaning an arbitrary number. A language-like protocol reuses parts or structures and can therefore compose unknown meanings.

## 2. Central research question

> Can independently trained AI agents themselves develop a communication protocol that is more efficient, clearer and more systematic than human language, given the same task performance?

### Subquestions

1. Can a reliable discrete protocol be created without human words?
2. Does this protocol generalize to never trained combinations?
3. Can the internal structure be explained systematically afterwards?
4. Can an independent translator unlock the messages correctly?
5. Can a new receiver learn the protocol without co-adapting with the original sender?
6. How does the protocol change under the pressure of message costs, noise, context and more complex reasoning tasks?

## 3. Operational definitions

### New

The meaning of individual symbols and symbol sequences has not been determined by a human. Only the task, world and channel capacity are designed.

### Efficient

A protocol focuses more favorably on the trade-off between task performance and costs. Costs are measured primarily in bits actually sent; latency, computation costs and error sensitivity are reported separately.

### Clear

The receiver reproducibly arrives at the intended meaning of the same message, even with unseen combinations and limited noise.

### Translatable

An independent model, which has not been trained with the agents, can convert a frozen message to its canonical meaning and then to Dutch.

### Transferable

A new receiver can learn to communicate with the frozen original sender with a limited number of examples.

### Completely efficient

This is not used as an absolute property. Efficiency only exists with respect to load balancing, channel, fault tolerance and hardware. Step 3 therefore looks for a Pareto front instead of one universal optimum.

## 4. Predetermined hypotheses

- **H1 — Reliability:** at least four of five ECP-0 runs achieve 99% exact reconstruction on known meanings.
- **H2 — Combinatorial generalization:** a learned protocol clearly outperforms a non-compositional lookup baseline on withheld color-shape pairs.
- **H3 — Translatability:** an independent translator generalizes above the lookup baseline to the same withheld pairs.
- **H4 — Structure:** meaning distance and message distance show more correlation than with randomly permuted messages.
- **H5 — Transfer:** in step 2, a new receiver learns the frozen protocol with fewer examples than a completely new protocol.
- **H6 — Efficiency:** in step 2, a bit penalty reduces the average message length without falling below a predetermined performance threshold.

A negative result is a valid result. Thresholds should not be adjusted retroactively after reviewing test results.

## 5. Step 1 — ECP-0: translatable base

### 5.1 Artificial world

Every meaning is the Cartesian product of four factors:

| Factor | Number of values | Internal representation |
|---|---:|---|
| color | 8 | `c0` to `c7` |
| shape | 8 | `s0` to `s7` |
| size | 4 | `z0` to `z3` |
| texture | 4 | `t0` to `t3` |

This yields 1024 unique meanings. Human labels may exist for visualization, but are never used as model input.

The source is uniformly distributed. As a result, error-free identification requires at least `log2(1024) = 10` bits of information.

### 5.2 Communication task

1. The sender receives one meaning as four categorical factors.
2. The sender produces exactly four symbols.
3. The receiver only sees those four symbols.
4. The receiver predicts all four factors.
5. An episode is only exactly correct if all four factors are correct.

The channel contains 16 possible symbols. So one symbol costs 4 bits and each ECP-0 message costs exactly 16 bits. The symbols have no meaning at first. ECP-0.2 uses this extra space to first test learnability and translatability; compression to three symbols/12 bits is explored in step 2.

### 5.3 Agents

- Both agents are trained from random initialization.
- They use separate weights, embeddings and random seeds.
- They receive no pre-trained language model and no natural language as input.
- A straight-through Gumbel-Softmax estimate may be used during training.
- Only hard integer symbol IDs are sent during validation and testing.
- For the final evaluation, the sender and receiver run as logically separate processes.

Transmitting gradients during training is a learning signal, not an evaluation channel. All conclusions are based solely on discrete evaluation.

### 5.4 Data splitting

The split is generated deterministically before training:

1. Create a random one-to-one matching between the eight colors and eight shapes using the recorded data-split seed. Each color and shape appears exactly once in a held-out pair.
2. Retain all 16 combinations of size and texture for each pair.
3. This forms a compositional test set of 128 meanings.
4. Select a stratified development set of 128 meanings from the remaining 896 meanings.
5. The remaining 768 meanings form the training set.

Every atomic value appears in training. Only specific combinations are missing. The test set remains sealed until model and hyperparameter choices are finalized.

### 5.5 Freeze and translate

After training, the sender and receiver are frozen. Then a third model is trained:

- input: the discrete message only;
- output: the four canonical factors;
- training: only messages from the training split;
- evaluation: the development set and then the compositional test set once.

A Dutch renderer deterministically converts the predicted factors into readable text. The renderer does not count as an intelligent translator; performance is measured on the predicted canonical factors.

### 5.6 Baselines

| Baseline | Function |
|---|---|
| Dutch template | Comparison with human readability and UTF-8 size |
| Canonical JSON | Comparison with common machine communication |
| Manually packed factor code, 10 bits | Domain-specific technical lower bound |
| Random Lookup Code | High known-set performance without compositionality |
| Manual compositional factor code | Check for maximum explicit structure |

The comparison with Dutch and JSON is about message size, not about overall expressiveness. The 10-bit factor code prevents the incorrect claim that a learned protocol can beat any designed binary representation.

### 5.7 Primary measurements

- exact reconstruction accuracy;
- accuracy per factor;
- performance on known and withheld meanings;
- actual number of channel bits;
- message entropy and number of unique messages;
- collisions: different meanings with the same message;
- topographic similarity between meaning and message distance;
- minimal pair analysis and symbol ablation;
- independent translation accuracy;
- spread across five training seeds;
- training and inference latency, as a secondary measure only.

No single structural measure can be taken separately as evidence for compositionality. The conclusion combines generalization, translation, minimal pairs, ablations, and comparison with controls.

### 5.8 Checks against false success

- **Message shuffling:** exact reconstruction should drop to approximately chance level.
- **Consistent symbol permutation:** performance should remain the same if symbol IDs are renamed identically on both sides.
- **Channel Isolation:** Receiver does not receive episode ID, meaning ID, clock time, shared memory, or file channel.
- **No shared state:** models do not share weights, cache, random generator, or hidden activations during evaluation.
- **Full logging:** every message, response, model hash, config hash and seed is saved.
- **Hard quantization:** conclusions are not based on continuous, indefinitely precise vectors.
- **Test seal:** the compositional test set does not influence model selection.

### 5.9 Classification of the outcome

Step 1 is methodologically completed when all five preset runs, baselines, and checks have been performed. The outcome is then classified as follows:

- **Strong evidence:** at least four runs get 99% on known meanings, 90% on the compositional test and 85% independent translation on that test.
- **Mixed evidence:** known meanings reach 99%, but generalization or translation is between lookup level and the strong threshold.
- **Negative result:** the agents do not learn a reliable channel, or generalization and translation are not meaningfully different from the lookup check.
- **Invalid run:** a check failed, a side channel is possible or the predefined configuration has been changed without registration.

These percentages are research thresholds, not a guarantee that ECP-0 will achieve them.

## 6. Step 2 — Refinement and Evolution

Step 2 only builds on a frozen report from Step 1. New hypotheses and configurations are pre-registered.

Planned extensions:

- variable message length from one to six symbols;
- full bit accounting, including length information;
- information pressure via an explicit bit penalty;
- noise due to symbol loss, replacement and swapping;
- context in which irrelevant properties can be safely omitted;
- relationships between multiple objects;
- populations of multiple senders and receivers;
- periodic replacement by newly initialized agents;
- transmission testing with a frozen sender or receiver;
- comparison between joint training and iterative learning across generations.

The core question here shifts from “can it communicate?” to “does the protocol remain efficient, learnable and robust when the environment changes?”

## 7. Step 3 — Efficiency and complex reasoning

Step 3 introduces more complex meanings and multiple channel forms:

- hierarchical concepts;
- object-relationship graphs;
- time, uncertainty, intention and conditional actions;
- abstract reasoning rules instead of only visible features;
- discrete sequences, typed graphs and quantized vectors;
- task transfer to an environment where the protocol has not been trained.

Continuous vectors are always quantized to a predetermined number of bits. Otherwise a fair efficiency comparison is impossible.

The outcome is reported as a Pareto front on:

1. task performance;
2. sent bits;
3. robustness;
4. generalization;
5. translatability;
6. portability;
7. latency and computation costs.

## 8. Reproducibility and reporting

Each run receives an unchangeable run ID and contains at least:

- full configuration;
- software and hardware versions;
- dataset manifest and hashes;
- model initialization seeds;
- checkpoints and model hashes;
- raw episode messages and predictions;
- calculated metrics;
- registered deviations from the protocol;
- automatic and human summarized result.

Failed runs are not deleted. A change after result inspection starts a new experiment version.

## 9. Limits of interpretation

A positive result shows an efficient emergent protocol in the tested world. It does not prove that:

- the protocol is a general alternative to human language;
- agents have deliberately designed a language;
- the same structure arises spontaneously in large language models;
- communication outside the experimental task remains efficient;
- incomprehensibility in itself demonstrates intelligence or semantic depth.

## 10. Research base

The design is in line with previous research into emergent communication:

- [Natural Language Does Not Emerge 'Naturally' in Multi-Agent Dialog](https://aclanthology.org/D17-1321/) — successful task performance does not guarantee interpretable or compositional language.
- [Emergent Communication: Generalization and Overfitting in Lewis Games](https://proceedings.neurips.cc/paper_files/paper/2022/hash/093b08a7ad6e6dd8d34b9cc86bb5f07c-Abstract-Conference.html) — co-adaptation and overfitting can undermine generalization.
- [Trading off Utility, Informativeness, and Complexity in Emergent Communication](https://proceedings.neurips.cc/paper_files/paper/2022/hash/8bb5f66371c7e4cbf6c223162c62c0f4-Abstract-Conference.html) — information value and protocol complexity should be measured together.
- [Emergent Communication for Rules Reasoning](https://proceedings.neurips.cc/paper_files/paper/2023/hash/d8ace30c68b085556ccce04ed4ae4ebb-Abstract-Conference.html) — more complex reasoning tasks can encourage more structural protocols.
- [A Compressive-Expressive Communication Framework for Compositional Representations](https://proceedings.neurips.cc/paper_files/paper/2025/hash/3310034c97fab48fdbcba18f90fd5364-Abstract-Conference.html) — compressive pressure and iterative learning can support efficiency and compositionality.
