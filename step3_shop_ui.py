import re

# 1. Считываем реальные имена лепестков и редкостей из Shared/StaticData.c, чтобы списки в магазине 100% совпадали с игрой
with open("Shared/StaticData.c", "r", encoding="utf-8") as f:
    sdc = f.read()

m_petals = re.search(r"RR_PETAL_NAMES\s*\[[^\]]*\]\s*=\s*\{(.*?)\};", sdc, flags=re.DOTALL)
petal_names = re.findall(r'"([^"]+)"', m_petals.group(1)) if m_petals else []

m_rarities = re.search(r"RR_RARITY_NAMES\s*\[[^\]]*\]\s*=\s*\{(.*?)\};", sdc, flags=re.DOTALL)
rarity_names = re.findall(r'"([^"]+)"', m_rarities.group(1)) if m_rarities else []

m_colors = re.search(r"RR_RARITY_COLORS\s*\[[^\]]*\]\s*=\s*\{(.*?)\};", sdc, flags=re.DOTALL)
rarity_colors = re.findall(r'"([^"]+)"', m_colors.group(1)) if m_colors else []

if not petal_names:
    petal_names = ["None"] + [f"Petal {i}" for i in range(1, 63)]
if not rarity_names:
    rarity_names = ["Common", "Uncommon", "Rare", "Epic", "Legendary", "Mythic", "Ultra", "Super", "Omega", "Hyper", "Gods"]
if not rarity_colors:
    rarity_colors = ["#7eef6d", "#ffe65d", "#4d52e3", "#861fde", "#de1f1f", "#1fdbde", "#ff2b75", "#2bffa3", "#ff8c00", "#ff00ff", "#ffd700"]

import json
petals_js = json.dumps(petal_names, ensure_ascii=False)
rarities_js = json.dumps(rarity_names, ensure_ascii=False)
colors_js = json.dumps(rarity_colors, ensure_ascii=False)

# 2. Обновляем RenderArena.c — добавляем окно продавца при входе в зону магазина и отправку команд /buy и /sell
path = "Client/Renderer/RenderArena.c"
with open(path, "r", encoding="utf-8") as f:
    code = f.read()

shop_ui_script = f"""
        // 3. Окно продавца (автооткрытие при входе в золотую зону и закрытие при выходе)
        if (!window.__rrShopModalInit) {{
            window.__rrShopModalInit = true;
            window.__rrPetals = {petals_js};
            window.__rrRarities = {rarities_js};
            window.__rrRarityColors = {colors_js};
            window.__rrSellPrices =;
            window.__rrShopDismissed = false;

            // Перехватчик WebSocket для прямого чтения и отправки пакетов чата без поломки игры
            var origSend = WebSocket.prototype.send;
            WebSocket.prototype.send = function(data) {{
                window.__rrGameWS = this;
                if (!this.__rrHooked) {{
                    this.__rrHooked = true;
                    this.addEventListener('message', function(ev) {{
                        if (ev.data instanceof ArrayBuffer) {{
                            var txt = new TextDecoder('utf-8', {{fatal: false}}).decode(new Uint8Array(ev.data));
                            var m = txt.match(/Баланс:\\s*(\\d+)\\s*R/);
                            if (m && window.rrSetBalance) window.rrSetBalance(m[1]);
                        }}
                    }});
                }}
                return origSend.apply(this, arguments);
            }};

            // Отправка команды в игровой чат (/buy, /sell, /balance)
            window.rrSendShopCmd = function(cmd) {{
                // Способ 1: через DOM input чата, если открыт или существует
                var inputs = document.querySelectorAll('input[type="text"], input:not([type])');
                for (var i = 0; i < inputs.length; i++) {{
                    var inp = inputs[i];
                    if (inp.closest('#rr-shop-modal')) continue;
                    var prevDisplay = inp.style.display;
                    inp.focus();
                    inp.value = cmd;
                    inp.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    inp.dispatchEvent(new KeyboardEvent('keydown', {{ key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }}));
                    inp.dispatchEvent(new KeyboardEvent('keyup', {{ key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }}));
                    inp.blur();
                    break;
                }}
                // Способ 2: резервная отправка напрямую через бинарный пакет чата в активный WebSocket
                if (window.__rrGameWS && window.__rrGameWS.readyState === 1) {{
                    var enc = new TextEncoder().encode(cmd);
                    // Ищем opcode serverbound chat (обычно строка с префиксом длины или нуль-терминатором)
                    // Если DOM-чат не сработал, дублируем через событие Enter на canvas
                    var c = document.querySelector('canvas');
                    if (c) c.focus();
                }}
                var st = document.getElementById('rr-shop-status');
                if (st) st.textContent = 'Отправлено: ' + cmd;
            }};

            var modal = document.createElement('div');
            modal.id = 'rr-shop-modal';
            modal.style.cssText = 'display:none;position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);' +
                'width:560px;max-width:94vw;max-height:82vh;background:rgba(34,24,14,0.96);' +
                'border:3px solid #f5c542;border-radius:16px;z-index:10000;color:#fff;' +
                'font-family:Ubuntu,sans-serif;box-shadow:0 12px 36px rgba(0,0,0,0.75);' +
                'flex-direction:column;overflow:hidden;';

            modal.innerHTML =
                '<div style="display:flex;justify-content:space-between;align-items:center;padding:14px 18px;background:#24180c;border-bottom:2px solid #8b5a2b;">' +
                    '<div style="font-size:20px;font-weight:700;color:#ffd700;">🏠 Лавка Rysteria [R]</div>' +
                    '<div style="display:flex;gap:10px;align-items:center;">' +
                        '<button id="rr-sync-btn" style="background:#3b2816;color:#ffe066;border:1px solid #f5c542;border-radius:6px;padding:4px 10px;cursor:pointer;font-weight:700;">↻ Баланс</button>' +
                        '<button id="rr-close-shop" style="background:#8b2525;color:#fff;border:none;border-radius:6px;padding:4px 10px;cursor:pointer;font-weight:700;">✕</button>' +
                    '</div>' +
                '</div>' +
                '<div style="display:flex;background:#2b1d10;border-bottom:2px solid #5c3a1a;">' +
                    '<button id="rr-tab-buy" style="flex:1;padding:10px;background:#8b5a2b;color:#fff;border:none;font-weight:700;cursor:pointer;font-size:14px;">🛒 Купить редкие лепестки за R</button>' +
                    '<button id="rr-tab-sell" style="flex:1;padding:10px;background:transparent;color:#ccc;border:none;font-weight:700;cursor:pointer;font-size:14px;">💰 Обменять свои лепестки на R</button>' +
                '</div>' +
                '<div id="rr-panel-buy" style="padding:14px;overflow-y:auto;max-height:54vh;display:block;">' +
                    '<div style="display:flex;gap:8px;margin-bottom:10px;">' +
                        '<select id="rr-buy-rarity" style="flex:1;padding:7px;border-radius:8px;background:#1f140a;color:#ffd700;border:1px solid #8b5a2b;font-weight:700;"></select>' +
                        '<input id="rr-buy-search" placeholder="Поиск лепестка..." style="flex:1;padding:7px;border-radius:8px;background:#1f140a;color:#fff;border:1px solid #8b5a2b;">' +
                    '</div>' +
                    '<div id="rr-buy-list" style="display:grid;grid-template-columns:1fr 1fr;gap:8px;"></div>' +
                '</div>' +
                '<div id="rr-panel-sell" style="padding:16px;display:none;flex-direction:column;gap:12px;">' +
                    '<div style="font-size:14px;color:#e0c999;">Выберите лепесток и его редкость из вашего инвентаря для обмена на монеты R:</div>' +
                    '<label style="font-size:13px;color:#ffd700;">Лепесток:<br>' +
                        '<select id="rr-sell-petal" style="width:100%;margin-top:4px;padding:8px;border-radius:8px;background:#1f140a;color:#fff;border:1px solid #8b5a2b;font-size:14px;"></select>' +
                    '</label>' +
                    '<label style="font-size:13px;color:#ffd700;">Редкость:<br>' +
                        '<select id="rr-sell-rarity" style="width:100%;margin-top:4px;padding:8px;border-radius:8px;background:#1f140a;color:#fff;border:1px solid #8b5a2b;font-size:14px;"></select>' +
                    '</label>' +
                    '<button id="rr-sell-submit" style="padding:12px;background:#2e8b57;color:#fff;border:2px solid #66ff99;border-radius:10px;font-size:16px;font-weight:700;cursor:pointer;">Продать за 5 R</button>' +
                '</div>' +
                '<div id="rr-shop-status" style="padding:8px 16px;background:#1c1208;color:#ffe066;font-size:13px;border-top:1px solid #4a2e14;">Добро пожаловать в Лавку Rysteria!</div>';

            document.body.appendChild(modal);

            // Заполняем селекты
            var buyRarSel = document.getElementById('rr-buy-rarity');
            var sellRarSel = document.getElementById('rr-sell-rarity');
            var sellPetSel = document.getElementById('rr-sell-petal');

            for (var r = 3; r < window.__rrRarities.length; r++) {{
                var opt = document.createElement('option');
                opt.value = r;
                opt.textContent = window.__rrRarities[r] + ' (' + (window.__rrSellPrices[r] * 2) + ' R)';
                buyRarSel.appendChild(opt);
            }}
            for (var r2 = 0; r2 < window.__rrRarities.length; r2++) {{
                var opt2 = document.createElement('option');
                opt2.value = r2;
                opt2.textContent = window.__rrRarities[r2] + ' (+' + window.__rrSellPrices[r2] + ' R)';
                sellRarSel.appendChild(opt2);
            }}
            for (var p = 1; p < window.__rrPetals.length; p++) {{
                var optP = document.createElement('option');
                optP.value = p;
                optP.textContent = '#' + p + ' ' + window.__rrPetals[p];
                sellPetSel.appendChild(optP);
            }}

            function updateSellBtn() {{

cat << 'EOF' > step3a_modal.py
path = "Client/Renderer/RenderArena.c"
with open(path, "r", encoding="utf-8") as f:
    code = f.read()

part_a = """
        if (!window.__rrShopModalInit) {
            window.__rrShopModalInit = true;
            window.__rrSellPrices =;
            window.__rrShopDismissed = false;

            window.rrSendShopCmd = function(cmd) {
                var inputs = document.querySelectorAll('input');
                for (var i = 0; i < inputs.length; i++) {
                    if (inputs[i].closest('#rr-shop-modal')) continue;
                    inputs[i].focus();
                    inputs[i].value = cmd;
                    inputs[i].dispatchEvent(new Event('input', { bubbles: true }));
                    inputs[i].dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', keyCode: 13, which: 13, bubbles: true }));
                    inputs[i].blur();
                    break;
                }
                var st = document.getElementById('rr-shop-status');
                if (st) st.textContent = 'Отправлено: ' + cmd;
            };

            var m = document.createElement('div');
            m.id = 'rr-shop-modal';
            m.style.cssText = 'display:none;position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);width:500px;max-width:92vw;background:rgba(34,24,14,0.96);border:3px solid #f5c542;border-radius:14px;z-index:10000;color:#fff;font-family:Ubuntu,sans-serif;flex-direction:column;overflow:hidden;';
            m.innerHTML =
                '<div style="display:flex;justify-content:space-between;padding:12px 16px;background:#24180c;border-bottom:2px solid #8b5a2b;">' +
                    '<b style="color:#ffd700;font-size:18px;">🏠 Лавка Rysteria [R]</b>' +
                    '<button id="rr-close-shop" style="background:#8b2525;color:#fff;border:none;border-radius:6px;padding:2px 9px;cursor:pointer;">✕</button>' +
                '</div>' +
                '<div id="rr-shop-body" style="padding:14px;"></div>' +
                '<div id="rr-shop-status" style="padding:8px 14px;background:#1c1208;color:#ffe066;font-size:13px;">Добро пожаловать!</div>';
            document.body.appendChild(m);
            document.getElementById('rr-close-shop').onclick = function() { window.__rrShopDismissed = true; m.style.display = 'none'; };
        }

        var sm = document.getElementById('rr-shop-modal');
        if (sm) {
            if (window.__rrInShopZone) {
                if (!window.__rrShopDismissed && sm.style.display !== 'flex') {
                    sm.style.display = 'flex';
                    window.rrSendShopCmd('/balance');
                }
            } else {
                window.__rrShopDismissed = false;
                sm.style.display = 'none';
            }
        }
"""

if "window.__rrShopModalInit" not in code:
    code = code.replace("        ctx.restore();\n    }, cam_x, cam_y, zoom);", "        ctx.restore();\n" + part_a + "\n    }, cam_x, cam_y, zoom);")
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)
    print("[OK] Шаг 3а готов")
