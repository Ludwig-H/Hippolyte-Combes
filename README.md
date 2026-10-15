# Hippolyte Combes (1876–1970) — Livre-Journal de campagne

Ce dépôt réunit les photographies du *Livre-Journal* d’Hippolyte Combes, daté du **25 juillet 1916 au 30 avril 1917**, une édition philologique et historique en vis-à-vis et des documents familiaux et militaires. Né à Millau le **14 août 1876** selon son acte de naissance (n° 395) et décédé le **2 septembre 1970** à l’**Hôtel du Centre** à **Saint-Chély-d’Apcher** (Lozère ; inhumé à Millau), Combes est professeur d’anglais et interprète militaire auprès de l’Armée britannique.

La révision d’octobre 2026 comprend une collation paléographique et une relecture historique sourcée des **186 vues** : **186 notices de contrôle**, **186 notices historiques révisées et sourcées**, dont **72 vues comportant une correction du texte transcrit ou de l’intitulé topographique**. Ces nombres décrivent le travail effectué ; les lectures qui demeurent ouvertes restent explicitement signalées dans l’édition.

## Lire l’édition et ses réserves

- [Édition en PDF](edition_philologique/carnet_hippolyte_combes.pdf), avec transcription et photographie en vis-à-vis, apparat marginal et commentaires.
- [Transcription en Markdown](transcriptions/transcription_integrale_186_scans.md) et [données structurées JSON](transcriptions/transcription_integrale_186_scans.json).
- [Dossier de révision](edition_philologique/revision_2026_10/README.md), [registre des 186 vues](edition_philologique/revision_2026_10/REGISTRE_COLLATION.md), [observations paléographiques](edition_philologique/revision_2026_10/PALEOGRAPHIE.md) et [sources consultées](edition_philologique/revision_2026_10/SOURCES.md).

Les signes `[?]` et les mots suivis d’un point d’interrogation indiquent une lecture proposée ; `[illis.]` signale une séquence non déchiffrée. Les doubles crochets `⟦…⟧` signalent une suppression autographe, dont le contenu peut lui-même rester incertain. Les abréviations, additions, comptes et changements de langue sont conservés et commentés. Les tracés ressemblant à `&` ou à `y` sont examinés occurrence par occurrence.

## Photographies et ordre des vues

Les dossiers [scans_haute_qualite/](scans_haute_qualite/) et [scans_compresses/](scans_compresses/) contiennent chacun 186 JPEG, de `20251126_092853.jpg` à `20251126_111833.jpg`. Les originaux représentent environ 1,10 Go et présentent des dimensions variables : largeurs de 1 940 à 2 816 pixels et hauteurs de 1 872 à 3 660 pixels. Les copies allégées représentent environ 32,7 Mo et facilitent la consultation et la compilation.

**Une vue est une photographie, pas un folio matériel.** Les vues 091 et 093 montrent la même page. L’ordre photographique des vues 063/064 et 112/113 diffère de l’ordre chronologique des entrées. Les anciens numéros recto-verso calculés d’après la succession des fichiers ne constituent pas une foliation vérifiée. La présence de 186 fichiers ne démontre pas la complétude physique du carnet.

## Sources et identifications

La copie autographe de la lettre du **21 février 1916** indique un service dans une compagnie d’*Army Service Corps* de la **18e Division britannique** (*18th Eastern Division*, commandée par le major-général **Sir Ivor Maxse**, vue 016) depuis le mois d’août 1915. Le carnet précise son appartenance au **18th Divisional Train** (vues 035, 090, 150), commandé par le lieutenant-colonel **Daniel Charles Evans Grose** (`Col. Grose`, vue 090), et nomme la **152nd Company A.S.C.** (vue 066, rattachée à la *54th Infantry Brigade*) ainsi que la **150th Company A.S.C.** (vues 121–123), avant son détachement auprès des officiers d’achats de fourrage (*Foraging* / *Army Purchase Board*). Un rattachement personnel aux *Irish Guards* n’est pas établi par les pièces examinées.

Le rapport relatif à Morlancourt mentionne un incident survenu « **lundi 2[?] mars** » : le dernier chiffre reste incertain. Le titre de l’annexe retient mars 1916 avec réserve ; une concordance calendaire ne remplace pas la lecture du chiffre et la date de l’incident ne date pas nécessairement la rédaction.

À la vue 142 (Millau, 4 février 1917, l. 6), la collation sur le cliché haute définition et le croisement avec les archives familiales (`Combes-annexe.DOC`) établissent la lecture `visite à l'oncle & tante Thérèse (Layral)` — identifiant la tante maternelle de Marguerite, Thérèse Cartairade, et son époux Mᵉ Charles Layral, notaire à Millau — au lieu de `(Spagnol)` (fleuriste niçois réglé aux vues 136 et 158). À la vue 168 (`M. & Mme Flutre, instituteurs, au Mesnil. Ont le fils, élève de Normle Supre`), le croisement des monographies locales établit avec certitude l’identification de **Fortuné Ernest Flutre** (né en 1862, instituteur public au **Mesnil-Martinsart** depuis 1888) et de son fils le philologue romaniste **Louis-Fernand Flutre** (né au Mesnil-Martinsart le 21 juin 1892 et mort à Paris le 8 février 1978, élève de l’ENS Lettres promotion 1913 ; la notice BnF indique par approximation le chef-lieu de canton Albert). Les références et limites de l’ensemble des rapprochements figurent dans le [dossier des sources](edition_philologique/revision_2026_10/SOURCES.md).

## Données et reproduction de l’édition

Les modules [data_scans_001_074.py](edition_philologique/data_scans_001_074.py), [data_scans_075_130.py](edition_philologique/data_scans_075_130.py) et [data_scans_131_186.py](edition_philologique/data_scans_131_186.py) constituent la transcription de base. Les documents de première transcription conservés dans [transcriptions/](transcriptions/) restent des témoins de travail, distincts des photographies originales.

Les propositions documentées sont réunies dans [revision_2026_10/](edition_philologique/revision_2026_10/). [assembler_revision.py](edition_philologique/assembler_revision.py) les consolide dans `corrections_validees.json` et vérifie les empreintes des modules sources. [revision_philologique.py](edition_philologique/revision_philologique.py) applique cette couche de corrections en contrôlant les valeurs remplacées. Une modification concurrente de la base doit être conciliée avant un nouvel assemblage.

[parse_all_186.py](edition_philologique/parse_all_186.py) produit les exports JSON et Markdown ; [generate_edition.py](edition_philologique/generate_edition.py) produit le [LaTeX](edition_philologique/carnet_hippolyte_combes.tex), puis XeLaTeX compile le PDF. Ces exports sont générés : les corrections doivent rester traçables dans les données et propositions qui les alimentent.

La reproduction demande Python avec `python-docx`, `Pillow` et `PyMuPDF`, ainsi qu’une installation TeX comprenant XeLaTeX et les paquets utilisés par le document. Depuis la racine du dépôt :

```bash
python -m pip install python-docx Pillow PyMuPDF
python edition_philologique/assembler_revision.py
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
