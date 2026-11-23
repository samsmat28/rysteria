LB, RB = chr(91), chr(93)

new_account_c = f"""#include <Client/Ui/Ui.h>
#include <emscripten.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <Client/Game.h>
#include <Client/InputData.h>
#include <Client/Renderer/Renderer.h>
#include <Client/Ui/Engine.h>

static char save_ui_msg{LB}96{RB} = "Auto-Save: ACTIVE (Browser + Server)";

static void acc_txt(struct rr_renderer *r, const char *t, float x, float y, float sz, uint32_t col) {{
    rr_renderer_set_text_baseline(r, 1); rr_renderer_set_text_align(r, 1); rr_renderer_set_text_size(r, sz);
    rr_renderer_set_fill(r, col); rr_renderer_set_stroke(r, 0xff111111); rr_renderer_set_line_width(r, sz * 0.14f);
    rr_renderer_stroke_text(r, t, x, y); rr_renderer_fill_text(r, t, x, y);
}}

static uint8_t acc_show(struct rr_ui_element *this, struct rr_game *g) {{
    (void)this;
    return g->menu_open == rr_game_menu_account;
}}

static void acc_anim(struct rr_ui_element *this, struct rr_game *g) {{
    (void)g;
    this->width = this->abs_width;
    this->height = this->abs_height;
}}

static void acc_btn_ev(struct rr_ui_element *this, struct rr_game *g) {{
    if (g->input_data->mouse_buttons_up_this_tick & 1) {{
        if (g->pressed != this) return;
        g->menu_open = (g->menu_open == rr_game_menu_account) ? rr_game_menu_none : rr_game_menu_account;
    }}
}}

static void acc_btn_rd(struct rr_ui_element *this, struct rr_game *g) {{
    struct rr_renderer *r = g->renderer;
    rr_renderer_scale(r, r->scale);
    rr_renderer_set_fill(r, (g->focused == this || g->menu_open == rr_game_menu_account) ? 0xff4fc3f7 : 0xff2980b9);
    rr_renderer_set_stroke(r, 0xff154360);
    rr_renderer_set_line_width(r, 4);
    rr_renderer_begin_path(r);
    rr_renderer_round_rect(r, -this->abs_width/2, -this->abs_height/2, this->abs_width, this->abs_height, 8);
    rr_renderer_fill(r); rr_renderer_stroke(r);
    acc_txt(r, "SAVE", 0, 0, 12, 0xffffffff);
}}

struct rr_ui_element *rr_ui_account_toggle_button_init() {{
    struct rr_ui_element *this = rr_ui_element_init();
    this->abs_width = this->abs_height = this->width = this->height = 44;
    this->on_event = acc_btn_ev;
    this->on_render = acc_btn_rd;
    return this;
}}

static void acc_win_ev(struct rr_ui_element *this, struct rr_game *g) {{
    if (!(g->input_data->mouse_buttons_up_this_tick & 1)) return;
    float mx = (g->input_data->touches{LB}0{RB}.touch_x - g->renderer->width / 2.0f) / g->renderer->scale - this->x;
    float my = (g->input_data->touches{LB}0{RB}.touch_y - g->renderer->height / 2.0f) / g->renderer->scale - this->y;
    (void)mx;
    if (my >= -45 && my <= 5) {{
        EM_ASM({{
            const key = localStorage.getItem('rr_save_id') || ('RR-' + Math.random().toString(36).slice(2, 10).toUpperCase());
            localStorage.setItem('rr_save_id', key);
            navigator.clipboard.writeText(key).catch(()=>{{}});
            alert('Ваш Код Сохранения скопирован: ' + key);
        }});
        snprintf(save_ui_msg, sizeof(save_ui_msg), "Save Code copied to clipboard!");
    }} else if (my >= 20 && my <= 70) {{
        EM_ASM({{
            const code = prompt('Вставьте ваш Код Сохранения (Save Code):');
            if (code && code.trim()) {{
                localStorage.setItem('rr_save_id', code.trim());
                location.reload();
            }}
        }});
    }}
}}

static void acc_win_rd(struct rr_ui_element *this, struct rr_game *g) {{
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

    rr_renderer_set_fill(r, 0xff2e8b57);
    rr_renderer_begin_path(r);
    rr_renderer_round_rect(r, -165, -45, 330, 48, 10);
    rr_renderer_fill(r);
    acc_txt(r, "COPY SAVE CODE", 0, -21, 16, 0xffffffff);

    rr_renderer_set_fill(r, 0xffd98a1c);
    rr_renderer_begin_path(r);
    rr_renderer_round_rect(r, -165, 20, 330, 48, 10);
    rr_renderer_fill(r);
    acc_txt(r, "LOAD BY SAVE CODE", 0, 44, 16, 0xffffffff);

    acc_txt(r, save_ui_msg, 0, 106, 13, 0xff7eef6d);
}}

struct rr_ui_element *rr_ui_account_container_init(struct rr_game *game) {{
    (void)game;
    struct rr_ui_element *this = rr_ui_element_init();
    this->abs_width = this->width = 420;
    this->abs_height = this->height = 280;
    this->animate = acc_anim;
    this->should_show = acc_show;
    this->on_event = acc_win_ev;
    this->on_render = acc_win_rd;
    return this;
}}
"""

with open("Client/Ui/TitleScreen/Account.c", "w", encoding="utf-8") as f:
    f.write(new_account_c)
print("[OK] Старый Account.c заменён на удобное окно SAVE & TRANSFER")
