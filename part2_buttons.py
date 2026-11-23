import re

path = "Client/Renderer/RenderArena.c"
with open(path, "r", encoding="utf-8") as f:
    ra = f.read()

# 1. Ищем реальные переменные камеры в RenderArena.c (например client->camera.x или ctx->camera_x)
m_sig = re.search(r"void\s+rr_render_arena\s*\(([^)]+)\)", ra)
arg = re.findall(r"\b([a-zA-Z0-9_]+)\s*$", m_sig.group(1).split(",")) if m_sig else "client"
m_cam = re.search(r"\b(" + re.escape(arg) + r"->(?:[a-zA-Z0-9_]+(?:\.|->))*[xX])\b", ra)
if m_cam:
    cx = m_cam.group(1)
    cy = cx[:-1] + ("Y" if cx.endswith("X") else "y")
    ra = re.sub(r"rr_draw_shop_house_and_hud\([^;]+\);", f"rr_draw_shop_house_and_hud((double)({cx}), (double)({cy}), 1.0);", ra)

# 2. Добавляем кнопки Лавки и Квестов слева сверху под Account
btns = """
            var qb = document.createElement('div');
            qb.style.cssText = 'position:fixed;top:56px;left:14px;z-index:9999;display:flex;gap:6px;';
            qb.innerHTML =
                '<button id="rr-open-s" style="background:#8b5a2b;color:#ffd700;border:2px solid #f5c542;border-radius:8px;padding:6px 12px;font-weight:700;cursor:pointer;">🏪 Лавка [R]</button>' +
                '<button id="rr-open-q" style="background:#2e5c22;color:#7eef6d;border:2px solid #7eef6d;border-radius:8px;padding:6px 12px;font-weight:700;cursor:pointer;">🌼 Квесты</button>';
            document.body.appendChild(qb);
            document.getElementById('rr-open-s').onclick = function() {
                var m = document.getElementById('rr-shop-modal');
                if (m) { var v = m.style.display === 'flex'; m.style.display = v ? 'none' : 'flex'; window.__rrShopDismissed = v; }
            };
            document.getElementById('rr-open-q').onclick = function() {
                var q = document.getElementById('rr-quest-modal');
                if (q) { var v = q.style.display === 'flex'; q.style.display = v ? 'none' : 'flex'; window.__rrQuestDismissed = v; }
            };
"""

if "rr-open-s" not in ra:
    ra = ra.replace("document.body.appendChild(hud);", "document.body.appendChild(hud);\n" + btns)
    with open(path, "w", encoding="utf-8") as f:
        f.write(ra)
    print("[OK] Часть 2 готова")
