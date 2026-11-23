import re

with open("Server/System/PetalBehavior.c", "r", encoding="utf-8") as f:
    pb = f.read()

pattern = re.compile(
    r'\n\s*if \(player_info->client && rr_simulation_has_physical\(simulation, player_info->flower\)\).*?\n\s*\}\s*\n\s*\}\s*\n\s*\}',
    re.DOTALL
)

replacement = """
    if (player_info->client && rr_simulation_has_physical(simulation, player_info->flower_id))
    {
        struct rr_component_physical *fphys =
            rr_simulation_get_physical(simulation, player_info->flower_id);
        struct rr_component_arena *farena =
            rr_simulation_get_arena(simulation, fphys->arena);
        if (farena && farena->maze)
        {
            uint32_t dim = farena->maze->maze_dim;
            uint32_t gx = (uint32_t)(fphys->x / farena->maze->grid_size);
            uint32_t gy = (uint32_t)(fphys->y / farena->maze->grid_size);
            if (gx < dim && gy < dim)
            {
                struct rr_maze_grid *g = &farena->maze->maze[gy * dim + gx];
                if (g->difficulty > player_info->client->checkpoint_difficulty)
                {
                    player_info->client->has_checkpoint = 1;
                    player_info->client->checkpoint_difficulty = g->difficulty;
                    player_info->client->checkpoint_x = fphys->x;
                    player_info->client->checkpoint_y = fphys->y;
                }
            }
        }
    }"""

pb_new, count = pattern.subn(replacement, pb, count=1)
assert count == 1, "Не удалось заменить старый блок чекпоинта в PetalBehavior.c"

with open("Server/System/PetalBehavior.c", "w", encoding="utf-8") as f:
    f.write(pb_new)

print("Исправлено! Собираем сервер...")
