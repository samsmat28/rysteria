import re

KEEP = [
    ("bubble","Bubble",0,20,4,18,"max",1,[("bubble",0.45),("droplet",0.2)]),
    ("crab","Crab",0,55,14,24,"rare",2,[("shell",0.3),("claw",0.2)]),
    ("jellyfish","Jellyfish",0,48,16,25,"unusual",2,[("droplet",0.25),("lightning",0.18)]),
    ("starfish","Starfish",0,65,12,26,"epic",2,[("sand",0.25),("clover",0.18)]),
    ("shell","Shell",0,90,10,24,"max",2,[("shell",0.4),("plate",0.15)]),
    ("clownfish","Clownfish",0,35,9,18,"max",1,[("scale",0.35),("bubble",0.2)]),
    ("seahorse","Seahorse",0,42,11,20,"epic",1,[("droplet",0.3),("sand",0.2)]),
    ("pufferfish","Pufferfish",1,85,22,27,"unusual",3,[("bubble",0.3),("stinger",0.25)]),
    ("hermit_crab","Hermit Crab",1,110,16,26,"rare",3,[("rolled_shell",0.35),("claw",0.2)]),
    ("coral_golem","Coral Golem",1,140,20,32,"rare",3,[("rock",0.35),("plate",0.2)]),
    ("moray_eel","Moray Eel",2,120,28,26,"common",3,[("fang",0.3),("lightning",0.18)]),
    ("stingray","Stingray",2,130,25,31,"unusual",3,[("stinger",0.35),("sail",0.2)]),
    ("sea_turtle","Sea Turtle",2,220,18,34,"epic",3,[("shell",0.45),("plate",0.25)]),
    ("octopus","Octopus",3,180,35,32,"common",4,[("droplet",0.35),("third_eye",0.12)]),
    ("swordfish","Swordfish",3,165,44,29,"common",4,[("horn",0.35),("scale",0.25)]),
    ("electric_eel","Electric Eel",3,160,42,27,"common",4,[("lightning",0.45),("uranium",0.12)]),
    ("anglerfish","Anglerfish",4,230,48,31,"common",4,[("lantern",0.45),("fang",0.3)]),
    ("nautilus","Nautilus",4,290,34,30,"unusual",4,[("rolled_shell",0.5),("relic",0.15)]),
    ("great_white","Great White",5,360,68,38,"common",5,[("tooth",0.5),("fang",0.35)]),
    ("king_crab","King Crab",5,420,60,38,"common",5,[("claw",0.5),("crown",0.14)]),
    ("megalodon","Megalodon",6,560,92,46,"common",6,[("tooth",0.6),("relic",0.25)]),
    ("kraken_spawn","Kraken Spawn",6,500,86,42,"common",6,[("scythe",0.35),("droplet",0.4)]),
    ("trident_guardian","Trident Guardian",7,780,115,45,"common",7,[("crown",0.3),("plate",0.45),("lightning",0.35)]),
    ("void_ray","Void Ray",7,700,120,46,"common",7,[("sail",0.5),("third_eye",0.28),("obsidian",0.25)]),
    ("storm_kraken","Storm Kraken",8,920,148,50,"common",8,[("lightning",0.65),("scythe",0.4),("crown",0.25)]),
    ("omega_shark","Omega Shark",8,1020,155,52,"common",8,[("tooth",0.7),("fang",0.55),("meteor",0.15)]),
    ("hyper_hydra","Hyper Sea Hydra",9,1300,180,56,"common",9,[("venom",0.6),("scale",0.65),("third_eye",0.35)]),
    ("celestial_whale","Celestial Whale",9,1450,170,60,"unusual",9,[("light",0.5),("amber",0.45),("yggdrasil",0.18)]),
    ("abyssal_leviathan","Abyssal Leviathan",10,1900,230,64,"common",10,[("relic",0.5),("crown",0.45),("yggdrasil",0.25)]),
    ("thalassa_core","Thalassa Core",10,2400,255,64,"common",10,[("bubble",0.9),("relic",0.65),("yggdrasil",0.35)]),
]

sh = open("Shared/StaticData.h").read()
sh = re.sub(r"    rr_mob_id_bubble,[\s\S]*?    rr_mob_id_max,", "\n".join(f"    rr_mob_id_{m[0]}," for m in KEEP) + "\n    rr_mob_id_max,", sh, count=1)
open("Shared/StaticData.h", "w").write(sh)

sc = open("Shared/StaticData.c").read()
rows = [f"    {{rr_mob_id_{m[0]}, rr_rarity_id_common, rr_rarity_id_gods, {m[3]}, {m[4]}, {m[5]}.0f, rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_{m[6]}, {{{','.join(f'{{rr_petal_id_{p}, {pr}f}}' for p,pr in m[8])}}}}}," for m in KEEP]
sc = re.sub(r"    \{rr_mob_id_bubble,[\s\S]*?\{rr_mob_id_thalassa_core,[^\n]*\n\};", "\n".join(rows) + "\n};", sc, count=1)
sc = re.sub(r'"Bubble","Crab",[\s\S]*?"Thalassa Core"\n\};', ",".join(f'"{m[1]}"' for m in KEEP) + "\n};", sc, count=1)
sc = re.sub(r"(    3, //edmo\n)    [0-9,]+\n\};", r"\g<1>    " + ",".join(str(m[7]) for m in KEEP) + "\n};", sc, count=1)
sc = re.sub(r"(double RR_HELL_CREEK_MOB_ID_RARITY_COEFFICIENTS\[rr_mob_id_max\]\s*=\s*\{[\s\S]*?),\n    [0,]+\n\};", r"\1,\n    " + ",".join("0" for _ in KEEP) + "\n};", sc, count=1)
open("Shared/StaticData.c", "w").write(sc)

by_t = {t: [m[0] for m in KEEP if m[2] == t] for t in range(11)}
th = [10.0, 18.0, 26.0, 34.0, 42.0, 50.0, 58.0, 65.0, 70.0, 74.0]
wc = ["    if (biome == rr_biome_id_ocean) {", "        float difficulty = zone ? zone->difficulty : 1.0f; double r = rr_frand();"]
for t in range(10):
    mt = by_t[t]
    wc.append(f"        {'if' if t == 0 else 'else if'} (difficulty <= {th[t]}f) {{")
    for i, mid in enumerate(mt[:-1]): wc.append(f"            if (r < {round((i+1)/len(mt), 2)}f) return rr_mob_id_{mid};")
    wc.append(f"            return rr_mob_id_{mt[-1]};\n        }}")
wc.append("        else {")
for i, mid in enumerate(by_t[10][:-1]): wc.append(f"            if (r < {round((i+1)/len(by_t[10]), 2)}f) return rr_mob_id_{mid};")
wc.append(f"            return rr_mob_id_{by_t[10][-1]};\n        }}\n    }}")
wv = re.sub(r"    if \(biome == rr_biome_id_ocean\)\s*\{[\s\S]*?\n    \}", "\n".join(wc), open("Server/Waves.c").read(), count=1)
open("Server/Waves.c", "w").write(wv)
print("TRIMMED_TO_30_OCEAN_MOBS")
