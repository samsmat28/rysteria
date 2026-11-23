import re

# 1. Обновляем RenderArena.c: четкий и красивый подземный пол Ant Hell
with open("Client/Renderer/RenderArena.c", "r", encoding="utf-8") as f:
    arena = f.read()

old_floor_pattern = re.compile(
    r'if\s*\(this->selected_biome\s*==\s*rr_biome_id_pvp\)\s*\{.*?\}\s*else if\s*\(this->selected_biome\s*==\s*rr_biome_id_hell_clerk|else if\s*\(this->selected_biome\s*==\s*rr_biome_id_hell_creek\)',
    re.DOTALL
)

new_floor_code = '''if (this->selected_biome == rr_biome_id_pvp)
        {
            // Уникальный хеш для каждого тайла, чтобы узор не повторялся каждые 3 клетки
            uint32_t h = rr_get_hash((uint32_t)(((newLeftX + 8192) / GRID_SIZE) * 73856093u ^ ((currY + 8192) / GRID_SIZE) * 19349663u));

            // Чистый базовый пол Ant Hell (теплый земляной оттенок florr.io)
            rr_renderer_set_fill(renderer, 0xff9d734d);
            rr_renderer_begin_path(renderer);
            rr_renderer_rect(renderer, -128, -128, 256, 256);
            rr_renderer_fill(renderer);

            // Песчаные крупинки (мелкие четкие точки)
            rr_renderer_set_fill(renderer, 0xff8b623e);
            for (int i = 0; i < 4; i++) {
                uint32_t sh = rr_get_hash(h + (uint32_t)(i * 101));
                float px = (float)((int)(sh % 210) - 105);
                float py = (float)((int)((sh >> 8) % 210) - 105);
                float pr = 2.2f + (float)((sh >> 16) % 3);
                rr_renderer_begin_path(renderer);
                rr_renderer_arc(renderer, px, py, pr);
                rr_renderer_fill(renderer);
            }

            // Четкие подземные камешки с темным контуром (на 65% тайлов)
            if ((h % 100) < 65) {
                float sx = (float)((int)((h >> 4) % 170) - 85);
                float sy = (float)((int)((h >> 12) % 170) - 85);
                float sr = 5.5f + (float)((h >> 20) % 5);

                // Тень/контур камешка
                rr_renderer_set_fill(renderer, 0xff6b492b);
                rr_renderer_begin_path(renderer);
                rr_renderer_arc(renderer, sx, sy + 1.5f, sr + 1.4f);
                rr_renderer_fill(renderer);

                // Тело камешка
                rr_renderer_set_fill(renderer, (h & 1) ? 0xff825b37 : 0xff785331);
                rr_renderer_begin_path(renderer);
                rr_renderer_arc(renderer, sx, sy, sr);
                rr_renderer_fill(renderer);
            }

            // Аккуратный второй мелкий камешек (на 35% тайлов)
            if (((h >> 3) % 100) < 35) {
                float sx2 = (float)((int)((h >> 6) % 180) - 90);
                float sy2 = (float)((int)((h >> 14) % 180) - 90);
                rr_renderer_set_fill(renderer, 0xff6e4c2e);
                rr_renderer_begin_path(renderer);
                rr_renderer_arc(renderer, sx2, sy2, 3.6f);
                rr_renderer_fill(renderer);
            }

            // Тонкая четкая трещинка (на 25% тайлов)
            if (((h >> 5) % 100) < 25) {
                float cx = (float)((int)((h >> 7) % 140) - 70);
                float cy = (float)((int)((h >> 15) % 140) - 70);
                rr_renderer_set_stroke(renderer, 0xff77512f);
                rr_renderer_set_line_width(renderer, 2.0f);
                rr_renderer_begin_path(renderer);
                rr_renderer_move_to(renderer, cx - 10.0f, cy - 4.0f);
                rr_renderer_line_to(renderer, cx, cy + 2.0f);
                rr_renderer_line_to(renderer, cx + 11.0f, cy - 2.0f);
                rr_renderer_stroke(renderer);
            }
        }
        else if (this->selected_biome == rr_biome_id_hell_creek)'''

arena_new, count = old_floor_pattern.subn(new_floor_code, arena, count=1)
assert count == 1, "Не удалось найти блок пола Ant Hell в RenderArena.c"
with open("Client/Renderer/RenderArena.c", "w", encoding="utf-8") as f:
    f.write(arena_new)

# 2. Обновляем Shared/StaticData.c: добавляем символы o, h, g и строим понятную карту редкостей Ant Hell
with open("Shared/StaticData.c", "r", encoding="utf-8") as f:
    sdata = f.read()

if "#define o 64" not in sdata:
    sdata = sdata.replace(
        "#define A 60\n",
        "#define A 60\n#define o 64\n#define O 64\n#define h 68\n#define H 68\n#define g 72\n#define G 72\n"
    )

maze_match = re.search(r'(RR_DEFINE_MAZE\(PVP,\s*160\)\s*=\s*\{)(.*?)(\n\};)', sdata, re.DOTALL)
assert maze_match, "Не найден блок RR_DEFINE_MAZE(PVP, 160)"

maze_body = maze_match.group(2)
rows = re.findall(r'\{([^}]+)\}', maze_body)
assert len(rows) == 80, f"Ожидалось 80 строк в шаблоне PVP, найдено {len(rows)}"

grid = []
for r in rows:
    tokens = [t.strip() for t in r.split(',') if t.strip()]
    assert len(tokens) == 80, f"Ожидалось 80 колонок, найдено {len(tokens)}"
    grid.append(tokens)

# Вычисляем расстояние от центра спавна (x=28, y=28 в шаблоне 80x80) по проходимым клеткам (BFS)
from collections import deque
walkable = {(y, x) for y in range(80) for x in range(80) if grid[y][x] != '_'}

# Находим ближайшую проходимую клетку к верхнему-левому хабу (x=25, y=22)
start = min(walkable, key=lambda p: (p[0] - 22)**2 + (p[1] - 25)**2)
dist = {start: 0}
q = deque([start])
while q:
    cy, cx = q.popleft()
    for dy, dx in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
        ny, nx = cy + dy, cx + dx
        if (ny, nx) in walkable and (ny, nx) not in dist:
            dist[(ny, nx)] = dist[(cy, cx)] + 1
            q.append((ny, nx))

# Для недостижимых островков (если есть) считаем евклидово расстояние
max_d = max(dist.values()) if dist else 1
for (y, x) in walkable:
    if (y, x) not in dist:
        d_est = int(((y - start[0])**2 + (x - start[1])**2)**0.5 * 1.4)
        dist[(y, x)] = min(max_d, d_est)

max_d = max(dist.values())

# Четкие, плавные зоны редкостей от входа к глубине туннелей
tiers = [
    (0.08, 'c'),  # Common (вход)
    (0.17, 'u'),  # Uncommon
    (0.27, 'r'),  # Rare
    (0.38, 'e'),  # Epic
    (0.50, 'l'),  # Legendary
    (0.62, 'm'),  # Mythic
    (0.73, 'x'),  # Ultra
    (0.83, 'a'),  # Super
    (0.91, 'o'),  # Omega (фиолетовый)
    (0.96, 'h'),  # Hyper (серый)
    (1.01, 'g'),  # Gods (белый — самые дальние залы боссов)
]

new_rows = []
for y in range(80):
    row_tokens = []
    for x in range(80):
        if grid[y][x] == '_':
            row_tokens.append('_')
        else:
            ratio = dist[(y, x)] / max(1, max_d)
            sym = 'g'
            for thresh, ch in tiers:
                if ratio <= thresh:
                    sym = ch
                    break
            row_tokens.append(sym)
    new_rows.append(f"    {{{','.join(row_tokens)}}}, // {y}")

new_maze_block = maze_match.group(1) + "\n" + "\n".join(new_rows) + maze_match.group(3)
sdata = sdata[:maze_match.start()] + new_maze_block + sdata[maze_match.end():]

with open("Shared/StaticData.c", "w", encoding="utf-8") as f:
    f.write(sdata)

print("Готово! Пол Ant Hell и карта редкостей успешно обновлены.")
