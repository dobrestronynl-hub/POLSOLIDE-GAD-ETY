import os, sys, json, math, subprocess, concurrent.futures, zipfile, xml.etree.ElementTree as ET, csv, shutil, textwrap
from pathlib import Path
import numpy as np
import trimesh

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'kolekcja-20-serie8h'
SCAD=OUT/'src'; STL=OUT/'stl'; MF=OUT/'3mf'; PREV=OUT/'previews'
for d in (SCAD,STL,MF,PREV):d.mkdir(parents=True,exist_ok=True)
# id, slug, title, form, bounding width height, thickness, intended use, finish, retail estimate euro, min series
P=[
('01','brelok-domek','Brelok „Domek”','house',48,43,3.0,'Klucze do lokali i przekazanie mieszkań','Bez montażu (kółko opcjonalne)',3.9,30),
('02','brelok-klucz','Brelok „Klucz”','key',64,28,3.0,'Upominek przy przekazaniu kluczy','Bez montażu (kółko opcjonalne)',4.5,25),
('03','brelok-tarcza','Brelok „Tarcza”','shield',43,46,3.0,'Brelok dla obsługi i partnerów','Bez montażu (kółko opcjonalne)',4.2,30),
('04','brelok-owal','Brelok „Owal”','oval',56,31,3.0,'Identyfikator kompletu kluczy','Bez montażu (kółko opcjonalne)',3.7,30),
('05','zeton-okragly','Żeton okrągły','coin',35,35,2.6,'Mały firmowy żeton lub znacznik','Bez montażu',2.9,50),
('06','zeton-szesciokat','Żeton sześciokątny','hex',38,34,2.6,'Numerator, pamiątka lub znacznik','Bez montażu',3.1,40),
('07','numer-kluczy','Numerator kluczy','tag',48,30,3.0,'Klucze do mieszkań i skrzynek','Bez montażu (kółko opcjonalne)',3.6,40),
('08','identyfikator-gosc','Identyfikator GOŚĆ','rounded',62,29,2.8,'Obsługa mieszkań na wynajem','Bez montażu (klips opcjonalny)',4.2,30),
('09','identyfikator-serwis','Identyfikator SERWIS','tag',60,31,2.8,'Technicy i obsługa techniczna','Bez montażu (kółko opcjonalne)',4.3,30),
('10','zawieszka-bagaz','Zawieszka bagażowa','luggage',68,39,3.0,'Przekazania i pobyty pracowników','Bez montażu (pasek opcjonalny)',4.7,24),
('11','numer-szafki','Numer szafki','rounded',46,34,2.8,'Szafki pracownicze i techniczne','Bez montażu',3.5,40),
('12','tabliczka-lokalu','Tabliczka lokalu','arch',68,42,2.8,'Numeracja lokali, drzwi i pomieszczeń','Montaż taśmą dwustronną',5.9,20),
('13','oznaczenie-parking','Oznaczenie PARKING','rounded',66,35,2.8,'Miejsca parkingowe i identyfikacja','Montaż taśmą dwustronną',5.5,25),
('14','oznaczenie-magazyn','Oznaczenie MAGAZYN','tag',65,35,2.8,'Strefy składowania i organizacja','Montaż taśmą dwustronną',5.3,25),
('15','etykieta-skrzynka','Etykieta skrzynki','plaque',64,26,2.6,'Skrzynki pocztowe i schowki','Montaż taśmą dwustronną',4.1,30),
('16','plakietka-partner','Plakietka PARTNER','shield',49,49,3.0,'Gadżet dla partnerów B2B','Bez montażu',4.6,30),
('17','plakietka-dach','Plakietka „Dach”','house',55,47,2.8,'Mini prezent i oznaczenie firmy','Bez montażu',4.3,25),
('18','minimagnes-domek','Minimagnes „Domek”','house',48,43,3.5,'Magnes na lodówkę ze znakiem domu','Wkleić magnes 10×2 mm',5.9,25),
('19','minimagnes-owal','Minimagnes „Owal”','oval',55,34,3.5,'Upominek promocyjny','Wkleić magnes 10×2 mm',5.9,25),
('20','karta-wizytowka','Mini karta POLSOLIDE','plaque',69,39,2.8,'Wizytówka 3D do zestawu powitalnego','Bez montażu',5.5,25),
]

# SCAD templates are self-contained, parametric and are fully editable.
TEMPLATE=r'''// POLSOLIDE — __TITLE__
// Materiały: base=czarny (#18181B); red=czerwony (#B7131C); white=biały (#F1F0EC).
// Zapisz do STL: openscad -o element.stl -D 'part="base"' tenplik.scad
// Model na płasko: wszystkie barwy zmieniają się tylko na samym końcu druku.
$fn=40;
part="all"; // all, base, red, white
W=__W__; H=__H__; T=__T__; kind="__KIND__";
RH=0.48; WH=0.40; // wysokość czerwonego i białego detalowania
magnet=__MAGNET__;
label="__LABEL__"; // zmień np. numer lokalu, oznaczenie stanowiska lub pomieszczenia

module rr(w,h,r){offset(r=r) square([max(0.1,w-2*r),max(0.1,h-2*r)],center=true);}
module outline(){
 if(kind=="house")polygon(points=[[-W/2,-H/2],[W/2,-H/2],[W/2,H*.13],[0,H/2],[-W/2,H*.13]]);
 else if(kind=="shield")polygon(points=[[-W*.46,H*.48],[W*.46,H*.48],[W*.49,-H*.05],[W*.25,-H*.32],[0,-H*.49],[-W*.25,-H*.32],[-W*.49,-H*.05]]);
 else if(kind=="hex")polygon(points=[[-W*.35,-H/2],[W*.35,-H/2],[W/2,0],[W*.35,H/2],[-W*.35,H/2],[-W/2,0]]);
 else if(kind=="oval")scale([W/2,H/2])circle(r=1,$fn=60);
 else if(kind=="coin")circle(d=W,$fn=72);
 else if(kind=="plaque")rr(W,H,3.0);
 else if(kind=="luggage")rr(W,H,6.5);
 else if(kind=="arch")union(){translate([0,-H*.10])rr(W,H*.8,5);translate([0,H*.14])scale([W/2,H*.37])circle(r=1,$fn=48);}
 else if(kind=="key") union(){translate([-W*.3,0])circle(d=H,$fn=48);translate([W*.08,-H*.16])square([W*.68,H*.32],center=true);translate([W*.31,-H*.27])square([W*.11,H*.20],center=true);translate([W*.42,-H*.27])square([W*.09,H*.20],center=true);}
 else if(kind=="tag")union(){rr(W-7,H,5);translate([-W/2+5,0])circle(d=H*.78,$fn=48);}
 else rr(W,H,5);
}
module hole2d(){
 if(kind=="house")translate([0,H*.29])circle(d=4.6,$fn=40);
 else if(kind=="shield")translate([0,H*.34])circle(d=4.6,$fn=40);
 else if(kind=="key")translate([-W*.3,0])circle(d=4.6,$fn=40);
 else if(kind=="oval" && !magnet)translate([-W*.34,0])circle(d=4.6,$fn=40);
 else if(kind=="tag")translate([-W*.36,0])circle(d=4.6,$fn=40);
 else if(kind=="luggage")translate([-W*.40,0])circle(d=5,$fn=40);
}
module footprint(){difference(){outline(); if(!magnet)hole2d();}}
// W małych produktach monogram PS jest większy i czytelniejszy przy dyszy 0.4 mm.
small=(W<=50 || kind=="coin" || kind=="hex");
bw= min(W*.76,64);
bh=(label=="")?(small?13:15):20;
// dla breloka w kształcie klucza środek znaku przesunięto od oczka
badgeX=(kind=="key")?W*.13:(kind=="oval"&&!magnet?W*.055:(kind=="tag"?W*.07:(kind=="luggage"?W*.03:0)));
badgeY=(kind=="house" || kind=="shield")?-H*.10:0;
module brand_patch(){translate([badgeX,badgeY])rr(bw,bh,2.2);}
module base_black(){difference(){linear_extrude(height=T,convexity=8)footprint();
 if(magnet)translate([0,0,-0.02])cylinder(h=2.14,d=10.35,$fn=48);
}}
module red_cap(){translate([0,0,T])linear_extrude(height=RH)intersection(){offset(delta=-.55)footprint();brand_patch();}}
module white_brand(){
 translate([badgeX,badgeY,T+RH])linear_extrude(height=WH)
 if(label!="") {
   translate([0,3.8])text("POLSOLIDE",font="DejaVu Sans:style=Bold",size=min(4.0,bw*.087),halign="center",valign="center");
   translate([0,-4.0])text(label,font="DejaVu Sans:style=Bold",size=min(6.4,bw/(max(2,len(label))*0.75)),halign="center",valign="center");
 }
 else if(small) text("PS",font="DejaVu Sans:style=Bold",size=8.3,halign="center",valign="center");
 else text("POLSOLIDE",font="DejaVu Sans:style=Bold",size=min(6.4,bw*.127),halign="center",valign="center");
}
if(part=="all"||part=="base")color([.094,.094,.106])base_black();
if(part=="all"||part=="red")color([.718,.075,.11])red_cap();
if(part=="all"||part=="white")color([.945,.941,.925])white_brand();
'''
# patch: locate centered text within red emblem in smaller narrow models

def slugfile(row):return row[0]+'_'+row[1]
for row in P:
    idx,slug,title,kind,w,h,t,purpose,finish,price,minimum=row
    labels={'07':'01','08':'GOŚĆ','09':'SERWIS','10':'BAG','11':'01','12':'A1','13':'PARKING','14':'MAGAZYN','15':'12B','16':'PARTNER','20':'WELCOME'}
    src=TEMPLATE.replace('__TITLE__',title).replace('__W__',str(w)).replace('__H__',str(h)).replace('__T__',str(t)).replace('__KIND__',kind).replace('__MAGNET__','true' if 'magnes' in slug else 'false').replace('__LABEL__',labels.get(idx,''))
    (SCAD/(slugfile(row)+'.scad')).write_text(src,encoding='utf-8')

def render_job(row,kind):
    item=slugfile(row); dest=STL/f'{item}_{kind}.stl'; src=SCAD/(item+'.scad')
    cmd=['openscad','-o',str(dest),'--export-format','binstl','-D',f'part="{kind}"',str(src)]
    p=subprocess.run(cmd,capture_output=True,text=True,timeout=90)
    if p.returncode or not dest.exists() or dest.stat().st_size<100: raise RuntimeError(f'{item}/{kind}\n'+p.stderr[-1800:])
    return str(dest)
if '--render' in sys.argv:
    jobs=[(row,kind) for row in P for kind in ['base','red','white']]
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        for i,result in enumerate(pool.map(lambda j: render_job(*j),jobs),1):
            if i%10==0: print('exported',i,'/',len(jobs),flush=True)

# 3mf, individual colored objects composite and plate with repeated composites.
def plate_positions(w,h):
    dx=w+4.5;dy=h+4.5;positions=[]
    # 8 mm edge margins on a 256 mm bed; bottom-left area left for purge tower
    for row in range(math.floor(232/dy)):
        for col in range(math.floor(232/dx)):
            x=8+(col+.5)*dx;y=8+(row+.5)*dy
            if x-w/2<58 and y-h/2<58:
                continue
            positions.append((x,y))
    return positions
CORE='http://schemas.microsoft.com/3dmanufacturing/core/2015/02'
CT='http://schemas.openxmlformats.org/package/2006/content-types'
REL='http://schemas.openxmlformats.org/package/2006/relationships'

def m3mf(row, qty=1, plate=False):
    idx,slug,title,kind,w,h,t,purpose,finish,price,minn=row
    name=slugfile(row); obj=[]
    scene=ET.Element('model',{'unit':'millimeter','xml:lang':'pl-PL','xmlns':CORE})
    res=ET.SubElement(scene,'resources')
    mats=ET.SubElement(res,'basematerials',{'id':'1'})
    for c,title in [('#18181BFF','czarny'),('#B7131CFF','czerwony'),('#F1F0ECFF','biały')]:ET.SubElement(mats,'base',{'name':title,'displaycolor':c})
    totalvol=0
    for i,part in enumerate(['base','red','white']):
        mesh=trimesh.load_mesh(STL/(name+'_'+part+'.stl'),process=True)
        if not mesh.is_volume: print('WARNING nonvolume',name,part,mesh.is_watertight)
        totalvol+=max(0,mesh.volume)
        o=ET.SubElement(res,'object',{'id':str(10+i),'type':'model','name':name+'_'+part,'pid':'1','pindex':str(i)})
        me=ET.SubElement(o,'mesh'); vertices=ET.SubElement(me,'vertices')
        for x,y,z in mesh.vertices:ET.SubElement(vertices,'vertex',{'x':f'{x:.5f}','y':f'{y:.5f}','z':f'{z:.5f}'})
        tri=ET.SubElement(me,'triangles')
        for x,y,z in mesh.faces:ET.SubElement(tri,'triangle',{'v1':str(x),'v2':str(y),'v3':str(z)})
    comp=ET.SubElement(res,'object',{'id':'20','type':'model','name':name})
    comps=ET.SubElement(comp,'components')
    for i in range(3):ET.SubElement(comps,'component',{'objectid':str(10+i)})
    build=ET.SubElement(scene,'build')
    if plate:
        # compact 236mm printable area, avoids outer margins and leaves modest clearance
        positions=plate_positions(w,h)
        for x,y in positions[:qty]:
            ET.SubElement(build,'item',{'objectid':'20','transform':f'1 0 0 0 1 0 0 0 1 {x:.3f} {y:.3f} 0'})
    else:ET.SubElement(build,'item',{'objectid':'20'})
    data=ET.tostring(scene,encoding='utf-8',xml_declaration=True)
    content=ET.Element('Types',{'xmlns':CT});ET.SubElement(content,'Default',{'Extension':'rels','ContentType':'application/vnd.openxmlformats-package.relationships+xml'});ET.SubElement(content,'Default',{'Extension':'model','ContentType':'application/vnd.ms-package.3dmanufacturing-3dmodel+xml'})
    rel=ET.Element('Relationships',{'xmlns':REL});ET.SubElement(rel,'Relationship',{'Target':'/3D/3dmodel.model','Id':'rel0','Type':'http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel'})
    filename=MF/(name+('_plyta' if plate else '')+'.3mf')
    with zipfile.ZipFile(filename,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        z.writestr('[Content_Types].xml',ET.tostring(content,encoding='utf-8',xml_declaration=True))
        z.writestr('_rels/.rels',ET.tostring(rel,encoding='utf-8',xml_declaration=True))
        z.writestr('3D/3dmodel.model',data)
    return totalvol

# Svg previews are vector-based sketches of silhouette and color geometry; 3d details represented with subtle shadows.
def svgpath(kind,w,h):
    if kind=='house':return f'M {-w/2} {h/2} L {w/2} {h/2} L {w/2} {-h*.13} L 0 {-h/2} L {-w/2} {-h*.13} Z'
    if kind=='shield':return f'M {-w*.46} {-h*.48} L {w*.46} {-h*.48} L {w*.49} {h*.05} L {w*.25} {h*.32} L 0 {h*.49} L {-w*.25} {h*.32} L {-w*.49} {h*.05} Z'
    if kind=='hex':return f'M {-w*.35} {h/2} L {w*.35} {h/2} L {w/2} 0 L {w*.35} {-h/2} L {-w*.35} {-h/2} L {-w/2} 0 Z'
    if kind=='key':return f'M {-w*.19} {-h*.17} L {w*.46} {-h*.17} L {w*.46} {h*.25} L {w*.30} {h*.25} L {w*.30} {h*.16} L {w*.20} {h*.16} L {w*.20} {h*.17} L {-w*.19} {h*.17} Z'
    return ''

def svg_preview(row):
    idx,slug,title,kind,w,h,t,purpose,finish,price,m=row
    name=slugfile(row);W,H=w,h;is_small=w<=50 or kind in ('coin','hex')
    dx=320/W; dy=225/H; scale=min(dx,dy)
    labels={'07':'01','08':'GOŚĆ','09':'SERWIS','10':'BAG','11':'01','12':'A1','13':'PARKING','14':'MAGAZYN','15':'12B','16':'PARTNER','20':'WELCOME'}
    label=labels.get(idx,'')
    bw=min(w*.76,64); bh=20 if label else (13 if is_small else 15)
    bx=w*.13 if kind=='key' else (w*.055 if kind=='oval' and 'magnes' not in slug else (w*.07 if kind=='tag' else (w*.03 if kind=='luggage' else 0)))
    by=-h*.10 if kind in ('house','shield') else 0
    trans=f'translate(200 146) scale({scale:.4f})'
    if kind in ('coin','oval'):
        body=f'<ellipse cx="0" cy="0" rx="{w/2}" ry="{h/2}" fill="#18181B"/>'
    elif kind=='key':
        body=f'<circle cx="{-w*.3}" cy="0" r="{h/2}" fill="#18181B"/><path d="{svgpath(kind,w,h)}" fill="#18181B"/>'
    elif kind=='tag':
        body=f'<rect x="{-w/2+3.5}" y="{-h/2}" width="{w-7}" height="{h}" rx="5" fill="#18181B"/><circle cx="{-w/2+5}" r="{h*.39}" fill="#18181B"/>'
    elif kind=='arch':
        body=f'<rect x="{-w/2}" y="{-h*.36}" width="{w}" height="{h*.8}" rx="6" fill="#18181B"/><ellipse cx="0" cy="{-h*.14}" rx="{w/2}" ry="{h*.37}" fill="#18181B"/>'
    elif kind in ('house','hex','shield'):
        body=f'<path d="{svgpath(kind,w,h)}" fill="#18181B"/>'
    else:
        body=f'<rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" rx="{5 if kind != "plaque" else 3}" fill="#18181B"/>'
    hole=''
    if kind=='house' and 'magnes' not in slug: hole=f'<circle cx="0" cy="{-h*.29}" r="2.3" fill="#e2e2e5"/>'
    elif kind=='shield':hole=f'<circle cx="0" cy="{-h*.34}" r="2.3" fill="#e2e2e5"/>'
    elif kind=='key':hole=f'<circle cx="{-w*.3}" cy="0" r="2.3" fill="#e2e2e5"/>'
    elif kind=='tag':hole=f'<circle cx="{-w*.36}" cy="0" r="2.3" fill="#e2e2e5"/>'
    elif kind=='luggage':hole=f'<circle cx="{-w*.40}" cy="0" r="2.5" fill="#e2e2e5"/>'
    elif kind=='oval' and 'magnes' not in slug:hole=f'<circle cx="{-w*.34}" cy="0" r="2.3" fill="#e2e2e5"/>'
    word='PS' if is_small else 'POLSOLIDE'; fs=8.3 if is_small else min(6.4,bw*.127)
    if label:
        txt=f'<text x="{bx}" y="{by-3.8:.2f}" dominant-baseline="middle" fill="#F1F0EC" text-anchor="middle" font-family="DejaVu Sans,sans-serif" font-size="{min(4.0,bw*.087):.2f}" font-weight="bold">POLSOLIDE</text><text x="{bx}" y="{by+4:.2f}" dominant-baseline="middle" fill="#F1F0EC" text-anchor="middle" font-family="DejaVu Sans,sans-serif" font-size="{min(6.4,bw/(max(2,len(label))*.75)):.2f}" font-weight="bold">{label}</text>'
    else:
        txt=f'<text x="{bx}" y="{by+.10:.2f}" dominant-baseline="middle" fill="#F1F0EC" text-anchor="middle" font-family="DejaVu Sans,sans-serif" font-size="{fs:.2f}" font-weight="bold">{word}</text>'
    mark=f'<rect x="{bx-bw/2:.2f}" y="{by-bh/2:.2f}" width="{bw:.2f}" height="{bh:.2f}" rx="2.2" fill="#B7131C"/>'+txt
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 320" role="img" aria-label="{title}: projekt 3D POLSOLIDE">
<defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#fafafa"/><stop offset="1" stop-color="#e9e9ec"/></linearGradient><filter id="shadow"><feGaussianBlur stdDeviation="8"/></filter></defs>
<rect width="400" height="320" fill="url(#bg)"/><ellipse cx="200" cy="270" rx="125" ry="18" fill="#000" opacity="0.11" filter="url(#shadow)"/>
<g transform="{trans}"><g filter="url(#shadow)" opacity=".15" transform="translate(0 2)">{body}</g>{body}{hole}{mark}</g>
<path d="M25 30 h35" stroke="#B7131C" stroke-width="5" stroke-linecap="round"/>
<text x="25" y="293" font-family="Arial,sans-serif" fill="#6b6b72" font-size="13">POLSOLIDE · 3D · {idx}/20</text></svg>'''

# Estimate based on volumetric deposition (not slicer-verified); job plate quantity bounded by bed.
meta=[]
if '--pack' in sys.argv:
 for row in P:
    idx,slug,title,kind,w,h,t,purpose,finish,price,minn=row
    name=slugfile(row);(PREV/(name+'.svg')).write_text(svg_preview(row),encoding='utf-8')
    volume=m3mf(row)
    capacity=len(plate_positions(w,h))
    # pragmatic one-color base and 2 collective filament swaps; effective throughput 7-10mm3/s with overhead
    grams=volume*1.26/1000 # g for PLA 1.26g/cm3
    est_minutes=(volume/8.5/60)*1.40 + 2.4 # conservatively travel and swap amortized approx
    goal=math.ceil(480/est_minutes)
    copies=min(capacity,goal)
    m3mf(row,copies,plate=True)
    meta.append(dict(id=idx,slug=slug,name=title,kind=kind,w=w,h=h,thickness=t,volume_mm3=round(volume),weight_g=round(grams,1),max_print_copies=capacity,batch_copies=copies,rough_batch_hours=round(copies*est_minutes/60+0.4,1),price_eur=price,min_series=minn,description=purpose,finish=finish))
 (OUT/'produkty.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
 with open(OUT/'kalkulator_produkcji.csv','w',encoding='utf-8-sig',newline='') as f:
    wr=csv.DictWriter(f,fieldnames=meta[0].keys());wr.writeheader();wr.writerows(meta)
 print(json.dumps({'n':len(meta),'summary':[(x['id'],x['name'],x['weight_g'],x['batch_copies'],x['rough_batch_hours']) for x in meta]},ensure_ascii=False,indent=2))
