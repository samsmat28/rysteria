#include <Client/Ui/Ui.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <Client/Game.h>
#include <Client/InputData.h>
#include <Client/Renderer/Renderer.h>
#include <Client/Ui/Engine.h>
#include <Shared/StaticData.h>
#include <Shared/Utilities.h>
#include <Shared/pb.h>

static uint8_t shop_tab = 0;
static int shop_petal = 43;
static int shop_rarity = 3;
static char shop_status[96] = "Enter game & click action!";
static const uint64_t RR_SELL_PRICES[11] = {5,15,40,120,350,1000,3000,9000,25000,75000,200000};

static void rr_shop_text(struct rr_renderer *r, const char *txt, float x, float y, float sz, uint32_t col) {
    rr_renderer_set_text_baseline(r, 1); rr_renderer_set_text_align(r, 1); rr_renderer_set_text_size(r, sz);
    rr_renderer_set_fill(r, col); rr_renderer_set_stroke(r, 0xff111111); rr_renderer_set_line_width(r, sz * 0.14f);
    rr_renderer_stroke_text(r, txt, x, y); rr_renderer_fill_text(r, txt, x, y);
}

static void rr_shop_send_chat(struct rr_game *game, const char *cmd) {
    if (!game || !cmd) return;
    struct proto_bug encoder;
    proto_bug_init(&encoder, RR_OUTGOING_PACKET);
    proto_bug_write_uint8(&encoder, game->socket.quick_verification, "qv");
    proto_bug_write_uint8(&encoder, rr_serverbound_chat, "header");
    proto_bug_write_string(&encoder, cmd, 64, "chat");
    rr_websocket_send(&game->socket, encoder.current - encoder.start);
    snprintf(shop_status, sizeof(shop_status), "Sent: %s", cmd);
}

struct shop_act_meta { int action_id; };
static void act_btn_anim(struct rr_ui_element *this, struct rr_game *g) { (void)g; this->width = this->abs_width; this->height = this->abs_height; }

static void act_btn_ev(struct rr_ui_element *this, struct rr_game *g) {
    if (!(g->input_data->mouse_buttons_up_this_tick & 1)) return;
    struct shop_act_meta *m = this->data;
    if (!m) return;
    int id = m->action_id, min_r = (shop_tab == 0) ? 3 : 0;
    if (id == 1) shop_tab = 0;
    else if (id == 2) shop_tab = 1;
    else if (id == 3) { shop_petal--; if (shop_petal < 1) shop_petal = rr_petal_id_max - 1; }
    else if (id == 4) { shop_petal++; if (shop_petal >= rr_petal_id_max) shop_petal = 1; }
    else if (id == 5) { shop_rarity--; if (shop_rarity < min_r) shop_rarity = rr_rarity_id_max - 1; }
    else if (id == 6) { shop_rarity++; if (shop_rarity >= rr_rarity_id_max) shop_rarity = min_r; }
    else if (id == 7) {
        char cmd[48];
        if (shop_tab == 0) { if (shop_rarity < 3) shop_rarity = 3; snprintf(cmd, sizeof(cmd), "/buy %d %d", shop_petal, shop_rarity); }
        else snprintf(cmd, sizeof(cmd), "/sell %d %d", shop_petal, shop_rarity);
        rr_shop_send_chat(g, cmd);
    }
    else if (id == 8) rr_shop_send_chat(g, "/quest");
    else if (id == 9) rr_shop_send_chat(g, "/claim");
}

static void act_btn_rd(struct rr_ui_element *this, struct rr_game *g) {
    struct shop_act_meta *m = this->data;
    int id = m ? m->action_id : 0;
    uint8_t hov = (g->focused == this);
    struct rr_renderer *r = g->renderer;
    rr_renderer_scale(r, r->scale);
    uint32_t bg = hov ? 0xffa86d34 : 0xff6e451e;
    const char *lbl = ""; char dyn[64];
    if (id == 1) { bg = (shop_tab == 0) ? 0xffb87635 : (hov ? 0xff5e3d1e : 0xff3b2613); lbl = "BUY RARE"; }
    else if (id == 2) { bg = (shop_tab == 1) ? 0xffb87635 : (hov ? 0xff5e3d1e : 0xff3b2613); lbl = "SELL PETAL"; }
    else if (id == 3 || id == 5) lbl = "<";
    else if (id == 4 || id == 6) lbl = ">";
    else if (id == 7) {
        if (shop_tab == 0 && shop_rarity < 3) shop_rarity = 3;
        uint64_t val = shop_tab == 0 ? (RR_SELL_PRICES[shop_rarity] * 2) : RR_SELL_PRICES[shop_rarity];
        bg = (shop_tab == 0) ? (hov ? 0xfff29f24 : 0xffd98a1c) : (hov ? 0xff3cb371 : 0xff2e8b57);
        snprintf(dyn, sizeof(dyn), shop_tab == 0 ? "BUY FOR %llu R" : "SELL FOR +%llu R", (unsigned long long)val);
        lbl = dyn;
    }
    else if (id == 8) { bg = hov ? 0xff4d8c3b : 0xff3a6b2c; lbl = "GET QUEST"; }
    else if (id == 9) { bg = hov ? 0xfff29f24 : 0xffd98a1c; lbl = "CLAIM R"; }
    rr_renderer_set_fill(r, bg); rr_renderer_set_stroke(r, 0xff1f140a); rr_renderer_set_line_width(r, 3);
    rr_renderer_begin_path(r); rr_renderer_round_rect(r, -this->width/2, -this->height/2, this->width, this->height, 8);
    rr_renderer_fill(r); rr_renderer_stroke(r);
    rr_shop_text(r, lbl, 0, 0, (id >= 7) ? 18 : 15, 0xffffffff);
}

static struct rr_ui_element *make_shop_btn(int id, float x, float y, float w, float h) {
    struct rr_ui_element *b = rr_ui_element_init();
    struct shop_act_meta *m = malloc(sizeof(struct shop_act_meta));
    m->action_id = id; b->data = m; b->x = x; b->y = y;
    b->abs_width = b->width = w; b->abs_height = b->height = h; b->no_reposition = 1;
    b->animate = act_btn_anim; b->on_event = act_btn_ev; b->on_render = act_btn_rd;
    return b;
}

static void shop_btn_ev(struct rr_ui_element *this, struct rr_game *g) {
    (void)this;
    if (g->input_data->mouse_buttons_up_this_tick & 1) {
        g->menu_open = (g->menu_open == rr_game_menu_shop) ? rr_game_menu_none : rr_game_menu_shop;
        if (g->menu_open == rr_game_menu_shop) rr_shop_send_chat(g, "/balance");
    }
}
static void shop_btn_an(struct rr_ui_element *this, struct rr_game *g) {
    (void)this;
    if (rr_bitset_get_bit(g->input_data->keys_pressed_this_tick, 'B') && !g->text_input_focused) {
        g->menu_open = (g->menu_open == rr_game_menu_shop) ? rr_game_menu_none : rr_game_menu_shop;
        if (g->menu_open == rr_game_menu_shop) rr_shop_send_chat(g, "/balance");
    }
}
static void shop_btn_rd(struct rr_ui_element *this, struct rr_game *g) {
    struct rr_renderer *r = g->renderer; rr_renderer_scale(r, r->scale);
    rr_renderer_set_fill(r, (g->focused == this || g->menu_open == rr_game_menu_shop) ? 0xffd98a1c : 0xffa66814);
    rr_renderer_set_stroke(r, 0xff6e4209); rr_renderer_set_line_width(r, 5);
    rr_renderer_begin_path(r); rr_renderer_round_rect(r, -this->width/2, -this->height/2, this->width, this->height, 8);
    rr_renderer_fill(r); rr_renderer_stroke(r);
    rr_shop_text(r, "SHOP", 0, -4, 13, 0xffffffff); rr_shop_text(r, "[B]", 0, 15, 11, 0xffffe066);
}
struct rr_ui_element *rr_ui_shop_toggle_button_init() {
    struct rr_ui_element *this = rr_ui_element_init();
    this->abs_width = this->abs_height = this->width = this->height = 60;
    this->animate = shop_btn_an; this->on_event = shop_btn_ev; this->on_render = shop_btn_rd;
    return this;
}

static void q_btn_ev(struct rr_ui_element *this, struct rr_game *g) {
    (void)this;
    if (g->input_data->mouse_buttons_up_this_tick & 1) {
        g->menu_open = (g->menu_open == rr_game_menu_quests) ? rr_game_menu_none : rr_game_menu_quests;
        if (g->menu_open == rr_game_menu_quests) rr_shop_send_chat(g, "/quest");
    }
}
static void q_btn_an(struct rr_ui_element *this, struct rr_game *g) {
    (void)this;
    if (rr_bitset_get_bit(g->input_data->keys_pressed_this_tick, 'Q') && !g->text_input_focused) {
        g->menu_open = (g->menu_open == rr_game_menu_quests) ? rr_game_menu_none : rr_game_menu_quests;
        if (g->menu_open == rr_game_menu_quests) rr_shop_send_chat(g, "/quest");
    }
}
static void q_btn_rd(struct rr_ui_element *this, struct rr_game *g) {
    struct rr_renderer *r = g->renderer; rr_renderer_scale(r, r->scale);
    rr_renderer_set_fill(r, (g->focused == this || g->menu_open == rr_game_menu_quests) ? 0xff62cc52 : 0xff459e38);
    rr_renderer_set_stroke(r, 0xff28631f); rr_renderer_set_line_width(r, 5);
    rr_renderer_begin_path(r); rr_renderer_round_rect(r, -this->width/2, -this->height/2, this->width, this->height, 8);
    rr_renderer_fill(r); rr_renderer_stroke(r);
    rr_shop_text(r, "QUEST", 0, -4, 13, 0xffffffff); rr_shop_text(r, "[Q]", 0, 15, 11, 0xffd4ff9e);
}
struct rr_ui_element *rr_ui_quests_toggle_button_init() {
    struct rr_ui_element *this = rr_ui_element_init();
    this->abs_width = this->abs_height = this->width = this->height = 60;
    this->animate = q_btn_an; this->on_event = q_btn_ev; this->on_render = q_btn_rd;
    return this;
}

static uint8_t shop_show(struct rr_ui_element *this, struct rr_game *g) { (void)this; return g->menu_open == rr_game_menu_shop; }
static void shop_rd(struct rr_ui_element *this, struct rr_game *g) {
    (void)this; struct rr_renderer *r = g->renderer; rr_renderer_scale(r, r->scale);
    rr_renderer_set_fill(r, 0xee291b0e); rr_renderer_set_stroke(r, 0xfff5c542); rr_renderer_set_line_width(r, 6);
    rr_renderer_begin_path(r); rr_renderer_round_rect(r, -230, -180, 460, 360, 14); rr_renderer_fill(r); rr_renderer_stroke(r);
    rr_shop_text(r, "RYSTERIA SHOP [R]", 0, -158, 22, 0xffffd700);
    if (shop_tab == 0 && shop_rarity < 3) shop_rarity = 3;
    char pl[64], rl[64];
    snprintf(pl, sizeof(pl), "#%d %s", shop_petal, RR_PETAL_NAMES[shop_petal]);
    snprintf(rl, sizeof(rl), "%s", RR_RARITY_NAMES[shop_rarity]);
    rr_renderer_set_fill(r, 0xff1f140a);
    rr_renderer_begin_path(r); rr_renderer_round_rect(r, -140, -75, 280, 40, 8); rr_renderer_fill(r);
    rr_shop_text(r, pl, 0, -55, 18, 0xffffffff);
    rr_renderer_begin_path(r); rr_renderer_round_rect(r, -140, -15, 280, 40, 8); rr_renderer_fill(r);
    rr_shop_text(r, rl, 0, 5, 18, 0xffffe066);
    rr_shop_text(r, shop_status, 0, 142, 14, 0xffffe066);
}
struct rr_ui_element *rr_ui_shop_container_init(struct rr_game *g) {
    (void)g; struct rr_ui_element *this = rr_ui_container_init();
    this->abs_width = this->width = 460; this->abs_height = this->height = 360;
    this->animate = act_btn_anim; this->should_show = shop_show; this->on_render = shop_rd;
    rr_ui_container_add_element(this, make_shop_btn(1, -105, -123, 185, 34));
    rr_ui_container_add_element(this, make_shop_btn(2,  105, -123, 185, 34));
    rr_ui_container_add_element(this, make_shop_btn(3, -172,  -55,  46, 40));
    rr_ui_container_add_element(this, make_shop_btn(4,  172,  -55,  46, 40));
    rr_ui_container_add_element(this, make_shop_btn(5, -172,    5,  46, 40));
    rr_ui_container_add_element(this, make_shop_btn(6,  172,    5,  46, 40));
    rr_ui_container_add_element(this, make_shop_btn(7,    0,   78, 320, 52));
    return this;
}

static uint8_t q_show(struct rr_ui_element *this, struct rr_game *g) { (void)this; return g->menu_open == rr_game_menu_quests; }
static void q_rd(struct rr_ui_element *this, struct rr_game *g) {
    (void)this; struct rr_renderer *r = g->renderer; rr_renderer_scale(r, r->scale);
    rr_renderer_set_fill(r, 0xee182914); rr_renderer_set_stroke(r, 0xff7eef6d); rr_renderer_set_line_width(r, 6);
    rr_renderer_begin_path(r); rr_renderer_round_rect(r, -210, -155, 420, 310, 14); rr_renderer_fill(r); rr_renderer_stroke(r);
    rr_shop_text(r, "QUEST HUNTER [R]", 0, -132, 22, 0xff7eef6d);
    rr_renderer_set_fill(r, 0xffffe763); rr_renderer_set_stroke(r, 0xffcfb73c); rr_renderer_set_line_width(r, 4);
    rr_renderer_begin_path(r); rr_renderer_arc(r, 0, -68, 28); rr_renderer_fill(r); rr_renderer_stroke(r);
    rr_shop_text(r, "^   ^", 0, -72, 16, 0xff1f1f1f); rr_shop_text(r, "u", 0, -56, 16, 0xff1f1f1f);
    rr_shop_text(r, "Kill mobs of target rarity for R!", 0, -12, 15, 0xffeaffdf);
    rr_shop_text(r, "Check chat for target & reward", 0, 14, 13, 0xffa8e6a1);
    rr_shop_text(r, shop_status, 0, 122, 13, 0xffffe066);
}
struct rr_ui_element *rr_ui_quests_container_init(struct rr_game *g) {
    (void)g; struct rr_ui_element *this = rr_ui_container_init();
    this->abs_width = this->width = 420; this->abs_height = this->height = 310;
    this->animate = act_btn_anim; this->should_show = q_show; this->on_render = q_rd;
    rr_ui_container_add_element(this, make_shop_btn(8, -97, 72, 175, 48));
    rr_ui_container_add_element(this, make_shop_btn(9,  97, 72, 175, 48));
    return this;
}
