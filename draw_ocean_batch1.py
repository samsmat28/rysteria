import re

rm = open("Client/Renderer/RenderMob.c").read()

batch1_code = """    if (mob && physical && mob->id >= rr_mob_id_bubble && mob->id <= rr_mob_id_thalassa_core) {
        float r = physical->radius > 8.0f ? physical->radius : 24.0f;
        struct rr_renderer_context_state ost;
        rr_renderer_context_state_init(renderer, &ost);
        rr_renderer_translate(renderer, physical->x, physical->y);
        rr_renderer_rotate(renderer, physical->angle);

        if (mob->id == rr_mob_id_bubble) {
            rr_renderer_set_fill(renderer, 0x66f8e5b5);
            rr_renderer_set_stroke(renderer, 0xdde8c882);
            rr_renderer_set_line_width(renderer, 3.5f);
            rr_renderer_begin_path(renderer);
            rr_renderer_arc(renderer, 0, 0, r);
            rr_renderer_fill(renderer);
            rr_renderer_stroke(renderer);
            rr_renderer_set_fill(renderer, 0xccffffff);
            rr_renderer_begin_path(renderer);
            rr_renderer_arc(renderer, -r * 0.34f, -r * 0.34f, r * 0.25f);
            rr_renderer_arc(renderer, -r * 0.12f, -r * 0.52f, r * 0.11f);
            rr_renderer_fill(renderer);
            rr_renderer_context_state_free(renderer, &ost);
            return;
        }
        if (mob->id == rr_mob_id_crab) {
            rr_renderer_set_stroke(renderer, 0xff1e2d9e);
            rr_renderer_set_line_width(renderer, 4.5f);
            for (int k = -1; k <= 1; k++) {
                float ox = k * r * 0.32f;
                rr_renderer_begin_path(renderer);
                rr_renderer_move_to(renderer, ox, -r * 0.6f);
                rr_renderer_line_to(renderer, ox - r * 0.15f, -r * 1.15f);
                rr_renderer_move_to(renderer, ox, r * 0.6f);
                rr_renderer_line_to(renderer, ox - r * 0.15f, r * 1.15f);
                rr_renderer_stroke(renderer);
            }
            // Клешни
            rr_renderer_set_fill(renderer, 0xff2b44c9);
            rr_renderer_set_stroke(renderer, 0xff1b2b85);
            rr_renderer_set_line_width(renderer, 3.5f);
            for (int s = -1; s <= 1; s += 2) {
                rr_renderer_begin_path(renderer);
                rr_renderer_arc(renderer, r * 0.82f, s * r * 0.58f, r * 0.34f);
                rr_renderer_fill(renderer);
                rr_renderer_stroke(renderer);
            }
            // Панцирь
            rr_renderer_set_fill(renderer, 0xff3658e8);
            rr_renderer_set_stroke(renderer, 0xff1f3494);
            rr_renderer_set_line_width(renderer, 4.5f);
            rr_renderer_begin_path(renderer);
            rr_renderer_arc(renderer, 0, 0, r * 0.78f);
            rr_renderer_fill(renderer);
            rr_renderer_stroke(renderer);
            // Глаза
            rr_renderer_set_fill(renderer, 0xff111111);
            rr_renderer_begin_path(renderer);
            rr_renderer_arc(renderer, r * 0.55f, -r * 0.24f, r * 0.12f);
            rr_renderer_arc(renderer, r * 0.55f, r * 0.24f, r * 0.12f);
            rr_renderer_fill(renderer);
            rr_renderer_context_state_free(renderer, &ost);
            return;
        }
        if (mob->id == rr_mob_id_jellyfish) {
            rr_renderer_set_stroke(renderer, 0xaae6a8f5);
            rr_renderer_set_line_width(renderer, 3.5f);
            for (int k = -2; k <= 2; k++) {
                float yy = k * r * 0.26f;
                rr_renderer_begin_path(renderer);
                rr_renderer_move_to(renderer, -r * 0.2f, yy);
                rr_renderer_line_to(renderer, -r * 0.75f, yy + ((k % 2 == 0) ? r * 0.12f : -r * 0.12f));
                rr_renderer_line_to(renderer, -r * 1.3f, yy);
                rr_renderer_stroke(renderer);
            }
            rr_renderer_set_fill(renderer, 0xbbd98ae8);
            rr_renderer_set_stroke(renderer, 0xffa855b8);
            rr_renderer_set_line_width(renderer, 4.0f);
            rr_renderer_begin_path(renderer);
            rr_renderer_arc(renderer, r * 0.12f, 0, r * 0.82f);
            rr_renderer_fill(renderer);
            rr_renderer_stroke(renderer);
            rr_renderer_set_fill(renderer, 0x88f5d0fe);
            rr_renderer_begin_path(renderer);
            rr_renderer_arc(renderer, r * 0.24f, 0, r * 0.45f);
            rr_renderer_fill(renderer);
            rr_renderer_context_state_free(renderer, &ost);
            return;
        }
        if (mob->id == rr_mob_id_starfish) {
            rr_renderer_set_fill(renderer, 0xff5a68e0);
            rr_renderer_set_stroke(renderer, 0xff3b47ad);
            rr_renderer_set_line_width(renderer, 4.0f);
            rr_renderer_begin_path(renderer);
            for (int k = 0; k < 10; k++) {
                float a = k * 0.628318f;
                float rd = (k % 2 == 0) ? r * 1.05f : r * 0.42f;
                if (k == 0) rr_renderer_move_to(renderer, rd * cosf(a), rd * sinf(a));
                else rr_renderer_line_to(renderer, rd * cosf(a), rd * sinf(a));
            }
            rr_renderer_fill(renderer);
            rr_renderer_stroke(renderer);
            rr_renderer_set_fill(renderer, 0xff9aa5f5);
            for (int arm = 0; arm < 5; arm++) {
                float a = arm * 1.256637f;
                for (int d = 1; d <= 3; d++) {
                    float dist = r * 0.24f * d;
                    rr_renderer_begin_path(renderer);
                    rr_renderer_arc(renderer, dist * cosf(a), dist * sinf(a), r * 0.07f);
                    rr_renderer_fill(renderer);
                }
            }
            rr_renderer_context_state_free(renderer, &ost);
            return;
        }
        if (mob->id == rr_mob_id_shell) {
            rr_renderer_set_fill(renderer, 0xff9ec2db);
            rr_renderer_set_stroke(renderer, 0xff6e92ab);
            rr_renderer_set_line_width(renderer, 4.5f);
            rr_renderer_begin_path(renderer);
            rr_renderer_arc(renderer, 0, 0, r * 0.9f);
            rr_renderer_fill(renderer);
            rr_renderer_stroke(renderer);
            rr_renderer_set_stroke(renderer, 0xff7fa3bd);
            rr_renderer_set_line_width(renderer, 3.0f);
            for (int k = -2; k <= 2; k++) {
                rr_renderer_begin_path(renderer);
                rr_renderer_move_to(renderer, -r * 0.72f, 0);
                rr_renderer_line_to(renderer, r * 0.76f, k * r * 0.28f);
                rr_renderer_stroke(renderer);
            }
            rr_renderer_set_fill(renderer, 0xffb8d8ed);
            rr_renderer_begin_path(renderer);
            rr_renderer_arc(renderer, -r * 0.65f, 0, r * 0.24f);
            rr_renderer_fill(renderer);
            rr_renderer_context_state_free(renderer, &ost);
            return;
        }
        rr_renderer_context_state_free(renderer, &ost);
    }"""

rm_new, n = re.subn(
    r"    if \(mob && physical && mob->id >= rr_mob_id_bubble && mob->id <= rr_mob_id_thalassa_core\) \{[\s\S]*?rr_renderer_context_state_free\(renderer, &ost\);\n        return;\n    \}",
    batch1_code,
    rm,
    count=1,
)
assert n == 1, "Не найден старый блок RenderMob.c"
open("Client/Renderer/RenderMob.c", "w").write(rm_new)
print("BATCH_1_DRAWN_OK")
