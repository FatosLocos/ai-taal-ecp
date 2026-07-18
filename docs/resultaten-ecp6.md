# Resultaten ECP-6 — schaalreplicatie op 14 bits

Confirmatieve run: `runs/20260718T070018Z-ecp6-experiment`  
Configuratie-SHA-256: `994ca086e1542e4608fec935ec5b72471b2e2cf73c2193f99ab6997044c40133`  
Split-SHA-256: `da751db7853ddbb84f000464c2627d4880eb154aef2158fb958d9a3779117d33`  
Formele primaire classificatie: **sterk bewijs**

## Einduitkomst

ECP-6 repliceert het volledig efficiënte ECP-5-protocol op een zestienmaal grotere betekenisruimte:

- 5/5 seeds sterk;
- 100% communicatie op alle bekende betekenissen;
- 100% op de expliciet verzegelde nieuwe kleur-vormcombinaties;
- 100% voor het slechtste zender-ontvangerpaar;
- 100% universele vertaling;
- 16.384 unieke berichten voor 16.384 betekenissen, zonder botsingen;
- exact 14 bits per bericht, gelijk aan de theoretische ondergrens.

## Primaire confirmatieve resultaten

| Seed | Bekend | Nieuwe testcombinaties | Slechtste agentkoppeling | Universele vertaler | Classificatie |
|---:|---:|---:|---:|---:|---|
| 11 | 100% | 100% | 100% | 100% | sterk |
| 23 | 100% | 100% | 100% | 100% | sterk |
| 37 | 100% | 100% | 100% | 100% | sterk |
| 53 | 100% | 100% | 100% | 100% | sterk |
| 71 | 100% | 100% | 100% | 100% | sterk |
| **Gemiddeld** | **100%** | **100%** | **100%** | **100%** | **sterk** |

Alle compositionele validatiescores zijn eveneens 100%. Binnen iedere seed produceren de vier onafhankelijk geïnitialiseerde zenders voor dezelfde betekenis exact hetzelfde bericht.

## Efficiëntie en schaal

De bronentropie is `log2(16.384)=14` bits. De factorlokale alfabetten vereisen `4+4+3+3=14` bits. Iedere zender realiseert:

- berichtentropie: 14,0 bits;
- fractie van bronentropie: 1,0;
- botsingen: 0;
- gemiddelde berichtafstand bij een minimale factorwijziging: 1,0 slot;
- factor-positieconcentratie: 1,0;
- topografische Spearman-correlatie: 1,0.

| Representatie voor dezelfde afgebakende taak | Gemiddelde bits | Groter dan ECP-6 |
|---|---:|---:|
| Canonieke JSON in UTF-8 | 438 | 31,3× |
| Nederlands sjabloon in UTF-8 | 334 | 23,9× |
| ECP-5-payload | 10 | kleinere wereld; niet rechtstreeks voldoende |
| Handmatige factorlokale referentie | 14 | 1× |
| **ECP-6** | **14** | **1×; theoretisch minimaal** |

De tekstvergelijking betreft alleen representatiegrootte binnen hetzelfde vooraf gedeelde schema. Zij vergelijkt niet de open expressiviteit, robuustheid of sociale functie van menselijke taal.

## Universele leesbaarheid

De universele vertaler vindt in iedere seed de exacte slotgrammatica. De gekozen permutatie scoort steeds 14,0 bits empirische wederzijdse informatie; de beste alternatieve permutatie scoort 8,0 bits. De scheiding van 6 bits maakt de keuze niet marginaal.

| Gelabelde betekenissen voor een nieuwe lezer | Exact op test, gemiddeld | Mediaan |
|---:|---:|---:|
| 32 | 76,25% | 75% |
| 128 | 100% | 100% |
| 512 | 100% | 100% |
| 2.048 | 100% | 100% |

De benodigde overdrachtsset groeit dus veel langzamer dan het volledige codeboek van 16.384 betekenissen. De terugval bij 32 voorbeelden zit in nog niet waargenomen kleur- en vormatomen; grootte en textuur zijn dan al foutloos.

## Voorbeeld buiten een alfabet

Seed 11 gebruikt voor slots `[vorm, kleur, textuur, grootte]`. De verzegelde testbetekenis `(c0,s9,z0,t0)` wordt:

`⟦15 · 1 · 3 · 1⟧`

en op de draad:

`1111 | 0001 | 011 | 001` → `11110001011001`.

Dit is geen verkort Nederlands en geen nieuw alfabet. Het is een geleerde productcode: positie draagt factortype, lokaal symbool draagt factorwaarde en de codeboeken zijn betekenisloze permutaties buiten de gedeelde conventie.

## Integriteit en controles

- Alle 309 vastgelegde artefacthashes komen overeen.
- Alle 163.840 episodes zijn aanwezig en schema-gevalideerd.
- Alle 163.840 berichten gebruiken exact 14 bits.
- Symbolen buiten hun factorlokale alfabet: 0.
- Alle twintig zenders verslaan 100 topografische nultoewijzingen (`p=0,00990099`).
- Husselcontrole: gemiddeld `0,0092%` exact, ruim onder de grens van 1%.
- Consistente symboolhernoeming behoudt alle voorspellingen.
- Ontvangers en vertalers zijn met uitsluitend symboolmatrices in geïsoleerde processen geëvalueerd.

## Wat is aangetoond

Binnen deze synthetische, uniforme en vooraf gefactoriseerde wereld is aangetoond dat onafhankelijk geïnitialiseerde agents:

1. een niet-talige en niet-alfabetische codeconventie kunnen delen;
2. die conventie foutloos naar volledig nieuwe factorcombinaties kunnen generaliseren;
3. haar naar een onafhankelijke nieuwe lezer kunnen overdragen;
4. haar zonder efficiëntieverlies van 1.024 naar 16.384 betekenissen kunnen opschalen;
5. precies de informatietheoretisch noodzakelijke payload kunnen gebruiken.

## Wat niet is aangetoond

- De factorindeling ontstaat niet spontaan; de architectuur legt vier factorslots als inductieve bias op.
- De proef behandelt geen natuurlijke beelden, geluid, onzekerheid of continue betekenis.
- De code onderhandelt niet zelfstandig over nieuwe factoren of protocolversies.
- De 14 bits omvatten geen transportheaders, foutcorrectie of kosten van het vooraf leren van de conventie.
- Het resultaat toont geen vervanging van algemene menselijke taal aan.

De scherpste conclusie is daarom: **een volledig efficiënte, universeel induceerbare machineconventie kan op deze productwereld foutloos schalen**, niet dat een algemene autonome AI-taal al is gerealiseerd.

## Bewijsbestanden

- [`report.md`](../evidence/ecp6/report.md)
- [`manifest.json`](../evidence/ecp6/manifest.json)
- [`baselines.json`](../evidence/ecp6/baselines.json)

De volledige lokale run bevat daarnaast checkpoints, geïsoleerde procesmatrices en 163.840 episodes. Deze grote gegenereerde artefacten worden niet in Git opgenomen; de bevroren configuratie en reproductieopdracht staan in [`evidence/ecp6/README.md`](../evidence/ecp6/README.md).
