"""Build an atlas index after checking each crop against its source pixels."""
from pathlib import Path
import hashlib
import json
from PIL import Image

DOSSIER = Path(__file__).resolve().parent
ROOT = DOSSIER.parent.parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def build():
    index=[]
    for path in sorted(DOSSIER.glob('lot_*/observations.json')):
        data=json.loads(path.read_text())
        for a in data.get('observations',data.get('examples',[])):
            box=a.get('bbox_pixels_natifs',a.get('bbox'))
            name=a.get('crop_filename',a.get('crop'))
            src=ROOT/'scans_haute_qualite'/a['filename']
            crop=path.parent/name
            original=Image.open(src)
            extract=Image.open(crop)
            assert len(box)==4 and 0<=box[0]<box[2]<=original.width and 0<=box[1]<box[3]<=original.height,(crop,box)
            expected=original.crop(box)
            assert expected.mode==extract.mode and expected.size==extract.size and expected.tobytes()==extract.tobytes(),f'Pixels divergent: {crop}'
            assert sha(src)==a['source_sha256'],f'Source modified: {src}'
            if a.get('crop_sha256'):
                assert sha(crop)==a['crop_sha256'],f'Crop modified: {crop}'
            index.append({'scan_num':a['scan_num'],'filename':a['filename'],'bbox_pixels_natifs':box,'crop':str(crop.relative_to(DOSSIER)),'source_sha256':sha(src),'crop_sha256':sha(crop),'reading':a.get('forme_lue',a.get('reading')),'comparison':a.get('comparaison',a.get('comparaisons',a.get('observation',''))),'limits':a.get('limites',a.get('prudence','Voir la réserve de lecture dans la forme et la notice.'))})
    result={'method':'Rectangles découpés dans les JPEG décodés, sans redimensionnement, contraste ni retouche. Égalité exacte des pixels contrôlée. Le contrôle matériel ne certifie pas les lectures.','examples':index}
    (DOSSIER/'index_extraits.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    md=['# Index des extraits photographiques','','Les coordonnées en pixels natifs et les empreintes sont conservées dans [index_extraits.json](index_extraits.json). Chaque PNG est identique au rectangle découpé dans le JPEG source décodé. Les lectures proposées gardent les réserves de leur notice.','','| Vue | Extrait | Forme proposée |','| --- | --- | --- |']
    for a in index:
        text=a['reading'].replace('|','/').replace('\n',' ')
        md.append(f"| [{a['scan_num']:03d}](../../scans_haute_qualite/{a['filename']}) | [PNG natif]({a['crop']}) | {text} |")
    (DOSSIER/'INDEX.md').write_text('\n'.join(md)+'\n')
    print(len(index),'extraits vérifiés pixel par pixel,',len(set(a['scan_num'] for a in index)),'photographies sources.')

if __name__=='__main__':
    build()
