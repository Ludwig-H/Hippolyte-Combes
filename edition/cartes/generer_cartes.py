#!/usr/bin/env python3
"""Cartes de l'édition du Livre-Journal (PDF vectoriels avec relief ombré).

Projection : Lambert-93 (EPSG:2154). Relief : MNT Copernicus GLO-30 (cartes régionales) ou
Natural Earth « Gray Earth » (cartes nationales). Les définitions des cartes sont dans cartes.yaml ;
les lieux (coordonnées contrôlées) dans donnees/lieux.json ; les lignes de front dans donnees/fronts.yaml.

Usage : python3 edition/cartes/generer_cartes.py [--dem DOSSIER] [--seule ID] [--png]
"""
from __future__ import annotations

import argparse
import re
import json
import math
import os
from pathlib import Path

import matplotlib
matplotlib.use("pdf")
import matplotlib.pyplot as plt
from matplotlib import font_manager, patheffects
from matplotlib.patches import FancyArrowPatch, Polygon as MplPolygon, Rectangle
import numpy as np
import yaml
from pyproj import Transformer
from shapely.geometry import box, shape, LineString, Point
from shapely.ops import transform as shp_transform

ICI = Path(__file__).resolve().parent
DONNEES = ICI / "donnees"
SORTIE = ICI / "pdf"
POLICES = Path("/usr/share/texlive/texmf-dist/fonts/opentype/public/libertinus-fonts")
for f in POLICES.glob("Libertinus*.otf"):
    font_manager.fontManager.addfont(str(f))
plt.rcParams.update({
    "font.family": "Libertinus Sans",
    "pdf.fonttype": 42,
    "svg.fonttype": "none",
    "axes.linewidth": 0.4,
    "mathtext.fontset": "custom",
    "mathtext.rm": "Libertinus Sans",
    "mathtext.it": "Libertinus Sans:italic",
})

VERS_L93 = Transformer.from_crs(4326, 2154, always_xy=True)
VERS_GEO = Transformer.from_crs(2154, 4326, always_xy=True)

PAPIER = np.array([0.985, 0.976, 0.955])
MER = "#dfe9ee"
EAU = "#5b8fb0"
ENCRE = "#2a2a2a"
ROUGE = "#9c2a1e"
BLEU_ROUTE = "#2f5d8a"
HALO = [patheffects.withStroke(linewidth=2.2, foreground=(1, 1, 1, 0.85))]
HALO_FIN = [patheffects.withStroke(linewidth=1.4, foreground=(1, 1, 1, 0.8))]
MM = 1 / 25.4


def l93(lon, lat):
    return VERS_L93.transform(lon, lat)


def geom_l93(g):
    import shapely
    def f(c):
        x, y = VERS_L93.transform(c[:, 0], c[:, 1])
        return np.column_stack([x, y])
    return shapely.transform(g, f)


# ---------------------------------------------------------------------------
# Relief
# ---------------------------------------------------------------------------
class MNT:
    """Mosaïque de dalles Copernicus GLO-30 (GeoTIFF COG) lues à la demande."""

    def __init__(self, dossier: Path):
        import tifffile
        self.dalles = []
        for f in sorted(Path(dossier).glob("Copernicus_DSM_COG_10_*_DEM.tif")):
            with tifffile.TiffFile(f) as t:
                p = t.pages[0]
                sx, sy, _ = p.tags[33550].value
                tie = p.tags[33922].value
                lon0, lat0 = tie[3], tie[4]
                h, w = p.shape
            self.dalles.append({"f": f, "lon0": lon0, "lat0": lat0, "sx": sx, "sy": sy, "w": w, "h": h, "a": None})

    def _tableau(self, d):
        if d["a"] is None:
            import tifffile
            d["a"] = tifffile.imread(d["f"]).astype(np.float32)
        return d["a"]

    def altitude(self, lon: np.ndarray, lat: np.ndarray) -> np.ndarray:
        z = np.full(lon.shape, np.nan, dtype=np.float32)
        for d in self.dalles:
            lon1 = d["lon0"] + d["w"] * d["sx"]
            lat1 = d["lat0"] - d["h"] * d["sy"]
            m = (lon >= d["lon0"]) & (lon < lon1) & (lat <= d["lat0"]) & (lat > lat1)
            if not m.any():
                continue
            a = self._tableau(d)
            fx = (lon[m] - d["lon0"]) / d["sx"] - 0.5
            fy = (d["lat0"] - lat[m]) / d["sy"] - 0.5
            x0 = np.clip(np.floor(fx).astype(int), 0, d["w"] - 2)
            y0 = np.clip(np.floor(fy).astype(int), 0, d["h"] - 2)
            tx, ty = np.clip(fx - x0, 0, 1), np.clip(fy - y0, 0, 1)
            z[m] = (a[y0, x0] * (1 - tx) * (1 - ty) + a[y0, x0 + 1] * tx * (1 - ty)
                    + a[y0 + 1, x0] * (1 - tx) * ty + a[y0 + 1, x0 + 1] * tx * ty)
        return z


def ombrage(z: np.ndarray, pas: float, exag: float = 3.0, az: float = 315, alt: float = 42) -> np.ndarray:
    z = np.nan_to_num(z, nan=np.nanmin(z) if np.isfinite(z).any() else 0.0) * exag
    gy, gx = np.gradient(z, pas)
    pente = np.arctan(np.hypot(gx, gy))
    aspect = np.arctan2(-gx, gy)
    a, h = math.radians(az), math.radians(alt)
    s = np.sin(h) * np.cos(pente) + np.cos(h) * np.sin(pente) * np.cos(a - aspect)
    return np.clip(s, 0, 1)


def fond_relief(ax, emprise, mnt: MNT | None, ne_gris: Path | None, res: float, exag: float, teinte: bool):
    x0, y0, x1, y1 = emprise
    nx, ny = int((x1 - x0) / res), int((y1 - y0) / res)
    xs = x0 + (np.arange(nx) + 0.5) * res
    ys = y1 - (np.arange(ny) + 0.5) * res
    X, Y = np.meshgrid(xs, ys)
    lon, lat = VERS_GEO.transform(X, Y)
    if mnt is not None:
        z = mnt.altitude(lon, lat)
        terre = np.isfinite(z)
        hs = ombrage(z, res, exag=exag)
        lum = 0.93 + 0.16 * (hs - (hs[terre].mean() if terre.any() else hs.mean()))
        img = np.clip(PAPIER[None, None, :] * lum[..., None], 0, 1)
        if teinte and terre.any():
            zz = np.nan_to_num(z, nan=0.0)
            t = np.clip(zz / 220.0, 0, 1)[..., None]
            img = img * (1 - 0.10 * t) + np.array([0.93, 0.88, 0.78]) * 0.10 * t
        img[~terre] = np.array([0.90, 0.93, 0.95])
    else:
        import tifffile
        g = tifffile.imread(ne_gris)
        H, W = g.shape
        col = np.clip(((lon + 180) / 360 * W).astype(int), 0, W - 1)
        row = np.clip(((90 - lat) / 180 * H).astype(int), 0, H - 1)
        v = g[row, col].astype(np.float32) / 255.0
        lum = 0.93 + 0.22 * (v - 0.72)
        img = np.clip(PAPIER[None, None, :] * lum[..., None], 0, 1)
        # masque terre / mer d'après les contours Natural Earth
        from matplotlib.path import Path as MPath
        terre = np.zeros(X.shape, dtype=bool)
        pts = np.column_stack([X.ravel(), Y.ravel()])
        for f in charger_geojson("europe_countries.geojson"):
            g2 = geom_l93(shape(f["geometry"]))
            for poly in getattr(g2, "geoms", [g2]):
                if poly.geom_type != "Polygon":
                    continue
                bx0, by0, bx1, by1 = poly.bounds
                if bx1 < x0 or bx0 > x1 or by1 < y0 or by0 > y1:
                    continue
                m = MPath(np.asarray(poly.exterior.coords)).contains_points(pts).reshape(X.shape)
                terre |= m
        img[~terre] = np.array([0.88, 0.92, 0.945])
    ax.imshow(img, extent=(x0, x1, y0, y1), origin="upper", interpolation="bilinear", zorder=0)


# ---------------------------------------------------------------------------
# Couches vectorielles
# ---------------------------------------------------------------------------
def typo(o):
    """Typographie des textes imprimés sur les cartes : apostrophe courbe, « 1ᵉʳ » en exposant,
    espace fine insécable devant ; : ? !, tiret demi-cadratin entre deux années."""
    if isinstance(o, str):
        o = re.sub(r"\b1er\b", "1ᵉʳ", o.replace("'", "’"))
        o = re.sub(r"\b(1[89]\d\d|20\d\d)-(1[89]\d\d|20\d\d)\b", "\\1–\\2", o)
        return re.sub(r"[ \u00a0]([;:?!])", "\u202f\\1", o)
    if isinstance(o, list):
        return [typo(x) for x in o]
    if isinstance(o, dict):
        return {k: (v if k in ("id", "couches_eau", "fichier") else typo(v)) for k, v in o.items()}
    return o


def charger_geojson(nom):
    p = DONNEES / nom
    if not p.exists():
        return []
    return json.load(open(p, encoding="utf-8"))["features"]


def tracer_lignes(ax, g, **kw):
    if g.is_empty:
        return
    geoms = getattr(g, "geoms", [g])
    for s in geoms:
        if s.geom_type == "LineString":
            x, y = s.xy
            ax.plot(x, y, **kw)
        elif s.geom_type in ("MultiLineString", "GeometryCollection"):
            tracer_lignes(ax, s, **kw)


def tracer_polygones(ax, g, **kw):
    geoms = getattr(g, "geoms", [g])
    for s in geoms:
        if s.geom_type == "Polygon":
            ax.add_patch(MplPolygon(np.asarray(s.exterior.coords), closed=True, **kw))
        elif s.geom_type == "MultiPolygon":
            tracer_polygones(ax, s, **kw)


def etiquette_cours_deau(ax, g, nom, emprise, taille=6.0, pos_spec=None, evitement=None):
    """Nom du cours d'eau le long de son plus long tronçon visible, en évitant les villes."""
    vis = g.intersection(box(*emprise))
    if vis.is_empty:
        return
    geoms = [s for s in getattr(vis, "geoms", [vis]) if s.geom_type == "LineString"]
    if not geoms:
        return
    if isinstance(pos_spec, (list, tuple)) and len(pos_spec) == 2:
        px, py = l93(pos_spec[0], pos_spec[1])
        pt_cible = Point(px, py)
        tronc = min(geoms, key=lambda s: s.distance(pt_cible))
        t = tronc.project(pt_cible, normalized=True)
        t = max(0.08, min(0.92, t))
    else:
        tronc = max(geoms, key=lambda s: s.length)
        if tronc.length < 0.08 * (emprise[2] - emprise[0]):
            return
        if isinstance(pos_spec, (int, float)):
            t = float(pos_spec)
        elif evitement:
            w = emprise[2] - emprise[0]
            h = emprise[3] - emprise[1]
            best_t, best_d = 0.5, -1.0
            for cand in (0.18, 0.25, 0.32, 0.40, 0.50, 0.60, 0.68, 0.75, 0.82):
                pt = tronc.interpolate(cand, normalized=True)
                if not (emprise[0] + 0.08 * w <= pt.x <= emprise[2] - 0.08 * w and
                        emprise[1] + 0.06 * h <= pt.y <= emprise[3] - 0.06 * h):
                    continue
                dmin = min(math.hypot(pt.x - ex, pt.y - ey) for ex, ey in evitement)
                if dmin > best_d:
                    best_d, best_t = dmin, cand
            t = best_t
        else:
            t = 0.5
    dt = 0.02 if t <= 0.96 else -0.02
    p = tronc.interpolate(t, normalized=True)
    q = tronc.interpolate(t + dt, normalized=True)
    if dt < 0:
        p, q = q, p
    ang = math.degrees(math.atan2(q.y - p.y, q.x - p.x))
    if ang > 90:
        ang -= 180
    if ang < -90:
        ang += 180
    ax.text(p.x, p.y, nom, fontsize=taille, color=EAU, style="italic", rotation=ang, rotation_mode="anchor",
            ha="center", va="bottom", path_effects=HALO_FIN, zorder=4, family="Libertinus Serif", clip_on=True)


# ---------------------------------------------------------------------------
# Carte
# ---------------------------------------------------------------------------
def barre_echelle(ax, emprise, km: float, pos=(0.05, 0.05)):
    x0, y0, x1, y1 = emprise
    bx = x0 + pos[0] * (x1 - x0)
    by = y0 + pos[1] * (y1 - y0)
    L = km * 1000
    h = 0.006 * (y1 - y0)
    for i in range(2):
        ax.add_patch(Rectangle((bx + i * L / 2, by), L / 2, h, facecolor=ENCRE if i == 0 else "white",
                               edgecolor=ENCRE, linewidth=0.4, zorder=8))
    for frac, lab in ((0, "0"), (0.5, f"{km/2:g}".replace(".", ",")), (1, f"{km:g}".replace(".", ",") + "\u00a0km")):
        ax.text(bx + frac * L, by + 2.2 * h, lab, fontsize=5.5, ha="center", va="bottom", color=ENCRE,
                path_effects=HALO_FIN, zorder=8)


def fleche_nord(ax, emprise, pos=(0.95, 0.90)):
    x0, y0, x1, y1 = emprise
    x = x0 + pos[0] * (x1 - x0)
    y = y0 + pos[1] * (y1 - y0)
    d = 0.045 * (y1 - y0)
    ax.add_patch(FancyArrowPatch((x, y - d), (x, y), arrowstyle="-|>", mutation_scale=7, color=ENCRE,
                                 linewidth=0.6, zorder=8))
    ax.text(x, y + 0.01 * (y1 - y0), "N", fontsize=6.5, ha="center", va="bottom", color=ENCRE,
            path_effects=HALO_FIN, zorder=8)


def texte_mixte(fig, x, y_haut, texte, **kw):
    """Texte d'une ligne où les passages entre astérisques (*Livre-Journal*) sont en italique.
    Les segments sont posés sur une même ligne de base, l'un après l'autre."""
    from matplotlib.backends.backend_agg import RendererAgg
    segments = [(seg, i % 2 == 1) for i, seg in enumerate(texte.split("*")) if seg]
    rend = RendererAgg(fig.bbox.width, fig.bbox.height, fig.dpi)
    # ligne de base commune : on pose d'abord le texte entier (romain) aligné en haut pour la mesurer
    essai = fig.text(x, y_haut, texte.replace("*", ""), va="top", **kw)
    _, info, _ = essai._get_layout(rend)
    base_px = essai.get_transform().transform((x, y_haut))[1] + info[0][2][1]
    essai.remove()
    y = fig.transFigure.inverted().transform((0, base_px))[1]
    from matplotlib.textpath import text_to_path
    for seg, ital in segments:
        t = fig.text(x, y, seg, va="baseline", style="italic" if ital else "normal", **kw)
        # avance du segment (espace finale comprise), sans arrondi au pixel
        w_pt = text_to_path.get_text_width_height_descent(seg, t.get_fontproperties(), ismath=False)[0]
        x += w_pt / 72 / fig.get_figwidth()


def masquer_traits(fig, ax, marge_mm=0.3):
    """Interrompt les cours d'eau, frontières et fronts sous les étiquettes (masque de lisibilité).

    Chaque ligne d'étiquette (contour réel de l'encre, agrandi de marge_mm) est retirée des traits
    tracés sous les textes (zorder <= 5) ; les noms de cours d'eau, posés le long de leur trait, n'en font pas partie.
    Les flèches d'itinéraire ne sont pas masquées : leurs étiquettes sont placées hors de leur tracé."""
    from matplotlib.backends.backend_agg import RendererAgg
    from matplotlib.textpath import TextPath
    from matplotlib.transforms import Affine2D
    from shapely.geometry import Polygon as SPoly
    from shapely.ops import unary_union
    rend = RendererAgg(fig.bbox.width, fig.bbox.height, fig.dpi)
    inv = ax.transData.inverted()
    marge = marge_mm * fig.dpi / 25.4
    zones = []
    for t in ax.texts:
        if t.get_zorder() < 5 or not t.get_visible() or not t.get_text().strip():
            continue
        _, info, _ = t._get_layout(rend)
        x0, y0 = t.get_transform().transform(t.get_unitless_position())
        for ligne, _, (dx, dy) in info:
            propre, _ = t._preprocess_math(ligne)
            if not propre.strip():
                continue
            ext = TextPath((0, 0), propre, prop=t.get_fontproperties()).get_extents()
            coins = np.array([[ext.x0, ext.y0], [ext.x1, ext.y0], [ext.x1, ext.y1], [ext.x0, ext.y1]])
            tr = Affine2D().scale(fig.dpi / 72).rotate_deg(t.get_rotation()).translate(x0 + dx, y0 + dy)
            zones.append(SPoly(tr.transform(coins)).buffer(marge, join_style=2))
    if not zones:
        return
    masque = unary_union(zones)
    for l in list(ax.lines):
        xy = l.get_xydata()
        if l.get_zorder() > 5 or len(xy) < 2:
            continue
        reste = LineString(ax.transData.transform(xy)).difference(masque)
        if reste.equals(LineString(ax.transData.transform(xy))):
            continue
        if os.environ.get("CARTES_DIAG") and l.get_zorder() == 5:
            print("masque : front interrompu sous une étiquette")
        morceaux = [g for g in getattr(reste, "geoms", [reste]) if g.geom_type == "LineString" and not g.is_empty]
        if not morceaux:
            l.remove()
            continue
        pts = []
        for g in morceaux:
            pts += [tuple(c) for c in inv.transform(np.asarray(g.coords))] + [(np.nan, np.nan)]
        l.set_data(*zip(*pts[:-1]))


def generer(spec: dict, lieux: dict, fronts: dict, mnt: MNT | None, ne_gris: Path, png: bool):
    if spec.get("emprise", "auto") == "auto":
        pts = []
        for p in spec.get("lieux", []):
            pid = p if isinstance(p, str) else p["id"]
            pts.append(l93(lieux[pid]["longitude"], lieux[pid]["latitude"]))
        xs, ys = zip(*pts)
        m = spec.get("marge_km", 6) * 1000
        emprise = [min(xs) - m, min(ys) - m, max(xs) + m, max(ys) + m]
    else:
        lmin, bmin, lmax, bmax = spec["emprise"]  # lon/lat
        xs, ys = zip(*[l93(lo, la) for lo, la in ((lmin, bmin), (lmin, bmax), (lmax, bmin), (lmax, bmax))])
        emprise = [min(xs), min(ys), max(xs), max(ys)]
    w_mm, h_mm = spec.get("taille_mm", [141, 196])
    # ajuster l'emprise aux proportions de la figure (zone cartographique)
    marge_bas = spec.get("legende_mm", 34)
    carte_h_mm = h_mm - marge_bas - (9 if spec.get("titre_imprime", True) else 1)
    ratio = (carte_h_mm) / w_mm
    cx, cy = (emprise[0] + emprise[2]) / 2, (emprise[1] + emprise[3]) / 2
    W, H = emprise[2] - emprise[0], emprise[3] - emprise[1]
    if H / W < ratio:
        H = W * ratio
    else:
        W = H / ratio
    emprise = [cx - W / 2, cy - H / 2, cx + W / 2, cy + H / 2]

    fig = plt.figure(figsize=(w_mm * MM, h_mm * MM))
    ax = fig.add_axes([0, (marge_bas) / h_mm, 1, carte_h_mm / h_mm])
    ax.set_xlim(emprise[0], emprise[2])
    ax.set_ylim(emprise[1], emprise[3])
    ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_linewidth(0.5); s.set_color(ENCRE)

    # titre (omis pour les cartes de chapitre : le titre du chapitre est imprimé au-dessus)
    if spec.get("titre_imprime", True):
        fig.text(0.0, 1 - 2.5 / h_mm, spec.get("surtitre", "").upper(), fontsize=6, color="#555555", va="top")
        texte_mixte(fig, 0.0, 1 - 4.6 / h_mm, spec["titre"], fontsize=11, family="Libertinus Serif", color=ENCRE)

    # fond
    res = spec.get("resolution_m", (emprise[2] - emprise[0]) / 1400)
    fond_relief(ax, emprise, mnt if spec.get("relief", "mnt") == "mnt" else None, ne_gris, res,
                spec.get("exageration", 4.0), spec.get("teinte", True))

    zone = box(*emprise).buffer(0.2 * (emprise[2] - emprise[0]))
    # pays (vue nationale) : contours et étiquettes
    if spec.get("pays", False):
        for f in charger_geojson("europe_countries.geojson"):
            g = geom_l93(shape(f["geometry"])).intersection(zone)
            if g.is_empty:
                continue
            tracer_lignes(ax, g.boundary, color="#7d7d7d", linewidth=0.45, zorder=2)
    # frontière locale
    for f in charger_geojson("frontiere_franco_belge_lys.geojson") if spec.get("frontiere", False) else []:
        g = geom_l93(shape(f["geometry"])).intersection(zone)
        tracer_lignes(ax, g, color="#6b6b6b", linewidth=0.6, dashes=(3, 1.2, 0.8, 1.2), zorder=2)
    # points à éviter pour le placement des noms de cours d'eau
    evitement = []
    for lst in (spec.get("lieux", []), spec.get("contexte", [])):
        for p in lst:
            pid = p if isinstance(p, str) else p["id"]
            L = lieux[pid]
            evitement.append(l93(L["longitude"], L["latitude"]))

    # cours d'eau (regroupés par nom et fusionnés avant découpage)
    from shapely.ops import linemerge, unary_union
    noms_eau = set(spec.get("cours_deau", []))
    geoms_par_nom: dict[str, list] = {}
    for fichier in spec.get("couches_eau", ["hydro_nord.geojson", "hydro_nord_complement.geojson"]):
        for f in charger_geojson(fichier):
            nom = f["properties"].get("name")
            if noms_eau and nom not in noms_eau:
                continue
            geoms_par_nom.setdefault(nom or "", []).append(geom_l93(shape(f["geometry"])))
    pos_eau = spec.get("pos_cours_deau") or {}
    tol_simp = min(25.0, max(3.0, res * 0.4))
    for nom, liste_g in geoms_par_nom.items():
        u = unary_union(liste_g)
        if u.geom_type == "MultiLineString":
            u = linemerge(u)
        g = u.intersection(zone)
        if g.is_empty:
            continue
        g = g.simplify(tol_simp)
        lw = 0.9 if nom in ("Somme", "Lys", "Garonne", "Seine", "Loire", "Escaut", "Rhône", "Tarn") else 0.55
        tracer_lignes(ax, g, color=EAU, linewidth=lw, solid_capstyle="round", zorder=3)
        if nom and nom in spec.get("noms_cours_deau", noms_eau):
            etiquette_cours_deau(ax, g, nom, emprise, taille=spec.get("taille_eau", 6.0),
                                 pos_spec=pos_eau.get(nom), evitement=evitement)

    # zones et lignes de front
    for fr in spec.get("fronts", []):
        d = fronts[fr["id"]]
        pts = [l93(lo, la) for lo, la in d["points"]]
        ligne = LineString(pts)
        style = fr.get("style", d.get("style", "plein"))
        couleur = fr.get("couleur", d.get("couleur", ROUGE))
        kw = dict(color=couleur, linewidth=fr.get("epaisseur", 1.3), zorder=5, solid_capstyle="round")
        if style == "tirets":
            kw["dashes"] = (4, 2)
        elif style == "pointille":
            kw["dashes"] = (1.2, 1.4)
        tracer_lignes(ax, ligne, **kw)
        if fr.get("etiquette"):
            lx, ly = l93(*fr["etiquette_pos"])
            ax.text(lx, ly, fr["etiquette"], fontsize=5.8, color=couleur, style="italic", ha=fr.get("ha", "left"),
                    va="center", rotation=fr.get("rotation", 0), path_effects=HALO, zorder=7.5,
                    family="Libertinus Serif")

    # zone tenue par l'armée allemande : à l'est du front choisi (hachures légères)
    if spec.get("zone_allemande"):
        zid = spec["zone_allemande"]
        pts = [l93(lo, la) for lo, la in fronts[zid]["points"]]
        x1 = emprise[2] + 0.3 * (emprise[2] - emprise[0])
        poly = [pts[0]] + pts + [pts[-1]]
        poly = [(x1, pts[0][1] + 0.5 * (emprise[3] - emprise[1]))] + [(pts[0][0], pts[0][1] + 0.5 * (emprise[3] - emprise[1]))] + pts + \
               [(pts[-1][0], pts[-1][1] - 0.5 * (emprise[3] - emprise[1])), (x1, pts[-1][1] - 0.5 * (emprise[3] - emprise[1]))]
        ax.add_patch(MplPolygon(poly, closed=True, facecolor=(0.55, 0.45, 0.42, 0.10), edgecolor="none", zorder=1.5))
        ax.add_patch(MplPolygon(poly, closed=True, facecolor="none", edgecolor=(0.55, 0.35, 0.32, 0.25), hatch="////",
                                linewidth=0, zorder=1.6))

    # itinéraires
    for r in spec.get("itineraires", []):
        pts = [l93(lieux[i]["longitude"], lieux[i]["latitude"]) for i in r["lieux"]]
        couleur = r.get("couleur", BLEU_ROUTE)
        courbures = r.get("courbures") or [r.get("courbure", 0.08)] * (len(pts) - 1)
        for (xa, ya), (xb, yb), rad in zip(pts[:-1], pts[1:], courbures):
            ax.add_patch(FancyArrowPatch((xa, ya), (xb, yb), arrowstyle="-|>", mutation_scale=6,
                                         shrinkA=4, shrinkB=4, color=couleur, linewidth=0.9,
                                         linestyle=r.get("trait", "-"), zorder=6,
                                         connectionstyle=f"arc3,rad={rad}"))

    # repères de contexte (localités du front, villes) : petits, gris, sans lien avec le carnet
    for p in spec.get("contexte", []):
        if isinstance(p, str):
            p = {"id": p}
        L = lieux[p["id"]]
        x, y = l93(L["longitude"], L["latitude"])
        ax.plot([x], [y], marker="o", markersize=1.4, markerfacecolor="#8a8a8a", markeredgecolor="none", zorder=6)
        mx = (emprise[2] - emprise[0]) / w_mm
        ax.text(x + p.get("dx", 0.9) * mx, y + p.get("dy", 0.0) * mx, p.get("etiquette", L["name"]), fontsize=5.4,
                ha=p.get("ha", "left"), va=p.get("va", "center"), color="#6f6f6f", style="italic",
                family="Libertinus Serif", path_effects=HALO, zorder=6.5, clip_on=True)

    # lieux du carnet
    for p in spec.get("lieux", []):
        if isinstance(p, str):
            p = {"id": p}
        L = lieux[p["id"]]
        x, y = l93(L["longitude"], L["latitude"])
        rang = p.get("rang", 2)
        taille = {1: 3.8, 2: 2.8, 3: 2.1}[rang]
        ax.plot([x], [y], marker="o", markersize=taille, markerfacecolor=ROUGE if rang == 1 else "white",
                markeredgecolor=ENCRE, markeredgewidth=0.6, zorder=7)
        dx, dy = p.get("dx", 1.3 if p.get("ha", "left") == "left" else -1.3), p.get("dy", 0.0)  # en mm
        mx = (emprise[2] - emprise[0]) / w_mm
        lab = typo(p.get("etiquette", L.get("label", L["name"])))
        if p.get("date"):
            lab = lab + "\n" + p["date"]
        ax.text(x + dx * mx, y + dy * mx, lab, fontsize={1: 7.8, 2: 6.8, 3: 6.0}[rang],
                fontweight="bold" if rang == 1 else "normal", ha=p.get("ha", "left"), va=p.get("va", "center"),
                color=ENCRE, path_effects=HALO, zorder=8, linespacing=0.95, clip_on=True)

    # textes libres (régions, notes sur la carte)
    for t in spec.get("textes", []):
        x, y = l93(*t["pos"])
        ax.text(x, y, t["texte"], fontsize=t.get("taille", 6.5), color=t.get("couleur", "#6a6a6a"),
                style=t.get("style", "italic"), ha=t.get("ha", "center"), va=t.get("va", "center"),
                rotation=t.get("rotation", 0), path_effects=HALO_FIN, zorder=5, family="Libertinus Serif",
                fontweight=t.get("graisse", "normal"), clip_on=True)

    barre_echelle(ax, emprise, spec.get("echelle_km", 10))
    fleche_nord(ax, emprise, pos=tuple(spec.get("nord_pos", (0.95, 0.90))))
    masquer_traits(fig, ax)

    # légende sous la carte
    y = (marge_bas - 3) / h_mm
    for item in spec.get("legende", []):
        if item.get("type") == "ligne":
            fig.lines.append(plt.Line2D([0.0, 0.05], [y - 0.004, y - 0.004], transform=fig.transFigure,
                                        color=item.get("couleur", ROUGE), linewidth=item.get("epaisseur", 1.3),
                                        dashes=item.get("dashes", (None, None)) if item.get("dashes") else (None, None)))
        elif item.get("type") == "point":
            fig.lines.append(plt.Line2D([0.025], [y - 0.004], transform=fig.transFigure, marker="o",
                                        markersize=item.get("taille", 3.2), markerfacecolor=item.get("couleur", ROUGE),
                                        markeredgecolor=ENCRE, markeredgewidth=0.6, linestyle="none"))
        elif item.get("type") == "cercle":
            fig.lines.append(plt.Line2D([0.025], [y - 0.004], transform=fig.transFigure, marker="o",
                                        markersize=item.get("taille", 2.8), markerfacecolor="white",
                                        markeredgecolor=ENCRE, markeredgewidth=0.6, linestyle="none"))
        elif item.get("type") == "zone":
            hz = 2.4 / h_mm
            for fc, hat, ec in (((0.55, 0.45, 0.42, 0.10), None, "none"),
                                ("none", "////", (0.55, 0.35, 0.32, 0.45))):
                fig.patches.append(Rectangle((0.0, y - 0.004 - hz / 2), 0.05, hz, transform=fig.transFigure,
                                             facecolor=fc, edgecolor=ec, hatch=hat, linewidth=0))
        elif item.get("type") == "fleche":
            fig.patches.append(FancyArrowPatch((0.0, y - 0.004), (0.05, y - 0.004), transform=fig.transFigure,
                                               arrowstyle="-|>", mutation_scale=6, color=item.get("couleur", BLEU_ROUTE),
                                               linewidth=0.9))
        fig.text(0.065, y, item["texte"], fontsize=6.2, va="top", color=ENCRE, wrap=True)
        y -= item.get("hauteur", 3.6) / h_mm
    for note in spec.get("notes", []):
        fig.text(0.0, y, note, fontsize=5.6, va="top", color="#555555")
        y -= 3.0 / h_mm
    import textwrap
    src = spec.get("sources", "Fond : relief d'après Copernicus DEM GLO-30 (© DLR e.V. 2010–2014 et © Airbus Defence and Space "
                   "GmbH 2014–2018, programme Copernicus), cours d'eau IGN BD TOPO (Licence Ouverte 2.0) ; "
                   "repères actuels ; projection Lambert-93.")
    src = typo(src)
    fig.text(0.0, 0.2 / h_mm, "\n".join(textwrap.wrap(src, 170)), fontsize=4.6, va="bottom", color="#777777",
             linespacing=1.15)

    SORTIE.mkdir(parents=True, exist_ok=True)
    out = SORTIE / f"carte_{spec['id']}.pdf"
    fig.savefig(out)
    if png:
        fig.savefig(out.with_suffix(".png"), dpi=150)
    plt.close(fig)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dem", default="/workspaces/hc_work/carto/dem")
    ap.add_argument("--seule")
    ap.add_argument("--png", action="store_true")
    a = ap.parse_args()
    specs = typo(yaml.safe_load(open(ICI / "cartes.yaml", encoding="utf-8"))["cartes"])
    lieux = json.load(open(DONNEES / "lieux.json", encoding="utf-8"))
    sup = DONNEES / "lieux_complementaires.json"
    if sup.exists():
        lieux.update(json.load(open(sup, encoding="utf-8")))
    for k, v in lieux.items():
        v.setdefault("name", v.get("label", k))
    repertoire = json.load(open(DONNEES / "repertoire_communes.json", encoding="utf-8"))
    par_nom = {}
    for v in list(lieux.values()) + list(repertoire.values()):
        par_nom.setdefault(v["name"], v)

    class Lieux(dict):
        """Accès par identifiant ou, à défaut, par nom exact (catalogue, puis répertoire des communes)."""
        def __missing__(self, cle):
            if cle in par_nom:
                return par_nom[cle]
            raise KeyError(f"lieu inconnu : {cle}")
    lieux = Lieux(lieux)
    fronts = {}
    if (DONNEES / "fronts.yaml").exists():
        fy = yaml.safe_load(open(DONNEES / "fronts.yaml", encoding="utf-8"))
        fronts = {k: typo(v) for k, v in fy["fronts"].items()}
        for nom, parts in (fy.get("composes") or {}).items():
            pts = []
            for part in parts:
                for pt in fronts[part]["points"]:
                    if not pts or pts[-1] != pt:
                        pts.append(pt)
            fronts[nom] = {"nom": nom, "couleur": fronts[parts[0]].get("couleur", ROUGE), "points": pts}
    mnt = MNT(Path(a.dem))
    ne = Path(a.dem) / "ne_gray" / "GRAY_HR_SR_OB_DR.tif"
    for s in specs:
        if a.seule and s["id"] != a.seule:
            continue
        print(generer(s, lieux, fronts, mnt, ne, a.png))


if __name__ == "__main__":
    main()
