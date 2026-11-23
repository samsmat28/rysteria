import re

# 1. Добавляем поля квеста в Server/Client.h
with open("Server/Client.h", "r", encoding="utf-8") as f:
    ch = f.read()

if "quest_target" not in ch:
    ch = re.sub(
        r"(uint64_t\s+r_coins\s*;)",
        r"\1\n    uint8_t quest_rarity;\n    uint16_t quest_target;\n    uint16_t quest_progress;",
        ch,
        count=1
    )
    with open("Server/Client.h", "w", encoding="utf-8") as f:
        f.write(ch)
    print("[OK] Server/Client.h обновлен")

# 2. Добавляем логику квестов в Server/Server.c
with open("Server/Server.c", "r", encoding="utf-8") as f:
    sc = f.read()

# Инициализация первого квеста (убить 5 Common мобов)
if "quest_target = 5" not in sc:
    sc = re.sub(
        r"(client->r_coins\s*=\s*100\s*;)",
        r"\1\n    client->quest_rarity = 0;\n    client->quest_target = 5;\n    client->quest_progress = 0;",
        sc
    )

# Сохранение и загрузка прогресса квеста в .sav
if "fwrite(&client->quest_rarity" not in sc:
    sc = re.sub(
        r"(fwrite\(&client->r_coins,\s*sizeof\(uint64_t\),\s*1,\s*([a-zA-Z0-9_]+)\);)",
        r"\1\n            fwrite(&client->quest_rarity, sizeof(uint8_t), 1, \2);\n            fwrite(&client->quest_target, sizeof(uint16_t), 1, \2);\n            fwrite(&client->quest_progress, sizeof(uint16_t), 1, \2);",
        sc
    )
    sc = re.sub(
        r"(if\s*\(fread\(&client->r_coins[^;]+;)",
        r"\1\n            if (fread(&client->quest_rarity, sizeof(uint8_t), 1, f) != 1) { client->quest_rarity = 0; client->quest_target = 5; client->quest_progress = 0; } else { fread(&client->quest_target, sizeof(uint16_t), 1, f); fread(&client->quest_progress, sizeof(uint16_t), 1, f); }",
        sc
    )

# Подсчёт убийства моба нужной редкости при начислении опыта игроку
if "client->quest_progress++" not in sc:
    # Ищем место начисления опыта за убийство моба (обычно attacker->experience += или client->experience += рядом с mob)
    m_exp = re.search(r"([a-zA-Z0-9_]+)->experience\s*\+=\s*[^;]*([a-zA-Z0-9_]+)->rarity[^;]*;", sc)
    if m_exp:
        plr_v, mob_v = m_exp.group(1), m_exp.group(2)
        hook = (
            f"\n                if ({plr_v}->quest_target > 0 && {mob_v}->rarity == {plr_v}->quest_rarity && {plr_v}->quest_progress < {plr_v}->quest_target) {{\n"
            f"                    {plr_v}->quest_progress++;\n"
            f"                }}"
        )
        sc = sc[:m_exp.end()] + hook + sc[m_exp.end():]
        print(f"[OK] Подсчёт убийств привязан к {plr_v} и {mob_v}")
    else:
        print("[WARN] Не найдена строка начисления опыта за моба, проверь имя переменной моба")

# Команды /quest и /claim в чате
quest_cmds = """
            } else if (strcmp(cmd_buf, "/quest") == 0) {
                if (client->quest_target == 0) {
                    client->quest_rarity = (uint8_t)(rand() % 6);
                    client->quest_target = (uint16_t)(5 + (rand() % 6) * 2);
                    client->quest_progress = 0;
                }
                static const uint64_t q_rewards = { 40, 100, 250, 700, 2000, 6000, 18000, 50000, 150000, 400000, 1000000 };
                uint64_t rew = q_rewards[client->quest_rarity < 11 ? client->quest_rarity : 0];
                char out;
                snprintf(out, sizeof(out), "Квест: Убить %u мобов [%s] (%u/%u) | Награда: %llu R",
                         client->quest_target, RR_RARITY_NAMES[client->quest_rarity],
                         client->quest_progress, client->quest_target, (unsigned long long)rew);
                rr_send_shop_msg(client, out);
                break;
            } else if (strcmp(cmd_buf, "/claim") == 0) {
                if (client->quest_target > 0 && client->quest_progress >= client->quest_target) {
                    static const uint64_t q_rewards = { 40, 100, 250, 700, 2000, 6000, 18000, 50000, 150000, 400000, 1000000 };
                    uint8_t r = client->quest_rarity < 11 ? client->quest_rarity : 0;
                    uint64_t rew = q_rewards[r];
                    client->r_coins += rew;
                    client->quest_rarity = (uint8_t)(rand() % 7);
                    client->quest_target = (uint16_t)(5 + (rand() % 6) * 2);
                    client->quest_progress = 0;
                    rr_server_client_write_account(client);
                    char out;
                    snprintf(out, sizeof(out), "Квест выполнен! +%llu R (Баланс: %llu R). Новый квест: %u мобов [%s]",
                             (unsigned long long)rew, (unsigned long long)client->r_coins,
                             client->quest_target, RR_RARITY_NAMES[client->quest_rarity]);
                    rr_send_shop_msg(client, out);
                } else {
                    char out;
                    snprintf(out, sizeof(out), "Квест ещё не выполнен (%u/%u [%s])!",
                             client->quest_progress, client->quest_target, RR_RARITY_NAMES[client->quest_rarity]);
                    rr_send_shop_msg(client, out);
                }
                break;
"""

if 'strcmp(cmd_buf, "/quest")' not in sc:
    sc = sc.replace('if (strcmp(cmd_buf, "/balance") == 0) {', 'if (strcmp(cmd_buf, "/balance") == 0) {', 1)
    sc = re.sub(
        r'(if\s*\(\s*strcmp\(\s*cmd_buf\s*,\s*"/balance"\s*\)\s*==\s*0\s*\)\s*\{[^}]+\})',
        r'\1' + quest_cmds,
        sc,
        count=1
    )

with open("Server/Server.c", "w", encoding="utf-8") as f:
    f.write(sc)
print("[OK] Server/Server.c обновлен")
