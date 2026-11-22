import re

# 1. Shared/StaticData.c:
# - Увеличиваем здоровье Королев в 10x (3500, 4500, 4000)
# - Делаем лут Королев = лепесток Egg (rr_petal_id_egg)
# - Увеличиваем хитбокс малышей (рабочих, солдат и яиц) на ~40%
with open("Shared/StaticData.c", "r") as f:
    c = f.read()

# Малыши (рабочие, солдаты, яйца) -> крупнее радиус
c = c.replace("{rr_mob_id_worker_ant,       rr_rarity_id_common, rr_rarity_id_ultimate, 22, 10, 18.0f,",
              "{rr_mob_id_worker_ant,       rr_rarity_id_common, rr_rarity_id_ultimate, 22, 10, 26.0f,")
c = c.replace("{rr_mob_id_soldier_ant,      rr_rarity_id_common, rr_rarity_id_ultimate, 40, 16, 22.0f,",
              "{rr_mob_id_soldier_ant,      rr_rarity_id_common, rr_rarity_id_ultimate, 40, 16, 31.0f,")
c = c.replace("{rr_mob_id_fire_worker_ant,  rr_rarity_id_common, rr_rarity_id_ultimate, 30, 14, 19.0f,",
              "{rr_mob_id_fire_worker_ant,  rr_rarity_id_common, rr_rarity_id_ultimate, 30, 14, 27.0f,")
c = c.replace("{rr_mob_id_fire_soldier_ant, rr_rarity_id_common, rr_rarity_id_ultimate, 55, 22, 23.0f,",
              "{rr_mob_id_fire_soldier_ant, rr_rarity_id_common, rr_rarity_id_ultimate, 55, 22, 32.0f,")
c = c.replace("{rr_mob_id_termite_worker,   rr_rarity_id_common, rr_rarity_id_ultimate, 28, 12, 19.0f,",
              "{rr_mob_id_termite_worker,   rr_rarity_id_common, rr_rarity_id_ultimate, 28, 12, 27.0f,")
c = c.replace("{rr_mob_id_termite_soldier,  rr_rarity_id_common, rr_rarity_id_ultimate, 50, 20, 23.0f,",
              "{rr_mob_id_termite_soldier,  rr_rarity_id_common, rr_rarity_id_ultimate, 50, 20, 32.0f,")
c = c.replace("{rr_mob_id_ant_egg,          rr_rarity_id_common, rr_rarity_id_ultimate, 18,  0, 16.0f,",
              "{rr_mob_id_ant_egg,          rr_rarity_id_common, rr_rarity_id_ultimate, 18,  0, 24.0f,")
c = c.replace("{rr_mob_id_fire_ant_egg,     rr_rarity_id_common, rr_rarity_id_ultimate, 24,  0, 17.0f,",
              "{rr_mob_id_fire_ant_egg,     rr_rarity_id_common, rr_rarity_id_ultimate, 24,  0, 25.0f,")
c = c.replace("{rr_mob_id_termite_egg,      rr_rarity_id_common, rr_rarity_id_ultimate, 22,  0, 17.0f,",
              "{rr_mob_id_termite_egg,      rr_rarity_id_common, rr_rarity_id_ultimate, 22,  0, 25.0f,")

# Королевы: HP x10 и лут ТОЛЬКО яйца (rr_petal_id_egg)
c = re.sub(
    r'\{rr_mob_id_queen_ant,.*?\n',
    '    {rr_mob_id_queen_ant,        rr_rarity_id_common, rr_rarity_id_ultimate, 3500, 35, 185.0f, rr_rarity_id_max, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_egg, 0.85}}},\n',
    c
)
c = re.sub(
    r'\{rr_mob_id_queen_fire_ant,.*?\n',
    '    {rr_mob_id_queen_fire_ant,   rr_rarity_id_common, rr_rarity_id_ultimate, 4500, 45, 190.0f, rr_rarity_id_max, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_egg, 0.85}}},\n',
    c
)
c = re.sub(
    r'\{rr_mob_id_queen_termite,.*?\n',
    '    {rr_mob_id_queen_termite,    rr_rarity_id_common, rr_rarity_id_ultimate, 4000, 40, 185.0f, rr_rarity_id_max, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_egg, 0.85}}},\n',
    c
)

with open("Shared/StaticData.c", "w") as f:
    f.write(c)

# 2. Server/Waves.c: делаем всех 3 Королев редкими (~3% суммарно)
with open("Server/Waves.c", "r") as f:
    w = f.read()

old_rates = """        if (r_ant < 0.80) return rr_mob_id_termite_egg;
        if (r_ant < 0.87) return rr_mob_id_queen_ant;
        if (r_ant < 0.94) return rr_mob_id_queen_fire_ant;
        return rr_mob_id_queen_termite;"""

new_rates = """        if (r_ant < 0.97) return rr_mob_id_termite_egg;
        if (r_ant < 0.98) return rr_mob_id_queen_ant;
        if (r_ant < 0.99) return rr_mob_id_queen_fire_ant;
        return rr_mob_id_queen_termite;"""

if old_rates in w:
    w = w.replace(old_rates, new_rates, 1)
    with open("Server/Waves.c", "w") as f:
        f.write(w)

# 3. Client/Assets/RenderMobs.c: визуально увеличиваем малышей и яйца (~1.45x)
with open("Client/Assets/RenderMobs.c", "r") as f:
    rm = f.read()

old_ant_render = """    case rr_mob_id_worker_ant: case rr_mob_id_soldier_ant: case rr_mob_id_fire_worker_ant: case rr_mob_id_fire_soldier_ant: case rr_mob_id_termite_worker: case rr_mob_id_termite_soldier: case rr_mob_id_worm:
        render_sprite(renderer, id, 0, flags);
        break;"""

new_ant_render = """    case rr_mob_id_worker_ant: case rr_mob_id_soldier_ant: case rr_mob_id_fire_worker_ant: case rr_mob_id_fire_soldier_ant: case rr_mob_id_termite_worker: case rr_mob_id_termite_soldier: case rr_mob_id_worm:
        rr_renderer_scale(renderer, 1.45f);
        render_sprite(renderer, id, 0, flags);
        break;"""

if old_ant_render in rm:
    rm = rm.replace(old_ant_render, new_ant_render, 1)

rm = rm.replace(
    "    case rr_mob_id_termite_egg:\n        rr_renderer_scale(renderer, 0.25f);",
    "    case rr_mob_id_termite_egg:\n        rr_renderer_scale(renderer, 0.36f);",
    1
)

with open("Client/Assets/RenderMobs.c", "w") as f:
    f.write(rm)

print("Готово: Королевы x10 HP, редкие и роняют Egg; малыши увеличены!")
