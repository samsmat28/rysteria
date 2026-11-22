# 1. Добавляем Яйца и Королев в спавн Ant Hell (Server/Waves.c)
with open("Server/Waves.c", "r") as f:
    w = f.read()

old_spawn = """        if (r_ant < 0.84) return rr_mob_id_termite_worker;
        if (r_ant < 0.94) return rr_mob_id_termite_soldier;
        return rr_mob_id_worm;"""

new_spawn = """        if (r_ant < 0.56) return rr_mob_id_termite_worker;
        if (r_ant < 0.66) return rr_mob_id_termite_soldier;
        if (r_ant < 0.74) return rr_mob_id_worm;
        if (r_ant < 0.80) return rr_mob_id_ant_egg;
        if (r_ant < 0.86) return rr_mob_id_fire_ant_egg;
        if (r_ant < 0.91) return rr_mob_id_termite_egg;
        if (r_ant < 0.94) return rr_mob_id_queen_ant;
        if (r_ant < 0.97) return rr_mob_id_queen_fire_ant;
        return rr_mob_id_queen_termite;"""

assert old_spawn in w, "Не найден блок спавна в Waves.c!"
w = w.replace(old_spawn, new_spawn, 1)
with open("Server/Waves.c", "w") as f:
    f.write(w)

# 2. Добавляем иконки Grass, Rice, Clover, Light в Client/Assets/RenderPetals.c (отступ 4 пробела)
with open("Client/Assets/RenderPetals.c", "r") as f:
    rp = f.read()

icons = """    case rr_petal_id_grass:
        rr_renderer_set_fill(renderer, 0xff49b83d);
        rr_renderer_set_stroke(renderer, 0xff2c7a24);
        rr_renderer_set_line_width(renderer, 3.5f);
        rr_renderer_begin_path(renderer);
        rr_renderer_move_to(renderer, -14, 10);
        rr_renderer_line_to(renderer, 0, -16);
        rr_renderer_line_to(renderer, 14, 10);
        rr_renderer_line_to(renderer, 0, 4);
        rr_renderer_line_to(renderer, -14, 10);
        rr_renderer_fill(renderer);
        rr_renderer_stroke(renderer);
        break;

    case rr_petal_id_rice:
        rr_renderer_set_fill(renderer, 0xfff7f5eb);
        rr_renderer_set_stroke(renderer, 0xffb8b29c);
        rr_renderer_set_line_width(renderer, 3.5f);
        rr_renderer_begin_path(renderer);
        rr_renderer_arc(renderer, 0, 0, 9);
        rr_renderer_fill(renderer);
        rr_renderer_stroke(renderer);
        break;

    case rr_petal_id_clover:
        rr_renderer_set_fill(renderer, 0xff38c948);
        rr_renderer_set_stroke(renderer, 0xff1e8229);
        rr_renderer_set_line_width(renderer, 3.0f);
        rr_renderer_begin_path(renderer);
        rr_renderer_arc(renderer, -7, -7, 7.5f);
        rr_renderer_arc(renderer, 7, -7, 7.5f);
        rr_renderer_arc(renderer, -7, 7, 7.5f);
        rr_renderer_arc(renderer, 7, 7, 7.5f);
        rr_renderer_fill(renderer);
        rr_renderer_stroke(renderer);
        break;

    case rr_petal_id_light:
        rr_renderer_set_fill(renderer, 0xfffff8c9);
        rr_renderer_set_stroke(renderer, 0xffd9ca77);
        rr_renderer_set_line_width(renderer, 3.0f);
        rr_renderer_begin_path(renderer);
        rr_renderer_arc(renderer, 0, 0, 9.5f);
        rr_renderer_fill(renderer);
        rr_renderer_stroke(renderer);
        break;

    case rr_petal_id_rock:"""

assert "    case rr_petal_id_rock:" in rp, "Не найден case rr_petal_id_rock в RenderPetals.c!"
rp = rp.replace("    case rr_petal_id_rock:", icons, 1)
with open("Client/Assets/RenderPetals.c", "w") as f:
    f.write(rp)

print("Готово! Иконки и спавн Яиц/Королев добавлены!")
