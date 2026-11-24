import random
import re

random.seed(42)

def make_grid(fill='_'):
    return [[fill for _ in range(80)] for _ in range(80)]

def add_borders(g):
    for i in range(80):
        g[0][i] = g[1][i] = g[78][i] = g[79][i] = 'c'
        g[i][0] = g[i][1] = g[i][78] = g[i][79] = 'c'

def carve_rect(g, x1, y1, x2, y2, val='_'):
    for y in range(max(2, y1), min(78, y2)):
        for x in range(max(2, x1), min(78, x2)):
            g[y][x] = val

def carve_circle(g, cx, cy, r, val='_'):
    for y in range(max(2, cy - r), min(78, cy + r + 1)):
        for x in range(max(2, cx - r), min(78, cx + r + 1)):
            if (x - cx)**2 + (y - cy)**2 <= r*r:
                g[y][x] = val

def gen_escape():
    g = make_grid('c')
    # 5 комнат по горизонтали (y вокруг 30) + коридоры между ними
    rooms = [(6, 30, 5), (18, 30, 5), (30, 30, 5), (42, 30, 5), (54, 30, 6)]
    for idx, (rx, ry, r) in enumerate(rooms):
        carve_rect(g, rx - r, ry - r - 2, rx + r + 1, ry + r + 3, '_')
        # Декоративные колонны в комнатах 2 и 4
        if idx in (1, 3):
            g[ry - 2][rx - 2] = 'c'
            g[ry + 2][rx - 2] = 'c'
            g[ry - 2][rx + 2] = 'c'
            g[ry + 2][rx + 2] = 'c'
    # Соединяющие коридоры
    carve_rect(g, 6, 29, 58, 32, '_')
    # Дополнительные секретные ответвления вверх и вниз
    carve_rect(g, 17, 16, 20, 45, '_')
    carve_rect(g, 14, 14, 23, 19, '_')
    carve_rect(g, 14, 42, 23, 47, '_')
    carve_rect(g, 41, 16, 44, 45, '_')
    carve_rect(g, 38, 14, 47, 19, '_')
    carve_rect(g, 38, 42, 47, 47, '_')
    add_borders(g)
    return g

def gen_nether():
    g = make_grid('c')
    pts = [(13,13), (41,15), (63,23), (21,45), (51,47), (23,65), (57,65),
           (28,28), (48,30), (35,55), (65,45), (15,60)]
    for cx, cy in pts:
        carve_circle(g, cx, cy, random.randint(6, 9), '_')
    for i in range(len(pts) - 1):
        x1, y1 = pts[i]
        x2, y2 = pts[i + 1]
        steps = 40
        for s in range(steps + 1):
            t = s / steps
            px = int(x1 + (x2 - x1) * t + random.uniform(-1.5, 1.5))
            py = int(y1 + (y2 - y1) * t + random.uniform(-1.5, 1.5))
            carve_circle(g, px, py, 3, '_')
    # Лавовые колонны внутри залов
    for _ in range(18):
        ox, oy = random.randint(8, 71), random.randint(8, 71)
        if all((ox - cx)**2 + (oy - cy)**2 > 25 for cx, cy in pts[:7]):
            carve_circle(g, ox, oy, 2, 'c')
    add_borders(g)
    return g

def gen_ocean():
    g = make_grid('_')
    # Острова и рифы, не перекрывающие чекпоинты
    safe = [(39,13), (17,27), (61,27), (39,41), (17,57), (61,57), (39,67)]
    for _ in range(35):
        ix, iy = random.randint(6, 73), random.randint(6, 73)
        r = random.randint(2, 4)
        if all((ix - sx)**2 + (iy - sy)**2 > (r + 5)**2 for sx, sy in safe):
            carve_circle(g, ix, iy, r, 'c')
    add_borders(g)
    return g

def gen_plains():
    g = make_grid('_')
    safe = [(15,15), (44,15), (64,29), (19,44), (47,45), (21,66), (55,65)]
    # Небольшие рощи и камни на равнине
    for _ in range(55):
        tx, ty = random.randint(4, 75), random.randint(4, 75)
        if all((tx - sx)**2 + (ty - sy)**2 > 36 for sx, sy in safe):
            g[ty][tx] = 'c'
            if random.random() < 0.4 and tx + 1 < 76:
                g[ty][tx + 1] = 'c'
    add_borders(g)
    return g

def format_maze(name, grid):
    lines = [f"RR_DEFINE_MAZE({name}, 160) = {{"]
    for y, row in enumerate(grid):
        lines.append("    {" + ",".join(row) + "}, // " + str(y))
    lines.append("};")
    return "\n".join(lines)

with open("Shared/StaticData.c", "r") as f:
    sd = f.read()

maps = {
    "ESCAPE": gen_escape(),
    "NETHER": gen_nether(),
    "OCEAN": gen_ocean(),
    "PLAINS": gen_plains(),
}

for mname, mgrid in maps.items():
    new_block = format_maze(mname, mgrid)
    pattern = rf"RR_DEFINE_MAZE\({mname},\s*160\)\s*=\s*\{{.*?\n\}};"
    if re.search(pattern, sd, flags=re.DOTALL):
        sd = re.sub(pattern, new_block, sd, count=1, flags=re.DOTALL)
        print(f"Обновлена карта: {mname}")
    else:
        print(f"Внимание: блок {mname} не найден в StaticData.c")

# Подключаем сервер Escape Room на порт 1239
sd = sd.replace(
    '{"pvp",1235,"ant"},{NULL,0,NULL},{NULL,0,NULL}',
    '{"pvp",1235,"ant"},{"escape",1239,"esc"},{NULL,0,NULL}',
    1
)

with open("Shared/StaticData.c", "w") as f:
    f.write(sd)

# Добавляем спавн мобов для Escape Room в Server/Waves.c
with open("Server/Waves.c", "r") as f:
    wv = f.read()

if "rr_biome_id_garden" not in wv:
    esc_spawn = """    if (biome == rr_biome_id_garden) {
        float diff = zone ? zone->difficulty : 1.0f; double r = rr_frand();
        if (diff <= 15.0f) return r < 0.5 ? rr_mob_id_rock : rr_mob_id_ladybug;
        if (diff <= 30.0f) return r < 0.5 ? rr_mob_id_hornet : rr_mob_id_spider;
        return r < 0.5 ? rr_mob_id_centipede : rr_mob_id_beetle;
    }
    if (biome == rr_biome_id_nether)"""
    wv = wv.replace("    if (biome == rr_biome_id_nether)", esc_spawn, 1)
    with open("Server/Waves.c", "w") as f:
        f.write(wv)
    print("Добавлен спавн мобов для Escape Room в Waves.c")

# Добавляем цвет пола для Escape Room в RenderArena.c
with open("Client/Renderer/RenderArena.c", "r") as f:
    ra = f.read()

if "rr_biome_id_garden" not in ra:
    ra = ra.replace(
        "this->selected_biome == rr_biome_id_nether",
        "this->selected_biome == rr_biome_id_garden || this->selected_biome == rr_biome_id_nether",
        1
    )
    with open("Client/Renderer/RenderArena.c", "w") as f:
        f.write(ra)
    print("Добавлен фон для Escape Room в RenderArena.c")

print("ВСЕ КАРТЫ И НАСТРОЙКИ ГОТОВЫ!")
