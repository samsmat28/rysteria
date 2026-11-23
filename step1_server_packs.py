with open("Server/Server.c", "r", encoding="utf-8") as f:
    sc = f.read()

target = 'strcmp(animation->message, "/claim") == 0)'
pack_check = 'strcmp(animation->message, "/claim") == 0 ||\n                        strncmp(animation->message, "/pack ", 6) == 0)'

pack_handler = """} else if (strncmp(animation->message, "/pack ", 6) == 0) {
                            int pk = atoi(animation->message + 6);
                            if (pk == 1) {
                                // Набор Охотника (300 R): Epic Claw + Epic Bone + Epic Amber
                                if (client->r_coins >= 300) {
                                    client->r_coins -= 300;
                                    client->inventory[43][3]++;
                                    client->inventory[44][3]++;
                                    client->inventory[45][3]++;
                                    rr_server_client_write_account(client);
                                    snprintf(animation->message, 64, "Dino Pack x3! Bal: %llu R", (unsigned long long)client->r_coins);
                                } else {
                                    snprintf(animation->message, 64, "Need 300 R! Bal: %llu R", (unsigned long long)client->r_coins);
                                }
                            } else if (pk == 2) {
                                // Сундук Удачи (500 R): случайный доисторический лепесток Legendary-Ultra!
                                if (client->r_coins >= 500) {
                                    client->r_coins -= 500;
                                    int pid = 43 + (rand() % (rr_petal_id_max - 43));
                                    int rid = 4 + (rand() % 3); // Legendary(4), Mythic(5), Ultra(6)
                                    client->inventory[pid][rid]++;
                                    rr_server_client_write_account(client);
                                    snprintf(animation->message, 64, "Box: %s [%s]!", RR_PETAL_NAMES[pid], RR_RARITY_NAMES[rid]);
                                } else {
                                    snprintf(animation->message, 64, "Need 500 R! Bal: %llu R", (unsigned long long)client->r_coins);
                                }
                            } else if (pk == 3) {
                                // Набор Бога (5000 R): Mythic Crown + Mythic Relic
                                if (client->r_coins >= 5000) {
                                    client->r_coins -= 5000;
                                    client->inventory[61][5]++;
                                    client->inventory[62][5]++;
                                    rr_server_client_write_account(client);
                                    snprintf(animation->message, 64, "Mythic God Pack! Bal: %llu R", (unsigned long long)client->r_coins);
                                } else {
                                    snprintf(animation->message, 64, "Need 5000 R! Bal: %llu R", (unsigned long long)client->r_coins);
                                }
                            } else {
                                snprintf(animation->message, 64, "Usage: /pack 1..3");
                            }
                        } else if (strcmp(animation->message, "/claim") == 0)"""

if 'strncmp(animation->message, "/pack ", 6)' not in sc and target in sc:
    sc = sc.replace(target, pack_check, 1)
    sc = sc.replace('} else if (strcmp(animation->message, "/claim") == 0)', pack_handler, 1)
    with open("Server/Server.c", "w", encoding="utf-8") as f:
        f.write(sc)
    print("[OK] Наборы /pack 1..3 и Сундук Удачи добавлены в Server/Server.c")
