with open("Server/System/PetalBehavior.c", "r", encoding="utf-8") as f:
    pb = f.read()

anchor = "\tpetal_modifiers(simulation, player_info);"
if anchor not in pb:
    anchor = "    petal_modifiers(simulation, player_info);"
assert anchor in pb, "Не найден anchor в PetalBehavior.c"

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
        if (player_info->squad_member && player_info->squad_member->squad_id != 0) {
            for (uint64_t s = 0; s < player_info->slot_count; ++s) {
                if (player_info->slots[s].id == rr_petal_id_yggdrasil) {
                    for (EntityIdx oid = 0; oid < simulation->entity_cap; ++oid) {
                        if (rr_simulation_has_player_info(simulation, oid)) {
                            struct rr_component_player_info *m = rr_simulation_get_player_info(simulation, oid);
                            if (m->client && m->client != player_info->client && m->squad_member && m->squad_member->squad_id == player_info->squad_member->squad_id) {
                                m->client->has_ygg_teleport = 1; m->client->ygg_x = flower_physical->x; m->client->ygg_y = flower_physical->y;
                            }
                        }
                    }
                    break;
                }
            }
        }
    }"""

pb = pb.replace(anchor, hook, 1)
with open("Server/System/PetalBehavior.c", "w", encoding="utf-8") as f:
    f.write(pb)
print("PetalBehavior.c чисто обновлен!")
