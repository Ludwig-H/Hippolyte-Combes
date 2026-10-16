from pathlib import Path
import json,hashlib
import numpy as np
import shapely
from shapely.geometry import shape,mapping,box
from shapely.ops import transform
from pyproj import Transformer
import sys
P=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parent
BBOX={'nord':[1.9,49.85,3.0,50.86],'toulouse':[1.28,43.48,1.60,43.76]}
TO=Transformer.from_crs(4326,2154,always_xy=True).transform
BACK=Transformer.from_crs(2154,4326,always_xy=True).transform

def rounded(x):
 if isinstance(x,float):return round(x,6)
 if isinstance(x,(tuple,list)):return [rounded(z) for z in x]
 if isinstance(x,dict):return {k:rounded(v) for k,v in x.items()}
 return x

for region,b in BBOX.items():
 raw=json.loads((P/f'ign_communes_{region}_raw.geojson').read_text())
 records=[];polys=[]
 for f in raw['features']:
  g=shape(f['geometry']).intersection(box(*b))
  if g.is_empty:continue
  if g.geom_type not in ('Polygon','MultiPolygon'):continue
  g=transform(TO,g)
  assert g.is_valid
  if g.area<100:continue
  polys.append(g);records.append(f)
 arr=np.array(polys,dtype=object)
 valid_coverage=bool(shapely.coverage_is_valid(arr))
 if valid_coverage:
  simplified=shapely.coverage_simplify(arr,tolerance=50,simplify_boundary=False)
  method='shapely.coverage_simplify, limites partagées cohérentes, tolérance 50 m, contour extérieur préservé'
 else:
  simplified=np.array([g.simplify(50,preserve_topology=True) for g in arr],dtype=object)
  method='Douglas-Peucker 50 m avec conservation topologique de chaque polygone'
 features=[]
 for f,g in zip(records,simplified):
  assert g.is_valid and not g.is_empty
  p=f['properties']
  features.append({'type':'Feature','properties':{'name':p['nom_officiel'],'code_insee':p['code_insee'],'source_id':p['cleabs'],'source':'IGN ADMIN EXPRESS COG 2026, commune'},'geometry':mapping(transform(BACK,g))})
 doc={'type':'FeatureCollection','name':f'communes_{region}','crs':{'type':'name','properties':{'name':'urn:ogc:def:crs:OGC:1.3:CRS84'}},'source':'IGN ADMIN EXPRESS COG 2026, couche commune, https://data.geopf.fr/wfs/ows','licence':'Licence Ouverte / Etalab 2.0','extraction_date':'2026-10-16','processing':{'bbox_lon_lat':b,'method':method,'projection_for_simplification':'EPSG:2154','raw_coverage_valid':valid_coverage,'excluded_slivers_smaller_than_square_metres':100,'historical_status':'Limites communales contemporaines, fond de repérage géographique et non reconstitution administrative de 1916–1917.'},'features':features}
 out=P/f'communes_{region}.geojson';out.write_text(json.dumps(rounded(doc),ensure_ascii=False,separators=(',',':'))+'\n')
 print(region,len(features),out.stat().st_size,'bytes',valid_coverage,method)
man=json.loads((P/'manifest.json').read_text());src=json.loads((P/'sources_manifest.json').read_text())
for region in BBOX:
 for dic,name in [(man,f'communes_{region}.geojson'),(src,f'ign_communes_{region}_raw.geojson')]:dic[name]={'sha256':hashlib.sha256((P/name).read_bytes()).hexdigest(),'bytes':(P/name).stat().st_size}
(P/'manifest.json').write_text(json.dumps(man,ensure_ascii=False,indent=2)+'\n');(P/'sources_manifest.json').write_text(json.dumps(src,ensure_ascii=False,indent=2)+'\n')
