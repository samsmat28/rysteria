import glob, re

# 1. Ищем главный цикл рендера клиента (где вызывается rr_render_arena или emscripten_set_main_loop)
c_files = glob.glob("Client/**/*.c", recursive=True) + glob.glob("Client/*.c")
target_file = None
for fn in c_files:
    with open(fn, "r", encoding="utf-8") as f:
        txt = f.read()
    if "rr_render_arena" in txt and fn != "Client/Renderer/RenderArena.c":
        target_file = fn
        break

if not target_file:
    for fn in c_files:
        with open(fn, "r", encoding="utf-8") as f:
            txt = f.read()
        if "emscripten_set_main_loop" in txt:
            target_file = fn
            break

print("[INFO] Главный файл рендера:", target_file)

# 2. Извлекаем готовый блок rr_draw_shop_house_and_hud из RenderArena.c и переносим его в главный цикл рендера
with open("Client/Renderer/RenderArena.c", "r", encoding="utf-8") as f:
    ra = f.read()

m_fn = re.search(r"(static void rr_draw_shop_house_and_hud\(double cam_x, double cam_y, double zoom\) \{.*?\n\})\n", ra, re.DOTALL)
shop_fn_code = m_fn.group(1) if m_fn else ""

# Убираем старый вызов из RenderArena.c, чтобы не дублировать
ra = re.sub(r"\n\s*rr_draw_shop_house_and_hud\([^;]+\);\n", "\n", ra)
with open("Client/Renderer/RenderArena.c", "w", encoding="utf-8") as f:
    f.write(ra)

if target_file and shop_fn_code:
    with open(target_file, "r", encoding="utf-8") as f:
        tf = f.read()

    if "<emscripten.h>" not in tf and '"emscripten.h"' not in tf:
        tf = "#include <emscripten.h>\n" + tf

    # Находим реальные переменные камеры в target_file или RenderArena.c
    all_client = tf + "\n" + ra
    m_cx = re.search(r"([a-zA-Z0-9_>-]+(?:\.|->)(?:camera|cam|view|smooth_camera|player|self)(?:\.|_)[xX])", all_client)
    cx_expr = m_cx.group(1) if m_cx else "0.0"
    cy_expr = cx_expr[:-1] + ("Y" if cx_expr.endswith("X") else "y")

    # Проверяем, определена ли эта переменная в target_file; если нет — используем 0.0
    root_var = re.split(r"\.|->", cx_expr)
    if root_var not in tf:
        cx_expr, cy_expr = "0.0", "0.0"

    # Вставляем функцию перед вызовом rr_render_arena в target_file
    if "rr_draw_shop_house_and_hud" not in tf:
        tf = tf.replace("rr_render_arena(", shop_fn_code + "\n\n    rr_draw_shop_house_and_hud((double)(" + cx_expr + "), (double)(" + cy_expr + "), 1.0);\n    rr_render_arena(", 1)

    with open(target_file, "w", encoding="utf-8") as f:
        f.write(tf)
    print(f"[OK] Перенесено в {target_file} (камера: {cx_expr}, {cy_expr})")
