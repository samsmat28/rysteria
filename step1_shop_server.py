import os, re

# 1. Обновление Server/Client.h
with open("Server/Client.h", "r", encoding="utf-8") as f:
    ch = f.read()

if "uint64_t r_coins;" not in ch:
    ch = re.sub(
        r"(double\s+experience\s*;)",
        r"\1\n    uint64_t r_coins;",
        ch,
        count=1
    )
    with open("Server/Client.h", "w", encoding="utf-8") as f:
        f.write(ch)
    print("[OK] Server/Client.h обновлен")

# 2. Обновление Server/Server.c
with open("Server/Server.c", "r", encoding="utf-8") as f:
    sc = f.read()

# Инициализация стартового баланса 100 R при создании/сбросе клиента
if "r_coins = 100" not in sc:
    sc = re.sub(
        r"(client->experience\s*=\s*0[^;]*;)",
        r"\1\n    client->r_coins = 100;",
        sc
    )

# Сохранение и загрузка r_coins в accounts/<user>.sav
if "fwrite(&client->r_coins" not in sc:
    sc = re.sub(
        r"(fwrite\(&client->experience,\s*sizeof\(double\),\s*1,\s*([a-zA-Z0-9_]+)\);)",
        r"\1\n            fwrite(&client->r_coins, sizeof(uint64_t), 1, \2);",
        sc
    )
    sc = re.sub(
        r"(fread\(&client->experience,\s*sizeof\(double\),\s*1,\s*([a-zA-Z0-9_]+)\);)",
        r"\1\n            if (fread(&client->r_coins, sizeof(uint64_t), 1, \2) != 1) client->r_coins = 100;",
        sc
    )

# Вспомогательная функция отправки безопасного системного сообщения в чат
shop_helper = """
static void rr_send_shop_msg(struct rr_server_client *client, const char *text) {
    if (!client || !text) return;
    uint8_t buf[512];
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
    rr_server_send(client, buf, 3 + slen + tlen);
}
"""

if "rr_send_shop_msg" not in sc:
    sc = re.sub(
        r"(case\s+rr_serverbound_chat\s*:)",
        shop_helper + r"\n\1",
        sc,
        count=1
    )

# Обработка команд /balance, /sell, /buy до проверки уровня
chat_commands = """
        {
            static const uint64_t sell_prices[11] = {
                5, 15, 40, 120, 350, 1000, 3000, 9000, 25000, 75000, 200000
            };
            char cmd_buf[256];
            size_t copy_len = len < sizeof(cmd_buf) - 1 ? len : sizeof(cmd_buf) - 1;
            memcpy(cmd_buf, msg, copy_len);
            cmd_buf[copy_len] = '\\0';

            if (strcmp(cmd_buf, "/balance") == 0) {
                char out[128];
                snprintf(out, sizeof(out), "Ваш баланс: %llu R", (unsigned long long)client->r_coins);
                rr_send_shop_msg(client, out);
                break;
            } else if (strncmp(cmd_buf, "/sell ", 6) == 0) {
                int pid = -1, rid = -1;
                if (sscanf(cmd_buf + 6, "%d %d", &pid, &rid) == 2 &&
                    pid >= 1 && pid < rr_petal_id_max &&
                    rid >= 0 && rid < rr_rarity_id_max) {
                    if (client->inventory[pid][rid] > 0) {
                        client->inventory[pid][rid]--;
                        uint64_t reward = sell_prices[rid];
                        client->r_coins += reward;
                        rr_server_client_write_account(client);
                        char out[160];
                        snprintf(out, sizeof(out), "Продано! +%llu R (Баланс: %llu R)",
                                 (unsigned long long)reward, (unsigned long long)client->r_coins);
                        rr_send_shop_msg(client, out);
                    } else {
                        rr_send_shop_msg(client, "У вас нет такого лепестка!");
                    }
                } else {
                    rr_send_shop_msg(client, "Формат: /sell <petal_id> <rarity_id>");
                }
                break;
            } else if (strncmp(cmd_buf, "/buy ", 5) == 0) {
                int pid = -1, rid = -1;
                if (sscanf(cmd_buf + 5, "%d %d", &pid, &rid) == 2 &&
                    pid >= 1 && pid < rr_petal_id_max &&
                    rid >= 0 && rid < rr_rarity_id_max) {
                    uint64_t cost = sell_prices[rid] * 2;
                    if (client->r_coins >= cost) {
                        client->r_coins -= cost;
                        client->inventory[pid][rid]++;
                        rr_server_client_write_account(client);
                        char out[160];
                        snprintf(out, sizeof(out), "Куплено за %llu R! (Баланс: %llu R)",
                                 (unsigned long long)cost, (unsigned long long)client->r_coins);
                        rr_send_shop_msg(client, out);
                    } else {
                        char out[160];
                        snprintf(out, sizeof(out), "Недостаточно R! Нужно: %llu R", (unsigned long long)cost);
                        rr_send_shop_msg(client, out);
                    }
                } else {
                    rr_send_shop_msg(client, "Формат: /buy <petal_id> <rarity_id>");
                }
                break;
            }
        }
"""

if 'strncmp(cmd_buf, "/sell ", 6)' not in sc:
    sc = re.sub(
        r"(case\s+rr_serverbound_chat\s*:[^\n]*\n)",
        r"\1" + chat_commands,
        sc,
        count=1
    )

with open("Server/Server.c", "w", encoding="utf-8") as f:
    f.write(sc)
print("[OK] Server/Server.c обновлен")
