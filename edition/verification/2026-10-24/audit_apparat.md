# Audit de l'apparat, des renvois et de l'index — 24 octobre 2026

Base : `ce61fc3`. Travail dans la copie détachée `/tmp/hc_audit_20261024/repo`, sans modification du dossier principal ni de ses retouches non commitées.

## Portée des contrôles

- Les 186 fichiers YAML se chargent et leur balisage s'analyse ; 185 sont édités, le cliché 093 étant un doublon. Le texte édité compte 3 711 lignes.
- Les 3 580 entrées d'apparat initiales (3 569 sur les pages actives) ont été contrôlées par rapprochement du lemme et de la ligne correspondante après retrait du balisage. Aucun lemme absent ni numéro de ligne hors limites. Une première passe avant le redémarrage du serveur avait également relu les notes hors abréviations et emprunts ; la reprise a vérifié les défauts signalés et leurs corrections.
- Les 1 207 attestations manuelles des 132 personnes et 248 lieux de l'index pointent toutes vers une ligne existante d'une page active. Un filtrage des différences de graphie entre noms courts et lignes a produit 108 cas, relus : abréviations usuelles, désignations familiales et identifications déjà signalées comme incertaines. Ce contrôle ne démontre pas à lui seul l'identité de toutes les personnes.
- Les 568 renvois complets sous la forme « f. n r/v » repérés dans les champs `historique` et `critique` ont été confrontés à la foliotation. Un renvoi visait un verso non photographié ; il est corrigé ci-dessous. Cette vérification des cibles ne garantit pas la pertinence de chaque rapprochement historique.
- Photographies examinées ponctuellement pour SFl (033, première passe), nᵒˢ (120, première passe et seconde lecture par le responsable), et le mot biffé proposé « autos » (098, reprise). Il ne s'agit pas d'une nouvelle collation intégrale des 185 pages photographiées.

## Corrections retenues

| Fichier / feuillet | Correction | Preuve et portée |
|---|---|---|
| 026, f. 13 v°, commentaire | Renvoi à Maurin du 6 août : f. 7 r° au lieu de f. 6 v°. | Le passage « Après-midi, retrouvé Maurin » est au cliché 013, ligne 11 ; la concordance donne f. 7 r°. Le f. 6 v° n'est pas photographié. |
| 033, f. 17 r°, l. 9 | Suppression de « (Saint-Pol) » dans la note de lecture de SFl. | La ligne 6 donne Saint-Flochel et l'entrée d'abréviation développe correctement SFl. La parenthèse était contradictoire ; l'analyse des lettres reste conservée. |
| 098, f. 49 r°, l. 16 | Rétablissement d'une note sur le caractère conjectural du mot proposé « autos » sous une biffure très chargée. | La photographie montre la forte obstruction par l'encre. Le moteur n'ajoute automatiquement que « biffé », sans expliquer la fragilité de la lecture. Aucun changement à la conjecture diplomatique elle-même. |
| 098, titre, critique et commentaire | Beauquesne reste une identification probable, sans être présenté comme intégralement lisible. | La transcription est « Beauq » suivi d'une lacune, et l'apparat envisage aussi Beaucourt-sur-l'Hallue. Le titre reçoit « (?) » ; la critique décrit « Beauq… » ; le commentaire dit « probablement à Beauquesne ». |
| 120, f. 60 r°, l. 11 | nᵒˢ développé « numéros (du programme) », au lieu de « nos ». | Les lettres os sont suscrites ; le passage décrit la deuxième partie d'un programme de concert. Transcription conservée. |
| 163, f. 81 v°, commentaire | Renouleau remplace Raucoule dans le récit historique. | La transcription, l'apparat et l'index retiennent Renouleau, avec incertitude ; Raucoule demeure une variante dans l'apparat. Le commentaire conserve explicitement la réserve. |
| 186, f. 93 r°, critique | « Dernière page écrite photographiée du carnet ». | La codicologie constate seulement que le recto est photographié. Coordination avec l'audit des introductions : l'absence d'image du verso ne prouve pas qu'il est blanc. |
| index.yaml, notices Calmels et Pizzi | Les numéros internes 055, 060, 092 deviennent f. 28 r°, f. 30 v°, f. 46 v°. | Correspondances contrôlées dans codicologie.yaml ; les notices sont imprimées et doivent utiliser la foliotation éditoriale. |

## Résultat et limites

Après correction : 3 581 entrées d'apparat dans les 186 fichiers, dont 3 570 sur les 185 pages actives ; aucun défaut d'ancrage de lemme ; aucun renvoi complet de critique/historique vers une face non photographiée. Les 186 champs `transcription` sont strictement identiques à ceux de `ce61fc3`. `git diff --check` passe sur les données modifiées.

Les résultats de la régénération des exports et du PDF sont consignés dans le bilan général de cet audit. La vérification ne remplace ni une expertise codicologique de l'objet matériel, ni le dépouillement de toutes les sources historiques citées. Les lectures incertaines, les noms non identifiés et les conjectures déjà déclarées restent tels quels.
