import re, json

with open("Shared/StaticData.c", "r", encoding="utf-8") as f:
    sdc = f.read()

m_p = re.search(r"RR_PETAL_NAMES\s*\[[^\]]*\]\s*=\s*\{(.*?)\};", sdc, re.DOTALL)
petals = re.findall(r'"([^"]+)"', m_p.group(1)) if m_p else ["None"] + [f"Petal {i}" for i in range(1, 63)]

m_r = re.search(r"RR_RARITY_NAMES\s*\[[^\]]*\]\s*=\s*\{(.*?)\};", sdc, re.DOTALL)
rarities = re.findall(r'"([^"]+)"', m_r.group(1)) if m_r else ["Common","Uncommon","Rare","Epic","Legendary","Mythic","Ultra","Super","Omega","Hyper","Gods"]

part_b = f"""
            var body = document.getElementById('rr-shop-body');
            var P = {json.dumps(petals, ensure_ascii=False)};
            var R = {json.dumps(rarities, ensure_ascii=False)};
            var S =;

            body.innerHTML =
                '<div style="display:flex;gap:6px;margin-bottom:10px;">' +
                    '<button id="t-buy" style="flex:1;padding:7px;background:#8b5a2b;color:#fff;border:none;border-radius:6px;font-weight:700;cursor:pointer;">🛒 Купить (Epic–Gods)</button>' +
                    '<button id="t-sell" style="flex:1;padding:7px;background:#2b1d10;color:#ccc;border:none;border-radius:6px;font-weight:700;cursor:pointer;">💰 Продать свои</button>' +
                '</div>' +
                '<div id="p-buy">' +
                    '<select id="b-rar" style="width:100%;padding:6px;margin-bottom:8px;background:#1f140a;color:#ffd700;border:1px solid #8b5a2b;border-radius:6px;"></select>' +
                    '<div id="b-list" style="max-height:240px;overflow-y:auto;display:grid;grid-template-columns:1fr 1fr;gap:6px;"></div>' +
                '</div>' +
                '<div id="p-sell" style="display:none;flex-direction:column;gap:8px;">' +
                    '<select id="s-pet" style="padding:7px;background:#1f140a;color:#fff;border:1px solid #8b5a2b;border-radius:6px;"></select>' +
                    '<select id="s-rar" style="padding:7px;background:#1f140a;color:#ffd700;border:1px solid #8b5a2b;border-radius:6px;"></select>' +
                    '<button id="s-go" style="padding:10px;background:#2e8b57;color:#fff;border:none;border-radius:8px;font-weight:700;cursor:pointer;">Продать лепесток</button>' +
                '</div>';

            var bRar = document.getElementById('b-rar'), sRar = document.getElementById('s-rar'), sPet = document.getElementById('s-pet');
            for (var i = 3; i < R.length; i++) bRar.innerHTML += '<option value="'+i+'">'+R[i]+' ('+(S[i]*2)+' R)</option>';
            for (var i = 0; i < R.length; i++) sRar.innerHTML += '<option value="'+i+'">'+R[i]+' (+'+S[i]+' R)</option>';
            for (var i = 1; i < P.length; i++) sPet.innerHTML += '<option value="'+i+'">#'+i+' '+P[i]+'</option>';

            function drawBuy() {{
                var r = +bRar.value, cost = S[r] * 2, list = document.getElementById('b-list');
                list.innerHTML = '';
                for (var p = P.length - 1; p >= 1; p--) {{
                    var d = document.createElement('div');
                    d.style.cssText = 'background:#26190d;border:1px solid #8b5a2b;border-radius:6px;padding:6px;display:flex;justify-content:space-between;align-items:center;font-size:13px;';
                    d.innerHTML = '<span>'+(p>=43?'🦖 ':'')+P[p]+'</span><button style="background:#d98a1c;border:none;border-radius:5px;padding:4px 8px;font-weight:700;cursor:pointer;">'+cost+' R</button>';
                    (function(pid) {{ d.querySelector('button').onclick = function() {{ window.rrSendShopCmd('/buy '+pid+' '+r); }}; }})(p);
                    list.appendChild(d);
                }}
            }}
            bRar.onchange = drawBuy; drawBuy();

            document.getElementById('t-buy').onclick = function() {{
                this.style.background='#8b5a2b'; document.getElementById('t-sell').style.background='#2b1d10';
                document.getElementById('p-buy').style.display='block'; document.getElementById('p-sell').style.display='none';
            }};
            document.getElementById('t-sell').onclick = function() {{
                this.style.background='#8b5a2b'; document.getElementById('t-buy').style.background='#2b1d10';
                document.getElementById('p-sell').style.display='flex'; document.getElementById('p-buy').style.display='none';
            }};
            document.getElementById('s-go').onclick = function() {{ window.rrSendShopCmd('/sell '+sPet.value+' '+sRar.value); }};
"""

path = "Client/Renderer/RenderArena.c"
with open(path, "r", encoding="utf-8") as f:
    code = f.read()

target = "document.getElementById('rr-close-shop').onclick = function() { window.__rrShopDismissed = true; m.style.display = 'none'; };"
if "id=\"t-buy\"" not in code and target in code:
    code = code.replace(target, target + "\n" + part_b)
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)
    print("[OK] Шаг 3б встроен")
