with open("Client/Renderer/RenderArena.c", "r", encoding="utf-8") as f:
    code = f.read()

old = "uint32_t h = rr_get_hash((uint32_t)(((newLeftX + 8192) / GRID_SIZE) * 73856093u ^ ((currY + 8192) / GRID_SIZE) * 19349663u));"
new = "uint32_t h = rr_get_hash(((uint32_t)((newLeftX + 8192) / GRID_SIZE) * 73856093u) ^ ((uint32_t)((currY + 8192) / GRID_SIZE) * 19349663u));"

assert old in code, "Строка не найдена"
with open("Client/Renderer/RenderArena.c", "w", encoding="utf-8") as f:
    f.write(code.replace(old, new, 1))
print("Исправлено!")
