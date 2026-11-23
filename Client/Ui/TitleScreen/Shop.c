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
