LB, RB = chr(91), chr(93)

shop_c = f"""#include <Client/Ui/Ui.h>
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

static uint8_t shop_tab = 0; // 0 = Купить, 1 = Продать, 2 = Спец-товар за 100 R
static int shop_petal = 62;  // По умолчанию Relic (уникальный доисторический лепесток)
static int shop_rarity = 3;  // Epic
static char shop_status{LB}96{RB} = "Welcome! Click buttons below";
static const uint64_t RR_SELL_PRICES{LB}11{RB} = {{5,15,40,120,350,1000,3000,9000,25000,75000,200000}};

static void rr_shop_text(struct rr_renderer *r, const char *txt, float x, float y, float sz, uint32_t col) {{
    rr_renderer_set_text_baseline(r, 1); rr_renderer_set_text_align(r, 1); rr_renderer_set_text_size(r, sz);
    rr_renderer_set_fill(r, col); rr_renderer_set_stroke(r, 0xff111111); rr_renderer_set_line_width(r, sz * 0.14f);
    rr_renderer_stroke_text(r, txt, x, y); rr_renderer_fill_text(r, txt, x, y);
}}

static void rr_shop_send_chat(struct rr_game *game, const char *cmd) {{
    if (!game || !cmd) return;
    struct proto_bug encoder;
    proto_bug_init(&encoder, RR_OUTGOING_PACKET);
    proto_bug_write_uint8(&encoder, game->socket.quick_verification, "qv");
    proto_bug_write_uint8(&encoder, rr_serverbound_chat, "header");
    proto_bug_write_string(&encoder, cmd, 64, "chat");
    rr_websocket_send(&game->socket, encoder.current - encoder.start);
    snprintf(shop_status, sizeof(shop_status), "Sent: %s (see chat!)", cmd);
}}

struct shop_act_meta {{ int action_id; }};
static void act_btn_anim(struct rr_ui_element *this, struct rr_game *g) {{ (void)g; this->width = this->abs_width; this->height = this->abs_height; }}

static void act_btn_ev(struct rr_ui_element *this, struct rr_game *g) {{
    if (!(g->input_data->mouse_buttons_up_this_tick & 1)) return;
    struct shop_act_meta *m = this->data;
    if (!m) return;
    int id = m->action_id, min_r = (shop_tab == 0) ? 3 : 0;
    if (id == 1) shop_tab = 0;
    else if (id == 2) shop_tab = 1;
    else if (id == 3) {{ shop_petal--; if (shop_petal < 1) shop_petal = rr_petal_id_max - 1; }}
    else if (id == 4) {{ shop_petal++; if (shop_petal >= rr_petal_id_max) shop_petal = 1; }}
    else if (id == 5) {{ shop_rarity--; if (shop_rarity < min_r) shop_rarity = rr_rarity_id_max - 1; }}
    else if (id == 6) {{ shop_rarity++; if (shop_rarity >= rr_rarity_id_max) shop_rarity = min_r; }}
    else if (id == 7) {{
        char cmd{LB}48{RB};
        if (shop_tab == 0) {{ if (shop_rarity < 3) shop_rarity = 3; snprintf(cmd, sizeof(cmd), "/buy %d %d", shop_petal, shop_rarity); }}
        else snprintf(cmd, sizeof(cmd), "/sell %d %d", shop_petal, shop_rarity);
        rr_shop_send_chat(g, cmd);
    }}
    else if (id == 8) rr_shop_send_chat(g, "/quest");
    else if (id == 9) rr_shop_send_chat(g, "/claim");
    else if (id == 10) rr_shop_send_chat(g, "/buy 62 3"); // Уникальный Relic за 100 R!
}}

static void act_btn_rd(struct rr_ui_element *this, struct rr_game *g) {{
    struct shop_act_meta *m = this->data;
    int id = m ? m->action_id : 0;
    uint8_t hov = (g->focused == this);
    struct rr_renderer *r = g->renderer;
    rr_renderer_scale(r, r->scale);
    uint32_t bg = hov ? 0xffa86d34 : 0xff6e451e;
    const char *lbl = ""; char dyn{LB}64{RB};
    if (id == 1) {{ bg = (shop_tab == 0) ? 0xffb87635 : (hov ? 0xff5e3d1e : 0xff3b2613); lbl = "BUY RARE"; }}
    else if (id == 2) {{ bg = (shop_tab == 1) ? 0xffb87635 : (hov ? 0xff5e3d1e : 0xff3b2613); lbl = "SELL PETAL"; }}
    else if (id == 3 || id == 5) lbl = "<";
    else if (id == 4 || id == 6) lbl = ">";
    else if (id == 7) {{
        if (shop_tab == 0 && shop_rarity < 3) shop_rarity = 3;
        uint64_t val = shop_tab == 0 ? (RR_SELL_PRICES{LB}shop_rarity{RB} * 2) : RR_SELL_PRICES{LB}shop_rarity{RB};
        bg = (shop_tab == 0) ? (hov ? 0xfff29f24 : 0xffd98a1c) : (hov ? 0xff3cb371 : 0xff2e8b57);
        snprintf(dyn, sizeof(dyn), shop_tab == 0 ? "BUY FOR %llu R" : "SELL FOR +%llu R", (unsigned long long)val);
        lbl = dyn;
    }}
    else if (id == 8) {{ bg = hov ? 0xff4d8c3b : 0xff3a6b2c; lbl = "1. GET QUEST"; }}
    else if (id == 9) {{ bg = hov ? 0xfff29f24 : 0xffd98a1c; lbl = "2. CLAIM R"; }}
    else if (id == 10) {{ bg = hov ? 0xffa335ee : 0xff7b1fa2; lbl = "UNIQUE: EPIC RELIC (100 R)"; }}
    rr_renderer_set_fill(r, bg); rr_renderer_set_stroke(r, 0xff1f140a); rr_renderer_set_line_width(r, 3);
    rr_renderer_begin_path(r); rr_renderer_round_rect(r, -this->width/2, -this->height/2, this->width, this->height, 8);
    rr_renderer_fill(r); rr_renderer_stroke(r);
    rr_shop_text(r, lbl, 0, 0, (id == 10) ? 14 : ((id >= 7) ? 17 : 15), 0xffffffff);
}}

static struct rr_ui_element *make_shop_btn(int id, float x, float y, float w, float h) {{
    struct rr_ui_element *b = rr_ui_element_init();
    struct shop_act_meta *m = malloc(sizeof(struct shop_act_meta));
    m->action_id = id; b->data = m; b->x = x; b->y = y;
    b->abs_width = b->width = w; b->abs_height = b->height = h; b->no_reposition = 1;
    b->animate = act_btn_anim; b->on_event = act_btn_ev; b->on_render = act_btn_rd;
    return b;
}}
"""
with open("Client/Ui/TitleScreen/Shop.c", "w", encoding="utf-8") as f:
    f.write(shop_c)
print("[OK] Шаг 1 готов")
