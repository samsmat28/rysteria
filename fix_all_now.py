import re

# 1. Иконка Rice (изогнутая белая рисовинка как на скрине) в Client/Assets/RenderPetals.c
with open("Client/Assets/RenderPetals.c", "r") as f:
    rp = f.read()

old_rice = """    case rr_petal_id_rice:
        rr_renderer_set_fill(renderer, 0xfff7f5eb);
        rr_renderer_set_stroke(renderer, 0xffb8b29c);
        rr_renderer_set_line_width(renderer, 3.5f);
        rr_renderer_begin_path(renderer);
        rr_renderer_arc(renderer, 0, 0, 9);
        rr_renderer_fill(renderer);
        rr_renderer_stroke(renderer);
        break;"""

new_rice = """    case rr_petal_id_rice:
        rr_renderer_set_fill(renderer, 0xfff7f5eb);
        rr_renderer_set_stroke(renderer, 0xffcfcbc0);
        rr_renderer_set_line_width(renderer, 5.0f);
        rr_renderer_begin_path(renderer);
        rr_renderer_move_to(renderer, -8, -6);
        rr_renderer_line_to(renderer, 0, -2);
        rr_renderer_line_to(renderer, 8, 6);
        rr_renderer_line_to(renderer, 3, 10);
        rr_renderer_line_to(renderer, -4, 3);
        rr_renderer_line_to(renderer, -11, -1);
        rr_renderer_line_to(renderer, -8, -6);
        rr_renderer_fill(renderer);
        rr_renderer_stroke(renderer);
        break;"""

if old_rice in rp:
    rp = rp.replace(old_rice, new_rice, 1)
    with open("Client/Assets/RenderPetals.c", "w") as f:
        f.write(rp)
    print("Иконка Rice обновлена!")

# 2. Гарантируем, что в Shared/StaticData.c у всех 3 Королев минимальная редкость дропа = common (0)
with open("Shared/StaticData.c", "r") as f:
    c = f.read()

for q in ["rr_mob_id_queen_ant", "rr_mob_id_queen_fire_ant", "rr_mob_id_queen_termite"]:
    c = re.sub(
        r'(\{' + q + r',.*?)(rr_rarity_id_max|rr_rarity_id_common),\s*rr_rarity_id_common,\s*rr_rarity_id_max,\s*\{\{rr_petal_id_egg,\s*[0-9.]+\}\}',
        r'\1rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_egg, 1.0}}',
        c
    )

with open("Shared/StaticData.c", "w") as f:
    f.write(c)
print("Дроп Egg у Королев установлен на 100%!")
