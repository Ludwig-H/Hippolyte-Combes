# -*- coding: utf-8 -*-
"""
Enrichissement philologique, apparat des loci paralleli (en latin) et commentaire
historique resserré pour les 186 folios du Livre-Journal d'Hippolyte Combes.
"""

import json
import re
from pathlib import Path

EDITION_DIR = Path(__file__).resolve().parent
HIST_JSON_PATH = EDITION_DIR / "relecture_integrale_2026_10" / "relecture_historique_001_186.json"


def folio_label_for(scan_num: int) -> str:
    if scan_num == 1:
        return "Couverture (plat supérieur)"
    fnum = scan_num // 2
    rv = "recto" if (scan_num % 2 == 0) else "verso"
    return f"Folio {fnum} {rv}"


def folio_latin_ref(scan_num: int) -> str:
    if scan_num == 1:
        return r"in tegumento (p.~\pageref{fol:1})"
    fnum = scan_num // 2
    rv = r"r\textsuperscript{o}" if (scan_num % 2 == 0) else r"v\textsuperscript{o}"
    return f"f\\textsuperscript{{o}}~{fnum}~{rv} (p.~\\pageref{{fol:{scan_num}}})"


def folio_fr_ref(scan_num: int) -> str:
    if scan_num == 1:
        return r"Couverture (p.~\pageref{fol:1})"
    fnum = scan_num // 2
    rv = r"r\textsuperscript{o}" if (scan_num % 2 == 0) else r"v\textsuperscript{o}"
    return f"f\\textsuperscript{{o}}~{fnum}~{rv} (p.~\\pageref{{fol:{scan_num}}})"


def mois_annee_for(scan_num: int) -> str:
    if scan_num == 1:
        return "Juillet 1916 – Avril 1917"
    if scan_num <= 7:
        return "Juillet 1916"
    if scan_num <= 32:
        return "Août 1916"
    if scan_num <= 57:
        return "Septembre 1916"
    if scan_num <= 89:
        return "Octobre 1916"
    if scan_num <= 104:
        return "Novembre 1916"
    if scan_num <= 117:
        return "Décembre 1916"
    if scan_num <= 136:
        return "Janvier 1917"
    if scan_num <= 160:
        return "Février 1917"
    if scan_num <= 174:
        return "Mars 1917"
    return "Avril 1917"


# Lignes exactes du Folio 1 recto (Scan #002, 20251126_092932.jpg) :
# 21 lignes conformes à la disposition du manuscrit autographe (avec "m." à la l. 1
# et "Courte nuit, pensé très vivement à Margte —" à la l. 2).
SCAN_002_LINES = [
    r"25 Ma. Levé dès 8 H m. Bien reposé \hfill Juillet 1916",
    "Courte nuit, pensé très vivement à Margte —",
    "Toujours même ciel gris et bas : ciel de",
    "Flandre. Beaux arbres élancés aux branches",
    "retombantes entourent pâturages ou champs",
    "d'avoine et de blé — épis très hauts & serrés",
    "Mélancolie éparse à travers atmosphère",
    "Matin, venu à pied, avec fantastique",
    "lieutt Curtis au village de Sercus, où notre",
    "rassemblement se fait devant cimetière qui",
    "entoure église très curieuse —",
    "Après-midi : bien reposé chambre — quand",
    "terminé déménagement sur le derrière, à",
    "cause de l'arrivée 36 off. du R. Fusrs —",
    "Visité longuement église village : remarqué",
    "2 rangs de statues (en plâtre, en bois) sous les",
    "orgues",
    "Vers 7 h 1/2 s., visite des dames du chateau",
    "et les ai conduites au mess de mes off.",
    "A Mme Backer, pour repas d'hier & 4 oeufs : 1 f 75",
    "Varia : 75 c",
]


# Registre 1 : Commentaire critique interne (uniquement sur les folios présentant
# une particularité codicologique, matérielle, structurelle ou paléographique
# qui n'entre pas dans l'apparat marginal). Vide ("") partout ailleurs.
CRITIQUES_PERTINENTES = {
    1: r"\textbf{l.~1--5 :} Plat supérieur du carnet revêtu d'un papier fort rouge gaufré à motif de losanges ; au centre, étiquette rectangulaire de papier bleu à pans coupés portant l'intitulé autographe en cinq lignes à l'encre noire, avec soulignement du titre et deux tirets séparateurs.",
    2: r"\textbf{l.~1--21 :} Première page écrite du carnet, ouverte \textit{in medias res} le mardi 25 juillet 1916. Hippolyte Combes place la date soulignée (\textit{25 Ma.}) en tête de la l.~1 et le mois souligné (\textit{Juillet 1916}) légèrement surélevé dans l'angle supérieur droit ; au bas du feuillet (l.~20--21), un trait horizontal sépare le journal proprement dit du relevé des dépenses.",
    3: r"\textbf{l.~17 :} Un trait horizontal sépare au bas du feuillet le récit quotidien et le relevé comptable bilingue (\textit{Food} / \textit{Washing}).",
    4: r"\textbf{l.~18--25 :} Au bas du feuillet, le relevé des dépenses et de la solde est séparé du récit par un trait horizontal et subdivisé par deux sous-titres topographiques soulignés (\textit{A Renescure}, \textit{A Hazebrouck}).",
    5: r"\textbf{l.~20--23 :} Les quatre dernières lignes, consacrées au règlement de la logeuse de Lynde et aux frais de route, sont isolées du récit par un trait horizontal continu.",
    9: r"\textbf{l.~1--23 :} Ce feuillet réunit deux journées consécutives (mercredi 2 août, l.~1--12, et jeudi 3 août, l.~13--23) séparées par un trait horizontal à mi-page, chacune close par son relevé de dépenses.",
    13: r"\textbf{l.~15--17 :} Au bas du feuillet, un trait horizontal sépare du récit les trois lignes du compte d'achats auprès de la logeuse (\textit{oeufs, lait \& bière}) et de cartes postales.",
    16: r"\textbf{l.~1--20 :} La page regroupe le récit de la promenade du jeudi 10 août le long de la Lys jusqu'à Sailly (l.~1--18), une notation isolée (\textit{Les Australiens}, l.~19) et un relevé de dépenses au bas du feuillet (l.~20).",
    17: r"\textbf{l.~5--6 et 12 :} Dans le récit du bombardement d'Erquinghem, les mots les plus crus décrivant le sort du soldat touché (\textit{décapité}, \textit{bras emportés}, l.~6) et l'épithète initiale qualifiant l'insécurité (\textit{perpétuelle}, l.~12) ont été biffés par Hippolyte Combes, mais demeurent partiellement déchiffrables sous la rature.",
    21: r"\textbf{l.~1--22 :} Deux entrées successives (vendredi 18 août, l.~1--12, et samedi 19 août, l.~13--22) séparées par un trait horizontal ; la phrase de la l.~22 se poursuit sans interruption en tête du f\textsuperscript{o}~11~r\textsuperscript{o}.",
    22: r"\textbf{l.~1 :} La première ligne poursuit directement la phrase commencée au bas du f\textsuperscript{o}~10~v\textsuperscript{o} ; la mention de date (\textit{19 Sam --}) est rejetée à l'extrémité droite de la ligne.",
    23: r"\textbf{l.~1--24 :} Le feuillet réunit les journées du dimanche 20 août (l.~1--14) et du lundi 21 août (l.~15--24), séparées par un trait horizontal et closes par un relevé comptable entre crochets (l.~23--24).",
    28: r"\textbf{l.~1--22 :} Feuillet de suite du vendredi 25 août 1916 (\textit{Ven. 25 (suite)}) ; les réflexions personnelles des l.~6--8 sont ponctuées de tirets longs caractéristiques de l'écriture expressive d'Hippolyte Combes.",
    34: r"\textbf{l.~1--21 :} Ce feuillet réunit le samedi 2 septembre (l.~1--11, clos par un relevé de blanchissage entre crochets aux l.~10--11) et le début du dimanche 3 septembre (l.~12--21), dont la suite et les comptes se trouvent au f\textsuperscript{o}~18~r\textsuperscript{o}.",
    35: r"\textbf{l.~1--22 :} Le f\textsuperscript{o}~17~v\textsuperscript{o} porte les entrées des lundi 4 (l.~1--10) et mardi 5 septembre 1916 (l.~11--22), tandis que le f\textsuperscript{o}~18~r\textsuperscript{o} contient la fin de l'entrée du dimanche 3 septembre : Hippolyte Combes a rédigé les journées des 4 et 5 septembre sur la page de gauche avant ou après avoir complété le compte du 3 septembre sur la page en regard.",
    36: r"\textbf{l.~1--9 :} Fin du récit paysager (l.~1--5) et relevé des dépenses (l.~6--9) de la journée du dimanche 3 septembre 1916, faisant suite au f\textsuperscript{o}~17~r\textsuperscript{o}.",
    49: r"\textbf{l.~1--21 :} Le feuillet est intégralement consacré à la journée du dimanche 24 septembre 1916 au camp d'Acheux, sans bloc comptable final, la page se refermant sur la notation auditive du canon grondant sur le front (l.~21).",
    52: r"\textbf{l.~1--22 :} Première page consacrée à la journée parisienne du mardi 26 septembre 1916 (arrivée au Bourget, gare du Nord, gare d'Orsay et courses rive gauche), poursuivie au f\textsuperscript{o}~26~v\textsuperscript{o}.",
    53: r"\textbf{l.~11--21 :} Seconde page du mardi 26 septembre 1916, occupée dans sa moitié inférieure par le tableau détaillé des achats et frais de transport effectués par Hippolyte Combes à Paris avant son départ pour Toulouse.",
    61: r"\textbf{l.~1--10 :} Feuillet associant un bilan des dépenses de la permission toulousaine du 3 octobre 1916 (tailleur Guiraud, loyer de M\textsuperscript{lle}~Guilhem, l.~2--7) et une brève notation mondaine sur la visite de la propriété de M\textsuperscript{me}~de Labarthe (l.~8--10).",
    63: r"\textbf{l.~1--19 :} Le f\textsuperscript{o}~31~v\textsuperscript{o} (journée du jeudi 5 octobre 1916 à Paris et retour vers le front) et le f\textsuperscript{o}~32~r\textsuperscript{o} (soirée du mercredi 4 octobre et nuit du 4 au 5 octobre dans l'express Toulouse--Paris) ont été photographiés ou rédigés dans l'ordre inverse de la chronologie.",
    64: r"\textbf{l.~1--13 :} Ce feuillet (fin de la journée du 4 octobre 1916 au départ de Toulouse, l.~1--6, et relevé des dépenses de la veille, l.~7--13) précède chronologiquement le f\textsuperscript{o}~31~v\textsuperscript{o}.",
    74: r"\textbf{l.~14--15 :} Au bas du récit de l'étape de Beauval, un trait horizontal sépare les deux dernières lignes consacrées aux menues dépenses de blanchissage (\textit{washing \& darning}), d'ordonnance et de cartes postales.",
    75: r"\textbf{l.~1 :} L'en-tête de la l.~1 réunit sur une même ligne la date soulignée (\textit{Lundi 16}), un trait vertical de séparation, le début du récit (\textit{Sur pied à 5h~1/2}) et le rappel du mois (\textit{Oct /16}) rejeté à droite.",
    90: r"\textbf{l.~10--12 :} Au milieu du récit du départ d'Albert pour Acheux, Hippolyte Combes oppose en deux phrases nominales lapidaires la colère du major Hughes (\textit{Major Hughes tempêté}) et la décision écrite du colonel Grose (\textit{Col. Grose, signé ordre}).",
    91: r"\textbf{l.~1--17 :} Ce feuillet (fin de la journée du 2 novembre, l.~1--6, et journée du 3 novembre 1916, l.~7--17) figure deux fois dans la séquence photographique du carnet (voir f\textsuperscript{o}~46~v\textsuperscript{o}) ; la transcription diplomatique est maintenue à l'identique sur les deux doubles pages.",
    93: r"\textbf{l.~1--17 :} Reproduction de la même page manuscrite que le f\textsuperscript{o}~45~v\textsuperscript{o} (journées des 2 et 3 novembre 1916).",
    105: r"\textbf{l.~1--26 :} Le feuillet s'articule en deux journées (1\textsuperscript{er} décembre, l.~1--16, avec bloc comptable entre crochets aux l.~13--16 ; 2 décembre, l.~17--26) séparées par un trait horizontal.",
    112: r"\textbf{l.~1--24 :} Le f\textsuperscript{o}~56~r\textsuperscript{o} (journées du vendredi 22 décembre, l.~1--11, et du dimanche 24 décembre 1916, l.~12--24) et le f\textsuperscript{o}~56~v\textsuperscript{o} (journées des 19 et 20 décembre 1916) se présentent dans l'ordre inverse de la chronologie.",
    113: r"\textbf{l.~1--21 :} Ce feuillet, qui réunit les entrées des mardi 19 (l.~1--11) et mercredi 20 décembre 1916 (l.~12--21) séparées par un trait horizontal, précède chronologiquement le f\textsuperscript{o}~56~r\textsuperscript{o}.",
    118: r"\textbf{l.~1--23 :} L'année nouvelle (\textit{1917}) est mise en évidence dès l'en-tête souligné de la l.~1 (\textit{1\textsuperscript{er} Lundi --- 1917 --- \hfill Janvier.}) ; le feuillet regroupe les 1\textsuperscript{er} (l.~1--10) et 2 janvier 1917 (l.~11--23).",
    132: r"\textbf{l.~1--10 :} La première moitié de la page est entièrement dédiée au relevé des dépenses de voyage du samedi 27 janvier 1917 (Paris, gares du Nord et d'Orsay, billet pour Toulouse et achats au Bazar de l'Hôtel de Ville), avant le récit de l'arrivée à Toulouse le dimanche 28 janvier (l.~11--22).",
    133: r"\textbf{l.~1--15 :} Feuillet de suite du dimanche 28 janvier 1917 (\textit{Dim. 28. (suite)}), intégralement consacré aux fiançailles officieuses avec Marguerite Calmels à la villa Sainte-Marie et clos par une unique ligne de frais de tramway entre crochets (l.~15).",
    136: r"\textbf{l.~10 :} À la fin du récit de la halte à son appartement toulousain avec Marguerite, Hippolyte Combes a surchargé un mot demeuré incertain dans la proposition \textit{Évité troubler qq [mot non établi] précieuses}.",
    140: r"\textbf{l.~1--10 :} Page entièrement consacrée au relevé comptable des dépenses toulousaines et ferroviaires du samedi 3 février 1917 (dentiste M.~de Lersay, broche, étrennes à Marie, billets et buffet de Bédarieux), chaque poste étant introduit par un tiret cadratin.",
    147: r"\textbf{l.~1--21 :} Deuxième des trois feuillets consacrés à la seule journée du mercredi 7 février 1917 (\textit{Merc. 7 (suite)}), relatant le retour de permission à Acheux et le transfert immédiat en automobile vers Hérissart.",
    148: r"\textbf{l.~1--19 :} Troisième et dernier feuillet de la journée du 7 février 1917 (\textit{Merc. 7 (fin)}, l.~1--11, clos par un bloc comptable récapitulatif aux l.~7--11), suivi de l'entrée du jeudi 8 février (l.~12--19).",
    157: r"\textbf{l.~1 :} Exceptionnellement, Hippolyte Combes inscrit son solde disponible (\textit{En caisse : 225 f. 95}) directement sur la première ligne d'en-tête entre la date soulignée (\textit{19 Lundi}) et le mois (\textit{Février 1917}).",
    165: r"\textbf{l.~1--20 :} La page est entièrement occupée par la méditation du samedi 10 mars 1917 à Hérissart après le départ définitif du capitaine Williams (l.~8--9), sans aucune mention comptable au bas du feuillet.",
    186: r"\textbf{l.~1--17 :} Dernier feuillet écrit du \textit{Livre-Journal}, daté du lundi 30 avril 1917 (date qui correspond au \textit{terminus ad quem} inscrit par Hippolyte Combes sur l'étiquette de la couverture) et clos par deux lignes de dépenses entre crochets (l.~16--17).",
}


# Entrées d'apparat marginal redondantes avec la mise en page diplomatique (\cline, \underline)
# ou purement polémiques vis-à-vis d'anciennes lectures écartées :
APPARAT_DROP_KEYS = {
    (30, 16, "29 Ma"),
    (35, 11, "5 Ma."),
    (36, 3, "qui"),
    (36, 6, "A Saint-Pol"),
    (46, 12, "A Acheux"),
    (47, 16, "2 tins"),
    (48, 21, "litière"),
    (50, 18, "Tip"),
    (53, 11, "Tramway"),
    (54, 13, "Trams"),
    (64, 1, "..."),
    (64, 7, "Hier"),
    (65, 6, "Métro"),
    (69, 10, "A Bernaville"),
    (76, 2, "A Beauval"),
    (80, 20, "Cartes"),
    (84, 13, "Cartes"),
    (85, 14, "Merc. 25"),
    (91, 16, "Mission"),
    (93, 16, "Mission"),
    (111, 23, "[ — Cartes ples"),
    (119, 20, "[ — Amiens"),
    (121, 11, "[ — Washing"),
    (121, 24, "[ — Avis de réception"),
    (124, 11, "[ — Ctes ples"),
    (125, 17, "[ — Matin"),
    (133, 15, "[ — Trams"),
    (145, 16, "[ — Brioude, buffet, varia : 60 c ]"),
    (148, 12, "Jeudi 8."),
    (149, 15, "Ven. 9"),
    (150, 10, "Sam. 10."),
    (166, 4, "Éclat clair"),
    (177, 2, "Levé tôt"),
    (183, 3, "Métier à tisser"),
}

# Réécriture positive et concise des notes d'apparat marginal qui contenaient des mentions
# d'anciennes lectures écartées, de « cliché », de « vue » ou de crochets éditoriaux :
APPARAT_NOTE_OVERRIDES = {
    (9, 11, "5 f 50"): "fin du montant au bord du feuillet, lecture incertaine",
    (17, 6, "⟦décapité [?]⟧"): "rature autographe ; lecture sous la biffure incertaine",
    (17, 6, "⟦bras emportés [?]⟧"): "rature autographe ; lecture sous la biffure incertaine",
    (17, 12, "⟦perpétuelle [?]⟧"): "rature autographe ; lecture sous la biffure incertaine",
    (25, 7, "x"): "signe ou abréviation de quantité devant magasins",
    (27, 9, "[45 ?]"): "chiffres après 2 H de lecture incertaine",
    (28, 6, "[illis.]"): "groupe non déchiffré après L’Etat",
    (30, 24, "etc. [?]"): "fin de ligne peu distincte au bord inférieur du feuillet",
    (34, 20, "[mot surchargé]"): "petit groupe fortement encré avant orage, lecture incertaine",
    (37, 17, "[1/2 ?] longue[s?] heure[s?]"): "durée et marques de nombre incertaines",
    (39, 24, "[Connelly ?]"): "patronyme de lecture incertaine au bas du feuillet",
    (40, 9, "[s. ?]"): "indication horaire après 1 H de lecture incertaine",
    (46, 13, "0.25 c."): "notation décimale suivie de c. telle qu’inscrite dans le manuscrit",
    (47, 6, "Bedfs"): "Bedfords (Bedfordshire Regiment)",
    (47, 16, "2 tins of coffee milk"): "deux boîtes de lait concentré au café",
    (48, 20, "[bâche ?]"): "mot de lecture incertaine après épaisse",
    (48, 22, "("): "parenthèse ouvrante avant cooking non refermée dans le manuscrit",
    (48, 23, "Carte du Petit Journal"): "crochet ouvrant autographe à gauche du compte inférieur",
    (51, 15, "jeté bombes"): "construction elliptique sans auxiliaire",
    (53, 5, "[Lgt/1/2 h ?]"): "durée ou adverbe avant assis de lecture incertaine",
    (54, 2, "[wagt ?]"): "abréviation commençant par wa- (probablement wagon), finale incertaine",
    (57, 17, "p. Rem ?"): "ajout marginal à droite de Sons différents, lecture incertaine",
    (60, 10, "[Castanet/cravate ?]"): "groupe de lecture incertaine",
    (61, 5, "1916"): "millésime inscrit sous Juillet dans l’interligne",
    (62, 15, "[groupe surchargé illis.]"): "groupes fortement surchargés avant le choix du compartiment",
    (67, 10, "Ve"): "Veuve (suivi d’un espace laissé en blanc)",
    (74, 9, "[blanc]"): "espace laissé en blanc après de dans le manuscrit",
    (75, 12, "battalions"): "encrage très dense au contact des hampes de la ligne précédente",
    (77, 1, "1/2 route"): "mi-route, à mi-chemin",
    (77, 9, "17 Mardi"): "date inscrite au bas de la page après la fin du récit du 16 octobre",
    (79, 1, "sur l."): "sur laquelle",
    (83, 4, "1/2 jour"): "milieu du jour, vers midi",
    (83, 8, "1914 [?]"): "millésime de lecture incertaine",
    (85, 9, "[Lépin ?]"): "patronyme de lecture incertaine",
    (86, 11, "[R.E. ?]"): "R.E. ou R.F., initiales d’unité de lecture incertaine",
    (89, 7, "1/2"): "milieu, dans au milieu de pierres",
    (90, 7, "[Lépin ?]"): "patronyme de lecture incertaine",
    (90, 15, "[verbe illis.]"): "verbe non déchiffré devant [au ?] kit",
    (91, 4, "Donné"): "crochet ouvrant autographe à gauche réunissant les trois lignes de dépenses",
    (93, 4, "Donné"): "crochet ouvrant autographe à gauche réunissant les trois lignes de dépenses",
    (94, 15, "[ajout interl. illis.]"): "petit groupe interlinéaire non déchiffré sous du et avant corps",
    (94, 17, "qq froid"): "abréviation de lecture incertaine devant froid",
    (98, 16, "cars"): "véhicules automobiles",
    (99, 22, "[blanc]"): "espace laissé en blanc après M. dans le manuscrit",
    (102, 7, "[illis.]"): "groupe non déchiffré",
    (103, 17, "côtés"): "trait de renvoi courbe descendant de chaussées vers côtés",
    (108, 6, "Houtteman [?]"): "patronyme de lecture incertaine",
    (117, 24, "= 88 fr."): "total autographe différent de la somme des quatre postes inscrits (78 francs)",
    (128, 9, "[addition interlinéaire : compartiment]"): "mot ajouté dans l’interligne supérieur",
    (136, 10, "[mot non établi]"): "mot non déchiffré",
    (141, 2, "[Monté ?]"): "groupe initial fortement repassé, lecture incertaine",
    (142, 6, "Layral"): "graphie autographe sans -s final pour Layrals",
    (143, 3, "gd"): "grande (accordé avec chambre)",
    (143, 16, "s."): "abréviation horaire (soir) employée ici après minuit 30",
    (150, 12, "Lignes"): "Lignes (abrégé L suivi d’une terminaison suscrite)",
    (151, 19, "1/2 du jour"): "milieu du jour, vers midi",
    (153, 10, "une"): "mot ajouté sous la ligne précédente, devant buée grise",
    (154, 16, "Gouin[?]"): "toponyme ou patronyme de lecture incertaine",
    (155, 17, "[Roulé ?]"): "Roulé ou Rôdé, lecture incertaine",
    (158, 14, "de semelles liège"): "début de ligne abrupt devant de semelles liège",
    (159, 18, "9h"): "9 heures (chiffre 9 bouclé suivi de h suscrit)",
    (159, 20, "1/2 journée"): "une demi-journée",
    (159, 21, "English novel"): "roman anglais",
    (162, 18, "[ Washing : 60 c. ]"): "note tracée au crayon à droite",
    (163, 9, "Maral"): "maréchal (dans maréchal des logis)",
    (163, 12, "cie"): "compagnie",
    (164, 11, "logis..."): "points de suspension autographes tenant lieu de patronyme",
    (164, 15, "mervt"): "merveilleux ou merveilleusement (finale abrégée épaissie)",
    (165, 12, "English"): "Anglais (les militaires britanniques déjà connus d’Hippolyte Combes)",
    (166, 11, "n°, rue"): "deux emplacements laissés en blanc après n° et rue dans le manuscrit",
    (166, 15, "Godard"): "patronyme tracé au crayon après le grade",
    (167, 18, "Calvert's Tooth Powder"): "poudre dentifrice Calvert",
    (168, 13, "rue,"): "emplacement du nom de rue laissé en blanc dans le manuscrit",
    (168, 21, "1/2 jour"): "milieu du jour, vers midi",
    (169, 11, "répar."): "réparation(s)",
    (169, 22, "et à soie"): "complément sous la ligne de lecture incertaine",
    (170, 5, "q. mnts"): "quelques minutes (ou moments)",
    (171, 11, "Houtteman[?]"): "patronyme de lecture incertaine",
    (172, 11, "afternoon"): "après-midi",
    (175, 7, "dû au 31 mars"): "début d’intitulé d’encrage pâle (du ou dû)",
    (177, 3, "staff"): "membre du personnel d’état-major",
    (177, 15, "pamphlets"): "brochures ou opuscules",
    (178, 2, "1/2 après-midi"): "moitié de l’après-midi",
    (179, 9, "(10 f. 50 + 14 f. = 24 f. 50)"): "addition autographe entourée d’un trait oblique",
    (181, 11, "1915"): "millésime autographe (dernier chiffre 5 bien formé)",
    (181, 18, "Ribemont"): "toponyme ajouté sous Buire dans l’interligne",
    (181, 18, "stuck"): "embourbés, immobilisés",
    (182, 12, "Bte"): "Baptiste",
    (182, 14, "[avec ?]"): "préposition de lecture incertaine après carte",
    (185, 2, "Commt"): "commencement",
    (185, 17, "water-cart"): "voiture-citerne à eau",
    (185, 19, "cie"): "compagnie",
    (186, 7, "cie"): "compagnie",
    (186, 12, "tea-dinner"): "thé-dîner (repas du soir accompagné de thé)",
}


# Catalogue prosopographique, militaire, topographique et thématique pour la
# génération de l'apparat latin des Loci Paralleli :
# (id, regex_in_line, canonical_lemma_override_or_None, appendix_ref_or_None)
LOCI_ENTITIES = [
    ("marguerite", r"\b(?:Margte|Marg\.|Mte|Marguerite|Gueïte|ma\s+Femme|fiancée|Fiancée)\b", None, r"Appendicem I, doc.~5 (p.~\pageref{annexe:doc5})"),
    ("curtis", r"\b(?:Curtis|Ctis)\b", None, None),
    ("r_fusiliers", r"\b(?:R\.\s*Fusrs|Royal\s+Fusiliers|R\.F\.)\b", None, None),
    ("michel", r"\bLt\s+Michel\b", "Lt Michel", None),
    ("sercus", r"\bSercus\b", "Sercus", None),
    ("lynde", r"\bLynde\b", "Lynde", None),
    ("renescure", r"\bRenescure\b", "Renescure", None),
    ("hazebrouck", r"\bHazebrouck\b", "Hazebrouck", None),
    ("ypres", r"\bYpres\b", "Ypres", None),
    ("st_jans_cappel", r"\b(?:St-Jans-Cappel|Saint-Jans-Cappel)\b", None, None),
    ("mont_noir", r"\bMont[- ]Noir\b", None, None),
    ("bailleul", r"\bBailleul\b(?!-aux-Cornailles)", "Bailleul", None),
    ("steenwerck", r"\bSteenwerck\b", "Steenwerck", None),
    ("croix_du_bac", r"\b(?:La\s+)?Croix-du-Bac\b", "La Croix-du-Bac", None),
    ("bac_st_maur", r"\bBac-S(?:ain)?t-Maur\b", None, None),
    ("lys", r"\bLys\b", "Lys", None),
    ("connelly", r"\bConnelly\b", "Connelly", None),
    ("maurin", r"\bMaurin\b", "Maurin", None),
    ("sailly", r"\bSailly(?:-sur-la-Lys)?\b", None, None),
    ("maxse", r"\bMaxse\b", "Maxse", r"Appendicem I, doc.~1 (p.~\pageref{annexe:doc1})"),
    ("armentieres", r"\bArmentières\b", "Armentières", None),
    ("barbry", r"\bBarbry\b", "Barbry", None),
    ("fleurbaix", r"\bFleurbaix\b", "Fleurbaix", None),
    ("erquinghem", r"\bErquinghem\b", "Erquinghem", None),
    ("schumacher", r"\bSchumacher\b", "Schumacher", r"Appendicem I, doc.~1 (p.~\pageref{annexe:doc1})"),
    ("lepin", r"\b(?:Lupin|Lépin|Liepin)\b", None, None),
    ("nogent", r"\bNogent(?:-le-Rotrou|-le-R\.)?\b", None, r"Appendicem I, doc.~2 et 5 (p.~\pageref{annexe:doc2})"),
    ("estaires", r"\bEstaires\b", "Estaires", None),
    ("st_pol", r"\b(?:St-Pol|Saint-Pol)\b", None, r"Appendicem I, doc.~5 (p.~\pageref{annexe:doc5})"),
    ("marquay", r"\bMarquay\b", "Marquay", None),
    ("bailleul_cornailles", r"\bBailleul-aux-Cornailles\b", "Bailleul-aux-Cornailles", None),
    ("ramecourt", r"\bRamecourt\b", "Ramecourt", None),
    ("ostreville", r"\bOstreville\b", "Ostreville", None),
    ("ligny", r"\bLigny(?:-St-Flochel|-Saint-Flochel)?\b", None, None),
    ("roellecourt", r"\b(?:Roellecourt|Roëllecourt)\b", None, None),
    ("st_michel_ternoise", r"(?<!Bvd\s)(?<!faubg\s)\bSt-Michel\b", "St-Michel", None),
    ("bvd_st_michel", r"\bBvd\s+St-Michel\b", "Bvd St-Michel", None),
    ("bedfords", r"\b(?:Bedfords|Bedfs)\b", None, None),
    ("west", r"\b(?:Cap\.|Capt\.)\s*West\b|\bWest\b", None, None),
    ("panton", r"\b(?:Cap\.|Capt\.|Lt)\s*(?:Panton|Pant\.)|\bPanton\b", None, None),
    ("walsh", r"\b(?:Lt\s+)?Walsh\b", None, None),
    ("ford", r"\b(?:Lt\s+)?Ford\b", None, None),
    ("beaudricourt", r"\bBeaudricourt\b", "Beaudricourt", None),
    ("oppy", r"\bOppy\b", "Oppy", None),
    ("lucheux", r"\bLucheux\b", "Lucheux", None),
    ("thievres", r"\bThièvres\b", "Thièvres", None),
    ("raincheval", r"\bRaincheval\b", "Raincheval", None),
    ("acheux", r"\bAcheux(?:-Varennes|-en-Amiénois)?\b", None, None),
    ("hedauville", r"\bHédauville\b", "Hédauville", None),
    ("forceville", r"\bForceville\b", "Forceville", None),
    ("varennes", r"\bVarennes\b", "Varennes", None),
    ("lealvillers", r"\bLéalvillers\b", "Léalvillers", None),
    ("arquèves", r"\bArquèves\b", "Arquèves", None),
    ("belle_eglise", r"\bBelle[- ]Église\b", None, None),
    ("houthouan", r"\b(?:Houthouan|Houtteman)\b", None, None),
    ("louvencourt", r"\bLouvencourt\b", "Louvencourt", None),
    ("bertrancourt", r"\bBertrancourt\b", "Bertrancourt", None),
    ("bus_les_artois", r"\bBus(?:-lès-Artois)?\b", None, None),
    ("paris", r"\bParis\b", "Paris", r"Appendicem I, doc.~5 (p.~\pageref{annexe:doc5})"),
    ("neuilly", r"\bNeuilly\b", "Neuilly", r"Appendicem I, doc.~5 (p.~\pageref{annexe:doc5})"),
    ("faure", r"\bFaure\b", "Faure", r"Appendicem I, doc.~5 (p.~\pageref{annexe:doc5})"),
    ("st_jacques", r"\brue\s+St-Jacques\b|\bPanthéon\b|\bSte-Geneviève\b", None, r"Appendicem I, doc.~5 (p.~\pageref{annexe:doc5})"),
    ("zyromski", r"\bZyromski\b", "Zyromski", None),
    ("maeterlinck", r"\bMaeterlinck\b", "Maeterlinck", r"Appendicem I, doc.~5 (p.~\pageref{annexe:doc5})"),
    ("toulouse", r"\bToulouse\b", "Toulouse", r"Appendicem I, doc.~1 et 3 (p.~\pageref{annexe:doc1})"),
    ("crouzet", r"\b(?:Crouzet|Czt\.?|Oncle|Tante)\b", None, None),
    ("jean_crouzet", r"\bJean\b", "Jean", None),
    ("ste_marie", r"\bSte-Marie(?:-des-Champs)?\b", None, None),
    ("st_etienne", r"\bSt-Etienne\b|\bSaint-Étienne\b", None, None),
    ("st_sernin", r"\bSt-Sernin\b", "St-Sernin", None),
    ("dalbade", r"\bDalbade\b", "Dalbade", None),
    ("daurade", r"\bDaurade\b", "Daurade", None),
    ("assezat", r"\bAssézat\b", "Assézat", None),
    ("labit", r"\bLabit\b", "Labit", None),
    ("pfister", r"\bPfister\b", "Pfister", None),
    ("spagnol", r"\bSpagnol\b", "Spagnol", None),
    ("labarthe", r"\b(?:Mme\s+de\s+)?Labarthe\b", "Mme de Labarthe", None),
    ("guilhem", r"\bMlle\s+Guilhem\b", "Mlle Guilhem", None),
    ("millau", r"\bMillau\b", "Millau", r"Appendicem I, doc.~5 (p.~\pageref{annexe:doc5})"),
    ("mimi", r"\bMimi\b", "Mimi", None),
    ("madeleine", r"\b(?:Madeleine|Madne)\b", None, None),
    ("pierre_calmels", r"\bPierre\b", "Pierre", None),
    ("vincens", r"\b(?:Vincens|Fernand|Robert)\b|(?<!fille\s)\bGermaine\b", None, None),
    ("layral", r"\bLayral\b", "Layral", None),
    ("brioude", r"\bBrioude\b", "Brioude", None),
    ("amiens", r"\bAmiens\b", "Amiens", None),
    ("doullens", r"\bDoullens\b", "Doullens", None),
    ("canaples", r"\bCanaples\b", "Canaples", None),
    ("coy_152", r"\b152(?:nd|e)?\s*(?:Coy|Cy|Cie)?\b", None, None),
    ("coy_150", r"\b150(?:th|e)?\s*(?:Coy|Cy|Cie)?\b", None, None),
    ("div_18", r"\b18(?:th|e)\s*(?:Div(?:on|\.)?|Division)\b", None, r"Appendicem I, doc.~1 et 2 (p.~\pageref{annexe:doc1})"),
    ("brig_54", r"\b54(?:th|e)\s*Brigade\b", None, None),
    ("ribeaucourt", r"\bRibeaucourt\b", "Ribeaucourt", None),
    ("barlette", r"\bBarlette\b", "Barlette", None),
    ("bernaville", r"\bBernaville\b", "Bernaville", None),
    ("prouville", r"\bProuville\b", "Prouville", None),
    ("domqueur", r"\bDomqueur\b", "Domqueur", None),
    ("beauval", r"\bBeauval\b", "Beauval", None),
    ("warloy", r"\bWarloy(?:-Baillon)?\b", None, None),
    ("senlis", r"\bSenlis(?:-le-Sec)?\b", None, None),
    ("albert", r"\bAlbert\b", "Albert", None),
    ("aveluy", r"\bAveluy\b", "Aveluy", None),
    ("bouzincourt", r"\bBouzincourt\b", "Bouzincourt", None),
    ("martinsart", r"\bMartinsart\b", "Martinsart", None),
    ("mesnil", r"\bMesnil\b", "Mesnil", None),
    ("flutre", r"\bFlutre\b", "Flutre", None),
    ("pizzi", r"\bPizzi\b", "Pizzi", r"Appendicem I, doc.~1 (p.~\pageref{annexe:doc1})"),
    ("grose", r"\bGrose\b", "Col. Grose", None),
    ("hughes", r"\bHughes\b", "Major Hughes", None),
    ("levy", r"\bLevy\b", "Major Levy", None),
    ("purchase_board", r"\b(?:Purchase\s+Board|Army\s+P\.\s*Board|P\.\s*Board)\b", None, None),
    ("huguet", r"\b(?:Huguet|Cap\.\s*H\.)\b", None, None),
    ("raucoule", r"\bRaucoule\b", "Raucoule", None),
    ("williams", r"\b(?:Williams|Wms|Cap\.\s*W\.|Capt\.\s*W\.)\b", None, None),
    ("toutencourt", r"\bToutencourt\b", "Toutencourt", None),
    ("puchevillers", r"\bPuchevillers\b", "Puchevillers", None),
    ("herissart", r"\bHérissart\b", "Hérissart", None),
    ("rubempre", r"\bRubempré\b", "Rubempré", None),
    ("contay", r"\bContay\b", "Contay", None),
    ("pierregot", r"\bPierregot\b", "Pierregot", None),
    ("mirvaux", r"\bMirvaux\b", "Mirvaux", None),
    ("molliens", r"\bMolliens(?:-au-Bois)?\b", None, None),
    ("montigny", r"\bMontigny\b", "Montigny", None),
    ("beaucourt", r"\bBeaucourt\b", "Beaucourt", None),
    ("vadencourt", r"\bVadencourt\b", "Vadencourt", None),
    ("harponville", r"\bHarponville\b", "Harponville", None),
    ("talmas", r"\bTalmas\b", "Talmas", None),
    ("villers_bocage", r"\bVillers-Bocage\b", "Villers-Bocage", None),
    ("buire", r"\bBuire(?:-sur-l'Ancre)?\b", None, None),
    ("ribemont", r"\bRibemont\b", "Ribemont", None),
    ("heilly", r"\bHeilly\b", "Heilly", None),
    ("franvillers", r"\bFranvillers\b", "Franvillers", None),
    ("quesnoy", r"\bQuesnoy\b", "Quesnoy", None),
    ("beauquesne", r"\bBeauquesne\b", "Beauquesne", None),
    ("authie", r"\bAuthie\b", "Authie", None),
    ("st_leger", r"\bSt-Léger\b", "St-Léger", None),
    ("candas", r"\bCandas\b", "Candas", None),
    ("auxi", r"\bAuxi-le-Château\b", "Auxi-le-Château", None),
    ("croughton", r"\bCroughton\b", "Lt Croughton", None),
    ("valet", r"\bValet\b", "Valet", None),
    ("godard", r"\bGodard\b", "Lt Godard", None),
    ("gilbert", r"\bGilbert\b", "Lt Gilbert", None),
    ("jersey", r"\bJersey\b", "Jersey", None),
    ("div_63", r"\b63(?:rd|e)\s*Div(?:ision|\.)?\b|\bnaval\s+division\b", None, None),
    ("miraumont", r"\bMiraumont\b", "Miraumont", None),
    ("achiet", r"\bAchiet(?:-le-Pt\.|-le-Petit)?\b", None, None),
    ("lancers_17", r"\b17(?:th|e)\s*Lancers\b|\bDeath\s+or\s+Glory\b|\bcav(?:alerie|rie)\s+indienne\b", None, None),
    ("arras", r"\bArras\b", "Arras", None),
    ("forage", r"\b(?:green\s+forage|green\s+fourrage|fourrage|fourragères|luzerne|paille\s*&\s*foin)\b", None, None),
    ("bois_ribeaucourt", r"\b(?:grand\s+bois\s+de\s+Ribeaucourt|lisière\s+forêt|pénétré\s+forêt)\b", "forêt", None),
    ("solde_84", r"\b84\s*f(?:r\.?)?\b", "84 f.", None),
    ("solde_78_75", r"\b78\s*f(?:r\.?)?\s*75", "78 f. 75", None),
    ("cooking", r"\bcooking\b", "cooking", None),
    ("hair_cut", r"\b[Hh]air\s+cut\b", "Hair cut", None),
    ("ymca", r"\bY\.M\.C\.A\.", "Y.M.C.A.", None),
    ("efc", r"\b(?:E\.F\.C\.|Exp\.\s*F\.\s*Canteen|Canteen|canteen)\b", None, None),
]


# Réécritures historiques ciblées et resserrées pour les folios clés :
HISTORIQUE_OVERRIDES = {
    1: r"Les bornes chronologiques portées sur l'étiquette couvrent neuf mois de campagne d'\textbf{Hippolyte Combes} (né à Millau le 14 août 1876, décédé le 2 septembre 1970 à l'Hôtel du Centre à Saint-Chély-d'Apcher, Lozère) auprès du corps expéditionnaire britannique (\textit{British Expeditionary Force}). Affecté depuis août 1915 à la \textbf{152\textsuperscript{e} Compagnie de l'\textit{Army Service Corps}} au sein du Train divisionnaire de la \textbf{18\textsuperscript{e} Division britannique} (\textit{18th Eastern Division}), Hippolyte Combes passe en novembre 1916 au service des achats et réquisitions de fourrage (\textit{Foraging} puis \textit{Army Purchase Board}) dans la Somme.",
    2: r"Relevée de la Somme le 20 juillet 1916 après les combats du bois des Trônes, la \textbf{18\textsuperscript{e} Division britannique} (\textit{18th Eastern Division}, commandée par le major-général Sir Ivor Maxse) gagne la Flandre intérieure (Capt. G.~H.~F. Nichols, \textit{The 18th Division in the Great War}, Londres, Blackwood, 1922, p.~81–85). L'église entourée de son cimetière à \textbf{Sercus} (Nord) est l'église \textbf{Saint-Érasme} (soubassements romans du XII\textsuperscript{e}~s., transformée en \textit{hallekerke} à trois nefs au XVI\textsuperscript{e}~s. ; Base Mérimée, \texttt{PA00107816}).",
    3: r"À \textbf{Lynde} (Nord), Hippolyte Combes assiste le lieutenant Michel (\textit{billeting officer}) pour préparer le cantonnement de 36 officiers des \textbf{\textit{Royal Fusiliers}} (dont le 11\textsuperscript{e} Bataillon appartient à la 54\textsuperscript{e} Brigade de la 18\textsuperscript{e} Division) avant l'ordre de départ pour la frontière belge.",
    4: r"À \textbf{Renescure} (Nord), les deux châteaux remarqués par Hippolyte Combes correspondent au \textbf{château de Zuthove} (demeure seigneuriale de briques entourée de douves, reconstruite à la fin du XV\textsuperscript{e}~s. ; Base Mérimée, \texttt{PA00107784}) et au \textbf{château dit de Philippe de Comines} (ancienne motte castrale remaniée et transformée en mairie ; \texttt{PA00107783}), voisin de l'église-halle \textbf{Notre-Dame-de-l'Assomption}. À \textbf{Hazebrouck}, il visite l'église \textbf{Saint-Éloi} (XVI\textsuperscript{e}~s.) et perçoit 84~francs de solde et indemnités auprès de la Mission française.",
    5: r"Étape routière de huit heures (8~h~30 -- 16~h~30) transférant le train divisionnaire de la 18\textsuperscript{e} Division depuis \textbf{Lynde} jusqu'aux abords de \textbf{Saint-Jans-Cappel} (Nord), au pied des monts des Flandres, en contournant le nœud ferroviaire d'Hazebrouck par les faubourgs.",
    7: r"Le dimanche 30 juillet 1916, Hippolyte Combes note la séparation traditionnelle des hommes et des femmes dans la nef de l'église \textbf{Saint-Jean-Baptiste de Saint-Jans-Cappel} (reconstruite aux XVI\textsuperscript{e} et XVII\textsuperscript{e}~s. au pied du Mont-Noir) et remet 5~fr. de pourboire au maître-cuisinier (\textit{headcook}) \textbf{Hancock}.",
    8: r"Située à 3~km au sud de Saint-Jans-Cappel, la ville de \textbf{Bailleul} (Nord) s'ordonnait autour de sa vaste Grand-Place flamande dominée par l'église \textbf{Saint-Vaast} et l'\textbf{Hôtel de Ville} à beffroi gothique (édifices détruits lors des combats d'avril 1918) ; la comparaison avec \textbf{Béthune} rappelle le séjour antérieur d'Hippolyte Combes en Artois.",
    13: r"Le point de ravitaillement quotidien (\textit{refilling point}) est établi sur la Lys canalisée près de l'écluse de \textbf{Bac-Saint-Maur} (Sailly-sur-la-Lys). Au hameau de \textbf{La Croix-du-Bac} (Steenwerck), l'église de briques rouges décrite par Hippolyte Combes est l'église néo-gothique \textbf{Notre-Dame-des-Sept-Douleurs}, bâtie en 1869–1870 par l'architecte lillois Charles Leroy (Base Mérimée, \texttt{IA59000348}).",
    16: r"Promenade le long de la Lys jusqu'au pont de \textbf{Sailly-sur-la-Lys} (Pas-de-Calais), dont l'église Saint-Vaast avait été incendiée lors des combats d'octobre 1914. À l'écluse, Hippolyte Combes s'entretient avec l'éclusier au sujet du \textbf{major-général Sir Ivor Maxse} (1862–1958), commandant la \textbf{18\textsuperscript{e} Division britannique} de 1914 à janvier 1917 ; la mention des \textit{Australiens} fait écho à l'engagement des divisions de l'I~ et du II~ANZAC Corps dans le secteur voisin de Fromelles et d'Armentières en juillet–août 1916.",
    17: r"Le bombardement allemand du 11 août 1916 sur les abords d'\textbf{Armentières} touche un soldat britannique et endommage la \textbf{blanchisserie industrielle de fils et toiles Barbry}, établie en bordure de la Lys près du pont de Nieppe et dirigée par \textbf{Émile Barbry} (Base Mérimée, \texttt{IA59001501}). Aux l.~20–23, le passage raturé décrit la peine disciplinaire réglementaire britannique dite \textit{Field Punishment No.~1} (\textit{crucifixion}), consistant à attacher le condamné par les poignets et les chevilles à une roue de caisson.",
    21: r"Après avoir perçu le 18 août sa solde et son indemnité de fonctions (84~fr.), Hippolyte Combes accompagne à cheval le lieutenant Curtis le samedi 19 août à 14~h~30, sous des averses glaciales, dans la zone exposée immédiatement en arrière des tranchées de première ligne du secteur de \textbf{Fleurbaix} et d'\textbf{Armentières}.",
    23: r"Le dimanche 20 août 1916, Hippolyte Combes prend le café chez l'industriel blanchisseur \textbf{Émile Barbry} avec les adjudants interprètes français \textbf{Lupin} (ou \textit{Liepin}/\textit{Lépin}) et \textbf{Schumacher} — ce dernier déjà mentionné avec ironie dans la lettre d'Hippolyte Combes du 21 février 1916 comme ancien contremaître d'usine métallurgique l'ayant remplacé au secrétariat de la Mission française de la 18\textsuperscript{e} Division (Annexe~I, doc.~1).",
    24: r"Lors de cette rencontre à \textbf{Bac-Saint-Maur} avec son collègue méridional \textbf{Maurin}, l'expédition ferroviaire en petite vitesse d'un sac de 13~kg de linge personnel depuis la gare de \textbf{Steenwerck} (réseau du Nord) jusqu'à \textbf{Nogent-le-Rotrou} (Eure-et-Loir, réseau de l'État, où Hippolyte Combes résidait avant la guerre au 17, rue Saint-Hilaire comme professeur d'anglais au collège communal) illustre le fonctionnement du service des colis et bagages entre la zone des armées et l'intérieur (3~fr.~80 factage compris).",
    25: r"À \textbf{Estaires} (Nord, sur la Lys), la description de l'église \textbf{Saint-Vaast} (chœur, stalles néo-gothiques et statuettes de bois sculpté dont saint Ambroise) et de l'\textbf{Hôtel de Ville} Renaissance (orné des armoiries de la ville au-dessus du perron) possède une valeur patrimoniale directe : ces deux édifices et leur mobilier furent intégralement anéantis lors de la bataille de la Lys en avril 1918.",
    26: r"À la veille du départ de la 18\textsuperscript{e} Division vers l'Artois et la Somme, Hippolyte Combes entre dans l'église \textbf{Saint-Jean-Baptiste de Steenwerck} (édifice détruit lors de l'offensive allemande d'avril 1918) et y remarque un reliquaire de son saint patron, \textbf{saint Hippolyte}. Le soir, le soldat britannique \textbf{Fisher} transporte ses bagages sous la tente du bureau et Hippolyte Combes règle 4~fr. à sa logeuse \textbf{Mme Cliquennois}.",
    32: r"Descendu de Marquay à \textbf{Saint-Pol-sur-Ternoise} (Pas-de-Calais) par Ramecourt et Saint-Michel-sur-Ternoise, Hippolyte Combes visite l'ancienne chapelle conventuelle des \textbf{Carmes} (XVII\textsuperscript{e}~s., bâtie en briques rouges en 1697 et devenue église paroissiale Saint-Paul après la destruction de l'ancienne église au XVI\textsuperscript{e}~s.), où une plaque commémore la nuit de prière passée en mars 1767 par saint \textbf{Benoît-Joseph Labre} (1748–1783).",
    33: r"À \textbf{Ligny-Saint-Flochel} (Pas-de-Calais), les manœuvres observées en lisière des bois s'inscrivent dans l'entraînement tactique de la \textbf{18\textsuperscript{e} Division britannique} avant son retour sur la Somme (Nichols, 1922, p.~86). L'église \textbf{Saint-Flochel} conserve un clocher de pierre des XV\textsuperscript{e}–XVI\textsuperscript{e}~siècles classé monument historique (Base Mérimée, \texttt{PA00108332}).",
    35: r"Après avoir préparé ses bagages le 4 septembre 1916, Hippolyte Combes apprend le mardi 5 septembre par un sous-officier de service (\textit{orderly N.C.O.}) que le départ de la 18\textsuperscript{e} Division est différé de quelques jours ; l'après-midi, il se rend à pied sous l'averse à \textbf{Roëllecourt} (Pas-de-Calais), siège de la Mission militaire française, où il perçoit sa quinzaine de 78~fr.~75 (15 jours à 5~fr.~25).",
    36: r"Outre une boîte de savon anglais pour cuir de sellerie (\textit{saddle soap}) et du chocolat Poulain achetés à \textbf{Saint-Pol-sur-Ternoise}, l'acquisition d'une \textbf{carte du département de la Somme} (70~c.) et d'une géographie du Pas-de-Calais (35~c.) annonce dès le 3 septembre la marche prochaine de la 18\textsuperscript{e} Division du Ternois vers le front de la Somme.",
    38: r"Les deux fourgons (\textit{waggons}) venus charger le fourrage vert derrière la ferme Collet appartiennent au \textbf{\textit{Bedfordshire Regiment}} (\textit{Bedfords}), dont le 7\textsuperscript{e} Bataillon (\textit{Service}) fait partie de la 54\textsuperscript{e} Brigade de la \textbf{18\textsuperscript{e} Division britannique} (Nichols, 1922, p.~86).",
    40: r"Le hameau d'\textbf{Oppy} où cantonne la compagnie le 9 septembre 1916 est l'écart d'Oppy rattaché à la commune de \textbf{Beaudricourt} (Pas-de-Calais, canton d'Avesnes-le-Comte, à l'ouest d'Arras), où Hippolyte Combes se rend à pied le 10 septembre auprès du maire pour le service de cantonnement.",
    41: r"Longue étape à cheval conduisant la colonne du Pas-de-Calais dans la Somme par \textbf{Lucheux}, \textbf{Thièvres} et \textbf{Raincheval}. À \textbf{Lucheux} (Somme), Hippolyte Combes remarque les ruines du château fort des comtes de Saint-Pol (XII\textsuperscript{e}–XIV\textsuperscript{e}~s. ; Base Mérimée, \texttt{PA00116194}) et le beffroi abritant le chêne historique sous lequel la tradition locale situe la signature par \textbf{Louis~XI} de l'édit du 19 juin 1464 instituant la poste royale.",
    43: r"Après une première visite le 14 septembre au bureau de la Mission française de la 18\textsuperscript{e} Division dans le parc du château d'\textbf{Acheux-en-Amiénois}, Hippolyte Combes observe le 15 septembre près de Raincheval des exercices de grenades et de mortiers de tranchée et acquiert à la cantine britannique l'ouvrage de \textbf{Sir Max Aitken} (Lord Beaverbrook), \textit{Canada in Flanders: The Official Story of the Canadian Expeditionary Force} (Londres, Hodder \& Stoughton, 1916).",
    47: r"Informé des horaires de train à la gare de Raincheval en vue de sa permission du 25 septembre, Hippolyte Combes assiste à un match de football près des lignes de chevaux du \textbf{7\textsuperscript{e} Bataillon du \textit{Bedfordshire Regiment}} (\textit{Bedfords}, 54\textsuperscript{e} Brigade de la 18\textsuperscript{e} Division), avant d'apprendre par le \textbf{capitaine Panton} (\textit{152nd Company A.S.C.}) le départ de l'unité pour le lendemain.",
    48: r"Le samedi 23 septembre 1916 — à trois jours de l'attaque de la 18\textsuperscript{e} Division contre Thiepval —, la compagnie quitte Raincheval sous les ordres du \textbf{capitaine West} ; à hauteur de \textbf{Léalvillers}, le lieutenant interprète divisionnaire \textbf{Pizzi} apporte en automobile un contre-ordre qui dirige l'unité par la gare d'Acheux vers les coteaux de \textbf{Forceville}, où elle bivouaque en plein champ (\textit{in the open}).",
    49: r"Au bivouac de \textbf{Forceville} le dimanche 24 septembre 1916, le grondement continu du canon entendu dans la nuit (l.~21) correspond au bombardement préparatoire franco-britannique précédant les offensives de \textbf{Morval--Combles} (25 septembre) et de la crête de \textbf{Thiepval} (26 septembre 1916, où s'engage la 18\textsuperscript{e} Division).",
    50: r"Départ d'Hippolyte Combes pour sa première permission le lundi 25 septembre 1916 : après une corvée matinale de fourrage vert à Forceville avec le \textbf{lieutenant Ford}, il gagne à midi en fourgon la tête de ligne ferroviaire (\textit{railhead}) d'\textbf{Acheux-Varennes}, confie ses bagages au bureau du \textit{Railway Transport Officer} (\textit{R.T.O.}) et prend à 18~h~40 le train départemental à voie métrique vers Gézaincourt.",
    53: r"À la librairie Armand Colin (boulevard Saint-Michel), Hippolyte Combes acquiert deux ouvrages contemporains : l'essai d'\textbf{Ernest Zyromski} (1862–1933, professeur de littérature française à la Faculté des lettres de Toulouse), \textbf{\textit{L'Orgueil humain}} (Armand Colin, 1904), et le recueil d'essais de guerre de \textbf{Maurice Maeterlinck}, \textbf{\textit{Les Débris de la guerre}} (Fasquelle, Bibliothèque-Charpentier, 1916).",
    54: r"Arrivé à \textbf{Toulouse} pour sa première permission, Hippolyte Combes retrouve sa fiancée \textbf{Marguerite Calmels} (1892–1974) chez l'oncle et la tante de celle-ci, \textbf{Émile Crouzet} (1842–1921, agent de change à Toulouse) et \textbf{Élisabeth Calmels}, et revoit le pensionnat jésuite de \textbf{Sainte-Marie-des-Champs} (Le Caousou) où il avait accompli ses études secondaires.",
    55: r"Après avoir offert à Marguerite Calmels un bouquet acheté place Esquirol, Hippolyte Combes effectue avec elle, \textbf{Élisabeth Calmels-Crouzet} et \textbf{Émile Crouzet} (\textit{M.~Czt}) une promenade sur les coteaux dominant la Garonne au sud de Toulouse, par l'église de \textbf{Pouvourville} et la crête de \textbf{Pech-David}.",
    56: r"Journée de fiançailles à \textbf{Toulouse} le vendredi 29 septembre 1916 : Hippolyte Combes offre à \textbf{Marguerite Calmels} — qu'il appelle déjà dans l'intimité du carnet \textit{ma Femme}, un an avant leur mariage célébré à Millau le 25 octobre 1917 — un sautoir en or acquis 295~francs.",
    57: r"Promenade toulousaine avec Marguerite Calmels le long des allées et du \textbf{canal du Midi} jusqu'au faubourg Saint-Étienne, rythmée par la sonnerie des cinq cloches de la cathédrale \textbf{Saint-Étienne de Toulouse}.",
    58: r"Dimanche 1\textsuperscript{er} octobre 1916 à \textbf{Toulouse} : après la messe matinale à la cathédrale \textbf{Saint-Étienne}, Hippolyte Combes range sa bibliothèque personnelle dans son appartement toulousain avant une promenade vespérale au Grand-Rond avec Marguerite Calmels.",
    59: r"Le lundi 2 octobre 1916, \textbf{Marguerite Calmels} et sa mère \textbf{Mme Valentine Calmels} visitent l'appartement toulousain d'Hippolyte Combes, puis tous trois se recueillent à la chapelle \textbf{Notre-Dame-de-Nazareth} (rue Pharaon, quartier des Carmes, sanctuaire familial des Combes à Toulouse) avant de remonter à la Côte Pavée, d'où Hippolyte Combes repart à 21~h~30 avec l'abbé \textbf{Jean Crouzet}.",
    63: r"En escale à Paris le jeudi 5 octobre 1916 entre la gare d'Orsay et la gare du Nord, Hippolyte Combes visite l'église basilicale \textbf{Saint-Vincent-de-Paul} (X\textsuperscript{e}~arr., bâtie par Jacques-Ignace Hittorff de 1824 à 1844 ; Base Mérimée, \texttt{PA00086489}), célèbre pour ses deux ordres superposés de colonnes ioniques et corinthiennes en stuc marbré brun et la grande frise peinte par \textbf{Hippolyte Flandrin} (1849–1853), puis écrit au salon de correspondance des \textbf{Grands Magasins du Louvre}.",
    64: r"Pendant le trajet nocturne du 4 au 5 octobre 1916 de Toulouse-Matabiau à Paris-Orsay (billet militaire de 3\textsuperscript{e} classe à 11~fr.~75), Hippolyte Combes récapitule ses dernières dépenses toulousaines, dont deux images pieuses de sainte Thérèse (40~c.), un bouquet pour Marguerite Calmels (1~fr.~70) et 5~fr. d'étrennes à \textbf{Maria}, domestique de la famille Crouzet à Sainte-Marie.",
    66: r"Première mention explicite dans le carnet du numéro de l'unité britannique d'Hippolyte Combes : la \textbf{152\textsuperscript{e} Compagnie de l'\textit{Army Service Corps}} (\textit{152nd Company A.S.C.}), rattachée au \textit{18th Divisional Train} et chargée du ravitaillement de la \textbf{54\textsuperscript{e} Brigade d'infanterie} de la 18\textsuperscript{e} Division, qui vient de livrer la bataille de la crête de Thiepval (26–30 septembre 1916) et a établi sa tête de ligne ferroviaire (\textit{railhead}) à \textbf{Canaples} (Somme).",
    67: r"Tandis que les brigades de la 18\textsuperscript{e} Division sont relevées après la prise de Thiepval, la \textbf{152\textsuperscript{e} Compagnie A.S.C.} cantonne au repos du 6 au 15 octobre 1916 au hameau boisé de \textbf{Barlette} (commune de \textbf{Ribeaucourt}, Somme) ; Hippolyte Combes fait viser son titre de permission à la Mission française de \textbf{Bernaville} et remet un cadeau de 5~fr. au maréchal des logis-chef fourrier (\textit{Quartermaster Sergeant}) \textbf{Tait}.",
    68: r"Installé dans l'ancien salon d'une maison entourée de vergers de pommiers et de grands bois à \textbf{Barlette} (Ribeaucourt), Hippolyte Combes règle au \textbf{capitaine Panton} (officier de la \textit{152nd Company A.S.C.}, gérant de la popote des officiers) sa quote-part des frais de \textit{mess} du mois de septembre (29~fr., soit environ 2~fr.~20 par jour depuis son admission permanente au mess le 12 septembre).",
    73: r"Après avoir conduit le 12 octobre un avant-train articulé (\textit{limber}) et des fourgons réglementaires à quatre roues de l'A.S.C. (\textit{General Service wagons}) aux champs de luzerne de Ribeaucourt, Hippolyte Combes chevauche le vendredi 13 octobre avec le \textbf{capitaine Panton} jusqu'à \textbf{Prouville} (Somme) et apprend au dîner le départ prochain du train divisionnaire vers le front de l'Ancre.",
    78: r"Le mercredi 18 octobre 1916, profitant d'un camion de munitions depuis le bivouac de Bouzincourt, Hippolyte Combes découvre \textbf{Albert} (Somme) et s'arrête devant les ruines de la basilique de pèlerinage \textbf{Notre-Dame de Brebières} (édifice néo-byzantin de brique et de pierre élevé de 1885 à 1895 par l'architecte amiénois \textbf{Edmond Duthoit}, 1837–1889 ; Base Mérimée, \texttt{PA00116039}).",
    79: r"Sur la chaussée de Bouzincourt à \textbf{Albert} le 18 octobre 1916, Hippolyte Combes observe l'intensité du trafic logistique britannique (camions automobiles et caissons de munitions ravitaillant le II\textsuperscript{e} Corps en vue de l'attaque du 21 octobre sur la tranchée Regina) et perçoit 84~fr. de solde au bureau de la Mission française d'Albert.",
    80: r"Le jeudi 19 octobre 1916, la 152\textsuperscript{e} Compagnie A.S.C. quitte Bouzincourt pour le grand bivouac boueux du \textbf{\textit{Brickfields Area}} (secteur des briqueteries à l'entrée nord-ouest d'\textbf{Albert}), tandis qu'Hippolyte Combes parvient à se loger à 300 ou 400~mètres du camp chez la famille \textbf{Victor Duchâteau}, sous le roulement continu de la préparation d'artillerie britannique.",
    83: r"À \textbf{Albert} (Somme), Hippolyte Combes décrit la basilique \textbf{Notre-Dame de Brebières} (édifiée en briques rouges de 1885 à 1895 par l'architecte Edmond Duthoit), dont le dôme de 70~m frappé par les obus allemands en janvier 1915 retenait à l'horizontale la célèbre statue dorée de la \textbf{Vierge penchée} d'Albert Roze. L'adjudant interprète \textbf{Schumacher} lui annonce le projet ministériel de relève des jeunes interprètes de la réserve de l'armée territoriale (\textit{R.A.T.}).",
    84: r"Excursion en camion le 23 octobre 1916 jusqu'aux ruines de \textbf{La Boisselle} (Somme, à 3,5~km à l'est d'Albert sur la route de Bapaume), conquises en juillet 1916 : outre les profonds abris souterrains allemands creusés dans la craie (\textit{german dug-outs}), l'« énorme cratère sur la droite » est le célèbre cratère de mine de \textbf{Lochnagar} (\textit{Lochnagar Crater}), ouvert le \textbf{1\textsuperscript{er} juillet 1916} à 7~h~28 par l'explosion d'un fourneau britannique de 27~tonnes d'ammonal mis à feu par la \textit{179th Tunnelling Company, Royal Engineers}.",
    85: r"Au bureau de la Mission française de la 18\textsuperscript{e} Division à Albert, l'adjudant \textbf{Liepin} (ou \textit{Lupin}/\textit{Lépin}) et le lieutenant interprète chef de détachement \textbf{Pizzi} rassurent Hippolyte Combes (qui appartient à la classe 1896, âgée de quarante ans) : il n'est pas touché par le renvoi ministériel des jeunes classes de la réserve de l'armée territoriale (\textit{R.A.T.}) dans les corps de troupe.",
    87: r"La tournée en automobile du dimanche 29 octobre 1916 à \textbf{Acheux-en-Amiénois} et \textbf{Senlis-le-Sec} pour recenser les pailles et foins (\textit{straw \& hay}) disponibles préfigure le détachement permanent d'Hippolyte Combes et du lieutenant Curtis à Acheux quatre jours plus tard. Chez son logeur d'Albert, \textbf{Victor Duchâteau}, il écoute les récits de guerre du fils aîné de la maison, maréchal des logis d'artillerie dans l'armée belge.",
    89: r"Le mercredi \textbf{1\textsuperscript{er} novembre 1916} (Toussaint), Hippolyte Combes décrit le cimetière civil d'Albert ravagé par les obus et le carré militaire britannique contigu (\textit{Albert Communal Cemetery Extension}, ouvert en août 1915 ; notice CWGC), assiste à 15~h sur la place d'Albert à une remise de décorations aux combattants de la Somme, et apprend à 21~h par le lieutenant \textbf{Curtis} leur détachement au service des fourrages à \textbf{Acheux-en-Amiénois}.",
    90: r"Le commandant du Train divisionnaire (\textit{18th Divisional Train Office}) qui signe l'ordre détachant Hippolyte Combes au service du fourrage à Acheux-en-Amiénois est le \textbf{lieutenant-colonel Daniel Charles Evans Grose}, A.S.C. (\texttt{Col. Grose}), commandant le \textit{18th Divisional Train} de 1915 à 1918 et décoré du \textit{Distinguished Service Order} (\textit{London Gazette}, 4 juin 1917, p.~5470 ; Nichols, 1922, p.~110).",
    91: r"Dès son arrivée à \textbf{Acheux-en-Amiénois} le 2 novembre 1916, Hippolyte Combes est présenté à Raincheval au \textbf{major Levy} (officier supérieur britannique dirigeant le service des achats et réquisitions d'armée). Le 3 novembre, il revient faire ses adieux au camp de la \textbf{152\textsuperscript{e} Compagnie A.S.C.} et perçoit à Albert le reliquat de sa solde.",
    92: r"Le samedi 4 novembre 1916, une course pour l'approvisionnement en pétrole (nécessaire aux moteurs des batteuses mécaniques) conduit Hippolyte Combes à \textbf{Bertrancourt} (Somme), au quartier général de la \textbf{2\textsuperscript{e} Division britannique} (\textit{2nd Division}, V\textsuperscript{e} Corps, engagée le 13 novembre à Beaumont-Hamel), où il retrouve son collègue interprète d'artillerie de campagne (\textit{R.F.A.}) \textbf{Cordonnier}, connu lors d'un précédent séjour à \textbf{Béthune}.",
    93: r"À son arrivée à \textbf{Acheux-en-Amiénois} le 2 novembre 1916, Hippolyte Combes est présenté à Raincheval au \textbf{major Levy}, directeur du service des achats et réquisitions d'armée (\textit{Army Purchase Board}), et règle le 3 novembre ses adieux au camp de la \textbf{152\textsuperscript{e} Compagnie A.S.C.} ainsi que sa solde à Albert après la retenue réglementaire de six jours de permission.",
    94: r"Le dimanche 5 novembre 1916, Hippolyte Combes emménage au \textbf{n\textsuperscript{o}~1 de la route de Léalvillers} à \textbf{Acheux-en-Amiénois}, chez le maître tailleur \textbf{M.~Carluvant}, puis se présente à 18~h au \textbf{capitaine Huguet}, chef de la Mission militaire française auprès du \textbf{XIII\textsuperscript{e} Corps britannique} dans le secteur de la \textbf{V\textsuperscript{e} Armée britannique} (\textit{Fifth Army}, nouveau nom donné le 30 octobre 1916 à la \textit{Reserve Army} du général Sir Hubert Gough).",
    95: r"Première mention le 6 novembre 1916 de la \textbf{ferme de Belle-Église}, grand domaine agricole isolé de la commune d'\textbf{Arquèves} (Somme, ancienne commanderie templière puis hospitalière), exploitée par la famille belge \textbf{Houthouan}, où fonctionnent les batteuses à pétrole du service des fourrages ; le 7 novembre, Hippolyte Combes observe depuis Acheux le flot continu des troupes et convois de munitions montant vers la ligne de feu (\textit{firing line}).",
    96: r"Après une tournée à Forceville le 8 novembre avec le \textbf{major Hughes} (du \textit{18th Divisional Train}) et le lieutenant Curtis, Hippolyte Combes profite de ses courses des 8 et 9 novembre vers Varennes et \textbf{Albert} pour prendre le thé à la baraque-mess (\textit{mess-hut}) de son ancienne unité, la \textbf{152\textsuperscript{e} Compagnie A.S.C.}, tandis que le retour du temps clair sous la pleine lune du 9 novembre s'accompagne d'un bombardement sur Albert.",
    97: r"Le samedi 11 novembre 1916, en allant régler un achat de paille auprès de la \textit{B~Battery} d'une brigade de la \textit{Royal Field Artillery} (\textit{R.F.A.}) à \textbf{Varennes-en-Croix}, Hippolyte Combes rencontre son collègue interprète \textbf{M.~Sorgues}, professeur au lycée de Toulon (ville où Hippolyte Combes avait été incorporé au 10\textsuperscript{e}~R.A.P. en mars 1915) ; le soir, l'artillerie allemande à longue portée contre-bat le carrefour et la gare d'\textbf{Acheux}.",
    98: r"Témoignage direct sur le déclenchement de la \textbf{bataille de l'Ancre} (\textit{Battle of the Ancre}, 13–18 novembre 1916) : le lundi \textbf{13 novembre 1916} à 5~h~45 et le mardi \textbf{14 novembre}, le \textbf{V\textsuperscript{e} Corps britannique} (51\textsuperscript{e} \textit{Highland Division} et 63\textsuperscript{e} \textit{Royal Naval Division}) prend d'assaut \textbf{Beaumont-Hamel} et \textbf{Beaucourt-sur-l'Ancre}, tandis que les ambulances traversent Acheux et que les tournées de fourrage mènent Hippolyte Combes à la foire de \textbf{Doullens} et à \textbf{Frévent} (église Saint-Hilaire).",
    99: r"Les 15 et 16 novembre 1916, la canonnade qui ébranle les vitres d'Acheux répond aux combats de la \textbf{bataille de l'Ancre} devant \textbf{Beaumont-Hamel} et \textbf{Beaucourt-sur-l'Ancre} (condensés par Hippolyte Combes sous l'appellation \textit{Beaumont s/ Ancre}). Le 16 novembre, en tournée par Raincheval, Louvencourt et Toutencourt, il déjeune à \textbf{Hérissart} chez le \textbf{lieutenant Walsh} avec l'interprète \textbf{M.~Deloney}, industriel du textile de la région parisienne.",
    102: r"Retenu le 22 novembre 1916 par une crise d'entérite, Hippolyte Combes mentionne pour la première fois par son nom et sa profession son logeur du n\textsuperscript{o}~1 route de Léalvillers à Acheux, le maître tailleur \textbf{M.~Carluvant} (qui retouche sa culotte militaire pour 75~c. et chez qui il logera jusqu'au 7 février 1917).",
    103: r"Le samedi 25 novembre 1916 au matin, un tir d'artillerie allemande à longue portée de plus de vingt-cinq obus frappe \textbf{Acheux-en-Amiénois} aux abords de la râperie/sucrerie et de la ferme Royer, faisant plusieurs tués et blessés ; le lendemain dimanche 26 novembre, Hippolyte Combes reçoit pour le thé le \textbf{lieutenant Walsh} et son interprète \textbf{M.~Deloney}, qu'il raccompagne à pied sur la route d'Hérissart.",
    104: r"Le mardi 28 novembre 1916, une tournée conduit Hippolyte Combes au château de \textbf{Martinsart} (Somme, à 3,5~km au nord d'Albert, en arrière immédiat des batteries lourdes britanniques tirant vers l'Ancre), dont les propriétaires âgés seront peu après évacués à Franvillers ; les 29 et 30 novembre, les courses de fourrage s'étendent vers le sud-ouest jusqu'à \textbf{Rubempré}, \textbf{Septenville} et \textbf{Pierregot}.",
    105: r"En se rendant à \textbf{Franvillers} et \textbf{Buire-sur-l'Ancre} le 1\textsuperscript{er} décembre 1916, Hippolyte Combes revoit la vallée de \textbf{Ribemont-sur-Ancre} et \textbf{Heilly}, où il avait cantonné avec la 18\textsuperscript{e} Division durant l'hiver 1915–1916. Le samedi 2 décembre survient à Acheux l'arrivée du jeune \textbf{capitaine Williams} (\textit{Foraging Officer}), appelé à remplacer le lieutenant Curtis.",
    106: r"Le dimanche 3 décembre 1916, après un déjeuner à Hérissart chez le \textbf{lieutenant Walsh}, une longue tournée automobile entraîne Hippolyte Combes au sud de la Somme par \textbf{Corbie} et \textbf{Villers-Bretonneux} jusqu'à \textbf{Marcelcave} et \textbf{Warfusée-Abancourt} (commune de Lamotte-Warfusée, sur l'axe Amiens–Péronne), avant le paiement de sa quinzaine (78~fr.~75) à la Mission du XIII\textsuperscript{e} Corps à Acheux et les premières courses avec le \textbf{capitaine Williams} à Belle-Église et Louvencourt.",
    107: r"Après l'inspection le 5 décembre 1916 des villages dévastés de \textbf{Bayencourt} et \textbf{Coigneux} (en arrière immédiat des tranchées d'\textbf{Hébuterne} et du saillant de \textbf{Gommecourt}), le \textbf{lieutenant Curtis} quitte définitivement Acheux le 6 décembre pour réintégrer la \textbf{152\textsuperscript{e} Compagnie A.S.C.}, salué par Hippolyte Combes d'une épithète cinglante (\textit{A brainless ass}), tandis que le jeune \textbf{capitaine Williams} lui confie avoir débuté avant la guerre comme petit employé de bureau (\textit{office boy}) à 50~livres par an.",
    108: r"Les 7 et 8 décembre 1916, Hippolyte Combes supervise la mise en route du battage mécanique de la paille à la ferme de \textbf{Belle-Église} (commune d'\textbf{Arquèves}), exploitée par une famille d'agriculteurs belges, \textbf{M. et Mme Houthouan}, et gagne par Hédauville le village d'\textbf{Englebelmer} (Somme, à 4~km des lignes de Beaumont-Hamel), entièrement évacué de sa population civile et occupé par l'artillerie britannique.",
    109: r"Le samedi 9 décembre 1916, au cours d'une longue tournée jusqu'en Artois (\textbf{Orville}, \textbf{Saulty} et \textbf{L'Arbret}, Pas-de-Calais, sur la route de Doullens à Arras), Hippolyte Combes déjeune à \textbf{Authie} au mess de la 3\textsuperscript{e} Compagnie du Train divisionnaire de la \textbf{31\textsuperscript{e} Division britannique} (\textit{No.~3 Company, 31st Divisional Train, A.S.C.}, c'est-à-dire la \textit{280th Company A.S.C.}, rattachée au XIII\textsuperscript{e} Corps devant Serre–Hébuterne) avec le \textbf{lieutenant Croughton}.",
    110: r"Le mercredi 13 décembre 1916 au matin, Hippolyte Combes assiste le \textbf{major Levy} (chef du service d'achats et réquisitions du secteur) lors d'une réunion officielle organisée à la mairie de \textbf{Toutencourt} avec les habitants évacués du village d'\textbf{Englebelmer} pour le règlement des récoltes et fourrages laissés dans leurs exploitations.",
    111: r"Les tournées des 17 et 18 décembre 1916 sur les routes défoncées relient les centres de battage d'\textbf{Arquèves} (\textbf{Belle-Église}), \textbf{Raincheval}, \textbf{Toutencourt} et la \textbf{ferme du Quesnoy} (écart agricole près de Raincheval et Puchevillers), tandis que s'accuse la mésentente morale entre l'universitaire de quarante ans et le jeune \textbf{capitaine Williams} (« un capitaine de 20 ans, présomptueux et vain »).",
    112: r"Ce feuillet des 22 et 24 décembre 1916 marque une double crise à la veille de Noël : sur le plan intime, une lettre de \textbf{Marguerite Calmels} datée du 17 décembre provoque chez Hippolyte Combes de vives appréhensions ; sur le plan militaire, lors d'une visite de service le 24 décembre chez l'exploitante \textbf{Mme Cuisinier} à \textbf{Louvencourt}, l'exclamation francophobe du \textbf{capitaine Williams} (\textit{« Bloody France etc.! »}) indigne l'interprète, qui hésite à adresser un rapport officiel à la Mission française.",
    113: r"À \textbf{Raincheval}, Hippolyte Combes attend devant le bureau de la commission d'achats de l'armée (\textbf{\textit{Army Purchase Board}}) et perçoit sa solde bimensuelle (84~francs) au bureau de la Mission française du \textbf{XIII\textsuperscript{e} Corps britannique}.",
    115: r"Reprise des tournées dès le lendemain de Noël (26 décembre 1916) : entretien avec \textbf{M.~Guibet} à Raincheval et négociation à \textbf{Beauquesne} avec \textbf{Mme Capron} pour la location d'une batteuse mécanique (\textit{machine à battre}) destinée au battage des pailles réquisitionnées par l'armée britannique.",
    116: r"Soirée de Noël prolongée à Acheux le 28 décembre 1916 au foyer de la \textit{Y.M.C.A.} par le concert de la troupe divisionnaire des \textbf{\textit{13th Corps Archie Singers}} (groupe artistique formé par les batteries de défense contre aéronefs, familièrement appelées \textit{Archies} dans l'argot militaire britannique). Le lendemain, tournée à Raincheval, Le Quesnoy et Louvencourt dans une automobile d'état-major \textit{Sunbeam}.",
    117: r"Après avoir revu le 30 décembre 1916 à \textbf{Franvillers} les propriétaires âgés évacués du château de \textbf{Martinsart}, un nouvel éclat verbal du \textbf{capitaine Williams} à \textbf{Senlis-le-Sec} devant l'ordonnance provoque au retour à Acheux une mise au point ferme d'Hippolyte Combes : redoutant une plainte officielle auprès de la Mission française, le jeune officier lui présente ses excuses et garde tout le jour de la Saint-Sylvestre (31 décembre) une attitude contrite.",
    118: r"Les 1\textsuperscript{er} et 2 janvier 1917, le service des fourrages se poursuit sans trêve du Jour de l'An : tournée le lundi par \textbf{Authie} et \textbf{Pas-en-Artois} jusqu'à \textbf{Saulty} (Pas-de-Calais, sur la route de Doullens à Arras), et expertise contradictoire le mardi 2 janvier d'une machine agricole endommagée à la \textbf{ferme Cuisinier} à \textbf{Louvencourt}, tandis que le tailleur \textbf{M.~Carluvant} évoque un congé prochain de son logement d'Acheux.",
    119: r"Le mercredi 3 janvier 1917, en route vers \textbf{Amiens}, Hippolyte Combes s'arrête à \textbf{Montigny-sur-l'Hallue} (Somme) chez le maire \textbf{Paul Dubois}. À Amiens, après avoir garé l'automobile à l'\textbf{Hôtel de la Paix} (15, rue des Cordeliers), il rencontre le \textbf{capitaine Trefcon} rue \textbf{Sire-Firmin-Leroux} (au siège de la société de machines agricoles \textit{La Semeuse}), puis visite la cathédrale \textbf{Notre-Dame d'Amiens} dont il achète cinq gravures.",
    120: r"Après un second concert des \textbf{\textit{13th Corps Archie Singers}} au foyer de la Y.M.C.A. d'Acheux le 4 janvier 1917, la journée du vendredi 5 janvier mène Hippolyte Combes à la ferme Moulard à \textbf{Septenville} (Rubempré) puis à \textbf{Beauquesne}, où il déjeune au Café Continental avec le \textbf{lieutenant Walsh} et le \textbf{lieutenant Morris}, conclut avec \textbf{Mme Capron} le contrat de location de sa batteuse, et perçoit à Acheux sa quinzaine de 78~fr.~75 au bureau du XIII\textsuperscript{e} Corps.",
    121: r"Les mouvements de convois autour d'Acheux accompagnent l'extension du secteur du \textbf{V\textsuperscript{e} Corps britannique} dans la vallée de l'Ancre. À \textbf{Hédauville}, Hippolyte Combes rend visite le 9 janvier 1917 à la \textbf{150\textsuperscript{e} Compagnie de l'A.S.C.} (\textit{150th Company A.S.C.}, commandée par le major H.~G. Peachy), compagnie sœur de la 152\textsuperscript{e} Compagnie au sein du \textit{18th Divisional Train} (Maj. A.~F. Becke, \textit{Order of Battle}, Part~3A, p.~81), où sert son ami le \textbf{lieutenant Morris}.",
    122: r"La « très violente canonnade sur la ligne de Miraumont » notée le mercredi \textbf{10 janvier 1917} correspond aux opérations offensives menées sur l'Ancre les \textbf{10 et 11 janvier 1917} par le \textbf{V\textsuperscript{e} Corps britannique} (attaque de la 7\textsuperscript{e} Division sur les tranchées allemandes dominant Beaumont-Hamel et le vallon de \textbf{Miraumont} ; \textit{Official History, Military Operations France and Belgium, 1917}, vol.~I, p.~48–50) ; le même jour, Hippolyte Combes retrouve le \textbf{lieutenant Morris} à Belle-Église et expédie un mandat de 19~fr. à l'opticien parisien \textbf{Imbert}.",
    124: r"Après une tournée dans les fermes enneigées de Bouzincourt, Senlis-le-Sec et Rubempré le 16 janvier 1917, l'excursion du mercredi 17 janvier conduit Hippolyte Combes par Doullens jusqu'à \textbf{Auxi-le-Château} (Pas-de-Calais, dans la vallée de l'Authie), où son hôte \textbf{M.~Renard} le reçoit à déjeuner et lui présente sa collection d'objets d'art, dont un coffret en marqueterie de paille tressée acquis en 1858 au \textbf{bagne maritime de Toulon}.",
    125: r"Sous la vague de froid polaire de la mi-janvier 1917 en Picardie, Hippolyte Combes poursuit les tournées quotidiennes de réquisition à Belle-Église, Raincheval et Puchevillers et perçoit sa solde bimensuelle (84~francs) au bureau de la Mission française du \textbf{V\textsuperscript{e} Corps britannique}.",
    126: r"Tandis que la vague de froid exceptionnelle de fin janvier 1917 (l'un des hivers les plus rigoureux du XX\textsuperscript{e}~s. sur le front occidental) durcit la neige et couvre les vitres de givre, Hippolyte Combes se rend le dimanche 21 janvier à \textbf{Louvencourt} chez l'exploitante \textbf{Mme Cuisinier}, achète à la cantine britannique trois boîtes de graisse imperméabilisante pour brodequins (\textit{Wren's Dubbin}) et prépare son départ en permission.",
    130: r"En escale à Paris le samedi 27 janvier 1917 au matin, Hippolyte Combes se rend à \textbf{Neuilly-sur-Seine} pour rendre visite à la famille de \textbf{Mme Faure} (cousines de Marguerite Calmels).",
    131: r"Suite de la visite familiale du 27 janvier 1917 à \textbf{Neuilly-sur-Seine} chez \textbf{Mme Faure}, entourée de sa fille \textbf{Germaine} et de son fils \textbf{Marcel Faure} alors en permission, tandis que ses deux autres fils, \textbf{Henri} (aspirant d'infanterie) et \textbf{André} (candidat à l'École polytechnique), sont évoqués dans la conversation.",
    132: r"En arrivant à la gare Matabiau de \textbf{Toulouse} le dimanche 28 janvier 1917 à 8~h~15, Hippolyte Combes évoque avec émotion sa mère \textbf{Marie Anaïs Alric} (née à Millau le 20 avril 1838, décédée à Toulouse en 1907) et ses sœurs disparues (\textbf{Maria Combes}, 1875–1903, et \textbf{Joséphine Combes}, 1873–1914) qui l'attendaient autrefois à la gare, puis reçoit dans son appartement la visite de l'oncle \textbf{Émile Crouzet} (1842–1921).",
    133: r"Les retrouvailles chaleureuses du dimanche 28 janvier 1917 à Sainte-Marie dissipent entièrement le nuage épistolaire de la Noël : outre sa fiancée \textbf{Marguerite Calmels}, Hippolyte Combes retrouve \textbf{Élisabeth Crouzet née Calmels} (\textit{Tante}), la sœur aînée de Marguerite, \textbf{Madeleine Calmels-Vincens} (1882–1961, épouse du D\textsuperscript{r}~Fernand Vincens de Saint-Chély-d'Apcher), ainsi qu'à 18~h~30 leur cousin l'abbé \textbf{Jean Crouzet}.",
    134: r"À \textbf{Toulouse} le 29 janvier 1917, Hippolyte Combes retire en gare Matabiau un panier de fleurs expédié de Nice pour Marguerite Calmels, visite avec elle et sa sœur aînée \textbf{Madeleine Calmels-Vincens} la basilique romane \textbf{Saint-Sernin} et ses cryptes (voisines de l'ancien domicile familial des Combes rue du Taur), puis parcourt les grands magasins du Capitole et la \textbf{Maison Universelle} fondée par \textbf{Antoine Labit} (1832–1912, père du voyageur et collectionneur Georges Labit).",
    135: r"Journée toulousaine du 30 janvier 1917 : après une visite matinale à \textbf{Mme de Labarthe} et l'achat chez l'horloger-bijoutier \textbf{Pfister} (10, rue Gambetta, près de la place Esquirol et de la rue d'Alsace-Lorraine) d'une montre-bracelet en or (200~fr.) et de deux bagues, Hippolyte Combes assiste à 17~h avec Marguerite et Madeleine Calmels au cours public d'\textbf{Ernest Zyromski} (1862–1933) à la Faculté des lettres de Toulouse, consacré à \textbf{Maurice de Guérin} (1810–1839) et à l'influence de la Bretagne et de Lamennais (étude publiée dans \textit{Maurice de Guérin}, Armand Colin, 1921).",
    136: r"Promenade à \textbf{Toulouse} avec Marguerite Calmels le 31 janvier 1917 par le marché Victor-Hugo, la cour Renaissance de l'\textbf{Hôtel d'Assézat} (édifié à partir de 1555 sur les plans de Nicolas Bachelier), et les églises \textbf{Notre-Dame de la Daurade} et \textbf{Notre-Dame de la Dalbade} (dont le cousin Jean Crouzet deviendra curé), suivie au matin du 1\textsuperscript{er} février d'une marche vers \textbf{Lardenne} et les ruines de l'amphithéâtre gallo-romain de \textbf{Purpan-Ancely} (I\textsuperscript{er}~s. apr. J.-C.).",
    137: r"Le jeudi 1\textsuperscript{er} février 1917 à Toulouse, après avoir salué \textbf{Mme de Labarthe} et ses voisines d'appartement les \textbf{dames Delsol}, Hippolyte Combes descend en ville avec \textbf{Henriette}, se recueille à la chapelle \textbf{Notre-Dame-de-Nazareth} en mémoire de ses parents et sœurs défunts et choisit chez l'horloger-bijoutier \textbf{Pfister} une montre en or pour Marguerite Calmels, avant de noter le soir, rue de Languedoc, son détachement définitif à l'égard de Toulouse.",
    138: r"Dernière journée à Toulouse (vendredi 2 février 1917) : soins dentaires rue La Fayette chez le chirurgien-dentiste \textbf{M.~de Lersay}, visite d'adieu à \textbf{Mme de Labarthe} et à \textbf{Henriette}, et règlement chez l'horloger-bijoutier \textbf{Pfister} de la montre à remontoir en or mat de style Louis~XVI (105~fr.) destinée à être suspendue au sautoir en or offert à Marguerite Calmels lors de leurs fiançailles.",
    139: r"Voyage ferroviaire du samedi 3 février 1917 de \textbf{Toulouse} à \textbf{Millau} en compagnie de Marguerite Calmels : salut en gare de Carcassonne au cousin l'\textbf{abbé Jean Crouzet}, halte à \textbf{Béziers} avec visite de l'ancienne cathédrale gothique \textbf{Saint-Nazaire} et de sa terrasse dominant l'Orb, puis arrivée nocturne en gare de Millau où les attend \textbf{Pierre Calmels}, frère de Marguerite.",
    140: r"Relevé comptable de la journée de voyage du samedi 3 février 1917 : honoraires réduits du chirurgien-dentiste toulousain \textbf{M.~de Lersay} (25~fr. au lieu de 40~fr.), étrennes de 5~fr. à la domestique \textbf{Marie} à Toulouse, billet militaire au quart de tarif de Béziers à Millau (1~fr.~80 sur le réseau du Midi) et dîner des voyageurs au buffet de la gare de bifurcation de \textbf{Bédarieux} (Hérault, 7~fr.).",
    141: r"Première nuit d'Hippolyte Combes dans la demeure des Calmels au \textbf{10, rue Alfred-Guibert à Millau} (nuit du 3 au 4 février 1917) : le retour dans son « vallon natal » réveille le souvenir poignant de son père \textbf{François Augustin Hippolyte Combes} (avocat, 1825–1899), de sa mère \textbf{Marie Anaïs Alric} (1838–1907) et de ses sœurs défuntes \textbf{Maria} (1875–1903) et \textbf{Joséphine Combes} (1873–1914), tandis que dans la chambre voisine tousse la petite \textbf{Germaine Vincens} (fille du D\textsuperscript{r}~Fernand Vincens et de Madeleine Calmels).",
    142: r"\textbf{Thérèse Cartairade} et son époux \textbf{M\textsuperscript{e}~Charles Layrals}, notaire à Millau (parents du notaire Louis Layrals, \dag~1961, et du magistrat Jean Layrals, \dag~1947), auxquels Hippolyte Combes et Marguerite Calmels rendent visite le dimanche 4 février 1917 à 18~h~15, sont la tante et l'oncle maternels de Marguerite. \textbf{« Mimi »}, arrivée par le train de 18~h, est le surnom familial d'\textbf{Anne-Marie Calmels} (1888–1975), sœur de Marguerite et future épouse de l'avoué millavois \textbf{Joseph Delcamps}.",
    143: r"Le lundi 5 février 1917 après-midi, Hippolyte Combes et Marguerite Calmels se recueillent au \textbf{cimetière de Millau} (où repose notamment François Augustin Hippolyte Combes, mort à Millau le 11 août 1899). Après avoir remboursé 6~fr. de cadeaux pour ses neveux par alliance \textbf{Germaine et Robert Vincens} et pris congé de \textbf{Pierre Calmels} en gare de Millau, Hippolyte Combes remonte par la ligne des Causses enneigée jusqu'à \textbf{Saint-Flour} (Cantal).",
    147: r"Le mercredi 7 février 1917 après-midi, rentrant de permission à Acheux où il déjeune une dernière fois chez ses logeurs \textbf{M. et Mme Carluvant}, Hippolyte Combes apprend par la postière \textbf{Mme Delille} et par un pli laissé à la Mission française que le bureau des fourrages du \textbf{capitaine Williams} est transféré à \textbf{Hérissart} (Somme), où le \textit{Town Major} lui attribue le logement (\textit{billet}) \textbf{n\textsuperscript{o}~7b} au premier étage du \textbf{café Charlet}, face à l'église Saint-Martin.",
    148: r"Fin des comptes du mercredi 7 février 1917 et journée d'installation du jeudi 8 février à \textbf{Hérissart}, où le bureau et le \textit{mess} du service des fourrages occupent le billet \textbf{n\textsuperscript{o}~104} ; avant de quitter Acheux, Hippolyte Combes y a perçu sa quinzaine de 78~fr.~75 à la Mission française et laissé 5~fr. de gratification chez ses hôtes \textbf{M. et Mme Carluvant}.",
    150: r"Conduit le 9 février 1917 par le \textbf{lieutenant Croughton} au bureau de la Mission militaire française de la \textbf{V\textsuperscript{e} Armée britannique} (\textit{Fifth Army}) à \textbf{Toutencourt}, Hippolyte Combes apprend qu'il relève désormais administrativement de la Mission d'armée, avec paiement de la solde à dates fixes les \textbf{3 et 18 de chaque mois}. Le lendemain, après un passage aux lignes du parc automobile (\textit{Motor Transport}, \textit{M.T. A.S.C.}), il se rend en tournée au château de \textbf{Martinsart}.",
    151: r"Sur la route d'\textbf{Aveluy} (au nord d'Albert) le samedi 10 février 1917, Hippolyte Combes rend visite à son ancienne compagnie (\textbf{\textit{152nd Company A.S.C.}} du \textit{18th Divisional Train}), campée à proximité des pièces britanniques de marine à longue portée (\textit{naval guns}) camouflées sous des branchages : après avoir déjeuné avec le \textbf{lieutenant Bradfield} et salué au point de ravitaillement le \textbf{capitaine Lovet}, il s'arrête à \textbf{Senlis-le-Sec}, au bureau de la Mission française du \textbf{II\textsuperscript{e} Corps britannique} dirigé par le \textbf{capitaine de Casteljau}.",
    152: r"Longue tournée dominicale du 11 février 1917 par \textbf{Toutencourt} et \textbf{Doullens} jusqu'à \textbf{Auxi-le-Château} (Pas-de-Calais, dans la vallée de l'Authie), où Hippolyte Combes est reçu par un propriétaire terrien aisé, \textbf{M.~Romert}, qui lui sert un rhum millésimé de 1870 et du kirsch de la Forêt-Noire.",
    155: r"Après une visite officielle en grande tenue au maire d'\textbf{Hérissart} le 15 février 1917, Hippolyte Combes parcourt le lendemain les fermes et le château de \textbf{Beaucourt-sur-l'Hallue} (Somme, canton de Villers-Bocage, à 7~km au sud d'Hérissart) pour l'achat de paille et de foin.",
    156: r"Le dimanche 18 février 1917, Hippolyte Combes se rend au bureau de la Mission française de la \textbf{V\textsuperscript{e} Armée britannique} (\textit{Fifth Army}) à \textbf{Toutencourt}, où il perçoit 68~fr.~25 de solde (13 jours à 5~fr.~25), s'informe de l'existence éventuelle d'un détachement ou cantonnement britannique à \textbf{Toulouse} et assiste au prône dominical à l'église \textbf{Saint-Léger de Toutencourt}.",
    157: r"Après une tournée dans la vallée de l'Hallue (\textbf{Fréchencourt} et \textbf{Bavelincourt}) le lundi 19 février 1917, le \textbf{capitaine Leonard} notifie une réorganisation des cantonnements qui oblige Hippolyte Combes à quitter sa chambre du n\textsuperscript{o}~7b (en réglant 2~fr. à la domestique \textbf{Albertine}) pour la pièce humide et glaciale du \textbf{n\textsuperscript{o}~104} attenante au bureau ; le soir même, la propriétaire du n\textsuperscript{o}~104 étant tombée malade, il va quérir le curé d'Hérissart et le médecin militaire britannique (\textit{Medical Officer}, \textit{M.O.}).",
    158: r"Lors de sa halte du 21 février 1917 à \textbf{Doullens} au retour d'\textbf{Auxi-le-Château}, Hippolyte Combes expédie un mandat-poste de 42~francs à \textbf{Mme Spagnol} à \textbf{Nice} en règlement du panier de fleurs reçu en gare de Toulouse le 29 janvier pour Marguerite Calmels.",
    159: r"Fin février 1917 autour d'\textbf{Hérissart} : après des promenades vers le moulin de la route de \textbf{Contay} et le village de \textbf{Mirvaux}, le capitaine Williams se rend seul le lundi 26 février dans le secteur avancé de \textbf{Senlis-le-Sec} et \textbf{Martinsart} (où les troupes britanniques suivent les premiers décrochages allemands dans la vallée de l'Ancre, 24–26 février 1917), laissant à Hippolyte Combes une journée de lecture et de correspondance.",
    160: r"Les régiments de \textbf{cavalerie indienne} traversant \textbf{Hérissart} le 28 février 1917 appartiennent aux \textbf{4\textsuperscript{e} et 5\textsuperscript{e} Divisions de cavalerie} (anciennes \textit{1st} et \textit{2nd Indian Cavalry Divisions} renommées en novembre 1916 au sein du \textit{Cavalry Corps} de la B.E.F. ; Maj. A.~F. Becke, \textit{Order of Battle}, Part~2A, p.~35–48).",
    161: r"Les jeudi 1\textsuperscript{er} et vendredi 2 mars 1917, les tournées d'achats mènent Hippolyte Combes au château de \textbf{Rubempré} puis dans la vallée de l'Hallue à \textbf{Fréchencourt} et \textbf{Montigny-sur-l'Hallue} (direction de \textbf{Pont-Noyelles}), où il s'entretient longuement avec le fils du maire \textbf{Paul Dubois} puis le lendemain avec le \textbf{docteur Dubois}.",
    162: r"Le samedi 3 mars 1917, au bureau de la Mission de la V\textsuperscript{e} Armée à \textbf{Toutencourt}, Hippolyte Combes perçoit 43~fr.~75 net (quinzaine normale de 78~fr.~75 diminuée d'une retenue réglementaire de 35~fr., à raison de 5~fr. par jour, pour ses sept jours de permission de fin janvier–février) ; le lundi 5 mars, il apprend avec soulagement la relève prochaine du capitaine Williams par un officier australien de l'\textbf{\textit{I~Anzac Corps}}.",
    163: r"À l'arrivée de l'officier australien et de son interprète \textbf{Valet} (de la \textit{2nd Australian Division}) venus relever le poste d'Hérissart le mardi 6 mars 1917, Hippolyte Combes accompagne une dernière fois le capitaine Williams à \textbf{Doullens} (où il verse 50~c. à une quête pour les blessés d'un hôpital auxiliaire), puis se présente à 18~h au bureau de la Mission française de la V\textsuperscript{e} Armée à \textbf{Toutencourt}, auprès du \textbf{maréchal des logis Grauger} et du chef de mission, le \textbf{capitaine Raucoule}.",
    164: r"L'interprète \textbf{Valet}, rencontré le 8 mars 1917 à Hérissart, est rattaché à la \textbf{2\textsuperscript{e} Division australienne} (\textit{2nd Australian Division}, unité de l'\textit{I~Anzac Corps} alors engagée devant Bapaume). Le 9 mars au soir, Hippolyte Combes solde ses comptes de \textit{mess} avec le \textbf{capitaine Williams} à la veille du départ de ce dernier.",
    166: r"Le dimanche 11 mars 1917, au bureau de la Mission française de la V\textsuperscript{e} Armée à \textbf{Toutencourt}, Hippolyte Combes apprend que, sur la demande expresse du \textbf{major Levy}, il est maintenu à la commission d'achats de l'armée (\textbf{\textit{Army Purchase Board}}) à \textbf{Hérissart}, où il s'installe dans le logement (\textit{billet} n\textsuperscript{o}~220) laissé libre par l'interprète Valet.",
    167: r"Lors de la reprise des tournées de l'\textit{Army Purchase Board} le lundi 12 mars 1917 (Toutencourt, Contay, Molliens-au-Bois, Puchevillers, Raincheval et \textbf{Candas}), la comparaison entre les deux automobiles militaires — l'ancienne \textbf{Vauxhall} d'état-major conduite par le chauffeur britannique \textbf{Jimmie} et la \textbf{Wolseley} conduite par un soldat australien — reflète le passage partiel des services de transport du secteur aux unités de l'\textbf{\textit{I~Anzac Corps}}.",
    168: r"Au \textbf{Mesnil-Martinsart} (Somme), Hippolyte Combes rend visite le 13 mars 1917 à son collègue de l'Instruction publique \textbf{Fortuné Flutre}, instituteur de la commune (auteur en 1899 d'une notice historique sur Le Mesnil-Martinsart), et à son épouse, parents du romaniste \textbf{Louis-Fernand Flutre} (1892–1978), admis à l'\textbf{École normale supérieure} en 1914 (entré en 1919 après la guerre, agrégé de grammaire en 1921, professeur à la Faculté des lettres de Lyon et auteur en 1955 de deux monographies historiques et linguistiques sur Le Mesnil-Martinsart ; R.~Debrie, \textit{Revue de linguistique romane}, 42, 1978, p.~238–240).",
    169: r"Après avoir revu \textbf{Albert} (où cantonnent les troupes australiennes de l'\textit{I~Anzac Corps}) et \textbf{Ribemont-sur-Ancre} le 16 mars 1917, Hippolyte Combes marche le samedi \textbf{17 mars 1917} jusqu'à Puchevillers avec son nouvel officier, le \textbf{lieutenant Wentworth}, tandis que des colonnes de \textbf{cavalerie indienne et britannique} (4\textsuperscript{e} et 5\textsuperscript{e} Divisions de cavalerie) traversent Hérissart au trot pour suivre le repli stratégique allemand sur la ligne Hindenburg (opération \textit{Alberich}, prise de Bapaume le 17 mars).",
    170: r"Dans la nuit du 19 au 20 mars 1917, Hippolyte Combes cède le lit de sa chambre d'Hérissart à un jeune lieutenant britannique de la \textbf{63\textsuperscript{e} Division (\textit{63rd Royal Naval Division})}, dont le bataillon vient d'être relevé des tranchées boueuses de \textbf{Miraumont} et d'\textbf{Achiet-le-Petit} au début du repli stratégique allemand sur la ligne Hindenburg (opération \textit{Alberich}).",
    171: r"En mars 1917, lors de la marche en avant suivant le repli allemand sur la ligne Hindenburg, le \textbf{17\textsuperscript{e} Lanciers britannique} (\textit{17th Duke of Cambridge's Own Lancers}, surnommé \textit{Death or Glory Boys} d'après la devise de son insigne à tête de mort) formait l'unique régiment britannique de la \textit{Sialkot Cavalry Brigade} au sein de la \textbf{4\textsuperscript{e} Division de cavalerie} (ex-\textit{1st Indian Cavalry Division}), aux côtés des lanciers indiens des \textit{6th King Edward's Own Cavalry} et \textit{19th Lancers (Fane's Horse)} (Maj. A.~F. Becke, \textit{Order of Battle}, Part~2A, p.~35–40).",
    172: r"Trois journées de fin mars 1917 (23–25 mars) à \textbf{Hérissart} : l'automobile du service étant en réparation aux ateliers (\textit{workshops}), Hippolyte Combes obtient de conserver sa chambre d'étude du \textbf{billet n\textsuperscript{o}~220} et effectue à pied ses courses vers \textbf{Rubempré} et \textbf{Puchevillers}.",
    173: r"Après le passage à Hérissart de son camarade interprète \textbf{Monin} le lundi 26 mars 1917, toutes les unités cantonnées quittent le village dès l'aube du mardi \textbf{27 mars 1917} : à la suite du repli allemand sur la ligne Hindenburg et de la concentration des armées britanniques plus au nord pour l'offensive d'Arras, les villages de l'ancien arrière-front de l'Ancre (Hérissart, Acheux, Contay, Warloy, Toutencourt) se vident durablement de leurs troupes.",
    175: r"Le dimanche des Rameaux (\textbf{1\textsuperscript{er} avril 1917}) et les 2–3 avril sont marqués par de fortes chutes de neige tardives sur les plateaux de la Somme ; après avoir arrêté le 1\textsuperscript{er} avril sa quote-part des frais de \textit{mess} de mars à 27~fr.~50, Hippolyte Combes se rend le mardi 3 avril à \textbf{Toutencourt} à l'étude de \textbf{M\textsuperscript{e}~Bienaimé}, notaire de Toutencourt.",
    178: r"Le dimanche de \textbf{Pâques 8 avril 1917}, après une visite matinale au notaire \textbf{M\textsuperscript{e}~Bienaimé} à Toutencourt et une tournée à Harponville, Rubempré et Beauquesne, Hippolyte Combes passe pour la première fois la soirée à Hérissart chez la \textbf{famille Denis} (\textbf{Baptiste Denis} et les siens), dont le foyer amical deviendra son refuge régulier jusqu'à la fin d'avril.",
    179: r"Après la tempête de neige du 11 avril 1917 (jour de la première attaque anglo-australienne devant Bullecourt) et ses achats à \textbf{Doullens}, Hippolyte Combes noue le vendredi 13 avril une amitié intellectuelle avec le nouveau sous-lieutenant britannique du service des achats, le \textbf{\textit{Second Lieutenant} Gilbert}, originaire de l'île anglo-normande de \textbf{Jersey}, francophone, cultivé et poète.",
    181: r"Le jeudi 19 avril 1917, la tournée à \textbf{Bresle}, \textbf{Laviéville} et \textbf{Hénencourt} (Somme, à l'ouest d'Albert) fournit un repère autobiographique précieux : Hippolyte Combes n'était pas retourné dans ces trois villages depuis la \textbf{fin juillet 1915}, époque où la \textbf{18\textsuperscript{e} Division britannique}, tout juste débarquée en France et rassemblée autour de Flesselles, venait prendre en charge le secteur d'Albert. Le lendemain 20 avril, son automobile embourbée (\textit{stuck}) à \textbf{Buire-sur-l'Ancre} est dégagée par des soldats australiens avant une visite à la \textbf{famille Colart} à \textbf{Ribemont-sur-Ancre}.",
    182: r"La violente canonnade entendue les 21 et 22 avril 1917 au nord et au sud d'Arras correspond à la préparation d'artillerie britannique de la \textbf{seconde bataille de la Scarpe} (\textit{Second Battle of the Scarpe}, déclenchée à l'aube du 23 avril 1917 sur la ligne Croisilles–Guémappe). Le guide rapporté d'Amiens par Baptiste Denis est l'ouvrage illustré d'\textbf{Alexis Martin}, \textit{Une visite à Amiens} (Paris, Hennuyer, 1896).",
    185: r"Le samedi 28 avril 1917, un officier britannique rentrant de la station balnéaire anglaise de \textbf{Bournemouth} annonce le déplacement prochain du service des achats vers le secteur de \textbf{Cambrai} (vers lequel le front britannique s'est avancé depuis le repli allemand de mars 1917). Le dimanche 29 avril, après un retour de Contay sur une voiture-citerne (\textit{water-cart}) à la suite du bris de deux ressorts de l'automobile, Hippolyte Combes devise l'après-midi sur la route de Mirvaux avec son ami le sous-lieutenant jersiais \textbf{Gilbert}.",
    186: r"Dernière entrée datée du \textit{Livre-Journal} (\textbf{lundi 30 avril 1917}) : après une tournée matinale par \textbf{Vadencourt}, \textbf{Warloy-Baillon}, \textbf{Hénencourt}, \textbf{Millencourt} et \textbf{Laviéville}, Hippolyte Combes parcourt l'après-midi avec le \textbf{sous-lieutenant Gilbert} les villages de \textbf{Puchevillers}, \textbf{Pierregot} et \textbf{Villers-Bocage}. Six mois plus tard, le \textbf{25 octobre 1917}, il épousera \textbf{Marguerite Calmels} à Millau, avant de poursuivre son service d'interprète auprès de l'Armée britannique jusqu'à l'Armistice du 11 novembre 1918 (Annexe~I, doc.~5) et d'être nommé le 24 novembre 1918 professeur d'anglais à l'École militaire préparatoire des Andelys.",
}


def clean_and_condense_historique(raw_hist: str, scan_num: int) -> str:
    if scan_num in HISTORIQUE_OVERRIDES:
        return HISTORIQUE_OVERRIDES[scan_num]

    h = raw_hist
    # 1. Strip leading \textbf{l.~... :}
    h = re.sub(r"^\\textbf\{.*?\s*:\}\s*", "", h)
    # 2. Remove file references and raw URLs
    h = re.sub(r"\s*\([^()]*\\texttt\{[^}]+\}[^()]*\)", "", h)
    h = re.sub(r"\\texttt\{[^}]+\}", "", h)
    h = re.sub(r"https?://\S+", "", h)
    # 3. Remove parenthetical cross-references to other scans/folios (now in Latin loci)
    h = re.sub(
        r"\s*\((?:voir|cf\.|retrouv[ée]s?|déjà\s+mentionn[ée]s?|prolongeant|comme\s+au|nomm[ée]s?|évoqu[ée]s?|attest[ée]s?)[^()]*#[0-9]{3}[^()]*\)",
        "",
        h,
        flags=re.I,
    )
    h = re.sub(r"\s*;\s*voir\s+(?:aussi\s+)?[Ss]cans?\s*\\?#[0-9]{3}[^).;]*", "", h)
    h = re.sub(r"\s*\(voir\s+(?:aussi\s+)?[Ss]cans?\s*\\?#[0-9]{3}[^()]*\)", "", h, flags=re.I)
    h = re.sub(r",?\s*(?:voir\s+)?[Ss]cans?\s*\\?#[0-9]{3}(?:\s*(?:et|--|à)\s*(?:[Ss]cans?\s*)?\\?#[0-9]{3})*", "", h)

    # 4. Remove any "et non ..." or "quasi-certaine"
    h = re.sub(r"\s*\(et non\b[^()]*\)", "", h, flags=re.I)
    h = re.sub(r",?\s*et non\s+[^,.;)]+", "", h, flags=re.I)
    h = h.replace("de façon quasi-certaine ", "")
    h = h.replace("quasi-certainement ", "")
    h = h.replace("avec certitude ", "")
    h = h.replace("Identification topographique certaine : ", "")
    h = h.replace("Identification prosopographique certaine : ", "")

    # 5. Always call the diarist "Hippolyte Combes" (without corrupting saint Hippolyte, Hippolyte Flandrin, or Maria/Joséphine Combes)
    h = h.replace("le diariste", "Hippolyte Combes").replace("Le diariste", "Hippolyte Combes")
    h = re.sub(
        r"(?<!saint )(?<!Saint )(?<!Augustin )(?<!François-)\bHippolyte\b(?!\s+Combes|\s+Alric|\s+Flandrin)",
        "Hippolyte Combes",
        h,
    )
    h = re.sub(
        r"(?<!Hippolyte )(?<!François-Hippolyte )(?<!Augustin Hippolyte )(?<!Maria )(?<!Joséphine )(?<!Françoise )(?<!Pierre )(?<!famille )(?<!Famille )(?<!des )(?<!Madame )(?<!Mme )(?<!archives )\bCombes\b(?!-Calmels)",
        "Hippolyte Combes",
        h,
    )
    h = h.replace("de Hippolyte Combes", "d'Hippolyte Combes").replace("De Hippolyte Combes", "D'Hippolyte Combes")
    h = h.replace("que Hippolyte Combes", "qu'Hippolyte Combes").replace("Que Hippolyte Combes", "Qu'Hippolyte Combes")
    h = re.sub(r"\(\s*\)", "", h)
    h = re.sub(r"\s+([,.;:!?])", r"\1", h)
    h = re.sub(r"\s{2,}", " ", h).strip()

    # 6. Condense overly long entries (> 560 chars) by keeping the most informative sentences
    if len(h) > 560:
        sentences = re.split(r"(?<=\.)\s+(?=[A-ZÀÉÈÊÎÔÛÇ\\])", h)
        if len(sentences) > 1:
            kept = []
            cur_len = 0
            for s in sentences:
                if cur_len == 0 or (cur_len + len(s) <= 560):
                    kept.append(s)
                    cur_len += len(s) + 1
                else:
                    break
            h = " ".join(kept).strip()

    return h


def build_loci_paralleli(records: list[dict]) -> dict[int, str]:
    """
    Construit pour chacun des 186 folios l'apparat latin des Loci Paralleli,
    avec renvois au numéro de ligne, au lemme en italique, au folio (f° X r°/v°)
    et à la page exacte du PDF (p. \\pageref{fol:N}).
    """
    # 1. Indexer toutes les occurrences (scan_num, line_idx, matched_text) pour chaque entité
    entity_scans: dict[str, list[int]] = {ent_id: [] for ent_id, _, _, _ in LOCI_ENTITIES}
    scan_matches: dict[int, list[tuple[int, str, str, str | None]]] = {r["scan_num"]: [] for r in records}

    for r in records:
        n = r["scan_num"]
        seen_ent_on_scan = set()
        for l_idx, line in enumerate(r["lines"], 1):
            # Ignorer les balises \hfill pour la recherche
            clean_l = line.replace("\\hfill", " ")
            for ent_id, pat, canon_lemma, app_ref in LOCI_ENTITIES:
                if ent_id in seen_ent_on_scan:
                    continue
                m = re.search(pat, clean_l)
                if m:
                    seen_ent_on_scan.add(ent_id)
                    entity_scans[ent_id].append(n)
                    lemma_txt = canon_lemma if canon_lemma else m.group(0).strip(".,;:()[]")
                    scan_matches[n].append((l_idx, ent_id, lemma_txt, app_ref))
        # Aussi vérifier le lieu/titre si la page a très peu de matches dans les lignes
        for ent_id, pat, canon_lemma, app_ref in LOCI_ENTITIES:
            if ent_id in seen_ent_on_scan:
                continue
            if re.search(pat, r["lieu"]) or re.search(pat, r["title"]):
                entity_scans[ent_id].append(n)

    loci_by_scan: dict[int, str] = {}

    # Cas particulier : Couverture (Scan #001)
    loci_by_scan[1] = (
        r"\textbf{1} (\textit{Livre - Journal}) cf. infra "
        + folio_latin_ref(2)
        + r", "
        + folio_latin_ref(186)
        + r". — \textbf{3} (\textit{25 juillet 1916}) cf. infra "
        + folio_latin_ref(2)
        + r". — \textbf{4} (\textit{30 avril 1917}) cf. infra "
        + folio_latin_ref(186)
        + r"."
    )

    # Cas spécifiques où le texte autographe désigne le lieu ou l'action par périphrase :
    explicit_loci_overrides = {
        11: (
            r"\textbf{2} (\textit{pâtures ferme où je loge}) cf. supra "
            + folio_latin_ref(5)
            + r", "
            + folio_latin_ref(10)
            + r". — \textbf{9} (\textit{garret}) cf. supra "
            + folio_latin_ref(5)
            + r"."
        ),
        15: (
            r"\textbf{3} (\textit{nouvelle chambre}) cf. supra "
            + folio_latin_ref(14)
            + r", infra "
            + folio_latin_ref(20)
            + r". — \textbf{7} (\textit{Food : eggs}) cf. supra "
            + folio_latin_ref(3)
            + r", infra "
            + folio_latin_ref(18)
            + r"."
        ),
        81: (
            r"\textbf{4} (\textit{bombardemt terrifiant}) cf. supra "
            + folio_latin_ref(80)
            + r", infra "
            + folio_latin_ref(82)
            + r", "
            + folio_latin_ref(88)
            + r". — \textbf{15} (\textit{notre Coy}) cf. supra "
            + folio_latin_ref(66)
            + r", "
            + folio_latin_ref(80)
            + r"."
        ),
        88: (
            r"\textbf{6} (\textit{ville bombardée}) cf. supra "
            + folio_latin_ref(80)
            + r", "
            + folio_latin_ref(81)
            + r", infra "
            + folio_latin_ref(89)
            + r", "
            + folio_latin_ref(96)
            + r"."
        ),
    }

    for r in records:
        n = r["scan_num"]
        if n == 1:
            continue
        if n in explicit_loci_overrides:
            loci_by_scan[n] = explicit_loci_overrides[n]
            continue
        matches = sorted(scan_matches[n], key=lambda x: x[0])
        items = []
        for l_idx, ent_id, lemma_txt, app_ref in matches:
            all_s = sorted(set(entity_scans[ent_id]))
            others = [s for s in all_s if s != n]
            if not others and not app_ref:
                continue
            supra_s = [s for s in others if s < n]
            infra_s = [s for s in others if s > n]
            ref_parts = []
            if supra_s:
                chosen_supra = [supra_s[0]] if len(supra_s) == 1 else [supra_s[0], supra_s[-1]]
                chosen_supra = sorted(set(chosen_supra))
                ref_parts.append("supra " + ", ".join(folio_latin_ref(s) for s in chosen_supra))
            if infra_s:
                chosen_infra = [infra_s[0]] if len(infra_s) == 1 else [infra_s[0], infra_s[1]]
                chosen_infra = sorted(set(chosen_infra))
                ref_parts.append("infra " + ", ".join(folio_latin_ref(s) for s in chosen_infra))
            if len(others) > 4:
                ref_parts.append(r"\textit{et passim}")
            if app_ref and len(items) == 0:
                ref_parts.append(app_ref)
            ref_str = ", ".join(ref_parts)
            items.append(f"\\textbf{{{l_idx}}} (\\textit{{{lemma_txt}}}) cf. {ref_str}.")
            if len(items) >= 3:
                break

        # Doublon photographique 091 / 093 et inversions photographiques : ajouter le renvoi explicite en tête
        if n == 91:
            items.insert(0, r"\textbf{1--17} (\textit{eadem pagina bis photographata}) cf. infra " + folio_latin_ref(93) + ".")
            items = items[:3]
        elif n == 93:
            items.insert(0, r"\textbf{1--17} (\textit{eadem pagina bis photographata}) cf. supra " + folio_latin_ref(91) + ".")
            items = items[:3]
        elif n == 63:
            items.insert(0, r"\textbf{1} (\textit{Jeudi 5}) de ordine chronologico cf. infra " + folio_latin_ref(64) + ".")
            items = items[:3]
        elif n == 64:
            items.insert(0, r"\textbf{1} (\textit{4 au 5 Oct.}) de ordine chronologico cf. supra " + folio_latin_ref(63) + ".")
            items = items[:3]
        elif n == 112:
            items.insert(0, r"\textbf{1} (\textit{22 Ven.}) de ordine chronologico cf. infra " + folio_latin_ref(113) + ".")
            items = items[:3]
        elif n == 113:
            items.insert(0, r"\textbf{1} (\textit{19 Ma.}) de ordine chronologico cf. supra " + folio_latin_ref(112) + ".")
            items = items[:3]

        loci_by_scan[n] = " — ".join(items)

    return loci_by_scan


def _clean_apparat_entry_note(n: int, entry: dict) -> str:
    """Nettoie une note d'apparat marginal pour supprimer toute redondance ou mention d'ancienne lecture."""
    key = (n, entry["line"], entry["lemma"])
    if key in APPARAT_NOTE_OVERRIDES:
        return APPARAT_NOTE_OVERRIDES[key]
    note = entry["note"].strip()
    if entry["kind"] == "emprunt":
        # Supprimer la répétition ", anglais" ou ", latin" puisque render_notes préfixe déjà \textit{angl.} / \textit{lat.}
        note = re.sub(r",\s*(?:anglais|latin)\s*(?::\s*choses\s+diverses)?\.?$", "", note, flags=re.I)
        note = re.sub(r",\s*dans\s+l[’']usage\s+(?:militaire\s+)?britannique\.?$", "", note, flags=re.I)
        note = re.sub(r",\s*dans\s+l[’']armée\s+britannique\.?$", "", note, flags=re.I)
        note = re.sub(r",\s*anglais\s*;\s*", " ; ", note, flags=re.I)
    elif entry["kind"] == "abreviation":
        note = re.sub(r",\s*anglais\.?$", "", note, flags=re.I)
    note = re.sub(r"\bde la vue 0*(\d+)\b", lambda m: f"du {folio_label_for(int(m.group(1)))}", note)
    note = re.sub(r"\bà la vue 0*(\d+)\b", lambda m: f"au {folio_label_for(int(m.group(1)))}", note)
    note = re.sub(r"\bla vue 0*(\d+)\b", lambda m: f"le {folio_label_for(int(m.group(1)))}", note)
    return note


def enrichir_edition_philologique(records: list[dict], baseline_records: list[dict], clean_line_fn) -> list[dict]:
    """
    Applique à la liste des 186 enregistrements :
    - la correction diplomatique du Folio 1 recto (Scan #002) ;
    - la foliotation (« Couverture (plat supérieur) », « Folio 1 recto » .. « Folio 93 recto ») ;
    - le mois et l'année courants (« mois_annee ») ;
    - les intitulés et lieux nettoyés ;
    - le commentaire critique interne (« critique », uniquement quand pertinent, sinon "") ;
    - l'apparat latin des loci paralleli (« loci ») ;
    - le commentaire historique resserré et pertinent (« historique »).
    """
    from apparat_critique import render_notes

    base_by_num = {r["scan_num"]: r for r in baseline_records}
    hist_data = json.loads(HIST_JSON_PATH.read_text(encoding="utf-8"))
    raw_hist_by_num = {p["scan_num"]: p["changes"]["historique"] for p in hist_data["patches"]}

    # 1. Appliquer la correction des lignes du Folio 1 recto (Scan #002) et nettoyer l'apparat marginal de tous les folios
    for r in records:
        n = r["scan_num"]
        if n == 1:
            r["marginal_notes"] = {
                "1": r"\textbf{1 Livre - Journal} \textit{titulus in pittacio caeruleo.}",
                "3": r"\textbf{3 25 juillet 1916} \textit{terminus a quo.}",
                "4": r"\textbf{4 30 avril 1917} \textit{terminus ad quem.}",
            }
        elif n == 2:
            r["lines"] = list(SCAN_002_LINES)
            r["apparat_entries"] = [
                {"line": 1, "lemma": "Ma.", "kind": "abreviation", "note": "mardi"},
                {"line": 1, "lemma": "m.", "kind": "abreviation", "note": "matin"},
                {"line": 2, "lemma": "Margte", "kind": "abreviation", "note": "Marguerite (Calmels)"},
                {"line": 9, "lemma": "lieutt", "kind": "abreviation", "note": "lieutenant"},
                {"line": 14, "lemma": "off.", "kind": "abreviation", "note": "officiers"},
                {"line": 14, "lemma": "R. Fusrs", "kind": "emprunt", "language": "en", "note": "Royal Fusiliers"},
                {"line": 18, "lemma": "1/2", "kind": "abreviation", "note": "demi"},
                {"line": 18, "lemma": "s.", "kind": "abreviation", "note": "soir"},
                {"line": 19, "lemma": "off.", "kind": "abreviation", "note": "officiers"},
                {"line": 19, "lemma": "mess", "kind": "emprunt", "language": "en", "note": "popote des officiers"},
                {"line": 20, "lemma": "Mme", "kind": "abreviation", "note": "Madame"},
                {"line": 21, "lemma": "Varia", "kind": "emprunt", "language": "la", "note": "dépenses diverses"},
            ]
            r["marginal_notes"] = render_notes(r["apparat_entries"])
        elif "apparat_entries" in r:
            cleaned_entries = []
            for entry in r["apparat_entries"]:
                key = (n, entry["line"], entry["lemma"])
                if key in APPARAT_DROP_KEYS:
                    continue
                new_e = dict(entry)
                new_e["note"] = _clean_apparat_entry_note(n, new_e)
                cleaned_entries.append(new_e)
            r["apparat_entries"] = cleaned_entries
            r["marginal_notes"] = render_notes(cleaned_entries)

        # Foliotation et mois/année
        r["folio"] = folio_label_for(n)
        r["mois_annee"] = mois_annee_for(n)

        # Titre et lieu propres à partir de la base (sans préfixe FOLIO X ni mention de Vue/Scan)
        base_r = base_by_num[n]
        raw_t = base_r["title"]
        m_t = re.match(r"^FOLIO\s+\d+\s+(?:RECTO|VERSO)\s*\((.*)\)$", raw_t, re.I)
        clean_t = m_t.group(1) if m_t else raw_t
        if n == 1:
            clean_t = "Couverture rouge à motif losangé et étiquette bleue autographe : Livre-Journal, du 25 juillet 1916 au 30 avril 1917"
        elif n == 116:
            clean_t = "Concert des « 13th Corps Archie Singers » et tournée dans la voiture Sunbeam"
        elif n == 121:
            clean_t = "Mouvements de troupes autour d'Acheux et visite à la 150th Company A.S.C. près d'Hédauville"
        elif n == 142:
            clean_t = "Après-midi musical avec Marguerite Calmels, visite à l'oncle et la tante Thérèse (Layral) et arrivée de Mimi à Millau"
        r["title"] = clean_t
        r["lieu"] = base_r["lieu"]

        # Commentaire critique interne (Registre 1)
        r["critique"] = CRITIQUES_PERTINENTES.get(n, "")

        # Commentaire historique resserré (Registre 3)
        r["historique"] = clean_and_condense_historique(raw_hist_by_num[n], n)

    # Concilier les lectures et commentaires avant de calculer leurs renvois.
    from conciliation_argon import apply_conciliation
    records = apply_conciliation(records)

    # 2. Construire l'apparat latin des Loci Paralleli (Registre 2)
    from loci_verifies import build_verified_loci
    loci_map = build_verified_loci(records, LOCI_ENTITIES, folio_latin_ref)
    for r in records:
        r["loci"] = loci_map[r["scan_num"]]

    return records
