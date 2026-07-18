# Onderzoeksopzet ECP-6 — schaalbaarheid op de informatiegrens

Status: **bevroren vóór confirmatieve testtoegang**  
Bevroren: 18 juli 2026 om 06:58:14 UTC  
Configuratie: `config/ecp6.yaml`  
Configuratie-SHA-256: `994ca086e1542e4608fec935ec5b72471b2e2cf73c2193f99ab6997044c40133`

## Vraag

Blijft het in ECP-5 bevestigde, universeel leesbare protocol volledig correct wanneer de betekenisruimte zestienmaal groter wordt, terwijl de berichten exact op de nieuwe theoretische ondergrens van 14 bits blijven?

## Schaalvergroting

De wereld bevat vier onafhankelijke factoren:

- 16 kleuren;
- 16 vormen;
- 8 groottes;
- 8 texturen.

Daarmee zijn er `16 × 16 × 8 × 8 = 16.384 = 2^14` equiprobabele betekenissen. Het factorlokale bericht gebruikt vier slots met alfabetgroottes `[16,16,8,8]`. De breedtes zijn `[4,4,3,3]` bits en tellen op tot exact 14 bits. Een verliesloze vaste code kan voor deze wereld niet korter zijn.

## Gesloten datasplitsing

Kleur en vorm vormen de compositionele holdout. Voor validatie en test zijn elk zestien kleur-vormparen vooraf expliciet vastgelegd. Ieder achtergehouden paar bevat minstens één atomaire waarde uit de nieuwe helft (`8–15`), zodat de schaaluitbreiding daadwerkelijk wordt aangesproken.

| Split | Betekenissen | Kleur-vormparen |
|---|---:|---:|
| Train | 14.336 | 224 |
| Validatie | 1.024 | 16 |
| Confirmatieve test | 1.024 | 16 |

Split-SHA-256: `da751db7853ddbb84f000464c2627d4880eb154aef2158fb958d9a3779117d33`.

## Vastgelegd protocol

De architectuur en inductieregel blijven inhoudelijk gelijk aan ECP-5:

1. vier onafhankelijk geïnitialiseerde zenders produceren een factorlokale permutationslotcode;
2. vier ontvangers worden over alle zestien zender-ontvangerkoppelingen getraind;
3. een nieuwe universele vertaler krijgt uitsluitend gelabelde trainingsberichten;
4. de vertaler bepaalt zijn factor-slotbinding door alle `4! = 24` permutaties op empirische wederzijdse informatie te vergelijken en bevriest de winnaar;
5. overdracht wordt gemeten met 32, 128, 512 en 2.048 voorbeelden.

Er is geen nieuwe controlearm: ECP-5 heeft de bindingsinterventie al rechtstreeks gepaard getoetst. ECP-6 is uitsluitend een vooraf vastgelegde schaalreplicatie van de succesvolle interventie.

## Schaalveilige metingen

Botsingen, entropie, minimale paren en exacte taakprestatie worden over alle geëvalueerde betekenissen berekend. Voor topografische Spearman-correlatie worden bij maximaal 1.000.000 ongeordende betekenisparen uniform zonder teruglegging en met een vaste seed bemonsterd; kleinere werelden gebruiken alle paren. Deze regel is ingevoerd en getest vóór testontzegeling, omdat alle 134.209.536 paren tegelijk materialiseren niet schaalbaar is.

Ruwe geïsoleerde bericht- en voorspellingsmatrices blijven iedere geëvalueerde betekenis afdekken. Episode-JSONL bevat validatie en, pas na ontzegeling, test. De lokale kanaalaudit controleert ieder gelogd bericht op vier symbolen, factorlokale alfabetgrenzen en exact 14 bits.

## Vooraf vastgelegde criteria

De vijf seeds zijn `11,23,37,53,71`. Een seed is sterk wanneer de bestaande ECP-5-drempels worden gehaald: minstens 97% gemiddelde bekende exactheid, minstens 95% voor het slechtste bekende paar, minstens 80% gemiddelde compositionele testexactheid en minstens 70% universele vertaalexactheid.

ECP-6 geldt als volledig geslaagd wanneer:

1. minstens vier van vijf seeds sterk zijn;
2. de gemiddelde compositionele populatieprestatie minstens 99% is;
3. de gemiddelde universele vertaalprestatie minstens 99% is;
4. iedere zender alle 16.384 betekenissen botsingsvrij encodeert;
5. ieder bericht aantoonbaar exact 14 bits gebruikt;
6. alle artefacthashes, schemas, lokale alfabetgrenzen en testontzegelingscontroles slagen.

Na bevriezing worden geen model-, split-, meet- of drempelkeuzes meer aangepast op basis van ECP-6-testuitkomsten.
