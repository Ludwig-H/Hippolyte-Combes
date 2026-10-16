# Vérification finale du PDF de conciliation

Contrôle achevé le 16 octobre 2026 après les deux compilations définitives de publication. Aucun fichier du worktree détaché, code ou PDF n’a été modifié par cet audit.

PDF final inspecté : **424 pages**, SHA-256 `23782adbf4141a7f255ca79b0c3ed47c9c110ad403d9406f6f00f4019170d8a8`.

Module d’index vérifié : SHA-256 `892ac2a9145d82a61f2d2367f1f81f1b1d51923183d86a9aa34d354a634bc0ae`.

## Résultat et portée

Les vues **002, 037, 050, 098, 164 et 182**, pages **16, 88, 116, 214, 352 et 388**, restent propres après intégration des filets du développeur principal. Les longues notes augmentent la hauteur de leur rangée ; aucune fusion de notes, note coupée ou superposition n’est visible. Les registres du bas sont distincts et lisibles : trois à la vue 002, deux sur les autres pages lorsque le commentaire critique est vide.

Les **71 départs de notes** sont alignés sur le texte : écart maximal **0,000031 point PDF**, compatible avec la précision de stockage des coordonnées. L’écart minimal entre boîtes de notes est **3,65 points** ; la dernière note reste au moins **41,82 points** au-dessus du filet des registres. Aucun span ne sort des six pages.

Les dix pages d’index ont été contrôlées pour les limites de page ; quatre pages finales ont aussi été examinées visuellement (415, 417, 421, 424). Aucun débordement de page n’a été trouvé. **Aucune référence « ?? » n’apparaît dans le texte extrait des 424 pages.**

Il s’agit d’un contrôle typographique ciblé et d’une vérification des homonymes signalés, **pas d’une nouvelle relecture des 186 photographies du manuscrit ni d’une validation historique exhaustive des index**.

| Vue | Page PDF | Groupes de notes | Écart baseline maximal (pt) | Intervalle minimal entre notes (pt) | Dernière note → filet (pt) |
|---|---:|---:|---:|---:|---:|
| 002 | 16 | 9 | 0.000000 | 3.65 | 144.49 |
| 037 | 88 | 17 | 0.000000 | 3.65 | 87.37 |
| 050 | 116 | 10 | 0.000015 | 4.28 | 168.52 |
| 098 | 214 | 12 | 0.000031 | 3.65 | 99.41 |
| 164 | 352 | 15 | 0.000031 | 3.65 | 41.82 |
| 182 | 388 | 8 | 0.000031 | 3.65 | 130.94 |

Les mesures comparent les origines typographiques des spans PDF, et non les sommets de leurs contours. Elles conservent donc la distinction entre la baseline commune et les contours de glyphes dont la taille varie.

## Références documentaires et homonymes vérifiés

- Madeleine Calmels, Pierre Calmels et l’abbé Jean Crouzet ne reçoivent plus les faux renvois à l’arbre I fondés sur Madeleine Fabre-Hugou, les Pierre Alric/Combes ou Jean Combes. Leurs attestations identitaires de l’arbre II sont conservées.
- Maria domestique des Crouzet reste rattachée à 064 ; Maria Combes est distinctement mentionnée dans les commentaires 132 et 141 et dans l’arbre I. Marie recevant des étrennes reste rattachée à 140 et n’absorbe plus les autres Marie des arbres ou Sainte-Marie.
- L’entrée Fernand, Germaine et Robert Vincens renvoie à l’arbre II, sans absorber le P. Vincens de l’arbre I ni Louis-Fernand Flutre dans le commentaire 168.
- Saint-Michel-sur-Ternoise renvoie aux deux attestations 032 et 037 ; le tram toulousain de 132 n’y figure plus.
- Domqueur cite la carte IV, page 151 ; Talmas cite la carte VII, page 317, sans folio fictif. Les labels généalogiques donnent les pages 7 et 8. Les renvois biographiques annoncent explicitement « Prolégomènes, § I (début p. 5) » : ils ne présentent plus le début d’une section comme la page précise de chaque occurrence.

Les labels contrôlés sont présents et résolus : `genealogie:combes`, `genealogie:calmels`, `genealogie:militaires`, `carte:I`, `carte:IV`, `carte:VII`, `proleg:biographie`.

## Validation de publication

Après les deux dernières compilations (`publication_pass2.txt`), la légende de l’index des lieux distingue désormais les attestations du carnet, les commentaires et les références propres aux cartes ou arbres ; `lect. inc.` est expliqué. Le reliquat éditorial signalé lors du contrôle précédent est corrigé dans ce PDF.

Les 424 pages ne comportent aucune référence « ?? » dans le texte extrait. Les dix pages d’index restent dans leurs limites et les pages 419 et 424 ont été rendues puis revues après cette dernière modification. Les six pages de notes conservent exactement leurs textes, origines typographiques et contours de spans : les 71 mesures ci-dessous restent valides sans refaire une collation des images.

Aucun défaut résiduel n’a été identifié dans le périmètre ciblé de ce contrôle. Cette conclusion conserve les limites annoncées : six mises en page inspectées, homonymes signalés vérifiés et références du PDF contrôlées ; aucune validation exhaustive des lectures ou identifications historiques des 186 vues n’est revendiquée pour ce dernier passage.

## Mesures détaillées des 71 départs de notes

Artefacts : `qa_notes_final.json`, `measurements_final_raw.json`, `qa_index_final.json`, `index_contextes_finaux.json` et rendus sous `final/`. La première compilation reste documentée dans `verification_pass1.md`.

| Vue | Ligne de source | Baseline texte (pt) | Baseline note (pt) | Différence (pt) |
|---|---:|---:|---:|---:|
| 002 | 1 | 126.656006 | 126.656006 | 0.000000 |
| 002 | 2 | 135.981003 | 135.981003 | 0.000000 |
| 002 | 3 | 151.682007 | 151.682007 | 0.000000 |
| 002 | 10 | 216.957001 | 216.957001 | 0.000000 |
| 002 | 15 | 269.958008 | 269.958008 | 0.000000 |
| 002 | 19 | 313.634003 | 313.634003 | 0.000000 |
| 002 | 20 | 322.958984 | 322.958984 | 0.000000 |
| 002 | 21 | 340.061005 | 340.061005 | 0.000000 |
| 002 | 22 | 362.138000 | 362.138000 | 0.000000 |
| 037 | 1 | 127.276001 | 127.276001 | 0.000000 |
| 037 | 4 | 155.251007 | 155.251007 | 0.000000 |
| 037 | 5 | 170.951996 | 170.951996 | 0.000000 |
| 037 | 7 | 195.977997 | 195.977997 | 0.000000 |
| 037 | 8 | 211.679001 | 211.679001 | 0.000000 |
| 037 | 9 | 221.003998 | 221.003998 | 0.000000 |
| 037 | 11 | 242.250000 | 242.250000 | 0.000000 |
| 037 | 12 | 251.575012 | 251.575012 | 0.000000 |
| 037 | 13 | 267.276001 | 267.276001 | 0.000000 |
| 037 | 14 | 276.601013 | 276.601013 | 0.000000 |
| 037 | 17 | 304.575989 | 304.575989 | 0.000000 |
| 037 | 18 | 326.653015 | 326.653015 | 0.000000 |
| 037 | 19 | 335.977997 | 335.977997 | 0.000000 |
| 037 | 20 | 345.303009 | 345.303009 | 0.000000 |
| 037 | 21 | 354.627991 | 354.627991 | 0.000000 |
| 037 | 22 | 376.705994 | 376.705994 | 0.000000 |
| 037 | 25 | 411.057007 | 411.057007 | 0.000000 |
| 050 | 1 | 127.242004 | 127.242004 | 0.000000 |
| 050 | 6 | 178.391006 | 178.391006 | 0.000000 |
| 050 | 7 | 188.553009 | 188.553009 | 0.000000 |
| 050 | 8 | 198.714996 | 198.714996 | 0.000000 |
| 050 | 11 | 242.351013 | 242.350998 | 0.000015 |
| 050 | 12 | 265.664001 | 265.664001 | 0.000000 |
| 050 | 13 | 275.825989 | 275.825989 | 0.000000 |
| 050 | 15 | 309.299988 | 309.299988 | 0.000000 |
| 050 | 18 | 348.898010 | 348.898010 | 0.000000 |
| 050 | 19 | 372.210999 | 372.210999 | 0.000000 |
| 098 | 1 | 126.656006 | 126.656006 | 0.000000 |
| 098 | 11 | 222.501999 | 222.501999 | 0.000000 |
| 098 | 12 | 244.579010 | 244.579010 | 0.000000 |
| 098 | 13 | 261.681000 | 261.681000 | 0.000000 |
| 098 | 14 | 277.382019 | 277.382019 | 0.000000 |
| 098 | 15 | 293.083008 | 293.083008 | 0.000000 |
| 098 | 16 | 302.408020 | 302.408020 | 0.000000 |
| 098 | 19 | 355.888031 | 355.888000 | 0.000031 |
| 098 | 21 | 374.538025 | 374.537994 | 0.000031 |
| 098 | 22 | 390.239014 | 390.239014 | 0.000000 |
| 098 | 23 | 407.341003 | 407.341003 | 0.000000 |
| 098 | 24 | 429.417999 | 429.417999 | 0.000000 |
| 164 | 6 | 161.326004 | 161.326004 | 0.000000 |
| 164 | 7 | 189.779007 | 189.779007 | 0.000000 |
| 164 | 8 | 237.360001 | 237.360001 | 0.000000 |
| 164 | 9 | 253.062012 | 253.062012 | 0.000000 |
| 164 | 10 | 275.139008 | 275.139008 | 0.000000 |
| 164 | 11 | 284.463989 | 284.463989 | 0.000000 |
| 164 | 12 | 300.165009 | 300.165009 | 0.000000 |
| 164 | 14 | 325.190979 | 325.191010 | 0.000031 |
| 164 | 15 | 340.891998 | 340.891998 | 0.000000 |
| 164 | 18 | 383.020020 | 383.020020 | 0.000000 |
| 164 | 21 | 410.995026 | 410.994995 | 0.000031 |
| 164 | 22 | 420.320007 | 420.320007 | 0.000000 |
| 164 | 23 | 429.645020 | 429.645020 | 0.000000 |
| 164 | 24 | 441.566010 | 441.566010 | 0.000000 |
| 164 | 25 | 489.148010 | 489.148010 | 0.000000 |
| 182 | 5 | 163.955994 | 163.955994 | 0.000000 |
| 182 | 11 | 222.501999 | 222.501999 | 0.000000 |
| 182 | 12 | 250.955002 | 250.955002 | 0.000000 |
| 182 | 13 | 260.279999 | 260.279999 | 0.000000 |
| 182 | 14 | 269.605011 | 269.605011 | 0.000000 |
| 182 | 19 | 330.382996 | 330.382996 | 0.000000 |
| 182 | 22 | 371.111023 | 371.110992 | 0.000031 |
| 182 | 25 | 405.462006 | 405.462006 | 0.000000 |

Confirmation finale de publication : `qa_index_final.json` conserve le SHA du PDF et l’identité exacte des spans des six pages contrôlées ; `qa_notes_final.json` conserve les 71 mesures avec le même SHA final.
