with open("Client/public/shop.html", "r", encoding="utf-8") as f:
    html = f.read()

packs_block = """
  <div class="card" style="grid-column:1 / -1;border-color:#ea80fc;">
    <h3 style="margin-top:0;color:#ea80fc;">🎁 Уникальные наборы и Сундук Удачи [R]</h3>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;">
      <div class="promo" style="margin:0;background:linear-gradient(135deg,#1b5e20,#2e7d32);border-color:#81c784;">
        <div><b>🦖 Набор Охотника</b><br><small>3 Epic лепестка (Claw, Bone, Amber)</small></div>
        <button style="background:#a5d6a7;color:#0a260d;" onclick="copyCmd('/pack 1')">300 R</button>
      </div>
      <div class="promo" style="margin:0;background:linear-gradient(135deg,#e65100,#f57c00);border-color:#ffcc80;">
        <div><b>🎲 Сундук Удачи</b><br><small>Случайный Dino (Legendary–Ultra)</small></div>
        <button style="background:#ffe0b2;color:#331400;" onclick="copyCmd('/pack 2')">500 R</button>
      </div>
      <div class="promo" style="margin:0;background:linear-gradient(135deg,#4a148c,#880e4f);border-color:#f48fb1;">
        <div><b>👑 Набор Бога</b><br><small>Mythic Crown + Mythic Relic</small></div>
        <button style="background:#f8bbd0;color:#2b0014;" onclick="copyCmd('/pack 3')">5000 R</button>
      </div>
    </div>
  </div>
"""

if "Набор Охотника" not in html:
    html = html.replace('<div class="card">\n    <h3 style="margin-top:0;color:#ffd700;">', packs_block + '\n  <div class="card">\n    <h3 style="margin-top:0;color:#ffd700;">', 1)
    with open("Client/public/shop.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("[OK] Витрина наборов добавлена на сайт shop.html")
