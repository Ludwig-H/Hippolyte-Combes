#!/usr/bin/env python3
"""Planche paléographique : extrait des clichés les rectangles choisis (donnees/planche.yaml)
et écrit textes/planche_paleographique.tex (tableau d'extraits légendés).

Chaque extrait : cliché, rectangle relatif (x0, y0, x1, y1), légende. Les extraits sont tirés des
photographies en haute définition, sans retouche, et enregistrés dans illustrations/planche/.
"""
from __future__ import annotations

import os
from pathlib import Path

import yaml
from PIL import Image

RACINE = Path(__file__).resolve().parents[2]
EDITION = RACINE / "edition"
SRC = RACINE / "scans_haute_qualite"
DST = EDITION / "illustrations" / "planche"


def _folio(c: dict) -> str:
    if c.get("feuillet") is None:
        return "couv."
    return r"f.~%d~%s" % (c["feuillet"], r"r\textsuperscript{o}" if c["face"] == "r" else r"v\textsuperscript{o}")


def main():
    spec = yaml.safe_load(open(EDITION / "donnees" / "planche.yaml", encoding="utf-8"))
    codico = {c["cliche"]: c for c in yaml.safe_load(open(EDITION / "donnees" / "codicologie.yaml", encoding="utf-8"))["cliches"]}
    fichiers = sorted(f for f in os.listdir(SRC) if f.endswith(".jpg"))
    DST.mkdir(parents=True, exist_ok=True)
    cases = []
    for i, e in enumerate(spec["extraits"], 1):
        im = Image.open(SRC / fichiers[e["cliche"] - 1]).convert("RGB")
        W, H = im.size
        x0, y0, x1, y1 = e["rect"]
        c = im.crop((int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H)))
        nom = f"{i:02d}_{e['cliche']:03d}.jpg"
        c.save(DST / nom, quality=90)
        fol = _folio(codico[e["cliche"]])
        cases.append((nom, e["legende"], fol, c.size))
    colonnes = spec.get("colonnes", 3)
    larg = r"\dimexpr(\textwidth-%d\tabcolsep)/%d\relax" % (2 * colonnes, colonnes)
    lignes = []
    for k in range(0, len(cases), colonnes):
        rangee = cases[k:k + colonnes]
        imgs = [r"\includegraphics[width=0.96\linewidth,height=12.6mm,keepaspectratio]{illustrations/planche/%s}" % n
                for n, *_ in rangee]
        legs = [r"{\scriptsize %s \textcolor{LJgris}{(%s)}}" % (leg, fol) for _, leg, fol, _ in rangee]
        imgs += [""] * (colonnes - len(rangee))
        legs += [""] * (colonnes - len(rangee))
        lignes.append(" & ".join(imgs) + r" \\")
        lignes.append(" & ".join(legs) + r" \\[1.2mm]")
    tex = "\n".join([
        r"\begin{figure}[p]",
        r"\centering",
        r"\renewcommand{\arraystretch}{1.05}",
        r"\begin{tabular}{@{}" + ("p{%s}" % larg) * colonnes + "@{}}",
        *lignes,
        r"\end{tabular}",
        r"\caption{%s}" % spec.get("titre", "Planche paléographique"),
        r"\label{planche}",
        r"\end{figure}",
    ])
    (EDITION / "textes" / "planche_paleographique.tex").write_text(tex, encoding="utf-8")
    print(f"{len(cases)} extraits -> {DST}")


if __name__ == "__main__":
    main()
