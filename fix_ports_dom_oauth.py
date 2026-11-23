with open("Client/DOM.c", "r", encoding="utf-8") as f:
    dom = f.read()
dom = dom.replace("-(8080|55554)", "-(8080|8081|55554)")
dom = dom.replace('.replace("8080", ($1).toString())', '.replace(/8080|8081/, ($1).toString())')
with open("Client/DOM.c", "w", encoding="utf-8") as f:
    f.write(dom)

with open("Client/Oauth2.c", "r", encoding="utf-8") as f:
    oa = f.read()
oa = oa.replace('includes("-8080.")', 'match(/-808[01]\\./)')
oa = oa.replace('replace("-8080.", "-55554.")', 'replace(/-808[01]\\./, "-55554.")')
oa = oa.replace('port === "8080"', '(port === "8080" || port === "8081")')
with open("Client/Oauth2.c", "w", encoding="utf-8") as f:
    f.write(oa)

print("[OK] Client/DOM.c и Client/Oauth2.c обновлены для портов 8080 и 8081")
