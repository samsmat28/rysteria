import re

with open("Shared/StaticData.c", "r", encoding="utf-8") as f:
    sdata = f.read()

maze_match = re.search(r'(RR_DEFINE_MAZE\(HELL_CREEK,\s*160\)\s*=\s*\{)(.*?)(\n\};)', sdata, re.DOTALL)
assert maze_match, "Не найден блок RR_DEFINE_MAZE(HELL_CREEK, 160)"

rows = re.findall(r'\{([^}]+)\}', maze_match.group(2))
grid = [[t.strip() for t in r.split(',') if t.strip()] for r in rows]

# Находим финальную комнату 'U' / 'u' (справа-снизу в HELL_CREEK)
end_cells = [(y, x) for y in range(80) for x in range(80) if grid[y][x] in ('u', 'U') and (x > 35 or y > 50)]
assert end_cells, "Не найдены финальные клетки 'U' в HELL_CREEK"

# Делим финальную зону по координате x слева направо на Super -> Omega -> Hyper -> Gods
min_x = min(x for y, x in end_cells)
max_x = max(x for y, x in end_cells)
span = max(1, max_x - min_x)

for y, x in end_cells:
    ratio = (x - min_x) / span
    if ratio < 0.30:
        grid[y][x] = 'a'   # Super
    elif ratio < 0.58:
        grid[y][x] = 'o'   # Omega (фиолетовый)
    elif ratio < 0.82:
        grid[y][x] = 'h'   # Hyper (серый)
    else:
        grid[y][x] = 'g'   # Gods (белый)

new_rows = [f"    {{{','.join(grid[y])}}}, // {y}" for y in range(80)]
sdata = sdata[:maze_match.start()] + maze_match.group(1) + "\n" + "\n".join(new_rows) + maze_match.group(3) + sdata[maze_match.end():]

with open("Shared/StaticData.c", "w", encoding="utf-8") as f:
    f.write(sdata)

print(f"Готово! В Hell Creek добавлены зоны Super, Omega, Hyper и Gods ({len(end_cells)} клеток).")
