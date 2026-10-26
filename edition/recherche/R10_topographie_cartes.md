# R10 — Topographie des cartes (vérification, 25 octobre 2026)

Lecture seule de `/workspaces/Hippolyte-Combes/edition/cartes` (cartes.yaml, donnees/lieux.json, lieux_complementaires.json,
repertoire_communes.json, fronts.yaml, pdf/). Fichiers de travail : `/workspaces/hc_work/recherche2/R10_travail/`
(`resoudre.py` résout les 87 lieux réellement portés ; `nomi.py` les compare à Nominatim, résultat `nominatim.json` ;
`pages_lieux.txt` = date, lieux et titre des 186 pages ; rendus `r_*.png` des neuf cartes ; texte OCR de l'OH 1917-I dans `dl_oh1917/`).

## 1. Synthèse

Les neuf cartes sont justes pour l'essentiel. Les 87 points portés (lieux du carnet et repères de contexte) sont les bons
lieux : aucun homonyme mal choisi (Oppy = hameau de Beaudricourt, Barlette = hameau de Ribeaucourt, Belle-Église = hameau
d'Arquèves, Varennes de l'index = Varennes, Somme). Les coordonnées sont celles des mairies (geo.api.gouv.fr) ou de
points IGN/OSM ; comparées à Nominatim, aucune ne s'écarte de plus de 0,5 km sur les cartes régionales (hors écarts dus à
Nominatim lui-même). Sur le plan de Toulouse, seul Lardenne est un peu décalé (350 m) par rapport au lieu visé par le
carnet (l'église). Les dates de séjour imprimées concordent avec les pages du carnet ; les itinéraires aussi (train du
25 août par Hazebrouck, Berguette et Lillers ; 7 février par Raincheval et Puchevillers ; retour du 6 février par Gannat,
Gien et Montargis). Les distances données dans les introductions sont exactes.

Les lignes de front (construites sur les tables sourcées de R4 et R5) sont exactes à l'échelle des cartes, avec deux
écarts d'environ 1 à 1,5 km dans le tracé de Flandre-Artois, visibles surtout sur la carte générale du Nord et la carte II :
(a) entre Loos et Souchez, la ligne droite laisse Angres et le bois en Hache, allemands jusqu'au 12 avril 1917, du côté
britannique ; (b) au nord du saillant d'Ypres, le sommet placé à l'ouest de Wieltje met ce hameau, britannique, du côté
allemand. Il y a aussi quelques défauts de légende ou d'itinéraire, mineurs : les cercles blancs ne sont pas expliqués sur
la carte générale du Nord ; la flèche de retour de la carte VI ne passe pas par Amiens ; des lieux attestés par le carnet
sont imprimés comme « repères de contexte » gris ; Mirvaux (5 mentions) et Léalvillers (6 mentions) manquent. Enfin, la
notice des cartes ne cite pas la source des fronts et dit que tout point est un bourg, alors que plusieurs sont des
hameaux ou des monuments.

## 2. Faits numérotés

F1 [établi] Coordonnées : 87 lieux portés, comparés à Nominatim (requête du 25 oct. 2026, nominatim.openstreetmap.org/search).
Écarts ≤ 0,5 km pour tous les lieux du Nord et de la Somme (max. Lillers 0,49 km ; Bac-Saint-Maur 0,45 km ; Villers-Bocage
0,44 km). Écarts plus grands sans portée : Paris 2,4 km (Hôtel de Ville contre centroïde Nominatim, carte nationale),
Gien 0,84 km, Béziers 0,79 km (cartes nationales) ; Saint-Flour 81 km = erreur de Nominatim (il renvoie Saint-Flour-l'Étang).
Résultat brut : R10_travail/nominatim.json.

F2 [établi] Lardenne (plan de Toulouse) : le point (lieux.json, 1.380704 / 43.592422) est le « quartier » IGN
PAIHABIT0000000073089807. Le carnet (p. 058, 1er oct. 1916) : « venus à Lardenne. De l'église, continué à pied j-au pont du
Touch ». L'église de Lardenne (Église Saint-Michel, OSM way 74701771) est à 1.38438 / 43.59072, soit à 0,35 km du point
(seuil de 300 m dépassé). Identité historique de l'église : [probable] (non documentée en ligne).

F3 [établi] Montaudran : point = église (IGN), conforme au carnet (p. 057 : « village de Montaudran. Reposé ds l'eglise. Monté
… au clocher ») ; l'écart de 0,47 km avec le nœud « suburb » OSM est sans objet. Pouvourville : point à 86 m de l'église
Sainte-Madeleine (OSM way 63998972) que cite le carnet (p. 055 : « village de Pouvourville eglise »). Purpan : point =
amphithéâtre de Purpan-Ancely (OSM way 95656275) ; p. 056 : « course en tram. Esquirol – Purpan. Longue halte aux Ruines ».
Saint-Étienne, Terre-Cabade, Capitole, Blagnac : ≤ 0,12 km.

F4 [établi] Homonymes. Oppy = hameau de Beaudricourt (IGN, insee 62091 ; Nominatim « Oppy, Beaudricourt » à 0,06 km) ;
p. 040 : « arrivés à Oppy … Ptit hameau de 6 maisons … venu à pied à Beaudricourt ». Barlette = hameau de Ribeaucourt
(IGN ; Nominatim 0,08 km) ; p. 066–067. Belle-Église = lieu-dit d'Arquèves (IGN ; Nominatim 0,05 km). Croix-du-Bac
(Steenwerck), Bac-Saint-Maur (Sailly-sur-la-Lys), Mont-Noir (Saint-Jans-Cappel ; 0,37 km du sommet, sans portée),
Berguette (gare, Isbergues) : justes.

F5 [établi] Pièges latents (sans effet sur les cartes actuelles) : la résolution par nom de `generer_cartes.py` prend la
première entrée trouvée ; « Varennes » → 31568 (Haute-Garonne, entrée présente dans lieux_complementaires.json),
« Flers » → 62337 (Pas-de-Calais), « Mametz » → 62543 (Pas-de-Calais ; Mametz-Somme n'existe plus comme commune),
« Oppy » → 62639 (près d'Arras). Aucune carte n'appelle ces noms ; à ne pas utiliser comme `contexte` par leur nom.

F6 [établi] Dates des cartes contrôlées sur les pages : Lynde 25–28 juil. (p. 002–005) ; Saint-Jans-Cappel 28 juil. – 4 août
(p. 005–012) ; La Croix-du-Bac 5–25 août (p. 012–027) ; Marquay 25 août – 8 sept. (p. 028–039) ; Monts-en-Ternois 9 sept.,
Oppy 10 sept. (p. 039–040) ; Raincheval 11–23 sept. (p. 041–048) ; Barlette 6–14 oct. (p. 066–074) ; Beauval 15 oct.,
Warloy 16 oct., Bouzincourt 17–18 oct., Albert 19 oct. – 2 nov. (p. 074–090) ; Acheux dès le 2 nov. jusqu'au 7 févr.
(p. 090–147) ; Hérissart 7 févr. – 30 avr. (p. 147–186).

F7 [établi] Itinéraires : p. 027 (25 août) « A Lillers, vers 2H45 / Hazebrouck : 2H / A St-Pol, à 4H30 / Berguette : 2H30 »
= ordre Bailleul–Hazebrouck–Berguette–Lillers–Saint-Pol de la carte II ; p. 147 (7 févr.) « En auto à Hérissart, par
Raincheval & Puchevillers » = flèche de la carte VII ; p. 144 (6 févr.) Brioude, Clermont, Gannat, Gien, Montargis ; p. 145
Corbeil ; p. 146 (7 févr.) « Amiens à minuit et demi … Doullens … Louvencourt … Acheux » : la flèche verte de la carte VI va
directement de Paris à Acheux, sans Amiens.

F8 [établi] Front Loos–Souchez. OH 1917-I (Falls 1940), p. 301 : les défenseurs de Lorette « were driven back to the Bois en
Hache at the eastern extremity of the Lorette ridge » ; p. 303 : « the Bois en Hache, at the eastern end of the Lorette
ridge » reste à prendre ; p. 343–344 : « Capture of the Pimple and the Bois en Hache, 12th April » (texte :
archive.org/stream/in.ernet.dli.2015.210683, OCR, lignes 22245–22340 et 24874–24945). CWGC, Liévin Communal Cemetery
Extension (cwgc.org, cemetery-details/62400) : Liévin pris par le Canadian Corps le 14 avril 1917. Coordonnées : Angres
(village, IGN) 2.7578 / 50.4073 ; Liévin (mairie) 2.7847 / 50.4211 ; Cité de Calonne (IGN, Liévin) 2.7490 / 50.4313 ;
Souchez 2.7409 / 50.3910 ; chapelle de Lorette ≈ 2.718 / 50.400. Le tracé actuel va en ligne droite de [2.760, 50.392] à
[2.795, 50.455] : à la latitude d'Angres il passe par 2.769, soit 0,8 km à l'est du village et davantage à l'est du bois en
Hache : Angres et le bois apparaissent du côté britannique. [établi pour la situation ; position du sommet proposé : probable,
le bois en Hache n'ayant pas de coordonnées publiées trouvées]

F9 [probable] Front au nord-est d'Ypres. Wieltje (Nominatim, hameau) 2.9175 / 50.8707 ; Mouse Trap Farm (mémorial)
2.9213 / 50.8790. En juillet 1915, le 3rd Rifle Brigade relève les Buffs « in trenches at Wieltje facing Mouse Trap Farm »
(menonthegates.org.uk, « 3 Bn Rifle Brigade July 1915 ») ; front stable dans ce secteur jusqu'au 31 juillet 1917. Le sommet
[2.905, 50.873] place la ligne à 2.907 à la latitude de Wieltje, soit 0,75 km à l'ouest du hameau, qui apparaît ainsi du
côté allemand ; la ligne passait entre Wieltje et Mouse Trap Farm (≈ 2.919 / 50.875). Écart ≈ 1–1,4 km, visible seulement
sur la carte générale du Nord.

F10 [établi] Les autres sommets ont été recontrôlés contre R4/R5 et des positions indépendantes : Hawthorn (Wikipedia,
50.0833 / 2.6497), Lochnagar (50.0156 / 2.6972 ; le tracé passe à 250 m), Leipzig (CWGC Lonsdale), Hooge, cote 60, Saint-Éloi,
Le Touquet/Frelinghien, Fromelles (V.C. Corner), Neuve-Chapelle, Givenchy, Cuinchy, Neuville-Saint-Vaast/Thélus,
Blangy, Achicourt/Beaurains, Ficheux, Blairville, Ransart, Monchy-au-Bois/Hannescamps, Foncquevillers/Gommecourt ; front du
18 nov. (New Munich/Frankfurt, Beaucourt/Baillescourt, Desire/Regina, Le Sars/butte, Lesbœufs/Le Transloy, Sailly-Saillisel,
Bouchavesnes, Omiécourt-lès-Cléry, Biaches, Barleux, Belloy/Berny, Chaulnes) ; ligne Hindenburg (Telegraph Hill,
Neuville-Vitasse, Héninel, Fontaine-lès-Croisilles, Bullecourt, Quéant, Pronville, Mœuvres, Havrincourt). Écarts ≤ 1 km.
Remarques : entre Cambrin et Loos la droite passe ≈ 1 km à l'ouest de la redoute Hohenzollern (≈ 2.783 / 50.49) — tolérable ;
La Maisonnette (IGN 2.9119 / 49.9159) tombe 0,4 km à l'est du tracé du 18 nov. ; les communiqués français signalent une
attaque allemande au lance-flammes le 29 oct. 1916 et un gain partiel au nord de La Maisonnette (presse, argonnaute) :
statut exact au 18 nov. non établi, écart sous le seuil.

F11 [établi] Distances des introductions recalculées (mairies) : Wallon-Cappel–Lynde 4,1 km (« 4,2 km », centres) ;
Bayencourt–Gommecourt 5,3 km ; Morlancourt–Albert 5,8 km ; Marquay–Saint-Pol 5,9 km ; Varennes–Acheux 2,6 km (« moins de
trois kilomètres au sud ») ; Hérissart–Toutencourt (QG Fifth Army) 3,2 km ; Hérissart–Arras 39 km, –Croisilles 38 km,
–Bullecourt 41 km (« une quarantaine ») ; La Croix-du-Bac–Sailly 2,5 km ; Saint-Jans-Cappel–Wytschaete 11,6 km,
–Messines 12,5 km (« une douzaine ») ; Cambrai–Mœuvres 12,3 km, –Havrincourt 12,9 km (« douze ou treize »).

F12 [établi] Lieux attestés mais imprimés comme « contexte » gris (légende du fichier : « repères sans lien direct avec le
carnet ») : Martinsart sur la carte IV (p. 104, 28 nov. 1916, « course en auto à Martinsart Chateau ») ; Bertrancourt sur la
carte V (p. 121, 6–9 janv. 1917 ; aussi p. 092, 168) ; Doullens sur la carte VII (p. 152, 158, 163, 179). Lieux fréquents
absents : Mirvaux (p. 159, 169, 171, 183, 185 ; commune 80550, 2.3943 / 50.0030, à 2,8 km d'Hérissart), carte VII ;
Léalvillers (p. 094, 096, 097, 112, 116, 121 ; 80470, présent dans lieux_complementaires.json), carte V.

F13 [établi] Carte générale du Nord : la légende n'explique que les points rouges (« Principaux cantonnements … et dates de
séjour ») ; Hazebrouck, Saint-Pol, Lucheux, Doullens, Amiens, et deux cantonnements datés (Barlette 6–14 oct., Raincheval
11–23 sept.) sont des cercles blancs sans entrée de légende.

F14 [établi] Notice des cartes (textes/intro_cartes.tex) : « Chaque point marque le bourg (sa mairie ou son centre actuels) »,
alors que La Croix-du-Bac, Bac-Saint-Maur, le Mont-Noir, Oppy, Barlette, Belle-Église, la gare de Berguette et les lieux
toulousains sont des hameaux, lieux-dits ou monuments (repères IGN ou OSM, lieux.json) ; la phrase sur les fronts ne nomme
pas leurs sources (OH, Michelin), qui ne figurent que dans fronts.yaml.

## 3. Propositions

Voir l'objet structuré pour le texte exact. Résumé :
- P1 [fronts.yaml, flandre_artois_1916] après « - [2.795, 50.455] # Loos … » insérer [2.765, 50.432] (cité de Calonne B / Liévin A) et [2.738, 50.404] (à l'ouest d'Angres et du bois en Hache, A jusqu'au 12 avr. 1917) — OH 1917-I, p. 301, 343 ; CWGC Liévin. Haute/moyenne (erreur de camp sur ~1,5 km).
- P2 [fronts.yaml] [2.905, 50.873] → [2.919, 50.875] (entre Wieltje B et Mouse Trap Farm A). Basse, probable.
- P3 [lieux.json, lardenne] 1.380704 / 43.592422 → 1.38438 / 43.59072 (église Saint-Michel, OSM way 74701771), carnet p. 058. Basse.
- P4 [cartes.yaml, VI] flèche de retour ['75056', '80003'] → ['75056', '80021', '80003'] (p. 146). Basse.
- P5 [cartes.yaml, generale_nord] ajouter l'entrée de légende « cercle » (autres cantonnements, étapes et lieux cités). Basse.
- P6 [cartes.yaml, VII] ajouter Mirvaux (5 mentions). Basse.
- P7 [cartes.yaml, V] ajouter Léalvillers (6 mentions). Basse.
- P8 [cartes.yaml, V] Bertrancourt : de « contexte » gris en lieu du carnet (p. 121). Basse.
- P9 [cartes.yaml, IV] Martinsart : de « contexte » gris en lieu du carnet (p. 104). Basse.
- P10 [intro_cartes.tex] points : bourg ou, pour un hameau, un lieu-dit ou un monument, repère IGN ou OSM. Basse.
- P11 [intro_cartes.tex] nommer la source des fronts (histoire officielle britannique, guides Michelin). Moyenne.

## 4. Vérifications sans changement

Voir F1, F3, F4, F6, F7, F10, F11 : coordonnées, homonymes, dates, itinéraires, autres sommets de front, distances,
titres et légendes des cartes I–VII et générale de la France, notes des cartes II, III, IV (Croix-du-Bac déduite ; Purpan
proposé ; camp entre Bouzincourt et Hédauville non localisé), crédits des fonds (Copernicus, IGN, Natural Earth, OSM pour
Purpan) conformes aux couches utilisées.

## 5. Sources consultées

- Pages du carnet : donnees/pages/002–186.yaml ; index : donnees/index.yaml.
- Nominatim (OSM), https://nominatim.openstreetmap.org/search (25 oct. 2026) ; Overpass API (églises de Lardenne et de Pouvourville) ; IGN Géoplateforme, https://data.geopf.fr/geocodage/search (index poi) ; geo.api.gouv.fr.
- C. Falls, *Military Operations, France and Belgium, 1917*, I, Londres, 1940, p. 301, 303, 343–344 : https://archive.org/details/in.ernet.dli.2015.210683 (texte OCR).
- CWGC, Liévin Communal Cemetery Extension : https://www.cwgc.org/visit-us/find-cemeteries-memorials/cemetery-details/62400
- Men on the Gates, 3rd Rifle Brigade, July 1915 : https://menonthegates.org.uk/men_front/bo-1915-ypres-3-bn-rifle-brigade-july-1915/
- Wikipedia (en), Battle of Pilckem Ridge (front le long du canal au nord de Boesinghe) ; fr.wikipedia, Angres (« sur la ligne de front »).
- Long, Long Trail, Gazetteer : Biaches ; presse française d'oct. 1916 (La Contemporaine, argonnaute.parisnanterre.fr).
- Dossiers R4 (§ 2.3, tables A, B, C) et R5 (tableaux 2.D, 2.D bis).
