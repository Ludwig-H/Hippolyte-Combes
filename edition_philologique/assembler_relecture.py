"""Add the second visual collation to the archived first revision, with guards."""
import copy
import hashlib
import json
from pathlib import Path

from parse_all_186 import build_all_186_records, clean_line_and_extract_note
from revision_philologique import ALLOWED_FIELDS, CORRECTIONS_PATH

EDITION = Path(__file__).resolve().parent
DOSSIER = EDITION / 'relecture_integrale_2026_10'
LOTS = ['relecture_001_048.json', 'relecture_049_094.json', 'relecture_095_140.json', 'relecture_141_186.json']


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def assemble():
    if (EDITION / 'apparat_critique_2026_10/corrections_validees.json').exists():
        raise ValueError('Une révision intégrale de l’apparat est appliquée. Utiliser assembler_apparat.py ; ne pas remplacer sa révision parente.')
    frozen = json.loads((DOSSIER / 'base_relecture.json').read_text())
    witness = {r['scan_num']: r for r in frozen}
    previous = json.loads((DOSSIER / 'base_corrections_validees.json').read_text())
    baseline = {r['scan_num']: r for r in build_all_186_records(apply_revision=False)}
    for name, expected in previous['source_modules_sha256'].items():
        if digest(EDITION / name) != expected:
            raise ValueError(f'Module modifié : {name} ; concilier ses nouvelles lectures avant assemblage.')
    # Reconstruct the first edition's allowed fields without consulting the
    # current cumulative manifest (which this script is about to replace).
    reconstructed = copy.deepcopy(baseline)
    accepted = {}
    for patch in previous['patches']:
        n = patch['scan_num']
        for field, original in patch['originals'].items():
            if reconstructed[n][field] != original:
                raise ValueError(f'Base précédente divergente : {n:03d}/{field}')
        reconstructed[n].update(copy.deepcopy(patch['changes']))
        if 'lines' in patch['changes'] and 'marginal_notes' not in patch['changes']:
            reconstructed[n]['marginal_notes'] = notes_for(reconstructed[n]['lines'])
        accepted[n] = copy.deepcopy(patch)
    for n, record in reconstructed.items():
        if n > 1:
            prefix = record['folio'].upper() + ' ('
            record['folio'] = f'Vue {n:03d}'
            if record['title'].startswith(prefix) and record['title'].endswith(')'):
                record['title'] = record['title'][len(prefix):-1]
        for field in ALLOWED_FIELDS | {'filename', 'folio'}:
            if record[field] != witness[n][field]:
                raise ValueError(f'État figé non reproductible : {n:03d}/{field}')
    sources = []
    for source in previous['proposal_files']:
        archived = DOSSIER / 'premiere_passe' / Path(source['path']).name
        if digest(archived) != source['sha256']:
            raise ValueError(f'Proposition précédente non préservée : {archived.name}')
        sources.append({'path': '../relecture_integrale_2026_10/premiere_passe/' + archived.name, 'sha256': source['sha256']})
    for target in accepted.values():
        target['proposal_sources'] = ['../relecture_integrale_2026_10/premiere_passe/' + Path(name).name for name in target.get('proposal_sources', [])]
    reviews = {}
    text_changes = []
    for filename in LOTS:
        path = DOSSIER / filename
        data = json.loads(path.read_text())
        if data.get('base_sha256') != digest(DOSSIER / 'base_relecture.json'):
            raise ValueError(f'Empreinte de la base de relecture divergente : {filename}')
        sources.append({'path': '../relecture_integrale_2026_10/' + filename, 'sha256': digest(path)})
        for patch in data['patches']:
            n = patch['scan_num']
            if patch['filename'] != witness[n]['filename']:
                raise ValueError(f'Photographie divergente : {n:03d}')
            if set(patch['originals']) != set(patch['changes']):
                raise ValueError(f'Champs sans état antérieur : {n:03d}')
            changes = copy.deepcopy(patch['changes'])
            for field, value in changes.items():
                if field not in ALLOWED_FIELDS or patch['originals'][field] != witness[n][field]:
                    raise ValueError(f'Proposition non conciliée : {n:03d}/{field}')
            if 'lines' in changes and changes['lines'] != witness[n]['lines']:
                text_changes.append(n)
                # Prevent old manually supplied notes from surviving on changed
                # lines unless the new reviewer explicitly supplied new notes.
                if 'marginal_notes' not in changes:
                    changes['marginal_notes'] = notes_for(changes['lines'])
            target = accepted.setdefault(n, {'scan_num': n, 'filename': patch['filename'], 'originals': {}, 'changes': {}, 'evidence': [], 'proposal_sources': []})
            for field, value in changes.items():
                target['originals'][field] = copy.deepcopy(baseline[n][field])
                target['changes'][field] = value
            if not patch.get('evidence'):
                raise ValueError(f'Preuve absente : {n:03d}')
            target['evidence'].extend(copy.deepcopy(patch['evidence']))
            target['proposal_sources'].append('../relecture_integrale_2026_10/' + filename)
        for review in data['reviews']:
            n = review['scan_num']
            if n in reviews or review['filename'] != witness[n]['filename']:
                raise ValueError(f'Contrôle dupliqué ou photographie divergente : {n:03d}')
            if review['review_level'] != 'collation_ligne_a_ligne':
                raise ValueError(f'Contrôle incomplet : {n:03d}')
            reviews[n] = copy.deepcopy(review)
    if sorted(reviews) != list(range(1, 187)):
        raise ValueError('La nouvelle relecture doit couvrir les 186 vues.')
    for target in accepted.values():
        target['changes'] = {k: v for k, v in target['changes'].items() if v != target['originals'][k]}
        target['originals'] = {k: v for k, v in target['originals'].items() if k in target['changes']}
    accepted = {n: p for n, p in accepted.items() if p['changes']}
    result = copy.deepcopy(previous)
    result.update({'status': 'Édition de travail après étude comparative des graphies et seconde relecture visuelle des 186 vues ; les réserves persistent là où le tracé ne permet pas de trancher.', 'relecture_base_commit': 'ec1d94ad90a7bdb250b5e074650e49312b25a2fa', 'relecture_base_sha256': digest(DOSSIER / 'base_relecture.json'), 'previous_revision_sha256': digest(DOSSIER / 'base_corrections_validees.json'), 'proposal_files': sources, 'patches': [accepted[n] for n in sorted(accepted)], 'reviews': [reviews[n] for n in sorted(reviews)], 'relecture_text_changes': sorted(set(text_changes))})
    if (DOSSIER / 'apports_concurrents.json').exists():
        result['concurrent_proposals_sha256'] = digest(DOSSIER / 'apports_concurrents.json')
    CORRECTIONS_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    md = ['# Seconde relecture des 186 photographies', '', 'Chaque photographie entière a été relue après une étude préparatoire des graphies. Les numéros identifient des vues ; ils ne restituent pas une foliation matérielle.', '', '| Vue | Photographie | Texte modifié dans cette passe | Observations et réserves |', '| --- | --- | --- | --- |']
    for n, review in sorted(reviews.items()):
        observations = review.get('observations', '')
        if isinstance(observations, list):
            observations = ' ; '.join(observations)
        points = ' ; '.join(review.get('remaining_uncertainties', []))
        detail = (str(observations) + (' ; Réserves : ' + points if points else '')).replace('|', '/').replace('\n', ' ')
        md.append(f"| {n:03d} | [{witness[n]['filename']}](../../scans_haute_qualite/{witness[n]['filename']}) | {'Oui' if n in text_changes else 'Non'} | {detail} |")
    (DOSSIER / 'REGISTRE_RELECTURE.md').write_text('\n'.join(md)+'\n')
    print(f'Seconde relecture : 186 contrôles, {len(set(text_changes))} vues avec texte modifié ; {len(accepted)} notices cumulées.')


def notes_for(lines):
    result = {}
    for index, line in enumerate(lines, 1):
        _, note = clean_line_and_extract_note(line, index)
        if note:
            result[str(index)] = note
    return result


if __name__ == '__main__':
    assemble()
