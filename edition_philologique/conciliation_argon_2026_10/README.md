# Conciliation avec Gemini 4 Argon — 16 octobre 2026

Cette révision prolonge la collation intégrale et le [répertoire de l’écriture de Combes](../ecriture_combes/README.md). Elle conserve la composition de Gemini : format 155 × 225 mm, sept chapitres, trois registres en bas de page, trois arbres, huit cartes et deux index. Les derniers réglages de filets et de schémas de `eb681bb` sont intégrés.

## Décisions appliquées

Les 186 fiches ont été comparées à l’édition relue antérieure. L’examen direct supplémentaire porte sur 19 photographies pour les lectures, complétées par les contrôles d’images indiqués dans les propositions historiques et les métadonnées. Ce dossier ne présente pas cette comparaison comme une nouvelle lecture indépendante des 186 images.

- 13 fiches d’apparat : réserves rétablies, gloses précisées, 22 lignes restaurées pour la vue 002 (« Toute nuit »), et « Tip » expliqué à nouveau dans la vue 050. Le total est de 2 437 entrées pour 3 737 lignes.
- 95 notices historiques : 49 correctifs avérés et 46 rétablissements de réserve. Les 47 propositions facultatives restent consignées, sans application automatique. Les acquis récents de Gemini concernant Flutre et Labit sont conservés.
- 33 fiches de métadonnées : 24 titres et 16 champs de lieux corrigés ; le mois de la vue 089 est également remis à novembre 1916.
- 13 paragraphes d’introductions ou de résumés sont corrigés localement ; deux critiques codicologiques cessent d’attribuer sans preuve un écart chronologique à la disposition ou à la rédaction du manuscrit.

Au total, 111 fiches reçoivent des corrections gardées portant sur 166 champs. La base témoin conserve aussi les affirmations corrigées : elle sert à contrôler les changements, pas à certifier toutes ses lectures.

## Renvois et présentation

Les 453 loci, comprenant 852 cibles, reposent sur des lemmes et positions exacts dans les lignes transcrites. Titres, notices et champs de lieux ne créent aucun locus. Les rapprochements lexicaux ou thématiques sont distingués d’une identité personnelle assurée ; les lectures réservées et les ratures restent signalées. La double photographie 091/093 est traitée comme une seule page logique pour les rapprochements ordinaires.

Les index distinguent les attestations du carnet, les identifications du commentaire (`Comm.`) et les mentions des arbres, cartes ou prolégomènes. Les listes de pages proposées ne forcent aucune occurrence. Vingt-deux vedettes omises sont ajoutées sur des mentions littérales ; une occurrence d’un prénom seul dans un arbre ne suffit pas à identifier une personne.

La foliotation `1r–93r` est un repérage éditorial de la séquence photographique. Elle ne démontre ni 93 feuillets matériels distincts ni leur disposition originale. Les conventions de soulignement, d’exposants et de filets ne sont pas déclarées uniformément autographes.

Les notes marginales structurées occupent leur hauteur réelle et commencent sur la ligne annotée. Aucun quota ni fusion automatique ne supprime les explications. Le contrôle visuel reste un échantillon explicite ; il complète les contrôles de pagination et d’intégrité sur l’ensemble du PDF.

## Pièces et reproduction

- [Registre des corrections](REGISTRE.md), [sources historiques](SOURCES.md), [vérifications](VERIFICATION.md).
- [Base Argon témoin](base_argon.json), [corrections appliquées](corrections_validees.json).
- [Lectures](lectures.md), [audit historique des 186 vues](histoire.md), [audit des loci](audit_loci.md), [audit de l’index](audit_index.md).
- Les fichiers `propositions_*.json` gardent les valeurs antérieures, propositions, preuves et décisions. Les observations facultatives ne doivent pas être confondues avec les corrections appliquées.

Depuis la racine du dépôt :

```sh
python edition_philologique/parse_all_186.py
python edition_philologique/generate_edition.py
cd edition_philologique
xelatex -halt-on-error -interaction=nonstopmode carnet_hippolyte_combes.tex
xelatex -halt-on-error -interaction=nonstopmode carnet_hippolyte_combes.tex
cd ..
python edition_philologique/verifier_edition.py
```

`conciliation_argon.py` refuse une modification de la base, des propositions, de la révision parente, des photographies ou des valeurs à remplacer. Une valeur déjà conciliée est acceptée pour permettre une reprise idempotente. Toute nouvelle contribution divergente doit être réconciliée explicitement, afin de préserver le travail du développeur principal.
