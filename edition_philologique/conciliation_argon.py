"""Apply evidence-based corrections while preserving Argon's edition architecture."""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path

EDITION = Path(__file__).resolve().parent
DOSSIER = EDITION / 'conciliation_argon_2026_10'
MANIFEST = DOSSIER / 'corrections_validees.json'
FIELDS = {'lines', 'apparat_entries', 'marginal_notes', 'critique', 'historique', 'title', 'lieu', 'mois_annee'}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_manifest():
    data = json.loads(MANIFEST.read_text(encoding='utf-8'))
    if sha256(DOSSIER / 'base_argon.json') != data['base_sha256']:
        raise ValueError('La base de conciliation avec Argon a été modifiée.')
    if sha256(EDITION / 'apparat_critique_2026_10/corrections_validees.json') != data['apparat_parent_sha256']:
        raise ValueError('La révision philologique parente a changé ; conciliation nécessaire.')
    for source in data['proposal_files']:
        if sha256(DOSSIER / source['path']) != source['sha256']:
            raise ValueError('Proposition de conciliation modifiée : ' + source['path'])
    return data


def apply_conciliation(records):
    """Only replace explicitly reviewed fields, with exact previous-value guards."""
    from apparat_critique import validate_entries, render_notes
    data = load_manifest()
    if [r['scan_num'] for r in records] != list(range(1, 187)):
        raise ValueError('Conciliation : les 186 vues doivent être ordonnées sans doublon.')
    records = copy.deepcopy(records)
    by_num = {r['scan_num']: r for r in records}
    seen = set()
    for patch in data['patches']:
        n = patch['scan_num']
        if n in seen or n not in by_num:
            raise ValueError('Conciliation : correction dupliquée ou vue inconnue.')
        seen.add(n)
        record = by_num[n]
        if record['filename'] != patch['filename']:
            raise ValueError(f'Conciliation {n:03d} : photographie divergente.')
        if set(patch['changes']) != set(patch['originals']) or set(patch['changes']) - FIELDS:
            raise ValueError(f'Conciliation {n:03d} : champs sans garde ou non autorisés.')
        for field, value in patch['changes'].items():
            actual = record.get(field)
            if actual != patch['originals'][field] and actual != value:
                raise ValueError(f'Conciliation {n:03d}/{field} : nouvel apport à concilier avant export.')
        if not patch.get('evidence'):
            raise ValueError(f'Conciliation {n:03d} : preuve absente.')
        photo = EDITION.parent / 'scans_haute_qualite' / record['filename']
        if sha256(photo) != patch['source_sha256']:
            raise ValueError(f'Conciliation {n:03d} : photographie modifiée.')
        record.update(copy.deepcopy(patch['changes']))
        if 'apparat_entries' in record and n != 1:
            validate_entries(record['apparat_entries'], record['lines'], n)
            if record['marginal_notes'] != render_notes(record['apparat_entries']):
                raise ValueError(f'Conciliation {n:03d} : rendu d’apparat divergent des entrées.')
        record['conciliation_revision'] = {'status': 'Corrections conciliées avec les apports de Gemini 4 Argon',
                                           'evidence': copy.deepcopy(patch['evidence'])}
    for record in records:
        record['foliotation_statut'] = 'Foliotation éditoriale de la séquence photographique ; foliotation matérielle non établie'
    for field in ('lines', 'marginal_notes', 'apparat_entries'):
        if by_num[91].get(field) != by_num[93].get(field):
            raise ValueError(f'Conciliation : les clichés 091/093 de la même page diffèrent ({field}).')
    return records
