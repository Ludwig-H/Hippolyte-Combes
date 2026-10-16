# -*- coding: utf-8 -*-
"""
Generates the complete scientific philological LaTeX edition:
  /workspaces/Hippolyte-Combes/edition_philologique/carnet_hippolyte_combes.tex
modeled on Louis Hauseux's edition of Aristophanes' Thesmophories:
- Pure white, sober black-and-white typographic design.
- Continuous Arabic pagination from page 1 so that every \\pageref{fol:N} in the
  Latin loci paralleli apparatus and in the two final Indexes equals the exact
  page number of the compiled PDF file.
- Vis-à-vis spreads for all 186 folios (Couverture + Folio 1 recto to Folio 93 recto):
  * Left page (even/verso): True diplomatic transcription (with manuscript
    underlining, superscripts, horizontal separator strokes, and line numbers
    every 5 lines) + horizontally aligned marginal critical apparatus + three
    unnamed, visually distinct bottom registers:
      1. Internal critical commentary (present only when needed, flush left)
      2. Apparatus of loci paralleli in Latin (flush left, citing folio & PDF page)
      3. Concise, pertinent historical commentary (indented by 5 mm)
  * Right page (odd/recto): Full-page facsimile image with folio and month/year
    header.
- Prolégomènes with 3 TikZ genealogical trees, a general TikZ map, and explicit
  justification of the arbitrary 7-chapter editorial division.
- 7 chapters, each introduced by a 2-page spread (Left: longer analytical summary
  and historical introduction; Right: detailed TikZ vector itinerary map and
  archival illustrations).
- Two comprehensive end-of-book indexes (Index des noms de personnes and Index
  des noms de lieux) referencing both notebook folio and PDF page number.
"""

import os
import re
import json
from pathlib import Path
from cartes_et_index import (
    TIKZ_ARBRE_COMBES_ALRIC,
    TIKZ_ARBRE_CALMELS_ALLIANCES,
    TIKZ_ORGANIGRAMME_MILITAIRE,
    TIKZ_CARTE_GENERALE,
    TIKZ_CARTES_CHAPITRES,
    build_indexes_latex,
)

ROOT = str(Path(__file__).resolve().parent.parent)
JSON_PATH = os.path.join(ROOT, "transcriptions", "transcription_integrale_186_scans.json")
OUT_TEX = os.path.join(ROOT, "edition_philologique", "carnet_hippolyte_combes.tex")
SUPERSCRIPTS = {"ᵉ": "e", "ᵗ": "t", "ʳ": "r", "ᵈ": "d", "ⁿ": "n", "ˢ": "s", "ᵃ": "a", "ᵒ": "o"}


# Regex patterns for diplomatic superscripts in Hippolyte Combes's handwriting:
DIPLOMATIC_SUPERSCRIPT_PATTERNS = [
    r"\b(\d+)\s*([hH])\b(?=\s*(?:\d|1/2|m\.|s\.|matin|soir|—|–|-|,|\.|$))",
    r"\b(1)(er|ère)\b",
    r"\b(\d+)(ème|e|th|nd|rd)\b",
    r"\b(Sept|Oct|Nov|Déc)(bre|re|br|b)\b",
    r"\b(M)(me|mes|lle|lles|gr)\b",
    r"\b(S)(t|te)(?=[-\s])",
    r"\b(Marg)(te)\b",
    r"\b(M)(te)\b",
    r"\b(Hipp)(te)\b",
    r"\b(Joseph)(e)\b",
    r"\b(Mad)(ne)\b",
    r"\b([lL]ieut)(t)\b",
    r"\b(L)(t)\b",
    r"\b(R\.\s*Fus)(rs)\b",
    r"\b([dD]iv)(on)\b",
    r"\b(C)(oy)\b",
    r"\b(C)(tis)\b",
    r"\b(C)(zt)\b",
    r"\b(W)(ms)\b",
    r"\b([cC])(tes)\b",
    r"\b(p)(les)\b",
    r"\b(Norm)(le)\b",
    r"\b(Sup)(re)\b",
    r"\b(changem|cantonnem|bombardem|bombard|commencem|comm|appart|compartim|compart|départ|mouv|sentim|abrutiss|enchevêtr|enchevetr|arrang|dérang|ext|extr|merv|excessv|absol|abs|défint|définit|infinim|profondem|profond|lentem|notam|complèt|compl|entier|fortem|fort|rapid|exact|spécial|immédiat|légèr|admirab)(t|ts)\b",
    r"\b(tempér|ordin|propr|propri|milit|mil)(re)\b",
    r"\b(cath|horiz)(le)\b",
]

# Regex for leading date headers underlined in the manuscript:
DATE_PREFIX_RE = re.compile(
    r"^((?:—\s*)?(?:"
    r"Pâques\s*—\s*\d+\s*—"
    r"|—\s*Avril\s+1917\s*—"
    r"|(?:1er|\d{1,2})\s+(?:Jeudi-Saint|Lundi|Mardi|Mercredi|Jeudi|Vendredi|Samedi|Dimanche|lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche|Mar\.?|Ma\.?|Merc\.?|Mer\.?|Me\.?|Jeu\.?|J\.?|Vendr\.?|Ven\.?|Ve\.?|V\.?|Sam\.?|S\.?|Dim\.?|D\.?|Lun\.?|L\.?)\.?(?:\s*\((?:suite|fin|Rameaux)\))?(?:\s*[—–-]\s*(?:Assompt\.|1917))?"
    r"|(?:Lundi|Mardi|Mercredi|Jeudi|Vendredi|Samedi|Dimanche|lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche|Mar\.?|Ma\.?|Merc\.?|Mer\.?|Me\.?|Jeu\.?|J\.?|Vendr\.?|Ven\.?|Ve\.?|V\.?|Sam\.?|S\.?|Dim\.?|D\.?|Lun\.?|L\.?)\.?\s+(?:1er|\d{1,2})\.?(?:\s*\((?:suite|fin)\))?"
    r"))"
)

# Regex for mid-page new day entry (triggers a horizontal separator line \cline{1-1}):
MIDPAGE_DAY_START_RE = re.compile(
    r"^(?:—\s*)?(?:"
    r"(?:1er|\d{1,2})\s+(?:Jeudi-Saint|Lundi|Mardi|Mercredi|Jeudi|Vendredi|Samedi|Dimanche|lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche|Mar\.?|Ma\.?|Merc\.?|Mer\.?|Me\.?|Jeu\.?|J\.?|Vendr\.?|Ven\.?|Ve\.?|V\.?|Sam\.?|S\.?|Dim\.?|D\.?|Lun\.?|L\.?)\b"
    r"|(?:Lundi|Mardi|Mercredi|Jeudi|Vendredi|Samedi|Dimanche|lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche|Mar\.?|Ma\.?|Merc\.?|Mer\.?|Me\.?|Jeu\.?|J\.?|Vendr\.?|Ven\.?|Ve\.?|V\.?|Sam\.?|S\.?|Dim\.?|D\.?|Lun\.?|L\.?)\.?\s+(?:1er|\d{1,2})\b"
    r")"
)

# Regex for bottom accounting / expense / footnote block (triggers \cline{1-1} before its first line):
BOTTOM_ACCOUNTING_START_RE = re.compile(
    r"^(?:\[\s*|\(1\)|—\s*(?:En\s+caisse|Lunch|Dîner|Dinner|Washing|Payé|Acheté|Dépenses|Timbres|Cartes|Ctes|Tip|Groom|Bain|Coiffeur|Télégramme|Mandat|Donné|Reçu|Chocolat|Pâtisserie|Gâteaux)\b|En\s+caisse\b|A\s+(?:Mme|M\.|Renescure|Hazebrouck|Bailleul|St-Pol|Saint-Pol|Amiens|Paris|Toulouse|Millau|Acheux|Doullens|Albert)\b|Laissé\s+à\s+Mme\b|Food\b|Lunch\b|Dîner\b|Dinner\b|Washing\b|Payé\s+à\b|Acheté\b|Dépenses\b|Timbres\b|Cartes\s+ples\b|C\.\s*ples\b|Ctes\s+ples\b|Tip\b|Groom\b|Bain\b|Coiffeur\b|Télégramme\b|Mandat\b|Donné\b|Reçu\b|Pour\s+mon\b)"
)


def _escape_plain_segment(s: str) -> str:
    s = s.replace("½", "1/2")
    for char in SUPERSCRIPTS:
        s = s.replace(char, f"@@SUP{ord(char)}@@")
    s = s.replace("\\dots", "@@DOTS@@")
    s = s.replace("⟦", "@@LDEL@@").replace("⟧", "@@RDEL@@")

    # Apply diplomatic superscripts using placeholders before escaping backslashes
    sup_placeholders = []

    def _save_sup(m):
        idx = len(sup_placeholders)
        sup_placeholders.append((m.group(1), m.group(2)))
        return f"@@DSUP{idx}@@"

    for pat in DIPLOMATIC_SUPERSCRIPT_PATTERNS:
        s = re.sub(pat, _save_sup, s)

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
    s = s.replace("@@DOTS@@", "\\dots{}")
    s = s.replace("@@LDEL@@", "$[\\![$")
    s = s.replace("@@RDEL@@", "$]\\!]$")
    for char, letter in SUPERSCRIPTS.items():
        s = s.replace(f"@@SUP{ord(char)}@@", "\\textsuperscript{" + letter + "}")
    for idx, (base_txt, sup_txt) in enumerate(sup_placeholders):
        s = s.replace(f"@@DSUP{idx}@@", f"{base_txt}\\textsuperscript{{{sup_txt}}}")
    return s


def escape_diplomatic_line(s: str, line_idx: int = 1, scan_num: int = 2) -> str:
    """
    Formats a diplomatic transcription line for LaTeX with authentic manuscript features:
    - Underlining (\\underline{...}) of cover title, date headers, right-aligned month/year
      headers, and location/thematic subheadings;
    - Raised right-aligned month/year header on Line 1 when preceded by narrative text;
    - Superscripts (\\textsuperscript{...}) for hours, ordinals, and abbreviated endings.
    """
    if scan_num == 1 and line_idx == 1:
        return f"\\underline{{{_escape_plain_segment(s)}}}"

    # Split on \hfill if present
    if "\\hfill" in s:
        parts = [p.strip() for p in s.split("\\hfill")]
        left_raw = parts[0]
        right_raw = " \\hfill ".join(parts[1:])
    else:
        left_raw = s
        right_raw = None

    # Check if left_raw starts with a date header to underline
    m_date = DATE_PREFIX_RE.match(left_raw)
    if m_date:
        date_part = m_date.group(1)
        rest_part = left_raw[len(date_part):]
        left_tex = f"\\underline{{{_escape_plain_segment(date_part)}}}{_escape_plain_segment(rest_part)}"
    else:
        # Check for underlined location or thematic subheadings in accounting/narrative blocks
        m_loc = re.match(
            r"^((?:\[\s*(?:—\s*)?)?(?:A\s+(?:Renescure|Hazebrouck|Bailleul|Saint-Pol|St-Pol|Amiens|Paris|Toulouse|Millau|Doullens|Acheux)|Halles\s+Victor-Hugo|En\s+caisse|Invité|Métier\s+à\s+tisser))\b(.*)$",
            left_raw,
        )
        if m_loc:
            loc_part, rest_part = m_loc.group(1), m_loc.group(2)
            m_br = re.match(r"^(\[\s*(?:—\s*)?)(.*)$", loc_part)
            if m_br:
                prefix_br, clean_loc = m_br.group(1), m_br.group(2).strip()
                left_tex = f"{_escape_plain_segment(prefix_br)}\\underline{{{_escape_plain_segment(clean_loc)}}}{_escape_plain_segment(rest_part)}"
            else:
                left_tex = f"\\underline{{{_escape_plain_segment(loc_part)}}}{_escape_plain_segment(rest_part)}"
        else:
            left_tex = _escape_plain_segment(left_raw)

    if right_raw is not None:
        # Underline month/year headers on Line 1 (unless it's a bracketed note)
        if line_idx == 1 and not right_raw.startswith("["):
            right_inner = _escape_plain_segment(right_raw)
            if len(left_raw) > 14:
                right_tex = f"\\raisebox{{0.5ex}}{{\\underline{{{right_inner}}}}}"
            else:
                right_tex = f"\\underline{{{right_inner}}}"
        else:
            right_tex = _escape_plain_segment(right_raw)
        return f"{left_tex} \\hfill{{}} {right_tex}"

    return left_tex


def sanitize_latex_fragment(s: str) -> str:
    """
    Sanitizes a commentary, loci, or marginal note string that may already contain
    LaTeX commands (\\textbf, \\textit, \\texttt, \\pageref, \\&, \\#, \\_) or plain text.
    """
    if not s:
        return ""
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
    return s


CHAPTERS = [
    {
        "num": "I",
        "title": "De la Flandre intérieure à la vallée de la Lys",
        "subtitle": "Couverture et Folios 1 recto à 9 recto — Renescure, Lynde, Sercus, Hazebrouck, Saint-Jans-Cappel, Bailleul et La Croix-du-Bac (25 juillet – 12 août 1916)",
        "scan_start": 1,
        "scan_end": 18,
        "summary": (
            "Après la couverture autographe qui fixe les bornes chronologiques du carnet (25 juillet 1916 – 30 avril 1917), "
            "le premier chapitre suit Hippolyte Combes durant trois semaines en Flandre intérieure et dans la plaine de la Lys "
            "(f\\textsuperscript{o}~1~r\\textsuperscript{o} à f\\textsuperscript{o}~9~r\\textsuperscript{o}). "
            "Cantonné d'abord à Lynde du 25 au 28 juillet, il accompagne à pied le lieutenant Curtis au rassemblement de Sercus, "
            "assiste le lieutenant Michel pour loger trente-six officiers des \\textit{Royal Fusiliers} et profite d'une matinée libre "
            "pour visiter les deux châteaux et l'église-halle de Renescure ainsi que la ville d'Hazebrouck. "
            "Le vendredi 28 juillet, une longue étape à cheval en tête du convoi le conduit au pied du Mont-Noir, à Saint-Jans-Cappel, "
            "d'où il rayonne jusqu'au 5 août pour les achats de fourrage vert et découvre avec admiration la Grand-Place, le beffroi "
            "et les dentellières de Bailleul. Le 5 août, la compagnie descend dans la vallée alluviale de la Lys et s'établit au hameau "
            "de La Croix-du-Bac (commune de Steenwerck), à proximité du point de ravitaillement quotidien (\\textit{refilling point}) de "
            "Bac-Saint-Maur. Entre la chaleur orageuse, la poussière des convois et les promenades le long de la Lys jusqu'à l'écluse de "
            "Sailly-sur-la-Lys (où il s'entretient avec l'éclusier au sujet du général Maxse), la guerre se rappelle brutalement le "
            "11 août par le bombardement allemand de la blanchisserie Barbry aux portes d'Armentières et par la vision d'un soldat "
            "britannique soumis au supplice disciplinaire de la roue."
        ),
        "intro": (
            "Relevée du front de la Somme le 20 juillet 1916 après vingt jours de combats meurtriers au bois des Trônes et à Montauban-de-Picardie, "
            "la \\textbf{18\\textsuperscript{e} Division britannique} (\\textit{18th Eastern Division}, commandée par le major-général Sir Ivor Maxse) "
            "est transférée par voie ferrée en Flandre intérieure pour se reconstituer avant de relever les troupes australiennes dans le secteur "
            "d'Armentières et de Fleurbaix (Capt. G.~H.~F. Nichols, \\textit{The 18th Division in the Great War}, Londres, Blackwood, 1922, p.~81–85). "
            "Affecté depuis août 1915 à une compagnie du Train divisionnaire (la \\textbf{152\\textsuperscript{e} Compagnie de l'\\textit{Army Service Corps}}, "
            "chargée du ravitaillement de la 54\\textsuperscript{e} Brigade d'infanterie), Hippolyte Combes assure la liaison quotidienne entre les officiers "
            "britanniques d'approvisionnement (notamment le lieutenant Curtis), les municipalités et les exploitants agricoles flamands. "
            "Ses notes attentives sur le patrimoine architectural de la Flandre — l'église Saint-Érasme de Sercus, les châteaux de Zuthove et de "
            "Philippe de Comines à Renescure, le beffroi et les pignons Renaissance de Bailleul, ou l'église néo-gothique Notre-Dame-des-Sept-Douleurs "
            "de La Croix-du-Bac — revêtent une valeur documentaire d'autant plus précieuse que plusieurs de ces édifices furent anéantis au printemps 1918 "
            "lors de la bataille de la Lys."
        ),
        "illustrations": [
            [
                "illustrations/hippolyte_interprete_1.jpg",
                "Hippolyte Combes en uniforme d'interprète militaire attaché à l'Armée britannique (képi à bandeau et insignes au sphinx). Collection familiale Combes.",
                "0.46\\textwidth",
            ],
            [
                "illustrations/toulon_artillerie_1915.jpg",
                "Hippolyte Combes au 10\\textsuperscript{e} régiment d'artillerie à pied à Toulon (Saint-Jean-du-Var) au printemps 1915.",
                "0.46\\textwidth",
            ],
        ],
    },
    {
        "num": "II",
        "title": "De la vallée de la Lys à l’Artois et à la Somme",
        "subtitle": "Folios 9 verso à 24 verso — Armentières, Estaires, Marquay, Saint-Pol, Lucheux, Raincheval et Forceville (13 août – 24 septembre 1916)",
        "scan_start": 19,
        "scan_end": 49,
        "summary": (
            "Ce deuxième chapitre (f\\textsuperscript{o}~9~v\\textsuperscript{o} à f\\textsuperscript{o}~24~v\\textsuperscript{o}) retrace la transition "
            "de la vallée de la Lys vers les plateaux d'Artois puis vers l'arrière-front immédiat de la bataille de la Somme. "
            "Du 13 au 24 août, Hippolyte Combes célèbre son quarantième anniversaire (14 août 1916), effectue avec le lieutenant Curtis une reconnaissance "
            "à cheval sous les averses jusqu'aux villages ruinés de Fleurbaix et d'Armentières, partage le café chez l'industriel Émile Barbry avec ses "
            "collègues interprètes Lépin et Schumacher, expédie un sac de bagages vers sa maison de Nogent-le-Rotrou et visite l'église et l'hôtel de ville "
            "d'Estaires. Le vendredi 25 août, embarquée en gare de Bailleul, la compagnie gagne en train Saint-Pol-sur-Ternoise et cantonne durant deux "
            "semaines à Marquay (25 août – 9 septembre) : entre les corvées de fourrage vert (\\textit{green forage}) pour les fourgons des \\textit{Bedfords}, "
            "Hippolyte Combes note l'entrée en guerre de la Roumanie, explore les églises de Ligny-Saint-Flochel et de Saint-Michel-sur-Ternoise et flâne "
            "à plusieurs reprises dans Saint-Pol. Du 9 au 11 septembre, une marche par étapes à cheval achemine la division vers le sud par le hameau d'Oppy "
            "(Beaudricourt) et la cité médiévale de Lucheux jusqu'à Raincheval (11–22 septembre), où le capitaine West l'admet à la table du \\textit{mess} "
            "des officiers, avant le mouvement final vers Forceville (22–24 septembre) à la veille de l'assaut britannique contre Thiepval."
        ),
        "intro": (
            "Le déplacement de la \\textbf{18\\textsuperscript{e} Division britannique} de la Lys vers le Ternois puis vers le secteur de l'Ancre s'inscrit "
            "dans la préparation de la grande offensive de septembre 1916 : rattachée au \\textit{II~Corps} (lieutenant-général Sir Claud Jacob) au sein de la "
            "\\textit{Reserve Army} (future \\textit{Fifth Army}) du général Sir Hubert Gough, la division s'entraîne sur les plateaux autour de Saint-Pol avant "
            "de monter en ligne devant Thiepval, qu'elle prendra d'assaut le 26 septembre 1916 (Nichols, \\textit{op.~cit.}, p.~86–92). "
            "Sur le plan linguistique, l'écriture quotidienne d'Hippolyte Combes témoigne d'une imprégnation croissante du vocabulaire militaire et logistique "
            "anglais (\\textit{mess}, \\textit{billet}, \\textit{refilling point}, \\textit{green forage}, \\textit{horse-lines}, \\textit{orderly N.C.O.}, "
            "\\textit{on duty}, \\textit{groom}, \\textit{saddle soap}), tandis que ses méditations du 25 août dans le train de Saint-Pol font directement écho "
            "au pessimisme lucide de sa lettre confidentielle du 16 juin 1916 à sa sœur carmélite Françoise (Annexe~I, doc.~3)."
        ),
        "illustrations": [
            [
                "illustrations/hippolyte_interprete_2.jpg",
                "Portrait en buste d'Hippolyte Combes sur le front britannique (1916–1917), portant les insignes métalliques d'interprète détaché auprès de la B.E.F.",
                "0.42\\textwidth",
            ],
            [
                "illustrations/hippolyte_1897.jpg",
                "Hippolyte Combes jeune homme en 1897 (à l'âge de vingt et un ans), étudiant à Toulouse avant son séjour de quatre ans à Nottingham.",
                "0.42\\textwidth",
            ],
        ],
    },
    {
        "num": "III",
        "title": "La première permission : Paris et Toulouse",
        "subtitle": "Folios 25 recto à 33 recto — De Forceville et Acheux à Paris, Neuilly-sur-Seine et Toulouse, puis retour vers la Somme (25 septembre – 6 octobre 1916)",
        "scan_start": 50,
        "scan_end": 66,
        "summary": (
            "Le troisième chapitre (f\\textsuperscript{o}~25~r\\textsuperscript{o} à f\\textsuperscript{o}~33~r\\textsuperscript{o}) est entièrement consacré "
            "à la première permission du carnet, du 25 septembre au 6 octobre 1916. Quittant le plateau de Forceville le lundi 25 septembre sur un fourgon "
            "de ravitaillement jusqu'à la gare régulatrice (\\textit{railhead}) d'Acheux-Varennes, Hippolyte Combes gagne Amiens puis Paris à l'aube du "
            "26 septembre. Après une visite matinale à Neuilly-sur-Seine chez les cousines Faure, un déjeuner au boulevard Saint-Germain et l'achat au "
            "Quartier latin d'ouvrages d'Ernest Zyromski et de Maurice Maeterlinck, il prend le soir même à la gare d'Orsay l'express de Toulouse. "
            "Du 27 septembre au 4 octobre, il vit huit journées lumineuses à Toulouse auprès de sa fiancée Marguerite Calmels, logée chez son oncle et "
            "sa tante Émile et Élisabeth Crouzet : promenades sur les coteaux de Pouvourville et de Pech-David, achat d'un sautoir en or de fiançailles "
            "(295~francs) le 29 septembre, flâneries le long du canal du Midi et au Grand-Rond, offices à la cathédrale Saint-Étienne et rangement de "
            "sa bibliothèque dans son appartement toulousain. Reparti le 4 octobre au soir par l'express de Paris (où il admire le 5 octobre l'église "
            "Saint-Vincent-de-Paul avant de reprendre le train du front à la gare du Nord), il rejoint le 6 octobre par Doullens et le \\textit{railhead} "
            "de Canaples la 152\\textsuperscript{e} Compagnie A.S.C."
        ),
        "intro": (
            "Cette parenthèse civile au cœur de la guerre révèle l'ancrage intellectuel et familial d'Hippolyte Combes à Paris et à Toulouse. "
            "Les archives familiales de Millau et Montauban éclairent avec précision le cercle toulousain qui entoure sa fiancée \\textbf{Marguerite Calmels} "
            "(1892–1974) : l'agent de change \\textbf{Émile Crouzet} (1842–1921, \\textit{M.~C\\textsuperscript{zt}}), son épouse \\textbf{Élisabeth Calmels} "
            "(tante paternelle de Marguerite) et leur fils l'\\textbf{abbé Jean Crouzet}, futur curé de Notre-Dame de la Dalbade, ainsi que les cousines "
            "\\textbf{Faure} installées au 16, rue d'Armenonville à Neuilly-sur-Seine. Les achats en librairie du 26 septembre témoignent de la fidélité "
            "d'Hippolyte Combes à son ancien maître de la Faculté des lettres de Toulouse, \\textbf{Ernest Zyromski} (\\textit{L'Orgueil humain}, 1904), "
            "et de sa prédilection constante pour l'œuvre de \\textbf{Maurice Maeterlinck} (\\textit{Les Débris de la guerre}, 1916). "
            "Enfin, le f\\textsuperscript{o}~33~r\\textsuperscript{o} (6 octobre 1916) fournit la mention autographe décisive qui permet d'identifier "
            "formellement l'unité d'Hippolyte Combes au sein du \\textit{18th Divisional Train} : la \\textbf{152\\textsuperscript{e} Compagnie A.S.C.} "
            "(\\textit{152nd Company A.S.C.}), affectée au ravitaillement de la \\textbf{54\\textsuperscript{e} Brigade d'infanterie}."
        ),
        "illustrations": [
            [
                "illustrations/marguerite_1917.jpg",
                "Marguerite Calmels (1892–1974), photographiée par le studio Jublin à Millau à l'époque de ses fiançailles avec Hippolyte Combes.",
                "0.42\\textwidth",
            ],
            [
                "illustrations/maison_millau.jpg",
                "La demeure familiale de Millau (Aveyron), berceau de la famille Combes.",
                "0.46\\textwidth",
            ],
        ],
    },
    {
        "num": "IV",
        "title": "L’automne dans la Somme : de Ribeaucourt à Albert et Acheux",
        "subtitle": "Folios 33 verso à 52 recto — Ribeaucourt, Beauval, Warloy-Baillon, Bouzincourt, Albert et Acheux-en-Amiénois (6 octobre – 30 novembre 1916)",
        "scan_start": 67,
        "scan_end": 104,
        "summary": (
            "Le quatrième chapitre (f\\textsuperscript{o}~33~v\\textsuperscript{o} à f\\textsuperscript{o}~52~r\\textsuperscript{o}) couvre les deux mois "
            "d'octobre et de novembre 1916 sur le front de la Somme. Du 6 au 15 octobre, la 152\\textsuperscript{e} Compagnie A.S.C. jouit d'une semaine "
            "de repos dans les vergers du Ponthieu, à Ribeaucourt et au hameau de Barlette, où Hippolyte Combes visite le château de Ribeaucourt et le "
            "village voisin de Domqueur. Le 15 octobre, la colonne reprend la route du front par Beauval et Warloy-Baillon pour bivouaquer sous la tente "
            "dans la boue glaciale de Bouzincourt (17–19 octobre) puis du camp des briqueteries d'Albert (\\textit{Brickfields Area}, 19–31 octobre), où "
            "Hippolyte Combes trouve une chambre chez la famille Duchâteau, décrit avec émotion les ruines de la basilique Notre-Dame de Brebières et sa "
            "Vierge penchée, et rassure son statut d'interprète auprès du lieutenant Pizzi. Au début de novembre s'opère un tournant majeur dans son "
            "service : détaché le 2 novembre par le lieutenant-colonel Grose auprès du service des fourrages et achats d'armée (dirigé par le major Levy), "
            "il s'installe à Acheux-en-Amiénois chez le tailleur M.~Carluvant (n\\textsuperscript{o}~1, route de Léalvillers) et sillonne désormais en "
            "automobile ou à cheval les communes de l'arrière-front picard (Varennes, Léalvillers, Arquèves et la ferme de Belle-Église, Louvencourt, "
            "Bertrancourt, Bus-lès-Artois, Raincheval, Rubempré, Hérissart et le château de Martinsart)."
        ),
        "intro": (
            "Durant les mois d'octobre et de novembre 1916, tandis que les brigades de la \\textbf{18\\textsuperscript{e} Division britannique} livrent de "
            "rudes combats d'usure sous la pluie devant la redoute Schwaben, la tranchée Regina (\\textit{Regina Trench}) et les hauteurs de l'Ancre "
            "(Nichols, \\textit{op.~cit.}, chap.~VIII–IX), le \\textit{18th Divisional Train}, commandé par le \\textbf{lieutenant-colonel Daniel Charles "
            "Evans Grose, A.S.C.} (\\texttt{Col.~Grose}, f\\textsuperscript{o}~45~r\\textsuperscript{o}), assure le ravitaillement quotidien des unités "
            "depuis ses bases de Warloy-Baillon et d'Albert. Le détachement d'Hippolyte Combes à \\textbf{Acheux-en-Amiénois} le 2 novembre 1916 répond "
            "aux besoins considérables en paille et en foin de la cavalerie et des trains hippomobiles britanniques : rattaché aux services d'achats et "
            "de réquisitions (\\textit{Foraging} et \\textit{Army Purchase Board}, sous l'autorité du \\textbf{major Levy}), il contrôle les chantiers de "
            "battage mécanique (notamment à la commanderie de Belle-Église chez la famille belge Houthouan) et négocie directement avec les maires et "
            "les cultivateurs de la Somme."
        ),
        "illustrations": [
            [
                "illustrations/fiche_matricule.jpg",
                "Extrait du registre matricule d'Hippolyte Combes (classe 1896, matricule 911, bureau de recrutement de Toulouse) détaillant ses services auprès de la Mission militaire française attachée à l'Armée britannique (4 mai 1915 – 11 novembre 1918).",
                "0.76\\textwidth",
            ]
        ],
    },
    {
        "num": "V",
        "title": "L’hiver 1916–1917 à Acheux-en-Amiénois",
        "subtitle": "Folios 52 verso à 63 verso — Le capitaine Williams, les tournées de fourrage, Noël et le grand gel de janvier (1er décembre 1916 – 25 janvier 1917)",
        "scan_start": 105,
        "scan_end": 127,
        "summary": (
            "Le cinquième chapitre (f\\textsuperscript{o}~52~v\\textsuperscript{o} à f\\textsuperscript{o}~63~v\\textsuperscript{o}) relate le rude hiver "
            "1916–1917 à Acheux-en-Amiénois, du 1\\textsuperscript{er} décembre 1916 au 25 janvier 1917. Dès le 2 décembre, le lieutenant Curtis est remplacé "
            "au service des fourrages par le très jeune capitaine Williams (\\textit{Foraging Officer}), dont le caractère brusque et l'inexpérience "
            "provoquent de vives tensions morales avec l'universitaire français de quarante ans. Malgré la boue liquide de décembre puis la neige et le "
            "gel intense de janvier 1917, Hippolyte Combes accomplit chaque jour de longues tournées en automobile ou à cheval à travers toute la région "
            "entre Doullens, Albert et Amiens : Franvillers, Buire-sur-l'Ancre, Ribemont et Heilly (où il revoit avec émotion ses cantonnements de l'hiver "
            "1915–1916), Toutencourt (où il assiste le major Levy lors d'une réunion des réfugiés d'Englebelmer), Authie, Saint-Léger, Beauquesne, "
            "Raincheval, Le Quesnoy, Contay, Vadencourt, Puchevillers, Hérissart et Rubempré. Après la pénible tournée de la veille de Noël à Louvencourt "
            "avec le capitaine Williams, la fête de Noël au spectacle de music-hall de la \\textit{Y.M.C.A.} d'Acheux (qui succède aux concerts des "
            "\\textit{13th Corps Archie Singers}) et la visite du château d'Acheux occupé par la \\textit{Fifth Army School of Mortars}, il "
            "rend visite le 9 janvier près d'Hédauville à ses amis de la 150\\textsuperscript{e} Compagnie A.S.C. (dont le lieutenant Morris) avant d'obtenir "
            "fin janvier son titre de permission pour le Midi."
        ),
        "intro": (
            "Sur le plan militaire, cette période hivernale correspond à la réorganisation du dispositif britannique au nord de la Somme et de l'Ancre, "
            "avec l'extension du secteur de la \\textbf{V\\textsuperscript{e} Armée britannique} (\\textit{Fifth Army}) et la relève progressive du "
            "XIII\\textsuperscript{e} Corps par le \\textbf{V\\textsuperscript{e} Corps britannique} autour d'Acheux et de Toutencourt. "
            "La visite du 9 janvier 1917 au bivouac d'\\textbf{Hédauville} (f\\textsuperscript{o}~60~v\\textsuperscript{o}) éclaire l'articulation interne "
            "du Train divisionnaire de la 18\\textsuperscript{e} Division (\\textit{18th Divisional Train}), qui réunissait les \\textbf{150\\textsuperscript{e}, "
            "151\\textsuperscript{e}, 152\\textsuperscript{e} et 153\\textsuperscript{e} Compagnies A.S.C.} (Maj. A.~F. Becke, \\textit{Order of Battle of "
            "Divisions}, Part~3A, p.~81). Sur le plan humain, le portrait sans concession du jeune \\textbf{capitaine Williams} met en lumière la condition "
            "délicate des universitaires français détachés comme interprètes auprès d'officiers subalternes britanniques beaucoup plus jeunes qu'eux."
        ),
        "illustrations": [
            [
                "illustrations/camarades_ailly_1919.jpg",
                "Souvenir de camaraderie militaire sur le front de Picardie (carte-photo dédicacée à Hippolyte Combes, Ailly-sur-Noye, mai 1919). Collection familiale.",
                "0.50\\textwidth",
            ]
        ],
    },
    {
        "num": "VI",
        "title": "La deuxième permission : Neuilly, Toulouse et Millau",
        "subtitle": "Folios 64 recto à 73 recto — Étapes par Amiens et Neuilly-sur-Seine, séjour à Toulouse et pèlerinage familial à Millau (26 janvier – 7 février 1917)",
        "scan_start": 128,
        "scan_end": 146,
        "summary": (
            "Le sixième chapitre (f\\textsuperscript{o}~64~r\\textsuperscript{o} à f\\textsuperscript{o}~73~r\\textsuperscript{o}) retrace la permission "
            "d'hiver d'Hippolyte Combes, du 26 janvier au 7 février 1917, par un froid exceptionnel. Parti d'Acheux le 26 janvier par Amiens, il fait "
            "escale le samedi 27 janvier à Neuilly-sur-Seine chez Mme Faure (où il s'entretient avec ses cousines Germaine et Marguerite et avec Marcel "
            "Faure en permission) avant de gagner Toulouse le dimanche 28 janvier. Durant six jours à Toulouse (28 janvier – 3 février), il retrouve "
            "Marguerite Calmels et sa sœur aînée Madeleine Calmels-Vincens, achète chez l'horloger Pfister la montre-bracelet en or et les bagues de "
            "fiançailles, visite avec elles la basilique Saint-Sernin et ses cryptes, les grands magasins du Capitole et la Maison Universelle d'Antoine "
            "Labit, assiste au cours public d'Ernest Zyromski sur Maurice de Guérin à la Faculté des lettres, parcourt l'Hôtel d'Assézat, la Daurade et "
            "la Dalbade et marche jusqu'à Lardenne. Le samedi 3 février, Hippolyte Combes et Marguerite Calmels voyagent ensemble en train vers Millau "
            "en saluant l'abbé Jean Crouzet à Carcassonne et en visitant la cathédrale Saint-Nazaire de Béziers. Accueilli au 10, rue Alfred-Guibert "
            "par la famille Calmels, Hippolyte Combes rend visite aux familles Vincens et Layrals (l'oncle Charles Layrals et la tante Thérèse), revoit "
            "la sœur de Marguerite, « Mimi », et se recueille au cimetière de Millau sur les tombes des siens avant un long voyage de retour à travers "
            "la Lozère, le Cantal et l'Auvergne enneigés (Saint-Chély-d'Apcher, Saint-Flour, Brioude, Clermont-Ferrand, Paris)."
        ),
        "intro": (
            "Ce deuxième séjour dans le Midi unit pour la première fois dans le carnet les deux villes maîtresses de la vie d'Hippolyte Combes : "
            "\\textbf{Toulouse}, ville de ses études universitaires et de la famille Crouzet, et \\textbf{Millau}, berceau natal des familles Combes, "
            "Alric, Calmels et Cartairade, où sera célébré son mariage avec Marguerite Calmels le 25 octobre 1917. "
            "La collation directe du manuscrit avec les archives familiales permet d'identifier avec certitude tous les parents visités à Millau "
            "les 4 et 5 février 1917 : au 10, rue Alfred-Guibert, les parents de Marguerite (le \\textbf{D\\textsuperscript{r} Gabriel Calmels} et "
            "\\textbf{Valentine Cartairade}), son frère \\textbf{Pierre Calmels}, ses sœurs \\textbf{Madeleine Calmels} (épouse du \\textbf{D\\textsuperscript{r} "
            "Fernand Vincens}, mère de \\textbf{Germaine} et \\textbf{Robert Vincens}) et \\textbf{Anne-Marie dite « Mimi » Calmels} (1888–1975, future "
            "épouse de l'avoué \\textbf{Joseph Delcamps}), ainsi que son oncle et sa tante maternels \\textbf{M\\textsuperscript{e} Charles Layrals}, "
            "notaire à Millau, et \\textbf{Thérèse Cartairade} (f\\textsuperscript{o}~71~r\\textsuperscript{o}, l.~6 : \\texttt{visite à l'oncle \\& tante "
            "Thérèse (Layral)})."
        ),
        "illustrations": [
            [
                "illustrations/mariage_millau_1917.jpg",
                "Photographie officielle du mariage d'Hippolyte Combes (en uniforme d'interprète militaire) et de Marguerite Calmels à Millau (25 octobre 1917), entourés des familles Combes et Calmels.",
                "0.50\\textwidth",
            ],
            [
                "illustrations/menu_mariage_1917.jpg",
                "Menu du repas de noces d'Hippolyte Combes et Marguerite Calmels au 10, rue Alfred-Guibert à Millau (25 octobre 1917). Archives familiales.",
                "0.36\\textwidth",
            ],
        ],
    },
    {
        "num": "VII",
        "title": "De février à avril 1917 : Hérissart et le printemps sur la Somme",
        "subtitle": "Folios 73 verso à 93 recto — L'Army Purchase Board à Hérissart, le repli allemand sur l'Ancre, la famille Flutre et le sous-lieutenant Gilbert (7 février – 30 avril 1917)",
        "scan_start": 147,
        "scan_end": 186,
        "summary": (
            "Le septième et dernier chapitre (f\\textsuperscript{o}~73~v\\textsuperscript{o} à f\\textsuperscript{o}~93~r\\textsuperscript{o}) couvre "
            "près de trois mois, du retour de permission le 7 février jusqu'à la clôture du carnet le lundi 30 avril 1917. Le service des achats et le "
            "logement du capitaine Williams ayant été transférés d'Acheux à Hérissart pendant son absence, Hippolyte Combes s'installe à Hérissart et "
            "reprend les tournées quotidiennes de fourrage vers Toutencourt, Raincheval, Puchevillers, Rubempré, Beaucourt-sur-l'Hallue, Molliens-au-Bois, "
            "Doullens et Auxi-le-Château, tout en visitant le 10 février son ancienne 152\\textsuperscript{e} Compagnie A.S.C. au bois d'Aveluy. "
            "Le 10 mars, le départ définitif du capitaine Williams le délivre d'une cohabitation pesante ; dès le lendemain 11 mars, à la demande expresse "
            "du major Levy, Hippolyte Combes est maintenu à la commission d'achats de l'armée (\\textit{Army Purchase Board}) à Hérissart et emménage dans "
            "la chambre paisible du \\textit{billet} n\\textsuperscript{o}~220 laissée par l'interprète Valet (de la 2\\textsuperscript{e} Division "
            "australienne). Il rend visite le 13 mars au Mesnil-Martinsart au couple d'instituteurs Fortuné et Mme Flutre (parents du normalien "
            "Louis-Fernand Flutre), héberge le 19 mars un officier de la 63\\textsuperscript{e} Division navale revenant des tranchées de Miraumont et "
            "d'Achiet-le-Petit lors du repli allemand sur la ligne Hindenburg, et admire le 21 mars à Senlis-le-Sec le défilé de la cavalerie indienne et "
            "des \\textit{17th Lancers (Death or Glory Boys)}. Le mois d'avril 1917 est illuminé par l'arrivée de Pâques, par l'hospitalité chaleureuse de "
            "la famille Denis à Hérissart, par la canonnade de l'offensive d'Arras et surtout par les longues conversations littéraires et promenades "
            "printanières avec le sous-lieutenant poète Gilbert, originaire de Jersey, jusqu'à la dernière page radieuse du 30 avril 1917."
        ),
        "intro": (
            "Ce dernier trimestre du \\textit{Livre-Journal} offre un témoignage privilégié sur l'arrière-front de la Somme au moment du repli stratégique "
            "allemand vers la ligne Hindenburg (opération \\textit{Alberich}, février–mars 1917) et des offensives alliées d'avril 1917 (batailles d'Arras, "
            "de la Scarpe et de Bullecourt). Trois rencontres majeures illustrent la richesse prosopographique et historique de ces pages : "
            "le 13 mars 1917 au \\textbf{Mesnil-Martinsart} (f\\textsuperscript{o}~84~r\\textsuperscript{o}), la visite à l'instituteur \\textbf{Fortuné "
            "Flutre} et à son épouse, parents du philologue romaniste \\textbf{Louis-Fernand Flutre} (1892–1978, admis à l'École normale supérieure en 1914, "
            "agrégé en 1921 et auteur en 1955 des deux monographies de référence sur l'histoire et le parler picard du Mesnil-Martinsart ; R.~Debrie, "
            "\\textit{Revue de linguistique romane}, 42, 1978, p.~238–240) ; les 19–21 mars (f\\textsuperscript{o}~85~r\\textsuperscript{o}–v\\textsuperscript{o}), "
            "le passage de la \\textbf{63\\textsuperscript{e} Division (\\textit{Royal Naval Division})} et de la \\textbf{4\\textsuperscript{e} Division de "
            "cavalerie} (\\textit{Sialkot Cavalry Brigade}, unissant les \\textbf{17\\textsuperscript{e} Lanciers britanniques} \\textit{Death or Glory Boys} "
            "et les régiments de lanciers indiens) ; enfin, à partir du 13 avril (f\\textsuperscript{o}~89~v\\textsuperscript{o}), l'amitié intellectuelle "
            "nouée avec le \\textbf{sous-lieutenant Gilbert}, originaire de l'île anglo-normande de \\textbf{Jersey}, qui rend à Hippolyte Combes le goût "
            "des lettres et de la sérénité au seuil du printemps 1917."
        ),
        "illustrations": [
            [
                "illustrations/andelys_ecole_militaire.jpg",
                "Photographie de groupe devant l'École militaire préparatoire des Andelys (où Hippolyte Combes est nommé professeur d'anglais le 24 novembre 1918).",
                "0.31\\textwidth",
            ],
            [
                "illustrations/famille_combes_1925.jpg",
                "Hippolyte et Marguerite Combes entourés de leurs enfants à Montauban / Millau vers 1925.",
                "0.31\\textwidth",
            ],
            [
                "illustrations/hippolyte_cambridge_1930.jpg",
                "Hippolyte Combes en Angleterre (Cambridge, été 1930).",
                "0.31\\textwidth",
            ],
        ],
    },
]


def _should_insert_cline_before(lines: list[str], idx_1based: int, scan_num: int) -> bool:
    """
    Determines whether Hippolyte Combes drew a horizontal separator stroke before
    line `idx_1based` (1-indexed) on `scan_num`:
    - Case A: A new dated daily entry starts in the middle of a page (`idx_1based >= 3`).
    - Case B: A mid-page or bottom bracketed accounting block (`[ ... ]`) or the first
      line of the bottom accounting / expense / footnote block (`idx_1based >= max(4, len(lines) - 8)`).
    """
    if scan_num == 1 or idx_1based <= 2:
        return False
    line = lines[idx_1based - 1].strip()
    prev_line = lines[idx_1based - 2].strip()

    # Case A: Mid-page date header starting a new day
    if idx_1based >= 3 and MIDPAGE_DAY_START_RE.match(line):
        return True

    # Case B1: Bracketed accounting block `[ ...` anywhere from line 4 onwards
    if idx_1based >= 4 and line.startswith("[") and not prev_line.startswith("["):
        return True

    # Case B2: First line of the bottom accounting / footnote block
    n_lines = len(lines)
    start_window = max(4, n_lines - 8)
    if idx_1based >= start_window:
        if BOTTOM_ACCOUNTING_START_RE.match(line) and not BOTTOM_ACCOUNTING_START_RE.match(prev_line):
            # Ensure no earlier line in the bottom window already started an accounting block
            already_started = any(
                BOTTOM_ACCOUNTING_START_RE.match(lines[k].strip())
                for k in range(start_window - 1, idx_1based - 1)
            )
            if not already_started:
                return True

    return False


def build_spread_latex(rec: dict) -> str:
    """
    Generates the two-page vis-à-vis LaTeX code for a single folio record:
    - Even (left/verso) page: Diplomatic transcription (with underlining, superscripts,
      and horizontal separator strokes \\cline{1-1}) + horizontally aligned marginal
      apparatus + three unnamed, visually distinct bottom registers:
        1. Internal critical commentary (critique, omitted if empty)
        2. Apparatus of loci paralleli in Latin (loci)
        3. Historical commentary (historique, indented by 5 mm)
    - Odd (right/recto) page: Full-page facsimile image with folio and month/year header.
    """
    scan_num = rec["scan_num"]
    fname = rec["filename"]
    folio = sanitize_latex_fragment(rec["folio"])
    mois_annee = sanitize_latex_fragment(rec.get("mois_annee", ""))
    title = sanitize_latex_fragment(rec["title"])
    date_str = sanitize_latex_fragment(rec["date"])
    lieu_str = sanitize_latex_fragment(rec["lieu"])
    lines = rec["lines"]
    raw_mnotes = {int(k): sanitize_latex_fragment(v) for k, v in rec["marginal_notes"].items()}
    crit_str = sanitize_latex_fragment(rec.get("critique", ""))
    loci_str = sanitize_latex_fragment(rec.get("loci", ""))
    hist_str = sanitize_latex_fragment(rec["historique"])

    def _vis_len(s):
        s = re.sub(r"\\(?:textbf|textit|texttt|textsc|textsuperscript|emph)\{([^}]*)\}", r"\1", s)
        s = s.replace("$[\\![$", "[[").replace("$]\\!]$", "]]")
        s = re.sub(r"\\[a-zA-Z]+\s*", "", s)
        return len(s.replace("{", "").replace("}", "").replace("$", ""))

    mnotes = dict(raw_mnotes)
    for k in sorted(list(mnotes.keys())):
        if k not in mnotes:
            continue
        span = 1
        while True:
            needed_lines = max(1, (_vis_len(mnotes[k]) + 30) // 31)
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
    bottom_chars = len(crit_str) + len(loci_str) + len(hist_str)
    density_score = n_lines * 42 + bottom_chars
    if n_lines <= 18 and bottom_chars <= 850:
        line_font = "\\fontsize{7.7pt}{9.0pt}\\selectfont"
        note_font = "\\fontsize{6.2pt}{7.0pt}\\selectfont"
        bottom_font = "\\fontsize{6.6pt}{7.7pt}\\selectfont"
        row_stretch = "1.00"
    elif n_lines <= 22 and bottom_chars <= 950:
        line_font = "\\fontsize{7.3pt}{8.4pt}\\selectfont"
        note_font = "\\fontsize{6.1pt}{6.8pt}\\selectfont"
        bottom_font = "\\fontsize{6.5pt}{7.5pt}\\selectfont"
        row_stretch = "0.92"
    elif n_lines <= 24 and density_score <= 1950:
        line_font = "\\fontsize{6.9pt}{7.8pt}\\selectfont"
        note_font = "\\fontsize{5.9pt}{6.6pt}\\selectfont"
        bottom_font = "\\fontsize{6.3pt}{7.3pt}\\selectfont"
        row_stretch = "0.85"
    else:
        line_font = "\\fontsize{6.4pt}{7.2pt}\\selectfont"
        note_font = "\\fontsize{5.7pt}{6.4pt}\\selectfont"
        bottom_font = "\\fontsize{6.1pt}{7.0pt}\\selectfont"
        row_stretch = "0.78"

    rows_tex = []
    cline_inserted_at = -10
    extra_bottom_note_lines = 0
    for idx, l in enumerate(lines, 1):
        if (idx - cline_inserted_at >= 2) and _should_insert_cline_before(lines, idx, scan_num):
            if rows_tex and rows_tex[-1].endswith("\\\\"):
                rows_tex[-1] = rows_tex[-1][:-2] + "\\\\[1.2pt]"
            rows_tex.append("      \\cline{1-1}\\noalign{\\vspace{1.2pt}}")
            cline_inserted_at = idx

        esc_l = escape_diplomatic_line(l, idx, scan_num)
        if idx % 5 == 0:
            num_prefix = f"\\leavevmode\\llap{{\\fontsize{{6.2pt}}{{7.0pt}}\\selectfont\\color{{darkgray}}{idx}\\hspace{{1.8mm}}}}"
        else:
            num_prefix = "\\leavevmode"

        top_strut = "\\rule{0pt}{2.45ex}" if cline_inserted_at == idx else ""
        left_cell = f"{num_prefix}{line_font}\\strut{top_strut} {esc_l}\\strut"
        if idx in mnotes:
            mn = mnotes[idx]
            needed_mn_lines = max(1, (_vis_len(mn) + 30) // 31)
            rem_rows = n_lines - idx + 1
            if needed_mn_lines > rem_rows:
                extra_bottom_note_lines = max(extra_bottom_note_lines, needed_mn_lines - rem_rows)
            note_box = f"\\parbox[t]{{39mm}}{{{note_font}\\raggedright\\color{{black!88}}{mn}}}"
            right_cell = f"\\hspace*{{3.5mm}}\\smash{{{note_box}}}"
        else:
            right_cell = ""

        rows_tex.append(f"      {left_cell} & {right_cell} \\\\")

    rows_joined = "\n".join(rows_tex)
    extra_vspace = f"\\vspace{{{extra_bottom_note_lines * 2.2:.1f}mm}}" if extra_bottom_note_lines > 0 else ""

    # Build the 2 or 3 unnamed bottom registers (critique [optional], loci [Latin], historique [indented])
    bottom_blocks = []
    if crit_str:
        bottom_blocks.append(
            f"\\noindent\\normalfont {crit_str}\\par\\vspace{{0.45mm}}\n"
            f"\\noindent\\rule{{22mm}}{{0.3pt}}\\par\\vspace{{0.4mm}}"
        )
    if loci_str:
        bottom_blocks.append(
            f"\\noindent\\normalfont\\color{{black!92}} {loci_str}\\par\\vspace{{0.45mm}}\n"
            f"\\noindent\\rule{{38mm}}{{0.4pt}}\\par\\vspace{{0.45mm}}"
        )
    bottom_blocks.append(
        f"\\noindent\\hspace*{{5mm}}\\parbox{{\\dimexpr\\textwidth-5mm\\relax}}{{{bottom_font}\\color{{black!84}}{hist_str}}}\\par"
    )
    bottom_joined = "\n".join(bottom_blocks)

    tex = f"""
% =============================================================================
% VIS-A-VIS SPREAD : {folio.upper()} ({fname})
% =============================================================================
\\cleardoubleevenpage
\\renewcommand{{\\currentmonthyear}}{{{mois_annee}}}
\\renewcommand{{\\currentfoliolabel}}{{{folio}}}
\\phantomsection\\label{{fol:{scan_num}}}
% --- En-tête du folio (Page paire / gauche : Transcription, apparat & registres de bas de page) ---
\\noindent\\rule{{\\textwidth}}{{0.5pt}}\\par\\vspace{{0.5mm}}
\\noindent\\textbf{{\\footnotesize {folio.upper()}}} \\hfill \\textbf{{\\footnotesize {mois_annee.upper()}}}\\par\\vspace{{0.2mm}}
\\noindent{{\\fontsize{{6.8pt}}{{7.8pt}}\\selectfont {title}}}\\par\\vspace{{0.18mm}}
\\noindent{{\\fontsize{{6.8pt}}{{7.8pt}}\\selectfont\\textit{{{date_str}}} \\hfill \\textit{{{lieu_str}}}}}\\par\\vspace{{0.45mm}}
\\noindent\\rule{{\\textwidth}}{{0.35pt}}\\par\\vspace{{0.7mm}}
% --- Corps de la transcription diplomatique et apparat marginal en prolongement ---
{{\\renewcommand{{\\arraystretch}}{{{row_stretch}}}%
\\noindent\\hspace*{{3.5mm}}\\begin{{tabular}}{{@{{}}p{{87mm}}@{{}}p{{42.5mm}}@{{}}}}
{rows_joined}
\\end{{tabular}}}}\\par{extra_vspace}
\\vspace*{{\\fill}}
% --- Registres de bas de page (1. Critique interne [si pertinent] ; 2. Loci paralleli en latin ; 3. Commentaire historique en retrait) ---
\\noindent\\rule{{\\textwidth}}{{0.5pt}}\\par\\vspace{{0.55mm}}
{{{bottom_font}%
{bottom_joined}}}
\\newpage
\\phantomsection\\label{{fac:{scan_num}}}
% --- En-tête du fac-similé (Page impaire / droite : Photographie du manuscrit) ---
\\noindent\\rule{{\\textwidth}}{{0.5pt}}\\par\\vspace{{0.55mm}}
\\noindent\\textbf{{\\fontsize{{6.8pt}}{{7.8pt}}\\selectfont FAC-SIMILÉ EN VIS-À-VIS — {folio.upper()}}} \\hfill \\textbf{{\\fontsize{{6.8pt}}{{7.8pt}}\\selectfont {mois_annee.upper()}}}\\par\\vspace{{0.25mm}}
\\noindent{{\\fontsize{{6.8pt}}{{8.0pt}}\\selectfont\\textit{{Livre-Journal d'Hippolyte Combes}} — {date_str} ({lieu_str})}}\\par\\vspace{{0.55mm}}
\\noindent\\rule{{\\textwidth}}{{0.35pt}}\\par\\vspace*{{\\fill}}
{{\\centering
  \\setlength{{\\fboxsep}}{{1.2mm}}%
  \\setlength{{\\fboxrule}}{{0.4pt}}%
  \\fcolorbox{{gray!55}}{{white}}{{%
    \\includegraphics[width=0.95\\textwidth,height=0.81\\textheight,keepaspectratio]{{\\facsimiledir/{fname}}}%
  }}\\par}}
\\vspace*{{\\fill}}
\\newpage
"""
    return tex


def generate_full_tex():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        records = json.load(f)
    assert len(records) == 186, f"Expected 186 records, got {len(records)}"

    preamble = r"""\RequirePackage{fix-cm}
\documentclass[10pt,twoside,openany]{book}
\usepackage{fontspec}
\usepackage[french]{babel}
% Format petit in-octavo / carnet (155 x 225 mm), proche du livre de poche et homothétique au carnet autographe (ratio ~0,69)
\usepackage[paperwidth=155mm,paperheight=225mm,top=11mm,bottom=11mm,inner=12mm,outer=10mm,headheight=13.5pt,headsep=3.5mm,footskip=5mm]{geometry}
\usepackage{graphicx}
\usepackage{xcolor}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,decorations.pathmorphing,positioning,calc}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{array,booktabs,longtable}
\usepackage{fancyhdr}
\usepackage{titlesec}
\usepackage{hyperref}

% Palette sobre sur fond blanc pur (modèle de l'édition des Thesmophories)
\definecolor{darkgray}{HTML}{3A3A3A}
\definecolor{bordeaux}{HTML}{5A1818}

% Répertoire des fac-similés :
\newcommand{\facsimiledir}{../scans_compresses}
% \renewcommand{\facsimiledir}{../scans_haute_qualite}

% Macros d'en-tête courant indiquant le mois et l'année en cours ainsi que le folio :
\newcommand{\currentmonthyear}{Prolégomènes}
\newcommand{\currentfoliolabel}{Prolégomènes}

% Pages blanches de garde sans en-tête ni foliotage lors des sauts vers une belle page (impaire) ou une page paire :
\makeatletter
\def\cleardoublepage{\clearpage\if@twoside \ifodd\c@page\else
  \hbox{}\thispagestyle{empty}\newpage\if@twocolumn\hbox{}\newpage\fi\fi\fi}
\makeatother

% Saut automatique vers une page paire (gauche / verso) pour garantir le vis-à-vis strict :
\newcommand{\cleardoubleevenpage}{%
  \clearpage
  \ifodd\value{page}%
    \hbox{}\thispagestyle{empty}\newpage
  \fi
}

\pagestyle{fancy}
\fancyhf{}
\fancyhead[LE]{\scriptsize\textsc{Hippolyte Combes — Livre-Journal} \hfill \textbf{\currentmonthyear}}
\fancyhead[RO]{\scriptsize\textbf{\currentmonthyear} \hfill \textsc{\currentfoliolabel}}
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
\pagenumbering{arabic}

% =============================================================================
% 1. PREMIÈRE DE COUVERTURE (PAGE 1 DU PDF)
% =============================================================================
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
        \setlength{\fboxsep}{1.2mm}
        \setlength{\fboxrule}{0.4pt}
        \fcolorbox{black}{white}{%
          \includegraphics[width=58mm,height=50mm,keepaspectratio]{illustrations/vignette_couverture.jpg}%
        }\\[4.5mm]
        {\normalsize\textsc{Édition philologique, diplomatique et critique en vis-à-vis}}\\[2mm]
        {\scriptsize Transcription diplomatique intégrale des 93 folios numérotée de 5 en 5 lignes,\\
        apparat critique marginal aligné, apparat des \textit{loci paralleli},\\
        commentaire historique et fac-similés en regard}\par
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
\newpage

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
  {\footnotesize\textbf{Édition philologique, diplomatique et critique intégrale}}\\[1.5mm]
  {\scriptsize accompagnée d'arbres généalogiques, de cartes vectorielles d'itinéraires,\\
  des lettres de guerre inédites (1916–1918), de l'état signalétique des services\\
  et d'un double index des personnes et des lieux}\par
  \vfill
  {\footnotesize\textsc{Collection des Sources et Manuscrits Contemporains}}\\
  {\scriptsize Millau — Toulouse — Montauban — Paris}
  \vspace*{6mm}
\end{center}
\newpage

{\renewcommand{\currentmonthyear}{Table des matières}
\renewcommand{\currentfoliolabel}{Table des matières}
\small\tableofcontents}
\cleardoublepage

% =============================================================================
% 3. PROLÉGOMÈNES SCIENTIFIQUES ET HISTORIQUES
% =============================================================================
\renewcommand{\currentmonthyear}{Prolégomènes}
\renewcommand{\currentfoliolabel}{Prolégomènes}
\chapter*{Prolégomènes : Hippolyte Combes (1876–1970) et son \textit{Livre-Journal} de la Grande Guerre}
\addcontentsline{toc}{chapter}{Prolégomènes : Hippolyte Combes (1876–1970) et son \textit{Livre-Journal} de la Grande Guerre}
\renewcommand{\thesection}{\Roman{section}}
\setcounter{section}{0}
{\small

\section{Destin d'un universitaire rouergat et toulousain auprès de l'Armée britannique (1876–1970)}

L'acte de naissance n\textsuperscript{o}~395 du 16 août 1876 situe la naissance de \textbf{Marie Lucien Hippolyte Combes} à \textbf{Millau}, rue des Barris, le \textbf{14 août 1876}, fils de \textbf{François Augustin Hippolyte Combes} (1825–1899), avocat (lui-même fils de \textbf{François Combes}, 1789–1855, maître menuisier-ébéniste à Millau, et de \textbf{Madeleine Fabre-Hugou}, 1792–1863), et de \textbf{Marie Anaïs Alric} (1838–1907, fille de \textbf{Pierre Émile Alric}, 1798–1854, et de \textbf{Marie Bouquié}, 1804–1863), mariés à Millau le 22 juillet 1864. La fiche matricule porte la date du 22 août 1876 : les deux témoignages sont signalés sans harmonisation silencieuse. Les pièces d'état civil et la monographie familiale rédigée par son petit-fils \textbf{Pierre Combes} (fils du magistrat \textbf{Joseph Combes}, 1921–2021, troisième des sept enfants d'Hippolyte et de Marguerite Combes) retracent ses études à l'Institution Sainte-Marie-des-Champs (Le Caousou) et à la Faculté des lettres de Toulouse (47, rue du Taur), son séjour de quatre années en Angleterre (Nottingham) et sa carrière de professeur d'anglais aux collèges de Saint-Yrieix et de Nogent-le-Rotrou (17, rue Saint-Hilaire), puis au lycée Ingres de Montauban jusqu'à sa retraite à Millau et son décès le \textbf{2 septembre 1970} à l'\textbf{Hôtel du Centre} à \textbf{Saint-Chély-d'Apcher} (Lozère), avant son inhumation au cimetière de Millau.

\begin{figure}[htbp]
  \centering
  \begin{minipage}[b]{0.46\textwidth}
    \centering
    \includegraphics[height=42mm,keepaspectratio]{illustrations/hippolyte_1897.jpg}
    \par\vspace{1mm}{\scriptsize\textit{Fig. 1.} Hippolyte Combes en 1897, à l'âge de 21 ans.}
  \end{minipage}\hfill
  \begin{minipage}[b]{0.48\textwidth}
    \centering
    \includegraphics[height=42mm,keepaspectratio]{illustrations/hippolyte_interprete_1.jpg}
    \par\vspace{1mm}{\scriptsize\textit{Fig. 2.} Hippolyte Combes en uniforme d'interprète auprès de la B.E.F. (1916).}
  \end{minipage}
\end{figure}

Exempté dans sa jeunesse pour « faiblesse générale » (\textbf{classe 1896, bureau de recrutement de Toulouse, matricule n\textsuperscript{o}~911}), Hippolyte Combes est classé « Service armé » par le conseil de révision d'Eure-et-Loir le \textbf{18 décembre 1914}. Appelé à l'activité le \textbf{20 mars 1915} et incorporé le \textbf{21 mars 1915} à la 39\textsuperscript{e} batterie du \textbf{10\textsuperscript{e} régiment d'artillerie à pied} à Toulon (Saint-Jean-du-Var), il est détaché dès le \textbf{4 mai 1915} comme interprète militaire à la \textbf{Mission militaire française attachée à l'Armée britannique} (administrativement rattaché au \textbf{19\textsuperscript{e} escadron du Train des équipages militaires} le 15 octobre 1915) :

\begin{itemize}
  \item \textbf{Depuis août 1915 : service dans la 152\textsuperscript{e} Compagnie A.S.C. de la 18\textsuperscript{e} Division britannique.} Dans la copie autographe de sa lettre du 21 février 1916 (Annexe~I, doc.~1, p.~\pageref{annexe:doc1}), Hippolyte Combes écrit avoir été rattaché à l'été 1915 à la \textbf{18\textsuperscript{e} Division britannique} (\textit{18th Eastern Division}, commandée par le major-général Sir Ivor Maxse) qui se formait autour de Flesselles, avoir servi quinze jours au secrétariat de la Mission française (sous l'officier interprète divisionnaire M.~Pizzi), puis être affecté depuis le mois d'août 1915 à une compagnie d'\textit{Army Service Corps}. Le carnet précise le numéro de cette unité, la \textbf{152nd Company A.S.C.}, rattachée au \textit{18th Divisional Train} et chargée du ravitaillement de la \textit{54th Brigade} (f\textsuperscript{o}~33~r\textsuperscript{o}, p.~\pageref{fol:66}), relate sa démarche au \textit{Train Office} auprès du \textbf{lieutenant-colonel D.~C.~E. Grose} (f\textsuperscript{o}~45~r\textsuperscript{o}, p.~\pageref{fol:90}), et mentionne le 9 janvier 1917 une visite amicale à la \textbf{150th Company A.S.C., 18th Division}, près d'Hédauville (f\textsuperscript{o}~60~v\textsuperscript{o}, p.~\pageref{fol:121}).
  \item \textbf{Du Train divisionnaire aux services d'achats et de réquisitions (\textit{Foraging} / \textit{Army Purchase Board}, juillet 1916 – avril 1917).} Le carnet suit les déplacements d'Hippolyte Combes en Flandre intérieure (Lynde, Sercus, Renescure, Hazebrouck, Saint-Jans-Cappel, Bailleul) et dans la vallée de la Lys (La Croix-du-Bac, Bac-Saint-Maur, Sailly-sur-la-Lys, Armentières, Fleurbaix, Estaires), puis son transfert ferroviaire du \textbf{25 août 1916} vers Marquay par Saint-Pol-sur-Ternoise (f\textsuperscript{o}~13~v\textsuperscript{o}–14~r\textsuperscript{o}, p.~\pageref{fol:27}–\pageref{fol:28}) et sa remontée à cheval vers la Somme (Oppy/Beaudricourt, Lucheux, Raincheval, Acheux, Forceville). Après sa première permission à Paris et Toulouse (25 septembre – 6 octobre 1916) et son séjour d'octobre autour de Ribeaucourt et d'Albert, Hippolyte Combes est affecté le 2 novembre 1916 au service des fourrages et réquisitions à \textbf{Acheux-en-Amiénois} puis à \textbf{Hérissart}, d'abord avec le lieutenant Curtis, puis avec le capitaine Williams (décembre 1916 – mars 1917). Le 11 mars 1917, il est maintenu à l'\textit{Army Purchase Board} sur la demande expresse du \textbf{major Levy} (f\textsuperscript{o}~83~r\textsuperscript{o}, p.~\pageref{fol:166}) et se lie d'amitié en avril 1917 avec le sous-lieutenant poète \textbf{Gilbert}, originaire de Jersey (f\textsuperscript{o}~89~v\textsuperscript{o}, p.~\pageref{fol:179}).
  \item \textbf{Mariage, fin de campagne et carrière d'après-guerre.} Hippolyte Combes épouse \textbf{Marie Marguerite Calmels} (1892–1974) à Millau le \textbf{25 octobre 1917}. Affecté à l'École militaire préparatoire des Andelys comme professeur d'anglais le 24 novembre 1918 (nommé caporal le 4 décembre 1918), il est démobilisé le 7 février 1919 et nommé en 1920 professeur au lycée Ingres de Montauban.
\end{itemize}
""" + TIKZ_CARTE_GENERALE + r"""

\section{Présentation des protagonistes et arbres généalogiques}

Afin d'éclairer d'emblée les nombreuses mentions familiales, mondaines, militaires et universitaires qui parcourent le \textit{Livre-Journal}, les trois schémas généalogiques et prosopographiques ci-dessous présentent successivement : (I)~l'ascendance, la fratrie et la descendance d'Hippolyte Combes ; (II)~la famille de sa fiancée Marguerite Calmels et ses alliances à Millau, Toulouse et Neuilly-sur-Seine (branches Calmels, Cartairade, Crouzet, Vincens, Delcamps, Layrals et Faure) ; (III)~l'organigramme des officiers britanniques et français, collègues interprètes et universitaires côtoyés par Hippolyte Combes de 1915 à 1918.

""" + TIKZ_ARBRE_COMBES_ALRIC + "\n\\medskip\n" + TIKZ_ARBRE_CALMELS_ALLIANCES + "\n\\medskip\n" + TIKZ_ORGANIGRAMME_MILITAIRE + r"""

\section{Histoire matérielle, codicologie et paléographie du \textit{Livre-Journal}}

Le manuscrit autographe d'Hippolyte Combes se compose du plat supérieur de la couverture (revêtu d'un papier fort rouge à motif de losanges gaufrés sur lequel est collée une étiquette rectangulaire de papier bleu portant à l'encre noire l'intitulé autographe en cinq lignes : \textit{\underline{Livre - Journal} / — / Du 25 juillet 1916 / au 30 avril 1917 / —}) et d'une séquence de \textbf{93 folios} (\texttt{Folio 1 recto} à \texttt{Folio 93 recto}).

\begin{enumerate}
  \item \textbf{Ductus, soulignements et système abréviatif d'Hippolyte Combes.} L'écriture d'Hippolyte Combes est une cursive latine penchée, rapide et déliée, riche en abréviations par suspension et par lettres suscrites : \textit{ds} (\textit{dans}), \textit{pr} (\textit{pour}), \textit{s/} (\textit{sur}), \textit{j'à / j'au / j'aux} ou \textit{ju} (\textit{jusqu'à, jusqu'au, jusqu'aux}), \textit{lgt / lgs / longt} (\textit{longtemps}), \textit{tt / tte / ts} (\textit{tout, toute, tous}), \textit{tjs / tjours} (\textit{toujours}), \textit{qq} (\textit{quelques}), \textit{gd / gde / gds} (\textit{grand, grande, grands}), \textit{bp / bcp} (\textit{beaucoup}), \textit{cme} (\textit{comme}), \textit{chz} (\textit{chez}), ainsi que les finales adverbiales ou nominales suscrites (\textit{ext\textsuperscript{t}, merv\textsuperscript{t}, définit\textsuperscript{t}, admirab\textsuperscript{t}, appart\textsuperscript{t}, cantonnem\textsuperscript{t}, changem\textsuperscript{t}, propri\textsuperscript{re}, cath\textsuperscript{le}, c\textsuperscript{tes} p\textsuperscript{les}}). Conformément à l'usage diplomatique, la présente édition restitue fidèlement :
  \begin{itemize}
    \item les \textbf{soulignements autographes} (\texttt{\textbackslash underline\{...\}}) : dates en tête d'entrée (\textit{\underline{25 Ma.}}, \textit{\underline{26 Mer.}}, etc.), rappels du mois et de l'année dans l'angle supérieur droit (\textit{\underline{Juillet 1916}}, parfois légèrement surélevés au-dessus de la première ligne d'écriture comme au f\textsuperscript{o}~1~r\textsuperscript{o}), et sous-titres topographiques des blocs de dépenses (\textit{\underline{A Renescure}}, \textit{\underline{A Hazebrouck}}, \textit{\underline{En caisse}}) ;
    \item les \textbf{traits horizontaux de séparation} tracés par Hippolyte Combes à travers la page, soit entre deux journées successives réunies sur un même folio, soit au-dessus du relevé comptable ou d'une note infrapaginale en pied de page ;
    \item les \textbf{lettres suscrites} (\textit{8\textsuperscript{H}}, \textit{7\textsuperscript{h} 1/2}, \textit{Marg\textsuperscript{te}}, \textit{lieut\textsuperscript{t}}, \textit{R.~Fus\textsuperscript{rs}}, \textit{Div\textsuperscript{on}}) et les crochets ou accolades comptables (\texttt{[ ... ]}).
  \end{itemize}
  \item \textbf{Particularités de la séquence des folios.} Quelques inversions ponctuelles lors de la prise de vue photographique du carnet sont scrupuleusement signalées dans le commentaire critique et l'apparat des \textit{loci paralleli} tout en respectant l'ordre matériel de la séquence : le \textbf{Folio 17 verso} (4–5 septembre 1916, p.~\pageref{fol:35}) précède la fin du compte du 3 septembre inscrite au \textbf{Folio 18 recto} (p.~\pageref{fol:36}) ; le \textbf{Folio 31 verso} (jeudi 5 octobre 1916, p.~\pageref{fol:63}) et le \textbf{Folio 32 recto} (nuit du 4 au 5 octobre 1916, p.~\pageref{fol:64}), ainsi que le \textbf{Folio 56 recto} (22–24 décembre 1916, p.~\pageref{fol:112}) et le \textbf{Folio 56 verso} (19–21 décembre 1916, p.~\pageref{fol:113}), se présentent dans l'ordre inverse de la chronologie ; enfin, le \textbf{Folio 45 verso} (p.~\pageref{fol:91}) et le \textbf{Folio 46 verso} (p.~\pageref{fol:93}) correspondent à deux prises de vue successives du même feuillet original des 2 et 3 novembre 1916.
  \item \textbf{Caractère éditorial et arbitraire de la division en sept chapitres.} Il importe de souligner que \textbf{le manuscrit original d'Hippolyte Combes ne comporte aucune division en chapitres ni aucun titre de section} : le \textit{Livre-Journal} se présente matériellement comme une suite continue de notes quotidiennes courant sans interruption du 25 juillet 1916 au 30 avril 1917. \textbf{La répartition en sept chapitres adoptée dans la présente édition est donc purement éditoriale et arbitraire} : elle a été conçue pour offrir au lecteur des repères chronologiques et géographiques clairs en suivant pas à pas \textbf{les grands déplacements d'Hippolyte Combes} entre les Flandres, l'Artois, le front de la Somme et ses deux permissions à Paris, Toulouse et Millau.
\end{enumerate}

\section{Principes de l'édition philologique en vis-à-vis et des trois registres d'apparat}

Inspirée des principes de l'édition philologique classique (sur le modèle de l'édition savante des \textit{Thesmophories} d'Aristophane), la présente édition adopte un format maniable (\texttt{155 $\times$ 225 mm}, proche du livre de poche et homothétique au carnet original), une pagination arabe continue depuis la première page et met en regard sur chaque double page :
\begin{itemize}
  \item \textbf{En-tête courant :} L'en-tête indique en permanence, outre le folio (\texttt{Folio X recto} ou \texttt{Folio X verso}), \textbf{le mois et l'année en cours} (\textit{Juillet 1916} à \textit{Avril 1917}) afin de permettre au lecteur de se situer immédiatement dans la chronologie de la campagne.
  \item \textbf{Sur la page de gauche (page paire / verso) :}
    \begin{enumerate}
      \item \textbf{La transcription diplomatique ligne à ligne}, respectant la disposition spatiale, les soulignements, les traits horizontaux de séparation, les lettres suscrites, l'orthographe, la ponctuation et les crochets comptables \texttt{[ ... ]} du manuscrit. Les lignes sont numérotées de cinq en cinq dans la marge gauche (\texttt{5, 10, 15, 20, 25}). Les suppressions et ratures autographes sont placées entre doubles crochets droits ($[\![ \dots ]\!]$).
      \item \textbf{L'apparat critique marginal}, composé en petits caractères dans la colonne de droite dans le prolongement horizontal exact de la ligne concernée : il développe les abréviations tachygraphiques, signale les biffures du manuscrit, identifie les emprunts lexicaux anglais ou latins et précise les particularités matérielles.
      \item \textbf{En bas de page, jusqu'à trois registres dépourvus d'intitulés répétitifs mais immédiatement distingués par des filets horizontaux et un décrochement typographique franc :}
        \begin{itemize}
          \item \textit{Premier registre (critique interne, présent uniquement lorsque des précisions codicologiques ou structurelles excèdent le cadre des notes marginales) :} composé au fer à gauche immédiatement sous le filet horizontal de pleine largeur (\texttt{0,5 pt}), introduit directement par le renvoi aux lignes concernées (\textbf{l.~1--21 :}, etc., sans sous-titre thématique) et suivi d'un filet court de \texttt{22 mm}. Lorsqu'une page n'appelle aucune remarque critique interne en sus des notes marginales, ce registre est omis.
          \item \textit{Deuxième registre (apparat des \textbf{loci paralleli}, rédigé en latin) :} composé au fer à gauche entre le commentaire critique et le commentaire historique, et suivi d'un filet horizontal de \texttt{38 mm} (\texttt{0,4 pt}). Lorsqu'Hippolyte Combes mentionne une personne, une unité, un lieu ou un événement sur lequel d'autres passages du carnet (ou de la correspondance de l'Annexe~I) apportent un éclairage complémentaire, cet apparat latin renvoie simultanément \textbf{au folio du carnet} (\texttt{f\textsuperscript{o}~X~r\textsuperscript{o}/v\textsuperscript{o}}) \textbf{et à la page exacte du présent fichier PDF} (\texttt{p.~Y}).
          \item \textit{Troisième registre (commentaire historique) :} composé avec un retrait général de bloc de \texttt{5 mm} sur la gauche, il fournit de manière concise et dense l'élucidation historique, militaire, architecturale, prosopographique et littéraire du folio.
        \end{itemize}
    \end{enumerate}
  \item \textbf{Sur la page de droite (page impaire / recto) :} \textbf{le fac-similé photographique complet} du folio manuscrit correspondant en regard immédiat de sa transcription.
\end{itemize}
\par}
"""

    body_parts = [preamble, "\n\\renewcommand{\\thesection}{\\thechapter.\\arabic{section}}\n"]

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
        f_start = rec_by_num[s_start]["folio"]
        f_end = rec_by_num[s_end]["folio"]
        m_start = rec_by_num[max(s_start, 2)]["mois_annee"]
        m_end = rec_by_num[s_end]["mois_annee"]
        ch_period = m_start if m_start == m_end else f"{m_start} – {m_end}"

        illus_boxes = []
        for img_path, img_cap, img_w in illus_list:
            illus_boxes.append(
                f"""  \\begin{{minipage}}[b]{{{img_w}}}
    \\centering
    \\setlength{{\\fboxsep}}{{0.7mm}}\\setlength{{\\fboxrule}}{{0.4pt}}%
    \\fcolorbox{{gray!55}}{{white}}{{\\includegraphics[width=0.94\\linewidth,height=28mm,keepaspectratio]{{{img_path}}}}}
    \\par\\vspace{{0.6mm}}{{\\fontsize{{5.8pt}}{{6.7pt}}\\selectfont {img_cap}}}
  \\end{{minipage}}"""
            )
        illus_joined = "\\hfill\n".join(illus_boxes)
        ch_map_tikz = TIKZ_CARTES_CHAPITRES[ch_num]

        # Ouverture de chaque chapitre sur une double page en vis-à-vis (\cleardoubleevenpage) :
        # Page paire (gauche) = Titre du chapitre + Résumé analytique détaillé + Introduction historique et philologique
        # Page impaire (droite) = Grande carte vectorielle TikZ des déplacements du chapitre + Illustrations d'archives
        ch_tex = f"""
% =============================================================================
% CHAPITRE {ch_num} ({f_start.upper()} A {f_end.upper()})
% =============================================================================
\\cleardoubleevenpage
\\renewcommand{{\\currentmonthyear}}{{{ch_period}}}
\\renewcommand{{\\currentfoliolabel}}{{Chapitre {ch_num}}}
\\chapter{{{ch_title}}}

\\noindent{{\\fontsize{{7.8pt}}{{9.0pt}}\\selectfont\\textit{{{ch_sub}}}}}\\par\\vspace{{1.5mm}}
\\noindent\\rule{{\\textwidth}}{{0.5pt}}\\par\\vspace{{0.9mm}}
\\noindent\\textbf{{\\scriptsize\\textsc{{Résumé analytique du Chapitre {ch_num} ({f_start} à {f_end})}}}}\\par\\vspace{{0.5mm}}
\\noindent{{\\fontsize{{6.9pt}}{{8.1pt}}\\selectfont {ch_sum}}}\\par\\vspace{{1.0mm}}
\\noindent\\rule{{\\textwidth}}{{0.35pt}}\\par\\vspace{{1.4mm}}

\\noindent\\textbf{{\\scriptsize\\textsc{{Introduction historique et philologique}}}}\\par\\vspace{{0.6mm}}
{{\\fontsize{{7.1pt}}{{8.3pt}}\\selectfont {ch_intro}\\par}}
\\vfill
\\newpage
% --- Page de droite d'ouverture du chapitre : Carte vectorielle TikZ & Photographies d'archives ---
\\noindent\\rule{{\\textwidth}}{{0.5pt}}\\par\\vspace{{0.6mm}}
\\noindent\\textbf{{\\fontsize{{6.8pt}}{{7.8pt}}\\selectfont CARTE D'ITINÉRAIRE DU CHAPITRE {ch_num}}} \\hfill \\textbf{{\\fontsize{{6.8pt}}{{7.8pt}}\\selectfont {ch_period.upper()}}}\\par\\vspace{{0.25mm}}
\\noindent{{\\fontsize{{6.7pt}}{{7.8pt}}\\selectfont\\textit{{Déplacements, cantonnements et tournées d'Hippolyte Combes ({f_start} à {f_end})}}}}\\par\\vspace{{0.55mm}}
\\noindent\\rule{{\\textwidth}}{{0.35pt}}\\par\\vspace{{1.2mm}}
\\begin{{center}}
{ch_map_tikz}
\\end{{center}}
\\vfill
\\noindent\\rule{{\\textwidth}}{{0.3pt}}\\par\\vspace{{1.2mm}}
\\noindent\\begin{{center}}
{illus_joined}
\\end{{center}}
\\vspace*{{1mm}}
\\newpage
"""
        body_parts.append(ch_tex)

        for s_idx in range(s_start, s_end + 1):
            body_parts.append(build_spread_latex(rec_by_num[s_idx]))

    synoptic_rows = []
    for r in records:
        snum = r["scan_num"]
        fol_esc = sanitize_latex_fragment(r["folio"])
        dt_esc = sanitize_latex_fragment(r["date"])
        li_esc = sanitize_latex_fragment(r["lieu"])
        tit_esc = sanitize_latex_fragment(r["title"])
        synoptic_rows.append(
            f"{fol_esc} & p.~\\pageref{{fol:{snum}}} & {dt_esc} & \\textbf{{{li_esc}}} — {tit_esc} \\\\"
        )
    synoptic_table_body = "\n".join(synoptic_rows)

    indexes_tex = build_indexes_latex(records)

    appendices_tex = r"""
% =============================================================================
% ANNEXES DOCUMENTAIRES ET ÉPISTOLAIRES
% =============================================================================
\cleardoublepage
\appendix
\renewcommand{\currentmonthyear}{Annexe I — Correspondance}
\renewcommand{\currentfoliolabel}{Annexe I}
\titleformat{\chapter}[display]
  {\normalfont\normalsize\bfseries}
  {\textsc{Annexe\ \Roman{chapter}}}
  {0.8mm}
  {\large\color{black}}
\chapter{Correspondance de guerre inédite et pièces justificatives (1916–1918)}
\phantomsection\label{annexe:lettres}
{\small\sloppy

Les archives familiales d'Hippolyte Combes renferment huit pièces autographes majeures de la Grande Guerre qui éclairent directement la genèse et le contexte du \textit{Livre-Journal}.

\section{Document 1 : Copie autographe d'une lettre d'Hippolyte Combes à un capitaine, ancien collègue de la Faculté de Toulouse (Au front, 21 février 1916)}
\phantomsection\label{annexe:doc1}

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

\noindent Cette copie autographe du 21 février 1916 documente le passage d'Hippolyte Combes par Saint-Omer et Flesselles à l'été 1915, son rattachement à la 18\textsuperscript{e} Division britannique sous l'officier interprète divisionnaire M.~Pizzi et son affectation depuis août 1915 à une compagnie d'\textit{Army Service Corps}.

\section{Document 2 : Rapport d'Hippolyte Combes au sous-lieutenant Ferran sur l'incident de Morlancourt (mars 1916) et requête au sujet de l'indemnité des interprètes}
\phantomsection\label{annexe:doc2}

\begin{quote}\footnotesize
« \textbf{1.} [p.~26] \textbf{L'interprète Combes au sous-lieutenant Ferran, officier de liaison à la 18\textsuperscript{e} division}\\[1mm]
J'ai l'honneur de porter à votre connaissance un incident qui s'est produit lundi 2[?] mars, au village de Morlancourt.\\
La matinée \textsuperscript{de ce jour}, j'avais, dans ce village, avec un de mes officiers, le lieutenant May, fait un cantonnement et nous avions \textsuperscript{choisi} une ferme que nous avait indiquée le maire de la localité. Or, l'après-midi, en l'absence de mon officier, parti au devant de notre compagnie, un lieutenant du \textit{6th Liverpool Regiment} (5\textsuperscript{th} division), \textsuperscript{dont j'ignore le nom}, arriva dans la même ferme, et \textsuperscript{après avoir inspecté les lieux}, dit à la propriétaire qu'il comptait y cantonner ses hommes. Comme cette dernière \textsuperscript{lui} faisait comprendre qu'on avait déjà retenu cette ferme, le lieutenant s'écria \textsuperscript{qu'il était chez lui et que l'interprète n'était} à prendre pour un sous-officier \textbf{2.} [p.~27] et me donna l'ordre de chercher un autre cantonnement. Devant ma protestation ferme, mais respectueuse, l'officier reprit sur un ton dédaigneux :\\
\textit{« This billet is all right for me, it shall be mine — I don't want to discuss with an interpreter. »} Je n'insistai pas et m'éloignai aussitôt.\\
Deux jours plus tard, mon capitaine a reçu une plainte dans laquelle l'officier en question \textsuperscript{(sans doute)} prétend que j'ai été insolent et que je ne l'ai pas salué. Je proteste contre ces deux allégations avec la plus grande énergie.\\[1mm]
[Je ne vous avais pas mis au courant de ces faits, car je ne croyais pas que l'incident aurait de suites]\\
\hspace*{0pt}\hfill \textbf{H. Combes}, \textit{A.S.C.} 18\textsuperscript{e} D. »
\end{quote}

\noindent Au verso du second feuillet figure la fin d'une minute de lettre adressée à un parlementaire (« Monsieur le Président ») pour la défense de l'indemnité des interprètes militaires :
\begin{quote}\footnotesize
« \textbf{3.} [p.~37] Nous sommes très utiles. Les Anglais ne sauraient se passer de nous, car très peu \textsuperscript{d'entre eux} parlent assez \textsuperscript{bien} le français pour se faire comprendre. Ils sont les premiers à reconnaître les grands services que nous leur rendons.\\
Aussi, Monsieur le Président, si vous voulez bien vous intéresser à notre sort et faire valoir \textsuperscript{à qui de droit} les considérations qui militent en faveur du maintien intégral de notre \textsuperscript{faible} indemnité.\\
Daignez agréer, Monsieur le Président, avec toutes mes excuses pour mon importunité, l'hommage de mon très profond respect.\\
\noindent \textbf{Interprète H. C.} etc. \hfill \textbf{H. C.}, prof. au coll. de Nogent-le-R. »
\end{quote}

\section{Document 3 : Lettre confidentielle intégrale d'Hippolyte Combes à sa sœur Françoise au Carmel de Périgueux (Au front, vendredi 16 juin 1916)}
\phantomsection\label{annexe:doc3}

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

\section{Document 4 : Poème anglais intégral de Beatrice Chilcott (\textit{Wesley Band of Hope})}
\phantomsection\label{annexe:doc4}

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
\phantomsection\label{annexe:doc5}

\begin{enumerate}
  \item \textbf{Carte de Saint-Pol-sur-Ternoise au lendemain de l'Armistice (mardi 12 novembre 1918) :} Adressée à \textit{« Madame Combes, 10 rue Alfred Guibert, Millau (Aveyron) »} (cachet postal : \textit{Trésor et Postes 115, 13-11-18} ; franchise militaire : \textit{Field Service Post Card}) :
  \begin{quote}\scriptsize
  « Saint-Pol, mardi 12 nov\textsuperscript{bre} 1918. Affectueuses pensées. Bons baisers. \textbf{Hippolyte}. »
  \end{quote}
  \item \textbf{Première lettre-carte de Paris, Bibliothèque Sainte-Geneviève (lundi 25 novembre 1918, 11 h matin) :}
  \begin{quote}\scriptsize
  « Paris, lundi 25 novembre 1918, 11 h. matin.\\
  Ma Chérie, ce matin à 6 h., enfin je me suis retrouvé dans cette ville que je préfère à toutes les autres capitales du monde. Je ne repartirai que demain. Je n’ai pas voulu descendre chez tes cousines, à Neuilly, afin de ne point les déranger, et aussi pour me sentir plus libre. Cet après-midi j’irai les voir. Toutefois, si l’on me prie, j’accepterai à déjeuner demain seulement. [Avec ?] plaisir, je suis comme un voyageur $[\![$[illis.]$]\!]$ [illis.] pays [neuf ?]. Je n’ai pu me loger [ajout suscrit : faute de place] dans mon hôtel de prédilection, University Hôtel, 160, rue St-Jacques, tout près de l’École de Droit. J’ai pris une jolie chambre à l’Hôtel du Panthéon, en face, sur le devant. Tout à l’heure, je me suis débarbouillé et bien reposé ! Je t’écris dans la grande salle de la Bibliothèque Geneviève. Que de fois, [illis.] m’y a-t-elle accompagné ! Elle [illis.] à côté de moi. Comme je serais heureux de te posséder, de te sentir tout près de moi ! Courage et confiance, notre séparation finira bientôt.\\
  Ma nouvelle affectation, à défaut d’avantages plus appréciables, aura du moins celui de m’avoir bien rapproché de Paris, 102 kilomètres environ. De jeudi au dimanche, sans doute j’obtiendrai facilement des permissions de 24 heures. Ainsi je pourrai me rendre soit à Rouen, soit dans la capitale et aussi — et surtout — à Nogent-le-Rotrou. J’éprouverai une satisfaction profonde quand je reverrai mon chez moi du Perche, quitté depuis près de 4 ans. La maison que j’habite à Nogent, 17, rue Saint-Hilaire, est autrement jolie et pittoresque que celle de Toulouse, rue de Languedoc, [24 ?]. Elle a un petit air flamand qui lui donne une certaine originalité. [Santé ?] toujours parfaite. Je ne me suis jamais mieux porté, me semble-t-il. [Enfin ?] je me ressemble tout à fait, malgré les [illis.], et attends sans fièvre les événements. Je ne tarderai pas à recouvrer ma liberté entière et définitive. Ne t’alarme point au sujet de notre fillette. Elle prendra le dessus et grossira à l’aise à partir du 3ème mois.\\
  \textit{[En marge :]} Mes plus doux baisers. Ton petitou qui t’aime si tendrement — \textbf{Hippolyte}. Tu peux m’écrire à l’adresse que je t’ai indiquée dimanche. »
  \end{quote}
  \item \textbf{Deuxième lettre-carte de Paris, Bibliothèque Sainte-Geneviève (mardi 26 novembre 1918, 11 h matin) :}
  \begin{quote}\scriptsize
  « Paris, mardi 26 novembre 1918, 11 h. matin.\\
  Ma Margueritou tant aimée, Me voici de nouveau installé dans la grande salle de la Bibliothèque Sainte-Geneviève. Comme je m’y plais ! Tant de souvenirs me la rendent chère ! Devant moi, sur la table, j’ai des revues françaises et un volume de Maeterlinck. Mais, au lieu de lire, je fais ma petite correspondance. J’ai passé une excellente nuit. Je me suis bien reposé. Ce soir, je continuerai et terminerai mon voyage. Je prendrai l’express du Havre, à [illis.] [groupe traversé de traits : gare St-Lazare, j’arriverai] à certainement après minuit. Peu m’importe ! Partant par le dernier train, j’aurai pu rester qq heures de plus dans la Capitale.\\
  Hier, j’ai fait une très longue visite aux Cousines Faure. M[me ?] [illis.] descendait l’escalier, comme j’arrivais sur le 2ème étage, elle sortait avec ses [voisines ?], les dames [illis.], auxquelles elle m’a présenté. Elle a renoncé à sa promenade, pour me recevoir. Je l’avais priée de n’en rien faire. Germaine était aussi là, elle préparait ses devoirs. J’ai pu causer durant plusieurs heures avec Marguerite. Elle m’a raconté son pèlerinage bien triste à [Moyenneville ?]. Nous avons longuement parlé du pauvre défunt. [Toi ?] et notre fillette, naturellement, [avez ?] été l’inépuisable sujet de nos conversations. Ta Cousine [veut ?] t’écrire elle-même ce qu’elle pense et qu’elle te conseillerait. Je suis entièrement de son avis. Je te résumerai en qq mots ce qu’elle m’a dit à propos de notre mignonne Valentine. Tu ne dois point t’inquiéter, ni t’énerver ; avec le temps, l’enfant prendra le dessus et deviendra magnifique, comme le petit Bonhomme, que tu as vu, paraît-il, à Paris, chez les locataires du rez-de-chaussée, 26, rue d’[Angoulême ?] ; il était alors bien chétif, bien menu. Sois calme, patiente et surtout écoute ton excellente mère : apprends à dormir. Le sommeil t’est aussi nécessaire que le lait à la fillette.\\
  \textit{[En marge :]} Mes plus tendres baisers pour toutes deux. Ton mari qui t’aime [tendrement ?]. »
  \end{quote}
  \item \textbf{Lettres-cartes de l'École militaire préparatoire des Andelys (jeudi 28 novembre et lundi 2 décembre 1918) :}
  \begin{quote}\scriptsize
  « \textit{[1. Carte postale du 28 novembre 1918 :]} Les Andelys, jeudi soir 28 nov\textsuperscript{bre} 1918, École Militaire.\\
  Ma jolie Perlounette, Aujourd'hui encore, liberté entière. Je suis allé ce matin à l'École. L'emploi du temps pour l'anglais n'est pas encore fixé. Jusqu'à présent, on n'enseignait pas cette langue. Quand mon horaire aura été établi, samedi ou lundi, je commencerai mon nouveau service. À ma honte, je t'avouerai que le plus tard sera le mieux, je ne suis nullement pressé. Pour le moment, je jouis en paix d'un repos complet. Oh ! le paresseux ! Tu sais, il fait délicieux dans ma grande chambre, rue de la Sous-Préfecture. Affalé sur mon fauteuil — un vieux pouf — les jambes sur une chaise, je rumine, je lis et — je fume ! Hier soir, après dîner, j'ai travaillé deux heures à peine et je me suis mis au lit de bonne heure. Réveillé ce matin à 7 h. ½, j'ai flâné sous les couvertures une grosse demi-heure. Ensuite j'ai procédé à ma toilette qui a été très minutieuse, donc très longue. Parti à 9 h. pour l'École (20 minutes de marche environ), j'étais de retour avant 11 h. Cet après-midi, le temps étant très couvert, je ne suis pas sorti pour visiter la ville en détail.\\
  \textit{[Recto :]} Non loin de ma rue, se trouve l'église [Notre-Dame du Grand-Andely], admirable ! J'y suis entré deux minutes. Il y a de merveilleux vitraux (XIII\textsuperscript{e} et XIV\textsuperscript{e}) qui reproduisent les principaux faits de l'existence de St\textsuperscript{e} Clotilde. Cette reine avait fondé au VI\textsuperscript{e} siècle un monastère important aux Andelys. C'est là l'origine de cette petite cité. — J'ai des collègues fort sympathiques. Ce sont tous des universitaires, mobilisés eux aussi, et ne désirant qu'une chose : être libérés. Comme nous sommes des privilégiés (la plupart ont près de quarante ans ou ont dépassé la quarantaine), nous ne reprendrons nos fonctions d'avant-guerre que des premiers. En ce qui me concerne, ce sera sûrement en janvier au plus tard. Amen ! »\\[1mm]
  « \textit{[2. Carte-lettre du 2 décembre 1918 :]} École Militaire des Andelys, lundi 2 décembre 1918.\\
  Chérie, cette carte, écrite à l'encre noire, vient directement de ma chambre militaire. Tu le sais, je ne me sers que d'encre violette, dans ma chambre civile. Je ne commencerai pas les cours d'anglais avant demain mardi. Samedi 21 sera le dernier jour de classe de l'année. À mon retour de permission, en janvier, je serai presque à la veille du plus beau, du plus heureux jour de ma vie, celui où je serai enfin démobilisé. Je n'ai jamais autant désiré une chose, depuis que j'existe. En réalité, je n'aurai pas trop à me plaindre de mon séjour ici, étant donné les avantages considérables attachés à ma fonction : liberté, tranquillité et loisirs nombreux. Par moments, je me figure que je suis déjà tout à fait libre, et alors la pensée de mon bonheur très prochain fait battre mon cœur avec force. Notre séparation n'est plus qu'une question de semaines. Oh ! Dieu, la liberté, je vais donc la recouvrer ! Cette certitude me transporte d'allégresse.\\
  \textit{[En marge gauche verticale :]} Mes plus doux baisers pour Toi et pour la fillette. Ton mari qui t'aime tant, \textbf{Hippolyte}. »
  \end{quote}
\end{enumerate}
\par}

\cleardoublepage
\renewcommand{\currentmonthyear}{Annexe II — État des services}
\renewcommand{\currentfoliolabel}{Annexe II}
\chapter{État signalétique des services et table synoptique des folios}
{\small\sloppy

\section{Résumé de la fiche matricule d'Hippolyte Combes (Classe 1896, Matricule 911, Bureau de recrutement de Toulouse)}

\begin{figure}[htbp]
  \centering
  \begin{minipage}[b]{0.46\textwidth}
    \centering
    \includegraphics[height=40mm,keepaspectratio]{illustrations/mariage_millau_1917.jpg}
    \par\vspace{1mm}{\scriptsize\textit{Fig. 3.} Mariage d'Hippolyte Combes et Marguerite Calmels à Millau (25 octobre 1917).}
  \end{minipage}\hfill
  \begin{minipage}[b]{0.46\textwidth}
    \centering
    \includegraphics[height=40mm,keepaspectratio]{illustrations/famille_combes_1925.jpg}
    \par\vspace{1mm}{\scriptsize\textit{Fig. 4.} Hippolyte et Marguerite Combes entourés de leurs enfants (vers 1925).}
  \end{minipage}
\end{figure}

{\raggedright\noindent D'après le registre matricule du recrutement de Toulouse et les actes d'état civil de Millau :\par}
\begin{itemize}
  \item \textbf{État civil :} \textbf{Marie Lucien Hippolyte Combes}, né le \textbf{14 août 1876} à \textbf{Millau} (Aveyron), rue des Barris (inscrit sous la date du 22 août 1876 sur la fiche matricule), et décédé le \textbf{2 septembre 1970} à l'\textbf{Hôtel du Centre} à \textbf{Saint-Chély-d'Apcher} (Lozère ; inhumé à Millau), fils de \textbf{François Augustin Hippolyte Combes} et de \textbf{Marie Anaïs Alric}, domiciliés à Toulouse (47, rue du Taur). Signalement : cheveux et sourcils bruns, yeux châtains, taille 1,66 m. Professeur d'anglais au collège de Nogent-le-Rotrou (Eure-et-Loir) puis au lycée Ingres de Montauban.
  \item \textbf{Parcours militaire et campagnes (1914–1919) :}
    \begin{itemize}
      \item Exempté après deux ans d'ajournement pour « faiblesse générale » (numéro de tirage 74, canton de Toulouse-Nord) ; classé \textbf{Service armé} par le conseil de révision d'Eure-et-Loir le \textbf{18 décembre 1914}.
      \item Appelé à l'activité le \textbf{20 mars 1915} ; arrivé au corps le \textbf{21 mars 1915} au \textbf{10\textsuperscript{e} Régiment d'Artillerie à pied} (39\textsuperscript{e} batterie) à Toulon (campagne simple à l'intérieur du 21 mars au 3 mai 1915).
      \item Détaché à la \textbf{Mission militaire française attachée à l'Armée britannique} aux armées (campagne double) du \textbf{4 mai 1915 au 11 novembre 1918} ; passé administrativement au \textbf{19\textsuperscript{e} Escadron du Train des Équipages Militaires} le \textbf{15 octobre 1915}.
      \item Affecté auprès de la Mission française de Saint-Omer, de la 18\textsuperscript{e} Division britannique (Flesselles, juillet 1915), de la \textbf{152\textsuperscript{e} Compagnie d'\textit{Army Service Corps}} de la 18\textsuperscript{e} Division (à partir d'août 1915), puis des services d'approvisionnement (\textit{Foraging} / \textit{Army Purchase Board}) dans la Somme (novembre 1916 – avril 1917).
      \item Affecté le \textbf{24 novembre 1918} à l'\textbf{École militaire préparatoire des Andelys} comme professeur d'anglais ; nommé \textbf{caporal} le \textbf{4 décembre 1918}.
      \item Mis en congé illimité de démobilisation le \textbf{7 février 1919} (se retire à Nogent-le-Rotrou, 17, rue Saint-Hilaire, puis à Montauban le 24 janvier 1920 comme professeur au lycée Ingres).
    \end{itemize}
\end{itemize}

\section{Table synoptique des folios du \textit{Livre-Journal}}

{\fontsize{6.2pt}{7.3pt}\selectfont
\renewcommand{\arraystretch}{1.12}
\setlength{\tabcolsep}{2.5pt}
\noindent\begin{longtable}{@{}>{\raggedright\arraybackslash}p{21mm}>{\raggedright\arraybackslash}p{12mm}>{\raggedright\arraybackslash}p{26mm}>{\raggedright\arraybackslash}p{67mm}@{}}
\toprule
\textbf{Folio} & \textbf{Page} & \textbf{Date} & \textbf{Lieu \& Intitulé analytique} \\
\midrule
\endfirsthead
\toprule
\textbf{Folio} & \textbf{Page} & \textbf{Date} & \textbf{Lieu \& Intitulé analytique (suite)} \\
\midrule
\endhead
\bottomrule
\endfoot
""" + synoptic_table_body + r"""
\end{longtable}
}
\par}
""" + indexes_tex + r"""
\end{document}
"""

    body_parts.append(appendices_tex)
    full_tex = "".join(body_parts)

    with open(OUT_TEX, "w", encoding="utf-8") as f:
        f.write(full_tex)
    print(f"Successfully generated {OUT_TEX} ({len(full_tex)} bytes)")


if __name__ == "__main__":
    generate_full_tex()
