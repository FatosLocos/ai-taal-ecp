# Protocolspecificatie ECP-6

## Doel en bereik

ECP-6 encodeert precies één betekenis uit een gesloten productruimte van vier categorische factoren. Het is geen teksttaal en gebruikt geen alfabet, woorden of grammaticale zinnen. De communicatievorm is een structurele tuple van vier lokale gehele getallen plus een gedeelde protocolconventie.

De factorcardinaliteiten zijn:

`kleur:16 × vorm:16 × grootte:8 × textuur:8 = 16.384`.

## Logisch bericht

Een bericht is een tuple `⟦a · b · c · d⟧`. Per protocolinstantie gelden twee conventies:

1. een permutatie die iedere factor aan precies één slot koppelt;
2. per factor een bijectie tussen factorwaarden en lokale symbolen.

De zenders leren deze conventies tijdens training. Ze sturen de conventies niet per bericht mee. Binnen iedere confirmatieve seed maakten alle vier zenders exact dezelfde conventie; tussen afzonderlijke seeds mag de betekenis van slots en symbolen verschillen.

## Wire-formaat

De lokale alfabetgrootte bepaalt de bitbreedte:

- kleur en vorm: ieder 4 bits;
- grootte en textuur: ieder 3 bits.

De vier unsigned bitvelden worden in geleerde slotvolgorde zonder padding aaneengeschakeld. De totale berichtlengte is altijd:

`4 + 4 + 3 + 3 = 14 bits`.

Omdat er `2^14` equiprobabele betekenissen zijn, is dit exact de ondergrens voor iedere verliesloze vaste-lengtecode.

## Concreet voorbeeld

In confirmatieve seed 11 is de slotvolgorde:

`[vorm, kleur, textuur, grootte]`.

De nooit als trainingscombinatie aangeboden testbetekenis `(c0,s9,z0,t0)` krijgt het logische bericht:

`⟦15 · 1 · 3 · 1⟧`.

De wire-representatie is:

`1111 | 0001 | 011 | 001` → `11110001011001`.

Deze bits zijn niet door een mens aan `c0`, `s9`, `z0` of `t0` toegewezen. Hun betekenis bestaat uitsluitend binnen het geleerde codeboek en de slotconventie.

## Decodering door een bestaande ontvanger

Een bestaande ontvanger bewaart de inverse slotpermutatie en vier lokale symbooldecoders. Hij:

1. splitst de 14 bits volgens de factorbreedte van ieder slot;
2. zet ieder bitveld om naar een lokaal symbool;
3. routeert ieder slot naar zijn factor;
4. past de bijbehorende inverse symboolpermutatie toe.

De factoristische architectuur kan voor een factor geen informatie uit een ander slot gebruiken.

## Inductie door een nieuwe lezer

Een nieuwe lezer ontvangt gelabelde trainingsvoorbeelden, maar geen zenderparameters of codeboeken. Hij:

1. berekent de empirische wederzijdse informatie voor iedere factor-slotcombinatie;
2. scoort exhaustief alle 24 mogelijke slotpermutaties;
3. bevriest de best scorende binding;
4. leert per factor de lokale symboolpermutatie.

In alle vijf confirmatieve seeds scoorde de juiste binding 14,0 bits en de nummer twee 8,0 bits. Vanaf 128 gelabelde voorbeelden decodeerde iedere nieuwe lezer de volledige testset foutloos.

## Invarianten

- precies vier logische symbolen;
- precies 14 wire-bits;
- lokale alfabetten `[16,16,8,8]` gekoppeld aan de factor van ieder slot;
- iedere factor gebruikt precies één slot;
- ieder lokaal codeboek is bijectief;
- alle 16.384 betekenissen hebben een uniek bericht;
- wijziging van één factor verandert precies één slot;
- consistente hernoeming van symbolen met de overeenkomstige decoder behoudt alle voorspellingen.

## Grenzen en versiebeheer

ECP-6 veronderstelt dat schema, factorcardinaliteiten en protocolversie vooraf bekend zijn. Nieuwe waarden buiten de lokale alfabetcapaciteit, nieuwe factoren, variabele lengte, foutcorrectie en dynamische protocolonderhandeling vereisen een volgende versie. De 14 bits meten uitsluitend de payload binnen dit gedeelde gesloten schema; transportheaders en het eenmalig leren van de conventie vallen daar niet onder.
