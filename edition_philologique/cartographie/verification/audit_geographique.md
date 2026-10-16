# Audit géographique des huit cartes — 16 octobre 2026

Les cartes anciennes ne sont pas à une échelle géographique cohérente. Les positions doivent être recalculées ; les localités regroupées sous un symbole doivent être dissociées. Les données livrées donnent des repères contemporains de bourgs ou de lieux-dits, jamais la preuve d’un logement ou d’un trajet de1916.

## Anomalies et décisions

- **Toutes — avéré**. Coordonnées de dessin en mm sans projection ni géoréférencement ; distances et orientations incohérentes sous barres d’échelle kilométriques. Refaire toutes les positions par transformation unique de coordonnées WGS84 ; barres calculées dans la projection ; aucun déplacement de points pour dégager une étiquette.
- **Générale — avéré**. Contour polygonal de France inventé ; Belgique non représentée géographiquement ; villes du Midi, Massif central et Nord placées librement. Fond territorial sourcé avec contour réel ; signaler fond moderne si frontières actuelles (frontière orientale différente en1916).
- **Générale, III, VI — avéré**. Un point vaut plusieurs villes distinctes : Clermont/Saint-Flour, Carcassonne/Béziers, Amiens/Creil, Limoges/Brive/Cahors, Saint-Chély/Saint-Flour, Brioude/Clermont. Points distincts ou choix d’un lieu avec autres étapes dans la légende ; aucun point géographique double.
- **I — avéré**. Renescure dessiné au sud-ouest de Lynde alors qu’il est au nord-ouest ; Lynde–Renescure vaut4,12km environ, pas9km selon échelle du dessin. Reprojeter.
- **I et II — non documenté**. Frontière belge et ligne de front dessinées à main levée ; tracé de front daté août1916 ou multisection Armentières–Arras–Thiepval sans source militaire datée. Frontière moderne géométrique possible si explicite ; supprimer les fronts tant qu’une source datée et géoréférencée ne justifie pas le tracé.
- **II — avéré**. Saint-Pol et Marquay sont presque sur le même parallèle ; le dessin surestime leur distance (13,4km contre5,8km environ). Reprojeter ; conserver Marquay62558, pasMarquayDordogne.
- **II — identification confirmée**. Oppy est un hameau de Beaudricourt (62091), non la commune Oppy62639. Utiliser le point IGN du hameau 2.397407,50.255351. [Source](https://www.archivespasdecalais.fr/Recherche-par-commune/Lettre-B/Beaudricourt).
- **II, IV, V, VII — avéré**. Agrégations de villages séparés sous un point : Ligny/Roëllecourt/Bailleul-aux-Cornailles ; Ribeaucourt/Barlette ; Varennes/Léalvillers ; Martinsart/Aveluy ; Forceville/Englebelmer ; Bertrancourt/Bus ; Albert/Bouzincourt ; Contay/Warloy ; Raincheval/Puchevillers ; Talmas/Villers-Bocage. Dissocier les points affichés ou réduire la sélection.
- **V — avéré**. Léalvillers dessiné SE d’Acheux alors que SO ; Louvencourt NE alors que NO ; Arquèves NO alors que O ; Raincheval nettement S alors que presque même latitude. Positions officielles jointes.
- **V — avéré**. Ferme du Quesnoy dessinée au nord de Puchevillers ; le lieu-dit Le Quesnoy est au sud-est, dans Puchevillers. Utiliser repère IGN2.432466,50.048248, identification cohérente avec BRGM p35, réserve sur bâtiment précis.
- **VII — avéré**. Rubempré dessiné à l’est d’Hérissart alors qu’à l’ouest ; Senlis dessiné à l’ouest de Contay alors qu’à l’est. Reprojeter.
- **VII — non documenté**. Flèche Albert–Mesnil–Miraumont–Achiet–Bapaume/Arras suggère un parcours continu ou une avance ; elle mélange visites, contexte militaire et canonnade entendue. Distinguer lieux visités, lieux évoqués et contexte ; aucune liaison autobiographique non attestée.
- **III — à réserver**. Lieu Sainte-Marie-des-Champs préexiste au lycée1924 ; implantation historique CôtePavée attestée dès1878, mais équivalence exacte avec chapelle actuelle à établir. Mention localisable à l’échelle du quartier avec réserve, ou note hors plan ; aucune accusation d’anachronisme certaine.
- **III — avéré**. Pouvourville et Pech-David fusionnés ; Capitole/Esquirol fusionnés ; Garonne et Canal du Midi inventés graphiquement. Points géographiques distincts ; hydrographie issue d’un fond géoréférencé.
- **VI — non documenté**. Plan Millau attribue un emplacement arbitraire à l’étude Layrals et au cimetière non identifié ; géométrie Tarn/Dourbie approximative. Conserver seulement emplacements établis, documenter nature des sources et ne pas transformer mentions familiales en visite certaine.

## Contrôle des échelles anciennes

|Carte|Liaison|km entre repères officiels|km que suggère la barre ancienne|
|---|---|---:|---:|
|I|Lynde–Renescure|4.11|9.01|
|II|Saint-Pol-sur-Ternoise–Marquay|5.85|13.44|
|V|Acheux-en-Amiénois–Léalvillers|1.88|3.61|
|VII|Hérissart–Rubempré|2.43|8.95|

## Sources principales

- [API officielle des communes](https://geo.api.gouv.fr/decoupage-administratif/communes) : mairies et centres territoriaux explicitement distingués. Réponses brutes locales `communes_59.json`, `communes_62.json`, `communes_80.json`, `communes_31.json`, `communes_12.json`.
- [IGN Géoplateforme, géocodage](https://data.geopf.fr/geocodage/search) : requêtes complètes et identifiants BD TOPO conservés dans `hameaux_et_toulouse_verifies.json` ; réponses brutes `geocodage_*.json`.
- [Archives Pas-de-Calais, Beaudricourt](https://www.archivespasdecalais.fr/Recherche-par-commune/Lettre-B/Beaudricourt) : identification du hameau Oppy.
- [Inventaire régional, Ribeaucourt, IA80009629](https://inventaire-qualif.hautsdefrance.fr/dossier/IA80009629) : Barlette distinct de Ribeaucourt.
- [BRGM RP-55377-FR, p.35](https://infoterre.brgm.fr/rapports/RP-55377-FR.pdf) : ferme et puits du Quesnoy à Puchevillers.
- [Archives de la Compagnie de Jésus, catalogue de Toulouse1878](https://arsi.jesuits.global/wp-content/uploads/2022/06/TOLOSANAE_1878-lowquality.pdf), adresses p.7 : Sainte-Marie-des-Champs, Côte pavée-Montaudran ; le site préexiste donc au lycée installé en1924.
- [POP IA31126959](https://pop.culture.gouv.fr/notice/merimee/IA31126959) : Saint-Étienne de Montaudran ; [POP IA31104738](https://pop.culture.gouv.fr/notice/merimee/IA31104738) : cathédrale Saint-Étienne du centre de Toulouse.

## Réserve de méthode

Les incertitudes du manuscrit restent distinctes de l’identification géographique : pouvoir localiser Sercus n’assure pas la lecture [Sercus ?]. Des lignes droites entre étapes sont des liaisons indicatives, jamais la restitution d’une route ou d’une voie ferrée. Les contours modernes doivent être annoncés comme tels : la frontière orientale française n’était pas celle de2026 en1916.
