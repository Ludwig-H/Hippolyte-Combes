# Vérification de l’édition du 15 octobre 2026

L’assemblage contient 186 notices de contrôle, 170 notices modifiées par rapport aux modules sources et 71 vues dont le tableau de transcription est corrigé. Les trois modules sources ont été conservés dans l’état partagé contrôlé, avec leurs empreintes ; les valeurs antérieures des propositions restent archivées séparément. Aucune branche de travail supplémentaire n’a été créée.

## Résultat reproductible

La chaîne `assembler_revision.py`, `parse_all_186.py`, `generate_edition.py`, puis deux passes de XeLaTeX s’est terminée avec succès. Le [vérificateur](../verifier_edition.py) contrôle :

- les 186 identifiants et notices, les empreintes des modules et des propositions, et la concordance du JSON avec sa reconstruction ;
- les 186 sections Markdown et doubles pages LaTeX, les fichiers photographiques et les renvois des notes aux lignes ;
- les 186 paires de pages du PDF : transcription sur une page paire, fac-similé immédiatement suivant, légendes complètes sur cette même page ;
- l’identité SHA-256 du JPEG réellement embarqué avec la copie correspondante dans `scans_compresses` ;
- l’absence de texte ou d’image dépassant les limites des pages, avec une tolérance de 2 points, et l’absence d’erreur LaTeX, de caractère manquant ou de boîte débordante signalée dans les deux journaux de compilation.

Résultat : **186 paires conformes dans un PDF de 413 pages**. Empreinte du PDF vérifié : `0778a7cff6bf1f18467998fb81507c54a012c5e10a25126107656ff080657c58`. Une nouvelle compilation peut modifier cette empreinte, notamment par les métadonnées datées du PDF.

Commande du contrôle effectué, depuis la racine :

```bash
python edition_philologique/verifier_edition.py \
  --log /tmp/hc_reprise/xelatex_pass1.log \
  --log /tmp/hc_reprise/xelatex_pass2.log
```

Les chemins temporaires décrivent cette exécution. Pour une nouvelle compilation, fournir ses propres journaux avec `--log`, ou laisser le vérificateur lire le journal LaTeX du volume.

## Contrôles complémentaires

Les pages des vues 002, 030, 053, 062 et 181 ont été examinées visuellement dans le PDF reconstruit, ainsi que le fac-similé de la vue 053. Les liens locaux des notices et des documents de méthode ont été vérifiés.

Un essai de modification concurrente du texte de la vue 002 a provoqué l’arrêt attendu de la couche de correction. Les contrôles ponctuels du parseur distinguent `J. à` (*jusqu’à*) de `J.` (*jeudi*), `R.F.A.` de `R.F.`, et ne développent pas `c. temps` en centimes ni `y` en conjonction espagnole. Les mentions éditoriales de biffure et de groupes incertains sont préservées. Les lettres suscrites sont rendues en exposant par les deux fonctions de préparation LaTeX.

Ces contrôles établissent la cohérence des fichiers livrés et de leur présentation. Ils ne certifient ni la résolution de tous les déchiffrements ni toutes les identifications historiques : les réserves du [registre de collation](REGISTRE_COLLATION.md) restent partie intégrante de l’édition.
