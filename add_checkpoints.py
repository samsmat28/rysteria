import re

# 1. Server/Client.h
with open("Server/Client.h", "r", encoding="utf-8") as f:
    client_h = f.read()

pattern_client = re.compile(r'(struct rr_server_client\s*\{.*?)(\n\};)', re.DOTALL)
m_c = pattern_client.search(client_h)
assert m_c, "Не найдена структура rr_server_client в Server/Client.h"

if "has_checkpoint" not in client_h:
    extra_fields = "\n    uint8_t has_checkpoint;\n    uint8_t checkpoint_difficulty;\n    float checkpoint_x;\n    float checkpoint_y;"
    client_h = client_h[:m_c.end(1)] + extra_fields + client_h[m_c.start(2):]
    with open("Server/Client.h", "w", encoding="utf-8") as f:
        f.write(client_h)

# 2. Server/System/PetalBehavior.c
with open("Server/System/PetalBehavior.c", "r", encoding="utf-8") as f:
    pb = f.read()

pattern_pb = re.compile(
    r'(struct rr_component_player_info \*player_info =\s*rr_simulation_get_player_info\(simulation, id\);)'
)
m_pb = pattern_pb.search(pb)
assert m_pb, "Не найден блок player_info в Server/System/PetalBehavior.c"

checkpoint_logic = m_pb.group(1) + """
    if (player_info->client && rr_simulation_has_physical(simulation, player_info->flower))
    {
        struct rr_component_physical *fphys =
            rr_simulation_get_physical(simulation, player_info->flower);
        struct rr_component_arena *farena =
            rr_simulation_get_arena(simulation, fphys->arena);
        if (farena && farena->maze)
        {
            uint32_t gx = (uint32_t)(fphys->x / farena->maze->grid_size);
            uint32_t gy = (uint32_t)(fphys->y / farena->maze->grid_size);
            if (gx < farena->maze->width && gy < farena->maze->height)
            {
                struct rr_maze_grid *g =
                    &farena->maze->grid[gy * farena->maze->width + gx];
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

if "checkpoint_difficulty" not in pb:
    pb = pb[:m_pb.start()] + checkpoint_logic + pb[m_pb.end():]
    with open("Server/System/PetalBehavior.c", "w", encoding="utf-8") as f:
        f.write(pb)

# 3. Server/EntityAllocation.c
with open("Server/EntityAllocation.c", "r", encoding="utf-8") as f:
    ea = f.read()

pattern_ea = re.compile(
    r'([ \t]*rr_component_physical_set_x\(\s*physical, respawn_zone->x \+ 2 \* arena->maze->grid_size \* rr_frand\(\)\);\s*'
    r'rr_component_physical_set_y\(\s*physical, respawn_zone->y \+ 2 \* arena->maze->grid_size \* rr_frand\(\)\);)'
)
m_ea = pattern_ea.search(ea)
assert m_ea, "Не найден блок спавна цветка в Server/EntityAllocation.c"

replacement_ea = """    if (player_info->client && player_info->client->has_checkpoint)
    {
        rr_component_physical_set_x(physical, player_info->client->checkpoint_x);
        rr_component_physical_set_y(physical, player_info->client->checkpoint_y);
    }
    else
    {
        rr_component_physical_set_x(
            physical, respawn_zone->x + 2 * arena->maze->grid_size * rr_frand());
        rr_component_physical_set_y(
            physical, respawn_zone->y + 2 * arena->maze->grid_size * rr_frand());
    }"""

if "has_checkpoint" not in ea:
    ea = ea[:m_ea.start()] + replacement_ea + ea[m_ea.end():]
    with open("Server/EntityAllocation.c", "w", encoding="utf-8") as f:
        f.write(ea)

print("Готово! Автоматические чекпоинты прогрессии добавлены.")
