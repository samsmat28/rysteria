import re

with open("Client/InputData.h", "r", encoding="utf-8") as f:
    idh = f.read()

LB, RB = chr(91), chr(93)
if "mouse_x" in idh:
    mx_expr, my_expr = "g->input_data->mouse_x", "g->input_data->mouse_y"
else:
    mx_expr, my_expr = f"g->input_data->touches{LB}0{RB}.touch_x", f"g->input_data->touches{LB}0{RB}.touch_y"

win_code = f"""
static uint8_t shop_show(struct rr_ui_element *this, struct rr_game *g) {{ (void)this; return g->menu_open == rr_game_menu_shop; }}
static void shop_anim(struct rr_ui_element *this, struct rr_game *g) {{ (void)g; this->width = this->abs_width; this->height = this->abs_height; }}

static void shop_ev(struct rr_ui_element *this, struct rr_game *g) {{
    if (!(g->input_data->mouse_buttons_up_this_tick & 1)) return;
    float mx = ({mx_expr} - g->renderer->width / 2.0f) / g->renderer->scale - this->x;
    float my = ({my_expr} - g->renderer->height / 2.0f) / g->renderer->scale - this->y;
    if (my >= -145 && my <= -105) shop_tab = (mx < 0) ? 0 : 1;
    if (my >= -75 && my <= -35) {{ shop_petal += (mx < 0 ? -1 : 1); if (shop_petal < 1) shop_petal = rr_petal_id_max - 1; if (shop_petal >= rr_petal_id_max) shop_petal = 1; }}
    if (my >= -15 && my <= 25) {{ int m = (shop_tab == 0 ? 3 : 0); shop_rarity += (mx < 0 ? -1 : 1); if (shop_rarity < m) shop_rarity = rr_rarity_id_max - 1; if (shop_rarity >= rr_rarity_id_max) shop_rarity = m; }}
    if (my >= 50 && my <= 105) {{
        char cmd{LB}48{RB};
        if (shop_tab == 0) {{ if (shop_rarity < 3) shop_rarity = 3; snprintf(cmd, sizeof(cmd), "/buy %d %d", shop_petal, shop_rarity); }}
        else snprintf(cmd, sizeof(cmd), "/sell %d %d", shop_petal, shop_rarity);
        rr_shop_send_chat(g, cmd);
    }}
}}

static void shop_rd(struct rr_ui_element *this, struct rr_game *g) {{
    (void)this; struct rr_renderer *r = g->renderer; rr_renderer_scale(r, r->scale);
    rr_renderer_set_fill(r, 0xee291b0e); rr_renderer_set_stroke(r, 0xfff5c542); rr_renderer_set_line_width(r, 6);
    rr_renderer_begin_path(r); rr_renderer_round_rect(r, -230, -180, 460, 360, 14); rr_renderer_fill(r); rr_renderer_stroke(r);
    rr_shop_text(r, "RYSTERIA SHOP [R]", 0, -158, 22, 0xffffd700);

    rr_renderer_set_fill(r, shop_tab == 0 ? 0xff8b5a2b : 0xff3b2613);
    rr_renderer_begin_path(r); rr_renderer_round_rect(r, -200, -140, 190, 34, 8); rr_renderer_fill(r);
    rr_shop_text(r, "BUY RARE", -105, -123, 15, 0xffffffff);

    rr_renderer_set_fill(r, shop_tab == 1 ? 0xff8b5a2b : 0xff3b2613);
    rr_renderer_begin_path(r); rr_renderer_round_rect(r, 10, -140, 190, 34, 8); rr_renderer_fill(r);
    rr_shop_text(r, "SELL PETAL", 105, -123, 15, 0xffffffff);

    if (shop_tab == 0 && shop_rarity < 3) shop_rarity = 3;
    char pl{LB}64{RB}, rl{LB}64{RB}, al{LB}64{RB};
    snprintf(pl, sizeof(pl), "<  #%d %s  >", shop_petal, RR_PETAL_NAMES{LB}shop_petal{RB});
    snprintf(rl, sizeof(rl), "<  %s  >", RR_RARITY_NAMES{LB}shop_rarity{RB});
    uint64_t val = shop_tab == 0 ? (RR_SELL_PRICES{LB}shop_rarity{RB} * 2) : RR_SELL_PRICES{LB}shop_rarity{RB};
    snprintf(al, sizeof(al), shop_tab == 0 ? "BUY FOR %llu R" : "SELL FOR +%llu R", (unsigned long long)val);

    rr_renderer_set_fill(r, 0xff1f140a); rr_renderer_begin_path(r); rr_renderer_round_rect(r, -190, -75, 380, 40, 8); rr_renderer_fill(r);
    rr_shop_text(r, pl, 0, -55, 18, 0xffffffff);
    rr_renderer_begin_path(r); rr_renderer_round_rect(r, -190, -15, 380, 40, 8); rr_renderer_fill(r);
    rr_shop_text(r, rl, 0, 5, 18, 0xffffe066);

    rr_renderer_set_fill(r, shop_tab == 0 ? 0xffd98a1c : 0xff2e8b57);
    rr_renderer_begin_path(r); rr_renderer_round_rect(r, -160, 50, 320, 52, 10); rr_renderer_fill(r);
    rr_shop_text(r, al, 0, 76, 20, 0xffffffff);
    rr_shop_text(r, shop_status, 0, 140, 14, 0xffffe066);
}}

struct rr_ui_element *rr_ui_shop_container_init(struct rr_game *g) {{
    (void)g; struct rr_ui_element *this = rr_ui_element_init();
    this->abs_width = this->width = 460; this->abs_height = this->height = 360;
    this->animate = shop_anim; this->should_show = shop_show; this->on_event = shop_ev; this->on_render = shop_rd;
    return this;
}}

static uint8_t q_show(struct rr_ui_element *this, struct rr_game *g) {{ (void)this; return g->menu_open == rr_game_menu_quests; }}
static void q_ev(struct rr_ui_element *this, struct rr_game *g) {{
    if (!(g->input_data->mouse_buttons_up_this_tick & 1)) return;
    float mx = ({mx_expr} - g->renderer->width / 2.0f) / g->renderer->scale - this->x;
    float my = ({my_expr} - g->renderer->height / 2.0f) / g->renderer->scale - this->y;
    if (my >= 45 && my <= 100) rr_shop_send_chat(g, mx < 0 ? "/quest" : "/claim");
}}
static void q_rd(struct rr_ui_element *this, struct rr_game *g) {{
    (void)this; struct rr_renderer *r = g->renderer; rr_renderer_scale(r, r->scale);
    rr_renderer_set_fill(r, 0xee182914); rr_renderer_set_stroke(r, 0xff7eef6d); rr_renderer_set_line_width(r, 6);
    rr_renderer_begin_path(r); rr_renderer_round_rect(r, -210, -155, 420, 310, 14); rr_renderer_fill(r); rr_renderer_stroke(r);
    rr_shop_text(r, "QUEST HUNTER [R]", 0, -132, 22, 0xff7eef6d);

    rr_renderer_set_fill(r, 0xffffe763); rr_renderer_set_stroke(r, 0xffcfb73c); rr_renderer_set_line_width(r, 4);
    rr_renderer_begin_path(r); rr_renderer_arc(r, 0, -68, 28, 0, 6.2832f, 0); rr_renderer_fill(r); rr_renderer_stroke(r);
    rr_shop_text(r, "^   ^", 0, -72, 16, 0xff1f1f1f);
    rr_shop_text(r, "u", 0, -56, 16, 0xff1f1f1f);
    rr_shop_text(r, "Kill mobs of target rarity for R!", 0, -12, 15, 0xffeaffdf);
    rr_shop_text(r, "Check chat for target & reward", 0, 14, 13, 0xffa8e6a1);

    rr_renderer_set_fill(r, 0xff3a6b2c); rr_renderer_begin_path(r); rr_renderer_round_rect(r, -185, 48, 175, 48, 9); rr_renderer_fill(r);
    rr_shop_text(r, "GET QUEST", -97, 72, 16, 0xffffffff);
    rr_renderer_set_fill(r, 0xffd98a1c); rr_renderer_begin_path(r); rr_renderer_round_rect(r, 10, 48, 175, 48, 9); rr_renderer_fill(r);
    rr_shop_text(r, "CLAIM R", 97, 72, 16, 0xffffffff);
}}
struct rr_ui_element *rr_ui_quests_container_init(struct rr_game *g) {{
    (void)g; struct rr_ui_element *this = rr_ui_element_init();
    this->abs_width = this->width = 420; this->abs_height = this->height = 310;
    this->animate = shop_anim; this->should_show = q_show; this->on_event = q_ev; this->on_render = q_rd;
    return this;
}}
"""
with open("Client/Ui/TitleScreen/Shop.c", "a", encoding="utf-8") as f:
    f.write(win_code)
print("[OK] Часть 2 записана")
