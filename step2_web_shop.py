import re, json

# 1. Фиксим массивы цен в MasterServer/main.js (через chr(91)/chr(93))
LB, RB = chr(91), chr(93)
with open("MasterServer/main.js", "r", encoding="utf-8") as f:
    ms = f.read()
ms = ms.replace("const SELL_PRICES =;", f"const SELL_PRICES = {LB}5,15,40,120,350,1000,3000,9000,25000,75000,200000{RB};")
ms = ms.replace("const Q_REWARDS =;", f"const Q_REWARDS = {LB}40,100,250,700,2000,6000,18000,50000,150000,400000,1000000{RB};")
with open("MasterServer/main.js", "w", encoding="utf-8") as f:
    f.write(ms)

# 2. Берём имена лепестков и редкостей из Shared/StaticData.c для сайта
with open("Shared/StaticData.c", "r", encoding="utf-8") as f:
    sdc = f.read()
m_p = re.search(r"RR_PETAL_NAMES\s*\[[^\]]*\]\s*=\s*\{(.*?)\};", sdc, re.DOTALL)
petals = re.findall(r'"([^"]+)"', m_p.group(1)) if m_p else ["None"] + [f"Petal {i}" for i in range(1, 63)]
m_r = re.search(r"RR_RARITY_NAMES\s*\[[^\]]*\]\s*=\s*\{(.*?)\};", sdc, re.DOTALL)
rarities = re.findall(r'"([^"]+)"', m_r.group(1)) if m_r else ["Common","Uncommon","Rare","Epic","Legendary","Mythic","Ultra","Super","Omega","Hyper","Gods"]

# 3. Генерируем отдельный сайт Client/public/shop.html
html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>Rysteria — Лавка [R] и Квесты</title>
<style>
  body {{ margin:0; background:#1c140c; color:#fff; font-family:Ubuntu,sans-serif; }}
  .top {{ background:#2b1d10; border-bottom:3px solid #f5c542; padding:14px 24px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; }}
  .bal {{ background:#1a1007; border:2px solid #f5c542; border-radius:10px; padding:8px 16px; color:#ffe066; font-size:20px; font-weight:700; }}
  .wrap {{ max-width:980px; margin:20px auto; padding:0 16px; display:grid; grid-template-columns:1fr 1fr; gap:18px; }}
  .card {{ background:#26190d; border:2px solid #8b5a2b; border-radius:14px; padding:18px; }}
  .qcard {{ background:#162412; border:2px solid #7eef6d; border-radius:14px; padding:18px; grid-column:1 / -1; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:14px; }}
  .npc {{ width:64px; height:64px; border-radius:50%; background:#ffe763; border:4px solid #cfb73c; color:#1f1f1f; font-weight:700; font-size:22px; display:flex; align-items:center; justify-content:center; }}
  button {{ background:#d98a1c; color:#1a0f05; border:none; border-radius:8px; padding:9px 14px; font-weight:700; cursor:pointer; }}
  button:hover {{ filter:brightness(1.12); }}
  input, select {{ background:#1a1007; color:#fff; border:1px solid #8b5a2b; border-radius:8px; padding:8px 12px; }}
  .grid {{ display:grid; grid-template-columns:1fr 1fr; gap:8px; max-height:360px; overflow-y:auto; margin-top:10px; }}
  .item {{ background:#1c1208; border:1px solid #5c3a1a; border-radius:8px; padding:8px; display:flex; justify-content:space-between; align-items:center; font-size:13px; }}
  .promo {{ background:linear-gradient(90deg,#4a148c,#7b1fa2); border:2px solid #ea80fc; border-radius:10px; padding:12px; margin-bottom:12px; display:flex; justify-content:space-between; align-items:center; }}
  #msg {{ max-width:980px; margin:10px auto 0; padding:10px 16px; background:#2b1d10; border-left:4px solid #ffd700; border-radius:6px; color:#ffe066; }}
</style>
</head>
<body>
<div class="top">
  <div style="font-size:22px;font-weight:700;color:#ffd700;">🏠 Лавка Rysteria [R] & Охота</div>
  <div style="display:flex;gap:8px;align-items:center;">
    <input id="usr" placeholder="Логин из /login">
    <button onclick="api('status')">Войти / Обновить</button>
    <div class="bal" id="bal">R: —</div>
  </div>
</div>
<div id="msg">Введите свой логин (из команды /login в игре) и нажмите «Войти / Обновить».</div>
<div class="wrap">
  <div class="qcard">
    <div style="display:flex;align-items:center;gap:14px;">
      <div class="npc">◡‿◡</div>
      <div>
        <div style="font-size:18px;font-weight:700;color:#7eef6d;">Охотник Rysteria — Задание</div>
        <div id="qtxt" style="color:#eaffdf;margin-top:4px;">Загрузите профиль, чтобы увидеть цель...</div>
      </div>
    </div>
    <button style="background:#7eef6d;color:#10240b;font-size:15px;" onclick="api('claim')">💰 Забрать награду R</button>
  </div>

  <div class="card">
    <h3 style="margin-top:0;color:#ffd700;">🛒 Купить лепестки за R</h3>
    <div class="promo">
      <div><b>🦖 Уникальный Epic Relic</b><br><small>Спецпредложение за стартовый баланс</small></div>
      <button style="background:#ea80fc;color:#1a0026;" onclick="api('buy',62,3)">Купить за 100 R</button>
    </div>
    <select id="brar" onchange="renderBuy()" style="width:100%;"></select>
    <div class="grid" id="blist"></div>
  </div>

  <div class="card">
    <h3 style="margin-top:0;color:#7eef6d;">💰 Обменять свои лепестки на R</h3>
    <div style="font-size:13px;color:#ccc;">Ваши лепестки из сохранения (нажмите /save в игре перед обменом):</div>
    <div class="grid" id="slist" style="max-height:430px;"></div>
  </div>
</div>
<script>
const P = {json.dumps(petals, ensure_ascii=False)};
const R = {json.dumps(rarities, ensure_ascii=False)};
const S =;
const API_BASE = location.protocol + '//' + location.hostname.replace('-8080.', '-8085.') + (location.port === '8080' ? ':8085' : '');

const brar = document.getElementById('brar');
for (let i = 3; i < R.length; i++) brar.innerHTML += `<option value="${{i}}">${{R[i]}} (${{S[i]*2}} R)</option>`;

function renderBuy() {{
  const r = +brar.value, cost = S[r]*2, box = document.getElementById('blist');
  box.innerHTML = '';
  for (let p = P.length - 1; p >= 1; p--) {{
    const c = (p === 62 && r === 3) ? 100 : cost;
    box.innerHTML += `<div class="item"><span>${{p>=43?'🦖 ':''}}${{P[p]}}</span><button onclick="api('buy',${{p}},${{r}})">${{c}} R</button></div>`;
  }}
}}
renderBuy();

const saved = localStorage.getItem('rr_shop_user');
if (saved) document.getElementById('usr').value = saved;

async function api(action, pid=0, rid=0) {{
  const user = document.getElementById('usr').value.trim();
  if (!user) return alert('Введите логин!');
  localStorage.setItem('rr_shop_user', user);
  const res = await fetch(`${{API_BASE}}/?user=${{encodeURIComponent(user)}}&action=${{action}}&pid=${{pid}}&rid=${{rid}}`);
  const d = await res.json();
  document.getElementById('msg').textContent = d.msg || '';
  if (!d.ok) return;
  document.getElementById('bal').textContent = 'R: ' + d.r_coins;
  document.getElementById('qtxt').textContent = `Убить мобов [${{d.quest.rarity}}]: ${{d.quest.progress}} / ${{d.quest.target}} — Награда: ${{d.quest.reward}} R`;
  const sl = document.getElementById('slist');
  sl.innerHTML = '';
  for (const it of d.inventory) {{
    sl.innerHTML += `<div class="item"><span>${{P[it.pid]}} [${{R[it.rid]}}] x${{it.count}}</span><button style="background:#2e8b57;color:#fff;" onclick="api('sell',${{it.pid}},${{it.rid}})">+${{S[it.rid]}} R</button></div>`;
  }}
}}
if (saved) api('status');
</script>
</body>
</html>
"""
with open("Client/public/shop.html", "w", encoding="utf-8") as f:
    f.write(html)

# 4. Убираем тяжёлые окна из Client/Ui/TitleScreen/Shop.c — оставляем только 1 лёгкую кнопку открытия сайта /shop.html!
LB, RB = chr(91), chr(93)
light_shop_c = f"""#include <Client/Ui/Ui.h>
#include <emscripten.h>
#include <Client/Game.h>
#include <Client/InputData.h>
#include <Client/Renderer/Renderer.h>

static void shop_btn_ev(struct rr_ui_element *this, struct rr_game *g) {{
    (void)this;
    if (g->input_data->mouse_buttons_up_this_tick & 1) {{
        EM_ASM({{ window.open('/shop.html', '_blank'); }});
    }}
}}
static void shop_btn_rd(struct rr_ui_element *this, struct rr_game *g) {{
    struct rr_renderer *r = g->renderer; rr_renderer_scale(r, r->scale);
    rr_renderer_set_fill(r, (g->focused == this) ? 0xffd98a1c : 0xffa66814);
    rr_renderer_set_stroke(r, 0xff6e4209); rr_renderer_set_line_width(r, 5);
    rr_renderer_begin_path(r); rr_renderer_round_rect(r, -this->width/2, -this->height/2, this->width, this->height, 8);
    rr_renderer_fill(r); rr_renderer_stroke(r);
    rr_renderer_set_text_baseline(r, 1); rr_renderer_set_text_align(r, 1); rr_renderer_set_text_size(r, 12);
    rr_renderer_set_fill(r, 0xffffffff); rr_renderer_fill_text(r, "SHOP", 0, -4);
    rr_renderer_set_fill(r, 0xffffe066); rr_renderer_fill_text(r, "WEB", 0, 14);
}}
struct rr_ui_element *rr_ui_shop_toggle_button_init() {{
    struct rr_ui_element *this = rr_ui_element_init();
    this->abs_width = this->abs_height = this->width = this->height = 60;
    this->on_event = shop_btn_ev; this->on_render = shop_btn_rd;
    return this;
}}
struct rr_ui_element *rr_ui_quests_toggle_button_init() {{
    struct rr_ui_element *this = rr_ui_element_init();
    this->completely_hidden = 1;
    return this;
}}
struct rr_ui_element *rr_ui_shop_container_init(struct rr_game *g) {{
    (void)g; struct rr_ui_element *this = rr_ui_element_init();
    this->completely_hidden = 1; return this;
}}
struct rr_ui_element *rr_ui_quests_container_init(struct rr_game *g) {{
    (void)g; struct rr_ui_element *this = rr_ui_element_init();
    this->completely_hidden = 1; return this;
}}
"""
with open("Client/Ui/TitleScreen/Shop.c", "w", encoding="utf-8") as f:
    f.write(light_shop_c)

print("[OK] Отдельный сайт Client/public/shop.html создан, клиент облегчён")
