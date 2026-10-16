# -*- coding: utf-8 -*-
"""
Unifies all 186 scans (#001 to #186) of Hippolyte Combes's Livre-Journal (25 July 1916 – 30 April 1917):
- Extracts and structures Scans #001–#074 from `Carnet de campagne édition diplomatique.docx` + Scan #050
  and pairs them with the scholarly commentary in `data_scans_001_074.py`
- Integrates Scans #075–#130 (`data_scans_075_130.py`) and Scans #131–#186 (`data_scans_131_186.py`)
- Generates horizontally aligned marginal critical apparatus for every scan from genuine philological features
- Separates and enriches the two-level bottom commentary (1. Commentaire critique interne; 2. Commentaire historique)
- Exports `transcriptions/transcription_integrale_186_scans.json` and `transcriptions/transcription_integrale_186_scans.md`.
"""

import os
import re
import json
from pathlib import Path
import docx
from data_scans_001_074 import SCANS_001_074_META
from data_scans_075_130 import SCANS_075_130
from data_scans_131_186 import SCANS_131_186

ROOT = str(Path(__file__).resolve().parent.parent)


def get_sorted_scan_filenames():
    hq_dir = os.path.join(ROOT, "scans_haute_qualite")
    files = sorted([f for f in os.listdir(hq_dir) if f.endswith(".jpg")])
    assert len(files) == 186, f"Expected 186 scans, found {len(files)}"
    return files


def strip_html_keep_del(text):
    # Convert line-through spans to ⟦...⟧
    text = re.sub(
        r'<span[^>]*text-decoration:\s*line-through[^>]*>(.*?)</span>',
        r'⟦\1⟧',
        text,
        flags=re.I | re.S,
    )
    # Convert repeated &nbsp; to tab so it becomes \hfill
    text = re.sub(r'(?:&nbsp;\s*){3,}', '\t', text)
    text = text.replace('&nbsp;', ' ')
    # Strip all other HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Convert markdown superscripts like prop^re^, 1^ère^, T^s, p^r to plain/LaTeX-safe
    text = re.sub(r'\^([^\^\s]+)\^', r'\1', text)
    text = text.replace('^', '')
    return text


CHAT_TRANSITION_PREFIXES = (
    "Voici l'",
    "Voici la ",
    "Voici les ",
    "SUITE DE L'ÉDITION",
    "C'est exact",
    "C'est entendu",
    "Je vous présente",
    "Vous avez ",
    "J'ai repris",
    "Je maintiens",
    "Période :",
    "Ambiance :",
    "Thème :",
    "Corrections Majeures",
    "Ces feuillets sont",
)


def parse_docx_blocks():
    docx_path = os.path.join(ROOT, "transcriptions", "Carnet de campagne édition diplomatique.docx")
    d = docx.Document(docx_path)
    raw_paras = []
    for p in d.paragraphs:
        for subline in p.text.split("\n"):
            cleaned = strip_html_keep_del(subline).strip()
            if cleaned:
                raw_paras.append(cleaned)

    docs = []
    cur = None
    mode = None

    for p in raw_paras:
        if re.match(r"^DOCUMENT\s+\d+\s*:", p):
            if cur:
                docs.append(cur)
            cur = {"header": p, "meta": [], "lines": [], "comm": []}
            mode = "meta"
        elif cur is not None:
            if any(p.startswith(pref) for pref in CHAT_TRANSITION_PREFIXES):
                if mode == "comm":
                    mode = "skip"
                continue
            if re.match(r"^(I\.\s*Édition\s+Diplomatique|Transcription\s+diplomatique)", p, re.I):
                mode = "lines"
            elif re.match(r"^(II\.|III\.|Analyse\s+lettre|Commentaire|Apparat|Notes\s+de\s+lecture)", p, re.I):
                mode = "comm"
            elif p.startswith("Documents : 63"):
                continue
            else:
                if mode == "meta":
                    cur["meta"].append(p)
                elif mode == "lines":
                    cur["lines"].append(p)
                elif mode == "comm":
                    cur["comm"].append(p)

    if cur:
        docs.append(cur)
    assert len(docs) == 73, f"Expected 73 blocks in docx, got {len(docs)}"
    return docs


SCAN_050_DATA = {
    "title": "Départ en première permission : de Forceville au railhead d'Acheux-Varennes",
    "date": "25 septembre 1916 (matin et après-midi)",
    "lieu": "Forceville, Acheux-Varennes (Somme)",
    "lines": [
        "25 L. [Lundi]                                   Sept /16",
        "Vers 4h, s/ [sur] pied.",
        "Au firmament bleuissant, léger croissant lunaire",
        "et 2 étoiles très brillantes.",
        "Temps superbe.",
        "Bientôt, cabas prêt à partir.",
        "Journée chaude tt [tout] en haut plateau.",
        "Amené à Forceville avec Lt First, for green",
        "forage. Chaleur très forte.",
        "A midi enfin, monté sur le lourd wagon",
        "du convoi allant au railhead, puis cocher",
        "a trouvé place pr [pour] station d'Acheux-Varennes",
        "laissé mes colis à l'office de l'R.T.O. & vu",
        "village désert,",
        "puis attendu lgt. [longtemps] ds [dans] mon compartiment petit",
        "train départ 6h 40 en gare —",
        "chaleur intense",
        "[ Tip à mon groom : 2 f — Biscuits : 0.50 c",
        "  Lunch à Acheux : 1 f 50 ]",
    ],
}


# Comprehensive dictionary of genuine abbreviations & features in the manuscript
ABBREV_MAP = [
    # Days of the week
    (r"(?<![A-Za-z.])\bMa\.(?![A-Za-z])", "Ma.", "\\textit{scil.} Mardi"),
    (r"(?<![A-Za-z.])\bMar\b(?![A-Za-z])", "Mar", "\\textit{scil.} Mardi"),
    (r"(?<![A-Za-z.])\bMer\.(?![A-Za-z])", "Mer.", "\\textit{scil.} Mercredi"),
    (r"(?<![A-Za-z.])\bMerc\.(?![A-Za-z])", "Merc.", "\\textit{scil.} Mercredi"),
    (r"(?<![A-Za-z.])\bMerc\b(?![A-Za-z.])", "Merc", "\\textit{scil.} Mercredi"),
    (r"(?<![A-Za-z.])\bJ\.(?![A-Za-z]|\s*à\b)", "J.", "\\textit{scil.} Jeudi"),
    (r"(?<![A-Za-z.])\bVen\.(?![A-Za-z])", "Ven.", "\\textit{scil.} Vendredi"),
    (r"(?<![A-Za-z.])\bVendr\.(?![A-Za-z])", "Vendr.", "\\textit{scil.} Vendredi"),
    (r"(?<![A-Za-z.])\bVe\.(?![A-Za-z])", "Ve.", "\\textit{scil.} Vendredi"),
    (r"(?<![A-Za-z.])\bSam\.(?![A-Za-z])", "Sam.", "\\textit{scil.} Samedi"),
    (r"(?<![A-Za-z.])\bDim\.(?![A-Za-z])", "Dim.", "\\textit{scil.} Dimanche"),
    (r"(?<![A-Za-z.])\bL\.(?![A-Za-z])", "L.", "\\textit{scil.} Lundi"),
    (r"(?<![A-Za-z.])\bD\.(?![A-Za-z])", "D.", "\\textit{scil.} Dimanche"),
    # Prepositions, conjunctions, adverbs, pronouns
    (r"\bju\b", "ju", "\\textit{abbr. pro} jusqu'à"),
    (r"\bj'à\b", "j'à", "\\textit{abbr. pro} jusqu'à"),
    (r"\b[jJ]\.\s*à\b", "j. à", "\\textit{abbr. pro} jusqu'à"),
    (r"\bj-à\b", "j-à", "\\textit{abbr. pro} jusqu'à"),
    (r"\bj-au\b", "j-au", "\\textit{abbr. pro} jusqu'au"),
    (r"\bj-aux\b", "j-aux", "\\textit{abbr. pro} jusqu'aux"),
    (r"\bj'que\b", "j'que", "\\textit{abbr. pro} jusque"),
    (r"\bds\b", "ds", "\\textit{abbr. pro} dans"),
    (r"\bDs\b", "Ds", "\\textit{abbr. pro} Dans"),
    (r"\bpr\.?\b", "pr", "\\textit{abbr. pro} pour"),
    (r"(?<!\S)s/(?!\S)", "s/", "\\textit{abbr. pro} sur"),
    (r"\bcme\b", "cme", "\\textit{abbr. pro} comme"),
    (r"\bCme\b", "Cme", "\\textit{abbr. pro} Comme"),
    (r"\bpdt\b", "pdt", "\\textit{abbr. pro} pendant"),
    (r"\bns\b", "ns", "\\textit{abbr. pro} nous"),
    (r"\bvs\b", "vs", "\\textit{abbr. pro} vous"),
    (r"\blg\s+moment\b", "lg", "\\textit{abbr. pro} long"),
    (r"\blg\s+de\b", "lg", "\\textit{abbr. pro} le long"),
    (r"\blg\b", "lg", "\\textit{abbr. pro} longtemps"),
    (r"\blgt\.?\b", "lgt", "\\textit{abbr. pro} longtemps"),
    (r"\bLgt\b", "Lgt", "\\textit{abbr. pro} Longtemps"),
    (r"\blgts\b", "lgts", "\\textit{abbr. pro} longtemps"),
    (r"\blgs\b", "lgs", "\\textit{abbr. pro} longtemps"),
    (r"\blongt\b", "longt", "\\textit{abbr. pro} longtemps"),
    (r"\btt\b", "tt", "\\textit{abbr. pro} tout"),
    (r"\bTt\b", "Tt", "\\textit{abbr. pro} Tout"),
    (r"\btte\b", "tte", "\\textit{abbr. pro} toute"),
    (r"\bTte\b", "Tte", "\\textit{abbr. pro} Toute"),
    (r"\bttes\b", "ttes", "\\textit{abbr. pro} toutes"),
    (r"\bts\b", "ts", "\\textit{abbr. pro} tous"),
    (r"\bTs\b", "Ts", "\\textit{abbr. pro} Tous"),
    (r"\bbcp\b", "bcp", "\\textit{abbr. pro} beaucoup"),
    (r"\bbp\b", "bp", "\\textit{abbr. pro} beaucoup"),
    (r"\bqq\b", "qq", "\\textit{abbr. pro} quelque(s)"),
    (r"\bQq\b", "Qq", "\\textit{abbr. pro} Quelque(s)"),
    (r"\bqqs\b", "qqs", "\\textit{abbr. pro} quelques"),
    (r"\bQqs\b", "Qqs", "\\textit{abbr. pro} Quelques"),
    (r"\bqque\b", "qque", "\\textit{abbr. pro} quelque"),
    (r"\btjrs\b", "tjrs", "\\textit{abbr. pro} toujours"),
    (r"\bTjrs\b", "Tjrs", "\\textit{abbr. pro} Toujours"),
    (r"\btjs\b", "tjs", "\\textit{abbr. pro} toujours"),
    (r"\bTjs\b", "Tjs", "\\textit{abbr. pro} Toujours"),
    (r"\bauj'd'hui\b", "auj'd'hui", "\\textit{abbr. pro} aujourd'hui"),
    (r"\bAuj'd'hui\b", "Auj'd'hui", "\\textit{abbr. pro} Aujourd'hui"),
    (r"\bAujd'hui\b", "Aujd'hui", "\\textit{abbr. pro} Aujourd'hui"),
    (r"\bplusrs\b", "plusrs", "\\textit{abbr. pro} plusieurs"),
    (r"\bplusis\b", "plusis", "\\textit{abbr. pro} plusieurs"),
    (r"\bplusies\b", "plusies", "\\textit{abbr. pro} plusieurs"),
    (r"\bpl\.\s+fois\b", "pl.", "\\textit{abbr. pro} plusieurs"),
    # Adjectives & nouns
    (r"\bgd\b", "gd", "\\textit{abbr. pro} grand"),
    (r"\bGd\b", "Gd", "\\textit{abbr. pro} Grand(e)"),
    (r"\bgde\b", "gde", "\\textit{abbr. pro} grande"),
    (r"\bGde\b", "Gde", "\\textit{abbr. pro} Grande"),
    (r"\bgds\b", "gds", "\\textit{abbr. pro} grands"),
    (r"\bGds\b", "Gds", "\\textit{abbr. pro} Guards"),
    (r"\bgdes\b", "gdes", "\\textit{abbr. pro} grandes"),
    (r"\bgr\.\s+froid\b", "gr.", "\\textit{abbr. pro} grand"),
    (r"\bOn\s+pt\b", "pt", "\\textit{abbr. pro} peut"),
    (r"\bpt\b", "pt", "\\textit{abbr. pro} petit"),
    (r"\bPt\b", "Pt", "\\textit{abbr. pro} Petit"),
    (r"\bpte\b", "pte", "\\textit{abbr. pro} petite"),
    (r"\bptit\b", "ptit", "\\textit{abbr. pro} petit"),
    (r"\bPtit\b", "Ptit", "\\textit{abbr. pro} Petit"),
    (r"\bptts\b", "ptts", "\\textit{abbr. pro} petits"),
    (r"\bhte\b", "hte", "\\textit{abbr. pro} haute"),
    (r"\bht\b", "ht", "\\textit{abbr. pro} haut"),
    (r"\bappartt\b", "appartt", "\\textit{abbr. pro} appartement"),
    (r"\bcompartt\b", "compartt", "\\textit{abbr. pro} compartiment"),
    (r"\bcantonnemt\b", "cantonnemt", "\\textit{abbr. pro} cantonnement"),
    (r"\bcommt\b", "commt", "\\textit{abbr. pro} commencement"),
    (r"\bcommencemt\b", "commencemt", "\\textit{abbr. pro} commencement"),
    (r"\bbombardemt\b", "bombardemt", "\\textit{abbr. pro} bombardement"),
    (r"\bbombardt\b", "bombardt", "\\textit{abbr. pro} bombardement"),
    (r"\bchangemt\b", "changemt", "\\textit{abbr. pro} changement"),
    (r"\bmouvt\b", "mouvt", "\\textit{abbr. pro} mouvement"),
    (r"\bmouvts\b", "mouvts", "\\textit{abbr. pro} mouvements"),
    (r"\bsentimt\b", "sentimt", "\\textit{abbr. pro} sentiment"),
    (r"\babrutisst\b", "abrutisst", "\\textit{abbr. pro} abrutissement"),
    (r"\benchevetrt\b", "enchevetrt", "\\textit{abbr. pro} enchevêtrement"),
    (r"\brenseigts\b", "renseigts", "\\textit{abbr. pro} renseignements"),
    (r"\bEnregt\b", "Enregt", "\\textit{abbr. pro} Enregistrement"),
    (r"\bcorrespce\b", "correspce", "\\textit{abbr. pro} correspondance"),
    (r"\bCorresp\b", "Corresp", "\\textit{abbr. pro} Correspondance"),
    (r"\bsiton\b", "siton", "\\textit{abbr. pro} situation"),
    (r"\bconverson\b", "converson", "\\textit{abbr. pro} conversation"),
    (r"\bautorison\b", "autorison", "\\textit{abbr. pro} autorisation"),
    (r"\bstaton\b", "staton", "\\textit{abbr. pro} station"),
    (r"\bconfirmaton\b", "confirmaton", "\\textit{abbr. pro} confirmation"),
    (r"\btempérre\b", "tempérre", "\\textit{abbr. pro} température"),
    (r"\btempér\.", "tempér.", "\\textit{abbr. pro} température"),
    (r"\bchalr\b", "chalr", "\\textit{abbr. pro} chaleur"),
    (r"\bintellge\b", "intellge", "\\textit{abbr. pro} intelligence"),
    (r"\bimptes\b", "imptes", "\\textit{abbr. pro} importantes"),
    (r"\bimpts\b", "impts", "\\textit{abbr. pro} importants"),
    (r"\bimpte\b", "impte", "\\textit{abbr. pro} importante"),
    (r"\bimpt\b", "impt", "\\textit{abbr. pro} important"),
    (r"\bexcte\b", "excte", "\\textit{abbr. pro} excellente"),
    (r"\bexcellt\b", "excellt", "\\textit{abbr. pro} excellent"),
    (r"\bordinre\b", "ordinre", "\\textit{abbr. pro} ordinaire"),
    (r"\bdouzne\b", "douzne", "\\textit{abbr. pro} douzaine"),
    (r"\bJournx\b", "Journx", "\\textit{abbr. pro} Journaux"),
    (r"\bbrches\b", "brches", "\\textit{abbr. pro} branches"),
    (r"\bBne\b", "Bne", "\\textit{abbr. pro} Bonne"),
    (r"\bsymphe\b", "symphe", "\\textit{abbr. pro} sympathique"),
    (r"\bassz\b", "assz", "\\textit{abbr. pro} assez"),
    (r"\bas\.\s", "as.", "\\textit{abbr. pro} assez"),
    (r"\babomles\b", "abomles", "\\textit{abbr. pro} abominables"),
    (r"\badmles\b", "admles", "\\textit{abbr. pro} admirables"),
    # Adverbs in -t / -mt
    (r"\bextrt\b", "extrt", "\\textit{abbr. pro} extrêmement"),
    (r"\bextt\b", "extt", "\\textit{abbr. pro} extrêmement"),
    (r"\bmervt\b", "mervt", "\\textit{abbr. pro} merveilleusement"),
    (r"\bmerveillet\b", "merveillet", "\\textit{abbr. pro} merveilleusement"),
    (r"\bmervx\b", "mervx", "\\textit{abbr. pro} merveilleux"),
    (r"\bmerve\b", "merve", "\\textit{abbr. pro} merveilleuse"),
    (r"\bexcessvt\b", "excessvt", "\\textit{abbr. pro} excessivement"),
    (r"\babsolt\b", "absolt", "\\textit{abbr. pro} absolument"),
    (r"\babst\b", "abst", "\\textit{abbr. pro} absolument"),
    (r"\bdéfintt\b", "défintt", "\\textit{abbr. pro} définitivement"),
    (r"\baffrt\b", "affrt", "\\textit{abbr. pro} affreusement"),
    (r"\binfinimt\b", "infinimt", "\\textit{abbr. pro} infiniment"),
    (r"\bprofondemt\b", "profondemt", "\\textit{abbr. pro} profondément"),
    (r"\bprofondt\b", "profondt", "\\textit{abbr. pro} profondément"),
    (r"\blentemt\b", "lentemt", "\\textit{abbr. pro} lentement"),
    (r"\bnotamt\b", "notamt", "\\textit{abbr. pro} notamment"),
    (r"\bcontrt\b", "contrt", "\\textit{abbr. pro} contrairement"),
    (r"\bparallelt\b", "parallelt", "\\textit{abbr. pro} parallèlement"),
    (r"\bparallèlt\b", "parallèlt", "\\textit{abbr. pro} parallèlement"),
    (r"\bcomplètt\b", "complètt", "\\textit{abbr. pro} complètement"),
    (r"\bcomplt\b", "complt", "\\textit{abbr. pro} complètement"),
    (r"\bentiert\b", "entiert", "\\textit{abbr. pro} entièrement"),
    (r"\binutilt\b", "inutilt", "\\textit{abbr. pro} inutilement"),
    (r"\bprincipt\b", "principt", "\\textit{abbr. pro} principalement"),
    (r"\bfortt\b", "fortt", "\\textit{abbr. pro} fortement"),
    (r"\babondt\b", "abondt", "\\textit{abbr. pro} abondamment"),
    (r"\brapidt\b", "rapidt", "\\textit{abbr. pro} rapidement"),
    (r"\bdélicieust\b", "délicieust", "\\textit{abbr. pro} délicieusement"),
    (r"\bexactt\b", "exactt", "\\textit{abbr. pro} exactement"),
    (r"\bspécialt\b", "spécialt", "\\textit{abbr. pro} spécialement"),
    (r"\bimmédiatt\b", "immédiatt", "\\textit{abbr. pro} immédiatement"),
    (r"\blégèrt\b", "légèrt", "\\textit{abbr. pro} légèrement"),
    # Common abbreviated words, titles, places, people
    (r"\bdéj\.?\b", "déj", "\\textit{abbr. pro} déjeuné / déjeuner"),
    (r"\bdéjeun\.?\b", "déjeun.", "\\textit{abbr. pro} déjeuné / déjeuner"),
    (r"\bpromen\.", "promen.", "\\textit{abbr. pro} promener / promenade"),
    (r"\bét\.", "ét.", "\\textit{abbr. pro} étage"),
    (r"\brez-de-ch\.", "rez-de-ch.", "\\textit{abbr. pro} rez-de-chaussée"),
    (r"(?<![-A-Za-z])\bch\.", "ch.", "\\textit{abbr. pro} chez"),
    (r"\bCh\.\s+ds\s+ma\s+chambre\b", "Ch.", "\\textit{abbr. pro} Chaleur"),
    (r"\bCh\.\s+Pfister\b", "Ch.", "\\textit{abbr. pro} Chez"),
    (r"\bBvd\b", "Bvd", "\\textit{abbr. pro} Boulevard"),
    (r"\bBd\b", "Bd", "\\textit{abbr. pro} Boulevard"),
    (r"\bChau\b", "Chau", "\\textit{abbr. pro} Château"),
    (r"\bEgl\.?\b", "Egl.", "\\textit{abbr. pro} Église"),
    (r"\bégl\.", "égl.", "\\textit{abbr. pro} église"),
    (r"\bpropr\.", "propr.", "\\textit{abbr. pro} propriétaire"),
    (r"\bproprre\b", "proprre", "\\textit{abbr. pro} propriétaire"),
    (r"\bpropie\b", "propie", "\\textit{abbr. pro} propriétaire"),
    (r"\bProprié\b", "Proprié", "\\textit{abbr. pro} Propriétaire"),
    (r"\bhabts\b", "habts", "\\textit{abbr. pro} habitants"),
    (r"\bsous-préf\b", "sous-préf", "\\textit{abbr. pro} sous-préfecture"),
    (r"\bdept\b", "dept", "\\textit{abbr. pro} département"),
    (r"\bkils\b", "kils", "\\textit{abbr. pro} kilomètres"),
    (r"\bKils\b", "Kils", "\\textit{abbr. pro} Kilomètres"),
    (r"\bkil\.", "kil.", "\\textit{abbr. pro} kilomètres"),
    (r"\b\d+\s*k\.\s+de\b", "k.", "\\textit{abbr. pro} kilomètres"),
    (r"\bHippte\b", "Hippte", "\\textit{scil.} Hippolyte"),
    (r"\bMargte\b", "Margte", "\\textit{scil.} Marguerite (Calmels)"),
    (r"\bMte\b", "Mte", "\\textit{scil.} Marguerite (Calmels)"),
    (r"\bMarg\.", "Marg.", "\\textit{scil.} Marguerite (Calmels)"),
    (r"\bJosephe\b", "Josephe", "\\textit{scil.} Joséphine (Combes)"),
    (r"\bMme\b", "Mme", "\\textit{abbr. pro} Madame"),
    (r"\bMmes\b", "Mmes", "\\textit{abbr. pro} Mesdames"),
    (r"\bMlle\b", "Mlle", "\\textit{abbr. pro} Mademoiselle"),
    (r"\bMlles\b", "Mlles", "\\textit{abbr. pro} Mesdemoiselles"),
    (r"\bMre\b", "Mre", "\\textit{abbr. pro} Mère"),
    (r"\bSt[-\s]", "St", "\\textit{abbr. pro} Saint"),
    (r"\bSte[-\s]", "Ste", "\\textit{abbr. pro} Sainte"),
    (r"\bfrse\b", "frse", "\\textit{abbr. pro} française"),
    (r"\bfse\b", "fse", "\\textit{abbr. pro} française"),
    (r"\bFse\b", "Fse", "\\textit{abbr. pro} Française"),
    (r"\bFr\.se\b", "Fr.se", "\\textit{abbr. pro} Française"),
    (r"\bmilitre\b", "militre", "\\textit{abbr. pro} militaire"),
    (r"\bmilre\b", "milre", "\\textit{abbr. pro} militaire"),
    (r"\bmilit\.", "milit.", "\\textit{abbr. pro} militaire"),
    (r"\binfrie\b", "infrie", "\\textit{abbr. pro} infanterie"),
    (r"\bD\.on\b", "D.on", "\\textit{abbr. pro} Division"),
    (r"\bdivon\b", "divon", "\\textit{abbr. pro} division"),
    (r"\bDivon\b", "Divon", "\\textit{abbr. pro} Division"),
    (r"\bdiv\b", "div", "\\textit{abbr. pro} division"),
    (r"\bgal\b", "gal", "\\textit{abbr. pro} général"),
    (r"\bQt\s*Mr\b", "Qt Mr", "\\textit{angl.} Quartermaster"),
    (r"(?<![A-Za-z-])\bs-off\.", "s-off.", "\\textit{abbr. pro} sous-officier"),
    (r"(?<![A-Za-z-])\boff\.", "off.", "\\textit{abbr. pro} officier(s)"),
    (r"(?<![A-Za-z-])\boffs\b", "offs", "\\textit{abbr. pro} officiers"),
    (r"(?<![A-Za-z-])\boff\b(?!\.)", "off", "\\textit{abbr. pro} officier(s)"),
    (r"\bLieutt\b", "Lieutt", "\\textit{abbr. pro} Lieutenant"),
    (r"\bLt\b", "Lt", "\\textit{abbr. pro} Lieutenant"),
    (r"\bCap\.\s*W\.", "Cap. W.", "\\textit{scil.} Capitaine Williams"),
    (r"\bCapt\.\s*W\.", "Capt. W.", "\\textit{scil.} Captain Williams"),
    (r"\bCap\.", "Cap.", "\\textit{abbr. pro} Capitaine"),
    (r"\bCapt\.", "Capt.", "\\textit{angl.} Captain"),
    (r"\bCol\.", "Col.", "\\textit{abbr. pro} Colonel"),
    (r"\bCoy\b(?!\.)", "Coy", "\\textit{angl.} Company"),
    (r"\bCie\b", "Cie", "\\textit{abbr. pro} Compagnie"),
    (r"\bcie\b", "cie", "\\textit{abbr. pro} compagnie"),
    (r"\bM\.T\.", "M.T.", "\\textit{angl.} Motor Transport"),
    (r"\bM\.O\.", "M.O.", "\\textit{angl.} Medical Officer"),
    (r"(?<![A-Za-z.])H\.Q\.", "H.Q.", "\\textit{angl.} Headquarters"),
    (r"\bG\.H\.Q\.", "G.H.Q.", "\\textit{angl.} General Headquarters"),
    (r"\bN\.C\.O's\b", "N.C.O's", "\\textit{angl.} Non-Commissioned Officers"),
    (r"\bN\.C\.O\.", "N.C.O.", "\\textit{angl.} Non-Commissioned Officer"),
    (r"\bA\.S\.C\.", "A.S.C.", "\\textit{angl.} Army Service Corps"),
    (r"\bR\.F\.A\.", "R.F.A.", "\\textit{angl.} Royal Field Artillery"),
    (r"\bR\.F\.(?![A-Za-z.])", "R.F.", "\\textit{angl.} Royal Fusiliers"),
    (r"\bR\.T\.O\.", "R.T.O.", "\\textit{angl.} Railway Transport Officer"),
    (r"\bA\.P\.M\.", "A.P.M.", "\\textit{angl.} Assistant Provost Marshal"),
    (r"\bQ\.M\.S\.", "Q.M.S.", "\\textit{angl.} Quartermaster Sergeant"),
    (r"\bD\.O\.S\.T\.", "D.O.S.T.", "\\textit{sigle militaire, développement non établi}"),
    (r"\bE\.F\.C\.", "E.F.C.", "\\textit{angl.} Expeditionary Force Canteens"),
    (r"\bY\.M\.C\.A\.", "Y.M.C.A.", "\\textit{angl.} Young Men's Christian Assoc."),
    (r"\bP\.L\.M\.", "P.L.M.", "\\textit{scil.} Paris-Lyon-Méditerranée"),
    (r"\bc\.\s*ples\b", "c. ples", "\\textit{abbr. pro} cartes postales"),
    (r"\bC\.\s*ples\b", "C. ples", "\\textit{abbr. pro} Cartes postales"),
    (r"\bC\.\s*P\.", "C. P.", "\\textit{abbr. pro} Cartes postales"),
    (r"\bctes\s+ples\b", "ctes ples", "\\textit{abbr. pro} cartes postales"),
    (r"\bCtes\s+ples\b", "Ctes ples", "\\textit{abbr. pro} Cartes postales"),
    (r"\bCartes\s+ples\b", "Cartes ples", "\\textit{abbr. pro} Cartes postales"),
    (r"\bcartes\s+ples\b", "cartes ples", "\\textit{abbr. pro} cartes postales"),
    (r"\b[cC]tes\s+ph\.?", "ctes ph.", "\\textit{abbr. pro} cartes photographiques"),
    (r"\b[cC]artes\s+ph\.?", "cartes ph.", "\\textit{abbr. pro} cartes photographiques"),
    (r"\bCtis\b", "Ctis", "\\textit{abbr. pro} Curtis"),
    (r"\bCzt\b", "Czt", "\\textit{abbr. pro} Crouzet"),
    (r"\bR\.\s*Fusrs\b", "R. Fusrs", "\\textit{angl.} Royal Fusiliers"),
    (r"\bpassim\b", "passim", "\\textit{lat.} çà et là"),
    (r"\bpropre\b", "propre", "\\textit{abbr. pro} propriétaire"),
    (r"\bproprire\b", "proprire", "\\textit{abbr. pro} propriétaire"),
    (r"\bcommre\b", "commre", "\\textit{abbr. pro} commissionnaire"),
    (r"\bdépartt\b", "départt", "\\textit{abbr. pro} département"),
    (r"\bcompartimt\b", "compartimt", "\\textit{abbr. pro} compartiment"),
    (r"\bdérangt\b", "dérangt", "\\textit{abbr. pro} dérangement"),
    (r"\bépanchts\b", "épanchts", "\\textit{abbr. pro} épanchements"),
    (r"\barrangt\b", "arrangt", "\\textit{abbr. pro} arrangement"),
    (r"\benchevêtrt\b", "enchevêtrt", "\\textit{abbr. pro} enchevêtrement"),
    (r"\bdéfinitt\b", "définitt", "\\textit{abbr. pro} définitivement"),
    (r"\badmirabt\b", "admirabt", "\\textit{abbr. pro} admirablement"),
    (r"\bplaintivt\b", "plaintivt", "\\textit{abbr. pro} plaintivement"),
    (r"\bdélict\b", "délict", "\\textit{abbr. pro} délicieusement"),
    (r"\binsttr\b", "insttr", "\\textit{abbr. pro} instituteur"),
    (r"\bintte\b", "intte", "\\textit{abbr. pro} interprète"),
    (r"\bMaral\b", "Maral", "\\textit{abbr. pro} Maréchal"),
    (r"\bmaral\b", "maral", "\\textit{abbr. pro} maréchal"),
    (r"\bcathle\b", "cathle", "\\textit{abbr. pro} cathédrale"),
    (r"\bartiflles\b", "artiflles", "\\textit{abbr. pro} artificielles"),
    (r"\bhorizle\b", "horizle", "\\textit{abbr. pro} horizontale"),
    (r"\bchvx\b", "chvx", "\\textit{abbr. pro} cheveux"),
    (r"\bchps\b", "chps", "\\textit{abbr. pro} champs"),
    (r"\bmnts\b", "mnts", "\\textit{abbr. pro} moments / minutes"),
    (r"\bTre\s+d'iode\b", "Tre", "\\textit{abbr. pro} Teinture"),
    (r"\bNormle\s+Supre\b", "Normle Supre", "\\textit{abbr. pro} Normale Supérieure"),
    (r"\bAchiet-le-Pt\.", "Achiet-le-Pt.", "\\textit{scil.} Achiet-le-Petit"),
    (r"(?<=\bTjours\s)=", "=", "\\textit{signum aequalitatis pro} même"),
    (r"\b\d+\s*ct\.?\b", "ct", "\\textit{abbr. pro} courant"),
    (r"\b1/2\b", "1/2", "\\textit{scil.} demi / moitié"),
    (r"\b1er\b", "1er", "\\textit{scil.} premier"),
    (r"\b1ère\b", "1ère", "\\textit{scil.} première"),
    (r"\b\d+\s*f\.\s*\d*", "f.", "\\textit{abbr. pro} franc(s)"),
    (r"\b\d+\s*fr\.", "fr.", "\\textit{abbr. pro} franc(s)"),
    (r"\b\d+\s*c\.(?!\s*temps\b)", "c.", "\\textit{abbr. pro} centimes"),
    (r"\b\d+\s*[hH]\s*(?:\d+\s*|1/2\s*)?m\.?\b", "m.", "\\textit{abbr. pro} matin"),
    (r"\b\d+\s*[hH]\s*(?:\d+\s*|1/2\s*)?s\.?\b", "s.", "\\textit{abbr. pro} soir"),
    (r"\(\s*bois\s+chateau\b", "(bois", "\\textit{parenthesis non clausa in ms.}"),
    (r"\bOct\.\s*/\s*16\b", "Oct. /16", "\\textit{abbr. pro} Octobre 1916"),
    (r"\bobservon\b", "observon", "\\textit{abbr. pro} observation"),
    (r"(?<=\bde\s)=", "de =", "\\textit{signum aequalitatis pro} de même"),
    (r"\bpeu à peu chassé\b", "chassé", "\\textit{scil.} ont chassé (ellipse de l'auxiliaire)"),
]

ANGLICISM_WORDS = [
    "breakfast", "Breakfast", "lunch", "Lunch", "Lunché", "tea", "tea-dinner", "dinner", "After dinner",
    "sunset", "Washing", "washing", "darning", "cooking", "Food", "food", "Drink", "cottage", "garret",
    "billeting", "billets", "mess", "messroom", "messer", "shift", "shifte", "shifting",
    "shifterons", "shifté", "lorry", "lorries", "limber", "waggon", "waggons", "saddle soap",
    "refilling point", "horse-lines", "Horse-lines", "barbed wire", "tooth ache", "hair cut", "Hair cut",
    "wounded", "kit", "walk", "Purchase Board", "interview", "tommy", "tommies", "Tooth Powder",
    "tooth powder", "Blacksmith", "workshops", "Early lunch", "moving", "afternoon", "long talk",
    "home", "stuck", "anti-aircraft battery", "dug-outs", "lift", "water-cart", "Christmas dinner",
    "Christmas", "turkey", "plum-pudding", "Boxing Day", "Brickfield area", "Town Major",
    "Foraging Officer", "warrant", "English novel", "Death or Glory Boys", "nice", "green", "forage",
    "railhead", "groom", "headcook", "batman", "poney", "canteen", "Canteen", "boots", "nails",
    "sunshine", "very", "Sweets", "cakes", "Gift", "Tip", "room", "tins", "Dubbin",
]

INLINE_SUFFIX_FIXES = [
    ("1[9]16", "1916", None, None),
    ("C[ie]", "Cie", "Cie", "Compagnie"),
    ("off.[iciers]", "off.", "off.", "officiers"),
    ("off.[icier]", "off.", "off.", "officier"),
    ("milit.[aire]", "milit.", "milit.", "militaire"),
    ("égl.[ise]", "égl.", "égl.", "église"),
    ("délic.[ieuse]", "délic.", "délic.", "délicieuse"),
    ("l.[aquelle]", "l.", "l.", "laquelle"),
    ("b.[elle]", "b.", "b.", "belle"),
    ("fr[ançaise]", "fr.", "fr.", "française"),
    ("promen[er]", "promen.", "promen.", "promener"),
    ("tempér[ature]", "tempér.", "tempér.", "température"),
    ("élastiq[ues]", "élastiq.", "élastiq.", "élastiques"),
    ("Aucun[e]", "Aucun", "Aucun", "Aucune"),
    ("définitif[ve]", "définitif", "définitif", "définitive"),
]

EDITORIAL_PLACEHOLDERS = [
    "[Espace blanc important]",
    "[Espace blanc]",
    "[Espace vide]",
    "[Large espace vide, papier texturé]",
    "[Le reste de la page est laissé vide]",
    "[Suite immédiate du folio précédent]",
]

DAYS_SET = {"Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"}


def _norm_lemma_key(lem):
    return re.sub(r"[\s.]", "", lem).lower()


def clean_line_and_extract_note(raw_line, line_no):
    """
    Cleans markdown/editorial artifacts from a transcription line so the main text
    is pure diplomatic text, and returns (cleaned_line, marginal_note_str).
    Preserves all manuscript accounting brackets `[ ... ]` intact.
    """
    notes = []
    seen_lemmas = set()
    line = strip_html_keep_del(raw_line).strip()

    if line == "[Bas de page très pâle : ... Consommations : 50c]":
        line = "... Consommations : 50 c."
        notes.append(f"\\textbf{{{line_no}}} \\textit{{lect. pallida in imo folio.}}")

    if "[Suite immédiate du folio précédent]" in line:
        line = line.replace("[Suite immédiate du folio précédent]", "").strip()

    # Convert ~~...~~ to ⟦...⟧ and standalone ~ to —
    line = re.sub(r"~~([^~]+)~~", lambda m: f"⟦{m.group(1).strip()}⟧", line)
    line = line.replace("~", "—")

    # Record every `⟦...⟧` deletion once in marginal apparatus
    for m in re.finditer(r"⟦([^⟧]+)⟧", line):
        deleted_txt = m.group(1).strip()
        notes.append(f"\\textbf{{{line_no}}} \\llbracket {deleted_txt}\\rrbracket\\ \\textit{{del. in ms.}}")

    # Strip footnote numbers like [1], [2]
    line = re.sub(r"\s*\[\d+\]", "", line)

    # Restore line-initial `[plus]` (representing manuscript `+`)
    if line.startswith("[plus] "):
        line = "+ " + line[len("[plus] "):]
        notes.append(f"\\textbf{{{line_no} +}} \\textit{{scil.}} plus.")
        seen_lemmas.add("+")

    # Handle Scan #011 L12 conjectural glosses after `gds et ptts`
    if "[tous ?] [lui répondent ?]" in line:
        line = line.replace("[tous ?] [lui répondent ?]", "").strip()

    # Normalize spaces before `,.;!?` and after elision apostrophes before extracting inline expansions
    line = re.sub(r"\s+([,.;!?])", r"\1", line)
    line = re.sub(
        r"\b([dlmnstjcDLMNSTJC]|[qQ]u|[jJ]usqu|[aA]uj)[’']\s+(?=[A-Za-zÀ-ÖØ-öø-ÿ])",
        r"\1'",
        line,
    )
    line = re.sub(r"\(\s+", "(", line)
    line = re.sub(r"\s+\)", ")", line)

    # Apply inline suffix fixes (e.g. off.[iciers], C[ie])
    for pat, repl, lemma, exp in INLINE_SUFFIX_FIXES:
        if pat in line:
            line = line.replace(pat, repl)
            if lemma and exp:
                notes.append(f"\\textbf{{{line_no} {lemma}}} \\textit{{scil.}} {exp}.")
                seen_lemmas.add(_norm_lemma_key(lemma))

    # Check for uncertain reading [?] or [...]
    for m in re.finditer(r"([A-Za-zÀ-ÖØ-öø-ÿ0-9'/.-]+)\s*\[\?\]", line):
        w = m.group(1).strip(".,;:()")
        if w:
            notes.append(f"\\textbf{{{line_no} {w}}} \\textit{{lect. incert. in ms.}}")
            seen_lemmas.add(_norm_lemma_key(w))
    if "[?]" in line:
        if not any("lect. incert." in n for n in notes):
            notes.append(f"\\textbf{{{line_no}}} \\textit{{lect. incert. in ms.}}")
    # A doubtful reading must remain visibly doubtful in the transcription.
    # Protect it from the generic removal of inline abbreviation expansions below.
    uncertain_readings = []
    def protect_uncertainty(match):
        uncertain_readings.append(match.group(0))
        return f"@@UNCERTAIN{len(uncertain_readings) - 1}@@"
    line = re.sub(
        r"\[[^\[\]]*(?:\?|illis|incertain|blanc|signe|ajout|addition|non déchiffr|non établi|bord droit|bas de photographie|biffé|surchargé|groupe abrégé)[^\[\]]*\]",
        protect_uncertainty, line, flags=re.I,
    )
    if any("blanc" in reading.lower() for reading in uncertain_readings):
        notes.append(f"\\textbf{{{line_no}}} \\textit{{spatium relictum in ms.}}")
    if any("blanc" not in reading.lower() for reading in uncertain_readings) and not any("lect. incert." in n for n in notes):
        notes.append(f"\\textbf{{{line_no}}} \\textit{{lect. incert. in ms.}}")
    if "[...]" in line:
        line = line.replace("[...]", "\\dots")
        notes.append(f"\\textbf{{{line_no}}} \\textit{{lacuna vel lect. incert.}}")

    # Detect manuscript accounting brackets `[ ... ]` (either starting with `[ ` or containing `:` or `=`)
    has_accounting_bracket = ("[ " in line) or bool(re.search(r"\[[^\]]*[:=][^\]]*\]", line))
    if has_accounting_bracket:
        notes.append(f"\\textbf{{{line_no}}} \\textit{{in marg. cum unco}} (comptes).")

    # Extract inline editorial expansions `[expansion]` ONLY when the bracket is NOT an accounting bracket
    # (editorial expansions never start with a space after `[` and never contain `:` or `=`)
    for m in re.finditer(r"(\S+)\s+\[([^\]\s:=\"][^\]:=\"]*)\]", line):
        word_before = m.group(1).rstrip(":,;")
        expansion = m.group(2).strip()
        if not word_before or expansion.isdigit():
            continue
        if expansion in DAYS_SET:
            prefix = line[:m.start()] + word_before
            dm = re.search(
                r"\b(Lundi|Mardi|Mercredi|Jeudi|Vendredi|Samedi|Dimanche|Mar\.?|Ma\.?|Merc\.?|Mer\.?|Me\.?|Jeu\.?|J\.?|Vendr\.?|Ven\.?|Ve\.?|V\.?|Sam\.?|S\.?|Dim\.?|D\.?|Lun\.?|L\.?)(?=\s|$|\.)",
                prefix,
            )
            if dm:
                word_before = dm.group(0)
        elif word_before == "les" and expansion == "dans les":
            word_before = "ds"
            expansion = "dans"
        elif word_before == "ph" and "photos" in expansion.lower():
            word_before = "ctes ph."
        elif word_before == "à" and expansion.lower() == "jusqu'à":
            prefix = line[:m.start()] + word_before
            jm = re.search(r"\b([jJ]\.?\s*à)$", prefix)
            if jm:
                word_before = jm.group(1)
        elif word_before == "fait" and expansion.lower() == "tout à fait":
            word_before = "tt"
            expansion = "tout"
        elif word_before == "Mag" and expansion == "Bon Marché":
            word_before = "B. Mag"
        norm_wb = _norm_lemma_key(word_before)
        if norm_wb in seen_lemmas:
            continue
        if expansion.lower() == "sic":
            notes.append(f"\\textbf{{{line_no} {word_before}}} \\textit{{sic in ms.}}")
            seen_lemmas.add(norm_wb)
        elif word_before.rstrip(".") != expansion.rstrip("."):
            notes.append(f"\\textbf{{{line_no} {word_before}}} \\textit{{scil.}} {expansion}.")
            seen_lemmas.add(norm_wb)

    # Strip only non-accounting editorial brackets `[expansion]`
    line = re.sub(r"\s*\[([^\]\s:=\"][^\]:=\"]*)\]", "", line)

    # Check abbreviations in ABBREV_MAP (if not already noted for that lemma)
    if len(notes) < 2:
        for pat, lemma, expl in ABBREV_MAP:
            if re.search(pat, line):
                norm_lem = _norm_lemma_key(lemma)
                if norm_lem not in seen_lemmas:
                    notes.append(f"\\textbf{{{line_no} {lemma}}} {expl}.")
                    seen_lemmas.add(norm_lem)
                    if len(notes) >= 2:
                        break

    # The graph rendered y may be a conjunction, a pronoun or another sign.
    # A regular expression cannot establish its manuscript value; keep the graph
    # and reserve expansions for the scan-specific, documented apparatus.

    # Check anglicisms
    if len(notes) < 2:
        for ang in ANGLICISM_WORDS:
            if re.search(r"\b" + re.escape(ang) + r"\b", line):
                norm_ang = _norm_lemma_key(ang)
                if norm_ang not in seen_lemmas:
                    notes.append(f"\\textbf{{{line_no} {ang}}} \\textit{{angl. in ms.}}")
                    seen_lemmas.add(norm_ang)
                    break

    # Normalize tabs/multiple spaces (used for right-aligned month/year headers)
    if "\t" in line or "          " in line:
        parts = re.split(r"\t+|\s{6,}", line, maxsplit=1)
        if len(parts) == 2:
            line = f"{parts[0].strip()} \\hfill {parts[1].strip()}"

    # Collapse redundant spaces around `,.;!?` introduced by HTML span removal
    line = re.sub(r"\s+([,.;!?])", r"\1", line)
    line = re.sub(r"\s{2,}", " ", line).strip()
    for uncertainty_idx, reading in enumerate(uncertain_readings):
        line = line.replace(f"@@UNCERTAIN{uncertainty_idx}@@", reading)

    dedup_notes = list(dict.fromkeys(notes))
    return line, " ".join(dedup_notes)


def build_all_186_records(apply_revision=True, apply_apparatus=True):
    files = get_sorted_scan_filenames()
    docs = parse_docx_blocks() if any("lines" not in SCANS_001_074_META[n] for n in range(1, 75)) else []

    records = []

    for scan_idx in range(1, 187):
        fname = files[scan_idx - 1]
        if scan_idx == 1:
            folio_label = "Couverture extérieure"
        else:
            fnum = (scan_idx) // 2
            rv = "recto" if (scan_idx % 2 == 0) else "verso"
            folio_label = f"Folio {fnum} {rv}"

        if scan_idx <= 74:
            meta = SCANS_001_074_META[scan_idx]
            if "lines" in meta:
                raw_lines = meta["lines"]
            elif scan_idx <= 49:
                raw_lines = docs[scan_idx - 1]["lines"]
            elif scan_idx == 50:
                raw_lines = SCAN_050_DATA["lines"]
            elif 51 <= scan_idx <= 62:
                raw_lines = docs[scan_idx - 2]["lines"]
            elif scan_idx == 63:
                raw_lines = docs[62]["lines"]
            elif scan_idx == 64:
                raw_lines = docs[61]["lines"]
            else:
                raw_lines = docs[scan_idx - 2]["lines"]
            title = f"{folio_label.upper()} ({meta['title']})" if scan_idx > 1 else meta["title"]
            date_str = meta["date"]
            lieu_str = meta["lieu"]
            crit_str = meta["critique"]
            hist_str = meta["historique"]
        elif 75 <= scan_idx <= 130:
            entry = SCANS_075_130[scan_idx]
            raw_lines = entry["lines"]
            title = f"{folio_label.upper()} ({entry['title']})"
            date_str = entry["date"]
            lieu_str = entry["lieu"]
            crit_str = entry["critique"]
            hist_str = entry["historique"]
        else:
            entry = SCANS_131_186[scan_idx]
            raw_lines = entry["lines"]
            title = f"{folio_label.upper()} ({entry['title']})"
            date_str = entry["date"]
            lieu_str = entry["lieu"]
            crit_str = entry["critique"]
            hist_str = entry["historique"]

        cleaned_lines = []
        marginal_notes = {}
        filtered_raw_lines = [rl for rl in raw_lines if rl.strip() not in EDITORIAL_PLACEHOLDERS]
        for i, rl in enumerate(filtered_raw_lines, 1):
            cl, mnote = clean_line_and_extract_note(rl, i)
            cleaned_lines.append(cl)
            if mnote:
                marginal_notes[i] = mnote

        if scan_idx == 1:
            marginal_notes = {
                1: "\\textbf{1 Livre - Journal} \\textit{titulus in pittacio caeruleo.}",
                3: "\\textbf{3 25 juillet 1916} \\textit{terminus a quo.}",
                4: "\\textbf{4 30 avril 1917} \\textit{terminus ad quem.}",
            }

        records.append({
            "scan_num": scan_idx,
            "filename": fname,
            "folio": folio_label,
            "title": title,
            "date": date_str,
            "lieu": lieu_str,
            "lines": cleaned_lines,
            "marginal_notes": {str(k): v for k, v in sorted(marginal_notes.items())},
            "critique": crit_str,
            "historique": hist_str,
        })

    if apply_revision:
        import copy
        baseline_records = copy.deepcopy(records)
        from revision_philologique import apply_verified_corrections
        records = apply_verified_corrections(records, clean_line_and_extract_note)
        if apply_apparatus:
            from apparat_critique import apply_apparatus as apply_reviewed_apparatus
            records = apply_reviewed_apparatus(records)
            from commentaires_et_loci import enrichir_edition_philologique
            records = enrichir_edition_philologique(records, baseline_records, clean_line_and_extract_note)
    return records


def export_transcriptions(records):
    json_path = os.path.join(ROOT, "transcriptions", "transcription_integrale_186_scans.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    md_path = os.path.join(ROOT, "transcriptions", "transcription_integrale_186_scans.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Édition diplomatique et critique intégrale du *Livre-Journal* d'Hippolyte Combes (25 juillet 1916 – 30 avril 1917)\n\n")
        f.write("Ce document réunit la transcription diplomatique ligne à ligne, l'apparat critique marginal, l'apparat des *loci paralleli* et le commentaire critique et historique de la totalité des folios du carnet (`Couverture` et `Folio 1 recto` à `Folio 93 recto`).\n\n---\n\n")
        for r in records:
            f.write(f"## {r['folio']} — {r.get('mois_annee', '')}\n")
            f.write(f"- **Titre** : {r['title']}\n")
            f.write(f"- **Date** : {r['date']}\n")
            f.write(f"- **Lieu** : {r['lieu']}\n\n")
            f.write("```text\n")
            for idx, l in enumerate(r["lines"], 1):
                clean_md_line = l.replace("\\hfill", "        ")
                f.write(f"{idx:2d} | {clean_md_line}\n")
            f.write("```\n\n")
            for k, v in r["marginal_notes"].items():
                v_clean = re.sub(r"\\textbf\{([^}]*)\}", r"**\1**", v)
                v_clean = re.sub(r"\\textit\{([^}]*)\}", r"*\1*", v_clean)
                v_clean = v_clean.replace("\\llbracket ", "⟦").replace("\\rrbracket\\", "⟧").replace("\\&", "&")
                f.write(f"- *l. {k}* : {v_clean}\n")
            f.write("\n* * *\n\n")
            if r.get("critique"):
                c_clean = re.sub(r"\\textbf\{([^}]*)\}", r"**\1**", r["critique"])
                c_clean = re.sub(r"\\textit\{([^}]*)\}", r"*\1*", c_clean)
                c_clean = re.sub(r"\\texttt\{([^}]*)\}", r"`\1`", c_clean)
                c_clean = re.sub(r"\\textsuperscript\{([^}]*)\}", r"\1", c_clean)
                c_clean = c_clean.replace("\\&", "&").replace("\\#", "#").replace("\\_", "_")
                f.write(f"{c_clean}\n\n")
            if r.get("loci"):
                l_clean = re.sub(r"\\textbf\{([^}]*)\}", r"**\1**", r["loci"])
                l_clean = re.sub(r"\\textit\{([^}]*)\}", r"*\1*", l_clean)
                l_clean = re.sub(r"\\textsuperscript\{([^}]*)\}", r"\1", l_clean)
                l_clean = re.sub(r"\s*\(p\.~\\pageref\{[^}]+\}\)", "", l_clean)
                l_clean = l_clean.replace("~", " ").replace("\\&", "&")
                f.write(f"*{l_clean}*\n\n")
            h_clean = re.sub(r"\\textbf\{([^}]*)\}", r"**\1**", r["historique"])
            h_clean = re.sub(r"\\textit\{([^}]*)\}", r"*\1*", h_clean)
            h_clean = re.sub(r"\\texttt\{([^}]*)\}", r"`\1`", h_clean)
            h_clean = re.sub(r"\\textsuperscript\{([^}]*)\}", r"\1", h_clean)
            h_clean = h_clean.replace("\\&", "&").replace("\\#", "#").replace("\\_", "_")
            f.write(f"> {h_clean}\n\n---\n\n")

    print(f"Exported {len(records)} scans to {json_path} and {md_path}")


if __name__ == "__main__":
    recs = build_all_186_records()
    export_transcriptions(recs)
    max_lines = max(len(r["lines"]) for r in recs)
    min_lines = min(len(r["lines"]) for r in recs)
    print(f"Line counts across 186 scans: min={min_lines}, max={max_lines}")
