import re

with open("Server/Server.c", "r", encoding="utf-8") as f:
    sc = f.read()

with open("Server/Client.h", "r", encoding="utf-8") as f:
    ch = f.read()

# 1. Находим реальную функцию отправки пакета клиенту (из Client.h или Server.c)
m_fn = re.search(r"void\s+([a-zA-Z0-9_]+)\s*\(\s*struct\s+rr_server_client\s*\*\s*[a-zA-Z0-9_]+\s*,\s*(?:const\s+)?(?:uint8_t|void|char)\s*\*", ch + "\n" + sc)
if not m_fn:
    m_fn = re.search(r"([a-zA-Z0-9_]+)\s*\(\s*client\s*,\s*[a-zA-Z0-9_&]+\s*,\s*(?:sizeof|[0-9]+)", sc)
real_send = m_fn.group(1) if m_fn else "rr_server_client_send"

# Находим реальный enum для пакета чата (если 0 был заглушкой)
with open("Shared/StaticData.h", "r", encoding="utf-8") as f:
    sd = f.read()
m_enum = re.search(r"(rr_clientbound_[a-zA-Z0-9_]+)", sd)
# Ищем в Server.c как отправляется чат другим игрокам
m_chat_pkt = re.search(r"([a-zA-Z0-9_]+)\s*\[\s*0\s*\]\s*=\s*(rr_clientbound_[a-zA-Z0-9_]+chat[a-zA-Z0-9_]*)", sc)
chat_id = m_chat_pkt.group(2) if m_chat_pkt else (m_enum.group(1) if m_enum else "0")

# 2. Заменяем тело rr_send_shop_msg на корректное с индексами [0] и [1] через chr(91)/chr(93)
LB, RB = chr(91), chr(93)
new_helper = (
    "static void rr_send_shop_msg(struct rr_server_client *client, const char *text) {\n"
    "    if (!client || !text) return;\n"
    f"    uint8_t buf{LB}300{RB};\n"
    "    memset(buf, 0, sizeof(buf));\n"
    "    const char *sender = \"[Shop]\";\n"
    "    size_t slen = strlen(sender);\n"
    "    size_t tlen = strlen(text);\n"
    "    if (tlen > 240) tlen = 240;\n"
    f"    buf{LB}0{RB} = {chat_id};\n"
    f"    buf{LB}1{RB} = (uint8_t)slen;\n"
    "    memcpy(buf + 2, sender, slen);\n"
    f"    buf{LB}2 + slen{RB} = (uint8_t)tlen;\n"
    "    memcpy(buf + 3 + slen, text, tlen);\n"
    f"    {real_send}(client, buf, 3 + slen + tlen);\n"
    "}\n"
)

sc = re.sub(
    r"static void rr_send_shop_msg\(.*?\n\}\n",
    new_helper,
    sc,
    count=1,
    flags=re.DOTALL
)

# Исправляем вызов rr_send_shop_msg, если ранее передавался лишний аргумент server
sc = sc.replace("rr_send_shop_msg(server, client,", "rr_send_shop_msg(client,")

with open("Server/Server.c", "w", encoding="utf-8") as f:
    f.write(sc)

print(f"[OK] Использована функция {real_send} и пакет {chat_id}")
