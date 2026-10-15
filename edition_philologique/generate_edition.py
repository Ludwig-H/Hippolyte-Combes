# -*- coding: utf-8 -*-
"""
Generates the complete scientific philological LaTeX edition:
  /workspaces/Hippolyte-Combes/edition_philologique/carnet_hippolyte_combes.tex
modeled on Louis Hauseux's edition of Aristophanes' Thesmophories:
- Pure white, sober black-and-white typographic design (no cream/yellow backgrounds or colored boxes).
- Vis-à-vis spreads for all 186 scans:
  * Left page (even/verso): Diplomatic transcription with line numbers every 5 lines +
    horizontally aligned marginal critical apparatus + two unnamed but visually distinct
    bottom commentary registers separated by horizontal rules and typographic indentation.
  * Right page (odd/recto): Full-page facsimile scan with archival header and caption.
- Organized into 7 coherent chapters, each preceded by an analytical summary, historical
  and philological introduction, and archival/family/military illustrations.
"""

import os
import re
import json
from pathlib import Path

ROOT = str(Path(__file__).resolve().parent.parent)
JSON_PATH = os.path.join(ROOT, "transcriptions", "transcription_integrale_186_scans.json")
OUT_TEX = os.path.join(ROOT, "edition_philologique", "carnet_hippolyte_combes.tex")
SUPERSCRIPTS = {"ᵉ": "e", "ᵗ": "t", "ʳ": "r", "ᵈ": "d", "ⁿ": "n", "ˢ": "s", "ᵃ": "a", "ᵒ": "o"}


def escape_diplomatic_line(s):
    """Escapes a diplomatic transcription line for LaTeX while preserving \\hfill and \\dots."""
    s = s.replace("½", "1/2")
    for char in SUPERSCRIPTS:
        s = s.replace(char, f"@@SUP{ord(char)}@@")
    s = s.replace("\\hfill", "@@HFILL@@").replace("\\dots", "@@DOTS@@")
    s = s.replace("⟦", "@@LDEL@@").replace("⟧", "@@RDEL@@")
    s = s.replace("\\", "\\textbackslash{}")
    s = s.replace("&", "\\&")
    s = s.replace("%", "\\%")
    s = s.replace("$", "\\$")
    s = s.replace("#", "\\#")
    s = s.replace("_", "\\_")
    s = s.replace("{", "\\{")
    s = s.replace("}", "\\}")
    s = s.replace("~", "\\textasciitilde{}")
    s = s.replace("^", "\\textasciicircum{}")
    s = s.replace("@@HFILL@@", "\\hfill{}")
    s = s.replace("@@DOTS@@", "\\dots{}")
    s = s.replace("@@LDEL@@", "$[\\![$")
    s = s.replace("@@RDEL@@", "$]\\!]$")
    for char, letter in SUPERSCRIPTS.items():
        s = s.replace(f"@@SUP{ord(char)}@@", "\\textsuperscript{" + letter + "}")
    return s


def sanitize_latex_fragment(s):
    """
    Sanitizes a commentary or marginal note string that may already contain LaTeX commands
    (\\textbf, \\textit, \\texttt, \\&, \\#, \\_) or plain text.
    """
    s = s.replace("½", "1/2")
    for char, letter in SUPERSCRIPTS.items():
        s = s.replace(char, "\\textsuperscript{" + letter + "}")
    s = s.replace("$\\rightarrow$", "$\\rightarrow$").replace("\\rightarrow", "$\\rightarrow$")
    s = re.sub(r"\$\s*\$(?:\\rightarrow)\$\s*\$", r"$\\rightarrow$", s)
    s = re.sub(r"\^([a-zA-Z0-9]+)\^", r"\\textsuperscript{\1}", s)
    s = s.replace("^", "")
    s = s.replace("$\\llbracket$", "\\llbracket").replace("$\\rrbracket$", "\\rrbracket")
    s = s.replace("$\\llbracket", "\\llbracket").replace("\\rrbracket$", "\\rrbracket")
    s = s.replace("\\llbracket ", "$[\\![$").replace("\\llbracket", "$[\\![$")
    s = s.replace("\\rrbracket\\", "$]\\!]\\ $").replace("\\rrbracket", "$]\\!]$")
    s = s.replace("⟦", "$[\\![$").replace("⟧", "$]\\!]$")
    s = re.sub(r"(?<!\\)&", r"\\&", s)
    s = re.sub(r"(?<!\\)%", r"\\%", s)
    s = re.sub(r"(?<!\\)#", r"\\#", s)
    s = re.sub(r"(?<!\\)_", r"\\_", s)
    s = s.replace("20251126\\_", "20251126\\_\\allowbreak ")
    return s


CHAPTERS = [
    {
        "num": "I",
        "title": "De la Flandre intérieure à la vallée de la Lys",
        "subtitle": "Renescure, Hazebrouck, Saint-Jans-Cappel, Bailleul et La Croix-du-Bac (25 juillet – 12 août 1916)",
        "scan_start": 1,
        "scan_end": 18,
        "summary": "La couverture ouvre le dossier (vue \\#001). Les entrées suivantes décrivent le cantonnement d'officiers à Sercus, les tournées de fourrage avec Curtis à Lynde, les visites de Renescure, Hazebrouck et Bailleul, puis l'installation au hameau de La Croix-du-Bac (Steenwerck) dans la vallée de la Lys. Le bombardement d'Armentières du 11 août et les biffures relatives à un soldat condamné demandent une lecture prudente (vue \\#017).",
        "intro": "Relevée de la Somme le 20 juillet 1916 après les combats du bois des Trônes, la \\textit{18th (Eastern) Division} du major-général Sir Ivor Maxse gagne la Flandre intérieure avant de tenir le secteur de la Lys autour d'Armentières et de Fleurbaix (Capt. G. H. F. Nichols, \\textit{The 18th Division in the Great War}, 1922, p. 81--85). Ce contexte divisionnaire éclaire les déplacements de Combes, détaché depuis août 1915 auprès d'une compagnie d'\\textit{Army Service Corps} (lettre du 21 février 1916 ; \\textit{152nd Company A.S.C.} et \\textit{54th Brigade} à la vue \\#066). Il mentionne les \\textit{Royal Fusiliers} aux vues \\#002--\\#003, sans numéro de bataillon, décrit le clocher de Sercus (vue \\#002), deux châteaux qu'il qualifie du Moyen Âge à Renescure (vue \\#004) et l'architecture flamande de Bailleul (vues \\#008--\\#009). À la vue \\#016, il parle du général Maxse avec un éclusier ; il ne rapporte pas de rencontre avec le général.",
        "illustrations": [
            [
                "illustrations/hippolyte_interprete_1.jpg",
                "Hippolyte Combes en uniforme d'interprète militaire attaché à l'Armée britannique (képi à bandeau et insignes de col au sphinx). Collection familiale Combes.",
                "0.46\\textwidth"
            ],
            [
                "illustrations/toulon_artillerie_1915.jpg",
                "Hippolyte Combes au 10\\textsuperscript{e} régiment d'artillerie à pied à Toulon (Saint-Jean-du-Var) au printemps 1915.",
                "0.46\\textwidth"
            ]
        ]
    },
    {
        "num": "II",
        "title": "De la vallée de la Lys à l’Artois et à la Somme",
        "subtitle": "Armentières, Estaires, Marquay, Saint-Pol, Raincheval, Acheux et Forceville (13 août – 24 septembre 1916)",
        "scan_start": 19,
        "scan_end": 49,
        "summary": "Les vues \\#019 à \\#049 couvrent les dernières journées dans la vallée de la Lys (Fleurbaix, Armentières, Estaires), le transfert ferroviaire du 25 août par Bailleul et Saint-Pol vers la Ternoise (Marquay, Ligny-Saint-Flochel, Saint-Michel, Roëllecourt), puis la marche d'approche vers la Somme par Lucheux, Beauval, Raincheval, Acheux et Forceville à la veille de l'offensive de Thiepval.",
        "intro": "Le lexique technique des services britanniques s'entrelace à la phrase française : \\textit{mess}, \\textit{billet}, \\textit{refilling point}, \\textit{green forage}, \\textit{groom}, \\textit{orderly}. Combes arrive à Marquay le 25 août (vues \\#027--\\#028) et en repart le 9 septembre (vue \\#039). L'historique divisionnaire replace ce séjour dans la préparation de la 18\\textsuperscript{e} Division, qui rejoint le \\textit{II Corps} (Lt.-Gen. Sir Claud Jacob) au sein de la \\textit{Reserve Army} du général Sir Hubert Gough avant l'assaut de Thiepval Ridge du 26 septembre 1916 (Nichols, \\textit{op. cit.}, p. 86--92). Les descriptions monumentales appellent une confrontation avec les sources patrimoniales : la mention de Louis XI et d'un édit de 1464 à Lucheux se trouve à la vue \\#041 ; son attribution historique reste à distinguer du témoignage de Combes.",
        "illustrations": [
            [
                "illustrations/hippolyte_interprete_2.jpg",
                "Portrait en buste d'Hippolyte Combes sur le front britannique (1916--1917), portant les insignes métalliques d'interprète détaché auprès de la B.E.F.",
                "0.42\\textwidth"
            ],
            [
                "illustrations/hippolyte_1897.jpg",
                "Hippolyte Combes jeune homme en 1897 (à l'âge de vingt et un ans), étudiant à Toulouse avant son séjour de quatre ans à Nottingham.",
                "0.42\\textwidth"
            ]
        ]
    },
    {
        "num": "III",
        "title": "La première permission : Paris et Toulouse",
        "subtitle": "Permission et retour vers la Somme (25 septembre – 6 octobre 1916)",
        "scan_start": 50,
        "scan_end": 66,
        "summary": "Les vues \\#050 à \\#066 suivent le départ en permission le 25 septembre 1916, les étapes parisiennes (déjeuner à Neuilly chez Mme Faure, achats au Quartier latin), le séjour à Toulouse auprès de Marguerite Calmels et de la famille Crouzet, puis le retour au front le 6 octobre auprès de la \\textit{152nd Company A.S.C.}.",
        "intro": "L'ordre des photographies diffère ponctuellement de l'ordre des dates : la vue \\#063 porte le 5 octobre, la vue \\#064 revient au 4 octobre. L'édition conserve l'ordre des fichiers et signale ce décalage. Les archives familiales (\\texttt{Combes-annexe.DOC}) éclairent le cercle toulousain : l'oncle Émile Crouzet, son épouse Élisabeth Calmels et leur fils l'abbé Jean Crouzet. Elles documentent aussi les Faure à Neuilly, 16 rue d'Armenonville, tout en réservant leur degré de parenté. Le carnet mentionne les achats de Maurice Maeterlinck (\\textit{Les Débris de la guerre}, 1916) et d'Ernest Zyromski (\\textit{L'Orgueil humain}, 1904), ainsi que la visite à l'église Saint-Vincent-de-Paul à Paris (vue \\#063). Aucune visite au musée Georges-Labit n'est établie par les vues \\#057--\\#058.",
        "illustrations": [
            [
                "illustrations/marguerite_1917.jpg",
                "Marguerite Calmels (1892--1974), photographiée par le studio Jublin à Millau à l'époque de ses fiançailles avec Hippolyte Combes.",
                "0.42\\textwidth"
            ],
            [
                "illustrations/maison_millau.jpg",
                "La demeure familiale de Millau (Aveyron), berceau de la famille Combes.",
                "0.46\\textwidth"
            ]
        ]
    },
    {
        "num": "IV",
        "title": "L’automne dans la Somme : Albert et Acheux",
        "subtitle": "Ribeaucourt, Warloy-Baillon, Albert et Acheux (6 octobre – 30 novembre 1916)",
        "scan_start": 67,
        "scan_end": 104,
        "summary": "Les vues \\#067 à \\#104 relatent le retour sur le front de la Somme : repos de la compagnie dans les environs de Ribeaucourt, déplacement vers Albert, bivouac sous la tente et boue, description de la basilique Notre-Dame de Brebières mutilée et de la Vierge penchée, puis installation à Acheux-en-Amiénois pour le service des réquisitions et du fourrage.",
        "intro": "Pendant que la 18\\textsuperscript{e} Division combat devant la redoute Schwaben, la tranchée Regina et l'Ancre (octobre--novembre 1916), le \\textit{18th Divisional Train}, commandé par le lieutenant-colonel Daniel Charles Evans Grose (\\texttt{Col. Grose}, vue \\#090), assure le ravitaillement depuis Albert, Warloy-Baillon et Acheux. À partir de la fin d'octobre, Combes est détaché au service des achats et réquisitions de paille et de fourrage (\\textit{Foraging}) dans les communes de l'arrière-front picard (Varennes, Léalvillers, Louvencourt, Arquèves, Bertrancourt, Bus-lès-Artois). Les vues \\#091 et \\#093 reproduisent la même page manuscrite sous deux prises de vue.",
        "illustrations": [
            [
                "illustrations/fiche_matricule.jpg",
                "Extrait du registre matricule d'Hippolyte Combes (classe 1896, matricule 911, bureau de recrutement de Toulouse) détaillant ses services auprès de la Mission militaire française attachée à l'Armée britannique (4 mai 1915 -- 11 novembre 1918).",
                "0.78\\textwidth"
            ]
        ]
    },
    {
        "num": "V",
        "title": "L’hiver 1916–1917 à Acheux",
        "subtitle": "Williams, tournées, Noël et gel de janvier (1er décembre 1916 – 25 janvier 1917)",
        "scan_start": 105,
        "scan_end": 127,
        "summary": "Les vues \\#105 à \\#127 présentent l'arrivée du capitaine Williams (\\textit{Foraging Officer}), les tournées quotidiennes de réquisition dans les villages de la Somme et du Pas-de-Calais, les tensions de caractère avec Williams et le grand gel de janvier 1917. La vue \\#121 signale le 9 janvier une visite à la \\textit{150th Company A.S.C.}, près d'Hédauville ; elle n'établit pas une affectation de trois jours à cette compagnie.",
        "intro": "Les jugements portés sur le capitaine Williams relèvent du témoignage subjectif du diariste ; le commentaire distingue scrupuleusement les paroles rapportées, l'humeur de Combes et les faits institutionnels documentés (comme l'organisation du \\textit{18th Divisional Train} entre la \\textit{152nd} et la \\textit{150th Company A.S.C.}, et l'installation du \\textit{Fifth Army School of Mortars} au château d'Acheux après le départ du \\textit{XIII Corps} et l'extension de la \\textit{Fifth Army} en novembre--décembre 1916). Les vues \\#112 (24 décembre) et \\#113 (23 décembre) ont été photographiées dans l'ordre inverse de la chronologie.",
        "illustrations": [
            [
                "illustrations/camarades_ailly_1919.jpg",
                "Souvenir de camaraderie militaire sur le front de Picardie (carte-photo dédicacée à Hippolyte Combes, Ailly-sur-Noye, mai 1919). Collection familiale.",
                "0.50\\textwidth"
            ]
        ]
    },
    {
        "num": "VI",
        "title": "La deuxième permission : Toulouse et Millau",
        "subtitle": "Étapes par Amiens et Neuilly, séjour à Toulouse et Millau (26 janvier – 7 février 1917)",
        "scan_start": 128,
        "scan_end": 146,
        "summary": "Les vues \\#128 à \\#146 suivent la permission d'hiver : trajet par Amiens et Neuilly-sur-Seine, séjour à Toulouse auprès de Marguerite Calmels (cours public d'Ernest Zyromski sur Maurice de Guérin, achats de bagues et montre en or chez Pfister), voyage en train avec Marguerite jusqu'à Millau (10 rue Alfred-Guibert, visites aux familles Calmels, Vincens et Layral, recueillement au cimetière), puis retour au front par le Massif central (Saint-Flour, Brioude, Clermont-Ferrand) et Paris.",
        "intro": "La collation de la photographie et les archives familiales de Millau permettent de rectifier plusieurs lectures sans résoudre tous les passages : à la vue \\#136, le groupe commençant par \\textit{Évité troubler} reste partiellement incertain, et les mots \\textit{de me} ne sont pas assurés. À la vue \\#142 (l. 6), le manuscrit porte \\texttt{visite à l'oncle \\& tante Thérèse (Layral)}. L'annexe familiale identifie Thérèse Cartairade, tante maternelle de Marguerite, et son époux Charles Layrals, notaire à Millau ; cette source écrit le patronyme avec un s final. Spagnol apparaît séparément dans un télégramme à Nice et un règlement (vues \\#136 et \\#158) ; son identification comme fleuriste demeure une hypothèse.",
        "illustrations": [
            [
                "illustrations/mariage_millau_1917.jpg",
                "Photographie officielle du mariage d'Hippolyte Combes (en uniforme d'interprète militaire) et de Marguerite Calmels à Millau (25 octobre 1917), entourés des familles Combes et Calmels.",
                "0.50\\textwidth"
            ],
            [
                "illustrations/menu_mariage_1917.jpg",
                "Menu du repas de noces d'Hippolyte Combes et Marguerite Calmels au 10 rue Alfred-Guibert à Millau (25 octobre 1917). Archives familiales.",
                "0.36\\textwidth"
            ]
        ]
    },
    {
        "num": "VII",
        "title": "De février à avril 1917 : Hérissart et les environs",
        "subtitle": "Logements, tournées, nouvelles de guerre et printemps (7 février – 30 avril 1917)",
        "scan_start": 147,
        "scan_end": 186,
        "summary": "Les vues \\#147 à \\#186 couvrent le séjour à Hérissart, la mention d'interprètes de la \\textit{2nd Australian Division}, le départ du capitaine Williams, le maintien de Combes au \\textit{Purchase Board} sur la demande du major Levy et ses conversations avec Gilbert, de Jersey. Elles décrivent la visite aux instituteurs Flutre au Mesnil (vue \\#168), des troupes revenant de Miraumont et d'Achiet-le-Petit (vues \\#170--\\#171), puis le printemps et les nouvelles de guerre jusqu'à la dernière entrée, le lundi 30 avril 1917.",
        "intro": "La vue \\#168 décrit M. et Mme Flutre, instituteurs au Mesnil, dont le fils est élève de l'École normale supérieure. La nécrologie de Louis-Fernand Flutre par René Debrie (\\textit{Revue de linguistique romane}, 42, 1978, p. 238--240) nomme son père Fortuné, instituteur au Mesnil-Martinsart : cette filiation et le parcours du fils étayent fortement le rapprochement. Debrie situe sa naissance au Mesnil-Martinsart le 21 juin 1892, tandis que la notice BnF \\texttt{cb122063529} indique Albert ; la divergence reste ouverte. Admis à l'ENS en 1914, il n'y entre qu'en 1919 et est agrégé en 1921. Les autres mentions militaires sont plus limitées : Combes nomme les \\textit{17th Lancers} parmi des cavaliers indiens et anglais à la vue \\#171, sans permettre d'identifier toutes les unités aperçues ; il loge un officier de la \\textit{63rd Division, naval division} aux vues \\#170--\\#171. La trajectoire de ces témoins ne suffit pas à reconstituer celle de leurs divisions entières.",
        "illustrations": [
            [
                "illustrations/andelys_ecole_militaire.jpg",
                "Photographie de groupe devant l'École militaire préparatoire des Andelys (où Hippolyte est nommé professeur d'anglais le 24 novembre 1918).",
                "0.31\\textwidth"
            ],
            [
                "illustrations/famille_combes_1925.jpg",
                "Hippolyte et Marguerite Combes entourés de leurs enfants à Montauban / Millau vers 1925.",
                "0.31\\textwidth"
            ],
            [
                "illustrations/hippolyte_cambridge_1930.jpg",
                "Hippolyte Combes en Angleterre (Cambridge, été 1930).",
                "0.31\\textwidth"
            ]
        ]
    }
]


def build_spread_latex(rec):
    """
    Generates the exact two-page vis-à-vis LaTeX code for a single scan record:
    - Pure white page background, sober black horizontal rules (no colored boxes).
    - Sized for the compact notebook format (155 x 225 mm, matching the original carnet proportions).
    - Even (left/verso) page: Diplomatic transcription + horizontally aligned marginal apparatus +
      two unnamed but clearly distinguished bottom commentary registers.
    - Odd (right/recto) page: Full-page facsimile image with archival metadata frame.
    """
    scan_num = rec["scan_num"]
    fname = rec["filename"]
    fname_esc = fname.replace("_", "\\_")
    folio = sanitize_latex_fragment(rec["folio"])
    title = sanitize_latex_fragment(rec["title"])
    date_str = sanitize_latex_fragment(rec["date"])
    lieu_str = sanitize_latex_fragment(rec["lieu"])
    lines = rec["lines"]
    raw_mnotes = {int(k): sanitize_latex_fragment(v) for k, v in rec["marginal_notes"].items()}
    crit_str = sanitize_latex_fragment(rec["critique"])
    hist_str = sanitize_latex_fragment(rec["historique"])

    def _vis_len(s):
        s = re.sub(r"\\(?:textbf|textit|texttt|textsc|textsuperscript)\{([^}]*)\}", r"\1", s)
        s = s.replace("$[\\![$", "[[").replace("$]\\!]$", "]]")
        s = re.sub(r"\\[a-zA-Z]+\s*", "", s)
        return len(s.replace("{", "").replace("}", "").replace("$", ""))

    mnotes = dict(raw_mnotes)
    for k in sorted(list(mnotes.keys())):
        if k not in mnotes:
            continue
        span = 1
        while True:
            needed_lines = max(1, (_vis_len(mnotes[k]) + 25) // 26)
            merged_any = False
            while span < needed_lines:
                if (k + span) in mnotes:
                    mnotes[k] = mnotes[k] + " — " + mnotes[k + span]
                    del mnotes[k + span]
                    merged_any = True
                span += 1
            if not merged_any:
                break

    n_lines = len(lines)
    if n_lines <= 19:
        line_font = "\\fontsize{7.8pt}{9.2pt}\\selectfont"
        row_stretch = "1.02"
    elif n_lines <= 23:
        line_font = "\\fontsize{7.4pt}{8.6pt}\\selectfont"
        row_stretch = "0.95"
    else:
        line_font = "\\fontsize{7.0pt}{8.1pt}\\selectfont"
        row_stretch = "0.89"

    rows_tex = []
    for idx, l in enumerate(lines, 1):
        esc_l = escape_diplomatic_line(l)
        if idx % 5 == 0:
            num_prefix = f"\\leavevmode\\llap{{\\fontsize{{6.5pt}}{{7.5pt}}\\selectfont\\color{{darkgray}}{idx}\\hspace{{1.8mm}}}}"
        else:
            num_prefix = "\\leavevmode"

        left_cell = f"{num_prefix}{line_font}\\strut {esc_l}\\strut"
        if idx in mnotes:
            mn = mnotes[idx]
            right_cell = f"\\smash{{\\parbox[t]{{39mm}}{{\\fontsize{{6.3pt}}{{7.2pt}}\\selectfont\\raggedright\\color{{black!88}}{mn}}}}}"
        else:
            right_cell = ""

        rows_tex.append(f"      {left_cell} & {right_cell} \\\\")

    rows_joined = "\n".join(rows_tex)

    tex = f"""
% =============================================================================
% VIS-A-VIS SPREAD : SCAN #{scan_num:03d} ({fname}) — {folio}
% =============================================================================
\\cleardoubleevenpage
% --- En-tête du folio (Page paire / gauche : Transcription, apparat & double registre) ---
\\noindent\\rule{{\\textwidth}}{{0.5pt}}\\par\\vspace{{0.6mm}}
\\noindent\\textbf{{\\footnotesize SCAN \\#{scan_num:03d} — {folio.upper()}}} \\hfill {{\\scriptsize\\texttt{{{fname_esc}}}}}\\par\\vspace{{0.3mm}}
\\noindent{{\\fontsize{{7.0pt}}{{8.2pt}}\\selectfont {title}}}\\par\\vspace{{0.25mm}}
\\noindent{{\\fontsize{{7.0pt}}{{8.2pt}}\\selectfont\\textit{{{date_str}}} \\hfill \\textit{{{lieu_str}}}}}\\par\\vspace{{0.6mm}}
\\noindent\\rule{{\\textwidth}}{{0.35pt}}\\par\\vspace{{1.0mm}}
% --- Corps de la transcription diplomatique et apparat marginal en prolongement ---
{{\\renewcommand{{\\arraystretch}}{{{row_stretch}}}%
\\noindent\\hspace*{{3.5mm}}\\begin{{tabular}}{{@{{}}p{{87mm}}@{{\\hspace{{3.5mm}}}}p{{39mm}}@{{}}}}
{rows_joined}
\\end{{tabular}}}}%
\\par\\vspace*{{\\fill}}
% --- Deux registres de commentaires en bas de page (sans intitulés, distingués par filets et mise en page) ---
\\noindent\\rule{{\\textwidth}}{{0.5pt}}\\par\\vspace{{0.8mm}}
{{\\fontsize{{6.8pt}}{{8.0pt}}\\selectfont%
\\noindent\\normalfont {crit_str}\\par\\vspace{{0.75mm}}
\\noindent\\rule{{38mm}}{{0.4pt}}\\par\\vspace{{0.65mm}}
\\noindent\\hspace*{{5mm}}\\parbox{{\\dimexpr\\textwidth-5mm\\relax}}{{\\fontsize{{6.8pt}}{{8.0pt}}\\selectfont\\color{{black!82}}{hist_str}}}\\par}}
\\newpage
% --- En-tête du fac-similé (Page impaire / droite : Scan original) ---
\\noindent\\rule{{\\textwidth}}{{0.5pt}}\\par\\vspace{{0.6mm}}
\\noindent\\textbf{{\\fontsize{{6.5pt}}{{7.6pt}}\\selectfont FAC-SIMILÉ EN VIS-À-VIS — {folio.upper()} (SCAN \\#{scan_num:03d})}} \\hfill {{\\fontsize{{6.5pt}}{{7.6pt}}\\selectfont\\texttt{{{fname_esc}}}}}\\par\\vspace{{0.3mm}}
\\noindent{{\\fontsize{{6.8pt}}{{8pt}}\\selectfont\\textit{{Livre-Journal d'Hippolyte Combes}} — {date_str} ({lieu_str})}}\\par\\vspace{{0.6mm}}
\\noindent\\rule{{\\textwidth}}{{0.35pt}}\\par\\vspace*{{\\fill}}
{{\\centering
  \\setlength{{\\fboxsep}}{{1.2mm}}%
  \\setlength{{\\fboxrule}}{{0.4pt}}%
  \\fcolorbox{{gray!55}}{{white}}{{%
    \\includegraphics[width=0.94\\textwidth,height=0.76\\textheight,keepaspectratio]{{\\facsimiledir/{fname}}}%
  }}\\par}}
\\vspace*{{\\fill}}
\\noindent\\rule{{\\textwidth}}{{0.35pt}}\\par\\vspace{{0.5mm}}
\\noindent{{\\fontsize{{6pt}}{{7.1pt}}\\selectfont\\color{{darkgray}}\\textbf{{Source :}} Archives familiales Combes — Cliché numérique \\texttt{{{fname_esc}}} (Scan \\#{scan_num:03d}/186, {folio}). Haute définition : \\texttt{{scans\\_haute\\_qualite/{fname_esc}}} ; version allégée : \\texttt{{scans\\_compresses/{fname_esc}}}.}}
\\newpage
"""
    return tex


def generate_full_tex():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        records = json.load(f)
    assert len(records) == 186, f"Expected 186 records, got {len(records)}"

    preamble = r"""\documentclass[10pt,twoside,openany]{book}
\usepackage{fontspec}
\usepackage[french]{babel}
% Format petit in-octavo / carnet (155 x 225 mm), proche du livre de poche et homothétique au carnet autographe (ratio ~0,69)
\usepackage[paperwidth=155mm,paperheight=225mm,top=11mm,bottom=11mm,inner=12mm,outer=10mm,headheight=13.5pt,headsep=3.5mm,footskip=5mm]{geometry}
\usepackage{graphicx}
\usepackage{xcolor}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{array,booktabs,longtable}
\usepackage{fancyhdr}
\usepackage{titlesec}
\usepackage{hyperref}

% Palette sobre sur fond blanc pur (modèle de l'édition des Thesmophories)
\definecolor{darkgray}{HTML}{3A3A3A}
\definecolor{bordeaux}{HTML}{5A1818}

% Répertoire des fac-similés :
% Par défaut, pointe vers ../scans_compresses pour maintenir le PDF compilé sous la limite GitHub de 100 Mo (~36 Mo).
% Pour compiler un tirage utilisant les JPEG haute définition (~1,03 Go), décommenter la seconde ligne :
\newcommand{\facsimiledir}{../scans_compresses}
% \renewcommand{\facsimiledir}{../scans_haute_qualite}

% Pages blanches de garde sans en-tête ni foliotage lors des sauts vers une belle page (impaire) ou une page paire :
\makeatletter
\def\cleardoublepage{\clearpage\if@twoside \ifodd\c@page\else
  \hbox{}\thispagestyle{empty}\newpage\if@twocolumn\hbox{}\newpage\fi\fi\fi}
\makeatother

% Saut automatique vers une page paire (gauche / verso) pour garantir le vis-à-vis strict :
% Page paire (gauche) = Transcription diplomatique, apparat marginal & double registre de commentaire
% Page impaire (droite) = Fac-similé du scan correspondant
\newcommand{\cleardoubleevenpage}{%
  \clearpage
  \ifodd\value{page}%
    \hbox{}\thispagestyle{empty}\newpage
  \fi
}

\pagestyle{fancy}
\fancyhf{}
\fancyhead[LE]{\scriptsize\textsc{Hippolyte Combes — Livre-Journal (1916–1917)}}
\fancyhead[RO]{\scriptsize\nouppercase{\rightmark}}
\fancyfoot[LE,RO]{\scriptsize\thepage}
\renewcommand{\headrulewidth}{0.3pt}

\titleformat{\chapter}[display]
  {\normalfont\normalsize\bfseries}
  {\textsc{\chaptertitlename\ \Roman{chapter}}}
  {0.8mm}
  {\large\color{black}}
\titlespacing*{\chapter}{0pt}{-4mm}{2.5mm}
\titlespacing*{\section}{0pt}{2mm}{1mm}

\hypersetup{
  colorlinks=true,
  linkcolor=black,
  urlcolor=bordeaux,
  pdftitle={Hippolyte Combes (1876-1970) - Livre-Journal de campagne (25 juillet 1916 - 30 avril 1917) - Édition philologique et diplomatique},
  pdfauthor={Louis Hauseux (dir.)}
}

\setlength{\parindent}{1.0em}
\setlength{\parskip}{0.25em}
\setlength{\emergencystretch}{1.5em}

\begin{document}

% =============================================================================
% 1. PREMIÈRE DE COUVERTURE (SOBRE SUR FOND BLANC PUR, FORMAT CARNET 155x225mm)
% =============================================================================
\begin{titlepage}
\thispagestyle{empty}
\begin{center}
  \setlength{\fboxsep}{4.5mm}
  \setlength{\fboxrule}{0.7pt}
  \fcolorbox{black}{white}{%
    \parbox[t][188mm][s]{120mm}{%
      \begin{center}
        \vspace{2mm}
        {\footnotesize\textsc{Archives familiales de Millau, Toulouse \& du Front britannique}}\\[1.5mm]
        \rule{86mm}{0.4pt}\\[4mm]
        {\Large\textbf{HIPPOLYTE COMBES}}\\[1.5mm]
        {\footnotesize\textsc{(Millau, 14 août 1876 — Saint-Chély-d'Apcher, 2 septembre 1970)}}\\[5mm]
        {\LARGE\textbf{LIVRE - JOURNAL}}\\[2mm]
        {\large\textbf{DE CAMPAGNE (1916–1917)}}\\[2.5mm]
        {\normalsize\textit{Du 25 juillet 1916 au 30 avril 1917}}\\[2mm]
        {\footnotesize Interprète militaire auprès de l'Armée britannique\\
        (\textit{Army Service Corps}, puis services d’approvisionnement britanniques)}\\[4.5mm]
        % Vignette centrale extraite de la couverture du carnet autographe
        \setlength{\fboxsep}{1.2mm}
        \setlength{\fboxrule}{0.4pt}
        \fcolorbox{black}{white}{%
          \includegraphics[width=58mm,height=50mm,keepaspectratio]{illustrations/vignette_couverture.jpg}%
        }\\[4.5mm]
        {\normalsize\textsc{Édition philologique, diplomatique et critique en vis-à-vis}}\\[2mm]
        {\scriptsize Transcription de travail des 186 vues, numérotée de 5 en 5 lignes,\\
        apparat critique marginal aligné dans le prolongement de la ligne,\\
        double registre de commentaire et fac-similés en regard}\par
        \vfill
        \rule{70mm}{0.4pt}\\[2mm]
        {\footnotesize\textsc{Édition établie, introduite et annotée}}\\
        {\scriptsize d'après le manuscrit autographe et les archives familiales Combes-Calmels de Millau et Montauban}\\[1.5mm]
        {\footnotesize\textbf{MMXXVI}}
        \vspace{1mm}
      \end{center}
    }%
  }
\end{center}
\end{titlepage}

% Page blanche de garde (Page 2)
\hbox{}\thispagestyle{empty}\newpage

% =============================================================================
% 2. FAUX-TITRE & PAGE DE TITRE INTÉRIEURE (AVEC EMBLÈME FRAKTUR \mathfrak{Urtext})
% =============================================================================
\thispagestyle{empty}
\begin{center}
  \vspace*{10mm}
  {\large\textsc{Marie Lucien Hippolyte Combes}}\\
  {\footnotesize (Millau, 14 août 1876 — Saint-Chély-d'Apcher, 2 septembre 1970)}\\[10mm]
  {\LARGE\textbf{LIVRE-JOURNAL DE GUERRE}}\\[3mm]
  {\normalsize\textit{25 juillet 1916 — 30 avril 1917}}\\[4mm]
  {\footnotesize Des Flandres à l'Artois et au front de la Somme\\
  auprès de l'\textit{Army Service Corps} (18\textsuperscript{e} Division, XIII\textsuperscript{e} \& V\textsuperscript{e} Corps)}\\[14mm]
  {\Huge $\mathfrak{Urtext}$}\\[14mm]
  \rule{45mm}{0.4pt}\\[6mm]
  {\footnotesize\textbf{Édition de travail : première collation des 186 vues}}\\[1.5mm]
  {\scriptsize accompagnée des lettres de guerre inédites (1916–1918), de l'état signalétique des services\\
  et d'un répertoire prosopographique, militaire et topographique}\par
  \vfill
  {\footnotesize\textsc{Collection des Sources et Manuscrits Contemporains}}\\
  {\scriptsize Millau — Toulouse — Montauban — Paris}
  \vspace*{6mm}
\end{center}
\newpage

\frontmatter
\renewcommand{\thesection}{\Roman{section}}
{\small\tableofcontents}
\cleardoublepage

% =============================================================================
% 3. PROLÉGOMÈNES SCIENTIFIQUES ET HISTORIQUES
% =============================================================================
\chapter{Prolégomènes : Hippolyte Combes (1876–1970) et son \textit{Livre-Journal} de la Grande Guerre}
\markboth{Prolégomènes}{Prolégomènes}
{\small

\section{Destin d'un universitaire rouergat et toulousain auprès de l'Armée britannique (1876–1970)}

L'acte de naissance n\textsuperscript{o}~395 du 16 août 1876 situe la naissance de \textbf{Marie Lucien Hippolyte Combes} à \textbf{Millau}, rue des Barris, le \textbf{14 août 1876}, fils de \textbf{François Augustin Hippolyte Combes} (1825–1899), avocat, et de \textbf{Marie Anaïs Alric} (1838–1907). La fiche matricule porte une date différente, le 22 août : les deux témoignages sont signalés sans harmonisation silencieuse. Les pièces d'état civil et monographies familiales (\texttt{Combes-3-part 1.DOC}, \texttt{Combes-3-part 2.DOC}, \texttt{Combes-annexe.DOC}) retracent ses études à l'Institution Sainte-Marie et à la Faculté des lettres de Toulouse (47 rue du Taur), son séjour de quatre années en Angleterre (Nottingham) et sa carrière de professeur d'anglais aux collèges de Saint-Yrieix et de Nogent-le-Rotrou (17 rue Saint-Hilaire), puis au lycée Ingres de Montauban jusqu'à sa retraite à Millau et son décès le \textbf{2 septembre 1970} à l'\textbf{Hôtel du Centre} à \textbf{Saint-Chély-d'Apcher} (Lozère ; date et commune dans \texttt{Combes-3-part 2.DOC}, établissement transmis par la tradition familiale directe ; inhumé à Millau).

\begin{figure}[htbp]
  \centering
  \begin{minipage}[b]{0.46\textwidth}
    \centering
    \includegraphics[height=44mm,keepaspectratio]{illustrations/hippolyte_1897.jpg}
    \par\vspace{1mm}{\scriptsize\textit{Fig. 1.} Hippolyte Combes en 1897, à l'âge de 21 ans.}
  \end{minipage}\hfill
  \begin{minipage}[b]{0.48\textwidth}
    \centering
    \includegraphics[height=44mm,keepaspectratio]{illustrations/hippolyte_interprete_1.jpg}
    \par\vspace{1mm}{\scriptsize\textit{Fig. 2.} Hippolyte Combes en uniforme d'interprète auprès de la B.E.F. (1916).}
  \end{minipage}
\end{figure}

Exempté dans sa jeunesse pour « faiblesse générale » (\textbf{classe 1896, bureau de recrutement de Toulouse, matricule n\textsuperscript{o}~911}), Hippolyte Combes est classé « Service armé » par le conseil de révision d'Eure-et-Loir le \textbf{18 décembre 1914}. Appelé à l'activité le \textbf{20 mars 1915} et incorporé le \textbf{21 mars 1915} à la 39\textsuperscript{e} batterie du \textbf{10\textsuperscript{e} régiment d'artillerie à pied} à Toulon (Saint-Jean-du-Var), il est détaché dès le \textbf{4 mai 1915} comme interprète militaire à la \textbf{Mission militaire française attachée à l'Armée britannique} (administrativement rattaché au \textbf{19\textsuperscript{e} escadron du Train des équipages militaires} le 15 octobre 1915) :

\begin{itemize}
  \item \textbf{Depuis août 1915 : service dans une compagnie A.S.C. de la 18\textsuperscript{e} Division britannique.} Dans la copie autographe de sa lettre du 21 février 1916 (Annexe I, document 1), Combes écrit avoir été rattaché à l'été 1915 à la \textbf{18\textsuperscript{e} Division britannique} (\textit{18th Eastern Division}, commandée par le major-général Sir Ivor Maxse) qui se formait autour de Flesselles, avoir servi quinze jours au secrétariat de la Mission française (sous l'officier interprète divisionnaire M.~Pizzi), puis être affecté « depuis le mois d'août » [1915] à une compagnie d'\textit{Army Service Corps}. Le carnet nomme la \textbf{152nd Company A.S.C.} et la \textit{54th Brigade} (vue \#066), situe une démarche au \textit{Train Office} auprès du \texttt{Col. Grose} (vue \#090), et signale le 9 janvier 1917 une visite à la \textbf{150th Company A.S.C., 18th Division}, près d'Hédauville (vue \#121). Ce dernier passage n'établit pas une affectation de trois jours à cette compagnie.
  \item \textbf{Du Train divisionnaire aux services d'achats et de réquisitions (\textit{Foraging} / \textit{Army Purchase Board}, juillet 1916 – avril 1917).} Le carnet suit d'abord les déplacements de Combes en Flandre intérieure (Sercus, Renescure, Hazebrouck, Bailleul) et dans la vallée de la Lys (La Croix-du-Bac, Armentières, Fleurbaix), puis son transfert ferroviaire du \textbf{25 août} vers Marquay par Saint-Pol (vues \#027–\#028) et sa remontée vers la Somme (Beauval, Raincheval, Acheux, Forceville). L'historique divisionnaire situe ces étapes après la relève de la Somme du 20 juillet 1916 et avant Thiepval (26 septembre) et les combats de l'Ancre. À Acheux-en-Amiénois, puis à Hérissart, Combes décrit le service des approvisionnements et achats de fourrage, d'abord avec le capitaine Williams. Le 11 mars, il apprend son maintien au \textit{Purchase Board} sur demande du major Levy (vue \#166) ; il fréquente ensuite notamment le lieutenant Gilbert, donné comme originaire de Jersey (vue \#179).
  \item \textbf{Après le carnet.} Les pièces familiales documentent son mariage avec \textbf{Marie Marguerite Calmels} (1892–1974) à Millau le 25 octobre 1917. La fiche matricule donne son affectation à l'École militaire préparatoire des Andelys comme professeur d'anglais le 24 novembre 1918 (nommé caporal le 4 décembre 1918) et sa démobilisation le 7 février 1919. La mention de Montauban du 24 janvier 1920 relève de la rubrique des domiciles et indique sa profession au lycée Ingres.
\end{itemize}

\section{Histoire matérielle, codicologie et paléographie du \textit{Livre-Journal}}

Le dossier photographique comprend \textbf{186 clichés numériques}, de \texttt{20251126\_\allowbreak 092853.jpg} (Scan \#001) à \texttt{20251126\_\allowbreak 111833.jpg} (Scan \#186). Le premier cliché reproduit le plat supérieur de la couverture, revêtu d'un papier fort rouge à motif de losanges gaufrés sur lequel est collée une étiquette rectangulaire de papier bleu portant à l'encre noire l'intitulé autographe en cinq lignes : \textit{Livre - Journal / — / Du 25 juillet 1916 / au 30 avril 1917 / —}.

Cette édition de travail résulte d'une première collation, puis d'une étude comparative de l'écriture suivie d'une seconde relecture intégrale des 186 vues. Un atlas de 88 extraits natifs, issus de 54 photographies, documente les comparaisons dans le dépôt ; cette seconde passe modifie les lignes transcrites de 49 vues. Elle conserve les doutes de lecture. Les observations ci-dessous décrivent des usages fréquents ; elles ne remplacent pas la vérification de chaque tracé.
\begin{enumerate}
  \item \textbf{Ductus et système abréviatif d'Hippolyte Combes.} L'écriture d'Hippolyte Combes est une cursive latine penchée, rapide et nerveuse, riche en abréviations par suspension et par lettres suscrites : \textit{ds} (\textit{dans}), \textit{pr} (\textit{pour}), \textit{s/} (\textit{sur}), \textit{j'à / j'au / j'aux} ou \textit{ju} (\textit{jusqu'à, jusqu'au, jusqu'aux}), \textit{lgt / lgs / longt} (\textit{longtemps}), \textit{tt / tte / ts} (\textit{tout, toute, tous}), \textit{tjs / tjours} (\textit{toujours}), \textit{qq} (\textit{quelques}), \textit{gd / gde / gds} (\textit{grand, grande, grands}), \textit{bp / bcp} (\textit{beaucoup}), \textit{cme} (\textit{comme}), \textit{chz} (\textit{chez}), ainsi que les finales adverbiales ou nominales suscrites (\textit{ext\textsuperscript{t}, merv\textsuperscript{t}, défint\textsuperscript{t}, admirab\textsuperscript{t}, appart\textsuperscript{t}, cantonnem\textsuperscript{t}, changem\textsuperscript{t}, propri\textsuperscript{re}, cath\textsuperscript{le}}). Les chiffres peuvent avoir une valeur lexicale : 1 pour un ou une, 1/2 pour demi ou, selon le contexte, milieu. Les signes $+$ et $=$ sont conservés ; leur développement est motivé dans la notice, et non imposé partout.
  \item \textbf{Esperluette et y.} Certains tracés cursifs de \texttt{\&} ressemblent à la lettre y. Leur valeur est examinée occurrence par occurrence, d'après la forme, la position et les parallèles de la main. Aucun remplacement global de y par et ou par \texttt{\&} n'est appliqué comme règle de lecture ; un signe non établi reste marqué.
  \item \textbf{Lectures et identifications vérifiées.} Curtis est lisible dans plusieurs entrées et apparaît aussi sous la contraction \textit{Ctis}. La vue \#016 porte la date du 10 août, mentionne Sailly-sur-la-Lys et rapporte une conversation avec un éclusier au sujet du général Maxse. À la vue \#142 (l.~6, Millau, 4 février 1917), la réinspection du cliché établit \texttt{visite à l'oncle \& tante Thérèse (Layral)}. L'annexe familiale identifie Thérèse Cartairade et son époux Charles Layrals, notaire à Millau, avec un s final dans cette source. Spagnol est cité ailleurs, à propos d'un télégramme à Nice et d'un règlement (vues \#136 et \#158) ; le métier de fleuriste demeure conjectural. Le rapprochement des Flutre de la vue \#168 avec la famille du romaniste Louis-Fernand Flutre repose sur la nécrologie de René Debrie (1978, p.~238--240), qui nomme son père Fortuné, instituteur au Mesnil-Martinsart. Debrie donne une naissance au Mesnil-Martinsart, tandis que la BnF (\texttt{cb122063529}) indique Albert ; cette divergence n'est pas expliquée par les documents consultés. Debrie distingue l'admission à l'ENS en 1914, l'entrée en 1919 et l'agrégation en 1921. Le second prénom Ernest, la naissance du père en 1862 et son installation en 1888 demandent encore une pièce directement contrôlable.
  \item \textbf{Particularités de la séquence photographique.} Le cliché \#050 (\texttt{20251126\_\allowbreak 103019.jpg}, journée du 25 septembre 1916), omis dans le premier fichier Word, est restitué à sa place. Les clichés \#063 (5 octobre 1916) et \#064 (nuit du 4 au 5 octobre 1916), ainsi que les clichés \#112 (24 décembre 1916) et \#113 (23 décembre 1916), ont été photographiés dans l'ordre inverse de la chronologie. Enfin, les clichés \#091 (\texttt{20251126\_\allowbreak 104623.jpg}) et \#093 (\texttt{20251126\_\allowbreak 104648.jpg}) constituent deux prises de vue successives d'un même feuillet original (journées des 2 et 3 novembre 1916). Pour conserver une correspondance explicite avec les 186 fichiers JPEG des répertoires \texttt{scans\_\allowbreak haute\_\allowbreak qualite/} et \texttt{scans\_\allowbreak compresses/}, l'édition conserve la numérotation des vues (\texttt{Scan \#001} à \texttt{Scan \#186}). La désignation Vue identifie une photographie ; elle ne constitue pas une foliation matérielle. Les anciens numéros recto-verso calculés d'après l'ordre des fichiers n'ont pas valeur de constat codicologique.
\end{enumerate}

\section{Principes de l'édition philologique en vis-à-vis}

Inspirée des principes de l'édition philologique classique (sur le modèle de l'édition savante des \textit{Thesmophories} d'Aristophane), la présente édition adopte un format maniable (\texttt{155 $\times$ 225 mm}, proche du livre de poche et homothétique au carnet original), une typographie sobre en noir sur fond blanc pur et met en regard, sur chaque double page (du Scan \#001 au Scan \#186) :
\begin{itemize}
  \item \textbf{Sur la page de gauche (page paire / verso) :}
    \begin{enumerate}
      \item \textbf{La transcription de travail ligne à ligne}, cherchant à conserver la disposition matérielle, l'orthographe, les abréviations, la ponctuation et les crochets comptables \texttt{[ ... ]} du manuscrit. Les lignes sont numérotées de cinq en cinq dans la marge gauche (\texttt{5, 10, 15, 20, 25}). Les lectures proposées portent un point d'interrogation ; \texttt{[illis.]} signale une séquence non déchiffrée et les blancs ou additions sont décrits dans la notice. Les suppressions et ratures autographes sont placées entre doubles crochets droits ($[\![ \dots ]\!]$).
      \item \textbf{L'apparat critique marginal}, composé en petits caractères dans la colonne de droite en regard immédiat et dans le prolongement horizontal exact de la ligne concernée : il développe les abréviations tachygraphiques (\textit{scil.}, \textit{abbr. pro}), signale les biffures du manuscrit ($[\![ \dots ]\!]$ \textit{del. in ms.}), identifie les emprunts lexicaux anglais (\textit{angl. in ms.}) ou latins (\textit{lat.}) et précise les particularités matérielles (\textit{in marg. cum unco}).
      \item \textbf{En bas de page, deux registres de commentaires dépourvus d'intitulés répétitifs mais immédiatement distingués au premier coup d'œil par des filets horizontaux et un décrochement typographique franc :}
        \begin{itemize}
          \item \textit{Le premier registre}, placé immédiatement sous le filet horizontal de pleine largeur (\texttt{0,5 pt}) et composé au fer à gauche sur toute la justification (\texttt{133 mm}), est consacré à la \textbf{critique interne du carnet} : analyse codicologique et paléographique, génétique des repentirs, syntaxe elliptique, bilinguisme franco-anglais, tenue des comptes et degrés de certitude des lectures.
          \item \textit{Le second registre}, séparé du précédent par un filet horizontal court (\texttt{38 mm}, \texttt{0,4 pt}) et composé avec un retrait général de bloc de \texttt{5 mm} sur la gauche, est consacré à l'\textbf{élucidation historique, militaire, topographique et prosopographique} : références militaires et géographiques, localités et personnes mentionnées, avec distinction entre lecture, hypothèse d'identification et fait établi par une source extérieure.
        \end{itemize}
    \end{enumerate}
  \item \textbf{Sur la page de droite (page impaire / recto) :} \textbf{le fac-similé photographique complet} du feuillet manuscrit correspondant, accompagné de ses références archivistiques.
\end{itemize}

\section{Critique des sources militaires et archivistiques}

L'annotation historique repose sur le croisement méthodique des archives familiales du dépôt (\texttt{archives\_\allowbreak militaires/} et \texttt{biographie\_\allowbreak et\_\allowbreak famille/}) et des sources institutionnelles britanniques et françaises :
\begin{itemize}
  \item \textbf{18th (Eastern) Division et 18th Divisional Train A.S.C.} L'historique divisionnaire du capitaine G.~H.~F.~Nichols (\textit{The 18th Division in the Great War}, Londres, Blackwood, 1922, p.~107--110 et 432) et l'\textit{Order of Battle of Divisions} du major A.~F.~Becke (Part~3A, Londres, HMSO, 1938) établissent que le \textit{18th Divisional Train} comprenait quatre compagnies d'\textit{Army Service Corps} (\textbf{150th, 151st, 152nd et 153rd Companies A.S.C.}), commandées à Thiepval par le \textbf{Lt.-Col. D.~C.~E.~Grose, A.S.C.} (\textit{London Gazette}, 4 juin 1917, p.~5470 ; \texttt{Col. Grose} au \textit{Train Office}, vue \#090), avec notamment le \textbf{Maj. H.~G.~Peachy, A.S.C.} à la \textbf{150th Co.} et le \textbf{Capt. E.~M.~West, A.S.C.} à la \textbf{152nd Co.} (\textit{Military Cross}, p.~432 ; \texttt{Cap. West}, vues \#039, \#042, \#048), ainsi que le \textbf{Capt. E.~M.~Ford, M.C.} au \textit{18th Div. Train} (p.~432 ; \texttt{Lt Ford}, vue \#076). \textit{The Ringing World} (9 avril 1915, p.~184) atteste dès 1915 la \textbf{152nd Company A.S.C.} au \textit{18th Divisional Train}. Combes indique la \textbf{152nd Company A.S.C.} et la \textit{54th Brigade} (vue \#066), puis la \textbf{150th Company A.S.C., 18th Division} (vue \#121, 9 janvier). Il nomme des \textit{Royal Fusiliers} (vues \#002–\#003) et des \textit{Bedfords} (vue \#038), sans numéro de bataillon dans ces mentions. La vue \#150 porte \textit{M.T. (A.S.C.)}, à développer comme \textit{Motor Transport} ; la notice de la \textit{London Gazette} du 9 mars 1917, p.~2447, ne suffit pas à identifier l'unité personnelle de Combes à cette date.
  \item \textbf{Grandes unités alliées croisées dans la Somme en 1917.} La vue \#164 rattache l'interprète Valet à la \textbf{2nd Australian Division} ; elle ne décrit pas à elle seule la relève de tout le secteur. Combes observe des cavaliers indiens et anglais et nomme les \textbf{17th Lancers (\textit{Death or Glory Boys})} à la vue \#171. L'historique du Royal Lancers Museum rattache ce régiment à la \textit{1st Indian Cavalry Division} lors de son arrivée en France en 1914 ; le rattachement précis de tous les cavaliers aperçus aux vues \#160, \#169 et \#171 ne peut être déduit de leur seule présence. Aux vues \#170–\#171, Combes loge un officier de la \textbf{63rd Division, naval division}, dont le régiment revient des tranchées de Miraumont et d'Achiet-le-Petit. Ces mentions éclairent le repli allemand de mars 1917, sans établir que toutes les brigades de cette division reviennent ensemble des deux localités.
\end{itemize}

\section{Répertoire prosopographique, militaire et topographique}

{\footnotesize
\renewcommand{\arraystretch}{1.15}
\noindent\begin{longtable}{@{}>{\raggedright\arraybackslash}p{33mm}p{95mm}@{}}
\toprule
\textbf{Nom / Unité / Lieu} & \textbf{Identification biographique, militaire ou géographique} \\
\midrule
\endhead
\textbf{Combes, Hippolyte} (1876–1970) & Marie Lucien Hippolyte Combes, né à Millau le 14 août 1876 (acte n\textsuperscript{o}~395 ; 22 août sur la fiche matricule), décédé le 2 septembre 1970 à l'Hôtel du Centre à Saint-Chély-d'Apcher (Lozère ; date et commune dans \texttt{Combes-3-part 2.DOC}, établissement transmis par la tradition familiale directe ; inhumé à Millau). Professeur d'anglais à Saint-Yrieix, Nogent-le-Rotrou (17 rue Saint-Hilaire) puis au lycée Ingres de Montauban ; interprète militaire auprès de l'Armée britannique (4 mai 1915 – 11 novembre 1918). \\
\textbf{Calmels, Marguerite} (« Margte », « Mte », « Gueïte », 1892–1974) & Marie Marguerite Calmels, née à Millau le 15 avril 1892 (acte n\textsuperscript{o}~139, \texttt{1892\_acte\_naissance\_Marguerite\_Calmels.png}) et décédée à Millau le 19 mars 1974 (\texttt{biographie\_et\_famille/etat\_civil\_et\_actes/}), fille du Dr Gabriel Calmels (1852–1921) et de Valentine Cartairade (1858–1943), domiciliés au 10 rue Alfred-Guibert à Millau. Fiancée puis épouse d'Hippolyte Combes (25 octobre 1917). \\
\textbf{Combes, François-Hippolyte} (1825–1899) \& \textbf{Marie Anaïs Alric} (1838–1907) & Parents d'Hippolyte Combes : François Augustin Hippolyte Combes, avocat à Millau puis installé à Toulouse (47 rue du Taur), et Marie Anaïs Alric (Scans \#092, \#132, \#143). \\
\textbf{Françoise} (1871–1942), \textbf{Joséphine} (1873–1914) \& \textbf{Maria} (1875–1903) & Les trois sœurs d'Hippolyte Combes : Françoise (\textit{Sœur Marie de la Croix}, carmélite à Périgueux, destinataire de la lettre du 16 juin 1916), Joséphine (décédée chez Hippolyte à Nogent-le-Rotrou en octobre 1914) et Maria (religieuse décédée à Carthage le 19 novembre 1903). \\
\textbf{Crouzet, Émile} (1842–1921), \textbf{Élisabeth Calmels} \& \textbf{l'abbé Jean Crouzet} & Famille toulousaine chez qui réside Marguerite lors des permissions de septembre 1916 et janvier 1917 (47 rue du Taur et rue Pharaon) : Émile Crouzet (\texttt{M. Czt}, \texttt{oncle Crouzet}, \texttt{Oncle Émile}, agent de change à Toulouse, témoin de 39 ans sur l'acte de naissance n\textsuperscript{o}~139 de Marguerite en 1892), son épouse Élisabeth Calmels (\texttt{Tante}, tante paternelle de Marguerite) et leur fils l'abbé Jean Crouzet (\texttt{Jean}, prêtre, futur curé de Notre-Dame de la Dalbade ; \texttt{Combes-annexe.DOC}). \\
\textbf{Calmels, Vincens et Delcamps (familles)} & Famille de Marguerite au 10 rue Alfred-Guibert à Millau (Scans \#139–\#143) : le Dr Gabriel Calmels (1852–1921) et Valentine Cartairade (1858–1943) ; leurs filles Madeleine Calmels (1882–1961, épouse du Dr Fernand Vincens, mère de \textbf{Germaine} et \textbf{Robert Vincens}), Anne-Marie dite \textbf{« Mimi »} Calmels (1888–1975, future épouse de l'avoué Joseph Delcamps) et Marguerite, ainsi que leur fils \textbf{Pierre Calmels}. \\
\textbf{Layral, M\textsuperscript{e} Charles \& Thérèse Cartairade} & Oncle et tante maternels de Marguerite à Millau, visités le 4 février 1917 : \texttt{visite à l'oncle \& tante Thérèse (Layral)} (Scan \#142, l.~6 ; \texttt{Combes-annexe.DOC} et \texttt{faire-part-deces-Emilie-Noel.jpg}). \\
\textbf{Faure, Mme} (Germaine, Marcel, Henri, André) & Famille reçue à Neuilly-sur-Seine (vues \#130–\#131) ; la lecture du premier chiffre de l'adresse demeure réservée ; l'annexe familiale réserve expressément le degré de parenté. Marcel est présent lors de la visite de janvier 1917 (vue \#131). L'identification au futur Compagnon de la Libération Marcel Faure est proposée par la notice familiale et demande une vérification indépendante. Le récit de captivité et de rapatriement que l'ancienne annexe attribuait aux lettres des 25 et 26 novembre 1918 ne figure pas dans les quatre faces écrites contrôlées : ces pièces relatent la visite chez les Faure et des conversations familiales. \textbf{Henri} est dit aspirant et \textbf{André} prépare Polytechnique. \\
\textbf{Chilcott, Beatrice} & Amie anglaise d'Hippolyte Combes à l'époque de son séjour d'avant-guerre à Nottingham, signataire du poème autographe conservé dans ses papiers (\textit{Wesley Band of Hope}). \\
\textbf{Maxse, Maj.-Gen. Sir Ivor} (1862–1958) & Commandant de la \textbf{18th (Eastern) Division} britannique de 1915 à janvier 1917. Combes parle de lui avec un éclusier le 10 août 1916 lors de sa promenade vers Sailly-sur-la-Lys (vue \#016) ; aucune rencontre avec le général n'est rapportée dans ce passage. \\
\textbf{Grose, Lt.-Col. Daniel Charles Evans} & Commandant (\textit{Officer Commanding}) du \textbf{18th Divisional Train, A.S.C.} (DSO, \textit{London Gazette}, 4 juin 1917, p.~5470 ; Nichols, 1922, p.~110), mentionné au Scan \#090 (\texttt{Col. Grose}). \\
\textbf{152nd \& 150th Companies, A.S.C.} & Compagnies du \textbf{18th Divisional Train} (\textbf{150th, 151st, 152nd et 153rd Companies A.S.C.}, Nichols, 1922, p.~107--110 ; \textit{The Ringing World}, 9 avril 1915, p.~184). Combes nomme la \textbf{152nd Company} et la \textit{54th Brigade} à la vue \#066, puis visite la \textbf{150th Company, 18th Division} près d'Hédauville le 9 janvier 1917 (vue \#121). Les mentions de \textit{Royal Fusiliers} et de \textit{Bedfords} ne donnent pas à elles seules les numéros de bataillon. \\
\textbf{Curtis} (\textit{Ctis}), \textbf{Panton}, \textbf{West}, \textbf{Walsh}, \textbf{Ford} & Officiers britanniques mentionnés par Combes de juillet à novembre 1916. Nichols (1922, p.~110, 432) atteste au \textbf{18th Divisional Train} le \textbf{Capt. E.~M.~West, A.S.C.} (commandant la \textbf{152nd Co. A.S.C.} à Thiepval, décoré de la \textit{Military Cross}) et le \textbf{Capt. E.~M.~Ford, M.C.} ; l'unité exacte de Curtis, Panton et Walsh n'est pas précisée par le carnet. \\
\textbf{Williams, Capt.} & Capitaine britannique (\textit{Foraging Officer}) avec qui Combes effectue les tournées de réquisition de paille et de fourrage autour d'Acheux et d'Hérissart du 1\textsuperscript{er} décembre 1916 au 10 mars 1917 (Scans \#105–\#165). \\
\textbf{Levy, Major} \& \textbf{Gilbert} & Le major Levy demande le maintien de Combes au \textit{Purchase Board}, ce qu'il apprend le 11 mars 1917 (vue \#166). Le \textit{Second Lieutenant} Gilbert est dit originaire de \textbf{Jersey}, instruit et poète (vue \#179) ; Combes décrit ensuite leurs conversations et promenades. Ces mentions ne suffisent pas à établir une succession formelle au poste du capitaine Williams. \\
\textbf{Pizzi, Ferran, Huguet, Raucoule, Valet} & Officiers et interprètes rencontrés ou mentionnés dans le dossier de la Mission française. Leurs rattachements doivent être établis séparément ; le petit numéro interlinéaire de la vue \#094 demeure réservé. \\
\textbf{Flutre, Fortuné} \& \textbf{Louis-Fernand Flutre} (1892–1978) & Le couple d'instituteurs rencontré au Mesnil et leur fils normalien (vue \#168) se rapprochent fortement de cette famille : René Debrie (nécrologie, 1978, p.~238--240) nomme Fortuné, instituteur au \textbf{Mesnil-Martinsart}, comme père du romaniste. Il situe la naissance du fils dans ce village le 21 juin 1892 ; la notice BnF \texttt{cb122063529} indique \textbf{Albert}. Louis-Fernand est admis à l'ENS en \textbf{1914}, y entre en \textbf{1919}, est agrégé en \textbf{1921}, puis enseigne la philologie romane à Lyon ; il publie deux monographies de son village en 1955. Le second prénom Ernest et les dates du père restent à vérifier directement. \\
\textbf{Zyromski, Ernest} (1862–1933) & Professeur de littérature française à la Faculté des lettres de Toulouse ; Hippolyte achète son essai \textit{L'Orgueil humain} chez Armand Colin le 26 septembre 1916 (Scan \#053) et assiste à sa conférence sur Maurice de Guérin le 30 janvier 1917 (Scan \#135). \\
\textbf{Labit, Antoine} (1832–1912) \& \textbf{Georges} (1862–1899) & Père et fils : Antoine Labit est associé au grand magasin toulousain \textit{La Maison Universelle} et Georges fonde le musée portant son nom (INHA, notice Labit ; POP, \texttt{IA31110776}). Combes mentionne les magasins Labit à la vue \#134. Les vues \#057–\#058 n'établissent pas une visite au musée. \\
\bottomrule
\end{longtable}
}
\par}
"""

    body_parts = [preamble, "\n\\mainmatter\n\\renewcommand{\\thesection}{\\thechapter.\\arabic{section}}\n"]

    rec_by_num = {r["scan_num"]: r for r in records}

    for ch in CHAPTERS:
        ch_num = ch["num"]
        ch_title = ch["title"]
        ch_sub = ch["subtitle"]
        s_start = ch["scan_start"]
        s_end = ch["scan_end"]
        ch_sum = ch["summary"]
        ch_intro = ch["intro"]
        illus_list = ch["illustrations"]

        illus_boxes = []
        for img_path, img_cap, img_w in illus_list:
            illus_boxes.append(f"""  \\begin{{minipage}}[b]{{{img_w}}}
    \\centering
    \\setlength{{\\fboxsep}}{{0.7mm}}\\setlength{{\\fboxrule}}{{0.4pt}}%
    \\fcolorbox{{gray!55}}{{white}}{{\\includegraphics[width=0.94\\linewidth,height=22mm,keepaspectratio]{{{img_path}}}}}
    \\par\\vspace{{0.6mm}}{{\\fontsize{{5.8pt}}{{6.7pt}}\\selectfont {img_cap}}}
  \\end{{minipage}}""")
        illus_joined = "\\hfill\n".join(illus_boxes)

        ch_tex = f"""
% =============================================================================
% CHAPITRE {ch_num} (SCANS #{s_start:03d} A #{s_end:03d})
% =============================================================================
\\cleardoublepage
\\chapter{{{ch_title}}}
\\markboth{{Chapitre {ch_num} — {ch_title}}}{{Scans \\#{s_start:03d} à \\#{s_end:03d}}}

\\noindent{{\\fontsize{{8pt}}{{9.2pt}}\\selectfont\\textit{{{ch_sub}}}}}\\par\\vspace{{1.2mm}}
\\noindent\\rule{{\\textwidth}}{{0.5pt}}\\par\\vspace{{0.7mm}}
\\noindent\\textbf{{\\scriptsize\\textsc{{Argument analytique (Scans \\#{s_start:03d} à \\#{s_end:03d})}}}}\\par\\vspace{{0.4mm}}
\\noindent{{\\fontsize{{6.6pt}}{{7.6pt}}\\selectfont {ch_sum}}}\\par\\vspace{{0.7mm}}
\\noindent\\rule{{\\textwidth}}{{0.3pt}}\\par\\vspace{{1.2mm}}

\\noindent\\textbf{{\\scriptsize\\textsc{{Introduction historique et philologique}}}}\\par\\vspace{{0.5mm}}
{{\\fontsize{{7.1pt}}{{8.2pt}}\\selectfont {ch_intro}}}

\\vfill
\\noindent\\begin{{center}}
{illus_joined}
\\end{{center}}
\\clearpage
"""
        body_parts.append(ch_tex)

        for s_idx in range(s_start, s_end + 1):
            body_parts.append(build_spread_latex(rec_by_num[s_idx]))

    synoptic_rows = []
    for r in records:
        snum = r["scan_num"]
        fn_esc = r["filename"].replace("_", "\\_")
        fol_esc = sanitize_latex_fragment(r["folio"])
        dt_esc = sanitize_latex_fragment(r["date"])
        li_esc = sanitize_latex_fragment(r["lieu"])
        raw_tit = r["title"]
        m_tit = re.match(r"^FOLIO\s+\d+\s+(?:RECTO|VERSO)\s*\((.*)\)$", raw_tit, re.I)
        short_tit = m_tit.group(1) if m_tit else raw_tit
        tit_esc = sanitize_latex_fragment(short_tit)
        synoptic_rows.append(
            f"\\#{snum:03d} & \\texttt{{{fn_esc}}} & {fol_esc} & {dt_esc} & \\textbf{{{li_esc}}} — {tit_esc} \\\\"
        )
    synoptic_table_body = "\n".join(synoptic_rows)

    appendices_tex = r"""
% =============================================================================
% ANNEXES DOCUMENTAIRES ET ÉPISTOLAIRES
% =============================================================================
\cleardoublepage
\appendix
\titleformat{\chapter}[display]
  {\normalfont\normalsize\bfseries}
  {\textsc{Annexe\ \Roman{chapter}}}
  {0.8mm}
  {\large\color{black}}
\chapter{Correspondance de guerre inédite et pièces justificatives (1916–1918)}
\markboth{Annexe I — Correspondance de guerre}{Annexe I — Correspondance de guerre}
{\small\sloppy

Les archives familiales d'Hippolyte Combes conservées dans le sous-répertoire \texttt{archives\_\allowbreak militaires/\allowbreak lettres\_\allowbreak de\_\allowbreak guerre/} du dépôt renferment huit pièces autographes majeures de la Grande Guerre qui éclairent directement la genèse et le contexte du \textit{Livre-Journal}. Les transcriptions de travail ci-dessous sont accompagnées de leurs références ; les dates, attributions et mots difficiles restent à contrôler sur les images. La présence d'une pièce dans ce dossier ne certifie pas sa datation ni son destinataire.

\section{Document 1 : Copie autographe d'une lettre d'Hippolyte Combes à un capitaine, ancien collègue de la Faculté de Toulouse (Au front, 21 février 1916)}
{\raggedright\noindent\textbf{Source :} dossier \texttt{archives\_\allowbreak militaires/\allowbreak lettres\_\allowbreak de\_\allowbreak guerre/}, fichier \texttt{lettre fev 1916 au front à un capitaine.pdf} (feuillet autographe quadrillé recto-verso, numéroté \texttt{111} en marge).\par}

\begin{quote}\footnotesize
« \underline{\underline{Copie}} \hfill Au front, le 21 février 1916\\[1mm]
Mon Capitaine,\\
Vous vous êtes peut-être demandé ce qu'a \textsuperscript{bien} pu devenir l'un de vos collègues \textsuperscript{de l'enseignement}, ancien camarade à la Faculté de Toulouse, et retrouvé, simple interprète à St-Omer, l'été dernier. Vous en souvient-il ?\\
À cette époque, je fus attaché à la 18\textsuperscript{e} division qui se formait dans les parages de Flesselles. Je fus choisi $[\![$comme$]\!]$ \textsuperscript{pour être} secrétaire au $[\![$membre$]\!]$ bureau de la mission française et vous ne fûtes pas étranger à ma nomination. Au bout de quinze jours, je me fatiguai de cette vie trop sédentaire et monotone et sur ma demande réitérée, je reçus une autre affectation. \textit{[verso]}\\
Depuis le mois d'août, je suis avec une compagnie d'\textit{A.S.C.} Mes officiers anglais sont de parfaits \textit{gentlemen}. Je n'ai \textsuperscript{aussi} qu'à me louer de l'officier interprète de la 18\textsuperscript{e} division [M. Pizzi est d'une haute intelligence et d'une distinction rare].\\
Vous doutez-vous, \textsuperscript{mon Capitaine}, que les $[\![$professeurs$]\!]$ \textsuperscript{universitaires, pourtant en majorité,} sont assez mal vus de quelques interprètes ? Ainsi le sergent Schumacher, qui m'a remplacé, \textsuperscript{en mon absence}, comme secrétaire au bureau de la mission, a osé dire, sans rire et devant témoins, que les professeurs sont de « rudes ânes » (\textit{sic}). Vous pensez bien que cela ne nous touche guère. Nous qui avons donné des preuves de notre intelligence et de notre culture générale, nous pouvons mépriser les boutades d'un autodidacte jaloux [N'est-il pas $[\![$un ancien$]\!]$ contremaître d'usine métallurgique \textsuperscript{et d'instruction primaire} ?].\\
Y aura-t-il bientôt un concours pour être nommé stagiaire ?\\[1mm]
\textit{[En marge gauche verticale :]} Veuillez agréer, mon Capitaine, l'expression de mes meilleurs sentiments et me croire votre bien dévoué et reconnaissant collègue — (signé) \textbf{H. C.} — »
\end{quote}

\noindent La copie du 21 février 1916 donne Saint-Omer, Flesselles, la 18\textsuperscript{e} Division et le passage d'un secrétariat à une compagnie d'A.S.C. depuis le mois d'août, soit août 1915 par référence à l'été précédent. Elle ne nomme pas la 152nd Company. Le numéro de cette unité, attestée dans le Train de la 18\textsuperscript{e} Division par \textit{The Ringing World} du 9 avril 1915, p.~184, ne peut donc être ajouté à la lettre comme un renseignement autographe.

\section{Document 2 : Rapport d'Hippolyte Combes au sous-lieutenant Ferran sur l'incident de Morlancourt (mars 1916, datation à contrôler) et requête au sujet de l'indemnité des interprètes}
{\raggedright\noindent\textbf{Source :} dossier \texttt{archives\_\allowbreak militaires/\allowbreak lettres\_\allowbreak de\_\allowbreak guerre/}, fichier \texttt{lettre de l'interprete combes pour un incident.pdf} (double feuillet autographe quadrillé numéroté p.~26, p.~27 et p.~37).\par}

\begin{quote}\footnotesize
« \textbf{1.} [p.~26] \textbf{L'interprète Combes au sous-lieutenant Ferran, officier de liaison à la 18\textsuperscript{e} division}\\[1mm]
J'ai l'honneur de porter à votre connaissance un incident qui s'est produit lundi 2[?] mars, au village de Morlancourt.\\
La matinée \textsuperscript{de ce jour}, j'avais, dans ce village, avec un de mes officiers, le lieutenant May, fait un cantonnement et nous avions \textsuperscript{choisi} une ferme que nous avait indiquée le maire de la localité. Or, l'après-midi, en l'absence de mon officier, parti au devant de notre compagnie, un lieutenant du \textit{6th Liverpool Regiment} (5\textsuperscript{th} division), \textsuperscript{dont j'ignore le nom}, arriva dans la même ferme, et \textsuperscript{après avoir inspecté les lieux}, dit à la propriétaire qu'il comptait y cantonner ses hommes. Comme cette dernière \textsuperscript{lui} faisait comprendre qu'on avait déjà retenu cette ferme, le lieutenant s'écria \textsuperscript{qu'il était chez lui et que l'interprète n'était} à prendre pour un sous-officier \textbf{2.} [p.~27] et me donna l'ordre de chercher un autre cantonnement. Devant ma protestation ferme, mais respectueuse, l'officier reprit sur un ton dédaigneux :\\
\textit{« This billet is all right for me, it shall be mine — I don't want to discuss with an interpreter. »} Je n'insistai pas et m'éloignai aussitôt.\\
Deux jours plus tard, mon capitaine a reçu une plainte dans laquelle l'officier en question \textsuperscript{(sans doute)} prétend que j'ai été insolent et que je ne l'ai pas salué. Je proteste contre ces deux allégations avec la plus grande énergie.\\[1mm]
[Je ne vous avais pas mis au courant de ces faits, car je ne croyais pas que l'incident aurait de suites]\\
\hspace*{0pt}\hfill \textbf{H. Combes}, \textit{A.S.C.} 18\textsuperscript{e} D. »
\end{quote}

\noindent\textbf{Datation :} La date de l'incident se lit \textit{lundi 2[?] mars} : le dernier chiffre est mal établi. En mars 1916, le 20 est un lundi et le 24 un vendredi ; cette concordance rend 20 possible mais ne suffit pas à déchiffrer le chiffre ni à normaliser le texte. Le jour de l'incident ne date pas nécessairement la rédaction du rapport.\par\medskip
\noindent Au verso du second feuillet (numéroté \textbf{3} en haut à gauche et \textbf{37} en bas à droite) figure la fin d'une minute de lettre adressée à un parlementaire (« Monsieur le Président ») pour la défense de l'indemnité des interprètes militaires :
\begin{quote}\footnotesize
« \textbf{3.} [p.~37] Nous sommes très utiles. Les Anglais ne sauraient se passer de nous, car très peu \textsuperscript{d'entre eux} parlent assez \textsuperscript{bien} le français pour se faire comprendre. Ils sont les premiers à reconnaître les grands services que nous leur rendons.\\
Aussi, Monsieur le Président, si vous voulez bien vous intéresser à notre sort et faire valoir \textsuperscript{à qui de droit} les considérations qui militent en faveur du maintien intégral de notre \textsuperscript{faible} indemnité.\\
Daignez agréer, Monsieur le Président, avec toutes mes excuses pour mon importunité, l'hommage de mon très profond respect.\\
\noindent \textbf{Interprète H. C.} etc. \hfill \textbf{H. C.}, prof. au coll. de Nogent-le-R. »
\end{quote}

\section{Document 3 : Lettre confidentielle intégrale d'Hippolyte Combes à sa sœur Françoise au Carmel de Périgueux (Au front, vendredi 16 juin 1916)}
{\raggedright\noindent\textbf{Source :} dossier \texttt{archives\_\allowbreak militaires/\allowbreak lettres\_\allowbreak de\_\allowbreak guerre/}, fichier \texttt{lettre de Hippolyte à sa soeur Josephine - 16 juin 1916 - Au front.pdf} (bifolium autographe de 4 pages à l'encre noire sur papier vergé ; bien que le fichier informatique ait été intitulé par erreur « à sa sœur Joséphine », celle-ci était décédée à Nogent-le-Rotrou en octobre 1914 et la lettre s'adresse à sa dernière sœur survivante, Françoise, \textit{Sœur Marie de la Croix}, carmélite à Périgueux).\par}

\begin{quote}\footnotesize
« \textit{[En marge supérieure gauche verticale :]} \textbf{Brûle ce feuillet — Je ne veux pas que tu le gardes dans tes papiers.}\\[1mm]
\hspace*{0pt}\hfill Au front, vendredi 16 juin 1916\\
Ma bien chère Sœur,\\
Ta dernière lettre m'est parvenue assez rapidement. D'ordinaire toutes les correspondances du midi mettent au moins 4 et 5 jours pour arriver à destination. Tu es toujours très contente et en parfaite santé. Que cela dure ainsi ! Amen !\\
Ici, c'est à peu près la même vie, monotone et banale. On végète, tout simplement. Je n'ai jamais aimé la campagne : maintenant je l'ai en horreur. Avec les beaux \textit{[p.~2]} jours, la vie dans de petits villages devrait être plus facilement supportable. On se consume de nostalgie et d'ennui. Voudrait-on s'amuser ? on ne trouve rien. MM. les offs, eux, vont chercher des distractions dans les grandes villes les plus rapprochées.\\
Ah ! quand enfin, démuselés, nous pourrons gueuler tout ce que nous avons vu, on ne voudra pas nous croire. J'ai entendu de mauvais Français exprimer déjà du regret à la pensée que la guerre finira tôt ou tard. C'est révoltant. À combien de gens aura-t-elle profité ?...\\
À cause de la censure, je dois me taire. \textit{[p.~3]}\\
À Toulouse, j'ai retrouvé des camarades en permission — nous avons causé, j'ai constaté avec plaisir qu'ils pensent absolument comme moi. Mon ami, le docteur de B—, dont la mère m'est tout dévouée, disait : « Jamais un officier n'entrera dans mon salon, après la guerre !.. » Sa mère et sa jeune femme, après l'avoir écouté, l'approuvaient en pensées, et je faisais chorus.\\
En tout, nous en avons tous plus qu'assez de cette vie qui se prolonge. Pour ma part, j'aimerais autant être sous terre que de rester encore une année en esclavage. On est aigri, découragé, \textit{[p.~4]} on ne prend goût à rien. Toutes ces abstractions : gloire, honneur etc. quel tas de blagues ! Vivre avant tout. Dans la mort, il n'y a plus d'alliés ni d'ennemis... Être gouverné par 1 empereur, un roi, ou n'avoir qu'un vulgaire président, c'est kif-kif — on paie les impôts — et puis qu'on nous f. la paix, tonnerre de — diable !\\
Je vais bien. Ne m'écris qu'une fois par mois, c'est plus qu'assez. Si tu savais avec quelle indifférence je parcours tes pages.\\
Je me fous de tout et de tous — Je ne demande que la liberté ou la mort.\\[1mm]
\textit{[En marge gauche verticale :]} Bien à toi, quand même — \textbf{Hippolyte} »
\end{quote}

\noindent La lettre datée du 16 juin 1916 exprime des jugements personnels sur la guerre et le service. Ces paroles sont citées comme celles de Combes ; elles ne fondent pas à elles seules une caractérisation de l'ensemble des universitaires mobilisés. L'attribution du destinataire, différente du nom du fichier, reste accompagnée de sa justification familiale.

\section{Document 4 : Poème anglais intégral de Beatrice Chilcott (\textit{Wesley Band of Hope})}
{\raggedright\noindent\textbf{Source :} dossier \texttt{archives\_\allowbreak militaires/\allowbreak lettres\_\allowbreak de\_\allowbreak guerre/}, fichier \texttt{un poeme.pdf} (feuillet autographe recto-verso en trois strophes de huit vers, signé \textit{Beatrice Chilcott, Wesley Band of Hope}).\par}

\begin{quote}\footnotesize\itshape
What, love a passion ! Heaven forbid,\\
That man should call true love by such a name,\\
Passion is but the creature of an hour,\\
A glowing ember, a bright, short lived flame ;\\
A fire, kindled from a tiny spark,\\
Glowing and live, but soon the brightness wanes ;\\
Colder and paler still, the embers grow\\
Till nought but ashes, of the fire remains.\\[2mm]
No passion lives for ever ; so\\
True love is not a passion I contend,\\
Love is, a mutual affinity,\\
A strong affection 'twixt two souls that blend,\\
Placid and pure, and deep as is the sea.\\
Love can make two souls one in heart, in thought,\\
And love comes not at will ; it is not hired,\\
Cannot be sold, neither can it be bought.\\[2mm]
A mystic power, unfathomed still,\\
Which baffles all the probing powers of man.\\
Potent, enthralling, it shapes men's destinies,\\
And silent ruled since first the world began ;\\
Heav'ns greatest gift, love is the source of life\\
Which sweetens all the bitterness and pain ;\\
And ever points toward the divine love\\
Beside which, human love is poor and vain.\\[1mm]
\normalfont\footnotesize\hspace*{0pt}\hfill — \textbf{Beatrice Chilcott}, \textit{Wesley Band of Hope}.
\end{quote}

\section{Document 5 : Correspondance de l'armistice à Marguerite Calmels-Combes (Saint-Pol, 12 novembre 1918 ; Paris, 25–26 novembre 1918 ; Les Andelys, 28 novembre – 2 décembre 1918)}
{\raggedright\noindent\textbf{Sources :} dossier \texttt{archives\_\allowbreak militaires/\allowbreak lettres\_\allowbreak de\_\allowbreak guerre/}, fichiers \texttt{lettre à bonne maman 25 novembre 1918.jpg}, \texttt{lettre du 26 novembre 1918.pdf}, \texttt{lettre 28 Novembre 1918.pdf} et \texttt{carte 2 decembre 1918.pdf}.\par}

Les quatre faces écrites des lettres des 25 et 26 novembre 1918 ont été recollationnées sur les images : les lectures ouvertes sont signalées et les phrases absentes des témoins ont été retirées. Les autres extraits ci-dessous restent des transcriptions de travail antérieures ; cette seconde passe du carnet ne vaut pas nouvelle collation intégrale de ces autres pièces.

\begin{enumerate}
  \item \textbf{Carte de Saint-Pol-sur-Ternoise au lendemain de l'Armistice (mardi 12 novembre 1918) :} Adressée à \textit{« Madame Combes, 10 rue Alfred Guibert, Millau (Aveyron) »} (cachet postal : \textit{Trésor et Postes 115, 13-11-18} ; franchise militaire : \textit{Field Service Post Card}) :
  \begin{quote}\scriptsize
  « Saint-Pol, mardi 12 nov\textsuperscript{bre} 1918. Affectueuses pensées. Bons baisers. \textbf{Hippolyte}. »
  \end{quote}
  \item \textbf{Première lettre-carte de Paris, Bibliothèque Sainte-Geneviève (lundi 25 novembre 1918, 11 h matin) :}
  \begin{quote}\scriptsize
  « \textit{[Face écrite 1, partie supérieure du JPEG]} \\
  Paris, lundi 25 novembre 1918\\
  11 h. matin\\
  Ma Chérie, ce matin à\\
  6 h., enfin je me suis retrouvé dans cette\\
  ville que je préfère à toutes les autres capitales\\
  du monde. Je ne repartirai que demain.\\
  Je n’ai pas voulu descendre chez tes cousines,\\
  à Neuilly, afin de ne point les déranger,\\
  et aussi pour me sentir plus libre. Cet\\
  après-midi j’irai les voir. Toutefois, si\\
  l’on me prie, j’accepterai à déjeuner\\
  demain seulement.\\
  {}[Avec ?] plaisir, je suis comme un\\
  voyageur $[\![$[illis.]$]\!]$\\
  {}[illis.] pays [neuf ?]. Je n’ai pu me\\
  loger [ajout suscrit : faute de place] dans mon hôtel de\\
  prédilection, University Hôtel, 160, rue St-Jacques,\\
  tout près de l’École de Droit. J’ai pris une\\
  jolie chambre à l’Hôtel du Panthéon, en\\
  face, sur le devant. Tout à l’heure, je\\
  me suis débarbouillé et bien reposé !\\
  Je t’écris dans la grande salle\\
  de la Bibliothèque Geneviève. Que de fois,\\
  {}[illis.] m’y a-t-elle accompagné ! Elle\\
  {}[illis.] à côté de moi. Comme je serais\\
  heureux de te posséder, de te sentir\\[0.8mm]
  \textit{[Marge de cette face :]} Mes plus doux baisers. Ton petitou qui t’aime si tendrement — Hippolyte.\\[0.8mm]
  \textit{[Face écrite 2, partie inférieure du JPEG]} \\
  tout près de moi ! Courage et confiance, notre\\
  séparation finira bientôt.\\
  Ma nouvelle affectation, à défaut\\
  d’avantages plus appréciables, aura du moins\\
  celui de m’avoir bien rapproché de Paris, 102\\
  kilomètres environ. De jeudi au dimanche,\\
  sans doute j’obtiendrai facilement des\\
  permissions de 24 heures. Ainsi je pourrai me\\
  rendre soit à Rouen, soit dans la capitale\\
  et aussi — et surtout — à Nogent-le-Rotrou.\\
  J’éprouverai une satisfaction profonde quand\\
  je reverrai mon chez moi du Perche,\\
  quitté depuis près de 4 ans. La maison\\
  que j’habite à Nogent, 17, rue Saint-Hilaire,\\
  est autrement jolie et pittoresque que celle\\
  de Toulouse, rue de Languedoc, [24 ?]. Elle a\\
  un petit air flamand qui lui donne une\\
  certaine originalité.\\
  {}[Santé ?] toujours parfaite. Je ne me\\
  suis jamais mieux porté, me semble-t-il.\\
  {}[Enfin ?] je me ressemble tout à fait, malgré les\\
  {}[illis.], et attends sans fièvre les\\
  événements. Je ne tarderai pas à recouvrer\\
  ma liberté entière et définitive. Ne t’alarme\\
  point au sujet de notre fillette. Elle prendra\\
  le dessus et grossira à l’aise à partir du\\
  3ème mois.\\[0.8mm]
  \textit{[Marge de cette face :]} Tu peux m’écrire à l’adresse que je t’ai indiquée dimanche. »
  \end{quote}
  \item \textbf{Deuxième lettre-carte de Paris, Bibliothèque Sainte-Geneviève (mardi 26 novembre 1918, 11 h matin) :}
  \begin{quote}\scriptsize
  « \textit{[Face écrite 1, partie supérieure de la page 1 du PDF]} \\
  Paris, mardi 26 novembre 1918\\
  11 h. matin\\
  Ma Margueritou tant aimée,\\
  Me voici de nouveau installé\\
  dans la grande salle de la Bibliothèque\\
  Sainte-Geneviève. Comme je m’y plais !\\
  Tant de souvenirs me la rendent\\
  chère ! Devant moi, sur la table, j’ai\\
  des revues françaises et un volume de\\
  Maeterlinck. Mais, au lieu de lire, je\\
  fais ma petite correspondance.\\
  J’ai passé une excellente nuit.\\
  Je me suis bien reposé. Ce soir, je\\
  continuerai et terminerai mon voyage.\\
  Je prendrai l’express du Havre, à\\
  {}[illis.] [groupe traversé de traits : gare St-Lazare, j’arriverai] à\\
  certainement après minuit. Peu m’importe !\\
  Partant par le dernier train, j’aurai\\
  pu rester qq heures de plus dans la\\
  Capitale.\\
  Hier, j’ai fait une très\\
  longue visite aux Cousines Faure. M[me ?] [illis.]\\
  descendait l’escalier, comme j’arrivais\\
  sur le 2ème étage, elle sortait avec ses\\
  {}[voisines ?], les dames [illis.], auxquelles\\
  elle m’a présenté. Elle a renoncé à\\[0.8mm]
  \textit{[Marge de cette face :]} Mes plus tendres baisers pour toutes deux. Ton mari qui t’aime [tendrement ?].\\[0.8mm]
  \textit{[Face écrite 2, partie inférieure de la page 1 du PDF]} \\
  sa promenade, pour me recevoir. Je\\
  l’avais priée de n’en rien faire. Germaine\\
  était aussi là, elle préparait ses devoirs.\\
  J’ai pu causer durant plusieurs heures avec\\
  Marguerite. Elle m’a raconté son pèlerinage\\
  bien triste à [Moyenneville ?]. Nous avons\\
  longuement parlé du pauvre défunt.\\
  {}[Toi ?] et notre fillette, naturellement,\\
  {}[avez ?] été l’inépuisable sujet de nos conversations.\\
  Ta Cousine [veut ?] t’écrire elle-même ce\\
  qu’elle pense et qu’elle te conseillerait.\\
  Je suis entièrement de son avis. Je te\\
  résumerai en qq mots ce qu’elle m’a\\
  dit à propos de notre mignonne Valentine.\\
  Tu ne dois point t’inquiéter, ni t’énerver ;\\
  avec le temps, l’enfant prendra le\\
  dessus et deviendra magnifique, comme\\
  le petit Bonhomme, que tu as vu,\\
  paraît-il, à Paris, chez les locataires du\\
  rez-de-chaussée, 26, rue d’[Angoulême ?] ;\\
  il était alors bien chétif, bien menu.\\
  Sois calme, patiente et surtout\\
  écoute ton excellente mère : apprends à\\
  dormir. Le sommeil t’est aussi nécessaire\\
  que le lait à la fillette. »
  \end{quote}
  \item \textbf{Lettres-cartes de l'École militaire préparatoire des Andelys (jeudi 28 novembre et lundi 2 décembre 1918) :}
  \begin{quote}\scriptsize
  « \textit{[1. Carte postale du 28 novembre 1918, verso :]} Les Andelys, jeudi soir 28 nov\textsuperscript{bre} 1918, École Militaire.\\
  Ma jolie Perlounette, Aujourd'hui encore, liberté entière. Je suis allé ce matin à l'École. L'emploi du temps pour l'anglais n'est pas encore fixé. Jusqu'à présent, on n'enseignait pas cette langue. Quand mon horaire aura été établi, samedi ou lundi, je commencerai mon nouveau service. À ma honte, je t'avouerai que le plus tard sera le mieux, je ne suis nullement pressé. Pour le moment, je jouis en paix d'un repos complet. Oh ! le paresseux ! Tu sais, il fait délicieux dans ma grande chambre, rue de la Sous-Préfecture. Affalé sur mon fauteuil — un vieux pouf — les jambes sur une chaise, je rumine, je lis et — je fume ! Hier soir, après dîner, j'ai travaillé deux heures à peine et je me suis mis au lit de bonne heure. Réveillé ce matin à 7 h. ½, j'ai flâné sous les couvertures une grosse demi-heure. Ensuite j'ai procédé à ma toilette qui a été très minutieuse, donc très longue. Parti à 9 h. pour l'École (20 minutes de marche environ), j'étais de retour avant 11 h. Cet après-midi, le temps étant très couvert, je ne suis pas sorti pour visiter la ville en détail.\\
  \textit{[Recto, en tête de la carte-adresse :]} Non loin de ma rue, se trouve l'église [Notre-Dame du Grand-Andely], admirable ! J'y suis entré deux minutes. Il y a de merveilleux vitraux (XIII\textsuperscript{e} et XIV\textsuperscript{e}) qui reproduisent les principaux faits de l'existence de St\textsuperscript{e} Clotilde. Cette reine avait fondé au VI\textsuperscript{e} siècle un monastère important aux Andelys. C'est là l'origine de cette petite cité. — J'ai des collègues fort sympathiques. Ce sont tous des universitaires, mobilisés eux aussi, et ne désirant qu'une chose : être libérés. Comme nous sommes des privilégiés (la plupart ont près de quarante ans ou ont dépassé la quarantaine), nous ne reprendrons nos fonctions d'avant-guerre que des premiers. En ce qui me concerne, ce sera sûrement en janvier au plus tard. Amen ! »\\[1mm]
  « \textit{[2. Carte-lettre du 2 décembre 1918 :]} École Militaire des Andelys, lundi 2 décembre 1918.\\
  Chérie, cette carte, écrite à l'encre noire, vient directement de ma chambre militaire. Tu le sais, je ne me sers que d'encre violette, dans ma chambre civile. Je ne commencerai pas les cours d'anglais avant demain mardi. Samedi 21 sera le dernier jour de classe de l'année. À mon retour de permission, en janvier, je serai presque à la veille du plus beau, du plus heureux jour de ma vie, celui où je serai enfin démobilisé. Je n'ai jamais autant désiré une chose, depuis que j'existe. En réalité, je n'aurai pas trop à me plaindre de mon séjour ici, étant donné les avantages considérables attachés à ma fonction : liberté, tranquillité et loisirs nombreux. Par moments, je me figure que je suis déjà tout à fait libre, et alors la pensée de mon bonheur très prochain fait battre mon cœur avec force. Notre séparation n'est plus qu'une question de semaines. Oh ! Dieu, la liberté, je vais donc la recouvrer ! Cette certitude me transporte d'allégresse.\\
  \textit{[En marge gauche verticale :]} Mes plus doux baisers pour Toi et pour la fillette. Ton mari qui t'aime tant, \textbf{Hippolyte}. »
  \end{quote}
\end{enumerate}
\par}

\chapter{État signalétique des services et table synoptique des 186 scans}
\markboth{Annexe II — État des services et table des scans}{Annexe II — État des services et table des scans}
{\small\sloppy

\section{Résumé de la fiche matricule d'Hippolyte Combes (Classe 1896, Matricule 911, Bureau de recrutement de Toulouse)}

\begin{figure}[htbp]
  \centering
  \begin{minipage}[b]{0.46\textwidth}
    \centering
    \includegraphics[height=42mm,keepaspectratio]{illustrations/mariage_millau_1917.jpg}
    \par\vspace{1mm}{\scriptsize\textit{Fig. 3.} Mariage d'Hippolyte et Marguerite à Millau (25 octobre 1917).}
  \end{minipage}\hfill
  \begin{minipage}[b]{0.46\textwidth}
    \centering
    \includegraphics[height=42mm,keepaspectratio]{illustrations/famille_combes_1925.jpg}
    \par\vspace{1mm}{\scriptsize\textit{Fig. 4.} Hippolyte et Marguerite Combes entourés de leurs enfants (vers 1925).}
  \end{minipage}
\end{figure}

{\raggedright\noindent D'après le registre matricule du recrutement de Toulouse (conservé dans le sous-répertoire \texttt{\footnotesize archives\_\allowbreak militaires/\allowbreak fiche\_\allowbreak et\_\allowbreak parcours/}, image \texttt{\footnotesize Fiche\_\allowbreak militaire\_\allowbreak Combes\_\allowbreak Hippolyte.jpg}, accompagnée d'une transcription dérivée) et les actes d'état civil (\texttt{\footnotesize biographie\_\allowbreak et\_\allowbreak famille/\allowbreak etat\_\allowbreak civil\_\allowbreak et\_\allowbreak actes/}) :\par}
\begin{itemize}
  \item \textbf{État civil :} \textbf{Marie Lucien Hippolyte Combes}, né le \textbf{14 août 1876} à \textbf{Millau} (Aveyron), rue des Barris (inscrit sous la date du 22 août 1876 sur la fiche matricule), et décédé le \textbf{2 septembre 1970} à l'\textbf{Hôtel du Centre} à \textbf{Saint-Chély-d'Apcher} (Lozère ; date et commune dans \texttt{Combes-3-part 2.DOC}, établissement transmis par la tradition familiale directe ; inhumé à Millau), fils de \textbf{François Augustin Hippolyte Combes} et de \textbf{Marie Anaïs Alric}, domiciliés à Toulouse (47 rue du Taur). Signalement sur l'image de la fiche : cheveux et sourcils bruns, yeux châtains, taille 1,66 m. Profession portée à l'état civil de la fiche : étudiant en droit ; ultérieurement professeur d'anglais au collège de Nogent-le-Rotrou (Eure-et-Loir) puis au lycée Ingres de Montauban.
  \item \textbf{Parcours militaire et campagnes (1914–1919) :}
    \begin{itemize}
      \item Exempté après deux ans d'ajournement pour « faiblesse générale » (numéro de tirage 74, canton de Toulouse-Nord) ; classé \textbf{Service armé} par le conseil de révision d'Eure-et-Loir le \textbf{18 décembre 1914}.
      \item Appelé à l'activité le \textbf{20 mars 1915} ; arrivé au corps le \textbf{21 mars 1915} au \textbf{10\textsuperscript{e} Régiment d'Artillerie à pied} (39\textsuperscript{e} batterie) à Toulon (campagne simple à l'intérieur du 21 mars au 3 mai 1915).
      \item Détaché à la \textbf{Mission militaire française attachée à l'Armée britannique} aux armées (campagne double) du \textbf{4 mai 1915 au 11 novembre 1918} ; passé administrativement au \textbf{19\textsuperscript{e} Escadron du Train des Équipages Militaires} le \textbf{15 octobre 1915}.
      \item Affecté auprès de la Mission française de Saint-Omer, de la 18\textsuperscript{e} Division britannique (Flesselles, juillet 1915) puis, dès août 1915, d'une compagnie d'\textit{Army Service Corps} de la 18\textsuperscript{e} Division (numéro non donné par la lettre du 21 février 1916), puis des services d'approvisionnement (\textit{Foraging} / \textit{Army Purchase Board}), sans rattachement de corps établi par le petit numéro réservé de la vue \#094.
      \item Affecté le \textbf{24 novembre 1918} à l'\textbf{École militaire préparatoire des Andelys} comme professeur d'anglais ; nommé \textbf{caporal} le \textbf{4 décembre 1918}.
      \item Mis en congé illimité de démobilisation le \textbf{7 février 1919} (se retire à Nogent-le-Rotrou, 17 rue Saint-Hilaire). La rubrique des domiciles porte le \textbf{24 janvier 1920} à Montauban et indique la profession de professeur au lycée Ingres ; cette date ne prouve pas celle de la nomination.
    \end{itemize}
\end{itemize}

\section{Table de concordance intégrale des 186 clichés numériques}

Tous les clichés originaux sont disponibles en double résolution à la racine du dépôt :
\begin{enumerate}
  \item \texttt{scans\_haute\_qualite/} : 186 fichiers JPEG haute résolution (1,03 Go au total, env. 5,9 Mo par scan) ;
  \item \texttt{scans\_compresses/} : 186 fichiers JPEG allégés pour la consultation et l'édition électronique (31,1 Mo au total).
\end{enumerate}

{\fontsize{6pt}{7pt}\selectfont
\renewcommand{\arraystretch}{1.10}
\setlength{\tabcolsep}{2.2pt}
\noindent\begin{longtable}{@{}>{\raggedright\arraybackslash}p{7.5mm}>{\raggedright\arraybackslash}p{24.5mm}>{\raggedright\arraybackslash}p{16.5mm}>{\raggedright\arraybackslash}p{24.5mm}>{\raggedright\arraybackslash}p{52mm}@{}}
\toprule
\textbf{Scan} & \textbf{Fichier JPEG} & \textbf{Vue} & \textbf{Date} & \textbf{Lieu \& Intitulé analytique} \\
\midrule
\endfirsthead
\toprule
\textbf{Scan} & \textbf{Fichier JPEG} & \textbf{Vue} & \textbf{Date} & \textbf{Lieu \& Intitulé analytique (suite)} \\
\midrule
\endhead
\bottomrule
\endfoot
""" + synoptic_table_body + r"""
\end{longtable}
}
\par}

\end{document}
"""

    body_parts.append(appendices_tex)
    full_tex = "".join(body_parts)

    with open(OUT_TEX, "w", encoding="utf-8") as f:
        f.write(full_tex)
    print(f"Successfully generated {OUT_TEX} ({len(full_tex)} bytes)")


if __name__ == "__main__":
    generate_full_tex()
