import re

path = "Client/Renderer/RenderArena.c"
with open(path, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Ищем в RenderArena.c реальные выражения координат камеры/игрока (например game->camera.x или camera_x)
m_func = re.search(r"void\s+rr_render_arena[^{]*\{(.{1,3500})", code, re.DOTALL)
func_body = m_func.group(1) if m_func else code

# Ищем перевод контекста canvas (ctx_translate / Translate / camera)
m_cam = re.search(r"([a-zA-Z0-9_>-]+\.(?:camera|cam|view|pos|player|self)\.[xy]|[a-zA-Z0-9_>-]+->(?:camera|cam|view|pos|player|self)_[xy]|[a-zA-Z0-9_>-]+->[xy])", func_body)
cam_x_expr = "0.0"
cam_y_expr = "0.0"

if m_cam:
    base = m_cam.group(1)
    if base.endswith(".x") or base.endswith("_x") or base.endswith("->x"):
        cam_x_expr = base
        cam_y_expr = base[:-1] + "y"

# Заменяем вызов rr_draw_shop_house_and_hud на реальные координаты из RenderArena.c
code = re.sub(
    r"rr_draw_shop_house_and_hud\([^;]+\);",
    f"rr_draw_shop_house_and_hud((double)({cam_x_expr}), (double)({cam_y_expr}), 1.0);",
    code
)

# 2. Добавляем кнопку быстрого открытия Лавки/Квестов под кнопкой Account и стрелку-компас на экране
ui_boost = """
            // Кнопка быстрого открытия магазина и квестов под кнопкой Account (слева сверху)
            var quickBar = document.createElement('div');
            quickBar.style.cssText = 'position:fixed;top:56px;left:14px;z-index:9999;display:flex;gap:6px;';
            quickBar.innerHTML =
                '<button id="rr-btn-open-shop" style="background:#8b5a2b;color:#ffd700;border:2px solid #f5c542;border-radius:8px;padding:6px 12px;font-family:Ubuntu,sans-serif;font-weight:700;cursor:pointer;box-shadow:0 3px 8px rgba(0,0,0,0.4);">🏪 Лавка [R]</button>' +
                '<button id="rr-btn-open-quest" style="background:#2e5c22;color:#7eef6d;border:2px solid #7eef6d;border-radius:8px;padding:6px 12px;font-family:Ubuntu,sans-serif;font-weight:700;cursor:pointer;box-shadow:0 3px 8px rgba(0,0,0,0.4);">🌼 Квесты</button>';
            document.body.appendChild(quickBar);

            document.getElementById('rr-btn-open-shop').onclick = function() {
                var m = document.getElementById('rr-shop-modal');
                if (m) {
                    var open = (m.style.display === 'flex');
                    m.style.display = open ? 'none' : 'flex';
                    window.__rrShopDismissed = open;
                    if (!open && window.rrSendShopCmd) window.rrSendShopCmd('/balance');
                }
            };
            document.getElementById('rr-btn-open-quest').onclick = function() {
                var q = document.getElementById('rr-quest-modal');
                if (q) {
                    var open = (q.style.display === 'flex');
                    q.style.display = open ? 'none' : 'flex';
                    window.__rrQuestDismissed = open;
                    if (!open && window.rrSendShopCmd) window.rrSendShopCmd('/quest');
                }
            };
"""

if "rr-btn-open-shop" not in code:
    code = code.replace("document.body.appendChild(hud);", "document.body.appendChild(hud);\n" + ui_boost)

# Ставим домик и НПС прямо в центр спавна (x=220, y=-160 относительно нулевой точки / спавна) и рисуем компас-стрелку если домик за экраном
compass_js = """
        // Стрелка-указатель на Домик-магазин, если он за пределами экрана
        var dx = shopX - camX;
        var dy = shopY - camY;
        var dist = Math.hypot(dx, dy);
        if (dist > 360) {
            var ang = Math.atan2(dy, dx);
            var r = Math.min(canvas.width, canvas.height) * 0.36;
            var ax = canvas.width * 0.5 + Math.cos(ang) * r;
            var ay = canvas.height * 0.5 + Math.sin(ang) * r;
            ctx.save();
            ctx.translate(ax, ay);
            ctx.rotate(ang);
            ctx.fillStyle = '#ffd700';
            ctx.strokeStyle = '#2b1b0e';
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.moveTo(18, 0);
            ctx.lineTo(-10, -11);
            ctx.lineTo(-5, 0);
            ctx.lineTo(-10, 11);
            ctx.closePath();
            ctx.fill();
            ctx.stroke();
            ctx.restore();

            ctx.save();
            ctx.fillStyle = '#ffd700';
            ctx.font = 'bold 13px Ubuntu, sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText('SHOP [R]', ax, ay - 16);
            ctx.restore();
        }
"""

if "SHOP [R]', ax, ay" not in code:
    code = code.replace("        ctx.restore();\n\n        // 4. Квестовый НПС", "        ctx.restore();\n" + compass_js + "\n        // 4. Квестовый НПС")

with open(path, "w", encoding="utf-8") as f:
    f.write(code)

print(f"[OK] Координаты привязаны к ({cam_x_expr}, {cam_y_expr}), добавлен компас и кнопки под Account")
