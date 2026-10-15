# Fonds & Édition Philologique d'Hippolyte Combes (1876–1970)

**Livre-Journal de campagne de Marie Lucien Hippolyte Combes** (*25 juillet 1916 – 30 avril 1917*), né le 14 août 1876 à Millau (Aveyron), professeur d'anglais et interprète militaire détaché auprès de l'Armée britannique (*18th Division*, *152nd Company A.S.C.*, *XIIIe et Ve Corps*) du 4 mai 1915 au 11 novembre 1918 (Classe 1896, matricule 911, bureau de recrutement de Toulouse).

---

## Architecture du dépôt

### 1. Scans du carnet de guerre (186 clichés intégraux)
Le carnet original (*Livre-Journal* couvert du mardi 25 juillet 1916 au lundi 30 avril 1917) a été intégralement numérisé en **186 clichés** (`20251126_092853.jpg` à `20251126_111833.jpg`), répartis à la racine en deux dossiers :

- **[`scans_haute_qualite/`](scans_haute_qualite/)** : **186 clichés originaux en haute définition** (~1,03 Go au total, résolution native 3060 × 4080 px, ~5,9 Mo par cliché), destinés à la conservation archivistique et à l'examen paléographique de détail.
- **[`scans_compresses/`](scans_compresses/)** : **186 clichés optimisés** (~31,1 Mo au total), prêts pour la reconnaissance optique (HTR/OCR), la transcription automatique et l'inclusion directe dans la compilation LaTeX.

---

### 2. Édition philologique scientifique (`edition_philologique/`)
Le dossier **[`edition_philologique/`](edition_philologique/)** contient l'édition critique et diplomatique intégrale du *Livre-Journal*, conçue en noir sur fond blanc pur sur le modèle des éditions philologiques classiques (inspirée de l'édition des *Thesmophories* d'Aristophane) :

- **[`edition_philologique/carnet_hippolyte_combes.pdf`](edition_philologique/carnet_hippolyte_combes.pdf)** (**484 pages**, ~35 Mo) : Volume complet compilé en PDF (`xelatex`).
- **[`edition_philologique/carnet_hippolyte_combes.tex`](edition_philologique/carnet_hippolyte_combes.tex)** : Code source LaTeX intégral généré par [`edition_philologique/generate_edition.py`](edition_philologique/generate_edition.py) à partir des modules de données [`data_scans_001_074.py`](edition_philologique/data_scans_001_074.py), [`data_scans_075_130.py`](edition_philologique/data_scans_075_130.py) et [`data_scans_131_186.py`](edition_philologique/data_scans_131_186.py).
- **Principes d'édition et mise en page** :
  - **Double page en vis-à-vis sur fond blanc pur (186 doubles pages consécutives)** :
    - **Page de gauche (paire / verso)** : Transcription diplomatique intégrale ligne à ligne, avec numérotation marginale de 5 en 5 lignes (`5`, `10`, `15`, `20`, `25`…) à gauche.
    - **Apparat critique marginal à droite** : Placé dans la colonne extérieure droite de la page de gauche, **exactement dans le prolongement horizontal de la ligne concernée**, signalant les ratures (`⟦...⟧`), abréviations tachygraphiques d'Hippolyte Combes (`ds`, `pr`, `s/`, `j'à`, `lgt`, `tt`, `tjs`, `qq`, `gd`, `bp`, `cme`, `chz`, `cartes ples`), emprunts anglais ou latins (`passim`) et crochets comptables (`in marg. cum unco`).
    - **Double registre de commentaires en bas de la page de gauche, sans intitulés répétitifs mais clairement distingués par des filets horizontaux et un retrait typographique** :
      1. *Premier registre (sous le filet horizontal principal de 0,6 pt, au fer à gauche)* : critique interne, codicologique et paléographique du carnet, introduite par des lemmes gras indexés à la ligne (`l. ...`).
      2. *Second registre (sous un filet horizontal fin de 0,25 pt, avec retrait gauche de 3,5 mm)* : élucidation historique, militaire, topographique et prosopographique (*18th Division*, *Royal Fusiliers*, *Royal Sussex*, *Bedfordshire Regiment*, *152nd Company A.S.C.*, *XIIIe et Ve Corps*, *63rd Royal Naval Division*, *2nd Australian Division*, permissions à Paris, Neuilly, Toulouse et Millau).
    - **Page de droite (impaire / recto)** : Fac-similé pleine page du scan original en regard direct de sa transcription.
  - **Organisation en sept chapitres thématiques et chronologiques**, chacun précédé d'un argument analytique, d'une introduction historique et philologique et d'illustrations d'archives :
    - **Prolégomènes** : I. Destin d'un universitaire rouergat et toulousain auprès de l'Armée britannique (1876–1970) ; II. Histoire matérielle, codicologie et paléographie du *Livre-Journal* ; III. Principes de l'édition philologique en vis-à-vis ; IV. Répertoire prosopographique, militaire et topographique.
    - **Chapitre I** (*Scans #001 à #018*) : *De la vallée de l'Aa aux monts de Flandre avec la 18e Division britannique : Lumbres, Setques, l'Ebenezer Boarding School (Pradelles), le Mont-des-Cats, Bailleul et Steenwerck (25 juillet – 12 août 1916)*.
    - **Chapitre II** (*Scans #019 à #049*) : *De la vallée de la Lys à l'Artois et au front de la Somme : Bac-Saint-Maur, Marquay, Saint-Pol, Raincheval, Acheux et Forceville avec le lieutenant Curtis (13 août – 24 septembre 1916)*.
    - **Chapitre III** (*Scans #050 à #066*) : *La première permission : d'Acheux-Varennes à Paris, Toulouse et Millau (les librairies de la rive gauche, le sautoir d'or chez Pfister, la présentation de Marguerite Calmels et le retour par Neuilly, 25 septembre – 6 octobre 1916)*.
    - **Chapitre IV** (*Scans #067 à #104*) : *L'automne dans la Somme : de Barlette et Ribeaucourt au bivouac boueux d'Albert (Brickfield Area) et au XIIIe Corps à Acheux (6 octobre – 30 novembre 1916)*.
    - **Chapitre V** (*Scans #105 à #127*) : *L'hiver 1916–1917 à Acheux : le jeune capitaine Williams, la crise de Noël et le grand gel (Louvencourt, Senlis-le-Sec, Hérissart, 1er décembre 1916 – 25 janvier 1917)*.
    - **Chapitre VI** (*Scans #128 à #146*) : *La deuxième permission : par Gézaincourt, Amiens et Neuilly vers Toulouse et Millau (les fiançailles rue Alfred-Guibert et l'oncle Léopold à Carcassonne, 26 janvier – 7 février 1917)*.
    - **Chapitre VII** (*Scans #147 à #186*) : *De l'hiver polaire au renouveau printanier : d'Hérissart à Toutencourt (la débâcle des glaces, l'installation chez Marie Lécrivain, la visite aux parents du normalien Louis-Fernand Flutre au Mesnil-Martinsart et l'amitié du sous-lieutenant jersiais Gilbert, 7 février – 30 avril 1917)*.
    - **Annexes I & II** : Édition critique des pièces de correspondance de guerre (copie autographe du 21 février 1916 à un capitaine de la Faculté de Toulouse, rapport du 20 mars 1916 au sous-lieutenant Ferran sur l'incident de Morlancourt, lettre confidentielle du 16 juin 1916 à sa sœur Françoise au Carmel de Périgueux, poème de Beatrice Chilcott, lettres de novembre–décembre 1918 de Saint-Pol, Paris et des Andelys) et état signalétique des services (Classe 1896, Matricule 911, Bureau de recrutement de Toulouse) suivi de la table synoptique des 186 scans.

---

### 3. Transcriptions structurées (`transcriptions/`)
Le dossier **[`transcriptions/`](transcriptions/)** rassemble les états successifs de la transcription ainsi que la base de données intégrale des 186 clichés :
- [`transcriptions/transcription_integrale_186_scans.md`](transcriptions/transcription_integrale_186_scans.md) : Transcription diplomatique, apparat critique et double registre de commentaires des 186 scans au format Markdown.
- [`transcriptions/transcription_integrale_186_scans.json`](transcriptions/transcription_integrale_186_scans.json) : Base de données JSON structurée des 186 scans (métadonnées, lignes vérifiées sur les originaux, apparat marginal indexé par numéro de ligne et double registre de commentaires).
- Documents de travail originaux (`.docx` et `.pdf`) issus des premières campagnes de transcription.

---

### 4. Archives militaires (`archives_militaires/`)
Le dossier **[`archives_militaires/`](archives_militaires/)** regroupe les sources militaires relatives au parcours d'Hippolyte Combes durant la Grande Guerre :
- **[`fiche_et_parcours/`](archives_militaires/fiche_et_parcours/)** : Fiche matricule (Bureau de recrutement de Toulouse, Classe 1896, Matricule 911) et synthèse du parcours militaire (10e R.A.P. à Toulon, détachement à la Mission militaire française attachée à l'Armée britannique du 4 mai 1915 au 11 novembre 1918, 19e Escadron du Train, École militaire préparatoire des Andelys).
- **[`photos_militaires/`](archives_militaires/photos_militaires/)** : Photographies d'Hippolyte Combes au 10e R.A.P. à Toulon (printemps 1915) et en uniforme d'interprète militaire sur le front britannique (1916).
- **[`lettres_de_guerre/`](archives_militaires/lettres_de_guerre/)** : Correspondance de guerre autographe (21 février 1916, 20 mars 1916 à Morlancourt, 16 juin 1916, poème de Beatrice Chilcott, 12 novembre, 25–26 novembre, 28 novembre et 2 décembre 1918).
- **[`1st_Irish_Guards/`](archives_militaires/1st_Irish_Guards/)** : Photographies d'archives britanniques de 1916 utilisées à titre d'illustration contextuelle.

---

### 5. Biographie et archives familiales (`biographie_et_famille/`)
Le dossier **[`biographie_et_famille/`](biographie_et_famille/)** réunit les documents biographiques, généalogiques et littéraires :
- **[`biographie/`](biographie_et_famille/biographie/)** : Biographie d'Hippolyte Combes rédigée par son petit-fils Pierre Combes et notes généalogiques.
- **[`etat_civil_et_actes/`](biographie_et_famille/etat_civil_et_actes/)** : Actes de naissance d'Hippolyte Combes (Millau, 14 août 1876) et de Marguerite Calmels (Millau, 15 avril 1892), passeport britannique de séjour à Nottingham, contrat de location à Nogent-le-Rotrou (17 rue Saint-Hilaire).
- **[`discours_et_academie_montauban/`](biographie_et_famille/discours_et_academie_montauban/)** : Discours prononcés par Hippolyte Combes au lycée Ingres de Montauban (remise des prix de 1924, inauguration du monument aux morts du lycée en 1926) et hommage d'André Vergnes à l'Académie de Montauban.
- **[`portraits_et_lieux/`](biographie_et_famille/portraits_et_lieux/)** : Portraits d'Hippolyte Combes et de Marguerite Calmels, photographie de leur mariage à Millau (25 octobre 1917), portraits de famille et vues de Toulouse (rue du Taur), Brive et Nogent-le-Rotrou.
- **[`correspondance_familiale/`](biographie_et_famille/correspondance_familiale/)** : Lettres familiales (1940, 1966) et coupures de presse (*La Dépêche*).
- **[`La_Valette/`](biographie_et_famille/La_Valette/)** & **[`Livre_Pierre_Combes/`](biographie_et_famille/Livre_Pierre_Combes/)** : Photographies de la maison familiale de La Valette (Saint-Beauzély, Aveyron) et livre de souvenirs de Pierre Combes.
