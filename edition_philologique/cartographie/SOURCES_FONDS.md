# Fonds cartographiques vérifiés — 16 octobre 2026

Ces fonds représentent des **repères géographiques contemporains**. Ils ne restituent pas les limites de la France en 1916–1917, les fronts militaires ni l'état historique exact des lits et canaux. La carte générale peut employer les contours nationaux comme fond de localisation à condition d'expliciter cette convention ; aucun tracé du front de guerre n'est fourni.

Dans le dépôt, les GeoJSON finaux sont dans `donnees/` ; les requêtes, empreintes et scripts sont dans `sources_fonds/`. Les noms de réponses brutes cités ci-dessous désignent les fichiers récupérables dans un dossier temporaire par `sources_fonds/telecharger_sources.py` : ces fichiers volumineux ne sont pas inclus dans le dépôt.

Tous les GeoJSON livrés utilisent des coordonnées **longitude, latitude WGS 84** (`CRS84`). Le champ `properties.name` est l'étiquette française. Les opérations sont des intersections avec une emprise et une simplification métrique en Lambert 93, avec conservation de la topologie ; aucune géométrie n'a été dessinée ou interpolée à la main.

| Fichier livré | Contenu | Emprise longitude/latitude | Simplification |
|---|---|---|---|
| `europe_countries.geojson` | 34 pays intersectant le cadrage élargi autour de la France et de la Belgique | −15, 39, 20, 57 | 100 m, à partir d'un fond au 1:10 000 000 |
| `hydro_nord.geojson` | Lys, Ternoise, Authie, Ancre, Hallue, Somme | 1,4, 49,7, 3,3, 51,2 | 10 m |
| `hydro_toulouse.geojson` | Garonne, canal du Midi, canal de Brienne, canal latéral à la Garonne, Touch | 1,2, 43,4, 1,7, 43,8 | 10 m |
| `frontiere_franco_belge_lys.geojson` | Frontière franco-belge dans le seul secteur de la Lys | 2,4, 50,5, 3,3, 50,95 | 10 m |

## Contours généraux : Natural Earth

- Couche : **Natural Earth, Admin 0 – Countries, 1:10m**.
- [Fiche officielle](https://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-admin-0-countries/).
- GeoJSON fourni par le dépôt du co-auteur et responsable du projet, [révision fixe `9380cca83db5f9aef52d5e762765100745f84b27`](https://raw.githubusercontent.com/nvkelso/natural-earth-vector/9380cca83db5f9aef52d5e762765100745f84b27/geojson/ne_10m_admin_0_countries.geojson), dernière modification de ce fichier le 13 mai 2022.
- [Domaine public](https://www.naturalearthdata.com/about/terms-of-use/). Crédit conseillé : « Fond : Natural Earth ».
- Le fond au 1:10 millions convient à la vue d'ensemble ; **ne pas employer ses frontières comme tracé précis sur les cartes locales**.

## Hydrographie : IGN

- Couche : **IGN BD TOPO V3, `BDTOPO_V3:cours_d_eau`**, service WFS officiel `https://data.geopf.fr/wfs/ows`.
- [Fiche publique du jeu de données](https://www.data.gouv.fr/datasets/bd-topo-r) ; [explication IGN de la diffusion sous Licence Ouverte](https://www.ign.fr/institut/des-donnees-et-logiciels-ouverts-au-service-de-la-nation).
- [Descriptif officiel de la BD TOPO 3.3](https://geoservices.ign.fr/sites/default/files/2024-02/DC_BDTOPO_3-3_0.pdf). La classe Cours d'eau représente une entité hydrographique linéaire nommée ou identifiée par un code, composée de tronçons hydrographiques.
- Licence Ouverte / Etalab 2.0. Crédit : **« Hydrographie : IGN, BD TOPO, extraction du 16 octobre 2026 »**.
- Les réponses WFS brutes et les URL exactes sont dans `ign_nord_raw.geojson`, `ign_toulouse_raw.geojson` et leurs fichiers `*_request.json`. Les identifiants IGN des objets retenus et leurs codes hydrographiques sont conservés dans chaque objet final.
- Sélection par noms explicites des cours principaux. Les fossés, bras de décharge, ouvrages ou cours différents dont le nom contient fortuitement « Somme », « Lys », « Authie » ou « Touch » sont exclus. Plusieurs objets IGN formant un même cours ou ses bras proches sont réunis sans ajouter de liaison géométrique.
- La Lys est bien au nord/nord-ouest d'Armentières ; l'Ancre traverse Albert ; la Garonne arrive du sud, traverse Toulouse puis continue au nord-ouest. La géométrie de l'Ancre représente environ 41 km dans l'emprise, celle de la Ternoise environ 45 km. Tous les objets livrés ont une géométrie valide.

## Frontière locale précise : IGN

- Couche **IGN ADMIN EXPRESS COG 2026, `ADMINEXPRESS-COG.2026:region`**, objet Hauts-de-France (code INSEE 32), extrait du service WFS officiel.
- La frontière est obtenue comme limite réelle du polygone régional, découpée dans une emprise qui ne contient ni littoral ni limite interrégionale. Elle est appropriée aux cartes de la Lys seulement et ne doit pas être prolongée artificiellement.
- Licence Ouverte / Etalab 2.0. Crédit : **« Limites : IGN, ADMIN EXPRESS COG 2026 »**.
- La réponse brute et la requête sont dans `ign_hauts_de_france_raw.geojson` et `ign_hauts_de_france_request.json`.

## Reproduction et vérification

`preparer_fonds.py` produit les quatre GeoJSON livrés à partir des fichiers sources archivés et écrit `manifest.json` (empreintes SHA-256). Les dépendances sont `shapely` et `pyproj`. Les réponses WFS sont un état daté : une nouvelle interrogation ultérieure peut retourner des données modifiées. `sources_manifest.json` conserve l'empreinte des entrées brutes ; `natural_earth_source.json` donne en plus une URL immuable de la source Natural Earth.

Les coordonnées sont arrondies à six décimales après simplification. La tolérance de simplification est une opération graphique, pas une affirmation de la précision historique des données.

## Limites communales des cartes régionales

Deux extractions supplémentaires utilisent la couche officielle **IGN ADMIN EXPRESS COG 2026, `ADMINEXPRESS-COG.2026:commune`**, sous Licence Ouverte / Etalab 2.0 :

- `communes_nord.geojson` : emprise `[1.9,49.85,3.0,50.86]`, 1 201 objets finaux parmi 1 203 communes intersectant l'emprise dans la réponse WFS.
- `communes_toulouse.geojson` : emprise `[1.28,43.48,1.60,43.76]`, 104 objets finaux parmi 105 communes intersectant l'emprise dans la réponse WFS.

Les réponses ont été contrôlées intégrales (`numberReturned == numberMatched`). Les géométries sont découpées à l'emprise demandée ; trois intersections minuscules de moins de 100 m² chacune ont été écartées. Il s'agit des communes françaises uniquement. La propriété `code_insee` conserve l'identifiant administratif ; `name` donne le nom officiel actuel.

Les couvertures initiales sont topologiquement valides. `shapely.coverage_simplify` opère en Lambert 93 avec une tolérance de 50 m et conserve les limites partagées entre communes et le contour extérieur : cela évite les lacunes ou chevauchements que produirait une simplification indépendante de chaque polygone. Tous les polygones finaux sont valides. Les contours servent de contexte discret ; ils ne doivent pas être présentés comme des limites administratives datées de 1916–1917.

Les scripts `telecharger_communes.py` et `preparer_communes.py` permettent de répéter l'extraction et le traitement. Les réponses `ign_communes_*_raw.geojson`, les requêtes `ign_communes_*_request.json` et leurs empreintes sont conservées. Attribution : **« Limites communales : IGN, ADMIN EXPRESS COG 2026 »**.
