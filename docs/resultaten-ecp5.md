# Resultaten ECP-5 — volledig efficiënt 10-bitmodel

Confirmatieve interventie: `ecp5-confirmatory/intervention/20260718T062848Z-ecp5-experiment`  
Gepaarde controle: `ecp5-confirmatory/control/20260718T062848Z-ecp5-experiment`  
Split-SHA-256: `cc487fd9042c5190bee93278c4be5180363f46a46d0e8af2f9d7d75a4f173140`  
Formele primaire classificatie: **sterk bewijs**

## Einduitkomst

ECP-5 is binnen de gedefinieerde synthetische wereld een volledig efficiënt en robuust communicatieprotocol:

- 5/5 seeds sterk;
- 100% bekende communicatie;
- 100% op volledig nieuwe grootte-textuurcombinaties;
- 100% voor het slechtste zender-ontvangerpaar;
- 100% universele vertaling;
- exact 10 bits per bericht, gelijk aan de theoretische ondergrens;
- 1024 unieke berichten voor 1024 betekenissen, zonder botsingen.

## Confirmatieve resultaten

| Seed | Bekend | Nieuwe testcombinaties | Slechtste agentpaar | Universele vertaler | Classificatie |
|---:|---:|---:|---:|---:|---|
| 11 | 100% | 100% | 100% | 100% | sterk |
| 23 | 100% | 100% | 100% | 100% | sterk |
| 37 | 100% | 100% | 100% | 100% | sterk |
| 53 | 100% | 100% | 100% | 100% | sterk |
| 71 | 100% | 100% | 100% | 100% | sterk |
| **Gemiddeld** | **100%** | **100%** | **100%** | **100%** | **sterk** |

Ook alle compositionele validatiescores zijn 100%. De vier zenders binnen iedere seed produceren voor dezelfde betekenis exact hetzelfde bericht.

## Effect van bindingskalibratie

De ongekalibreerde controle behoudt eveneens 100% primaire populatiecommunicatie, maar slechts twee van vijf universele vertalers vinden de juiste slotgrammatica.

| Seed | Ongekalibreerde vertaler | Gekalibreerde vertaler | Verschil |
|---:|---:|---:|---:|
| 11 | 100,0% | 100,0% | 0,0 pp |
| 23 | 12,5% | 100,0% | +87,5 pp |
| 37 | 100,0% | 100,0% | 0,0 pp |
| 53 | 9,4% | 100,0% | +90,6 pp |
| 71 | 9,4% | 100,0% | +90,6 pp |
| **Gemiddeld** | **46,3%** | **100,0%** | **+53,8 pp** |

De interventie is beter in alle drie seeds waarin verbetering mogelijk was en gelijk op 100% in de andere twee. De vooraf vastgelegde tekenomklaptoets geeft `p=0,125`, omdat slechts drie verschillen niet nul zijn en de exacte toets daardoor maar acht effectieve tekencombinaties heeft. De effectgrootte en foutmodus zijn inhoudelijk ondubbelzinnig: iedere verkeerde controlebinding wordt door kalibratie hersteld.

In alle vijf interventieseeds scoort de gekozen slotpermutatie exact 10,0 bits wederzijdse informatie tegenover 8,0 bits voor de nummer twee.

## Overdraagbaarheid

| Gelabelde betekenissen | Exact op nieuwe testcombinaties |
|---:|---:|
| 32 | 97,5% gemiddeld; mediaan 100% |
| 128 | 100% |
| 256 | 100% |
| 512 | 100% |

Een nieuwe lezer hoeft dus geen volledig codeboek van 1024 betekenissen te zien. Vanaf 128 voorbeelden wordt de factorgrammatica in alle seeds foutloos overgedragen.

## Werkelijk 10 bits

De bron bevat `log2(1024)=10` bits informatie. ECP-5 gebruikt lokale alfabetten van 8, 8, 4 en 4 symbolen, dus `3+3+2+2=10` bits. De post-runanalyse heeft alle 81.920 episodeberichten opnieuw tegen de per-slotfactorbinding gecontroleerd:

- gecontroleerde berichten: 81.920;
- onjuiste bitlengtes: 0;
- symbolen buiten lokale alfabetten: 0;
- kanaalefficiëntie: 100% van de theoretisch noodzakelijke capaciteit.

| Representatie voor deze taak | Bits | Groter dan ECP-5 |
|---|---:|---:|
| Canonieke JSON in UTF-8 | 432 | 43,2× |
| Nederlands sjabloon in UTF-8 | 328 | 32,8× |
| ECP-3 | 16 | 1,6× |
| Handgemaakte compositionele referentie | 12 | 1,2× |
| **ECP-5** | **10** | **1×; theoretisch minimaal** |

Dit vergelijkt alleen de representatie van dezelfde afgebakende betekenisruimte, niet de algemene expressiviteit van menselijke taal.

## Voorbeeld van de machineconventie

Seed 11 koos de slotvolgorde `[grootte, textuur, kleur, vorm]`. De nooit getrainde combinatie `(c0,s0,z0,t1)` wordt verzonden als:

`⟦0 · 3 · 5 · 4⟧`

In de lokale alfabetten is de wire-representatie:

`00 | 11 | 101 | 100` → `0011101100`

De slotvolgorde en alle waarde-symboolpermutaties zijn door de agents gekozen. De bits hebben zonder het geleerde protocol geen vaste menselijke betekenis.

## Wat hiermee wel en niet is aangetoond

Wel aangetoond:

- onafhankelijke agents kunnen een arbitraire niet-alfabetische conventie delen;
- de conventie combineert bekende atomen foutloos tot nieuwe betekenissen;
- een onafhankelijke lezer kan de grammatica betrouwbaar induceren;
- voor deze wereld bereikt het kanaal de informatietheoretische ondergrens.

Niet aangetoond:

- dat de factorindeling zonder architectuurbias spontaan ontstaat;
- dat dit protocol open menselijke taal kan vervangen;
- dat dezelfde methode zonder nieuwe afspraken dynamisch onbekende factoren toevoegt;
- dat efficiëntie op deze uniforme laboratoriumwereld direct naar natuurlijke multimodale data overdraagt.

ECP-5 is daarmee het **volledig efficiënte eindmodel van deze onderzoekscasus**, niet een algemene universele AI-taal.

## Integriteit

- Alle 309 artefacten en hashes zijn geldig.
- Alle 81.920 episodes zijn aanwezig en schema-gevalideerd.
- Alle twintig zenders verslaan hun honderd topografische permutatienullen.
- Husselcontroles blijven onder 1%.
- Consistente symboolhernoeming behoudt alle voorspellingen.
- De definitieve ontvangers en vertalers draaiden in geïsoleerde processen.

## Lokale bewijsbestanden

De niet-versiebeheerde interventie- en controle-artefacten staan lokaal onder `runs/ecp5-confirmatory/`. Deze bevatten rapporten, samenvattingen, post-hocanalyses, de gepaarde vergelijking en alle per-seedartefacten.
