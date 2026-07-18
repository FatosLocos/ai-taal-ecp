# Ontwikkellog ECP-1

Alle onderstaande varianten gebruikten uitsluitend train en validatie. De nieuwe ECP-1-testmatching bleef gedurende deze ontwerpkeuzes gesloten.

| Variant | Interacties per stap | Bekend gemiddeld | Bekend slechtste | Validatie gemiddeld | Besluit |
|---|---:|---:|---:|---:|---|
| A — willekeurig één paar | 1 | 92,7% | 91,4% | 61,2% | te weinig directe paarupdates |
| B — één zender, alle ontvangers | 4 | 95,9% | 95,1% | 57,3% | stabieler maar onvoldoende bekend |
| C — alle zenders, alle ontvangers | 16 | 99,2% | 98,8% | 77,6% | bevroren voor confirmatief experiment |

## Variant A

Iedere cyclus gebruikte alle zestien paren eenmaal, maar één paar per trainingsstap. Op het beste checkpoint had ieder specifiek paar slechts een fractie van de leerinteracties van een ECP-0-paar. De agents ontwikkelden wel een gedeelde conventie, maar de bekende reconstructie bleef onvoldoende.

Lokaal, niet-versiebeheerd artefact: `runs/20260718T000531Z-ecp1-development/report.md`.

## Variant B

Eén gekozen zender stuurde per stap hetzelfde bericht naar alle vier ontvangers. Dit gaf ontvangers veel ervaring, maar iedere zender nog steeds minder directe updates. De bekende prestatie verbeterde, terwijl validatie niet verbeterde.

Lokaal, niet-versiebeheerd artefact: `runs/20260718T000811Z-ecp1-development/report.md`.

## Variant C

Iedere batch liep door alle zestien zender-ontvangerparen en alle verliezen werden gemiddeld. Er was geen leider, gedeeld gewicht of extra semantisch label. Ieder paar kreeg hiermee dezelfde orde van trainingsblootstelling als ECP-0.

De universele ontvanger behaalde testvrij 78,3% validatie. Een verse ontvanger behaalde met 512 van de 768 trainingsbetekenissen 74,2% validatie en met alle betekenissen 77,9%.

Lokaal, niet-versiebeheerd artefact: `runs/20260718T001224Z-ecp1-development/report.md`.

Na deze run zijn architectuur, leerinstellingen, drempels en datasplitsing bevroren. Latere wijzigingen krijgen een nieuw experiment-ID.
