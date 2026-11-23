import glob, re

# 1. Находим реальную структуру состояния клиента и координаты камеры/игрока в Client/Renderer/RenderArena.c
with open("Client/Renderer/RenderArena.c", "r", encoding="utf-8") as f:
    ra = f.read()

# Ищем функцию отрисовки арены и её аргументы (обычно struct rr_client *client или struct rr_renderer *renderer)
m_sig = re.search(r"void\s+rr_render_arena\s*\(([^)]+)\)", ra)
sig = m_sig.group(1) if m_sig else ""
arg_name = re.findall(r"\b([a-zA-Z0-9_]+)\s*$", sig.split(",")) if sig else "client"

# Ищем реальные поля координат камеры и масштаба в RenderArena.c
m_cam_field = re.search(r"\b" + re.escape(arg_name) + r"->([a-zA-Z0-9_>-]*?(?:camera|cam|view|smooth|pos|player|self)[a-zA-Z0-9_>-]*?\.[xy])\b", ra)
if not m_cam_field:
    m_cam_field = re.search(r"\b" + re.escape(arg_name) + r"->([a-zA-Z0-9_>-]+?\.[xy])\b", ra)

if m_cam_field:
    base = m_cam_field.group(1)[:-2]
    cx_expr = f"{arg_name}->{base}.x"
    cy_expr = f"{arg_name}->{base}.y"
else:
    cx_expr, cy_expr = "0.0", "0.0"

m_zoom_field = re.search(r"\b" + re.escape(arg_name) + r"->([a-zA-Z0-9_>-]*?(?:zoom|fov|scale)[a-zA-Z0-9_>-]*)\b", ra)
zoom_expr = f"{arg_name}->{m_zoom_field.group(1)}" if m_zoom_field else "1.0"

# Проверяем, как определяется текущая карта/локация (Hell Creek) в клиенте
all_c = ""
for fn in glob.glob("Client/**/*.[ch]", recursive=True) + glob.glob("Shared/*.[ch]"):
    with open(fn, "r", encoding="utf-8") as f:
        all_c += f.read() + "\n"

# Ищем координаты спавна или центра Hell Creek в Shared/ или Server/
hell_x, hell_y = 0.0, 0.0
for fn in glob.glob("Server/**/*.[ch]", recursive=True) + glob.glob("Shared/**/*.[ch]", recursive=True):
    with open(fn, "r", encoding="utf-8") as f:
        stxt = f.read()
    m_hc = re.search(r"Hell\s*Creek.{1,400}?(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)", stxt, re.DOTALL | re.IGNORECASE)
    if m_hc:
        hell_x = float(m_hc.group(1))
        hell_y = float(m_hc.group(2))
        break

# Ставим Домик-магазин и Квестового НПС рядом с точкой спавна Hell Creek (+260, -180 от центра спавна)
shop_x = hell_x + 260.0
shop_y = hell_y - 180.0
npc_x  = hell_x + 110.0
npc_y  = hell_y - 140.0

# 2. Обновляем координаты в функции rr_draw_shop_house_and_hud и подключаем её в самом конце rr_render_arena (поверх фона Hell Creek)
for fn in glob.glob("Client/**/*.c", recursive=True) + glob.glob("Client/*.c"):
    with open(fn, "r", encoding="utf-8") as f:
        txt = f.read()
    if "rr_draw_shop_house_and_hud" in txt:
        txt = re.sub(r"var shopX = [^;]+;", f"var shopX = {shop_x};", txt)
        txt = re.sub(r"var shopY = [^;]+;", f"var shopY = {shop_y};", txt)
        txt = re.sub(r"var npcX = [^;]+;", f"var npcX = {npc_x};", txt)
        txt = re.sub(r"var npcY = [^;]+;", f"var npcY = {npc_y};", txt)
        # Если это не RenderArena.c, убираем оттуда дублирующий вызов перед rr_render_arena
        if fn != "Client/Renderer/RenderArena.c":
            txt = re.sub(r"\n\s*rr_draw_shop_house_and_hud\([^;]+\);\n", "\n", txt)
        with open(fn, "w", encoding="utf-8") as f:
            f.write(txt)

# Вставляем вызов в конец rr_render_arena (после отрисовки арены, чтобы домик и НПС были видны поверх земли Hell Creek)
with open("Client/Renderer/RenderArena.c", "r", encoding="utf-8") as f:
    ra = f.read()

ra = re.sub(r"\n\s*rr_draw_shop_house_and_hud\([^;]+\);\n", "\n", ra)
m_ra_start = re.search(r"void\s+rr_render_arena\s*\([^)]+\)\s*\{", ra)
if m_ra_start:
    depth, end_pos = 0, -1
    for i in range(m_ra_start.end() - 1, len(ra)):
        if ra[i] == "{": depth += 1
        elif ra[i] == "}":
            depth -= 1
            if depth == 0:
                end_pos = i
                break
    if end_pos != -1:
        call = f"\n    rr_draw_shop_house_and_hud((double)({cx_expr}), (double)({cy_expr}), (double)({zoom_expr}));\n"
        ra = ra[:end_pos] + call + ra[end_pos:]

with open("Client/Renderer/RenderArena.c", "w", encoding="utf-8") as f:
    f.write(ra)

print(f"[OK] Размещено в Hell Creek: shop=({shop_x}, {shop_y}), npc=({npc_x}, {npc_y}), cam=({cx_expr}, {cy_expr})")
