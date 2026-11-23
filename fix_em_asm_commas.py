with open("Client/DOM.c", "r", encoding="utf-8") as f:
    dom = f.read()
dom = dom.replace('.replace(/8080|8081/, ($1).toString())', '.replace("8080", ($1).toString()).replace("8081", ($1).toString())')
with open("Client/DOM.c", "w", encoding="utf-8") as f:
    f.write(dom)

with open("Client/Oauth2.c", "r", encoding="utf-8") as f:
    oa = f.read()
oa = oa.replace('window.location.hostname.match(/-808\\./)', '(window.location.hostname.includes("-8080.") || window.location.hostname.includes("-8081."))')
oa = oa.replace('window.location.hostname.replace(/-808\\./, "-55554.")', 'window.location.hostname.replace("-8080.", "-55554.").replace("-8081.", "-55554.")')
with open("Client/Oauth2.c", "w", encoding="utf-8") as f:
    f.write(oa)

print("[OK] Убраны запятые внутри EM_ASM")
