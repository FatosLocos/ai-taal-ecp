# Ontwikkellog ECP-5

De ECP-5-testset bleef gedurende ontwikkeling gesloten.

## Oorzaakanalyse ECP-4

Alle vijf 10-bitpopulaties communiceerden foutloos. Vier universele vertalers bleven echter steken op 9,4–12,5%. Hun symboolkoppen waren niet het probleem: de harde ontvangerbinding wees factoren aan de verkeerde slots toe. Dezelfde fout trad ook tweemaal op in de 16-bitcontrole.

## Exacte kalibratie

De nieuwe procedure berekent een `4×4`-matrix met empirische wederzijdse informatie en scoort alle 24 permutaties. Een test met een verborgen synthetische slotvolgorde vindt de exacte inverse binding terug en bevriest haar. Alle 35 tests slagen.

## Gesloten ontwikkelrun

Run: `runs/ecp5-development-final/20260718T062526Z-ecp5-development`  
Seed: 11

| Metriek | Uitkomst |
|---|---:|
| Populatie bekend | 100% |
| Slechtste bekend paar | 100% |
| Nieuwe grootte-textuurvalidatie | 100% |
| Slechtste validatiepaar | 100% |
| Gekalibreerde universele vertaler | 100% |
| Nieuwe ontvanger met 32 voorbeelden | 100% |
| Nieuwe ontvanger met 128 voorbeelden | 100% |
| Nieuwe ontvanger met 256 voorbeelden | 100% |
| Nieuwe ontvanger met 512 voorbeelden | 100% |

De gekozen slotvolgorde per factor was `[2,3,0,1]`. De totale wederzijdse-informatiescore was exact 10,0 bits; de eerstvolgende permutatie scoorde 8,0 bits. De keuze is daardoor niet marginaal. Ook met slechts 32 voorbeelden bleef de juiste permutatie de duidelijke winnaar.

## Besluit

De kalibratie is zonder verdere varianten bevroren. De controle schakelt uitsluitend `binding_calibration.enabled` uit. Geen ECP-5-testpaar is vóór deze keuze geëvalueerd.
