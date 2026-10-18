import sys,json,urllib.request,urllib.parse
UA={'User-Agent':'VeloUniverseBuilder/1.0 (avtomaster24bot-lab github)'}
def api(p):
    p.update(format='json')
    u='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(p)
    return json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA)))
for q in sys.argv[1:]:
    r=api(dict(action='query',generator='search',gsrsearch=q+' filetype:bitmap',gsrnamespace=6,gsrlimit=8,prop='imageinfo',iiprop='extmetadata|size',iiextmetadatafilter='LicenseShortName|Artist'))
    print('##',q)
    for p in sorted(r.get('query',{}).get('pages',{}).values(),key=lambda x:x.get('index',0)):
        ii=p['imageinfo'][0];m=ii.get('extmetadata',{})
        import re
        a=re.sub('<[^>]+>','',m.get('Artist',{}).get('value',''))[:40]
        print(' ',p['title'],ii['width'],'x',ii['height'],'|',m.get('LicenseShortName',{}).get('value'),'|',a)
