# Development log ECP-1

All variants below used only training and validation data. The new ECP-1 test split remained sealed during these design choices.

| Variant | Pairings per step | Known mean | Known worst | Validation mean | Conclusion |
|---|---:|---:|---:|---:|---|
| One pair at random | 1 | 92.7% | 91.4% | 61.2% | too few direct pair updates |
| B: one sender, all receivers | 4 | 95.9% | 95.1% | 57.3% | more stable, but known accuracy is insufficient |
| C: all senders, all receivers | 16 | 99.2% | 98.8% | 77.6% | frozen for the confirmatory experiment |

## Variant A

Each cycle used all sixteen pairs once, but only one pair per training step. At the best checkpoint each specific pair had only a fraction of the learning interactions of an ECP-0 pair. The agents did develop a shared convention, but the known reconstruction remained insufficient.

Local, untracked artifact: `runs/20260718T000531Z-ecp1-development/report.md`.

## Variant B

One selected sender sent the same message per step to all four receivers, giving receivers a lot of experience, but each sender still less direct updates. The known performance improved, while validation did not improve.

Local, untracked artifact: `runs/20260718T000811Z-ecp1-development/report.md`.

## Variant C

Each batch ran through all sixteen sender-receiver pairs, and all losses were averaged. There was no leader, shared weight, or extra semantic label. Each pair received the same amount of training exposure as ECP-0.

The universal receiver achieved test-free 78.3% validation. A fresh receiver achieved 74.2% validation with 512 out of 768 training concepts and 77.9% with all meanings.

Local, untracked artifact: `runs/20260718T001224Z-ecp1-development/report.md`.

After this run, architecture, learning settings, thresholds and data split have been frozen. Subsequent changes will get a new experiment ID.
