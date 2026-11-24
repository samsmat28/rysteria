#include <Client/Ui/Ui.h>
#include <Client/Ui/Engine.h>
#include <emscripten.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <Client/Assets/RenderFunctions.h>
#include <Client/Game.h>
#include <Client/InputData.h>
#include <Client/Renderer/Renderer.h>
#include <Shared/Utilities.h>

extern uint64_t rr_ui_r_coins;
extern uint8_t rr_ui_q_rar;
extern uint16_t rr_ui_q_tgt, rr_ui_q_prg;
extern uint64_t rr_ui_ch_lo, rr_ui_ch_hi, rr_ui_play_sec;
extern void rr_send_shop_op(struct rr_game *this, uint8_t op, uint8_t a1, uint8_t a2);

static int shop_tab = 0, shop_rar = 3, shop_page = 0;
static const uint64_t SELL_P[11] = { 5, 15, 40, 120, 350, 1000, 3000, 9000, 25000, 75000, 200000 };
static const uint64_t Q_REW[11]  = { 40, 100, 250, 700, 2000, 6000, 18000, 50000, 150000, 400000, 1000000 };

static void stxt(struct rr_renderer *r, const char *t, float x, float y, float sz, uint32_t col, int align) {
    rr_renderer_set_text_baseline(r, 1); rr_renderer_set_text_align(r, align); rr_renderer_set_text_size(r, sz);
    rr_renderer_set_fill(r, col); rr_renderer_set_stroke(r, 0xff111111); rr_renderer_set_line_width(r, sz * 0.14f);
    rr_renderer_stroke_text(r, t, x, y); rr_renderer_fill_text(r, t, x, y);
}

static void shop_btn_ev(struct rr_ui_element *this, struct rr_game *g) {
    if (g->input_data->mouse_buttons_up_this_tick & 1) {
        if (g->pressed != this) return;
        g->menu_open = (g->menu_open == rr_game_menu_shop) ? rr_game_menu_none : rr_game_menu_shop;
        if (g->menu_open == rr_game_menu_shop) { shop_page = 0; rr_send_shop_op(g, 0, 0, 0); }
    }
}

static void shop_btn_rd(struct rr_ui_element *this, struct rr_game *g) {
    struct rr_renderer *r = g->renderer; rr_renderer_scale(r, r->scale);
    rr_renderer_set_fill(r, (g->focused == this || g->menu_open == rr_game_menu_shop) ? 0xfff39c12 : 0xffd98a1c);
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
static uint8_t shop_win_show(struct rr_ui_element *this, struct rr_game *g) { (void)this; return g->menu_open == rr_game_menu_shop; }
static void shop_win_anim(struct rr_ui_element *this, struct rr_game *g) { (void)g; this->width = this->abs_width; this->height = this->abs_height; }

static int collect_sell_items(struct rr_game *g, uint8_t *pids, uint8_t *rids, int max_n) {
    int n = 0;
    for (int p = 1; p < rr_petal_id_max && n < max_n; p++)
        for (int r = 0; r < rr_rarity_id_max && n < max_n; r++)
            if (g->inventory[p][r] > 0) { pids[n] = (uint8_t)p; rids[n] = (uint8_t)r; n++; }
    return n;
}
static void quest_desc(int q, char *buf, size_t sz) {
    static const char *tm[20] = {
        "Play 1 min","Play 3 min","Play 5 min","Play 10 min","Play 20 min",
        "Play 30 min","Play 45 min","Play 1 hour","Play 2 hours","Play 3 hours",
        "Play 5 hours","Play 8 hours","Play 12 hours","Play 1 day","Play 3 days",
        "Play 7 days","Play 14 days","Play 30 days","Play 60 days","Play 100 days"
    };
    static const uint32_t xp[20] = {
        500,1200,2500,5000,10000,18000,30000,45000,65000,90000,
        120000,160000,210000,270000,350000,450000,570000,700000,850000,1000000
    };
    static const int em[8] = {5,15,30,60,100,200,350,500};
    static const int lm[8] = {3,10,20,40,75,125,200,300};
    static const int mm[7] = {1,5,15,30,60,100,150};
    static const int um[7] = {1,3,10,20,40,70,100};
    if (q <= 20) snprintf(buf, sz, "#%d: %s online", q, tm[q-1]);
    else if (q <= 40) snprintf(buf, sz, "#%d: Reach %u XP", q, xp[q-21]);
    else if (q <= 48) snprintf(buf, sz, "#%d: Kill %d Epic mobs", q, em[q-41]);
    else if (q <= 56) snprintf(buf, sz, "#%d: Kill %d Legendary mobs", q, lm[q-49]);
    else if (q <= 63) snprintf(buf, sz, "#%d: Kill %d Mythic mobs", q, mm[q-57]);
    else if (q <= 70) snprintf(buf, sz, "#%d: Kill %d Ultra+ mobs", q, um[q-64]);
    else if (q <= 80) snprintf(buf, sz, "#%d: Own %d Epic+ petals", q, (q-70)*3);
    else if (q <= 90) snprintf(buf, sz, "#%d: Own %d Mythic+ petals", q, q-80);
    else snprintf(buf, sz, "#%d: Kill %d of ALL 45 species", q, (q-90)*100);
}

static void shop_win_ev(struct rr_ui_element *this, struct rr_game *g) {
    (void)this;
    if (g->menu_open != rr_game_menu_shop) return;
    if (!(g->input_data->mouse_buttons_up_this_tick & 1)) return;
    float s = g->renderer->scale > 0.0f ? g->renderer->scale : 1.0f;
    float tx = g->input_data->touches[0].touch_x, ty = g->input_data->touches[0].touch_y;
    if (tx == 0.0f && ty == 0.0f) { tx = g->input_data->mouse_x; ty = g->input_data->mouse_y; }
    float mx = (tx - g->renderer->width * 0.5f) / s, my = (ty - g->renderer->height * 0.5f) / s;

    if (my >= -176.0f && my <= -140.0f) {
        if (mx >= -285.0f && mx <= -100.0f) { shop_tab = 0; shop_page = 0; return; }
        if (mx >= -92.0f && mx <= 92.0f)    { shop_tab = 1; shop_page = 0; return; }
        if (mx >= 100.0f && mx <= 285.0f)   { shop_tab = 2; shop_page = 0; rr_send_shop_op(g, 0, 0, 0); return; }
    }
    if (my >= 170.0f && my <= 206.0f) {
        if (mx >= -150.0f && mx <= -40.0f && shop_page > 0) { shop_page--; return; }
        if (mx >= 40.0f && mx <= 150.0f) { shop_page++; return; }
    }
    if (shop_tab == 0) {
        if (my >= -134.0f && my <= -104.0f) {
            for (int r = 0; r < 8; r++) {
                float bx = -280.0f + r * 71.0f;
                if (mx >= bx && mx <= bx + 67.0f) { shop_rar = r; return; }
            }
        }
        int start_p = 1 + shop_page * 12;
        for (int idx = 0; idx < 12; idx++) {
            int pid = start_p + idx;
            if (pid >= rr_petal_id_max) break;
            float cx = -215.0f + (idx % 4) * 143.0f, cy = -55.0f + (idx / 4) * 82.0f;
            if (mx >= cx - 65.0f && mx <= cx + 65.0f && my >= cy - 36.0f && my <= cy + 36.0f) {
                rr_send_shop_op(g, 1, (uint8_t)pid, (uint8_t)shop_rar); return;
            }
        }
    } else if (shop_tab == 1) {
        uint8_t pids[256], rids[256];
        int total = collect_sell_items(g, pids, rids, 256), start = shop_page * 12;
        for (int idx = 0; idx < 12 && (start + idx) < total; idx++) {
            float cx = -215.0f + (idx % 4) * 143.0f, cy = -65.0f + (idx / 4) * 86.0f;
            if (mx >= cx - 65.0f && mx <= cx + 65.0f && my >= cy - 38.0f && my <= cy + 38.0f) {
                rr_send_shop_op(g, 2, pids[start + idx], rids[start + idx]); return;
            }
        }
    } else if (shop_tab == 2) {
        if (my >= -134.0f && my <= -94.0f && mx >= 120.0f && mx <= 280.0f) { rr_send_shop_op(g, 4, 0, 0); return; }
        int start_q = 1 + shop_page * 6;
        for (int i = 0; i < 6; i++) {
            int qid = start_q + i;
            if (qid > 100) break;
            float qy = -68.0f + i * 40.0f;
            if (my >= qy - 16.0f && my <= qy + 16.0f && mx >= 135.0f && mx <= 280.0f) {
                rr_send_shop_op(g, 3, (uint8_t)qid, 0); return;
            }
        }
    }
}
static void shop_win_rd(struct rr_ui_element *this, struct rr_game *g) {
    (void)this; struct rr_renderer *r = g->renderer; rr_renderer_scale(r, r->scale);
    rr_renderer_set_fill(r, 0xf01c130b); rr_renderer_set_stroke(r, 0xfff5c542); rr_renderer_set_line_width(r, 5);
    rr_renderer_begin_path(r); rr_renderer_round_rect(r, -300, -215, 600, 430, 14);
    rr_renderer_fill(r); rr_renderer_stroke(r);

    char hdr[64]; snprintf(hdr, sizeof(hdr), "RYSTERIA SHOP  |  BALANCE: %llu R", (unsigned long long)rr_ui_r_coins);
    stxt(r, hdr, 0, -194, 17, 0xffffd700, 1);

    const char *tabs[3] = { "BUY PETALS", "SELL INVENTORY", "QUESTS (100)" };
    for (int t = 0; t < 3; t++) {
        float bx = -285.0f + t * 192.0f;
        rr_renderer_set_fill(r, (shop_tab == t) ? 0xffd98a1c : 0xff3b2716);
        rr_renderer_begin_path(r); rr_renderer_round_rect(r, bx, -175, 185, 32, 8); rr_renderer_fill(r);
        stxt(r, tabs[t], bx + 92.5f, -159, 13, 0xffffffff, 1);
    }

    if (shop_tab == 0) {
        const char *rn[8] = { "Com", "Unu", "Rar", "Epic", "Leg", "Myth", "Exot", "Anc" };
        for (int rr = 0; rr < 8; rr++) {
            float bx = -280.0f + rr * 71.0f;
            rr_renderer_set_fill(r, (shop_rar == rr) ? 0xff2e8b57 : 0xff2a1c10);
            rr_renderer_begin_path(r); rr_renderer_round_rect(r, bx, -133, 67, 26, 6); rr_renderer_fill(r);
            stxt(r, rn[rr], bx + 33.5f, -120, 11, 0xffffffff, 1);
        }
        int start_p = 1 + shop_page * 12;
        if (start_p >= rr_petal_id_max) { shop_page = 0; start_p = 1; }
        for (int idx = 0; idx < 12 && (start_p + idx) < rr_petal_id_max; idx++) {
            int pid = start_p + idx;
            float cx = -215.0f + (idx % 4) * 143.0f, cy = -55.0f + (idx / 4) * 82.0f;
            uint64_t cost = (pid == 62 && shop_rar == 3) ? 100 : (SELL_P[shop_rar] * 2);
            rr_renderer_set_fill(r, 0xff2b1c10); rr_renderer_set_stroke(r, (rr_ui_r_coins >= cost) ? 0xff7eef6d : 0xff6e4209);
            rr_renderer_set_line_width(r, 2.5f); rr_renderer_begin_path(r);
            rr_renderer_round_rect(r, cx - 65, cy - 36, 130, 72, 8); rr_renderer_fill(r); rr_renderer_stroke(r);
            rr_renderer_save(r); rr_renderer_translate(r, cx, cy - 8); rr_renderer_scale(r, 0.58f);
            rr_renderer_draw_petal_with_name(r, (uint8_t)pid, (uint8_t)shop_rar); rr_renderer_restore(r);
            char pr[32]; snprintf(pr, sizeof(pr), "BUY: %llu R", (unsigned long long)cost);
            stxt(r, pr, cx, cy + 25, 11, (rr_ui_r_coins >= cost) ? 0xff7eef6d : 0xffff8787, 1);
        }
    } else if (shop_tab == 1) {
        uint8_t pids[256], rids[256];
        int total = collect_sell_items(g, pids, rids, 256);
        if (total == 0) stxt(r, "Your inventory is empty!", 0, 0, 18, 0xffcbd5e1, 1);
        else {
            int start = shop_page * 12;
            if (start >= total) { shop_page = 0; start = 0; }
            for (int idx = 0; idx < 12 && (start + idx) < total; idx++) {
                uint8_t pid = pids[start + idx], rid = rids[start + idx];
                float cx = -215.0f + (idx % 4) * 143.0f, cy = -65.0f + (idx / 4) * 86.0f;
                rr_renderer_set_fill(r, 0xff2b1c10); rr_renderer_set_stroke(r, 0xff4fc3f7);
                rr_renderer_set_line_width(r, 2.5f); rr_renderer_begin_path(r);
                rr_renderer_round_rect(r, cx - 65, cy - 38, 130, 76, 8); rr_renderer_fill(r); rr_renderer_stroke(r);
                rr_renderer_save(r); rr_renderer_translate(r, cx, cy - 10); rr_renderer_scale(r, 0.58f);
                rr_renderer_draw_petal_with_name(r, pid, rid); rr_renderer_restore(r);
                char sl[40]; snprintf(sl, sizeof(sl), "x%u SELL +%llu R", g->inventory[pid][rid], (unsigned long long)SELL_P[rid]);
                stxt(r, sl, cx, cy + 27, 10.5f, 0xffffe066, 1);
            }
        }
    } else if (shop_tab == 2) {
        rr_renderer_set_fill(r, 0xff162914); rr_renderer_set_stroke(r, 0xff7eef6d); rr_renderer_set_line_width(r, 2.5f);
        rr_renderer_begin_path(r); rr_renderer_round_rect(r, -285, -134, 570, 38, 8); rr_renderer_fill(r); rr_renderer_stroke(r);
        uint8_t qr = rr_ui_q_rar < 11 ? rr_ui_q_rar : 0;
        char qh[96]; snprintf(qh, sizeof(qh), "HUNT: Kill %u/%u %s mobs (+%llu R)", rr_ui_q_prg, rr_ui_q_tgt, RR_RARITY_NAMES[qr], (unsigned long long)Q_REW[qr]);
        stxt(r, qh, -272, -115, 13, 0xffeaffdf, 0);
        int hok = (rr_ui_q_tgt > 0 && rr_ui_q_prg >= rr_ui_q_tgt);
        rr_renderer_set_fill(r, hok ? 0xff2ecc71 : 0xff3b4d3a); rr_renderer_begin_path(r);
        rr_renderer_round_rect(r, 125, -129, 150, 28, 6); rr_renderer_fill(r);
        stxt(r, hok ? "CLAIM HUNT!" : "IN PROGRESS", 200, -115, 12, 0xffffffff, 1);

        int start_q = 1 + shop_page * 6;
        if (start_q > 100) { shop_page = 0; start_q = 1; }
        for (int i = 0; i < 6 && (start_q + i) <= 100; i++) {
            int qid = start_q + i, bit = qid - 1; float qy = -68.0f + i * 40.0f;
            int cl = (bit < 64) ? ((rr_ui_ch_lo >> bit) & 1) : ((rr_ui_ch_hi >> (bit - 64)) & 1);
            uint64_t rew = (uint64_t)(100 + qid * 50 + ((qid % 10 == 0) ? (qid * 100) : 0));
            rr_renderer_set_fill(r, cl ? 0xff1c241d : 0xff132230); rr_renderer_begin_path(r);
            rr_renderer_round_rect(r, -285, qy - 16, 570, 32, 6); rr_renderer_fill(r);
            char desc[80]; quest_desc(qid, desc, sizeof(desc));
            stxt(r, desc, -272, qy, 12.5f, cl ? 0xff889988 : 0xffffffff, 0);
            char bt[32]; if (cl) strcpy(bt, "CLAIMED"); else snprintf(bt, sizeof(bt), "CLAIM +%llu R", (unsigned long long)rew);
            rr_renderer_set_fill(r, cl ? 0xff333333 : 0xff2980b9); rr_renderer_begin_path(r);
            rr_renderer_round_rect(r, 135, qy - 13, 140, 26, 6); rr_renderer_fill(r);
            stxt(r, bt, 205, qy, 11, cl ? 0xffaaaaaa : 0xffffffff, 1);
        }
    }
    rr_renderer_set_fill(r, 0xff3b2716); rr_renderer_begin_path(r);
    rr_renderer_round_rect(r, -150, 172, 100, 30, 7); rr_renderer_round_rect(r, 50, 172, 100, 30, 7); rr_renderer_fill(r);
    stxt(r, "< PREV", -100, 187, 12, 0xffffffff, 1); stxt(r, "NEXT >", 100, 187, 12, 0xffffffff, 1);
    char pg[24]; snprintf(pg, sizeof(pg), "Page %d", shop_page + 1); stxt(r, pg, 0, 187, 12, 0xffffe066, 1);
}

struct rr_ui_element *rr_ui_shop_container_init(struct rr_game *g) {
    (void)g; struct rr_ui_element *this = rr_ui_element_init();
    this->abs_width = this->width = 600; this->abs_height = this->height = 430;
    this->animate = shop_win_anim; this->should_show = shop_win_show;
    this->on_event = shop_win_ev; this->on_render = shop_win_rd; return this;
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
    rr_renderer_set_fill(r, a_bg | 0x00132618); rr_renderer_set_stroke(r, a_fg | 0x007eef6d);
    rr_renderer_set_line_width(r, 3.0f); rr_renderer_begin_path(r);
    rr_renderer_round_rect(r, bx, by, 196.0f, 36.0f, 10.0f); rr_renderer_fill(r); rr_renderer_stroke(r);
    rr_renderer_set_fill(r, a_fg | 0x007eef6d); rr_renderer_begin_path(r); rr_renderer_arc(r, bx + 20.0f, by + 18.0f, 6.0f); rr_renderer_fill(r);
    rr_renderer_set_text_baseline(r, 1); rr_renderer_set_text_align(r, 0); rr_renderer_set_text_size(r, 14.0f);
    rr_renderer_set_fill(r, a_fg | 0x00eaffdf); rr_renderer_fill_text(r, "AUTO-SAVED", bx + 34.0f, by + 18.0f);
    rr_renderer_restore(r);
}
