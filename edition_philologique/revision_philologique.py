"""Apply documented readings, guarded against concurrent changes to their source."""
import copy
import json
from pathlib import Path

REVISION_DIR = Path(__file__).resolve().parent / 'revision_2026_10'
CORRECTIONS_PATH = REVISION_DIR / 'corrections_validees.json'
ALLOWED_FIELDS = {'lines', 'title', 'date', 'lieu', 'critique', 'historique', 'marginal_notes'}


def apply_verified_corrections(records, clean_line):
    records = copy.deepcopy(records)
    by_num = {record['scan_num']: record for record in records}
    if CORRECTIONS_PATH.exists():
        revision = json.loads(CORRECTIONS_PATH.read_text(encoding='utf-8'))
        for patch in revision['patches']:
            record = by_num[patch['scan_num']]
            if record['filename'] != patch['filename']:
                raise ValueError(f"Scan/filename mismatch: {patch['scan_num']}")
            for field, value in patch['changes'].items():
                if field not in ALLOWED_FIELDS:
                    raise ValueError(f'Unsupported field: {field}')
                if record[field] != patch['originals'][field]:
                    raise ValueError(f"Source changed for scan {patch['scan_num']:03d}, {field}; reconcile the source, correction and photograph before generating.")
            record.update(copy.deepcopy(patch['changes']))
            if 'lines' in patch['changes'] and 'marginal_notes' not in patch['changes']:
                # Extract notes, but preserve the diplomatic line verbatim.
                record['marginal_notes'] = {}
                for index, line in enumerate(record['lines'], 1):
                    _, note = clean_line(line, index)
                    if note:
                        record['marginal_notes'][str(index)] = note
            record['correction_evidence'] = copy.deepcopy(patch['evidence'])
        for review in revision.get('reviews', []):
            by_num[review['scan_num']]['revision'] = copy.deepcopy(review)
    for record in records:
        record['folio_editorial_ancien'] = record['folio']
        record['foliotation_statut'] = 'Foliotation matérielle non établie'
        if record['scan_num'] > 1:
            prefix = record['folio'].upper() + ' ('
            record['folio'] = f"Vue {record['scan_num']:03d}"
            if record['title'].startswith(prefix) and record['title'].endswith(')'):
                record['title'] = record['title'][len(prefix):-1]
    return records
