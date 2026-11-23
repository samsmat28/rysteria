import re

with open("Shared/StaticData.c", "r", encoding="utf-8") as f:
    sdata = f.read()

# 1. Поднимаем максимальную редкость спавна для мобов Hell Creek с super до gods
sdata = sdata.replace("rr_rarity_id_super,", "rr_rarity_id_gods,")

# 2. Обновляем дальнюю правую-нижнюю зону в RR_DEFINE_MAZE(HELL_CREEK, 160) -> Omega (o), Hyper (h), Gods (g)
maze_match = re.search(r'(RR_DEFINE_MAZE\(HELL_CREEK,\s*160\)\s*=\s*\{)(.*?)(\n\};)', sdata, re.DOTALL)
assert maze_match, "Не найден блок RR_DEFINE_MAZE(HELL_CREEK, 160)"

rows = re.findall(r'\{([^}]+)\}', maze_match.group(2))
assert len(rows) == 80, f"Ожидалось 80 строк, найдено {len(rows)}"

grid = []
for r in rows:
    tokens = [t.strip() for t in r.split(',') if t.strip()]
    assert len(tokens) == 80, f"Ожидалось 80 колонок, найдено {len(tokens)}"
    grid.append(tokens)

# Находим все клетки 'a' / 'A' (текущая финальная зона Super в правом-нижнем углу Hell Creek)
super_cells = [(y, x) for y in range(80) for x in range(80) if grid[y][x] in ('a', 'A')]
assert super_cells, "Не найдены клетки 'a'/'A' в карте HELL_CREEK"

# Сортируем клетки финальной зоны по прогрессии вправо-вниз (x + y * 0.8)
super_cells.sort(key=lambda p: p[1] + p[0] * 0.8)
n = len(super_cells)

for idx, (y, x) in enumerate(super_cells):
    ratio = idx / max(1, n - 1)
    is_upper = grid[y][x].isupper()
    if ratio < 0.35:
        sym = 'A' if is_upper else 'a'  # Super
    elif ratio < 0.62:
        sym = 'O' if is_upper else 'o'  # Omega (фиолетовый)
    elif ratio < 0.84:
        sym = 'H' if is_upper else 'h'  # Hyper (серый)
    else:
        sym = 'G' if is_upper else 'g'  # Gods (белый)
    grid[y][x] = sym

new_rows = [f"    {{{','.join(grid[y])}}}, // {y}" for y in range(80)]
new_maze_block = maze_match.group(1) + "\n" + "\n".join(new_rows) + maze_match.group(3)
sdata = sdata[:maze_match.start()] + new_maze_block + sdata[maze_match.end():]

with open("Shared/StaticData.c", "w", encoding="utf-8") as f:
    f.write(sdata)

print(f"Готово! В Hell Creek добавлены зоны Omega, Hyper и Gods ({n} клеток распределено).")
