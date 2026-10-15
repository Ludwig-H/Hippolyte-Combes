"""Consolidate photographed readings; refuse an unreviewed source modification."""
import copy
import hashlib
import json
from pathlib import Path
from parse_all_186 import build_all_186_records
from revision_philologique import ALLOWED_FIELDS, REVISION_DIR


def assemble():
    baseline = {r['scan_num']: r for r in build_all_186_records(apply_revision=False)}
    witness = {r['scan_num']: r for r in json.loads((REVISION_DIR / 'base_edition_reprise.json').read_text())}
    source_hashes = json.loads((REVISION_DIR / 'base_sources_sha256.json').read_text())
    for name, expected in source_hashes.items():
        if hashlib.sha256((REVISION_DIR.parent / name).read_bytes()).hexdigest() != expected:
            raise ValueError(f'Source module changed: {name}; review its new readings before reassembling.')
    accepted, reviews, sources = {}, {}, []
    for name in ['reprise_001_031.json', 'reprise_032_062.json', 'reprise_063_124.json', 'reprise_125_186.json']:
        path = REVISION_DIR / name
        data = json.loads(path.read_text())
        sources.append({'path': name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
        for patch in data['patches']:
            n = patch['scan_num']
            assert patch['filename'] == witness[n]['filename'], (name, n, 'filename')
            target = accepted.setdefault(n, {'scan_num': n, 'filename': patch['filename'], 'originals': {}, 'changes': {}, 'evidence': [], 'proposal_sources': []})
            for field, value in patch['changes'].items():
                assert field in ALLOWED_FIELDS, (name, n, field)
                assert patch['originals'][field] == witness[n][field], (name, n, field, 'unmatched proposal original')
                target['originals'][field] = copy.deepcopy(baseline[n][field])
                target['changes'][field] = copy.deepcopy(value)
            target['evidence'].extend(copy.deepcopy(patch['evidence']))
            target['proposal_sources'].append(name)
        for review in data['reviews']:
            assert review['scan_num'] not in reviews, ('duplicate review', review['scan_num'])
            normalized = copy.deepcopy(review)
            if 'review_level' not in normalized and 'niveau' in normalized:
                normalized['review_level'] = normalized.pop('niveau')
            reviews[review['scan_num']] = normalized
    assert sorted(reviews) == list(range(1, 187)), 'Incomplete review coverage'
    assert all(r['review_level'] == 'collation_ligne_a_ligne' for r in reviews.values())
    for target in accepted.values():
        target['changes'] = {k: v for k, v in target['changes'].items() if v != target['originals'][k]}
        target['originals'] = {k: v for k, v in target['originals'].items() if k in target['changes']}
    accepted = {n: p for n, p in accepted.items() if p['changes']}
    data = {'revision_date': '2026-10-15', 'base_commit': '5cfd0f6', 'status': 'Édition de travail : collation des 186 vues et réserves explicites ; aucune certification de déchiffrement définitif.', 'proposal_files': sources, 'source_modules_sha256': source_hashes, 'patches': [accepted[n] for n in sorted(accepted)], 'reviews': [reviews[n] for n in sorted(reviews)]}
    (REVISION_DIR / 'corrections_validees.json').write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')
    md = ['# Registre de collation des 186 vues', '', 'Les fichiers sont des vues photographiques, pas une foliation matérielle. Les réserves ne constituent pas des pertes physiques du papier.', '', '| Vue | Photographie | Texte corrigé | Points ouverts |', '| --- | --- | --- | --- |']
    for n, review in sorted(reviews.items()):
        points = ' ; '.join(review.get('remaining_uncertainties', [])) or 'Aucun point particulier consigné ; ne vaut pas certitude absolue.'
        points = points.replace('|', '/').replace('\n', ' ')
        name = witness[n]['filename']
        md.append(f"| {n:03d} | [{name}](../../scans_haute_qualite/{name}) | {'Oui' if 'lines' in accepted.get(n, {}).get('changes', {}) else 'Non'} | {points} |")
    (REVISION_DIR / 'REGISTRE_COLLATION.md').write_text('\n'.join(md)+'\n')
    print(f"Consolidated {len(accepted)} notices, {sum('lines' in p['changes'] for p in accepted.values())} textual changes, 186 reviews.")


if __name__ == '__main__':
    assemble()
