# Collation du carnet au 15 octobre 2026

Ce dossier rassemble les propositions de correction et leurs preuves photographiques pour les 186 vues du carnet. Il documente une édition de travail : le statut de collation ligne à ligne décrit le contrôle effectué et laisse subsister les réserves de lecture consignées pour chaque vue.

## Les quatre lots

| Vues | Propositions structurées | Explications |
| --- | --- | --- |
| 001 à 031 | [reprise_001_031.json](reprise_001_031.json) | [reprise_001_031.md](reprise_001_031.md) |
| 032 à 062 | [reprise_032_062.json](reprise_032_062.json) | [reprise_032_062.md](reprise_032_062.md) |
| 063 à 124 | [reprise_063_124.json](reprise_063_124.json) | [reprise_063_124.md](reprise_063_124.md) |
| 125 à 186 | [reprise_125_186.json](reprise_125_186.json) | [reprise_125_186.md](reprise_125_186.md) |

Chaque proposition indique le numéro de vue, le fichier photographique, les valeurs antérieures exactes, les modifications et les éléments qui les justifient. Une correction du texte fournit le tableau complet des lignes de la vue. Les notices de contrôle signalent aussi les difficultés restantes lorsque le texte n’est pas modifié. Les développements d’abréviations, identifications de personnes et rapprochements historiques doivent rester distincts des lettres effectivement lues.

La [synthèse paléographique](PALEOGRAPHIE.md) expose les conventions observées, les ratures, les ajouts et la différence entre lecture incertaine et lacune matérielle. Les numéros désignent des photographies, sans foliation physique établie ; 091 et 093 reproduisent notamment la même page.

Le [registre des 186 vues](REGISTRE_COLLATION.md) rassemble les points ouverts. Les [sources et leur provenance](SOURCES.md) ainsi que le [compte rendu de vérification](VERIFICATION.md) documentent la livraison.

## Validation et travail partagé

[base_edition_reprise.json](base_edition_reprise.json) conserve l’état de comparaison utilisé pour cette reprise. [base_sources_sha256.json](base_sources_sha256.json) enregistre les empreintes des trois modules de données. Ces témoins permettent de distinguer les propositions de cette collation des modifications réalisées simultanément sur les sources.

[assembler_revision.py](../assembler_revision.py) confronte les valeurs antérieures de chaque proposition à cet état de comparaison et vérifie les empreintes des modules. Il rassemble ensuite les corrections dans `corrections_validees.json`, avec la provenance des lots, et produit `REGISTRE_COLLATION.md`. Le mot *validées* désigne ici une intégration contrôlée des propositions documentées ; il ne certifie pas un déchiffrement définitif.

Au moment de produire les transcriptions, [revision_philologique.py](../revision_philologique.py) vérifie encore le couple numéro de vue/fichier et les valeurs exactes des champs à remplacer. Si une source a changé, la génération s’arrête pour permettre de confronter la nouvelle lecture, la correction et la photographie. Cette garde évite qu’une révision concurrente soit écrasée silencieusement. Elle ne remplace pas l’examen philologique.

Les modules de transcription restent les sources de base. La couche de correction s’applique lors de la génération par [parse_all_186.py](../parse_all_186.py), puis [generate_edition.py](../generate_edition.py) produit le fichier LaTeX de l’édition. Une correction nouvelle exige de mettre à jour sa preuve et sa réserve éventuelle, puis de régénérer les sorties ; une intervention limitée au PDF ou au Markdown exporté serait perdue à la génération suivante.

## Documents associés

Les exports textuels conservés dans [sources_drive](sources_drive) permettent la comparaison avec l’édition diplomatique et la transcription de la fiche militaire trouvées dans le Drive familial. Ils sont des témoins de travail distincts des photographies autographes. Les sources historiques extérieures sont identifiées dans les propositions qui en dépendent et, pour le dernier lot, dans sa liste `external_sources`.
