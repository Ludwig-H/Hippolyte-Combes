# Cartographie du carnet

Les huit cartes — une vue d'ensemble et sept cartes de chapitre — sont produites depuis des coordonnées géographiques et des fonds vectoriels sourcés. Les localités ont été contrôlées dans les référentiels publics français ; les choix et rectifications sont consignés dans `verification/audit_geographique.md` et les fichiers de données associés.

## Conventions de lecture

- Les marqueurs des bourgs correspondent en général au **point de mairie utilisé comme repère du bourg**. Ils ne localisent pas la chambre, le logement, le cantonnement ou le poste exact d'Hippolyte Combes. Une localisation fine ne peut être déduite de ce seul point.
- Les fonds hydrographiques et limites administratives sont des **repères contemporains**. Ils ne constituent pas une restitution des frontières, limites communales, cours d'eau canalisés ou bâtiments dans leur état de 1916–1917. Cette réserve vaut notamment pour le contour national oriental.
- Les limites communales sont un fond discret de repérage, sans valeur de limite militaire. Aucun front de guerre n'est déduit de ces contours.
- Une liaison entre lieux, lorsqu'elle est indiquée, ne suffit pas à établir le tracé exact d'une route, d'une ligne ferroviaire ou d'une marche. Les intitulés et légendes de chaque carte précisent le statut des relations figurées.
- Les positions données en longitude et latitude WGS84 sont projetées en **Lambert 93, EPSG:2154**, pour construire des cartes dont les axes utilisent la même unité métrique. Les échelles graphiques se lisent dans cette projection.

## Données et sources

`donnees/` contient les coordonnées documentées des lieux et les fonds prêts à dessiner :

- contours généraux Natural Earth au 1:10 millions, domaine public, extraits sur une emprise élargie `[−15,39,20,57]` pour couvrir entièrement les cadrages projetés ;
- hydrographie IGN BD TOPO V3 ;
- frontière franco-belge du secteur de la Lys et limites communales IGN ADMIN EXPRESS COG 2026, Licence Ouverte / Etalab 2.0.

[SOURCES_FONDS.md](SOURCES_FONDS.md) décrit chaque couche, son extraction, sa licence et ses limites d'emploi. Les géométries finales sont en GeoJSON WGS84, avec le nom dans `properties.name`. Les limites locales proviennent des données IGN détaillées ; le fond Natural Earth sert à la vue générale.

`sources_fonds/` archive les URL exactes des requêtes, les empreintes des réponses utilisées, la référence immuable Natural Earth et les scripts de préparation. Les volumineuses réponses brutes sont récupérables dans un dossier de travail extérieur au dépôt ; les GeoJSON allégés sont conservés dans `donnees/`.

## Génération des cartes

Depuis la racine du dépôt, dans un environnement Python 3.14 (version utilisée pour cette livraison) :

```bash
python -m pip install -r edition_philologique/cartographie/requirements.txt
python edition_philologique/cartographie/generer_cartes.py --jobs 8
python edition_philologique/cartographie/verifier_cartes.py
```

Le générateur produit les huit cartes en **PDF vectoriel**, SVG et PNG dans `cartes/`, ainsi qu'un manifeste de production. Le PDF est destiné à l'inclusion dans l'édition ; les PNG facilitent l'inspection visuelle. Les fichiers vectoriels permettent une reproduction nette à l'impression.

Les polices **EB Garamond** et **Noto Sans** doivent être installées (paquets Debian `fonts-ebgaramond` et `fonts-noto-core`).

Les huit processus disponibles peuvent être employés pour le rendu indépendant des cartes. Les contrôles portent notamment sur les localités, les emprises, la lisibilité des noms, les chevauchements et l'intégration dans le PDF du carnet.

## Reproduire les fonds

Les traitements de géométrie emploient `shapely`, `pyproj` et `numpy`. La récupération commune des sources utilise la bibliothèque standard Python. Exemple depuis la racine du dépôt :

```bash
python edition_philologique/cartographie/sources_fonds/telecharger_sources.py /tmp/hc-fonds-reproduction --jobs 4
python edition_philologique/cartographie/sources_fonds/preparer_fonds.py /tmp/hc-fonds-reproduction
python edition_philologique/cartographie/sources_fonds/preparer_communes.py /tmp/hc-fonds-reproduction
```

La version Natural Earth est fixée par sa révision. Les services WFS IGN sont susceptibles d'évoluer : le téléchargement compare leurs empreintes à l'extraction du 16 octobre 2026 et compare aussi le contenu canonique des objets (hors horodatage de la réponse WFS), et signale les différences dans `verification_telechargement.json`. Une différence appelle un nouveau contrôle, sans substitution automatique des données publiées.

La simplification des cours d'eau et de la frontière locale utilise une tolérance de 10 m en Lambert 93. Celle des communes utilise une tolérance de 50 m et conserve les limites partagées, afin d'éviter des lacunes ou recouvrements artificiels. La simplification du fond général vaut 100 m, sans augmenter la précision intrinsèque de Natural Earth au 1:10 millions.

## Choix éditoriaux et contrôle

Le catalogue final `donnees/lieux.json` contient **82 lieux** : 63 repères de mairie et 19 points particuliers. `repertoire_communes.json` conserve les 3 190 candidats contrôlés, sans les confondre avec les lieux retenus. Les libellés abrégés « Acheux », « Saint-Pol » et « Montigny » renvoient respectivement à Acheux-en-Amiénois, Saint-Pol-sur-Ternoise et Montigny-sur-l'Hallue. Thièvres désigne le village partagé entre les deux communes actuelles, sans attribution administrative historique.

Les principaux correctifs concernent Oppy (hameau de Beaudricourt), Le Mont-Noir (hameau, distinct du sommet), les étapes de septembre, la première permission sans Neuilly, les villes distinctes du retour de Millau et la suppression des déplacements personnels non attestés vers Arras, Bapaume ou Miraumont. Le faux plan urbain de Millau est remplacé par la boucle de la seconde permission. Les lieux sont sélectionnés pour conserver une lecture à l'échelle du livre ; les cartes ne prétendent pas répertorier chaque mention du carnet.

Les fonds IGN détaillés dessinent la frontière locale. Les contours Natural Earth ne sont utilisés qu'à l'échelle nationale, afin de ne pas juxtaposer deux frontières de précisions différentes. Les limites communales sont omises des vues régionales les plus étendues. Les noms déplacés gardent des lignes de rappel vers leurs points exacts. Les étiquettes PDF restent du texte, afin de permettre recherche et indexation ; elles ne sont pas converties en contours.

Le fichier `cartes.json` relie chaque liaison à ses scans justificatifs. Les 12 séquences ont été recoupées avec la transcription ; elles ne forment pas un trajet continu couvrant chaque journée. Le manifeste conserve la projection, les coordonnées projetées, les barres d'échelle, les boîtes d'étiquettes et les empreintes des PDF. `verifier_cartes.py` contrôle les données et les sorties ; `verifier_edition.py` vérifie leur présence dans le livre et les 186 vis-à-vis. La revue visuelle indépendante est conservée dans `verification/`.

La mention générale « repères actuels » ne résout pas les localisations historiques : Sercus garde sa réserve de lecture, le logement proche de Saint-Jans-Cappel et le camp entre Bouzincourt et Hédauville ne reçoivent pas de point précis, et Sainte-Marie-des-Champs reste sans bâtiment attribué. Le repère Pech-David désigne un coteau, non le point exact atteint par Combes.

Les fichiers `verification/audit_*` décrivent les défauts des anciennes cartes ; `revue_geographique_finale`, `revue_visuelle` et `validation_cartes` documentent la livraison corrigée.
