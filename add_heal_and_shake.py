import re

with open("Client/Renderer/RenderFlower.c", "r", encoding="utf-8") as f:
    rf = f.read()

pattern = re.compile(r'(\s*rr_renderer_context_state_free\(renderer, &state\);\s*\}\s*\}\s*\})\s*$')
m = pattern.search(rf)
assert m, "Не найден конец функции в RenderFlower.c"

fx_code = """
        rr_renderer_context_state_free(renderer, &state);
    }

    if (entity == game->player_info->flower_id && !flower->dead)
    {
        struct rr_component_health *hp = rr_simulation_get_health(simulation, entity);
        if (hp != NULL)
        {
            static float prev_hp = -1.0f;
            static float heal_anim = 0.0f;
            static float heal_tick = 0.0f;
            if (prev_hp > 0.0f && hp->hp > prev_hp + 0.05f)
                heal_anim = 1.0f;
            prev_hp = hp->hp;

            if (heal_anim > 0.01f)
            {
                heal_tick += 0.06f;
                float p = 1.0f - heal_anim;
                struct rr_renderer_context_state hstate;
                rr_renderer_context_state_init(renderer, &hstate);
                rr_renderer_rotate(renderer, -physical->lerp_angle);

                rr_renderer_set_global_alpha(renderer, heal_anim * 0.65f);
                rr_renderer_set_stroke(renderer, 0xff2ecc71);
                rr_renderer_set_line_width(renderer, 3.2f * heal_anim + 1.0f);
                rr_renderer_begin_path(renderer);
                rr_renderer_arc(renderer, 0, 0, 26.0f + p * 34.0f);
                rr_renderer_stroke(renderer);

                rr_renderer_set_global_alpha(renderer, heal_anim * 0.18f);
                rr_renderer_set_fill(renderer, 0xff51cf66);
                rr_renderer_begin_path(renderer);
                rr_renderer_arc(renderer, 0, 0, 28.0f + p * 12.0f);
                rr_renderer_fill(renderer);

                rr_renderer_set_global_alpha(renderer, heal_anim * 0.95f);
                rr_renderer_set_stroke(renderer, 0xff40c057);
                rr_renderer_set_line_width(renderer, 3.0f);
                float ox0 = -18.0f, ox1 = 0.0f, ox2 = 18.0f;
                float oy0 = -8.0f, oy1 = -18.0f, oy2 = -6.0f;
                float px0 = ox0 + sinf(heal_tick) * 3.0f, py0 = oy0 - p * 26.0f;
                float px1 = ox1 + sinf(heal_tick + 2.1f) * 3.0f, py1 = oy1 - p * 31.0f;
                float px2 = ox2 + sinf(heal_tick + 4.2f) * 3.0f, py2 = oy2 - p * 36.0f;

                rr_renderer_begin_path(renderer);
                rr_renderer_move_to(renderer, px0 - 4.5f, py0); rr_renderer_line_to(renderer, px0 + 4.5f, py0);
                rr_renderer_move_to(renderer, px0, py0 - 4.5f); rr_renderer_line_to(renderer, px0, py0 + 4.5f);
                rr_renderer_move_to(renderer, px1 - 4.5f, py1); rr_renderer_line_to(renderer, px1 + 4.5f, py1);
                rr_renderer_move_to(renderer, px1, py1 - 4.5f); rr_renderer_line_to(renderer, px1, py1 + 4.5f);
                rr_renderer_move_to(renderer, px2 - 4.5f, py2); rr_renderer_line_to(renderer, px2 + 4.5f, py2);
                rr_renderer_move_to(renderer, px2, py2 - 4.5f); rr_renderer_line_to(renderer, px2, py2 + 4.5f);
                rr_renderer_stroke(renderer);

                rr_renderer_context_state_free(renderer, &hstate);
                heal_anim -= 0.032f;
                if (heal_anim < 0.0f) heal_anim = 0.0f;
            }

            if (hp->damage_animation > 0.15f)
            {
                float shake = hp->damage_animation * 6.5f;
                rr_renderer_translate(renderer, sinf(hp->damage_animation * 47.0f) * shake, cosf(hp->damage_animation * 53.0f) * shake);
            }
        }
    }
}
"""

if "heal_anim" not in rf:
    rf = rf[:m.start()] + fx_code
    with open("Client/Renderer/RenderFlower.c", "w", encoding="utf-8") as f:
        f.write(rf)
print("Крутая анимация хила и динамичная тряска добавлены!")
