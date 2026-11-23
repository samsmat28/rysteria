import random, re

random.seed(42)
W, H = 160, 160
grid = [['#' for _ in range(W)] for _ in range(H)]

def carve_blob(cx, cy, rx, ry, val, jitter=0.28):
    for y in range(max(3, int(cy - ry - 4)), min(H - 3, int(cy + ry + 5))):
        for x in range(max(3, int(cx - rx - 4)), min(W - 3, int(cx + rx + 5))):
            dx = (x - cx) / max(rx, 1.0)
            dy = (y - cy) / max(ry, 1.0)
            n = 1.0 + jitter * (((x * 17 + y * 31) % 11) - 5) / 5.0
            if dx*dx + dy*dy <= n:
                grid[y][x] = val

def carve_winding_tunnel(pts, r_min, r_max, val):
    for i in range(len(pts) - 1):
        x1, y1 = pts[i]
        x2, y2 = pts[i + 1]
        steps = max(abs(x2 - x1), abs(y2 - y1), 1) * 2
        for s in range(steps + 1):
            t = s / steps
            cx = x1 + (x2 - x1) * t + random.uniform(-1.5, 1.5)
            cy = y1 + (y2 - y1) * t + random.uniform(-1.5, 1.5)
            r = random.uniform(r_min, r_max)
            carve_blob(cx, cy, r, r, val, jitter=0.2)

# 1. ВЕРХНИЙ СЕКТОР (y: 6..62, x: 12..92) — Извилистые тоннели Обычных Муравьёв (Ant)
ant_tunnels = [
    [(42, 56), (34, 46), (22, 42), (16, 30), (28, 22), (44, 24), (56, 16), (72, 18), (82, 28)],
    [(42, 56), (52, 46), (64, 48), (74, 38), (62, 30), (46, 36), (32, 32)],
    [(28, 22), (24, 12), (42, 10), (56, 16)],
    [(64, 48), (82, 52), (88, 40)]
]
for idx_t, path in enumerate(ant_tunnels):
    val = 'c' if idx_t in (0, 1) else ('r' if idx_t == 2 else 'e')
    carve_winding_tunnel(path, 3.2, 4.8, val)

# Камеры в верхнем секторе
carve_blob(42, 56, 8, 7, 'c')   # Точка входа (Spawn)
carve_blob(22, 26, 7, 6, 'r')
carve_blob(68, 20, 8, 7, 'e')
carve_blob(48, 12, 7, 6, 'l')   # Зал Queen Ant

# 2. НИЖНИЙ-ЛЕВЫЙ СЕКТОР (y: 64..152, x: 8..82) — Крупные пещеры Огненных Муравьёв (Fire Ant)
carve_winding_tunnel([(42, 56), (36, 68), (28, 80)], 3.5, 4.5, 'r')
fire_chambers = [
    (26, 82, 12, 10, 'r'),
    (52, 86, 11, 9,  'e'),
    (22, 110, 13, 11, 'e'),
    (48, 114, 11, 10, 'l'),
    (28, 140, 15, 12, 'm'),
    (58, 142, 15, 12, 'u')  # Глубокий зал Queen Fire Ant
]
for cx, cy, rx, ry, val in fire_chambers:
    carve_blob(cx, cy, rx, ry, val, jitter=0.22)

fire_links = [
    [(26, 82), (40, 84), (52, 86)],
    [(26, 82), (22, 96), (22, 110)],
    [(52, 86), (50, 100), (48, 114)],
    [(22, 110), (35, 112), (48, 114)],
    [(22, 110), (16, 126), (28, 140)],
    [(48, 114), (54, 128), (58, 142)],
    [(28, 140), (43, 142), (58, 142)]
]
for path in fire_links:
    carve_winding_tunnel(path, 3.0, 4.2, 'e')

# 3. ПРАВЫЙ СЕКТОР (y: 12..152, x: 86..152) — Лабиринт Термитов (Termite) + Черви (Worm)
carve_winding_tunnel([(82, 52), (96, 54), (108, 44)], 3.2, 4.5, 'r')
termite_paths = [
    [(108, 44), (102, 28), (118, 18), (138, 22), (144, 38), (128, 46)],
    [(108, 44), (116, 62), (100, 74), (114, 88), (134, 82), (142, 64), (128, 46)],
    [(114, 88), (98, 102), (112, 118), (134, 112), (142, 96)],
    [(112, 118), (102, 136), (122, 146), (142, 138), (134, 112)]
]
for idx_t, path in enumerate(termite_paths):
    val = ['r', 'e', 'l', 'm'][idx_t]
    carve_winding_tunnel(path, 3.5, 5.2, val)

carve_blob(126, 24, 9, 8, 'e')
carve_blob(124, 66, 10, 9, 'l')
carve_blob(122, 102, 10, 9, 'm')
carve_blob(126, 140, 12, 10, 'u') # Тронный зал Queen Termite и Worm

# 4. Записываем новую карту в Shared/StaticData.c
with open("Shared/StaticData.c", "r") as f:
    c = f.read()

rows_str = ",\n".join('    "' + "".join(row) + '"' for row in grid)
new_maze = f"const char RR_MAZE_PVP[{H}][{W + 1}] = {{\n{rows_str}\n}};"
c = re.sub(r'const char RR_MAZE_PVP\[\d+\]\[\d+\]\s*=\s*\{.*?\};', new_maze, c, count=1, flags=re.DOTALL)
with open("Shared/StaticData.c", "w") as f:
    f.write(c)

# 5. Обновляем сектора спавна в Server/Waves.c строго под 3 зоны этой карты
with open("Server/Waves.c", "r") as f:
    w = f.read()

new_waves = """    if (biome == rr_biome_id_pvp)
    {
        long idx = zone - &RR_MAZE_PVP;
        int gx = (idx >= 0 && idx < 160 * 160) ? (int)(idx % 160) : 42;
        int gy = (idx >= 0 && idx < 160 * 160) ? (int)(idx / 160) : 56;
        double r_ant = rr_frand();

        // ПРАВЫЙ СЕКТОР (gx >= 85): Лабиринт Термитов + глубокие Черви (gy >= 122)
        if (gx >= 85)
        {
            if (gy >= 122 && r_ant < 0.35) return rr_mob_id_worm;
            if (r_ant < 0.55) return rr_mob_id_termite_worker;
            if (r_ant < 0.88) return rr_mob_id_termite_soldier;
            if (r_ant < 0.98) return rr_mob_id_termite_egg;
            return rr_mob_id_queen_termite;
        }
        // ВЕРХНИЙ СЕКТОР (gx < 85 && gy < 64): Тоннели Обычных Муравьёв
        if (gy < 64)
        {
            if (r_ant < 0.55) return rr_mob_id_worker_ant;
            if (r_ant < 0.88) return rr_mob_id_soldier_ant;
            if (r_ant < 0.98) return rr_mob_id_ant_egg;
            return rr_mob_id_queen_ant;
        }
        // НИЖНИЙ-ЛЕВЫЙ СЕКТОР (gx < 85 && gy >= 64): Пещеры Огненных Муравьёв
        if (r_ant < 0.55) return rr_mob_id_fire_worker_ant;
        if (r_ant < 0.88) return rr_mob_id_fire_soldier_ant;
        if (r_ant < 0.98) return rr_mob_id_fire_ant_egg;
        return rr_mob_id_queen_fire_ant;
    }"""

w = re.sub(r'    if \(biome == rr_biome_id_pvp\)\s*\{.*?\n    \}', new_waves, w, count=1, flags=re.DOTALL)
with open("Server/Waves.c", "w") as f:
    f.write(w)

# 6. Ставим точку входа игрока на перекрёсток (42, 56) в Server/Simulation.c
with open("Server/Simulation.c", "r") as f:
    sim = f.read()
sim = re.sub(r'x = 80 \* RR_MAZE_CELL_SIZE; y = 74 \* RR_MAZE_CELL_SIZE;', 'x = 42 * RR_MAZE_CELL_SIZE; y = 56 * RR_MAZE_CELL_SIZE;', sim)
with open("Server/Simulation.c", "w") as f:
    f.write(sim)

print("Органический лабиринт Ant Hell (верх Ant, низ-лево Fire Ant, право Termite) готов!")
