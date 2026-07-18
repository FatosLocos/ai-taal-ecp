# Resultaten ECP-0.2

Confirmatieve run: `20260717T221924Z-ecp0-experiment`  
Configuratie bevroren: 17 juli 2026 om 22:18:41 UTC  
Configuratie-SHA-256: `7415f5732fed4d5e7e72ca82e917e4110a9f9f8ba68566daba3aa26e652b90cc`  
Primaire classificatie: **gemengd bewijs**

## Samenvatting

ECP-0.2 toont dat twee vanaf nul getrainde agents binnen een kanaal van 16 bits zelfstandig een vrijwel injectief communicatieprotocol kunnen ontwikkelen. Het protocol reconstrueert bekende betekenissen in vier van vijf runs voor minstens 99% correct. Het draagt bovendien semantische structuur over naar een onafhankelijke vertaler.

Het protocol generaliseert echter nog niet betrouwbaar naar kleur-vormparen die volledig buiten training zijn gehouden. De gemiddelde exacte testprestatie is 15,9%, met een spreiding van 0% tot 43,8%. Daarmee is er bewijs voor gedeeltelijke structurele generalisatie, maar niet voor een stabiele nieuwe taalvorm.

## Primaire resultaten

| Seed | Bekend exact | Validatie exact | Achtergehouden paren | Vertaler op achtergehouden paren | Classificatie |
|---:|---:|---:|---:|---:|---|
| 11 | 99,5% | 73,4% | 7,8% | 12,5% | gemengd |
| 23 | 99,9% | 83,6% | 0,0% | 3,1% | gemengd |
| 37 | 99,1% | 79,7% | 20,3% | 12,5% | gemengd |
| 53 | 91,3% | 60,9% | 7,8% | 7,0% | negatief |
| 71 | 99,2% | 95,3% | 43,8% | 38,3% | gemengd |
| **Gemiddeld** | **97,8%** | **78,6%** | **15,9%** | **14,7%** | **gemengd** |
| **Mediaan** | **99,2%** | **79,7%** | **7,8%** | **12,5%** | — |

De niet-compositionele lookupbaseline scoort per definitie 0% op onbekende betekenissen. De handmatig compositionele baseline scoort 100% met 12 bits; de optimaal gepakte factorcode scoort 100% met 10 bits.

## Hypothesen

### H1 — Betrouwbaarheid: ondersteund

Vier van vijf runs overschrijden de vooraf vastgelegde grens van 99% bekende reconstructie. Eén seed blijft met 91,3% duidelijk achter. De basis is dus reproduceerbaar, maar het trainingsproces kent nog een ongunstige lokale oplossing.

### H2 — Combinatorische generalisatie: gedeeltelijk ondersteund

Vier van vijf runs presteren boven de 0%-lookupbaseline op volledig achtergehouden kleur-vormparen. De mediaan is slechts 7,8% en één run bereikt 0%. Seed 71 laat met 43,8% zien dat aanzienlijk betere generalisatie binnen dezelfde architectuur mogelijk is, maar niet dat deze betrouwbaar ontstaat.

### H3 — Onafhankelijke vertaalbaarheid: gedeeltelijk ondersteund

De vertaler reconstrueert trainingsberichten vrijwel foutloos en scoort in alle vijf runs boven de lookupbaseline op de achtergehouden paren. De gemiddelde testprestatie van 14,7% blijft echter te laag om het protocol algemeen vertaalbaar te noemen.

### H4 — Structurele semantiek: ondersteund

De topografische overeenkomst tussen betekenisafstand en berichtafstand ligt per seed tussen 0,308 en 0,448. Een post-runanalyse met 100 willekeurige betekenis-berichtkoppelingen per seed vond per seed een maximale nulwaarde van hoogstens 0,004. Alle vijf waarnemingen lagen daarboven; de empirische eenzijdige `p`-waarde is telkens `1/101 ≈ 0,0099`.

Deze permutatietoets voltooit de vooraf geregistreerde diagnostische vergelijking, maar is na de primaire run uitgevoerd en verandert de primaire classificatie niet.

### H5 en H6 — Nog niet getest

Overdracht naar nieuwe agents en compressie via een bitstraf behoren tot stap 2.

## Wat voor protocol ontstond?

De agents ontwikkelden geen eenvoudig woordenboek met één vaste berichtpositie per factor:

- tussen 955 en 1015 van de 1024 betekenissen kregen een uniek bericht;
- de berichtentropie lag tussen 9,86 en 9,98 bits, dicht bij de 10 bits broninformatie;
- iedere berichtpositie bleek belangrijk bij ablaties;
- de gemiddelde concentratie van factorveranderingen op één positie lag rond 0,31, slechts beperkt boven 0,25 bij een gelijkmatige verdeling;
- betekenisgelijkheid is wel duidelijk terug te zien in afstanden tussen berichten.

De beste beschrijving is daarom: **een grotendeels gedistribueerde, bijna injectieve code met gedeeltelijke semantische geometrie**. Dat is meer dan een willekeurige lookupcode, maar nog minder systematisch dan een compositionele taal.

## Efficiëntie

| Representatie | Bits per betekenis | Exact op onbekende combinaties |
|---|---:|---:|
| Nederlands vast sjabloon, UTF-8 | 328 | 100% bij correcte productie |
| Canonieke JSON, UTF-8 | 432 | 100% |
| ECP-0.2 | 16 | gemiddeld 15,9% |
| Handmatig compositioneel | 12 | 100% |
| Optimaal gepakte factoren | 10 | 100% |

ECP-0.2 is zeer compact ten opzichte van ongecomprimeerde tekst en JSON. Het is niet efficiënter dan een ontworpen domeincode en de foutgraad op onbekende combinaties is nog te hoog. Er is dus nog geen grond voor de claim dat AI een superieure algemene communicatievorm heeft ontwikkeld.

## Geldigheid en integriteit

- Alle vijf seeds gebruikten dezelfde bevroren configuratie.
- De compositionele testset werd niet gebruikt voor training of modelselectie.
- Zender en ontvanger draaiden tijdens evaluatie in afzonderlijke processen.
- De ontvanger kreeg uitsluitend een matrix met vier symbool-ID's.
- Alle husselcontroles bleven op 0% of 0,098% exacte reconstructie.
- Consistente hernoeming van alle symbool-ID's behield in iedere run exact dezelfde voorspellingen.
- Iedere seed bevat 1024 schema-gevalideerde episodes.
- Alle 179 vooraf gehashte artefacten kwamen bij de post-runanalyse byte voor byte overeen.

## Besluit voor stap 2

Direct comprimeren van 16 naar 12 bits is nu methodologisch te vroeg. De bottleneck is niet berichtgrootte, maar betrouwbare compositionaliteit en overdracht.

De aanbevolen volgorde voor ECP-1 is:

1. gebruik een nieuwe datasplitseed en nieuwe achtergehouden paren; de ECP-0-testset is nu opgebruikt;
2. train een populatie van zenders en ontvangers met wisselende koppelingen om co-adaptatie van één paar te verminderen;
3. voeg periodiek een nieuw geïnitialiseerde ontvanger toe en meet hoeveel voorbeelden die nodig heeft;
4. onderzoek iteratief leren over generaties en progressieve reconstructie na ieder symbool;
5. behoud eerst het 16-bitkanaal om het effect op generalisatie zuiver te meten;
6. vergelijk daarna dezelfde methode op 16 en 12 bits voordat variabele lengte en bitstraf worden toegevoegd.

Pas wanneer generalisatie en overdraagbaarheid stabiel zijn, kan stap 3 eerlijk op maximale efficiëntie worden gericht.

## Lokale bewijsbestanden

De niet-versiebeheerde bronrun staat lokaal onder `runs/20260717T221924Z-ecp0-experiment/`. Deze bevat `report.md`, `summary.json`, `posthoc-analysis.json` en de per-seedmetrics, episodes, modellen en geïsoleerde procesinvoer.
