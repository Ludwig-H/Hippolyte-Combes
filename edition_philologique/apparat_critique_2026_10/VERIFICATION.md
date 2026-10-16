# Vérification finale, 16 octobre 2026

Les 186 photographies ont chacune une fiche de contrôle d’apparat sur image, avec SHA-256, lignes examinées, observations et réserves. Les quatre lots couvrent 186 vues uniques et contiennent **2 467 entrées**, réparties sur **1 733 lignes annotées** : 1 665 abréviations, 428 emprunts, 147 lectures, 122 dispositions, 42 signes, 33 ajouts, 17 ratures, 7 comptes et 6 observations de syntaxe.

Les lignes de neuf vues sont ajustées : 002, 054, 098, 103, 113, 153, 163, 175 et 185. Les lectures nouvelles réservées portent leur doute dans le texte et l’apparat. Les vues 091/093, deux clichés de la même page, ont des lignes et des apparats identiques.

La construction sans la nouvelle couche reproduit exactement la base `04673ef`. L’assembleur et l’application contrôlent les valeurs antérieures, les empreintes des quatre lots et des sous-lots 001–024/025–048, la révision parente, les 186 photographies et la couverture des lignes. Le vérificateur compare la révision antérieure à l’état antérieur, puis la nouvelle couche à l’export final. Chaque lemme est présent dans sa ligne ; les marques de réserve et de suppression ont une entrée ancrée.

Le rendu conserve toutes les entrées, sans limite par ligne ni fusion entre lignes différentes. Le TeX contient intégralement chaque bloc courant de transcription, d’apparat et de commentaires. Le PDF porte en métadonnées l’empreinte des enregistrements sources, ce qui permet de refuser un PDF périmé malgré des en-têtes restés identiques.

Deux compilations XeLaTeX finales réussissent, sans caractère manquant, erreur ni boîte débordante. Le PDF compte **412 pages**, au format **185 × 270 mm** : le format antérieur faisait déborder 22 vues avec l’apparat complet. Le contrôle vérifie **186 vis-à-vis**, transcription en page paire et cliché immédiatement suivant, identité SHA-256 des JPEG affichés, légendes sur la bonne page et texte dans les limites physiques des pages (tolérance 2 points).

Les pages denses et les corrections matérielles ont reçu un contrôle visuel ciblé. Le décalage initial des notes a été corrigé : leurs premières lignes partagent désormais la ligne de base de la transcription. Les huit pages denses 050 (p. 116), 053 (p. 122), 055 (p. 126), 059 (p. 134), 060 (p. 136), 062 (p. 140), 067 (p. 152) et 090 (p. 198) ont aussi été examinées indépendamment : écart mesuré des premières lignes de base 0,000 point, aucune rognure ni superposition. Voir [le rapport visuel](controle_visuel.json). Les contrôles des vues 002, 037, 098 et 164, entre autres, confirment la présence des deux commentaires inférieurs et l’absence de chevauchement.

Neuf contrôles négatifs réussissent sans écriture de production : faux SHA de lot ou de photographie, lemme absent, ligne hors limites, date antérieure modifiée, vue manquante, ID dupliqué, ordre altéré et appel de l’ancien assembleur. Ce dernier refuse avant toute lecture ou écriture de données. Voir [le rapport](controles_negatifs.json).

Commande finale :

```bash
python edition_philologique/verifier_edition.py \
  --log edition_philologique/apparat_critique_2026_10/xelatex_pass_final1.txt \
  --log edition_philologique/apparat_critique_2026_10/xelatex_pass_final2.txt
```

[Résultat du vérificateur](verification_final.txt), [première compilation](xelatex_pass_final1.txt), [seconde compilation](xelatex_pass_final2.txt) et [empreintes des artefacts et du code](artefacts_sha256.json) sont conservés. Ces vérifications établissent la cohérence des artefacts et du rendu ; elles ne certifient ni une graphie incertaine ni un fait historique extérieur.
