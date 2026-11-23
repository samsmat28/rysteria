#include <Client/Ui/Ui.h>
#include <stdio.h>
#include <string.h>
#include <Client/Assets/RenderFunctions.h>
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
static char shop_status[96] = "Ready to trade!";
static const uint64_t RR_SELL_PRICES[11] = {5,15,40,120,350,1000,3000,9000,25000,75000,200000};

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

static void shop_btn_ev(struct rr_ui_element *this, struct rr_game *g, enum rr_ui_event ev) {
    if (ev == rr_ui_click && this->hovered) {
        g->menu_open = (g->menu_open == rr_game_menu_shop) ? rr_game_menu_none : rr_game_menu_shop;
        if (g->menu_open == rr_game_menu_shop) rr_shop_send_chat(g, "/balance");
    }
}
static void shop_btn_an(struct rr_ui_element *this, struct rr_game *g) {
    (void)this;
    if (rr_bitset_get_bit(g->input_data->keys_pressed_this_tick, 'B') && !g->text_input_focused)
        g->menu_open = (g->menu_open == rr_game_menu_shop) ? rr_game_menu_none : rr_game_menu_shop;
}
static void shop_btn_rd(struct rr_ui_element *this, struct rr_game *g) {
    struct rr_renderer *r = g->renderer;
    rr_renderer_scale(r, r->scale);
    rr_renderer_set_fill(r, this->hovered || g->menu_open == rr_game_menu_shop ? 0xffd98a1c : 0xffa66814);
    rr_renderer_set_stroke(r, 0xff6e4209);
    rr_renderer_set_line_width(r, 5);
    rr_renderer_begin_path(r);
    rr_renderer_round_rect(r, -this->width/2, -this->height/2, this->width, this->height, 8);
    rr_renderer_fill(r); rr_renderer_stroke(r);
    rr_render_text(r, "SHOP", 0, -2, 13, 0xffffffff, 0xff000000, 2.5f);
    rr_render_text(r, "[B]", 0, 16, 11, 0xffffe066, 0xff000000, 2.0f);
}
struct rr_ui_element *rr_ui_shop_toggle_button_init() {
    struct rr_ui_element *this = rr_ui_element_init();
    this->abs_width = this->abs_height = this->width = this->height = 60;
    this->animate = shop_btn_an; this->on_event = shop_btn_ev; this->on_render = shop_btn_rd;
    return this;
}

static void q_btn_ev(struct rr_ui_element *this, struct rr_game *g, enum rr_ui_event ev) {
    if (ev == rr_ui_click && this->hovered) {
        g->menu_open = (g->menu_open == rr_game_menu_quests) ? rr_game_menu_none : rr_game_menu_quests;
        if (g->menu_open == rr_game_menu_quests) rr_shop_send_chat(g, "/quest");
    }
}
static void q_btn_an(struct rr_ui_element *this, struct rr_game *g) {
    (void)this;
    if (rr_bitset_get_bit(g->input_data->keys_pressed_this_tick, 'Q') && !g->text_input_focused)
        g->menu_open = (g->menu_open == rr_game_menu_quests) ? rr_game_menu_none : rr_game_menu_quests;
}
static void q_btn_rd(struct rr_ui_element *this, struct rr_game *g) {
    struct rr_renderer *r = g->renderer;
    rr_renderer_scale(r, r->scale);
    rr_renderer_set_fill(r, this->hovered || g->menu_open == rr_game_menu_quests ? 0xff62cc52 : 0xff459e38);
    rr_renderer_set_stroke(r, 0xff28631f);
    rr_renderer_set_line_width(r, 5);
    rr_renderer_begin_path(r);
    rr_renderer_round_rect(r, -this->width/2, -this->height/2, this->width, this->height, 8);
    rr_renderer_fill(r); rr_renderer_stroke(r);
    rr_render_text(r, "QUEST", 0, -2, 13, 0xffffffff, 0xff000000, 2.5f);
    rr_render_text(r, "[Q]", 0, 16, 11, 0xffd4ff9e, 0xff000000, 2.0f);
}
struct rr_ui_element *rr_ui_quests_toggle_button_init() {
    struct rr_ui_element *this = rr_ui_element_init();
    this->abs_width = this->abs_height = this->width = this->height = 60;
    this->animate = q_btn_an; this->on_event = q_btn_ev; this->on_render = q_btn_rd;
    return this;
}


static uint8_t shop_show(struct rr_ui_element *this, struct rr_game *g) { (void)this; return g->menu_open == rr_game_menu_shop; }
static void shop_anim(struct rr_ui_element *this, struct rr_game *g) { (void)g; this->width = this->abs_width; this->height = this->abs_height; }

static void shop_ev(struct rr_ui_element *this, struct rr_game *g, enum rr_ui_event ev) {
    if (ev != rr_ui_click || !this->hovered) return;
    float mx = (g->input_data->mouse_x - g->renderer->width / 2.0f) / g->renderer->scale - this->x;
    float my = (g->input_data->mouse_y - g->renderer->height / 2.0f) / g->renderer->scale - this->y;
    if (my >= -145 && my <= -105) shop_tab = (mx < 0) ? 0 : 1;
    if (my >= -75 && my <= -35) { shop_petal += (mx < 0 ? -1 : 1); if (shop_petal < 1) shop_petal = rr_petal_id_max - 1; if (shop_petal >= rr_petal_id_max) shop_petal = 1; }
    if (my >= -15 && my <= 25) { int m = (shop_tab == 0 ? 3 : 0); shop_rarity += (mx < 0 ? -1 : 1); if (shop_rarity < m) shop_rarity = rr_rarity_id_max - 1; if (shop_rarity >= rr_rarity_id_max) shop_rarity = m; }
    if (my >= 50 && my <= 105) {
        char cmd[48];
        if (shop_tab == 0) { if (shop_rarity < 3) shop_rarity = 3; snprintf(cmd, sizeof(cmd), "/buy %d %d", shop_petal, shop_rarity); }
        else snprintf(cmd, sizeof(cmd), "/sell %d %d", shop_petal, shop_rarity);
        rr_shop_send_chat(g, cmd);
    }
}

static void shop_rd(struct rr_ui_element *this, struct rr_game *g) {
    (void)this; struct rr_renderer *r = g->renderer; rr_renderer_scale(r, r->scale);
    rr_renderer_set_fill(r, 0xee291b0e); rr_renderer_set_stroke(r, 0xfff5c542); rr_renderer_set_line_width(r, 6);
    rr_renderer_begin_path(r); rr_renderer_round_rect(r, -230, -180, 460, 360, 14); rr_renderer_fill(r); rr_renderer_stroke(r);
    rr_render_text(r, "RYSTERIA SHOP [R]", 0, -158, 22, 0xffffd700, 0xff000000, 3.0f);

    rr_renderer_set_fill(r, shop_tab == 0 ? 0xff8b5a2b : 0xff3b2613);
    rr_renderer_begin_path(r); rr_renderer_round_rect(r, -200, -140, 190, 34, 8); rr_renderer_fill(r);
    rr_render_text(r, "BUY RARE", -105, -123, 15, 0xffffffff, 0xff000000, 2.0f);

    rr_renderer_set_fill(r, shop_tab == 1 ? 0xff8b5a2b : 0xff3b2613);
    rr_renderer_begin_path(r); rr_renderer_round_rect(r, 10, -140, 190, 34, 8); rr_renderer_fill(r);
    rr_render_text(r, "SELL PETAL", 105, -123, 15, 0xffffffff, 0xff000000, 2.0f);

    if (shop_tab == 0 && shop_rarity < 3) shop_rarity = 3;
    char pl[64], rl[64], al[64];
    snprintf(pl, sizeof(pl), "<  #%d %s  >", shop_petal, RR_PETAL_NAMES[shop_petal]);
    snprintf(rl, sizeof(rl), "<  %s  >", RR_RARITY_NAMES[shop_rarity]);
    uint64_t val = shop_tab == 0 ? (RR_SELL_PRICES[shop_rarity] * 2) : RR_SELL_PRICES[shop_rarity];
    snprintf(al, sizeof(al), shop_tab == 0 ? "BUY FOR %llu R" : "SELL FOR +%llu R", (unsigned long long)val);

    rr_renderer_set_fill(r, 0xff1f140a); rr_renderer_begin_path(r); rr_renderer_round_rect(r, -190, -75, 380, 40, 8); rr_renderer_fill(r);
    rr_render_text(r, pl, 0, -55, 18, 0xffffffff, 0xff000000, 2.5f);
    rr_renderer_begin_path(r); rr_renderer_round_rect(r, -190, -15, 380, 40, 8); rr_renderer_fill(r);
    rr_render_text(r, rl, 0, 5, 18, 0xffffe066, 0xff000000, 2.5f);

    rr_renderer_set_fill(r, shop_tab == 0 ? 0xffd98a1c : 0xff2e8b57);
    rr_renderer_begin_path(r); rr_renderer_round_rect(r, -160, 50, 320, 52, 10); rr_renderer_fill(r);
    rr_render_text(r, al, 0, 76, 20, 0xffffffff, 0xff000000, 3.0f);
    rr_render_text(r, shop_status, 0, 140, 14, 0xffffe066, 0xff000000, 2.0f);
}

struct rr_ui_element *rr_ui_shop_container_init(struct rr_game *g) {
    (void)g; struct rr_ui_element *this = rr_ui_element_init();
    this->abs_width = this->width = 460; this->abs_height = this->height = 360;
    this->animate = shop_anim; this->should_show = shop_show; this->on_event = shop_ev; this->on_render = shop_rd;
    return this;
}

static uint8_t q_show(struct rr_ui_element *this, struct rr_game *g) { (void)this; return g->menu_open == rr_game_menu_quests; }
static void q_ev(struct rr_ui_element *this, struct rr_game *g, enum rr_ui_event ev) {
    if (ev != rr_ui_click || !this->hovered) return;
    float mx = (g->input_data->mouse_x - g->renderer->width / 2.0f) / g->renderer->scale - this->x;
    float my = (g->input_data->mouse_y - g->renderer->height / 2.0f) / g->renderer->scale - this->y;
    if (my >= 45 && my <= 100) rr_shop_send_chat(g, mx < 0 ? "/quest" : "/claim");
}
static void q_rd(struct rr_ui_element *this, struct rr_game *g) {
    (void)this; struct rr_renderer *r = g->renderer; rr_renderer_scale(r, r->scale);
    rr_renderer_set_fill(r, 0xee182914); rr_renderer_set_stroke(r, 0xff7eef6d); rr_renderer_set_line_width(r, 6);
    rr_renderer_begin_path(r); rr_renderer_round_rect(r, -210, -155, 420, 310, 14); rr_renderer_fill(r); rr_renderer_stroke(r);
    rr_render_text(r, "QUEST HUNTER [R]", 0, -132, 22, 0xff7eef6d, 0xff000000, 3.0f);

    rr_renderer_set_fill(r, 0xffffe763); rr_renderer_set_stroke(r, 0xffcfb73c); rr_renderer_set_line_width(r, 4);
    rr_renderer_begin_path(r); rr_renderer_arc(r, 0, -68, 28, 0, 6.2832f, 0); rr_renderer_fill(r); rr_renderer_stroke(r);
    rr_render_text(r, "^   ^", 0, -72, 16, 0xff1f1f1f, 0x00000000, 0);
    rr_render_text(r, "u", 0, -56, 16, 0xff1f1f1f, 0x00000000, 0);
    rr_render_text(r, "Kill mobs of target rarity for R!", 0, -12, 15, 0xffeaffdf, 0xff000000, 2.0f);

    rr_renderer_set_fill(r, 0xff3a6b2c); rr_renderer_begin_path(r); rr_renderer_round_rect(r, -185, 48, 175, 48, 9); rr_renderer_fill(r);
    rr_render_text(r, "GET QUEST", -97, 72, 16, 0xffffffff, 0xff000000, 2.5f);
    rr_renderer_set_fill(r, 0xffd98a1c); rr_renderer_begin_path(r); rr_renderer_round_rect(r, 10, 48, 175, 48, 9); rr_renderer_fill(r);
    rr_render_text(r, "CLAIM R", 97, 72, 16, 0xffffffff, 0xff000000, 2.5f);
}
struct rr_ui_element *rr_ui_quests_container_init(struct rr_game *g) {
    (void)g; struct rr_ui_element *this = rr_ui_element_init();
    this->abs_width = this->width = 420; this->abs_height = this->height = 310;
    this->animate = shop_anim; this->should_show = q_show; this->on_event = q_ev; this->on_render = q_rd;
    return this;
}
