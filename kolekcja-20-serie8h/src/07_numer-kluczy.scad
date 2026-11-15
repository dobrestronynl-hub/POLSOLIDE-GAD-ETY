// POLSOLIDE — Numerator kluczy
// Materiały: base=czarny (#18181B); red=czerwony (#B7131C); white=biały (#F1F0EC).
// Zapisz do STL: openscad -o element.stl -D 'part="base"' tenplik.scad
// Model na płasko: wszystkie barwy zmieniają się tylko na samym końcu druku.
$fn=40;
part="all"; // all, base, red, white
W=48; H=30; T=3.0; kind="tag";
RH=0.48; WH=0.40; // wysokość czerwonego i białego detalowania
magnet=false;
label="01"; // zmień np. numer lokalu, oznaczenie stanowiska lub pomieszczenia

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
