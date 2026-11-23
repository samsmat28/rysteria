with open("Shared/StaticData.c", "r", encoding="utf-8") as f:
    sdata = f.read()

replacements = [
    (
        "{rr_mob_id_worm,             rr_rarity_id_common, rr_rarity_id_gods, 45, 24, 21.0f, rr_rarity_id_max, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_sand, 0.25},{rr_petal_id_peas, 0.15}}},",
        "{rr_mob_id_worm,             rr_rarity_id_common, rr_rarity_id_gods, 45, 24, 21.0f, rr_rarity_id_max, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_sand, 0.35},{rr_petal_id_peas, 0.25},{rr_petal_id_gravel, 0.20},{rr_petal_id_bone, 0.15}}},"
    ),
    (
        "{rr_mob_id_queen_ant,        rr_rarity_id_common, rr_rarity_id_gods, 3500, 35, 185.0f, rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_egg, 1.0}}},",
        "{rr_mob_id_queen_ant,        rr_rarity_id_common, rr_rarity_id_gods, 3500, 35, 185.0f, rr_rarity_id_max, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_egg, 1.0},{rr_petal_id_clover, 0.60},{rr_petal_id_light, 0.75},{rr_petal_id_leaf, 0.85}}},"
    ),
    (
        "{rr_mob_id_queen_fire_ant,   rr_rarity_id_common, rr_rarity_id_gods, 4500, 45, 190.0f, rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_triangle, 0.70},{rr_petal_id_corn, 0.70},{rr_petal_id_yucca, 0.70}}},",
        "{rr_mob_id_queen_fire_ant,   rr_rarity_id_common, rr_rarity_id_gods, 4500, 45, 190.0f, rr_rarity_id_max, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_triangle, 0.85},{rr_petal_id_corn, 0.85},{rr_petal_id_yucca, 0.85},{rr_petal_id_egg, 0.70}}},"
    ),
    (
        "{rr_mob_id_queen_termite,    rr_rarity_id_common, rr_rarity_id_gods, 4000, 40, 185.0f, rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_bone, 0.70},{rr_petal_id_mandible, 0.70},{rr_petal_id_egg, 0.85}}},",
        "{rr_mob_id_queen_termite,    rr_rarity_id_common, rr_rarity_id_gods, 4000, 40, 185.0f, rr_rarity_id_max, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_egg, 0.95},{rr_petal_id_bone, 0.85},{rr_petal_id_mandible, 0.85},{rr_petal_id_sand, 0.80}}},"
    ),
]

for old, new in replacements:
    assert old in sdata, f"Не найдена строка: {old[:50]}"
    sdata = sdata.replace(old, new, 1)

with open("Shared/StaticData.c", "w", encoding="utf-8") as f:
    f.write(sdata)
print("Лут Королев и Червя (Worm) успешно обновлен!")
