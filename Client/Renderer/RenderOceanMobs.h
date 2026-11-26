#pragma once
static const struct { uint32_t c1, c2, c3; uint8_t a, p; } RR_OCEAN_ART[55] = {
    {0x66f8e5b5u,0xdde8c882u,0xccffffffu,0,1},
    {0xff2b44c9u,0xff1b2b85u,0xff5a75ffu,1,0},
    {0xbbd98ae8u,0xffa855b8u,0x88f5d0feu,2,5},
    {0xff5a68e0u,0xff3b47adu,0xff9aa5f5u,3,5},
    {0xff9ec2dbu,0xff6e92abu,0xffc7e2f5u,4,0},
    {0xff1673f9u,0xff0d47a1u,0xffffffffu,5,3},
    {0xff15ccfau,0xff0c58eau,0xff8af0ffu,5,0},
    {0xff871c58u,0xff4a0d30u,0xfff755a8u,6,12},
    {0xff3c92fbu,0xff1d4ed8u,0xffaad7feu,5,0},
    {0xaa99d334u,0xff15803du,0xffd0f3a7u,0,2},
    {0xfff8bd38u,0xff0369a1u,0xff47e0fdu,7,4},
    {0xff24bffbu,0xff0f3578u,0xff99e5ffu,6,10},
    {0xff0953b4u,0xff451a03u,0xff4444efu,1,1},
    {0xff5e3ff4u,0xff881337u,0xffbfd42du,8,0},
    {0xffc78402u,0xff1e3a8au,0xfffde6bau,5,0},
    {0xff3d8015u,0xff052e16u,0xff64f2beu,7,0},
    {0xff695547u,0xff1e293bu,0xfff8bd38u,9,1},
    {0xff1c1cb9u,0xff450a0au,0xffa5a5fcu,1,2},
    {0xff8b7464u,0xff1e293bu,0xfff0e8e2u,5,0},
    {0xff346516u,0xff052e16u,0xffacef86u,8,0},
    {0xffea3393u,0xff4c1d95u,0xfff979e8u,2,8},
    {0xff481de1u,0xff881337u,0xffafa4fdu,2,6},
    {0xffd84e1du,0xff172554u,0xfffdc593u,10,0},
    {0xff3b291eu,0xff020617u,0xfff8bd38u,9,2},
    {0xffeb6325u,0xff1e3a8au,0xff8af0feu,7,1},
    {0xff4b1b1eu,0xff090d16u,0xff8af0feu,11,0},
    {0xff63554bu,0xff1f2937u,0xffaf9ca3u,5,0},
    {0xff0677d9u,0xff78350fu,0xffc7f3feu,4,0},
    {0xff2626dcu,0xff7f1d1du,0xffffffffu,6,14},
    {0xfff6823bu,0xff1d4ed8u,0xfffef2e0u,10,0},
    {0xff554133u,0xff0f172au,0xfffcfaf8u,5,1},
    {0xff2a170fu,0xff020617u,0xffffffffu,5,3},
    {0xff1b1b99u,0xff450a0au,0xff24bffbu,1,3},
    {0xdd951d4cu,0xff2e1065u,0xffeed322u,2,7},
    {0xff465f06u,0xff022c22u,0xff99d334u,7,2},
    {0xff5d18beu,0xff500724u,0xffe8cffbu,12,6},
    {0xff3b291eu,0xff090d16u,0xff4444efu,5,2},
    {0xff871c58u,0xff2e1065u,0xfffc84c0u,2,10},
    {0xff0f3578u,0xff451a03u,0xff8af0feu,4,1},
    {0xff6e760fu,0xff042f2eu,0xffd4ea5eu,7,0},
    {0xffa16903u,0xff082f49u,0xfffcd37du,7,3},
    {0xffd84e1du,0xff172554u,0xff15ccfau,1,3},
    {0xff4b1b1eu,0xff090d16u,0xfff755a8u,9,3},
    {0xff4a4e13u,0xff042f2eu,0xffbfd42du,8,1},
    {0xff64073bu,0xff1e1b4bu,0xfff8bd38u,12,9},
    {0xff160d09u,0xff020617u,0xff5e3ff4u,5,3},
    {0xff3b4e06u,0xff022c22u,0xff47e0fdu,7,3},
    {0xff8a3a1eu,0xff172554u,0xff8af0feu,5,3},
    {0xff751a70u,0xff3b0764u,0xfffcabf0u,4,0},
    {0xff170602u,0xff000000u,0xff4444efu,7,1},
    {0xff6e4a0cu,0xff082f49u,0xff15ccfau,8,0},
    {0xff65102eu,0xff1e1b4bu,0xffb672f4u,12,12},
    {0xff031a45u,0xff1c0a00u,0xff8af0feu,4,1},
    {0xff371388u,0xff4c0519u,0xff8571fbu,3,7},
    {0xff443308u,0xff042f2eu,0xffeed322u,8,0}
};
static inline void rr_draw_ocean_mob(struct rr_renderer *renderer, uint8_t mob_id, float x, float y, float angle, float radius) {
    uint32_t idx = (uint32_t)(mob_id - rr_mob_id_bubble);
    if (idx >= 55) return;
    uint32_t c1 = RR_OCEAN_ART[idx].c1, c2 = RR_OCEAN_ART[idx].c2, c3 = RR_OCEAN_ART[idx].c3;
    uint8_t a = RR_OCEAN_ART[idx].a, p = RR_OCEAN_ART[idx].p;
    float r = radius > 8.0f ? radius : 24.0f;
    struct rr_renderer_context_state ost;
    rr_renderer_context_state_init(renderer, &ost);
    rr_renderer_translate(renderer, x, y);
    rr_renderer_rotate(renderer, angle);
    if (a == 0) {
        rr_renderer_set_fill(renderer, c1); rr_renderer_set_stroke(renderer, c2); rr_renderer_set_line_width(renderer, 3.5f);
        rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, 0, 0, r); rr_renderer_fill(renderer); rr_renderer_stroke(renderer);
        rr_renderer_set_fill(renderer, c3); rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, -r*0.33f, -r*0.33f, r*0.24f); rr_renderer_fill(renderer);
    } else if (a == 1) {
        rr_renderer_set_stroke(renderer, c2); rr_renderer_set_line_width(renderer, 4.5f);
        for (int k = -1; k <= 1; k++) { rr_renderer_begin_path(renderer); rr_renderer_move_to(renderer, k*r*0.32f, -r*1.1f); rr_renderer_line_to(renderer, k*r*0.32f, r*1.1f); rr_renderer_stroke(renderer); }
        rr_renderer_set_fill(renderer, c3); rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, r*0.82f, -r*0.58f, r*0.34f); rr_renderer_arc(renderer, r*0.82f, r*0.58f, r*0.34f); rr_renderer_fill(renderer);
        rr_renderer_set_fill(renderer, c1); rr_renderer_set_stroke(renderer, c2); rr_renderer_set_line_width(renderer, 4.5f);
        rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, 0, 0, r*0.78f); rr_renderer_fill(renderer); rr_renderer_stroke(renderer);
        rr_renderer_set_fill(renderer, 0xff111111); rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, r*0.54f, -r*0.24f, r*0.12f); rr_renderer_arc(renderer, r*0.54f, r*0.24f, r*0.12f); rr_renderer_fill(renderer);
    } else if (a == 2 || a == 12) {
        int tc = p > 0 ? p : 5;
        rr_renderer_set_stroke(renderer, c3); rr_renderer_set_line_width(renderer, 3.5f);
        for (int k = 0; k < tc; k++) { float yy = ((k / (float)(tc > 1 ? tc - 1 : 1)) - 0.5f) * r * 1.15f; rr_renderer_begin_path(renderer); rr_renderer_move_to(renderer, -r*0.2f, yy); rr_renderer_line_to(renderer, -r*1.35f, yy); rr_renderer_stroke(renderer); }
        rr_renderer_set_fill(renderer, c1); rr_renderer_set_stroke(renderer, c2); rr_renderer_set_line_width(renderer, 4.0f);
        rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, r*0.12f, 0, r*0.82f); rr_renderer_fill(renderer); rr_renderer_stroke(renderer);
        rr_renderer_set_fill(renderer, c3); rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, r*0.24f, 0, r*0.42f); rr_renderer_fill(renderer);
    }
    else if (a == 3) {
        int arms = p > 0 ? p : 5;
        rr_renderer_set_fill(renderer, c1); rr_renderer_set_stroke(renderer, c2); rr_renderer_set_line_width(renderer, 4.0f);
        rr_renderer_begin_path(renderer);
        for (int k = 0; k < arms * 2; k++) { float ang = k * 3.1415926f / (float)arms, rd = (k % 2 == 0) ? r * 1.05f : r * 0.42f; if (k == 0) rr_renderer_move_to(renderer, rd*cosf(ang), rd*sinf(ang)); else rr_renderer_line_to(renderer, rd*cosf(ang), rd*sinf(ang)); }
        rr_renderer_fill(renderer); rr_renderer_stroke(renderer);
        rr_renderer_set_fill(renderer, c3);
        for (int arm = 0; arm < arms; arm++) { float ang = arm * 6.283185f / (float)arms; for (int d = 1; d <= 3; d++) { rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, r*0.24f*d*cosf(ang), r*0.24f*d*sinf(ang), r*0.07f); rr_renderer_fill(renderer); } }
    } else if (a == 4) {
        rr_renderer_set_fill(renderer, c1); rr_renderer_set_stroke(renderer, c2); rr_renderer_set_line_width(renderer, 4.5f);
        rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, 0, 0, r*0.92f); rr_renderer_fill(renderer); rr_renderer_stroke(renderer);
        rr_renderer_set_stroke(renderer, c2); rr_renderer_set_line_width(renderer, 3.0f);
        for (int k = -2; k <= 2; k++) { rr_renderer_begin_path(renderer); rr_renderer_move_to(renderer, -r*0.72f, 0); rr_renderer_line_to(renderer, r*0.76f, k*r*0.28f); rr_renderer_stroke(renderer); }
    } else if (a == 6 || a == 8) {
        int sp = (a == 6) ? (p > 0 ? p : 12) : 6;
        rr_renderer_set_stroke(renderer, c3); rr_renderer_set_line_width(renderer, 4.0f);
        for (int k = 0; k < sp; k++) { float ang = k * 6.283185f / (float)sp; rr_renderer_begin_path(renderer); rr_renderer_move_to(renderer, r*0.4f*cosf(ang), r*0.4f*sinf(ang)); rr_renderer_line_to(renderer, r*1.15f*cosf(ang), r*1.15f*sinf(ang)); rr_renderer_stroke(renderer); }
        rr_renderer_set_fill(renderer, c1); rr_renderer_set_stroke(renderer, c2); rr_renderer_set_line_width(renderer, 4.0f);
        rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, 0, 0, r*0.76f); rr_renderer_fill(renderer); rr_renderer_stroke(renderer);
    } else if (a == 7) {
        for (int s = 3; s >= 0; s--) { float sx = -s*r*0.34f, sy = sinf(s*1.1f)*r*0.22f, sr = r*(0.68f - s*0.1f); rr_renderer_set_fill(renderer, (s%2==0)?c1:c3); rr_renderer_set_stroke(renderer, c2); rr_renderer_set_line_width(renderer, 3.5f); rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, sx, sy, sr); rr_renderer_fill(renderer); rr_renderer_stroke(renderer); }
    } else {
        rr_renderer_set_fill(renderer, c3); rr_renderer_begin_path(renderer); rr_renderer_move_to(renderer, -r*0.65f, 0); rr_renderer_line_to(renderer, -r*1.38f, -r*0.58f); rr_renderer_line_to(renderer, -r*1.38f, r*0.58f); rr_renderer_fill(renderer);
        if (a == 10 || a == 11) { rr_renderer_set_stroke(renderer, c3); rr_renderer_set_line_width(renderer, 5.0f); rr_renderer_begin_path(renderer); rr_renderer_move_to(renderer, r*0.7f, 0); rr_renderer_line_to(renderer, r*1.5f, 0); rr_renderer_stroke(renderer); }
        rr_renderer_set_fill(renderer, c1); rr_renderer_set_stroke(renderer, c2); rr_renderer_set_line_width(renderer, 4.0f);
        rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, r*0.1f, 0, r*0.84f); rr_renderer_fill(renderer); rr_renderer_stroke(renderer);
        rr_renderer_set_fill(renderer, 0xffffffff); rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, r*0.48f, -r*0.3f, r*0.15f); rr_renderer_arc(renderer, r*0.48f, r*0.3f, r*0.15f); rr_renderer_fill(renderer);
    }
    rr_renderer_context_state_free(renderer, &ost);
}
