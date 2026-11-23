import re

with open("Server/Server.c", "r", encoding="utf-8") as f:
    sc = f.read()

# 1. Удаляем кривой блок из прошлого скрипта
sc = re.sub(
    r"static void rr_send_shop_msg\(struct rr_server_client \*client, const char \*text\).*?case rr_serverbound_chat:\s*\{.*?\n        \}\n",
    "case rr_serverbound_chat:\n",
    sc,
    flags=re.DOTALL
)
# На случай если фигурной скобки не было сразу после case
sc = re.sub(
    r"static void rr_send_shop_msg\(struct rr_server_client \*client, const char \*text\).*?case rr_serverbound_chat:",
    "case rr_serverbound_chat:",
    sc,
    flags=re.DOTALL
)

# Выводим реальный контекст case rr_serverbound_chat и сохранения аккаунта, чтобы подставить 100% точные имена
m_chat = re.search(r"case\s+rr_serverbound_chat\s*:(.{1,900})", sc, flags=re.DOTALL)
chat_ctx = m_chat.group(1) if m_chat else ""
print("=== CONTEXT ===")
print(chat_ctx[:500])

# Определяем имена переменных буфера, длины и функции отправки из контекста
m_send = re.search(r"([a-zA-Z0-9_]+)\s*\(\s*client\s*,\s*[^,]+,\s*[^)]+\)", chat_ctx)
send_fn = m_send.group(1) if m_send else "rr_server_send"

m_msg = re.search(r"const\s+char\s*\*\s*([a-zA-Z0-9_]+)\s*=|char\s*\*\s*([a-zA-Z0-9_]+)\s*=|strncmp\(\s*([a-zA-Z0-9_]+)", chat_ctx)
msg_var = next((g for g in m_msg.groups() if g), "msg") if m_msg else "msg"

m_len = re.search(r"size_t\s+([a-zA-Z0-9_]+)\s*=|uint(?:8|16|32)_t\s+([a-zA-Z0-9_]+)\s*=", chat_ctx)
len_var = next((g for g in m_len.groups() if g), "len") if m_len else "len"

# Ищем функцию, в которой находится case rr_serverbound_chat, и вставляем helper ПЕРЕД ней
chat_pos = sc.find("case rr_serverbound_chat:")
func_start = sc.rfind("\nvoid ", 0, chat_pos)
if func_start == -1:
    func_start = sc.rfind("\nstatic ", 0, chat_pos)

helper_code = f"""
static void rr_send_shop_msg(struct rr_server_client *client, const char *text) {{
    if (!client || !text) return;
    uint8_t buf[300];
    memset(buf, 0, sizeof(buf));
    const char *sender = "[Shop]";
    size_t slen = strlen(sender);
    size_t tlen = strlen(text);
    if (tlen > 240) tlen = 240;
    buf[0] = rr_clientbound_chat;
    buf[1] = (uint8_t)slen;
    memcpy(buf + 2, sender, slen);
    buf[2 + slen] = (uint8_t)tlen;
    memcpy(buf + 3 + slen, text, tlen);
    {send_fn}(client, buf, 3 + slen + tlen);
}}
"""

if func_start != -1 and "rr_send_shop_msg" not in sc:
    sc = sc[:func_start] + "\n" + helper_code + sc[func_start:]

# Вставляем команды ПОСЛЕ объявления переменных msg и len в case rr_serverbound_chat
# Находим точку сразу перед проверкой уровня (обычно if (client->experience ...)
shop_logic = f"""
        {{
            static const uint64_t sell_prices[11] = {{
                5, 15, 40, 120, 350, 1000, 3000, 9000, 25000, 75000, 200000
            }};
            char cmd_buf[256];
            size_t copy_len = (size_t){len_var} < sizeof(cmd_buf) - 1 ? (size_t){len_var} : sizeof(cmd_buf) - 1;
            memcpy(cmd_buf, {msg_var}, copy_len);
            cmd_buf[copy_len] = 0;

            if (strcmp(cmd_buf, "/balance") == 0) {{
                char out[128];
                snprintf(out, sizeof(out), "Ваш баланс: %llu R", (unsigned long long)client->r_coins);
                rr_send_shop_msg(client, out);
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
                        rr_send_shop_msg(client, out);
                    }} else {{
                        rr_send_shop_msg(client, "У вас нет такого лепестка!");
                    }}
                }} else {{
                    rr_send_shop_msg(client, "Формат: /sell <petal_id> <rarity_id>");
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
                        rr_send_shop_msg(client, out);
                    }} else {{
                        char out[128];
                        snprintf(out, sizeof(out), "Недостаточно R! Нужно: %llu R", (unsigned long long)cost);
                        rr_send_shop_msg(client, out);
                    }}
                }} else {{
                    rr_send_shop_msg(client, "Формат: /buy <petal_id> <rarity_id>");
                }}
                break;
            }}
        }}
"""

# Вставляем перед проверкой client->experience или перед обработкой '/'
target_pattern = r"(case\s+rr_serverbound_chat\s*:.*?)(if\s*\(\s*client->experience|if\s*\(\s*" + re.escape(msg_var) + r"\s*\[\s*0\s*\]\s*==\s*'/')"
if re.search(target_pattern, sc, flags=re.DOTALL):
    sc = re.sub(target_pattern, r"\1" + shop_logic + r"\n        \2", sc, count=1, flags=re.DOTALL)
else:
    # Фолбэк: выводим кусок файла для точного патча, если структура нестандартная
    print("[WARN] Не найдена точка вставки команды, проверь вывод CONTEXT выше")

with open("Server/Server.c", "w", encoding="utf-8") as f:
    f.write(sc)
