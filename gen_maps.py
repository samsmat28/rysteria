import re

# 1. Фикс ошибки компиляции в Client/Renderer/RenderArena.c
with open("Client/Renderer/RenderArena.c", "r") as f:
    arena_code = f.read()
arena_code = arena_code.replace("this->should_play = 1;", "this->rr_auto_enter_portal = 1;")
with open("Client/Renderer/RenderArena.c", "w") as f:
    f.write(arena_code)

# 2. Генератор шаблона 80x80 (даёт карту 160x160 с толстыми стенами и большими залами)
def build_template(is_ant_hell=False):
    W, H = 80, 80
    grid = [['_' for _ in range(W)] for _ in range(H)]

    # Большие залы фарма: (cx, cy, rx, ry, tier_char)
    if not is_ant_hell:
        # Hell Creek: плавный прогресс от Common (c) до Ultra (U)
        rooms = [
            (14, 14, 10, 10, 'c'), # Зал 1: Старт (Common / Uncommon)
            (42, 15, 11, 10, 'r'), # Зал 2: Rare
            (65, 22, 10, 12, 'e'), # Зал 3: Epic
            (20, 46, 12, 11, 'l'), # Зал 4: Legendary
            (50, 48, 12, 11, 'm'), # Зал 5: Mythic
            (22, 68, 13, 8,  'x'), # Зал 6: Mythic+ / Ultra-low
            (58, 67, 15, 9,  'U'), # Зал 7: Эндгейм Ultra зал
        ]
        corridors = [
            ((14, 14), (42, 15), 3, 'C'),
            ((42, 15), (65, 22), 3, 'R'),
            ((14, 14), (20, 46), 3, 'E'),
            ((42, 15), (50, 48), 3, 'L'),
            ((20, 46), (50, 48), 3, 'M'),
            ((20, 46), (22, 68), 3, 'a'),
            ((50, 48), (58, 67), 3, 'A'),
            ((22, 68), (58, 67), 3, 'u'),
        ]
    else:
        # Ant Hell: гигантские подземные камеры муравейника и широкие туннели
        rooms = [
            (40, 12, 12, 8,  'c'), # Вход в муравейник (верхний зал)
            (16, 26, 11, 11, 'r'), # Левая камера рабочих
            (64, 26, 11, 11, 'e'), # Правая камера огненных
            (40, 40, 13, 12, 'l'), # Центральный перекрёсток
            (16, 58, 11, 12, 'm'), # Глубокий зал термитов
            (64, 58, 11, 12, 'x'), # Зал солдат
            (40, 68, 16, 8,  'U'), # Тронный зал королевы / червей (Ultra)
        ]
        corridors = [
            ((40, 12), (16, 26), 3, 'C'),
            ((40, 12), (64, 26), 3, 'R'),
            ((16, 26), (40, 40), 3, 'E'),
            ((64, 26), (40, 40), 3, 'L'),
            ((40, 40), (16, 58), 3, 'M'),
            ((40, 40), (64, 58), 3, 'a'),
            ((16, 58), (40, 68), 3, 'A'),
            ((64, 58), (40, 68), 3, 'u'),
        ]

    # Рисуем коридоры (ширина 2*radius + 1 -> толстые проходы)
    for (x1, y1), (x2, y2), rad, ch in corridors:
        steps = max(abs(x2 - x1), abs(y2 - y1))
        for s in range(steps + 1):
            t = s / max(1, steps)
            cx = int(round(x1 + (x2 - x1) * t))
            cy = int(round(y1 + (y2 - y1) * t))
            for dy in range(-rad, rad + 1):
                for dx in range(-rad, rad + 1):
                    nx, ny = cx + dx, cy + dy
                    if 3 <= nx < W - 3 and 3 <= ny < H - 3:
                        grid[ny][nx] = ch

    # Рисуем просторные скруглённые залы
    for cx, cy, rx, ry, ch in rooms:
        for y in range(cy - ry, cy + ry + 1):
            for x in range(cx - rx, cx + rx + 1):
                if 3 <= x < W - 3 and 3 <= y < H - 3:
                    # Слегка скругляем углы зала
                    norm = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
                    if norm <= 1.15:
                        grid[y][x] = ch

    lines = []
    for y in range(H):
        row_str = ",".join(grid[y])
        lines.append(f"    {{{row_str}}}, // {y}")
    return "\n".join(lines)

# 3. Обновляем Shared/StaticData.h (80 -> 160)
with open("Shared/StaticData.h", "r") as f:
    h_code = f.read()
h_code = h_code.replace("RR_DECLARE_MAZE(HELL_CREEK, 80)", "RR_DECLARE_MAZE(HELL_CREEK, 160)")
h_code = h_code.replace("RR_DECLARE_MAZE(PVP, 80)", "RR_DECLARE_MAZE(PVP, 160)")
with open("Shared/StaticData.h", "w") as f:
    f.write(h_code)

# 4. Обновляем Shared/StaticData.c
with open("Shared/StaticData.c", "r") as f:
    c_code = f.read()

hc_maze_block = f"RR_DEFINE_MAZE(HELL_CREEK, 160) = {{\n{build_template(False)}\n}};"
pvp_maze_block = f"RR_DEFINE_MAZE(PVP, 160) = {{\n{build_template(True)}\n}};"

c_code = re.sub(r"RR_DEFINE_MAZE\(HELL_CREEK,\s*\d+\)\s*=\s*\{.*?\n\};", hc_maze_block, c_code, flags=re.DOTALL)
c_code = re.sub(r"RR_DEFINE_MAZE\(PVP,\s*\d+\)\s*=\s*\{.*?\n\};", pvp_maze_block, c_code, flags=re.DOTALL)

# Обновляем координаты спавна в RR_MAZES под новые залы 80x80
new_rr_mazes = """struct rr_maze_declaration RR_MAZES[rr_biome_id_max] = {
    {MAZE_ENTRY(HELL_CREEK, 2048), 7, {
        {12, 12, 4, 4, 14, 14, 1},   // Зал 1 (старт)
        {40, 13, 4, 4, 42, 15, 15},  // Зал 2
        {63, 20, 4, 4, 65, 22, 30},  // Зал 3
        {18, 44, 4, 4, 20, 46, 45},  // Зал 4
        {48, 46, 4, 4, 50, 48, 60},  // Зал 5
        {20, 66, 4, 4, 22, 68, 75},  // Зал 6
        {56, 65, 4, 4, 58, 67, 90},  // Зал 7 (Ultra)
    }},
    {MAZE_ENTRY(PVP, 2048), 7, {
        {38, 10, 4, 4, 40, 12, 1},   // Вход в Ant Hell
        {14, 24, 4, 4, 16, 26, 15},  // Левая камера
        {62, 24, 4, 4, 64, 26, 30},  // Правая камера
        {38, 38, 4, 4, 40, 40, 45},  // Центр
        {14, 56, 4, 4, 16, 58, 60},  // Термиты
        {62, 56, 4, 4, 64, 58, 75},  // Солдаты
        {38, 66, 4, 4, 40, 68, 90},  // Зал королевы / червей
    }},"""

c_code = re.sub(
    r"struct rr_maze_declaration RR_MAZES\[rr_biome_id_max\]\s*=\s*\{\s*\{MAZE_ENTRY\(HELL_CREEK.*?\}\},\s*\{MAZE_ENTRY\(PVP.*?\}\},",
    new_rr_mazes,
    c_code,
    flags=re.DOTALL
)

with open("Shared/StaticData.c", "w") as f:
    f.write(c_code)

print("Готово! Карты 160x160 и фикс RenderArena.c применены.")
