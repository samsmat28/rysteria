# 1. Shared/StaticData.h
with open("Shared/StaticData.h", "r", encoding="utf-8") as f:
    sd_h = f.read()

new_petals_h = """    rr_petal_id_yggdrasil,      // 42
    rr_petal_id_claw,           // 43
    rr_petal_id_fang,           // 44
    rr_petal_id_tooth,          // 45
    rr_petal_id_horn,           // 46
    rr_petal_id_thagomizer,     // 47
    rr_petal_id_scythe,         // 48
    rr_petal_id_magma,          // 49
    rr_petal_id_obsidian,       // 50
    rr_petal_id_plate,          // 51
    rr_petal_id_scale,          // 52
    rr_petal_id_amber,          // 53
    rr_petal_id_branch,         // 54
    rr_petal_id_pearl,          // 55
    rr_petal_id_tail,           // 56
    rr_petal_id_frill,          // 57
    rr_petal_id_venom,          // 58
    rr_petal_id_sail,           // 59
    rr_petal_id_ash,            // 60
    rr_petal_id_crown,          // 61
    rr_petal_id_relic,          // 62
    rr_petal_id_max,            // 63"""

new_mobs_h = """    rr_mob_id_queen_termite,    // 35
    rr_mob_id_compsognathus,    // 36
    rr_mob_id_stegosaurus,      // 37
    rr_mob_id_dilophosaurus,    // 38
    rr_mob_id_spinosaurus,      // 39
    rr_mob_id_carnotaurus,      // 40
    rr_mob_id_brachiosaurus,    // 41
    rr_mob_id_therizinosaurus,  // 42
    rr_mob_id_mosasaurus,       // 43
    rr_mob_id_volcano,          // 44
    rr_mob_id_titanoboa,        // 45
    rr_mob_id_max,              // 46"""

if "rr_petal_id_claw" not in sd_h:
    sd_h = sd_h.replace("    rr_petal_id_yggdrasil,      // 42\n    rr_petal_id_max,            // 43", new_petals_h, 1)
    sd_h = sd_h.replace("    rr_mob_id_queen_termite,    // 35\n\n    rr_mob_id_max,              // 36", new_mobs_h, 1)
    with open("Shared/StaticData.h", "w", encoding="utf-8") as f:
        f.write(sd_h)

# 2. Shared/StaticData.c
with open("Shared/StaticData.c", "r", encoding="utf-8") as f:
    sd_c = f.read()

if "rr_petal_id_claw" not in sd_c:
    petals_data = """    {rr_petal_id_yggdrasil,     rr_rarity_id_mythic,  defensive,   8.0f, 10.0f,  0.0f,  60,  0, {1,1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_claw,          rr_rarity_id_common,  offensive,  14.0f, 18.0f,  0.0f,  25,  0, {1,1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_fang,          rr_rarity_id_common,  offensive,  16.0f, 22.0f,  0.0f,  30,  0, {1,1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_tooth,         rr_rarity_id_common,  offensive,  15.0f, 26.0f,  0.0f,  32,  0, {1,1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_horn,          rr_rarity_id_common,  offensive,  18.0f, 24.0f,  0.0f,  35,  0, {1,1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_thagomizer,    rr_rarity_id_common,  offensive,  11.0f, 15.0f,  0.0f,  30,  0, {4,4,4,4,4,4,4,4,4,4,4}},
    {rr_petal_id_scythe,        rr_rarity_id_common,  offensive,  22.0f, 32.0f,  0.0f,  40,  0, {1,1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_magma,         rr_rarity_id_common,  offensive,  20.0f, 28.0f,  0.0f,  38,  0, {1,1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_obsidian,      rr_rarity_id_common,  offensive,  35.0f, 45.0f,  0.0f,  55,  0, {1,1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_plate,         rr_rarity_id_common,  defensive,  28.0f,  8.0f,  0.0f,  40,  0, {1,1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_scale,         rr_rarity_id_common,  defensive,  22.0f, 12.0f,  0.0f,  35,  0, {2,2,2,2,2,2,2,2,2,2,2}},
    {rr_petal_id_amber,         rr_rarity_id_common,  defensive,  18.0f,  8.0f,  8.0f,  45,  0, {1,1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_branch,        rr_rarity_id_common,  defensive,  16.0f, 10.0f,  6.0f,  35,  0, {1,1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_pearl,         rr_rarity_id_common,  defensive,  14.0f,  6.0f, 10.0f,  40,  0, {1,1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_tail,          rr_rarity_id_common,  defensive,  12.0f, 10.0f,  0.0f,  25,  0, {1,1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_frill,         rr_rarity_id_common,  defensive,  16.0f, 11.0f,  0.0f,  30,  0, {1,1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_venom,         rr_rarity_id_common,  offensive,  10.0f, 24.0f,  0.0f,  32,  0, {2,2,2,2,2,2,2,2,2,2,2}},
    {rr_petal_id_sail,          rr_rarity_id_common,  defensive,  15.0f,  9.0f,  0.0f,  30,  0, {1,1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_ash,           rr_rarity_id_common,  defensive,  12.0f, 14.0f,  0.0f,  28,  0, {3,3,3,3,3,3,3,3,3,3,3}},
    {rr_petal_id_crown,         rr_rarity_id_mythic,  defensive,  30.0f, 25.0f, 12.0f,  50,  0, {1,1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_relic,         rr_rarity_id_mythic,  offensive,  32.0f, 38.0f,  8.0f,  48,  0, {1,1,1,1,1,1,1,1,1,1,1}},"""

    sd_c = sd_c.replace(
        "    {rr_petal_id_yggdrasil,     rr_rarity_id_mythic,  defensive,   8.0f, 10.0f,  0.0f,  60,  0, {1,1,1,1,1,1,1,1,1,1,1}},",
        petals_data, 1
    )
    sd_c = sd_c.replace(
        '"Yucca", "Triangle", "Corn", "Yggdrasil"',
        '"Yucca", "Triangle", "Corn", "Yggdrasil", "Claw", "Fang", "Tooth", "Horn", "Thagomizer", "Scythe", "Magma", "Obsidian", "Plate", "Scale", "Amber", "Branch", "Pearl", "Tail", "Frill", "Venom", "Sail", "Ash", "Crown", "Relic"', 1
    )
    descs = """    "Revives & teleports dead squadmates to you.",
    "A razor-sharp raptor claw.", "A venomous predator fang.", "A serrated prehistoric tooth.",
    "A heavy charging dinosaur horn.", "Four deadly tail spikes.", "A massive slashing claw scythe.",
    "Molten volcanic magma.", "Razor-sharp volcanic glass.", "Thick armored stegosaur plate.",
    "Hardened prehistoric scale.", "Ancient fossilized tree resin.", "A sturdy Cretaceous branch.",
    "A lustrous primordial pearl.", "A agile balancing dinosaur tail.", "A wide intimidating neck frill.",
    "Toxic dilophosaur spit.", "A tall heat-catching dorsal sail.", "Smoldering volcanic ash.",
    "Crown of the Cretaceous Apex.", "Ancient relic of the Gods." """
    sd_c = sd_c.replace('    "Revives & teleports dead squadmates to you."', descs, 1)

    mobs_data = """    {rr_mob_id_queen_termite,    rr_rarity_id_common, rr_rarity_id_gods, 4000, 40, 185.0f, rr_rarity_id_max, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_egg, 0.95},{rr_petal_id_bone, 0.85},{rr_petal_id_mandible, 0.85},{rr_petal_id_yggdrasil, 0.45}}},
    {rr_mob_id_compsognathus,    rr_rarity_id_common, rr_rarity_id_gods, 22, 12, 18.0f, rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_claw, 0.35},{rr_petal_id_tail, 0.30},{rr_petal_id_bone, 0.20}}},
    {rr_mob_id_stegosaurus,      rr_rarity_id_common, rr_rarity_id_gods, 85, 18, 38.0f, rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_thagomizer, 0.35},{rr_petal_id_plate, 0.35},{rr_petal_id_leaf, 0.30}}},
    {rr_mob_id_dilophosaurus,    rr_rarity_id_common, rr_rarity_id_gods, 48, 22, 26.0f, rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_venom, 0.35},{rr_petal_id_frill, 0.30},{rr_petal_id_fang, 0.30}}},
    {rr_mob_id_spinosaurus,      rr_rarity_id_common, rr_rarity_id_gods, 140, 32, 46.0f, rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_sail, 0.40},{rr_petal_id_tooth, 0.35},{rr_petal_id_scale, 0.35}}},
    {rr_mob_id_carnotaurus,      rr_rarity_id_common, rr_rarity_id_gods, 110, 30, 36.0f, rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_horn, 0.40},{rr_petal_id_claw, 0.35},{rr_petal_id_meat, 0.35}}},
    {rr_mob_id_brachiosaurus,    rr_rarity_id_common, rr_rarity_id_gods, 320, 15, 68.0f, rr_rarity_id_max, rr_rarity_id_max, rr_rarity_id_max, {{rr_petal_id_amber, 0.45},{rr_petal_id_branch, 0.45},{rr_petal_id_leaf, 0.50}}},
    {rr_mob_id_therizinosaurus,  rr_rarity_id_common, rr_rarity_id_gods, 180, 42, 44.0f, rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_scythe, 0.45},{rr_petal_id_feather, 0.40},{rr_petal_id_claw, 0.40}}},
    {rr_mob_id_mosasaurus,       rr_rarity_id_common, rr_rarity_id_gods, 260, 45, 56.0f, rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_pearl, 0.45},{rr_petal_id_scale, 0.45},{rr_petal_id_tooth, 0.40}}},
    {rr_mob_id_volcano,          rr_rarity_id_common, rr_rarity_id_gods, 500, 35, 64.0f, rr_rarity_id_max, rr_rarity_id_max, rr_rarity_id_max, {{rr_petal_id_magma, 0.50},{rr_petal_id_obsidian, 0.45},{rr_petal_id_ash, 0.50}}},
    {rr_mob_id_titanoboa,        rr_rarity_id_common, rr_rarity_id_gods, 1600, 55, 72.0f, rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_crown, 0.65},{rr_petal_id_relic, 0.65},{rr_petal_id_yggdrasil, 0.50}}},"""

    sd_c = sd_c.replace(
        "    {rr_mob_id_queen_termite,    rr_rarity_id_common, rr_rarity_id_gods, 4000, 40, 185.0f, rr_rarity_id_max, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_egg, 0.95},{rr_petal_id_bone, 0.85},{rr_petal_id_mandible, 0.85},{rr_petal_id_yggdrasil, 0.45}}},",
        mobs_data, 1
    )
    sd_c = sd_c.replace(
        '"Queen Fire Ant", "Queen Termite"',
        '"Queen Fire Ant", "Queen Termite", "Compsognathus", "Stegosaurus", "Dilophosaurus", "Spinosaurus", "Carnotaurus", "Brachiosaurus", "Therizinosaurus", "Mosasaurus", "Volcano", "Titanoboa"', 1
    )
    sd_c = sd_c.replace("100, 120, 140, 10000, 12000, 11000\n};", "100, 120, 140, 10000, 12000, 11000, 15, 45, 35, 80, 75, 150, 110, 160, 220, 5000\n};", 1)
    sd_c = sd_c.replace("0.0, 0.0, 0.0\n};", "0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0\n};", 2)

with open("Shared/StaticData.c", "w", encoding="utf-8") as f:
    f.write(sd_c)

# 3. Server/Waves.c: вплетаем 10 новых мобов в зоны Hell Creek
with open("Server/Waves.c", "r", encoding="utf-8") as f:
    waves = f.read()

new_hc_waves = """    if (biome == rr_biome_id_hell_creek)
    {
        float diff = zone ? zone->difficulty : 1.0f;
        double r = rr_frand();
        if (diff <= 18.0f)
        {
            if (r < 0.22) return rr_mob_id_compsognathus;
            if (r < 0.42) return rr_mob_id_stegosaurus;
            if (r < 0.60) return rr_mob_id_triceratops;

cat << 'EOF' > s1a.py
with open("Shared/StaticData.h", "r") as f: h = f.read()
if "rr_petal_id_claw" not in h:
    p = "    rr_petal_id_yggdrasil,      // 42\n" + "".join(
        f"    rr_petal_id_{n},\n" for n in ["claw","fang","tooth","horn","thagomizer","scythe","magma","obsidian","plate","scale","amber","branch","pearl","tail","frill","venom","sail","ash","crown","relic"]
    ) + "    rr_petal_id_max,"
    m = "    rr_mob_id_queen_termite,    // 35\n" + "".join(
        f"    rr_mob_id_{n},\n" for n in ["compsognathus","stegosaurus","dilophosaurus","spinosaurus","carnotaurus","brachiosaurus","therizinosaurus","mosasaurus","volcano","titanoboa"]
    ) + "    rr_mob_id_max,"
    h = h.replace("    rr_petal_id_yggdrasil,      // 42\n    rr_petal_id_max,            // 43", p, 1)
    h = h.replace("    rr_mob_id_queen_termite,    // 35\n\n    rr_mob_id_max,              // 36", m, 1)
    with open("Shared/StaticData.h", "w") as f: f.write(h)
print("s1a OK")
