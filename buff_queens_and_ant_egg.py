import re

# 1. Увеличиваем радиус Королев в 5 раз в Shared/StaticData.c + добавляем rr_petal_id_egg в дроп Яиц и Королев
with open("Shared/StaticData.c", "r") as f:
    c = f.read()

c = c.replace("{rr_mob_id_ant_egg,          rr_rarity_id_common, rr_rarity_id_ultimate, 18,  0, 16.0f,",
              "{rr_mob_id_ant_egg,          rr_rarity_id_common, rr_rarity_id_ultimate, 18,  0, 16.0f,")
c = c.replace("{rr_mob_id_queen_ant,        rr_rarity_id_common, rr_rarity_id_ultimate, 140, 28, 36.0f,",
              "{rr_mob_id_queen_ant,        rr_rarity_id_common, rr_rarity_id_ultimate, 350, 35, 185.0f,")
c = c.replace("{rr_mob_id_queen_fire_ant,   rr_rarity_id_common, rr_rarity_id_ultimate, 180, 36, 38.0f,",
              "{rr_mob_id_queen_fire_ant,   rr_rarity_id_common, rr_rarity_id_ultimate, 450, 45, 190.0f,")
c = c.replace("{rr_mob_id_queen_termite,    rr_rarity_id_common, rr_rarity_id_ultimate, 165, 32, 37.0f,",
              "{rr_mob_id_queen_termite,    rr_rarity_id_common, rr_rarity_id_ultimate, 400, 40, 185.0f,")

# Добавляем rr_petal_id_egg в лут Яиц, Королев и Солдат Ant Hell
c = c.replace("{{rr_petal_id_clover, 0.40},{rr_petal_id_rice, 0.35}}",
              "{{rr_petal_id_egg, 0.50},{rr_petal_id_clover, 0.40},{rr_petal_id_rice, 0.35}}")
c = c.replace("{{rr_petal_id_mandible, 0.40},{rr_petal_id_stinger, 0.35}}",
              "{{rr_petal_id_egg, 0.50},{rr_petal_id_mandible, 0.40},{rr_petal_id_stinger, 0.35}}")
c = c.replace("{{rr_petal_id_mandible, 0.40},{rr_petal_id_sand, 0.35}}",
              "{{rr_petal_id_egg, 0.50},{rr_petal_id_mandible, 0.40},{rr_petal_id_sand, 0.35}}")
c = c.replace("{{rr_petal_id_leaf, 0.25},{rr_petal_id_clover, 0.10}}",
              "{{rr_petal_id_egg, 0.35},{rr_petal_id_leaf, 0.25},{rr_petal_id_clover, 0.10}}")
c = c.replace("{{rr_petal_id_stinger, 0.25},{rr_petal_id_pellet, 0.15}}",
              "{{rr_petal_id_egg, 0.35},{rr_petal_id_stinger, 0.25},{rr_petal_id_pellet, 0.15}}")
c = c.replace("{{rr_petal_id_sand, 0.25},{rr_petal_id_pellet, 0.15}}",
              "{{rr_petal_id_egg, 0.35},{rr_petal_id_sand, 0.25},{rr_petal_id_pellet, 0.15}}")

with open("Shared/StaticData.c", "w") as f:
    f.write(c)

# 2. Переключаем вылупление из лепестка Egg (rr_petal_id_egg) на дружелюбного Soldier Ant в Server/System/PetalBehavior.c
with open("Server/System/PetalBehavior.c", "r") as f:
    pb = f.read()

pb = pb.replace("m_id = rr_mob_id_trex;", "m_id = rr_mob_id_soldier_ant;")
with open("Server/System/PetalBehavior.c", "w") as f:
    f.write(pb)

# 3. Увеличиваем визуальный размер Королев в 5 раз в Client/Assets/RenderMobs.c
with open("Client/Assets/RenderMobs.c", "r") as f:
    rm = f.read()

old_queen_draw = """    case rr_mob_id_queen_ant:
    case rr_mob_id_queen_fire_ant:
    case rr_mob_id_queen_termite:
    {
        uint8_t base_id = (id == rr_mob_id_queen_ant) ? rr_mob_id_soldier_ant : ((id == rr_mob_id_queen_fire_ant) ? rr_mob_id_fire_soldier_ant : rr_mob_id_termite_soldier);
        render_sprite(renderer, base_id, 0, flags);
        rr_renderer_scale(renderer, 0.25f);"""

new_queen_draw = """    case rr_mob_id_queen_ant:
    case rr_mob_id_queen_fire_ant:
    case rr_mob_id_queen_termite:
    {
        rr_renderer_scale(renderer, 5.0f);
        uint8_t base_id = (id == rr_mob_id_queen_ant) ? rr_mob_id_soldier_ant : ((id == rr_mob_id_queen_fire_ant) ? rr_mob_id_fire_soldier_ant : rr_mob_id_termite_soldier);
        render_sprite(renderer, base_id, 0, flags);
        rr_renderer_scale(renderer, 0.25f);"""

assert old_queen_draw in rm, "Не найден блок отрисовки Королев!"
rm = rm.replace(old_queen_draw, new_queen_draw, 1)
with open("Client/Assets/RenderMobs.c", "w") as f:
    f.write(rm)

print("Королевы x5 и лепесток Egg с питомцем-муравьём готовы!")
