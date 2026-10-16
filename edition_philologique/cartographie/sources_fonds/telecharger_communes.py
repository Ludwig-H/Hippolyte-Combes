from pathlib import Path
import requests,json,concurrent.futures
import sys
P=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parent
BBOX={'nord':[1.9,49.85,3.0,50.86],'toulouse':[1.28,43.48,1.60,43.76]}
def task(item):
 name,b=item
 params={'service':'WFS','version':'2.0.0','request':'GetFeature','typeNames':'ADMINEXPRESS-COG.2026:commune','outputFormat':'application/json','srsName':'EPSG:4326','count':5000,'CQL_FILTER':f"BBOX(geometrie,{','.join(str(v) for v in b)},'EPSG:4326')"}
 r=requests.get('https://data.geopf.fr/wfs/ows',params=params,timeout=150);r.raise_for_status();x=r.json()
 assert x['numberReturned']==x['numberMatched'],(name,x['numberReturned'],x['numberMatched'])
 (P/f'ign_communes_{name}_raw.geojson').write_bytes(r.content)
 (P/f'ign_communes_{name}_request.json').write_text(json.dumps({'url':r.url,'status':r.status_code,'bbox':b,'retrieved':'2026-10-16','numberMatched':x['numberMatched'],'numberReturned':x['numberReturned'],'source':'IGN ADMIN EXPRESS COG 2026, couche commune','licence':'Licence Ouverte / Etalab 2.0'},ensure_ascii=False,indent=2)+'\n')
 print(name,len(r.content),'bytes',x['numberReturned'],'communes')
with concurrent.futures.ThreadPoolExecutor(2) as e:list(e.map(task,BBOX.items()))
