# Hippolyte Combes (1876–1970) — Livre-Journal de campagne (1916–1917)

Ce dépôt réunit les photographies du *Livre-Journal* d’Hippolyte Combes (**25 juillet 1916 – 30 avril 1917**), son édition philologique, diplomatique et critique intégrale en vis-à-vis, ainsi que les archives familiales et militaires associées. Né à Millau le **14 août 1876** selon son acte de naissance (n° 395) et décédé le **2 septembre 1970** à l’**Hôtel du Centre** à **Saint-Chély-d’Apcher** (Lozère), **Hippolyte Combes** est professeur d’anglais et interprète militaire auprès de l’Armée britannique (*152nd Company A.S.C.* de la *18th Eastern Division*, puis services d’approvisionnement et d’achats des XIIIe et Ve Corps).

## Architecture de l’édition philologique et diplomatique en vis-à-vis

L’édition ([`edition_philologique/carnet_hippolyte_combes.pdf`](edition_philologique/carnet_hippolyte_combes.pdf), 437 pages au format maniable `155 × 225 mm` à pagination arabe continue depuis la page 1) présente successivement :

1. **Prolégomènes scientifiques et historiques** :
   - Biographie universitaire et militaire d’Hippolyte Combes (1876–1970) et **carte vectorielle générale (TikZ)** des théâtres d’opérations (Flandres, Artois, Somme) et des permissions (Paris, Toulouse, Millau).
   - **Trois arbres généalogiques et prosopographiques (TikZ)** présentant l’ensemble des protagonistes : (I) la famille Combes–Alric ; (II) la famille de sa fiancée Marguerite Calmels et ses alliances (branches Calmels, Cartairade, Crouzet, Vincens, Delcamps, Layrals et Faure) ; (III) l’entourage militaire et universitaire (officiers britanniques et français, collègues interprètes et universitaires).
   - **Étude codicologique et paléographique** du manuscrit (`Couverture` et `Folio 1 recto` à `Folio 93 recto`), justification explicite du caractère purement éditorial et arbitraire de la division en sept chapitres (fondée sur les grands déplacements géographiques d’Hippolyte Combes), et exposé des principes d’édition.
2. **Sept chapitres introduits chacun par une double page d’ouverture** :
   - **Page de gauche (paire)** : résumé analytique détaillé du chapitre et introduction historique et philologique.
   - **Page de droite (impaire)** : **carte vectorielle TikZ détaillée** de l’itinéraire, des cantonnements et des tournées d’Hippolyte Combes durant le chapitre, accompagnée de photographies d’archives.
3. **Édition intégrale en vis-à-vis de la Couverture et des Folios 1 recto à 93 recto (186 doubles pages)** :
   - **En-tête courant** indiquant en permanence **le mois et l’année en cours** (*Juillet 1916* à *Avril 1917*) ainsi que le numéro de folio (`Folio X recto` ou `Folio X verso`).
   - **Page de gauche (paire / verso)** :
     - **Transcription diplomatique fidèle** restituant la mise en page du manuscrit : soulignements autographes des dates, des rappels de mois/année dans l’angle supérieur droit et des sous-titres de lieux dans les relevés de dépenses (`\underline{...}`), traits horizontaux de séparation entre deux journées ou au-dessus du bloc comptable (`\cline{1-1}`), lettres suscrites (`8\textsuperscript{H}`, `Marg\textsuperscript{te}`, `lieut\textsuperscript{t}`, `R. Fus\textsuperscript{rs}`, etc.), crochets comptables `[ ... ]` et numérotation marginale de 5 en 5 lignes.
     - **Apparat critique marginal** composé dans le prolongement horizontal exact de chaque ligne annotée.
     - **En bas de page, jusqu’à trois registres dépourvus d’intitulés répétitifs mais immédiatement distingués par des filets horizontaux et un décrochement typographique franc** :
       1. *Premier registre (commentaire critique interne, au fer à gauche, présent uniquement lorsque des remarques codicologiques ou structurelles excèdent l’apparat marginal)* ;
       2. *Deuxième registre (apparat des **loci paralleli** en latin, au fer à gauche, renvoyant simultanément au folio du carnet `f° X r°/v°` et à la page exacte du PDF `p. Y`)* ;
       3. *Troisième registre (commentaire historique concis et dense, composé avec un retrait général de `5 mm` sur la gauche)*.
   - **Page de droite (impaire / recto)** : **fac-similé photographique complet** du folio manuscrit correspondant en regard immédiat de sa transcription.
4. **Annexes documentaires et double index final** :
   - **Annexe I** : correspondance de guerre inédite et pièces justificatives (1916–1918).
   - **Annexe II** : état signalétique des services et table synoptique des folios (`Couverture` et `Folio 1 recto` à `Folio 93 recto`).
   - **Index des noms de personnes (*Index nominum*)** et **Index des noms de lieux (*Index locorum*)**, renvoyant chacun simultanément au numéro de folio dans le carnet (`f° X r°/v°`) et au numéro de page exact dans le fichier PDF (`p. Y`).

## Consulter et compiler l’édition

- [Édition complète en PDF (`edition_philologique/carnet_hippolyte_combes.pdf`)](edition_philologique/carnet_hippolyte_combes.pdf)
- [Source LaTeX générée (`edition_philologique/carnet_hippolyte_combes.tex`)](edition_philologique/carnet_hippolyte_combes.tex)
- [Transcription diplomatique en Markdown (`transcriptions/transcription_integrale_186_scans.md`)](transcriptions/transcription_integrale_186_scans.md)
- [Base structurée JSON (`transcriptions/transcription_integrale_186_scans.json`)](transcriptions/transcription_integrale_186_scans.json)

Pour régénérer les exports, recompiler l’édition PDF (en deux passes XeLaTeX pour résoudre toutes les références croisées `\pageref{fol:N}`) et exécuter le script de vérification :

```bash
python3 edition_philologique/parse_all_186.py
python3 edition_philologique/generate_edition.py
cd edition_philologique
xelatex -halt-on-error -interaction=nonstopmode carnet_hippolyte_combes.tex
xelatex -halt-on-error -interaction=nonstopmode carnet_hippolyte_combes.tex
cd ..
python3 edition_philologique/verifier_edition.py
```

## Dossiers du dépôt

- [`edition_philologique/`](edition_philologique/) : code source Python et LaTeX de l’édition philologique (`parse_all_186.py`, `commentaires_et_loci.py`, `cartes_et_index.py`, `generate_edition.py`, `verifier_edition.py`), illustrations et dossiers de collation.
- [`transcriptions/`](transcriptions/) : exports JSON et Markdown intégraux des 93 folios et témoins de travail.
- [`scans_haute_qualite/`](scans_haute_qualite/) et [`scans_compresses/`](scans_compresses/) : clichés numériques haute résolution et clichés optimisés du manuscrit original.
- [`archives_militaires/`](archives_militaires/) : fiche matricule, parcours, photographies et correspondance de guerre (1916–1918).
- [`biographie_et_famille/`](biographie_et_famille/) : notices familiales, actes d’état civil, documents de carrière et portraits.
