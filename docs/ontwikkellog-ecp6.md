# Ontwikkellog ECP-6

De ECP-6-testset bleef gedurende alle onderstaande werkzaamheden gesloten.

## Schaalinvarianten

De code is gegeneraliseerd van de oorspronkelijke factoromvang `[8,8,4,4]` naar `[16,16,8,8]`. Configuratievalidatie, betekenis-ID's, schemas, factorlokale alfabetten en baselines volgen nu de feitelijke factoromvang. De volledige testsuite telt 39 geslaagde tests.

De eerste smoke-poging bracht één meetkundig schaalprobleem aan het licht: topografische gelijkenis materialiseerde alle `n(n-1)/2` paren. De poging is vóór voltooiing afgebroken, zonder testtoegang. De meting gebruikt nu maximaal 1.000.000 deterministisch en uniform bemonsterde paren. Een tweede smoke-run voltooide normaal en logde uitsluitend validatie.

## Gesloten ontwikkelrun

Run: `runs/20260718T065639Z-ecp6-development`  
Seed: 11  
Test ontzegeld: nee

| Metriek | Uitkomst |
|---|---:|
| Populatie bekend, gemiddeld | 100% |
| Slechtste bekende koppeling | 100% |
| Nieuwe kleur-vormvalidatie, gemiddeld | 100% |
| Slechtste validatiekoppeling | 100% |
| Universele vertaler op train | 100% |
| Universele vertaler op validatie | 100% |
| Overdracht met 32 voorbeelden, validatie | 81,25% |
| Overdracht met 128 voorbeelden, validatie | 100% |
| Overdracht met 512 voorbeelden, validatie | 100% |
| Overdracht met 2.048 voorbeelden, validatie | 100% |

De bindingskalibratie koos slotvolgorde `[1,0,3,2]`. De totale wederzijdse-informatiescore was exact 14,0 bits; de nummer twee scoorde 8,0 bits. Alle vier zenders codeerden de 15.360 toegankelijke train- plus validatiebetekenissen injectief.

De ontwikkelrun schreef 16.384 episodes: `1.024 validatiebetekenissen × 4 zenders × 4 ontvangers`. Er is geen testepisode geschreven.

## Bevriezingsbesluit

De ontwikkeling gaf geen inhoudelijke reden voor een extra variant. Wereld, expliciete holdoutparen, 14-bitkanaal, trainingsbudgetten, bindingskalibratie, overdrachtsbudgetten, topografische steekproefregel, vijf seeds en succescriteria zijn daarom ongewijzigd bevroren voor confirmatie.
