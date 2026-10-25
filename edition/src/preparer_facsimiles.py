#!/usr/bin/env python3
"""Prépare les fac-similés de l'édition à partir des photographies en haute définition.

Chaque cliché est redressé (inclinaison mesurée sur les bords du feuillet, là où la table est visible),
débarrassé des bandes de table le long des bords, réduit à 1 400 pixels sur son grand côté (environ 170 dpi à
la taille d’impression) et enregistré en JPEG progressif. Pour que les pages se suivent sans saut de ton,
l'éclairage est égalisé (division par le fond du papier très lissé : seules les variations à grande échelle,
reflets et dégradés de la prise de vue, sont corrigées ; l'encre et les taches ne le sont pas), puis un gain par
canal ramène le ton du papier (médiane des pixels clairs du centre de la page) à une valeur commune. L'écriture
n'est pas retouchée ; la couverture (cliché 1) est laissée telle quelle.
Sortie : edition/fac-similes/NNN.jpg (dossier régénérable, non versionné).
"""
from __future__ import annotations

import os
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

RACINE = Path(__file__).resolve().parents[2]
SRC = RACINE / "scans_haute_qualite"
DST = RACINE / "edition" / "fac-similes"
COTE = 1400
QUALITE = 66
PAPIER = np.array([222.0, 218.0, 206.0])  # ton commun du papier (R, V, B)
MARQUE = b"fac-simile LJ : redresse, rogne sans toucher l'encre, eclairage et ton harmonises (v3)"


def masque_table(a: np.ndarray) -> np.ndarray:
    """Pixels du bois de la table (brun, plus sombre que le papier)."""
    r, g, b = (a[..., i].astype(np.int32) for i in range(3))
    lum = (r + g + b) / 3
    h, w = lum.shape
    pap = np.percentile(lum[h // 4:3 * h // 4, w // 4:3 * w // 4], 70)
    return ((r - b) > 30) & (lum < 0.80 * pap)


def bande(m: np.ndarray, bord: str) -> np.ndarray:
    """Largeur de la bande de table depuis un bord, ligne par ligne (ou colonne par colonne)."""
    x = {"gauche": m, "droite": m[:, ::-1], "haut": m.T, "bas": m.T[:, ::-1]}[bord]
    nt = ~x
    return np.where(nt.any(axis=1), nt.argmax(axis=1), x.shape[1])


def inclinaison(m: np.ndarray) -> float:
    """Angle (degrés) déduit des bords gauche et droit du feuillet, quand la table y est visible."""
    angs = []
    for bord, signe in (("gauche", 1), ("droite", -1)):
        b = bande(m, bord).astype(float)
        k = len(b)
        y = np.arange(k)[int(k * .08):int(k * .92)]
        b = b[int(k * .08):int(k * .92)]
        if np.median(b) < 5:
            continue
        ok = b < np.percentile(b, 97)
        a, _ = np.polyfit(y[ok], b[ok], 1)
        angs.append(signe * np.degrees(np.arctan(a)))
    return float(np.mean(angs)) if angs else 0.0


def encre_proche(a: np.ndarray, bord: str, pap: float) -> int:
    """Distance (pixels) du bord à la première ligne ou colonne qui porte de l'écriture (traits sombres)."""
    r, g, b = (a[..., i].astype(np.int32) for i in range(3))
    lum = (r + g + b) / 3
    sombre = (lum < 0.62 * pap) & ((r - b) < 30)  # encre violette, noire ou crayon ; pas le bois de la table
    x = {"gauche": sombre.T, "droite": sombre.T[::-1], "haut": sombre, "bas": sombre[::-1]}[bord]
    lignes = np.where(x.sum(axis=1) >= 3)[0]
    return int(lignes[0]) if len(lignes) else x.shape[0]


def redresser_rogner(im: Image.Image) -> Image.Image:
    """Redresse le feuillet et rogne les bandes de table, sans jamais toucher l'écriture : le rognage d'un bord
    s'arrête avant la première trace d'encre et ne dépasse pas 1,2 % de la dimension ; les coins découverts par
    la rotation prennent le ton du papier."""
    a = np.asarray(im)
    h, w = a.shape[:2]
    lum = a.astype(np.float32).mean(axis=2)
    centre = lum[h // 4:3 * h // 4, w // 4:3 * w // 4]
    pap = float(np.percentile(centre, 70))
    ang = inclinaison(masque_table(a))
    # pas de rotation si l'écriture s'approche d'un bord plus que le déplacement des coins
    depl = np.tan(np.radians(abs(ang))) * max(w, h) / 2 + 6
    if abs(ang) > 0.12 and min(encre_proche(a, bd, pap) for bd in ("gauche", "droite", "haut", "bas")) > depl:
        c = a[h // 4:3 * h // 4, w // 4:3 * w // 4].reshape(-1, 3)
        clair = c[c.mean(axis=1) > np.percentile(c.mean(axis=1), 60)]
        fond = tuple(int(v) for v in np.median(clair, axis=0))
        im = im.rotate(-ang, resample=Image.BICUBIC, expand=False, fillcolor=fond)
        a = np.asarray(im)
    m = masque_table(a)
    rog = {}
    for bord, dim in (("gauche", w), ("droite", w), ("haut", h), ("bas", h)):
        b = bande(m, bord)
        k = len(b)
        v = int(np.percentile(b[int(k * .05):int(k * .95)], 75))
        v = v + 2 if v > 2 else 0
        v = min(v, int(0.012 * dim), max(0, encre_proche(a, bord, pap) - 4))
        rog[bord] = v
    return im.crop((rog["gauche"], rog["haut"], w - rog["droite"], h - rog["bas"]))


def harmoniser(im: Image.Image) -> Image.Image:
    """Éclairage égalisé (fond du papier très lissé), puis gain par canal ramenant le ton du papier à PAPIER."""
    a = np.asarray(im, dtype=np.float32)
    petit = im.resize((max(8, im.width // 8), max(8, im.height // 8)), Image.BILINEAR)
    fond = petit.filter(ImageFilter.MaxFilter(9)).filter(
        ImageFilter.GaussianBlur(radius=max(petit.width, petit.height) / 6))
    fond = np.maximum(np.asarray(fond.resize(im.size, Image.BICUBIC)).astype(np.float32), 40)
    a = a * (np.median(fond.reshape(-1, 3), axis=0) / fond)
    h, w, _ = a.shape
    c = a[int(h * .12):int(h * .88), int(w * .12):int(w * .88)].reshape(-1, 3)
    lum = c.mean(axis=1)
    papier = np.median(c[(lum > np.percentile(lum, 55)) & (lum < np.percentile(lum, 97))], axis=0)
    gain = np.clip(PAPIER / papier, 0.83, 1.2)
    return Image.fromarray(np.clip(a * gain + 0.5, 0, 255).astype(np.uint8))


def traiter(args):
    n, nom = args
    out = DST / f"{n:03d}.jpg"
    src = SRC / nom
    if out.exists() and out.stat().st_mtime >= src.stat().st_mtime:
        with Image.open(out) as deja:
            if max(deja.size) == COTE and deja.info.get("comment") == MARQUE:
                return n, False
    im = Image.open(src).convert("RGB")
    if n != 1:
        im = redresser_rogner(im)
    im.thumbnail((COTE, COTE), Image.LANCZOS)
    if n != 1:
        im = harmoniser(im)
    im.save(out, "JPEG", quality=QUALITE, optimize=True, progressive=True, subsampling=2, comment=MARQUE)
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
