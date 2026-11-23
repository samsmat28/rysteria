# 1. Server/Client.h: добавляем char logged_user[32];
with open("Server/Client.h", "r", encoding="utf-8") as f:
    ch = f.read()

if "logged_user" not in ch:
    ch = ch.replace("    float ygg_y;\n};", "    float ygg_y;\n    char logged_user[32];\n};", 1)
    with open("Server/Client.h", "w", encoding="utf-8") as f:
        f.write(ch)

# 2. Server/Server.c: добавляем команды /register, /login, /save прямо в папку Server/accounts/
with open("Server/Server.c", "r", encoding="utf-8") as f:
    srv = f.read()

if "<sys/stat.h>" not in srv:
    srv = "#include <sys/stat.h>\n" + srv

target = """        if (animation->message == 0)
        {
            --this->simulation.animation_length;
            break;
        }"""

auth_cmds = target + """
        if (strncmp(animation->message, "/register ", 10) == 0 ||
            strncmp(animation->message, "/login ", 7) == 0 ||
            strcmp(animation->message, "/save") == 0)
        {
            mkdir("accounts", 0755);
            char cmd[16] = {0}, user[32] = {0}, pass[32] = {0};
            int args = sscanf(animation->message, "%15s %31s %31s", cmd, user, pass);
            strcpy(animation->name, "[Account]");
            if (strcmp(cmd, "/save") == 0)
            {
                if (client->logged_user[0] == 0)
                    strcpy(animation->message, "Use: /register <login> <pass> or /login <login> <pass>");
                else
                {
                    char path[96];
                    snprintf(path, sizeof(path), "accounts/%s.sav", client->logged_user);
                    FILE *f = fopen(path, "rb+");
                    if (f) {
                        fseek(f, 32, SEEK_SET);
                        fwrite(&client->experience, sizeof(client->experience), 1, f);
                        fwrite(client->inventory, sizeof(client->inventory), 1, f);
                        fwrite(client->mob_gallery, sizeof(client->mob_gallery), 1, f);
                        fwrite(&client->has_checkpoint, 1, 1, f);
                        fwrite(&client->checkpoint_difficulty, 1, 1, f);
                        fwrite(&client->checkpoint_x, sizeof(float), 1, f);
                        fwrite(&client->checkpoint_y, sizeof(float), 1, f);
                        fclose(f);
                        snprintf(animation->message, 64, "Saved account: %s!", client->logged_user);
                    } else strcpy(animation->message, "Save file error!");
                }
            }
            else if (args < 3 || strlen(user) < 3 || strlen(pass) < 3)
            {
                strcpy(animation->message, "Format: /register <login> <pass> (min 3 chars)");
            }
            else
            {
                char path[96];
                snprintf(path, sizeof(path), "accounts/%s.sav", user);
                if (strcmp(cmd, "/register") == 0)
                {
                    FILE *chk = fopen(path, "rb");
                    if (chk) { fclose(chk); strcpy(animation->message, "Login already exists! Use /login"); }
                    else {
                        FILE *f = fopen(path, "wb");
                        if (f) {
                            fwrite(pass, 32, 1, f);
                            fwrite(&client->experience, sizeof(client->experience), 1, f);
                            fwrite(client->inventory, sizeof(client->inventory), 1, f);
                            fwrite(client->mob_gallery, sizeof(client->mob_gallery), 1, f);
                            fwrite(&client->has_checkpoint, 1, 1, f);
                            fwrite(&client->checkpoint_difficulty, 1, 1, f);
                            fwrite(&client->checkpoint_x, sizeof(float), 1, f);
                            fwrite(&client->checkpoint_y, sizeof(float), 1, f);
                            fclose(f);
                            strcpy(client->logged_user, user);
                            snprintf(animation->message, 64, "Registered & saved: %s!", user);
                        } else strcpy(animation->message, "Failed to create account file!");
                    }
                }
                else if (strcmp(cmd, "/login") == 0)
                {
                    FILE *f = fopen(path, "rb");
                    if (!f) strcpy(animation->message, "Account not found! Use /register");
                    else {
                        char saved_pass[32] = {0};
                        fread(saved_pass, 32, 1, f);
                        if (strncmp(saved_pass, pass, 32) != 0) {
                            fclose(f);
                            strcpy(animation->message, "Wrong password!");
                        } else {
                            fread(&client->experience, sizeof(client->experience), 1, f);
                            fread(client->inventory, sizeof(client->inventory), 1, f);
                            fread(client->mob_gallery, sizeof(client->mob_gallery), 1, f);
                            fread(&client->has_checkpoint, 1, 1, f);
                            fread(&client->checkpoint_difficulty, 1, 1, f);
                            fread(&client->checkpoint_x, sizeof(float), 1, f);
                            fread(&client->checkpoint_y, sizeof(float), 1, f);
                            fclose(f);
                            strcpy(client->logged_user, user);
                            rr_server_client_write_account(client);
                            snprintf(animation->message, 64, "Loaded account: %s!", user);
                        }
                    }
                }
            }
            break;
        }"""

assert target in srv, "Не найден блок animation->message в Server/Server.c"
if "accounts/%s.sav" not in srv:
    srv = srv.replace(target, auth_cmds, 1)
    with open("Server/Server.c", "w", encoding="utf-8") as f:
        f.write(srv)

print("Серверная система аккаунтов (/register, /login, /save) успешно добавлена!")
