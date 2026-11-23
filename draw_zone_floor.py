with open("Client/Renderer/RenderArena.c", "r", encoding="utf-8") as f:
    ra = f.read()

target = "if (this->cache.show_coordinates && nx % 2 && currY % 2)"

floor_zones = """if (nx >= 0 && nx < maze_dim && currY >= 0 && currY < maze_dim && grid[currY * maze_dim + nx].value == 1)
            {
                uint8_t r_cur = grid[currY * maze_dim + nx].difficulty / 8;
                if (r_cur >= rr_rarity_id_max) r_cur = rr_rarity_id_max - 1;
                uint8_t r_left = (nx > 0 && grid[currY * maze_dim + (nx - 1)].value == 1) ? (grid[currY * maze_dim + (nx - 1)].difficulty / 8) : r_cur;
                uint8_t r_top = (currY > 0 && grid[(currY - 1) * maze_dim + nx].value == 1) ? (grid[(currY - 1) * maze_dim + nx].difficulty / 8) : r_cur;
                if (r_left >= rr_rarity_id_max) r_left = rr_rarity_id_max - 1;
                if (r_top >= rr_rarity_id_max) r_top = rr_rarity_id_max - 1;

                if (r_cur != r_left)
                {
                    uint8_t hi = r_cur > r_left ? r_cur : r_left;
                    float lx = nx * grid_size;
                    float ly = currY * grid_size;
                    rr_renderer_set_stroke(renderer, RR_RARITY_COLORS[hi]);
                    rr_renderer_set_line_width(renderer, 10.0f);
                    rr_renderer_begin_path(renderer);
                    rr_renderer_move_to(renderer, lx, ly);
                    rr_renderer_line_to(renderer, lx, ly + grid_size);
                    rr_renderer_stroke(renderer);

                    rr_renderer_set_fill(renderer, RR_RARITY_COLORS[hi]);
                    rr_renderer_set_stroke(renderer, 0xff1a1a1a);
                    rr_renderer_set_line_width(renderer, 6.0f);
                    rr_renderer_set_text_size(renderer, 68);
                    rr_renderer_set_text_align(renderer, 1);
                    rr_renderer_set_text_baseline(renderer, 1);
                    float tx = (r_cur > r_left) ? (lx + grid_size * 0.45f) : (lx - grid_size * 0.45f);
                    float ty = ly + grid_size * 0.5f;
                    rr_renderer_stroke_text(renderer, RR_RARITY_NAMES[hi], tx, ty);
                    rr_renderer_fill_text(renderer, RR_RARITY_NAMES[hi], tx, ty);
                }
                if (r_cur != r_top)
                {
                    uint8_t hi = r_cur > r_top ? r_cur : r_top;
                    float lx = nx * grid_size;
                    float ly = currY * grid_size;
                    rr_renderer_set_stroke(renderer, RR_RARITY_COLORS[hi]);
                    rr_renderer_set_line_width(renderer, 10.0f);
                    rr_renderer_begin_path(renderer);
                    rr_renderer_move_to(renderer, lx, ly);
                    rr_renderer_line_to(renderer, lx + grid_size, ly);
                    rr_renderer_stroke(renderer);

                    rr_renderer_set_fill(renderer, RR_RARITY_COLORS[hi]);
                    rr_renderer_set_stroke(renderer, 0xff1a1a1a);
                    rr_renderer_set_line_width(renderer, 6.0f);
                    rr_renderer_set_text_size(renderer, 68);
                    rr_renderer_set_text_align(renderer, 1);
                    rr_renderer_set_text_baseline(renderer, 1);
                    float tx = lx + grid_size * 0.5f;
                    float ty = (r_cur > r_top) ? (ly + grid_size * 0.45f) : (ly - grid_size * 0.45f);
                    rr_renderer_stroke_text(renderer, RR_RARITY_NAMES[hi], tx, ty);
                    rr_renderer_fill_text(renderer, RR_RARITY_NAMES[hi], tx, ty);
                }
            }
            """ + target

assert target in ra, "Не найдена строка show_coordinates в RenderArena.c"
if "RR_RARITY_NAMES[hi]" not in ra:
    ra = ra.replace(target, floor_zones, 1)
    with open("Client/Renderer/RenderArena.c", "w", encoding="utf-8") as f:
        f.write(ra)
print("Цветные линии редкости и крупные надписи зон на полу добавлены!")
