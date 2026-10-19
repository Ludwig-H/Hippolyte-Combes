#!/usr/bin/env python3
"""Écrit livret_A4.tex : imposition de livre_journal.pdf en cahiers pliés (deux pages par face de feuille A4 paysage).

Pour un cahier de S pages (multiple de 4), la k-ième feuille porte au recto les pages (S − 2k, 1 + 2k)
et au verso (2 + 2k, S − 1 − 2k). Imprimer en recto verso avec retournement sur le bord court,
plier chaque cahier en son milieu, puis assembler les cahiers dans l'ordre.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pymupdf

EDITION = Path(__file__).resolve().parents[1]
CAHIER = 16


def ordre(n_pages: int, s: int = CAHIER) -> list[str]:
    total = -(-n_pages // s) * s
    out = []
    for debut in range(0, total, s):
        for k in range(s // 4):
            for p in (s - 2 * k, 1 + 2 * k, 2 + 2 * k, s - 1 - 2 * k):
                q = debut + p
                out.append(str(q) if q <= n_pages else "{}")
    return out


def main() -> None:
    n = pymupdf.open(EDITION / "livre_journal.pdf").page_count
    pages = ",".join(ordre(n))
    tex = rf"""% Imposition en livret (générée par src/livret.py) : cahiers de {CAHIER} pages, deux pages de l'édition
% (160 × 226 mm, réduites à 92,8 %) par face de feuille A4 paysage. Impression recto verso,
% retournement sur le bord court ; plier chaque cahier en son milieu et les assembler dans l'ordre.
\documentclass{{article}}
\usepackage[a4paper,landscape,margin=0mm]{{geometry}}
\usepackage{{pdfpages}}
\begin{{document}}
\includepdf[pages={{{pages}}},nup=2x1,frame=false,delta=0mm 0mm]{{livre_journal.pdf}}
\end{{document}}
"""
    (EDITION / "livret_A4.tex").write_text(tex, encoding="utf-8")
    print(f"livret_A4.tex : {n} pages en {-(-n // CAHIER)} cahiers de {CAHIER}")


if __name__ == "__main__":
    main()
