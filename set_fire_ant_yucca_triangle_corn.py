import re

# 1. Shared/StaticData.h: заменяем bur/wing на triangle и corn (ID 40, 41)
with open("Shared/StaticData.h", "r") as f:
    h = f.read()

h = h.replace("rr_petal_id_bur,", "rr_petal_id_triangle,")
h = h.replace("rr_petal_id_wing,", "rr_petal_id_corn,")
with open("Shared/StaticData.h", "w") as f:
    f.write(h)

# 2. Shared/StaticData.c: статы Yucca, Triangle, Corn + лут красных (огненных) муравьёв
with open("Shared/StaticData.c", "r") as f:
    c = f.read()

c = re.sub(
    r'\{rr_petal_id_bur,.*?\n',
    '    {rr_petal_id_triangle,           rr_rarity_id_unusual,   offensive, 14.0f,   6.0f,  0.0f,  30,  0, {1,1,1,1,1,1,1}},\n',
    c
)
c = re.sub(
    r'\{rr_petal_id_wing,.*?\n',
    '    {rr_petal_id_corn,               rr_rarity_id_common,    offensive, 12.0f,  65.0f,  0.0f,  35,  0, {1,1,1,1,1,1,1}},\n',
    c
)
c = c.replace('"Light", "Yucca", "Bur", "Wing"', '"Light", "Yucca", "Triangle", "Corn"')

# Лут огненных (красных) муравьёв — ТОЛЬКО Yucca, Triangle, Corn
c = re.sub(
    r'\{rr_mob_id_fire_worker_ant,.*?\n',
    '    {rr_mob_id_fire_worker_ant,  rr_rarity_id_common, rr_rarity_id_ultimate, 30, 14, 27.0f, rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_yucca, 0.35},{rr_petal_id_corn, 0.30},{rr_petal_id_triangle, 0.20}}},\n',
    c
)
c = re.sub(
    r'\{rr_mob_id_fire_soldier_ant,.*?\n',
    '    {rr_mob_id_fire_soldier_ant, rr_rarity_id_common, rr_rarity_id_ultimate, 55, 22, 32.0f, rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_triangle, 0.35},{rr_petal_id_corn, 0.30},{rr_petal_id_yucca, 0.25}}},\n',
    c
)
c = re.sub(
    r'\{rr_mob_id_fire_ant_egg,.*?\n',
    '    {rr_mob_id_fire_ant_egg,     rr_rarity_id_common, rr_rarity_id_ultimate, 24,  0, 25.0f, rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_yucca, 0.35},{rr_petal_id_corn, 0.30},{rr_petal_id_triangle, 0.20}}},\n',
    c
)
c = re.sub(
    r'\{rr_mob_id_queen_fire_ant,.*?\n',
    '    {rr_mob_id_queen_fire_ant,   rr_rarity_id_common, rr_rarity_id_ultimate, 4500, 45, 190.0f, rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_triangle, 0.70},{rr_petal_id_corn, 0.70},{rr_petal_id_yucca, 0.70}}},\n',
    c
)

with open("Shared/StaticData.c", "w") as f:
    f.write(c)

# 3. Механика Triangle (как в florr.io: чем больше Triangle экипировано, тем выше их урон) в Server/System/Health.c
with open("Server/System/Health.c", "r") as f:
    hc = f.read()

triangle_bonus = """
    // Механика Triangle из florr.io: каждый дополнительный Triangle в слотах увеличивает урон Triangle на +50%
    if (rr_simulation_has_petal(this, attacker))
    {
        struct rr_component_petal *p = rr_simulation_get_petal(this, attacker);
        struct rr_component_relations *rel = rr_simulation_get_relations(this, attacker);
        if (p && p->id == rr_petal_id_triangle && rel)
        {
            EntityIdx owner = rr_simulation_resolve_entity_hash(this, rel->owner);
            if (owner != RR_NULL_ENTITY && rr_simulation_has_player_info(this, owner))
            {
                struct rr_component_player_info *pi = rr_simulation_get_player_info(this, owner);
                int tri_count = 0;
                for (int s = 0; s < 10; ++s)
                    if (pi->slots[s].id == rr_petal_id_triangle) tri_count++;
                if (tri_count > 1)
                    damage *= (1.0f + 0.5f * (tri_count - 1));
            }
        }
    }
"""

if "rr_petal_id_triangle" not in hc and "float damage =" in hc:
    hc = hc.replace("float damage =", triangle_bonus + "\n    float damage =", 1)
    with open("Server/System/Health.c", "w") as f:
        f.write(hc)

# 4. Client/Assets/RenderPetals.c: иконки Triangle (оранжево-красный треугольник) и Corn (жёлтый початок)
with open("Client/Assets/RenderPetals.c", "r") as f:
    rp = f.read()

old_bur_wing = re.search(r'    case rr_petal_id_bur:.*?    case rr_petal_id_rock:', rp, flags=re.DOTALL)
if old_bur_wing:
    new_icons = """    case rr_petal_id_triangle:
        rr_renderer_set_fill(renderer, 0xffd94e34);
        rr_renderer_set_stroke(renderer, 0xff8c2816);
        rr_renderer_set_line_width(renderer, 3.5f);
        rr_renderer_begin_path(renderer);
        rr_renderer_move_to(renderer, 0, -13);
        rr_renderer_line_to(renderer, 12, 10);
        rr_renderer_line_to(renderer, -12, 10);
        rr_renderer_line_to(renderer, 0, -13);
        rr_renderer_fill(renderer);
        rr_renderer_stroke(renderer);
        break;

    case rr_petal_id_corn:
        rr_renderer_set_fill(renderer, 0xfff5d13d);
        rr_renderer_set_stroke(renderer, 0xffb89614);
        rr_renderer_set_line_width(renderer, 3.5f);
        rr_renderer_begin_path(renderer);
        rr_renderer_arc(renderer, -3, -3, 7.5f);
        rr_renderer_arc(renderer, 3, 3, 7.5f);
        rr_renderer_fill(renderer);
        rr_renderer_stroke(renderer);
        break;

    case rr_petal_id_rock:"""
    rp = rp[:old_bur_wing.start()] + new_icons + rp[old_bur_wing.end():]
    with open("Client/Assets/RenderPetals.c", "w") as f:
        f.write(rp)

print("Лут красных муравьёв (Yucca, Triangle с механикой florr.io, Corn) готов!")
