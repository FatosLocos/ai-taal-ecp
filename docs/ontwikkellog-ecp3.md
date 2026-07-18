# Ontwikkellog ECP-3

De confirmatieve ECP-3-testmatching bleef tijdens alle onderstaande handelingen gesloten.

## Oorzaak uit ECP-2

ECP-2 leerde in iedere seed een gedeelde factor-slotbinding, maar slechts twee van vijf seeds haalden alle drempels. De zwakke seeds hadden geen structureel slotprobleem meer; zij bleven steken in niet-unieke of onvoldoende stabiele symbolen voor afzonderlijke factorwaarden. Daardoor konden zelfs bekende betekenissen in seeds 37 en 53 niet volledig worden onderscheiden.

## Vooraf gekozen reparatie

ECP-3 vervangt de neurale slotkoppen door per factor een vrij geleerde injectieve symbooltoewijzing. De zender mag nog steeds ieder symbool voor iedere waarde kiezen, maar twee waarden binnen dezelfde factor mogen niet samenvallen. De bestaande vrije factor-slotpermutatie blijft behouden. Naast bindingsconsensus wordt dezelfde betekenisvrije populatieconsensus op de zachte atoomcodeboeken toegepast.

Er is één ontwikkelseed gebruikt: seed 11. De trainingsbegroting, populatiegrootte, ontvangerarchitectuur en kanaalcapaciteit zijn gelijk gehouden aan ECP-2.

## Resultaat op train en compositionele validatie

| Metriek | Uitkomst |
|---|---:|
| Bekend gemiddeld | 100,0% |
| Slechtste bekend zender-ontvangerpaar | 100,0% |
| Volledig nieuwe validatieparen | 100,0% |
| Slechtste validatiepaar | 100,0% |
| Universele vertaler op validatie | 100,0% |
| Nieuwe ontvanger met 128 voorbeelden | 94,3% |
| Nieuwe ontvanger met 512 voorbeelden | 99,8% |
| Nieuwe ontvanger met 768 voorbeelden | 100,0% |

Alle vier zenders kozen dezelfde slotvolgorde `[vorm, textuur, grootte, kleur]`. Hun exacte atoomcodeboeken kwamen nog niet overal overeen, maar iedere code bleef injectief en alle zestien zender-ontvangerkoppelingen decodeerden beide dialectvarianten foutloos.

Voor ieder van de vier zenders gelden over de 896 train- en validatiebetekenissen:

- 896 unieke berichten en nul botsingen;
- berichtentropie `9,807` bits, gelijk aan de bronentropie van deze subset;
- gemiddelde berichtafstand exact één bij een minimale betekenisverandering;
- volledige concentratie van zo'n verandering in één positie;
- topografische Spearman-overeenkomst `1,0`.

De technische rooktest, checkpointcyclus, geïsoleerde processen, husselcontrole en consistente symboolpermutatie zijn geslaagd. Alle 29 tests slagen.

## Besluit

Er is geen verdere verfijning toegestaan vóór de confirmatieve test. De ontwikkelvariant behaalt alle doelen zonder de verzegelde matching te openen en is daarom ongewijzigd bevroren als ECP-3-interventie. Een identieke controle schakelt uitsluitend slot- en atoomcodeconsensus uit.

Ontwikkelrun: `runs/ecp3-development/20260718T020325Z-ecp3-development`.
