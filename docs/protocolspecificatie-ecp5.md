# Protocolspecificatie ECP-5

## Logisch bericht

Een betekenis bestaat uit vier categorische factoren met cardinaliteiten `8,8,4,4`. Een bericht bevat vier lokale symbolen. Het protocol bevat per seed twee duurzame conventies:

1. een permutatie van factoren naar berichtslots;
2. per factor een permutatie van waarden naar lokale symbolen.

Deze conventies horen bij het bevroren protocol en worden niet in ieder bericht meegestuurd, zoals grammatica en woordenboek bij menselijke taal evenmin per zin worden herhaald.

## Wire-formaat

Voor ieder slot is uit de factorbinding bekend hoeveel bits nodig zijn:

- kleur of vorm: 3 bits;
- grootte of textuur: 2 bits.

De vier lokale symbolen worden in slotvolgorde als unsigned bitvelden aaneengeschakeld. De totale lengte is altijd 10 bits. Er is geen padding, eindteken of lengteveld nodig.

Voor seed 11:

- slotfactoren: `[grootte, textuur, kleur, vorm]`;
- bericht: `[0,3,5,4]`;
- bitvelden: `00 | 11 | 101 | 100`;
- wire: `0011101100`.

## Decodering

Een bestaande ontvanger bewaart de inverse factor-slotpermutatie in zijn checkpoint. Een nieuwe lezer krijgt gelabelde trainingsvoorbeelden en:

1. berekent voor iedere factor-slotcombinatie de empirische wederzijdse informatie;
2. scoort alle 24 één-op-éénpermutaties;
3. bevriest de beste binding;
4. leert per factor uitsluitend de lokale symboolpermutatie.

De ontvanger kan geen informatie uit niet-geselecteerde slots gebruiken. Daardoor kan hij geen contextregel tussen factoren memoriseren.

## Invarianten

- exact vier logische symbolen;
- exact 10 wire-bits;
- één factor per slot en één slot per factor;
- ieder factorcodeboek is een harde permutatie;
- geen twee betekenissen delen een bericht;
- één factorwijziging verandert exact één slot;
- consistente hernoeming binnen het protocol verandert de semantiek niet.

## Protocoluitbreiding

Nieuwe waarden kunnen alleen worden toegevoegd als het lokale alfabet nog capaciteit heeft of opnieuw wordt onderhandeld. Een volledig nieuwe factor vereist een nieuwe slot- en wireversie. ECP-5 optimaliseert dus een gesloten factorschema; dynamische schema-evolutie valt buiten deze versie.

