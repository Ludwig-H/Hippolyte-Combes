#!/usr/bin/env python3
"""Contrôle indépendant des huit cartes, sans appeler le moteur de rendu.

Dépendances : bibliothèque standard, pyproj, PyMuPDF. Les sources géographiques
archivées, les citations du carnet, les coordonnées, la projection et le PDF
réel sont confrontés. Ce contrôle ne transforme pas une liaison schématique en
tracé routier historique, ni un repère contemporain en adresse de 1916.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import re
import sys
import unicodedata

from pyproj import Transformer
import pymupdf

ROOT = Path(__file__).resolve().parent
IDS = ('generale', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII')
LAYOUT_DPI = 160  # Unité des label_bbox_pixels produites par generer_cartes.py.
POINT_TOLERANCE_PT = 0.15


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized(text):
    return ''.join(c for c in unicodedata.normalize('NFKC', text).casefold() if c.isalnum())


def numeric(value):
    return isinstance(value, (float, int)) and not isinstance(value, bool) and math.isfinite(value)


def overlap(a, b, tolerance=0.02):
    return min(a[2], b[2]) - max(a[0], b[0]) > tolerance and min(a[3], b[3]) - max(a[1], b[1]) > tolerance


def inside(inner, outer, tolerance=0.03):
    return (inner[0] >= outer[0] - tolerance and inner[1] >= outer[1] - tolerance
            and inner[2] <= outer[2] + tolerance and inner[3] <= outer[3] + tolerance)


def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


class Audit:
    def __init__(self, root):
        self.root = root
        self.errors = []
        self.inputs = {}
        self.report = {'version': 1, 'checked_at_utc': datetime.now(timezone.utc).isoformat(),
                       'projection': 'EPSG:2154', 'maps': [], 'limitations': [
                           'Les sources archivées sont contrôlées ; aucun nouveau géocodage en ligne.',
                           'Les points sont des repères contemporains, non les logements de 1916–1917.',
                           'Les routes restent des liaisons entre étapes ; le contrôle vérifie leurs références auditées, pas un itinéraire routier reconstitué.',
                           'Les collisions sont contrôlées sur les rectangles de sécurité des libellés et les cercles réels du PDF ; une alerte peut concerner les marges avant de toucher le texte. La revue visuelle complète le contrôle des fonds et liaisons.',
                       ]}

    def require(self, condition, message):
        if not condition:
            self.errors.append(message)
        return bool(condition)

    def read(self, relative):
        path = self.root / relative
        self.inputs[str(relative)] = digest(path)
        return json.loads(path.read_text(encoding='utf-8'))

    def audit_evidence(self, audit, records):
        count = 0
        for m in audit['maps']:
            for category in ('main_places', 'secondary_places', 'documented_links', 'issues'):
                for item in m.get(category, []):
                    for citation in item.get('evidence', []):
                        scan = citation['scan']
                        if not self.require(scan in records, f"Audit {m['id']}: scan {scan} absent"):
                            continue
                        a, b = citation['lines']
                        lines = records[scan]['lines']
                        if not self.require(1 <= a <= b <= len(lines), f"Audit {m['id']}, scan {scan}: lignes {a}–{b} invalides"):
                            continue
                        expected = ' / '.join(lines[a - 1:b])
                        # Formatting-only spaces in the human audit do not change its citation.
                        flat = lambda s: re.sub(r'\s+', '', unicodedata.normalize('NFKC', s))
                        self.require(flat(expected) == flat(citation['quote']),
                                     f"Audit {m['id']}, scan {scan}, lignes {a}–{b}: citation divergente")
                        count += 1
        self.report['notebook_citations_checked'] = count

    def run(self):
        catalog = self.read('donnees/lieux.json')
        communes = self.read('donnees/repertoire_communes.json')
        special = self.read('donnees/hameaux_et_toulouse_verifies.json')
        config = self.read('cartes.json')
        manifest = self.read('cartes/manifest.json')
        reading = self.read('verification/audit_carnet.json')
        records_path = self.root.parent.parent / 'transcriptions/transcription_integrale_186_scans.json'
        self.inputs['../../transcriptions/transcription_integrale_186_scans.json'] = digest(records_path)
        records = {r['scan_num']: r for r in json.loads(records_path.read_text())}
        self.require(set(records) == set(range(1, 187)), 'Carnet: séquence 001–186 incomplète')
        self.audit_evidence(reading, records)
        self.require(len(catalog) == 82, f'Catalogue: 82 lieux attendus, reçu {len(catalog)}')
        self.require([m['id'] for m in config] == list(IDS), 'Configuration: huit cartes attendues, dans leur ordre éditorial')
        self.require([m['id'] for m in manifest['maps']] == list(IDS), 'Manifeste: huit cartes distinctes attendues')
        sources = {**communes, **{p['id']: p for p in special['points']}}
        for key, place in catalog.items():
            self.require(place.get('id') == key, f'Catalogue {key}: identifiant divergent')
            source = sources.get(key)
            if not self.require(source is not None, f'Catalogue {key}: source géographique archivée absente'):
                continue
            for field in ('longitude', 'latitude', 'source'):
                self.require(place.get(field) == source.get(field), f'Catalogue {key}: {field} divergent de la source archivée')
            self.require(str(place.get('source', '')).startswith('https://'), f'Catalogue {key}: URL source absente')
            for field, limit in [('longitude', 180), ('latitude', 90)]:
                value = place.get(field)
                self.require(numeric(value) and abs(value) <= limit, f'Catalogue {key}: {field} invalide')
        self.report['catalog_places_checked'] = len(catalog)
        self.report['catalog_source_matches'] = sum(all(p.get(f) == sources.get(k, {}).get(f) for f in ('longitude', 'latitude', 'source')) for k, p in catalog.items())
        tf = Transformer.from_crs('EPSG:4326', 'EPSG:2154', always_xy=True)
        by_map = {m['id']: m for m in manifest['maps']}
        audit_by_map = {m['id']: m for m in reading['maps']}
        used = set()
        pdf_digests = []
        for cfg in config:
            map_id = cfg['id']
            if map_id not in by_map:
                self.require(False, f'Carte {map_id}: absente du manifeste')
                continue
            entry = by_map[map_id]
            first_error = len(self.errors)
            local = {'id': map_id, 'panels': [], 'routes': [], 'places_checked': 0}
            self.require(entry.get('projection') == 'EPSG:2154', f'Carte {map_id}: projection divergente')
            self.require(entry['size_mm'] == cfg['size_mm'], f'Carte {map_id}: format divergent')
            self.require(entry['pdf'] == map_id + '.pdf', f'Carte {map_id}: nom PDF divergent')
            path = self.root / 'cartes' / (map_id + '.pdf')
            file_digest = digest(path)
            self.inputs['cartes/' + path.name] = file_digest
            pdf_digests.append(file_digest)
            self.require(file_digest == entry['sha256'], f'Carte {map_id}: empreinte PDF divergente')
            with pymupdf.open(path) as document:
                if not self.require(len(document) == 1, f'Carte {map_id}: PDF de plusieurs pages'):
                    continue
                page = document[0]
                text = page.get_text('text', clip=pymupdf.INFINITE_RECT())
                self.require(text == entry['printed_text'], f'Carte {map_id}: texte PDF différent de printed_text')
                self.require(bool(text.strip()), f'Carte {map_id}: texte non extractible')
                width, height = page.rect.width, page.rect.height
                self.require(abs(width * 25.4 / 72 - cfg['size_mm'][0]) < .01 and abs(height * 25.4 / 72 - cfg['size_mm'][1]) < .01,
                             f'Carte {map_id}: taille physique PDF divergente')
                drawings = page.get_drawings()
                self.require(bool(drawings), f'Carte {map_id}: tracés vectoriels absents')
                circles = [d['rect'] for d in drawings if 2 < d['rect'].width < 10 and 2 < d['rect'].height < 10
                           and abs(d['rect'].width - d['rect'].height) < .08
                           and len(d['items']) >= 4 and all(i[0] == 'c' for i in d['items'])]
                segments = [(tuple(i[1]), tuple(i[2])) for d in drawings for i in d['items'] if i[0] == 'l']
                page_box = (0, 0, width, height)
                for block in page.get_text('dict', clip=pymupdf.INFINITE_RECT())['blocks']:
                    for line in block.get('lines', []):
                        for span in line['spans']:
                            if span.get('text', '').strip():
                                self.require(inside(span['bbox'], page_box, .5), f"Carte {map_id}: texte hors page : {span['text']!r}")
                actual = {p['id']: p for p in entry['places']}
                self.require(len(actual) == len(entry['places']), f'Carte {map_id}: lieux dupliqués au manifeste')
                expected_ids = [k for panel in cfg['panels'] for k in panel['places']]
                self.require(set(actual) == set(expected_ids), f'Carte {map_id}: lieux du manifeste différents de la configuration')
                self.require(len(expected_ids) == len(set(expected_ids)), f'Carte {map_id}: points dupliqués entre panneaux')
                used.update(expected_ids)
                self.require(len(entry['scale_bars']) == len(cfg['panels']), f'Carte {map_id}: nombre de panneaux/échelles divergent')
                expected_routes = [r for panel in cfg['panels'] for r in panel.get('routes', [])]
                self.require(entry['routes'] == expected_routes, f'Carte {map_id}: routes du manifeste divergentes')
                links = audit_by_map.get(map_id, {}).get('documented_links', [])
                audited_scans = {e['scan'] for link in links for e in link.get('evidence', [])}
                for panel_no, panel in enumerate(cfg['panels']):
                    if panel_no >= len(entry['scale_bars']):
                        continue
                    scale = entry['scale_bars'][panel_no]
                    bx, by, bw, bh = panel['box']
                    self.require(bw > 0 and bh > 0 and bx >= 0 and by >= 0 and bx + bw <= 1 and by + bh <= 1,
                                 f'Carte {map_id}, panneau {panel_no + 1}: cadre invalide')
                    self.require(scale['box'] == panel['box'], f'Carte {map_id}: boîte du panneau divergente')
                    x0, x1, y0, y1 = scale['extent_l93']
                    self.require(x1 > x0 and y1 > y0, f'Carte {map_id}: étendue projetée invalide')
                    mx = (x1 - x0) / (bw * cfg['size_mm'][0])
                    my = (y1 - y0) / (bh * cfg['size_mm'][1])
                    self.require(math.isclose(mx, my, rel_tol=1e-8), f'Carte {map_id}: échelles horizontale et verticale différentes')
                    frame = (bx * width, (1 - by - bh) * height, (bx + bw) * width, (1 - by) * height)
                    to_page = lambda x, y: (frame[0] + (x - x0) / (x1 - x0) * bw * width,
                                            frame[3] - (y - y0) / (y1 - y0) * bh * height)
                    length = scale['metres']
                    self.require(numeric(length) and 0 < length < x1 - x0, f'Carte {map_id}: barre métrique invalide')
                    # Compare physical PDF line length/position with the stated metric extent.
                    start = to_page(x0 + (x1 - x0) * .065, y0 + (y1 - y0) * .045)
                    end = to_page(x0 + (x1 - x0) * .065 + length, y0 + (y1 - y0) * .045)
                    bar_found = any((distance(a, start) < POINT_TOLERANCE_PT and distance(b, end) < POINT_TOLERANCE_PT)
                                    or (distance(b, start) < POINT_TOLERANCE_PT and distance(a, end) < POINT_TOLERANCE_PT)
                                    for a, b in segments)
                    self.require(bar_found, f'Carte {map_id}, panneau {panel_no + 1}: barre d’échelle physique absente ou fausse')
                    label_boxes = []
                    point_boxes = []
                    for key in panel['places']:
                        if not self.require(key in catalog and key in actual, f'Carte {map_id}: lieu inconnu {key}'):
                            continue
                        base, rendered = catalog[key], actual[key]
                        for old, new in [('longitude', 'lon'), ('latitude', 'lat')]:
                            self.require(base[old] == rendered[new], f'Carte {map_id}, {key}: {new} divergent du catalogue')
                        x, y = tf.transform(base['longitude'], base['latitude'])
                        self.require(abs(x - rendered['x_l93']) < .001 and abs(y - rendered['y_l93']) < .001,
                                     f'Carte {map_id}, {key}: projection Lambert-93 divergente')
                        self.require(x0 <= x <= x1 and y0 <= y <= y1, f'Carte {map_id}, {key}: point hors cadre')
                        label = panel.get('labels', {}).get(key, base['label'])
                        self.require(rendered['label'] == label, f'Carte {map_id}, {key}: libellé divergent de la configuration')
                        self.require(normalized(label) in normalized(text), f'Carte {map_id}, {key}: nom non extractible du PDF')
                        for flag in ('label_overlap', 'point_overlap', 'outside_pixels'):
                            self.require(rendered.get(flag) == 0, f'Carte {map_id}, {key}: {flag} non nul')
                        center = to_page(x, y)
                        matches = [c for c in circles if distance(((c.x0 + c.x1) / 2, (c.y0 + c.y1) / 2), center) < POINT_TOLERANCE_PT]
                        self.require(len(matches) == 1, f'Carte {map_id}, {key}: repère vectoriel déplacé, absent ou dupliqué')
                        if matches:
                            point_boxes.append((key, tuple(matches[0])))
                        a, b, c, d = rendered['label_bbox_pixels']
                        ratio = 72 / LAYOUT_DPI
                        bounds = (a * ratio, height - d * ratio, c * ratio, height - b * ratio)
                        self.require(inside(bounds, frame, .1), f'Carte {map_id}, {key}: rectangle de libellé hors cadre')
                        label_boxes.append((key, bounds))
                        local['places_checked'] += 1
                    for index, (key, rect) in enumerate(label_boxes):
                        for other_key, other_rect in label_boxes[index + 1:]:
                            self.require(not overlap(rect, other_rect), f'Carte {map_id}: chevauchement des libellés {key}/{other_key}')
                        for other_key, point_rect in point_boxes:
                            self.require(not overlap(rect, point_rect), f'Carte {map_id}: libellé {key} recouvre le point {other_key}')
                    for route in panel.get('routes', []):
                        self.require(len(route['places']) >= 2 and set(route['places']) <= set(panel['places']),
                                     f"Carte {map_id}: route hors des lieux du panneau : {route.get('label')}")
                        scan_ids = [int(n) for n in route.get('scans', [])]
                        self.require(bool(scan_ids) and all(n in records for n in scan_ids), f'Carte {map_id}: route sans scans valides')
                        self.require(set(scan_ids) <= audited_scans, f'Carte {map_id}: route citant des scans non examinés dans l’audit des parcours')
                        self.require('non reconstitué' in route.get('geometry', ''), f'Carte {map_id}: statut schématique de la liaison absent')
                        local['routes'].append({'label': route['label'], 'scans': scan_ids,
                                                'audited_links': [link['date'] for link in links if set(scan_ids) & {e['scan'] for e in link.get('evidence', [])}]})
                    local['panels'].append({'number': panel_no + 1, 'metres_per_mm_x': mx, 'metres_per_mm_y': my,
                                            'scale_length_metres': length, 'physical_scale_line_verified': bar_found,
                                            'point_markers_verified': len(point_boxes), 'labels_checked': len(label_boxes)})
                local['pdf_sha256'] = file_digest
                local['printed_text_exact_match'] = text == entry['printed_text']
                local['passed'] = len(self.errors) == first_error
                self.report['maps'].append(local)
        self.require(len(set(pdf_digests)) == 8, 'PDF: les huit cartes ne sont pas distinctes')
        self.require(used == set(catalog), f'Catalogue et cartes: lieux non utilisés {sorted(set(catalog) - used)}, inconnus {sorted(used - set(catalog))}')
        self.report['distinct_places_printed'] = len(used)
        self.report['point_instances_checked'] = sum(m['places_checked'] for m in self.report['maps'])
        self.report['routes_checked'] = sum(len(m['routes']) for m in self.report['maps'])
        # Reject a report that spans concurrent regeneration of its inputs.
        for name, old_digest in self.inputs.items():
            self.require(digest(self.root / name) == old_digest, f'Entrée modifiée pendant le contrôle : {name}')
        self.report['input_sha256'] = self.inputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    output = args.output or root / 'verification' / 'validation_cartes.json'
    audit = Audit(root)
    try:
        audit.run()
    except Exception as exc:
        audit.errors.append(f'Contrôle interrompu : {type(exc).__name__}: {exc}')
    audit.report['passed'] = not audit.errors
    audit.report['errors'] = audit.errors
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(audit.report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for error in audit.errors:
        print('ÉCHEC:', error, file=sys.stderr)
    print(('OK' if not audit.errors else 'ÉCHEC') + f": {len(audit.report['maps'])} cartes, "
          f"{audit.report.get('distinct_places_printed', 0)} lieux, "
          f"{audit.report.get('point_instances_checked', 0)} repères, "
          f"{audit.report.get('routes_checked', 0)} liaisons. Rapport : {output}")
    return int(bool(audit.errors))


if __name__ == '__main__':
    raise SystemExit(main())
