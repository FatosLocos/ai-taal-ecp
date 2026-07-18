# Resultaten ECP-2

Confirmatieve interventie: `ecp2-confirmatory/intervention/20260718T013310Z-ecp2-experiment`  
Gepaarde controle: `ecp2-confirmatory/control/20260718T013310Z-ecp2-experiment`  
Split-SHA-256: `7a227e22d86f00d8ab5078690de37de794774cdab636e7db374c5adbd0985126`  
Formele primaire classificatie: **gemengd bewijs**

## Conclusie

ECP-2 levert het eerste duidelijk compositionele protocol in deze reeks op, maar nog geen robuust eindmodel. De interventie geeft iedere factor een afzonderlijk slot, laat de zenders zelf een één-op-één factor-slotpermutatie kiezen en oefent uitsluitend consensus uit op die vrije keuze. Alle interventiezenders kwamen per seed op dezelfde slotbinding uit.

De gemiddelde exacte reconstructie van volledig nieuwe kleur-vormcombinaties stijgt ten opzichte van de gepaarde controle van 58,2% naar 66,1%. Vier van vijf seeds verbeteren, maar de exacte eenzijdige gepaarde tekenomklaptoets is met vijf paren niet significant (`p = 0,15625`). De universele vertaler stijgt van 66,2% naar 77,6%, verbetert in alle vijf seeds en heeft `p = 0,03125`.

Toch halen slechts twee van vijf interventieseeds alle vooraf vastgelegde drempels. De zwakke seeds bevatten nog botsingen in de vrij geleerde symbolen voor factorwaarden. Slotstructuur alleen garandeert dus niet dat elke waarde een unieke atoomcode krijgt.

## Primaire resultaten

| Seed | Bekend | Slechtste bekend paar | Compositionele validatie | Nieuwe testparen | Slechtste testpaar | Universele vertaler | Classificatie |
|---:|---:|---:|---:|---:|---:|---:|---|
| 11 | 100,0% | 100,0% | 97,0% | 86,4% | 76,6% | 98,2% | sterk |
| 23 | 100,0% | 100,0% | 100,0% | 100,0% | 100,0% | 100,0% | sterk |
| 37 | 89,6% | 89,6% | 55,5% | 35,4% | 21,9% | 75,0% | gemengd |
| 53 | 91,7% | 91,7% | 72,7% | 55,3% | 49,2% | 51,6% | gemengd |
| 71 | 100,0% | 100,0% | 40,1% | 53,2% | 34,4% | 63,3% | gemengd |
| **Gemiddeld** | **96,3%** | **96,3%** | **73,0%** | **66,1%** | **56,4%** | **77,6%** | **gemengd** |

## Gepaarde vergelijking

| Metriek | Zonder bindingsconsensus | Met bindingsconsensus | Verschil | Seeds beter | Exacte eenzijdige `p` |
|---|---:|---:|---:|---:|---:|
| Nieuwe testparen | 58,2% | 66,1% | +7,9 procentpunt | 4/5 | 0,15625 |
| Universele vertaler | 66,2% | 77,6% | +11,4 procentpunt | 5/5 | 0,03125 |
| Sterke seeds | 1/5 | 2/5 | +1 seed | — | — |

De slotarchitectuur zelf is krachtig: ook de controle zonder consensus haalt gemiddeld veel meer compositionele generalisatie dan ECP-1. De gepaarde vergelijking isoleert uitsluitend het extra effect van bindingsconsensus, niet het effect van de structurele slotbias.

## Interpretatie

ECP-2 denkt aantoonbaar buiten woorden en alfabetten: een bericht is een reeks van vier discrete symbolen, en zowel symboolgebruik als slotvolgorde zijn arbitrair. De code is op goede seeds perfect injectief, heeft topografische overeenkomst 1,0 en kan nieuwe combinaties exact samenstellen.

Het succes is echter niet volledig spontane taalemergentie. De architectuur schrijft vooraf voor dat de vier betekenisfactoren in vier afzonderlijke slots moeten worden uitgedrukt. Zij kiest niet wat de slots betekenen, maar krijgt wel de grammaticale vorm “één factor per positie” opgelegd. Dit experiment toont daarom dat een efficiënte niet-menselijke conventie betrouwbaar kan worden **geleerd binnen een compositioneel kanaal**, niet dat neural agents die kanaalstructuur zonder inductieve bias zelf ontdekken.

## Geldigheid en integriteit

- Interventie en controle gebruiken exact dezelfde split, vijf seeds, architectuur en trainingsbegroting; alleen bindingsconsensus verschilt.
- ECP-0- en ECP-1-testparen zijn uitgesloten. De ECP-2-testmatching bleef tijdens ontwikkeling en modelselectie gesloten.
- Alle definitieve zenders en ontvangers draaiden in geïsoleerde processen; ontvangers kregen alleen de vier harde symbolen.
- Husselcontroles bleven onder de vastgelegde grens en consistente symboolhernoeming behield alle voorspellingen.
- Per arm zijn 81.920 episodes en 309 artefacten gecontroleerd; alle hashes kwamen byte voor byte overeen.
- De twintig zender-seedcombinaties lagen boven alle honderd permutatienullen voor topografische overeenkomst.

## Besluit voor ECP-3

ECP-3 behoudt de vrij geleerde slotpermutatie, maar maakt de atoomcode binnen iedere factor injectief: verschillende factorwaarden moeten verschillende symbolen gebruiken. De symbolen zelf blijven betekenisvrij en vrij gekozen. Populatieconsensus wordt uitgebreid van slotbinding naar atoomcode. Een volledig nieuwe validatie- en testmatching sluit zowel eerdere testparen als de reeds gebruikte ECP-2-validatieparen uit.

Het doel is niet een hogere topscore — ECP-2 heeft al een seed met 100% — maar stabiliteit over seeds. Pas bij minstens vier van vijf sterke seeds, bij voorkeur vijf, is dit een kandidaat voor het eerste bruikbare basismodel.

## Lokale bewijsbestanden

De niet-versiebeheerde bronruns staan lokaal onder `runs/ecp2-confirmatory/intervention/20260718T013310Z-ecp2-experiment/` en `runs/ecp2-confirmatory/control/20260718T013310Z-ecp2-experiment/`. Daar staan de gepaarde vergelijking, post-hocanalyses en alle per-seedartefacten.
