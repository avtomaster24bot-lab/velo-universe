import json,urllib.request,urllib.parse,re,io,os,time
from PIL import Image
UA={'User-Agent':'VeloUniverseBuilder/1.0 (avtomaster24bot-lab github)'}
IM={
'draisine':"Draisine or Laufmaschine, c. 1820 - Kurpfälzisches Museum der Stadt Heidelberg - Heidelberg, Germany - DSC01526.jpg",
'draisine-1817':"Draisine1817.jpg",
'michaux':"Velocipede Michaux-4.jpg",
'penny':"Ariel 50 inch High Wheel Bike.jpg",
'rover':"Rover safety bicycle of 1885 (left cropped).jpg",
'rover-ad':"1885 Rover bicycle advertisement.jpg",
'safety-1890':"Safety Bicycle ca. 1890.jpg",
'dunlop':"Dunlop first pneumatic bicycle tyre.JPG",
'moulton':"1965 moulton drive side bootiebike.jpg",
'mtb':"Full suspension mountain bike.jpg",
'road':"Rennrad Racing Bicycle noBG.jpg",
'bmx':"Freestyle BMX bike 2019-04-05 (1).jpg",
'brompton-folded':"Brompton bicycle folded.jpg",
'brompton':"Brompton, Velo 24, Berlin (VB243556).jpg",
'gravel':"Crow, Velo 24, Berlin (VB243505).jpg",
'city':"Vélo Hollandais classique.jpg",
'ebike':"Cowboy 3 pedelec.jpg",
'fatbike':"Fatbike in Ukraine 01.jpg",
'tandem':"Tandem bicycle red.jpg",
'cargo':"Bakfiets in De Hoge Veluwe — 2024-07-09 16.05.29.jpg",
'track':"Blue fixed-gear (track) bicycle locked up.JPG",
'lefty':"Cannondale Lefty Fork.jpg",
'nexus7':"Shimano Nexus Inter 7 hub gear.jpg",
'nexus3-clickbox':"Shimano Nexus 3 bell crank clickbox.jpg",
'rear-derailleur':"SRAM Rival rear derailleur - topview.jpg",
'hanger':"Mounted derailleur hanger.jpg",
'disc-brake':"Bike disc break disc pads and caliper.jpg",
'crankset':"Bicycle crankset Shimano 105 R7000 (chainring 50-34, length 172.5mm, 11 speed).jpg",
'headset-exploded':"Bicycle headset (threadless) exploded view-en.png",
'valves':"Air inlet valve on bike schrader and presta.jpg",
'chain-tool':"Disassembling a bicycle chain with a chain tool.JPG",
'tire-levers':"TyreLevers.jpg",
'spoke-wrench':"Spoke wrench in use.jpg",
'truing-stand':"Bicycle wheel on a truing stand.jpg",
'crank-puller':"Crank pullers (crank extractors, crank removal tools) for sqare taper bottom brackets.jpg",
'hex-keys':"Folding Allen key set, unfolded.jpg",
'cone-wrenches':"Bicycle cone wrenches at Somerville Bike Kitchen.jpg",
'park-tools':"Park Tools.jpg",
'workshop':"Ben's Bikes, Namibia (10677004674).jpg",
}
os.makedirs('site/img/photos',exist_ok=True)
credits=json.load(open('content/credits.json')) if os.path.exists('content/credits.json') else {}
import sys
if len(sys.argv)>1: IM=json.load(open(sys.argv[1]))
IM={k:v for k,v in IM.items() if k not in credits}
def clean(s): return re.sub(r'\s+',' ',re.sub('<[^>]+>','',s or '')).strip()
for k,t in IM.items():
    u='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(dict(action='query',titles='File:'+t,prop='imageinfo',iiprop='url|extmetadata',iiurlwidth=1200,format='json'))
    p=list(json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA)))['query']['pages'].values())[0]
    if 'imageinfo' not in p: print('MISSING',k,t);continue
    ii=p['imageinfo'][0];m=ii['extmetadata']
    g=lambda x:clean(m.get(x,{}).get('value',''))
    lic=g('LicenseShortName')
    if any(b in lic for b in ['GFDL','FAL','Fair']): print('SKIP lic',k,lic);continue
    data=urllib.request.urlopen(urllib.request.Request(ii.get('thumburl') or ii['url'],headers=UA)).read()
    im=Image.open(io.BytesIO(data));im=im.convert('RGBA' if im.mode in('RGBA','LA','P') else 'RGB')
    im.thumbnail((1200,1200))
    im.save(f'site/img/photos/{k}.webp','WEBP',quality=78)
    credits[k]=dict(file=t,author=g('Artist')[:200] or 'Unknown',license=lic,license_url=g('LicenseUrl'),source=ii['descriptionurl'],w=im.width,h=im.height,desc=g('ImageDescription')[:300])
    print(k,lic,im.size,len(data)//1024,'KB');time.sleep(0.3)
json.dump(credits,open('content/credits.json','w'),ensure_ascii=False,indent=1)
