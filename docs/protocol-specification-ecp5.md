# Protocol specification ECP-5

## Logical message

A meaning consists of four categorical factors with cardinalities `8,8,4,4`. A message contains four local symbols. The protocol contains two stable conventions per seed:

1. a permutation of factors to message slots;
2. per factor a permutation of values to local symbols.

These conventions are part of the frozen protocol and are not included in every message, just as the grammar and lexicon of a human language are not repeated in every sentence.

## Wire format

The number of bits required for each slot follows from the factor binding:

- color or shape: 3 bits;
- size or texture: 2 bits.

The four local symbols are concatenated as unsigned bit fields in slot order. The total length is always 10 bits. No padding, terminator, or length field is required.

For seed 11:

- slot factors: `[size, texture, color, shape]`;
- message: `[0,3,5,4]`;
- bitfields: `00 | 11 | 101 | 100`;
- wire: `0011101100`.

## Decoding

An existing receiver keeps the inverse factor slot permutation in its checkpoint. A new reader gets labeled training examples and:

1. calculates the empirical mutual information for each factor-slot combination;
2. scores all 24 one-to-one permutations;
3. freezes the best binding;
4. learns only the local symbol permutation for each factor.

The receiver cannot use information from unselected slots, so it cannot memorize a context rule between factors.

## Invariants

- exactly four logical symbols;
- exactly 10 wire bits;
- exactly one factor per slot and one slot per factor;
- each factor codebook is a hard permutation;
- no two meanings share a message;
- changing one factor changes exactly one slot;
- consistent renaming within the protocol does not change semantics.

## Protocol extension

New values can be added only if the local alphabet still has capacity or is renegotiated. A completely new factor requires a new slot and wire version. ECP-5 optimizes a closed factor schema; dynamic schema evolution is outside the scope of this version.
