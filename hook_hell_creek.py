import re

with open("Client/Renderer/RenderArena.c", "r", encoding="utf-8") as f:
    ra = f.read()

m_fn = re.search(r"(static void rr_draw_shop_house_and_hud\(double cam_x, double cam_y, double zoom\) \{.*?\n\})\n", ra, re.DOTALL)
shop_fn = m_fn.group(1) if m_fn else ""

with open("Client/Assets/Tile/HellCreek.c", "r", encoding="utf-8") as f:
    hc = f.read()

if "<emscripten.h>" not in hc and '"emscripten.h"' not in hc:
    hc = "#include <emscripten.h>\n" + hc

# Смотрим параметры функции рендера в HellCreek.c (обычно camera_x, camera_y, zoom или ctx)
m_func = re.search(r"void\s+([a-zA-Z0-9_]+)\s*\(([^)]+)\)\s*\{", hc)
func_name = m_func.group(1) if m_func else ""
params_str = m_func.group(2) if m_func else ""

# Находим имена переменных координат и зума из параметров функции в HellCreek.c
p_names = re.findall(r"\b([a-zA-Z0-9_]+)\s*(?:,|$)", params_str)
cx = next((p for p in p_names if "x" in p.lower()), "0.0")
cy = next((p for p in p_names if "y" in p.lower()), "0.0")
zm = next((p for p in p_names if "zoom" in p.lower() or "scale" in p.lower()), "1.0")

# Если передаётся структура (например ctx или game), ищем её поля
if cx == "0.0" and p_names:
    st = next(iter(p_names))
    m_sx = re.search(r"\b" + re.escape(st) + r"->([a-zA-Z0-9_>-]*?[xX])\b", hc)
    if m_sx:
        cx = f"{st}->{m_sx.group(1)}"
        cy = cx[:-1] + ("Y" if cx.endswith("X") else "y")
    m_sz = re.search(r"\b" + re.escape(st) + r"->([a-zA-Z0-9_>-]*?(?:zoom|scale|fov)[a-zA-Z0-9_>-]*)\b", hc)
    if m_sz:
        zm = f"{st}->{m_sz.group(1)}"

if "rr_draw_shop_house_and_hud" not in hc and shop_fn and m_func:
    hc = hc[:m_func.start()] + "\n" + shop_fn + "\n" + hc[m_func.start():]
    m_func = re.search(r"void\s+" + re.escape(func_name) + r"\s*\([^)]+\)\s*\{", hc)
    depth, end_p = 0, -1
    for i in range(m_func.end() - 1, len(hc)):
        if hc[i] == "{": depth += 1
        elif hc[i] == "}":
            depth -= 1
            if depth == 0:
                end_p = i
                break
    if end_p != -1:
        call = f"\n    rr_draw_shop_house_and_hud((double)({cx}), (double)({cy}), (double)({zm}));\n"
        hc = hc[:end_p] + call + hc[end_p:]
        with open("Client/Assets/Tile/HellCreek.c", "w", encoding="utf-8") as f:
            f.write(hc)
        print(f"[OK] Встроено в HellCreek.c -> {func_name}() с координатами ({cx}, {cy}, {zm})")
