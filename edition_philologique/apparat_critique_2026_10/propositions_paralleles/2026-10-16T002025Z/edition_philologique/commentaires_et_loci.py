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
    1: r"\textbf{Codicologie :} Plat supérieur du carnet revêtu d'un papier fort rouge gaufré à motif de losanges ; au centre, étiquette rectangulaire de papier bleu à pans coupés portant l'intitulé autographe en cinq lignes à l'encre noire, avec soulignement du titre et deux tirets séparateurs.",
    2: r"\textbf{Disposition de la page :} Première page écrite du carnet, ouverte \textit{in medias res} le mardi 25 juillet 1916. Hippolyte Combes place la date soulignée (\textit{25 Ma.}) en tête de la l.~1 et le mois souligné (\textit{Juillet 1916}) légèrement surélevé dans l'angle supérieur droit ; au bas du feuillet (l.~20--21), un trait horizontal sépare le journal proprement dit du relevé des dépenses.",
    3: r"\textbf{Disposition :} Un trait horizontal sépare au bas du feuillet le récit quotidien et le relevé comptable bilingue de la l.~17 (\textit{Food} / \textit{Washing}).",
    4: r"\textbf{Structure comptable :} Au bas du feuillet (l.~18--24), le relevé des dépenses et de la solde est séparé du récit par un trait horizontal et subdivisé par deux sous-titres topographiques soulignés (\textit{A Renescure}, \textit{A Hazebrouck}).",
    5: r"\textbf{Disposition :} Les quatre dernières lignes (l.~20--23), consacrées au règlement de la logeuse de Lynde et aux frais de route, sont isolées du récit par un trait horizontal continu.",
    9: r"\textbf{Unité de page :} Ce feuillet réunit deux journées consécutives (mercredi 2 août, l.~1--11, et jeudi 3 août, l.~12--19) séparées par un trait horizontal à mi-page, suivies d'un relevé de dépenses au bas du folio.",
    13: r"\textbf{Disposition :} Au bas du feuillet (l.~20--23), une grande accolade marginale gauche réunit les quatre lignes du compte de \textit{mess} et d'achats.",
    16: r"\textbf{Unité de page :} La page regroupe le récit du jeudi 10 août (l.~1--18), un relevé de dépenses (l.~19) et une brève notation datée du mercredi 9 août (l.~20--22) ajoutée en bas de page.",
    17: r"\textbf{Autocensure autographe (l.~20--23) :} Aux quatre dernières lignes du récit, les mots décrivant le supplice infligé au soldat britannique (\textit{attaché à la roue}, \textit{les mains liées}, \textit{les pieds liés}) ont été biffés après coup de traits obliques serrés par Hippolyte Combes, mais demeurent déchiffrables sous la rature.",
    21: r"\textbf{Unité de page :} Deux entrées successives (vendredi 18 août, l.~1--7, et samedi 19 août, l.~8--22) séparées par un trait horizontal ; la phrase de la l.~22 se poursuit sans interruption en tête du f\textsuperscript{o}~11~r\textsuperscript{o}.",
    22: r"\textbf{Enchaînement matériel :} La l.~1 poursuit directement la phrase commencée au bas du f\textsuperscript{o}~10~v\textsuperscript{o} ; la mention de date (\textit{19 Sam --}) est rejetée à l'extrémité droite de la première ligne.",
    23: r"\textbf{Unité de page :} Le feuillet réunit les journées du dimanche 20 août (l.~1--15) et du lundi 21 août (l.~16--20), séparées par un trait horizontal.",
    28: r"\textbf{Continuité :} Feuillet de suite du vendredi 25 août 1916 (\textit{Ven. 25 (suite)}) ; les réflexions personnelles des l.~5--14 sont encadrées de tirets longs caractéristiques de la ponctuation expressive d'Hippolyte Combes.",
    34: r"\textbf{Unité de page :} Ce feuillet réunit le samedi 2 septembre (l.~1--8) et le début du dimanche 3 septembre (l.~9--22), dont la suite et les comptes se trouvent au f\textsuperscript{o}~18~r\textsuperscript{o}.",
    35: r"\textbf{Ordre des folios :} Le f\textsuperscript{o}~17~v\textsuperscript{o} porte les entrées des lundi 4 et mardi 5 septembre 1916, tandis que le f\textsuperscript{o}~18~r\textsuperscript{o} contient la fin de l'entrée du dimanche 3 septembre : Hippolyte Combes a rédigé les journées des 4 et 5 septembre sur la page de gauche avant ou après avoir complété le compte du 3 septembre sur la page en regard.",
    36: r"\textbf{Continuité :} Fin du récit et relevé des dépenses de la journée du dimanche 3 septembre 1916, faisant suite au f\textsuperscript{o}~17~r\textsuperscript{o}.",
    49: r"\textbf{Disposition :} Le feuillet réunit le dimanche 24 septembre (l.~1--16) et le relevé récapitulatif des dépenses des 23 et 24 septembre (l.~17--22) encadré d'un crochet comptable.",
    52: r"\textbf{Continuité :} Première page consacrée à la journée parisienne du mardi 26 septembre 1916 (arrivée à la gare du Nord et matinée à Neuilly), poursuivie au f\textsuperscript{o}~26~v\textsuperscript{o}.",
    53: r"\textbf{Structure comptable :} Seconde page du mardi 26 septembre 1916, occupée aux l.~12--23 par le tableau détaillé des achats effectués par Hippolyte Combes à Paris avant son départ pour Toulouse.",
    61: r"\textbf{Tableau financier :} Page entièrement consacrée au bilan comptable de la permission toulousaine du 3 octobre 1916, articulé autour d'un solde encadré (\textit{En caisse : 272 f.}) suivi des dépenses détaillées.",
    63: r"\textbf{Inversion de la séquence photographique :} Le f\textsuperscript{o}~31~v\textsuperscript{o} (journée du jeudi 5 octobre 1916 à Paris et retour vers le front) et le f\textsuperscript{o}~32~r\textsuperscript{o} (soirée du mercredi 4 octobre et nuit du 4 au 5 octobre dans l'express Toulouse–Paris) ont été photographiés dans l'ordre inverse de la chronologie.",
    64: r"\textbf{Chronologie interne :} Ce feuillet (fin de la journée du 4 octobre 1916 au départ de Toulouse et voyage de nuit vers Paris) précède chronologiquement le f\textsuperscript{o}~31~v\textsuperscript{o}.",
    74: r"\textbf{Renvoi infrapaginal autographe :} À la l.~10, Hippolyte Combes insère un appel de note \texttt{(1)} renvoyant au post-scriptum de cinq lignes (l.~17--21) tracé au bas du feuillet sous un trait horizontal de séparation.",
    75: r"\textbf{Unité de page :} La page s'ouvre par un bloc comptable entre crochets (l.~1--4) soldant les frais de logement à Ribeaucourt, suivi de l'entrée du lundi 16 octobre 1916 (l.~5--21).",
    90: r"\textbf{Discours direct bilingue :} Aux l.~17--19, Hippolyte Combes rapporte au style direct, en français puis en anglais entre guillemets, sa réplique au major Hughes et l'accueil du colonel Grose.",
    91: r"\textbf{Doublon photographique :} Ce feuillet (fin de la journée du 2 novembre et journée du 3 novembre 1916) a fait l'objet de deux prises de vue lors de la numérisation du carnet (voir f\textsuperscript{o}~46~v\textsuperscript{o}) ; la transcription diplomatique est maintenue à l'identique sur les deux doubles pages.",
    93: r"\textbf{Seconde prise de vue du même feuillet :} Ce cliché reproduit la même page manuscrite que le f\textsuperscript{o}~45~v\textsuperscript{o} (journées des 2 et 3 novembre 1916).",
    105: r"\textbf{Renvoi interne :} L'appel de note \texttt{(1)} placé à la fin du récit du 1\textsuperscript{er} décembre (l.~14) renvoie à la mention d'achat de tabac pour le capitaine Huguet inscrite au bas du feuillet (l.~26).",
    112: r"\textbf{Inversion photographique :} Le f\textsuperscript{o}~56~r\textsuperscript{o} (journées des 22, 23 et vigile de Noël 24 décembre 1916) et le f\textsuperscript{o}~56~v\textsuperscript{o} (journées des 19, 20 et 21 décembre 1916) ont été photographiés dans l'ordre inverse de la chronologie.",
    113: r"\textbf{Chronologie interne :} Ce feuillet, qui réunit les entrées des mardi 19, mercredi 20 et jeudi 21 décembre 1916 séparées par des traits horizontaux, précède chronologiquement le f\textsuperscript{o}~56~r\textsuperscript{o}.",
    118: r"\textbf{Disposition :} L'année nouvelle (\textit{1917}) est mise en évidence dès l'en-tête souligné de la l.~1 (\textit{1\textsuperscript{er} Lundi — 1917 — \hfill Janvier.}) ; le feuillet regroupe les 1\textsuperscript{er} et 2 janvier 1917.",
    132: r"\textbf{Feuillet comptable :} Page entièrement dédiée au relevé des dépenses de voyage des 27 et 28 janvier 1917 (Paris, train d'Orsay et arrivée à Toulouse), réparties par localités soulignées.",
    133: r"\textbf{Bilan financier :} Second feuillet comptable récapitulant les grands achats de fiançailles à Toulouse le 28 janvier 1917 (montre en or, bagues, chaîne) et l'état de la caisse (\textit{En caisse}).",
    136: r"\textbf{Rature autographe (l.~15) :} À la fin du récit de la visite à son ancien appartement toulousain, Hippolyte Combes a biffé une proposition commençant par \textit{Évité troubler} sous une surcharge d'encre dense.",
    140: r"\textbf{Feuillet comptable :} Page récapitulative des dépenses toulousaines du samedi 3 février 1917 (dentiste M.~de Lersay, billets de chemin de fer pour Millau) et du solde en caisse (\textit{En caisse : 244 f. 85}).",
    147: r"\textbf{Continuité :} Deuxième des trois feuillets consacrés à la seule journée du mercredi 7 février 1917 (\textit{Merc. 7 (suite)}), relatant le retour de permission entre Paris, Amiens et Hérissart.",
    148: r"\textbf{Continuité :} Troisième et dernier feuillet de la journée du 7 février 1917 (\textit{Merc. 7 (fin)}), complété par le début de l'entrée du jeudi 8 février (l.~12--18).",
    157: r"\textbf{Mention financière en en-tête :} Exceptionnellement, Hippolyte Combes inscrit son solde disponible (\textit{En caisse : 225 f. 95}) directement sur la première ligne entre la date soulignée et le mois.",
    165: r"\textbf{Unité de page :} La page réunit le départ du capitaine Williams le samedi 10 mars 1917 (l.~1--18, avec citation anglaise au style direct à la l.~9) et un état récapitulatif de caisse au bas du feuillet (l.~19--22).",
    186: r"\textbf{Clôture du carnet :} Dernier feuillet du \textit{Livre-Journal}, daté du lundi 30 avril 1917 (date qui correspond au \textit{terminus ad quem} inscrit par Hippolyte Combes sur l'étiquette de la couverture).",
}


# Corrections ciblées de notes marginales pour éliminer toute glose française
# métatextuelle et harmoniser le latin philologique :
MARGINAL_NOTES_FIXES = {
    (17, "6"): r"\textbf{6} \llbracket décapité [?]\rrbracket\ \textit{del. in ms.} \textbf{6} \llbracket bras emportés [?]\rrbracket\ \textit{del. in ms.}",
    (17, "12"): r"\textbf{12} \llbracket perpétuelle [?]\rrbracket\ \textit{del. in ms.}",
    (57, "17"): r"\textbf{17} \textit{add. in marg. (lect. incert.).}",
    (86, "11"): r"\textbf{11} \textit{in marg. cum unco} (comptes). \textbf{11 R.E.} \textit{vel} R.F., \textit{lect. incert.} \textbf{11 Hair cut} \textit{angl. in ms.}",
    (90, "15"): r"\textbf{15} \textit{lect. incert. in ms.} \textbf{15 Lt} \textit{abbr. pro} Lieutenant. \textbf{15 kit} \textit{angl. in ms.}",
    (141, "2"): r"\textbf{2 Monté} \textit{lect. incert. in ms.} \textbf{2 chambre} \textit{supra lin. in ms.}",
    (142, "6"): r"\textbf{6 (Layral)} \textit{scil.} Charles et Thérèse Layrals.",
    (148, "11"): r"\textbf{11 f.} \textit{abbr. pro} franc(s). \textbf{11 lunch, room} \textit{angl. in ms. (\emph{et room} infra lin. add.).}",
    (151, "19"): r"\textbf{19 Ds} \textit{abbr. pro} Dans. \textbf{19 1/2 du jour} \textit{scil.} milieu du jour.",
    (155, "17"): r"\textbf{17 Roulé} \textit{vel} Rôdé, \textit{lect. incert. in ms.}",
    (158, "14"): r"\textbf{14 f.} \textit{abbr. pro} franc(s).",
    (182, "14"): r"\textbf{14 gde} \textit{abbr. pro} grande. \textbf{14 cathle} \textit{abbr. pro} cathédrale. \textbf{14 avec} \textit{lect. incert. in ms.}",
}


# Catalogue prosopographique, militaire, topographique et thématique pour la
# génération de l'apparat latin des Loci Paralleli :
# (id, regex_in_line, canonical_lemma_override_or_None, appendix_ref_or_None)
LOCI_ENTITIES = [
    ("marguerite", r"\b(?:Margte|Marg\.|Mte|Marguerite|Gueïte|ma\s+Femme|fiancée)\b", None, r"Appendicem I, doc.~5 (p.~\pageref{annexe:doc5})"),
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
    ("st_michel_ternoise", r"\bSt-Michel\b", "St-Michel", None),
    ("bedfords", r"\b(?:Bedfords|Bedfs)\b", None, None),
    ("west", r"\b(?:Cap\.|Capt\.)\s*West\b|\bWest\b", None, None),
    ("panton", r"\b(?:Cap\.|Capt\.|Lt)\s*Panton\b|\bPanton\b", None, None),
    ("walsh", r"\b(?:Lt\s+)?Walsh\b", None, None),
    ("ford", r"\b(?:Lt\s+)?Ford\b", None, None),
    ("first", r"\bLt\s+First\b", "Lt First", None),
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
    ("houthouan", r"\bHouthouan\b", "Houthouan", None),
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
    ("millau", r"\bMillau\b", "Millau", r"Appendicem I, doc.~5 (p.~\pageref{annexe:doc5})"),
    ("mimi", r"\bMimi\b", "Mimi", None),
    ("madeleine", r"\b(?:Madeleine|Madne)\b", None, None),
    ("pierre_calmels", r"\bPierre\b", "Pierre", None),
    ("vincens", r"\b(?:Vincens|Fernand|Germaine|Robert)\b", None, None),
    ("layral", r"\bLayral\b", "Layral", None),
    ("amiens", r"\bAmiens\b", "Amiens", None),
    ("doullens", r"\bDoullens\b", "Doullens", None),
    ("canaples", r"\bCanaples\b", "Canaples", None),
    ("coy_152", r"\b152(?:nd|e)?\s*(?:Coy|Cy|Cie)?\b", None, None),
    ("coy_150", r"\b150(?:th|e)?\s*(?:Coy|Cy|Cie)?\b", None, None),
    ("div_18", r"\b18(?:th|e)\s*(?:Div(?:on|\.)?|Division)\b", None, r"Appendicem I, doc.~1 et 2 (p.~\pageref{annexe:doc1})"),
    ("brig_54", r"\b54(?:th|e)\s*Brigade\b", None, None),
    ("ribeaucourt", r"\bRibeaucourt\b", "Ribeaucourt", None),
    ("barlette", r"\bBarlette\b", "Barlette", None),
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
    ("forage", r"\b(?:green\s+forage|green\s+fourrage|fourrage|paille\s*&\s*foin)\b", None, None),
    ("solde_84", r"\b84\s*f(?:r\.?)?\b", "84 f.", None),
    ("ymca", r"\bY\.M\.C\.A\.\b", "Y.M.C.A.", None),
    ("efc", r"\b(?:E\.F\.C\.|Exp\.\s*F\.\s*Canteen|Canteen|canteen)\b", None, None),
]


# Réécritures historiques ciblées et resserrées pour les folios clés :
HISTORIQUE_OVERRIDES = {
    1: r"Les bornes chronologiques portées sur l'étiquette couvrent neuf mois de campagne d'\textbf{Hippolyte Combes} (né à Millau le 14 août 1876, décédé le 2 septembre 1970 à l'Hôtel du Centre à Saint-Chély-d'Apcher, Lozère) auprès du corps expéditionnaire britannique (\textit{British Expeditionary Force}). Affecté depuis août 1915 à la \textbf{152\textsuperscript{e} Compagnie de l'\textit{Army Service Corps}} au sein du Train divisionnaire de la \textbf{18\textsuperscript{e} Division britannique} (\textit{18th Eastern Division}), Hippolyte Combes passe en novembre 1916 au service des achats et réquisitions de fourrage (\textit{Foraging} puis \textit{Army Purchase Board}) dans la Somme.",
    2: r"Relevée de la Somme le 20 juillet 1916 après les combats du bois des Trônes, la \textbf{18\textsuperscript{e} Division britannique} (\textit{18th Eastern Division}, commandée par le major-général Sir Ivor Maxse) gagne la Flandre intérieure (Capt. G.~H.~F. Nichols, \textit{The 18th Division in the Great War}, Londres, Blackwood, 1922, p.~81–85). L'église entourée de son cimetière à \textbf{Sercus} (Nord) est l'église \textbf{Saint-Érasme} (soubassements romans du XII\textsuperscript{e}~s., transformée en \textit{hallekerke} à trois nefs au XVI\textsuperscript{e}~s. ; Base Mérimée, \texttt{PA00107816}).",
    3: r"À \textbf{Lynde} (Nord), Hippolyte Combes assiste le lieutenant Michel (\textit{billeting officer}) pour préparer le cantonnement de 36 officiers des \textbf{\textit{Royal Fusiliers}} (dont le 11\textsuperscript{e} Bataillon appartient à la 54\textsuperscript{e} Brigade de la 18\textsuperscript{e} Division) avant l'ordre de départ pour la frontière belge.",
    4: r"À \textbf{Renescure} (Nord), les deux châteaux remarqués par Hippolyte Combes correspondent au \textbf{château de Zuthove} (demeure seigneuriale de briques entourée de douves, reconstruite à la fin du XV\textsuperscript{e}~s. ; Base Mérimée, \texttt{PA00107784}) et au \textbf{château dit de Philippe de Comines} (ancienne motte castrale remaniée et transformée en mairie ; \texttt{PA00107783}), voisin de l'église-halle \textbf{Notre-Dame-de-l'Assomption}. À \textbf{Hazebrouck}, il visite l'église \textbf{Saint-Éloi} (XVI\textsuperscript{e}~s.) et perçoit 84~francs de solde et indemnités auprès de la Mission française.",
    13: r"Le point de ravitaillement quotidien (\textit{refilling point}) est établi sur la Lys canalisée près de l'écluse de \textbf{Bac-Saint-Maur} (Sailly-sur-la-Lys). Au hameau de \textbf{La Croix-du-Bac} (Steenwerck), l'église de briques rouges décrite par Hippolyte Combes est l'église néo-gothique \textbf{Notre-Dame-des-Sept-Douleurs}, bâtie en 1869–1870 par l'architecte lillois Charles Leroy (Base Mérimée, \texttt{IA59000348}).",
    16: r"Promenade le long de la Lys jusqu'au pont de \textbf{Sailly-sur-la-Lys} (Pas-de-Calais), dont l'église Saint-Vaast avait été incendiée lors des combats d'octobre 1914. À l'écluse, Hippolyte Combes s'entretient avec l'éclusier au sujet du \textbf{major-général Sir Ivor Maxse} (1862–1958), commandant la \textbf{18\textsuperscript{e} Division britannique} de 1914 à janvier 1917 ; la mention des \textit{Australiens} fait écho à l'engagement des divisions de l'I~ et du II~ANZAC Corps dans le secteur voisin de Fromelles et d'Armentières en juillet–août 1916.",
    17: r"Le bombardement allemand du 11 août 1916 sur les abords d'\textbf{Armentières} touche un soldat britannique et endommage la \textbf{blanchisserie industrielle de fils et toiles Barbry}, établie en bordure de la Lys près du pont de Nieppe et dirigée par \textbf{Émile Barbry} (Base Mérimée, \texttt{IA59001501}). Aux l.~20–23, le passage raturé décrit la peine disciplinaire réglementaire britannique dite \textit{Field Punishment No.~1} (\textit{crucifixion}), consistant à attacher le condamné par les poignets et les chevilles à une roue de caisson.",
    32: r"Descendu de Marquay à \textbf{Saint-Pol-sur-Ternoise} (Pas-de-Calais) par Ramecourt et Saint-Michel-sur-Ternoise, Hippolyte Combes visite l'ancienne chapelle conventuelle des \textbf{Carmes} (XVII\textsuperscript{e}~s., bâtie en briques rouges en 1697 et devenue église paroissiale Saint-Paul après la destruction de l'ancienne église au XVI\textsuperscript{e}~s.), où une plaque commémore la nuit de prière passée en mars 1767 par saint \textbf{Benoît-Joseph Labre} (1748–1783).",
    33: r"À \textbf{Ligny-Saint-Flochel} (Pas-de-Calais), les manœuvres observées en lisière des bois s'inscrivent dans l'entraînement tactique de la \textbf{18\textsuperscript{e} Division britannique} avant son retour sur la Somme (Nichols, 1922, p.~86). L'église \textbf{Saint-Flochel} conserve un clocher de pierre des XV\textsuperscript{e}–XVI\textsuperscript{e}~siècles classé monument historique (Base Mérimée, \texttt{PA00108332}).",
    38: r"Les deux fourgons (\textit{waggons}) venus charger le fourrage vert derrière la ferme Collet appartiennent au \textbf{\textit{Bedfordshire Regiment}} (\textit{Bedfords}), dont le 7\textsuperscript{e} Bataillon (\textit{Service}) fait partie de la 54\textsuperscript{e} Brigade de la \textbf{18\textsuperscript{e} Division britannique} (Nichols, 1922, p.~86).",
    40: r"Le hameau d'\textbf{Oppy} où cantonne la compagnie le 9 septembre 1916 est l'écart d'Oppy rattaché à la commune de \textbf{Beaudricourt} (Pas-de-Calais, canton d'Avesnes-le-Comte, à l'ouest d'Arras), où Hippolyte Combes se rend à pied le 10 septembre auprès du maire pour le service de cantonnement.",
    41: r"Longue étape à cheval conduisant la colonne du Pas-de-Calais dans la Somme par \textbf{Lucheux}, \textbf{Thièvres} et \textbf{Raincheval}. À \textbf{Lucheux} (Somme), Hippolyte Combes remarque les ruines du château fort des comtes de Saint-Pol (XII\textsuperscript{e}–XIV\textsuperscript{e}~s. ; Base Mérimée, \texttt{PA00116194}) et le beffroi abritant le chêne historique sous lequel la tradition locale situe la signature par \textbf{Louis~XI} de l'édit du 19 juin 1464 instituant la poste royale.",
    53: r"À la librairie Armand Colin (boulevard Saint-Michel), Hippolyte Combes acquiert deux ouvrages contemporains : l'essai d'\textbf{Ernest Zyromski} (1862–1933, professeur de littérature française à la Faculté des lettres de Toulouse), \textbf{\textit{L'Orgueil humain}} (Armand Colin, 1904), et le recueil d'essais de guerre de \textbf{Maurice Maeterlinck}, \textbf{\textit{Les Débris de la guerre}} (Fasquelle, Bibliothèque-Charpentier, 1916).",
    54: r"Arrivé à \textbf{Toulouse} pour sa première permission, Hippolyte Combes retrouve sa fiancée \textbf{Marguerite Calmels} (1892–1974) chez l'oncle et la tante de celle-ci, \textbf{Émile Crouzet} (1842–1921, agent de change à Toulouse) et \textbf{Élisabeth Calmels}, et revoit le pensionnat jésuite de \textbf{Sainte-Marie-des-Champs} (Le Caousou) où il avait accompli ses études secondaires.",
    55: r"Après avoir offert à Marguerite Calmels un bouquet acheté place Esquirol, Hippolyte Combes effectue avec elle, \textbf{Élisabeth Calmels-Crouzet} et \textbf{Émile Crouzet} (\textit{M.~Czt}) une promenade sur les coteaux dominant la Garonne au sud de Toulouse, par l'église de \textbf{Pouvourville} et la crête de \textbf{Pech-David}.",
    56: r"Journée de fiançailles à \textbf{Toulouse} le vendredi 29 septembre 1916 : Hippolyte Combes offre à \textbf{Marguerite Calmels} — qu'il appelle déjà dans l'intimité du carnet \textit{ma Femme}, un an avant leur mariage célébré à Millau le 25 octobre 1917 — un sautoir en or acquis 295~francs.",
    57: r"Promenade toulousaine avec Marguerite Calmels le long des allées et du \textbf{canal du Midi} jusqu'au faubourg Saint-Étienne, rythmée par la sonnerie des cinq cloches de la cathédrale \textbf{Saint-Étienne de Toulouse}.",
    58: r"Dimanche 1\textsuperscript{er} octobre 1916 à \textbf{Toulouse} : après la messe matinale à la cathédrale \textbf{Saint-Étienne}, Hippolyte Combes range sa bibliothèque personnelle dans son appartement toulousain avant une promenade vespérale au Grand-Rond avec Marguerite Calmels.",
    66: r"Première mention explicite dans le carnet du numéro de l'unité britannique d'Hippolyte Combes : la \textbf{152\textsuperscript{e} Compagnie de l'\textit{Army Service Corps}} (\textit{152nd Company A.S.C.}), rattachée au \textit{18th Divisional Train} et chargée du ravitaillement de la \textbf{54\textsuperscript{e} Brigade d'infanterie} de la 18\textsuperscript{e} Division, qui vient de livrer la bataille de la crête de Thiepval (26–30 septembre 1916) et a établi sa tête de ligne ferroviaire (\textit{railhead}) à \textbf{Canaples} (Somme).",
    83: r"À \textbf{Albert} (Somme), Hippolyte Combes décrit la basilique \textbf{Notre-Dame de Brebières} (édifiée en briques rouges de 1885 à 1895 par l'architecte Edmond Duthoit), dont le dôme de 70~m frappé par les obus allemands en janvier 1915 retenait à l'horizontale la célèbre statue dorée de la \textbf{Vierge penchée} d'Albert Roze. L'adjudant interprète \textbf{Schumacher} lui annonce le projet ministériel de relève des jeunes interprètes de la réserve de l'armée territoriale (\textit{R.A.T.}).",
    90: r"Le commandant du Train divisionnaire (\textit{18th Divisional Train Office}) qui signe l'ordre détachant Hippolyte Combes au service du fourrage à Acheux-en-Amiénois est le \textbf{lieutenant-colonel Daniel Charles Evans Grose}, A.S.C. (\texttt{Col. Grose}), commandant le \textit{18th Divisional Train} de 1915 à 1918 et décoré du \textit{Distinguished Service Order} (\textit{London Gazette}, 4 juin 1917, p.~5470 ; Nichols, 1922, p.~110).",
    91: r"Dès son arrivée à \textbf{Acheux-en-Amiénois} le 2 novembre 1916, Hippolyte Combes est présenté à Raincheval au \textbf{major Levy} (officier supérieur britannique dirigeant le service des achats et réquisitions d'armée). Le 3 novembre, il revient faire ses adieux au camp de la \textbf{152\textsuperscript{e} Compagnie A.S.C.} et perçoit à Albert le reliquat de sa solde.",
    93: r"Seconde prise de vue du feuillet des 2 et 3 novembre 1916 : présentation d'Hippolyte Combes au \textbf{major Levy} à Raincheval et règlement de sa solde au bureau de la Mission française à \textbf{Albert} après six jours de retenue de permission.",
    105: r"En se rendant à \textbf{Franvillers} et \textbf{Buire-sur-l'Ancre} le 1\textsuperscript{er} décembre 1916, Hippolyte Combes revoit la vallée de \textbf{Ribemont-sur-Ancre} et \textbf{Heilly}, où il avait cantonné avec la 18\textsuperscript{e} Division durant l'hiver 1915–1916. Le samedi 2 décembre survient à Acheux l'arrivée du jeune \textbf{capitaine Williams} (\textit{Foraging Officer}), appelé à remplacer le lieutenant Curtis.",
    112: r"Réveillon et nuit de Noël 1916 au château d'\textbf{Acheux-en-Amiénois}, où est installée l'école de mortiers de tranchée de la V\textsuperscript{e} Armée britannique (\textit{Fifth Army School of Mortars}).",
    113: r"À \textbf{Raincheval}, Hippolyte Combes attend devant le bureau de la commission d'achats de l'armée (\textbf{\textit{Army Purchase Board}}) et perçoit sa solde bimensuelle (84~francs) au bureau de la Mission française du \textbf{XIII\textsuperscript{e} Corps britannique}.",
    116: r"Soirée de Noël prolongée à Acheux le 28 décembre 1916 au foyer de la \textit{Y.M.C.A.} par le concert de la troupe divisionnaire des \textbf{\textit{13th Corps Archie Singers}} (groupe artistique formé par les batteries de défense contre aéronefs, familièrement appelées \textit{Archies} dans l'argot militaire britannique). Le lendemain, tournée à Raincheval, Le Quesnoy et Louvencourt dans une automobile d'état-major \textit{Sunbeam}.",
    121: r"Les mouvements de convois autour d'Acheux accompagnent l'extension du secteur du \textbf{V\textsuperscript{e} Corps britannique} dans la vallée de l'Ancre. À \textbf{Hédauville}, Hippolyte Combes rend visite le 9 janvier 1917 à la \textbf{150\textsuperscript{e} Compagnie de l'A.S.C.} (\textit{150th Company A.S.C.}, commandée par le major H.~G. Peachy), compagnie sœur de la 152\textsuperscript{e} Compagnie au sein du \textit{18th Divisional Train} (Maj. A.~F. Becke, \textit{Order of Battle}, Part~3A, p.~81), où sert son ami le \textbf{lieutenant Morris}.",
    125: r"Sous la vague de froid polaire de la mi-janvier 1917 en Picardie, Hippolyte Combes poursuit les tournées quotidiennes de réquisition à Belle-Église, Raincheval et Puchevillers et perçoit sa solde bimensuelle (84~francs) au bureau de la Mission française du \textbf{V\textsuperscript{e} Corps britannique}.",
    130: r"En escale à Paris le samedi 27 janvier 1917 au matin, Hippolyte Combes se rend à \textbf{Neuilly-sur-Seine} pour rendre visite à la famille de \textbf{Mme Faure} (cousines de Marguerite Calmels).",
    131: r"Suite de la visite familiale du 27 janvier 1917 à \textbf{Neuilly-sur-Seine} chez \textbf{Mme Faure}, entourée de sa fille \textbf{Germaine} et de son fils \textbf{Marcel Faure} alors en permission, tandis que ses deux autres fils, \textbf{Henri} (aspirant d'infanterie) et \textbf{André} (candidat à l'École polytechnique), sont évoqués dans la conversation.",
    134: r"À \textbf{Toulouse} le 29 janvier 1917, Hippolyte Combes retire en gare Matabiau un panier de fleurs expédié de Nice pour Marguerite Calmels, visite avec elle et sa sœur aînée \textbf{Madeleine Calmels-Vincens} la basilique romane \textbf{Saint-Sernin} et ses cryptes (voisines de l'ancien domicile familial des Combes rue du Taur), puis parcourt les grands magasins du Capitole et la \textbf{Maison Universelle} fondée par \textbf{Antoine Labit} (1832–1912, père du voyageur et collectionneur Georges Labit).",
    135: r"Journée toulousaine du 30 janvier 1917 : après l'achat d'une montre-bracelet en or (200~fr.) et de deux bagues chez l'horloger-bijoutier \textbf{Pfister} (rue d'Alsace-Lorraine / place Esquirol), Hippolyte Combes assiste à 17~h avec Marguerite Calmels et sa sœur Madeleine au cours public du professeur \textbf{Ernest Zyromski} (1862–1933) à la Faculté des lettres de Toulouse, consacré au poète tarnais \textbf{Maurice de Guérin} (1810–1839).",
    136: r"Promenade à \textbf{Toulouse} avec Marguerite Calmels le 31 janvier 1917 par le marché Victor-Hugo, la cour Renaissance de l'\textbf{Hôtel d'Assézat} (édifié à partir de 1555 sur les plans de Nicolas Bachelier), et les églises \textbf{Notre-Dame de la Daurade} et \textbf{Notre-Dame de la Dalbade} (dont le cousin Jean Crouzet deviendra curé), suivie au matin du 1\textsuperscript{er} février d'une marche vers \textbf{Lardenne} et les ruines de l'amphithéâtre gallo-romain de \textbf{Purpan-Ancely} (I\textsuperscript{er}~s. apr. J.-C.).",
    139: r"Voyage ferroviaire du samedi 3 février 1917 de \textbf{Toulouse} à \textbf{Millau} en compagnie de Marguerite Calmels : salut en gare de Carcassonne au cousin l'\textbf{abbé Jean Crouzet}, halte à \textbf{Béziers} avec visite de l'ancienne cathédrale gothique \textbf{Saint-Nazaire} et de sa terrasse dominant l'Orb, puis arrivée nocturne en gare de Millau où les attend \textbf{Pierre Calmels}, frère de Marguerite.",
    142: r"\textbf{Thérèse Cartairade} et son époux \textbf{M\textsuperscript{e}~Charles Layrals}, notaire à Millau (parents du notaire Louis Layrals, \dag~1961, et du magistrat Jean Layrals, \dag~1947), auxquels Hippolyte Combes et Marguerite Calmels rendent visite le dimanche 4 février 1917 à 18~h~15, sont la tante et l'oncle maternels de Marguerite. \textbf{« Mimi »}, arrivée par le train de 18~h, est le surnom familial d'\textbf{Anne-Marie Calmels} (1888–1975), sœur de Marguerite et future épouse de l'avoué millavois \textbf{Joseph Delcamps}.",
    150: r"Conduit le 9 février 1917 par le \textbf{lieutenant Croughton} au bureau de la Mission militaire française de la \textbf{V\textsuperscript{e} Armée britannique} (\textit{Fifth Army}) à \textbf{Toutencourt}, Hippolyte Combes apprend qu'il relève désormais administrativement de la Mission d'armée, avec paiement de la solde à dates fixes les \textbf{3 et 18 de chaque mois}. Le lendemain, après un passage aux lignes du parc automobile (\textit{Motor Transport}, \textit{M.T. A.S.C.}), il se rend en tournée au château de \textbf{Martinsart}.",
    155: r"Après une visite officielle en grande tenue au maire d'\textbf{Hérissart} le 15 février 1917, Hippolyte Combes parcourt le lendemain les fermes et le château de \textbf{Beaucourt-sur-l'Hallue} (Somme, canton de Villers-Bocage, à 7~km au sud d'Hérissart) pour l'achat de paille et de foin.",
    158: r"Lors de sa halte du 21 février 1917 à \textbf{Doullens} au retour d'\textbf{Auxi-le-Château}, Hippolyte Combes expédie un mandat-poste de 42~francs à \textbf{Mme Spagnol} à \textbf{Nice} en règlement du panier de fleurs reçu en gare de Toulouse le 29 janvier pour Marguerite Calmels.",
    160: r"Les régiments de \textbf{cavalerie indienne} traversant \textbf{Hérissart} le 28 février 1917 appartiennent aux \textbf{4\textsuperscript{e} et 5\textsuperscript{e} Divisions de cavalerie} (anciennes \textit{1st} et \textit{2nd Indian Cavalry Divisions} renommées en novembre 1916 au sein du \textit{Cavalry Corps} de la B.E.F. ; Maj. A.~F. Becke, \textit{Order of Battle}, Part~2A, p.~35–48).",
    164: r"L'interprète \textbf{Valet}, rencontré le 8 mars 1917 à Hérissart, est rattaché à la \textbf{2\textsuperscript{e} Division australienne} (\textit{2nd Australian Division}, unité de l'\textit{I~Anzac Corps} alors engagée devant Bapaume). Le 9 mars au soir, Hippolyte Combes solde ses comptes de \textit{mess} avec le \textbf{capitaine Williams} à la veille du départ de ce dernier.",
    166: r"Le dimanche 11 mars 1917, au bureau de la Mission française de la V\textsuperscript{e} Armée à \textbf{Toutencourt}, Hippolyte Combes apprend que, sur la demande expresse du \textbf{major Levy}, il est maintenu à la commission d'achats de l'armée (\textbf{\textit{Army Purchase Board}}) à \textbf{Hérissart}, où il s'installe dans le logement (\textit{billet} n\textsuperscript{o}~220) laissé libre par l'interprète Valet.",
    168: r"Au \textbf{Mesnil-Martinsart} (Somme), Hippolyte Combes rend visite le 13 mars 1917 à son collègue de l'Instruction publique \textbf{Fortuné Flutre}, instituteur de la commune (auteur en 1899 d'une notice historique sur Le Mesnil-Martinsart), et à son épouse, parents du romaniste \textbf{Louis-Fernand Flutre} (1892–1978), admis à l'\textbf{École normale supérieure} en 1914 (entré en 1919 après la guerre, agrégé de grammaire en 1921, professeur à la Faculté des lettres de Lyon et auteur en 1955 de deux monographies historiques et linguistiques sur Le Mesnil-Martinsart ; R.~Debrie, \textit{Revue de linguistique romane}, 42, 1978, p.~238–240).",
    170: r"Dans la nuit du 19 au 20 mars 1917, Hippolyte Combes cède le lit de sa chambre d'Hérissart à un jeune lieutenant britannique de la \textbf{63\textsuperscript{e} Division (\textit{63rd Royal Naval Division})}, dont le bataillon vient d'être relevé des tranchées boueuses de \textbf{Miraumont} et d'\textbf{Achiet-le-Petit} au début du repli stratégique allemand sur la ligne Hindenburg (opération \textit{Alberich}).",
    171: r"En mars 1917, lors de la marche en avant suivant le repli allemand sur la ligne Hindenburg, le \textbf{17\textsuperscript{e} Lanciers britannique} (\textit{17th Duke of Cambridge's Own Lancers}, surnommé \textit{Death or Glory Boys} d'après la devise de son insigne à tête de mort) formait l'unique régiment britannique de la \textit{Sialkot Cavalry Brigade} au sein de la \textbf{4\textsuperscript{e} Division de cavalerie} (ex-\textit{1st Indian Cavalry Division}), aux côtés des lanciers indiens des \textit{6th King Edward's Own Cavalry} et \textit{19th Lancers (Fane's Horse)} (Maj. A.~F. Becke, \textit{Order of Battle}, Part~2A, p.~35–40).",
    179: r"Après la tempête de neige du 11 avril 1917 (jour de la première attaque anglo-australienne devant Bullecourt) et ses achats à \textbf{Doullens}, Hippolyte Combes noue le vendredi 13 avril une amitié intellectuelle avec le nouveau sous-lieutenant britannique du service des achats, le \textbf{\textit{Second Lieutenant} Gilbert}, originaire de l'île anglo-normande de \textbf{Jersey}, francophone, cultivé et poète.",
    182: r"La violente canonnade entendue les 21 et 22 avril 1917 au nord et au sud d'Arras correspond à la préparation d'artillerie britannique de la \textbf{seconde bataille de la Scarpe} (\textit{Second Battle of the Scarpe}, déclenchée à l'aube du 23 avril 1917 sur la ligne Croisilles–Guémappe). Le guide rapporté d'Amiens par Baptiste Denis est l'ouvrage illustré d'\textbf{Alexis Martin}, \textit{Une visite à Amiens} (Paris, Hennuyer, 1896).",
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
        r"\s*\((?:voir|cf\.|retrouv[ée]s?|déjà\s+mentionn[ée]s?|prolongeant|comme\s+au)[^()]*#[0-9]{3}[^()]*\)",
        "",
        h,
        flags=re.I,
    )
    h = re.sub(r"\s*;\s*voir\s+(?:aussi\s+)?[Ss]cans?\s*\\?#[0-9]{3}[^).;]*", "", h)
    h = re.sub(r"\s*\(voir\s+(?:aussi\s+)?[Ss]cans?\s*\\?#[0-9]{3}[^()]*\)", "", h, flags=re.I)

    def _s2f(m):
        s = int(m.group(1))
        if s == 1:
            return "Couverture"
        rv = "r" if (s % 2 == 0) else "v"
        return f"f\\textsuperscript{{o}}~{s // 2}~{rv}\\textsuperscript{{o}}"

    h = re.sub(r"[Ss]cans?\s*\\?#(\d{3})", _s2f, h)
    h = re.sub(r"\\?#(\d{3})", _s2f, h)

    # 4. Remove any "et non ..." or "quasi-certaine"
    h = re.sub(r"\s*\(et non\b[^()]*\)", "", h, flags=re.I)
    h = re.sub(r",?\s*et non\s+[^,.;)]+", "", h, flags=re.I)
    h = h.replace("de façon quasi-certaine ", "")
    h = h.replace("avec certitude ", "")
    h = h.replace("Identification topographique certaine : ", "")
    h = h.replace("Identification prosopographique certaine : ", "")

    # 5. Always call the diarist "Hippolyte Combes"
    h = h.replace("le diariste", "Hippolyte Combes").replace("Le diariste", "Hippolyte Combes")
    h = re.sub(r"\bHippolyte\b(?!\s+Combes|\s+Alric)", "Hippolyte Combes", h)
    h = re.sub(
        r"(?<!Hippolyte )(?<!François-Hippolyte )(?<!Augustin Hippolyte )(?<!Pierre )(?<!famille )(?<!Famille )(?<!Madame )(?<!Mme )(?<!archives )\bCombes\b(?!-Calmels)",
        "Hippolyte Combes",
        h,
    )
    h = h.replace("de Hippolyte Combes", "d'Hippolyte Combes").replace("De Hippolyte Combes", "D'Hippolyte Combes")
    h = h.replace("que Hippolyte Combes", "qu'Hippolyte Combes").replace("Que Hippolyte Combes", "Qu'Hippolyte Combes")
    h = re.sub(r"\(\s*\)", "", h)
    h = re.sub(r"\s+([,.;:!?])", r"\1", h)
    h = re.sub(r"\s{2,}", " ", h).strip()

    # 6. Condense overly long entries (> 470 chars) by keeping the most informative sentences
    if len(h) > 470:
        sentences = re.split(r"(?<=\.)\s+(?=[A-ZÀÉÈÊÎÔÛÇ\\])", h)
        if len(sentences) > 1:
            kept = []
            cur_len = 0
            for s in sentences:
                if cur_len == 0 or (cur_len + len(s) <= 470):
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

    for r in records:
        n = r["scan_num"]
        if n == 1:
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
                # Choisir la première occurrence et la plus proche avant n
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

        # Doublon photographique 091 / 093 : ajouter le renvoi explicite en tête
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

        # Si aucune entité n'a été détectée dans les lignes (très rare), relier au folio adjacent du même lieu
        if not items:
            prev_n = max(2, n - 1) if n > 2 else 3
            direction = "supra" if prev_n < n else "infra"
            items.append(f"\\textbf{{1}} (\\textit{{de eodem commorationis loco}}) cf. {direction} {folio_latin_ref(prev_n)}.")

        loci_by_scan[n] = " — ".join(items)

    return loci_by_scan


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
    base_by_num = {r["scan_num"]: r for r in baseline_records}
    hist_data = json.loads(HIST_JSON_PATH.read_text(encoding="utf-8"))
    raw_hist_by_num = {p["scan_num"]: p["changes"]["historique"] for p in hist_data["patches"]}

    # 1. Appliquer la correction des lignes du Folio 1 recto (Scan #002) et recalculer ses notes marginales
    for r in records:
        n = r["scan_num"]
        if n == 2:
            r["lines"] = list(SCAN_002_LINES)
            mnotes = {}
            for idx, line in enumerate(r["lines"], 1):
                _, note = clean_line_fn(line, idx)
                if note:
                    mnotes[str(idx)] = note
            mnotes["1"] = r"\textbf{1 Ma.} \textit{scil.} Mardi. \textbf{1 m.} \textit{abbr. pro} matin."
            mnotes["2"] = r"\textbf{2 Margte} \textit{scil.} Marguerite (Calmels)."
            mnotes["9"] = r"\textbf{9 lieutt} \textit{abbr. pro} lieutenant."
            mnotes["14"] = r"\textbf{14 off.} \textit{abbr. pro} officier(s). \textbf{14 R. Fusrs} \textit{angl.} Royal Fusiliers."
            mnotes["18"] = r"\textbf{18 1/2} \textit{scil.} demi / moitié. \textbf{18 s.} \textit{abbr. pro} soir."
            mnotes["19"] = r"\textbf{19 off.} \textit{abbr. pro} officier(s). \textbf{19 mess} \textit{angl. in ms.}"
            mnotes["20"] = r"\textbf{20 Mme} \textit{abbr. pro} Madame. \textbf{20 f} \textit{abbr. pro} franc."
            mnotes["21"] = r"\textbf{21 Varia} \textit{lat. in ms.} \textbf{21 c} \textit{abbr. pro} centimes."
            r["marginal_notes"] = {k: mnotes[k] for k in sorted(mnotes, key=lambda x: int(x))}
            if "apparat_entries" in r:
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

        # Nettoyer les notes marginales (supprimer toute glose française métatextuelle et les doubles points)
        new_mnotes = {}
        for k, v in r["marginal_notes"].items():
            if "apparat_entries" not in r and (n, k) in MARGINAL_NOTES_FIXES:
                v = MARGINAL_NOTES_FIXES[(n, k)]
            v = v.replace("Assoc..", "Assoc.")
            v = re.sub(r"\s*Le groupe «1pr» de l’ancienne transcription n’est pas visible\.", "", v)
            new_mnotes[k] = v
        r["marginal_notes"] = new_mnotes

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

    # 2. Construire l'apparat latin des Loci Paralleli (Registre 2)
    loci_map = build_loci_paralleli(records)
    for r in records:
        r["loci"] = loci_map[r["scan_num"]]

    return records
