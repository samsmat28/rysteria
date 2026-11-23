import re

with open("Client/Renderer/RenderFlower.c", "r", encoding="utf-8") as f:
    rf = f.read()

pattern = re.compile(r'if \(entity == game->player_info->flower_id && !flower->dead\).*?\n\}\s*$', re.DOTALL)
m = pattern.search(rf)
assert m, "Не найден блок анимации в RenderFlower.c"

new_fx = """if (entity == game->player_info->flower_id && !flower->dead)
    {
        struct rr_component_health *hp = rr_simulation_get_health(simulation, entity);
        if (hp != NULL)
        {
            static float prev_hp = -1.0f;
            static float heal_anim = 0.0f;
            static float heal_tick = 0.0f;
            static float pulse_timer = 0.0f;
            pulse_timer += 0.03f;

            if (prev_hp > 0.0f && hp->health > prev_hp + 0.01f)
                heal_anim = 1.0f;
            else if (hp->health < hp->max_health && pulse_timer > 1.0f)
            {
                heal_anim = 1.0f;
                pulse_timer = 0.0f;
            }
            prev_hp = hp->health;

            if (heal_anim > 0.01f)
            {
                heal_tick += 0.08f;
                float p = 1.0f - heal_anim;
                struct rr_renderer_context_state hstate;
                rr_renderer_context_state_init(renderer, &hstate);
                rr_renderer_rotate(renderer, -physical->lerp_angle);

                rr_renderer_set_global_alpha(renderer, heal_anim * 0.85f);
                rr_renderer_set_stroke(renderer, 0xff2ecc71);
                rr_renderer_set_line_width(renderer, 4.5f * heal_anim + 1.5f);
                rr_renderer_begin_path(renderer);
                rr_renderer_arc(renderer, 0, 0, 28.0f + p * 46.0f);
                rr_renderer_stroke(renderer);

                rr_renderer_set_global_alpha(renderer, heal_anim * 0.28f);
                rr_renderer_set_fill(renderer, 0xff51cf66);
                rr_renderer_begin_path(renderer);
                rr_renderer_arc(renderer, 0, 0, 32.0f + p * 18.0f);
                rr_renderer_fill(renderer);

                rr_renderer_set_global_alpha(renderer, heal_anim);
                rr_renderer_set_stroke(renderer, 0xff2b8a3e);
                rr_renderer_set_line_width(renderer, 4.0f);
                float px0 = -22.0f + sinf(heal_tick) * 4.0f, py0 = -10.0f - p * 34.0f;
                float px1 = 0.0f + sinf(heal_tick + 2.1f) * 4.0f, py1 = -22.0f - p * 40.0f;
                float px2 = 22.0f + sinf(heal_tick + 4.2f) * 4.0f, py2 = -8.0f - p * 36.0f;

                rr_renderer_begin_path(renderer);
                rr_renderer_move_to(renderer, px0 - 6.0f, py0); rr_renderer_line_to(renderer, px0 + 6.0f, py0);
                rr_renderer_move_to(renderer, px0, py0 - 6.0f); rr_renderer_line_to(renderer, px0, py0 + 6.0f);
                rr_renderer_move_to(renderer, px1 - 6.0f, py1); rr_renderer_line_to(renderer, px1 + 6.0f, py1);
                rr_renderer_move_to(renderer, px1, py1 - 6.0f); rr_renderer_line_to(renderer, px1, py1 + 6.0f);
                rr_renderer_move_to(renderer, px2 - 6.0f, py2); rr_renderer_line_to(renderer, px2 + 6.0f, py2);
                rr_renderer_move_to(renderer, px2, py2 - 6.0f); rr_renderer_line_to(renderer, px2, py2 + 6.0f);
                rr_renderer_stroke(renderer);

                rr_renderer_context_state_free(renderer, &hstate);
                heal_anim -= 0.022f;
                if (heal_anim < 0.0f) heal_anim = 0.0f;
            }

            if (hp->damage_animation > 0.05f)
            {
                float shake = hp->damage_animation * 10.0f;
                rr_renderer_translate(renderer, sinf(hp->damage_animation * 47.0f) * shake, cosf(hp->damage_animation * 53.0f) * shake);
            }
        }
    }
}
"""

rf = rf[:m.start()] + new_fx
with open("Client/Renderer/RenderFlower.c", "w", encoding="utf-8") as f:
    f.write(rf)
print("Яркая анимация хила и усиленная тряска готовы!")
