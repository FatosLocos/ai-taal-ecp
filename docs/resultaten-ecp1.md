# Resultaten ECP-1

Confirmatieve run: `20260718T001805Z-ecp1-experiment`  
Configuratie bevroren: 18 juli 2026 om 00:17:09 UTC  
Configuratie-SHA-256: `13ebb1186aa87e98093f64a02a9961d35a2fdf6b06b6f56e47ab5a53c2a6e977`  
Formele primaire classificatie: **gemengd bewijs**  
Inhoudelijke uitkomst voor de populatiehypothese: **niet ondersteund**

## Samenvatting

ECP-1 testte vier onafhankelijk geparametriseerde zenders tegen vier onafhankelijk geparametriseerde ontvangers. Alle zestien koppelingen werden samen getraind. Hierdoor ontstond inderdaad een gedeelde conventie: een willekeurige ontvanger reconstrueert bekende berichten van iedere zender gemiddeld voor 98,5% correct en zelfs de gemiddeld slechtste zender-ontvangerkoppeling haalt 98,1%.

De populatietraining lost het belangrijkste probleem van ECP-0 echter niet op. Op volledig achtergehouden kleur-vormparen daalt de gemiddelde exacte reconstructie van 15,9% bij ECP-0 naar 10,1% bij ECP-1. De universele vertaler haalt 15,2%. Geen enkele seed benadert de vooraf vereiste 60% populatiegeneraliseerbaarheid of 50% vertaalbaarheid.

De juiste conclusie is daarom niet dat er al een nieuwe efficiënte AI-taal is ontstaan. Er is wel sterk bewijs dat meerdere onafhankelijke agents een compacte, gedeelde en structurele code kunnen afspreken. Die code is nog onvoldoende compositioneel: bekende combinaties worden grotendeels gememoriseerd en nieuwe combinaties worden niet systematisch uit bekende onderdelen samengesteld.

## Primaire resultaten

| Seed | Bekend gemiddeld | Slechtste bekend paar | Validatie | Nieuwe paren | Slechtste testpaar | Universele vertaler | Nieuwe ontvanger, 768 voorbeelden | Classificatie |
|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 11 | 99,2% | 98,8% | 77,6% | 17,0% | 7,8% | 24,4% | 18,8% | gemengd |
| 23 | 99,2% | 98,8% | 82,4% | 7,2% | 2,3% | 9,2% | 9,4% | negatief |
| 37 | 97,5% | 97,1% | 73,6% | 6,5% | 3,9% | 13,1% | 12,5% | negatief |
| 53 | 99,1% | 98,4% | 76,5% | 5,4% | 2,3% | 10,9% | 7,8% | negatief |
| 71 | 97,6% | 97,4% | 81,7% | 14,5% | 10,9% | 18,6% | 18,8% | negatief |
| **Gemiddeld** | **98,5%** | **98,1%** | **78,4%** | **10,1%** | **5,5%** | **15,2%** | **13,4%** | **gemengd** |

De testfactoren kleur en vorm — precies de twee factoren waarvan combinaties waren achtergehouden — worden gemiddeld voor 39,4% en 46,5% correct gereconstrueerd. Grootte en textuur blijven met 98,6% en 97,9% vrijwel intact. De fout zit dus gericht in het opnieuw combineren van de twee uitgesloten factoren, niet in een algemeen defect van de decoder.

## Vergelijking met ECP-0

| Metriek | ECP-0 | ECP-1 | Verschil |
|---|---:|---:|---:|
| Bekende betekenissen | 97,8% | 98,5% | +0,7 procentpunt |
| Validatie | 78,6% | 78,4% | −0,2 procentpunt |
| Volledig nieuwe kleur-vormparen | 15,9% | 10,1% | **−5,8 procentpunt** |
| Onafhankelijke/universele vertaler | 14,7% | 15,2% | +0,5 procentpunt |

Deze vergelijking is richtinggevend, niet gelijk aan een meting op exact dezelfde testitems: ECP-1 gebruikte bewust een nieuwe datasetseed en acht nieuwe achtergehouden paren, omdat de ECP-0-testset al was geopend. Van de vijf ECP-1-seeds presteert alleen seed 11 met 17,0% nipt boven het ECP-0-gemiddelde van 15,9%.

De formele classificatie blijft **gemengd bewijs**, omdat de vooraf geïmplementeerde aggregatieregel dat label toekent zodra minstens één geldige seed boven de ECP-0-referentie komt. Die regel wordt na het openen van de testset niet aangepast. Voor de wetenschappelijke interpretatie is het gemiddelde effect doorslaggevend: populatietraining heeft de generalisatie in deze proef niet verbeterd. Een volgend protocol moet de aggregatieregel expliciet op het gemiddelde en de onzekerheid daarvan vastleggen.

## Hypothesen

### H1 — Een gedeeld populatieprotocol ontstaat: ondersteund

Alle zestien zender-ontvangerkoppelingen leren dezelfde taak. De gemiddelde bekende nauwkeurigheid is 98,5% en de slechtste koppeling per seed blijft gemiddeld op 98,1%. Alle vijf seeds passeren de grens van 95% voor het slechtste paar; drie van vijf passeren ook de strengere grens van 99% gemiddeld.

De vier zenders produceren voor dezelfde betekenis gemiddeld in 54,3% van de gevallen exact hetzelfde bericht. Dat is geen volledige uniformiteit, maar wel aanzienlijke convergentie tussen modellen zonder gedeelde parameters.

### H2 — Populatietraining verbetert compositionele generalisatie: niet ondersteund

Het gemiddelde van 10,1% ligt onder ECP-0 en ver onder de vooraf vastgelegde grens van 60%. Geen van de vijf seeds passeert die grens. Het wisselen van communicatiepartners voorkomt dus wel exclusieve co-adaptatie van één paar, maar dwingt op zichzelf geen factorieel opgebouwde taal af.

### H3 — Eén universele vertaler ontsluit alle zenders: gedeeltelijk structureel, prestatiedrempel niet gehaald

De vertaler wordt pas na het bevriezen van de vier zenders getraind en haalt gemiddeld 15,2% op nieuwe paren. Dit toont dat één model de gedeeltelijk gedeelde conventie kan lezen, maar geen seed haalt de vereiste 50%.

### H4 — Een nieuwe ontvanger leert het protocol snel: niet ondersteund

| Gelabelde betekenissen | Gemiddeld exact op nieuwe paren |
|---:|---:|
| 32 | 1,3% |
| 128 | 7,9% |
| 512 | 11,7% |
| 768 | 13,4% |

De leercurve stijgt met meer voorbeelden, maar er is geen few-shotoverdracht. Zelfs na alle 768 trainingsbetekenissen blijft de nieuwe ontvanger ver onder een betrouwbaar niveau.

### H5 — De berichten bevatten semantische structuur: ondersteund als diagnostiek

De topografische overeenkomst tussen betekenisafstand en berichtafstand ligt voor de twintig zender-seedcombinaties tussen 0,308 en 0,432. In de vooraf aangekondigde post-runanalyse ligt iedere waarneming boven alle 100 willekeurige herkoppelingen; de empirische eenzijdige `p`-waarde is telkens `1/101 ≈ 0,0099`.

Dit bewijst structuur, niet voldoende compositionaliteit. Een code kan semantisch nabije betekenissen vergelijkbare berichten geven en toch falen bij een volledig nieuwe combinatie van twee factoren.

## Wat voor protocol ontstond?

Per zender worden 960 tot 1007 unieke berichten gebruikt voor 1024 betekenissen. De berichtentropie ligt tussen 9,864 en 9,967 bits, dicht bij de 10 bits broninformatie. Samen met de hoge bekende nauwkeurigheid wijst dit opnieuw op een bijna injectieve, gedistribueerde code.

ECP-1 voegt daar een belangrijk resultaat aan toe: meerdere onafhankelijke zenders en ontvangers kunnen zo'n code gezamenlijk stabiliseren. De gedeelde conventie is echter nog steeds meer een compact geometrisch codeboek dan een grammatica die kleur, vorm, grootte en textuur consequent als herbruikbare onderdelen combineert.

## Geldigheid en integriteit

- De ECP-1-configuratie is vóór de confirmatieve run bevroren.
- De acht ECP-0-testparen zijn expliciet uitgesloten bij het maken van de nieuwe split.
- De compositionele ECP-1-testset is niet gebruikt voor training of modelselectie.
- Vier zenders en vier ontvangers hebben volledig onafhankelijke parameters.
- Definitieve decodering vond plaats in afzonderlijke processen die uitsluitend symboolmatrices ontvingen.
- Alle husselcontroles bleven op of onder 1,0% en gemiddeld rond 0,09% exacte reconstructie.
- Consistente hernoeming van de zestien symbolen behield in alle seeds alle voorspellingen.
- Iedere seed bevat 16.384 schema-gevalideerde episodes; samen zijn dat 81.920 episodes.
- Alle 309 vooraf gehashte artefacten kwamen bij de post-runanalyse byte voor byte overeen.

## Besluit voor ECP-2

Nog meer agents toevoegen is niet de logische volgende stap. ECP-1 laat zien dat partnerwissel compatibiliteit creëert, maar niet vanzelf compositionaliteit. ECP-2 moet daarom een leerdruk invoeren die memorisatie moeilijker maakt zonder de semantiek vooraf in symbolen te programmeren.

De aanbevolen confirmatieve vergelijking is:

1. behoud de onafhankelijke populatie en het 16-bitkanaal;
2. train iteratief over generaties, waarbij nieuwe ontvangers alleen berichten en een beperkt aantal voorbeelden van de vorige generatie krijgen;
3. maak de trainingswereld systematisch onvolledig met wisselende combinaties per generatie;
4. selecteer uitsluitend op validatiegeneraliseerbaarheid en snelheid waarmee een nieuwe ontvanger leert;
5. vergelijk deze methode tegen een exact gelijke ECP-1-controle zonder generatievervanging;
6. gebruik opnieuw een volledig nieuwe, verzegelde testset;
7. leg de primaire groepsvergelijking en onzekerheidsmarge vooraf vast.

Compressie naar 12 of 10 bits blijft uitgesteld. Eerst moet een robuust herbruikbaar protocol ontstaan; pas daarna is maximale efficiëntie een zinvolle hoofdvraag.

## Lokale bewijsbestanden

De niet-versiebeheerde bronrun staat lokaal onder `runs/20260718T001805Z-ecp1-experiment/`. Deze bevat `report.md`, `summary.json`, `posthoc-analysis.json` en de per-seedmetrics, 81.920 episodes, checkpoints en geïsoleerde procesinvoer.
