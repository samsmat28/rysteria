# 1. Чуть уменьшаем скорость появления мобов в Server/Simulation.c (/ 15.0f -> / 9.0f)
with open("Server/Simulation.c", "r") as f:
    sim = f.read()

sim = sim.replace("(150 + 3 * grid->difficulty) / 15.0f;", "(150 + 3 * grid->difficulty) / 9.0f;", 1)
with open("Server/Simulation.c", "w") as f:
    f.write(sim)

# 2. Гарантируем выпадение лепестка Egg (rr_petal_id_egg) со всех 3 Королев в Shared/StaticData.c
with open("Shared/StaticData.c", "r") as f:
    c = f.read()

c = c.replace("rr_rarity_id_max, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_egg, 0.85}}",
              "rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_egg, 1.0}}")
with open("Shared/StaticData.c", "w") as f:
    f.write(c)

print("Спавн мобов уменьшен, а 100% дроп Egg с Королев прописан!")
