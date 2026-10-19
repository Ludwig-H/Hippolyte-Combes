"""Mise en page d'une double page : transcription et apparat (page paire), fac-similé (page impaire)."""
from __future__ import annotations

import re

from balisage import Rangee, analyser, rendre

HAUTEUR = {"texte": 1.0, "filet": 0.5}
LIGNE_DE_BASE = 0.76  # position de la ligne de base dans une rangée de texte (en interlignes)


def echapper(s: str) -> str:
    """Échappe un texte éditorial ordinaire (pas de balisage diplomatique)."""
    if s is None:
        return ""
    return (s.replace("\\", r"\textbackslash{}").replace("&", r"\&").replace("%", r"\%")
             .replace("#", r"\#").replace("_", r"\_").replace("$", r"\$"))


_DIPLO = {"sll": r"\LJsll", "sl": r"\LJsl", "del": r"\LJdel", "addm": r"\LJaddm", "add": r"\LJadd",
          "inc": r"\LJinc", "fr": r"\LJfrac"}


def editorial(s: str) -> str:
    """Texte éditorial en LaTeX simple (en-tête, registres critique et historique).

    Convertit le balisage diplomatique qui y est cité (^{te}, \\sl{…}, \\inc{…}, \\ill…) et échappe
    les & % # laissés nus ; le reste (\\textit{}, « », etc.) passe tel quel."""
    if not s:
        return ""
    s = str(s).strip()
    s = re.sub(r"\\(sll|sl|del|addm|add|inc|fr)\{", lambda m: _DIPLO[m.group(1)] + "{", s)
    s = re.sub(r"\\sur\{([^{}]*)\}\{([^{}]*)\}", r"\2", s)
    s = re.sub(r"\\ill\[(\d+)\]", r"\\LJill{\1}", s)
    s = re.sub(r"\\ill(?![a-zA-Z{])", r"\\LJill{}", s)
    s = re.sub(r"\\lac(?![a-zA-Z])", r"\\LJlac{}", s)
    s = re.sub(r"\\trait(?![a-zA-Z])", "—", s)
    s = re.sub(r"\\hfill(?![a-zA-Z])\s*", " ", s)
    s = re.sub(r"\^\{([^{}]*)\}", r"\\textsuperscript{\1}", s)
    s = re.sub(r"\^([A-Za-z0-9])", r"\\textsuperscript{\1}", s)
    s = re.sub(r"(?<!\\)([&%#])", r"\\\1", s)
    return s


def _hauteur(r: Rangee) -> float:
    if r.type == "blanc":
        return r.blanc
    return HAUTEUR[r.type]


def _signes_latex(rangees: list[Rangee], i: int) -> str:
    r = rangees[i]
    out = []
    for sg in r.signes:
        # hauteur couverte : de la rangée i jusqu'à la n-ième ligne de texte comprise
        h, vus, j = 0.0, 0, i
        while j < len(rangees):
            h += _hauteur(rangees[j])
            if rangees[j].type == "texte":
                vus += 1
                if vus == sg.n:
                    break
            j += 1
        if sg.nom == "accolade":
            out.append(r"\LJaccolade{%.3f}{%s}" % (h, rendre(sg.etiquette)))
        else:
            out.append(r"\LJ%s{%.3f}" % (sg.nom, h))
    return "".join(out)


def colonne_transcription(rangees: list[Rangee]) -> tuple[str, dict[int, float]]:
    """Renvoie le LaTeX des rangées et la position (ligne de base, en interlignes) de chaque ligne."""
    lignes, positions, y = [], {}, 0.0
    for i, r in enumerate(rangees):
        if r.type == "texte":
            positions[r.numero] = y + LIGNE_DE_BASE
            num = str(r.numero) if r.numero % 5 == 0 else ""
            macro = r"\LJtp" if r"\hfill" in r.latex else r"\LJt"
            lignes.append("%s{%s}{%g}{%s}{%s}{%s}" % (
                macro, num, 1.2 * r.retrait, r.alignement, _signes_latex(rangees, i), r.latex))
        elif r.type == "filet":
            lignes.append(r"\LJf{%s}{%g}" % (r.filet_pos, r.filet_frac))
        else:
            lignes.append(r"\LJb{%g}" % r.blanc)
        y += _hauteur(r)
    return "\n".join(lignes), positions


TYPES_IMPRIMES = None  # tous les types d'entrées sont imprimés


def _note(e: dict) -> str:
    lemme = e.get("lemme", "")
    lemme = "" if lemme is None else str(lemme)
    note = e.get("note", "")
    note = "" if note is None else str(note)
    t = e.get("type", "")
    lem = rendre(lemme) if lemme else ""
    if t == "emprunt":
        corps = r"\textit{angl.} " + editorial(note) if note else ""
    elif t == "abreviation":
        corps = r"\textit{%s}" % editorial(note)
    else:
        corps = editorial(note)
    if lem:
        return r"{\LJpolice %s}\,]\enspace %s" % (lem, corps)
    return corps


def colonne_apparat(apparat: list[dict], positions: dict[int, float], notes_auto: dict[int, list]) -> str:
    """Regroupe les entrées par ligne et produit les appels \\LJapp."""
    par_ligne: dict[int, list[str]] = {}
    for n, liste in notes_auto.items():
        for lemme, t, note in liste:
            par_ligne.setdefault(n, []).append(_note({"lemme": lemme, "type": t, "note": note}))
    for e in apparat:
        n = int(e.get("ligne", 0))
        par_ligne.setdefault(n, []).append(_note(e))
    out = []
    for n in sorted(par_ligne):
        if n not in positions:
            raise ValueError(f"note d'apparat sur une ligne inexistante : {n}")
        txt = r" \textbar\ ".join(par_ligne[n])
        out.append(r"\LJapp{%.3f}{\textbf{\LJchiffres %d}\enspace %s}" % (positions[n], n, txt))
    return "\n".join(out)


def double_page(page: dict, meta: dict) -> str:
    """LaTeX de la double page. ``meta`` : feuillet, cliché, mois, image, légende, label."""
    rangees = analyser(page["transcription"])
    trans, positions = colonne_transcription(rangees)
    auto = {r.numero: r.notes_auto for r in rangees if r.type == "texte" and r.notes_auto}
    app = colonne_apparat(page.get("apparat", []), positions, auto)
    blocs = []
    if page.get("critique"):
        blocs.append(r"\LJregcritique{%s}" % editorial(page["critique"]))
    if meta.get("loci"):
        blocs.append(r"\LJregloci{%s}" % meta["loci"])
    if page.get("historique"):
        blocs.append(r"\LJreghistoire{%s}" % editorial(page["historique"]))
    registres = [r"\LJdebutreg"] if blocs else []
    for k, b in enumerate(blocs):
        if k:
            registres.append(r"\LJsepreg{%s}" % ("22mm" if k == 1 else "38mm"))
        registres.append(b)
    entete = r"\LJentete{%s}{%s}{%s}{%s}{%s}" % (
        meta["feuillet"], meta["cliche"], editorial(page.get("date", "")),
        editorial(page.get("lieux", "")), editorial(page.get("titre", "")))
    return "\n".join([
        "%% ---- %s (cliché %s) ----" % (meta["feuillet"], meta["cliche"]),
        r"\LJpagepaire",
        r"\renewcommand{\LJmois}{%s}" % meta["mois"],
        r"\phantomsection\label{%s}\renewcommand{\LJlabelcourant}{%s}" % (meta["label"], meta["label"]),
        r"\LJpagetranscription{%s}{%%" % entete,
        trans + "}{%",
        app + "}{%",
        "\n".join(registres) + "}",
        r"\renewcommand{\LJfolio}{%s}" % meta["legende"],
        r"\phantomsection\label{%s-fac}" % meta["label"],
        (r"\LJfacsimilepaysage{%s}" if meta.get("paysage") else r"\LJfacsimile{%s}") % meta["image"],
    ])
