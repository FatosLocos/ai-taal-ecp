# Ontwikkellog ECP-2

De confirmatieve ECP-2-testset blijft gedurende dit document verzegeld. Alle onderstaande prestaties komen uitsluitend uit training en de afzonderlijke compositionele validatiematching.

## Variant A — algebraïsche consistentiedruk

Seed: 11  
Architectuur: vier onafhankelijke zenders × vier onafhankelijke ontvangers  
Kanaal: vier symbolen uit een vocabulaire van zestien, 16 bits  
Split: `7a227e22d86f00d8ab5078690de37de794774cdab636e7db374c5adbd0985126`

| Variant | Gewicht | Bekend gemiddeld | Slechtste bekend paar | Compositionele validatie | Universele vertaler validatie |
|---|---:|---:|---:|---:|---:|
| Controle | 0 | 97,0% | 96,5% | **9,5%** | **13,9%** |
| Licht | 0,25 | 95,8% | 95,1% | 4,6% | 10,0% |
| Midden | 1,0 | 59,9% | 35,2% | 2,6% | 3,5% |
| Sterk | 4,0 | 2,0% | 1,6% | 1,4% | 2,3% |

Lokale artefacten staan onder `runs/ecp2-variants/{control,light,medium,strong}/20260718T005403Z-ecp2-development/`.

### Besluit

De interventie wordt verworpen. Geen gewicht verbetert de compositionele validatie en alleen de controle benadert de bekende-prestatiedrempel. De testset is niet geopend.

De regularisatie heeft een informatieve degeneratie blootgelegd. Bij sterke druk worden grootte en textuur op de validatieset perfect gereconstrueerd, terwijl kleur en vorm richting kansniveau dalen. Omdat de algebraïsche eis gemiddeld over alle veranderingen wordt geminimaliseerd, kan de zender de eis goedkoop vervullen door de moeilijkste factoren niet meer te coderen. Een hogere taakverliesweging zou de twee doelen slechts opnieuw tegen elkaar uitruilen en verandert het fundamentele ontsnappingspad niet.

Conform de vooraf vastgelegde fallback gaat ontwikkeling verder met generationele transmissie. Die methode selecteert op leerbaarheid door nieuwe agents in plaats van rechtstreeks een gewenste geometrie in berichten af te dwingen.

## Variant B — culturele transmissie door agentvervanging

De populatie behoudt vier zenders en vier ontvangers. Na een vast interval wordt telkens één zender en één ontvanger volledig opnieuw geïnitialiseerd. De overige zes agents vormen het tijdelijke culturele geheugen. Na vier vervangingen is geen oorspronkelijke agent meer aanwezig; checkpoints van vóór die volledige turnover zijn niet selecteerbaar.

Drie vooraf gekozen intervallen worden met seed 11 en dezelfde gesloten testset vergeleken:

| Variant | Stappen tussen vervangingen | Eerste volledige turnover |
|---|---:|---:|
| Snel | 400 | stap 1.600 |
| Midden | 600 | stap 2.400 |
| Langzaam | 800 | stap 3.200 |

De trainingsbegroting blijft 5.000 stappen. Selectie gebruikt opnieuw eerst de bekende-prestatiedrempels en daarna uitsluitend de compositionele validatie. De algebraïsche regularisatie staat in deze drie varianten uit.

### Eerste uitkomst

| Variant | Bekend gemiddeld | Slechtste bekend paar | Compositionele validatie | Universele vertaler validatie |
|---|---:|---:|---:|---:|
| Snel, doorlopend | 97,4% | 93,9% | **19,5%** | **18,4%** |
| Midden, doorlopend | 95,2% | 92,1% | 10,0% | 12,7% |
| Langzaam, doorlopend | 94,1% | 90,8% | 10,1% | 11,9% |

De snelle variant verdubbelt de compositionele validatie bijna ten opzichte van de 9,5%-controle, maar blijft nieuwe agents introduceren. Daardoor is steeds een recent vervangen koppeling de zwakste. De volgende vooraf vastgelegde verfijning scheidt transmissie en consolidatie:

| Variant | Interval | Maximum vervangingen | Turnovers | Consolidatie na laatste vervanging |
|---|---:|---:|---:|---:|
| Eén snelle turnover | 400 | 4 | 1 | 3.400 stappen |
| Twee snelle turnovers | 400 | 8 | 2 | 1.800 stappen |
| Eén rustige turnover | 600 | 4 | 1 | 2.600 stappen |

De eindtest blijft ook voor deze verfijning gesloten.

### Consolidatie-uitkomst

| Variant | Bekend gemiddeld | Slechtste bekend paar | Compositionele validatie | Universele vertaler validatie |
|---|---:|---:|---:|---:|
| Eén snelle turnover | 98,8% | 97,5% | 10,3% | 15,0% |
| Twee snelle turnovers | **99,3%** | **98,8%** | **19,9%** | **25,2%** |
| Eén rustige turnover | 97,2% | 96,6% | 7,3% | 10,4% |

Twee snelle turnovers is de beste culturele variant. Zij voldoet aan de bekende-prestatiedrempels en verdubbelt de compositionele validatie ten opzichte van controle, maar blijft ver onder de ontwikkeldoelen van 80% populatie en 70% vertaler. Culturele transmissie wordt bewaard als beste zwak-gestuurde interventie, maar niet als confirmatieve ECP-2-kandidaat.

## Variant C — geleerde permutationslots

Als de consolidatievarianten de compositionele validatiedrempel niet halen, wordt één structureel sterkere architectuur getest. De zender bevat vier discrete berichtslots en kiest intern een harde één-op-éénpermutatie tussen de vier betekenisfactoren en die slots.

Niet vooraf bepaald zijn:

- welke factor aan welk slot wordt gekoppeld;
- welk van de zestien symbolen een factorwaarde vertegenwoordigt;
- of verschillende zenders dezelfde interne permutatie of symbolen kiezen;
- hoe ontvangers de vier symbolen decoderen.

Wel vooraf bepaald is dat iedere factor precies één afzonderlijk slot gebruikt. Dit is daarom een expliciete compositionele architectuurbias en een strengere ingreep dan algebraïsche of culturele druk. De variant is waardevol als werkend model en als positieve controle, maar een succes mag niet worden beschreven als volledig onbeïnvloede taalemergentie.

De slotvariant wordt eerst zonder algebraïsche regularisatie en zonder agentvervanging met seed 11 getraind. De vooraf gekozen ontwikkeldoelen zijn 97% bekend gemiddeld, 95% voor het slechtste paar, 80% compositionele validatie en 70% universele vertalervalidatie.

### Eerste slotuitkomst en consensusverfijning

De eerste volledig getrainde slotpopulatie haalt op train/validatie, zonder testtoegang:

- 100% bekende reconstructie voor ieder zender-ontvangerpaar;
- 69,4% gemiddelde compositionele validatie;
- 30,5% voor het slechtste compositionele paar;
- 50,6% universele vertalervalidatie.

De vier zenders kozen drie verschillende factor-slotpermutaties. Twee zenders kwamen onafhankelijk op dezelfde permutatie uit; de andere twee kozen ieder een andere. Daarom wordt één betekenisvrije verfijning getest: minimaliseer het verschil tussen de vier zachte bindingsmatrices en maak iedere matrix scherp. De consensus kiest geen factor-slotmapping vooraf; iedere van de 24 permutaties kan winnen.

Vooraf gekozen consensusgewichten:

| Variant | Consensusgewicht | Scherptegewicht |
|---|---:|---:|
| Licht | 0,1 | 0,1 |
| Midden | 1,0 | 0,1 |
| Sterk | 5,0 | 0,1 |

De eindtest blijft gesloten. Bij vrijwel gelijke validatie wint het lagere consensusgewicht.

### Consensusuitkomst en definitieve keuze

| Variant | Bekend gemiddeld | Slechtste bekend paar | Compositionele validatie | Slechtste validatiepaar | Universele vertaler validatie |
|---|---:|---:|---:|---:|---:|
| Licht, 0,1 | 100% | 100% | 76,9% | 51,6% | 50,6% |
| Midden, 1,0 | 100% | 100% | 90,0% | 82,0% | 95,3% |
| **Sterk, 5,0** | **100%** | **100%** | **97,0%** | **93,8%** | **95,3%** |

Gewicht 5,0 wint ondubbelzinnig en wordt de confirmatieve ECP-2-kandidaat. Alle vier zenders kozen dezelfde intern bepaalde permutatie `[kleur, textuur, vorm, grootte]`; de zachte bindingskansen hebben per slot maxima tussen 0,968 en 0,986. De populatie gebruikt voor 896 train- en validatiebetekenissen 896 unieke berichten, heeft nul botsingen, minimale-paarafstand exact één en topografische overeenkomst 1,0.

De confirmatieve interventie wordt gepaard met een controle die exact dezelfde permutationslotarchitectuur, split, seeds en trainingsbegroting gebruikt, maar zonder bindingsconsensus. Beide configuraties worden vóór enige ECP-2-testtoegang bevroren.
