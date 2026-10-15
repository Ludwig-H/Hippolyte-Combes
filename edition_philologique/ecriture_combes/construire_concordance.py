"""Index attested transcription phrases; the photographs remain the witnesses."""
import json
import re
from pathlib import Path

DOSSIER = Path(__file__).resolve().parent
BASE = DOSSIER.parent / 'relecture_integrale_2026_10/base_relecture.json'
PHRASES = {
    'lever et heures': r'\b(?:Levé|Sur pied|s/ pied)\b',
    'repos sans auxiliaire': r'\b(?:Bien reposé|Resté|Dormi|Lu et écrit|lu, et écrit)\b',
    'déplacement sans auxiliaire': r'\b(?:Venu|Allé|Quitté|Rentré|Revenus|Chevauché|Promené|Parcouru)\b',
    'comparaison météorologique': r'\b(?:Tjours|Toujours|Encore|Même|même)\b.*(?:temps|ciel|tempér|froid|pluie)',
    'longtemps ou longuement abrégés': r'\b(?:lgt|lgs|lgts|longt|longuemt)\b',
    'merveilleux et merveilleusement': r'\b(?:merv\w*|merve\w*)\b',
    'jusqu’à abrégé': r"\b(?:j[.'’-]?\s*à|ju|j-au|j-aux)\b",
    'demi et milieu': r'1/2|½',
    'comptes domestiques anglais': r'\b(?:Food|Washing|washing|cooking|darning|room|Drink|Tip)\b',
    'fourrage et déplacement anglais': r'green|forage|shifte|shifting|shifterons|railhead|refilling',
    'perception du paysage': r'\b(?:Regardé|contemplé|admiré|assis|ruminé)\b',
    'mon amie et Marguerite': r'\b(?:Margte|Mte|mon amie|ma Femme)\b',
}
records = json.loads(BASE.read_text())
result = {'status': 'Index des transcriptions de base, non validation automatique des leçons. Chaque parallèle doit être revu sur son image.', 'base': '../relecture_integrale_2026_10/base_relecture.json', 'groups': {}}
md = ['# Concordance des formes et tours de langue', '', 'Index établi sur l’état figé avant la seconde relecture. Les occurrences donnent accès aux photographies ; elles ne corroborent une lecture qu’après examen du tracé. Cet index conserve les variantes et les incertitudes de sa base.', '']
for name, pattern in PHRASES.items():
    hits = []
    for r in records:
        for n, line in enumerate(r['lines'], 1):
            if re.search(pattern, line, re.I):
                hits.append({'scan_num': r['scan_num'], 'filename': r['filename'], 'line': n, 'text': line})
    result['groups'][name] = hits
    md.extend([f'## {name.capitalize()}', '', '| Vue / ligne | Forme transcrite |', '| --- | --- |'])
    for h in hits:
        line = h['text'].replace('|', '/').replace('\\hfill', ' / ')
        md.append(f"| [{h['scan_num']:03d}, l. {h['line']}](../../scans_haute_qualite/{h['filename']}) | {line} |")
    md.append('')
(DOSSIER / 'concordance_tours.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
(DOSSIER / 'CONCORDANCE.md').write_text('\n'.join(md))
print(sum(len(h) for h in result['groups'].values()), 'occurrences indexed.')
