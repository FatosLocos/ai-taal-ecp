# Onderzoeksopzet ECP-2: algebraïsch consistent emergent protocol

Status: bevroren voor confirmatieve uitvoering op 18 juli 2026 om 01:31:00 UTC  
Ouderexperiment: ECP-1  
Interventieconfiguratie: `config/ecp2.yaml`  
Controleconfiguratie: `config/ecp2-control.yaml`

## Aanleiding

ECP-1 liet zien dat vier onafhankelijke zenders en vier onafhankelijke ontvangers een gedeeld protocol kunnen stabiliseren. De populatiegeneraliseerbaarheid daalde desondanks van 15,9% in ECP-0 naar 10,1%. Alleen meerdere communicatiepartners aanbieden is dus onvoldoende.

Dat resultaat past bij bestaand onderzoek. Lee vond eveneens dat alleen één zender naar meerdere luisteraars laten uitzenden niet vanzelf meer compositionaliteit oplevert ([EMNLP 2024](https://aclanthology.org/2024.emnlp-main.1157/)). Rita et al. schrijven slechte emergente generalisatie mede toe aan overfitting van co-adaptatie ([NeurIPS 2022](https://openreview.net/forum?id=qqHMvHbfu6)). Chaabouni et al. laten zien dat compositionelere protocollen gemakkelijker overdraagbaar zijn, maar dat gewone generalisatiedruk compositionaliteit niet noodzakelijk laat ontstaan ([ACL 2020](https://aclanthology.org/2020.acl-main.407/)).

## Centrale hypothese

> Een protocol generaliseert beter wanneer dezelfde atomaire betekenisverandering in verschillende contexten een vergelijkbare verandering in de interne berichtverdeling veroorzaakt.

Voor een factorverandering `A → A'` en dezelfde verandering in een andere context `B → B'` minimaliseert ECP-2:

`||(M(A') − M(A)) − (M(B') − M(B))||²`

`M` is de door de zender geleerde verdeling over de vier posities en zestien symbolen. De uiteindelijke communicatie blijft exact hetzelfde harde 16-bitkanaal als in ECP-1.

## Wat niet wordt voorgeprogrammeerd

- Geen symbool krijgt vooraf een betekenis.
- Geen berichtpositie wordt aan kleur, vorm, grootte of textuur toegewezen.
- De vier zenders delen geen parameters of embeddings.
- De regularisatie schrijft niet voor welk bericht een betekenis moet krijgen.
- De ontvangers zien alleen de geproduceerde symbolen en niet de algebraïsche viertallen.

De experimentele druk gebruikt wel de bekende factorstructuur van de kunstmatige wereld. Dit is een expliciete inductieve bias en moet in de interpretatie worden meegewogen. Het experiment test dus of agents binnen zo'n algemene consistentiedruk zelf een bruikbaar discreet protocol ontdekken, niet of compositionaliteit zonder enige omgevingsstructuur ontstaat.

## Algebraïsche trainingsviertallen

Ieder viertal bevat `A`, `B`, `A'` en `B'`:

1. `A → A'` verandert precies één factorwaarde;
2. `B → B'` verandert exact dezelfde bronwaarde naar dezelfde doelwaarde;
3. de overige factoren vormen verschillende contexten;
4. alle vier betekenissen moeten in de trainingsset staan;
5. validatie- en testbetekenissen worden nooit als regularisatie-invoer gebruikt.

Daardoor kan de zender bijvoorbeeld leren dat één kleurverandering zich contextinvariant gedraagt, zonder dat vooraf wordt bepaald welk symbool of welke positie die verandering draagt.

## Twee onafhankelijke compositionele hold-outs

ECP-2 corrigeert een methodologische zwakte uit ECP-0 en ECP-1. De oude validatiesets bevatten losse betekenissen waarvan de kleur-vormparen al in training voorkwamen. Ze maten daardoor vooral interpolatie.

ECP-2 reserveert twee volledige en onderling disjuncte matchings:

- 128 betekenissen uit acht kleur-vormparen vormen de compositionele validatieset;
- 128 betekenissen uit acht andere paren vormen de verzegelde compositionele testset;
- de resterende 768 betekenissen vormen de training;
- alle zestien eerder geopende ECP-0- en ECP-1-testparen zijn voor beide nieuwe matchings uitgesloten.

De validatieset mag voor modelselectie worden gebruikt. De testset wordt tijdens ontwikkeling niet gecodeerd, gedecodeerd of geëvalueerd.

## Ontwikkelvergelijking

Met seed 11 worden maximaal vier vooraf gekozen gewichten vergeleken:

| Variant | Algebraïsch gewicht |
|---|---:|
| Controle | 0 |
| Licht | 0,25 |
| Midden | 1,0 |
| Sterk | 4,0 |

De gekozen variant is de variant met de hoogste exacte compositionele validatieprestatie, mits bekende betekenissen gemiddeld minstens 97% en voor het slechtste paar minstens 95% halen. Bij een verschil kleiner dan twee procentpunten wint het lagere gewicht.

Na deze keuze worden architectuur, gewicht, trainingsduur, vijf seeds en uitkomstdrempels bevroren. De controle en interventie gebruiken in de confirmatieve fase exact dezelfde split, seeds, populatiearchitectuur en trainingsbegroting.

## Confirmatieve eisen voor een ontwikkeld ECP-2-model

Sterk bewijs vereist in minstens vier van vijf interventieruns:

- minstens 97% bekende reconstructie gemiddeld;
- minstens 95% voor het slechtste bekende zender-ontvangerpaar;
- minstens 80% exacte reconstructie op de verzegelde compositionele test;
- minstens 70% voor één onafhankelijke universele vertaler;
- geslaagde kanaalisolatie-, hussel- en symboolpermutatiecontroles.

Daarnaast moet het gemiddelde van de interventie hoger zijn dan dat van de gepaarde controle op dezelfde testmatching. Alleen een hogere ECP-1-referentiescore is niet voldoende.

## Vervolg bij een negatieve ontwikkeluitkomst

Als geen algebraïsch gewicht de compositionele validatie duidelijk verbetert, wordt de testset niet geopend. De volgende ontwikkelvariant wordt dan generatietransmissie: agents worden periodiek vervangen en nieuwe agents krijgen een beperkte transmissiebottleneck. Dat volgt de positieve resultaten over iteratief en generationeel leren van [Guo et al.](https://arxiv.org/abs/1910.05291) en [Cogswell et al.](https://openreview.net/forum?id=r1gzoaNtvr&noteId=SJl3j-ScjB).

## Bevroren definitieve variant

De algebraïsche interventie faalde en culturele transmissie verbeterde compositionele validatie tot 19,9%, maar niet tot de vooraf gekozen prestatiedrempel. De definitieve kandidaat gebruikt daarom de transparant geregistreerde permutationslotarchitectuur met betekenisvrije bindingsconsensus:

- iedere zender kiest intern één van 24 factor-slotpermutaties;
- geen concrete permutatie, symboolbetekenis of symboolcode is vooraf opgegeven;
- vier onafhankelijke zenders krijgen consensusgewicht 5,0 op hun zachte bindingsmatrices;
- de controlegroep gebruikt exact dezelfde slotarchitectuur zonder consensusdruk;
- beide armen gebruiken dezelfde vijf seeds, split, trainingsbegroting, vertaler en overdrachtscurve;
- de verzegelde test wordt pas geopend nadat beide effectieve configuraties zijn vastgelegd.

De sterke ontwikkelvariant behaalde 100% bekend, 97,0% compositionele validatie en 95,3% universele vertalervalidatie. Deze ontwikkelprestatie is geen confirmatief resultaat.
