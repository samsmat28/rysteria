LB, RB = chr(91), chr(93)

# 1. Добавляем рендер эффектного индикатора сохранения в Client/Ui/TitleScreen/Shop.c
with open("Client/Ui/TitleScreen/Shop.c", "r", encoding="utf-8") as f:
    sc = f.read()

badge_code = f"""
#include <Shared/Utilities.h>

static double rr_save_toast_until = 0.0;

void rr_trigger_save_toast() {{
    rr_save_toast_until = rr_get_time() + 2600.0; // Показываем 2.6 секунды с плавным затуханием
}}

void rr_render_save_toast(struct rr_game *g) {{
    if (!g || !g->renderer) return;
    double rem = rr_save_toast_until - rr_get_time();
    if (rem <= 0.0) return;

    float alpha = (rem > 2300.0) ? (float)((2600.0 - rem) / 300.0) : ((rem < 500.0) ? (float)(rem / 500.0) : 1.0f);
    if (alpha < 0.0f) alpha = 0.0f;
    if (alpha > 1.0f) alpha = 1.0f;
    uint32_t a_bg = ((uint32_t)(alpha * 225.0f)) << 24;
    uint32_t a_fg = ((uint32_t)(alpha * 255.0f)) << 24;

    struct rr_renderer *r = g->renderer;
    rr_renderer_save(r);
    rr_renderer_scale(r, r->scale);

    float w = r->width / r->scale;
    float bx = w - 215.0f;
    float by = 18.0f - (1.0f - alpha) * 12.0f;

    rr_renderer_set_fill(r, a_bg | 0x00132618);
    rr_renderer_set_stroke(r, a_fg | 0x007eef6d);
    rr_renderer_set_line_width(r, 3.0f);
    rr_renderer_begin_path(r);
    rr_renderer_round_rect(r, bx, by, 196.0f, 36.0f, 10.0f);
    rr_renderer_fill(r);
    rr_renderer_stroke(r);

    // Зелёный индикатор-огонёк
    rr_renderer_set_fill(r, a_fg | 0x007eef6d);
    rr_renderer_begin_path(r);
    rr_renderer_arc(r, bx + 20.0f, by + 18.0f, 6.0f);
    rr_renderer_fill(r);

    rr_renderer_set_text_baseline(r, 1);
    rr_renderer_set_text_align(r, 0);
    rr_renderer_set_text_size(r, 14.0f);
    rr_renderer_set_fill(r, a_fg | 0x00eaffdf);
    rr_renderer_fill_text(r, "AUTO-SAVED", bx + 34.0f, by + 18.0f);
    rr_renderer_restore(r);
}}
"""

if "rr_trigger_save_toast" not in sc:
    sc += "\n" + badge_code
    with open("Client/Ui/TitleScreen/Shop.c", "w", encoding="utf-8") as f:
        f.write(sc)

# 2. Подключаем вызов rr_trigger_save_toast() при получении rr_clientbound_account_result и отрисовку в Client/Game.c
with open("Client/Game.c", "r", encoding="utf-8") as f:
    gc = f.read()

if "extern void rr_trigger_save_toast" not in gc:
    gc = "extern void rr_trigger_save_toast();\nextern void rr_render_save_toast(struct rr_game *g);\n" + gc

gc = gc.replace(
    "case rr_clientbound_account_result:\n        {",
    "case rr_clientbound_account_result:\n        {\n            rr_trigger_save_toast();"
)
gc = gc.replace(
    "rr_ui_engine_render(&this->ui_engine, this);",
    "rr_ui_engine_render(&this->ui_engine, this);\n    rr_render_save_toast(this);"
)

with open("Client/Game.c", "w", encoding="utf-8") as f:
    f.write(gc)

print("[OK] Эффектный индикатор AUTO-SAVED добавлен в клиент")
