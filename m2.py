import re
from m1 import MOBS

rm = open("Client/Renderer/RenderMob.c").read()
if "rr_mob_id_bubble" not in rm:
    arr = ",\n".join(f"        {{0x{m[9]:08x}u, 0x{m[10]:08x}u, {m[11]}}}" for m in MOBS)
    blk = f"""    if (mob->id >= rr_mob_id_bubble && mob->id <= rr_mob_id_thalassa_core) {{
        static const struct {{ uint32_t c1; uint32_t c2; uint8_t sh; }} om[] = {{
{arr}
        }};
        uint32_t idx = mob->id - rr_mob_id_bubble;
        uint32_t c1 = om[idx].c1, c2 = om[idx].c2; uint8_t sh = om[idx].sh;
        float r = physical->radius > 8.0f ? physical->radius : 24.0f;
        struct rr_renderer_context_state ost;
        rr_renderer_context_state_init(renderer, &ost);
        rr_renderer_translate(renderer, physical->x, physical->y);
        rr_renderer_rotate(renderer, physical->angle);
        if (sh == 0) {{
            rr_renderer_set_fill(renderer, c1); rr_renderer_set_stroke(renderer, c2); rr_renderer_set_line_width(renderer, 4.0f);
            rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, 0, 0, r); rr_renderer_fill(renderer); rr_renderer_stroke(renderer);
            rr_renderer_set_fill(renderer, c2); rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, -r*0.32f, -r*0.32f, r*0.24f); rr_renderer_fill(renderer);
        }} else if (sh == 1) {{
            rr_renderer_set_stroke(renderer, c2); rr_renderer_set_line_width(renderer, 5.0f);
            for (int k = -1; k <= 1; k++) {{ rr_renderer_begin_path(renderer); rr_renderer_move_to(renderer, k*r*0.35f, -r*1.1f); rr_renderer_line_to(renderer, k*r*0.35f, r*1.1f); rr_renderer_stroke(renderer); }}
            rr_renderer_set_fill(renderer, c2); rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, r*0.85f, -r*0.65f, r*0.35f); rr_renderer_arc(renderer, r*0.85f, r*0.65f, r*0.35f); rr_renderer_fill(renderer);
            rr_renderer_set_fill(renderer, c1); rr_renderer_set_stroke(renderer, 0xff222222); rr_renderer_set_line_width(renderer, 4.0f);
            rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, 0, 0, r*0.85f); rr_renderer_fill(renderer); rr_renderer_stroke(renderer);
        }} else if (sh == 2) {{
            rr_renderer_set_stroke(renderer, c2); rr_renderer_set_line_width(renderer, 4.0f);
            for (int k = -2; k <= 2; k++) {{ rr_renderer_begin_path(renderer); rr_renderer_move_to(renderer, -r*0.3f, k*r*0.28f); rr_renderer_line_to(renderer, -r*1.25f, k*r*0.34f); rr_renderer_stroke(renderer); }}
            rr_renderer_set_fill(renderer, c1); rr_renderer_set_stroke(renderer, c2); rr_renderer_set_line_width(renderer, 4.0f);
            rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, r*0.15f, 0, r*0.85f); rr_renderer_fill(renderer); rr_renderer_stroke(renderer);
        }} else if (sh == 3) {{
            rr_renderer_set_fill(renderer, c1); rr_renderer_set_stroke(renderer, c2); rr_renderer_set_line_width(renderer, 4.0f);
            rr_renderer_begin_path(renderer);
            for (int k = 0; k < 10; k++) {{ float a = k * 0.628318f, rd = (k % 2 == 0) ? r : r * 0.45f; if (k == 0) rr_renderer_move_to(renderer, rd*cosf(a), rd*sinf(a)); else rr_renderer_line_to(renderer, rd*cosf(a), rd*sinf(a)); }}
            rr_renderer_close_path(renderer); rr_renderer_fill(renderer); rr_renderer_stroke(renderer);
        }} else if (sh == 4) {{
            rr_renderer_set_fill(renderer, c1); rr_renderer_set_stroke(renderer, c2); rr_renderer_set_line_width(renderer, 5.0f);
            rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, 0, 0, r*0.92f); rr_renderer_fill(renderer); rr_renderer_stroke(renderer);
            rr_renderer_set_stroke(renderer, c2); rr_renderer_set_line_width(renderer, 3.0f);
            for (int k = -2; k <= 2; k++) {{ rr_renderer_begin_path(renderer); rr_renderer_move_to(renderer, -r*0.7f, 0); rr_renderer_line_to(renderer, r*0.75f, k*r*0.28f); rr_renderer_stroke(renderer); }}
        }} else {{
            rr_renderer_set_fill(renderer, c2); rr_renderer_begin_path(renderer); rr_renderer_move_to(renderer, -r*0.7f, 0); rr_renderer_line_to(renderer, -r*1.35f, -r*0.55f); rr_renderer_line_to(renderer, -r*1.35f, r*0.55f); rr_renderer_close_path(renderer); rr_renderer_fill(renderer);
            rr_renderer_set_fill(renderer, c1); rr_renderer_set_stroke(renderer, 0xff1e293b); rr_renderer_set_line_width(renderer, 4.0f);
            rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, r*0.1f, 0, r*0.85f); rr_renderer_fill(renderer); rr_renderer_stroke(renderer);
            rr_renderer_set_fill(renderer, 0xff0f172a); rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, r*0.45f, -r*0.32f, r*0.14f); rr_renderer_arc(renderer, r*0.45f, r*0.32f, r*0.14f); rr_renderer_fill(renderer);
        }}
        rr_renderer_context_state_free(renderer, &ost);
        return;
    }}
"""
    open("Client/Renderer/RenderMob.c", "w").write(rm.replace("    uint8_t is_friendly =", blk + "\n    uint8_t is_friendly =", 1))

by_t = {t: [m[0] for m in MOBS if m[2] == t] for t in range(11)}
th = [10.0, 18.0, 26.0, 34.0, 42.0, 50.0, 58.0, 65.0, 70.0, 74.0]
wc = ["    if (biome == rr_biome_id_ocean) {"]
for t in range(10):
    mt = by_t[t]
    wc.append(f"        {'if' if t == 0 else 'else if'} (difficulty <= {th[t]}f) {{")
    for i, mid in enumerate(mt[:-1]): wc.append(f"            if (r < {round((i+1)/len(mt), 2)}f) return rr_mob_id_{mid};")
    wc.append(f"            return rr_mob_id_{mt[-1]};\n        }}")
wc.append("        else {")
for i, mid in enumerate(by_t[10][:-1]): wc.append(f"            if (r < {round((i+1)/len(by_t[10]), 2)}f) return rr_mob_id_{mid};")
wc.append(f"            return rr_mob_id_{by_t[10][-1]};\n        }}\n    }}")

wv = re.sub(r"    if \(biome == rr_biome_id_ocean\)\s*\{[\s\S]*?\n    \}", "\n".join(wc), open("Server/Waves.c").read(), count=1)
open("Server/Waves.c", "w").write(wv)
open("Server/Simulation.c", "w").write(open("Server/Simulation.c").read().replace("if (RR_GLOBAL_BIOME != rr_biome_id_ocean) spawn_mob(this, grid_x, grid_y);", "spawn_mob(this, grid_x, grid_y);"))
print("STEP_2_OK")
