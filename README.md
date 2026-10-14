# Fonds & Édition Philologique d'Hippolyte Combes (1876–1970)

**Livre-Journal de campagne d'Hippolyte Combes** (*25 juillet 1916 – 30 avril 1917*), soldat au 11e Escadron du Train des Équipages Militaires (11e ETEM) détaché comme interprète militaire auprès du Corps expéditionnaire britannique (*British Expeditionary Force* — *1st Battalion Irish Guards* puis *152nd Company Army Service Corps*, *Guards Division*).

---

## Architecture du dépôt

### 1. Scans du carnet de guerre (186 clichés intégraux)
Le carnet original (*Agenda Buvard du Bon Marché, 1906*, réemployé d'août 1916 à avril 1917) a été intégralement numérisé en **186 clichés** (`20251126_092853.jpg` à `20251126_111833.jpg`), répartis à la racine en deux dossiers :

- **[`scans_haute_qualite/`](scans_haute_qualite/)** : **186 scans originaux en haute définition sans compression** (~1,03 Go au total, résolution native 3060 × 4080 px), destinés à la conservation archivistique et à l'examen paléographique de détail.
- **[`scans_compresses/`](scans_compresses/)** : **186 scans compressés et optimisés** (~31 Mo au total), prêts pour la reconnaissance optique (HTR/OCR), la transcription automatique et l'inclusion rapide dans la compilation LaTeX.

---

### 2. Édition philologique scientifique (`edition_philologique/`)
Le dossier **[`edition_philologique/`](edition_philologique/)** contient l'édition critique et diplomatique intégrale du *Livre-Journal*, conçue sur le modèle des éditions philologiques classiques (inspirée de l'édition des *Thesmophories* d'Aristophane par Louis Hauseux) :

- **[`edition_philologique/carnet_hippolyte_combes.pdf`](edition_philologique/carnet_hippolyte_combes.pdf)** (**399 pages**) : Volume complet compilé en PDF.
- **[`edition_philologique/carnet_hippolyte_combes.tex`](edition_philologique/carnet_hippolyte_combes.tex)** : Code source LaTeX intégral.
- **Principes d'édition et mise en page** :
  - **Double page en vis-à-vis (belle page / fausse page)** :
    - **Page de gauche (paire / verso)** : Transcription diplomatique intégrale linéarisée, avec numérotation marginale de 5 en 5 lignes (`5`, `10`, `15`, `20`, `25`…) à gauche.
    - **Apparat critique marginal à droite** : Placé dans la colonne extérieure droite de la page de gauche, **exactement dans le prolongement horizontal de la ligne concernée**, signalant les ratures (`⟦...⟧`), surcharges, ajouts interlinéaires (`\.../`), graphies phonétiques du « franglais » de tranchée, abréviations militaires et anomalies matérielles du support.
    - **Double niveau de notes en bas de la page de gauche** :
      1. *Commentaire critique, interne à l'histoire du carnet* (codicologie de l'Agenda Buvard 1906, paléographie, dynamique de rédaction au crayon ou à la plume, bilinguisme franco-anglais, comptabilité de popote, psychologie de l'auteur et renvois internes).
      2. *Commentaire historique pertinent* (contexte opérationnel de la *Guards Division* sur la Somme, à Ginchy, Combles, Morval, Lesbœufs, le *Transloy Ridge*, l'hiver 1916-1917, le repli allemand sur la ligne Hindenburg, et prosopographie familiale et militaire).
    - **Page de droite (impaire / recto)** : Fac-similé du scan original en regard direct de sa transcription.
  - **Organisation en sept chapitres thématiques et chronologiques**, chacun précédé d'une notice introductive illustrée et d'un sommaire analytique :
    - **Prolégomènes** : Notice biographique, étude codicologique, principes d'édition et répertoire prosopographique.
    - **Chapitre I** (*Scans #001 à #012*) : *Prélude : Paris, les permissions et le départ (25 juillet – 17 août 1916)*.
    - **Chapitre II** (*Scans #013 à #037*) : *Des Flandres à la Somme : la marche des Irish Guards (18 août – 10 septembre 1916)*.
    - **Chapitre III** (*Scans #038 à #053*) : *L'enfer de Ginchy, Combles et Lesbœufs : l'offensive de septembre 1916 (11 – 30 septembre 1916)*.
    - **Chapitre IV** (*Scans #054 à #082*) : *Les relais de l'Artois et le retour dans la boue de la Somme (1er octobre – 15 novembre 1916)*.
    - **Chapitre V** (*Scans #083 à #117*) : *L'hiver terrible de 1916 : Carnoy, Méaulte et la Noël au front (16 novembre – 31 décembre 1916)*.
    - **Chapitre VI** (*Scans #118 à #164*) : *La Somme glacée et la poursuite vers la ligne Hindenburg (1er janvier – 30 avril 1917)*.
    - **Chapitre VII** (*Scans #165 à #186*) : *À rebours dans l'Agenda 1906 : comptes de popote, adresses, lexique franco-anglais et notes militaires*.
    - **Appendices A & B** : Lettres de guerre (permission du 15 août 1915, lettre de Ginchy du 13 septembre 1916) et état signalétique et des services (matricule 1207, classe 1896, subdivision de Montauban).

---

### 3. Transcriptions structurées (`transcriptions/`)
Le dossier **[`transcriptions/`](transcriptions/)** rassemble les états successifs de la transcription ainsi que la base de données complète des 186 clichés :
- [`transcriptions/transcription_integrale_186_scans.md`](transcriptions/transcription_integrale_186_scans.md) : Transcription diplomatique, apparat critique et commentaires des 186 scans au format Markdown.
- [`transcriptions/transcription_integrale_186_scans.json`](transcriptions/transcription_integrale_186_scans.json) : Base de données JSON structurée des 186 scans (métadonnées, lignes, apparat marginal indexé par numéro de ligne, commentaire codicologique et commentaire historique).
- Documents de travail originaux (`.docx` et `.pdf`) issus des premières campagnes de transcription.

---

### 4. Archives militaires (`archives_militaires/`)
Le dossier **[`archives_militaires/`](archives_militaires/)** regroupe les sources militaires relatives au parcours d'Hippolyte Combes durant la Grande Guerre :
- **[`fiche_et_parcours/`](archives_militaires/fiche_et_parcours/)** : Fiche matricule (AD Tarn-et-Garonne, 1 R 1896, n° 1207), synthèse du parcours militaire (17e Escadron du Train, 11e Escadron du Train détaché à l'Armée britannique, 22e Section de COA).
- **[`photos_militaires/`](archives_militaires/photos_militaires/)** : Photographies d'Hippolyte Combes en uniforme de l'Armée française et aux côtés des soldats britanniques (*1916 sur le front anglais*, portraits en tenue).
- **[`lettres_de_guerre/`](archives_militaires/lettres_de_guerre/)** : Correspondance de guerre (lettres du 15 août 1915 et du 13 septembre 1916 depuis les ruines de Ginchy, *Field Post Office* britannique).
- **[`1st_Irish_Guards/`](archives_militaires/1st_Irish_Guards/)** : Photographies historiques et documentation sur le *1st Battalion Irish Guards* dans la Somme (tranchées, rations, artillerie, chapelle commémorative).

---

### 5. Biographie et archives familiales (`biographie_et_famille/`)
Le dossier **[`biographie_et_famille/`](biographie_et_famille/)** réunit les documents biographiques, généalogiques et littéraires :
- **[`biographie/`](biographie_et_famille/biographie/)** : Synthèse biographique d'Hippolyte Combes (1876–1970), commerçant en tissus et président du Syndicat d'Initiative de Montauban.
- **[`etat_civil_et_actes/`](biographie_et_famille/etat_civil_et_actes/)** : Actes de naissance (Cahors, 12 mai 1876), de mariage (avec Anne-Marie Mercadier, 1903), de décès (Montauban, 15 février 1970) et passeport.
- **[`discours_et_academie_montauban/`](biographie_et_famille/discours_et_academie_montauban/)** : Discours prononcés par Hippolyte Combes (obsèques d'Émile Pouvillon en 1906, monument aux morts de 1870, réception d'André Vergnes à l'Académie de Montauban en 1957).
- **[`portraits_et_lieux/`](biographie_et_famille/portraits_et_lieux/)** : Portraits de jeunesse et de maturité, maison familiale de Saint-Cirq-Lapopie, devanture de la maison de tissus *Hippolyte Combes* (18, place Nationale à Montauban).
- **[`correspondance_familiale/`](biographie_et_famille/correspondance_familiale/)** : Lettres familiales (1940, 1966) et coupures de presse (*La Dépêche*).
- **[`La_Valette/`](biographie_et_famille/La_Valette/)** & **[`Livre_Pierre_Combes/`](biographie_et_famille/Livre_Pierre_Combes/)** : Archives de la propriété de La Valette et souvenirs familiaux de Pierre Combes.