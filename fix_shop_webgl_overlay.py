import re

path = "Client/Renderer/RenderArena.c"
with open(path, "r", encoding="utf-8") as f:
    ra = f.read()

# 1. Находим реальные переменные камеры/позиции игрока и масштаба в RenderArena.c
# Ищем аргумент функции rr_render_arena
m_sig = re.search(r"void\s+rr_render_arena\s*\(([^)]+)\)", ra)
sig = m_sig.group(1) if m_sig else ""
arg_name = re.findall(r"\b([a-zA-Z0-9_]+)\s*$", sig.split(",")[0])[0] if sig else "client"

# Печатаем первые 40 строк rr_render_arena для диагностики, если понадобится, и ищем поля x/y
m_body = re.search(r"void\s+rr_render_arena\s*\([^)]+\)\s*\{(.{1,2500})", ra, re.DOTALL)
body_snip = m_body.group(1) if m_body else ""

# Ищем в RenderArena.c упоминания camera / view / pos / x / y
m_xy = re.search(r"\b(" + re.escape(arg_name) + r"->(?:[a-zA-Z0-9_]+(?:\.|->))*[xX])\b", body_snip)
if m_xy:
    cx_expr = m_xy.group(1)
    cy_expr = cx_expr[:-1] + ("Y" if cx_expr.endswith("X") else "y")
else:
    cx_expr, cy_expr = "0.0", "0.0"

m_zm = re.search(r"\b(" + re.escape(arg_name) + r"->(?:[a-zA-Z0-9_]+(?:\.|->))*(?:zoom|fov|scale)[a-zA-Z0-9_]*)\b", body_snip)
zm_expr = m_zm.group(1) if m_zm else "1.0"

# 2. Заменяем rr_draw_shop_house_and_hud на версию с отдельным прозрачным 2D-слоем поверх WebGL
new_draw_fn = """
static void rr_draw_shop_house_and_hud(double cam_x, double cam_y, double zoom) {
    if (zoom <= 0.001 || zoom > 50.0) zoom = 1.0;
    EM_ASM({
        var camX = $0;
        var camY = $1;
        var zoom = $2;

        // 1. Создаём отдельный прозрачный 2D Canvas поверх WebGL, чтобы графику НИЧТО не перекрывало
        var overlay = document.getElementById('rr-shop-overlay');
        if (!overlay) {
            overlay = document.createElement('canvas');
            overlay.id = 'rr-shop-overlay';
            overlay.style.cssText = 'position:fixed;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:9990;';
            document.body.appendChild(overlay);
        }
        if (overlay.width !== window.innerWidth || overlay.height !== window.innerHeight) {
            overlay.width = window.innerWidth;
            overlay.height = window.innerHeight;
        }
        var ctx = overlay.getContext('2d');
        ctx.clearRect(0, 0, overlay.width, overlay.height);

        // 2. HUD баланса R, координаты и кнопки быстрого доступа к Лавке и Квестам
        if (!window.__rrShopHudInit) {
            window.__rrShopHudInit = true;
            window.__rrCoins = 100;
            window.__rrInShopZone = false;
            window.__rrInNpcZone = false;

            var hud = document.createElement('div');
            hud.id = 'rr-r-balance-hud';
            hud.style.cssText = 'position:fixed;top:14px;right:190px;z-index:9999;' +
                'background:rgba(28,20,10,0.92);border:2px solid #f5c542;border-radius:10px;' +
                'padding:7px 14px;color:#ffe066;font-family:Ubuntu,sans-serif;font-weight:700;' +
                'font-size:18px;box-shadow:0 4px 12px rgba(0,0,0,0.5);pointer-events:none;' +
                'text-shadow:1px 1px 2px #000;';
            hud.textContent = 'R: 100';
            document.body.appendChild(hud);

            var quickBar = document.createElement('div');
            quickBar.style.cssText = 'position:fixed;top:56px;left:14px;z-index:9999;display:flex;gap:6px;';
            quickBar.innerHTML =
                '<button id="rr-btn-open-shop" style="background:#8b5a2b;color:#ffd700;border:2px solid #f5c542;border-radius:8px;padding:6px 12px;font-family:Ubuntu,sans-serif;font-weight:700;cursor:pointer;box-shadow:0 3px 8px rgba(0,0,0,0.4);">🏪 Лавка [R]</button>' +
                '<button id="rr-btn-open-quest" style="background:#2e5c22;color:#7eef6d;border:2px solid #7eef6d;border-radius:8px;padding:6px 12px;font-family:Ubuntu,sans-serif;font-weight:700;cursor:pointer;box-shadow:0 3px 8px rgba(0,0,0,0.4);">🌼 Квесты</button>';
            document.body.appendChild(quickBar);

            window.rrSetBalance = function(val) {
                var n = parseInt(val, 10);
                if (!isNaN(n)) {
                    window.__rrCoins = n;
                    var el = document.getElementById('rr-r-balance-hud');
                    if (el) el.textContent = 'R: ' + n;
                }
            };
        }

        // Запоминаем точку спавна игрока при первом входе на арену (Hell Creek), чтобы поставить домик рядом
        if (window.__rrSpawnX === undefined && (camX !== 0 || camY !== 0)) {
            window.__rrSpawnX = camX;
            window.__rrSpawnY = camY;
        }
        var baseX = (window.__rrSpawnX !== undefined) ? window.__rrSpawnX : 0.0;
        var baseY = (window.__rrSpawnY !== undefined) ? window.__rrSpawnY : 0.0;

        // Координаты Домика-магазина и Квестового НПС прямо возле спавна в Hell Creek
        var shopX = baseX + 260.0;
        var shopY = baseY - 170.0;
        var npcX  = baseX + 105.0;
        var npcY  = baseY - 135.0;

        var houseW = 220.0;
        var houseH = 150.0;
        var zoneX = shopX;
        var zoneY = shopY + houseH * 0.5 + 55.0;
        var zoneW = 140.0;
        var zoneH = 85.0;

        var inZone = Math.abs(camX - zoneX) <= (zoneW * 0.5 + 25.0) &&
                     Math.abs(camY - zoneY) <= (zoneH * 0.5 + 25.0);
        window.__rrInShopZone = inZone;

        var inNpcZone = Math.hypot(camX - npcX, camY - npcY) <= 75.0;
        window.__rrInNpcZone = inNpcZone;

        ctx.save();
        ctx.translate(overlay.width * 0.5, overlay.height * 0.5);
        ctx.scale(zoom, zoom);
        ctx.translate(-camX, -camY);

        // Золотая зона входа у Домика-магазина
        ctx.fillStyle = inZone ? 'rgba(255, 215, 0, 0.45)' : 'rgba(255, 200, 40, 0.25)';
        ctx.strokeStyle = '#ffd700';
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.rect(zoneX - zoneW * 0.5, zoneY - zoneH * 0.5, zoneW, zoneH);
        ctx.fill();
        ctx.stroke();

        ctx.fillStyle = '#fff3b0';
        ctx.font = 'bold 15px Ubuntu, sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(inZone ? 'ВХОД В ЛАВКУ' : 'SHOP ZONE', zoneX, zoneY);

        // Тень домика
        ctx.fillStyle = 'rgba(0, 0, 0, 0.28)';
        ctx.fillRect(shopX - houseW * 0.5 + 10, shopY - houseH * 0.5 + 12, houseW, houseH);

        // Деревянные стены
        ctx.fillStyle = '#8b5a2b';
        ctx.strokeStyle = '#4a2e14';
        ctx.lineWidth = 6;
        ctx.fillRect(shopX - houseW * 0.5, shopY - houseH * 0.5, houseW, houseH);
        ctx.strokeRect(shopX - houseW * 0.5, shopY - houseH * 0.5, houseW, houseH);

        // Дверь
        ctx.fillStyle = '#5c3317';
        ctx.strokeStyle = '#3b1f0b';
        ctx.lineWidth = 4;
        ctx.fillRect(shopX - 26, shopY + houseH * 0.5 - 68, 52, 68);
        ctx.strokeRect(shopX - 26, shopY + houseH * 0.5 - 68, 52, 68);

        // Окна
        ctx.fillStyle = '#ffe999';
        ctx.fillRect(shopX - houseW * 0.5 + 22, shopY - 12, 36, 36);
        ctx.strokeRect(shopX - houseW * 0.5 + 22, shopY - 12, 36, 36);
        ctx.fillRect(shopX + houseW * 0.5 - 58, shopY - 12, 36, 36);
        ctx.strokeRect(shopX + houseW * 0.5 - 58, shopY - 12, 36, 36);

        // Крыша
        ctx.fillStyle = '#a04020';
        ctx.strokeStyle = '#4a1c0d';
        ctx.lineWidth = 6;
        ctx.beginPath();
        ctx.moveTo(shopX - houseW * 0.5 - 18, shopY - houseH * 0.5 + 8);
        ctx.lineTo(shopX, shopY - houseH * 0.5 - 65);
        ctx.lineTo(shopX + houseW * 0.5 + 18, shopY - houseH * 0.5 + 8);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();

        // Вывеска SHOP [R]
        ctx.fillStyle = '#2b1b0e';
        ctx.strokeStyle = '#ffd700';
        ctx.lineWidth = 3.5;
        ctx.fillRect(shopX - 83, shopY - houseH * 0.5 - 32, 166, 40);
        ctx.strokeRect(shopX - 83, shopY - houseH * 0.5 - 32, 166, 40);
        ctx.fillStyle = '#ffd700';
        ctx.font = 'bold 22px Ubuntu, sans-serif';
        ctx.fillText('SHOP [R]', shopX, shopY - houseH * 0.5 - 11);

        // Квестовый НПС-цветочек с личиком как у игрока
        var bobY = Math.sin(performance.now() * 0.004) * 2.5;
        ctx.fillStyle = inNpcZone ? 'rgba(126, 239, 109, 0.35)' : 'rgba(126, 239, 109, 0.18)';
        ctx.strokeStyle = '#7eef6d';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.arc(npcX, npcY, 58, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();

        ctx.fillStyle = '#ffe763';
        ctx.strokeStyle = '#cfb73c';
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.arc(npcX, npcY + bobY, 26, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();

        ctx.fillStyle = '#1f1f1f';
        ctx.beginPath();
        ctx.arc(npcX - 8, npcY - 5 + bobY, 3.5, 0, Math.PI * 2);
        ctx.arc(npcX + 8, npcY - 5 + bobY, 3.5, 0, Math.PI * 2);
        ctx.fill();

        ctx.strokeStyle = '#1f1f1f';
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        ctx.arc(npcX, npcY + 2 + bobY, 7, 0.15 * Math.PI, 0.85 * Math.PI);
        ctx.stroke();

        ctx.fillStyle = '#7eef6d';
        ctx.font = 'bold 15px Ubuntu, sans-serif';
        ctx.fillText('! КВЕСТЫ [R] !', npcX, npcY - 38 + bobY);

        ctx.restore();

        // Стрелка-указатель на Домик-магазин, если игрок отошёл далеко
        var dx = shopX - camX;
        var dy = shopY - camY;
        if (Math.hypot(dx, dy) > 380) {
            var ang = Math.atan2(dy, dx);
            var r = Math.min(overlay.width, overlay.height) * 0.36;
            var ax = overlay.width * 0.5 + Math.cos(ang) * r;
            var ay = overlay.height * 0.5 + Math.sin(ang) * r;
            ctx.save();
            ctx.translate(ax, ay);
            ctx.rotate(ang);
            ctx.fillStyle = '#ffd700';
            ctx.strokeStyle = '#2b1b0e';
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.moveTo(18, 0);
            ctx.lineTo(-10, -11);

cat << 'EOF' > part1_overlay.py
import re

path = "Client/Renderer/RenderArena.c"
with open(path, "r", encoding="utf-8") as f:
    ra = f.read()

old_head = """        var canvas = document.querySelector('canvas');
        if (!canvas) return;
        var ctx = canvas.getContext('2d');
        if (!ctx) return;

        var shopX = 340.0;
        var shopY = -240.0;"""

new_head = """        var canvas = document.getElementById('rr-shop-overlay');
        if (!canvas) {
            canvas = document.createElement('canvas');
            canvas.id = 'rr-shop-overlay';
            canvas.style.cssText = 'position:fixed;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:9990;';
            document.body.appendChild(canvas);
        }
        if (canvas.width !== window.innerWidth || canvas.height !== window.innerHeight) {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }
        var ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        if (window.__rrSpawnX === undefined && (camX !== 0 || camY !== 0)) {
            window.__rrSpawnX = camX;
            window.__rrSpawnY = camY;
        }
        var baseX = (window.__rrSpawnX !== undefined) ? window.__rrSpawnX : 0.0;
        var baseY = (window.__rrSpawnY !== undefined) ? window.__rrSpawnY : 0.0;
        var shopX = baseX + 250.0;
        var shopY = baseY - 170.0;"""

if old_head in ra:
    ra = ra.replace(old_head, new_head)
    ra = ra.replace("var npcX = 170.0;\n        var npcY = -185.0;", "var npcX = baseX + 100.0;\n        var npcY = baseY - 135.0;")
    with open(path, "w", encoding="utf-8") as f:
        f.write(ra)
    print("[OK] Часть 1 готова")
