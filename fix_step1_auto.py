import re

with open("Shared/StaticData.h", "r", encoding="utf-8") as f:
    sd = f.read()

with open("Server/Server.c", "r", encoding="utf-8") as f:
    sc = f.read()

# 1. Удаляем старый helper rr_send_shop_msg
sc = re.sub(r"\nstatic void rr_send_shop_msg\(struct rr_server_client \*client, const char \*text\).*?\n\}\n", "\n", sc, flags=re.DOTALL)

# 2. Находим точный enum clientbound пакета чата в Shared/StaticData.h
m_cb = re.search(r"(rr_clientbound_[a-zA-Z0-9_]*chat[a-zA-Z0-9_]*|rr_clientbound_[a-zA-Z0-9_]*msg[a-zA-Z0-9_]*|rr_clientbound_[a-zA-Z0-9_]*message[a-zA-Z0-9_]*)", sd)
cb_chat_enum = m_cb.group(1) if m_cb else "0"

# 3. Извлекаем весь блок case rr_serverbound_chat в Server/Server.c
m_case = re.search(r"(case\s+rr_serverbound_chat\s*:.*?)(?=\n\s*(?:case\s+rr_serverbound_|default\s*:))", sc, flags=re.DOTALL)
case_block = m_case.group(1) if m_case else ""

# Ищем в этом блоке функцию отправки клиенту и переменные сообщения/длины
m_send = re.search(r"([a-zA-Z0-9_]+)\s*\(\s*(?:server\s*,\s*)?client\s*,", case_block)
send_call = m_send.group(0) if m_send else "rr_server_send(client,"
send_fn = m_send.group(1) if m_send else ""

# Если в case rr_serverbound_chat нет отправки, ищем любую функцию отправки пакета в Server.c
if not send_fn or send_fn in ("if", "while", "for", "switch", "memcpy", "memset", "snprintf", "strncmp", "strcmp", "strlen"):
    m_any_send = re.search(r"([a-zA-Z0-9_]*send[a-zA-Z0-9_]*)\s*\(\s*(?:struct\s+rr_server\s*\*\s*[a-zA-Z0-9_]+\s*,\s*)?struct\s+rr_server_client\s*\*", sc)
    if m_any_send:
        send_fn = m_any_send.group(1)
        sig = m_any_send.group(0)
        send_call = f"{send_fn}(server, client," if "rr_server *" in sig else f"{send_fn}(client,"

# Ищем переменные текста и длины в case rr_serverbound_chat
m_txt = re.search(r"(?:const\s+)?char\s*\*\s*([a-zA-Z0-9_]+)\s*=", case_block)
txt_var = m_txt.group(1) if m_txt else "message"

m_len = re.search(r"(?:size_t|uint(?:8|16|32)_t|int)\s+([a-zA-Z0-9_]+)\s*=", case_block)
len_var = m_len.group(1) if m_len else "length"

# Ищем в case_block, как уже формируется системный ответ в чат (например, при ошибке уровня или /login)
m_existing_chat = re.search(r"(uint8_t\s+[a-zA-Z0-9_]+\[\d+\].*?" + re.escape(send_fn) + r"\([^;]+;)", case_block, flags=re.DOTALL)

# Вставляем helper перед функцией с case rr_serverbound_chat
chat_pos = sc.find("case rr_serverbound_chat:")
func_start = sc.rfind("\nvoid ", 0, chat_pos)
if func_start == -1:
    func_start = sc.rfind("\nstatic ", 0, chat_pos)

# Проверяем, принимает ли функция отправки (server, client, ...) или (client, ...)
needs_server = "(server, client," in send_call
helper_sig = "struct rr_server *server, struct rr_server_client *client" if needs_server else "struct rr_server_client *client"
helper_arg = "server, client" if needs_server else "client"

helper_code = f"""
static void rr_send_shop_msg({helper_sig}, const char *text) {{
    if (!client || !text) return;
    uint8_t buf[300];
    memset(buf, 0, sizeof(buf));
    const char *sender = "[Shop]";
    size_t slen = strlen(sender);
    size_t tlen = strlen(text);
    if (tlen > 240) tlen = 240;
    buf = {cb_chat_enum};
    buf = (uint8_t)slen;
    memcpy(buf + 2, sender, slen);
    buf[2 + slen] = (uint8_t)tlen;
    memcpy(buf + 3 + slen, text, tlen);
    {send_call} buf, 3 + slen + tlen);
}}
"""

if func_start != -1:
    sc = sc[:func_start] + "\n" + helper_code + sc[func_start:]

# Находим место вставки команд сразу после инициализации txt_var и len_var в case rr_serverbound_chat
shop_logic = f"""
        {{
            static const uint64_t sell_prices = {{
                5, 15, 40, 120, 350, 1000, 3000, 9000, 25000, 75000, 200000
            }};
            char cmd_buf[128];
            size_t copy_len = (size_t){len_var} < sizeof(cmd_buf) - 1 ? (size_t){len_var} : sizeof(cmd_buf) - 1;
            memcpy(cmd_buf, {txt_var}, copy_len);
            cmd_buf[copy_len] = 0;

            if (strcmp(cmd_buf, "/balance") == 0) {{
                char out[128];
                snprintf(out, sizeof(out), "Ваш баланс: %llu R", (unsigned long long)client->r_coins);
                rr_send_shop_msg({helper_arg}, out);
                break;
            }} else if (strncmp(cmd_buf, "/sell ", 6) == 0) {{
                int pid = -1, rid = -1;
                if (sscanf(cmd_buf + 6, "%d %d", &pid, &rid) == 2 &&
                    pid >= 1 && pid < rr_petal_id_max &&
                    rid >= 0 && rid < rr_rarity_id_max) {{
                    if (client->inventory[pid][rid] > 0) {{
                        client->inventory[pid][rid]--;
                        uint64_t reward = sell_prices[rid];
                        client->r_coins += reward;
                        rr_server_client_write_account(client);
                        char out[128];
                        snprintf(out, sizeof(out), "Продано! +%llu R (Баланс: %llu R)",
                                 (unsigned long long)reward, (unsigned long long)client->r_coins);
                        rr_send_shop_msg({helper_arg}, out);
                    }} else {{
                        rr_send_shop_msg({helper_arg}, "У вас нет такого лепестка!");
                    }}
                }} else {{
                    rr_send_shop_msg({helper_arg}, "Формат: /sell <petal_id> <rarity_id>");
                }}
                break;
            }} else if (strncmp(cmd_buf, "/buy ", 5) == 0) {{
                int pid = -1, rid = -1;
                if (sscanf(cmd_buf + 5, "%d %d", &pid, &rid) == 2 &&
                    pid >= 1 && pid < rr_petal_id_max &&
                    rid >= 0 && rid < rr_rarity_id_max) {{
                    uint64_t cost = sell_prices[rid] * 2;
                    if (client->r_coins >= cost) {{
                        client->r_coins -= cost;
                        client->inventory[pid][rid]++;
                        rr_server_client_write_account(client);
                        char out[128];
                        snprintf(out, sizeof(out), "Куплено за %llu R! (Баланс: %llu R)",
                                 (unsigned long long)cost, (unsigned long long)client->r_coins);
                        rr_send_shop_msg({helper_arg}, out);
                    }} else {{
                        char out[128];
                        snprintf(out, sizeof(out), "Недостаточно R! Нужно: %llu R", (unsigned long long)cost);
                        rr_send_shop_msg({helper_arg}, out);
                    }}
                }} else {{
                    rr_send_shop_msg({helper_arg}, "Формат: /buy <petal_id> <rarity_id>");
                }}
                break;
            }}
        }}
"""

# Вставляем после строчки объявления txt_var в case rr_serverbound_chat
insert_pat = r"(case\s+rr_serverbound_chat\s*:.*?" + re.escape(txt_var) + r"\s*=[^;]+;)"
if re.search(insert_pat, sc, flags=re.DOTALL):
    sc = re.sub(insert_pat, r"\1\n" + shop_logic, sc, count=1, flags=re.DOTALL)
    print(f"[OK] Вставлено! enum={cb_chat_enum}, send={send_fn}, txt={txt_var}, len={len_var}")
else:
    print("[DUMP] Покажи этот блок:")
    print(case_block[:700])

with open("Server/Server.c", "w", encoding="utf-8") as f:
    f.write(sc)
