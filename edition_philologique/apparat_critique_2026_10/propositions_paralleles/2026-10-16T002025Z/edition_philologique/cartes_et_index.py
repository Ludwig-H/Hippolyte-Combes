# -*- coding: utf-8 -*-
"""
Arbres généalogiques vectoriels (TikZ), cartes d'itinéraires vectorielles (TikZ)
pour les Prolégomènes et les sept chapitres, et génération des deux index finaux
(Index des noms de personnes et Index des noms de lieux) avec double référence
au folio du carnet (f° X r°/v°) et à la page du PDF (p. \\pageref{fol:N}).
"""

import re
from commentaires_et_loci import folio_fr_ref


# =============================================================================
# 1. TROIS ARBRES GÉNÉALOGIQUES ET PROSOPOGRAPHIQUES EN TIKZ (PROLÉGOMÈNES)
# =============================================================================

TIKZ_ARBRE_COMBES_ALRIC = r"""
\begin{center}
\begin{tikzpicture}[
  every node/.style={font=\fontsize{6.2pt}{7.2pt}\selectfont, align=center},
  box/.style={draw=black!80, line width=0.4pt, fill=white, rounded corners=1.2pt, inner sep=2.2pt},
  hero/.style={draw=bordeaux, line width=0.8pt, fill=white, rounded corners=1.2pt, inner sep=2.6pt},
  edge/.style={draw=black!75, line width=0.4pt}
]
% Grands-parents
\node[box, text width=34mm] (gp1) at (-42mm, 34mm) {\textbf{Jean-Pierre Combes}\\(1788–1875)\\\textit{Avoué licencié à Millau}};
\node[box, text width=34mm] (gm1) at (-4mm, 34mm) {\textbf{Marie-Julie-Rose Descuret}\\(1801–1876)\\\textit{Millau}};
\node[box, text width=30mm] (gp2) at (30mm, 34mm) {\textbf{Augustin Alric}\\\textit{Banquier à Millau}};
\node[box, text width=28mm] (gm2) at (62mm, 34mm) {\textbf{Émilie Noël}\\(\dag~1906)\\\textit{Millau}};

% Parents
\node[box, text width=46mm] (pere) at (-23mm, 18mm) {\textbf{François Augustin Hippolyte Combes}\\(1825–1899)\\\textit{Avocat à Millau puis Toulouse (47, rue du Taur)}};
\node[box, text width=38mm] (mere) at (35mm, 18mm) {\textbf{Marie Anaïs Alric}\\(1838–1907)\\\textit{Mariés en 1870}};
\node[box, text width=24mm] (oncle_alric) at (67mm, 18mm) {\textbf{Hippolyte Alric}\\\textit{Ingénieur ECP}};

\draw[edge] (gp1.south) -- ++(0,-2.5mm) -| (pere.north);
\draw[edge] (gm1.south) -- ++(0,-2.5mm) -| (pere.north);
\draw[edge] (gp2.south) -- ++(0,-2.5mm) -| (mere.north);
\draw[edge] (gm2.south) -- ++(0,-2.5mm) -| (mere.north);
\draw[edge] (gp2.south) -- ++(0,-2.5mm) -| (oncle_alric.north);
\draw[edge] (pere.east) -- node[above, font=\fontsize{5.5pt}{6.5pt}\selectfont]{$\times$} (mere.west);

% Fratrie Combes
\coordinate (frat_mid) at (6mm, 11mm);
\draw[edge] (6mm, 18mm) -- (frat_mid);

\node[box, text width=27mm] (s1) at (-46mm, 1mm) {\textbf{Françoise Combes}\\(1871–1942)\\\textit{Sœur Marie de la Croix}\\Carmel de Périgueux};
\node[box, text width=27mm] (s2) at (-16mm, 1mm) {\textbf{Joséphine Combes}\\(1873 – oct. 1914)\\\textit{\dag~à Nogent-le-Rotrou}};
\node[box, text width=26mm] (s3) at (13mm, 1mm) {\textbf{Maria Combes}\\(1875 – 19 nov. 1903)\\\textit{Religieuse, \dag~à Carthage}};
\node[hero, text width=44mm] (hc) at (52mm, 1mm) {\textbf{Marie Lucien Hippolyte Combes}\\(Millau, 14 août 1876 –\\Saint-Chély-d'Apcher, 2 sept. 1970)\\\textit{Professeur d'anglais, interprète B.E.F.}};

\draw[edge] (frat_mid) -| (s1.north);
\draw[edge] (frat_mid) -| (s2.north);
\draw[edge] (frat_mid) -| (s3.north);
\draw[edge] (frat_mid) -| (hc.north);

% Mariage Hippolyte & Marguerite et enfants
\node[hero, text width=42mm] (mc) at (-18mm, -15mm) {\textbf{Marie Marguerite Calmels}\\(Millau, 15 avril 1892 – 19 mars 1974)\\\textit{« Marg\textsuperscript{te} / M\textsuperscript{te} / Gueïte »}};
\draw[edge, bordeaux, line width=0.6pt] (hc.south) -- ++(0,-3mm) -| node[pos=0.25, above, font=\fontsize{5.6pt}{6.5pt}\selectfont]{\textbf{Mariés à Millau le 25 oct. 1917}} (mc.north);

\node[box, text width=92mm] (enfants) at (22mm, -26mm) {\textbf{Enfants d'Hippolyte et Marguerite Combes :} \textbf{Valentine Combes} (née en 1918), \textbf{Geneviève Combes}, \textbf{Jean Combes} et \textbf{François Combes} (père de \textbf{Pierre Combes})};
\draw[edge] (17mm, -11mm) -- (enfants.north);
\end{tikzpicture}
\par\vspace{0.8mm}{\scriptsize\textit{Arbre généalogique I.} La famille Combes–Alric (Millau, Toulouse, Nogent-le-Rotrou et Montauban).}
\end{center}
"""

TIKZ_ARBRE_CALMELS_ALLIANCES = r"""
\begin{center}
\begin{tikzpicture}[
  every node/.style={font=\fontsize{6.0pt}{7.0pt}\selectfont, align=center},
  box/.style={draw=black!80, line width=0.4pt, fill=white, rounded corners=1.2pt, inner sep=2.0pt},
  hero/.style={draw=bordeaux, line width=0.75pt, fill=white, rounded corners=1.2pt, inner sep=2.2pt},
  edge/.style={draw=black!75, line width=0.4pt}
]
% Ligne supérieure : Crouzet-Calmels (Toulouse), Calmels-Cartairade (Millau), Layrals-Cartairade (Millau)
\node[box, text width=38mm] (crouzet) at (-43mm, 24mm) {\textbf{Émile Crouzet} (1842–1921)\\\textit{Agent de change à Toulouse}\\$\times$ \textbf{Élisabeth Calmels}\\(\textit{« Oncle Émile \& Tante »})};
\node[box, text width=42mm] (calmels) at (1mm, 24mm) {\textbf{D\textsuperscript{r} Gabriel Calmels} (1852–1921)\\\textit{Médecin à Millau (10, rue A.-Guibert)}\\$\times$ \textbf{Valentine Cartairade} (1858–1943)};
\node[box, text width=38mm] (layrals) at (45mm, 24mm) {\textbf{M\textsuperscript{e} Charles Layrals}\\\textit{Notaire à Millau}\\$\times$ \textbf{Thérèse Cartairade}\\(\textit{« l'oncle \& tante Thérèse »})};

\draw[edge, dashed] (crouzet.east) -- (calmels.west);
\draw[edge, dashed] (calmels.east) -- (layrals.west);

% Cousin Jean Crouzet et cousins Layrals
\node[box, text width=32mm] (jean_cr) at (-46mm, 8mm) {\textbf{Abbé Jean Crouzet}\\\textit{« Jean », prêtre à Toulouse}\\(futur curé de la Dalbade)};
\draw[edge] (crouzet.south) -- (jean_cr.north);

\node[box, text width=32mm] (fils_layrals) at (48mm, 8mm) {\textbf{Louis Layrals} (\dag~1961, notaire)\\\textbf{Jean Layrals} (\dag~1947, magistrat)};
\draw[edge] (layrals.south) -- (fils_layrals.north);

% Enfants Calmels
\coordinate (cal_mid) at (1mm, 15.5mm);
\draw[edge] (calmels.south) -- (cal_mid);

\node[box, text width=32mm] (mad) at (-38mm, -5mm) {\textbf{Madeleine Calmels}\\(1882–1961, \textit{« Mad\textsuperscript{ne} »})\\$\times$ \textbf{D\textsuperscript{r} Fernand Vincens}\\\textit{Enfants :} \textbf{Germaine} \& \textbf{Robert}};
\node[box, text width=28mm] (mimi) at (-5mm, -5mm) {\textbf{Anne-Marie Calmels}\\(1888–1975, \textit{« Mimi »})\\$\times$ \textbf{M\textsuperscript{e} Joseph Delcamps}\\\textit{Avoué à Millau}};
\node[box, text width=20mm] (pierre) at (22mm, -5mm) {\textbf{Pierre Calmels}\\\textit{Frère de}\\Marguerite\\(Millau)};
\node[hero, text width=33mm] (marg) at (51mm, -5mm) {\textbf{Marguerite Calmels}\\(1892–1974)\\\textit{« Marg\textsuperscript{te} / M\textsuperscript{te} »}\\$\times$ \textbf{Hippolyte Combes}};

\draw[edge] (cal_mid) -| (mad.north);
\draw[edge] (cal_mid) -| (mimi.north);
\draw[edge] (cal_mid) -| (pierre.north);
\draw[edge] (cal_mid) -| (marg.north);

% Branche Faure à Neuilly-sur-Seine
\node[box, text width=122mm] (faure) at (1mm, -18.5mm) {\textbf{Branche cousine de Neuilly-sur-Seine (16, rue d'Armenonville) :} \textbf{M\textsuperscript{me} Faure} et ses cinq enfants : \textbf{Marguerite}, \textbf{Germaine}, \textbf{Marcel Faure} (en permission en janv. 1917), \textbf{Henri Faure} (aspirant) et \textbf{André Faure} (candidat à Polytechnique)};
\end{tikzpicture}
\par\vspace{0.8mm}{\scriptsize\textit{Arbre généalogique II.} La famille Calmels–Cartairade et ses alliances à Millau, Toulouse et Neuilly-sur-Seine.}
\end{center}
"""

TIKZ_ORGANIGRAMME_MILITAIRE = r"""
\begin{center}
\begin{tikzpicture}[
  every node/.style={font=\fontsize{5.9pt}{6.9pt}\selectfont, align=center},
  box/.style={draw=black!80, line width=0.4pt, fill=white, rounded corners=1.2pt, inner sep=2.0pt},
  hero/.style={draw=bordeaux, line width=0.75pt, fill=white, rounded corners=1.2pt, inner sep=2.2pt},
  edge/.style={draw=black!75, line width=0.4pt, ->, >=stealth}
]
\node[box, text width=56mm] (bef) at (-32mm, 22mm) {\textbf{18th (Eastern) Division \& Fifth Army (B.E.F.)}\\\textbf{Maj.-Gen. Sir Ivor Maxse} (cmdt la 18\textsuperscript{e} Division)\\\textbf{Lt.-Col. D.~C.~E. Grose} (cmdt le \textit{18th Divisional Train})};
\node[box, text width=56mm] (mmf) at (33mm, 22mm) {\textbf{Mission militaire française (B.E.F.)}\\\textbf{Lt Pizzi} (18\textsuperscript{e} Div.), \textbf{S/Lt Ferran} (liaison),\\\textbf{Cap. Huguet} (XIII\textsuperscript{e} Corps), \textbf{Cap. Bresson} (V\textsuperscript{e} Armée)};

\node[hero, text width=68mm] (hc) at (0mm, 9mm) {\textbf{Interprète Hippolyte Combes (matr. 911, classe 1896)}\\Détaché auprès de l'Armée britannique (4 mai 1915 – 11 nov. 1918)};

\draw[edge] (bef.south) -- (hc.north west);
\draw[edge] (mmf.south) -- (hc.north east);

\node[box, text width=40mm] (asc) at (-43mm, -6mm) {\textbf{152nd \& 150th Cos. A.S.C.}\\\textit{(Juillet – Octobre 1916)}\\\textbf{Cap. E.~M. West}, \textbf{Cap. E.~M. Ford},\\\textbf{Lt Curtis} (\textit{C\textsuperscript{tis}}), \textbf{Cap. Panton},\\\textbf{Lt Walsh}, \textbf{Lt Michel}, \textbf{Lt First},\\\textbf{Maj. Hughes}, \textbf{Lt Morris}};
\node[box, text width=41mm] (forage) at (0mm, -6mm) {\textbf{Foraging \& Purchase Board}\\\textit{(Acheux \& Hérissart, nov. 1916 – avr. 1917)}\\\textbf{Major Levy} (\textit{Purchase Board}),\\\textbf{Cap. Williams} (déc. 1916 – mars 1917),\\\textbf{2nd Lt Gilbert} (de Jersey, avr. 1917),\\\textbf{Lt Croughton}, \textbf{Lt Godard}, \textbf{Lt Wentworth}};
\node[box, text width=38mm] (coll) at (43mm, -6mm) {\textbf{Collègues \& Universitaires}\\\textit{Interprètes :} \textbf{Maurin}, \textbf{Lépin},\\\textbf{Schumacher}, \textbf{Raucoule}, \textbf{Valet}\\(\textit{2nd Austr. Div.}), \textbf{Brammas}\\\textit{Lettres :} \textbf{E.~Zyromski} (Toulouse),\\\textbf{Fortuné \& L.-F. Flutre} (ENS)};

\draw[edge] (hc.south) -- (-43mm, 1.5mm);
\draw[edge] (hc.south) -- (0mm, 1.5mm);
\draw[edge] (hc.south) -- (43mm, 1.5mm);
\end{tikzpicture}
\par\vspace{0.8mm}{\scriptsize\textit{Organigramme III.} Cadre militaire britannique et français et réseau intellectuel d'Hippolyte Combes (1916–1917).}
\end{center}
"""


# =============================================================================
# 2. CARTE GÉNÉRALE (PROLÉGOMÈNES) ET SEPT CARTES DE CHAPITRES EN TIKZ
# =============================================================================

TIKZ_CARTE_GENERALE = r"""
\begin{center}
\begin{tikzpicture}[
  scale=0.92,
  every node/.style={font=\fontsize{6.0pt}{7.0pt}\selectfont},
  city/.style={circle, fill=black, inner sep=1.1pt},
  hub/.style={circle, draw=bordeaux, fill=white, line width=0.7pt, inner sep=1.5pt},
  route/.style={draw=bordeaux, line width=0.65pt, ->, >=stealth},
  perm/.style={draw=black!65, line width=0.55pt, dashed, ->, >=stealth}
]
% Cadre géographique schématique de la France
\draw[black!40, line width=0.35pt] (-58mm,-36mm) rectangle (62mm,36mm);
% Silhouette schématique des côtes et frontières de la France
\draw[black!30, line width=0.5pt, fill=black!2]
  (-8mm,33mm) -- (4mm,31mm) -- (18mm,24mm) -- (28mm,16mm) -- (26mm,2mm)
  -- (30mm,-10mm) -- (28mm,-22mm) -- (14mm,-29mm) -- (-4mm,-33mm) -- (-22mm,-31mm)
  -- (-28mm,-16mm) -- (-34mm,2mm) -- (-44mm,12mm) -- (-26mm,18mm) -- (-16mm,27mm) -- cycle;

% Nord / Pas-de-Calais / Somme
\node[hub] (flandre) at (-4mm, 30mm) {};
\node[above right] at (flandre) {\textbf{1. Flandre \& Lys} (Lynde, Bailleul, Steenwerck, juill.–août 1916)};

\node[hub] (ternois) at (-8mm, 24mm) {};
\node[left] at (ternois) {\textbf{2. Artois / Ternois} (Saint-Pol, Marquay, août–sept. 1916)};

\node[hub] (somme) at (-5mm, 19mm) {};
\node[right] at (somme) {\textbf{3. Front de la Somme} (Albert, Acheux, Hérissart, sept. 1916 – avr. 1917)};

\node[city] (amiens) at (-9mm, 16mm) {};
\node[left] at (amiens) {Amiens};

% Paris / Neuilly / Nogent
\node[hub] (paris) at (-7mm, 8mm) {};
\node[right] at (paris) {\textbf{Paris \& Neuilly-sur-Seine} (permissions)};
\node[city] (nogent) at (-18mm, 5mm) {};
\node[left] at (nogent) {Nogent-le-Rotrou};
\node[city] (andelys) at (-14mm, 12mm) {};
\node[left] at (andelys) {Les Andelys (1918)};

% Massif central
\node[city] (clermont) at (3mm, -8mm) {};
\node[right] at (clermont) {Clermont-Ferrand / Saint-Flour (retour févr. 1917)};

% Midi : Toulouse, Montauban, Millau, Béziers
\node[city] (montauban) at (-12mm, -21mm) {};
\node[left] at (montauban) {Montauban};
\node[hub] (toulouse) at (-11mm, -26mm) {};
\node[left] at (toulouse) {\textbf{Toulouse} (sept.–oct. 1916 \& janv.–févr. 1917)};
\node[hub] (millau) at (2mm, -22mm) {};
\node[right] at (millau) {\textbf{Millau} (berceau familial, févr. \& oct. 1917)};
\node[city] (beziers) at (5mm, -29mm) {};
\node[right] at (beziers) {Carcassonne \& Béziers (3 févr. 1917)};

% Flèches d'itinéraires
\draw[route] (flandre) -- (ternois);
\draw[route] (ternois) -- (somme);
\draw[perm] (somme) -- (amiens) -- (paris);
\draw[perm] (paris) to[bend right=12] (toulouse);
\draw[perm] (toulouse) to[bend right=15] (beziers) to[bend right=12] (millau);
\draw[perm] (millau) -- (clermont) -- (paris);

% Rose des vents
\draw[->, line width=0.5pt] (53mm, 24mm) -- (53mm, 31mm) node[above]{\textbf{N}};
\end{tikzpicture}
\par\vspace{0.8mm}{\scriptsize\textit{Carte générale.} Les théâtres d'opérations (Flandre, Artois, Somme) et les grands déplacements de permission d'Hippolyte Combes (1916–1917).}
\end{center}
"""


TIKZ_CARTES_CHAPITRES = {
    "I": r"""
\begin{tikzpicture}[
  scale=0.96,
  every node/.style={font=\fontsize{6.0pt}{7.0pt}\selectfont},
  loc/.style={circle, fill=black, inner sep=1.1pt},
  step/.style={circle, draw=bordeaux, fill=white, line width=0.75pt, inner sep=1.5pt},
  move/.style={draw=bordeaux, line width=0.75pt, ->, >=stealth},
  excur/.style={draw=black!65, line width=0.5pt, dashed, ->, >=stealth},
  river/.style={draw=black!35, line width=1.1pt}
]
\draw[black!50, line width=0.4pt] (-60mm,-42mm) rectangle (60mm,42mm);
\fill[black!3] (-60mm,-42mm) rectangle (60mm,42mm);

% Cours de la Lys et frontière belge
\draw[river] (-55mm,-30mm) .. controls (-20mm,-26mm) and (5mm,-22mm) .. (55mm,-14mm)
  node[pos=0.35, below, font=\fontsize{5.8pt}{6.5pt}\selectfont\itshape]{La Lys (canalisée)};
\draw[black!45, dash pattern=on 3pt off 2pt, line width=0.5pt]
  (-10mm,40mm) -- (5mm,22mm) -- (22mm,14mm) -- (45mm,-8mm)
  node[pos=0.25, right, font=\fontsize{5.6pt}{6.5pt}\selectfont]{\textit{Frontière franco-belge}};

% Ligne de front (août 1916)
\draw[bordeaux!80, line width=0.9pt, decorate, decoration={zigzag, segment length=4pt, amplitude=1pt}]
  (48mm,10mm) -- (46mm,-16mm) -- (42mm,-38mm);
\node[rotate=-82, font=\fontsize{5.6pt}{6.5pt}\selectfont, bordeaux] at (51mm,-14mm) {\textbf{Ligne de front (secteur d'Armentières–Fleurbaix)}};

% Localités Flandre intérieure (Ouest)
\node[loc] (renescure) at (-48mm, 14mm) {};
\node[below left] at (renescure) {\textbf{Renescure} (châteaux, 27 juill.)};

\node[step] (lynde) at (-36mm, 18mm) {};
\node[above left] at (lynde) {\textbf{1. Lynde} (25–28 juill.)};

\node[loc] (sercus) at (-32mm, 10mm) {};
\node[below] at (sercus) {\textbf{Sercus} (25 juill.)};

\node[loc] (hazebrouck) at (-22mm, 16mm) {};
\node[above] at (hazebrouck) {\textbf{Hazebrouck} (27–28 juill.)};

% Monts des Flandres
\node[step] (stjans) at (-2mm, 18mm) {};
\node[above left] at (stjans) {\textbf{2. Saint-Jans-Cappel} (28 juill. – 5 août)};

\node[loc] (montnoir) at (6mm, 22mm) {};
\node[right] at (montnoir) {Mont-Noir (29 juill.)};

\node[step] (bailleul) at (0mm, 6mm) {};
\node[left] at (bailleul) {\textbf{Bailleul} (30 juill. – 5 août)};

% Vallée de la Lys
\node[loc] (steenwerck) at (4mm, -8mm) {};
\node[left] at (steenwerck) {Steenwerck};

\node[step] (croixdubac) at (12mm, -15mm) {};
\node[above right] at (croixdubac) {\textbf{3. La Croix-du-Bac} (5–12 août)};

\node[loc] (bacstmaur) at (14mm, -23mm) {};
\node[below] at (bacstmaur) {\textbf{Bac-Saint-Maur} (\textit{refilling point})};

\node[loc] (sailly) at (6mm, -26mm) {};
\node[below left] at (sailly) {\textbf{Sailly-sur-la-Lys} (écluse, 10 août)};

\node[loc] (armentieres) at (34mm, -16mm) {};
\node[above] at (armentieres) {\textbf{Armentières} \& blanchisserie Barbry (11 août)};

% Flèches de déplacement principal et tournées
\draw[excur] (lynde) -- (sercus);
\draw[excur] (lynde) -- (renescure);
\draw[move] (lynde) -- (hazebrouck) -- (stjans);
\draw[excur] (stjans) -- (montnoir);
\draw[move] (stjans) -- (bailleul) -- (steenwerck) -- (croixdubac);
\draw[excur] (croixdubac) -- (bacstmaur);
\draw[excur] (bacstmaur) -- (sailly);
\draw[excur] (croixdubac) -- (armentieres);

% Échelle et Nord
\draw[line width=0.6pt] (-54mm,-36mm) -- (-34mm,-36mm);
\draw (-54mm,-37mm) -- (-54mm,-35mm) (-34mm,-37mm) -- (-34mm,-35mm);
\node[above] at (-44mm,-36mm) {0 \hfill 5 \hfill 10 km};
\draw[->, line width=0.6pt] (52mm, 28mm) -- (52mm, 37mm) node[above]{\textbf{N}};
\end{tikzpicture}
""",
    "II": r"""
\begin{tikzpicture}[
  scale=0.96,
  every node/.style={font=\fontsize{6.0pt}{7.0pt}\selectfont},
  loc/.style={circle, fill=black, inner sep=1.1pt},
  step/.style={circle, draw=bordeaux, fill=white, line width=0.75pt, inner sep=1.5pt},
  rail/.style={draw=black!80, line width=0.75pt, double distance=0.8pt, ->, >=stealth},
  move/.style={draw=bordeaux, line width=0.75pt, ->, >=stealth},
  excur/.style={draw=black!65, line width=0.5pt, dashed, ->, >=stealth},
  river/.style={draw=black!35, line width=1.0pt}
]
\draw[black!50, line width=0.4pt] (-60mm,-42mm) rectangle (60mm,42mm);
\fill[black!3] (-60mm,-42mm) rectangle (60mm,42mm);

% Rivières : la Lys au nord, la Ternoise au centre, l'Authie et l'Ancre au sud
\draw[river] (-20mm,31mm) -- (35mm,34mm) node[pos=0.8, below]{\textit{La Lys}};
\draw[river] (-45mm,10mm) .. controls (-20mm,6mm) and (-5mm,4mm) .. (10mm,2mm) node[right]{\textit{La Ternoise}};
\draw[river] (-40mm,-14mm) .. controls (-10mm,-16mm) and (10mm,-18mm) .. (25mm,-20mm) node[right]{\textit{L'Authie}};

% Ligne de front (Armentières - Arras - Thiepval)
\draw[bordeaux!80, line width=0.85pt, dash pattern=on 4pt off 2pt]
  (38mm,38mm) -- (32mm,14mm) -- (36mm,-4mm) -- (34mm,-36mm);
\node[rotate=-86, font=\fontsize{5.5pt}{6.5pt}\selectfont, bordeaux] at (40mm,2mm) {\textbf{Ligne de front (Armentières – Arras – Thiepval)}};

% Secteur 1 : Vallée de la Lys (13-25 août)
\node[step] (bailleul) at (-4mm, 36mm) {};
\node[above] at (bailleul) {\textbf{1. Bailleul} (embarquement 25 août)};
\node[loc] (croix) at (12mm, 33mm) {};
\node[below right] at (croix) {\textbf{La Croix-du-Bac}, Fleurbaix, Armentières (13–24 août)};
\node[loc] (estaires) at (4mm, 28mm) {};
\node[below left] at (estaires) {Estaires (23 août)};
\node[loc] (hazebrouck) at (-22mm, 34mm) {};
\node[above] at (hazebrouck) {Hazebrouck};

% Secteur 2 : Ternois / Artois (25 août - 9 sept.)
\node[step] (stpol) at (-14mm, 8mm) {};
\node[above left] at (stpol) {\textbf{Saint-Pol-sur-Ternoise} (25 août – 7 sept.)};
\node[step] (marquay) at (-2mm, 6mm) {};
\node[above right] at (marquay) {\textbf{2. Marquay} (cantonnement, 25 août – 9 sept.)};
\node[loc] (ligny) at (-4mm, 0mm) {};
\node[right] at (ligny) {Ligny-Saint-Flochel, Roëllecourt, Bailleul-aux-Cornailles};

% Secteur 3 : Marche vers la Somme (9-24 sept.)
\node[step] (oppy) at (4mm, -6mm) {};
\node[right] at (oppy) {\textbf{3. Oppy / Beaudricourt} (9–10 sept.)};
\node[step] (lucheux) at (-4mm, -15mm) {};
\node[left] at (lucheux) {\textbf{4. Lucheux} (11 sept.)};
\node[loc] (thievres) at (4mm, -22mm) {};
\node[right] at (thievres) {Thièvres};
\node[step] (raincheval) at (-2mm, -27mm) {};
\node[left] at (raincheval) {\textbf{5. Raincheval} (11–22 sept.)};
\node[loc] (acheux) at (10mm, -29mm) {};
\node[right] at (acheux) {\textbf{Acheux-en-Amiénois}};
\node[step] (forceville) at (14mm, -35mm) {};
\node[below] at (forceville) {\textbf{6. Forceville} \& Hédauville (22–24 sept.)};

% Trajets
\draw[excur] (croix) -- (estaires);
\draw[move] (croix) -- (bailleul);
\draw[rail] (bailleul) -- (hazebrouck) to[bend right=18] node[pos=0.5, left, font=\fontsize{5.6pt}{6.5pt}\selectfont]{\textit{Train militaire (25 août)}} (stpol);
\draw[move] (stpol) -- (marquay);
\draw[move] (marquay) -- (oppy) -- (lucheux) -- (thievres) -- (raincheval) -- (acheux) -- (forceville);

% Échelle et Nord
\draw[line width=0.6pt] (-54mm,-36mm) -- (-32mm,-36mm);
\node[above] at (-43mm,-36mm) {0 \hfill 10 \hfill 20 km};
\draw[->, line width=0.6pt] (52mm, 28mm) -- (52mm, 37mm) node[above]{\textbf{N}};
\end{tikzpicture}
""",
    "III": r"""
\begin{tikzpicture}[
  scale=0.96,
  every node/.style={font=\fontsize{6.0pt}{7.0pt}\selectfont},
  loc/.style={circle, fill=black, inner sep=1.1pt},
  step/.style={circle, draw=bordeaux, fill=white, line width=0.75pt, inner sep=1.5pt},
  rail/.style={draw=bordeaux, line width=0.75pt, ->, >=stealth}
]
\draw[black!50, line width=0.4pt] (-60mm,-42mm) rectangle (60mm,42mm);
\fill[black!3] (-60mm,-42mm) rectangle (60mm,42mm);

% Partie gauche : Grand axe ferroviaire Somme - Paris - Toulouse (-58mm à -2mm)
\node[font=\fontsize{6.3pt}{7.2pt}\selectfont\bfseries] at (-30mm, 37mm) {A. Trajet ferroviaire (25 sept. – 6 oct. 1916)};
\node[step] (acheux) at (-32mm, 30mm) {};
\node[right] at (acheux) {\textbf{1. Forceville / Acheux} (25 sept.)};
\node[loc] (amiens) at (-36mm, 23mm) {};
\node[left] at (amiens) {Amiens \& Creil};
\node[step] (paris) at (-32mm, 14mm) {};
\node[right] at (paris) {\textbf{2. Paris \& Neuilly} (26 sept. / 5 oct.)};
\node[loc] (limoges) at (-36mm, -2mm) {};
\node[left] at (limoges) {Limoges, Brive, Cahors};
\node[loc] (montauban) at (-33mm, -16mm) {};
\node[left] at (montauban) {Montauban};
\node[step] (toulouse) at (-30mm, -28mm) {};
\node[right] at (toulouse) {\textbf{3. Toulouse} (27 sept. – 4 oct.)};
\node[step] (canaples) at (-18mm, 26mm) {};
\node[right] at (canaples) {\textbf{4. Doullens / Canaples} (6 oct.)};

\draw[rail] (acheux) -- (amiens) -- (paris);
\draw[rail] (paris) -- (limoges) -- (montauban) -- (toulouse);
\draw[rail, dashed] (toulouse) to[bend right=22] (paris);
\draw[rail, dashed] (paris) to[bend right=15] (canaples);

% Filet vertical de séparation
\draw[black!40, line width=0.4pt] (-1mm,-38mm) -- (-1mm,38mm);

% Partie droite : Plan vectoriel de Toulouse (0mm à 58mm)
\node[font=\fontsize{6.3pt}{7.2pt}\selectfont\bfseries] at (29mm, 37mm) {B. Plan des lieux fréquentés à Toulouse};
% La Garonne et le Canal du Midi
\draw[black!35, line width=1.6pt] (6mm,-34mm) .. controls (12mm,-10mm) and (14mm,10mm) .. (6mm,30mm)
  node[pos=0.18, right, font=\fontsize{5.6pt}{6.5pt}\selectfont\itshape]{La Garonne};
\draw[black!45, line width=0.8pt] (28mm,32mm) .. controls (40mm,18mm) and (42mm,-4mm) .. (36mm,-28mm)
  node[pos=0.5, right, font=\fontsize{5.5pt}{6.5pt}\selectfont\itshape]{Canal du Midi};

\node[loc] (matabiau) at (34mm, 26mm) {};
\node[left] at (matabiau) {Gare Matabiau};
\node[step] (taur) at (20mm, 18mm) {};
\node[right] at (taur) {\textbf{Rue du Taur} (n\textsuperscript{o}~47) \& St-Sernin};
\node[loc] (capitole) at (19mm, 11mm) {};
\node[right] at (capitole) {Capitole \& Place Esquirol};
\node[step] (pharaon) at (17mm, 3mm) {};
\node[right] at (pharaon) {\textbf{Rue Pharaon} (famille Crouzet)};
\node[step] (stetienne) at (28mm, 6mm) {};
\node[above right] at (stetienne) {\textbf{Cath. Saint-Étienne}};
\node[loc] (grandrond) at (32mm, -2mm) {};
\node[left] at (grandrond) {Grand-Rond};
\node[loc] (stemarie) at (40mm, -8mm) {};
\node[right] at (stemarie) {\textbf{Ste-Marie-des-Champs}};
\node[loc] (pechdavid) at (18mm, -26mm) {};
\node[right] at (pechdavid) {\textbf{Pouvourville \& Pech-David} (28 sept.)};
\end{tikzpicture}
""",
    "IV": r"""
\begin{tikzpicture}[
  scale=0.96,
  every node/.style={font=\fontsize{6.0pt}{7.0pt}\selectfont},
  loc/.style={circle, fill=black, inner sep=1.1pt},
  step/.style={circle, draw=bordeaux, fill=white, line width=0.75pt, inner sep=1.5pt},
  move/.style={draw=bordeaux, line width=0.75pt, ->, >=stealth},
  excur/.style={draw=black!65, line width=0.5pt, dashed, ->, >=stealth},
  river/.style={draw=black!35, line width=1.1pt}
]
\draw[black!50, line width=0.4pt] (-60mm,-42mm) rectangle (60mm,42mm);
\fill[black!3] (-60mm,-42mm) rectangle (60mm,42mm);

% Vallée de l'Ancre
\draw[river] (36mm,26mm) .. controls (30mm,6mm) and (26mm,-12mm) .. (20mm,-36mm)
  node[pos=0.75, right, font=\fontsize{5.6pt}{6.5pt}\selectfont\itshape]{L'Ancre};

% Ligne de front de l'Ancre (Thiepval - Beaumont-Hamel)
\draw[bordeaux!80, line width=0.9pt, decorate, decoration={zigzag, segment length=4pt, amplitude=1pt}]
  (38mm,36mm) -- (42mm,12mm) -- (45mm,-14mm);
\node[rotate=-84, font=\fontsize{5.5pt}{6.5pt}\selectfont, bordeaux] at (47mm,10mm) {\textbf{Front de l'Ancre (Thiepval – Redoute Schwaben)}};

% Cantonnement de repos dans le Ponthieu (6-15 oct.)
\node[step] (ribeaucourt) at (-46mm, 24mm) {};
\node[above right] at (ribeaucourt) {\textbf{1. Ribeaucourt \& Barlette} (6–15 oct.)};
\node[loc] (domqueur) at (-48mm, 14mm) {};
\node[below right] at (domqueur) {Domqueur (9 oct.)};
\node[loc] (canaples) at (-32mm, 2mm) {};
\node[left] at (canaples) {Canaples (\textit{railhead}, 6 oct.)};

% Marche vers Albert (15-17 oct.)
\node[step] (beauval) at (-14mm, 20mm) {};
\node[above] at (beauval) {\textbf{2. Beauval} (15–16 oct.)};
\node[loc] (rubempre) at (-8mm, -8mm) {};
\node[left] at (rubempre) {Rubempré \& Septenville};
\node[step] (warloy) at (6mm, -10mm) {};
\node[below left] at (warloy) {\textbf{3. Warloy-Baillon} (16 oct.)};
\node[loc] (senlis) at (16mm, -6mm) {};
\node[left] at (senlis) {Senlis-le-Sec};

% Secteur d'Albert (17-31 oct.)
\node[step] (bouzincourt) at (22mm, -2mm) {};
\node[above left] at (bouzincourt) {\textbf{4. Bouzincourt} (17–19 oct.)};
\node[step] (albert) at (28mm, -12mm) {};
\node[below right] at (albert) {\textbf{5. Albert (\textit{Brickfields})} (19–31 oct.)};
\node[loc] (martinsart) at (30mm, 4mm) {};
\node[right] at (martinsart) {Martinsart \& Aveluy};

% Secteur d'Acheux (novembre 1916)
\node[step] (acheux) at (12mm, 18mm) {};
\node[above left] at (acheux) {\textbf{6. Acheux-en-Amiénois} (2–30 nov.)};
\node[loc] (varennes) at (16mm, 12mm) {};
\node[right] at (varennes) {Varennes \& Léalvillers};
\node[loc] (raincheval) at (-2mm, 10mm) {};
\node[left] at (raincheval) {Raincheval \& Arquèves};
\node[loc] (louvencourt) at (10mm, 28mm) {};
\node[above] at (louvencourt) {Louvencourt, Bertrancourt, Bus-lès-Artois};
\node[loc] (herissart) at (-6mm, -1mm) {};
\node[left] at (herissart) {Hérissart \& Puchevillers};

% Flèches d'itinéraires
\draw[move] (canaples) -- (ribeaucourt);
\draw[excur] (ribeaucourt) -- (domqueur);
\draw[move] (ribeaucourt) -- (beauval) -- (warloy) -- (bouzincourt) -- (albert);
\draw[move] (albert) to[bend left=18] (acheux);
\draw[excur] (acheux) -- (louvencourt);
\draw[excur] (acheux) -- (raincheval);
\draw[excur] (acheux) -- (varennes);
\draw[excur] (acheux) -- (herissart);

\draw[line width=0.6pt] (-54mm,-36mm) -- (-34mm,-36mm);
\node[above] at (-44mm,-36mm) {0 \hfill 5 \hfill 10 km};
\draw[->, line width=0.6pt] (52mm, 28mm) -- (52mm, 37mm) node[above]{\textbf{N}};
\end{tikzpicture}
""",
    "V": r"""
\begin{tikzpicture}[
  scale=0.96,
  every node/.style={font=\fontsize{6.0pt}{7.0pt}\selectfont},
  loc/.style={circle, fill=black, inner sep=1.1pt},
  hub/.style={circle, draw=bordeaux, fill=white, line width=0.85pt, inner sep=1.8pt},
  tour/.style={draw=bordeaux!85, line width=0.55pt, ->, >=stealth},
  river/.style={draw=black!35, line width=1.1pt}
]
\draw[black!50, line width=0.4pt] (-60mm,-42mm) rectangle (60mm,42mm);
\fill[black!3] (-60mm,-42mm) rectangle (60mm,42mm);

% Rivière l'Ancre
\draw[river] (36mm,28mm) .. controls (32mm,8mm) and (28mm,-12mm) .. (18mm,-36mm)
  node[pos=0.82, right, font=\fontsize{5.6pt}{6.5pt}\selectfont\itshape]{L'Ancre};

% Centre d'Acheux-en-Amiénois
\node[hub] (acheux) at (4mm, 14mm) {};
\node[above right] at (acheux) {\textbf{ACHEUX-EN-AMIÉNOIS} (centre des tournées)};

% Nord et Nord-Ouest
\node[loc] (authie) at (-4mm, 32mm) {};
\node[above] at (authie) {\textbf{Authie} \& St-Léger (9 déc., 6 janv.)};
\node[loc] (louvencourt) at (2mm, 24mm) {};
\node[left] at (louvencourt) {\textbf{Louvencourt}};
\node[loc] (bertrancourt) at (18mm, 24mm) {};
\node[right] at (bertrancourt) {\textbf{Bertrancourt} \& Bus-lès-Artois};
\node[loc] (beauquesne) at (-26mm, 24mm) {};
\node[left] at (beauquesne) {\textbf{Beauquesne} (20 déc., 5 janv.)};
\node[loc] (quesnoy) at (-18mm, 16mm) {};
\node[left] at (quesnoy) {Ferme du Quesnoy};
\node[loc] (raincheval) at (-14mm, 10mm) {};
\node[below left] at (raincheval) {\textbf{Raincheval} (\textit{Army P. Board})};
\node[loc] (arqueves) at (-6mm, 16mm) {};
\node[above left] at (arqueves) {Arquèves (\textbf{Belle-Église})};

% Est et Sud-Est (vers l'Ancre)
\node[loc] (lealvillers) at (8mm, 8mm) {};
\node[right] at (lealvillers) {Léalvillers};
\node[loc] (varennes) at (14mm, 4mm) {};
\node[right] at (varennes) {Varennes};
\node[loc] (forceville) at (20mm, 12mm) {};
\node[right] at (forceville) {Forceville \& \textbf{Englebelmer}};
\node[loc] (hedauville) at (18mm, -1mm) {};
\node[right] at (hedauville) {\textbf{Hédauville} (\textit{150th Co. A.S.C.}, 9 janv.)};
\node[loc] (albert) at (30mm, -12mm) {};
\node[right] at (albert) {\textbf{Albert} \& Bouzincourt};
\node[loc] (buire) at (24mm, -24mm) {};
\node[right] at (buire) {\textbf{Buire-sur-l'Ancre}, Ribemont \& Heilly (1\textsuperscript{er} déc.)};
\node[loc] (franvillers) at (10mm, -30mm) {};
\node[below] at (franvillers) {\textbf{Franvillers}};

% Sud et Sud-Ouest
\node[loc] (toutencourt) at (-4mm, -2mm) {};
\node[left] at (toutencourt) {\textbf{Toutencourt} (Mission V\textsuperscript{e} Armée)};
\node[loc] (harponville) at (6mm, -4mm) {};
\node[right] at (harponville) {Harponville};
\node[loc] (contay) at (6mm, -12mm) {};
\node[left] at (contay) {\textbf{Contay} \& Vadencourt};
\node[loc] (puchevillers) at (-18mm, -2mm) {};
\node[left] at (puchevillers) {\textbf{Puchevillers}};
\node[loc] (herissart) at (-20mm, -10mm) {};
\node[left] at (herissart) {\textbf{Hérissart}};
\node[loc] (rubempre) at (-16mm, -18mm) {};
\node[left] at (rubempre) {\textbf{Rubempré} \& Septenville};

% Rayons des tournées quotidiennes
\foreach \dest in {authie,louvencourt,bertrancourt,beauquesne,raincheval,arqueves,forceville,hedauville,albert,toutencourt,contay,puchevillers,herissart,rubempre} {
  \draw[tour] (acheux) -- (\dest);
}
\draw[tour] (albert) -- (buire) -- (franvillers);

\draw[line width=0.6pt] (-54mm,-36mm) -- (-34mm,-36mm);
\node[above] at (-44mm,-36mm) {0 \hfill 4 \hfill 8 km};
\draw[->, line width=0.6pt] (52mm, 28mm) -- (52mm, 37mm) node[above]{\textbf{N}};
\end{tikzpicture}
""",
    "VI": r"""
\begin{tikzpicture}[
  scale=0.96,
  every node/.style={font=\fontsize{6.0pt}{7.0pt}\selectfont},
  loc/.style={circle, fill=black, inner sep=1.1pt},
  step/.style={circle, draw=bordeaux, fill=white, line width=0.75pt, inner sep=1.5pt},
  aller/.style={draw=bordeaux, line width=0.75pt, ->, >=stealth},
  retour/.style={draw=black!75, line width=0.65pt, dashed, ->, >=stealth}
]
\draw[black!50, line width=0.4pt] (-60mm,-42mm) rectangle (60mm,42mm);
\fill[black!3] (-60mm,-42mm) rectangle (60mm,42mm);

% Partie gauche : Boucle ferroviaire Amiens - Paris - Toulouse - Béziers - Millau - Clermont - Paris
\node[font=\fontsize{6.2pt}{7.2pt}\selectfont\bfseries] at (-29mm, 37mm) {A. Boucle de la 2\textsuperscript{e} permission (26 janv. – 7 févr. 1917)};
\node[step] (amiens) at (-30mm, 31mm) {};
\node[right] at (amiens) {\textbf{1. Acheux / Amiens} (26 janv.)};
\node[step] (paris) at (-30mm, 21mm) {};
\node[right] at (paris) {\textbf{2. Paris \& Neuilly} (famille Faure, 27 janv.)};
\node[step] (toulouse) at (-44mm, -22mm) {};
\node[above left] at (toulouse) {\textbf{3. Toulouse} (28 janv. – 3 févr.)};
\node[loc] (carca) at (-28mm, -28mm) {};
\node[below] at (carca) {Carcassonne (Jean Crouzet)};
\node[step] (beziers) at (-10mm, -28mm) {};
\node[below] at (beziers) {\textbf{4. Béziers} (cath. St-Nazaire, 3 févr.)};
\node[step] (millau) at (-12mm, -14mm) {};
\node[right] at (millau) {\textbf{5. Millau} (3–5 févr.)};
\node[loc] (stflour) at (-14mm, -3mm) {};
\node[right] at (stflour) {St-Chély \& St-Flour};
\node[step] (clermont) at (-16mm, 7mm) {};
\node[right] at (clermont) {\textbf{6. Brioude \& Clermont-F\textsuperscript{d}} (6 févr.)};

\draw[aller] (amiens) -- (paris);
\draw[aller] (paris) to[bend right=18] node[pos=0.5, left]{\textit{Aller (27–28 janv.)}} (toulouse);
\draw[aller] (toulouse) -- (carca) -- (beziers) -- (millau);
\draw[retour] (millau) -- (stflour) -- (clermont) -- (paris) -- (amiens);

% Filet vertical
\draw[black!40, line width=0.4pt] (3mm,-38mm) -- (3mm,38mm);

% Partie droite : Plan vectoriel de Millau (4mm à 58mm)
\node[font=\fontsize{6.2pt}{7.2pt}\selectfont\bfseries] at (31mm, 37mm) {B. Lieux familiaux à Millau (3–5 févr. 1917)};
% Le Tarn et la Dourbie
\draw[black!35, line width=1.6pt] (8mm,-32mm) .. controls (22mm,-18mm) and (36mm,-10mm) .. (54mm,8mm)
  node[pos=0.75, below right, font=\fontsize{5.6pt}{6.5pt}\selectfont\itshape]{Le Tarn};
\draw[black!35, line width=1.1pt] (36mm,-10mm) -- (55mm,-24mm)
  node[pos=0.7, below left, font=\fontsize{5.5pt}{6.5pt}\selectfont\itshape]{La Dourbie};

\node[loc] (gare_m) at (16mm, 18mm) {};
\node[right] at (gare_m) {Gare de Millau (arrivée 3 févr., 22 h 30)};
\node[step] (guibert) at (22mm, 6mm) {};
\node[right] at (guibert) {\textbf{10, rue Alfred-Guibert} (maison Calmels)};
\node[loc] (barris) at (20mm, -2mm) {};
\node[right] at (barris) {\textbf{Rue des Barris} (maison natale Combes)};
\node[loc] (mandarous) at (24mm, 12mm) {};
\node[right] at (mandarous) {Place du Mandarous \& Bd de l'Ayrolle};
\node[step] (layral_m) at (26mm, -9mm) {};
\node[right] at (layral_m) {\textbf{Étude \& maison Layrals} (oncle \& tante Thérèse)};
\node[loc] (cimetiere) at (18mm, 26mm) {};
\node[right] at (cimetiere) {\textbf{Cimetière de Millau} (tombeaux familiaux, 5 févr.)};
\end{tikzpicture}
""",
    "VII": r"""
\begin{tikzpicture}[
  scale=0.96,
  every node/.style={font=\fontsize{6.0pt}{7.0pt}\selectfont},
  loc/.style={circle, fill=black, inner sep=1.1pt},
  hub/.style={circle, draw=bordeaux, fill=white, line width=0.85pt, inner sep=1.8pt},
  tour/.style={draw=bordeaux!85, line width=0.55pt, ->, >=stealth},
  advance/.style={draw=black!75, line width=0.65pt, dashed, ->, >=stealth},
  river/.style={draw=black!35, line width=1.1pt}
]
\draw[black!50, line width=0.4pt] (-60mm,-42mm) rectangle (60mm,42mm);
\fill[black!3] (-60mm,-42mm) rectangle (60mm,42mm);

% Rivières : l'Authie au nord, l'Ancre à l'est, l'Hallue au sud
\draw[river] (-52mm,30mm) -- (12mm,26mm) node[right]{\textit{L'Authie}};
\draw[river] (42mm,24mm) .. controls (34mm,6mm) and (30mm,-10mm) .. (22mm,-34mm) node[right]{\textit{L'Ancre}};

% Centre d'Hérissart (Army Purchase Board)
\node[hub] (herissart) at (-8mm, 0mm) {};
\node[above left] at (herissart) {\textbf{HÉRISSART (\textit{Purchase Board})}};

% Nord-Ouest : Doullens, Auxi-le-Château, Candas
\node[loc] (auxi) at (-48mm, 28mm) {};
\node[below right] at (auxi) {\textbf{Auxi-le-Château} (21 févr.)};
\node[loc] (doullens) at (-20mm, 26mm) {};
\node[right] at (doullens) {\textbf{Doullens} (achats \& cantine)};
\node[loc] (candas) at (-30mm, 14mm) {};
\node[left] at (candas) {Candas};
\node[loc] (raincheval) at (-10mm, 14mm) {};
\node[left] at (raincheval) {Raincheval \& Puchevillers};
\node[loc] (acheux) at (6mm, 16mm) {};
\node[above] at (acheux) {Acheux \& Bertrancourt};

% Ouest et Sud : Villers-Bocage, Talmas, Rubempré, Molliens, Beaucourt
\node[loc] (talmas) at (-36mm, -6mm) {};
\node[left] at (talmas) {Talmas \& \textbf{Villers-Bocage}};
\node[loc] (pierregot) at (-16mm, -8mm) {};
\node[left] at (pierregot) {Pierregot \& Mirvaux};
\node[loc] (rubempre) at (-8mm, -10mm) {};
\node[below] at (rubempre) {\textbf{Rubempré}};
\node[loc] (molliens) at (-14mm, -20mm) {};
\node[left] at (molliens) {Molliens-au-Bois};
\node[loc] (beaucourt) at (-4mm, -24mm) {};
\node[below] at (beaucourt) {\textbf{Beaucourt-sur-l'Hallue} \& Montigny (16 févr.)};

% Est : Toutencourt, Contay, Warloy, Senlis, Mesnil-Martinsart, Albert
\node[loc] (toutencourt) at (2mm, 6mm) {};
\node[right] at (toutencourt) {\textbf{Toutencourt} (Mission V\textsuperscript{e} Armée)};
\node[loc] (contay) at (6mm, -6mm) {};
\node[right] at (contay) {\textbf{Contay} \& Warloy-Baillon};
\node[loc] (senlis) at (18mm, -2mm) {};
\node[right] at (senlis) {\textbf{Senlis-le-Sec} (\textit{17th Lancers}, 21 mars)};
\node[loc] (mesnil) at (28mm, 4mm) {};
\node[right] at (mesnil) {\textbf{Le Mesnil-Martinsart} (famille Flutre, 13 mars)};
\node[loc] (albert) at (28mm, -12mm) {};
\node[right] at (albert) {\textbf{Albert}, Aveluy \& Buire-sur-l'Ancre};

% Nord-Est : Secteur du repli allemand (Miraumont, Achiet-le-Petit, Bapaume, Arras)
\node[loc] (miraumont) at (38mm, 18mm) {};
\node[right] at (miraumont) {\textbf{Miraumont}};
\node[loc] (achiet) at (40mm, 26mm) {};
\node[right] at (achiet) {\textbf{Achiet-le-Petit} (\textit{63rd Naval Div.}, 19 mars)};
\node[loc] (arras) at (36mm, 36mm) {};
\node[above] at (arras) {\textbf{Vers Bapaume \& Arras} (canonnade, avr. 1917)};

% Rayons et mouvements
\foreach \dest in {doullens,candas,raincheval,acheux,toutencourt,contay,senlis,mesnil,albert,rubempre,pierregot,molliens,beaucourt,talmas} {
  \draw[tour] (herissart) -- (\dest);
}
\draw[tour] (doullens) -- (auxi);
\draw[advance] (albert) -- (mesnil) -- (miraumont) -- (achiet) -- (arras);

\draw[line width=0.6pt] (-54mm,-36mm) -- (-34mm,-36mm);
\node[above] at (-44mm,-36mm) {0 \hfill 5 \hfill 10 km};
\draw[->, line width=0.6pt] (52mm, 28mm) -- (52mm, 37mm) node[above]{\textbf{N}};
\end{tikzpicture}
""",
}


# =============================================================================
# 3. INDEX DES NOMS DE PERSONNES (INDEX NOMINUM) & INDEX DES NOMS DE LIEUX (INDEX LOCORUM)
# =============================================================================

# Catalogue exhaustif des personnes nommées ou évoquées dans le carnet :
# (Entrée triée alphabétiquement, Notice d'identification, Regex dans lignes/titre/historique, Scans explicites additionnels)
INDEX_PERSONNES_CATALOG = [
    ("Alric, Marie Anaïs (1838–1907)", "mère d'Hippolyte Combes, épouse de François-Hippolyte Combes", r"\b(?:Maman|mère|Anaïs\s+Alric)\b", [92, 132, 143]),
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
    ("Calmels, D\\textsuperscript{r} Gabriel (1852–1921) \\& Valentine Cartairade (1858–1943)", "parents de Marguerite Calmels au 10, rue Alfred-Guibert à Millau", r"\bCalmels\b", [139, 141, 142, 143]),
    ("Calmels, Madeleine (1882–1961, \\textit{Mad\\textsuperscript{ne}})", "sœur aînée de Marguerite Calmels, épouse du D\\textsuperscript{r} Fernand Vincens", r"\b(?:Madeleine|Madne)\b", [134, 135, 141, 143]),
    ("Calmels, Marie Marguerite (1892–1974, \\textit{Marg\\textsuperscript{te}}, \\textit{M\\textsuperscript{te}}, \\textit{Gueïte})", "fiancée puis épouse d'Hippolyte Combes", r"\b(?:Margte|Marg\.|Mte|Marguerite|Gueïte|ma\s+Femme)\b", [2, 6, 19, 54, 55, 56, 57, 58, 59, 60, 62, 133, 134, 135, 136, 137, 138, 139, 141, 142, 143]),
    ("Calmels, Pierre", "frère de Marguerite Calmels à Millau", r"\bPierre\b", [139, 141, 143]),
    ("Capron, M\\textsuperscript{me}", "propriétaire d'une batteuse agricole à Beauquesne (Somme)", r"\bCapron\b", [115, 120]),
    ("Carluvant, M.", "maître tailleur et logeur d'Hippolyte Combes au n\\textsuperscript{o}~1, route de Léalvillers à Acheux", r"\bCarluvant\b", [94, 102, 118, 146, 147, 148]),
    ("Combes, François Augustin Hippolyte (1825–1899)", "avocat à Millau puis à Toulouse, père d'Hippolyte Combes", r"\bpère\b", [60, 143]),
    ("Combes, Françoise (1871–1942, \\textit{Sœur Marie de la Croix})", "sœur aînée d'Hippolyte Combes, carmélite à Périgueux", r"\bFrançoise\b", []),
    ("Combes, Joséphine (1873–1914, \\textit{Joseph\\textsuperscript{e}})", "sœur d'Hippolyte Combes, décédée à Nogent-le-Rotrou en octobre 1914", r"\b(?:Josephe|Joséphine)\b", [60]),
    ("Combes, Maria (1875–1903)", "sœur d'Hippolyte Combes, religieuse décédée à Carthage", r"\bMaria\b", []),
    ("Combes, Marie Lucien Hippolyte (1876–1970)", "auteur du \\textit{Livre-Journal}, professeur d'anglais et interprète auprès de l'Armée britannique (mention nominale autographe \\textit{Hipp\\textsuperscript{te}})", r"\bHippte\b", [1, 135]),
    ("Connelly", "soldat britannique, ordonnance (\\textit{groom}) d'Hippolyte Combes à la 152\\textsuperscript{e} Compagnie A.S.C.", r"\bConnelly\b", [12, 39, 41, 45, 74]),
    ("Croughton, Lieutenant", "officier britannique du service automobile et des achats", r"\bCroughton\b", [109, 150]),
    ("Crouzet, Abbé Jean", "cousin germain de Marguerite Calmels, prêtre à Toulouse (futur curé de la Dalbade)", r"\bJean\b", [54, 58, 60, 139]),
    ("Crouzet, Émile (1842–1921, \\textit{M.~C\\textsuperscript{zt}}, \\textit{Oncle}) \\& Élisabeth Calmels (\\textit{Tante})", "oncle et tante de Marguerite Calmels à Toulouse (rue du Taur et rue Pharaon)", r"\b(?:Crouzet|Czt\.?|Oncle|Tante)\b", [54, 55, 56, 58, 60, 62, 133, 137, 139]),
    ("Curtis, Lieutenant (\\textit{C\\textsuperscript{tis}})", "officier britannique d'approvisionnement et de fourrage (18\\textsuperscript{e} Division puis Acheux)", r"\b(?:Curtis|Ctis)\b", [2, 6, 13, 14, 19, 21, 22, 23, 30, 37, 45, 74, 87, 90, 96, 105]),
    ("Denis, Baptiste \\& famille", "famille d'Hérissart hôte d'Hippolyte Combes au printemps 1917", r"\bDenis\b", [178, 180, 182, 183, 184]),
    ("Donze, M\\textsuperscript{me}", "logeuse d'Hippolyte Combes à Lynde (Nord)", r"\bDonze\b", [5]),
    ("Dubois, D\\textsuperscript{r}", "médecin rencontré par Hippolyte Combes dans la Somme", r"\bDubois\b", [161]),
    ("Duchâteau, Victor \\& famille", "famille logeant Hippolyte Combes près du camp des briqueteries à Albert", r"\bDuchâteau\b", [80, 82, 87, 91, 93]),
    ("Faure, M\\textsuperscript{me} \\& ses enfants (Marguerite, Germaine, Marcel, Henri, André)", "cousines de Marguerite Calmels à Neuilly-sur-Seine (16, rue d'Armenonville)", r"\b(?:Faure|Marcel|Henri|André)\b", [52, 130, 131]),
    ("First, Lieutenant", "officier britannique à Forceville", r"\bFirst\b", [50]),
    ("Flutre, Fortuné \\& Louis-Fernand (1892–1978)", "instituteur du Mesnil-Martinsart et son fils élève de l'École normale supérieure", r"\bFlutre\b", [168]),
    ("Ford, Capitaine E.~M.", "officier britannique du \\textit{18th Divisional Train, A.S.C.}, décoré de la \\textit{Military Cross}", r"\bFord\b", [50, 76]),
    ("Gilbert, Second Lieutenant", "sous-lieutenant britannique originaire de Jersey, poète, attaché au \\textit{Purchase Board} à Hérissart", r"\bGilbert\b", [166, 179, 181, 185, 186]),
    ("Godard, Lieutenant", "jeune officier britannique du \\textit{Purchase Board} à Toutencourt et Hérissart", r"\bGodard\b", [166]),
    ("Grose, Lieutenant-Colonel Daniel Charles Evans", "commandant (\\textit{Officer Commanding}) le \\textit{18th Divisional Train, A.S.C.}", r"\bGrose\b", [90]),
    ("Guérin, Maurice de (1810–1839)", "poète tarnais étudié dans le cours public d'Ernest Zyromski à Toulouse", r"\bGuérin\b", [135]),
    ("Guibet, M.", "habitant de Raincheval (Somme)", r"\bGuibet\b", [121]),
    ("Guiraud", "tailleur à Toulouse", r"\bGuiraud\b", [61]),
    ("Houthouan, M. \\& famille", "exploitants agricoles belges de la ferme de Belle-Église à Arquèves (Somme)", r"\bHouthouan\b", [95, 108, 171]),
    ("Hughes, Major", "officier supérieur britannique au \\textit{18th Divisional Train}", r"\bHughes\b", [90, 96]),
    ("Huguet, Capitaine (\\textit{Cap.~H.})", "officier de la Mission militaire française auprès du XIII\\textsuperscript{e} Corps à Acheux", r"\b(?:Huguet|Cap\.\s*H\.)\b", [94, 105]),
    ("Imbert", "opticien à Paris", r"\bImbert\b", [116]),
    ("Jimmie", "conducteur britannique de l'automobile Vauxhall du service des achats", r"\bJimmie\b", [167]),
    ("Labit, Antoine (1832–1912) \\& Georges (1862–1899)", "fondateur du grand magasin toulousain \\textit{La Maison Universelle} et son fils", r"\bLabit\b", [134]),
    ("Layrals, M\\textsuperscript{e} Charles \\& Thérèse Cartairade (\\textit{Layral})", "notaire à Millau et son épouse, oncle et tante maternels de Marguerite Calmels", r"\bLayral\b", [142]),
    ("Lépin (ou \\textit{Liepin}, \\textit{Lupin})", "adjudant interprète à la Mission française de la 18\\textsuperscript{e} Division", r"\b(?:Lupin|Lépin|Liepin)\b", [23, 85, 90]),
    ("Lersay, M. de", "chirurgien-dentiste à Toulouse", r"\bLersay\b", [138, 140]),
    ("Levy, Major", "officier supérieur britannique dirigeant le service des achats (\\textit{Purchase Board}) dans la Somme", r"\bLevy\b", [91, 93, 110, 166]),
    ("Louis XI (1423–1483)", "roi de France, associé au chêne historique du beffroi de Lucheux (édit de 1464)", r"\bLouis\s+XI\b", [41]),
    ("Lovet, Capitaine", "officier britannique revu au \\textit{refilling point} près d'Albert", r"\bLovet\b", [151]),
    ("Maeterlinck, Maurice (1862–1949)", "écrivain belge, auteur du recueil \\textit{Les Débris de la guerre} (1916) acquis par Hippolyte Combes", r"\bMaeterlinck\b", [53]),
    ("Martin, Alexis", "auteur du guide illustré \\textit{Une visite à Amiens} rapporté à Hippolyte Combes", r"\bAlexis\s+Martin\b", [182]),
    ("Maurin", "collègue interprète militaire dans la vallée de la Lys", r"\bMaurin\b", [13, 24]),
    ("Maxse, Major-General Sir Ivor (1862–1958)", "commandant la 18\\textsuperscript{e} Division britannique (\\textit{18th Eastern Division}) de 1914 à janvier 1917", r"\bMaxse\b", [16]),
    ("Michel, Lieutenant", "officier britannique de cantonnement (\\textit{billeting officer}) à Lynde", r"\bLt\s+Michel\b", [3]),
    ("Monin", "collègue interprète retrouvé de passage à Hérissart", r"\bMonin\b", [173]),
    ("Morris, Lieutenant", "officier britannique ami d'Hippolyte Combes à la 150\\textsuperscript{e} Compagnie A.S.C.", r"\bMorris\b", [120, 121, 122]),
    ("Mortreux (famille)", "famille d'agriculteurs de Varennes (Somme) amie d'Hippolyte Combes", r"\bMortreux\b", [97, 184]),
    ("Moulard (ferme)", "exploitation agricole à Septenville (Rubempré, Somme)", r"\bMoulard\b", [120]),
    ("Newton", "militaire britannique mentionné à Forceville", r"\bNewton\b", [49]),
    ("Panton, Capitaine", "officier britannique de la 152\\textsuperscript{e} Compagnie A.S.C.", r"\bPanton\b", [47, 68, 74, 90]),
    ("Pfister", "horloger-bijoutier à Toulouse (rue d'Alsace-Lorraine / place Esquirol)", r"\bPfister\b", [133, 134, 135]),
    ("Pizzi, Lieutenant", "officier interprète chef du détachement français auprès de la 18\\textsuperscript{e} Division britannique", r"\bPizzi\b", [85, 90]),
    ("Raucoule", "collègue interprète militaire originaire du Midi", r"\bRaucoule\b", [88, 90]),
    ("Schumacher", "adjudant interprète au bureau de la Mission française de la 18\\textsuperscript{e} Division", r"\bSchumacher\b", [23, 83]),
    ("Serpin", "sous-officier interprète à la Mission française", r"\bSerpin\b", [90]),
    ("Spagnol, M\\textsuperscript{me}", "horticultrice-fleuriste à Nice ayant expédié un panier de fleurs à Toulouse", r"\bSpagnol\b", [134, 136, 158]),
    ("Valet", "interprète militaire français rattaché à la 2\\textsuperscript{e} Division australienne à Hérissart", r"\bValet\b", [164, 166]),
    ("Vauchel, M\\textsuperscript{me}", "exploitante agricole à Marquay (Pas-de-Calais)", r"\bVauchel\b", [37]),
    ("Vincens, D\\textsuperscript{r} Fernand, Germaine \\& Robert", "beau-frère, nièce et neveu de Marguerite Calmels à Millau", r"\b(?:Vincens|Fernand|Germaine|Robert)\b", [56, 141, 143]),
    ("Walsh, Lieutenant", "officier britannique du \\textit{18th Divisional Train, A.S.C.}", r"\bWalsh\b", [74, 120]),
    ("Wentworth, Lieutenant", "officier britannique du \\textit{Purchase Board} à Hérissart", r"\bWentworth\b", [166]),
    ("West, Capitaine E.~M.", "commandant la 152\\textsuperscript{e} Compagnie A.S.C., décoré de la \\textit{Military Cross}", r"\bWest\b", [39, 42, 48, 74]),
    ("Williams, Capitaine (\\textit{Cap.~W.}, \\textit{W\\textsuperscript{ms}})", "jeune officier britannique (\\textit{Foraging Officer}) à Acheux puis Hérissart de décembre 1916 à mars 1917", r"\b(?:Williams|Wms|Cap\.\s*W\.|Capt\.\s*W\.)\b", [105, 106, 108, 111, 115, 126, 148, 157, 164, 165]),
    ("Zyromski, Ernest (1862–1933)", "professeur de littérature française à la Faculté des lettres de Toulouse, auteur de \\textit{L'Orgueil humain}", r"\bZyromski\b", [53, 135]),
]


# Catalogue exhaustif des noms de lieux (Index locorum) :
INDEX_LIEUX_CATALOG = [
    ("Abbeville (Somme)", "chef-lieu d'arrondissement de la Somme", r"\bAbbeville\b", [181]),
    ("Acheux-en-Amiénois (Somme)", "chef-lieu de canton de la Somme, gare (\\textit{railhead} d'Acheux-Varennes), château et cantonnement d'Hippolyte Combes (nov. 1916 – févr. 1917)", r"\bAcheux\b", [43, 45, 50, 87, 90, 91, 92, 93, 94, 102, 105, 112, 116, 128, 147, 168]),
    ("Achiet-le-Petit (Pas-de-Calais)", "village au nord-est de Miraumont repris lors du repli allemand de mars 1917", r"\bAchiet\b", [170]),
    ("Albert (Somme)", "ville de la vallée de l'Ancre, basilique Notre-Dame de Brebières (\\textit{Vierge penchée}) et bivouac des briqueteries (\\textit{Brickfields})", r"\bAlbert\b", [78, 80, 81, 82, 83, 84, 85, 91, 93, 96, 151, 164, 171, 181]),
    ("Amiens (Somme)", "préfecture de la Somme, cathédrale Notre-Dame et nœud ferroviaire des permissions", r"\bAmiens\b", [51, 65, 119, 128, 129, 147, 182]),
    ("Ancre (vallée de l')", "affluent de la Somme traversant Miraumont, Albert, Aveluy, Buire, Ribemont et Heilly", r"\bAncre\b", [105, 181]),
    ("Antibes (Alpes-Maritimes)", "ville de la Côte d'Azur évoquée avec l'interprète Maurin", r"\bAntibes\b", [24]),
    ("Armentières (Nord)", "ville industrielle linière sur la Lys, bombardée par l'artillerie allemande", r"\bArmentières\b", [17, 19, 21, 22]),
    ("Arquèves \\& ferme de Belle-Église (Somme)", "commune du canton d'Acheux et ancienne commanderie exploitée par la famille Houthouan", r"\b(?:Arquèves|Belle[- ]Église)\b", [95, 108, 110, 111, 113, 125, 171, 179]),
    ("Arras (Pas-de-Calais)", "préfecture du Pas-de-Calais et secteur de l'offensive britannique d'avril 1917 (bataille de la Scarpe)", r"\bArras\b", [182]),
    ("Authie (Somme)", "village de la haute vallée de l'Authie au nord d'Acheux", r"\bAuthie\b", [109, 121]),
    ("Auxi-le-Château (Pas-de-Calais)", "chef-lieu de canton sur l'Authie visité en tournée", r"\bAuxi-le-Château\b", [158]),
    ("Aveluy (Somme)", "village et bois au nord d'Albert sur l'Ancre", r"\bAveluy\b", [151]),
    ("Bac-Saint-Maur (Pas-de-Calais)", "écart de Sailly-sur-la-Lys et écluse sur la Lys (\\textit{refilling point})", r"\bBac-S(?:ain)?t-Maur\b", [13, 14, 15, 18, 24]),
    ("Bailleul (Nord)", "ville de Flandre flamingante au pied des Monts, Grand-Place, beffroi et gare d'embarquement", r"\bBailleul\b(?!-aux-Cornailles)", [7, 8, 9, 10, 12, 27, 28]),
    ("Bailleul-aux-Cornailles (Pas-de-Calais)", "village du Ternois voisin de Marquay", r"\bBailleul-aux-Cornailles\b", [29]),
    ("Barlette (Somme)", "hameau de la commune de Ribeaucourt où cantonne la 152\\textsuperscript{e} Compagnie A.S.C.", r"\bBarlette\b", [67, 68]),
    ("Beaucourt-sur-l'Hallue (Somme)", "village et château au sud d'Hérissart", r"\bBeaucourt\b", [123, 155, 183]),
    ("Beaudricourt \\& hameau d'Oppy (Pas-de-Calais)", "commune et hameau du canton d'Avesnes-le-Comte, étape du 9–10 septembre 1916", r"\b(?:Beaudricourt|Oppy)\b", [39, 40]),
    ("Beaumont-Hamel (Somme)", "village du front de l'Ancre", r"\bBeaumont\b", [167]),
    ("Beauquesne (Somme)", "bourg du canton de Doullens", r"\bBeauquesne\b", [113, 115, 120, 178]),
    ("Beauval (Somme)", "bourg entre Doullens et Amiens, étape des 15–16 octobre 1916", r"\bBeauval\b", [74, 75, 76]),
    ("Bédarieux (Hérault)", "gare de bifurcation vers Millau sur la ligne des Causses", r"\bBédarieux\b", [139]),
    ("Bertrancourt (Somme)", "commune à l'est d'Acheux-en-Amiénois", r"\bBertrancourt\b", [92, 105, 121, 168]),
    ("Béziers (Hérault)", "ville du Languedoc visitée avec Marguerite Calmels (cathédrale Saint-Nazaire et terrasse sur l'Orb)", r"\bBéziers\b", [139]),
    ("Bouzincourt (Somme)", "village à l'ouest d'Albert où bivouaque la compagnie en octobre 1916", r"\bBouzincourt\b", [77, 78, 79, 80]),
    ("Bresle (Somme)", "village entre Warloy-Baillon et Albert", r"\bBresle\b", [181]),
    ("Brioude \\& Arvant (Haute-Loire)", "gares de la ligne des Cévennes lors du retour de Millau en février 1917", r"\b(?:Brioude|Arvant)\b", [145]),
    ("Buire-sur-l'Ancre (Somme)", "village de la vallée de l'Ancre en aval d'Albert", r"\bBuire\b", [105, 181]),
    ("Bus-lès-Artois (Somme)", "commune au nord-est d'Acheux-en-Amiénois", r"\bBus(?:-lès-Artois)?\b", [92, 100]),
    ("Cambrai (Nord)", "ville du Nord évoquée comme destination d'offensive au printemps 1917", r"\bCambrai\b", [185]),
    ("Canaples (Somme)", "commune et gare de ravitaillement (\\textit{railhead}) au nord d'Amiens", r"\bCanaples\b", [66]),
    ("Candas (Somme)", "commune entre Doullens et Rubempré", r"\bCandas\b", [167]),
    ("Carcassonne (Aude)", "escale ferroviaire où Hippolyte Combes et Marguerite Calmels embrassent l'abbé Jean Crouzet", r"\bCarcassonne\b", [139]),
    ("Clermont-Ferrand (Puy-de-Dôme)", "étape ferroviaire du retour de Millau le 6 février 1917", r"\bClermont\b", [145]),
    ("Coisy (Somme)", "village au sud-ouest de Rubempré", r"\bCoisy\b", [95]),
    ("Contay (Somme)", "village et château de la vallée de l'Hallue entre Toutencourt et Warloy", r"\bContay\b", [107, 161, 167, 171, 181, 184, 185]),
    ("Creil (Oise)", "nœud ferroviaire entre Amiens et Paris", r"\bCreil\b", [51, 65]),
    ("Domqueur (Somme)", "village du Ponthieu voisin de Ribeaucourt", r"\bDomqueur\b", [70]),
    ("Doullens (Somme)", "sous-préfecture de la Somme, église Notre-Dame, cantine militaire et commerces", r"\bDoullens\b", [66, 158, 179]),
    ("Englebelmer (Somme)", "village du front de l'Ancre évacué par ses habitants", r"\bEnglebelmer\b", [108, 110]),
    ("Erquinghem-Lys (Nord)", "commune de la vallée de la Lys en amont d'Armentières", r"\bErquinghem\b", [22]),
    ("Estaires (Nord)", "ville sur la Lys (église Saint-Vaast et hôtel de ville Renaissance détruits en 1918)", r"\bEstaires\b", [25]),
    ("Flandre", "plaine flamande et Flandre intérieure traversées en juillet–août 1916", r"\bFlandre\b", [2, 52]),
    ("Fleurbaix (Pas-de-Calais)", "village du front au sud d'Armentières", r"\bFleurbaix\b", [21, 22]),
    ("Forceville (Somme)", "village au sud-est d'Acheux-en-Amiénois, cantonnement de septembre 1916", r"\bForceville\b", [45, 48, 49, 50, 96]),
    ("Franvillers (Somme)", "commune sur la route d'Albert à Amiens", r"\bFranvillers\b", [105]),
    ("Fréchencourt (Somme)", "village de la vallée de l'Hallue", r"\bFréchencourt\b", [161]),
    ("Harponville (Somme)", "village entre Toutencourt et Warloy-Baillon", r"\bHarponville\b", [110, 178, 184]),
    ("Hazebrouck (Nord)", "sous-préfecture du Nord, église Saint-Éloi et nœud ferroviaire", r"\bHazebrouck\b", [4, 5, 27]),
    ("Hébuterne (Pas-de-Calais)", "secteur du front au nord d'Acheux et de Serre", r"\bHébuterne\b", [116]),
    ("Hédauville (Somme)", "village entre Forceville et Warloy-Baillon (bivouac de la 150\\textsuperscript{e} Compagnie A.S.C.)", r"\bHédauville\b", [45, 121]),
    ("Heilly (Somme)", "village de la vallée de l'Ancre où Hippolyte Combes avait cantonné durant l'hiver 1915–1916", r"\bHeilly\b", [105]),
    ("Hénencourt (Somme)", "village et château entre Warloy-Baillon et Albert", r"\bHénencourt\b", [181]),
    ("Hérissart (Somme)", "commune du canton d'Acheux, siège du \\textit{Purchase Board} et résidence d'Hippolyte Combes de février à avril 1917 (logements n\\textsuperscript{os}~104, 220 et 216)", r"\bHérissart\b", [95, 104, 148, 149, 150, 152, 155, 157, 160, 164, 166, 168, 170, 172, 178, 186]),
    ("Jersey (île anglo-normande)", "patrie du sous-lieutenant poète Gilbert", r"\bJersey\b", [179]),
    ("La Croix-du-Bac (Steenwerck, Nord)", "hameau de la vallée de la Lys, église Notre-Dame-des-Sept-Douleurs et cantonnement d'août 1916", r"\bCroix-du-Bac\b", [10, 12, 13, 14]),
    ("Lardenne \\& Purpan-Ancely (Toulouse, Haute-Garonne)", "faubourg occidental de Toulouse et ruines de l'amphithéâtre gallo-romain", r"\bLardenne\b", [136, 137]),
    ("Laviéville (Somme)", "village entre Warloy-Baillon et Albert", r"\bLavieville\b|\bLaviéville\b", [181]),
    ("Le Mesnil-Martinsart (Somme)", "commune du canton d'Albert où enseignent M. et M\\textsuperscript{me} Fortuné Flutre", r"\bMesnil\b", [104, 168]),
    ("Le Quesnoy (ferme, Somme)", "écart agricole entre Raincheval et Puchevillers", r"\bQuesnoy\b", [111, 113, 115, 116, 118]),
    ("Léalvillers (Somme)", "village immédiatement voisin d'Acheux-en-Amiénois", r"\bLéalvillers\b", [94, 102, 116]),
    ("Ligny-Saint-Flochel (Pas-de-Calais)", "village du Ternois à l'église gothique classée (XV\\textsuperscript{e}–XVI\\textsuperscript{e}~s.)", r"\bLigny\b", [33]),
    ("Louvencourt (Somme)", "commune au nord d'Acheux-en-Amiénois", r"\bLouvencourt\b", [92, 116, 121]),
    ("Lucheux (Somme)", "bourg de la vallée de la Grouches (ruines du château des comtes de Saint-Pol et beffroi au chêne de Louis~XI)", r"\bLucheux\b", [41]),
    ("Lynde (Nord)", "village de Flandre intérieure entre Renescure et Hazebrouck, premier cantonnement du carnet", r"\bLynde\b", [2, 3, 5]),
    ("Lys (vallée de la)", "rivière franco-belge canalisée entre Aire, Estaires, Sailly, Bac-Saint-Maur et Armentières", r"\bLys\b", [13, 16, 18, 25]),
    ("Marquay (Pas-de-Calais)", "commune du Ternois, cantonnement de la compagnie du 25 août au 9 septembre 1916", r"\bMarquay\b", [28, 29, 30, 31, 34, 37, 39]),
    ("Martinsart (Somme)", "hameau et château de la commune du Mesnil-Martinsart près d'Albert", r"\bMartinsart\b", [104, 150]),
    ("Millau (Aveyron)", "ville natale d'Hippolyte Combes et de Marguerite Calmels (10, rue Alfred-Guibert ; rue des Barris ; cimetière)", r"\bMillau\b", [1, 139, 140, 141, 142, 143, 144]),
    ("Miraumont (Somme)", "village aux sources de l'Ancre évacué par l'armée allemande en février–mars 1917", r"\bMiraumont\b", [170]),
    ("Mirvaux (Somme)", "village voisin de Pierregot et Rubempré", r"\bMirvaux\b", [185]),
    ("Molliens-au-Bois (Somme)", "commune du canton de Villers-Bocage", r"\bMolliens\b", [158, 167]),
    ("Mont-Noir (Nord)", "colline des Monts des Flandres au nord de Saint-Jans-Cappel", r"\bMont[- ]Noir\b", [6]),
    ("Montauban (Tarn-et-Garonne)", "ville traversée en train lors des permissions et futur poste d'Hippolyte Combes au lycée Ingres", r"\bMontauban\b", [54]),
    ("Montigny-sur-l'Hallue (Somme)", "village voisin de Beaucourt-sur-l'Hallue", r"\bMontigny\b", [123, 158, 161, 183]),
    ("Neuilly-sur-Seine (Hauts-de-Seine)", "résidence de la famille Faure (16, rue d'Armenonville) visitée lors des permissions", r"\bNeuilly\b", [52, 130, 131]),
    ("Nice (Alpes-Maritimes)", "ville d'où provient le panier de fleurs commandé chez M\\textsuperscript{me} Spagnol", r"\bNice\b", [134, 136, 158]),
    ("Nogent-le-Rotrou (Eure-et-Loir)", "ville du Perche où Hippolyte Combes enseignait au collège communal (17, rue Saint-Hilaire)", r"\bNogent\b", [23, 24]),
    ("Ostreville (Pas-de-Calais)", "village du Ternois entre Marquay et Saint-Pol", r"\bOstreville\b", [32]),
    ("Paris", "capitale traversée aux permissions de septembre–octobre 1916 et janvier–février 1917 (gare du Nord, gare d'Orsay, boulevard Saint-Germain, boulevard Saint-Michel, rue Saint-Jacques, Panthéon, église Saint-Vincent-de-Paul)", r"\b(?:Paris|St-Germain|St-Jacques|Panthéon|St-Vincent-de-Paul|Gare\s+du\s+Nord|Gare\s+d'Orsay)\b", [52, 53, 63, 65, 116, 130, 131, 132, 145, 146]),
    ("Pech-David \\& Pouvourville (Toulouse, Haute-Garonne)", "coteaux dominant le sud de Toulouse et la Garonne", r"\b(?:Pouvourville|Pech\s+David)\b", [55]),
    ("Pierregot (Somme)", "village à l'ouest de Rubempré", r"\bPierregot\b", [104, 184, 185]),
    ("Puchevillers (Somme)", "commune entre Raincheval et Hérissart, centre d'hôpitaux d'évacuation britanniques (\\textit{Casualty Clearing Stations})", r"\bPuchevillers\b", [104, 110, 125, 155, 158, 166, 167, 168, 171, 172, 173, 184]),
    ("Raincheval (Somme)", "commune et château au nord d'Hérissart, cantonnement de septembre 1916 et siège de l'\\textit{Army Purchase Board}", r"\bRaincheval\b", [41, 42, 43, 44, 47, 91, 93, 104, 111, 113, 116, 121, 125, 155, 166, 167]),
    ("Ramecourt (Pas-de-Calais)", "commune et plateau à l'ouest de Saint-Pol-sur-Ternoise", r"\bRamecourt\b", [32]),
    ("Renescure (Nord)", "bourg de Flandre intérieure (château de Zuthove, château dit de Philippe de Comines et église Notre-Dame-de-l'Assomption)", r"\bRenescure\b", [4]),
    ("Ribeaucourt (Somme)", "commune et château du Ponthieu où la compagnie prend son repos du 6 au 15 octobre 1916", r"\bRibeaucourt\b", [67, 68, 69, 71, 72, 73, 74, 75]),
    ("Ribemont-sur-Ancre (Somme)", "village de la vallée de l'Ancre en aval d'Albert", r"\bRibemont\b", [105, 181]),
    ("Roëllecourt (Pas-de-Calais)", "village du Ternois entre Saint-Pol et Marquay", r"\b(?:Roellecourt|Roëllecourt)\b", [35]),
    ("Roumanie", "royaume entré en guerre aux côtés des Alliés le 27 août 1916", r"\bRoumanie\b", [30]),
    ("Rubempré \\& Septenville (Somme)", "chef-lieu de commune et hameau voisins d'Hérissart", r"\b(?:Rubempré|Septenville)\b", [95, 104, 120, 161, 172, 173, 178, 181]),
    ("Sailly-sur-la-Lys (Pas-de-Calais)", "commune de la vallée de la Lys (pont, écluse et ruines de l'église Saint-Vaast)", r"\bSailly\b", [16]),
    ("Saint-Chély-d'Apcher (Lozère)", "ville de Lozère traversée sur la ligne des Causses (et où Hippolyte Combes décédera à l'Hôtel du Centre le 2 septembre 1970)", r"\bSt-Chély\b", [1, 145]),
    ("Saint-Flour (Cantal)", "sous-préfecture du Cantal traversée sous la neige le 6 février 1917", r"\bSt-Flour\b|\bSaint-Flour\b", [145]),
    ("Saint-Jans-Cappel (Nord)", "village au pied du Mont-Noir où cantonne Hippolyte Combes du 28 juillet au 5 août 1916", r"\b(?:St-Jans-Cappel|Saint-Jans-Cappel)\b", [5, 6, 7, 10, 11, 12]),
    ("Saint-Léger-lès-Authie (Somme)", "village de la vallée de l'Authie", r"\bSt-Léger\b", [109]),
    ("Saint-Michel-sur-Ternoise (Pas-de-Calais)", "village et église ancienne à l'est de Saint-Pol-sur-Ternoise", r"\bSt-Michel\b", [32, 37]),
    ("Saint-Pol-sur-Ternoise (Pas-de-Calais)", "sous-préfecture du Pas-de-Calais, gare de débarquement et église des Carmes (1697)", r"\b(?:St-Pol|Saint-Pol)\b", [27, 28, 32, 34, 36, 37]),
    ("Senlis-le-Sec (Somme)", "village entre Warloy-Baillon et Bouzincourt", r"\bSenlis\b", [87, 96, 151, 171, 181]),
    ("Sercus (Nord)", "village de Flandre intérieure et église Saint-Érasme visités le 25 juillet 1916", r"\bSercus\b", [2]),
    ("Steenwerck (Nord)", "bourg de la plaine de la Lys, gare et église Saint-Jean-Baptiste", r"\bSteenwerck\b", [10, 12, 14, 15, 24, 26]),
    ("Talmas (Somme)", "commune sur la route d'Amiens à Doullens", r"\bTalmas\b", [162]),
    ("Thièvres (Somme / Pas-de-Calais)", "village de la vallée de l'Authie entre Lucheux et Raincheval", r"\bThièvres\b", [41]),
    ("Toulouse (Haute-Garonne)", "métropole languedocienne où séjournent Hippolyte Combes et Marguerite Calmels lors des deux permissions (rue du Taur, rue Pharaon, cathédrale Saint-Étienne, basilique Saint-Sernin, Daurade, Dalbade, Hôtel d'Assézat, Faculté des lettres, Sainte-Marie-des-Champs, Capitole, place Esquirol, marché Victor-Hugo, canal du Midi)", r"\b(?:Toulouse|St-Etienne|St-Sernin|Dalbade|Daurade|Assézat|Esquirol|Ste-Marie-des-Champs)\b", [54, 55, 56, 57, 58, 59, 60, 61, 62, 64, 132, 133, 134, 135, 136, 137, 138, 139, 140]),
    ("Toutencourt (Somme)", "commune entre Raincheval et Contay, siège de la Mission militaire française auprès de la V\\textsuperscript{e} Armée britannique", r"\bToutencourt\b", [105, 110, 111, 150, 155, 160, 164, 166, 167, 178]),
    ("Vadencourt (Somme)", "village et château voisins de Contay", r"\bVadencourt\b", [107]),
    ("Varennes-en-Croix (Somme)", "commune voisine d'Acheux-en-Amiénois (famille Mortreux)", r"\bVarennes\b", [50, 96, 97, 121, 184]),
    ("Villers-Bocage (Somme)", "chef-lieu de canton entre Amiens et Doullens", r"\bVillers-Bocage\b", [162]),
    ("Warloy-Baillon (Somme)", "bourg entre Contay et Senlis-le-Sec", r"\bWarloy\b", [76, 96, 171, 179, 181]),
    ("Ypres (Belgique)", "ville martyre de Flandre occidentale (cartes postales acquises à Renescure)", r"\bYpres\b", [4]),
]


def _collect_scans_for_entry(records: list[dict], regex_pat: str, explicit_scans: list[int]) -> list[int]:
    matched = set(explicit_scans)
    for r in records:
        n = r["scan_num"]
        haystack = "\n".join(r["lines"]) + "\n" + r["title"] + "\n" + r["lieu"]
        if re.search(regex_pat, haystack):
            matched.add(n)
    return sorted(matched)


def build_indexes_latex(records: list[dict]) -> str:
    """
    Construit le code LaTeX des deux index finaux :
    1. Index des noms de personnes (Index nominum)
    2. Index des noms de lieux (Index locorum)
    Chaque occurrence cite à la fois le folio du carnet (f° X r°/v°) et la page
    exacte du fichier PDF généré (p. \\pageref{fol:N}).
    """
    person_items = []
    for headword, desc, pat, explicit in INDEX_PERSONNES_CATALOG:
        scans = _collect_scans_for_entry(records, pat, explicit)
        if scans:
            refs = ", ".join(folio_fr_ref(s) for s in scans)
        else:
            refs = r"Prolégomènes \& Annexe~I (p.~\pageref{annexe:doc1}--\pageref{annexe:doc5})"
        person_items.append(
            f"\\noindent\\hangindent=4.5mm\\textbf{{{headword}}}, {desc} : {refs}.\\par\\vspace{{0.55mm}}"
        )

    place_items = []
    for headword, desc, pat, explicit in INDEX_LIEUX_CATALOG:
        scans = _collect_scans_for_entry(records, pat, explicit)
        if not scans:
            continue
        refs = ", ".join(folio_fr_ref(s) for s in scans)
        place_items.append(
            f"\\noindent\\hangindent=4.5mm\\textbf{{{headword}}}, {desc} : {refs}.\\par\\vspace{{0.55mm}}"
        )

    persons_joined = "\n".join(person_items)
    places_joined = "\n".join(place_items)

    return f"""
% =============================================================================
% INDEX DES NOMS DE PERSONNES (INDEX NOMINUM) ET INDEX DES NOMS DE LIEUX (INDEX LOCORUM)
% =============================================================================
\\cleardoublepage
\\chapter*{{Index des noms de personnes (\\textit{{Index nominum}})}}
\\addcontentsline{{toc}}{{chapter}}{{Index des noms de personnes (\\textit{{Index nominum}})}}
\\markboth{{Index des noms de personnes}}{{Index des noms de personnes}}
{{\\fontsize{{7.0pt}}{{8.3pt}}\\selectfont
\\noindent Chaque entrée renvoie simultanément à la foliotation du \\textit{{Livre-Journal}} (\\texttt{{f\\textsuperscript{{o}}~X~r\\textsuperscript{{o}}/v\\textsuperscript{{o}}}}) et à la pagination exacte de la présente édition (\\texttt{{p.~Y}}).\\par\\vspace{{2.0mm}}
{persons_joined}
\\par}}

\\cleardoublepage
\\chapter*{{Index des noms de lieux (\\textit{{Index locorum}})}}
\\addcontentsline{{toc}}{{chapter}}{{Index des noms de lieux (\\textit{{Index locorum}})}}
\\markboth{{Index des noms de lieux}}{{Index des noms de lieux}}
{{\\fontsize{{7.0pt}}{{8.3pt}}\\selectfont
\\noindent Chaque toponyme renvoie simultanément au folio du \\textit{{Livre-Journal}} (\\texttt{{f\\textsuperscript{{o}}~X~r\\textsuperscript{{o}}/v\\textsuperscript{{o}}}}) et au numéro de page correspondant du présent volume (\\texttt{{p.~Y}}).\\par\\vspace{{2.0mm}}
{places_joined}
\\par}}
"""
