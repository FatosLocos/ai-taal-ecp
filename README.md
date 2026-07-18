# AI-taal — onderzoek naar emergente communicatie

Dit project onderzoekt of onafhankelijk getrainde AI-agents zelf een communicatieprotocol kunnen ontwikkelen dat voor een afgebakende taak compacter, minder ambigu en beter overdraagbaar is dan menselijke taal.

De eerste versie heet **ECP-0**: *Emergent Communication Protocol, experiment 0*. ECP-0 gebruikt geen woorden of vooraf toegekende symboolbetekenissen. Een zender en ontvanger moeten via vier discrete symbolen een betekenis uit een kunstmatige wereld reconstrueren.

## Onderzoeksvraag

> Kunnen onafhankelijke AI-agents zelf een communicatieprotocol ontwikkelen dat bij gelijke taakprestatie efficiënt, generaliseerbaar, vertaalbaar en overdraagbaar is?

Een protocol geldt binnen dit onderzoek pas als een serieuze nieuwe communicatievorm wanneer het:

1. niet door mensen semantisch is voorgeprogrammeerd;
2. onbekende combinaties kan uitdrukken;
3. door een onafhankelijke vertaler kan worden ontsloten;
4. door nieuwe agents kan worden aangeleerd;
5. aantoonbaar efficiënt is ten opzichte van vaste baselines;
6. uitsluitend het toegestane en volledig gelogde kanaal gebruikt.

## Huidige status

**ECP-6 is de geslaagde schaalreplicatie van het volledig efficiënte protocol.** Alle vijf seeds reconstrueren bekende én volledig nieuwe factorcombinaties voor 100%. De universele vertaler en het slechtste agentpaar halen eveneens 100%. De vooraf vastgelegde classificatie is **sterk bewijs**.

Het protocol gebruikt geen woorden of alfabet, maar vier betekenisvrije lokale symbolen. Voor `16 × 16 × 8 × 8 = 16.384` uniforme betekenissen gebruikt het exact `4+4+3+3=14` bits: de informatietheoretische ondergrens. Voor deze afgebakende taak is dat gemiddeld 23,9 keer compacter dan het Nederlandse tekstsjabloon.

Zie [`docs/resultaten-ecp6.md`](docs/resultaten-ecp6.md) voor de conclusie, [`docs/protocolspecificatie-ecp6.md`](docs/protocolspecificatie-ecp6.md) voor het wire-formaat en [`evidence/ecp6/report.md`](evidence/ecp6/report.md) voor de compacte confirmatieve evidence.

## Verder bouwen

Een nieuwe ontwikkelaar of verse AI-agent kan zonder eerdere chatcontext beginnen. Lees eerst [`AGENTS.md`](AGENTS.md) voor de bindende onderzoeksregels en volg daarna [`docs/AI_AGENT_START.md`](docs/AI_AGENT_START.md) voor installatie, architectuuroverzicht, reproductie en het correct opzetten van ECP-7.

Bijdragen zijn welkom via [`CONTRIBUTING.md`](CONTRIBUTING.md). Grote gegenereerde runs blijven lokaal; compacte verifieerbare resultaten komen onder [`evidence/`](evidence/).

## Bestanden

- [`docs/onderzoeksopzet.md`](docs/onderzoeksopzet.md) — volledige onderzoeksvraag, fasering, metingen en stopcriteria.
- [`docs/experiment-template.md`](docs/experiment-template.md) — vast verslagformat per experimentele run.
- [`docs/resultaten-ecp0.md`](docs/resultaten-ecp0.md) — uitkomsten, hypothesetoetsing en aanbeveling voor stap 2.
- [`docs/onderzoeksopzet-ecp1.md`](docs/onderzoeksopzet-ecp1.md) — vooraf vastgelegde populatieproef en besliscriteria.
- [`docs/ontwikkellog-ecp1.md`](docs/ontwikkellog-ecp1.md) — ontwikkeling die plaatsvond terwijl de ECP-1-testset gesloten bleef.
- [`docs/resultaten-ecp1.md`](docs/resultaten-ecp1.md) — confirmatieve uitkomsten, vergelijking met ECP-0 en aanbeveling voor ECP-2.
- [`docs/resultaten-ecp2.md`](docs/resultaten-ecp2.md) — permutationslots, gepaarde consensusproef en resterende symboolbotsingen.
- [`docs/onderzoeksopzet-ecp3.md`](docs/onderzoeksopzet-ecp3.md) — vooraf bevroren hypothese, split en beslisregels voor het injectieve protocol.
- [`docs/ontwikkellog-ecp3.md`](docs/ontwikkellog-ecp3.md) — ontwikkeling terwijl de ECP-3-testmatching gesloten bleef.
- [`docs/resultaten-ecp3.md`](docs/resultaten-ecp3.md) — sterk bewijs, protocolvoorbeeld, efficiëntie en grenzen van het basismodel.
- [`docs/resultaten-ecp4.md`](docs/resultaten-ecp4.md) — perfecte 10-bitpopulatie en de geïsoleerde vertalerfout.
- [`docs/onderzoeksopzet-ecp5.md`](docs/onderzoeksopzet-ecp5.md) — vooraf bevroren kalibratieproef en orthogonale holdout.
- [`docs/ontwikkellog-ecp5.md`](docs/ontwikkellog-ecp5.md) — gesloten ontwikkeling van exacte bindingsinductie.
- [`docs/resultaten-ecp5.md`](docs/resultaten-ecp5.md) — 5/5 foutloze seeds en volledige efficiëntieanalyse.
- [`docs/protocolspecificatie-ecp5.md`](docs/protocolspecificatie-ecp5.md) — logisch bericht, 10-bit-wireformaat en decoderprocedure.
- [`docs/onderzoeksopzet-ecp6.md`](docs/onderzoeksopzet-ecp6.md) — vooraf bevroren schaalproef voor 16.384 betekenissen.
- [`docs/ontwikkellog-ecp6.md`](docs/ontwikkellog-ecp6.md) — schaalinvarianten en gesloten 14-bitontwikkeling.
- [`docs/resultaten-ecp6.md`](docs/resultaten-ecp6.md) — 5/5 foutloze schaalreplicaties en integriteitsanalyse.
- [`docs/protocolspecificatie-ecp6.md`](docs/protocolspecificatie-ecp6.md) — machinecode, 14-bit-wireformaat en inductieprocedure.
- [`config/ecp0.yaml`](config/ecp0.yaml) — machineleesbare configuratie van stap 1.
- [`config/ecp1.yaml`](config/ecp1.yaml) — bevroren configuratie van de populatieproef.
- [`config/ecp3.yaml`](config/ecp3.yaml) — bevroren configuratie van het eerste geslaagde basismodel.
- [`config/ecp5.yaml`](config/ecp5.yaml) — bevroren configuratie van het volledig efficiënte eindmodel.
- [`config/ecp6.yaml`](config/ecp6.yaml) — bevroren configuratie van de 16× schaalreplicatie.
- [`AGENTS.md`](AGENTS.md) — bindende onderzoeks- en wijzigingsregels voor AI-agents.
- [`docs/AI_AGENT_START.md`](docs/AI_AGENT_START.md) — volledige onboarding voor een verse AI-agent.
- [`evidence/ecp6/manifest.json`](evidence/ecp6/manifest.json) — compacte machineleesbare confirmatieve evidence.
- [`schemas/meaning.schema.json`](schemas/meaning.schema.json) — formaat van een betekenis.
- [`schemas/message.schema.json`](schemas/message.schema.json) — formaat van een agentbericht.
- [`schemas/episode.schema.json`](schemas/episode.schema.json) — formaat van een geëvalueerde aflevering.

## ECP-0 in één minuut

- De wereld bevat `8 × 8 × 4 × 4 = 1024` mogelijke betekenissen.
- Iedere betekenis bestaat uit vier onafhankelijke factoren: kleur, vorm, grootte en textuur.
- De agents zien alleen numerieke categorieën, geen menselijke labels.
- Het kanaal heeft 16 mogelijke symbolen en exact 4 posities: 16 bits per bericht.
- De zender en ontvanger delen geen gewichten, embeddings of toestand.
- 128 betekenissen worden als onbekende kleur-vormcombinaties volledig buiten training gehouden.
- Na training wordt het protocol bevroren en door een derde model vertaald.
- Vijf onafhankelijke trainingsruns voorkomen conclusies op basis van één toevallige code.

De theoretische ondergrens voor het exact onderscheiden van 1024 uniforme betekenissen is 10 bits. ECP-0 gebruikt bewust 16 bits: ruim genoeg om eerst leerbaarheid, compositionaliteit en vertaalbaarheid te testen. Compressie naar 12 bits en daarna richting de 10-bitondergrens hoort bij stap 2.

## Simulator

De reproduceerbare simulator bevat:

1. deterministische datasetgeneratie;
2. afzonderlijke zender-, ontvanger- en vertaalmodellen;
3. discrete evaluatie zonder verborgen nevenkanaal;
4. automatische baselines, controles, metingen en runrapporten.

## Uitvoeren

Vereist: Python 3.12.

```bash
python3.12 -m venv .venv
.venv/bin/pip install -e '.[dev]'
.venv/bin/ecp0 validate
.venv/bin/pytest
```

De drie uitvoermodi hebben bewust verschillende toegang tot de data:

```bash
# 25 stappen: alleen controleren of de hele technische keten werkt
.venv/bin/ecp0 smoke --seed 11

# Volledig trainen op train en validatie; test blijft gesloten
.venv/bin/ecp0 develop --seed 11

# Confirmatief: alle vastgelegde seeds en eenmalige testontzegeling
.venv/bin/ecp0 experiment --unseal-test

# Controleer hashes en vergelijk protocolstructuur met willekeurige koppelingen
.venv/bin/ecp0 analyze runs/<run-id> --permutations 100

# ECP-1 gebruikt dezelfde interface met de populatieconfiguratie
.venv/bin/ecp1 --config config/ecp1.yaml validate
.venv/bin/ecp1 --config config/ecp1.yaml analyze runs/<ecp1-run-id> --permutations 100

# ECP-3: injectieve atoomcodes en geleerde protocolconsensus
.venv/bin/ecp3 --config config/ecp3.yaml validate
.venv/bin/ecp3 --config config/ecp3.yaml analyze runs/<ecp3-run-id> --permutations 100

# ECP-5: theoretisch minimale 10-bitcode met gekalibreerde lezer
.venv/bin/ecp5 --config config/ecp5.yaml validate
.venv/bin/ecp5 --config config/ecp5.yaml analyze runs/<ecp5-run-id> --permutations 100

# ECP-6: 16.384 betekenissen bij de exacte 14-bitondergrens
.venv/bin/ecp6 --config config/ecp6.yaml validate
.venv/bin/ecp6 --config config/ecp6.yaml analyze runs/<ecp6-run-id> --permutations 100
```

Iedere uitvoering schrijft configuratie, omgeving, checkpoints, ruwe berichten, controles, hashes, metrics en een rapport naar een nieuwe map onder `runs/`.
