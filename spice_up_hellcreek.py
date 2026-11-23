with open("Server/Simulation.c", "r", encoding="utf-8") as f:
    sim = f.read()

# Делаем плотность мобов комфортной (0.75 вместо 0.45) и спавн в 2 раза живее (2.2f вместо 4.5f)
sim = sim.replace("get_max_points(this, grid) * 0.45f;", "get_max_points(this, grid) * 0.75f;", 1)
sim = sim.replace("spawn_at *= 4.5f;", "spawn_at *= 2.2f;", 1)

with open("Server/Simulation.c", "w", encoding="utf-8") as f:
    f.write(sim)

with open("Server/Waves.c", "r", encoding="utf-8") as f:
    waves = f.read()

old_block = """        if (diff <= 24.0f)
        {
            if (r < 0.22) return rr_mob_id_triceratops;"""

new_block = """        // 12% шанс на элитного мини-босса (T-Rex или Meteor) в любой зоне!
        if (r < 0.07) return rr_mob_id_trex;
        if (r < 0.12) return rr_mob_id_meteor;
        if (diff <= 24.0f)
        {
            if (r < 0.30) return rr_mob_id_triceratops;"""

assert old_block in waves, "Не найден блок Hell Creek в Server/Waves.c"
waves = waves.replace(old_block, new_block, 1)

with open("Server/Waves.c", "w", encoding="utf-8") as f:
    f.write(waves)

print("Темп спавна и элитные мини-боссы в Hell Creek обновлены!")
