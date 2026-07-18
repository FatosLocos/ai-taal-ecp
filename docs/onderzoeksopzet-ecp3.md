# Onderzoeksopzet ECP-3

Status: **bevroren vóór confirmatieve testtoegang**  
Bevroren: 18 juli 2026 om 02:07:44 UTC  
Interventieconfiguratie: `config/ecp3.yaml`  
SHA-256: `2cab56d55a0364a218755d8815a7efaf36292896a125fdc4c593150c19b93f6e`  
Controleconfiguratie: `config/ecp3-control.yaml`  
SHA-256: `9569c5f5cef10681f4fd02ba0c70907910246d14802836ffe5bf0d2c5f0edcfa`

## Vraag

Verwijdert een harde injectiviteitsvoorwaarde voor atomaire factorcodes de lokale symboolbotsingen van ECP-2 en ontstaat daardoor een robuust compositioneel populatieprotocol?

## Model

Vier onafhankelijke zenders communiceren met vier onafhankelijke ontvangers via exact vier symbolen uit een vocabulaire van zestien. Iedere zender leert twee soorten arbitraire discrete toewijzingen:

1. een vrije één-op-éénpermutatie van de vier factoren naar de vier berichtslots;
2. per factor een vrije injectieve toewijzing van factorwaarden naar symbolen.

Een Sinkhorn-benadering levert de gradiënten; verzending en evaluatie gebruiken uitsluitend een harde factor-slotpermutatie en harde unieke symbolen. De interventie lijnt de zachte slot- en atoomtoewijzingen tussen zenders uit. De gepaarde controle heeft exact dezelfde injectieve architectuur, split, seeds en trainingsbegroting, maar beide consensusverliezen staan uit.

Geen slot en geen symbool krijgt vooraf een betekenis. Wel is vooraf vastgelegd dat iedere factor één positie gebruikt en dat twee waarden van dezelfde factor niet hetzelfde symbool mogen hebben. ECP-3 is dus een expliciet factorieel inductief vooroordeel, geen bewijs van ongestuurde taalemergentie.

## Nieuwe verzegelde split

De wereld blijft `8 × 8 × 4 × 4 = 1024` betekenissen groot. ECP-3 gebruikt:

- 768 trainingsbetekenissen;
- 128 betekenissen uit één volledig achtergehouden kleur-vormmatching voor selectie;
- 128 betekenissen uit een tweede volledig achtergehouden matching voor de eenmalige confirmatieve test.

Alle ECP-0-, ECP-1- en ECP-2-testparen zijn uitgesloten. Uit extra voorzichtigheid zijn ook de acht ECP-2-validatieparen uitgesloten, omdat zij de architectuurkeuze hebben beïnvloed. De nieuwe split heeft SHA-256 `91d6439fada82b1384a8d03f7cc1f5602091f794477be31c179c5a26e1b0464b`.

## Vooraf vastgelegde criteria

Per seed vereist sterk bewijs:

- minstens 97% bekende gemiddelde exacte reconstructie;
- minstens 95% voor het slechtste bekende zender-ontvangerpaar;
- minstens 80% gemiddelde exacte reconstructie op nieuwe testparen;
- minstens 70% exacte reconstructie door de universele vertaler.

De populatie-uitkomst is sterk bij minstens vier van vijf sterke seeds. Vijf vooraf vastgelegde seeds (`11, 23, 37, 53, 71`) worden gebruikt. Resultaten worden ook als gepaarde verschillen ten opzichte van de controle gerapporteerd, inclusief de exacte eenzijdige tekenomklaptoets over alle `2^5 = 32` tekencombinaties.

Het model geldt als bruikbaar ECP-basismodel wanneer de interventie minstens vier sterke seeds oplevert, alle kanaalcontroles slaagt en geen artefactintegriteitsfout bevat. Een controle-effect is informatief over consensus, maar geen aanvullende voorwaarde voor bruikbaarheid van het model zelf.

## Integriteitscontroles

- De testmatching wordt niet gebruikt voor training, vroegstoppen of selectie.
- Zenders en ontvangers delen geen parameters, embeddings of toestand.
- Definitieve evaluatie draait in afzonderlijke processen; ontvangers ontvangen alleen symboolmatrices.
- Alle berichten en reconstructies worden schema-gevalideerd en gelogd.
- Husselen moet onder 1% exact blijven.
- Consistente hernoeming van symbolen moet alle voorspellingen behouden.
- Alle vooraf geschreven artefacten worden na afloop gehasht en opnieuw gecontroleerd.

