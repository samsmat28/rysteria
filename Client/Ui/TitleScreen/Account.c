#include <Client/Ui/Ui.h>
#include <emscripten.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <Client/Game.h>
#include <Client/InputData.h>
#include <Client/Renderer/Renderer.h>
#include <Client/Ui/Engine.h>

static char save_ui_msg[96] = "Auto-Save: ACTIVE (Browser + Server)";

static void acc_txt(struct rr_renderer *r, const char *t, float x, float y, float sz, uint32_t col) {
    rr_renderer_set_text_baseline(r, 1); rr_renderer_set_text_align(r, 1); rr_renderer_set_text_size(r, sz);
    rr_renderer_set_fill(r, col); rr_renderer_set_stroke(r, 0xff111111); rr_renderer_set_line_width(r, sz * 0.14f);
    rr_renderer_stroke_text(r, t, x, y); rr_renderer_fill_text(r, t, x, y);
}

static uint8_t acc_show(struct rr_ui_element *this, struct rr_game *g) {
    (void)this;
    return g->menu_open == rr_game_menu_account;
}

static void acc_anim(struct rr_ui_element *this, struct rr_game *g) {
    (void)g;
    this->width = this->abs_width;
    this->height = this->abs_height;
}

static void acc_btn_ev(struct rr_ui_element *this, struct rr_game *g) {
    if (g->input_data->mouse_buttons_up_this_tick & 1) {
        if (g->pressed != this) return;
        g->menu_open = (g->menu_open == rr_game_menu_account) ? rr_game_menu_none : rr_game_menu_account;
    }
}

static void acc_btn_rd(struct rr_ui_element *this, struct rr_game *g) {
    struct rr_renderer *r = g->renderer;
    rr_renderer_scale(r, r->scale);
    rr_renderer_set_fill(r, (g->focused == this || g->menu_open == rr_game_menu_account) ? 0xff4fc3f7 : 0xff2980b9);
    rr_renderer_set_stroke(r, 0xff154360);
    rr_renderer_set_line_width(r, 4);
    rr_renderer_begin_path(r);
    rr_renderer_round_rect(r, -this->abs_width/2, -this->abs_height/2, this->abs_width, this->abs_height, 8);
    rr_renderer_fill(r); rr_renderer_stroke(r);
    acc_txt(r, "SAVE", 0, 0, 12, 0xffffffff);
}

struct rr_ui_element *rr_ui_account_toggle_button_init() {
    struct rr_ui_element *this = rr_ui_element_init();
    this->abs_width = this->abs_height = this->width = this->height = 44;
    this->on_event = acc_btn_ev;
    this->on_render = acc_btn_rd;
    return this;
}

static void copy_btn_ev(struct rr_ui_element *this, struct rr_game *g) {
    if (g->input_data->mouse_buttons_up_this_tick & 1) {
        if (g->pressed != this) return;
        EM_ASM({
            const key = globalThis['localStorage'].getItem('rr_save_id') || ('RR-' + Math.random().toString(36).slice(2, 10).toUpperCase());
            globalThis['localStorage'].setItem('rr_save_id', key);
            globalThis['localStorage'].setItem('rivet_account_uuid', key);
            if (globalThis['navigator'] && globalThis['navigator']['clipboard']) {
                globalThis['navigator']['clipboard'].writeText(key).catch(()=>{});
            }
            globalThis['prompt']('Ваш Код Сохранения (Ctrl+C чтобы скопировать):', key);
        });
        snprintf(save_ui_msg, sizeof(save_ui_msg), "Save Code ready!");
    }
}

static void copy_btn_rd(struct rr_ui_element *this, struct rr_game *g) {
    struct rr_renderer *r = g->renderer;
    rr_renderer_scale(r, r->scale);
    rr_renderer_set_fill(r, (g->focused == this) ? 0xff3cb371 : 0xff2e8b57);
    rr_renderer_set_stroke(r, 0xff1b5e20);
    rr_renderer_set_line_width(r, 4);
    rr_renderer_begin_path(r);
    rr_renderer_round_rect(r, -this->abs_width/2, -this->abs_height/2, this->abs_width, this->abs_height, 10);
    rr_renderer_fill(r); rr_renderer_stroke(r);
    acc_txt(r, "COPY SAVE CODE", 0, 0, 16, 0xffffffff);
}

static void load_btn_ev(struct rr_ui_element *this, struct rr_game *g) {
    if (g->input_data->mouse_buttons_up_this_tick & 1) {
        if (g->pressed != this) return;
        EM_ASM({
            const code = globalThis['prompt']('Вставьте ваш Код Сохранения (Save Code):');
            if (code && code.trim()) {
                const clean = code.trim();
                globalThis['localStorage'].setItem('rr_save_id', clean);
                globalThis['localStorage'].setItem('rivet_account_uuid', clean);
                globalThis['location'].reload();
            }
        });
    }
}

static void load_btn_rd(struct rr_ui_element *this, struct rr_game *g) {
    struct rr_renderer *r = g->renderer;
    rr_renderer_scale(r, r->scale);
    rr_renderer_set_fill(r, (g->focused == this) ? 0xfff39c12 : 0xffd98a1c);
    rr_renderer_set_stroke(r, 0xff8e5b0e);
    rr_renderer_set_line_width(r, 4);
    rr_renderer_begin_path(r);
    rr_renderer_round_rect(r, -this->abs_width/2, -this->abs_height/2, this->abs_width, this->abs_height, 10);
    rr_renderer_fill(r); rr_renderer_stroke(r);
    acc_txt(r, "LOAD BY SAVE CODE", 0, 0, 16, 0xffffffff);
}

static void acc_win_rd(struct rr_ui_element *this, struct rr_game *g) {
    (void)this;
    struct rr_renderer *r = g->renderer;
    rr_renderer_scale(r, r->scale);

    rr_renderer_set_fill(r, 0xee101e2b);
    rr_renderer_set_stroke(r, 0xff4fc3f7);
    rr_renderer_set_line_width(r, 5);
    rr_renderer_begin_path(r);
    rr_renderer_round_rect(r, -210, -140, 420, 280, 14);
    rr_renderer_fill(r); rr_renderer_stroke(r);

    acc_txt(r, "PROGRESS SAVE & TRANSFER", 0, -112, 20, 0xff4fc3f7);
    acc_txt(r, "Progress saves automatically every action", 0, -78, 13, 0xffb3e5fc);
    acc_txt(r, save_ui_msg, 0, 106, 13, 0xff7eef6d);
}

struct rr_ui_element *rr_ui_account_container_init(struct rr_game *game) {
    (void)game;
    struct rr_ui_element *this = rr_ui_element_init();
    this->abs_width = this->width = 420;
    this->abs_height = this->height = 280;
    this->animate = acc_anim;
    this->should_show = acc_show;
    this->on_render = acc_win_rd;

    struct rr_ui_element *copy_btn = rr_ui_element_init();
    copy_btn->abs_width = copy_btn->width = 330;
    copy_btn->abs_height = copy_btn->height = 48;
    copy_btn->y = -21;
    copy_btn->animate = acc_anim;
    copy_btn->on_event = copy_btn_ev;
    copy_btn->on_render = copy_btn_rd;
    rr_ui_element_add_child(this, copy_btn);

    struct rr_ui_element *load_btn = rr_ui_element_init();
    load_btn->abs_width = load_btn->width = 330;
    load_btn->abs_height = load_btn->height = 48;
    load_btn->y = 44;
    load_btn->animate = acc_anim;
    load_btn->on_event = load_btn_ev;
    load_btn->on_render = load_btn_rd;
    rr_ui_element_add_child(this, load_btn);

    return this;
}
