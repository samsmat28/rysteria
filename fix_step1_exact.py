import re, glob

with open("Shared/StaticData.h", "r", encoding="utf-8") as f:
    sd = f.read()

# 1. Находим все enum rr_clientbound_... из Shared/StaticData.h
cb_enums = re.findall(r"(rr_clientbound_[a-zA-Z0-9_]+)", sd)
chat_enum = next((e for e in cb_enums if "chat" in e or "msg" in e or "message" in e), cb_enums[-1] if cb_enums else "0")

# 2. Ищем во всех файлах Server/*.c и Server/*.h реальную функцию отправки пакета клиенту (например lws_write / rr_client_send / etc)
server_files = glob.glob("Server/*.[ch]")
all_code = ""
for fn in server_files:
    with open(fn, "r", encoding="utf-8") as f:
        all_code += f"\n/* FILE: {fn} */\n" + f.read()

# Ищем в коде место, где используется chat_enum (как сервер шлёт чат игроку)
m_chat_impl = re.search(r"([^\n;]*?" + re.escape(chat_enum) + r".{1,500}?;)", all_code, flags=re.DOTALL)
# Ищем любую функцию отправки клиенту, отличную от rr_send_shop_msg
send_candidates = re.findall(r"\b([a-zA-Z0-9_]+)\s*\(\s*client\s*,\s*[^,]+,\s*[^)]+\)", all_code)
send_candidates = [s for s in send_candidates if s not in ("rr_send_shop_msg", "memcpy", "memset", "snprintf", "strncmp", "strncpy", "fread", "fwrite")]
real_send = send_candidates[0] if send_candidates else None

# Если не нашли по шаблону (client, buf, len), ищем в rr_server_client_write_account как он шлёт данные клиенту
if not real_send:
    m_wa = re.search(r"void\s+rr_server_client_write_account\s*\([^)]*\)\s*\{(.{1,1200}?)\n\}", all_code, flags=re.DOTALL)
    if m_wa:
        wa_body = m_wa.group(1)
        m_wcall = re.search(r"\b([a-zA-Z0-9_]+)\s*\(\s*client\s*,", wa_body)
        if m_wcall:
            real_send = m_wcall.group(1)

with open("Server/Server.c", "r", encoding="utf-8") as f:
    sc = f.read()

LB, RB = chr(91), chr(93)

if real_send:
    new_helper = (
        "static void rr_send_shop_msg(struct rr_server_client *client, const char *text) {\n"
        "    if (!client || !text) return;\n"
        f"    uint8_t buf{LB}300{RB};\n"
        "    memset(buf, 0, sizeof(buf));\n"
        "    const char *sender = \"[Shop]\";\n"
        "    size_t slen = strlen(sender);\n"
        "    size_t tlen = strlen(text);\n"
        "    if (tlen > 240) tlen = 240;\n"
        f"    buf{LB}0{RB} = {chat_enum};\n"
        f"    buf{LB}1{RB} = (uint8_t)slen;\n"
        "    memcpy(buf + 2, sender, slen);\n"
        f"    buf{LB}2 + slen{RB} = (uint8_t)tlen;\n"
        "    memcpy(buf + 3 + slen, text, tlen);\n"
        f"    {real_send}(client, buf, 3 + slen + tlen);\n"
        "}\n"
    )
    sc = re.sub(r"static void rr_send_shop_msg\(.*?\n\}\n", new_helper, sc, count=1, flags=re.DOTALL)
    with open("Server/Server.c", "w", encoding="utf-8") as f:
        f.write(sc)
    print(f"[OK] Найдена реальная отправка: {real_send}, enum: {chat_enum}")
else:
    print("[INFO] Список enum:", cb_enums)
    m_wa = re.search(r"void\s+rr_server_client_write_account\s*\([^)]*\)\s*\{(.{1,800})", all_code, flags=re.DOTALL)
    print("[INFO] write_account:", m_wa.group(1) if m_wa else "not found")
