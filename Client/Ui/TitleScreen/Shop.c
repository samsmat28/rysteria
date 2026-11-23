#include <Client/Ui/Ui.h>
#include <emscripten.h>
#include <Client/Game.h>
#include <Client/InputData.h>
#include <Client/Renderer/Renderer.h>

static void shop_btn_ev(struct rr_ui_element *this, struct rr_game *g) {
    (void)this;
    if (g->input_data->mouse_buttons_up_this_tick & 1) {
        EM_ASM({ window.open('/shop.html', '_blank'); });
    }
}
static void shop_btn_rd(struct rr_ui_element *this, struct rr_game *g) {
    struct rr_renderer *r = g->renderer; rr_renderer_scale(r, r->scale);
    rr_renderer_set_fill(r, (g->focused == this) ? 0xffd98a1c : 0xffa66814);
    rr_renderer_set_stroke(r, 0xff6e4209); rr_renderer_set_line_width(r, 5);
    rr_renderer_begin_path(r); rr_renderer_round_rect(r, -this->width/2, -this->height/2, this->width, this->height, 8);
    rr_renderer_fill(r); rr_renderer_stroke(r);
    rr_renderer_set_text_baseline(r, 1); rr_renderer_set_text_align(r, 1); rr_renderer_set_text_size(r, 12);
    rr_renderer_set_fill(r, 0xffffffff); rr_renderer_fill_text(r, "SHOP", 0, -4);
    rr_renderer_set_fill(r, 0xffffe066); rr_renderer_fill_text(r, "WEB", 0, 14);
}
struct rr_ui_element *rr_ui_shop_toggle_button_init() {
    struct rr_ui_element *this = rr_ui_element_init();
    this->abs_width = this->abs_height = this->width = this->height = 60;
    this->on_event = shop_btn_ev; this->on_render = shop_btn_rd;
    return this;
}
struct rr_ui_element *rr_ui_quests_toggle_button_init() {
    struct rr_ui_element *this = rr_ui_element_init();
    this->completely_hidden = 1;
    return this;
}
struct rr_ui_element *rr_ui_shop_container_init(struct rr_game *g) {
    (void)g; struct rr_ui_element *this = rr_ui_element_init();
    this->completely_hidden = 1; return this;
}
struct rr_ui_element *rr_ui_quests_container_init(struct rr_game *g) {
    (void)g; struct rr_ui_element *this = rr_ui_element_init();
    this->completely_hidden = 1; return this;
}


#include <Shared/Utilities.h>

static double rr_save_toast_until = 0.0;

void rr_trigger_save_toast() {
    rr_save_toast_until = emscripten_get_now() + 2600.0; // Показываем 2.6 секунды с плавным затуханием
}

void rr_render_save_toast(struct rr_game *g) {
    if (!g || !g->renderer) return;
    double rem = rr_save_toast_until - emscripten_get_now();
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
}
