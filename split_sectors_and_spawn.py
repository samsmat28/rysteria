import re

# 1. Разделяем Ant Hell по секторам в Server/Waves.c
with open("Server/Waves.c", "r") as f:
    w = f.read()

new_pvp_block = """    if (biome == rr_biome_id_pvp)
    {
        // Вычисляем координаты клетки (0..159, 0..159) в сетке Ant Hell
        ptrdiff_t idx = zone - &RR_MAZE_PVP[0][0];
        int gx = (idx >= 0 && idx < 160 * 160) ? (int)(idx % 160) : 80;
        int gy = (idx >= 0 && idx < 160 * 160) ? (int)(idx / 160) : 24;
        double r_ant = rr_frand();

        // Сектор 4 (Нижний глубокий зал): Черви (Worm) и редкая Королева
        if (gy >= 124)
        {
            if (r_ant < 0.94) return rr_mob_id_worm;
            if (r_ant < 0.96) return rr_mob_id_queen_ant;
            if (r_ant < 0.98) return rr_mob_id_queen_fire_ant;
            return rr_mob_id_queen_termite;
        }
        // Сектор 1 (Верхний зал входа): ТОЛЬКО обычные муравьи
        if (gy < 44)
        {
            if (r_ant < 0.55) return rr_mob_id_worker_ant;
            if (r_ant < 0.88) return rr_mob_id_soldier_ant;
            if (r_ant < 0.98) return rr_mob_id_ant_egg;
            return rr_mob_id_queen_ant;
        }
        // Сектор 2 (Правая половина): ТОЛЬКО огненные муравьи
        if (gx >= 80)
        {
            if (r_ant < 0.55) return rr_mob_id_fire_worker_ant;
            if (r_ant < 0.88) return rr_mob_id_fire_soldier_ant;
            if (r_ant < 0.98) return rr_mob_id_fire_ant_egg;
            return rr_mob_id_queen_fire_ant;
        }
        // Сектор 3 (Левая половина): ТОЛЬКО термиты
        if (r_ant < 0.55) return rr_mob_id_termite_worker;
        if (r_ant < 0.88) return rr_mob_id_termite_soldier;
        if (r_ant < 0.98) return rr_mob_id_termite_egg;
        return rr_mob_id_queen_termite;
    }"""

w = re.sub(
    r'    if \(biome == rr_biome_id_pvp\)\s*\{.*?\n    \}',
    new_pvp_block,
    w,
    count=1,
    flags=re.DOTALL
)

with open("Server/Waves.c", "w") as f:
    f.write(w)

# 2. Уменьшаем спавн мобов ещё в 2.5 раза в Server/Simulation.c (/ 9.0f -> / 3.5f)
with open("Server/Simulation.c", "r") as f:
    sim = f.read()

sim = sim.replace("(150 + 3 * grid->difficulty) / 9.0f;", "(150 + 3 * grid->difficulty) / 3.5f;", 1)
with open("Server/Simulation.c", "w") as f:
    f.write(sim)

print("Сектора Ant Hell разделены, а спавн мобов уменьшен в 2.5 раза!")
