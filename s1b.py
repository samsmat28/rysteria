with open("Shared/StaticData.c", "r") as f: c = f.read()
if "rr_petal_id_claw" not in c:
    p_rows = [
        ("claw","offensive",14,18,0,25,1),("fang","offensive",16,22,0,30,1),("tooth","offensive",15,26,0,32,1),
        ("horn","offensive",18,24,0,35,1),("thagomizer","offensive",11,15,0,30,4),("scythe","offensive",22,32,0,40,1),
        ("magma","offensive",20,28,0,38,1),("obsidian","offensive",35,45,0,55,1),("plate","defensive",28,8,0,40,1),
        ("scale","defensive",22,12,0,35,2),("amber","defensive",18,8,8,45,1),("branch","defensive",16,10,6,35,1),
        ("pearl","defensive",14,6,10,40,1),("tail","defensive",12,10,0,25,1),("frill","defensive",16,11,0,30,1),
        ("venom","offensive",10,24,0,32,2),("sail","defensive",15,9,0,30,1),("ash","defensive",12,14,0,28,3),
        ("crown","defensive",30,25,12,50,1),("relic","offensive",32,38,8,48,1)
    ]
    p_str = "    {rr_petal_id_yggdrasil,     rr_rarity_id_mythic,  defensive,   8.0f, 10.0f,  0.0f,  60,  0, {1,1,1,1,1,1,1,1,1,1,1}},\n" + "".join(
        f"    {{rr_petal_id_{n}, rr_rarity_id_common, {t}, {hp}.0f, {dmg}.0f, {hl}.0f, {rl}, 0, {{{','.join([str(cnt)]*11)}}}}},\n" for n,t,hp,dmg,hl,rl,cnt in p_rows
    )
    c = c.replace("    {rr_petal_id_yggdrasil,     rr_rarity_id_mythic,  defensive,   8.0f, 10.0f,  0.0f,  60,  0, {1,1,1,1,1,1,1,1,1,1,1}},\n", p_str, 1)
    c = c.replace('"Yucca", "Triangle", "Corn", "Yggdrasil"', '"Yucca", "Triangle", "Corn", "Yggdrasil", ' + ", ".join(f'"{n.capitalize()}"' for n,*_ in p_rows), 1)
    c = c.replace('"Revives & teleports dead squadmates to you."', '"Revives & teleports dead squadmates to you.", ' + ", ".join(f'"Prehistoric {n} petal."' for n,*_ in p_rows), 1)
    m_rows = [
        ("compsognathus",22,12,18,"common","claw",0.35,"tail",0.30),("stegosaurus",85,18,38,"common","thagomizer",0.35,"plate",0.35),
        ("dilophosaurus",48,22,26,"common","venom",0.35,"frill",0.30),("spinosaurus",140,32,46,"common","sail",0.40,"tooth",0.35),
        ("carnotaurus",110,30,36,"common","horn",0.40,"claw",0.35),("brachiosaurus",320,15,68,"max","amber",0.45,"branch",0.45),
        ("therizinosaurus",180,42,44,"common","scythe",0.45,"feather",0.40),("mosasaurus",260,45,56,"common","pearl",0.45,"scale",0.45),
        ("volcano",500,35,64,"max","magma",0.50,"obsidian",0.45),("titanoboa",1600,55,72,"common","crown",0.65,"relic",0.65)
    ]
    m_str = "    {rr_mob_id_queen_termite,    rr_rarity_id_common, rr_rarity_id_gods, 4000, 40, 185.0f, rr_rarity_id_max, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_egg, 0.95},{rr_petal_id_bone, 0.85},{rr_petal_id_mandible, 0.85},{rr_petal_id_yggdrasil, 0.45}}},\n" + "".join(
        f"    {{rr_mob_id_{n}, rr_rarity_id_common, rr_rarity_id_gods, {hp}, {dmg}, {rad}.0f, rr_rarity_id_{ai}, rr_rarity_id_{ai}, rr_rarity_id_max, {{{{rr_petal_id_{d1}, {c1}}},{{rr_petal_id_{d2}, {c2}}}}}}},\n" for n,hp,dmg,rad,ai,d1,c1,d2,c2 in m_rows
    )
    c = c.replace("    {rr_mob_id_queen_termite,    rr_rarity_id_common, rr_rarity_id_gods, 4000, 40, 185.0f, rr_rarity_id_max, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_egg, 0.95},{rr_petal_id_bone, 0.85},{rr_petal_id_mandible, 0.85},{rr_petal_id_yggdrasil, 0.45}}},\n", m_str, 1)
    c = c.replace('"Queen Fire Ant", "Queen Termite"', '"Queen Fire Ant", "Queen Termite", ' + ", ".join(f'"{n.capitalize()}"' for n,*_ in m_rows), 1)
    c = c.replace("100, 120, 140, 10000, 12000, 11000\n};", "100, 120, 140, 10000, 12000, 11000, 15, 45, 35, 80, 75, 150, 110, 160, 220, 5000\n};", 1)
    c = c.replace("0.0, 0.0, 0.0\n};", "0.0, 0.0, 0.0" + ", 0.0"*10 + "\n};", 2)
    with open("Shared/StaticData.c", "w") as f: f.write(c)
print("s1b OK")
