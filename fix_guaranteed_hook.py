import glob, re

# 1. Ищем главный цикл рендера в Client/
client_files = glob.glob("Client/**/*.[ch]", recursive=True)
hooked_file = None

# Сначала достаём готовую функцию rr_draw_shop_house_and_hud из RenderArena.c
with open("Client/Renderer/RenderArena.c", "r", encoding="utf-8") as f:
    ra = f.read()

m_fn = re.search(r"(static void rr_draw_shop_house_and_hud\(double cam_x, double cam_y, double zoom\) \{.*?\n\})\n", ra, re.DOTALL)
shop_fn = m_fn.group(1) if m_fn else ""

# Находим реальную точку вызова отрисовки в главном файле клиента (обычно Main.c или Client.c)
for fn in client_files:
    with open(fn, "r", encoding="utf-8") as f:
        txt = f.read()
    if "emscripten_set_main_loop" in txt:
        # Ищем функцию-коллбэк, переданную в emscripten_set_main_loop(loop_fn, ...)
        m_cb = re.search(r"emscripten_set_main_loop\s*\(\s*([a-zA-Z0-9_]+)", txt)
        if m_cb:
            cb_name = m_cb.group(1)
            m_cb_def = re.search(r"void\s+" + re.escape(cb_name) + r"\s*\([^)]*\)\s*\{", txt)
            if m_cb_def and shop_fn:
                if "<emscripten.h>" not in txt and '"emscripten.h"' not in txt:
                    txt = "#include <emscripten.h>\n" + txt
                # Убираем старую копию, если есть
                txt = re.sub(r"static void rr_draw_shop_house_and_hud\(double cam_x, double cam_y, double zoom\) \{.*?\n\}\n", "", txt, flags=re.DOTALL)
                txt = re.sub(r"\n\s*rr_draw_shop_house_and_hud\([^;]+\);\n", "\n", txt)

                # Ищем координаты камеры в этом файле (например client.camera.x или g_client.camera.x)
                m_c = re.search(r"\b([a-zA-Z0-9_]+(?:\.|->)(?:camera|cam|view|smooth_camera|player|self)(?:\.|_)[xX])\b", txt)
                cx = m_c.group(1) if m_c else "0.0"
                cy = cx[:-1] + ("Y" if cx.endswith("X") else "y")

                # Вставляем функцию перед cb_name и её вызов в самый конец cb_name
                m_cb_def = re.search(r"void\s+" + re.escape(cb_name) + r"\s*\([^)]*\)\s*\{", txt)
                txt = txt[:m_cb_def.start()] + "\n" + shop_fn + "\n" + txt[m_cb_def.start():]

                m_cb_def = re.search(r"void\s+" + re.escape(cb_name) + r"\s*\([^)]*\)\s*\{", txt)
                depth, end_p = 0, -1
                for i in range(m_cb_def.end() - 1, len(txt)):
                    if txt[i] == "{": depth += 1
                    elif txt[i] == "}":
                        depth -= 1
                        if depth == 0:
                            end_p = i
                            break
                if end_p != -1:
                    call = f"\n    rr_draw_shop_house_and_hud((double)({cx}), (double)({cy}), 1.0);\n"
                    txt = txt[:end_p] + call + txt[end_p:]
                    with open(fn, "w", encoding="utf-8") as f:
                        f.write(txt)
                    hooked_file = fn
                    print(f"[OK] Встроено в главный цикл {cb_name}() файла {fn}, камера: ({cx}, {cy})")
        break

if not hooked_file:
    print("[WARN] Не найден emscripten_set_main_loop, список .c файлов:", [f for f in client_files if f.endswith(".c")])
