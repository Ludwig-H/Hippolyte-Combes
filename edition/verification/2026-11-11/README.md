# Rapport de relecture intégrale et de mise à jour de l'édition du *Livre-Journal* (11 novembre 2026)

Ce rapport détaille l'ensemble des vérifications et retouches apportées à l'édition du *Livre-Journal* d'Hippolyte Combes (25 juillet 1916 – 30 avril 1917), sans modifier l'architecture, la mise en page ni les principes éditoriaux du volume.

---

## 1. Bilan chiffré de la révision

| Indicateur | État antérieur | Nouvel état | Écart / Remarque |
| :--- | :---: | :---: | :--- |
| **Clichés du carnet collationnés** | 186 | **186** | Relecture intégrale lettre à lettre sur [`scans_haute_qualite/`](../../../scans_haute_qualite/) |
| **Clichés des pièces annexes collationnés** | 16 | **16** | Documents 1 à 7 relus sur [`edition/illustrations/lettres/`](../../illustrations/lettres/) |
| **Pages du carnet retouchées** (`pages/*.yaml`) | — | **176 / 185** | 9 pages déjà intégralement conformes au trait près |
| **Lignes de transcription rectifiées** | — | **756 lignes** | Accents, ponctuation, suscriptions, soulignements, ratures et mots |
| **Nombre total de lignes du carnet** | 3 712 | **3 713** | Scission conforme au manuscrit au f. 90 v° ([`181.yaml`](../../donnees/pages/181.yaml#L13-L14)) |
| **Lectures signalées incertaines (`\inc{}`)** | 385 | **350** | −35 conjectures résolues avec certitude sur les scans HD |
| **Notes d'apparat critique** | 1 217 | **1 182** | 74 lemmes ajustés, 54 notes devenues sans objet retirées, 22 ajoutées |
| **Index des noms de personnes** | 133 entrées | **174 entrées** | +10 notices nouvelles et +31 renvois (surnoms, parenté, prénoms) |
| **Index des noms de lieux** | 248 entrées | **285 entrées** | +9 sous-lieux nouveaux et +28 renvois directs |
| **Pagination de [`livre_journal.pdf`](../../livre_journal.pdf)** | 496 pages | **498 pages** | +2 pages dues au développement des index ; divisions toujours au recto |
| **Imposition de [`livret_A4.pdf`](../../livret_A4.pdf)** | 31 cahiers | **32 cahiers** | 32 cahiers de 16 pages ; contrôle [`verifier.py`](../../src/verifier.py) : **0 erreur** |

> [!NOTE]
> L'historique détaillé de chaque rectification apportée au carnet a été consigné page par page sous la clé `collation_2026_11` dans les 176 fichiers correspondants de [`edition/donnees/relecture/`](../../donnees/relecture/).

---

## 2. Méthodologie et critères paléographiques de la collation

La collation intégrale des **186 photographies haute définition** du carnet et des **16 photographies des pièces de guerre** a confirmé le diagnostic formulé au départ :

1. **Traitement rigoureux des accents (déport latéral à droite vs absence réelle)** :
   - Dans l'écriture rapide d'Hippolyte Combes, les accents aigus, graves et circonflexes ainsi que les trémas sont très fréquemment **déportés de 0,5 à 1,5 lettre vers la droite** (au-dessus de la consonne suivante, voire en fin de mot). De nombreux accents parfaitement tracés à la plume et conformes à l'orthographe française avaient ainsi été omis : par ex. `journée` ([`010.yaml`](../../donnees/pages/010.yaml#L18)), `Fév. '17`, `à 6^{H}15, cédant`, `Thérèse`, `Rues désertes` ([`142.yaml`](../../donnees/pages/142.yaml#L8-L15)), `Méricourt`, `Dégel`, `Croûtes` ([`153.yaml`](../../donnees/pages/153.yaml#L13-L24)), `étoilée` ([`155.yaml`](../../donnees/pages/155.yaml#L17)), `Pâques` ([`178.yaml`](../../donnees/pages/178.yaml#L8)), `Laviéville`, `Hénencourt` ([`181.yaml`](../../donnees/pages/181.yaml#L16-L26)).
   - Inversement, lorsque le zoom haute résolution montre un espace interlinéaire entièrement vierge de tout trait diacritique (omission courante chez le scripteur pressé, surtout à l'initiale ou sur les participes et prépositions), les accents indûment normalisés ont été retirés pour respecter la fidélité diplomatique : par ex. `s'elève l'eglise` ([`037.yaml`](../../donnees/pages/037.yaml#L31)), `brise legère`, `Verdures etincelantes` ([`051.yaml`](../../donnees/pages/051.yaml#L12-L13)), `reciproque` ([`056.yaml`](../../donnees/pages/056.yaml#L14)), `boise` ([`069.yaml`](../../donnees/pages/069.yaml#L16)), `Dejeuné`, `Apres dejeuner`, `Mange` ([`109.yaml`](../../donnees/pages/109.yaml#L12-L17)).
2. **Ponctuation autographe et filets de clôture** :
   - Restitution des points, virgules, points-virgules, deux-points, apostrophes (`l'air` [`025.yaml`](../../donnees/pages/025.yaml#L11), `qu'hier` [`103.yaml`](../../donnees/pages/103.yaml#L9), `m'attendant` [`132.yaml`](../../donnees/pages/132.yaml#L23), `'17` [`165.yaml`](../../donnees/pages/165.yaml#L8)), traits d'union (`tête-à-tête` [`133.yaml`](../../donnees/pages/133.yaml#L13)) et parenthèses fermantes (`ferme)` [`031.yaml`](../../donnees/pages/031.yaml#L12)).
   - Distinction systématique entre simples tirets cadratins/demi-cadratins (`–`, `—`) et longs traits horizontaux de fin de développement (`\trait`), par ex. aux ff. 8 v° ([`016.yaml`](../../donnees/pages/016.yaml#L14)), 29 v° ([`058.yaml`](../../donnees/pages/058.yaml#L12-L18)), 84 r° ([`168.yaml`](../../donnees/pages/168.yaml#L12)) et 85 r° ([`170.yaml`](../../donnees/pages/170.yaml#L24)).
3. **Suscriptions, soulignements, ratures et surcharges** :
   - Restitution des finales suscrites omises : `mission f^{se}` ([`010.yaml`](../../donnees/pages/010.yaml#L10)), `Sept^{bre}` ([`035.yaml`](../../donnees/pages/035.yaml#L8), [`044.yaml`](../../donnees/pages/044.yaml#L8)), `g^{de}` ([`056.yaml`](../../donnees/pages/056.yaml#L11)), `cath^{le}`, `appart^{t}` ([`060.yaml`](../../donnees/pages/060.yaml#L11-L15)), `ext^{t}` ([`067.yaml`](../../donnees/pages/067.yaml#L12), [`155.yaml`](../../donnees/pages/155.yaml#L17)), `2^{de} division`, `1^{ères}` ([`092.yaml`](../../donnees/pages/092.yaml#L17-L24)), `L^{t}` ([`109.yaml`](../../donnees/pages/109.yaml#L13)), `instrum^{ts}` ([`119.yaml`](../../donnees/pages/119.yaml#L21)), `réparat^{on}` ([`122.yaml`](../../donnees/pages/122.yaml#L17)), `prof^{r}` ([`130.yaml`](../../donnees/pages/130.yaml#L12)), `9^{H}` / `6^{H}` / `11^{H}` ([`133.yaml`](../../donnees/pages/133.yaml#L16), [`142.yaml`](../../donnees/pages/142.yaml#L12-L20)), `mar^{al} logis` ([`163.yaml`](../../donnees/pages/163.yaml#L16-L18)), `fort^{t}` ([`164.yaml`](../../donnees/pages/164.yaml#L9), [`172.yaml`](../../donnees/pages/172.yaml#L21)), `V^{th} army H.Q.` ([`177.yaml`](../../donnees/pages/177.yaml#L11)), `1^{ers}` ([`181.yaml`](../../donnees/pages/181.yaml#L18)).
   - Surcharge d'en-tête mensuel restituée au f. 29 v° : `\sl{\sur{Sept}{Oct}obre /16}` ([`058.yaml`](../../donnees/pages/058.yaml#L8)).
4. **Disposition matérielle des lignes** :
   - Au f. 90 v° ([`181.yaml`](../../donnees/pages/181.yaml#L13-L14)), la date `\sl{19 Jeudi}.` occupe seule sa ligne sur le feuillet, suivie à la ligne suivante d'un alinéa `\ind Tout le jour, ciel couvert. Qq averses.` : la ligne fusionnée a été scindée en deux, et les numéros de lignes de l'apparat comme des 17 attestations d'index de cette page ont été décalés de `+1`.

---

## 3. Principales restitutions textuelles dans le carnet

Outre les rectifications fines d'accents, de ponctuation, d'accords pluriels et de suscriptions, la relecture sur les clichés haute définition a permis de restituer **144 passages** comportant une différence lexicale, chiffrée ou structurelle. Les plus significatifs pour le sens et le commentaire historique sont réunis ci-dessous :

| Feuillet (cliché) | Lecture antérieure | Lecture restituée sur le manuscrit | Portée philologique et historique |
| :--- | :--- | :--- | :--- |
| **f. 3 v°** ([`007.yaml`](../../donnees/pages/007.yaml#L30)) | `en plein soleil cuisant ai` | `en plein soleil canicul^{re}` | Restitue l'adjectif abrégé *caniculaire* (ajouté à la table des abréviations). |
| **f. 5 v°** ([`011.yaml`](../../donnees/pages/011.yaml#L17)) | `j'entends famille ferme` | `\add{pu} entendre famille ferme` | Restitue l'ajout interlinéaire et l'infinitif autographe. |
| **f. 6 r°** ([`012.yaml`](../../donnees/pages/012.yaml#L29)) | `St Jans-Capel` | `St Jans-Cappel` | Double `p` autographe restitué, supprimant une note de graphie erronée. |
| **f. 11 v°** ([`022.yaml`](../../donnees/pages/022.yaml#L19)) | `Vu \inc{çà} & la. de toits` | `Vu très gd n. de toits` | *Vu très grand nombre de toits* [endommagés], à Fleurbaix / Erquinghem. |
| **f. 13 r°** ([`025.yaml`](../../donnees/pages/025.yaml#L11-L30)) | `de \inc{e} lair` / `\inc{ft} de bien` / `livre` | `ds l'air` / `bp de bien` / `libre` | Résout deux lectures conjecturales et relève le lapsus *libre* pour *livre*. |
| **f. 17 v°** ([`034.yaml`](../../donnees/pages/034.yaml#L11)) | `Terre friable (\inc{boueuse}` | `Terre friable s'accroche` | Restitue le verbe qui gouverne la phrase suivante sur la boue crayeuse d'Artois. |
| **f. 19 r°** ([`037.yaml`](../../donnees/pages/037.yaml#L20-L34)) | `une b. journée` ; `Hair cut – 50 c` ; `Consommations : \inc{50} c` | `très b. journée` ; `Hair cut : \inc{25} c` ; `Consommations : \inc{40} c` | Rectifie les montants des dépenses en marge droite. |
| **f. 20 r°** ([`039.yaml`](../../donnees/pages/039.yaml#L21)) | `à l'\inc{entrée} du` | `à l'\inc{extr^{te}} du` | *À l'extrémité du [village]* (abréviation par suscription). |
| **f. 24 v°** ([`048.yaml`](../../donnees/pages/048.yaml#L28)) | `verte cme litière — Couché bonne nuit` | `verte cme toiture – Passé bonne nuit` | Décrit la toile de tente verte servant de toiture au campement. |
| **f. 26 r°** ([`051.yaml`](../../donnees/pages/051.yaml#L9)) | `au ciel bleu, qq nuages, nettement détachés.` | `au ciel bleu, qq saucisses, nettement detachées.` | Restitue les *saucisses* (ballons captifs d'observation sur le front de la Somme), ajoutées à l'apparat et au glossaire. |
| **f. 27 v°** ([`054.yaml`](../../donnees/pages/054.yaml#L9)) | `nuit passée \inc{ds} \inc{wag^{t}}.` | `nuit passé très rap^{t}.` | *Nuit passée très rapidement* dans l'express Paris–Toulouse. |
| **f. 28 v°** ([`056.yaml`](../../donnees/pages/056.yaml#L13-L29)) | `Marché déjeuné` ; `Remboursé à mes \inc{nièces}` | `Midi – déjeuné` ; `Remboursé à mes voisines` | **Crucial** : lève l'aporie généalogique d'hypothétiques « nièces » inconnues de la famille ; il s'agit de ses *voisines* du 22, rue de Languedoc (sans doute Mmes Delsol, cf. f. 68 v°). Commentaire et sources mis à jour. |
| **f. 31 v°** ([`062.yaml`](../../donnees/pages/062.yaml#L22)) | `\inc{Alle} – Gare – \inc{venu} – \ill \inc{puis}` | `\inc{Allé} \inc{Entré} seul s/ \inc{quais}` | Déchiffrement de la fin de ligne au départ de la gare Matabiau. |
| **f. 34 r°** ([`067.yaml`](../../donnees/pages/067.yaml#L14)) | `et \inc{visé} mon titre de` | `et remis mon titre de` | Lecture certaine (*remis mon titre de permission*), synchronisée dans le titre courant et au f. 35 r° ([`069.yaml`](../../donnees/pages/069.yaml#L26)). |
| **f. 34 v°** ([`068.yaml`](../../donnees/pages/068.yaml#L20)) | `Devant maison, pâture` | `Derrière maison, pâture` | Rectifie la topographie du logement de Barlette. |
| **f. 47 v°** ([`095.yaml`](../../donnees/pages/095.yaml#L21-L30)) | `18^{ie} divon` ; `route de \inc{Lealvillo} ( )` | `18^{th} div^{on}` ; `route de \inc{Lealvillers})` | Élimine la fausse abréviation `18^{ie}` (retirée de la table des abréviations) et rétablit *Léalvillers*. |
| **f. 48 r°** ([`096.yaml`](../../donnees/pages/096.yaml#L9)) | `major \inc{Hughs}` | `major Hughes` | Le `e` est bien présent : retrait du balisage d'incertitude. |
| **f. 51 v°** ([`103.yaml`](../../donnees/pages/103.yaml#L17)) | `F^{me} Royer\add{\inc{fille}}` | `F^{me} Royer\add{et sa fille}` | Lecture complète de l'ajout interlinéaire lors du bombardement d'Acheux. |
| **f. 59 r°** ([`118.yaml`](../../donnees/pages/118.yaml#L17)) | `Chambre chaude –` | `Cherche chambre –` | Cohérent avec le contexte (« Regrette de partir d'ici. Cherche chambre »). |
| **f. 76 v°** ([`153.yaml`](../../donnees/pages/153.yaml#L15-L19)) | `Et ces villages où vecu \inc{jadis} bien vide & triste.` / `\add{une} buée` / `\inc{v.} nombreux` | `Et ces villages m'ont paru bien vides & tristes.` / `\add{encore} buée` / `& nombreux` | Restitue la phrase exacte sur les villages évacués de l'Ancre ; citation mise à jour aux deux endroits d'[`intro_biographie.tex`](../../textes/intro_biographie.tex#L56). |
| **f. 82 r°–v°** ([`164.yaml`](../../donnees/pages/164.yaml#L16-L29), [`165.yaml`](../../donnees/pages/165.yaml#L15-L26)) | `Valet, \inc{est}` ; `tt pensif` ; `Cap. \inc{monté}` ; `archi- / libre` ; `tt penché` | `Valet, ext^{t}` ; `tt penétré` ; `Cap. \inc{Morris}` ; `entier^{t} / libre` ; `tt pénetré` | Relie l'officier partant au capitaine Morris de la veille, rétablit *entièrement libre* (mis à jour dans [`VII.tex`](../../textes/chapitres/VII.tex#L12)) et l'expression récurrente *tout pénétré [de] tristesse / mélancolie*. |
| **f. 85 r°** ([`170.yaml`](../../donnees/pages/170.yaml#L28-L34)) | `Fait parler ces / 2 offs` | `Fait parler clerk / & off.^{r}` | Distingue l'officier et le commis (*clerk*) de la 63rd (Royal Naval) Division ; titre courant et [`VII.tex`](../../textes/chapitres/VII.tex#L16) synchronisés. |
| **f. 88 v°** ([`177.yaml`](../../donnees/pages/177.yaml#L10)) | `1 \inc{staff} du bureau` | `1 ss-off du bureau` | *Un sous-officier du bureau de la Mission française* (et non l'anglais *staff*, retiré du glossaire et du lexique). |

---

## 4. Collation des pièces annexes et mise en cohérence de l'appareil éditorial

### 4.1. Lettres, notes et pièces de guerre ([`annexe_lettres.tex`](../../textes/annexe_lettres.tex))
Les **16 photographies** des sept groupes de documents en annexe ont fait l'objet de la même collation diplomatique :
- **Document 1** (lettre au capitaine et brouillon de rapport d'incident, fin 1915) : restitution du point d'interrogation `vous en souvient il ?` ([l. 20](../../textes/annexe_lettres.tex#L20)), de `attache` en surcharge sur `affecte` et de la rature `\LJdel{nouveau} bureau` au lieu de `\LJdel{membre}` ([l. 22](../../textes/annexe_lettres.tex#L22)) ; dans le rapport d'incident, lecture de `\LJdel{Dans} la matinée` (au lieu de `\LJdel{\LJinc{Avant}} \LJdel{Le} La`), `comptait` récrit sur `voulait`, `retenu` (avec `e` final biffé) et `\LJadd{et que l'interprète etait \LJadd{encore} chz elle}` ([l. 54](../../textes/annexe_lettres.tex#L54)), ainsi que des soulignements et suscriptions aux ff. suivants.
- **Document 2** (lettre du 16 juin 1916 à Marguerite) : restitution du circonflexe bien visible dans l'injonction marginale `Brûle ce feuillet` ([l. 106](../../textes/annexe_lettres.tex#L106)) et vérification de la ponctuation et des accents sur les quatre pages.
- **Documents 3 et 6** (poème anglais et sommaire des *Feuillets de Route*) : au chap. XIII, lecture certaine `Sports \LJadd{games –} & Pastimes des E\LJsup{sh} – Gramophones` (*des English*, au lieu de `de \LJinc{7}\LJsup{th}`, [l. 401](../../textes/annexe_lettres.tex#L401)) ; au chap. XIX, lecture `Sunday service in village \LJinc{church-army}` (tente ou baraque de la *Church Army* anglicane, plutôt que `churchway`, répercutée dans la notice du doc. 3 [l. 139](../../textes/annexe_lettres.tex#L139), dans [`intro_biographie.tex`](../../textes/intro_biographie.tex#L124) et dans [`II.tex`](../../textes/chapitres/II.tex#L11)) ; au chap. XX, `armée Brit\LJsup{sh}` ([l. 413](../../textes/annexe_lettres.tex#L413)).
- **Document 5** (cartes et lettres de novembre–décembre 1918 à Marguerite) : restitution de `Saint-Pol,` ([l. 195](../../textes/annexe_lettres.tex#L195)), du soulignement `\LJsl{(Aveyron)} \LJsl{Millau}` ([l. 211](../../textes/annexe_lettres.tex#L211)), et pose d'ancres `\label` pour l'indexation directe des hypocoristiques `Petitou`, `Margueritou`, `Perlounette` et `Kouine`.
- **Document 7** (notes autographes sur la revue passée par George V et Raymond Poincaré le 25 octobre 1915) : lecture `\LJadd{\LJinc{Daumas}}` (nom propre d'interprète plutôt que `avons`, [l. 572](../../textes/annexe_lettres.tex#L572)), rattachement exact de `\LJadd{deployé}` sous `abaissé` ([l. 587](../../textes/annexe_lettres.tex#L587)), lecture `\LJinc{les} \LJinc{landaus}` (sans point-virgule parasite, [l. 593](../../textes/annexe_lettres.tex#L593)), soulignement `\LJsl{(revue)}` ([l. 605](../../textes/annexe_lettres.tex#L605)), lecture certaine `du rectangle` (le rectangle entouré d'une corde décrit au f. 39, au lieu de `des \LJinc{rechange}`, [l. 619](../../textes/annexe_lettres.tex#L619)), tréma sur `baïonnettes` ([l. 623](../../textes/annexe_lettres.tex#L623)) et abréviation `t.` (*tandis que*, au lieu de `& que`, [l. 634](../../textes/annexe_lettres.tex#L634)).

### 4.2. Introductions, chapitres, glossaire, planche et table des abréviations
Toutes les citations du carnet dans les textes liminaires et les annexes ont été contrôlées par script contre le `diff` intégral des pages :
- **Introductions et chapitres** : mise à jour des citations modifiées dans [`intro_biographie.tex`](../../textes/intro_biographie.tex#L56-L124), [`II.tex`](../../textes/chapitres/II.tex#L11), [`V.tex`](../../textes/chapitres/V.tex#L14) (`déplacement de troupes`) et [`VII.tex`](../../textes/chapitres/VII.tex#L8-L16) (`champ dévasté, sous des tentes`, `entièrement libre`, `un officier ... et un commis (clerk)`).
- **Glossaire ([`annexe_glossaire.tex`](../../textes/annexe_glossaire.tex))** : synchronisation des graphies exactes (`V\LJsup{th} army H.Q.`, `reseaux de barbed wire`, `Canteen, station de Raincheval`, `mes offs`, `permiss\LJsup{res}`, `1 shirt, 1 vest`), ajout de l'entrée `saucisses` et retrait de `staff`.
- **Table des abréviations ([`annexe_abreviations.tex`](../../textes/annexe_abreviations.tex))**, **planche paléographique ([`planche.yaml`](../../donnees/planche.yaml), [`planche_paleographique.tex`](../../textes/planche_paleographique.tex))** et **guide d'écriture ([`GUIDE_PALEOGRAPHIQUE.md`](../../ecriture/GUIDE_PALEOGRAPHIQUE.md), [`LEXIQUE.md`](../../ecriture/LEXIQUE.md))** : recalcul intégral des formes attestées et des comptages d'occurrences sur les 3 713 lignes révisées (`canicul\LJsup{re}`, `mar\LJsup{al}`, `ss-off`, `prof\LJsup{r}`, `instrum\LJsup{ts}`, retrait de `18\LJsup{ie}`, etc.).

---

## 5. Complément systématique des index

Le générateur [`index_latex`](../../src/loci_index.py#L95-L123) dans [`loci_index.py`](../../src/loci_index.py) a été étendu pour prendre en charge deux clés optionnelles dans [`index.yaml`](../../donnees/index.yaml) sans alourdir le registre latin des *loci paralleli* de bas de page :
- `renvoi` : génère une entrée alphabétique de renvoi (`\textit{voir} ...`), seule ou à la suite d'attestations propres ;
- `refs_extra` : permet d'indexer des mentions situées hors des pages du carnet (introduction biographique, lettres et cartes de guerre en annexe) au moyen de références paginées dynamiques `\pageref{...}`.

> [!IMPORTANT]
> **À propos de l'exemple « Tata » évoqué dans la consigne :** la vérification intégrale des 3 713 lignes du carnet et des 7 dossiers de lettres en annexe montre que le mot *Tata* n'apparaît pas littéralement sous la plume d'Hippolyte Combes. Celui-ci emploie toujours le terme **`tante`** : *« Vu tante & Madeleine »* (f. 66 v°, [`133.yaml`](../../donnees/pages/133.yaml#L11), désignant sa sœur aînée **Marie Combes, épouse Vincens**, tante de Madeleine) et *« visite à l'oncle & tantes [?] Thérèse (Layral) »* (f. 71 r°, [`142.yaml`](../../donnees/pages/142.yaml#L13)). Afin qu'aucun lecteur cherchant un terme de parenté ou un surnom familial ne soit pris en défaut, **toutes les appellations familiales, affectives et hypocoristiques** ont reçu leur propre entrée alphabétique dans l'index.

### 5.1. Enrichissements de l'Index des noms de personnes (de 133 à 174 entrées)
- **Surnoms et hypocoristiques** :
  - `Mimi` (*voir* Combes, Émilie), `Josèphe` (*voir* Combes, Joséphine), `Gaby` (sobriquet familial d'Hippolyte attesté dans l'introduction biographique, p. vii, avec renvoi à *Combes, Hippolyte*) ;
  - Surnoms intimes de la correspondance de novembre–décembre 1918 (annexe, doc. 5) : `Petitou` (surnom que se donne Hippolyte auprès de sa femme), `Margueritou` et `Perlounette` (surnoms affectueux de Marguerite), `Kouine (?)` (surnom de lecture incertaine dans la carte des Andelys).
- **Termes de parenté et désignations relationnelles** :
  - `Tante` (*voir* Vincens, Marie ; Layral, Thérèse), `Thérèse (tante)` (*voir* Layral, Thérèse), `Oncle` (*voir* Crouzet, Émile ; Layral, Jean-Pierre-Émile), `Émile (oncle)` (*voir* Crouzet, Émile), `Papa` (*voir* Calmels, Gabriel), `Maman` (*voir* Calmels, Mme), `Mère` (*voir* Calmels, Mme ; Combes, Joséphine), `B. Mm` (« Bonne-Maman », *voir* Fabry, Julie), `Bon Papa` (grand-père d'Hippolyte, introduction biographique), `Parents (de Marguerite)` (*voir* Calmels, Gabriel ; Calmels, Mme), `Sœurs` (*voir* Combes, Émilie ; Vincens, Marie), `Femme (ma) ; Fiancée (ma)` (*voir* Calmels, Marguerite) ;
  - Désignations de fonction ou de voisinage récurrentes : `Voisines (mes)` (*voir* Delsol, Mmes), `Grand ami (notre)` (*voir* Montané, Louis), `Groom (mon)` (*voir* William), `Headcook` (*voir* Connelly).
- **Prénoms employés seuls dans le carnet** :
  - `André` (*voir* Vincens, André), `Germaine` (*voir* Calmels, Germaine), `Henri` (*voir* Calmels, Henri), `Jean` (*voir* Calmels, Jean), `Madeleine` (*voir* Vincens, Madeleine), `Marcel` (*voir* Calmels, Marcel), `Marguerite` (*voir* Calmels, Marguerite), `Pierre` (*voir* Vincens, Pierre), `Victor` (*voir* Calmels, Victor), ainsi que les renvois `C^h, C^l (Mme)` (*voir* Calmels, Mme), `Denis, B^te (?)` (*voir* B^te, Denis), `Lupin (adjudant)` (*voir* Lopin) et `Pozzi (lieutenant)` (*voir* Paggi, Mario).
- **Nouvelles notices de personnes et attestations complétées** :
  - Ajout de notices dédiées pour `Adhémar` (f. 70 r°), `Calmels, Gabriel` (père de Marguerite, ff. 28 v°, 30 v°, 67 v°), `Flutre (fils)` (fils des instituteurs retraités de Martinsart, mobilisé, ff. 52 r°, 84 r°), `Veuve (de Barlette)` (hôtesse d'Hippolyte à Barlette, f. 34 r°–v°) et `Vincens, Gabriel` (beau-frère d'Hippolyte mentionné dans la notice du f. 66 v°) ;
  - Ajout d'attestations manquantes sur des notices existantes : `Calmels, Mme` (ff. 27 v°, 29 v°, 30 r°, 66 v°), `Cliquennois` (f. 85 v°), `Connelly` (f. 21 r°), `Delsol, Mmes` (f. 28 v°, suite à la restitution de *mes voisines*), `Denis, M. et Mme` (f. 89 r°), `Hancock` (f. 41 r°), `Morris` (f. 82 v°, suite à la restitution de *Cap. Morris*) et `Vincens, Madeleine` (f. 67 r°).

### 5.2. Enrichissements de l'Index des noms de lieux (de 248 à 285 entrées)
- **9 sous-lieux nouvellement distingués** : `Acheux-en-Amiénois, château` (ff. 22 r°, 50 v°), `Albert, cimetière` (f. 45 r°), `Amiens, La Semeuse` (f. 59 v°), `Hérissart, cimetière` (ff. 81 v°, 88 r°, 91 v°), `Millau, cimetière` (f. 71 v°), `Toulouse, chapelle de l'Archevêché` (f. 68 v°), `Toulouse, Compagnie Française` (f. 31 r°), `Toulouse, musée (des Augustins)` (f. 66 r°) et `Toulouse, restaurant du Change` (f. 28 v°), plus les attestations complétées de `Raincheval, château` (f. 22 v°), `Amiens, foyer Y.M.C.A. de la gare` (ff. 73 r°, 74 r°), `Toulouse, gare Matabiau` (f. 69 v°) et `Coigneux` (corrigé de l. 7 à l. 8 au f. 53 v°).
- **28 renvois alphabétiques directs** permettant de trouver immédiatement les édifices, quartiers, gares, fermes et commerces nommés sans préfixe communal dans le carnet : `Abri du Soldat`, `Assézat (hôtel d')`, `Automate (restaurant L')`, `Belle-Église (ferme de)`, `Brickfield area`, `Capitole`, `Change (restaurant du)`, `Compagnie Française`, `Côte-Pavée`, `Dalbade (Notre-Dame de la)`, `Daurade (Notre-Dame de la)`, `Esquirol (place)`, `Lardenne`, `Matabiau (gare)`, `Montaudran`, `Nazareth`, `Pech-David`, `Ponts-Jumeaux`, `Pouvourville`, `Purpan`, `Récollets (carrefour des)`, `Saint-Agne`, `Saint-Étienne (cathédrale)`, `Saint-Sernin (basilique)`, `Sainte-Marie-des-Champs`, `Semeuse (La)`, `Terre-Cabade (cimetière de)` et `Victor-Hugo (marché)`.

---

## 6. Reconstruction, contrôles et publication Git

1. **Compilation complète** : régénération de [`planche_paleographique.tex`](../../textes/planche_paleographique.tex), [`annexe_illustrations.tex`](../../textes/annexe_illustrations.tex), des fac-similés et de `livre_journal.tex` via [`generer.py`](../../src/generer.py), triple passe XeLaTeX produisant [`livre_journal.pdf`](../../livre_journal.pdf) (498 pages, 63,9 Mo), imposition de [`livret_A4.pdf`](../../livret_A4.pdf) (32 cahiers de 16 pages) via [`livret.py`](../../src/livret.py), et export actualisé de [`livre_journal_transcription.md`](../../../transcriptions/livre_journal_transcription.md) et [`livre_journal_donnees.json`](../../../transcriptions/livre_journal_donnees.json) via [`exporter.py`](../../src/exporter.py).
2. **Contrôles automatiques et visuels** :
   - [`verifier.py`](../../src/verifier.py) : **`vérification : réussie (0 erreur(s))`** (parité recto/verso des 185 vis-à-vis, intégrité des images incorporées, absence totale de débordements typographiques, de références indéfinies et de glyphes manquants, conformité stricte de l'export JSON aux YAML).
   - [`verifier_regressions.py`](../2026-10-24/verifier_regressions.py) : **100 % conforme**.
   - Inspection visuelle sur rendus PNG des pages liminaires, de doubles pages remaniées (notamment f. 90 v°), des annexes et de l'intégralité des nouvelles pages d'index (p. LIII–LXI).
3. **Publication Git** : mise à jour des chiffres descriptifs dans [`README.md`](../../../README.md), commit sur `main` et publication directe sans aucune branche supplémentaire.
