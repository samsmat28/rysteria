import random

def generate_maze(size=80):
    grid = [['_' for _ in range(size)] for _ in range(size)]
    x, y = size // 2, size // 2
    steps = 3500
    
    for _ in range(steps):
        grid[y][x] = 'c'
        dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        nx, ny = x + dx * 2, y + dy * 2
        if 2 <= nx < size - 2 and 2 <= ny < size - 2:
            grid[y + dy][x + dx] = 'c'
            x, y = nx, ny
            
    return grid

maze_grid = generate_maze(80)

with open("Plains_map.h", "w") as f:
    f.write("// Автоматически сгенерированная карта для Plains\n")
    f.write("RR_DEFINE_MAZE(PLAINS, 160) = {\n")
    for i, row in enumerate(maze_grid):
        f.write("    {" + ",".join(row) + "}, // " + str(i) + "\n")
    f.write("};\n")

print("Готово! Файл Plains_map.h успешно создан.")
