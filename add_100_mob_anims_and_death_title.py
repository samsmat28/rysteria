# 1. Client/Renderer/RenderFlower.c: эпичная надпись "FALLEN IN GLORY" и золотой нимб над головой после смерти
with open("Client/Renderer/RenderFlower.c", "r", encoding="utf-8") as f:
    rf = f.read()

dead_target = """\t\trr_renderer_stroke(renderer);
\t}"""
if dead_target not in rf:
    dead_target = """        rr_renderer_stroke(renderer);
    }"""

death_epic = """        rr_renderer_stroke(renderer);
        static float death_float = 0.0f;
        death_float += 0.04f;
        struct rr_renderer_context_state dstate;
        rr_renderer_context_state_init(renderer, &dstate);
        rr_renderer_rotate(renderer, -physical->lerp_angle);
        float bob = sinf(death_float) * 4.0f;

        // Восходящий золотой нимб
        rr_renderer_set_global_alpha(renderer, 0.85f);
        rr_renderer_set_stroke(renderer, 0xffffd43b);
        rr_renderer_set_line_width(renderer, 2.5f);
        rr_renderer_begin_path(renderer);
        rr_renderer_ellipse(renderer, 0, -34.0f + bob, 14.0f, 4.5f);
        rr_renderer_stroke(renderer);

        // Эпичная надпись над головой
        rr_renderer_set_fill(renderer, 0xffffd43b);
        rr_renderer_set_stroke(renderer, 0xff1a1a1a);
        rr_renderer_set_line_width(renderer, 4.0f);
        rr_renderer_set_text_size(renderer, 15);
        rr_renderer_set_text_align(renderer, 1);
        rr_renderer_set_text_baseline(renderer, 1);
        rr_renderer_stroke_text(renderer, "FALLEN IN GLORY", 0, -50.0f + bob);
        rr_renderer_fill_text(renderer, "FALLEN IN GLORY", 0, -50.0f + bob);
        rr_renderer_context_state_free(renderer, &dstate);
    }"""

assert dead_target in rf, "Не найден блок flower->dead в RenderFlower.c"
if "FALLEN IN GLORY" not in rf:
    rf = rf.replace(dead_target, death_epic, 1)
    with open("Client/Renderer/RenderFlower.c", "w", encoding="utf-8") as f:
        f.write(rf)

# 2. Client/Renderer/RenderMob.c: 100 уникальных анимаций для всех мобов (дыхание, ярость, руны, частицы шлейфа и взрыв при смерти)
with open("Client/Renderer/RenderMob.c", "r", encoding="utf-8") as f:
    rm = f.read()

breath_target = "rr_renderer_scale(renderer, RR_MOB_RARITY_SCALING[mob->rarity].radius);"
breath_code = breath_target + """
    int anim_style = (mob->id * 7 + mob->rarity * 13) % 100;
    float breath_speed = 1.0f + (float)(anim_style % 5) * 0.35f;
    float breath_amp = 0.025f + (float)((anim_style / 5) % 4) * 0.012f;
    float breath = 1.0f + sinf(physical->animation_timer * breath_speed + (float)entity) * breath_amp;
    rr_renderer_scale(renderer, breath);"""

assert breath_target in rm, "Не найден scale в RenderMob.c"
if "anim_style" not in rm:
    rm = rm.replace(breath_target, breath_code, 1)

end_target = """\t\t\trr_renderer_stroke(renderer);
\t\t}
\t}
}"""
if end_target not in rm:
    end_target = """            rr_renderer_stroke(renderer);
        }
    }"""

mob_100_anims = end_target + """

    // 100 вариаций боевых аур, частиц шлейфа, ярости и взрыва при гибели
    int m_style = (mob->id * 7 + mob->rarity * 13) % 100;
    uint32_t r_col = RR_RARITY_COLORS[mob->rarity];

    // 1) Аура ярости при низком HP (< 35%)
    if (!has_arena && health != NULL && health->health > 0 && health->health < health->max_health * 0.35f)
    {
        float rage = 0.5f + 0.5f * sinf(physical->animation_timer * 4.0f);
        rr_renderer_set_global_alpha(renderer, 0.35f + rage * 0.35f);
        rr_renderer_set_stroke(renderer, 0xffff3b30);
        rr_renderer_set_line_width(renderer, 2.5f + rage * 2.0f);
        rr_renderer_begin_path(renderer);
        rr_renderer_arc(renderer, 0, 0, 26.0f + rage * 8.0f);
        rr_renderer_stroke(renderer);
    }

    // 2) Орбитальные руны и кольца для редких мобов и боссов (Mythic+)
    if (mob->rarity >= rr_rarity_id_mythic)
    {
        int orbit_count = 2 + (m_style % 5);
        float orbit_r = 28.0f + (float)((m_style / 10) % 4) * 4.0f;
        float dir = (m_style % 2 == 0) ? 1.0f : -1.0f;
        rr_renderer_set_global_alpha(renderer, 0.55f);
        rr_renderer_set_fill(renderer, r_col);
        for (int o = 0; o < orbit_count; ++o)
        {
            float a = physical->animation_timer * dir + o * (6.28318f / (float)orbit_count);
            rr_renderer_begin_path(renderer);
            rr_renderer_arc(renderer, cosf(a) * orbit_r, sinf(a) * orbit_r, 3.0f);
            rr_renderer_fill(renderer);
        }
    }

    // 3) Частицы движения и магии в мире (по стилям 0..99)
    if (rr_frand() < 0.22f)
    {
        struct rr_simulation_animation *p = rr_particle_alloc(&game->default_particle_manager, rr_animation_type_default);
        if (p != NULL)
        {
            float ang = rr_frand() * 6.28318f;
            float dist = (10.0f + rr_frand() * 18.0f) * RR_MOB_RARITY_SCALING[mob->rarity].radius;
            rr_vector_from_polar(&p->velocity, (1.5f + (float)(m_style % 4)) * RR_MOB_RARITY_SCALING[mob->rarity].radius, ang);
            p->friction = 0.92f;
            p->x = physical->lerp_x + cosf(ang) * dist;
            p->y = physical->lerp_y + sinf(ang) * dist;
            p->size = (2.5f + (float)((m_style / 20) % 4)) * RR_MOB_RARITY_SCALING[mob->rarity].radius;
            p->opacity = 0.65f;
            p->disappearance = 5.0f;
            p->color = (m_style % 3 == 0) ? r_col : ((m_style % 3 == 1) ? 0xffffd43b : 0xff69db7c);
        }
    }

    // 4) Взрыв частиц в цвете редкости при смерти моба
    if (physical->deletion_animation > 0.05f && rr_frand() < 0.65f)
    {
        struct rr_simulation_animation *dp = rr_particle_alloc(&game->default_particle_manager, rr_animation_type_default);
        if (dp != NULL)
        {
            float ang = rr_frand() * 6.28318f;
            rr_vector_from_polar(&dp->velocity, (8.0f + rr_frand() * 10.0f) * RR_MOB_RARITY_SCALING[mob->rarity].radius, ang);
            dp->friction = 0.9f;
            dp->x = physical->lerp_x;
            dp->y = physical->lerp_y;
            dp->size = 5.0f * RR_MOB_RARITY_SCALING[mob->rarity].radius;
            dp->opacity = 0.9f;
            dp->disappearance = 6.0f;
            dp->color = r_col;
        }
    }
}"""

assert end_target in rm, "Не найден конец RenderMob.c"
if "m_style" not in rm:
    rm = rm.replace(end_target, mob_100_anims, 1)
    with open("Client/Renderer/RenderMob.c", "w", encoding="utf-8") as f:
        f.write(rm)

print("Эпичная надпись после смерти цветка и 100 анимаций мобов добавлены!")
