"""Consolidate four image-reviewed apparatus lots without rewriting older work."""
import copy
import json
from pathlib import Path
from apparat_critique import DOSSIER, MANIFEST, FIELDS, digest, validate_entries, render_notes
from parse_all_186 import build_all_186_records

LOTS = ['apparat_001_048.json', 'apparat_049_094.json', 'apparat_095_140.json', 'apparat_141_186.json']


def assemble():
    meta = json.loads((DOSSIER / 'base_manifest.json').read_text())
    if digest(DOSSIER / 'base_edition.json') != meta['base_sha256']:
        raise ValueError('Base figée de l’apparat modifiée.')
    parent = DOSSIER.parent / 'revision_2026_10/corrections_validees.json'
    if digest(parent) != meta['parent_revision_sha256']:
        raise ValueError('Révision parallèle modifiée : conciliation nécessaire avant assemblage.')
    frozen = json.loads((DOSSIER / 'base_edition.json').read_text())
    current = build_all_186_records(apply_apparatus=False)
    if current != frozen:
        raise ValueError('La construction antérieure ne reproduit plus la base figée de l’apparat.')
    witness = {r['scan_num']: r for r in frozen}
    patches, reviews, sources = {}, {}, []
    for name in LOTS:
        path = DOSSIER / name
        data = json.loads(path.read_text())
        if data['base_sha256'] != meta['base_sha256']:
            raise ValueError(f'Base divergente : {name}.')
        for component in data.get('component_files', []):
            if digest(DOSSIER / component['path']) != component['sha256']:
                raise ValueError(f"Sous-lot modifié : {component['path']}.")
        sources.append({'path': name, 'sha256': digest(path)})
        for patch in data['patches']:
            n = patch['scan_num']
            if n in patches or patch['filename'] != witness[n]['filename']:
                raise ValueError(f'Photographie dupliquée ou divergente : {n:03d}.')
            if set(patch['changes']) - FIELDS:
                raise ValueError(f'Champs non autorisés : {n:03d}.')
            if set(patch['originals']) != set(patch['changes']) | {'marginal_notes'}:
                raise ValueError(f'Gardes incomplètes : {n:03d}.')
            for field, original in patch['originals'].items():
                if original != witness[n][field]:
                    raise ValueError(f'Apparat non concilié : {n:03d}/{field}.')
            if not patch.get('evidence'):
                raise ValueError(f'Apparat {n:03d} : preuve absente.')
            lines = patch['changes'].get('lines', witness[n]['lines'])
            validate_entries(patch['entries'], lines, n)
            patches[n] = copy.deepcopy(patch)
        for review in data['reviews']:
            n = review['scan_num']
            if n in reviews or review['filename'] != witness[n]['filename']:
                raise ValueError(f'Revue dupliquée ou divergente : {n:03d}.')
            if review['review_level'] != 'apparat_integral_sur_image':
                raise ValueError(f'Revue incomplète : {n:03d}.')
            photo = DOSSIER.parent.parent / 'scans_haute_qualite' / review['filename']
            if digest(photo) != review['source_sha256']:
                raise ValueError(f'Photographie modifiée : {n:03d}.')
            reviews[n] = copy.deepcopy(review)
    if sorted(patches) != list(range(1, 187)) or sorted(reviews) != list(range(1, 187)):
        raise ValueError('La révision de l’apparat doit couvrir les 186 vues.')
    for field in ('entries',):
        if patches[91][field] != patches[93][field]:
            raise ValueError('Apparats différents sur les deux photos de la même page 091/093.')
    if patches[91]['changes'].get('lines', witness[91]['lines']) != patches[93]['changes'].get('lines', witness[93]['lines']):
        raise ValueError('Lignes différentes sur les deux photos de la même page 091/093.')
    for n, review in reviews.items():
        lines = patches[n]['changes'].get('lines', witness[n]['lines'])
        if review.get('controlled_lines', review.get('checked_lines')) != list(range(1, len(lines)+1)):
            raise ValueError(f'Contrôle des lignes incomplet : {n:03d}.')
    result = dict(meta, status='Apparat révisé intégralement sur les images ; réserves conservées.', proposal_files=sources,
                  patches=[patches[n] for n in sorted(patches)], reviews=[reviews[n] for n in sorted(reviews)])
    MANIFEST.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    md = ['# Registre de la révision intégrale de l’apparat', '',
          '| Vue | Entrées | Contrôle et réserves |', '| --- | --- | --- |']
    for n, review in sorted(reviews.items()):
        detail = review.get('observations', '')
        if isinstance(detail, list):
            detail = ' ; '.join(detail)
        detail += ' ; Réserves : ' + ' ; '.join(review.get('remaining_uncertainties', [])) if review.get('remaining_uncertainties') else ''
        detail = detail.replace('|', '/').replace('\n', ' ')
        md.append(f"| [{n:03d}](../../scans_haute_qualite/{review['filename']}) | {len(patches[n]['entries'])} | {detail} |")
    (DOSSIER / 'REGISTRE.md').write_text('\n'.join(md)+'\n')
    print(f'Apparat : 186 revues, {sum(len(p["entries"]) for p in patches.values())} entrées contrôlées.')


if __name__ == '__main__':
    assemble()
