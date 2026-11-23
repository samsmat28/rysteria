import re

with open("Server/Simulation.c", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Уменьшаем максимальное количество мобов (max_points * 0.45)
target_max = "float max_points = get_max_points(this, grid);"
replacement_max = "float max_points = get_max_points(this, grid) * 0.45f;"
assert target_max in code, "Не найдена строка max_points"

# 2. Увеличиваем время ожидания между спавнами в 4.5 раза
pattern_spawn = re.compile(
    r'(float spawn_at = base_modifier \* difficulty_modifier \* overload_modifier /\s*\(player_modifier\);)'
)
m = pattern_spawn.search(code)
assert m, "Не найдена строка spawn_at"

if "* 0.45f" not in code:
    code = code.replace(target_max, replacement_max, 1)
    code = pattern_spawn.sub(r'\1\n    spawn_at *= 4.5f;', code, count=1)
    with open("Server/Simulation.c", "w", encoding="utf-8") as f:
        f.write(code)
    print("Готово! Интервал спавна увеличен в 4.5 раза, а максимальное число мобов снижено вдвое.")
else:
    print("Настройки спавна уже применены.")
