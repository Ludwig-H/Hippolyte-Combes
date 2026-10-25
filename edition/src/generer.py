#!/usr/bin/env python3
"""Génère la source LaTeX de l'édition du Livre-Journal d'Hippolyte Combes.

Entrées (edition/donnees/) :
  codicologie.yaml   modèle matériel : feuillets, faces, ordre de lecture des 186 clichés
  pages/NNN.yaml     une page par cliché : transcription balisée, apparat, commentaires
  chapitres.yaml     division éditoriale en chapitres
  index.yaml         entités (personnes, lieux) et leurs formes, pour les index et les loci
Textes rédigés (edition/textes/*.tex) : pages liminaires, introduction, introductions de chapitre, annexes.
Sortie : edition/livre_journal.tex (à compiler deux fois avec XeLaTeX).
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

import yaml

ICI = Path(__file__).resolve().parent
EDITION = ICI.parent
RACINE = EDITION.parent
sys.path.insert(0, str(ICI))

import gabarit  # noqa: E402
import loci_index  # noqa: E402

MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
        "septembre", "octobre", "novembre", "décembre"]


def charger(p: Path):
    with open(p, encoding="utf-8") as f:
        return yaml.safe_load(f)


def folio(feuillet: int | None, face: str | None) -> str:
    if feuillet is None:
        return "Couverture"
    return r"f.~%d~%s" % (feuillet, r"r\textsuperscript{o}" if face == "r" else r"v\textsuperscript{o}")


def mois_de(date: str) -> str:
    """« Mardi 25 juillet 1916 » -> « Juillet 1916 » (premier mois cité, année suivante ou précédente)."""
    d = (date or "").lower()
    for i, m in enumerate(MOIS):
        k = d.find(m)
        if k >= 0:
            an = re.search(r"(19\d\d)", d[k:]) or re.search(r"(19\d\d)", d)
            return m.capitalize() + (" " + an.group(1) if an else "")
    return ""


def texte(nom: str) -> str:
    """Contenu d'un texte rédigé (edition/textes/), avec résolution des \\input{textes/...}."""
    p = EDITION / "textes" / nom
    if not p.exists():
        return "%% texte manquant : %s\n" % nom
    s = p.read_text(encoding="utf-8")
    return re.sub(r"\\input\{textes/([^}]+)\}", lambda m: texte(m.group(1)), s)


def image_fac(cliche: int, dossier: str) -> str:
    return f"{dossier}/{cliche:03d}.jpg"


def table_concordance(codico: list[dict], pages: dict) -> str:
    """Table des feuillets : ordre de lecture, feuillet et face, date, page."""
    lignes = []
    for c in sorted(codico, key=lambda c: (c["ordre"] is None, c["ordre"] if c["ordre"] is not None else c["cliche"])):
        n = c["cliche"]
        if c["statut"] == "doublon":
            continue
        p = pages.get(n, {})
        rem = []
        if c.get("orientation") == "paysage":
            rem.append("trav.")
        if "Seule face" in (c.get("remarque") or ""):
            rem.append("seule face")
        if "verso de ce feuillet est resté blanc" in (c.get("remarque") or ""):
            rem.append("verso blanc")
        lignes.append(r"%s & %s & \pageref{cl%03d} & %s \\" % (
            folio(c["feuillet"], c["face"]), gabarit.date_ed(p.get("date", "")), n, ", ".join(rem)))
    return "\n".join([
        r"\LJtableconcordance{%",
        "\n".join(lignes),
        "}{}",
    ])


def construire(dossier_pages: Path, dossier_images: str, sortie: Path) -> None:
    codico = charger(EDITION / "donnees" / "codicologie.yaml")["cliches"]
    chapitres = charger(EDITION / "donnees" / "chapitres.yaml")["chapitres"]
    pages = {}
    for c in codico:
        p = dossier_pages / f"{c['cliche']:03d}.yaml"
        if c["statut"] in ("page", "couverture"):
            pages[c["cliche"]] = charger(p)
    lecture = sorted((c for c in codico if c["statut"] in ("page", "couverture")), key=lambda c: c["ordre"])
    info = {c["cliche"]: c for c in codico}

    # renvois (loci paralleli) et index
    entites = charger(EDITION / "donnees" / "index.yaml") if (EDITION / "donnees" / "index.yaml").exists() else {}
    occ = loci_index.occurrences(lecture, pages, entites)
    loci = loci_index.loci_par_page(lecture, occ, info)

    debut_chapitre = {ch["premier_cliche"]: ch for ch in chapitres}
    corps = []
    for c in lecture:
        n = c["cliche"]
        if n in debut_chapitre:
            ch = debut_chapitre[n]
            photos = [r"\LJphoto{%s}{%s}{%s}" % (i.get("largeur", "0.48\\textwidth"), i["fichier"], i["legende"])
                      for i in ch.get("illustrations", [])]
            illus = r"\hspace*{\fill}" + photos[0] + r"\hspace*{\fill}" if len(photos) == 1 else " \\hfill ".join(photos)
            corps.append(r"\LJouverture{%s}{%s}{%s}{cartes/pdf/carte_%s.pdf}{%s}" % (
                ch["numero"], ch["titre"], ch["periode"], ch["numero"], illus))
            corps.append(texte(f"chapitres/{ch['numero']}.tex"))
            fin = ch.get("illustration_fin")
            corps.append(r"\LJfinintro{%s}" % (
                r"\begin{center}\LJphoto{\textwidth}{%s}{%s}\end{center}" % (fin["fichier"], fin["legende"]) if fin else ""))
        p = pages[n]
        meta = {
            "feuillet": folio(c["feuillet"], c["face"]),
            "cliche": f"{n:03d}",
            "mois": p.get("mois") or mois_de(p.get("date", "")),
            "label": f"cl{n:03d}",
            "image": image_fac(n, dossier_images),
            "paysage": c.get("orientation") == "paysage",
            "legende": r"Fac-similé — %s" % folio(c["feuillet"], c["face"]),
            "loci": loci.get(n, ""),
        }
        corps.append(gabarit.double_page(p, meta))

    concordance = table_concordance(codico, pages)

    tex = [
        (ICI / "preambule.tex").read_text(encoding="utf-8"),
        r"\begin{document}",
        texte("liminaires.tex"),
        r"\tableofcontents",
        texte("introduction.tex"),
        texte("titre_journal.tex"),
        *corps,
        texte("annexes.tex"),
        concordance,
        loci_index.index_latex(occ, info, entites),
        texte("colophon.tex"),
        r"\end{document}",
    ]
    sortie.write_text("\n".join(tex), encoding="utf-8")
    print(f"{sortie} : {len(lecture)} pages éditées, {len(chapitres)} chapitres")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", default=str(EDITION / "donnees" / "pages"))
    ap.add_argument("--images", default="fac-similes")
    ap.add_argument("--sortie", default=str(EDITION / "livre_journal.tex"))
    a = ap.parse_args()
    construire(Path(a.pages), a.images, Path(a.sortie))
