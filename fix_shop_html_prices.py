LB, RB = chr(91), chr(93)
with open("Client/public/shop.html", "r", encoding="utf-8") as f:
    html = f.read()
html = html.replace("const S =;", f"const S = {LB}5,15,40,120,350,1000,3000,9000,25000,75000,200000{RB};")
with open("Client/public/shop.html", "w", encoding="utf-8") as f:
    f.write(html)
print("[OK] Цены в Client/public/shop.html обновлены")
