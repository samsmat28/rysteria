import random
import re

random.seed(777)
SIZE = 160

def make_grid(fill='_'):
    return [[fill for _ in range(SIZE)] for _ in range(SIZE)]

def add_borders(g):
    for i in range(SIZE):
        for b in (0, 1, SIZE - 2, SIZE - 1):
            g[b][i] = 'c'
            g[i][b] = 'c'

def carve_rect(g, x1, y1, x2, y2, val='_'):
    for y in range(max(2, int(y1)), min(SIZE - 2, int(y2))):
        for x in range(max(2, int(x1)), min(SIZE - 2, int(x2))):
            g[y][x] = val

def carve_circle(g, cx, cy, r, val='_'):
    r2 = r * r
    for y in range(max(2, int(cy - r)), min(SIZE - 2, int(cy + r + 1))):
        for x in range(max(2, int(cx - r)), min(SIZE - 2, int(cx + r + 1))):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r2:
                g[y][x] = val

def carve_corridor(g, x1, y1, x2, y2, half_width=4):
    steps = max(abs(x2 - x1), abs(y2 - y1)) * 2 + 1
    for s in range(steps + 1):
        t = s / steps
        px = x1 + (x2 - x1) * t
        py = y1 + (y2 - y1) * t
        carve_circle(g, px, py, half_width, '_')

CPS = {
    "ESCAPE": [
        (16, 78, 4, 4, 20, 82, 1),    # Комната 1 (Старт)
        (46, 78, 4, 4, 50, 82, 10),   # Комната 2
        (76, 78, 4, 4, 80, 82, 20),   # Комната 3
        (106, 78, 4, 4, 110, 82, 35), # Комната 4
        (136, 78, 4, 4, 140, 82, 50), # Комната 5 (Финал)
    ],
    "NETHER": [
        (24, 24, 4, 4, 28, 28, 1),
        (80, 28, 4, 4, 84, 32, 15),
        (124, 44, 4, 4, 128, 48, 30),
        (40, 88, 4, 4, 44, 92, 45),
        (100, 92, 4, 4, 104, 96, 60),
        (44, 128, 4, 4, 48, 132, 75),
        (112, 128, 4, 4, 116, 132, 90),
    ],
    "OCEAN": [
        (76, 24, 4, 4, 80, 28, 1),
        (32, 52, 4, 4, 36, 56, 15),
        (120, 52, 4, 4, 124, 56, 30),
        (76, 80, 4, 4, 80, 84, 45),
        (32, 112, 4, 4, 36, 116, 60),
        (120, 112, 4, 4, 124, 116, 75),
        (76, 132, 4, 4, 80, 136, 90),
    ],
    "PLAINS": [
        (28, 28, 4, 4, 32, 32, 1),
        (86, 28, 4, 4, 90, 32, 15),
        (126, 56, 4, 4, 130, 60, 30),
        (36, 86, 4, 4, 40, 90, 45),
        (92, 88, 4, 4, 96, 92, 60),
        (40, 130, 4, 4, 44, 134, 75),
        (108, 128, 4, 4, 112, 132, 90),
    ],
}

def safe_points(cps):
    pts = [(80, 80)] # Центр карты всегда свободен
    for cp in cps:
        pts.append(((cp[0] + cp[4]) // 2, (cp[1] + cp[5]) // 2))
    return pts

def clear_safe_zones(g, cps, radius=13):
    for cx, cy in safe_points(cps):
        carve_circle(g, cx, cy, radius, '_')

def gen_escape():
    g = make_grid('c')
    # 5 больших залов по центру
    rooms = [(18, 80, 12), (48, 80, 13), (78, 80, 13), (108, 80, 13), (138, 80, 15)]
    for idx, (rx, ry, r) in enumerate(rooms):
        carve_rect(g, rx - r, ry - r - 4, rx + r + 1, ry + r + 5, '_')
        if idx in (1, 3):
            for dx in (-6, 6):
                for dy in (-6, 6):
                    carve_rect(g, rx + dx - 1, ry + dy - 1, rx + dx + 2, ry + dy + 2, 'c')
    # Широкий главный коридор через все комнаты
    carve_rect(g, 18, 76, 144, 85, '_')
    # Верхние и нижние залы-ответвления
    for bx in (48, 108):
        carve_rect(g, bx - 4, 28, bx + 5, 132, '_')
        carve_rect(g, bx - 14, 22, bx + 15, 38, '_')
        carve_rect(g, bx - 14, 122, bx + 15, 138, '_')
    clear_safe_zones(g, CPS["ESCAPE"], radius=11)
    add_borders(g)
    return g

def gen_nether():
    g = make_grid('c')
    pts = safe_points(CPS["NETHER"]) + [(40, 50), (115, 65), (75, 115), (30, 115), (125, 105)]
    # Большие круглые пещерные залы
    for cx, cy in pts:
        carve_circle(g, cx, cy, 17, '_')
    # Широкие дороги между соседними залами
    for i in range(len(pts)):
        x1, y1 = pts[i]
        # Соединяем с двумя ближайшими залами
        others = sorted(pts, key=lambda p: (p[0]-x1)**2 + (p[1]-y1)**2)[1:3]
        for x2, y2 in others:
            carve_corridor(g, x1, y1, x2, y2, half_width=6)
    clear_safe_zones(g, CPS["NETHER"], radius=14)
    add_borders(g)
    return g

def gen_ocean():
    g = make_grid('_')
    pts = safe_points(CPS["OCEAN"])
    # Аккуратные острова далеко от точек спавна
    islands = []
    for _ in range(45):
        ix, iy = random.randint(14, SIZE - 15), random.randint(14, SIZE - 15)
        r = random.randint(4, 7)
        if all((ix - px)**2 + (iy - py)**2 > (r + 16)**2 for px, py in pts):
            if all((ix - ox)**2 + (iy - oy)**2 > (r + orad + 8)**2 for ox, oy, orad in islands):
                carve_circle(g, ix, iy, r, 'c')
                islands.append((ix, iy, r))
    clear_safe_zones(g, CPS["OCEAN"], radius=14)
    add_borders(g)
    return g

def gen_plains():
    g = make_grid('_')
    pts = safe_points(CPS["PLAINS"])
    # Небольшие рощи и камни, не мешающие проходу
    for _ in range(70):
        tx, ty = random.randint(12, SIZE - 13), random.randint(12, SIZE - 13)
        r = random.randint(1, 3)
        if all((tx - px)**2 + (ty - py)**2 > (r + 15)**2 for px, py in pts):
            carve_circle(g, tx, ty, r, 'c')
    clear_safe_zones(g, CPS["PLAINS"], radius=14)
    add_borders(g)
    return g

def write_map_header(filename, maze_name, grid):
    with open(filename, "w") as f:
        f.write(f"// Карта 160x160 для {maze_name}\n")
        f.write(f"RR_DEFINE_MAZE({maze_name}, 160) = {{\n")
        for y, row in enumerate(grid):
            f.write("    {" + ",".join(row) + "}, // " + str(y) + "\n")
        f.write("};\n")
    print(f"Готово: {filename}")

write_map_header("Shared/Escape_map.h", "ESCAPE", gen_escape())
write_map_header("Shared/Nether_map.h", "NETHER", gen_nether())
write_map_header("Shared/Ocean_map.h", "OCEAN", gen_ocean())
write_map_header("Shared/Plains_map.h", "PLAINS", gen_plains())

with open("Shared/StaticData.c", "r") as f:
    sd = f.read()

for mname, cps in CPS.items():
    cp_str = ",".join("{" + ",".join(map(str, c)) + "}" for c in cps)
    new_entry = f"{{MAZE_ENTRY({mname}, 2048), {len(cps)}, {{{cp_str}}}}},"
    entry_pattern = rf"\{{MAZE_ENTRY\({mname},\s*2048\),.*?\}}\}},"
    sd = re.sub(entry_pattern, new_entry, sd, count=1, flags=re.DOTALL)

with open("Shared/StaticData.c", "w") as f:
    f.write(sd)
