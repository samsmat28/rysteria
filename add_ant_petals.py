import re

# 1. Shared/StaticData.h: добавляем 4 лепестка (35..38)
with open("Shared/StaticData.h", "r") as f:
    h = f.read()

if "rr_petal_id_grass" not in h:
    h = re.sub(
        r"(rr_petal_id_rock\s*,[^\n]*\n)\s*rr_petal_id_max\s*,[^\n]*",
        r"""\1    rr_petal_id_grass,               // 35
    rr_petal_id_rice,                // 36
    rr_petal_id_clover,              // 37
    rr_petal_id_light,               // 38

    rr_petal_id_max,                 // 39""",
        h,
        count=1
    )
    with open("Shared/StaticData.h", "w") as f:
        f.write(h)

# 2. Shared/StaticData.c: статы лепестков, имена и дроп обычных муравьёв
with open("Shared/StaticData.c", "r") as f:
    c = f.read()

if "rr_petal_id_grass" not in c:
    c = re.sub(
        r'(\{rr_petal_id_rock\b.*?\},\s*\n)(\};)',
        r"""\1    {rr_petal_id_grass,              rr_rarity_id_common,    defensive,  5.0f,  15.0f, 10.0f,  50,  0, {1,1,1,1,1,1,1}},
    {rr_petal_id_rice,               rr_rarity_id_common,    offensive,  6.0f,   5.0f,  0.0f,   5,  0, {1,1,1,1,1,1,1}},
    {rr_petal_id_clover,             rr_rarity_id_unusual,   defensive,  4.0f,  10.0f,  0.0f,  50,  0, {1,1,1,1,1,1,1}},
    {rr_petal_id_light,              rr_rarity_id_common,    offensive,  8.0f,   6.0f,  0.0f,  15,  0, {1,2,3,3,5,6,6}},
\2""",
        c,
        count=1
    )

    # Имена лепестков (первое вхождение "Rock" в RR_PETAL_NAMES)
    c = c.replace('"Rock"\n};', '"Rock", "Grass", "Rice", "Clover", "Light"\n};', 1)

    # Лут с обычных муравьёв (Worker Ant и Soldier Ant) — ТОЛЬКО Leaf, Grass, Rice, Clover, Light
    c = re.sub(
        r'\{rr_mob_id_worker_ant,.*?\},',
        '{rr_mob_id_worker_ant,       rr_rarity_id_common, rr_rarity_id_ultimate, 22, 10, 18.0f, rr_rarity_id_max, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_leaf, 0.25},{rr_petal_id_grass, 0.25},{rr_petal_id_rice, 0.20},{rr_petal_id_light, 0.20},{rr_petal_id_clover, 0.08}}},',
        c,
        count=1
    )
    c = re.sub(
        r'\{rr_mob_id_soldier_ant,.*?\},',
        '{rr_mob_id_soldier_ant,      rr_rarity_id_common, rr_rarity_id_ultimate, 40, 16, 22.0f, rr_rarity_id_max, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_leaf, 0.25},{rr_petal_id_grass, 0.25},{rr_petal_id_rice, 0.20},{rr_petal_id_light, 0.20},{rr_petal_id_clover, 0.12}}},',
        c,
        count=1
    )

    with open("Shared/StaticData.c", "w") as f:
        f.write(c)

# 3. Server/System/Drops.c: Clover даёт 10x удачу лута при подборе дропа!
with open("Server/System/Drops.c", "r") as f:
    drops = f.read()

old_collect = "->collected_this_run[drop->id * rr_rarity_id_max + drop->rarity] +=100,"
new_collect = """->collected_this_run[drop->id * rr_rarity_id_max + drop->rarity] += (
        (player_info->primary_slots[0].id == rr_petal_id_clover || player_info->primary_slots[1].id == rr_petal_id_clover ||
         player_info->primary_slots[2].id == rr_petal_id_clover || player_info->primary_slots[3].id == rr_petal_id_clover ||
         player_info->primary_slots[4].id == rr_petal_id_clover || player_info->primary_slots[5].id == rr_petal_id_clover ||
         player_info->primary_slots[6].id == rr_petal_id_clover || player_info->primary_slots[7].id == rr_petal_id_clover ||
         player_info->primary_slots[8].id == rr_petal_id_clover || player_info->primary_slots[9].id == rr_petal_id_clover) ? 1000 : 100),"""

if "rr_petal_id_clover" not in drops and old_collect in drops:
    drops = drops.replace(old_collect, new_collect, 1)
    with open("Server/System/Drops.c", "w") as f:
        f.write(drops)

# 4. Client/Assets/RenderPetals.c: отрисовка Grass, Rice, Clover, Light
with open("Client/Assets/RenderPetals.c", "r") as f:
    rp = f.read()

if "rr_petal_id_grass" not in rp:
    petal_cases = """        case rr_petal_id_grass:
            rr_renderer_set_fill(renderer, 0xff49b83d);
            rr_renderer_set_stroke(renderer, 0xff2c7a24);
            rr_renderer_set_line_width(renderer, 3);
            rr_renderer_begin_path(renderer);
            rr_renderer_move_to(renderer, -12, 8);
            rr_renderer_line_to(renderer, 0, -14);
            rr_renderer_line_to(renderer, 12, 8);
            rr_renderer_line_to(renderer, 0, 3);
            rr_renderer_line_to(renderer, -12, 8);
            rr_renderer_fill(renderer);
            rr_renderer_stroke(renderer);
            break;

        case rr_petal_id_rice:
            rr_renderer_set_fill(renderer, 0xfff7f5eb);
            rr_renderer_set_stroke(renderer, 0xffcfc9b4);
            rr_renderer_set_line_width(renderer, 3);
            rr_renderer_begin_path(renderer);
            rr_renderer_arc(renderer, -4, 0, 7);
            rr_renderer_arc(renderer, 4, 0, 7);
            rr_renderer_fill(renderer);
            rr_renderer_stroke(renderer);
            break;

        case rr_petal_id_clover:
            rr_renderer_set_fill(renderer, 0xff38c948);
            rr_renderer_set_stroke(renderer, 0xff1e8229);
            rr_renderer_set_line_width(renderer, 2.5f);
            rr_renderer_begin_path(renderer);
            rr_renderer_arc(renderer, -6, -6, 6.5f);
            rr_renderer_arc(renderer, 6, -6, 6.5f);
            rr_renderer_arc(renderer, -6, 6, 6.5f);
            rr_renderer_arc(renderer, 6, 6, 6.5f);
            rr_renderer_fill(renderer);
            rr_renderer_stroke(renderer);
            break;

        case rr_petal_id_light:
            rr_renderer_set_fill(renderer, 0xfffff8c9);
            rr_renderer_set_stroke(renderer, 0xffe6d88a);
            rr_renderer_set_line_width(renderer, 2.5f);
            rr_renderer_begin_path(renderer);
            rr_renderer_arc(renderer, 0, 0, 8);
            rr_renderer_fill(renderer);
            rr_renderer_stroke(renderer);
            break;

        case rr_petal_id_rock:"""
    rp = rp.replace("        case rr_petal_id_rock:", petal_cases, 1)
    with open("Client/Assets/RenderPetals.c", "w") as f:
        f.write(rp)

print("4 лепестка (Grass, Rice, Clover 10x, Light) и лут муравьёв готовы!")
