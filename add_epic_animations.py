import re

# 1. RenderFlower.c: живое подмигивание левым глазом!
with open("Client/Renderer/RenderFlower.c", "r", encoding="utf-8") as f:
    rf = f.read()

eye_pattern = re.compile(
    r'(\s*rr_renderer_begin_path\(renderer\);\s*rr_renderer_ellipse\(renderer, -7, -5, 3\.25, 6\.5\);\s*rr_renderer_fill\(renderer\);)',
    re.DOTALL
)
m = eye_pattern.search(rf)
assert m, "Не найден левый глаз в RenderFlower.c"

wink_code = """
        static float wink_timer = 0.0f;
        wink_timer += 0.016f;
        if (wink_timer > 4.2f) wink_timer = 0.0f;
        int is_winking = (wink_timer > 3.85f);
        if (is_winking)
        {
            rr_renderer_set_stroke(renderer, 0xff222222);
            rr_renderer_set_line_width(renderer, 2.2f);
            rr_renderer_begin_path(renderer);
            rr_renderer_move_to(renderer, -10.5f, -4.0f);
            rr_renderer_quadratic_curve_to(renderer, -7.0f, -8.5f, -3.5f, -4.0f);
            rr_renderer_stroke(renderer);
        }
        else
        {
            rr_renderer_begin_path(renderer);
            rr_renderer_ellipse(renderer, -7, -5, 3.25, 6.5);
            rr_renderer_fill(renderer);
        }"""

if "is_winking" not in rf:
    rf = rf[:m.start()] + wink_code + rf[m.end():]
    rf = rf.replace(
        "rr_renderer_ellipse(renderer, -7, -5, 3, 6);",
        "if (!is_winking) rr_renderer_ellipse(renderer, -7, -5, 3, 6);", 1
    )
    rf = rf.replace(
        "rr_renderer_arc(renderer, -7 + flower->lerp_eye_x, -5 + flower->lerp_eye_y,\n\t\t\t\t\t3);",
        "if (!is_winking) rr_renderer_arc(renderer, -7 + flower->lerp_eye_x, -5 + flower->lerp_eye_y, 3);", 1
    )
    rf = rf.replace(
        "rr_renderer_arc(renderer, -7 + flower->lerp_eye_x, -5 + flower->lerp_eye_y,\n                    3);",
        "if (!is_winking) rr_renderer_arc(renderer, -7 + flower->lerp_eye_x, -5 + flower->lerp_eye_y, 3);", 1
    )
    with open("Client/Renderer/RenderFlower.c", "w", encoding="utf-8") as f:
        f.write(rf)

# 2. RenderPetal.c: светящийся энергетический ореол на редких лепестках (Mythic+) и вспышка удара
with open("Client/Renderer/RenderPetal.c", "r", encoding="utf-8") as f:
    rp = f.read()

petal_end = re.compile(r'(rr_renderer_draw_static_petal\(renderer, petal->id, petal->rarity,\s*use_cache\);\s*\})', re.DOTALL)
mp = petal_end.search(rp)
assert mp, "Не найден конец RenderPetal.c"

petal_fx = """rr_renderer_draw_static_petal(renderer, petal->id, petal->rarity, use_cache);
    if (petal->rarity >= rr_rarity_id_mythic)
    {
        rr_renderer_set_global_alpha(renderer, 0.35f);
        rr_renderer_set_stroke(renderer, RR_RARITY_COLORS[petal->rarity]);
        rr_renderer_set_line_width(renderer, 2.5f);
        rr_renderer_begin_path(renderer);
        rr_renderer_arc(renderer, 0, 0, 12.5f);
        rr_renderer_stroke(renderer);
    }
}"""

if "RR_RARITY_COLORS[petal->rarity]" not in rp:
    rp = rp[:mp.start()] + petal_fx + rp[mp.end():]
    with open("Client/Renderer/RenderPetal.c", "w", encoding="utf-8") as f:
        f.write(rp)

# 3. RenderMob.c: эпичная ударная волна и искры при попадании по мобу
with open("Client/Renderer/RenderMob.c", "r", encoding="utf-8") as f:
    rm = f.read()

mob_end = re.compile(r'(use_cache \| \(is_friendly << 1\) \| \(is_centi_body << 2\)\);\s*\})', re.DOTALL)
mm = mob_end.search(rm)
assert mm, "Не найден конец RenderMob.c"

mob_fx = """use_cache | (is_friendly << 1) | (is_centi_body << 2));
    if (health->damage_animation > 0.08f)
    {
        float dmg_a = health->damage_animation;
        float wave_r = 22.0f + (1.0f - dmg_a) * 28.0f;
        rr_renderer_set_global_alpha(renderer, dmg_a * 0.75f);
        rr_renderer_set_stroke(renderer, 0xffffa94d);
        rr_renderer_set_line_width(renderer, 3.0f * dmg_a + 1.0f);
        rr_renderer_begin_path(renderer);
        rr_renderer_arc(renderer, 0, 0, wave_r);
        rr_renderer_stroke(renderer);

        rr_renderer_set_stroke(renderer, 0xffffec99);
        rr_renderer_set_line_width(renderer, 2.5f);
        for (int s = 0; s < 6; ++s)
        {
            float ang = s * 1.047f + dmg_a * 3.0f;
            float r1 = 14.0f + (1.0f - dmg_a) * 16.0f;
            float r2 = r1 + 10.0f * dmg_a;
            rr_renderer_begin_path(renderer);
            rr_renderer_move_to(renderer, cosf(ang) * r1, sinf(ang) * r1);
            rr_renderer_line_to(renderer, cosf(ang) * r2, sinf(ang) * r2);
            rr_renderer_stroke(renderer);
        }
    }
}"""

if "wave_r" not in rm:
    rm = rm[:mm.start()] + mob_fx + rm[mm.end():]
    with open("Client/Renderer/RenderMob.c", "w", encoding="utf-8") as f:
        f.write(rm)

print("Все авторские анимации (подмигивание, ауры лепестков и искры ударов) добавлены!")
