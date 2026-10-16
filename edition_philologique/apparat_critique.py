"""Apply the fully reviewed apparatus after the older transcription revisions."""
import copy
import hashlib
import json
from collections import defaultdict
from pathlib import Path

EDITION = Path(__file__).resolve().parent
DOSSIER = EDITION / 'apparat_critique_2026_10'
MANIFEST = DOSSIER / 'corrections_validees.json'
FIELDS = {'lines', 'critique', 'historique', 'title'}
KINDS = {'abreviation', 'emprunt', 'rature', 'ajout', 'lecture', 'signe', 'compte', 'syntaxe', 'disposition'}
LANGUAGES = {'en': 'angl.', 'la': 'lat.', 'de': 'all.', 'hybride': 'hybr.'}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tex_text(value):
    # Entries are plain text. Escape once, character by character.
    escapes = {'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$',
               '#': r'\#', '_': r'\_', '{': r'\{', '}': r'\}',
               '~': r'\textasciitilde{}', '^': r'\textasciicircum{}'}
    return ''.join(escapes.get(c, c) for c in value)


def validate_entries(entries, lines, n):
    if not isinstance(entries, list):
        raise ValueError(f'Apparat {n:03d} : entries doit être une liste.')
    seen = set()
    for entry in entries:
        line, lemma = entry.get('line'), entry.get('lemma')
        if not isinstance(line, int) or not 1 <= line <= len(lines):
            raise ValueError(f'Apparat {n:03d} : ligne hors texte {line!r}.')
        if not isinstance(lemma, str) or not lemma.strip() or lemma not in lines[line-1]:
            raise ValueError(f'Apparat {n:03d}/{line} : lemme absent {lemma!r}.')
        if entry.get('kind') not in KINDS:
            raise ValueError(f'Apparat {n:03d}/{line} : catégorie inconnue.')
        if not isinstance(entry.get('note'), str) or not entry['note'].strip():
            raise ValueError(f'Apparat {n:03d}/{line} : note vide.')
        if entry.get('language', 'en') not in LANGUAGES:
            raise ValueError(f'Apparat {n:03d}/{line} : langue inconnue.')
        key = (line, lemma, entry['kind'], entry['note'])
        if key in seen:
            raise ValueError(f'Apparat {n:03d}/{line} : entrée dupliquée {lemma!r}.')
        seen.add(key)


def render_notes(entries):
    """Keep every reviewed entry, in source order, without a per-line quota."""
    grouped = defaultdict(list)
    for entry in entries:
        grouped[entry['line']].append(entry)
    result = {}
    for line, row in sorted(grouped.items()):
        parts = []
        for entry in row:
            lemma = tex_text(entry['lemma'])
            note = tex_text(entry['note'].strip().rstrip('.'))
            if entry['kind'] == 'abreviation':
                explanation = r'\textit{' + note + '}'
            elif entry['kind'] == 'emprunt':
                language = LANGUAGES[entry.get('language', 'en')]
                explanation = r'\textit{' + language + '} ' + note
            else:
                explanation = note
            parts.append(r'\textbf{' + lemma + '} ' + explanation)
        result[str(line)] = r'\textbf{' + str(line) + '} ' + ' ; '.join(parts) + '.'
    return result


def load_manifest():
    data = json.loads(MANIFEST.read_text())
    meta = json.loads((DOSSIER / 'base_manifest.json').read_text())
    for name, key in [('base_edition.json', 'base_sha256'), ('base_revision.json', 'parent_revision_sha256')]:
        if digest(DOSSIER / name) != data[key] or data[key] != meta[key]:
            raise ValueError(f'Base de l’apparat modifiée : {name}.')
    parent = EDITION / 'revision_2026_10/corrections_validees.json'
    if digest(parent) != data['parent_revision_sha256']:
        raise ValueError('Révision antérieure modifiée ; concilier les apports avant application de l’apparat.')
    for source in data['proposal_files']:
        if digest(DOSSIER / source['path']) != source['sha256']:
            raise ValueError(f"Lot d’apparat modifié : {source['path']}.")
        proposal = json.loads((DOSSIER / source['path']).read_text())
        for component in proposal.get('component_files', []):
            if digest(DOSSIER / component['path']) != component['sha256']:
                raise ValueError(f"Sous-lot d’apparat modifié : {component['path']}.")
    if [r.get('scan_num') for r in data['reviews']] != list(range(1, 187)):
        raise ValueError('Apparat : les 186 contrôles doivent être présents exactement une fois.')
    for review in data['reviews']:
        if review.get('review_level') != 'apparat_integral_sur_image':
            raise ValueError('Apparat : contrôle visuel incomplet.')
        photo = EDITION.parent / 'scans_haute_qualite' / review['filename']
        if digest(photo) != review['source_sha256']:
            raise ValueError(f"Photographie de l’apparat modifiée : {review['scan_num']:03d}.")
    return data


def apply_apparatus(records):
    if not MANIFEST.exists():
        if (DOSSIER / 'base_manifest.json').exists():
            raise FileNotFoundError('Manifeste de l’apparat absent : exécuter assembler_apparat.py avant l’export ; aucune régression silencieuse vers l’ancien apparat.')
        return records
    data = load_manifest()
    base = {r['scan_num']: r for r in json.loads((DOSSIER / 'base_edition.json').read_text())}
    records = copy.deepcopy(records)
    if [r.get('scan_num') for r in records] != list(range(1, 187)):
        raise ValueError('Apparat : la base doit contenir les 186 vues ordonnées sans doublon.')
    by_num = {r['scan_num']: r for r in records}
    for n, record in by_num.items():
        for field in FIELDS | {'filename', 'date', 'lieu', 'marginal_notes'}:
            if record[field] != base[n][field]:
                raise ValueError(f'Apparat : état antérieur divergent {n:03d}/{field}.')
    if sorted(p['scan_num'] for p in data['patches']) != list(range(1, 187)):
        raise ValueError('Apparat : les 186 vues doivent être présentes exactement une fois.')
    for patch in data['patches']:
        n = patch['scan_num']
        record = by_num[n]
        if record['filename'] != patch['filename']:
            raise ValueError(f'Apparat {n:03d} : photographie divergente.')
        for field, original in patch['originals'].items():
            if record[field] != original:
                raise ValueError(f'Apparat {n:03d}/{field} : valeur antérieure divergente.')
        if set(patch['changes']) - FIELDS:
            raise ValueError(f'Apparat {n:03d} : champ non autorisé.')
        if set(patch['originals']) != set(patch['changes']) | {'marginal_notes'}:
            raise ValueError(f'Apparat {n:03d} : gardes incomplètes.')
        record.update(copy.deepcopy(patch['changes']))
        validate_entries(patch['entries'], record['lines'], n)
        record['marginal_notes'] = render_notes(patch['entries'])
        record['apparat_entries'] = copy.deepcopy(patch['entries'])
        record['apparat_evidence'] = copy.deepcopy(patch['evidence'])
    for review in data['reviews']:
        record = by_num[review['scan_num']]
        if review['filename'] != record['filename']:
            raise ValueError('Apparat : photographie du contrôle divergente.')
        if review.get('controlled_lines', review.get('checked_lines')) != list(range(1, len(record['lines'])+1)):
            raise ValueError(f"Apparat {record['scan_num']:03d} : contrôle des lignes incomplet.")
        record['apparat_revision'] = copy.deepcopy(review)
    for field in ('lines', 'marginal_notes', 'apparat_entries'):
        if by_num[91][field] != by_num[93][field]:
            raise ValueError(f'Apparat : vues dupliquées 091/093 différentes ({field}).')
    return records
