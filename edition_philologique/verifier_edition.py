#!/usr/bin/env python3
"""Check the reproducibility and physical layout of the 186-view working edition.

Run from any directory::
    python edition_philologique/verifier_edition.py
    python edition_philologique/verifier_edition.py --log /tmp/hc_reprise/xelatex_final.txt

No files are generated or changed. PyMuPDF is required for PDF inspection. The
checks establish artifact consistency, not the correctness of manuscript readings.
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
        return self.require(values == EXPECTED,
                            f'{label}: expected ordered unique IDs 001–186; '
                            f'missing={sorted(set(EXPECTED)-set(values))}, '
                            f'duplicates={[n for n, count in Counter(values).items() if count > 1]}')


def read_json(path, checks):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        checks.require(False, f'{path}: {exc}')
        return None


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def local_path(parent, name, checks):
    """Reject manifest paths escaping the repository, without fetching URLs."""
    if not isinstance(name, str) or not name:
        checks.require(False, f'Invalid local manifest path: {name!r}')
        return None
    candidate = (parent / name).resolve()
    if not checks.require(candidate.is_relative_to(ROOT.resolve()),
                          f'Manifest path escapes repository: {name}'):
        return None
    return candidate


def check_digest(parent, name, expected, checks, label):
    path = local_path(parent, name, checks)
    if path is None:
        return
    if not checks.require(isinstance(expected, str) and bool(re.fullmatch(r'[0-9a-f]{64}', expected)),
                          f'{label}: invalid SHA-256 for {name}'):
        return
    if not checks.require(path.is_file(), f'{label}: missing file {path}'):
        return
    checks.require(sha256(path) == expected, f'{label}: SHA-256 mismatch for {path}')


def check_revision(records, revision_path, checks):
    revision = read_json(revision_path, checks)
    if not isinstance(revision, dict):
        checks.require(False, 'Missing or invalid accepted revision manifest')
        return
    reviews = revision.get('reviews', [])
    checks.ids([r.get('scan_num') for r in reviews], 'Accepted reviews')
    by_num = {r.get('scan_num'): r for r in records}
    for review in reviews:
        n = review.get('scan_num')
        record = by_num.get(n)
        if not checks.require(record is not None, f'Review {n}: no corresponding record'):
            continue
        checks.require(review.get('filename') == record.get('filename'), f'Review {n}: photograph mismatch')
        checks.require(review.get('review_level', review.get('niveau')) == 'collation_ligne_a_ligne',
                       f'Review {n}: detailed collation status missing')
        checks.require(isinstance(review.get('remaining_uncertainties'), list),
                       f'Review {n}: remaining_uncertainties must be a list')
        checks.require(record.get('revision') == review, f'Record {n}: review differs from manifest')
    patches = revision.get('patches', [])
    patch_ids = [p.get('scan_num') for p in patches]
    checks.require(len(patch_ids) == len(set(patch_ids)), 'Accepted patches: duplicate scan IDs')
    for patch in patches:
        n = patch.get('scan_num')
        record = by_num.get(n)
        if not checks.require(record is not None, f'Patch {n}: unknown scan'):
            continue
        checks.require(patch.get('filename') == record.get('filename'), f'Patch {n}: photograph mismatch')
        checks.require(set(patch.get('changes', {})) == set(patch.get('originals', {})),
                       f'Patch {n}: changes and originals differ in fields')
        checks.require(bool(patch.get('evidence')), f'Patch {n}: no evidence recorded')
        for key, value in patch.get('changes', {}).items():
            checks.require(record.get(key) == value, f'Patch {n}: export differs for {key}')
    proposals = revision.get('proposal_files', [])
    checks.require(bool(proposals), 'Revision: no proposal SHA-256 manifest')
    for source in proposals:
        check_digest(revision_path.parent, source.get('path'), source.get('sha256'), checks, 'Proposal')
    modules = revision.get('source_modules_sha256', {})
    checks.require(bool(modules), 'Revision: no source module SHA-256 manifest')
    for name, digest in modules.items():
        check_digest(EDITION_DIR, name, digest, checks, 'Source module')
    if 'relecture_base_sha256' in revision:
        second = EDITION_DIR / 'relecture_integrale_2026_10'
        check_digest(second, 'base_relecture.json', revision['relecture_base_sha256'], checks, 'Second collation baseline')
        check_digest(second, 'base_corrections_validees.json', revision.get('previous_revision_sha256'), checks, 'Archived first revision')
        if 'concurrent_proposals_sha256' in revision:
            check_digest(second, 'apports_concurrents.json', revision['concurrent_proposals_sha256'], checks, 'Concurrent proposals')
    # These archived input manifests are optional when using another revision
    # directory, but are checked if present. They must agree with the accepted one.
    archived = revision_path.parent / 'base_sources_sha256.json'
    if archived.exists():
        original_manifest = read_json(archived, checks)
        checks.require(original_manifest == modules, 'Archived source hashes differ from accepted manifest')
    baseline = revision_path.parent / 'base_edition_reprise.json'
    for source in proposals:
        path = local_path(revision_path.parent, source.get('path'), checks)
        if path and path.is_file():
            data = read_json(path, checks)
            if isinstance(data, dict) and data.get('baseline_sha256'):
                if checks.require(baseline.is_file(), 'Proposal baseline snapshot missing'):
                    checks.require(sha256(baseline) == data['baseline_sha256'],
                                   f'Proposal baseline SHA-256 mismatch: {path.name}')
            if isinstance(data, dict) and data.get('base_sha256'):
                check_digest(EDITION_DIR / 'relecture_integrale_2026_10', 'base_relecture.json', data['base_sha256'], checks, 'Second collation proposal baseline')


def check_records(records, checks):
    checks.ids([r.get('scan_num') for r in records], 'Export records')
    checks.require(len({r.get('filename') for r in records}) == 186, 'Photograph filenames are not unique')
    for r in records:
        n = r.get('scan_num')
        name = r.get('filename')
        if not checks.require(isinstance(name, str) and Path(name).name == name and name.endswith('.jpg'),
                              f'Scan {n}: invalid JPEG filename'):
            continue
        for folder in ('scans_haute_qualite', 'scans_compresses'):
            checks.require((ROOT / folder / name).is_file(), f'Scan {n}: missing {folder}/{name}')
        for key in ('folio', 'title', 'date', 'lieu', 'critique', 'historique'):
            checks.require(isinstance(r.get(key), str) and bool(r[key].strip()),
                           f'Scan {n}: empty/non-string {key}')
        lines = r.get('lines')
        if not checks.require(isinstance(lines, list) and bool(lines) and all(isinstance(s, str) for s in lines),
                              f'Scan {n}: invalid transcription lines'):
            continue
        notes = r.get('marginal_notes')
        if checks.require(isinstance(notes, dict), f'Scan {n}: invalid marginal notes'):
            for key, value in notes.items():
                checks.require(isinstance(key, str) and key.isdecimal() and 1 <= int(key) <= len(lines),
                               f'Scan {n}: marginal note {key!r} points outside lines')
                checks.require(isinstance(value, str) and bool(value.strip()),
                               f'Scan {n}: empty/non-string marginal note {key!r}')
        checks.require(isinstance(r.get('folio_editorial_ancien'), str) and bool(r['folio_editorial_ancien']),
                       f'Scan {n}: old editorial foliation not archived')
        checks.require(r.get('foliotation_statut') == 'Foliotation matérielle non établie',
                       f'Scan {n}: physical foliation status missing')
        if isinstance(n, int) and n > 1:
            checks.require(r.get('folio') == f'Vue {n:03d}', f'Scan {n}: must be labelled Vue, not physical folio')
            checks.require(not re.match(r'^FOLIO\s+\d+', r.get('title', ''), re.I),
                           f'Scan {n}: title still asserts old physical folio')
    by_num = {r.get('scan_num'): r for r in records}
    if 91 in by_num and 93 in by_num:
        for key in ('lines', 'marginal_notes'):
            checks.require(by_num[91][key] == by_num[93][key], f'Photograph duplicate 091/093: different {key}')


def check_apparatus(records, prior_records, checks):
    """Check the new layer separately from the immutable earlier revision."""
    from apparat_critique import DOSSIER, MANIFEST, validate_entries, render_notes, load_manifest
    if not MANIFEST.exists():
        return
    try:
        data = load_manifest()
    except Exception as exc:
        checks.require(False, f'Apparatus manifest: {exc}')
        return
    frozen = read_json(DOSSIER / 'base_edition.json', checks)
    checks.require(prior_records == frozen, 'Apparatus: earlier edition no longer reproduces the frozen baseline')
    patches, reviews = data.get('patches', []), data.get('reviews', [])
    checks.ids([p.get('scan_num') for p in patches], 'Apparatus patches')
    checks.ids([r.get('scan_num') for r in reviews], 'Apparatus image reviews')
    source_patches, source_reviews = [], []
    for source in data['proposal_files']:
        proposal = read_json(DOSSIER / source['path'], checks)
        if isinstance(proposal, dict):
            source_patches.extend(proposal.get('patches', []))
            source_reviews.extend(proposal.get('reviews', []))
    checks.require(patches == sorted(source_patches, key=lambda p: p['scan_num']),
                   'Apparatus: accepted patches differ from reviewed proposal files')
    checks.require(reviews == sorted(source_reviews, key=lambda r: r['scan_num']),
                   'Apparatus: accepted reviews differ from reviewed proposal files')
    by_num = {r['scan_num']: r for r in records}
    old = {r['scan_num']: r for r in prior_records}
    for patch in patches:
        n = patch['scan_num']
        record = by_num[n]
        checks.require(bool(patch.get('evidence')), f'Apparatus {n:03d}: evidence missing')
        for key, value in patch['originals'].items():
            checks.require(old[n].get(key) == value, f'Apparatus {n:03d}: original guard differs for {key}')
        for key, value in patch['changes'].items():
            checks.require(record.get(key) == value, f'Apparatus {n:03d}: accepted change differs for {key}')
        entries = patch['entries']
        try:
            validate_entries(entries, record['lines'], n)
        except ValueError as exc:
            checks.require(False, str(exc))
        checks.require(record.get('apparat_entries') == entries, f'Apparatus {n:03d}: structured entries differ')
        checks.require(record.get('marginal_notes') == render_notes(entries), f'Apparatus {n:03d}: rendered notes differ or are truncated')
        checks.require(record.get('apparat_evidence') == patch['evidence'], f'Apparatus {n:03d}: evidence differs')
        for line_no, line in enumerate(record['lines'], 1):
            # Editorial doubts and deletions need a corresponding anchored note.
            # This checks coverage, not the philological interpretation itself.
            for pattern, kind in [(r'⟦[^⟧]*⟧', 'rature'),
                                  (r'\[[^\[\]]*(?:\?|illis|incertain|non établi)[^\[\]]*\]', 'lecture')]:
                for match in re.finditer(pattern, line):
                    if kind == 'lecture' and any(m.start() <= match.start() < m.end() for m in re.finditer(r'⟦[^⟧]*⟧', line)):
                        continue
                    accepted_kinds = (kind, 'ajout', 'rature') if 'biff' in match.group() else (kind, 'ajout')
                    covered = any(e['line'] == line_no and e['kind'] in accepted_kinds and
                                  any(m.start() < match.end() and m.end() > match.start()
                                      for m in re.finditer(re.escape(e['lemma']), line)) for e in entries)
                    checks.require(covered, f'Apparatus {n:03d}/{line_no}: {kind} marker lacks anchored entry: {match.group()}')
    for review in reviews:
        record = by_num[review['scan_num']]
        checks.require(record.get('apparat_revision') == review, f"Apparatus {review['scan_num']:03d}: review differs")
        checks.require(review.get('controlled_lines', review.get('checked_lines')) == list(range(1, len(record['lines'])+1)),
                       f"Apparatus {review['scan_num']:03d}: incomplete line coverage")


def check_exports(records, md_path, tex_path, checks):
    for path in (md_path, tex_path):
        if not checks.require(path.is_file(), f'Missing artifact: {path}'):
            return
    md = md_path.read_text(encoding='utf-8')
    sections = re.findall(r'^##\s+Scan\s+#(\d{3})\s+[—–-]\s+`([^`]+)`', md, re.M)
    checks.ids([int(n) for n, _ in sections], 'Markdown sections')
    checks.require([name for _, name in sections] == [r['filename'] for r in records],
                   'Markdown section photograph sequence differs from JSON')
    tex = tex_path.read_text(encoding='utf-8')
    spreads = re.findall(r'^%\s*VIS-A-VIS\s+SPREAD\s*:\s*SCAN\s+#(\d{3})\s*\(([^)]+)\)', tex, re.M)
    checks.ids([int(n) for n, _ in spreads], 'TeX spreads')
    checks.require([name for _, name in spreads] == [r['filename'] for r in records],
                   'TeX spread photograph sequence differs from JSON')
    included = re.findall(r'\\includegraphics(?:\[[^\]]*\])?\s*\{\\facsimiledir/([^}]+)\}', tex)
    checks.require(included == [r['filename'] for r in records], 'TeX facsimile inclusion sequence differs from JSON')
    from generate_edition import build_spread_latex
    for record in records:
        checks.require(build_spread_latex(record) in tex,
                       f"TeX scan {record['scan_num']:03d}: complete current transcription/apparatus/commentary spread absent")


def ascii_text(text):
    return ''.join(c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c))


def check_pdf(records, pdf_path, tolerance, checks):
    try:
        import pymupdf as fitz
    except ImportError:
        try:
            import fitz
        except ImportError:
            checks.require(False, 'PDF checks require PyMuPDF (pymupdf)')
            return None
    if not checks.require(pdf_path.is_file(), f'Missing PDF: {pdf_path}'):
        return None
    try:
        document = fitz.open(pdf_path)
    except Exception as exc:
        checks.require(False, f'Cannot open PDF: {exc}')
        return None
    records_digest = hashlib.sha256(json.dumps(records, ensure_ascii=False, sort_keys=True).encode('utf-8')).hexdigest()
    checks.require('edition-records-sha256:' + records_digest in (document.metadata.get('keywords') or ''),
                   'PDF metadata: source records SHA-256 differs (PDF may precede current apparatus)')
    transcriptions, facsimiles = {}, {}
    page_texts = []
    for page_no, page in enumerate(document):
        # Infinite clipping includes text outside the media box instead of
        # accidentally hiding the very overflow this validator is looking for.
        text = page.get_text('text', clip=fitz.INFINITE_RECT())
        page_texts.append(text)
        plain = ascii_text(text)
        headings = re.findall(r'^\s*SCAN\s*#\s*(\d{3})\s*[—–-]', plain, re.M)
        fac_headings = re.findall(r'^\s*FAC[ -]*SIMILE\b[^\n]*(?:\n[^\n]*){0,3}?\(SCAN\s*#\s*(\d{3})\)', plain, re.M)
        for label, numbers, mapping in [('transcription', headings, transcriptions), ('facsimile', fac_headings, facsimiles)]:
            for number in numbers:
                n = int(number)
                if checks.require(n not in mapping, f'PDF: duplicate {label} heading {n:03d}'):
                    mapping[n] = page_no
        overflow = []
        for block in page.get_text('dict', clip=fitz.INFINITE_RECT()).get('blocks', []):
            if block.get('type') != 0:
                continue
            for line in block.get('lines', []):
                for span in line.get('spans', []):
                    if not span.get('text', '').strip():
                        continue
                    x0, y0, x1, y1 = span['bbox']
                    rect = page.rect
                    if x0 < rect.x0-tolerance or y0 < rect.y0-tolerance or x1 > rect.x1+tolerance or y1 > rect.y1+tolerance:
                        overflow.append(span['text'][:80])
        checks.require(not overflow, f'PDF page {page_no+1}: text outside page (+/-{tolerance:g} pt): {overflow[:3]}')
    checks.ids(sorted(transcriptions), 'PDF transcription headings')
    checks.ids(sorted(facsimiles), 'PDF facsimile headings')
    source_digests = {r['scan_num']: sha256(ROOT / 'scans_compresses' / r['filename'])
                      for r in records if (ROOT / 'scans_compresses' / r['filename']).is_file()}
    image_digest_cache = {}
    for record in records:
        n, name = record['scan_num'], record['filename']
        left, right = transcriptions.get(n), facsimiles.get(n)
        if left is None or right is None:
            continue
        checks.require((left+1) % 2 == 0, f'PDF scan {n:03d}: transcription on odd physical page {left+1}')
        checks.require(right == left+1, f'PDF scan {n:03d}: facsimile {right+1} is not adjacent to transcription {left+1}')
        compact = re.sub(r'\s+', '', page_texts[right])
        checks.require(f'scans_compresses/{name}' in compact,
                       f'PDF scan {n:03d}: compressed source caption absent from facsimile page {right+1} (possible caption overflow)')
        checks.require(f'scans_haute_qualite/{name}' in compact,
                       f'PDF scan {n:03d}: HQ source caption absent from facsimile page {right+1}')
        checks.require(name in re.sub(r'\s+', '', page_texts[left]),
                       f'PDF scan {n:03d}: photograph filename absent from transcription header')
        displayed = document[right].get_image_info(xrefs=True)
        matches = []
        for info in displayed:
            xref = info.get('xref', 0)
            if not xref:
                continue
            if xref not in image_digest_cache:
                image_digest_cache[xref] = hashlib.sha256(document.extract_image(xref)['image']).hexdigest()
            if image_digest_cache[xref] == source_digests.get(n):
                matches.append(info)
        checks.require(len(matches) == 1,
                       f'PDF scan {n:03d}: expected JPEG not displayed exactly once on page {right+1}; source identity checked by SHA-256')
        for info in matches:
            x0, y0, x1, y1 = info['bbox']
            bounds = document[right].rect
            checks.require(x0 >= bounds.x0-tolerance and y0 >= bounds.y0-tolerance and x1 <= bounds.x1+tolerance and y1 <= bounds.y1+tolerance,
                           f'PDF scan {n:03d}: photograph outside physical page bounds')
    total = len(document)
    document.close()
    return total


def check_logs(paths, pdf_pages, checks):
    checks.require(bool(paths), 'No XeLaTeX log found; pass --log PATH for the final compilation')
    for path in paths:
        if not checks.require(path.is_file(), f'XeLaTeX log missing: {path}'):
            continue
        content = path.read_text(encoding='utf-8', errors='replace')
        faults = re.findall(r'^.*(?:Missing character:|Overfull \\[hv]box|Undefined control sequence|Emergency stop|Fatal error occurred|LaTeX Error:).*$', content, re.M)
        checks.require(not faults, f'{path}: compilation/font/layout faults: {faults[:5]}')
        checks.require('Output written on' in content, f'{path}: successful PDF completion marker absent')
        counts = re.findall(r'Output written on[\s\S]{0,240}?\((\d+) pages?', content)
        if pdf_pages is not None and counts:
            checks.require(int(counts[-1]) == pdf_pages,
                           f'{path}: logged page count {counts[-1]} differs from PDF {pdf_pages}')
        if not counts:
            checks.warn(f'{path}: PDF page count could not be extracted from log')


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--json', type=Path, default=ROOT / 'transcriptions/transcription_integrale_186_scans.json')
    parser.add_argument('--markdown', type=Path, default=ROOT / 'transcriptions/transcription_integrale_186_scans.md')
    parser.add_argument('--tex', type=Path, default=EDITION_DIR / 'carnet_hippolyte_combes.tex')
    parser.add_argument('--pdf', type=Path, default=EDITION_DIR / 'carnet_hippolyte_combes.pdf')
    parser.add_argument('--revision', type=Path, default=EDITION_DIR / 'revision_2026_10/corrections_validees.json')
    parser.add_argument('--log', type=Path, action='append', help='Final XeLaTeX log; repeat to inspect both final passes')
    parser.add_argument('--tolerance', type=float, default=2.0, help='Physical page boundary tolerance in points (default: 2)')
    args = parser.parse_args()
    checks = Checks()
    records = read_json(args.json, checks)
    if not isinstance(records, list) or not all(isinstance(r, dict) for r in records):
        checks.require(False, 'Export must be a list of record objects')
    else:
        prior_records = None
        try:
            sys.path.insert(0, str(EDITION_DIR))
            builder = importlib.import_module('parse_all_186').build_all_186_records
            expected = builder()
            prior_records = builder(apply_apparatus=False)
            checks.require(records == expected, 'JSON export differs from a fresh build_all_186_records()')
            if records != expected:
                differing = [r.get('scan_num') for r, s in zip(records, expected) if r != s]
                checks.warn(f'Differing records (first 20): {differing[:20]}')
        except Exception as exc:
            checks.require(False, f'Fresh parser build failed (possible concurrent source change): {exc}')
        check_records(records, checks)
        if prior_records is not None:
            check_revision(prior_records, args.revision, checks)
            check_apparatus(records, prior_records, checks)
        check_exports(records, args.markdown, args.tex, checks)
        pages = check_pdf(records, args.pdf, args.tolerance, checks)
        logs = args.log
        if logs is None:
            canonical = args.tex.with_suffix('.log')
            if canonical.is_file():
                logs = [canonical]
            else:
                candidates = list(Path('/tmp/hc_reprise').glob('*xelatex*.txt'))
                logs = [max(candidates, key=lambda p: p.stat().st_mtime)] if candidates else []
        check_logs(logs, pages, checks)
    for message in checks.warnings:
        print(f'WARNING: {message}', file=sys.stderr)
    for message in checks.errors:
        print(f'FAIL: {message}', file=sys.stderr)
    if checks.errors:
        print(f'FAILED: {len(checks.errors)} consistency/layout check(s).', file=sys.stderr)
        return 1
    print(f'OK: 186 records and reviews; matching source/proposal hashes; JSON/Markdown/TeX consistent; '
          f'186 facing PDF pairs across {pages} pages; correct JPEGs and captions; no detected text overflow.')
    print('Limit: artifact consistency is verified, not philological certainty or factual accuracy of historical notes.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
