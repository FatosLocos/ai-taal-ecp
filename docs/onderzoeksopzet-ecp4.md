# Onderzoeksopzet ECP-4 — theoretisch minimale 10-bitcode

Status: **bevroren vóór confirmatieve testtoegang**  
Bevroren: 18 juli 2026 om 06:11:20 UTC  
Interventieconfiguratie: `config/ecp4.yaml`  
SHA-256: `c335483534248eda96094ceea7ff49cd3270256fdfff6e01824654a886bc6e17`  
Controleconfiguratie: `config/ecp4-control.yaml`  
SHA-256: `84c1024d49c9d2aff34fb56dbcabf41c9af76dc2ba478760e42d1098afa777c8`

## Vraag

Kan het ECP-protocol van 16 naar exact 10 bits worden gecomprimeerd — de bronondergrens van de uniforme wereld — zonder compositionele generalisatie, populatiecompatibiliteit of universele vertaling te verliezen?

## Waarom 10 bits minimaal is

De wereld bevat `8 × 8 × 4 × 4 = 1024 = 2^10` equiprobabele betekenissen. Iedere ondubbelzinnige code vereist daarom minstens `log2(1024) = 10` bits.

ECP-4 gebruikt vier lokale factoralfabetten:

| Factor | Waarden | Bits |
|---|---:|---:|
| Kleur | 8 | 3 |
| Vorm | 8 | 3 |
| Grootte | 4 | 2 |
| Textuur | 4 | 2 |
| **Totaal** | **1024 combinaties** | **10** |

Iedere zender kiest vrij een permutatie van factor naar slot en binnen iedere factor een vrije permutatie van waarde naar lokaal symbool. De semantiek van slots en symbolen is dus niet vooraf benoemd. Wel is de minimale factorstructuur als architectuurbias opgelegd.

## Factor-geïsoleerde ontvanger

ECP-3 had één uitbijter doordat een algemene GRU kleur en vorm als gezamenlijke contextregel kon memoriseren. ECP-4 laat iedere factoruitgang exact één vrij geleerd slot lezen. Een wijziging in een ander slot kan die uitgang architectonisch niet beïnvloeden. Iedere ontvanger leert zijn eigen harde slotpermutatie en deelt geen parameters met zenders of andere ontvangers.

De universele vertaler en nieuwe overdrachtsontvangers gebruiken dezelfde factor-geïsoleerde architectuur, maar worden pas na het bevriezen van het zenderprotocol onafhankelijk getraind.

## Laatste onafhankelijke kleur-vormsplit

Na ECP-0 tot en met ECP-3 waren 48 van de 64 kleur-vormparen gebruikt als validatie of test. De resterende zestien paren vormen exact twee perfecte matchings. Zij zijn expliciet, zonder sampling, verdeeld over:

- acht ontwikkelvalidatieparen;
- acht verzegelde confirmatieve testparen.

De split heeft SHA-256 `0f8b5505e1a3dceb0c87005a32d6bcffd39c66a6bb4246102617c92a8915b180`. Na ontzegeling van deze test zijn alle 64 kleur-vormparen minstens eenmaal als validatie of test gebruikt; vervolgonderzoek moet daarom een nieuwe wereld of een orthogonale holdoutfamilie gebruiken.

## Gepaarde 16-bitcontrole

De controle gebruikt exact dezelfde split, vijf seeds, factor-geïsoleerde ontvangers, consensusverliezen, trainingsbegroting en evaluatie. Alleen de zendercode en het kanaal verschillen:

- interventie: lokale alfabetten `8,8,4,4`, exact 10 bits;
- controle: vier globale symbolen uit zestien, 16 bits.

Hierdoor meet de vergelijking of theoretisch minimale compressie prestatiedaling veroorzaakt binnen dezelfde verbeterde decoderarchitectuur.

## Vooraf vastgelegde criteria

Per seed vereist sterk bewijs:

- minstens 97% bekende gemiddelde exacte reconstructie;
- minstens 95% voor het slechtste bekende zender-ontvangerpaar;
- minstens 80% gemiddelde exacte reconstructie op nieuwe testparen;
- minstens 70% exacte reconstructie door de universele vertaler.

ECP-4 geldt als geslaagd minimaal model wanneer:

1. minstens vier van vijf interventieseeds sterk zijn;
2. de interventie exact 10 kanaalbits gebruikt;
3. alle zendercodes injectief en botsingsvrij zijn;
4. alle kanaal- en integriteitscontroles slagen;
5. de gemiddelde testexactheid niet meer dan één procentpunt onder de gepaarde 16-bitcontrole ligt.

Vijf seeds (`11,23,37,53,71`) en een exacte gepaarde tekenomklaptoets over 32 tekencombinaties zijn vooraf vastgelegd. Het ideale resultaat is vijf foutloze seeds, maar de formele succesregel blijft vier van vijf om consistent te zijn met ECP-3.

