import re

with open("Shared/StaticData.h", "r", encoding="utf-8") as f:
    sd_h = f.read()
if "rr_petal_id_yggdrasil" not in sd_h:
    sd_h = sd_h.replace(
        "    rr_petal_id_corn,           // 41\n    rr_petal_id_max,            // 42",
        "    rr_petal_id_corn,           // 41\n    rr_petal_id_yggdrasil,      // 42\n    rr_petal_id_max,            // 43", 1
    )
    with open("Shared/StaticData.h", "w", encoding="utf-8") as f:
        f.write(sd_h)

with open("Shared/StaticData.c", "r", encoding="utf-8") as f:
    sd_c = f.read()
if "rr_petal_id_yggdrasil" not in sd_c:
    sd_c = sd_c.replace(
        "    {rr_petal_id_corn,          rr_rarity_id_common,  offensive,  12.0f, 65.0f,  0.0f,  35,  0, {1,1,1,1,1,1,1,1,1,1,1}},",
        "    {rr_petal_id_corn,          rr_rarity_id_common,  offensive,  12.0f, 65.0f,  0.0f,  35,  0, {1,1,1,1,1,1,1,1,1,1,1}},\n"
        "    {rr_petal_id_yggdrasil,     rr_rarity_id_mythic,  defensive,   8.0f, 10.0f,  0.0f,  60,  0, {1,1,1,1,1,1,1,1,1,1,1}},", 1
    )
    sd_c = sd_c.replace('"Yucca", "Triangle", "Corn"', '"Yucca", "Triangle", "Corn", "Yggdrasil"', 1)
    sd_c = sd_c.replace('"A sharp golden kernel of corn."', '"A sharp golden kernel of corn.",\n    "Revives & teleports dead squadmates to you."', 1)

for mob in ("fire_worker_ant", "fire_soldier_ant", "fire_ant_egg"):
    sd_c = re.sub(
        rf'(\{{rr_mob_id_{mob},\s*rr_rarity_id_common,\s*rr_rarity_id_gods,\s*\d+,\s*\d+,\s*[\d.]+f,\s*)rr_rarity_id_common,',
        r'\1rr_rarity_id_max,', sd_c
    )

sd_c = sd_c.replace("{rr_petal_id_leaf, 0.85}", "{rr_petal_id_yggdrasil, 0.45}")
sd_c = sd_c.replace("{rr_petal_id_egg, 0.70}", "{rr_petal_id_yggdrasil, 0.45}")
sd_c = sd_c.replace("{rr_petal_id_sand, 0.80}", "{rr_petal_id_yggdrasil, 0.45}")
with open("Shared/StaticData.c", "w", encoding="utf-8") as f:
    f.write(sd_c)
print("Шаг 1 (данные и лут) готов!")
