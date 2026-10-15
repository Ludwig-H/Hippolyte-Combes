# Vérification de la seconde relecture — 15 octobre 2026

La vérification matérielle est terminée sur l’édition PDF de **416 pages**. Elle accompagne une seconde collation visuelle des **186 photographies** après l’étude comparative de l’écriture ; elle ne certifie pas les tracés que les notices laissent ouverts.

## Couverture et provenance

- Quatre lots : 48 + 46 + 46 + 46 = 186 revues uniques, toutes au niveau `collation_ligne_a_ligne`, avec les noms de photographies correspondants.
- 49 vues comportent une modification des lignes par rapport à l’état figé `ec1d94a`. Le manifeste cumulé contient 186 notices et 94 vues dont les lignes diffèrent des modules de base ; ces nombres décrivent des comparaisons différentes.
- Les valeurs `originals` des quatre lots correspondent exactement à la base figée. Les huit empreintes des propositions (quatre lots archivés et quatre lots nouveaux) et les trois empreintes des modules sources sont contrôlées.
- Les 186 historiques ont été conciliés avec les apports parallèles conservés. Le commit `06c8ea0` est préservé dans la chaîne Git.
- Les vues 091 et 093 conservent des lignes et des marges identiques. Les numéros restent ceux des photographies, sans foliation physique inventée.
- 88 extraits de 54 photographies : rectangles, dimensions, empreintes et égalité exacte des pixels avec les JPEG décodés contrôlés par `indexer_extraits.py`. Aucun contraste, redimensionnement ou retouche. La concordance indexe 618 occurrences de l’état antérieur et ne certifie pas leurs lectures.
- Les quatre faces écrites des lettres des 25–26 novembre 1918 ont été recollationnées séparément : 104 lignes, coordonnées et réserves conservées. Les deux empreintes des témoins ont été vérifiées. Les phrases de captivité sans témoin ont été retirées des citations et des commentaires concernés.

## Construction et PDF

Commandes exécutées, dans cet ordre :

```bash
python edition_philologique/ecriture_combes/indexer_extraits.py
python edition_philologique/assembler_relecture.py
python edition_philologique/parse_all_186.py
python edition_philologique/generate_edition.py
cd edition_philologique
xelatex -halt-on-error -interaction=nonstopmode carnet_hippolyte_combes.tex
xelatex -halt-on-error -interaction=nonstopmode carnet_hippolyte_combes.tex
python verifier_edition.py --log /tmp/hc_relecture/xelatex_pass1.log --log /tmp/hc_relecture/xelatex_pass2.log
```

Résultat du vérificateur : **PASS**, 186 enregistrements et revues, exports JSON/Markdown/LaTeX cohérents, 186 paires en vis-à-vis. Chaque transcription occupe une page physique paire et son fac-similé la page suivante. Les légendes restent avec leur image ; les 186 JPEG incorporés correspondent par SHA-256 aux sources allégées attendues. Aucun texte hors des limites physiques détecté, à la tolérance de 2 points du vérificateur. Les deux journaux finaux ne contiennent ni caractère manquant, ni boîte débordante, ni commande inconnue, ni erreur LaTeX.

Les pages rendues des vues 048 (texte et fac-similé), 097, 142, 177 et d’une partie des lettres ont également été inspectées. Les réserves, ajouts, numéros de lignes et registres de commentaire restent lisibles. Les crochets en début de ligne des nouvelles citations sont protégés dans le LaTeX afin de les imprimer comme du texte.

La structure exécutable du générateur est identique à celle de `06c8ea0` après masquage des chaînes : seules ses chaînes de présentation, de contexte et de citations ont changé. Les trois modules de transcription sont inchangés. Les liens locaux des nouveaux dossiers ont été contrôlés et `git diff --check` est passé. Deux archives sont conservées sans nettoyage : les espaces de contexte du diff unifié et la fin de fichier du premier compte rendu 032–062. Leurs exceptions de contrôle des espaces sont limitées à ces deux chemins dans `.gitattributes`.

## Refus des régressions

Deux simulations en mémoire, sans écriture dans le dépôt, ont vérifié les refus suivants :

- valeur originale altérée : `Proposition non conciliée : 001/historique` ;
- empreinte de module altérée : `Module modifié : data_scans_001_074.py`.

L’ancien `assembler_revision.py` a également été exécuté après intégration : il refuse la suppression de la seconde passe, demande `assembler_relecture.py` et laisse le manifeste inchangé. Le nouveau vérificateur contrôle aussi les empreintes de la base figée, de la première révision archivée et de la capture des apports concurrents.

## Empreintes de livraison

| Artefact | SHA-256 |
| --- | --- |
| `edition_philologique/carnet_hippolyte_combes.pdf` | `e7c43105339c9d5067f2546f1d7ebacd78cf21a12db383580c775724ed3f527d` |
| `transcriptions/transcription_integrale_186_scans.json` | `2658a78e37e431f46e30a6c411bc16fb2148a36187ddfac847ceb3c0dc2d860c` |
| `edition_philologique/revision_2026_10/corrections_validees.json` | `2f5118e0223d95c7b96e0ac9b3ec2e8e18de04d6a1095a295ff9e8f052450ad5` |
| `edition_philologique/ecriture_combes/index_extraits.json` | `d63caeac1d941ccd1db7e005bb1bcd8e4faded27ffc5c7aa72a010ef4011e476` |
| `edition_philologique/relecture_integrale_2026_10/annexes_25_26_novembre_1918.json` | `6c01fb92f942145365f3fb361b9075587a878ace1b9096cc7c58591ef6a57f20` |

Ces contrôles établissent la traçabilité et la cohérence des artefacts. Les incertitudes paléographiques, les rapprochements prosopographiques et les divergences documentaires restent ceux explicités dans l’édition et le registre.
