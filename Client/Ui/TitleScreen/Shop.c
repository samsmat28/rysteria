#include <Client/Ui/Ui.h>
#include <Client/Ui/Engine.h>
#include <emscripten.h>
#include <Client/Game.h>
#include <Client/InputData.h>
#include <Client/Renderer/Renderer.h>

static void stxt(struct rr_renderer *r, const char *t, float x, float y, float sz, uint32_t col, int align) {
    rr_renderer_set_text_baseline(r, 1); rr_renderer_set_text_align(r, align); rr_renderer_set_text_size(r, sz);
    rr_renderer_set_fill(r, col);
    rr_renderer_fill_text(r, t, x, y);
}

static void shop_btn_ev(struct rr_ui_element *this, struct rr_game *g) {
    if (g->input_data->mouse_buttons_up_this_tick & 1) {
        if (g->pressed != this) return;
        EM_ASM({ window.open('/shop.html', '_blank'); });
    }
}

static void shop_btn_rd(struct rr_ui_element *this, struct rr_game *g) {
    struct rr_renderer *r = g->renderer; rr_renderer_scale(r, r->scale);
    rr_renderer_set_fill(r, (g->focused == this) ? 0xfff39c12 : 0xffd98a1c);
    rr_renderer_set_stroke(r, 0xff6e4209); rr_renderer_set_line_width(r, 4);
    rr_renderer_begin_path(r);
    rr_renderer_round_rect(r, -this->abs_width/2, -this->abs_height/2, this->abs_width, this->abs_height, 8);
    rr_renderer_fill(r); rr_renderer_stroke(r);
    stxt(r, "SHOP", 0, -5, 11, 0xffffffff, 1); stxt(r, "& QUEST", 0, 8, 9, 0xffffe066, 1);
}

struct rr_ui_element *rr_ui_shop_toggle_button_init() {
    struct rr_ui_element *this = rr_ui_element_init();
    this->abs_width = this->abs_height = this->width = this->height = 52;
    this->on_event = shop_btn_ev; this->on_render = shop_btn_rd; return this;
}
struct rr_ui_element *rr_ui_quests_toggle_button_init() {
    struct rr_ui_element *this = rr_ui_element_init(); this->completely_hidden = 1; return this;
}
struct rr_ui_element *rr_ui_quests_container_init(struct rr_game *g) {
    (void)g; struct rr_ui_element *this = rr_ui_element_init(); this->completely_hidden = 1; return this;
}
struct rr_ui_element *rr_ui_shop_container_init(struct rr_game *g) {
    (void)g; struct rr_ui_element *this = rr_ui_element_init(); this->completely_hidden = 1; return this;
}
static double rr_save_toast_until = 0.0;
void rr_trigger_save_toast() { rr_save_toast_until = emscripten_get_now() + 2600.0; }
void rr_render_save_toast(struct rr_game *g) {
    if (!g || !g->renderer) return; double rem = rr_save_toast_until - emscripten_get_now(); if (rem <= 0.0) return;
    float alpha = (rem > 2300.0) ? (float)((2600.0 - rem) / 300.0) : ((rem < 500.0) ? (float)(rem / 500.0) : 1.0f);
    if (alpha < 0.0f) alpha = 0.0f; if (alpha > 1.0f) alpha = 1.0f;
    uint32_t a_bg = ((uint32_t)(alpha * 225.0f)) << 24, a_fg = ((uint32_t)(alpha * 255.0f)) << 24;
    struct rr_renderer *r = g->renderer; rr_renderer_save(r); rr_renderer_scale(r, r->scale);
    float w = r->width / r->scale, bx = w - 215.0f, by = 18.0f - (1.0f - alpha) * 12.0f;
    rr_renderer_set_fill(r, 0x00132418 | a_bg); rr_renderer_set_stroke(r, 0x002ecc71 | a_fg); rr_renderer_set_line_width(r, 2.5f);
    rr_renderer_begin_path(r); rr_renderer_round_rect(r, bx, by, 195.0f, 34.0f, 8.0f); rr_renderer_fill(r); rr_renderer_stroke(r);
    stxt(r, "PROGRESS SAVED", bx + 97.5f, by + 17.0f, 12.0f, 0x007eef6d | a_fg, 1);
    rr_renderer_restore(r);
}
