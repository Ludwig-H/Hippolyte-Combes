#!/usr/bin/env python3
"""Prépare les fac-similés de l'édition à partir des photographies en haute définition.

Chaque cliché est réduit à 1 400 pixels sur son grand côté (environ 170 dpi à la taille d’impression)
et enregistré en JPEG progressif, sans retouche de contraste ni de couleur.
Sortie : edition/fac-similes/NNN.jpg (dossier régénérable, non versionné).
"""
from __future__ import annotations

import os
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from PIL import Image

RACINE = Path(__file__).resolve().parents[2]
SRC = RACINE / "scans_haute_qualite"
DST = RACINE / "edition" / "fac-similes"
COTE = 1400
QUALITE = 66


def traiter(args):
    n, nom = args
    out = DST / f"{n:03d}.jpg"
    src = SRC / nom
    if out.exists() and out.stat().st_mtime >= src.stat().st_mtime:
        with Image.open(out) as deja:
            if max(deja.size) == COTE:
                return n, False
    im = Image.open(src).convert("RGB")
    im.thumbnail((COTE, COTE), Image.LANCZOS)
    im.save(out, "JPEG", quality=QUALITE, optimize=True, progressive=True, subsampling=2)
    return n, True


def main():
    DST.mkdir(parents=True, exist_ok=True)
    fichiers = sorted(f for f in os.listdir(SRC) if f.endswith(".jpg"))
    if len(fichiers) != 186:
        sys.exit(f"186 photographies attendues, {len(fichiers)} trouvées")
    with ProcessPoolExecutor(max_workers=os.cpu_count()) as ex:
        faits = sum(1 for _, f in ex.map(traiter, enumerate(fichiers, 1)) if f)
    print(f"{faits} fac-similés préparés dans {DST}")


if __name__ == "__main__":
    main()
