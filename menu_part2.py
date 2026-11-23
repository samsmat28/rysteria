import re, json

with open("Shared/StaticData.c", "r", encoding="utf-8") as f:
    sdc = f.read()

m_p = re.search(r"RR_PETAL_NAMES\s*\[[^\]]*\]\s*=\s*\{(.*?)\};", sdc, re.DOTALL)
petals = re.findall(r'"([^"]+)"', m_p.group(1)) if m_p else ["None"] + [f"Petal {i}" for i in range(1, 63)]

m_r = re.search(r"RR_RARITY_NAMES\s*\[[^\]]*\]\s*=\s*\{(.*?)\};", sdc, re.DOTALL)
rarities = re.findall(r'"([^"]+)"', m_r.group(1)) if m_r else ["Common","Uncommon","Rare","Epic","Legendary","Mythic","Ultra","Super","Omega","Hyper","Gods"]

code_p2 = f"""
        var P = {json.dumps(petals, ensure_ascii=False)};
        var R = {json.dumps(rarities, ensure_ascii=False)};
        var S =;

        var ws = document.createElement('div');
        ws.id = 'rr-win-shop';
        ws.style.cssText = 'display:none;position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);width:480px;max-width:92vw;background:rgba(34,24,14,0.97);border:3px solid #f5c542;border-radius:14px;z-index:100000;color:#fff;font-family:Ubuntu,sans-serif;flex-direction:column;overflow:hidden;';
        ws.innerHTML =
            '<div style="display:flex;justify-content:space-between;padding:10px 14px;background:#24180c;border-bottom:2px solid #8b5a2b;">' +
                '<b style="color:#ffd700;">🏪 Лавка Rysteria [R]</b>' +
                '<button id="rr-x-shop" style="background:#8b2525;color:#fff;border:none;border-radius:5px;padding:2px 8px;cursor:pointer;">✕</button>' +
            '</div>' +
            '<div style="padding:12px;">' +
                '<div style="display:flex;gap:6px;margin-bottom:8px;">' +
                    '<button id="rr-tb-buy" style="flex:1;padding:7px;background:#8b5a2b;color:#fff;border:none;border-radius:6px;font-weight:700;cursor:pointer;">🛒 Купить</button>' +
                    '<button id="rr-tb-sell" style="flex:1;padding:7px;background:#2b1d10;color:#ccc;border:none;border-radius:6px;font-weight:700;cursor:pointer;">💰 Продать свои</button>' +
                '</div>' +
                '<div id="rr-pn-buy">' +
                    '<select id="rr-sl-brar" style="width:100%;padding:6px;margin-bottom:8px;background:#1f140a;color:#ffd700;border:1px solid #8b5a2b;border-radius:6px;"></select>' +
                    '<div id="rr-gr-buy" style="max-height:220px;overflow-y:auto;display:grid;grid-template-columns:1fr 1fr;gap:6px;"></div>' +
                '</div>' +
                '<div id="rr-pn-sell" style="display:none;flex-direction:column;gap:8px;">' +
                    '<select id="rr-sl-spet" style="padding:7px;background:#1f140a;color:#fff;border:1px solid #8b5a2b;border-radius:6px;"></select>' +
                    '<select id="rr-sl-srar" style="padding:7px;background:#1f140a;color:#ffd700;border:1px solid #8b5a2b;border-radius:6px;"></select>' +
                    '<button id="rr-bt-sell" style="padding:9px;background:#2e8b57;color:#fff;border:none;border-radius:8px;font-weight:700;cursor:pointer;">Продать лепесток</button>' +
                '</div>' +
            '</div>' +
            '<div id="rr-m-status" style="padding:7px 12px;background:#1c1208;color:#ffe066;font-size:12px;">Готово к торговле</div>';
        document.body.appendChild(ws);

        var wq = document.createElement('div');
        wq.id = 'rr-win-quest';
        wq.style.cssText = 'display:none;position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);width:390px;max-width:90vw;background:rgba(24,36,20,0.97);border:3px solid #7eef6d;border-radius:14px;z-index:100001;color:#fff;font-family:Ubuntu,sans-serif;flex-direction:column;overflow:hidden;';
        wq.innerHTML =
            '<div style="display:flex;justify-content:space-between;padding:10px 14px;background:#162412;border-bottom:2px solid #4a7c3a;">' +
                '<b style="color:#7eef6d;">🌼 Охотник Rysteria</b>' +
                '<button id="rr-x-quest" style="background:#8b2525;color:#fff;border:none;border-radius:5px;padding:2px 8px;cursor:pointer;">✕</button>' +
            '</div>' +
            '<div style="padding:14px;display:flex;flex-direction:column;gap:10px;align-items:center;">' +
                '<div style="width:48px;height:48px;border-radius:50%;background:#ffe763;border:3px solid #cfb73c;display:flex;align-items:center;justify-content:center;font-size:20px;color:#1f1f1f;font-weight:700;">◡‿◡</div>' +
                '<div id="rr-q-info" style="width:100%;background:#121c0f;border:1px solid #4a7c3a;border-radius:8px;padding:10px;font-size:13px;color:#eaffdf;text-align:center;">Зайди в игру и нажми «Задание»!</div>' +
                '<div style="display:flex;gap:8px;width:100%;">' +
                    '<button id="rr-bt-qget" style="flex:1;padding:9px;background:#3a6b2c;color:#fff;border:none;border-radius:8px;font-weight:700;cursor:pointer;">🔄 Задание</button>' +
                    '<button id="rr-bt-qclm" style="flex:1;padding:9px;background:#d98a1c;color:#1a0f05;border:none;border-radius:8px;font-weight:700;cursor:pointer;">💰 Награда R</button>' +
                '</div>' +
            '</div>';
        document.body.appendChild(wq);

        var bRar = document.getElementById('rr-sl-brar'), sRar = document.getElementById('rr-sl-srar'), sPet = document.getElementById('rr-sl-spet');
        for (var i = 3; i < R.length; i++) bRar.innerHTML += '<option value="'+i+'">'+R[i]+' ('+(S[i]*2)+' R)</option>';
        for (var i = 0; i < R.length; i++) sRar.innerHTML += '<option value="'+i+'">'+R[i]+' (+'+S[i]+' R)</option>';
        for (var i = 1; i < P.length; i++) sPet.innerHTML += '<option value="'+i+'">#'+i+' '+P[i]+'</option>';

        function fillBuy() {{
            var r = +bRar.value, cost = S[r] * 2, g = document.getElementById('rr-gr-buy');
            g.innerHTML = '';
            for (var p = P.length - 1; p >= 1; p--) {{
                var d = document.createElement('div');
                d.style.cssText = 'background:#26190d;border:1px solid #8b5a2b;border-radius:6px;padding:5px;display:flex;justify-content:space-between;align-items:center;font-size:12px;';
                d.innerHTML = '<span>'+(p>=43?'🦖 ':'')+P[p]+'</span><button style="background:#d98a1c;border:none;border-radius:4px;padding:3px 7px;font-weight:700;cursor:pointer;">'+cost+' R</button>';
                (function(pid) {{ d.querySelector('button').onclick = function() {{ window.rrMenuCmd('/buy '+pid+' '+r); }}; }})(p);
                g.appendChild(d);
            }}
        }}
        bRar.onchange = fillBuy; fillBuy();

        document.getElementById('rr-m-shop').onclick = function() {{ ws.style.display = ws.style.display === 'flex' ? 'none' : 'flex'; wq.style.display = 'none'; window.rrMenuCmd('/balance'); }};
        document.getElementById('rr-m-quest').onclick = function() {{ wq.style.display = wq.style.display === 'flex' ? 'none' : 'flex'; ws.style.display = 'none'; window.rrMenuCmd('/quest'); }};
        document.getElementById('rr-x-shop').onclick = function() {{ ws.style.display = 'none'; }};
        document.getElementById('rr-x-quest').onclick = function() {{ wq.style.display = 'none'; }};
        document.getElementById('rr-tb-buy').onclick = function() {{ this.style.background='#8b5a2b'; document.getElementById('rr-tb-sell').style.background='#2b1d10'; document.getElementById('rr-pn-buy').style.display='block'; document.getElementById('rr-pn-sell').style.display='none'; }};
        document.getElementById('rr-tb-sell').onclick = function() {{ this.style.background='#8b5a2b'; document.getElementById('rr-tb-buy').style.background='#2b1d10'; document.getElementById('rr-pn-sell').style.display='flex'; document.getElementById('rr-pn-buy').style.display='none'; }};
        document.getElementById('rr-bt-sell').onclick = function() {{ window.rrMenuCmd('/sell '+sPet.value+' '+sRar.value); }};
        document.getElementById('rr-bt-qget').onclick = function() {{ window.rrMenuCmd('/quest'); }};
        document.getElementById('rr-bt-qclm').onclick = function() {{ window.rrMenuCmd('/claim'); }};

        setInterval(function() {{
            var t = document.body ? document.body.innerText : '';
            var mb = t.match(/(?:Баланс|баланс):\\s*(\\d+)\\s*R/g);
            if (mb && mb.length) {{ var n = mb[mb.length - 1].match(/(\\d+)/); if (n) document.getElementById('rr-r-bal').textContent = 'R: ' + n; }}
            var mq = t.match(/Квест:[^\\n]+/g);
            if (mq && mq.length) {{ var qe = document.getElementById('rr-q-info'); if (qe) qe.textContent = mq[mq.length - 1]; }}
        }}, 500);
"""

with open("Client/Main.c", "r", encoding="utf-8") as f:
    mc = f.read()

target = "            var st = document.getElementById('rr-m-status');\n            if (st) st.textContent = 'Отправлено: ' + cmd;\n        };"
if "rr-win-shop" not in mc and target in mc:
    mc = mc.replace(target, target + "\n" + code_p2)
    with open("Client/Main.c", "w", encoding="utf-8") as f:
        f.write(mc)
    print("[OK] Часть 2 встроена в Client/Main.c")
