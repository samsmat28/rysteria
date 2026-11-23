import re, json

# 1. Очищаем MasterServer/main.js от лишнего блока, чтобы серверы и Account работали стабильно
with open("MasterServer/main.js", "r", encoding="utf-8") as f:
    ms = f.read()
if "// === Rysteria Web Shop & Quests API ===" in ms:
    ms = next(iter(ms.split("// === Rysteria Web Shop ms.split("// === Rysteria Web Shop & Quests API ===").rstrip() Quests API ==="))).rstrip() + "\n"
    with open("MasterServer/main.js", "w", encoding="utf-8") as f:
        f.write(ms)
    print("[OK] MasterServer/main.js очищен")

# 2. Берём имена лепестков и редкостей из Shared/StaticData.c
with open("Shared/StaticData.c", "r", encoding="utf-8") as f:
    sdc = f.read()
m_p = re.search(r"RR_PETAL_NAMES\s*\[[^\]]*\]\s*=\s*\{(.*?)\};", sdc, re.DOTALL)
petals = re.findall(r'"([^"]+)"', m_p.group(1)) if m_p else ["None"] + [f"Petal {i}" for i in range(1, 63)]
m_r = re.search(r"RR_RARITY_NAMES\s*\[[^\]]*\]\s*=\s*\{(.*?)\};", sdc, re.DOTALL)
rarities = re.findall(r'"([^"]+)"', m_r.group(1)) if m_r else ["Common","Uncommon","Rare","Epic","Legendary","Mythic","Ultra","Super","Omega","Hyper","Gods"]

LB, RB = chr(91), chr(93)
prices_js = f"{LB}5,15,40,120,350,1000,3000,9000,25000,75000,200000{RB}"

# 3. Простой и надёжный сайт Client/public/shop.html (работает без внешних портов!)
html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>Rysteria — Лавка [R] и Квесты</title>
<style>
  body {{ margin:0; background:#1c140c; color:#fff; font-family:Ubuntu,sans-serif; }}
  .top {{ background:#2b1d10; border-bottom:3px solid #f5c542; padding:14px 24px; display:flex; justify-content:space-between; align-items:center; }}
  .wrap {{ max-width:920px; margin:20px auto; padding:0 16px; display:grid; grid-template-columns:1fr 1fr; gap:18px; }}
  .card {{ background:#26190d; border:2px solid #8b5a2b; border-radius:14px; padding:18px; }}
  .qcard {{ background:#162412; border:2px solid #7eef6d; border-radius:14px; padding:18px; grid-column:1 / -1; display:flex; align-items:center; justify-content:space-between; gap:14px; flex-wrap:wrap; }}
  .npc {{ width:60px; height:60px; border-radius:50%; background:#ffe763; border:4px solid #cfb73c; color:#1f1f1f; font-weight:700; font-size:20px; display:flex; align-items:center; justify-content:center; }}
  button {{ background:#d98a1c; color:#1a0f05; border:none; border-radius:8px; padding:9px 14px; font-weight:700; cursor:pointer; }}
  button:hover {{ filter:brightness(1.12); }}
  select {{ background:#1a1007; color:#fff; border:1px solid #8b5a2b; border-radius:8px; padding:8px 12px; width:100%; }}
  .grid {{ display:grid; grid-template-columns:1fr 1fr; gap:8px; max-height:340px; overflow-y:auto; margin-top:10px; }}
  .item {{ background:#1c1208; border:1px solid #5c3a1a; border-radius:8px; padding:8px; display:flex; justify-content:space-between; align-items:center; font-size:13px; }}
  .promo {{ background:linear-gradient(90deg,#4a148c,#7b1fa2); border:2px solid #ea80fc; border-radius:10px; padding:12px; margin-bottom:12px; display:flex; justify-content:space-between; align-items:center; }}
  #toast {{ max-width:920px; margin:12px auto 0; padding:12px 16px; background:#2b1d10; border-left:4px solid #ffd700; border-radius:6px; color:#ffe066; font-weight:700; }}
</style>
</head>
<body>
<div class="top">
  <div style="font-size:22px;font-weight:700;color:#ffd700;">🏠 Лавка Rysteria [R] & Квесты</div>
  <button onclick="copyCmd('/balance')">💰 Команда баланса (/balance)</button>
</div>
<div id="toast">Нажми на любую кнопку — команда скопируется, просто вставь её в чат игры (Enter -> Ctrl+V -> Enter)!</div>
<div class="wrap">
  <div class="qcard">
    <div style="display:flex;align-items:center;gap:14px;">
      <div class="npc">◡‿◡</div>
      <div>
        <div style="font-size:18px;font-weight:700;color:#7eef6d;">Охотник Rysteria — Задания на R</div>
        <div style="color:#eaffdf;margin-top:4px;">1) Узнай цель (/quest) → 2) Убей мобов нужной редкости → 3) Забери награду (/claim)</div>
      </div>
    </div>
    <div style="display:flex;gap:8px;">
      <button style="background:#3a6b2c;color:#fff;" onclick="copyCmd('/quest')">🔄 Узнать задание (/quest)</button>
      <button style="background:#7eef6d;color:#10240b;" onclick="copyCmd('/claim')">💰 Забрать награду (/claim)</button>
    </div>
  </div>

  <div class="card">
    <h3 style="margin-top:0;color:#ffd700;">🛒 Купить лепестки за R</h3>
    <div class="promo">
      <div><b>🦖 Уникальный Epic Relic</b><br><small>Спеццена: 100 R (стартовый баланс)</small></div>
      <button style="background:#ea80fc;color:#1a0026;" onclick="copyCmd('/buy 62 3')">Купить (100 R)</button>
    </div>
    <select id="brar" onchange="renderBuy()"></select>
    <div class="grid" id="blist"></div>
  </div>

  <div class="card">
    <h3 style="margin-top:0;color:#7eef6d;">💰 Продать свои лепестки за R</h3>
    <div style="display:flex;flex-direction:column;gap:10px;margin-top:10px;">
      <select id="spet" onchange="updSell()"></select>
      <select id="srar" onchange="updSell()"></select>
      <button id="sbtn" style="background:#2e8b57;color:#fff;padding:12px;font-size:15px;" onclick="copyCmd('/sell '+spet.value+' '+srar.value)">Продать за +5 R</button>
    </div>
  </div>
</div>
<script>
const P = {json.dumps(petals, ensure_ascii=False)};
const R = {json.dumps(rarities, ensure_ascii=False)};
const S = {prices_js};

for (let i = 3; i < R.length; i++) brar.innerHTML += `<option value="${{i}}">${{R[i]}} (${{S[i]*2}} R)</option>`;
for (let i = 0; i < R.length; i++) srar.innerHTML += `<option value="${{i}}">${{R[i]}} (+${{S[i]}} R)</option>`;
for (let i = 1; i < P.length; i++) spet.innerHTML += `<option value="${{i}}">#${{i}} ${{P[i]}}</option>`;

function renderBuy() {{
  const r = +brar.value, cost = S[r]*2;
  blist.innerHTML = '';
  for (let p = P.length - 1; p >= 1; p--) {{
    const c = (p === 62 && r === 3) ? 100 : cost;
    blist.innerHTML += `<div class="item"><span>${{p>=43?'🦖 ':''}}${{P[p]}}</span><button onclick="copyCmd('/buy ${{p}} ${{r}}')">${{c}} R</button></div>`;
  }}
}}
function updSell() {{
  sbtn.textContent = `Продать ${{P[+spet.value]}} [${{R[+srar.value]}}] за +${{S[+srar.value]}} R`;
}}
renderBuy(); updSell();

function copyCmd(cmd) {{
  navigator.clipboard.writeText(cmd).catch(()=>{{}});
  toast.textContent = `✅ Скопировано: ${{cmd}} — вставь в чат игры (Enter → Ctrl+V → Enter)`;
}}
</script>
</body>
</html>
"""
with open("Client/public/shop.html", "w", encoding="utf-8") as f:
    f.write(html)
print("[OK] Простой и стабильный сайт Client/public/shop.html готов")
