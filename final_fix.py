import re

# 1. Shared/StaticData.h: добавляем rr_petal_id_yggdrasil
with open("Shared/StaticData.h", "r", encoding="utf-8") as f:
    sd_h = f.read()
if "rr_petal_id_yggdrasil" not in sd_h:
    sd_h = re.sub(
        r'(rr_petal_id_corn,\s*//\s*41\s*\n\s*)(rr_petal_id_max,\s*//\s*42)',
        r'\1rr_petal_id_yggdrasil,      // 42\n    rr_petal_id_max,            // 43',
        sd_h, count=1
    )
    with open("Shared/StaticData.h", "w", encoding="utf-8") as f:
        f.write(sd_h)

# 2. Shared/StaticData.c: данные Yggdrasil + фикс лута огненных муравьев
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

# 3. Server/System/PetalBehavior.c: чистый блок чекпоинта + Yggdrasil через player_info->client->in_squad
with open("Server/System/PetalBehavior.c", "r", encoding="utf-8") as f:
    pb = f.read()

old_ygg = re.compile(
    r'if \(player_info->squad_member && player_info->squad_member->squad_id != 0\).*?\n\s*\}\s*\n\s*\}',
    re.DOTALL
)
new_ygg = """if (player_info->client->in_squad) {
            for (uint64_t s = 0; s < player_info->slot_count; ++s) {
                if (player_info->slots[s].id == rr_petal_id_yggdrasil) {
                    struct rr_squad *sq = &player_info->client->server->squads[player_info->client->squad];
                    for (uint32_t i = 0; i < RR_SQUAD_MEMBER_COUNT; ++i) {
                        struct rr_server_client *mc = sq->members[i].client;
                        if (mc && mc != player_info->client) {
                            mc->has_ygg_teleport = 1;
                            mc->ygg_x = flower_physical->x;
                            mc->ygg_y = flower_physical->y;
                        }
                    }
                    break;
                }
            }
        }
    }"""

pb_new, cnt = old_ygg.subn(new_ygg, pb, count=1)
assert cnt == 1, "Не найден блок Yggdrasil в PetalBehavior.c"
with open("Server/System/PetalBehavior.c", "w", encoding="utf-8") as f:
    f.write(pb_new)

print("Готово! Запускаем полную сборку...")
