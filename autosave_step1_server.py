# 1. Добавляем автосохранение на диск внутрь rr_server_client_write_account в Server/Client.c
with open("Server/Client.c", "r", encoding="utf-8") as f:
    cc = f.read()

if "#include <sys/stat.h>" not in cc:
    cc = "#include <sys/stat.h>\n#include <stdio.h>\n" + cc

save_helper = """
void rr_server_autosave_disk(struct rr_server_client *client)
{
    if (!client) return;
    const char *id = (client->logged_user[0] != 0) ? client->logged_user : client->rivet_account.uuid;
    if (!id || id[0] == 0) return;
    mkdir("accounts", 0755);
    char path[128];
    snprintf(path, sizeof(path), "accounts/%s.auto", id);
    FILE *f = fopen(path, "wb");
    if (!f) return;
    uint32_t magic = 0x52525331; // "RRS1"
    fwrite(&magic, sizeof(magic), 1, f);
    fwrite(&client->experience, sizeof(client->experience), 1, f);
    fwrite(client->inventory, sizeof(client->inventory), 1, f);
    fwrite(client->mob_gallery, sizeof(client->mob_gallery), 1, f);
    fwrite(&client->has_checkpoint, 1, 1, f);
    fwrite(&client->checkpoint_difficulty, 1, 1, f);
    fwrite(&client->checkpoint_x, sizeof(float), 1, f);
    fwrite(&client->checkpoint_y, sizeof(float), 1, f);
    fwrite(&client->r_coins, sizeof(client->r_coins), 1, f);
    fwrite(&client->quest_rarity, 1, 1, f);
    fwrite(&client->quest_target, sizeof(client->quest_target), 1, f);
    fwrite(&client->quest_progress, sizeof(client->quest_progress), 1, f);
    fclose(f);
}

void rr_server_autoload_disk(struct rr_server_client *client)
{
    if (!client) return;
    const char *id = (client->logged_user[0] != 0) ? client->logged_user : client->rivet_account.uuid;
    if (!id || id[0] == 0) return;
    char path[128];
    snprintf(path, sizeof(path), "accounts/%s.auto", id);
    FILE *f = fopen(path, "rb");
    if (!f) return;
    uint32_t magic = 0;
    if (fread(&magic, sizeof(magic), 1, f) == 1 && magic == 0x52525331) {
        fread(&client->experience, sizeof(client->experience), 1, f);
        fread(client->inventory, sizeof(client->inventory), 1, f);
        fread(client->mob_gallery, sizeof(client->mob_gallery), 1, f);
        fread(&client->has_checkpoint, 1, 1, f);
        fread(&client->checkpoint_difficulty, 1, 1, f);
        fread(&client->checkpoint_x, sizeof(float), 1, f);
        fread(&client->checkpoint_y, sizeof(float), 1, f);
        fread(&client->r_coins, sizeof(client->r_coins), 1, f);
        fread(&client->quest_rarity, 1, 1, f);
        fread(&client->quest_target, sizeof(client->quest_target), 1, f);
        fread(&client->quest_progress, sizeof(client->quest_progress), 1, f);
    }
    fclose(f);
}
"""

if "rr_server_autosave_disk" not in cc:
    cc = cc.replace(
        "void rr_server_client_write_account(struct rr_server_client *client)\n{",
        save_helper + "\nvoid rr_server_client_write_account(struct rr_server_client *client)\n{\n    rr_server_autosave_disk(client);"
    )
    with open("Server/Client.c", "w", encoding="utf-8") as f:
        f.write(cc)
    print("[OK] Автосохранение встроено в Server/Client.c")

# 2. В Server/Server.c вызываем rr_server_autoload_disk перед rr_server_client_write_account при входе (строка 1640)
with open("Server/Server.c", "r", encoding="utf-8") as f:
    sc = f.read()

if "extern void rr_server_autoload_disk" not in sc:
    sc = "extern void rr_server_autoload_disk(struct rr_server_client *client);\n" + sc

target_join = 'rr_server_client_write_oauth2_data(client);\n                rr_server_client_write_account(client);'
if target_join in sc and "rr_server_autoload_disk(client);" not in sc:
    sc = sc.replace(target_join, 'rr_server_client_write_oauth2_data(client);\n                rr_server_autoload_disk(client);\n                rr_server_client_write_account(client);', 1)
    with open("Server/Server.c", "w", encoding="utf-8") as f:
        f.write(sc)
    print("[OK] Автозагрузка при входе встроена в Server/Server.c")
