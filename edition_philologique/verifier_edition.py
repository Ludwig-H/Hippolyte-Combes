#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify the scientific, philological, and typographic integrity of the 186-folio edition.

Run from any directory:
    python3 edition_philologique/verifier_edition.py
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import importlib
import json
from pathlib import Path
import re
import sys
import unicodedata

EDITION_DIR = Path(__file__).resolve().parent
ROOT = EDITION_DIR.parent
EXPECTED = list(range(1, 187))


class Checks:
    def __init__(self):
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def require(self, condition, message):
        if not condition:
            self.errors.append(message)
        return bool(condition)

    def warn(self, message):
        self.warnings.append(message)

    def ids(self, values, label):
        values = list(values)
        return self.require(
            values == EXPECTED,
            f"{label}: expected ordered unique IDs 001–186; "
            f"missing={sorted(set(EXPECTED) - set(values))}, "
            f"duplicates={[n for n, count in Counter(values).items() if count > 1]}",
        )


def read_json(path: Path, checks: Checks):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        checks.require(False, f"{path}: {exc}")
        return None


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def expected_folio_label(scan_num: int) -> str:
    if scan_num == 1:
        return "Couverture (plat supérieur)"
    f_num = scan_num // 2
    side = "recto" if (scan_num % 2 == 0) else "verso"
    return f"Folio {f_num} {side}"


def check_records(records: list[dict], checks: Checks):
    checks.ids([r.get("scan_num") for r in records], "Export records")
    checks.require(len({r.get("filename") for r in records}) == 186, "Photograph filenames are not unique")
    non_empty_critique = 0
    non_empty_loci = 0
    for r in records:
        n = r.get("scan_num")
        name = r.get("filename")
        if not checks.require(
            isinstance(name, str) and Path(name).name == name and name.endswith(".jpg"),
            f"Folio {n}: invalid JPEG filename",
        ):
            continue
        for folder in ("scans_haute_qualite", "scans_compresses"):
            checks.require((ROOT / folder / name).is_file(), f"Folio {n}: missing {folder}/{name}")
        for key in ("folio", "mois_annee", "title", "date", "lieu", "historique"):
            checks.require(isinstance(r.get(key), str) and bool(r[key].strip()), f"Folio {n}: empty/non-string {key}")
        checks.require(isinstance(r.get("critique"), str), f"Folio {n}: critique must be a string")
        checks.require(isinstance(r.get("loci"), str), f"Folio {n}: loci must be a string")
        if r.get("critique", "").strip():
            non_empty_critique += 1
        if r.get("loci", "").strip():
            non_empty_loci += 1
        checks.require(
            r.get("folio") == expected_folio_label(n),
            f"Folio {n}: expected folio label {expected_folio_label(n)!r}, got {r.get('folio')!r}",
        )
        checks.require(
            "Scan #" not in r.get("title", "") and "Vue " not in r.get("title", ""),
            f"Folio {n}: title still contains Scan # or Vue",
        )
        lines = r.get("lines")
        if not checks.require(
            isinstance(lines, list) and bool(lines) and all(isinstance(s, str) for s in lines),
            f"Folio {n}: invalid transcription lines",
        ):
            continue
        notes = r.get("marginal_notes")
        if checks.require(isinstance(notes, dict), f"Folio {n}: invalid marginal notes"):
            for key, value in notes.items():
                checks.require(
                    isinstance(key, str) and key.isdecimal() and 1 <= int(key) <= len(lines),
                    f"Folio {n}: marginal note {key!r} points outside lines",
                )
                checks.require(
                    isinstance(value, str) and bool(value.strip()),
                    f"Folio {n}: empty/non-string marginal note {key!r}",
                )
                checks.require(
                    "et non établi" in value.lower() or "et non " not in value.lower(),
                    f"Folio {n}: marginal note {key!r} still mentions previous misreading ('et non')",
                )
                checks.require(
                    not re.search(r"ne pas lire|n'est pas soutenu|sont éditoriaux|premier document|cliché", value, re.I),
                    f"Folio {n}: marginal note {key!r} still mentions discarded reading or cliché: {value!r}",
                )
                checks.require(
                    not re.search(r"\bvue\s+\d+", value, re.I),
                    f"Folio {n}: marginal note {key!r} still mentions a 'vue' number",
                )
        for field in ("critique", "loci", "historique"):
            val = r.get(field, "")
            checks.require(
                "scans_haute_qualite" not in val
                and "scans_compresses" not in val
                and "cliché" not in val.lower(),
                f"Folio {n}: {field} mentions digitization folder or cliché",
            )
            checks.require(
                "module concurrent" not in val.lower()
                and "ancienne transcription" not in val.lower()
                and "premier document de transcription" not in val.lower(),
                f"Folio {n}: {field} mentions previous draft or module concurrent",
            )
            checks.require(
                "le diariste" not in val.lower(),
                f"Folio {n}: {field} uses 'le diariste' instead of 'Hippolyte Combes'",
            )
            checks.require(
                not re.search(
                    r"saint\s+Hippolyte\s+Combes|Hippolyte\s+Combes\s+Flandrin|(?:Maria|Joséphine)\s+Hippolyte\s+Combes",
                    val,
                ),
                f"Folio {n}: {field} contains corrupted name substitution",
            )
        checks.require(
            "de eodem commorationis loco" not in r.get("loci", ""),
            f"Folio {n}: loci uses generic fallback 'de eodem commorationis loco'",
        )
        crit_val = r.get("critique", "").strip()
        if crit_val:
            checks.require(
                crit_val.startswith(r"\textbf{l.~"),
                f"Folio {n}: critique (Register 1) must start with a line reference \\textbf{{l.~... :}}, got {crit_val[:40]!r}",
            )

    checks.require(
        30 <= non_empty_critique <= 60,
        f"Expected selective internal critical commentary on ~41 folios, got {non_empty_critique}",
    )
    checks.require(
        non_empty_loci == 186,
        f"Expected Latin loci paralleli apparatus on all 186 folios, got {non_empty_loci}",
    )

    from apparat_critique import validate_entries, render_notes
    from loci_verifies import validate_loci_entries
    for record in records:
        if record['scan_num'] != 1:
            try:
                validate_entries(record['apparat_entries'], record['lines'], record['scan_num'])
                checks.require(record['marginal_notes'] == render_notes(record['apparat_entries']),
                               f"Apparat {record['scan_num']:03d}: rendu incomplet ou divergent")
            except (ValueError, KeyError) as exc:
                checks.require(False, str(exc))
        checks.require(record.get('foliotation_statut', '').startswith('Foliotation éditoriale'),
                       f"Folio {record['scan_num']}: convention éditoriale non déclarée")
    try:
        validate_loci_entries(records)
    except ValueError as exc:
        checks.require(False, str(exc))
    from conciliation_argon import load_manifest
    accepted = load_manifest()
    by_num = {r.get("scan_num"): r for r in records}
    for patch in accepted['patches']:
        for field, value in patch['changes'].items():
            checks.require(by_num[patch['scan_num']].get(field) == value,
                           f"Conciliation {patch['scan_num']:03d}: {field} divergent")
    # Verify Folio 1 recto (scan_num == 2) Lines 1 and 2 specifically:
    f1r = by_num.get(2, {})
    f1r_lines = f1r.get("lines", [])
    checks.require(
        len(f1r_lines) == 22
        and f1r_lines[0] == r"25 Ma. \hfill Juillet 1916"
        and f1r_lines[1] == r"Levé [dès ?] 8 H m. \hfill Bien reposé"
        and f1r_lines[2] == "Toute nuit, pensé très vivement à Margte —",
        f"Folio 1 recto lines 1-2 do not match verified reading: {f1r_lines[:2]}",
    )
    if 91 in by_num and 93 in by_num:
        for key in ("lines", "marginal_notes"):
            checks.require(by_num[91][key] == by_num[93][key], f"Photograph duplicate 091/093: different {key}")


def check_exports(records: list[dict], md_path: Path, tex_path: Path, checks: Checks):
    for path in (md_path, tex_path):
        if not checks.require(path.is_file(), f"Missing artifact: {path}"):
            return
    md = md_path.read_text(encoding="utf-8")
    sections = re.findall(r"^##\s+([^\n—]+?)\s+—\s+([^\n]+)$", md, re.M)
    checks.require(len(sections) == 186, f"Markdown sections: expected 186, got {len(sections)}")
    checks.require(
        [fol.strip() for fol, _ in sections] == [r["folio"] for r in records],
        "Markdown section folio sequence differs from JSON",
    )
    checks.require("scans_haute_qualite" not in md and "scans_compresses" not in md, "Markdown still mentions scan folders")
    tex = tex_path.read_text(encoding="utf-8")
    spreads = re.findall(r"^%\s*VIS-A-VIS\s+SPREAD\s*:\s*(.+?)\s*\((20251126_\d{6}\.jpg)\)", tex, re.M)
    checks.require(len(spreads) == 186, f"TeX spreads: expected 186, got {len(spreads)}")
    checks.require(
        [name for _, name in spreads] == [r["filename"] for r in records],
        "TeX spread photograph sequence differs from JSON",
    )
    included = re.findall(r"\\includegraphics(?:\[[^\]]*\])?\s*\{\\facsimiledir/([^}]+)\}", tex)
    checks.require(included == [r["filename"] for r in records], "TeX facsimile inclusion sequence differs from JSON")
    checks.require(
        r"\cline{1-1}\noalign{\vspace{1.2pt}}" in tex and r"\begin{tabular}{@{}p{87mm}@{}p{42.5mm}@{}}" in tex,
        "TeX spread tabular is missing vertical spacing around \\cline{1-1} or isolated inter-column gap",
    )
    checks.require("Lt First" not in tex, "TeX still contains spurious 'Lt First' in Organigramme III")
    for expected_gen in ("Madeleine Fabre-Hugou", "Marie Bouquié", "Sept enfants d'Hippolyte et Marguerite Combes"):
        checks.require(expected_gen in tex, f"TeX Arbre généalogique I missing {expected_gen!r}")
    from generate_edition import build_spread_latex

    for record in records:
        checks.require(
            build_spread_latex(record) in tex,
            f"TeX {record['folio']}: complete current transcription/apparatus/commentary spread absent",
        )


    from cartes_et_index import MAP_IDS, build_indexes_latex
    expected_maps = [f"cartographie/cartes/{map_id}.pdf" for map_id in MAP_IDS]
    included_maps = re.findall(
        r"\\includegraphics(?:\[[^\]]*\])?\s*\{(cartographie/cartes/[^}]+\.pdf)\}", tex)
    checks.require(included_maps == expected_maps,
                   f"TeX: huit cartes PDF requises dans l'ordre attendu ; reçu {included_maps!r}")
    for map_id in MAP_IDS:
        checks.require(tex.count(r'\label{carte:' + map_id + '}') == 1,
                       f"TeX: ancre de carte {map_id} absente ou dupliquée")
    checks.require(tex.count(r'\begin{tikzpicture}') == 3,
                   "TeX: seuls les trois arbres doivent utiliser TikZ ; ancienne carte encore présente")
    context = tex.split('% CHAPITRE I ', 1)[0]
    try:
        checks.require(build_indexes_latex(records, document_context=context) in tex,
                       'TeX: index différents des attestations et commentaires courants')
    except (OSError, ValueError, TypeError) as exc:
        checks.require(False, f"TeX: index des cartes non vérifiable : {exc}")


def ascii_text(text: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c))



def normalized_map_text(text: str) -> str:
    """Ignore PDF line wrapping and punctuation variants, preserving letters."""
    return ''.join(c for c in unicodedata.normalize('NFKC', text).casefold() if c.isalnum())


def check_map_assets(checks: Checks):
    """Check the eight geographical originals and their actual printed labels."""
    from cartes_et_index import MAP_IDS, load_map_manifest, map_asset_path
    try:
        entries = load_map_manifest()
    except (OSError, ValueError, TypeError) as exc:
        checks.require(False, f"Manifeste cartographique : {exc}")
        return []
    try:
        import pymupdf as fitz
    except ImportError:
        try:
            import fitz
        except ImportError:
            checks.require(False, "Le contrôle des cartes PDF requiert PyMuPDF.")
            return []
    assets = []
    paths, digests = [], []
    for entry in entries:
        map_id = entry['id']
        path = map_asset_path(entry)
        paths.append(path)
        if not checks.require(path.is_file(), f"Carte {map_id}: PDF absent : {path}"):
            continue
        digest = sha256(path)
        digests.append(digest)
        checks.require(digest == entry['sha256'], f"Carte {map_id}: SHA-256 du PDF divergent du manifeste")
        try:
            with fitz.open(path) as source:
                if not checks.require(len(source) == 1, f"Carte {map_id}: un PDF d'une seule page est requis"):
                    continue
                page = source[0]
                text = page.get_text('text', clip=fitz.INFINITE_RECT())
                checks.require(bool(page.get_drawings()), f"Carte {map_id}: contenu vectoriel absent")
        except Exception as exc:
            checks.require(False, f"Carte {map_id}: PDF illisible : {exc}")
            continue
        normalized = normalized_map_text(text)
        checks.require(bool(normalized), f"Carte {map_id}: texte extractible absent")
        printed = entry['printed_text']
        for fragment in printed.splitlines():
            needle = normalized_map_text(fragment)
            if needle:
                checks.require(needle in normalized,
                               f"Carte {map_id}: printed_text contient un fragment absent du PDF : {fragment!r}")
        place_ids = []
        valid_places = []
        for place in entry['places']:
            if not checks.require(isinstance(place, dict), f"Carte {map_id}: lieu mal formé : {place!r}"):
                continue
            place_id, label = place.get('id'), place.get('label')
            if not checks.require(isinstance(place_id, str) and bool(place_id.strip()),
                                  f"Carte {map_id}: identifiant de lieu absent"):
                continue
            place_ids.append(place_id)
            if not checks.require(isinstance(label, str) and bool(label.strip()),
                                  f"Carte {map_id}, {place_id}: libellé absent"):
                continue
            needle = normalized_map_text(label)
            checks.require(bool(needle) and needle in normalized,
                           f"Carte {map_id}: libellé du lieu absent du PDF : {label!r}")
            checks.require(bool(needle) and needle in normalized_map_text(printed),
                           f"Carte {map_id}: libellé du lieu absent de printed_text : {label!r}")
            for key, bound in [('lon', 180), ('lat', 90)]:
                value = place.get(key)
                numeric = isinstance(value, (int, float)) and not isinstance(value, bool)
                checks.require(numeric and -bound <= value <= bound,
                               f"Carte {map_id}, {label}: coordonnée {key} invalide : {value!r}")
            valid_places.append(place)
        checks.require(len(place_ids) == len(set(place_ids)), f"Carte {map_id}: lieux dupliqués dans places")
        assets.append({'id': map_id, 'path': path, 'places': valid_places,
                       'printed_text': printed, 'source_text': text})
    checks.require(len(paths) == len(set(paths)) == len(MAP_IDS),
                   "Cartes: huit chemins de PDF distincts sont requis")
    checks.require(len(digests) == len(set(digests)) == len(MAP_IDS),
                   "Cartes: huit PDF distincts et présents sont requis (empreintes SHA-256)")
    return assets


def check_embedded_maps(document, page_texts, assets, checks):
    """Check each map's labels on its own page in the compiled edition."""
    found_pages = []
    for asset in assets:
        map_id = asset['id']
        marker = (r'^\s*CARTE GENERALE\s*$' if map_id == 'generale' else
                  r'^\s*REPERES DU CHAPITRE ' + re.escape(map_id) + r'(?:\s|$)')
        pages = [index for index, text in enumerate(page_texts)
                 if re.search(marker, ascii_text(text), re.M)]
        if not checks.require(len(pages) == 1,
                              f"PDF: carte {map_id}, page propre absente ou répétée : {[p + 1 for p in pages]}"):
            continue
        page_no = pages[0]
        found_pages.append(page_no)
        normalized = normalized_map_text(page_texts[page_no])
        for place in asset['places']:
            checks.require(normalized_map_text(place['label']) in normalized,
                           f"PDF page {page_no + 1}: carte {map_id}, lieu absent : {place['label']!r}")
        for fragment in asset['printed_text'].splitlines():
            needle = normalized_map_text(fragment)
            if needle:
                checks.require(needle in normalized,
                               f"PDF page {page_no + 1}: texte de carte {map_id} absent : {fragment!r}")
        checks.require(bool(document[page_no].get_drawings()),
                       f"PDF page {page_no + 1}: carte {map_id}, tracés vectoriels absents")
    checks.require(len(found_pages) == len(set(found_pages)) == 8,
                   "PDF: les huit cartes doivent occuper huit pages distinctes")


def check_pdf(records: list[dict], pdf_path: Path, tolerance: float, checks: Checks, map_assets=None):
    try:
        import pymupdf as fitz
    except ImportError:
        try:
            import fitz
        except ImportError:
            checks.require(False, "PDF checks require PyMuPDF (pymupdf)")
            return None
    if not checks.require(pdf_path.is_file(), f"Missing PDF: {pdf_path}"):
        return None
    try:
        document = fitz.open(pdf_path)
    except Exception as exc:
        checks.require(False, f"Cannot open PDF: {exc}")
        return None

    folio_to_num = {ascii_text(r["folio"].upper()): r["scan_num"] for r in records}
    records_digest = hashlib.sha256(json.dumps(records, ensure_ascii=False, sort_keys=True).encode('utf-8')).hexdigest()
    checks.require('edition-records-sha256:' + records_digest in (document.metadata.get('keywords') or ''),
                   'PDF: empreinte des enregistrements absente ou périmée')
    from cartes_et_index import MAP_MANIFEST
    if MAP_MANIFEST.is_file():
        checks.require('edition-cartography-sha256:' + sha256(MAP_MANIFEST)
                       in (document.metadata.get('keywords') or ''),
                       'PDF: empreinte du manifeste cartographique absente ou périmée')
    transcriptions: dict[int, int] = {}
    facsimiles: dict[int, int] = {}
    page_texts: list[str] = []

    for page_no, page in enumerate(document):
        text = page.get_text("text", clip=fitz.INFINITE_RECT())
        page_texts.append(text)
        plain = ascii_text(text)

        # Check that no visible text mentions digitization folders or raw JPEG filenames
        checks.require(
            "scans_haute_qualite" not in text and "scans_compresses" not in text and "Cliche numerique" not in plain,
            f"PDF page {page_no + 1}: visible text mentions digitization folder or Cliche numerique",
        )
        checks.require(
            not re.search(r"20251126_\d{6}\.jpg", text),
            f"PDF page {page_no + 1}: visible text exposes raw JPEG filename",
        )

        for fol_upper, snum in folio_to_num.items():
            # Transcription page header starts with FOLIO X RECTO/VERSO or COUVERTURE (PLAT SUPERIEUR)
            if re.search(rf"^\s*{re.escape(fol_upper)}\s+", plain, re.M) and not re.search(
                rf"FAC-SIMILE EN VIS-A-VIS\s*[—–-]\s*{re.escape(fol_upper)}", plain
            ):
                if snum not in transcriptions:
                    transcriptions[snum] = page_no
            if re.search(rf"FAC-SIMILE EN VIS-A-VIS\s*[—–-]\s*{re.escape(fol_upper)}", plain):
                if snum not in facsimiles:
                    facsimiles[snum] = page_no

        overflow = []
        for block in page.get_text("dict", clip=fitz.INFINITE_RECT()).get("blocks", []):
            if block.get("type") != 0:
                continue
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    if not span.get("text", "").strip():
                        continue
                    x0, y0, x1, y1 = span["bbox"]
                    rect = page.rect
                    if (
                        x0 < rect.x0 - tolerance
                        or y0 < rect.y0 - tolerance
                        or x1 > rect.x1 + tolerance
                        or y1 > rect.y1 + tolerance
                    ):
                        overflow.append(span["text"][:80])
        checks.require(not overflow, f"PDF page {page_no + 1}: text outside page (+/-{tolerance:g} pt): {overflow[:3]}")

    checks.ids(sorted(transcriptions), "PDF transcription headings")
    checks.ids(sorted(facsimiles), "PDF facsimile headings")

    source_digests = {
        r["scan_num"]: sha256(ROOT / "scans_compresses" / r["filename"])
        for r in records
        if (ROOT / "scans_compresses" / r["filename"]).is_file()
    }
    image_digest_cache = {}
    for record in records:
        n, fol = record["scan_num"], record["folio"]
        left, right = transcriptions.get(n), facsimiles.get(n)
        if left is None or right is None:
            continue
        checks.require((left + 1) % 2 == 0, f"PDF {fol}: transcription on odd physical page {left + 1}")
        checks.require(right == left + 1, f"PDF {fol}: facsimile {right + 1} is not adjacent to transcription {left + 1}")
        displayed = document[right].get_image_info(xrefs=True)
        matches = []
        for info in displayed:
            xref = info.get("xref", 0)
            if not xref:
                continue
            if xref not in image_digest_cache:
                image_digest_cache[xref] = hashlib.sha256(document.extract_image(xref)["image"]).hexdigest()
            if image_digest_cache[xref] == source_digests.get(n):
                matches.append(info)
        checks.require(
            len(matches) == 1,
            f"PDF {fol}: expected JPEG not displayed exactly once on page {right + 1}; source identity checked by SHA-256",
        )
        for info in matches:
            x0, y0, x1, y1 = info["bbox"]
            bounds = document[right].rect
            checks.require(
                x0 >= bounds.x0 - tolerance
                and y0 >= bounds.y0 - tolerance
                and x1 <= bounds.x1 + tolerance
                and y1 <= bounds.y1 + tolerance,
                f"PDF {fol}: photograph outside physical page bounds",
            )

    full_pdf_text = "\n".join(page_texts)
    checks.require("Index des noms de personnes" in full_pdf_text, "PDF: missing Index des noms de personnes")
    checks.require("Index des noms de lieux" in full_pdf_text, "PDF: missing Index des noms de lieux")
    checks.require("Arbre généalogique I" in full_pdf_text, "PDF: missing Arbre généalogique I")
    checks.require("Arbre généalogique II" in full_pdf_text, "PDF: missing Arbre généalogique II")
    checks.require("Organigramme III" in full_pdf_text, "PDF: missing Organigramme III")

    check_embedded_maps(document, page_texts, map_assets or [], checks)
    total = len(document)
    document.close()
    return total


def check_logs(paths: list[Path], pdf_pages: int | None, checks: Checks):
    checks.require(bool(paths), "No XeLaTeX log found; pass --log PATH for the final compilation")
    for path in paths:
        if not checks.require(path.is_file(), f"XeLaTeX log missing: {path}"):
            continue
        content = path.read_text(encoding="utf-8", errors="replace")
        faults = re.findall(
            r"^.*(?:Missing character:|Overfull \\[hv]box|Undefined control sequence|Emergency stop|Fatal error occurred|LaTeX Error:).*$",
            content,
            re.M,
        )
        checks.require(not faults, f"{path}: compilation/font/layout faults: {faults[:5]}")
        checks.require("Output written on" in content, f"{path}: successful PDF completion marker absent")
        counts = re.findall(r"Output written on[\s\S]{0,240}?\((\d+) pages?", content)
        if pdf_pages is not None and counts:
            checks.require(
                int(counts[-1]) == pdf_pages,
                f"{path}: logged page count {counts[-1]} differs from PDF {pdf_pages}",
            )


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--json", type=Path, default=ROOT / "transcriptions/transcription_integrale_186_scans.json")
    parser.add_argument("--markdown", type=Path, default=ROOT / "transcriptions/transcription_integrale_186_scans.md")
    parser.add_argument("--tex", type=Path, default=EDITION_DIR / "carnet_hippolyte_combes.tex")
    parser.add_argument("--pdf", type=Path, default=EDITION_DIR / "carnet_hippolyte_combes.pdf")
    parser.add_argument("--log", type=Path, action="append", help="Final XeLaTeX log")
    parser.add_argument("--tolerance", type=float, default=2.0, help="Physical page boundary tolerance in points")
    args = parser.parse_args()

    checks = Checks()
    records = read_json(args.json, checks)
    if not isinstance(records, list) or not all(isinstance(r, dict) for r in records):
        checks.require(False, "Export must be a list of record objects")
    else:
        try:
            sys.path.insert(0, str(EDITION_DIR))
            builder = importlib.import_module("parse_all_186").build_all_186_records
            expected = builder()
            checks.require(records == expected, "JSON export differs from a fresh build_all_186_records()")
        except Exception as exc:
            checks.require(False, f"Fresh parser build failed: {exc}")
        map_assets = check_map_assets(checks)
        check_records(records, checks)
        check_exports(records, args.markdown, args.tex, checks)
        pages = check_pdf(records, args.pdf, args.tolerance, checks, map_assets)
        logs = args.log
        if logs is None:
            canonical = args.tex.with_suffix(".log")
            logs = [canonical] if canonical.is_file() else []
        check_logs(logs, pages, checks)

    for message in checks.warnings:
        print(f"WARNING: {message}", file=sys.stderr)
    for message in checks.errors:
        print(f"FAIL: {message}", file=sys.stderr)
    if checks.errors:
        print(f"FAILED: {len(checks.errors)} consistency/layout check(s).", file=sys.stderr)
        return 1
    print(
        f"OK: 186 folios (Couverture + Folio 1 recto to Folio 93 recto); "
        f"JSON/Markdown/TeX consistent; 186 facing PDF pairs across {pages} pages; "
        f"diplomatic layout, 3 bottom registers, 3 genealogical trees, 8 geographical vector PDF maps, and 2 Indexes verified; "
        f"0 Overfull boxes and 0 text overflows."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
