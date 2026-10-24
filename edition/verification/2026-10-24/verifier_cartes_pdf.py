#!/usr/bin/env python3
"""Contrôle indépendant des points, des échelles et des limites des neuf PDF cartographiques."""

from pathlib import Path
import yaml, json, math, hashlib
import pymupdf
from pyproj import Transformer

base = Path(__file__).resolve().parents[2] / "cartes"
data = base / "donnees"
places = json.loads((data / "lieux.json").read_text()) | json.loads(
    (data / "lieux_complementaires.json").read_text()
)
rep = json.loads((data / "repertoire_communes.json").read_text())
for k, v in places.items():
    v.setdefault("name", v.get("label", k))
byn = {}
for v in list(places.values()) + list(rep.values()):
    byn.setdefault(v["name"], v)
proj = Transformer.from_crs(4326, 2154, always_xy=True)
report = {
    "base": "ce61fc3",
    "scope": "Géométrie des PDF et identité des points avec le catalogue courant ; ne prouve pas les identifications historiques.",
    "maps": [],
}
for c in yaml.safe_load((base / "cartes.yaml").read_text())["cartes"]:
    w, h = c["taille_mm"]
    bottom = c["legende_mm"]
    top = 9 if c.get("titre_imprime", True) else 1
    chart_h = h - bottom - top
    xmin, ymin, xmax, ymax = c["emprise"]
    pts = [proj.transform(x, y) for x in (xmin, xmax) for y in (ymin, ymax)]
    x0, x1 = min(x for x, y in pts), max(x for x, y in pts)
    y0, y1 = min(y for x, y in pts), max(y for x, y in pts)
    W = max(x1 - x0, (y1 - y0) * w / chart_h)
    H = W * chart_h / w
    cx = (x0 + x1) / 2
    cy = (y0 + y1) / 2
    x0 = cx - W / 2
    y1 = cy + H / 2
    pdf = base / "pdf" / f"carte_{c['id']}.pdf"
    d = pymupdf.open(pdf)
    page = d[0]
    draw = page.get_drawings()
    circles = [
        p["rect"]
        for p in draw
        if len(p["items"]) == 8
        and all(it[0] == "c" for it in p["items"])
        and abs(p["rect"].width - p["rect"].height) < 0.005
        and 0.8 < p["rect"].width < 4.1
    ]
    errs = []
    maxerr = 0
    count = 0
    for group in ["lieux", "contexte"]:
        for pt in c.get(group, []):
            k = pt["id"]
            loc = places.get(k, byn.get(k))
            x, y = proj.transform(loc["longitude"], loc["latitude"])
            px = (x - x0) / W * page.rect.width
            py = top / 25.4 * 72 + (y1 - y) / H * chart_h / 25.4 * 72
            distances = [
                math.hypot((b.x0 + b.x1) / 2 - px, (b.y0 + b.y1) / 2 - py)
                for b in circles
            ]
            e = min(distances)
            maxerr = max(maxerr, e)
            count += 1
            if e > 0.02:
                errs.append({"point": k, "error_pt": e})
    # Two real scale-bar rectangles must have half the nominal projected length each.
    expect = c["echelle_km"] * 1000 / W * page.rect.width / 2
    rects = [
        p["rect"]
        for p in draw
        if len(p["items"]) == 1
        and p["items"][0][0] == "re"
        and abs(p["rect"].width - expect) < 0.02
    ]
    if len(rects) != 2:
        errs.append({"scale_rectangles": len(rects)})
    outside = []
    for b in page.get_text("dict")["blocks"]:
        for line in b.get("lines", []):
            for sp in line["spans"]:
                a, b1, cc, dd = sp["bbox"]
                if sp["text"].strip() and (
                    a < -0.5
                    or b1 < -0.5
                    or cc > page.rect.width + 0.5
                    or dd > page.rect.height + 0.5
                ):
                    outside.append(sp["text"])
    if outside:
        errs.append({"text_outside": outside})
    report["maps"].append(
        {
            "id": c["id"],
            "printed_points": count,
            "max_point_error_pt": round(maxerr, 7),
            "scale_km": c["echelle_km"],
            "scale_rectangles": len(rects),
            "errors": errs,
            "sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
        }
    )
report["ok"] = all(not x["errors"] for x in report["maps"])
Path(__file__).with_name("cartes_controles.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2) + "\n"
)
print(json.dumps(report, ensure_ascii=False, indent=2))

raise SystemExit(0 if report["ok"] else 1)
