# Runs

De simulator schrijft hier onveranderlijke uitvoerbestanden van ECP-experimenten. Iedere run krijgt een eigen map met minimaal:

- de effectieve configuratie en hash;
- datasetmanifest en hashes;
- model- en softwareversies;
- ruwe berichten en reconstructies;
- metrics en controles;
- een ingevuld experimentrapport.

Runmappen kunnen honderden megabytes groot worden en staan daarom in `.gitignore`. Commit geen checkpoints, geïsoleerde matrices of episodebestanden. Publiceer een compacte, gecontroleerde resultatensnapshot onder `evidence/` en leg de reproductieopdracht vast.
