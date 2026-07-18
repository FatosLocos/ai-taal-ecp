# Onderzoeksopzet ECP-1: populatie en overdraagbaarheid

Status: bevroren voor confirmatieve uitvoering op 18 juli 2026 om 00:17:09 UTC  
Ouderexperiment: ECP-0.2

## Aanleiding

ECP-0 ontwikkelde vrijwel injectieve protocollen met aantoonbare semantische geometrie, maar slechts 15,9% gemiddelde exacte generalisatie naar volledig achtergehouden kleur-vormparen. De grote verschillen tussen seeds wijzen op co-adaptatie: één zender en één ontvanger kunnen samen een bruikbare maar slecht overdraagbare code stabiliseren.

## Centrale hypothese

> Als iedere zender tijdens training met meerdere onafhankelijk geparametriseerde ontvangers moet communiceren en omgekeerd, ontstaat meer druk naar een gedeeld, systematisch en overdraagbaar protocol.

ECP-1 verandert daarom één primair mechanisme: één paar wordt vervangen door vier zenders en vier ontvangers. Kanaal, wereld, modellen en reconstructietaak blijven gelijk aan ECP-0.2.

## Nieuwe en onafhankelijke testset

De acht ECP-0-testparen zijn expliciet uitgesloten. ECP-1 gebruikt een nieuwe datasplitseed en accepteert alleen een één-op-éénmatching die geen enkel oud testpaar bevat. De nieuwe testset blijft gesloten tijdens ontwikkeling en modelselectie.

Omdat de ECP-0-testset bekend is, mag die niet als confirmatieve ECP-1-test worden hergebruikt.

## Populatietraining

- Vier zenders en vier ontvangers starten met onafhankelijke initialisaties.
- Er worden geen gewichten, embeddings, gradients buiten het gekozen paar of verborgen toestanden gedeeld.
- Per stap produceren alle vier zenders ieder één bericht voor dezelfde willekeurige batch.
- Alle vier ontvangers reconstrueren ieder zenderbericht; de zestien verliezen worden gemiddeld.
- Iedere stap bevat daardoor alle zestien zender-ontvangerinteracties, zonder leider of voorkeursdialect.
- Over 7.000 stappen krijgt ieder paar evenveel directe leerinteracties als een ECP-0-paar.
- Modelselectie gebruikt alleen train en validatie.
- Een checkpoint is pas primair selecteerbaar bij minstens 99% gemiddelde bekende nauwkeurigheid én minstens 95% voor het slechtste paar.

## Universele vertaler en nieuwe ontvanger

Na het bevriezen van de populatie wordt één nieuwe ontvanger getraind op berichten van alle vier zenders. Deze ontvanger heeft geen toegang tot de oorspronkelijke ontvangers en fungeert tegelijk als universele vertaler.

Een overdrachtscurve traint daarnaast verse ontvangers met 32, 128, 512 en 768 unieke trainingsbetekenissen. Alle vier zenders leveren berichten voor dezelfde geselecteerde betekenissen. De curve meet of het populatieprotocol met weinig voorbeelden kan worden overgenomen.

## Primaire uitkomstmaten

1. gemiddelde exacte nauwkeurigheid over alle zestien paren;
2. nauwkeurigheid van het slechtste paar;
3. gemiddelde nauwkeurigheid op de nieuwe achtergehouden kleur-vormparen;
4. nauwkeurigheid van de universele vertaler op die paren.

Sterk bewijs vereist in minstens vier van vijf geldige seeds:

- minimaal 99% gemiddeld op bekende betekenissen;
- minimaal 95% voor het slechtste bekende paar;
- minimaal 60% gemiddeld op de compositionele test;
- minimaal 50% voor de universele vertaler op de compositionele test.

## Controles

- Definitieve zender- en ontvangerevaluaties draaien in afzonderlijke processen.
- Ontvangers krijgen alleen de symboolmatrix.
- Berichten worden binnen iedere zender gehusseld; de nauwkeurigheid moet tot maximaal 1% dalen.
- Een consistente vocabulairepermutatie wordt op alle berichten en ontvangerembeddings toegepast; voorspellingen moeten identiek blijven.
- Resultaten worden per paar en als populatiegemiddelde opgeslagen, zodat een goed gemiddelde geen falend paar verbergt.

## Interpretatie

Een verbetering ten opzichte van ECP-0 ondersteunt de hypothese dat communicatieve diversiteit co-adaptatie vermindert. Geen verbetering is eveneens informatief: dan is alleen populatiedruk onvoldoende en moet ECP-2 iteratief leren, progressieve reconstructie of explicietere contextdruk isoleren.

Compressie naar 12 bits wordt in ECP-1 bewust niet getest. Eerst moet de semantische overdracht stabieler worden.

De vijf seeds mogen gelijktijdig in afzonderlijke processen draaien. Dit verandert geen data, modelinteractie of random generator binnen een seed en dient uitsluitend om de wandkloktijd te verkorten.
