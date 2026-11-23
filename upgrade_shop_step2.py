LB, RB = chr(91), chr(93)

# 1. На сервере делаем покупку Epic уникального лепестка по акции 100 R (чтобы стартовых 100 R сразу хватало!)
with open("Server/Server.c", "r", encoding="utf-8") as f:
    sc = f.read()

sc = sc.replace(
    "uint64_t cost = sell_p[rid] * 2;",
    "uint64_t cost = (pid == 62 && rid == 3) ? 100 : (sell_p[rid] * 2);"
)
with open("Server/Server.c", "w", encoding="utf-8") as f:
    f.write(sc)

# 2. Дописываем окна Shop и Quests с нативными кнопками в Client/Ui/TitleScreen/Shop.c
code = f"""
static void shop_btn_ev(struct rr_ui_element *this, struct rr_game *g) {{
    (void)this;
    if (g->input_data->mouse_buttons_up_this_tick & 1) {{
        g->menu_open = (g->menu_open == rr_game_menu_shop) ? rr_game_menu_none : rr_game_menu_shop;
        if (g->menu_open == rr_game_menu_shop) rr_shop_send_chat(g, "/balance");
    }}
}}
static void shop_btn_an(struct rr_ui_element *this, struct rr_game *g) {{
    (void)this;
    if (rr_bitset_get_bit(g->input_data->keys_pressed_this_tick, 'B') && !g->text_input_focused) {{
        g->menu_open = (g->menu_open == rr_game_menu_shop) ? rr_game_menu_none : rr_game_menu_shop;
        if (g->menu_open == rr_game_menu_shop) rr_shop_send_chat(g, "/balance");
    }}
}}
static void shop_btn_rd(struct rr_ui_element *this, struct rr_game *g) {{
    struct rr_renderer *r = g->renderer; rr_renderer_scale(r, r->scale);
    rr_renderer_set_fill(r, (g->focused == this || g->menu_open == rr_game_menu_shop) ? 0xffd98a1c : 0xffa66814);
    rr_renderer_set_stroke(r, 0xff6e4209); rr_renderer_set_line_width(r, 5);
    rr_renderer_begin_path(r); rr_renderer_round_rect(r, -this->width/2, -this->height/2, this->width, this->height, 8);
    rr_renderer_fill(r); rr_renderer_stroke(r);
    rr_shop_text(r, "SHOP", 0, -4, 13, 0xffffffff); rr_shop_text(r, "[B]", 0, 15, 11, 0xffffe066);
}}
struct rr_ui_element *rr_ui_shop_toggle_button_init() {{
    struct rr_ui_element *this = rr_ui_element_init();
    this->abs_width = this->abs_height = this->width = this->height = 60;
    this->animate = shop_btn_an; this->on_event = shop_btn_ev; this->on_render = shop_btn_rd;
    return this;
}}

static void q_btn_ev(struct rr_ui_element *this, struct rr_game *g) {{
    (void)this;
    if (g->input_data->mouse_buttons_up_this_tick & 1) {{
        g->menu_open = (g->menu_open == rr_game_menu_quests) ? rr_game_menu_none : rr_game_menu_quests;
        if (g->menu_open == rr_game_menu_quests) rr_shop_send_chat(g, "/quest");
    }}
}}
static void q_btn_an(struct rr_ui_element *this, struct rr_game *g) {{
    (void)this;
    if (rr_bitset_get_bit(g->input_data->keys_pressed_this_tick, 'Q') && !g->text_input_focused) {{
        g->menu_open = (g->menu_open == rr_game_menu_quests) ? rr_game_menu_none : rr_game_menu_quests;
        if (g->menu_open == rr_game_menu_quests) rr_shop_send_chat(g, "/quest");
    }}
}}
static void q_btn_rd(struct rr_ui_element *this, struct rr_game *g) {{
    struct rr_renderer *r = g->renderer; rr_renderer_scale(r, r->scale);
    rr_renderer_set_fill(r, (g->focused == this || g->menu_open == rr_game_menu_quests) ? 0xff62cc52 : 0xff459e38);
    rr_renderer_set_stroke(r, 0xff28631f); rr_renderer_set_line_width(r, 5);
    rr_renderer_begin_path(r); rr_renderer_round_rect(r, -this->width/2, -this->height/2, this->width, this->height, 8);
    rr_renderer_fill(r); rr_renderer_stroke(r);
    rr_shop_text(r, "QUEST", 0, -4, 13, 0xffffffff); rr_shop_text(r, "[Q]", 0, 15, 11, 0xffd4ff9e);
}}
struct rr_ui_element *rr_ui_quests_toggle_button_init() {{
    struct rr_ui_element *this = rr_ui_element_init();
    this->abs_width = this->abs_height = this->width = this->height = 60;
    this->animate = q_btn_an; this->on_event = q_btn_ev; this->on_render = q_btn_rd;
    return this;
}}

static uint8_t shop_show(struct rr_ui_element *this, struct rr_game *g) {{ (void)this; return g->menu_open == rr_game_menu_shop; }}
static void shop_rd(struct rr_ui_element *this, struct rr_game *g) {{
    (void)this; struct rr_renderer *r = g->renderer; rr_renderer_scale(r, r->scale);
    rr_renderer_set_fill(r, 0xee291b0e); rr_renderer_set_stroke(r, 0xfff5c542); rr_renderer_set_line_width(r, 6);
    rr_renderer_begin_path(r); rr_renderer_round_rect(r, -230, -195, 460, 390, 14); rr_renderer_fill(r); rr_renderer_stroke(r);
    rr_shop_text(r, "RYSTERIA SHOP [R]", 0, -172, 22, 0xffffd700);
    if (shop_tab == 0 && shop_rarity < 3) shop_rarity = 3;
    char pl{LB}64{RB}, rl{LB}64{RB};
    snprintf(pl, sizeof(pl), "#%d %s", shop_petal, RR_PETAL_NAMES{LB}shop_petal{RB});
    snprintf(rl, sizeof(rl), "%s", RR_RARITY_NAMES{LB}shop_rarity{RB});
    rr_renderer_set_fill(r, 0xff1f140a);
    rr_renderer_begin_path(r); rr_renderer_round_rect(r, -140, -55, 280, 38, 8); rr_renderer_fill(r);
    rr_shop_text(r, pl, 0, -36, 17, 0xffffffff);
    rr_renderer_begin_path(r); rr_renderer_round_rect(r, -140, -5, 280, 38, 8); rr_renderer_fill(r);
    rr_shop_text(r, rl, 0, 14, 17, 0xffffe066);
    rr_shop_text(r, shop_status, 0, 168, 13, 0xffffe066);
}}
struct rr_ui_element *rr_ui_shop_container_init(struct rr_game *g) {{
    (void)g; struct rr_ui_element *this = rr_ui_element_init();
    this->abs_width = this->width = 460; this->abs_height = this->height = 390;
    this->animate = act_btn_anim; this->should_show = shop_show; this->on_render = shop_rd;
    rr_ui_container_add_element(this, make_shop_btn(10,   0, -138, 380, 34));
    rr_ui_container_add_element(this, make_shop_btn(1, -105,  -95, 185, 32));
    rr_ui_container_add_element(this, make_shop_btn(2,  105,  -95, 185, 32));
    rr_ui_container_add_element(this, make_shop_btn(3, -172,  -36,  46, 38));
    rr_ui_container_add_element(this, make_shop_btn(4,  172,  -36,  46, 38));
    rr_ui_container_add_element(this, make_shop_btn(5, -172,   14,  46, 38));
    rr_ui_container_add_element(this, make_shop_btn(6,  172,   14,  46, 38));
    rr_ui_container_add_element(this, make_shop_btn(7,    0,   88, 320, 48));
    return this;
}}

static uint8_t q_show(struct rr_ui_element *this, struct rr_game *g) {{ (void)this; return g->menu_open == rr_game_menu_quests; }}
static void q_rd(struct rr_ui_element *this, struct rr_game *g) {{
    (void)this; struct rr_renderer *r = g->renderer; rr_renderer_scale(r, r->scale);
    rr_renderer_set_fill(r, 0xee182914); rr_renderer_set_stroke(r, 0xff7eef6d); rr_renderer_set_line_width(r, 6);
    rr_renderer_begin_path(r); rr_renderer_round_rect(r, -210, -165, 420, 330, 14); rr_renderer_fill(r); rr_renderer_stroke(r);
    rr_shop_text(r, "QUEST HUNTER [R]", 0, -142, 22, 0xff7eef6d);
    rr_renderer_set_fill(r, 0xffffe763); rr_renderer_set_stroke(r, 0xffcfb73c); rr_renderer_set_line_width(r, 4);
    rr_renderer_begin_path(r); rr_renderer_arc(r, 0, -82, 26); rr_renderer_fill(r); rr_renderer_stroke(r);
    rr_shop_text(r, "^   ^", 0, -86, 15, 0xff1f1f1f); rr_shop_text(r, "u", 0, -70, 15, 0xff1f1f1f);
    rr_shop_text(r, "Step 1: Click GET QUEST to see target", 0, -34, 14, 0xffeaffdf);
    rr_shop_text(r, "Step 2: Kill mobs of that rarity", 0, -12, 14, 0xffeaffdf);
    rr_shop_text(r, "Step 3: Click CLAIM R to get coins!", 0, 10, 14, 0xffa8e6a1);
    rr_shop_text(r, shop_status, 0, 134, 13, 0xffffe066);
}}
struct rr_ui_element *rr_ui_quests_container_init(struct rr_game *g) {{
    (void)g; struct rr_ui_element *this = rr_ui_element_init();
    this->abs_width = this->width = 420; this->abs_height = this->height = 330;
    this->animate = act_btn_anim; this->should_show = q_show; this->on_render = q_rd;
    rr_ui_container_add_element(this, make_shop_btn(8, -97, 74, 175, 48));
    rr_ui_container_add_element(this, make_shop_btn(9,  97, 74, 175, 48));
    return this;
}}
"""
with open("Client/Ui/TitleScreen/Shop.c", "a", encoding="utf-8") as f:
    f.write(code)
print("[OK] Шаг 2 готов")
