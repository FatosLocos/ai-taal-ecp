# Onderzoeksopzet: emergente AI-communicatie

Versie: 0.2  
Datum: 17 juli 2026  
Eerste experiment: ECP-0

## 1. Doel

Dit onderzoek test of AI-agents onder gecontroleerde omstandigheden zelf een communicatieprotocol kunnen ontwikkelen dat:

- informatie betrouwbaar overdraagt;
- compacter is dan menselijke tekstrepresentaties;
- nieuwe combinaties kan beschrijven;
- door een onafhankelijke vertaler kan worden gereconstrueerd;
- door agents buiten het oorspronkelijke trainingspaar kan worden geleerd;
- controleerbaar blijft doordat alle communicatie door één meetbaar kanaal loopt.

Het onderzoek maakt onderscheid tussen een **code** en een **taalachtig protocol**. Een code kan iedere complete betekenis een willekeurig nummer geven. Een taalachtig protocol hergebruikt onderdelen of structuren en kan daardoor onbekende betekenissen samenstellen.

## 2. Centrale onderzoeksvraag

> Kunnen onafhankelijk getrainde AI-agents zelf een communicatieprotocol ontwikkelen dat bij gelijke taakprestatie efficiënter, duidelijker en systematischer is dan menselijke taal?

### Deelvragen

1. Ontstaat er zonder menselijke woorden een betrouwbaar discrete protocol?
2. Generaliseert dit protocol naar nooit getrainde combinaties?
3. Is de interne structuur achteraf systematisch te verklaren?
4. Kan een onafhankelijke vertaler de berichten correct ontsluiten?
5. Kan een nieuwe ontvanger het protocol leren zonder gezamenlijk met de oorspronkelijke zender te co-adapteren?
6. Hoe verandert het protocol onder druk van berichtkosten, ruis, context en complexere redeneertaken?

## 3. Operationele definities

### Nieuw

De betekenis van individuele symbolen en symboolreeksen is niet door een mens vastgelegd. Alleen de taak, wereld en kanaalcapaciteit zijn ontworpen.

### Efficiënt

Een protocol ligt gunstiger op de afruil tussen taakprestatie en kosten. Kosten worden primair in daadwerkelijk verzonden bits gemeten; latency, rekenkosten en foutgevoeligheid worden apart gerapporteerd.

### Duidelijk

De ontvanger komt bij hetzelfde bericht reproduceerbaar tot de bedoelde betekenis, ook bij ongeziene combinaties en beperkte ruis.

### Vertaalbaar

Een onafhankelijk model, dat niet met de agents is meegetraind, kan een bevroren bericht naar de canonieke betekenis en vervolgens naar Nederlands omzetten.

### Overdraagbaar

Een nieuwe ontvanger kan met een beperkte hoeveelheid voorbeelden leren communiceren met de bevroren oorspronkelijke zender.

### Volledig efficiënt

Dit wordt niet als absolute eigenschap gebruikt. Efficiëntie bestaat alleen ten opzichte van een taakverdeling, kanaal, fouttolerantie en hardware. Stap 3 zoekt daarom een Paretofront in plaats van één universeel optimum.

## 4. Vooraf vastgelegde hypothesen

- **H1 — Betrouwbaarheid:** minstens vier van vijf ECP-0-runs bereiken 99% exacte reconstructie op bekende betekenissen.
- **H2 — Combinatorische generalisatie:** een geleerd protocol presteert op achtergehouden kleur-vormparen duidelijk boven een niet-compositionele lookupbaseline.
- **H3 — Vertaalbaarheid:** een onafhankelijke vertaler generaliseert boven de lookupbaseline naar dezelfde achtergehouden paren.
- **H4 — Structuur:** betekenisafstand en berichtafstand vertonen meer samenhang dan bij willekeurig gepermuteerde berichten.
- **H5 — Overdracht:** in stap 2 leert een nieuwe ontvanger het bevroren protocol met minder voorbeelden dan een volledig nieuw protocol.
- **H6 — Efficiëntie:** in stap 2 verlaagt een bitstraf de gemiddelde berichtlengte zonder een vooraf bepaalde prestatiedrempel te onderschrijden.

Een negatieve uitkomst is een geldig resultaat. Drempels mogen na het bekijken van de testresultaten niet met terugwerkende kracht worden aangepast.

## 5. Stap 1 — ECP-0: vertaalbare basis

### 5.1 Kunstmatige wereld

Iedere betekenis is het cartesisch product van vier factoren:

| Factor | Aantal waarden | Interne representatie |
|---|---:|---|
| kleur | 8 | `c0` t/m `c7` |
| vorm | 8 | `s0` t/m `s7` |
| grootte | 4 | `z0` t/m `z3` |
| textuur | 4 | `t0` t/m `t3` |

Dit levert 1024 unieke betekenissen op. Menselijke labels mogen voor visualisatie bestaan, maar worden nooit als modelinvoer gebruikt.

De bron is uniform verdeeld. Daardoor is voor foutloze identificatie minimaal `log2(1024) = 10` bits informatie nodig.

### 5.2 Communicatietaak

1. De zender ontvangt één betekenis als vier categorische factoren.
2. De zender produceert exact vier symbolen.
3. De ontvanger ziet uitsluitend die vier symbolen.
4. De ontvanger voorspelt alle vier factoren.
5. Een aflevering is alleen exact correct als alle vier factoren kloppen.

Het kanaal bevat 16 mogelijke symbolen. Eén symbool kost dus 4 bits en ieder ECP-0-bericht kost exact 16 bits. De symbolen hebben bij aanvang geen betekenis. ECP-0.2 gebruikt deze extra ruimte om eerst leerbaarheid en vertaalbaarheid te testen; compressie naar drie symbolen/12 bits wordt in stap 2 onderzocht.

### 5.3 Agents

- Beide agents worden vanaf willekeurige initialisatie getraind.
- Ze gebruiken afzonderlijke gewichten, embeddings en random seeds.
- Ze krijgen geen voorgetraind taalmodel en geen natuurlijke taal als invoer.
- Tijdens training mag een straight-through Gumbel-Softmaxschatting worden gebruikt.
- Tijdens validatie en test worden uitsluitend harde gehele symbool-ID's verzonden.
- Voor de definitieve evaluatie draaien zender en ontvanger als logisch gescheiden processen.

Het doorgeven van gradients tijdens training is leersignaal, geen evaluatiekanaal. Alle conclusies worden uitsluitend op discrete evaluatie gebaseerd.

### 5.4 Datasplitsing

De splitsing wordt vóór training deterministisch gegenereerd:

1. Maak met de vastgelegde datasplitseed een willekeurige één-op-éénkoppeling tussen de acht kleuren en acht vormen. Zo komt iedere kleur en iedere vorm precies één keer in een achtergehouden paar voor.
2. Houd voor ieder paar alle 16 combinaties van grootte en textuur achter.
3. Dit vormt een compositionele testset van 128 betekenissen.
4. Selecteer uit de overige 896 betekenissen een gestratificeerde ontwikkelset van 128 betekenissen.
5. De resterende 768 betekenissen vormen de trainingsset.

Iedere atomaire waarde komt in training voor. Alleen specifieke combinaties ontbreken. De testset blijft verzegeld tot model- en hyperparameterkeuzes zijn afgerond.

### 5.5 Bevriezen en vertalen

Na training worden zender en ontvanger bevroren. Daarna wordt een derde model getraind:

- invoer: uitsluitend het discrete bericht;
- uitvoer: de vier canonieke factoren;
- training: alleen berichten uit de trainingssplitsing;
- evaluatie: de ontwikkelset en daarna eenmalig de compositionele testset.

Een Nederlandse renderer zet de voorspelde factoren deterministisch om naar leesbare tekst. De renderer telt niet als intelligente vertaler; de prestatie wordt gemeten op de voorspelde canonieke factoren.

### 5.6 Baselines

| Baseline | Functie |
|---|---|
| Nederlands sjabloon | Vergelijking met menselijke leesbaarheid en UTF-8-grootte |
| Canonieke JSON | Vergelijking met gangbare machinecommunicatie |
| Handmatig gepakte factorcode, 10 bits | Domeinspecifieke technische ondergrens |
| Willekeurige lookupcode | Hoge bekende-setprestatie zonder compositionaliteit |
| Handmatig compositionele factorcode | Controle voor maximaal expliciete structuur |

De vergelijking met Nederlands en JSON gaat over berichtgrootte, niet over algemene expressiviteit. De 10-bit factorcode voorkomt de onjuiste claim dat een geleerd protocol iedere ontworpen binaire representatie kan verslaan.

### 5.7 Primaire metingen

- exacte reconstructienauwkeurigheid;
- nauwkeurigheid per factor;
- prestatie op bekende en achtergehouden betekenissen;
- daadwerkelijk aantal kanaalbits;
- berichtentropie en aantal unieke berichten;
- botsingen: verschillende betekenissen met hetzelfde bericht;
- topografische overeenkomst tussen betekenis- en berichtafstand;
- minimale-paaranalyse en symboolablatie;
- onafhankelijke vertaalnauwkeurigheid;
- spreiding over vijf trainingsseeds;
- trainings- en inferentielatency, uitsluitend als secundaire maat.

Geen enkele structuurmaat geldt afzonderlijk als bewijs voor compositionaliteit. De conclusie combineert generalisatie, vertaling, minimale paren, ablaties en vergelijking met controles.

### 5.8 Controles tegen schijnsucces

- **Berichten husselen:** exacte reconstructie moet terugvallen tot ongeveer kansniveau.
- **Consistente symboolpermutatie:** prestatie moet gelijk blijven als symbool-ID's aan beide kanten identiek worden hernoemd.
- **Kanaalisolatie:** ontvanger krijgt geen episode-ID, betekenis-ID, kloktijd, gedeeld geheugen of bestandskanaal.
- **Geen gedeelde toestand:** modellen delen tijdens evaluatie geen gewichten, cache, random generator of verborgen activaties.
- **Volledige logging:** ieder bericht, antwoord, modelhash, config-hash en seed wordt opgeslagen.
- **Harde kwantisatie:** conclusies worden niet op continue, onbeperkt precieze vectoren gebaseerd.
- **Testverzegeling:** de compositionele testset beïnvloedt geen modelselectie.

### 5.9 Classificatie van de uitkomst

Stap 1 is methodologisch voltooid wanneer alle vijf vooraf ingestelde runs, baselines en controles zijn uitgevoerd. De uitkomst wordt daarna als volgt geclassificeerd:

- **Sterk bewijs:** ten minste vier runs halen 99% op bekende betekenissen, 90% op de compositionele test en 85% onafhankelijke vertaling op die test.
- **Gemengd bewijs:** bekende betekenissen halen 99%, maar generalisatie of vertaling ligt tussen lookupniveau en de sterke drempel.
- **Negatief resultaat:** de agents leren geen betrouwbaar kanaal, of generalisatie en vertaling verschillen niet betekenisvol van de lookupcontrole.
- **Ongeldige run:** een controle faalt, een nevenkanaal is mogelijk of de vooraf vastgelegde configuratie is zonder registratie gewijzigd.

Deze percentages zijn onderzoeksdrempels, geen garantie dat ECP-0 ze zal halen.

## 6. Stap 2 — Verfijning en evolutie

Stap 2 bouwt alleen voort op een bevroren rapport van stap 1. Nieuwe hypothesen en configuraties worden vooraf geregistreerd.

Geplande uitbreidingen:

- variabele berichtlengte van één tot zes symbolen;
- volledige bitboekhouding, inclusief lengte-informatie;
- informatiedruk via een expliciete bitstraf;
- ruis door symboolverlies, vervanging en verwisseling;
- context waarin irrelevante eigenschappen veilig kunnen worden weggelaten;
- relaties tussen meerdere objecten;
- populaties van meerdere zenders en ontvangers;
- periodieke vervanging door nieuw geïnitialiseerde agents;
- overdrachtstests met een bevroren zender of ontvanger;
- vergelijking tussen gezamenlijke training en iteratief leren over generaties.

De kernvraag verschuift hier van “kan het communiceren?” naar “blijft het protocol efficiënt, leerbaar en robuust wanneer de omgeving verandert?”

## 7. Stap 3 — Efficiëntie en complex redeneren

Stap 3 introduceert complexere betekenissen en meerdere kanaalvormen:

- hiërarchische concepten;
- object-relatiegrafen;
- tijd, onzekerheid, intentie en voorwaardelijke acties;
- abstracte redeneerregels in plaats van alleen zichtbare kenmerken;
- discrete sequenties, getypeerde grafen en gekwantiseerde vectoren;
- taakoverdracht naar een omgeving waarop het protocol niet is getraind.

Continue vectoren worden altijd naar een vooraf vastgelegd aantal bits gekwantiseerd. Anders is een eerlijke efficiëntievergelijking onmogelijk.

De uitkomst wordt als Paretofront gerapporteerd over:

1. taakprestatie;
2. verzonden bits;
3. robuustheid;
4. generalisatie;
5. vertaalbaarheid;
6. overdraagbaarheid;
7. latency en rekenkosten.

## 8. Reproduceerbaarheid en rapportage

Iedere run krijgt een onveranderlijk run-ID en bevat minimaal:

- volledige configuratie;
- software- en hardwareversies;
- datasetmanifest en hashes;
- modelinitialisatieseeds;
- checkpoints en modelhashes;
- ruwe episodeberichten en voorspellingen;
- berekende metrics;
- geregistreerde afwijkingen van het protocol;
- automatisch en menselijk samengevat resultaat.

Mislukte runs worden niet verwijderd. Een wijziging na resultaatinspectie start een nieuwe experimentversie.

## 9. Interpretatiegrenzen

Een positief resultaat toont een efficiënt emergent protocol in de geteste wereld. Het bewijst niet dat:

- het protocol een algemeen alternatief voor menselijke taal is;
- agents bewust een taal hebben ontworpen;
- dezelfde structuur spontaan bij grote taalmodellen ontstaat;
- communicatie buiten de experimentele taak efficiënt blijft;
- onbegrijpelijkheid op zichzelf intelligentie of semantische diepte aantoont.

## 10. Onderzoeksbasis

De opzet sluit aan bij eerder onderzoek naar emergente communicatie:

- [Natural Language Does Not Emerge ‘Naturally’ in Multi-Agent Dialog](https://aclanthology.org/D17-1321/) — succesvolle taakprestatie garandeert geen interpreteerbare of compositionele taal.
- [Emergent Communication: Generalization and Overfitting in Lewis Games](https://proceedings.neurips.cc/paper_files/paper/2022/hash/093b08a7ad6e6dd8d34b9cc86bb5f07c-Abstract-Conference.html) — co-adaptatie en overfitting kunnen generalisatie ondermijnen.
- [Trading off Utility, Informativeness, and Complexity in Emergent Communication](https://proceedings.neurips.cc/paper_files/paper/2022/hash/8bb5f66371c7e4cbf6c223162c62c0f4-Abstract-Conference.html) — informatiewaarde en protocolcomplexiteit moeten samen worden gemeten.
- [Emergent Communication for Rules Reasoning](https://proceedings.neurips.cc/paper_files/paper/2023/hash/d8ace30c68b085556ccce04ed4ae4ebb-Abstract-Conference.html) — complexere redeneertaken kunnen structurelere protocollen stimuleren.
- [A Compressive-Expressive Communication Framework for Compositional Representations](https://proceedings.neurips.cc/paper_files/paper/2025/hash/3310034c97fab48fdbcba18f90fd5364-Abstract-Conference.html) — compressiedruk en iteratief leren kunnen efficiëntie en compositionaliteit ondersteunen.
