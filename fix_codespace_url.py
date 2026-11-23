with open("Client/Oauth2.c", "r", encoding="utf-8") as f:
    oa = f.read()

old_base = 'const base = window.location.port === "8080" ? (window.location.protocol + "//" + window.location.hostname + ":3000") : "";'
new_base = 'const base = window.location.hostname.includes("-8080.") ? (window.location.protocol + "//" + window.location.hostname.replace("-8080.", "-3000.")) : (window.location.port === "8080" ? (window.location.protocol + "//" + window.location.hostname + ":3000") : "");'

assert old_base in oa, "Не найдена строка base в Client/Oauth2.c"
oa = oa.replace(old_base, new_base, 1)

with open("Client/Oauth2.c", "w", encoding="utf-8") as f:
    f.write(oa)
print("URL для Codespaces обновлен!")
