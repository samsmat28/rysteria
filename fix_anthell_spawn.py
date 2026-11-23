import re

with open("Shared/StaticData.c", "r", encoding="utf-8") as f:
    sdata = f.read()

maze_match = re.search(r'RR_DEFINE_MAZE\(PVP,\s*160\)\s*=\s*\{(.*?)\n\};', sdata, re.DOTALL)
rows = re.findall(r'\{([^}]+)\}', maze_match.group(1))
c_coords = []
for y, r in enumerate(rows):
    tokens = [t.strip() for t in r.split(',') if t.strip()]
    for x, tok in enumerate(tokens):
        if tok == 'c':
            c_coords.append((x, y))

avg_x = sum(x for x, y in c_coords) / len(c_coords)
avg_y = sum(y for x, y in c_coords) / len(c_coords)
spawn_x, spawn_y = min(c_coords, key=lambda pt: (pt[0] - avg_x)**2 + (pt[1] - avg_y)**2)
print(f"Точка спавна в зеленой зоне Common: x={spawn_x}, y={spawn_y}")

with open("Server/Simulation.c", "r", encoding="utf-8") as f:
    sim = f.read()

target = "set_respawn_zone(arena, SPAWN_ZONE_X, SPAWN_ZONE_Y);"
replacement = f"""if (RR_GLOBAL_BIOME == rr_biome_id_pvp)
        set_respawn_zone(arena, {spawn_x}, {spawn_y});
    else
        set_respawn_zone(arena, SPAWN_ZONE_X, SPAWN_ZONE_Y);"""

if "RR_GLOBAL_BIOME == rr_biome_id_pvp" not in sim:
    sim = sim.replace(target, replacement, 1)
    with open("Server/Simulation.c", "w", encoding="utf-8") as f:
        f.write(sim)
    print("Server/Simulation.c успешно обновлен!")
