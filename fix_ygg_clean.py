import re

# 1. Добавляем rr_petal_id_yggdrasil и чиним лут огненных муравьёв
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

# 2. В PetalBehavior.c добавляем #include "../Squad.h" и правильный цикл по player_info
with open("Server/System/PetalBehavior.c", "r", encoding="utf-8") as f:
    pb = f.read()
if '#include "../Squad.h"' not in pb:
    pb = '#include "../Squad.h"\n' + pb

old_loop = """                    for (EntityIdx oid = 0; oid < simulation->entity_cap; ++oid) {
                        if (rr_simulation_has_player_info(simulation, oid)) {
                            struct rr_component_player_info *m = rr_simulation_get_player_info(simulation, oid);
                            if (m->client && m->client != player_info->client && m->squad_member && m->squad_member->squad_id == player_info->squad_member->squad_id) {
                                m->client->has_ygg_teleport = 1; m->client->ygg_x = flower_physical->x; m->client->ygg_y = flower_physical->y;
                            }
                        }
                    }"""

new_loop = """                    for (uint32_t i = 0; i < RR_SQUAD_MEMBER_COUNT; ++i) {
                        struct rr_squad_member *sm = &player_info->squad_member->squad->members[i];
                        if (sm->client && sm->client != player_info->client) {
                            sm->client->has_ygg_teleport = 1;
                            sm->client->ygg_x = flower_physical->x;
                            sm->client->ygg_y = flower_physical->y;
                        }
                    }"""

assert old_loop in pb, "Не найден цикл тиммейтов в PetalBehavior.c"
pb = pb.replace(old_loop, new_loop, 1)
with open("Server/System/PetalBehavior.c", "w", encoding="utf-8") as f:
    f.write(pb)

print("Все исправлено! Запускаем сборку...")
