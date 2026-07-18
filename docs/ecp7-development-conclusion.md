# ECP-7 Sealed Development Conclusion

Status: **development closed; confirmatory test never accessed**<br>
Closed: July 18, 2026<br>
Completed variants: ECP7-B1-I through ECP7-B29-I

## Conclusion

ECP-7 asked whether the 14-bit, 16,384-meaning ECP-6 result would survive when
the explicit one-factor-per-slot sender and receiver bias was weakened. No
development variant passed the full preregistered gate. Therefore no frozen
`config/ecp7.yaml` exists and no confirmatory ECP-7 experiment was run.

The strongest weak-structure family used a bounded parallel sender and a
position-aware MLP receiver. Batch 25 reached 85.26% train, 85.24% validation,
82.71% worst-link validation and 85.13% universal-translator validation. Batch
26 reached the highest mean validation at 85.38%, but did not improve hard-code
capacity. Every strong variant remained non-injective and below the 97% mean
and 95% worst-link train thresholds.

## What the development series established

1. A generic weak-structure sender-receiver pair can learn a compact,
   translatable protocol far above chance without semantic symbol assignments.
2. The position-aware receiver removes a major recurrent decoding bottleneck.
3. Receiver-only catch-up can approach the mathematical ceiling of an existing
   non-injective sender codebook, but cannot raise that ceiling.
4. Sender-only and route-cycled ordinary-task replay redistribute shared errors
   into link-specific errors instead of creating new codes.
5. Direct relaxed collision-pair pressure reduces collision multiplicity and
   increases entropy, but does not increase the number of occupied hard codes.
6. Generic extra sender depth promotes training-relation memorization and
   destroys compositional validation, even with exact identity and RNG-
   equivalent initialization.
7. Activating that residual capacity only after the successful shallow
   trajectory still reduces code capacity and worst-link validation.

## Scientific boundary

ECP-7 is a negative development result, not a failed confirmatory experiment.
The sealed test contains no published metric because it was never opened. This
prevents repeated development choices from leaking into confirmatory evidence.

ECP-6 remains the latest confirmed result: its fully factorized architecture
learns a lossless, transferable and information-theoretically minimal protocol
inside the synthetic product world. ECP-7 shows that this result does not yet
survive the tested weakening of that architectural bias.

## Next research phase

Do not add ECP7-B30. A future ECP-8 must start with a new question and fresh
preregistration. It should explicitly choose whether to study learned
compositional structure, variable-length efficiency, interactive negotiation,
or transfer across altered worlds. Those are different hypotheses and must not
be combined in one development batch.

Full per-batch preregistrations, metrics, decisions and artifact identities are
in [`development-log-ecp7.md`](development-log-ecp7.md), with compact manifests
under [`../evidence/ecp7-development/`](../evidence/ecp7-development/).
