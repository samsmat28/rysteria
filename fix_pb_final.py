with open("Server/System/PetalBehavior.c", "r", encoding="utf-8") as f:
    pb = f.read()

pb = '#include "../Server.h"\n' + pb

anchor = "\tpetal_modifiers(simulation, player_info);"
if anchor not in pb:
    anchor = "    petal_modifiers(simulation, player_info);"

hook = anchor + """
    if (player_info->client) {
        struct rr_component_arena *fa = rr_simulation_get_arena(simulation, flower_physical->arena);
        if (fa && fa->maze) {
            uint32_t dim = fa->maze->maze_dim, gx = (uint32_t)(flower_physical->x / fa->maze->grid_size), gy = (uint32_t)(flower_physical->y / fa->maze->grid_size);
            if (gx < dim && gy < dim && fa->maze->maze[gy * dim + gx].difficulty > player_info->client->checkpoint_difficulty) {
                player_info->client->has_checkpoint = 1;
                player_info->client->checkpoint_difficulty = fa->maze->maze[gy * dim + gx].difficulty;
                player_info->client->checkpoint_x = flower_physical->x;
                player_info->client->checkpoint_y = flower_physical->y;
            }
        }
        if (player_info->client->in_squad) {
            for (uint64_t s = 0; s < player_info->slot_count; ++s) {
                if (player_info->slots[s].id == rr_petal_id_yggdrasil) {
                    struct rr_squad *sq = &player_info->client->server->squads[player_info->client->squad];
                    for (uint32_t i = 0; i < RR_SQUAD_MEMBER_COUNT; ++i) {
                        struct rr_server_client *mc = sq->members[i].client;
                        if (mc && mc != player_info->client) {
                            mc->has_ygg_teleport = 1;
                            mc->ygg_x = flower_physical->x;
                            mc->ygg_y = flower_physical->y;
                        }
                    }
                    break;
                }
            }
        }
    }"""

assert anchor in pb
pb = pb.replace(anchor, hook, 1)
with open("Server/System/PetalBehavior.c", "w", encoding="utf-8") as f:
    f.write(pb)
print("Чисто вставлено! Собираем всё...")
