# R11 — Les lieux de l'index et des commentaires (vérification, 25 oct. 2026)

Périmètre : les 248 notices de lieux de `donnees/index.yaml`, les champs `lieux` et `historique` des 186 pages,
les introductions des chapitres I–VII et les passages géographiques des introductions (biographie, interprète,
cartes) ; données des cartes (`cartes/donnees/lieux*.json`). Aucun fichier du dépôt modifié. Fichiers de travail :
`/workspaces/hc_work/recherche2/R11_comm.txt`, `R11_intros.txt`, `web/`.
NB : pendant le travail, d'autres agents ont déjà corrigé deux distances (Molliens-au-Bois 5 km, cl. 158 ;
Toutencourt 3 km, cl. 160) ; elles ne sont plus proposées.

## 1. Synthèse

L'ensemble est solide : identifications, communes actuelles, départements, hameaux, QG et distances concordent dans
leur immense majorité avec les sources (OSM/Nominatim, geo.api.gouv.fr, POP, LLT, Baedeker). Restent :
- une erreur d'identification : la « rue de Flandre » du 26 sept. 1916 (cl. 052) est la grand-rue du Bourget
  (route de Flandre, auj. avenue de la Division-Leclerc), où l'on prend le tramway ; l'index la met à Paris (XIXᵉ) ;
- Frévent (Baedeker 1909, p. 22) : l'« hôtel d'Amiens » est l'hôtel de Frévent (à Doullens, le Baedeker ne connaît que
  les Quatre-Fils-Aymon) ; la « belle église » peut être Saint-Hilaire ou Saint-Vaast : le commentaire tranche trop ;
- la notice de Millau omet qu'Hippolyte Combes y est né (le chap. VI dit « leur ville natale à tous deux ») ;
- précisions : L'Arbret est un hameau de Bavincourt ; « Ramecourt » doit porter dans l'index la marque d'incertitude
  qu'il a dans la page ; la ferme du Quesnoy est un écart de Puchevillers (OSM), vers Toutencourt ;
- petites inexactitudes : Contay à 5,3 km (non 4) d'Hérissart ; Auxi-le-Château à 18 km à l'O.-N.-O. de Doullens
  (non 19 km au N.-O.) ; basilique d'Albert 1884–1897 selon la notice Mérimée citée (non 1885) ;
- données de carte : quatre homonymes erronés dans `lieux_complementaires.json`, sans effet actuel.

## 2. Faits

F1. Le Bourget, rue de Flandre. Carnet, cl. 052 : « du Bourget, sortie de la rue de Flandre, pris tramway qui m'a
conduit j-à gare du Nord ». Cartes postales anciennes du Bourget (Geneanet, nᵒˢ 301078, 301016, 301021) : « Rue de
Flandre » au Bourget, voies de tramway, une carte datée du 29 nov. 1914 ; classées sous « Av. de la Division Leclerc »,
ancien nom « Route de Flandres ». [probable]
F2. Baedeker, Northern France, 1909, p. 22 : « Frévent (Hôt. d'Amiens), with 4755 inhab. … The church of St. Vaast
dates partly from the 15th century » ; p. 23 : « Doullens (Hôt. des Quatre-Fils-Aymon) ».
https://archive.org/stream/northernfranc00karl/northernfranc00karl_djvu.txt [établi]
F3. Frévent : Saint-Hilaire, XVIᵉ s., classée 1982 (Mérimée PA00108287) ; Saint-Vaast, église du XVIIᵉ s. détruite
pendant la Seconde Guerre mondiale, reconstruite au XXᵉ s. (Wikipédia, « Frévent »). Deux églises en 1916. [établi]
F4. Millau ville natale d'Hippolyte Combes (acte n° 395 ; cl. 019, 139 ; chap. VI). [établi]
F5. L'Arbret, hameau de Bavincourt (Wikipédia « Bavincourt » ; OSM 50.2135/2.5600) ; « gare de ravitaillement » de
Saulty-L'Arbret photographiée en 1915 (commune-mairie.fr). [établi / probable]
F6. XIII Corps : Couin 4 oct. 1916, Acheux 29 nov. 1916, Doullens 12 janv. 1917 (LLT). [établi]
F7. « Le Quesnoy, Puchevillers », farmyard, 50.0486/2.4326 (OSM) : 1,8 km E.-S.-E. de la mairie de Puchevillers. [probable]
F8. Ramecourt : `lieux` du cl. 032 « Ramecourt ? », apparat « lecture incertaine », commentaire « n'est pas sur le
trajet » ; index sans « ? » ni notice. [établi]
F9. Distances (mairies) : Hérissart–Contay 5,3 km (120°) [cl. 159 : 4 km] ; Doullens–Auxi 17,9 km (297°) [cl. 158 :
19 km au N.-O.]. [établi par le calcul]
F10. Mérimée PA80000002 : « Construite … entre 1884 et 1897 » [cl. 078 : 1885]. [établi]
F11. Barlette (Mérimée IA80009826) : dépendait de Franqueville, rattaché à Ribeaucourt « au 20ᵉ siècle ». Cohérent
avec les cl. 067 et 072. [établi]
F12. Baedeker 1909, p. 25 : « Hôt. de la Paix, Rue Duméril 15 » (Amiens) : confirme le cl. 119. [établi]
F13. Rue Saint-Joseph (Toulouse), quartier du Busca, entre Côte-Pavée et Saint-Agne (OSM) : cohérent avec cl. 055, 060.
F14. Tombeau Bergès à Terre-Cabade (Mérimée PA31000115, concession de 1908). [établi]
F15. lieux_complementaires.json : "31568" Varennes (Haute-Garonne ; bon code 80776), "31341" Merville (Haute-Garonne ;
59400), "62543" Mametz (Pas-de-Calais ; Somme = Carnoy-Mametz 80505, déjà présent), "62337" Flers (Pas-de-Calais ;
80314). Non appelés par cartes.yaml, mais generer_cartes.py résout aussi par nom. [établi]
F16. Rue Saint-Martin → 10, place Emma-Calvé (P. Combes, livre familial, Combes-2 l. 104) ; église Saint-Martin,
2, place Emma-Calvé. [établi]
F17. Caserne Niel, 42, boulevard des Récollets (cl. 055). [probable]

## 3. Propositions (détail dans l'objet structuré)
P1 rue de Flandre → Le Bourget ; P2 hôtel d'Amiens de Frévent ; P3 églises de Frévent (cl. 098) ; P4 notice de Millau ;
P5 L'Arbret ; P6 Ramecourt ? ; P7 Quesnoy ; P8 Contay 5 km (cl. 159) ; P9 Auxi 18 km O.-N.-O. (cl. 158) ;
P10 basilique 1884 (cl. 078) ; P11 homonymes du fichier de carte.

## 4. Vérifications sans changement
Hameaux/communes : Oppy (Beaudricourt), Belle-Église (Arquèves), Barlette (Ribeaucourt), Septenville (Rubempré),
Berguette (Isbergues), Bac-Saint-Maur (Sailly-sur-la-Lys), La Croix-du-Bac (Steenwerck), Martinsart et le Mesnil,
La Boisselle (Ovillers), Couin (Pas-de-Calais), Thièvres, Lamotte-Warfusée, Corbeil-Essonnes (1951), Bournemouth ;
Flutre né à Mesnil-Martinsart le 21 juin 1892 (Wikidata Q559663).
QG : XIII Corps (LLT) ; Toutencourt 2 juil. 1916 – 28 mars 1917 (R4 F32) ; II et IV Corps à Senlis (R4) ; Bailleul
occupée le 14 oct. 1914, railhead, air depot, hospital centre, QG de corps, prise en avril 1918 (CWGC).
Monuments (POP) : PA00107816, PM59000995, PA00107784, PA00107783, PA00107549, PA00107358 (1929), PA59000232,
PA59000231 (1928), PA00108424 (1682), PM62001934, PA00108332, PA00116194/93/95, PA00116224 (1719), PA00116138,
PA80000063 (16 févr. 2009), PA80000004, IA00076408, PM80005288, IA80000292, PA80000086, PA00094498, PA00094499
(4, rue Philippe-Féral), PA31000123, PA00086489 ; Estaires (Wikipédia).
Distances justes à ±0,3 km : Lynde–Sercus 2,7 ; Lynde–Renescure 4,1 ; Lynde–Saint-Jans-Cappel 21,9 ; Lynde–Wallon-
Cappel 4,1 ; Mont-Noir–Saint-Jans 1,9 ; Croix-du-Bac–Bac-Saint-Maur 1,7, –Sailly 2,5, –Steenwerck 2,9, –Estaires 6,0,
–Armentières 6,5 ; Marquay–Bailleul-aux-C. 2,2, –Ligny 2,8, –Monts 7,2, –Saint-Pol 5,9, –Roëllecourt 2,8,
–La Thieuloye 3,7, –Saint-Michel 4,4 ; Oppy–Monts 7,4, –Lucheux 6,6 ; Raincheval–Hédauville 9,8 ; Acheux–Raincheval 6,7,
–Belle-Église 3,2, –Martinsart 8,0, –Amplier 11,9, –Beaumont-Hamel 8,9, –Varennes 2,6, –Marcelcave 24,9, –Bertrancourt
2,9, –Forceville 2,1, –Bouzincourt 7,5, –Englebelmer 5,6, –Franvillers 11,9, –Louvencourt 3,4, –Senlis 6,0 ;
Albert–Martinsart 4,5, –Bouzincourt 4,1, –Aveluy 2,5, –La Boisselle 3,6, –Senlis 6,0 ; Hérissart–Puchevillers 2,8,
–Rubempré 2,4, –Toutencourt 3,2, –Molliens 5,0, –Doullens 15,3, –Irles 25,4, –Arras 39,2, –Flixecourt 23,9 ;
Bayencourt–Gommecourt 5,3.
Rues : rue d'Armenonville (Neuilly), rues Sire-Firmin-Leroux et Duméril, bd d'Alsace-Lorraine (Amiens), rue de
Raincheval (Toutencourt), rue Alfred-Guibert, place Emma-Calvé (Millau), rues de Lille et d'Ypres (Bailleul) existent.
Itinéraires : métro (lignes 1, 4, 5 ; Porte Maillot terminus), Clermont–Gannat–Saint-Germain-des-Fossés (pas encore de
Vichy–Riom), Brioude sur Clermont–Nîmes, ligne des Causses, gare d'Orsay.

## 5. Sources consultées
POP https://www.pop.culture.gouv.fr ; Nominatim https://nominatim.openstreetmap.org ; geo.api.gouv.fr ;
Baedeker, Northern France, 1909 (archive.org/details/northernfranc00karl) ; LLT, XIII Corps
(longlongtrail.co.uk) ; CWGC, Bailleul Communal Cemetery Extension (cwgc.org/find-a-cemetery/cemetery/2000048) ;
Wikipédia « Bavincourt », « Frévent », « Estaires » ; Geneanet, cartes postales du Bourget ; commune-mairie.fr
(Saulty) ; Wikidata Q559663 ; dossiers R4–R6 ; P. Combes, livre familial.
