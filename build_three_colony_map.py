import re

W, H = 160, 160
grid = [['#' for _ in range(W)] for _ in range(H)]

def carve_circle(cx, cy, r, val):
    for y in range(max(3, cy - r), min(H - 3, cy + r + 1)):
        for x in range(max(3, cx - r), min(W - 3, cx + r + 1)):
            if (x - cx)**2 + (y - cy)**2 <= r**2:
                grid[y][x] = val

def carve_tunnel(x1, y1, x2, y2, r, val):
    steps = max(abs(x2 - x1), abs(y2 - y1), 1)
    for i in range(steps + 1):
        t = i / steps
        cx = int(round(x1 + (x2 - x1) * t))
        cy = int(round(y1 + (y2 - y1) * t))
        carve_circle(cx, cy, r, val)

# 1. Центральный перекрёсток (вход игрока)
carve_circle(80, 74, 14, 'c')

# 2. Северное крыло (Верх) — Обычные муравьи (Common -> Rare -> Epic -> Legendary)
carve_tunnel(80, 74, 80, 52, 6, 'c')
carve_circle(80, 48, 13, 'c')
carve_tunnel(80, 48, 56, 30, 6, 'r')
carve_tunnel(80, 48, 104, 30, 6, 'r')
carve_circle(54, 28, 13, 'r')
carve_circle(106, 28, 13, 'r')
carve_tunnel(54, 28, 80, 16, 6, 'e')
carve_tunnel(106, 28, 80, 16, 6, 'e')
carve_circle(80, 16, 14, 'l') # Тронный зал Queen Ant

# 3. Юго-Западное крыло (Низ-Лево) — Огненные муравьи
carve_tunnel(80, 74, 54, 92, 6, 'c')
carve_circle(50, 95, 13, 'r')
carve_tunnel(50, 95, 24, 102, 6, 'e')
carve_tunnel(50, 95, 44, 126, 6, 'e')
carve_circle(22, 104, 13, 'e')
carve_circle(42, 128, 13, 'l')
carve_tunnel(22, 104, 20, 136, 6, 'l')
carve_tunnel(42, 128, 20, 136, 6, 'l')
carve_circle(20, 136, 15, 'm') # Тронный зал Queen Fire Ant

# 4. Юго-Восточное крыло (Низ-Право) — Термиты
carve_tunnel(80, 74, 106, 92, 6, 'c')
carve_circle(110, 95, 13, 'r')
carve_tunnel(110, 95, 136, 102, 6, 'e')
carve_tunnel(110, 95, 116, 126, 6, 'e')
carve_circle(138, 104, 13, 'e')
carve_circle(118, 128, 13, 'l')
carve_tunnel(138, 104, 140, 136, 6, 'l')
carve_tunnel(118, 128, 140, 136, 6, 'l')
carve_circle(140, 136, 15, 'm') # Тронный зал Queen Termite

# 5. Глубокая центральная шахта (Самый низ) — Логово Червей (Worm)
carve_tunnel(80, 74, 80, 114, 5, 'e')
carve_circle(80, 118, 12, 'l')
carve_tunnel(80, 118, 80, 142, 6, 'm')
carve_circle(80, 144, 14, 'u') # Глубокое логово Worm

# 6. Записываем новую карту RR_MAZE_PVP в Shared/StaticData.c
with open("Shared/StaticData.c", "r") as f:
    c = f.read()

rows_str = ",\n".join('    "' + "".join(row) + '"' for row in grid)
new_maze = f"const char RR_MAZE_PVP[{H}][{W + 1}] = {{\n{rows_str}\n}};"

c = re.sub(
    r'const char RR_MAZE_PVP\[\d+\]\[\d+\]\s*=\s*\{.*?\};',
    new_maze,
    c,
    count=1,
    flags=re.DOTALL
)
with open("Shared/StaticData.c", "w") as f:
    f.write(c)

# 7. Обновляем сектора спавна в Server/Waves.c строго под 3 крыла + шахту червей
with open("Server/Waves.c", "r") as f:
    w = f.read()

new_waves = """    if (biome == rr_biome_id_pvp)
    {
        long idx = zone - &RR_MAZE_PVP;
        int gx = (idx >= 0 && idx < 160 * 160) ? (int)(idx % 160) : 80;
        int gy = (idx >= 0 && idx < 160 * 160) ? (int)(idx / 160) : 74;
        double r_ant = rr_frand();

        // Центральная шахта снизу (64 <= gx <= 96 и gy >= 106): Черви (Worm)
        if (gy >= 106 && gx >= 64 && gx <= 96)
        {
            if (r_ant < 0.94) return rr_mob_id_worm;
            if (r_ant < 0.96) return rr_mob_id_queen_ant;
            if (r_ant < 0.98) return rr_mob_id_queen_fire_ant;
            return rr_mob_id_queen_termite;
        }
        // Северное крыло (gy < 66): ТОЛЬКО Обычные муравьи
        if (gy < 66)
        {
            if (r_ant < 0.55) return rr_mob_id_worker_ant;
            if (r_ant < 0.88) return rr_mob_id_soldier_ant;
            if (r_ant < 0.98) return rr_mob_id_ant_egg;
            return rr_mob_id_queen_ant;
        }
        // Юго-Западное крыло (gx < 80, gy >= 66): ТОЛЬКО Огненные (красные) муравьи
        if (gx < 80)
        {
            if (r_ant < 0.55) return rr_mob_id_fire_worker_ant;
            if (r_ant < 0.88) return rr_mob_id_fire_soldier_ant;
            if (r_ant < 0.98) return rr_mob_id_fire_ant_egg;
            return rr_mob_id_queen_fire_ant;
        }
        // Юго-Восточное крыло (gx >= 80, gy >= 66): ТОЛЬКО Термиты
        if (r_ant < 0.55) return rr_mob_id_termite_worker;
        if (r_ant < 0.88) return rr_mob_id_termite_soldier;
        if (r_ant < 0.98) return rr_mob_id_termite_egg;
        return rr_mob_id_queen_termite;
    }"""

w = re.sub(
    r'    if \(biome == rr_biome_id_pvp\)\s*\{.*?\n    \}',
    new_waves,
    w,
    count=1,
    flags=re.DOTALL
)
with open("Server/Waves.c", "w") as f:
    f.write(w)

# 8. Устанавливаем точку спавна игрока в Ant Hell ровно в центр перекрёстка (80, 74) в Server/Simulation.c
with open("Server/Simulation.c", "r") as f:
    sim = f.read()

sim = re.sub(
    r'(biome == rr_biome_id_pvp.*?\n.*?)x\s*=\s*[^;]+;\s*y\s*=\s*[^;]+;',
    r'\1x = 80 * RR_MAZE_CELL_SIZE; y = 74 * RR_MAZE_CELL_SIZE;',
    sim,
    count=1
)
with open("Server/Simulation.c", "w") as f:
    f.write(sim)

print("Новая 3-крылая карта Ant Hell построена и разделена по колониям!")
