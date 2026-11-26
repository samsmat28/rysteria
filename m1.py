import re, math

MOBS = [
    ("bubble","Bubble",0,20,4,18,"max",1,[("bubble",0.45),("droplet",0.2)],0x887dd3fc,0xffe0f2fe,0),
    ("crab","Crab",0,55,14,24,"rare",2,[("shell",0.3),("claw",0.2)],0xffea580c,0xffdc2626,1),
    ("jellyfish","Jellyfish",0,48,16,25,"unusual",2,[("droplet",0.25),("lightning",0.18)],0xffc084fc,0xfff472b6,2),
    ("starfish","Starfish",0,65,12,26,"epic",2,[("sand",0.25),("clover",0.18)],0xfffb7185,0xfff97316,3),
    ("shell","Shell",0,90,10,24,"max",2,[("shell",0.4),("plate",0.15)],0xffd6c3a5,0xff92400e,4),
    ("clownfish","Clownfish",0,35,9,18,"max",1,[("scale",0.35),("bubble",0.2)],0xfff97316,0xffffffff,5),
    ("seahorse","Seahorse",0,42,11,20,"epic",1,[("droplet",0.3),("sand",0.2)],0xfffacc15,0xffea580c,5),
    ("sea_urchin","Sea Urchin",0,50,18,20,"common",2,[("stinger",0.35),("shell",0.15)],0xff581c87,0xffa855f7,3),
    ("shrimp","Shrimp",0,30,10,17,"rare",1,[("claw",0.25),("meat",0.2)],0xfffb923c,0xfffed7aa,5),
    ("plankton","Plankton",0,18,5,14,"max",1,[("bubble",0.4),("berry",0.2)],0xff34d399,0xffa7f3d0,0),
    ("sea_slug","Sea Slug",1,60,12,22,"epic",2,[("droplet",0.35),("venom",0.15)],0xff38bdf8,0xfffde047,5),
    ("pufferfish","Pufferfish",1,85,22,27,"unusual",3,[("bubble",0.3),("stinger",0.25)],0xfffbbf24,0xff78350f,3),
    ("hermit_crab","Hermit Crab",1,110,16,26,"rare",3,[("rolled_shell",0.35),("claw",0.2)],0xffb45309,0xffef4444,1),
    ("coral_golem","Coral Golem",1,140,20,32,"rare",3,[("rock",0.35),("plate",0.2)],0xfff43f5e,0xff2dd4bf,4),
    ("flying_fish","Flying Fish",1,55,18,21,"unusual",2,[("sonic_wing",0.3),("scale",0.25)],0xff0284c7,0xffbae6fd,5),
    ("moray_eel","Moray Eel",2,120,28,26,"common",3,[("fang",0.3),("lightning",0.18)],0xff15803d,0xffbef264,5),
    ("stingray","Stingray",2,130,25,31,"unusual",3,[("stinger",0.35),("sail",0.2)],0xff475569,0xff38bdf8,5),
    ("lobster","Lobster",2,150,30,28,"common",3,[("claw",0.4),("plate",0.2)],0xffb91c1c,0xfffca5a5,1),
    ("barracuda","Barracuda",2,110,34,25,"common",3,[("tooth",0.35),("scale",0.25)],0xff64748b,0xffe2e8f0,5),
    ("sea_turtle","Sea Turtle",2,220,18,34,"epic",3,[("shell",0.45),("plate",0.25)],0xff166534,0xff86efac,4),
    ("octopus","Octopus",3,180,35,32,"common",4,[("droplet",0.35),("third_eye",0.12)],0xff9333ea,0xffe879f9,2),
    ("squid","Giant Squid",3,195,38,33,"common",4,[("sail",0.3),("fang",0.22)],0xffe11d48,0xfffda4af,2),
    ("swordfish","Swordfish",3,165,44,29,"common",4,[("horn",0.35),("scale",0.25)],0xff1d4ed8,0xff93c5fd,5),
    ("manta_ray","Manta Ray",3,240,30,38,"rare",4,[("sail",0.4),("magnet",0.15)],0xff1e293b,0xff38bdf8,5),
    ("electric_eel","Electric Eel",3,160,42,27,"common",4,[("lightning",0.45),("uranium",0.12)],0xff2563eb,0xfffef08a,5),
    ("anglerfish","Anglerfish",4,230,48,31,"common",4,[("lantern",0.45),("fang",0.3)],0xff1e1b4b,0xfffef08a,5),
    ("hammerhead","Hammerhead",4,270,52,35,"common",5,[("tooth",0.4),("plate",0.22)],0xff4b5563,0xff9ca3af,5),
    ("nautilus","Nautilus",4,290,34,30,"unusual",4,[("rolled_shell",0.5),("relic",0.15)],0xffd97706,0xfffef3c7,4),
    ("lionfish","Lionfish",4,200,55,28,"common",4,[("venom",0.4),("frill",0.25)],0xffdc2626,0xffffffff,3),
    ("narwhal","Narwhal",4,280,50,34,"unusual",5,[("horn",0.45),("amber",0.18)],0xff3b82f6,0xffe0f2fe,5),
    ("great_white","Great White",5,360,68,38,"common",5,[("tooth",0.5),("fang",0.35)],0xff334155,0xfff8fafc,5),
    ("orca","Orca",5,400,64,40,"common",5,[("meat",0.4),("relic",0.18)],0xff0f172a,0xffffffff,5),
    ("king_crab","King Crab",5,420,60,38,"common",5,[("claw",0.5),("crown",0.14)],0xff991b1b,0xfffbbf24,1),
    ("abyss_jelly","Abyss Jelly",5,310,72,36,"common",5,[("lightning",0.5),("third_eye",0.16)],0xff4c1d95,0xff22d3ee,2),
    ("sea_serpent","Sea Serpent",5,380,66,36,"common",5,[("scale",0.45),("venom",0.3)],0xff065f46,0xff34d399,5),
    ("siren","Deep Siren",6,440,78,34,"common",6,[("crown",0.22),("third_eye",0.22)],0xffbe185d,0xfffbcfe8,2),
    ("megalodon","Megalodon",6,560,92,46,"common",6,[("tooth",0.6),("relic",0.25)],0xff1e293b,0xffef4444,5),
    ("kraken_spawn","Kraken Spawn",6,500,86,42,"common",6,[("scythe",0.35),("droplet",0.4)],0xff581c87,0xffc084fc,2),
    ("colossal_clam","Colossal Clam",6,650,55,44,"unusual",6,[("shell",0.6),("light",0.25)],0xff78350f,0xfffef08a,4),
    ("abyss_dragon","Abyss Dragon",6,540,90,42,"common",6,[("magma",0.3),("scale",0.45)],0xff0f766e,0xff5eead4,5),
    ("leviathan_larva","Leviathan Larva",7,720,110,44,"common",7,[("scale",0.55),("amber",0.3),("relic",0.2)],0xff0369a1,0xff7dd3fc,5),
    ("trident_guardian","Trident Guardian",7,780,115,45,"common",7,[("crown",0.3),("plate",0.45),("lightning",0.35)],0xff1d4ed8,0xfffacc15,1),
    ("void_ray","Void Ray",7,700,120,46,"common",7,[("sail",0.5),("third_eye",0.28),("obsidian",0.25)],0xff1e1b4b,0xffa855f7,5),
    ("tidal_titan","Tidal Titan",8,960,140,52,"common",8,[("rock",0.6),("relic",0.3),("yggdrasil",0.12)],0xff134e4a,0xff2dd4bf,4),
    ("storm_kraken","Storm Kraken",8,920,148,50,"common",8,[("lightning",0.65),("scythe",0.4),("crown",0.25)],0xff3b0764,0xff38bdf8,2),
    ("omega_shark","Omega Shark",8,1020,155,52,"common",8,[("tooth",0.7),("fang",0.55),("meteor",0.15)],0xff090d16,0xfff43f5e,5),
    ("hyper_hydra","Hyper Sea Hydra",9,1300,180,56,"common",9,[("venom",0.6),("scale",0.65),("third_eye",0.35)],0xff064e3b,0xfffde047,5),
    ("celestial_whale","Celestial Whale",9,1450,170,60,"unusual",9,[("light",0.5),("amber",0.45),("yggdrasil",0.18)],0xff1e3a8a,0xfffef08a,5),
    ("hyper_nautilus","Hyper Nautilus",9,1380,175,54,"common",9,[("rolled_shell",0.75),("obsidian",0.45),("crown",0.35)],0xff701a75,0xfff0abfc,4),
    ("abyssal_leviathan","Abyssal Leviathan",10,1900,230,64,"common",10,[("relic",0.5),("crown",0.45),("yggdrasil",0.25)],0xff020617,0xffef4444,5),
    ("poseidon_avatar","Poseidon Avatar",10,2100,245,62,"common",10,[("crown",0.6),("lightning",0.8),("third_eye",0.45)],0xff0c4a6e,0xfffacc15,1),
    ("ocean_god_kraken","Ocean God Kraken",10,2300,260,68,"common",10,[("yggdrasil",0.35),("relic",0.6),("meteor",0.3)],0xff2e1065,0xfff472b6,2),
    ("primordial_shell","Primordial Shell",10,2500,210,64,"unusual",10,[("shell",0.9),("light",0.55),("crown",0.5)],0xff451a03,0xfffef08a,4),
    ("abyss_star_god","Abyss Star God",10,2000,240,60,"common",10,[("clover",0.65),("third_eye",0.5),("yggdrasil",0.3)],0xff881337,0xfffb7185,3),
    ("thalassa_core","Thalassa Core",10,2400,255,64,"common",10,[("bubble",0.9),("relic",0.65),("yggdrasil",0.35)],0xff083344,0xff22d3ee,0),
]

sh = open("Shared/StaticData.h").read()
if "rr_mob_id_bubble" not in sh:
    sh = sh.replace("    rr_mob_id_max,", "\n".join(f"    rr_mob_id_{m[0]}," for m in MOBS) + "\n    rr_mob_id_max,", 1)
    open("Shared/StaticData.h", "w").write(sh)

sc = open("Shared/StaticData.c").read()
if "rr_mob_id_bubble" not in sc:
    rows = [f"    {{rr_mob_id_{m[0]}, rr_rarity_id_common, rr_rarity_id_gods, {m[3]}, {m[4]}, {m[5]}.0f, rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_{m[6]}, {{{','.join(f'{{rr_petal_id_{p}, {pr}f}}' for p,pr in m[8])}}}}}," for m in MOBS]
    sc = sc.replace("    {rr_mob_id_meadow_centipede, rr_rarity_id_common, rr_rarity_id_gods, 160, 20, 34.0f, rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_meadow_segment, 0.35}}},\n};", "    {rr_mob_id_meadow_centipede, rr_rarity_id_common, rr_rarity_id_gods, 160, 20, 34.0f, rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_meadow_segment, 0.35}}},\n" + "\n".join(rows) + "\n};", 1)
    sc = sc.replace('"Cricket", "Aphid", "Meadow Centipede"\n};', '"Cricket", "Aphid", "Meadow Centipede",\n    ' + ",".join(f'"{m[1]}"' for m in MOBS) + "\n};", 1)
    sc = sc.replace("    3, //edmo\n};", "    3, //edmo\n    " + ",".join(str(m[7]) for m in MOBS) + "\n};", 1)
    sc = re.sub(r"(double RR_HELL_CREEK_MOB_ID_RARITY_COEFFICIENTS\[rr_mob_id_max\]\s*=\s*\{[\s\S]*?)(\n\};)", r"\1,\n    " + ",".join("0" for _ in MOBS) + r"\2", sc, count=1)

g = [["_"]*80 for _ in range(80)]
rooms = [(64,40,5,"c"),(66,26,4,"c"),(56,32,4,"c"),(65,54,4,"u"),(54,50,4,"u"),(56,16,4,"u"),(44,14,4,"r"),(32,14,4,"r"),(20,14,4,"e"),(10,16,4,"l"),(44,30,4,"r"),(42,44,4,"e"),(30,28,4,"l"),(30,42,4,"m"),(18,30,4,"x"),(18,44,4,"a"),(52,65,4,"r"),(38,64,4,"e"),(26,58,4,"l"),(24,68,4,"m"),(14,66,4,"x"),(10,56,4,"a"),(10,46,5,"o"),(10,34,4,"h"),(9,22,4,"g")]
edges = [(0,1),(0,2),(0,3),(3,4),(2,4),(1,5),(5,6),(6,7),(7,8),(8,9),(2,10),(4,11),(10,11),(6,10),(10,12),(11,13),(12,13),(7,12),(12,14),(13,15),(14,15),(9,14),(3,16),(16,17),(11,17),(17,18),(13,18),(18,19),(19,20),(15,20),(20,21),(21,22),(15,22),(22,23),(14,23),(23,24),(9,24)]
def carve(cx,cy,rad,t):
    for dy in range(-rad,rad+1):
        for dx in range(-rad,rad+1):
            if dx*dx+dy*dy<=rad*rad and 4<=cx+dx<=75 and 4<=cy+dy<=75: g[cy+dy][cx+dx]=t
for ia,ib in edges:
    x0,y0,_,t0=rooms[ia]; x1,y1,_,t1=rooms[ib]; st=max(abs(x1-x0),abs(y1-y0))*2; d=max(1.0,math.hypot(x1-x0,y1-y0)); px,py=-(y1-y0)/d,(x1-x0)/d
    for s in range(st+1):
        u=s/float(max(1,st)); wb=2.0*math.sin(u*math.pi*2+ia)
        carve(int(round(x0+(x1-x0)*u+px*wb)),int(round(y0+(y1-y0)*u+py*wb)),2,t0 if u<0.5 else t1)
for cx,cy,rad,t in rooms: carve(cx,cy,rad,t)
sc = re.sub(r"RR_DEFINE_MAZE\(OCEAN,\s*160\)\s*=\s*\{[\s\S]*?\};", "RR_DEFINE_MAZE(OCEAN, 160) = {\n"+"\n".join("    {"+",".join(r)+"}," for r in g)+"\n};", sc, count=1)
open("Shared/StaticData.c", "w").write(sc)
print("STEP_1_OK")
