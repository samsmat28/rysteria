import re

with open("Server/System/Checkpoints.c", "r", encoding="utf-8") as f:
    cp = f.read()

pattern = re.compile(r'(\s*uint32_t grid_y = rr_fclamp\(physical->y / arena->maze->grid_size,\s*0, arena->maze->maze_dim - 1\);)')
m = pattern.search(cp)
assert m, "Не найдена строка grid_y в Checkpoints.c"

hook = m.group(1) + """
    struct rr_maze_grid *cur_g = &arena->maze->maze[grid_y * arena->maze->maze_dim + grid_x];
    if (cur_g->difficulty > player_info->client->checkpoint_difficulty)
    {
        player_info->client->has_checkpoint = 1;
        player_info->client->checkpoint_difficulty = cur_g->difficulty;
        player_info->client->checkpoint_x = physical->x;
        player_info->client->checkpoint_y = physical->y;
        if (this->animation_length < 256)
        {
            struct rr_simulation_animation *anim = &this->animations[this->animation_length++];
            memset(anim, 0, sizeof(*anim));
            anim->type = rr_animation_type_chat;
            strcpy(anim->name, "[Checkpoint]");
            strcpy(anim->message, "New zone progress saved!");
        }
    }"""

if "checkpoint_difficulty" not in cp:
    cp = "#include <string.h>\n" + cp[:m.start()] + hook + cp[m.end():]
    with open("Server/System/Checkpoints.c", "w", encoding="utf-8") as f:
        f.write(cp)
print("Чекпоинты встроены в Server/System/Checkpoints.c!")
