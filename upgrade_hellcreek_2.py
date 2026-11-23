with open("Client/Renderer/RenderArena.c", "r", encoding="utf-8") as f:
    arena = f.read()

old_hc_tile = """        else if (this->selected_biome == rr_biome_id_hell_creek)
            rr_renderer_draw_tile_hell_creek(renderer, tile_index);"""

new_hc_tile = """        else if (this->selected_biome == rr_biome_id_hell_creek)
        {
            uint32_t h = rr_get_hash(((uint32_t)((newLeftX + 8192) / GRID_SIZE) * 2654435761u) ^ ((uint32_t)((currY + 8192) / GRID_SIZE) * 2246822519u));

            // Теплая доисторическая почва мелового периода
            rr_renderer_set_fill(renderer, 0xff755338);
            rr_renderer_begin_path(renderer);
            rr_renderer_rect(renderer, -128, -128, 256, 256);
            rr_renderer_fill(renderer);

            // Мелкие песчано-земляные гранулы
            rr_renderer_set_fill(renderer, 0xff66462e);
            for (int i = 0; i < 4; i++) {
                uint32_t sh = rr_get_hash(h + (uint32_t)(i * 137));
                float px = (float)((int)(sh % 210) - 105);
                float py = (float)((int)((sh >> 8) % 210) - 105);
                rr_renderer_begin_path(renderer);
                rr_renderer_arc(renderer, px, py, 2.5f + (float)((sh >> 16) % 3));
                rr_renderer_fill(renderer);
            }

            // Камешки с темным контуром (на 60% тайлов)
            if ((h % 100) < 60) {
                float sx = (float)((int)((h >> 4) % 170) - 85);
                float sy = (float)((int)((h >> 12) % 170) - 85);
                float sr = 5.0f + (float)((h >> 20) % 5);
                rr_renderer_set_fill(renderer, 0xff4d3421);
                rr_renderer_begin_path(renderer);
                rr_renderer_arc(renderer, sx, sy + 1.5f, sr + 1.4f);
                rr_renderer_fill(renderer);
                rr_renderer_set_fill(renderer, (h & 1) ? 0xff5f422b : 0xff694930);
                rr_renderer_begin_path(renderer);
                rr_renderer_arc(renderer, sx, sy, sr);
                rr_renderer_fill(renderer);
            }

            // Веточка древнего папоротника на земле (на 28% тайлов)
            if (((h >> 3) % 100) < 28) {
                float fx = (float)((int)((h >> 6) % 150) - 75);
                float fy = (float)((int)((h >> 14) % 150) - 75);
                rr_renderer_set_stroke(renderer, 0xff496e35);
                rr_renderer_set_line_width(renderer, 2.2f);
                rr_renderer_begin_path(renderer);
                rr_renderer_move_to(renderer, fx - 12.0f, fy + 6.0f);
                rr_renderer_line_to(renderer, fx + 12.0f, fy - 6.0f);
                rr_renderer_move_to(renderer, fx - 4.0f, fy + 2.0f);
                rr_renderer_line_to(renderer, fx - 8.0f, fy - 5.0f);
                rr_renderer_move_to(renderer, fx + 2.0f, fy - 1.0f);
                rr_renderer_line_to(renderer, fx + 6.0f, fy + 6.0f);
                rr_renderer_stroke(renderer);
            }

            // Окаменелость / древняя косточка в породе (на 16% тайлов)
            if (((h >> 7) % 100) < 16) {
                float bx = (float)((int)((h >> 9) % 140) - 70);
                float by = (float)((int)((h >> 17) % 140) - 70);
                rr_renderer_set_stroke(renderer, 0xff9c8870);
                rr_renderer_set_line_width(renderer, 2.4f);
                rr_renderer_begin_path(renderer);
                rr_renderer_move_to(renderer, bx - 8.0f, by - 3.0f);
                rr_renderer_line_to(renderer, bx + 8.0f, by + 3.0f);
                rr_renderer_stroke(renderer);
                rr_renderer_set_fill(renderer, 0xff9c8870);
                rr_renderer_begin_path(renderer);
                rr_renderer_arc(renderer, bx - 8.0f, by - 3.0f, 2.3f);
                rr_renderer_arc(renderer, bx + 8.0f, by + 3.0f, 2.3f);
                rr_renderer_fill(renderer);
            }
        }"""

assert old_hc_tile in arena, "Не найдена строка отрисовки тайла Hell Creek в RenderArena.c"
arena = arena.replace(old_hc_tile, new_hc_tile, 1)
with open("Client/Renderer/RenderArena.c", "w", encoding="utf-8") as f:
    f.write(arena)

print("Шаг 2 (красивый доисторический пол Hell Creek) готов! Пересобираем...")
