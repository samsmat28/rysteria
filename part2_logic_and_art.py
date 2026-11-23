import re

with open("Server/Client.h", "r", encoding="utf-8") as f:
    ch = f.read()
if "has_ygg_teleport" not in ch:
    ch = ch.replace("    float checkpoint_y;\n};", "    float checkpoint_y;\n    uint8_t has_ygg_teleport;\n    float ygg_x;\n    float ygg_y;\n};", 1)
    with open("Server/Client.h", "w", encoding="utf-8") as f:
        f.write(ch)

with open("Server/EntityAllocation.c", "r", encoding="utf-8") as f:
    ea = f.read()
if "has_ygg_teleport" not in ea:
    ea = ea.replace(
        "    if (player_info->client && player_info->client->has_checkpoint)",
        "    if (player_info->client && player_info->client->has_ygg_teleport)\n    {\n        rr_component_physical_set_x(physical, player_info->client->ygg_x);\n        rr_component_physical_set_y(physical, player_info->client->ygg_y);\n        player_info->client->has_ygg_teleport = 0;\n    }\n    else if (player_info->client && player_info->client->has_checkpoint)", 1
    )
    with open("Server/EntityAllocation.c", "w", encoding="utf-8") as f:
        f.write(ea)

with open("Server/System/PetalBehavior.c", "r", encoding="utf-8") as f:
    pb = f.read()
pb = re.sub(r'\n\s*if \(player_info->client\)\s*\{\s*struct rr_component_arena \*farena =.*?\n\s*\}\s*\n\s*\}\s*\n\s*\}', "", pb, count=1, flags=re.DOTALL)
anchor = "    petal_modifiers(simulation, player_info);"
if anchor not in pb:
    anchor = "\tpetal_modifiers(simulation, player_info);"
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
if "has_ygg_teleport" not in pb:
    pb = pb.replace(anchor, hook, 1)
    with open("Server/System/PetalBehavior.c", "w", encoding="utf-8") as f:
        f.write(pb)

with open("Client/Assets/RenderPetals.c", "r", encoding="utf-8") as f:
    rp = f.read()
art = """    case rr_petal_id_yucca:
        rr_renderer_set_fill(renderer, 0xff4ea832); rr_renderer_set_stroke(renderer, 0xff2d6b1a); rr_renderer_set_line_width(renderer, 2.5f);
        rr_renderer_begin_path(renderer); rr_renderer_move_to(renderer, -12, -4); rr_renderer_line_to(renderer, 0, 12); rr_renderer_line_to(renderer, 12, -4); rr_renderer_line_to(renderer, 4, 2); rr_renderer_line_to(renderer, 0, -14); rr_renderer_line_to(renderer, -4, 2); rr_renderer_fill(renderer); rr_renderer_stroke(renderer); break;
    case rr_petal_id_triangle:
        rr_renderer_set_fill(renderer, 0xffff922b); rr_renderer_set_stroke(renderer, 0xffb85800); rr_renderer_set_line_width(renderer, 3.0f);
        rr_renderer_begin_path(renderer); rr_renderer_move_to(renderer, 0, -13); rr_renderer_line_to(renderer, 12, 10); rr_renderer_line_to(renderer, -12, 10); rr_renderer_line_to(renderer, 0, -13); rr_renderer_fill(renderer); rr_renderer_stroke(renderer); break;
    case rr_petal_id_corn:
        rr_renderer_set_fill(renderer, 0xffffd43b); rr_renderer_set_stroke(renderer, 0xffc99a00); rr_renderer_set_line_width(renderer, 2.5f);
        rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, 0, -2, 8.5f); rr_renderer_fill(renderer); rr_renderer_stroke(renderer);
        rr_renderer_set_fill(renderer, 0xff51cf66); rr_renderer_begin_path(renderer); rr_renderer_move_to(renderer, -9, 2); rr_renderer_line_to(renderer, 0, 13); rr_renderer_line_to(renderer, 9, 2); rr_renderer_fill(renderer); break;
    case rr_petal_id_yggdrasil:
        rr_renderer_set_fill(renderer, 0xff20c997); rr_renderer_set_stroke(renderer, 0xff099268); rr_renderer_set_line_width(renderer, 2.5f);
        rr_renderer_begin_path(renderer); rr_renderer_move_to(renderer, 0, -14); rr_renderer_line_to(renderer, 10, 0); rr_renderer_line_to(renderer, 0, 14); rr_renderer_line_to(renderer, -10, 0); rr_renderer_line_to(renderer, 0, -14); rr_renderer_fill(renderer); rr_renderer_stroke(renderer);
        rr_renderer_set_stroke(renderer, 0xffffec99); rr_renderer_begin_path(renderer); rr_renderer_move_to(renderer, 0, 11); rr_renderer_line_to(renderer, 0, -9); rr_renderer_stroke(renderer); break;
    case rr_petal_id_rock:"""
if "rr_petal_id_yggdrasil" not in rp:
    rp = rp.replace("    case rr_petal_id_rock:", art, 1)
    with open("Client/Assets/RenderPetals.c", "w", encoding="utf-8") as f:
        f.write(rp)
print("Шаг 2 готов! Пересобираем...")
