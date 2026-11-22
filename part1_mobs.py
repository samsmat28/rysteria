import re

with open("Shared/StaticData.h", "r") as f:
    h_code = f.read()
old_enum = """    rr_mob_id_rock,                  // 22

    rr_mob_id_max,                   // 23"""
new_enum = """    rr_mob_id_rock,                  // 22
    rr_mob_id_worker_ant,            // 23
    rr_mob_id_soldier_ant,           // 24
    rr_mob_id_fire_worker_ant,       // 25
    rr_mob_id_fire_soldier_ant,      // 26
    rr_mob_id_termite_worker,        // 27
    rr_mob_id_termite_soldier,       // 28
    rr_mob_id_worm,                  // 29

    rr_mob_id_max,                   // 30"""
if "rr_mob_id_worker_ant" not in h_code:
    h_code = h_code.replace(old_enum, new_enum, 1)
    with open("Shared/StaticData.h", "w") as f: f.write(h_code)

with open("Shared/StaticData.c", "r") as f:
    c_code = f.read()
if "rr_mob_id_worker_ant" not in c_code:
    old_data = """    {rr_mob_id_rock,        rr_rarity_id_common, rr_rarity_id_ultimate, 150, 10, 38.0f, rr_rarity_id_max, rr_rarity_id_max, rr_rarity_id_max, {{rr_petal_id_rock, 0.35},{rr_petal_id_magnet, 0.25}}},
};"""
    new_data = """    {rr_mob_id_rock,        rr_rarity_id_common, rr_rarity_id_ultimate, 150, 10, 38.0f, rr_rarity_id_max, rr_rarity_id_max, rr_rarity_id_max, {{rr_petal_id_rock, 0.35},{rr_petal_id_magnet, 0.25}}},
    {rr_mob_id_worker_ant,       rr_rarity_id_common, rr_rarity_id_ultimate, 22, 10, 18.0f, rr_rarity_id_max, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_leaf, 0.20},{rr_petal_id_pellet, 0.15}}},
    {rr_mob_id_soldier_ant,      rr_rarity_id_common, rr_rarity_id_ultimate, 40, 16, 22.0f, rr_rarity_id_max, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_mandible, 0.20},{rr_petal_id_leaf, 0.15}}},
    {rr_mob_id_fire_worker_ant,  rr_rarity_id_common, rr_rarity_id_ultimate, 30, 14, 19.0f, rr_rarity_id_max, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_stinger, 0.20},{rr_petal_id_pellet, 0.15}}},
    {rr_mob_id_fire_soldier_ant, rr_rarity_id_common, rr_rarity_id_ultimate, 55, 22, 23.0f, rr_rarity_id_max, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_mandible, 0.25},{rr_petal_id_stinger, 0.15}}},
    {rr_mob_id_termite_worker,   rr_rarity_id_common, rr_rarity_id_ultimate, 28, 12, 19.0f, rr_rarity_id_max, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_sand, 0.20},{rr_petal_id_pellet, 0.15}}},
    {rr_mob_id_termite_soldier,  rr_rarity_id_common, rr_rarity_id_ultimate, 50, 20, 23.0f, rr_rarity_id_max, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_mandible, 0.25},{rr_petal_id_sand, 0.15}}},
    {rr_mob_id_worm,             rr_rarity_id_common, rr_rarity_id_ultimate, 45, 24, 21.0f, rr_rarity_id_max, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_sand, 0.25},{rr_petal_id_peas, 0.15}}},
};"""
    c_code = c_code.replace(old_data, new_data, 1)
    c_code = re.sub(r'("Rock"\s*,?\s*\n\s*\};)', '"Rock", "Worker Ant", "Soldier Ant", "Fire Worker Ant", "Fire Soldier Ant", "Termite Worker", "Termite Soldier", "Worm"\n};', c_code, count=1)
    c_code = c_code.replace("    45,  //rock\n};", "    45,  //rock\n    0, 0, 0, 0, 0, 0, 0\n};", 1)
    with open("Shared/StaticData.c", "w") as f: f.write(c_code)

with open("Server/Waves.c", "r") as f: w = f.read()
if "rr_mob_id_worker_ant" not in w:
    w = w.replace("uint8_t get_spawn_id(uint8_t biome, struct rr_maze_grid *zone)\n{", """uint8_t get_spawn_id(uint8_t biome, struct rr_maze_grid *zone)
{
    if (biome == rr_biome_id_pvp)
    {
        double r_ant = rr_frand();
        if (r_ant < 0.22) return rr_mob_id_worker_ant;
        if (r_ant < 0.38) return rr_mob_id_soldier_ant;
        if (r_ant < 0.56) return rr_mob_id_fire_worker_ant;
        if (r_ant < 0.70) return rr_mob_id_fire_soldier_ant;
        if (r_ant < 0.84) return rr_mob_id_termite_worker;
        if (r_ant < 0.94) return rr_mob_id_termite_soldier;
        return rr_mob_id_worm;
    }""", 1)
    with open("Server/Waves.c", "w") as f: f.write(w)

with open("Server/Simulation.c", "r") as f: s = f.read()
s = re.sub(r"if\s*\(\s*this->biome\s*==\s*rr_biome_id_pvp\s*\)\s*return\s*0\s*;", "// Ant Hell spawn", s)
with open("Server/Simulation.c", "w") as f: f.write(s)

with open("Server/EntityAllocation.c", "r") as f: a = f.read()
if "rr_mob_id_worm" not in a:
    a = a.replace("else if (mob_id == rr_mob_id_house_centipede)", "else if (mob_id == rr_mob_id_house_centipede || mob_id == rr_mob_id_worm)")
    with open("Server/EntityAllocation.c", "w") as f: f.write(a)

print("PART 1 OK")
