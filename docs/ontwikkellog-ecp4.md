# Ontwikkellog ECP-4

De confirmatieve ECP-4-testmatching bleef gedurende alle onderstaande ontwikkeling technisch gesloten.

## Implementatie

ECP-4 voegt twee vooraf gerichte componenten toe:

1. `MinimalPermutationSlotSender`: per factor een vrij geleerde harde permutatie binnen een lokaal alfabet van exact de benodigde grootte;
2. `FactorizedPermutationSlotReceiver`: per factoruitgang een vrij geleerd maar hard geïsoleerd berichtslot.

De transportmetadata, configuratievalidatie en episodeschema's ondersteunen nu protocolspecifieke bitlengtes. Iedere episode wordt aanvullend tegen de actieve configuratie gecontroleerd op exacte berichtlengte, bitlengte en symboolbereik.

## Technische verificatie

De tests bewijzen onder meer dat:

- de vier lokale codeboeken exact `8×8`, `8×8`, `4×4` en `4×4` harde permutaties zijn;
- ieder werkelijk verzonden symbool binnen het lokale factoralfabet valt;
- een factoruitgang onveranderd blijft wanneer een niet-geselecteerd slot wijzigt;
- minimale zender en factorontvanger afzonderlijk door checkpoints en geïsoleerde processen lopen;
- `3+3+2+2 = 10` bits exact gelijk is aan de bronentropie;
- de expliciete validatie- en testmatchings exact de laatste zestien ongebruikte paren zijn.

Alle 34 tests slagen.

## Gesloten ontwikkeluitkomst

Ontwikkelrun: `runs/ecp4-development/20260718T060943Z-ecp4-development`  
Seed: 11

| Metriek | Uitkomst |
|---|---:|
| Bekend gemiddeld | 100,0% |
| Slechtste bekend zender-ontvangerpaar | 100,0% |
| Volledig nieuwe validatieparen | 100,0% |
| Slechtste validatiepaar | 100,0% |
| Universele vertaler op validatie | 100,0% |
| Nieuwe ontvanger, 32 voorbeelden | 100,0% |
| Nieuwe ontvanger, 128 voorbeelden | 100,0% |
| Nieuwe ontvanger, 512 voorbeelden | 100,0% |
| Nieuwe ontvanger, 768 voorbeelden | 100,0% |

Alle vier zenders kozen dezelfde intern bepaalde slotvolgorde `[grootte, textuur, kleur, vorm]` en exact dezelfde atoomcodes. De berichtovereenkomst tussen ieder zenderpaar is 100%. Over de 896 train- en validatiebetekenissen gebruikt iedere zender 896 unieke berichten, zonder botsingen, met topografische overeenkomst 1,0.

De beste toestand werd al bij stap 400 geselecteerd. Er is daarom geen 12-bit-tussenvariant nodig: de directe 10-bitvariant behaalt alle gesloten ontwikkeldoelen.

## Besluit

De 10-bitvariant wordt zonder verdere wijziging bevroren. De gepaarde controle behoudt dezelfde factorontvanger maar gebruikt het 16-bit injectieve ECP-3-kanaal. Geen confirmatief testpaar is vóór deze keuze geëvalueerd.
