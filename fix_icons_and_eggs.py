import re

# 1. Поднимаем спавн Яиц и Королев в Server/Waves.c
with open("Server/Waves.c", "r") as f:
    w = f.read()

old_rates = """        if (r_ant < 0.78) return rr_mob_id_termite_worker;
        if (r_ant < 0.86) return rr_mob_id_termite_soldier;
        if (r_ant < 0.91) return rr_mob_id_worm;
        if (r_ant < 0.93) return rr_mob_id_ant_egg;
        if (r_ant < 0.95) return rr_mob_id_fire_ant_egg;
        if (r_ant < 0.97) return rr_mob_id_termite_egg;
        if (r_ant < 0.98) return rr_mob_id_queen_ant;
        if (r_ant < 0.99) return rr_mob_id_queen_fire_ant;
        return rr_mob_id_queen_termite;"""

new_rates = """        if (r_ant < 0.56) return rr_mob_id_termite_worker;
        if (r_ant < 0.66) return rr_mob_id_termite_soldier;
        if (r_ant < 0.74) return rr_mob_id_worm;
        if (r_ant < 0.80) return rr_mob_id_ant_egg;
        if (r_ant < 0.86) return rr_mob_id_fire_ant_egg;
        if (r_ant < 0.91) return rr_mob_id_termite_egg;
        if (r_ant < 0.94) return rr_mob_id_queen_ant;
        if (r_ant < 0.97) return rr_mob_id_queen_fire_ant;
        return rr_mob_id_queen_termite;"""

if old_rates in w:
    w = w.replace(old_rates, new_rates, 1)
    with open("Server/Waves.c", "w") as f:
        f.write(w)

# 2. Увеличиваем время вылупления яиц до 12 сек (300 тиков) в Server/System/_Ai.c
with open("Server/System/_Ai.c", "r") as f:
    ai = f.read()
ai = ai.replace("ai->ticks_until_next_action = 125;", "ai->ticks_until_next_action = 300;")
with open("Server/System/_Ai.c", "w") as f:
    f.write(ai)

# 3. Чиним иконки Grass, Rice, Clover, Light в Client/Assets/RenderPetals.c
with open("Client/Assets/RenderPetals.c", "r") as f:
    rp = f.read()

# Убираем старую вставку, если она попала не в ту функцию, и вставляем прямо в rr_renderer_draw_petal
rp = re.sub(
    r'        case rr_petal_id_grass:.*?case rr_petal_id_rock:',
    '        case rr_petal_id_rock:',
    rp,
    flags=re.DOTALL
)

draw_cases = """        case rr_petal_id_grass:
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

rp = rp.replace("        case rr_petal_id_rock:", draw_cases, 1)
with open("Client/Assets/RenderPetals.c", "w") as f:
    f.write(rp)

print("Иконки лепестков и спавн Яиц/Королев обновлены!")
