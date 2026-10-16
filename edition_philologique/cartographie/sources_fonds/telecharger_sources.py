#!/usr/bin/env python3
"""Récupérer les sources des fonds dans un dossier de travail hors du dépôt.

La version Natural Earth est immuable. Les WFS IGN peuvent évoluer : les
empreintes téléchargées sont comparées à l'état du 16 octobre 2026 et consignées.
"""
from pathlib import Path
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import shutil
import urllib.request

ARCHIVE = Path(__file__).resolve().parent

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', type=Path)
    parser.add_argument('--jobs', type=int, default=4)
    args = parser.parse_args()
    dest = args.destination.resolve()
    dest.mkdir(parents=True, exist_ok=True)
    expected = json.loads((ARCHIVE / 'sources_manifest.json').read_text())
    ne = json.loads((ARCHIVE / 'natural_earth_source.json').read_text())
    jobs = [('ne_10m_admin_0_countries.geojson', ne['download_url'])]
    for request_path in sorted(ARCHIVE.glob('ign_*_request.json')):
        request = json.loads(request_path.read_text())
        name = request_path.name.replace('_request.json', '_raw.geojson')
        jobs.append((name, request['url']))
    def fetch(job):
        name, url = job
        request = urllib.request.Request(url, headers={'User-Agent':'Hippolyte-Combes-cartographie/1.0'})
        with urllib.request.urlopen(request, timeout=180) as response:
            raw = response.read()
        document = json.loads(raw)
        if document.get('type') != 'FeatureCollection':
            raise ValueError(f'{name}: réponse non GeoJSON')
        if 'numberMatched' in document and document['numberMatched'] != document.get('numberReturned'):
            raise ValueError(f'{name}: réponse WFS tronquée')
        sha = hashlib.sha256(raw).hexdigest()
        matched = sha == expected[name]['sha256']
        features = sorted(document['features'], key=lambda f: str(f.get('id',f.get('properties',{}).get('ADMIN',''))))
        canonical = json.dumps(features,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
        semantic_sha = hashlib.sha256(canonical).hexdigest()
        semantic_match = semantic_sha == expected[name]['sha256_features']
        if name == 'ne_10m_admin_0_countries.geojson' and not matched:
            raise ValueError('La source Natural Earth à révision fixe diffère de son empreinte.')
        (dest / name).write_bytes(raw)
        return {'file':name,'url':url,'sha256':sha,'bytes':len(raw),
                'identical_to_2026_10_16':matched,'sha256_features':semantic_sha,
                'features_identical_to_2026_10_16':semantic_match}
    with ThreadPoolExecutor(max_workers=max(1,min(args.jobs,8))) as pool:
        results = list(pool.map(fetch,jobs))
    (dest / 'verification_telechargement.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
    shutil.copy2(ARCHIVE / 'sources_manifest.json', dest / 'sources_manifest.json')
    for result in results:
        status = ('identique' if result['identical_to_2026_10_16'] else
                  'données identiques ; métadonnées de réponse différentes' if result['features_identical_to_2026_10_16'] else
                  'MODIFIÉE : réexamen requis avant publication')
        print(f"{result['file']}: {status}")

if __name__ == '__main__':
    main()
