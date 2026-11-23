import re

with open("Client/Main.c", "r", encoding="utf-8") as f:
    mc = f.read()

if "<emscripten.h>" not in mc and '"emscripten.h"' not in mc:
    mc = "#include <emscripten.h>\n" + mc

code_p1 = """
    EM_ASM({
        if (window.__rrMenuShopReady) return;
        window.__rrMenuShopReady = true;

        var bar = document.createElement('div');
        bar.style.cssText = 'position:fixed;top:54px;left:14px;z-index:99999;display:flex;gap:8px;align-items:center;font-family:Ubuntu,sans-serif;';
        bar.innerHTML =
            '<div id="rr-r-bal" style="background:rgba(28,20,10,0.92);border:2px solid #f5c542;border-radius:8px;padding:6px 12px;color:#ffe066;font-weight:700;font-size:15px;">R: 100</div>' +
            '<button id="rr-m-shop" style="background:#8b5a2b;color:#ffd700;border:2px solid #f5c542;border-radius:8px;padding:6px 12px;font-weight:700;cursor:pointer;font-size:14px;">🏪 Лавка [R]</button>' +
            '<button id="rr-m-quest" style="background:#2e5c22;color:#7eef6d;border:2px solid #7eef6d;border-radius:8px;padding:6px 12px;font-weight:700;cursor:pointer;font-size:14px;">🌼 Квесты</button>';
        document.body.appendChild(bar);

        window.rrMenuCmd = function(cmd) {
            var inputs = document.querySelectorAll('input');
            for (var i = 0; i < inputs.length; i++) {
                if (inputs[i].closest('#rr-win-shop') || inputs[i].closest('#rr-win-quest')) continue;
                inputs[i].focus();
                inputs[i].value = cmd;
                inputs[i].dispatchEvent(new Event('input', { bubbles: true }));
                inputs[i].dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', keyCode: 13, which: 13, bubbles: true }));
                inputs[i].blur();
                break;
            }
            var st = document.getElementById('rr-m-status');
            if (st) st.textContent = 'Отправлено: ' + cmd;
        };
    });
"""

if "window.__rrMenuShopReady" not in mc:
    mc = re.sub(r"(int\s+main\s*\([^)]*\)\s*\{)", r"\1\n" + code_p1, mc, count=1)
    with open("Client/Main.c", "w", encoding="utf-8") as f:
        f.write(mc)
    print("[OK] Часть 1 встроена в Client/Main.c")
