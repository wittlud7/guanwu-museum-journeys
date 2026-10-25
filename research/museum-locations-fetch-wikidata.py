import urllib.request,urllib.parse,json
from pathlib import Path
r=json.loads(Path('research/museum-locations-wikipedia-items.json').read_text(encoding='utf8'));ids=[x.get('pageprops',{}).get('wikibase_item') for x in r['query']['pages'].values()];ids=[x for x in ids if x]
p={'action':'wbgetentities','ids':'|'.join(ids),'props':'labels|claims|descriptions','languages':'zh|en','format':'json'};u='https://www.wikidata.org/w/api.php?'+urllib.parse.urlencode(p)
d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'GuanwuMuseumGuide/3.0 educational guide'}),timeout=30));Path('research/museum-locations-wikidata.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
for q,v in d['entities'].items():
 coords=[c.get('mainsnak',{}).get('datavalue',{}).get('value') for c in v.get('claims',{}).get('P625',[])];print(q,v.get('labels',{}).get('zh',v.get('labels',{}).get('en',{})).get('value'),coords)
