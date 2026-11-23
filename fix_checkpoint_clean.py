with open("Server/System/PetalBehavior.c", "r", encoding="utf-8") as f:
    pb = f.read()

target = """\tstruct rr_component_physical *flower_physical =
\t\trr_simulation_get_physical(simulation, player_info->flower_id);"""

if target not in pb:
    target = """    struct rr_component_physical *flower_physical =
        rr_simulation_get_physical(simulation, player_info->flower_id);"""

assert target in pb, "Не найдена строка flower_physical в PetalBehavior.c"

checkpoint_code = target + """
    if (player_info->client)
    {
        struct rr_component_arena *farena =
            rr_simulation_get_arena(simulation, flower_physical->arena);
        if (farena && farena->maze)
        {
            uint32_t dim = farena->maze->maze_dim;
            uint32_t gx = (uint32_t)(flower_physical->x / farena->maze->grid_size);
            uint32_t gy = (uint32_t)(flower_physical->y / farena->maze->grid_size);
            if (gx < dim && gy < dim)
            {
                struct rr_maze_grid *g = &farena->maze->maze[gy * dim + gx];
                if (g->difficulty > player_info->client->checkpoint_difficulty)
                {
                    player_info->client->has_checkpoint = 1;
                    player_info->client->checkpoint_difficulty = g->difficulty;
                    player_info->client->checkpoint_x = flower_physical->x;
                    player_info->client->checkpoint_y = flower_physical->y;
                }
            }
        }
    }"""

pb = pb.replace(target, checkpoint_code, 1)
with open("Server/System/PetalBehavior.c", "w", encoding="utf-8") as f:
    f.write(pb)

print("Чисто вставлено! Собираем сервер...")
