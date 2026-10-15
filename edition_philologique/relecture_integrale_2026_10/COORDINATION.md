# Coordination de la relecture en cours

La seconde relecture demandée par Louis prend pour comparaison l’export du commit `ec1d94a`, conservé dans `base_relecture.json`. Quatre lots nouveaux couvrent001–048,049–094,095–140 et141–186. Les propositions indiquent leurs valeurs antérieures exactes. Les photographies entières sont relues après l’étude préparatoire conservée dans `../ecriture_combes/`.

Des modifications simultanées des anciens lots de `revision_2026_10/`, du générateur et des exports ont été constatées pendant cette relecture. Elles sont conservées et comparées séparément avant l’assemblage final. Le nouveau travail ne modifie pas les trois modules de base.

Le commit parallèle `06c8ea0` est conservé dans l’historique. Les quatre lots nouveaux confrontent ses enrichissements au carnet et aux pièces citées. Les modifications finales de sa vue 001 concernent le cadre biographique et militaire, repris avec distinction des sources dans l’introduction ; celles de 168 sont conciliées avec Debrie. Les propositions parallèles demeurent archivées, y compris lorsqu’elles ont été corrigées ou qualifiées.

Pour poursuivre le travail partagé, ajouter les propositions avec leurs preuves dans un fichier distinct et garder la base figée. `assembler_relecture.py` contrôle les valeurs antérieures avant de régénérer JSON, Markdown, LaTeX et PDF. Il conserve les preuves de la première passe et ajoute celles de la seconde. Aucun push forcé ni branche supplémentaire n’est utilisé.
