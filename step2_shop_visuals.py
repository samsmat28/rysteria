import re

path = "Client/Renderer/RenderArena.c"
with open(path, "r", encoding="utf-8") as f:
    code = f.read()

if "<emscripten.h>" not in code and '"emscripten.h"' not in code:
    code = "#include <emscripten.h>\n" + code

# Определяем имена переменных камеры/игрока и масштаба в RenderArena.c
m_cam_x = re.search(r"\b(camera_x|cam_x|view_x|center_x|player_x|self_x|x)\b", code)
m_cam_y = re.search(r"\b(camera_y|cam_y|view_y|center_y|player_y|self_y|y)\b", code)
m_zoom  = re.search(r"\b(zoom|scale|fov|camera_zoom)\b", code)

# Ищем функцию отрисовки арены
m_func = re.search(r"(void\s+rr_render_arena[^{]*\{)", code)
if not m_func:
    m_func = re.search(r"(void\s+[a-zA-Z0-9_]*render[a-zA-Z0-9_]*arena[^{]*\{)", code, re.IGNORECASE)

func_header = m_func.group(1) if m_func else ""
# Извлекаем параметры функции отрисовки арены, чтобы точно знать имена координат
params = re.findall(r"(?:float|double|int)\s+([a-zA-Z0-9_]+)", func_header)
px_var = params[0] if len(params) >= 2 else (m_cam_x.group(1) if m_cam_x else "0.0f")
py_var = params[1] if len(params) >= 2 else (m_cam_y.group(1) if m_cam_y else "0.0f")
zm_var = params[2] if len(params) >= 3 else (m_zoom.group(1) if m_zoom else "1.0f")

shop_render_fn = """
static void rr_draw_shop_house_and_hud(double cam_x, double cam_y, double zoom) {
    if (zoom <= 0.001) zoom = 1.0;
    EM_ASM({
        var camX = $0;
        var camY = $1;
        var zoom = $2;

        // 1. Инициализация HUD индикатора баланса R и перехватчика баланса из чата
        if (!window.__rrShopHudInit) {
            window.__rrShopHudInit = true;
            window.__rrCoins = 100;
            window.__rrInShopZone = false;

            var hud = document.createElement('div');
            hud.id = 'rr-r-balance-hud';
            hud.style.cssText = 'position:fixed;top:14px;right:18px;z-index:9999;' +
                'background:rgba(28,20,10,0.88);border:2px solid #f5c542;border-radius:10px;' +
                'padding:8px 16px;color:#ffe066;font-family:Ubuntu,sans-serif;font-weight:700;' +
                'font-size:20px;box-shadow:0 4px 12px rgba(0,0,0,0.45);pointer-events:none;' +
                'text-shadow:1px 1px 2px #000;';
            hud.textContent = 'R: 100';
            document.body.appendChild(hud);

            window.rrSetBalance = function(val) {
                var n = parseInt(val, 10);
                if (!isNaN(n)) {
                    window.__rrCoins = n;
                    var el = document.getElementById('rr-r-balance-hud');
                    if (el) el.textContent = 'R: ' + n;
                }
            };

            // Автоматически отслеживаем ответы сервера [Shop] в DOM-чате или canvas
            setInterval(function() {
                var text = document.body ? document.body.innerText : '';
                var matches = text.match(/(?:Баланс|баланс):\\s*(\\d+)\\s*R/g);
                if (matches && matches.length > 0) {
                    var last = matches[matches.length - 1];
                    var m = last.match(/(\\d+)/);
                    if (m) window.rrSetBalance(m[1]);
                }
            }, 600);
        }

        // 2. Отрисовка Домика-магазина на канвасе рядом со спавном (мир: x=340, y=-240)
        var canvas = document.querySelector('canvas');
        if (!canvas) return;
        var ctx = canvas.getContext('2d');
        if (!ctx) return;

        var shopX = 340.0;
        var shopY = -240.0;
        var houseW = 220.0;
        var houseH = 150.0;

        // Проверка нахождения игрока (camX, camY) в золотой зоне входа перед дверью
        var zoneX = shopX;
        var zoneY = shopY + houseH * 0.5 + 55.0;
        var zoneW = 140.0;
        var zoneH = 85.0;
        var inZone = Math.abs(camX - zoneX) <= (zoneW * 0.5 + 20.0) &&
                     Math.abs(camY - zoneY) <= (zoneH * 0.5 + 20.0);
        window.__rrInShopZone = inZone;

        ctx.save();
        ctx.translate(canvas.width * 0.5, canvas.height * 0.5);
        ctx.scale(zoom, zoom);
        ctx.translate(-camX, -camY);

        // Золотистая зона входа на полу
        ctx.fillStyle = inZone ? 'rgba(255, 215, 0, 0.42)' : 'rgba(255, 200, 40, 0.24)';
        ctx.strokeStyle = '#ffd700';
        ctx.lineWidth = 4;
        ctx.beginPath();
        if (ctx.roundRect) {
            ctx.roundRect(zoneX - zoneW * 0.5, zoneY - zoneH * 0.5, zoneW, zoneH, 14);
        } else {
            ctx.rect(zoneX - zoneW * 0.5, zoneY - zoneH * 0.5, zoneW, zoneH);
        }
        ctx.fill();
        ctx.stroke();

        ctx.fillStyle = '#fff3b0';
        ctx.font = 'bold 16px Ubuntu, sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(inZone ? 'ВХОД В МАГАЗИН' : 'SHOP ZONE', zoneX, zoneY);

        // Тень домика
        ctx.fillStyle = 'rgba(0, 0, 0, 0.25)';
        ctx.fillRect(shopX - houseW * 0.5 + 10, shopY - houseH * 0.5 + 12, houseW, houseH);

        // Деревянные стены
        ctx.fillStyle = '#8b5a2b';
        ctx.strokeStyle = '#4a2e14';
        ctx.lineWidth = 6;
        ctx.fillRect(shopX - houseW * 0.5, shopY - houseH * 0.5, houseW, houseH);
        ctx.strokeRect(shopX - houseW * 0.5, shopY - houseH * 0.5, houseW, houseH);

        // Горизонтальные доски стен
        ctx.strokeStyle = 'rgba(60, 32, 10, 0.45)';
        ctx.lineWidth = 2;
        for (var py = shopY - houseH * 0.5 + 25; py < shopY + houseH * 0.5; py += 25) {
            ctx.beginPath();
            ctx.moveTo(shopX - houseW * 0.5 + 4, py);
            ctx.lineTo(shopX + houseW * 0.5 - 4, py);
            ctx.stroke();
        }

        // Дверь
        var doorW = 52;
        var doorH = 68;
        ctx.fillStyle = '#5c3317';
        ctx.strokeStyle = '#3b1f0b';
        ctx.lineWidth = 4;
        ctx.fillRect(shopX - doorW * 0.5, shopY + houseH * 0.5 - doorH, doorW, doorH);
        ctx.strokeRect(shopX - doorW * 0.5, shopY + houseH * 0.5 - doorH, doorW, doorH);

        // Золотая ручка двери
        ctx.fillStyle = '#ffd700';
        ctx.beginPath();
        ctx.arc(shopX + doorW * 0.28, shopY + houseH * 0.5 - doorH * 0.45, 4.5, 0, Math.PI * 2);
        ctx.fill();

        // Окна по бокам
        ctx.fillStyle = '#ffe999';
        ctx.strokeStyle = '#4a2e14';
        ctx.lineWidth = 3;
        ctx.fillRect(shopX - houseW * 0.5 + 22, shopY - 12, 36, 36);
        ctx.strokeRect(shopX - houseW * 0.5 + 22, shopY - 12, 36, 36);
        ctx.fillRect(shopX + houseW * 0.5 - 58, shopY - 12, 36, 36);
        ctx.strokeRect(shopX + houseW * 0.5 - 58, shopY - 12, 36, 36);

        // Деревянная крыша
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

        // Крупная вывеска "SHOP [R]"
        var signW = 166;
        var signH = 40;
        var signY = shopY - houseH * 0.5 - 12;
        ctx.fillStyle = '#2b1b0e';
        ctx.strokeStyle = '#ffd700';
        ctx.lineWidth = 3.5;
        ctx.fillRect(shopX - signW * 0.5, signY - signH * 0.5, signW, signH);
        ctx.strokeRect(shopX - signW * 0.5, signY - signH * 0.5, signW, signH);

        ctx.fillStyle = '#ffd700';
        ctx.font = 'bold 22px Ubuntu, sans-serif';
        ctx.fillText('SHOP [R]', shopX, signY + 1);

        ctx.restore();
    }, cam_x, cam_y, zoom);
}
"""

if "rr_draw_shop_house_and_hud" not in code:
    if m_func:
        idx = m_func.start()
        code = code[:idx] + shop_render_fn + "\n" + code[idx:]
        # Вставляем вызов перед закрывающей скобкой функции отрисовки арены
        brace_depth = 0
        end_idx = -1
        for i in range(m_func.end() - 1, len(code)):
            if code[i] == "{":
                brace_depth += 1
            elif code[i] == "}":
                brace_depth -= 1
                if brace_depth == 0:
                    end_idx = i
                    break
        if end_idx != -1:
            call_str = f"\n    rr_draw_shop_house_and_hud((double){px_var}, (double){py_var}, (double){zm_var});\n"
            code = code[:end_idx] + call_str + code[end_idx:]
            print(f"[OK] Встроено в {func_header.strip()} с координатами ({px_var}, {py_var}, {zm_var})")
    else:
        print("[WARN] Не найдена функция rr_render_arena, проверь имена функций в RenderArena.c")

with open(path, "w", encoding="utf-8") as f:
    f.write(code)
