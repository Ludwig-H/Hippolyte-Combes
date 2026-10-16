#!/usr/bin/env python3
"""Préparer des fonds cartographiques : découpage réel, simplification métrique.
Exécuter avec shapely et pyproj. Les fichiers *_raw.geojson sont les réponses IGN
WFS archivées ; les requêtes exactes sont dans *_request.json.
"""
from pathlib import Path
import json, hashlib
from shapely.geometry import shape, mapping, box
from shapely.ops import transform, unary_union, linemerge
from pyproj import Transformer
import sys
P=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parent
TO=Transformer.from_crs(4326,2154,always_xy=True).transform
FROM=Transformer.from_crs(2154,4326,always_xy=True).transform

def load(n): return json.loads((P/n).read_text())
def round_coords(x):
    if isinstance(x,float): return round(x,6)
    if isinstance(x,(list,tuple)): return [round_coords(y) for y in x]
    if isinstance(x,dict): return {k:round_coords(v) for k,v in x.items()}
    return x

def write(n,features,source,bounds,tol):
    doc={'type':'FeatureCollection','name':n,'crs':{'type':'name','properties':{'name':'urn:ogc:def:crs:OGC:1.3:CRS84'}},'source':source,'downloaded':'2026-10-16','processing':{'bbox_lon_lat':bounds,'simplification_tolerance_metres':tol,'projection_for_simplification':'EPSG:2154','historical_status':'Repères géographiques contemporains, non une reconstitution des tracés de 1916–1917.'},'features':features}
    (P/n).write_text(json.dumps(round_coords(doc),ensure_ascii=False,separators=(',',':'))+'\n')
    print(n,len(features),'features',len((P/n).read_bytes()),'bytes')

def simplify_clip(g,bounds,tol):
    g=g.intersection(box(*bounds))
    if g.is_empty:return g
    return transform(FROM,transform(TO,g).simplify(tol,preserve_topology=True))

b=[-15,39,20,57];fs=[]
for f in load('ne_10m_admin_0_countries.geojson')['features']:
    g=simplify_clip(shape(f['geometry']),b,100)
    if g.is_empty:continue
    p=f['properties'];fs.append({'type':'Feature','properties':{'name':p['NAME_FR'],'admin':p['ADMIN'],'iso3':p['ADM0_A3'],'source':'Natural Earth 1:10m, Admin 0 countries'},'geometry':mapping(g)})
write('europe_countries.geojson',fs,'Natural Earth 1:10m, domaine public ; https://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-admin-0-countries/',b,100)

nord={
    'Lys':{'la Lys','Rivière la Lys','Cunette ou Lys'},
    'Ternoise':{'Ternoise','Rivière la Ternoise'},
    'Authie':{'Authie',"Fleuve l'Authie"},
    'Ancre':{'Ancre',"Rivière l'Ancre"},
    'Hallue':{"Rivière l'Hallue","Rivière d'Hallue"},
    'Somme':{'la Somme Rivière','Fleuve la Somme','la Somme Canalisée'},
}
toulouse={
    'Garonne':{'la Garonne','Bras Inférieur Garonne'},
    'Canal du Midi':{'Canal du Midi'},
    'Canal de Brienne':{'Canal de Brienne'},
    'Canal latéral à la Garonne':{'Canal Latéral à la Garonne'},
    'Touch':{'le Touch'},
}
for region,groups,b in [('nord',nord,[1.4,49.7,3.3,51.2]),('toulouse',toulouse,[1.2,43.4,1.7,43.8])]:
    source=load(f'ign_{region}_raw.geojson')['features'];fs=[]
    for name,names in groups.items():
        selected=[f for f in source if f['properties']['toponyme'] in names]
        assert selected,name
        geoms=[shape(f['geometry']) for f in selected]
        g=simplify_clip(unary_union(geoms),b,10)
        if g.is_empty:continue
        fs.append({'type':'Feature','properties':{'name':name,'source':'IGN BD TOPO V3, couche cours_d_eau','raw_names':sorted({f['properties']['toponyme'] for f in selected}),'source_ids':[f['properties']['cleabs'] for f in selected],'hydrographic_codes':[f['properties']['code_hydrographique'] for f in selected]},'geometry':mapping(g)})
    write(f'hydro_{region}.geojson',fs,'IGN BD TOPO V3, WFS data.geopf.fr, Licence Ouverte / Etalab 2.0',b,10)

b=[2.4,50.5,3.3,50.95]
f=load('ign_hauts_de_france_raw.geojson')['features'][0]
g=simplify_clip(shape(f['geometry']).boundary,b,10)
write('frontiere_franco_belge_lys.geojson',[{'type':'Feature','properties':{'name':'Frontière franco-belge — secteur de la Lys','source':'IGN ADMIN EXPRESS COG 2026, limite de la région Hauts-de-France','source_id':f['properties']['cleabs'],'restriction':'Emprise choisie sans côte ni frontière interrégionale ; ne pas extrapoler hors de cette emprise.'},'geometry':mapping(g)}],'IGN ADMIN EXPRESS COG 2026, WFS data.geopf.fr, Licence Ouverte / Etalab 2.0',b,10)

outputs=['europe_countries.geojson','hydro_nord.geojson','hydro_toulouse.geojson','frontiere_franco_belge_lys.geojson']
manifest=json.loads((P/'manifest.json').read_text()) if (P/'manifest.json').exists() else {}
manifest.update({name:{'sha256':hashlib.sha256((P/name).read_bytes()).hexdigest(),'bytes':(P/name).stat().st_size} for name in outputs})
(P/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
