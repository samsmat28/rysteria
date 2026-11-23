with open("Server/Server.c", "r", encoding="utf-8") as f:
    sc = f.read()

target = 'if (strncmp(animation->message, "/register ", 10) == 0 ||'
shop_block = """if (strcmp(animation->message, "/balance") == 0 ||
                        strncmp(animation->message, "/buy ", 5) == 0 ||
                        strncmp(animation->message, "/sell ", 6) == 0 ||
                        strcmp(animation->message, "/quest") == 0 ||
                        strcmp(animation->message, "/claim") == 0)
                    {
                        static const uint64_t sell_p = { 5, 15, 40, 120, 350, 1000, 3000, 9000, 25000, 75000, 200000 };
                        static const uint64_t q_rew = { 40, 100, 250, 700, 2000, 6000, 18000, 50000, 150000, 400000, 1000000 };
                        strcpy(animation->name, "[Shop]");
                        animation->type = rr_animation_type_chat;
                        animation->owner = client->player_info->parent_id;
                        if (strcmp(animation->message, "/balance") == 0) {
                            snprintf(animation->message, 64, "Balance: %llu R", (unsigned long long)client->r_coins);
                        } else if (strncmp(animation->message, "/buy ", 5) == 0) {
                            int pid = -1, rid = -1;
                            if (sscanf(animation->message + 5, "%d %d", &pid, &rid) == 2 && pid >= 1 && pid < rr_petal_id_max && rid >= 0 && rid < rr_rarity_id_max) {
                                uint64_t cost = sell_p[rid] * 2;
                                if (client->r_coins >= cost) {
                                    client->r_coins -= cost;
                                    client->inventory[pid][rid]++;
                                    rr_server_client_write_account(client);
                                    snprintf(animation->message, 64, "Bought! Bal: %llu R", (unsigned long long)client->r_coins);
                                } else {
                                    snprintf(animation->message, 64, "Need %llu R! Bal: %llu R", (unsigned long long)cost, (unsigned long long)client->r_coins);
                                }
                            } else {
                                snprintf(animation->message, 64, "Usage: /buy <id> <rarity>");
                            }
                        } else if (strncmp(animation->message, "/sell ", 6) == 0) {
                            int pid = -1, rid = -1;
                            if (sscanf(animation->message + 6, "%d %d", &pid, &rid) == 2 && pid >= 1 && pid < rr_petal_id_max && rid >= 0 && rid < rr_rarity_id_max) {
                                if (client->inventory[pid][rid] > 0) {
                                    client->inventory[pid][rid]--;
                                    client->r_coins += sell_p[rid];
                                    rr_server_client_write_account(client);
                                    snprintf(animation->message, 64, "Sold +%llu R! Bal: %llu R", (unsigned long long)sell_p[rid], (unsigned long long)client->r_coins);
                                } else {
                                    snprintf(animation->message, 64, "You don't have this petal!");
                                }
                            } else {
                                snprintf(animation->message, 64, "Usage: /sell <id> <rarity>");
                            }
                        } else if (strcmp(animation->message, "/quest") == 0) {
                            if (client->quest_target == 0) { client->quest_rarity = 0; client->quest_target = 5; client->quest_progress = 0; }
                            uint8_t r = client->quest_rarity < 11 ? client->quest_rarity : 0;
                            snprintf(animation->message, 64, "Quest: %u/%u %s (+%llu R)", client->quest_progress, client->quest_target, RR_RARITY_NAMES[r], (unsigned long long)q_rew[r]);
                        } else if (strcmp(animation->message, "/claim") == 0) {
                            if (client->quest_target > 0 && client->quest_progress >= client->quest_target) {
                                uint8_t r = client->quest_rarity < 11 ? client->quest_rarity : 0;
                                client->r_coins += q_rew[r];
                                client->quest_rarity = (uint8_t)((r + 1) % 7);
                                client->quest_target = (uint16_t)(5 + client->quest_rarity * 2);
                                client->quest_progress = 0;
                                rr_server_client_write_account(client);
                                snprintf(animation->message, 64, "Claimed! Bal: %llu R", (unsigned long long)client->r_coins);
                            } else {
                                snprintf(animation->message, 64, "Not done: %u/%u!", client->quest_progress, client->quest_target);
                            }
                        }
                        break;
                    }
                    else """

if 'strcmp(animation->message, "/balance")' not in sc and target in sc:
    sc = sc.replace(target, shop_block + target, 1)
    with open("Server/Server.c", "w", encoding="utf-8") as f:
        f.write(sc)
    print("[OK] Команды магазина и квестов встроены в Server/Server.c")
