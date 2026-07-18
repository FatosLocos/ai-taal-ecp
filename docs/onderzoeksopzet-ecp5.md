# Onderzoeksopzet ECP-5 — robuuste protocolinductie

Status: **bevroren vóór confirmatieve testtoegang**  
Bevroren: 18 juli 2026 om 06:27:09 UTC  
Interventieconfiguratie: `config/ecp5.yaml`  
SHA-256: `5e4bf30517e0edbe96d5f0b5c666b9b03f6fe8366fd80bcc5ab455d615d11b8b`  
Controleconfiguratie: `config/ecp5-control.yaml`  
SHA-256: `4ee2f8ff314acd6f042c66fd4e81b6beb0c360b979f585f5d00b0e9df6ed2582`

## Vraag

Kan een nieuwe universele lezer de arbitraire slotgrammatica van het perfecte 10-bitprotocol betrouwbaar induceren wanneer de discrete factor-slotpermutatie exact uit gelabelde trainingsberichten wordt gekalibreerd?

## Interventie

Voor iedere combinatie van vier factoren en vier slots wordt de empirische wederzijdse informatie berekend. Er zijn slechts `4! = 24` geldige één-op-éénpermutaties. De interventie kiest exhaustief de permutatie met de hoogste totale informatie en bevriest die binding voordat de vier symbooldecoders worden getraind.

De procedure:

- leest alleen berichten en betekenislabellen uit de toegestane trainingsset;
- opent geen validatie- of testbetekenissen;
- leest geen zenderparameters, codeboeken of verborgen toestand;
- schrijft geen symboolbetekenissen voor;
- bepaalt uitsluitend welke berichtpositie statistisch bij welke factor hoort.

De gepaarde controle leert dezelfde binding opnieuw met de bestaande straight-throughgradiënten. Alle overige code, data, seeds en trainingsbudgetten zijn identiek.

## Orthogonale verzegelde test

Omdat na ECP-4 alle kleur-vormparen als validatie of test waren gebruikt, schakelt ECP-5 vooraf over op een grootte-textuurholdout:

- 512 trainingsbetekenissen;
- 256 betekenissen uit vier volledig achtergehouden validatieparen;
- 256 betekenissen uit vier andere, verzegelde testparen.

Kleur en vorm variëren volledig binnen ieder achtergehouden paar. De split-SHA-256 is `cc487fd9042c5190bee93278c4be5180363f46a46d0e8af2f9d7d75a4f173140`.

## Criteria

Per seed blijven de ECP-3/4-drempels gelden: 97% bekend gemiddeld, 95% voor het slechtste bekende paar, 80% compositionele testexactheid en 70% universele vertaalexactheid.

ECP-5 is geslaagd wanneer:

1. minstens vier van vijf interventieseeds sterk zijn;
2. de gemiddelde populatie- en vertaalexactheid ieder minstens 95% zijn;
3. ieder bericht exact 10 bits gebruikt en alle codes botsingsvrij zijn;
4. alle kanaal- en artefactcontroles slagen;
5. de gekalibreerde vertaler in minstens vier van vijf seeds beter presteert dan de ongekalibreerde controle of daarmee gelijk eindigt op 100%.

Seeds `11,23,37,53,71` en de exacte gepaarde tekenomklaptoets zijn vóór testtoegang vastgelegd.

