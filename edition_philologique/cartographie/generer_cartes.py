#!/usr/bin/env python3
"""Huit cartes vectorielles documentées ; projection métrique Lambert-93.

Usage: python generer_cartes.py --jobs 8
Dépendances : matplotlib, shapely, pyproj, numpy. Les fonds sont archivés.
Aucun service de géocodage n'est appelé lors du rendu.
"""

from __future__ import annotations
import argparse, concurrent.futures, hashlib, json, math, os
from pathlib import Path

os.environ.setdefault("SOURCE_DATE_EPOCH", "1792108800")
import pymupdf
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.path import Path as MPath
from matplotlib.patches import PathPatch
from matplotlib.collections import LineCollection
from matplotlib.transforms import Bbox
import numpy as np
from pyproj import Transformer
from shapely.geometry import shape, box
from shapely.ops import transform

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "donnees"
OUT = ROOT / "cartes"
TF = Transformer.from_crs(4326, 2154, always_xy=True)
COLORS = ["#934d4c", "#b08b43", "#456f77"]
INK = "#263b43"
MUTED = "#677572"
WATER = "#a9c8ce"
LAND = "#f4f2e9"
plt.rcParams.update(
    {
        "font.family": ["Noto Sans", "DejaVu Sans"],
        "font.size": 8.2,
        "text.color": INK,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        "axes.linewidth": 0.45,
        "savefig.facecolor": "white",
        "figure.facecolor": "white",
        "svg.hashsalt": "combes-cartes-v1",
    }
)


def read(name):
    return json.loads((DATA / name).read_text())


def lines(geom):
    if geom.is_empty:
        return
    if geom.geom_type == "LineString":
        yield np.asarray(geom.coords)
    elif geom.geom_type in ("MultiLineString", "GeometryCollection"):
        for g in geom.geoms:
            yield from lines(g)
    elif geom.geom_type == "Polygon":
        yield np.asarray(geom.exterior.coords)
        for i in geom.interiors:
            yield np.asarray(i.coords)
    elif geom.geom_type == "MultiPolygon":
        for g in geom.geoms:
            yield from lines(g)


def polygon(ax, g, color):
    gs = (
        [g]
        if g.geom_type == "Polygon"
        else list(g.geoms) if g.geom_type == "MultiPolygon" else []
    )
    for p in gs:
        vertices = []
        codes = []
        for ring in [p.exterior, *p.interiors]:
            xy = np.asarray(ring.coords)
            vertices.extend(xy)
            codes.extend(
                [MPath.MOVETO] + [MPath.LINETO] * (len(xy) - 2) + [MPath.CLOSEPOLY]
            )
        ax.add_patch(
            PathPatch(
                MPath(vertices, codes),
                facecolor=color,
                edgecolor="#abb4ae",
                lw=0.55,
                zorder=0,
            )
        )


def load_features(name):
    return [
        (f.get("properties", {}), transform(TF.transform, shape(f["geometry"])))
        for f in read(name)["features"]
    ]


def metric_extent(p, locs, fig):
    if p.get("extent"):
        w, s, e, n = p["extent"]
        xy = np.array(
            [
                TF.transform(x, y)
                for x in np.linspace(w, e, 15)
                for y in np.linspace(s, n, 15)
            ]
        )
    else:
        xy = np.array(
            [
                TF.transform(locs[k]["longitude"], locs[k]["latitude"])
                for k in p["places"]
            ]
        )
    x0, y0 = xy.min(axis=0)
    x1, y1 = xy.max(axis=0)
    if not p.get("extent"):
        dx = max(x1 - x0, 3000)
        dy = max(y1 - y0, 3000)
        x0 -= dx * 0.19
        x1 += dx * 0.19
        y0 -= dy * 0.18
        y1 += dy * 0.18
    # Preserve equal distance in both directions, filling the requested panel.
    ratio = (p["box"][2] * fig.get_figwidth()) / (p["box"][3] * fig.get_figheight())
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    w, h = x1 - x0, y1 - y0
    if w / h < ratio:
        w = h * ratio
    else:
        h = w / ratio
    return cx - w / 2, cx + w / 2, cy - h / 2, cy + h / 2


def scale_and_north(ax, extent):
    x0, x1, y0, y1 = extent
    span = x1 - x0
    candidates = [100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000]
    length = max(v for v in candidates if v < span * 0.23)
    x = x0 + span * 0.065
    y = y0 + (y1 - y0) * 0.045
    ax.plot([x, x + length], [y, y], color=INK, lw=1.05, zorder=10)
    for z in [x, x + length]:
        ax.plot([z, z], [y, y + (y1 - y0) * 0.013], color=INK, lw=0.7, zorder=10)
    ax.text(
        x + length / 2,
        y + (y1 - y0) * 0.026,
        f"{length/1000:g} km",
        ha="center",
        va="bottom",
        fontsize=6.5,
        zorder=10,
    )
    # Arrow follows a true local meridian, not grid north.
    lon, lat = Transformer.from_crs(2154, 4326, always_xy=True).transform(
        x0 + span * 0.93, y0 + (y1 - y0) * 0.86
    )
    a = np.array(TF.transform(lon, lat))
    b = np.array(TF.transform(lon, lat + 0.1))
    d = (b - a) / np.linalg.norm(b - a) * (y1 - y0) * 0.065
    ax.annotate(
        "",
        xy=a + d,
        xytext=a,
        arrowprops={"arrowstyle": "-|>", "color": INK, "lw": 0.65, "mutation_scale": 7},
        zorder=10,
    )
    ax.text(*(a + d * 1.25), "N", fontsize=6.5, ha="center", va="bottom", zorder=10)
    return length


def layout_labels(ax, p, locs, fig):
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    frame = ax.get_window_extent()
    positions = {
        k: TF.transform(locs[k]["longitude"], locs[k]["latitude"]) for k in p["places"]
    }
    pixels = {k: ax.transData.transform(v) for k, v in positions.items()}
    occupied = [
        t.get_window_extent(renderer).expanded(1.08, 1.15)
        for t in ax.texts
        if t.get_text()
    ]
    report = []
    point_boxes = [Bbox.from_bounds(v[0] - 3, v[1] - 3, 6, 6) for v in pixels.values()]
    # Protect scale and compass areas.
    occupied.extend(
        [
            Bbox.from_bounds(
                frame.x0, frame.y0, frame.width * 0.32, frame.height * 0.11
            ),
            Bbox.from_bounds(
                frame.x0 + frame.width * 0.88,
                frame.y0 + frame.height * 0.82,
                frame.width * 0.12,
                frame.height * 0.18,
            ),
        ]
    )
    # Long names first within each class, ensuring each label has sufficient space.
    keys = sorted(
        p["places"],
        key=lambda k: (
            k not in p.get("offsets", {}),
            k not in p["hubs"],
            -len(locs[k]["label"]),
        ),
    )
    for k in keys:
        x, y = positions[k]
        label = locs[k]["label"]
        hub = k in p["hubs"]
        font = p.get("label_font", 8.6) + (0.8 if hub else 0)
        # Explicit multiline labels preserve place spelling in the manifest via extraction.
        label = p.get("labels", {}).get(k, label)
        txt = ax.annotate(
            label,
            (x, y),
            xytext=(6, 3),
            textcoords="offset points",
            ha="left",
            va="center",
            fontsize=font,
            fontweight="bold" if hub else "normal",
            zorder=8,
            bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.88, "pad": 0.2},
        )
        best = None
        for radius in [6, 11, 18, 27, 39, 53, 69, 88]:
            for direction in [0, 180, 45, 135, -45, -135, 90, -90]:
                angle = math.radians(direction)
                dx = radius * math.cos(angle)
                dy = radius * math.sin(angle)
                ha = "left" if dx > 2 else "right" if dx < -2 else "center"
                txt.set_position((dx, dy))
                txt.set_ha(ha)
                bb = txt.get_window_extent(renderer).expanded(1.035, 1.16)
                outside = (
                    max(frame.x0 + 2 - bb.x0, 0)
                    + max(bb.x1 - frame.x1 + 2, 0)
                    + max(frame.y0 + 2 - bb.y0, 0)
                    + max(bb.y1 - frame.y1 + 2, 0)
                )
                overlaps = sum(bb.overlaps(other) for other in occupied)
                dot_hits = sum(bb.overlaps(other) for other in point_boxes)
                cost = (
                    outside * 10000
                    + overlaps * 100000
                    + dot_hits * 30000
                    + radius
                    + abs(dy) * 0.05
                )
                if best is None or cost < best[0]:
                    best = (cost, dx, dy, ha, bb, overlaps, dot_hits, outside)
            if best[0] < 30000:
                break
        if k in p.get("offsets", {}):
            dx, dy = p["offsets"][k]
            ha = "left" if dx > 2 else "right" if dx < -2 else "center"
            txt.set_position((dx, dy))
            txt.set_ha(ha)
            bb = txt.get_window_extent(renderer).expanded(1.035, 1.16)
            overlaps = sum(bb.overlaps(other) for other in occupied)
            hits = sum(bb.overlaps(other) for other in point_boxes)
            outside = (
                max(frame.x0 + 2 - bb.x0, 0)
                + max(bb.x1 - frame.x1 + 2, 0)
                + max(frame.y0 + 2 - bb.y0, 0)
                + max(bb.y1 - frame.y1 + 2, 0)
            )
            if not (overlaps or hits or outside):
                best = (0, dx, dy, ha, bb, overlaps, hits, outside)
        _, dx, dy, ha, bb, overlap, hits, outside = best
        txt.set_position((dx, dy))
        txt.set_ha(ha)
        occupied.append(bb)
        if math.hypot(dx, dy) > 13:
            target = np.array(
                [
                    max(bb.x0, min(pixels[k][0], bb.x1)),
                    max(bb.y0, min(pixels[k][1], bb.y1)),
                ]
            )
            end = ax.transData.inverted().transform(target)
            ax.plot([x, end[0]], [y, end[1]], color="#8a9693", lw=0.45, zorder=5)
        report.append(
            {
                "id": k,
                "label": label,
                "lon": locs[k]["longitude"],
                "lat": locs[k]["latitude"],
                "x_l93": x,
                "y_l93": y,
                "label_bbox_pixels": [round(float(v), 2) for v in bb.extents],
                "label_overlap": int(overlap),
                "point_overlap": int(hits),
                "outside_pixels": round(outside, 3),
            }
        )
    return report


def render_map(m):
    locs = read("lieux.json")
    w, h = m["size_mm"]
    fig = plt.figure(figsize=(w / 25.4, h / 25.4), dpi=160)
    fig.text(
        0.045, 0.965, m["period"], fontsize=7.2, color=MUTED, weight="normal", va="top"
    )
    fig.text(
        0.045,
        0.925,
        m["title"],
        fontfamily="EB Garamond",
        fontsize=17.5,
        va="top",
        color=INK,
    )
    fig.add_artist(
        plt.Line2D(
            [0.045, 0.955],
            [0.89, 0.89],
            transform=fig.transFigure,
            lw=0.7,
            color="#b8a87f",
        )
    )
    reports = []
    scales = []
    countries = load_features("europe_countries.geojson")
    for p in m["panels"]:
        ax = fig.add_axes(p["box"])
        ex = metric_extent(p, locs, fig)
        x0, x1, y0, y1 = ex
        clip = box(x0, y0, x1, y1)
        ax.set_facecolor("#e9f0f0" if p["region"] == "national" else "#faf9f5")
        for props, g in countries:
            if p["region"] == "national" and g.intersects(clip):
                polygon(
                    ax,
                    g.intersection(clip),
                    LAND if props.get("name") in ("France", "Belgium") else "#f6f6f0",
                )
        if p["region"] != "national":
            borders = load_features(
                "communes_"
                + ("toulouse" if p["region"] == "toulouse" else "nord")
                + ".geojson"
            )
            segs = [
                s
                for _, g in borders
                if g.intersects(clip)
                for s in lines(g.boundary.intersection(clip))
            ]
            if p["region"] == "toulouse" or x1 - x0 < 65000:
                ax.add_collection(
                    LineCollection(segs, colors="#d5d8ca", linewidths=0.32, zorder=1)
                )
            hydro = load_features("hydro_" + p["region"] + ".geojson")
            for props, g in hydro:
                if g.intersects(clip):
                    ax.add_collection(
                        LineCollection(
                            list(lines(g.intersection(clip))),
                            colors=WATER,
                            linewidths=1.05 if p["region"] == "toulouse" else 0.9,
                            zorder=2,
                        )
                    )
                    if p.get("hydro_labels", True) and props["name"] not in (
                        "Canal de Brienne",
                        "Canal latéral à la Garonne",
                    ):
                        inner = box(
                            x0 + (x1 - x0) * 0.12,
                            y0 + (y1 - y0) * 0.15,
                            x1 - (x1 - x0) * 0.15,
                            y1 - (y1 - y0) * 0.12,
                        )
                        candidates = list(lines(g.intersection(inner)))
                        if candidates:
                            segment = max(candidates, key=lambda a: len(a))
                            pts = [
                                np.array(
                                    TF.transform(
                                        locs[k]["longitude"], locs[k]["latitude"]
                                    )
                                )
                                for k in p["places"]
                            ]
                            sample = segment[:: max(1, len(segment) // 12)]
                            at = max(
                                sample,
                                key=lambda v: min(np.linalg.norm(v - z) for z in pts),
                            )
                            ax.annotate(
                                props["name"],
                                at,
                                xytext=(3, 3),
                                textcoords="offset points",
                                fontsize=6.8,
                                fontstyle="italic",
                                color="#6b989f",
                                zorder=3,
                                bbox={
                                    "facecolor": "#faf9f5",
                                    "edgecolor": "none",
                                    "alpha": 0.85,
                                    "pad": 0.2,
                                },
                            )
            if p["region"] == "nord":
                segs = [
                    s
                    for _, g in load_features("frontiere_franco_belge_lys.geojson")
                    if g.intersects(clip)
                    for s in lines(g.intersection(clip))
                ]
                if segs:
                    ax.add_collection(
                        LineCollection(
                            segs,
                            colors="#7d8880",
                            linewidths=0.8,
                            linestyles=(0, (3, 2)),
                            zorder=3,
                        )
                    )
        for r in p["routes"]:
            xy = np.array(
                [
                    TF.transform(locs[k]["longitude"], locs[k]["latitude"])
                    for k in r["places"]
                ]
            )
            ax.plot(
                xy[:, 0],
                xy[:, 1],
                color=COLORS[r["color"]],
                lw=1.05,
                alpha=0.82,
                zorder=4,
            )
            # A small arrow on each segment communicates sequence without a false road trace.
            for start, end in zip(xy[:-1], xy[1:]):
                mid = start * 0.35 + end * 0.65
                tail = start * 0.43 + end * 0.57
                ax.annotate(
                    "",
                    xy=mid,
                    xytext=tail,
                    arrowprops={
                        "arrowstyle": "-|>",
                        "color": COLORS[r["color"]],
                        "lw": 0.65,
                        "mutation_scale": 6,
                    },
                    zorder=4,
                )
        for k in p["places"]:
            x, y = TF.transform(locs[k]["longitude"], locs[k]["latitude"])
            hub = k in p["hubs"]
            ax.scatter(
                [x],
                [y],
                s=25 if hub else 13,
                facecolor=COLORS[0] if hub else "white",
                edgecolor=COLORS[0] if hub else INK,
                lw=0.8,
                zorder=7,
            )
        ax.set_xlim(x0, x1)
        ax.set_ylim(y0, y1)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_edgecolor("#c5cdc6")
        scales.append(
            {"metres": scale_and_north(ax, ex), "extent_l93": list(ex), "box": p["box"]}
        )
        if p.get("title"):
            ax.set_title(p["title"], loc="left", fontsize=6.8, color=MUTED, pad=4)
        reports.extend(layout_labels(ax, p, locs, fig))
    # National overview country labels are geographical context, not itinerary places.
    if m["id"] == "generale":
        ax = fig.axes[0]
        for text, x, y in [
            ("FRANCE", 2.5, 46.4),
            ("BELGIQUE", 4.7, 50.8),
            ("MANCHE", -2, 49.6),
            ("OCÉAN ATLANTIQUE", -3.1, 45.9),
            ("MÉDITERRANÉE", 4.8, 42.8),
        ]:
            ax.text(
                *TF.transform(x, y),
                text,
                ha="center",
                fontsize=8 if text == "FRANCE" else 6.6,
                color="#8e9c97",
                zorder=1,
                fontstyle="italic" if text not in ("FRANCE", "BELGIQUE") else "normal",
            )
        x, y = 0.53, 0.235
        fig.text(
            x, y, "UN CARNET, DEUX ESPACES", fontsize=7.2, color=MUTED, weight="bold"
        )
        for i, line in enumerate(
            [
                "Les cantonnements du Nord",
                "et les permissions dans le Midi.",
                "",
                "Les points désignent des localités,",
                "sans localiser les logements.",
            ]
        ):
            fig.text(x, y - 0.023 * (i + 1), line, fontsize=7.1)
        y = 0.195
    elif m["id"] == "III":
        x, y = 0.40, 0.30
        for i, line in enumerate(m["notes"]):
            fig.text(x, y - i * 0.022, line, fontsize=6.5, va="top")
        fig.text(x, 0.205, "Amiens → Paris → Toulouse", fontsize=7, color=COLORS[0])
        fig.text(
            x, 0.18, "25–27 septembre · étapes principales", fontsize=6.4, color=MUTED
        )
        fig.text(
            x,
            0.153,
            "Liaison schématique entre lieux géoréférencés.",
            fontsize=6.2,
            color=MUTED,
        )
        y = 0.085
    else:
        y = 0.184
        rs = [r for p in m["panels"] for r in p["routes"]]
        if not rs:
            fig.text(
                0.05, y, "●  Repère principal     ○  Autre lieu mentionné", fontsize=6.8
            )
            y -= 0.027
        for r in rs:
            fig.add_artist(
                plt.Line2D(
                    [0.05, 0.09],
                    [y + 0.004, y + 0.004],
                    transform=fig.transFigure,
                    color=COLORS[r["color"]],
                    lw=1.4,
                )
            )
            fig.text(0.105, y, r["label"], fontsize=6.6)
            y -= 0.023
        for line in m["notes"]:
            fig.text(0.05, y, line, fontsize=6.5, color=MUTED)
            y -= 0.021
    if m["id"] not in ("III", "generale") and any(p["routes"] for p in m["panels"]):
        fig.text(
            0.05,
            y,
            "Liaisons entre étapes ; tracé historique des voies non reconstitué.",
            fontsize=6.0,
            color=MUTED,
        )
    foot_y = 0.035 if m["id"] != "generale" else 0.017
    fig.text(
        0.05,
        foot_y,
        "Repères actuels · Lambert-93 · fonds Natural Earth / IGN · sources et réserves : dossier cartographie",
        fontsize=5.7,
        color=MUTED,
    )
    if m["id"] == "III":
        fig.text(
            0.05,
            0.014,
            "Purpan : localisation OSM, site patrimonial PA00094494. Limites communales contemporaines.",
            fontsize=5.6,
            color=MUTED,
        )
    if m["id"] == "generale":
        fig.text(0.05, 0.298, m["notes"][0], fontsize=6.2, color=MUTED)
    OUT.mkdir(exist_ok=True)
    pdf = OUT / f"{m['id']}.pdf"
    svg = OUT / f"{m['id']}.svg"
    png = OUT / f"{m['id']}.png"
    fig.savefig(
        pdf,
        metadata={
            "Title": m["title"],
            "Author": "Édition philologique Hippolyte Combes",
            "Subject": "Cartographie documentée ; repères actuels, séjours de 1916–1917",
            "CreationDate": None,
            "ModDate": None,
        },
    )
    fig.savefig(svg, metadata={"Date": None})
    fig.savefig(png, dpi=220)
    plt.close(fig)
    with pymupdf.open(pdf) as document:
        printed = document[0].get_text("text")
    return {
        "id": m["id"],
        "pdf": pdf.name,
        "sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
        "printed_text": printed,
        "places": reports,
        "projection": "EPSG:2154",
        "scale_bars": scales,
        "routes": [r for p in m["panels"] for r in p["routes"]],
        "size_mm": m["size_mm"],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jobs", type=int, default=8)
    parser.add_argument("--only", nargs="*")
    args = parser.parse_args()
    maps = json.loads((ROOT / "cartes.json").read_text())
    selected = [m for m in maps if not args.only or m["id"] in args.only]
    with concurrent.futures.ProcessPoolExecutor(
        max_workers=min(args.jobs, len(selected))
    ) as pool:
        results = list(pool.map(render_map, selected))
    target = OUT / "manifest.json"
    if args.only and target.exists():
        previous = json.loads(target.read_text())["maps"]
        by_id = {m["id"]: m for m in previous}
        by_id.update({m["id"]: m for m in results})
        results = [by_id[m["id"]] for m in maps]
    target.write_text(
        json.dumps({"version": 1, "maps": results}, ensure_ascii=False, indent=2) + "\n"
    )
    for m in results:
        bad = [
            x["label"]
            for x in m["places"]
            if x["label_overlap"] or x["point_overlap"] or x["outside_pixels"]
        ]
        print(
            m["id"],
            len(m["places"]),
            "points",
            "à contrôler: " + ", ".join(bad) if bad else "étiquettes dégagées",
            flush=True,
        )


if __name__ == "__main__":
    main()
