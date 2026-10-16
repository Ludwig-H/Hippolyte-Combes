# -*- coding: utf-8 -*-
"""
Arbres généalogiques vectoriels (TikZ), cartes géographiques vectorielles (PDF)
pour les Prolégomènes et les sept chapitres, et génération des deux index finaux
(Index des noms de personnes et Index des noms de lieux) avec double référence
au folio du carnet (f° X r°/v°) et à la page du PDF (p. \\pageref{fol:N}).
"""

import re
import json
from pathlib import Path
from commentaires_et_loci import folio_fr_ref


# =============================================================================
# 1. TROIS ARBRES GÉNÉALOGIQUES ET PROSOPOGRAPHIQUES EN TIKZ (PROLÉGOMÈNES)
# =============================================================================

TIKZ_ARBRE_COMBES_ALRIC = r"""
\begin{center}
\resizebox{\textwidth}{!}{%
\begin{tikzpicture}[
  every node/.style={font=\fontsize{6.2pt}{7.2pt}\selectfont, align=center},
  box/.style={draw=black!80, line width=0.4pt, fill=white, rounded corners=1.2pt, inner sep=2.2pt},
  hero/.style={draw=bordeaux, line width=0.8pt, fill=white, rounded corners=1.2pt, inner sep=2.6pt},
  edge/.style={draw=black!75, line width=0.4pt}
]
\phantomsection\label{genealogie:combes}
% Grands-parents
\node[box, text width=32mm] (gp1) at (-48mm, 36mm) {\textbf{François Combes}\\(1789–1855)\\\textit{Maître menuisier-ébéniste à Millau}};
\node[box, text width=32mm] (gm1) at (-8mm, 36mm) {\textbf{Madeleine Fabre-Hugou}\\(1792–1863)\\\textit{Millau}};
\node[box, text width=28mm] (gp2) at (28mm, 36mm) {\textbf{Pierre Émile Alric}\\(1798–1854)\\\textit{Millau}};
\node[box, text width=26mm] (gm2) at (62mm, 36mm) {\textbf{Marie Bouquié}\\(1804–1863)\\\textit{Millau}};

% Parents
\node[box, text width=48mm] (pere) at (-28mm, 19.5mm) {\textbf{François Augustin Hippolyte Combes}\\(1825–1899)\\\textit{Avocat à Millau puis Toulouse\\(47, rue du Taur)}};
\node[box, text width=36mm] (mere) at (26mm, 19.5mm) {\textbf{Marie Anaïs Alric}\\(1838–1907)\\\textit{Mariés à Millau le 22 juill. 1864}};
\node[box, text width=25mm] (oncle_alric) at (62mm, 19.5mm) {\textbf{Pierre Émile Alric}\\(né en 1836)\\\textit{« Alric la sagesse »}};

\draw[edge] (gp1.east) -- coordinate[midway] (gpm1) node[above, font=\fontsize{5.2pt}{6.0pt}\selectfont]{×} (gm1.west);
\draw[edge] (gpm1) -- (pere.north);
\draw[edge] (gp2.east) -- coordinate[midway] (gpm2) node[above, font=\fontsize{5.2pt}{6.0pt}\selectfont]{×} (gm2.west);
\coordinate (alric_bus) at (45.5mm, 27.5mm);
\draw[edge] (gpm2) -- (alric_bus);
\draw[edge] (alric_bus) -| (mere.north);
\draw[edge] (alric_bus) -| (oncle_alric.north);
\draw[edge] (pere.east) -- coordinate[midway] (parents_mid) node[above, font=\fontsize{5.5pt}{6.5pt}\selectfont]{×} (mere.west);

% Fratrie Combes
\coordinate (frat_mid) at (2mm, 9.2mm);
\draw[edge] (parents_mid) -- (frat_mid);

\node[box, text width=27mm, anchor=north] (s1) at (-46mm, 6.2mm) {\textbf{Françoise Combes}\\(1871–1942)\\\textit{Sœur Marie de la Croix}\\Carmel de Périgueux};
\node[box, text width=27mm, anchor=north] (s2) at (-16mm, 6.2mm) {\textbf{Joséphine Combes}\\(1873 – oct. 1914)\\\textit{\dag~à Nogent-le-Rotrou}};
\node[box, text width=26mm, anchor=north] (s3) at (13mm, 6.2mm) {\textbf{Maria Combes}\\(1875 – 19 nov. 1903)\\\textit{Religieuse, \dag~à Carthage}};
\node[hero, text width=44mm, anchor=north] (hc) at (52mm, 6.2mm) {\textbf{Marie Lucien Hippolyte Combes}\\(Millau, 14 août 1876 –\\Saint-Chély-d'Apcher, 2 sept. 1970)\\\textit{Professeur d'anglais, interprète B.E.F.}};

\draw[edge] (frat_mid) -| (s1.north);
\draw[edge] (frat_mid) -| (s2.north);
\draw[edge] (frat_mid) -| (s3.north);
\draw[edge] (frat_mid) -| (hc.north);

% Mariage Hippolyte & Marguerite et enfants
\node[hero, text width=42mm] (mc) at (-18mm, -20.5mm) {\textbf{Marie Marguerite Calmels}\\(Millau, 15 avril 1892 – 19 mars 1974)\\\textit{« Marg\textsuperscript{te} / M\textsuperscript{te} / Gueïte »}};
\draw[edge, bordeaux, line width=0.6pt] (hc.south) -- ++(0,-5.0mm) -| coordinate[pos=0.25] (mariage_mid) node[pos=0.25, above, font=\fontsize{5.6pt}{6.5pt}\selectfont]{\textbf{Mariés à Millau le 25 oct. 1917}} (mc.north);

\node[box, text width=118mm] (enfants) at (15mm, -35.0mm) {\textbf{Sept enfants d'Hippolyte et Marguerite Combes :} \textbf{Valentine} (née en 1918, ép.~A.~Combès),\\\textbf{François} (1920–2021, agrégé de physique), \textbf{Joseph} (1921–2021, magistrat, père de \textbf{Pierre Combes}),\\\textbf{Jean} (1923–2012, normalien, prof. de mathématiques), \textbf{Marie-Thérèse} (née en 1925, ép.~M\textsuperscript{e}~P.~Vincens),\\\textbf{Pierre} (1928–2014, polytechnicien) et \textbf{Michel} (né en 1930)};
\draw[edge, bordeaux, line width=0.6pt] (mariage_mid) -- (mariage_mid |- enfants.north);
\end{tikzpicture}%
}
\par\vspace{0.8mm}{\scriptsize\textit{Arbre généalogique I.} La famille Combes–Alric (Millau, Toulouse, Nogent-le-Rotrou et Montauban).}
\end{center}
"""

TIKZ_ARBRE_CALMELS_ALLIANCES = r"""
\begin{center}
\resizebox{\textwidth}{!}{%
\begin{tikzpicture}[
  every node/.style={font=\fontsize{6.0pt}{7.0pt}\selectfont, align=center},
  box/.style={draw=black!80, line width=0.4pt, fill=white, rounded corners=1.2pt, inner sep=2.0pt},
  hero/.style={draw=bordeaux, line width=0.75pt, fill=white, rounded corners=1.2pt, inner sep=2.2pt},
  edge/.style={draw=black!75, line width=0.4pt}
]
% Ligne supérieure : Crouzet-Calmels (Toulouse), Calmels-Cartairade (Millau), Layrals-Cartairade (Millau)
\node[box, text width=38mm] (crouzet) at (-46mm, 25mm) {\textbf{Émile Crouzet} (1842–1921)\\\textit{Agent de change à Toulouse}\\× \textbf{Élisabeth Calmels}\\(\textit{« Oncle Émile \& Tante »})};
\node[box, text width=44mm] (calmels) at (0mm, 25mm) {\textbf{D\textsuperscript{r} Gabriel Calmels} (1852–1921)\\\textit{Médecin à Millau (10, rue A.-Guibert)}\\× \textbf{Valentine Cartairade}\\(1858–1943)};
\node[box, text width=38mm] (layrals) at (46mm, 25mm) {\textbf{M\textsuperscript{e} Charles Layrals}\\\textit{Notaire à Millau}\\× \textbf{Thérèse Cartairade}\\(\textit{« l'oncle \& tante Thérèse »})};

\draw[edge, dashed] (crouzet.east) -- (calmels.west);
\draw[edge, dashed] (calmels.east) -- (layrals.west);

% Rang intermédiaire gauche et droite : Cousin Jean Crouzet et cousins Layrals
\node[box, text width=34mm] (jean_cr) at (-46mm, 10.5mm) {\textbf{Abbé Jean Crouzet}\\\textit{« Jean », prêtre à Toulouse}\\(futur curé de la Dalbade)};
\draw[edge] (crouzet.south) -- (jean_cr.north);

\node[box, text width=34mm] (fils_layrals) at (46mm, 10.5mm) {\textbf{Louis Layrals} (\dag~1961, notaire)\\\textbf{Jean Layrals} (\dag~1947, magistrat)};
\draw[edge] (layrals.south) -- (fils_layrals.north);

% Enfants Calmels (tige centrale descendant dans le couloir médian jusqu'au-dessous du rang intermédiaire)
\coordinate (cal_mid) at (0mm, 2.0mm);
\draw[edge] (calmels.south) -- (cal_mid);

\node[box, text width=35mm, anchor=north] (mad) at (-46mm, -1.0mm) {\textbf{Madeleine Calmels}\\(1882–1961, \textit{« Mad\textsuperscript{ne} »})\\× \textbf{D\textsuperscript{r} Fernand Vincens}\\\textit{Enfants :}\\\textbf{Germaine} \& \textbf{Robert}};
\node[box, text width=28mm, anchor=north] (mimi) at (-10mm, -1.0mm) {\textbf{Anne-Marie Calmels}\\(1888–1975, \textit{« Mimi »})\\× \textbf{M\textsuperscript{e} Joseph Delcamps}\\\textit{Avoué à Millau}};
\node[box, text width=20mm, anchor=north] (pierre) at (18mm, -1.0mm) {\textbf{Pierre Calmels}\\\textit{Frère de}\\Marguerite\\(Millau)};
\node[hero, text width=33mm, anchor=north] (marg) at (49mm, -1.0mm) {\textbf{Marguerite Calmels}\\(1892–1974)\\\textit{« Marg\textsuperscript{te} / M\textsuperscript{te} »}\\× \textbf{Hippolyte Combes}};

\draw[edge] (cal_mid) -| (mad.north);
\draw[edge] (cal_mid) -| (mimi.north);
\draw[edge] (cal_mid) -| (pierre.north);
\draw[edge] (cal_mid) -| (marg.north);

% Branche Faure à Neuilly-sur-Seine
\node[box, text width=124mm] (faure) at (2mm, -21.5mm) {\textbf{Branche cousine de Neuilly-sur-Seine (16, rue d'Armenonville) :} \textbf{M\textsuperscript{me} Faure} et ses cinq enfants : \textbf{Marguerite}, \textbf{Germaine}, \textbf{Marcel Faure} (en permission en janv. 1917), \textbf{Henri Faure} (aspirant) et \textbf{André Faure} (candidat à Polytechnique)};
\end{tikzpicture}\phantomsection\label{genealogie:calmels}%
}
\par\vspace{0.8mm}{\scriptsize\textit{Arbre généalogique II.} La famille Calmels–Cartairade et ses alliances à Millau, Toulouse et Neuilly-sur-Seine.}
\end{center}
"""

TIKZ_ORGANIGRAMME_MILITAIRE = r"""
\begin{center}
\resizebox{\textwidth}{!}{%
\begin{tikzpicture}[
  every node/.style={font=\fontsize{5.9pt}{6.9pt}\selectfont, align=center},
  box/.style={draw=black!80, line width=0.4pt, fill=white, rounded corners=1.2pt, inner sep=2.0pt},
  hero/.style={draw=bordeaux, line width=0.75pt, fill=white, rounded corners=1.2pt, inner sep=2.4pt},
  edge/.style={draw=black!75, line width=0.4pt, ->, >=stealth}
]
\node[box, text width=56mm, anchor=south] (bef) at (-32mm, 19mm) {\textbf{18th (Eastern) Division \& Fifth Army (B.E.F.)}\\\textbf{Maj.-Gen. Sir Ivor Maxse} (cmdt la 18\textsuperscript{e} Division)\\\textbf{Lt.-Col. D.~C.~E. Grose} (cmdt le \textit{18th Divisional Train})};
\node[box, text width=56mm, anchor=south] (mmf) at (32mm, 19mm) {\textbf{Mission militaire française (B.E.F.)}\\\textbf{Lt Pizzi} (18\textsuperscript{e} Div.), \textbf{S/Lt Ferran} (liaison),\\\textbf{Cap. Huguet} (XIII\textsuperscript{e} Corps), \textbf{Cap. Bresson} (V\textsuperscript{e} Armée)};

\node[hero, text width=68mm] (hc) at (0mm, 10mm) {\textbf{Interprète Hippolyte Combes (matr. 911, classe 1896)}\\Détaché auprès de l'Armée britannique\\(4 mai 1915 – 11 nov. 1918)};

\draw[edge] (bef.south) -- ++(0,-2.2mm) -| ([xshift=-14mm]hc.north);
\draw[edge] (mmf.south) -- ++(0,-2.2mm) -| ([xshift=14mm]hc.north);

\coordinate (org_mid) at (0mm, 1.5mm);
\draw[draw=black!75, line width=0.4pt] (hc.south) -- (org_mid);

\node[box, text width=40mm, anchor=north] (asc) at (-43mm, -1.5mm) {\textbf{152nd \& 150th Cos. A.S.C.}\\\textit{(Juillet – Octobre 1916)}\\\textbf{Cap. E.~M. West}, \textbf{Cap. E.~M. Ford},\\\textbf{Lt Curtis} (\textit{C\textsuperscript{tis}}), \textbf{Cap. Panton},\\\textbf{Lt Walsh}, \textbf{Lt Michel},\\\textbf{Maj. Hughes}, \textbf{Lt Morris}};
\node[box, text width=41mm, anchor=north] (forage) at (0mm, -1.5mm) {\textbf{Foraging \& Purchase Board}\\\textit{(Acheux \& Hérissart, nov. 1916 – avr. 1917)}\\\textbf{Major Levy} (\textit{Purchase Board}),\\\textbf{Cap. Williams} (déc. 1916 – mars 1917),\\\textbf{2nd Lt Gilbert} (de Jersey, avr. 1917),\\\textbf{Lt Croughton},\\\textbf{Lt Godard}, \textbf{Lt Wentworth}};
\node[box, text width=38mm, anchor=north] (coll) at (43mm, -1.5mm) {\textbf{Collègues \& Universitaires}\\\textit{Interprètes :} \textbf{Maurin}, \textbf{Lépin},\\\textbf{Schumacher}, \textbf{Raucoule}, \textbf{Valet}\\(\textit{2nd Austr. Div.}), \textbf{Brammas}\\\textit{Lettres :} \textbf{E.~Zyromski} (Toulouse),\\\textbf{Fortuné \& L.-F. Flutre} (ENS)};

\draw[edge] (org_mid) -| (asc.north);
\draw[edge] (org_mid) -- (forage.north);
\draw[edge] (org_mid) -| (coll.north);
\end{tikzpicture}\phantomsection\label{genealogie:militaires}%
}
\par\vspace{0.8mm}{\scriptsize\textit{Organigramme III.} Cadre militaire britannique et français et réseau intellectuel d'Hippolyte Combes (1916–1917).}
\end{center}
"""


# =============================================================================
# 2. CARTES GÉOGRAPHIQUES VECTORIELLES ET LEURS ATTESTATIONS IMPRIMÉES
# =============================================================================

MAP_IDS = ("generale", "I", "II", "III", "IV", "V", "VI", "VII")
MAP_DIR = Path(__file__).resolve().parent / "cartographie" / "cartes"
MAP_MANIFEST = MAP_DIR / "manifest.json"


def map_asset_path(entry):
    """Resolve one canonical map PDF without accepting a different asset."""
    map_id = entry.get("id")
    if map_id not in MAP_IDS:
        raise ValueError(f"Identifiant de carte inconnu : {map_id!r}")
    value = entry.get("pdf")
    allowed = {f"{map_id}.pdf", f"cartographie/cartes/{map_id}.pdf"}
    if value not in allowed:
        raise ValueError(f"Carte {map_id}: chemin PDF attendu {map_id}.pdf, reçu {value!r}")
    return MAP_DIR / f"{map_id}.pdf"


def load_map_manifest():
    """Read labels from the generated map, never from abandoned TikZ sketches."""
    manifest = json.loads(MAP_MANIFEST.read_text(encoding="utf-8"))
    entries = manifest.get("maps") if isinstance(manifest, dict) else None
    if not isinstance(entries, list) or not all(isinstance(item, dict) for item in entries):
        raise ValueError("Le manifeste cartographique doit contenir une liste maps.")
    ids = [item.get("id") for item in entries]
    if len(ids) != len(MAP_IDS) or len(set(ids)) != len(ids) or set(ids) != set(MAP_IDS):
        raise ValueError(f"Huit cartes distinctes sont requises : {MAP_IDS!r}; reçu {ids!r}")
    by_id = {item["id"]: item for item in entries}
    for map_id in MAP_IDS:
        item = by_id[map_id]
        map_asset_path(item)
        if not isinstance(item.get("printed_text"), str) or not item["printed_text"].strip():
            raise ValueError(f"Carte {map_id}: printed_text doit reproduire le texte réellement imprimé.")
        if not isinstance(item.get("sha256"), str) or not re.fullmatch(r"[0-9a-f]{64}", item["sha256"]):
            raise ValueError(f"Carte {map_id}: empreinte SHA-256 absente ou mal formée.")
        if not isinstance(item.get("places"), list) or not item["places"]:
            raise ValueError(f"Carte {map_id}: liste places vide ou absente.")
    return [by_id[map_id] for map_id in MAP_IDS]


CARTE_GENERALE = r"""
\clearpage
\phantomsection\label{carte:generale}
\addcontentsline{toc}{section}{Carte générale : lieux de séjour et permissions}
\noindent\rule{\textwidth}{0.5pt}\par\vspace{1mm}
\noindent{\fontsize{9.5pt}{11pt}\selectfont\bfseries CARTE GÉNÉRALE}\par\vspace{1mm}
\noindent{\small\itshape Lieux de séjour et déplacements attestés, juillet 1916 – avril 1917}\par
\vfill
\noindent\includegraphics[width=\textwidth,height=176mm,keepaspectratio]{cartographie/cartes/generale.pdf}\par
\vfill
\noindent{\scriptsize Les cartes sélectionnent les lieux attestés par le carnet. Les liaisons représentent une succession d'étapes ; elles ne restituent pas le tracé historique des routes ou des voies ferrées. Les lectures et localisations réservées sont signalées sur les cartes.}\par
\clearpage
"""

CARTES_CHAPITRES = {
    chapter: (r"\phantomsection\label{carte:" + chapter + "}\n"
              + r"\noindent\includegraphics[width=\textwidth,height=128mm,keepaspectratio]{cartographie/cartes/"
              + chapter + ".pdf}")
    for chapter in MAP_IDS[1:]
}


# =============================================================================
# 3. INDEX DES NOMS DE PERSONNES (INDEX NOMINUM) & INDEX DES NOMS DE LIEUX (INDEX LOCORUM)
# =============================================================================

# Catalogue exhaustif des personnes nommées ou évoquées dans le carnet :
# (Entrée triée alphabétiquement, Notice d'identification, Regex dans lignes/titre/historique, Scans explicites additionnels)
INDEX_PERSONNES_CATALOG = [
    ("Alric, Marie Anaïs (1838–1907)", "mère d'Hippolyte Combes, épouse de François-Hippolyte Combes", r"\bAnaïs\s+Alric\b", [60, 92, 132, 143]),
    ("Auriol", "joaillier à Toulouse", r"\bAuriol\b", [139]),
    ("Backer, M\\textsuperscript{me}", "logeuse d'Hippolyte Combes à Lynde (Nord)", r"\bBacker\b", [2]),
    ("Barbry, Émile", "industriel blanchisseur sur la Lys près d'Armentières", r"\bBarbry\b", [17, 22, 23]),
    ("Benoît-Joseph Labre, saint (1748–1783)", "pèlerin vénéré en l'église de Saint-Pol-sur-Ternoise", r"\bLabre\b", [32]),
    ("Bertin (famille)", "hôtes au château de Martinsart (Somme)", r"\bBertin\b", [104]),
    ("Bienaimé, M\\textsuperscript{e}", "notaire à Toutencourt (Somme)", r"\bBienaimé\b", [178]),
    ("Bradfield, Lieutenant", "officier britannique de la 152\\textsuperscript{e} Compagnie A.S.C.", r"\bBradfield\b", [151]),
    ("Brammas", "collègue interprète militaire", r"\bBrammas\b", [45]),
    ("Bresson, Capitaine", "officier de la Mission militaire française auprès de la V\\textsuperscript{e} Armée à Toutencourt", r"\bBresson\b", [105]),
    ("Calmels, Anne-Marie dite « Mimi » (1888–1975)", "sœur de Marguerite Calmels, future épouse de M\\textsuperscript{e} Joseph Delcamps", r"\bMimi\b", [139, 141, 142, 143]),
    ('Calmels (famille)', 'famille de Marguerite Calmels, dont ses parents Gabriel Calmels et Valentine Cartairade', '\\bCalmels\\b', [54, 59, 60, 139, 141, 142, 143]),
    ("Calmels, Madeleine (1882–1961, \\textit{Mad\\textsuperscript{ne}})", "sœur aînée de Marguerite Calmels, épouse du D\\textsuperscript{r} Fernand Vincens", r"\b(?:Madeleine|Madne)\b", [133, 134, 135, 141, 143]),
    ("Calmels, Marie Marguerite (1892–1974, \\textit{Marg\\textsuperscript{te}}, \\textit{M\\textsuperscript{te}}, \\textit{Gueïte})", "fiancée puis épouse d'Hippolyte Combes", r"\b(?:Margte|Marg\.|Mte|Marguerite|Gueïte|ma\s+Femme)\b", [2, 6, 19, 54, 55, 56, 57, 58, 59, 60, 62, 64, 112, 114, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143]),
    ("Calmels, Pierre", "frère de Marguerite Calmels à Millau", r"\bPierre\b", [139, 141, 143]),
    ('Capron, M\\textsuperscript{me}', 'personne mentionnée à propos d’une location de battage à Beauquesne', '\\bCapron\\b', [115, 120]),
    ("Carluvant, M.", "tailleur et logeur d'Hippolyte Combes au n\\textsuperscript{o}~1, route de Léalvillers à Acheux", r"\bCarluvant\b", [94, 102, 118, 146, 147, 148]),
    ("Cliquennois, M\\textsuperscript{me}", "habitante de Steenwerck (Nord) chez qui Hippolyte Combes prend le café", r"\bCliquennois\b", [26]),
    ("Combes, François Augustin Hippolyte (1825–1899)", "avocat à Millau puis à Toulouse, père d'Hippolyte Combes", r"\bFrançois[\s-]+(?:Augustin\s+)?Hippolyte\s+Combes\b", [60, 143]),
    ("Combes, Françoise (1871–1942, \\textit{Sœur Marie de la Croix})", "sœur aînée d'Hippolyte Combes, carmélite à Périgueux", r"^\b$", []),
    ("Combes, Joséphine (1873–1914, \\textit{Joseph\\textsuperscript{e}})", "sœur d'Hippolyte Combes, décédée à Nogent-le-Rotrou en octobre 1914", r"\b(?:Josephe|Joséphine)\b", [57, 60]),
    ("Combes, Maria (1875–1903)", "sœur d'Hippolyte Combes, religieuse décédée à Carthage", r"^\b$", []),
    ('Combes, Marie Lucien Hippolyte (1876–1970)', "auteur du \\textit{Livre-Journal}, professeur d'anglais et interprète auprès de l'Armée britannique", '(?<!St\\s)\\bHippte\\b', [1, 135]),
    ("Connelly", "soldat britannique, ordonnance (\\textit{groom}) d'Hippolyte Combes à la 152\\textsuperscript{e} Compagnie A.S.C.", r"\bConnelly\b", [12, 39, 41, 45, 74]),
    ("Croughton, Lieutenant", "officier britannique du service automobile et des achats", r"\bCroughton\b", [109, 150]),
    ("Crouzet, Abbé Jean", "cousin germain de Marguerite Calmels, prêtre à Toulouse (futur curé de la Dalbade)", r"\bJean\b", [54, 58, 59, 60, 133, 139]),
    ('Crouzet (famille ; Émile, Élisabeth et Jean)', 'famille toulousaine apparentée aux Calmels', '\\b(?:Crouzet|Czt\\.?)\\b', [54, 55, 56, 58, 60, 62, 64, 132, 133, 137, 139]),
    ('Cuisinier, M\\textsuperscript{me}', 'hôtesse rencontrée notamment à Louvencourt et Acheux', '\\bCuisinier\\b', [112, 118, 126]),
    ("Curtis, Lieutenant (\\textit{C\\textsuperscript{tis}})", "officier britannique d'approvisionnement et de fourrage (18\\textsuperscript{e} Division puis Acheux)", r"\b(?:Curtis|Ctis)\b", [2, 6, 13, 14, 19, 21, 22, 23, 30, 37, 45, 74, 87, 89, 90, 91, 93, 96, 97, 101, 104, 105, 107]),
    ("Delille, M\\textsuperscript{me}", "habitante d'Acheux-en-Amiénois (Somme)", r"\bDelille\b", [147]),
    ("Delsol (dames)", "relations toulousaines visitées avec Marguerite Calmels", r"\bDelsol\b", [137]),
    ("Denis, Baptiste \\& famille", "famille d'Hérissart hôte d'Hippolyte Combes au printemps 1917", r"\bDenis\b", [178, 180, 182, 183, 184]),
    ("Donze, M\\textsuperscript{me}", "logeuse d'Hippolyte Combes à Lynde (Nord)", r"\bDonze\b", [5]),
    ("Dubois, D\\textsuperscript{r}", "médecin rencontré par Hippolyte Combes à Fréchencourt (Somme)", r"\bDr\s+Dubois\b", [161]),
    ("Dubois, Paul", "maire de Montigny-sur-l'Hallue (Somme)", r"\bDubois\s+Paul\b", [119]),
    ("Duchâteau, Victor \\& famille", "famille logeant Hippolyte Combes près du camp des briqueteries à Albert", r"\bDuchâteau\b", [80, 82, 87, 91, 93]),
    ("Dupuich, M.", "interprète militaire français détaché auprès du XIII\\textsuperscript{e} Corps britannique à Candas", r"\bDupuich\b", [167]),
    ('Faure, M\\textsuperscript{me} \\& ses enfants (Marguerite, Germaine, Marcel, Henri, André)', 'famille visitée à Neuilly-sur-Seine ; parenté avec les Calmels rapprochée du dossier familial', '\\b(?:Faure|Marcel|André)\\b', [52, 130, 131]),
    ("Flutre, Fortuné \\& Louis-Fernand (1892–1978)", "instituteur du Mesnil-Martinsart et son fils élève de l'École normale supérieure", r"\bFlutre\b", [168]),
    ("Ford, Capitaine E.~M.", "officier britannique du \\textit{18th Divisional Train, A.S.C.}, décoré de la \\textit{Military Cross}", r"\bFord\b", [50, 76]),
    ("Gilbert, Second Lieutenant", "sous-lieutenant britannique originaire de Jersey, poète, attaché au \\textit{Purchase Board} à Hérissart", r"\bGilbert\b", [166, 179, 181, 185, 186]),
    ("Godard, Lieutenant", "jeune officier britannique du \\textit{Purchase Board} à Toutencourt et Hérissart", r"\bGodard\b", [166]),
    ("Grauger, maréchal des logis", "sous-officier français rencontré à Toutencourt", r"\bGrauger\b", [163]),
    ("Grose, Lieutenant-Colonel Daniel Charles Evans", "commandant (\\textit{Officer Commanding}) le \\textit{18th Divisional Train, A.S.C.}", r"\bGrose\b", [90]),
    ("Guérin, Maurice de (1810–1839)", "poète tarnais étudié dans le cours public d'Ernest Zyromski à Toulouse", r"\bGuérin\b", [135]),
    ("Guibet, M.", "habitant de Raincheval (Somme)", r"\bGuibet\b", [115, 121]),
    ("Guilhem, M\\textsuperscript{lle}", "relation toulousaine mentionnée lors de la permission d'automne 1916", r"\bGuilhem\b", [61]),
    ("Guiraud", "tailleur à Toulouse", r"\bGuiraud\b", [61]),
    ("Hancock", "militaire britannique mentionné lors de la marche vers Bailleul", r"\bHancock\b", [7]),
    ("Henriette", "amie de Marguerite Calmels à Toulouse", r"\bHenriette\b", [137, 138]),
    ("Hippolyte, saint", "martyr chrétien dont le reliquaire est conservé en l'église Saint-Jean-Baptiste de Steenwerck", r"\bSt\s+Hippte\b", [26]),
    ("Houtteman (lecture réservée), M. \\& M\\textsuperscript{me}", "exploitants agricoles belges de la ferme de Belle-Église à Arquèves (Somme)", r"\b(?:Houthouan|Houtteman)\b", [95, 108, 171]),
    ("Hughes, Major", "officier supérieur britannique au \\textit{18th Divisional Train}", r"\bHughes\b", [90, 96]),
    ("Huguet, Capitaine (\\textit{Cap.~H.})", "officier de la Mission militaire française auprès du XIII\\textsuperscript{e} Corps à Acheux", r"\b(?:Huguet|Cap\.\s*H\.)\b", [94, 105, 123]),
    ("Imbert", "opticien à Paris", r"\bImbert\b", [116, 121, 122, 131]),
    ("Jimmie", "conducteur britannique de l'automobile Vauxhall du service des achats", r"\bJimmie\b", [167]),
    ("Labarthe, M\\textsuperscript{me} de", "propriétaire et voisine d'Hippolyte Combes à Toulouse", r"\bLabarthe\b", [60, 61, 135, 137, 138]),
    ("Labit, Antoine (1832–1912) \\& Georges (1862–1899)", "fondateur du grand magasin toulousain \\textit{La Maison Universelle} et son fils", r"\bLabit\b", [134]),
    ("Layrals, M\\textsuperscript{e} Charles \\& Thérèse Cartairade (\\textit{Layral})", "notaire à Millau et son épouse, oncle et tante maternels de Marguerite Calmels", r"\bLayral\b", [142]),
    ("Lefèvre, M.", "interlocuteur d'Hippolyte Combes à Toutencourt (Somme)", r"\bLefèvre\b", [154]),
    ("Leonard, Capitaine", "officier britannique au mess d'Hérissart", r"\bLeonard\b", [157]),
    ("Lépin (ou \\textit{Liepin}, \\textit{Lupin})", "adjudant interprète à la Mission française de la 18\\textsuperscript{e} Division", r"\b(?:Lupin|Lépin|Liepin)\b", [23, 85, 90]),
    ("Lersay, M. de", "chirurgien-dentiste à Toulouse", r"\bLersay\b", [138, 140]),
    ("Levy, Major", "officier supérieur britannique dirigeant le service des achats (\\textit{Purchase Board}) dans la Somme", r"\bLevy\b", [91, 93, 110, 116, 166]),
    ("Louis XI (1423–1483)", "roi de France, associé au chêne historique du beffroi de Lucheux (édit de 1464)", r"\bLouis\s+XI\b", [41]),
    ("Lovet, Capitaine", "officier britannique revu au \\textit{refilling point} près d'Albert", r"\bLovet\b", [151]),
    ("Maeterlinck, Maurice (1862–1949)", "écrivain belge, auteur du recueil \\textit{Les Débris de la guerre} (1916) acquis par Hippolyte Combes", r"\bMaeterlinck\b", [53]),
    ("Maria", "domestique au service de la famille Crouzet à Toulouse", r"\bMaria\b", [64]),
    ("Marie", "personne recevant des étrennes à Toulouse", r"\bMarie\b(?!\s+de\s+la\s+Croix)", [140]),
    ("Martin, Alexis", "auteur du guide illustré \\textit{Une visite à Amiens} rapporté à Hippolyte Combes", r"\bAlexis\s+Martin\b", [182]),
    ("Maurin", "collègue interprète militaire dans la vallée de la Lys", r"\bMaurin\b", [13, 14, 19, 21, 24, 26]),
    ("Maxse, Major-General Sir Ivor (1862–1958)", "commandant la 18\\textsuperscript{e} Division britannique (\\textit{18th Eastern Division}) de 1914 à janvier 1917", r"\bMaxse\b", [16]),
    ("Michel, Lieutenant", "officier britannique de cantonnement (\\textit{billeting officer}) à Lynde", r"\bLt\s+Michel\b", [3]),
    ("Mignot, M\\textsuperscript{me} \\& Louise", "tisserandes à domicile visitées à Hérissart (Somme)", r"\bMignot\b", [183]),
    ("Monin", "collègue interprète retrouvé de passage à Hérissart", r"\bMonin\b", [173]),
    ("Morris, Lieutenant", "officier britannique ami d'Hippolyte Combes à la 150\\textsuperscript{e} Compagnie A.S.C.", r"\bMorris\b", [120, 121, 122]),
    ("Mortreux (famille)", "famille d'agriculteurs de Varennes (Somme) amie d'Hippolyte Combes", r"\bMortreux\b", [97, 184]),
    ("Moulard (ferme)", "exploitation agricole à Septenville (Rubempré, Somme)", r"\bMoulard\b", [120]),
    ("Newton", "militaire britannique mentionné à Forceville", r"\bNewton\b", [49]),
    ("Panton, Capitaine", "officier britannique de la 152\\textsuperscript{e} Compagnie A.S.C.", r"\bPanton\b", [47, 68, 73, 74, 90]),
    ("Pfister", "horloger-bijoutier à Toulouse (10, rue Gambetta / place Esquirol)", r"\bPfister\b", [56, 133, 134, 135, 137, 138]),
    ("Pizzi, Lieutenant", "officier interprète chef du détachement français auprès de la 18\\textsuperscript{e} Division britannique", r"\bPizzi\b", [48, 85, 90, 92]),
    ("Raucoule", "collègue interprète militaire originaire du Midi", r"\bRaucoule\b", [88, 90, 163]),
    ("Renard, M.", "fournisseur de paille et de fourrage à Rubempré (Somme)", r"\bRenard\b", [124]),
    ('Romert, M.', 'personne visitée à Auxi-le-Château, décrite comme riche et aimable', '\\bRomert\\b', [152]),
    ("Schumacher", "adjudant interprète au bureau de la Mission française de la 18\\textsuperscript{e} Division", r"\bSchumacher\b", [23, 83]),
    ("Serpin", "sous-officier interprète à la Mission française", r"\bSerpin\b", [90]),
    ("Sorgues, M.", "directeur d'école à Varennes-en-Croix (Somme)", r"\bSorgues\b", [97]),
    ("Spagnol, M\\textsuperscript{me}", "personne mentionnée au sujet d’un panier de fleurs ; profession non établie", r"\bSpagnol\b", [134, 136, 158]),
    ("Testet, Henri", "pâtissier aux allées Lafayette à Toulouse", r"\bTestet\b", [136]),
    ("Trefcon, Capitaine", "officier français rencontré rue Sire-Firmin-Leroux à Amiens", r"\bTrefcon\b", [119]),
    ("Valet", "interprète militaire français rattaché à la 2\\textsuperscript{e} Division australienne à Hérissart", r"\bValet\b", [164, 166]),
    ("Vauchel, M\\textsuperscript{me}", "exploitante agricole à Marquay (Pas-de-Calais)", r"\bVauchel\b", [37]),
    ("Vincens, D\\textsuperscript{r} Fernand, Germaine \\& Robert", "beau-frère, nièce et neveu de Marguerite Calmels à Millau", r"\b(?:Vincens|Fernand|Robert)\b", [56, 141, 143]),
    ("Walsh, Lieutenant", "officier britannique du \\textit{18th Divisional Train, A.S.C.}", r"\bWalsh\b", [74, 99, 103, 106, 120]),
    ("Wentworth, Lieutenant", "officier britannique du \\textit{Purchase Board} à Hérissart", r"\bWentworth\b", [166, 169, 170, 177]),
    ("West, Capitaine E.~M.", "commandant la 152\\textsuperscript{e} Compagnie A.S.C., décoré de la \\textit{Military Cross}", r"\bWest\b", [39, 42, 48, 74]),
    ("Williams, Capitaine (\\textit{Cap.~W.}, \\textit{W\\textsuperscript{ms}})", "jeune officier britannique (\\textit{Foraging Officer}) à Acheux puis Hérissart de décembre 1916 à mars 1917", r"\b(?:Williams|Wms|Cap\.\s*W\.|Capt\.\s*W\.)\b", [105, 106, 107, 108, 109, 111, 114, 115, 117, 126, 147, 148, 157, 160, 163, 164, 165]),
    ("Zyromski, Ernest (1862–1933)", "professeur de littérature française à la Faculté des lettres de Toulouse, auteur de \\textit{L'Orgueil humain}", r"\bZyromski\b", [53, 135]),
]


# Catalogue exhaustif des noms de lieux (Index locorum) :
INDEX_LIEUX_CATALOG = [
    ("Abbeville (Somme)", "chef-lieu d'arrondissement de la Somme", r"\bAbbeville\b", [181]),
    ("Acheux-en-Amiénois (Somme)", "chef-lieu de canton de la Somme, gare (\\textit{railhead} d'Acheux-Varennes), château et cantonnement d'Hippolyte Combes (nov. 1916 – févr. 1917)", r"\bAcheux\b", [43, 45, 50, 87, 90, 91, 92, 93, 94, 102, 105, 112, 116, 128, 147, 168]),
    ("Achiet-le-Petit (Pas-de-Calais)", "village au nord-est de Miraumont repris lors du repli allemand de mars 1917", r"\bAchiet\b", [170]),
    ("Albert (Somme)", "ville de la vallée de l'Ancre, basilique Notre-Dame de Brebières (\\textit{Vierge penchée}) et bivouac des briqueteries (\\textit{Brickfields})", r"\bAlbert\b", [78, 80, 81, 82, 83, 84, 85, 91, 93, 96, 151, 164, 171, 181]),
    ("Amiens (Somme)", "préfecture de la Somme, cathédrale Notre-Dame et nœud ferroviaire des permissions", r"\bAmiens\b", [51, 65, 119, 128, 129, 147, 182]),
    ("Ancre (vallée de l')", "affluent de la Somme traversant Miraumont, Albert, Aveluy, Buire, Ribemont et Heilly", r"\bAncre\b", [99, 105, 153, 181]),
    ("Antibes (Alpes-Maritimes)", "ville de la Côte d'Azur évoquée avec l'interprète Maurin", r"\bAntibes\b", [24]),
    ("Armentières (Nord)", "ville industrielle linière sur la Lys, bombardée par l'artillerie allemande", r"\bArmentières\b", [17, 19, 21, 22]),
    ("Arquèves \\& ferme de Belle-Église (Somme)", "commune du canton d'Acheux et ancienne commanderie exploitée par la famille dont le nom est proposé Houtteman", r"\b(?:Arquèves|Belle[- ]Église)\b", [95, 108, 110, 111, 113, 125, 171, 179]),
    ("Arras (Pas-de-Calais)", "préfecture du Pas-de-Calais et secteur de l'offensive britannique d'avril 1917 (bataille de la Scarpe)", r"\bArras\b", [32, 118, 178, 182]),
    ("Authie (Somme)", "village de la haute vallée de l'Authie au nord d'Acheux", r"\bAuthie\b", [100, 102, 107, 108, 109, 112, 118, 121, 122, 154]),
    ("Auxi-le-Château (Pas-de-Calais)", "chef-lieu de canton sur l'Authie visité en tournée", r"\bAuxi-le-Château\b", [124, 152, 158]),
    ("Aveluy (Somme)", "village et bois au nord d'Albert sur l'Ancre", r"\bAveluy\b", [82, 150, 151]),
    ("Bac-Saint-Maur (Pas-de-Calais)", "écart de Sailly-sur-la-Lys et écluse sur la Lys (\\textit{refilling point})", r"\bBac-S(?:ain)?t-Maur\b", [13, 14, 15, 16, 18, 19, 20, 24]),
    ("Bailleul (Nord)", "ville de Flandre flamingante au pied des Monts, Grand-Place, beffroi et gare d'embarquement", r"\bBailleul\b(?!-aux-Cornailles)", [7, 8, 9, 10, 12, 27, 28]),
    ("Bailleul-aux-Cornailles (Pas-de-Calais)", "village du Ternois voisin de Marquay", r"\bBailleul-aux-Cornailles\b", [29, 31, 37]),
    ("Barlette (Somme)", "hameau de la commune de Ribeaucourt où cantonne la 152\\textsuperscript{e} Compagnie A.S.C.", r"\bBarlette\b", [66, 67, 68, 69, 70, 71, 72, 73, 74]),
    ("Beaucourt-sur-l'Hallue (Somme)", "village et château au sud d'Hérissart", r"\bBeaucourt\b(?!\s*s/\s*Ancre)(?!-sur-l'Ancre)", [123, 155, 183]),
    ("Beaudricourt \\& hameau d'Oppy (Pas-de-Calais)", "commune et hameau du canton d'Avesnes-le-Comte, étape du 9–10 septembre 1916", r"\b(?:Beaudricourt|Oppy)\b", [39, 40, 41]),
    ("Beaumont-Hamel \\& Beaumont-sur-Ancre (Somme)", "village et positions fortifiées du front de l'Ancre", r"\bBeaumont\b", [98, 99, 167]),
    ("Beauquesne (Somme)", "bourg du canton de Doullens", r"\bBeauquesne\b", [75, 98, 112, 113, 115, 117, 120, 122, 123, 178]),
    ("Beauval (Somme)", "bourg entre Doullens et Amiens, étape des 15–16 octobre 1916", r"\bBeauval\b", [74, 75, 76]),
    ("Bédarieux (Hérault)", "gare de bifurcation vers Millau sur la ligne des Causses", r"\bBédarieux\b", [139, 140]),
    ("Bertrancourt (Somme)", "commune à l'est d'Acheux-en-Amiénois", r"\bBertrancourt\b", [92, 105, 121, 168]),
    ("Béziers (Hérault)", "ville du Languedoc visitée avec Marguerite Calmels (cathédrale Saint-Nazaire et terrasse sur l'Orb)", r"\bBéziers\b", [139, 140, 143]),
    ("Bouzincourt (Somme)", "village à l'ouest d'Albert où bivouaque la compagnie en octobre 1916", r"\bBouzincourt\b", [77, 78, 79, 80, 101, 124]),
    ("Bresle (Somme)", "village entre Warloy-Baillon et Albert", r"\bBresle\b", [181]),
    ("Brioude \\& Arvant (Haute-Loire)", "gares de la ligne des Cévennes lors du retour de Millau en février 1917", r"\b(?:Brioude|Arvant)\b", [144, 145]),
    ("Buire-sur-l'Ancre (Somme)", "village de la vallée de l'Ancre en aval d'Albert", r"\bBuire\b", [105, 181, 182]),
    ("Bus-lès-Artois (Somme)", "commune au nord-est d'Acheux-en-Amiénois", r"\bBus(?:-lès-Artois)?\b", [92, 100, 154]),
    ("Cambrai (Nord)", "ville du Nord évoquée comme destination d'offensive au printemps 1917", r"\bCambrai\b", [185]),
    ("Canaples (Somme)", "commune et gare de ravitaillement (\\textit{railhead}) au nord d'Amiens", r"\bCanaples\b", [66]),
    ("Candas (Somme)", "commune entre Doullens et Rubempré", r"\bCandas\b", [167]),
    ("Carcassonne (Aude)", "escale ferroviaire où Hippolyte Combes et Marguerite Calmels embrassent l'abbé Jean Crouzet", r"\bCarcassonne\b", [139]),
    ("Clermont-Ferrand (Puy-de-Dôme)", "étape ferroviaire du retour de Millau le 6 février 1917", r"\bClermont\b", [144, 145]),
    ("Coisy (Somme)", "village au sud-ouest de Rubempré", r"\bCoisy\b", [95]),
    ("Contay (Somme)", "village et château de la vallée de l'Hallue entre Toutencourt et Warloy", r"\bContay\b", [98, 101, 107, 159, 161, 167, 169, 171, 176, 177, 178, 181, 182, 184, 185]),
    ("Creil (Oise)", "nœud ferroviaire entre Amiens et Paris", r"\bCreil\b", [51, 65]),
    ("Domqueur (Somme)", "village du Ponthieu voisin de Ribeaucourt", r"\bDomqueur\b", [70]),
    ("Doullens (Somme)", "sous-préfecture de la Somme, église Notre-Dame, cantine militaire et commerces", r"\bDoullens\b", [51, 65, 66, 67, 98, 115, 123, 124, 128, 146, 152, 158, 163, 179]),
    ("Englebelmer (Somme)", "village du front de l'Ancre évacué par ses habitants", r"\bEnglebelmer\b", [101, 108, 110]),
    ("Erquinghem-Lys (Nord)", "commune de la vallée de la Lys en amont d'Armentières", r"\bErquinghem\b", [17, 22, 23, 24]),
    ("Estaires (Nord)", "ville sur la Lys (église Saint-Vaast et hôtel de ville Renaissance détruits en 1918)", r"\bEstaires\b", [16, 25]),
    ("Flandre", "plaine flamande et Flandre intérieure traversées en juillet–août 1916", r"\bFlandre\b", [2, 52]),
    ("Fleurbaix (Pas-de-Calais)", "village du front au sud d'Armentières", r"\bFleurbaix\b", [21, 22]),
    ("Forceville (Somme)", "village au sud-est d'Acheux-en-Amiénois, cantonnement de septembre 1916", r"\bForceville\b", [45, 48, 49, 50, 96]),
    ("Franvillers (Somme)", "commune sur la route d'Albert à Amiens", r"\bFranvillers\b", [105, 117]),
    ("Fréchencourt (Somme)", "village de la vallée de l'Hallue", r"\bFréchencourt\b", [157, 161, 162, 178, 180]),
    ("Harponville (Somme)", "village entre Toutencourt et Warloy-Baillon", r"\bHarponville\b", [110, 178, 184]),
    ("Hazebrouck (Nord)", "sous-préfecture du Nord, église Saint-Éloi et nœud ferroviaire", r"\bHazebrouck\b", [4, 5, 8, 16, 27]),
    ("Hébuterne (Pas-de-Calais)", "secteur du front au nord d'Acheux et de Serre", r"\bHébuterne\b", [107, 116]),
    ("Hédauville (Somme)", "village entre Forceville et Warloy-Baillon (bivouac de la 150\\textsuperscript{e} Compagnie A.S.C.)", r"\bHédauville\b", [45, 77, 108, 121]),
    ("Heilly (Somme)", "village de la vallée de l'Ancre où Hippolyte Combes avait cantonné durant l'hiver 1915–1916", r"\bHeilly\b", [105]),
    ("Hénencourt (Somme)", "village et château entre Warloy-Baillon et Albert", r"\bHénencourt\b", [181, 186]),
    ("Hérissart (Somme)", "commune du canton d'Acheux, siège du \\textit{Purchase Board} et résidence d'Hippolyte Combes de février à avril 1917 (logements n\\textsuperscript{os}~104, 220 et 216)", r"\bHérissart\b", [95, 104, 148, 149, 150, 152, 155, 157, 160, 164, 166, 168, 170, 172, 178, 186]),
    ("Jersey (île anglo-normande)", "patrie du sous-lieutenant poète Gilbert", r"\bJersey\b", [179]),
    ("La Croix-du-Bac (Steenwerck, Nord)", "hameau de la vallée de la Lys, église Notre-Dame-des-Sept-Douleurs et cantonnement d'août 1916", r"\bCroix-du-Bac\b", [10, 12, 13, 14]),
    ("Lardenne \\& Purpan-Ancely (Toulouse, Haute-Garonne)", "faubourg occidental de Toulouse et ruines de l'amphithéâtre gallo-romain", r"\bLardenne\b", [58, 136, 137]),
    ("Laviéville (Somme)", "village entre Warloy-Baillon et Albert", r"\bLavieville\b|\bLaviéville\b", [181, 186]),
    ("Le Mesnil-Martinsart (Somme)", "commune du canton d'Albert où enseignent M. et M\\textsuperscript{me} Fortuné Flutre", r"\bMesnil\b", [104, 168]),
    ("Le Quesnoy (ferme, Somme)", "écart agricole entre Raincheval et Puchevillers", r"\bQuesnoy\b", [111, 112, 113, 115, 116, 118]),
    ("Léalvillers (Somme)", "village immédiatement voisin d'Acheux-en-Amiénois", r"\bLéalvillers\b", [48, 94, 95, 96, 97, 101, 102, 112, 116, 177]),
    ("Ligny-Saint-Flochel (Pas-de-Calais)", "village du Ternois à l'église gothique classée (XV\\textsuperscript{e}–XVI\\textsuperscript{e}~s.)", r"\bLigny\b", [33, 39]),
    ("Louvencourt (Somme)", "commune au nord d'Acheux-en-Amiénois", r"\bLouvencourt\b", [92, 99, 106, 107, 112, 114, 116, 118, 121, 122, 123, 126, 146]),
    ("Lucheux (Somme)", "bourg de la vallée de la Grouches (ruines du château des comtes de Saint-Pol et beffroi au chêne de Louis~XI)", r"\bLucheux\b", [41]),
    ("Lynde (Nord)", "village de Flandre intérieure entre Renescure et Hazebrouck, premier cantonnement du carnet", r"\bLynde\b", [2, 3, 4, 5]),
    ("Lys (vallée de la)", "rivière franco-belge canalisée entre Aire, Estaires, Sailly, Bac-Saint-Maur et Armentières", r"\bLys\b", [13, 15, 16, 17, 18, 19, 22, 23, 24, 25]),
    ("Marquay (Pas-de-Calais)", "commune du Ternois, cantonnement de la compagnie du 25 août au 9 septembre 1916", r"\bMarquay\b", [28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39]),
    ("Martinsart (Somme)", "hameau et château de la commune du Mesnil-Martinsart près d'Albert", r"\bMartinsart\b", [104, 105, 117, 150, 159, 168]),
    ("Millau (Aveyron)", "ville natale d'Hippolyte Combes et de Marguerite Calmels (10, rue Alfred-Guibert ; rue des Barris ; cimetière)", r"\bMillau\b", [1, 138, 139, 140, 141, 142, 143, 144]),
    ("Miraumont (Somme)", "village aux sources de l'Ancre évacué par l'armée allemande en février–mars 1917", r"\bMiraumont\b", [122, 170]),
    ("Mirvaux (Somme)", "village voisin de Pierregot et Rubempré", r"\bMirvaux\b", [159, 169, 171, 183, 185]),
    ("Molliens-au-Bois (Somme)", "commune du canton de Villers-Bocage", r"\bMolliens\b", [158, 167, 171, 174, 182]),
    ("Mont-Noir (Nord)", "colline des Monts des Flandres au nord de Saint-Jans-Cappel", r"\bMont[- ]Noir\b", [6]),
    ("Montauban (Tarn-et-Garonne)", "ville traversée en train lors des permissions et futur poste d'Hippolyte Combes au lycée Ingres", r"\bMontauban\b", [54]),
    ("Montigny-sur-l'Hallue (Somme)", "village voisin de Beaucourt-sur-l'Hallue", r"\bMontigny\b", [119, 123, 158, 161, 162, 183]),
    ("Neuilly-sur-Seine (Hauts-de-Seine)", "résidence de la famille Faure (16, rue d'Armenonville) visitée lors des permissions", r"\bNeuilly\b", [52, 130, 131]),
    ("Nice (Alpes-Maritimes)", "ville d'où provient le panier de fleurs commandé chez M\\textsuperscript{me} Spagnol", r"\bNice\b", [134, 136, 158]),
    ("Nogent-le-Rotrou (Eure-et-Loir)", "ville du Perche où Hippolyte Combes enseignait au collège communal (17, rue Saint-Hilaire)", r"\bNogent\b", [23, 24]),
    ("Ostreville (Pas-de-Calais)", "village du Ternois entre Marquay et Saint-Pol", r"\bOstreville\b", [32]),
    ("Paris", "capitale traversée aux permissions de septembre–octobre 1916 et janvier–février 1917 (gare du Nord, gare d'Orsay, boulevard Saint-Germain, boulevard Saint-Michel, rue Saint-Jacques, Panthéon, église Saint-Vincent-de-Paul)", r"\b(?:Paris|St-Germain|St-Jacques|Panthéon|St-Vincent-de-Paul|Gare\s+du\s+Nord|Gare\s+d'Orsay)\b", [1, 51, 52, 53, 63, 64, 65, 99, 116, 122, 130, 131, 132, 145, 146, 148]),
    ("Pech-David \\& Pouvourville (Toulouse, Haute-Garonne)", "coteaux dominant le sud de Toulouse et la Garonne", r"\b(?:Pouvourville|Pech\s+David)\b", [55]),
    ("Pierregot (Somme)", "village à l'ouest de Rubempré", r"\bPierregot\b", [104, 157, 169, 171, 174, 175, 178, 180, 182, 183, 184, 185, 186]),
    ("Puchevillers (Somme)", "commune entre Raincheval et Hérissart, centre d'hôpitaux d'évacuation britanniques (\\textit{Casualty Clearing Stations})", r"\bPuchevillers\b", [75, 104, 110, 112, 125, 147, 154, 155, 158, 162, 166, 167, 168, 169, 170, 171, 172, 173, 174, 183, 184, 186]),
    ("Raincheval (Somme)", "commune et château au nord d'Hérissart, cantonnement de septembre 1916 et siège de l'\\textit{Army Purchase Board}", r"\bRaincheval\b", [41, 42, 43, 44, 45, 46, 47, 48, 91, 93, 97, 98, 99, 104, 107, 108, 111, 113, 115, 116, 117, 118, 121, 122, 123, 125, 147, 155, 166, 167, 175]),
    ("Ramecourt (Pas-de-Calais)", "commune et plateau à l'ouest de Saint-Pol-sur-Ternoise", r"\bRamecourt\b", [32]),
    ("Renescure (Nord)", "bourg de Flandre intérieure (château de Zuthove, château dit de Philippe de Comines et église Notre-Dame-de-l'Assomption)", r"\bRenescure\b", [4]),
    ("Ribeaucourt (Somme)", "commune et château du Ponthieu où la compagnie prend son repos du 6 au 15 octobre 1916", r"\bRibeaucourt\b", [67, 68, 69, 70, 71, 72, 73, 74, 75]),
    ("Ribemont-sur-Ancre (Somme)", "village de la vallée de l'Ancre en aval d'Albert", r"\bRibemont\b", [105, 153, 169, 181]),
    ("Roëllecourt (Pas-de-Calais)", "village du Ternois entre Saint-Pol et Marquay", r"\b(?:Roellecourt|Roëllecourt)\b", [35]),
    ("Roumanie", "royaume entré en guerre aux côtés des Alliés le 27 août 1916", r"\bRoumanie\b", [30, 53]),
    ("Rubempré \\& Septenville (Somme)", "chef-lieu de commune et hameau voisins d'Hérissart", r"\b(?:Rubempré|Septenville)\b", [95, 104, 106, 112, 120, 122, 124, 149, 161, 162, 172, 173, 174, 175, 177, 178, 180, 181, 184]),
    ("Sailly-sur-la-Lys (Pas-de-Calais)", "commune de la vallée de la Lys (pont, écluse et ruines de l'église Saint-Vaast)", r"\bSailly\b", [16]),
    ("Saint-Chély-d'Apcher (Lozère)", "ville de Lozère traversée sur la ligne des Causses (et où Hippolyte Combes décédera à l'Hôtel du Centre le 2 septembre 1970)", r"\b(?:St|Saint)-Chély\b", [1, 145]),
    ("Saint-Flour (Cantal)", "sous-préfecture du Cantal traversée sous la neige le 6 février 1917", r"\bSt-Flour\b|\bSaint-Flour\b", [143, 144, 145]),
    ("Saint-Jans-Cappel (Nord)", "village au pied du Mont-Noir où cantonne Hippolyte Combes du 28 juillet au 5 août 1916", r"\b(?:St-Jans-Cappel|Saint-Jans-Cappel)\b", [5, 6, 7, 8, 10, 11, 12]),
    ("Saint-Léger-lès-Authie (Somme)", "village de la vallée de l'Authie", r"\bSt-Léger\b", [108, 109, 112, 121, 122, 123]),
    ("Saint-Michel-sur-Ternoise (Pas-de-Calais)", "village et église ancienne à l'est de Saint-Pol-sur-Ternoise", r"\bSt[. -]+Michel[- ](?:s[- ]|sur[- ])Ternoise\b", [32, 37]),
    ("Saint-Pol-sur-Ternoise (Pas-de-Calais)", "sous-préfecture du Pas-de-Calais, gare de débarquement et église des Carmes (1697)", r"\b(?:St-Pol|Saint-Pol)\b", [27, 28, 32, 34, 36, 37]),
    ("Senlis-le-Sec (Somme)", "village entre Warloy-Baillon et Bouzincourt", r"\bSenlis\b", [75, 77, 87, 96, 110, 112, 117, 124, 151, 159, 169, 171, 181]),
    ("Sercus (Nord)", "village de Flandre intérieure et église Saint-Érasme visités le 25 juillet 1916", r"\bSercus\b", [2]),
    ("Steenwerck (Nord)", "bourg de la plaine de la Lys, gare et église Saint-Jean-Baptiste", r"\bSteenwerck\b", [10, 12, 14, 15, 17, 20, 21, 23, 24, 26, 27]),
    ("Talmas (Somme)", "commune sur la route d'Amiens à Doullens", r"\bTalmas\b", [162]),
    ("Thièvres (Somme / Pas-de-Calais)", "village de la vallée de l'Authie entre Lucheux et Raincheval", r"\bThièvres\b", [41]),
    ("Toulouse (Haute-Garonne)", "métropole languedocienne où séjournent Hippolyte Combes et Marguerite Calmels lors des deux permissions (rue du Taur, rue Pharaon, cathédrale Saint-Étienne, basilique Saint-Sernin, Daurade, Dalbade, Hôtel d'Assézat, Faculté des lettres, Sainte-Marie-des-Champs, Capitole, place Esquirol, marché Victor-Hugo, canal du Midi)", r"\b(?:Toulouse|St-Etienne|St-Sernin|Dalbade|Daurade|Assézat|Esquirol|Ste-Marie-des-Champs)\b", [1, 47, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 64, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 156]),
    ("Toutencourt (Somme)", "commune entre Raincheval et Contay, siège de la Mission militaire française auprès de la V\\textsuperscript{e} Armée britannique", r"\bToutencourt\b", [105, 110, 111, 150, 155, 160, 164, 166, 167, 178]),
    ("Vadencourt (Somme)", "village et château voisins de Contay", r"\bVadencourt\b", [107, 186]),
    ("Varennes-en-Croix (Somme)", "commune voisine d'Acheux-en-Amiénois (famille Mortreux)", r"\bVarennes\b", [50, 96, 97, 98, 121, 128, 176, 184]),
    ("Villers-Bocage (Somme)", "chef-lieu de canton entre Amiens et Doullens", r"\bVillers-Bocage\b", [162, 186]),
    ("Warloy-Baillon (Somme)", "bourg entre Contay et Senlis-le-Sec", r"\bWarloy\b", [75, 76, 96, 169, 171, 176, 179, 181, 186]),
    ("Ypres (Belgique)", "ville martyre de Flandre occidentale (cartes postales acquises à Renescure)", r"\bYpres\b", [4, 9]),
]


def _collect_scans_for_entry(records: list[dict], regex_pat: str, explicit_scans: list[int]) -> list[int]:
    matched = set(explicit_scans)
    for r in records:
        n = r["scan_num"]
        haystack = "\n".join(r["lines"]) + "\n" + r["lieu"]
        if re.search(regex_pat, haystack):
            matched.add(n)
    return sorted(matched)


def index_document_sources(document_context=""):
    sources = [
        {'id': 'genealogie_combes', 'text': TIKZ_ARBRE_COMBES_ALRIC, 'reference': r'Généalogie I (p.~\pageref{genealogie:combes})'},
        {'id': 'genealogie_calmels', 'text': TIKZ_ARBRE_CALMELS_ALLIANCES, 'reference': r'Généalogie II (p.~\pageref{genealogie:calmels})'},
        {'id': 'organigramme', 'text': TIKZ_ORGANIGRAMME_MILITAIRE, 'reference': r'Organigramme III (p.~\pageref{genealogie:militaires})'},
    ]
    marker = r'\section{Destin'
    if marker in document_context:
        biography = document_context[document_context.index(marker):].split(r'\section{Présentation', 1)[0]
        sources.append({'id': 'biographie', 'text': biography, 'reference': r'Prolégomènes, §~I (début p.~\pageref{proleg:biographie})'})
    for item in load_map_manifest():
        map_id = item['id']
        title = 'Carte générale' if map_id == 'generale' else 'Carte du chapitre ' + map_id
        sources.append({'id': 'carte:' + map_id, 'text': item['printed_text'],
                        'reference': title + r' (p.~\pageref{carte:' + map_id + '})'})
    return sources


def build_indexes_latex(records: list[dict], document_context: str = "") -> str:
    """
    Construit le code LaTeX des deux index finaux :
    1. Index des noms de personnes (Index nominum)
    2. Index des noms de lieux (Index locorum)
    Chaque occurrence cite à la fois le folio du carnet (f° X r°/v°) et la page
    exacte du fichier PDF généré (p. \\pageref{fol:N}).
    """
    from index_verifie import collect_index_entries, index_reference_text, validate_index_entries
    from index_complements import EXTRA_PERSONS, EXTRA_PLACES
    document_sources = index_document_sources(document_context)
    import unicodedata
    def alphabetic(row):
        return ''.join(c for c in unicodedata.normalize('NFKD', row[0]).casefold() if not unicodedata.combining(c))
    people = collect_index_entries(records, sorted(INDEX_PERSONNES_CATALOG + EXTRA_PERSONS, key=alphabetic), 'personne', document_sources)
    places = collect_index_entries(records, sorted(INDEX_LIEUX_CATALOG + EXTRA_PLACES, key=alphabetic), 'lieu', document_sources)
    validate_index_entries(records, people + places, document_sources)
    person_items, place_items = [], []
    for entries, items in [(people, person_items), (places, place_items)]:
        for entry in entries:
            refs = index_reference_text(entry, folio_fr_ref)
            if not refs and entry['headword'].startswith(('Combes, Françoise', 'Combes, Maria')):
                refs = r'Généalogie I (p.~\pageref{genealogie:combes})'
            if not refs:
                continue
            headword, desc = entry['headword'], entry['description']
            items.append(f"\\noindent\\hangindent=4.5mm\\textbf{{{headword}}}, {desc} : {refs}.\\par\\vspace{{0.55mm}}")

    persons_joined = "\n".join(person_items)
    places_joined = "\n".join(place_items)

    return f"""
% =============================================================================
% INDEX DES NOMS DE PERSONNES (INDEX NOMINUM) ET INDEX DES NOMS DE LIEUX (INDEX LOCORUM)
% =============================================================================
\\cleardoublepage
\\renewcommand{{\\currentmonthyear}}{{Index des noms de personnes}}
\\renewcommand{{\\currentfoliolabel}}{{Index nominum}}
\\chapter*{{Index des noms de personnes (\\textit{{Index nominum}})}}
\\addcontentsline{{toc}}{{chapter}}{{Index des noms de personnes (\\textit{{Index nominum}})}}
\\markboth{{Index des noms de personnes}}{{Index des noms de personnes}}
{{\\fontsize{{7.0pt}}{{8.3pt}}\\selectfont
\\noindent Les renvois citent les noms effectivement présents dans le texte ; \\textit{{Comm.}} distingue les seules mentions du commentaire et \\textit{{lect. inc.}} une lecture réservée. Les attestations du carnet renvoient à la foliotation éditoriale du \\textit{{Livre-Journal}} (\\texttt{{f\\textsuperscript{{o}}~X~r\\textsuperscript{{o}}/v\\textsuperscript{{o}}}}) et à la pagination exacte de la présente édition (\\texttt{{p.~Y}}). Les renvois aux arbres, cartes et prolégomènes sont signalés séparément et donnent la page de ces documents.\\par\\vspace{{2.0mm}}
{persons_joined}
\\par}}

\\cleardoublepage
\\renewcommand{{\\currentmonthyear}}{{Index des noms de lieux}}
\\renewcommand{{\\currentfoliolabel}}{{Index locorum}}
\\chapter*{{Index des noms de lieux (\\textit{{Index locorum}})}}
\\addcontentsline{{toc}}{{chapter}}{{Index des noms de lieux (\\textit{{Index locorum}})}}
\\markboth{{Index des noms de lieux}}{{Index des noms de lieux}}
{{\\fontsize{{7.0pt}}{{8.3pt}}\\selectfont
\\noindent Les renvois distinguent les attestations du carnet, les mentions du commentaire (\\textit{{Comm.}}) et les documents imprimés. Les attestations du carnet donnent le folio éditorial du \\textit{{Livre-Journal}} (\\texttt{{f\\textsuperscript{{o}}~X~r\\textsuperscript{{o}}/v\\textsuperscript{{o}}}}) et au numéro de page correspondant du présent volume (\\texttt{{p.~Y}}). Les cartes et arbres citent leur propre page ; \\textit{{lect. inc.}} signale une lecture réservée.\\par\\vspace{{2.0mm}}
{places_joined}
\\par}}
"""

