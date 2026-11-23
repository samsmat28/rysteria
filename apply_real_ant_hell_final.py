import random, re

random.seed(77)
W, H = 80, 80
grid = [['_' for _ in range(W)] for _ in range(H)]

def carve_blob(cx, cy, rx, ry, val, jitter=0.22):
    for y in range(max(2, int(cy - ry - 3)), min(H - 2, int(cy + ry + 4))):
        for x in range(max(2, int(cx - rx - 3)), min(W - 2, int(cx + rx + 4))):
            dx = (x - cx) / max(rx, 1.0)
            dy = (y - cy) / max(ry, 1.0)
            n = 1.0 + jitter * (((x * 13 + y * 29) % 9) - 4) / 4.0
            if dx*dx + dy*dy <= n:
                grid[y][x] = val

def carve_tunnel(pts, r_min, r_max, val):
    for i in range(len(pts) - 1):
        x1, y1 = pts[i]
        x2, y2 = pts[i + 1]
        steps = max(abs(x2 - x1), abs(y2 - y1), 1) * 2
        for s in range(steps + 1):
            t = s / steps
            cx = x1 + (x2 - x1) * t + random.uniform(-0.8, 0.8)
            cy = y1 + (y2 - y1) * t + random.uniform(-0.8, 0.8)
            r = random.uniform(r_min, r_max)
            carve_blob(cx, cy, r, r, val, jitter=0.18)

# 1. ВЕРХНИЙ СЕКТОР (y: 4..31, x: 6..44) — Извилистые тоннели Обычных Муравьёв (Ant)
ant_paths = [
    [(22, 28), (17, 23), (11, 20), (8, 14), (14, 10), (22, 11), (28, 7), (36, 9), (41, 14)],
    [(22, 28), (27, 23), (33, 24), (37, 19), (31, 15), (23, 18), (16, 16)],
    [(14, 10), (12, 6), (21, 5), (28, 7)],
    [(33, 24), (41, 26), (44, 20)]
]
for idx_t, p in enumerate(ant_paths):
    carve_tunnel(p, 1.8, 2.5, ['c', 'c', 'r', 'e'][idx_t])

carve_blob(22, 28, 4.5, 4.0, 'c') # Точка входа (Spawn)
carve_blob(11, 13, 4.0, 3.5, 'r')
carve_blob(34, 10, 4.5, 4.0, 'e')
carve_blob(24, 6,  4.0, 3.5, 'l') # Тронный зал Queen Ant

# 2. НИЖНИЙ-ЛЕВЫЙ СЕКТОР (y: 33..76, x: 4..41) — Пещеры Огненных Муравьёв (Fire Ant)
carve_tunnel([(22, 28), (18, 34), (14, 41)], 1.8, 2.4, 'r')
fire_chambers = [
    (13, 41, 6.0, 5.0, 'r'),
    (26, 43, 5.5, 4.5, 'e'),
    (11, 55, 6.5, 5.5, 'e'),
    (24, 57, 5.5, 5.0, 'l'),
    (14, 70, 7.5, 6.0, 'm'),
    (29, 71, 7.5, 6.0, 'u') # Тронный зал Queen Fire Ant
]
for cx, cy, rx, ry, val in fire_chambers:
    carve_blob(cx, cy, rx, ry, val, jitter=0.2)

for p in [
    [(13, 41), (20, 42), (26, 43)],
    [(13, 41), (11, 48), (11, 55)],
    [(26, 43), (25, 50), (24, 57)],
    [(11, 55), (18, 56), (24, 57)],
    [(11, 55), (8, 63), (14, 70)],
    [(24, 57), (27, 64), (29, 71)],
    [(14, 70), (22, 71), (29, 71)]
]:
    carve_tunnel(p, 1.6, 2.2, 'e')

# 3. ПРАВЫЙ СЕКТОР (y: 6..76, x: 43..76) — Лабиринт Термитов (Termite) + Черви (Worm)
carve_tunnel([(41, 26), (48, 27), (54, 22)], 1.8, 2.4, 'r')
termite_paths = [
    [(54, 22), (51, 14), (59, 9), (69, 11), (72, 19), (64, 23)],
    [(54, 22), (58, 31), (50, 37), (57, 44), (67, 41), (71, 32), (64, 23)],
    [(57, 44), (49, 51), (56, 59), (67, 56), (71, 48)],
    [(56, 59), (51, 68), (61, 73), (71, 69), (67, 56)]
]
for idx_t, p in enumerate(termite_paths):
    carve_tunnel(p, 1.9, 2.6, ['r', 'e', 'l', 'm'][idx_t])

carve_blob(63, 12, 4.5, 4.0, 'e')
carve_blob(62, 33, 5.0, 4.5, 'l')
carve_blob(61, 51, 5.0, 4.5, 'm')
carve_blob(63, 70, 6.0, 5.0, 'u') # Тронный зал Queen Termite и Worm

# 4. Записываем новую сетку в RR_DEFINE_MAZE(PVP, 160) в Shared/StaticData.c
with open("Shared/StaticData.c", "r") as f:
    c = f.read()

# Удаляем временный неиспользуемый RR_MAZE_PVP[160][161], если он был добавлен ранее
c = re.sub(r'const char RR_MAZE_PVP\[\d+\]\[\d+\]\s*=\s*\{.*?\};\s*', '', c, flags=re.DOTALL)

maze_rows = []
for y in range(H):
    maze_rows.append("    {" + ",".join(grid[y]) + "}, // " + str(y))
new_pvp_maze = "RR_DEFINE_MAZE(PVP, 160) = {\n" + "\n".join(maze_rows) + "\n};"

assert "RR_DEFINE_MAZE(PVP, 160)" in c, "Не найден RR_DEFINE_MAZE(PVP, 160)!"
c = re.sub(r'RR_DEFINE_MAZE\(PVP,\s*160\)\s*=\s*\{.*?\};', new_pvp_maze, c, count=1, flags=re.DOTALL)

with open("Shared/StaticData.c", "w") as f:
    f.write(c)

# 5. Обновляем спавн по секторам в Server/Waves.c (по координатам 0..159 в RR_MAZE_PVP)
with open("Server/Waves.c", "r") as f:
    w = f.read()

new_waves = """    if (biome == rr_biome_id_pvp)
    {
        long idx = zone - &RR_MAZE_PVP;
        int gx = (idx >= 0 && idx < 160 * 160) ? (int)(idx % 160) : 44;
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

# 6. Переименовываем кнопку мира с "PvP" на "Ant Hell" в Client/Game.c
with open("Client/Game.c", "r") as f:
    gc = f.read()
gc = gc.replace('rr_ui_biome_button_init("PvP", 0xff3a6ee0, rr_biome_id_pvp)', 'rr_ui_biome_button_init("Ant Hell", 0xff8a5a36, rr_biome_id_pvp)')
with open("Client/Game.c", "w") as f:
    f.write(gc)

# 7. Полностью отключаем PvP урон между игроками в Server/System/Health.c
with open("Server/System/Health.c", "r") as f:
    hc = f.read()
hc = hc.replace("arena == rr_biome_id_pvp", "0 /* pvp disabled */")
with open("Server/System/Health.c", "w") as f:
    f.write(hc)

print("Настоящая карта Ant Hell (80x80 -> 160x160), название Ant Hell и отключение PvP готовы!")
