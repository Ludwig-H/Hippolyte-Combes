# Revue géographique indépendante des huit cartes

Revue du 16 octobre 2026. Le contrôle porte sur **82 lieux effectivement utilisés** : **63 repères de mairies** issus de l’API officielle des communes et **19 points particuliers** (17 objets IGN, l’amphithéâtre de Purpan d’après son périmètre OSM et un repère paysager municipal de Pech-David). Le catalogue final ne contient aucun lieu inutilisé. Les **3 190 entrées** de `repertoire_communes.json` sont une archive de candidats, et non autant de lieux du carnet.

Chaque coordonnée du catalogue a été comparée à la source sauvegardée correspondante : **aucune divergence restante**. Les empreintes des données contrôlées et les douze liaisons examinées sont archivées dans `revue_geographique_finale.json`.

## Corrections incorporées après revue

- **I — Le Mont-Noir** : le scan 006 nomme expressément un hameau. Le point IGN du lieu habité (PAIHABIT0000000056580794 ; 2,727754°, 50,779533°) remplace le sommet voisin.
- **II — 25 août** : le voyage est ferroviaire jusqu’à Saint-Pol, puis routier jusqu’à Marquay (scans 027–028). La légende précise « train puis route ».
- **IV — Camp** : le camp entre Bouzincourt et Hédauville est installé le 17 octobre, puis occupé le 18 (scans 077–079). La note donne désormais les deux dates, sans inventer un emplacement précis.
- **V — Symboles** : « Repère principal » remplace « Lieu de séjour principal », qui prêtait à Raincheval et Toutencourt un statut de cantonnement non établi pour cette période.
- **Frontière régionale** : le double contour produit par la superposition Natural Earth/IGN est supprimé ; le contour régional détaillé est celui de l’IGN.

## Chronologie des liaisons

| Carte | Séquence contrôlée | Scans |
|---|---|---|
| I | 28 juillet : Lynde, Hazebrouck, secteur de Saint-Jans-Cappel ; 5 août : Saint-Jans-Cappel, Bailleul, La Croix-du-Bac | 005–006 ; 012 |
| II | 25 août : Bailleul, Hazebrouck, Berguette, Lillers, Saint-Pol, Marquay ; 9–11 septembre : Marquay, Ligny, Monts, Oppy, Lucheux, Thièvres, Raincheval | 027–028 ; 039–041 |
| III | 25–27 septembre : Amiens, Paris, Toulouse, principales étapes retenues | 050–051 ; 053–054 |
| IV | 15–17 octobre : Barlette, Beauval, Beauquesne, Puchevillers, Warloy, Senlis ; 2 novembre : Albert, Acheux, Raincheval | 074–075 ; 077 ; 089–091 |
| VI | 26–28 janvier : Acheux, Amiens, Paris, Toulouse ; 3 février : Toulouse, Carcassonne, Béziers, Bédarieux, Millau ; 5–7 février : retour par Saint-Flour, Brioude, Clermont-Ferrand, Gannat, Gien, Montargis, Corbeil, Paris, Amiens, Acheux | 128–132 ; 139–140 ; 143–146 |
| VII | 7 février : Acheux, Raincheval, Puchevillers, Hérissart ; 30 avril après-midi : tournée par Puchevillers, Pierregot, Villers-Bocage, avec Hérissart comme base | 147 ; 186 |

La carte générale est un répertoire spatial ; la carte V montre des lieux de tournées sans en faire un itinéraire unique. Les liaisons représentent des étapes, pas le dessin des routes ou des voies ferrées.

## Distinctions géographiques et réserves

Oppy est le hameau de Beaudricourt, distinct de la commune près d’Arras. La Boisselle est le lieu habité d’Ovillers-la-Boisselle, distinct du lieu-dit homonyme de Contay. Le Mesnil est au nord-est de Martinsart. Rubempré est au sud-ouest d’Hérissart : **2,434 km à vol d’oiseau entre les deux repères de mairies**. Renescure est au nord-ouest de Lynde ; Léalvillers au sud-ouest d’Acheux ; Louvencourt au nord-ouest ; Arquèves à l’ouest. Ces relations sont contrôlées numériquement dans le rapport associé.

À Toulouse, Purpan désigne l’amphithéâtre romain, et non l’hôpital ; Pouvourville est distinct du coteau de Pech-David ; la cathédrale Saint-Étienne et l’église de Montaudran sont distinctes. Le point de Pech-David représente le coteau, sans reconstitution de promenade. Sainte-Marie-des-Champs n’est pas ponctuée : l’implantation exacte du bâtiment en 1916 reste à établir. La lecture Sercus [?] reste réservée.

Les coordonnées sont des repères contemporains, sans prétendre restituer logements, fermes précises, quais de gare, frontières ou hydrographie de 1916. Les sources détaillées et leurs limites sont conservées dans les dossiers `donnees/` et `verification/`.

## Revue visuelle

Les huit PNG ont été examinés pour la géométrie, l’orientation, les signes et l’attribution des noms. Après ajustement des libellés, l’encart Nord distingue clairement Acheux/Albert et Saint-Jans-Cappel/La Croix-du-Bac ; VII distingue Le Mesnil/Martinsart. Dans V, les textes Arquèves/Belle-Église sont déportés de part et d’autre de leurs points : les deux lignes de rappel doivent être suivies. Il reste une réserve mineure de lisibilité, sans inversion des coordonnées. Le contrôle des textes extractibles du PDF relève du rendu final et non de ce contrôle géographique.

Mise au point graphique finale (Codex) : les étiquettes de Belle-Église et Arquèves sont désormais disposées respectivement au-dessus et au-dessous de leurs points, sans croisement. La position de Senlis-le-Sec a également été ajustée pour éviter un rappel masqué par Toutencourt. Les coordonnées restent identiques ; voir la revue visuelle finale et le manifeste livré.
