# Resultaten ECP-3 — eerste robuuste basismodel

Confirmatieve interventie: `ecp3-confirmatory/intervention/20260718T020939Z-ecp3-experiment`  
Gepaarde controle: `ecp3-confirmatory/control/20260718T020939Z-ecp3-experiment`  
Split-SHA-256: `91d6439fada82b1384a8d03f7cc1f5602091f794477be31c179c5a26e1b0464b`  
Formele primaire classificatie: **sterk bewijs**

## Uitkomst

ECP-3 voldoet aan de vooraf vastgelegde definitie van een bruikbaar basismodel. Vier van vijf onafhankelijke seeds halen alle drempels; in die vier seeds reconstrueren de populatie en de universele vertaler iedere volledig nieuwe testbetekenis foutloos. Gemiddeld over alle vijf seeds is de testexactheid 89,0% en de vertaalexactheid 95,0%.

Het protocol gebruikt geen woorden, letters of vooraf benoemde symbolen. Een bericht bestaat uit vier gehele symbool-ID's tussen 0 en 15. De zenders leren zelf welke factor in welke positie komt en welk symbool een factorwaarde vertegenwoordigt. De enige opgelegde grammaticale voorwaarden zijn één factor per slot en een unieke code voor verschillende waarden binnen dezelfde factor.

## Primaire resultaten

| Seed | Bekend | Slechtste bekend paar | Compositionele validatie | Nieuwe testparen | Slechtste testpaar | Universele vertaler | Classificatie |
|---:|---:|---:|---:|---:|---:|---:|---|
| 11 | 100,0% | 100,0% | 100,0% | 100,0% | 100,0% | 100,0% | sterk |
| 23 | 100,0% | 100,0% | 100,0% | 100,0% | 100,0% | 100,0% | sterk |
| 37 | 100,0% | 100,0% | 99,6% | 100,0% | 100,0% | 100,0% | sterk |
| 53 | 100,0% | 100,0% | 51,8% | 45,0% | 38,3% | 75,0% | negatief |
| 71 | 100,0% | 100,0% | 100,0% | 100,0% | 100,0% | 100,0% | sterk |
| **Gemiddeld** | **100,0%** | **100,0%** | **90,3%** | **89,0%** | **87,7%** | **95,0%** | **sterk** |

De mediaan is zowel voor testexactheid als vertaalexactheid 100%. De lage gemiddelde score wordt volledig door één uitbijter veroorzaakt, niet door kleine fouten over alle runs.

## Gepaarde controle: wat doet consensus?

De controle gebruikt dezelfde injectieve zenderarchitectuur maar zonder consensus op slotbinding en atoomcodes.

| Metriek | Zonder consensus | Met consensus | Verschil | Interventie beter | Exacte eenzijdige `p` |
|---|---:|---:|---:|---:|---:|
| Nieuwe testparen | 79,0% | 89,0% | +10,0 procentpunt | 5/5 seeds | 0,03125 |
| Universele vertaler | 79,2% | 95,0% | +15,8 procentpunt | 3 beter, 1 gelijk, 1 lager | 0,125 |
| Sterke seeds | 3/5 | 4/5 | +1 seed | — | — |

De interventie vergroot de exacte berichtovereenkomst tussen zenders gemiddeld van 27,2% naar 77,0%. Consensus is dus geen semantisch woordenboek, maar een mechanisme waardoor onafhankelijke agents vaker hetzelfde arbitraire dialect kiezen.

## Hoe de nieuwe communicatievorm eruitziet

Seed 11 koos voor alle vier zenders de slotvolgorde:

`[vorm, textuur, grootte, kleur]`

Zender 0 koos onder meer de vrije atoomcodes:

- kleuren `c0..c7` → `[1,12,2,6,10,5,8,11]`;
- vormen `s0..s7` → `[10,13,11,2,12,3,9,14]`;
- groottes `z0..z3` → `[3,15,7,4]`;
- texturen `t0..t3` → `[0,2,7,15]`.

Daarmee wordt de nooit getrainde combinatie `(c0,s0,z0,t0)` verzonden als:

`⟦10 · 0 · 3 · 1⟧`

De vier ontvangers en de afzonderlijk getrainde universele vertaler reconstrueren dit exact. De getallen hebben buiten dit ene geleerde protocol geen vaste menselijke betekenis; consistente hernoeming van alle zestien symbolen verandert geen enkele voorspelling.

## Efficiëntie

| Representatie voor deze synthetische taak | Bits per bericht | Relatief tot ECP-3 |
|---|---:|---:|
| Nederlands sjabloon in UTF-8 | 328 | 20,5× groter |
| Canonieke JSON in UTF-8 | 432 | 27× groter |
| **ECP-3** | **16** | **1×** |
| Handgemaakte compositionele referentie | 12 | 25% kleiner dan ECP-3 |
| Theoretisch gepakte ondergrens | 10 | 37,5% kleiner dan ECP-3 |

ECP-3 gebruikt 16 kanaalbits voor 10 bits broninformatie: 62,5% van de capaciteit draagt theoretisch noodzakelijke informatie. Het is dus al veel compacter dan menselijke tekst voor exact deze afgebakende betekenisruimte, maar nog niet bit-optimaal. De vergelijking zegt niets over de algemene expressiviteit van Nederlands; dit is uitsluitend een taakgebonden representatievergelijking.

Iedere zender gebruikt over alle 1024 betekenissen 1024 unieke berichten en heeft nul berichtbotsingen. Het protocol is daardoor ondubbelzinnig. De berichtentopologie is exact factorieel: een verandering van één factor verandert gemiddeld exact één symboolpositie en de topografische Spearman-overeenkomst is 1,0.

## Wat seed 53 ons leert

Seed 53 heeft eveneens injectieve zenders, een gedeelde harde slotbinding en 100% bekende communicatie. De algemene GRU-ontvangers leerden kleur en vorm echter deels als gezamenlijke contextregel. Op nieuwe combinaties blijft kleur 90,7% correct maar vorm slechts 48,2%, waardoor exactheid naar 45,0% zakt.

Dit is geen botsing of ambiguïteit in het verzonden protocol; de universele vertaler haalt op dezelfde berichten 75,0%. Het is een decoderlocal optimum. Daarom is ECP-3 volgens de vooraf gekozen 4/5-regel robuust genoeg als basismodel, maar nog niet deterministisch foutloos over iedere initialisatie. Een volgende modelversie kan de ontvanger eveneens factor-geïsoleerd maken.

## Geldigheid en integriteit

- De configuraties en beslisregels zijn vóór testtoegang bevroren.
- Alle 48 eerder gebruikte ECP-0/1/2-paren zijn buiten de nieuwe validatie- en testmatchings gehouden.
- De testmatching is niet gebruikt voor training, vroegstoppen of modelselectie.
- Vier zenders en vier ontvangers zijn onafhankelijk geparametriseerd.
- Definitieve evaluatie draaide in afzonderlijke processen die uitsluitend de toegestane matrices ontvingen.
- Alle hussel- en symboolpermutatiecontroles zijn geslaagd.
- Iedere arm bevat 81.920 schema-gevalideerde episodes.
- Alle 309 artefacten per arm kwamen bij herberekening byte voor byte met hun hashes overeen.
- Alle twintig zender-seedcombinaties lagen boven alle honderd permutatienullen voor topografische overeenkomst.

## Wetenschappelijke conclusie

Binnen deze synthetische wereld is nu aangetoond dat onafhankelijke AI-agents een betekenisvrije, niet-alfabetische en taak-efficiënte conventie kunnen leren die nieuwe combinaties systematisch uit herbruikbare atomen samenstelt en door een onafhankelijke vertaler kan worden gelezen.

Niet aangetoond is dat zo'n grammatica zonder architectuurbias spontaan ontstaat, dat zij beter is dan menselijke taal voor open communicatie, of dat zij al de theoretische bitondergrens bereikt. ECP-3 is daarom het **eerste werkende basismodel**, niet het eindpunt van het volledige onderzoeksprogramma.

## Lokale bewijsbestanden

De niet-versiebeheerde bronrun staat lokaal onder `runs/ecp3-confirmatory/intervention/20260718T020939Z-ecp3-experiment/`. Deze bevat rapport, samenvatting, post-hocanalyse, gepaarde vergelijking en alle per-seedartefacten.
