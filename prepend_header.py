LB, RB = chr(91), chr(93)
head = f"""#include <Client/Ui/Ui.h>
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
static char shop_status{LB}96{RB} = "Ready to trade!";
static const uint64_t RR_SELL_PRICES{LB}11{RB} = {{5,15,40,120,350,1000,3000,9000,25000,75000,200000}};

static void rr_shop_send_chat(struct rr_game *game, const char *cmd) {{
    if (!game || !cmd) return;
    struct proto_bug encoder;
    proto_bug_init(&encoder, RR_OUTGOING_PACKET);
    proto_bug_write_uint8(&encoder, game->socket.quick_verification, "qv");
    proto_bug_write_uint8(&encoder, rr_serverbound_chat, "header");
    proto_bug_write_string(&encoder, cmd, 64, "chat");
    rr_websocket_send(&game->socket, encoder.current - encoder.start);
    snprintf(shop_status, sizeof(shop_status), "Sent: %s", cmd);
}}

static void shop_btn_ev(struct rr_ui_element *this, struct rr_game *g, enum rr_ui_event ev) {{
    if (ev == rr_ui_click && this->hovered) {{
        g->menu_open = (g->menu_open == rr_game_menu_shop) ? rr_game_menu_none : rr_game_menu_shop;
        if (g->menu_open == rr_game_menu_shop) rr_shop_send_chat(g, "/balance");
    }}
}}
static void shop_btn_an(struct rr_ui_element *this, struct rr_game *g) {{
    (void)this;
    if (rr_bitset_get_bit(g->input_data->keys_pressed_this_tick, 'B') && !g->text_input_focused)
        g->menu_open = (g->menu_open == rr_game_menu_shop) ? rr_game_menu_none : rr_game_menu_shop;
}}
static void shop_btn_rd(struct rr_ui_element *this, struct rr_game *g) {{
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
}}
struct rr_ui_element *rr_ui_shop_toggle_button_init() {{
    struct rr_ui_element *this = rr_ui_element_init();
    this->abs_width = this->abs_height = this->width = this->height = 60;
    this->animate = shop_btn_an; this->on_event = shop_btn_ev; this->on_render = shop_btn_rd;
    return this;
}}

static void q_btn_ev(struct rr_ui_element *this, struct rr_game *g, enum rr_ui_event ev) {{
    if (ev == rr_ui_click && this->hovered) {{
        g->menu_open = (g->menu_open == rr_game_menu_quests) ? rr_game_menu_none : rr_game_menu_quests;
        if (g->menu_open == rr_game_menu_quests) rr_shop_send_chat(g, "/quest");
    }}
}}
static void q_btn_an(struct rr_ui_element *this, struct rr_game *g) {{
    (void)this;
    if (rr_bitset_get_bit(g->input_data->keys_pressed_this_tick, 'Q') && !g->text_input_focused)
        g->menu_open = (g->menu_open == rr_game_menu_quests) ? rr_game_menu_none : rr_game_menu_quests;
}}
static void q_btn_rd(struct rr_ui_element *this, struct rr_game *g) {{
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
}}
struct rr_ui_element *rr_ui_quests_toggle_button_init() {{
    struct rr_ui_element *this = rr_ui_element_init();
    this->abs_width = this->abs_height = this->width = this->height = 60;
    this->animate = q_btn_an; this->on_event = q_btn_ev; this->on_render = q_btn_rd;
    return this;
}}
"""
with open("Client/Ui/TitleScreen/Shop.c", "r", encoding="utf-8") as f:
    tail = f.read()
with open("Client/Ui/TitleScreen/Shop.c", "w", encoding="utf-8") as f:
    f.write(head + "\n" + tail)
print("[OK] Шапка добавлена")
