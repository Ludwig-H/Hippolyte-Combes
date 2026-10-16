# Hippolyte Combes (1876–1970) — Livre-Journal de campagne

Ce dépôt réunit les photographies du *Livre-Journal* d’Hippolyte Combes, daté du **25 juillet 1916 au 30 avril 1917**, une édition philologique et historique en vis-à-vis et des documents familiaux et militaires. Né à Millau le **14 août 1876** selon son acte de naissance (n° 395) et décédé le **2 septembre 1970** à l’**Hôtel du Centre** à **Saint-Chély-d’Apcher** (Lozère ; date et commune dans `Combes-3-part 2.DOC`, précision de l’établissement issue de la tradition familiale), Combes est professeur d’anglais et interprète militaire auprès de l’Armée britannique.

Après une première collation, une étude comparative de l’écriture a précédé une **seconde relecture intégrale des 186 vues**. Elle apporte des corrections aux lignes transcrites de **49 vues** et concilie les commentaires historiques des 186 vues avec le travail parallèle de l’autre développeur. L’atlas conserve **88 extraits natifs de 54 photographies**, ainsi qu’une concordance des tours de langue. Les lectures qui demeurent ouvertes restent explicitement signalées dans l’édition.

La **révision intégrale de l’apparat critique** est documentée séparément dans le [dossier de contrôle](edition_philologique/apparat_critique_2026_10/README.md) : les 186 vues ont été contrôlées et portent 2 467 entrées à lemmes exacts, avec développements contextuels et réserves explicites. Neuf vues reçoivent aussi un ajustement des lignes. Le PDF adopte le format 185 × 270 mm pour maintenir le vis-à-vis avec l’apparat complet.

## Lire l’édition et ses réserves

- [Édition en PDF](edition_philologique/carnet_hippolyte_combes.pdf), avec transcription et photographie en vis-à-vis, apparat marginal et commentaires.
- [Transcription en Markdown](transcriptions/transcription_integrale_186_scans.md) et [données structurées JSON](transcriptions/transcription_integrale_186_scans.json).
- [Seconde relecture intégrale](edition_philologique/relecture_integrale_2026_10/README.md), [registre des 186 vues](edition_philologique/relecture_integrale_2026_10/REGISTRE_RELECTURE.md) et [atlas de l’écriture et de la langue](edition_philologique/ecriture_combes/README.md).
- [Première passe](edition_philologique/revision_2026_10/README.md), [provenance Gmail et Drive](edition_philologique/revision_2026_10/SOURCES.md) et [sources de la seconde relecture](edition_philologique/relecture_integrale_2026_10/SOURCES_RELECTURE.md).

Les signes `[?]` et les mots suivis d’un point d’interrogation indiquent une lecture proposée ; `[illis.]` signale une séquence non déchiffrée. Les doubles crochets `⟦…⟧` signalent une suppression autographe, dont le contenu peut lui-même rester incertain. Les abréviations, additions, comptes et changements de langue sont conservés et commentés. Les tracés ressemblant à `&` ou à `y` sont examinés occurrence par occurrence.

## Photographies et ordre des vues

Les dossiers [scans_haute_qualite/](scans_haute_qualite/) et [scans_compresses/](scans_compresses/) contiennent chacun 186 JPEG, de `20251126_092853.jpg` à `20251126_111833.jpg`. Les originaux représentent environ 1,10 Go et présentent des dimensions variables : largeurs de 1 940 à 2 816 pixels et hauteurs de 1 872 à 3 660 pixels. Les copies allégées représentent environ 32,7 Mo et facilitent la consultation et la compilation.

**Une vue est une photographie, pas un folio matériel.** Les vues 091 et 093 montrent la même page. L’ordre photographique des vues 063/064 et 112/113 diffère de l’ordre chronologique des entrées. Les anciens numéros recto-verso calculés d’après la succession des fichiers ne constituent pas une foliation vérifiée. La présence de 186 fichiers ne démontre pas la complétude physique du carnet.

## Sources et identifications

La copie autographe de la lettre du **21 février 1916** indique un service dans une compagnie d’*Army Service Corps* de la **18e Division britannique** depuis le mois d’août 1915. Le carnet nomme la **152nd Company A.S.C.** et la *54th Brigade* (vue 066), puis le `Col. Grose` au *Train Office* (vue 090). Le 9 janvier 1917, il rapporte une visite à la **150th Company A.S.C., 18th Division** (vue 121) ; cette visite ne démontre pas une affectation personnelle à cette compagnie. À la vue 016, Combes parle du général **Maxse** avec un éclusier. Un rattachement personnel aux *Irish Guards* n’est pas établi par les pièces examinées.

Le rapport relatif à Morlancourt mentionne un incident survenu « **lundi 2[?] mars** » : le dernier chiffre reste incertain. Le titre de l’annexe retient mars 1916 avec réserve ; une concordance calendaire ne remplace pas la lecture du chiffre et la date de l’incident ne date pas nécessairement la rédaction.

À la vue 142, le cliché donne `visite à l'oncle & tante Thérèse (Layral)`. L’annexe familiale relie Thérèse Cartairade à Charles **Layrals**, notaire à Millau, avec un s final dans cette source. Spagnol est mentionné ailleurs ; son métier de fleuriste reste conjectural. À la vue 168, la nécrologie de René Debrie étaye fortement le rapprochement des instituteurs Flutre avec **Fortuné Flutre** et son fils **Louis-Fernand**, né au **Mesnil-Martinsart** le 21 juin 1892, admis à l’ENS en **1914**, entré en **1919** et agrégé en **1921**. La notice BnF donne **Albert** comme lieu de naissance : la divergence reste signalée sans explication inventée. Les références et limites figurent dans le [dossier des sources](edition_philologique/relecture_integrale_2026_10/SOURCES_RELECTURE.md).

## Données et reproduction de l’édition

Les modules [data_scans_001_074.py](edition_philologique/data_scans_001_074.py), [data_scans_075_130.py](edition_philologique/data_scans_075_130.py) et [data_scans_131_186.py](edition_philologique/data_scans_131_186.py) constituent la transcription de base. Les documents de première transcription conservés dans [transcriptions/](transcriptions/) restent des témoins de travail, distincts des photographies originales.

Les propositions de la seconde passe sont réunies dans [relecture_integrale_2026_10/](edition_philologique/relecture_integrale_2026_10/), avec les états antérieurs archivés. [assembler_relecture.py](edition_philologique/assembler_relecture.py) les consolide avec la première passe dans `revision_2026_10/corrections_validees.json` et vérifie les empreintes des modules sources. [revision_philologique.py](edition_philologique/revision_philologique.py) applique cette couche de corrections en contrôlant les valeurs remplacées. Une modification concurrente de la base doit être conciliée avant un nouvel assemblage.

[assembler_apparat.py](edition_philologique/assembler_apparat.py) consolide la nouvelle révision de l’apparat en conservant la couche précédente comme base gardée. L’ancien assembleur refuse de remplacer cette base une fois l’apparat appliqué.

[parse_all_186.py](edition_philologique/parse_all_186.py) produit les exports JSON et Markdown ; [generate_edition.py](edition_philologique/generate_edition.py) produit le [LaTeX](edition_philologique/carnet_hippolyte_combes.tex), puis XeLaTeX compile le PDF. Ces exports sont générés : les corrections doivent rester traçables dans les données et propositions qui les alimentent.

La reproduction demande Python avec `python-docx`, `Pillow` et `PyMuPDF`, ainsi qu’une installation TeX comprenant XeLaTeX et les paquets utilisés par le document. Depuis la racine du dépôt :

```bash
python -m pip install python-docx Pillow PyMuPDF
python edition_philologique/assembler_apparat.py
python edition_philologique/parse_all_186.py
python edition_philologique/generate_edition.py
cd edition_philologique
xelatex -halt-on-error -interaction=nonstopmode carnet_hippolyte_combes.tex
xelatex -halt-on-error -interaction=nonstopmode carnet_hippolyte_combes.tex
python verifier_edition.py
```

Le contrôle final vérifie la cohérence des données et des exports ainsi que la correspondance des vues dans le PDF. Il complète la lecture des images sans certifier le déchiffrement des passages incertains.

## Documents complémentaires

- [Archives militaires](archives_militaires/) : fiche matricule, parcours, photographies et correspondance de guerre. Le dossier [1st_Irish_Guards/](archives_militaires/1st_Irish_Guards/) fournit des illustrations contextuelles.
- [Biographie et famille](biographie_et_famille/) : notice familiale de Pierre Combes, actes d’état civil, documents de carrière, portraits, correspondance et souvenirs.

La fiche matricule est lue sur son image : cheveux et sourcils bruns, yeux châtains, profession initiale d’étudiant en droit. Sa mention du **24 janvier 1920** concerne le domicile à Montauban et la profession au lycée Ingres ; elle ne fixe pas la date de nomination dans cet établissement. Les transcriptions dérivées et les notices familiales sont confrontées aux pièces originales.
