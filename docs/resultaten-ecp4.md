# Resultaten ECP-4 — perfecte 10-bitpopulatie, instabiele vertaler

Confirmatieve interventie: `ecp4-confirmatory/intervention/20260718T061339Z-ecp4-experiment`  
Gepaarde 16-bitcontrole: `ecp4-confirmatory/control/20260718T061339Z-ecp4-experiment`  
Formele primaire classificatie: **gemengd bewijs**

## Uitkomst

ECP-4 bereikt de theoretische 10-bitondergrens zonder enig verlies in de primaire agentcommunicatie. Alle vijf seeds, alle zestien zender-ontvangerkoppelingen en alle 2.048 testepisodes per seed zijn exact correct. De 16-bitcontrole is eveneens 100%; het gepaarde compressieverschil is exact nul.

De afzonderlijk getrainde universele vertaler haalt de drempel echter slechts in seed 11. In de overige vier seeds kiest de vertaler een verkeerde harde factor-slotpermutatie. Daardoor blijft de formele totaalclassificatie gemengd, ondanks een foutloos verzonden protocol.

## Resultaten

| Seed | Bekend | Nieuwe testparen | Slechtste testpaar | Universele vertaler | Classificatie |
|---:|---:|---:|---:|---:|---|
| 11 | 100% | 100% | 100% | 100,0% | sterk |
| 23 | 100% | 100% | 100% | 9,4% | gemengd |
| 37 | 100% | 100% | 100% | 9,4% | gemengd |
| 53 | 100% | 100% | 100% | 9,4% | gemengd |
| 71 | 100% | 100% | 100% | 12,5% | gemengd |
| **Gemiddeld** | **100%** | **100%** | **100%** | **28,1%** | **gemengd** |

De 16-bitcontrole haalt eveneens gemiddeld 100% populatieexactheid en 65,9% vertaalexactheid. Ook daar falen twee vertalerseeds. Het probleem komt dus niet uit informatieverlies door compressie, maar uit het leren van één discrete keuze uit 24 mogelijke slotpermutaties.

## Efficiëntie

De vier lokale factoralfabetten gebruiken `3+3+2+2 = 10` bits. Dit is exact `log2(1024)` en kan voor een uniforme, ondubbelzinnige code niet verder worden verkleind. Iedere zender gebruikt 1024 unieke berichten voor 1024 betekenissen, zonder botsingen. ECP-4 heeft daarmee 100% theoretische kanaalefficiëntie.

## Integriteit

- Alle vijf populaties zijn zowel op train, validatie als test exact 100%.
- Alle twintig zenders hebben topografische overeenkomst 1,0.
- Iedere arm bevat 81.920 schema-gevalideerde episodes.
- Alle 309 artefacten per arm en hun hashes zijn integraal geldig.
- Hussel- en consistente symboolpermutatiecontroles zijn geslaagd.

## Besluit voor ECP-5

De 10-bitcode en factor-geïsoleerde populatie blijven ongewijzigd. ECP-5 vervangt uitsluitend de foutgevoelige gradientselectie van het vertalersslot door een exacte kalibratie over de 24 mogelijke permutaties. De kalibratie gebruikt alleen de gelabelde trainingsberichten waarover iedere universele vertaler al mocht beschikken.

## Lokale bewijsbestanden

De niet-versiebeheerde post-hocanalyse en gepaarde vergelijking staan lokaal onder `runs/ecp4-confirmatory/intervention/20260718T061339Z-ecp4-experiment/`.
