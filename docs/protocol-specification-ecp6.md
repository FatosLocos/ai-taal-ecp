# Protocol specification ECP-6

## Purpose and scope

ECP-6 encodes exactly one meaning from a closed product space of four categorical factors. It is not a text language and does not use an alphabet, words, or grammatical phrases. Its communication form is a structured tuple of four local integers plus a shared protocol convention.

The factor cardinalities are:

`color:16 × shape:16 × size:8 × texture:8 = 16,384`.

## Logical message

A message is a tuple `⟦a · b · c · d⟧`. Two conventions apply to each protocol instance:

1. a permutation linking each factor to exactly one slot;
2. for each factor, a bijection between factor values and local symbols.

The senders learn these conventions during training; they do not transmit them with every message. Within each confirmatory seed, all four channels converge on exactly the same convention. Across different seeds, the meanings of slots and symbols may differ.

## Wire format

The local alphabet size determines the bit width:

- color and shape: 4 bits each;
- size and texture: 3 bits each.

The four unsigned bit fields are concatenated in learned slot order without padding. The total message length is always:

`4 + 4 + 3 + 3 = 14 bits`.

Because there are `2^14` equiprobable meanings, this is exactly the lower bound for any lossless fixed-length code.

## Concrete example

In confirmatory seed 11, the slot order is:

`[shape, color, texture, size]`.

The test meaning never offered as a training combination `(c0,s9,z0,t0)` gets the logical message:

`⟦15 · 1 · 3 · 1⟧`.

The wire representation is:

`1111 | 0001 | 011 | 001` → `11110001011001`.

These bits are not intrinsically tied to `c0`, `s9`, `z0`, or `t0`. Their meaning exists only within the codebook and the learned convention.

## Decoding by an existing receiver

An existing receiver preserves the inverse slot permutation and four local symbol decoders. It:

1. splits the 14 bits according to the factor width of each slot;
2. converts each bit field to a local symbol;
3. routes each slot to its factor;
4. applies the corresponding inverse symbol permutation.

Factorized architecture cannot use information from another slot for a factor.

## Induction by a new reader

A new reader receives labeled training examples, but no sender parameters or codebooks. It:

1. calculates empirical mutual information for each factor-slot combination;
2. exhaustively scores all 24 possible slot permutations;
3. freezes the best-scoring binding;
4. learns the local symbol permutation for each factor.

In all five confirmatory seeds, the correct binding scored 14.0 bits and the runner-up scored 8.0 bits. From 128 labeled examples, every new reader decoded the complete test set flawlessly.

## Invariants

- exactly four logical symbols;
- exactly 14 wire bits;
- local alphabets `[16,16,8,8]` linked to the factor assigned to each slot;
- each factor uses exactly one slot;
- each local codebook is bijective;
- all 16,384 meanings have a unique message;
- changing one factor changes exactly one slot;
- consistent renaming of symbols with the corresponding decoder retains all predictions.

## Boundaries and version management

ECP-6 assumes that the schema, factor cardinalities, and protocol version are known in advance. Values beyond local-alphabet capacity, new factors, variable length, error correction, and dynamic protocol negotiation require a new version. The 14 bits measure only the payload within this shared closed schema; transport headers and one-time convention-learning costs are not included.
