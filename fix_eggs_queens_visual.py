# 1. Добавляем векторную отрисовку Яиц и Королев прямо в switch в Client/Assets/RenderMobs.c
with open("Client/Assets/RenderMobs.c", "r") as f:
    rm = f.read()

old_line = "    case rr_mob_id_worker_ant: case rr_mob_id_soldier_ant: case rr_mob_id_fire_worker_ant: case rr_mob_id_fire_soldier_ant: case rr_mob_id_termite_worker: case rr_mob_id_termite_soldier: case rr_mob_id_worm: render_sprite(renderer, id, 0, flags); break;"

new_cases = """    case rr_mob_id_worker_ant: case rr_mob_id_soldier_ant: case rr_mob_id_fire_worker_ant: case rr_mob_id_fire_soldier_ant: case rr_mob_id_termite_worker: case rr_mob_id_termite_soldier: case rr_mob_id_worm:
        render_sprite(renderer, id, 0, flags);
        break;
    case rr_mob_id_ant_egg:
    case rr_mob_id_fire_ant_egg:
    case rr_mob_id_termite_egg:
        rr_renderer_scale(renderer, 0.25f);
        rr_renderer_set_fill(renderer, id == rr_mob_id_ant_egg ? 0xfff5f0e1 : (id == rr_mob_id_fire_ant_egg ? 0xfff5a895 : 0xffe8d5b5));
        rr_renderer_set_stroke(renderer, id == rr_mob_id_ant_egg ? 0xffb8ae93 : (id == rr_mob_id_fire_ant_egg ? 0xffb84b32 : 0xff8c5828));
        rr_renderer_set_line_width(renderer, 12);
        rr_renderer_begin_path(renderer);
        rr_renderer_arc(renderer, -16.0f, 0.0f, 54.0f);
        rr_renderer_arc(renderer, 20.0f, 0.0f, 44.0f);
        rr_renderer_fill(renderer);
        rr_renderer_stroke(renderer);
        break;
    case rr_mob_id_queen_ant:
    case rr_mob_id_queen_fire_ant:
    case rr_mob_id_queen_termite:
    {
        uint8_t base_id = (id == rr_mob_id_queen_ant) ? rr_mob_id_soldier_ant : ((id == rr_mob_id_queen_fire_ant) ? rr_mob_id_fire_soldier_ant : rr_mob_id_termite_soldier);
        render_sprite(renderer, base_id, 0, flags);
        rr_renderer_scale(renderer, 0.25f);
        rr_renderer_set_fill(renderer, 0xffffd700);
        rr_renderer_set_stroke(renderer, 0xff9e7b00);
        rr_renderer_set_line_width(renderer, 6);
        rr_renderer_begin_path(renderer);
        rr_renderer_move_to(renderer, -22, -26);
        rr_renderer_line_to(renderer, 16, -34);
        rr_renderer_line_to(renderer, 4, -12);
        rr_renderer_line_to(renderer, 24, 0);
        rr_renderer_line_to(renderer, 4, 12);
        rr_renderer_line_to(renderer, 16, 34);
        rr_renderer_line_to(renderer, -22, 26);
        rr_renderer_line_to(renderer, -22, -26);
        rr_renderer_fill(renderer);
        rr_renderer_stroke(renderer);
        break;
    }"""

assert old_line in rm, "Не найдена строка в RenderMobs.c!"
rm = rm.replace(old_line, new_cases, 1)
with open("Client/Assets/RenderMobs.c", "w") as f:
    f.write(rm)

# 2. Поднимаем шанс спавна Королев в Server/Waves.c до ~20%
with open("Server/Waves.c", "r") as f:
    w = f.read()

old_w = """        if (r_ant < 0.91) return rr_mob_id_termite_egg;
        if (r_ant < 0.94) return rr_mob_id_queen_ant;
        if (r_ant < 0.97) return rr_mob_id_queen_fire_ant;
        return rr_mob_id_queen_termite;"""

new_w = """        if (r_ant < 0.80) return rr_mob_id_termite_egg;
        if (r_ant < 0.87) return rr_mob_id_queen_ant;
        if (r_ant < 0.94) return rr_mob_id_queen_fire_ant;
        return rr_mob_id_queen_termite;"""

if old_w in w:
    w = w.replace(old_w, new_w, 1)
    with open("Server/Waves.c", "w") as f:
        f.write(w)

print("Яйца, Королевы с золотой короной и их спавн готовы!")
