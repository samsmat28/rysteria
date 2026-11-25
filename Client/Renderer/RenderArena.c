#include <emscripten.h>
// Copyright (C) 2024 Paul Johnson
// Copyright (C) 2024-2025 Maxim Nesterov

// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as
// published by the Free Software Foundation, either version 3 of the
// License, or (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Affero General Public License for more details.

// You should have received a copy of the GNU Affero General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.

#include <Client/Renderer/ComponentRender.h>

#include <math.h>

#include <Client/Assets/RenderFunctions.h>
#include <Client/Game.h>
#include <Client/InputData.h>
#include <Client/Renderer/Renderer.h>
#include <Client/Simulation.h>
#include <Shared/Crypto.h>

void render_background(struct rr_component_player_info *player_info,
                       struct rr_game *this)
{
    if (player_info->arena == 0)
        return;
    struct rr_renderer *renderer = this->renderer;
    double extra = 100;
    double scale = player_info->lerp_camera_fov * renderer->scale;
    double leftX =
        player_info->lerp_camera_x - renderer->width / (2 * scale) - extra;
    double rightX =
        player_info->lerp_camera_x + renderer->width / (2 * scale) + extra;
    double topY =
        player_info->lerp_camera_y - renderer->height / (2 * scale) - extra;
    double bottomY =
        player_info->lerp_camera_y + renderer->height / (2 * scale) + extra;

#define GRID_SIZE (512.0f)
    double newLeftX = floorf(leftX / GRID_SIZE) * GRID_SIZE;
    double newTopY = floorf(topY / GRID_SIZE) * GRID_SIZE;
    // rr_renderer_scale(renderer, scale);
    for (; newLeftX < rightX; newLeftX += GRID_SIZE)
    {
        for (double currY = newTopY; currY < bottomY; currY += GRID_SIZE)
        {
            uint32_t tile_index =
                rr_get_hash((uint32_t)(((newLeftX + 8192) / GRID_SIZE + 1) *
                                       ((currY + 8192) / GRID_SIZE + 2))) %
                3;
            struct rr_renderer_context_state state;
            rr_renderer_context_state_init(renderer, &state);
            rr_renderer_translate(renderer, newLeftX + GRID_SIZE / 2,
                                  currY + GRID_SIZE / 2);
            rr_renderer_scale(renderer, (GRID_SIZE + 2) / 256);
                   if (this->selected_biome == rr_biome_id_garden || this->selected_biome == rr_biome_id_nether || this->selected_biome == rr_biome_id_ocean || this->selected_biome == rr_biome_id_plains) {
            uint32_t bg = (this->selected_biome == rr_biome_id_nether) ? 0xff3b1414 : ((this->selected_biome == rr_biome_id_ocean) ? 0xff154360 : 0xff3e8e41);
            rr_renderer_set_fill(renderer, bg); rr_renderer_begin_path(renderer); rr_renderer_rect(renderer, -128, -128, 256, 256); rr_renderer_fill(renderer);
        }
        if (this->selected_biome == rr_biome_id_pvp)
        {
            // Базовый светло-коричневый пол Ant Hell
            rr_renderer_set_fill(renderer, 0xff9e744e);
            rr_renderer_begin_path(renderer);
            rr_renderer_rect(renderer, -128, -128, 256, 256);
            rr_renderer_fill(renderer);

            // Псевдослучайные координаты по tile_index для узоров грунта
            float ox1 = ((tile_index * 73) % 180) - 90.0f;
            float oy1 = ((tile_index * 41) % 180) - 90.0f;
            float ox2 = ((tile_index * 113) % 170) - 85.0f;
            float oy2 = ((tile_index * 89) % 170) - 85.0f;

            // Мягкое тёмно-коричневое пятно земли
            rr_renderer_set_fill(renderer, 0xff8c633f);
            rr_renderer_begin_path(renderer);
            rr_renderer_arc(renderer, ox1, oy1, 18.0f + (tile_index % 12));
            rr_renderer_fill(renderer);

            // Подземные камешки (на 2 из 3 тайлов)
            if (tile_index % 3 != 0)
            {
                rr_renderer_set_fill(renderer, 0xff755030);
                rr_renderer_begin_path(renderer);
                rr_renderer_arc(renderer, ox2, oy2, 7.0f + (tile_index % 5));
                rr_renderer_fill(renderer);

                rr_renderer_set_fill(renderer, 0xff825a37);
                rr_renderer_begin_path(renderer);
                rr_renderer_arc(renderer, ox2 + 16.0f, oy2 - 10.0f, 4.5f);
                rr_renderer_fill(renderer);
            }

            // Тонкие трещинки в грунте (на каждом втором тайле)
            if (tile_index % 2 == 0)
            {
                rr_renderer_set_stroke(renderer, 0xff734e2e);
                rr_renderer_set_line_width(renderer, 2.5f);
                rr_renderer_begin_path(renderer);
                rr_renderer_move_to(renderer, -ox1 * 0.6f - 14.0f, -oy2 * 0.6f);
                rr_renderer_line_to(renderer, -ox1 * 0.6f, -oy2 * 0.6f + 8.0f);
                rr_renderer_line_to(renderer, -ox1 * 0.6f + 15.0f, -oy2 * 0.6f + 4.0f);
                rr_renderer_stroke(renderer);
            }

            // Дополнительные подземные прожилки, крошка и кратеры
            rr_renderer_set_fill(renderer, 0xff855c38);
            rr_renderer_begin_path(renderer);
            rr_renderer_arc(renderer, -ox2 * 0.7f, ox1 * 0.7f, 11.0f + (tile_index % 7));
            rr_renderer_fill(renderer);

            rr_renderer_set_fill(renderer, 0xff6b4728);
            rr_renderer_begin_path(renderer);
            rr_renderer_arc(renderer, oy1 * 0.8f, -ox2 * 0.8f, 4.5f);
            rr_renderer_arc(renderer, oy1 * 0.8f + 12.0f, -ox2 * 0.8f + 7.0f, 3.5f);
            rr_renderer_arc(renderer, -oy2 * 0.75f, oy1 * 0.75f, 5.0f);
            rr_renderer_fill(renderer);

            if (tile_index % 3 == 1)
            {
                rr_renderer_set_stroke(renderer, 0xff7d5533);
                rr_renderer_set_line_width(renderer, 2.0f);
                rr_renderer_begin_path(renderer);
                rr_renderer_move_to(renderer, oy2 * 0.5f - 10.0f, ox1 * 0.5f + 10.0f);
                rr_renderer_line_to(renderer, oy2 * 0.5f + 4.0f, ox1 * 0.5f - 2.0f);
                rr_renderer_line_to(renderer, oy2 * 0.5f + 14.0f, ox1 * 0.5f - 12.0f);
                rr_renderer_stroke(renderer);
            }
        }
        if (this->selected_biome == rr_biome_id_pvp)
        {
            // Уникальный хеш для каждого тайла, чтобы узор не повторялся каждые 3 клетки
            uint32_t h = rr_get_hash(((uint32_t)((newLeftX + 8192) / GRID_SIZE) * 73856093u) ^ ((uint32_t)((currY + 8192) / GRID_SIZE) * 19349663u));

            // Чистый базовый пол Ant Hell (теплый земляной оттенок florr.io)
            rr_renderer_set_fill(renderer, 0xff9d734d);
            rr_renderer_begin_path(renderer);
            rr_renderer_rect(renderer, -128, -128, 256, 256);
            rr_renderer_fill(renderer);

            // Песчаные крупинки (мелкие четкие точки)
            rr_renderer_set_fill(renderer, 0xff8b623e);
            for (int i = 0; i < 4; i++) {
                uint32_t sh = rr_get_hash(h + (uint32_t)(i * 101));
                float px = (float)((int)(sh % 210) - 105);
                float py = (float)((int)((sh >> 8) % 210) - 105);
                float pr = 2.2f + (float)((sh >> 16) % 3);
                rr_renderer_begin_path(renderer);
                rr_renderer_arc(renderer, px, py, pr);
                rr_renderer_fill(renderer);
            }

            // Четкие подземные камешки с темным контуром (на 65% тайлов)
            if ((h % 100) < 65) {
                float sx = (float)((int)((h >> 4) % 170) - 85);
                float sy = (float)((int)((h >> 12) % 170) - 85);
                float sr = 5.5f + (float)((h >> 20) % 5);

                // Тень/контур камешка
                rr_renderer_set_fill(renderer, 0xff6b492b);
                rr_renderer_begin_path(renderer);
                rr_renderer_arc(renderer, sx, sy + 1.5f, sr + 1.4f);
                rr_renderer_fill(renderer);

                // Тело камешка
                rr_renderer_set_fill(renderer, (h & 1) ? 0xff825b37 : 0xff785331);
                rr_renderer_begin_path(renderer);
                rr_renderer_arc(renderer, sx, sy, sr);
                rr_renderer_fill(renderer);
            }

            // Аккуратный второй мелкий камешек (на 35% тайлов)
            if (((h >> 3) % 100) < 35) {
                float sx2 = (float)((int)((h >> 6) % 180) - 90);
                float sy2 = (float)((int)((h >> 14) % 180) - 90);
                rr_renderer_set_fill(renderer, 0xff6e4c2e);
                rr_renderer_begin_path(renderer);
                rr_renderer_arc(renderer, sx2, sy2, 3.6f);
                rr_renderer_fill(renderer);
            }

            // Тонкая четкая трещинка (на 25% тайлов)
            if (((h >> 5) % 100) < 25) {
                float cx = (float)((int)((h >> 7) % 140) - 70);
                float cy = (float)((int)((h >> 15) % 140) - 70);
                rr_renderer_set_stroke(renderer, 0xff77512f);
                rr_renderer_set_line_width(renderer, 2.0f);
                rr_renderer_begin_path(renderer);
                rr_renderer_move_to(renderer, cx - 10.0f, cy - 4.0f);
                rr_renderer_line_to(renderer, cx, cy + 2.0f);
                rr_renderer_line_to(renderer, cx + 11.0f, cy - 2.0f);
                rr_renderer_stroke(renderer);
            }
        }
        else if (this->selected_biome == rr_biome_id_hell_creek)
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
        }
        else
                rr_renderer_draw_tile_garden(renderer, tile_index);
            rr_renderer_context_state_free(renderer, &state);
        }
    }

#undef GRID_SIZE
    struct rr_component_arena *arena =
        rr_simulation_get_arena(this->simulation, player_info->arena);
    float grid_size = RR_MAZES[arena->biome].grid_size;
    uint32_t maze_dim = RR_MAZES[arena->biome].maze_dim;
    struct rr_maze_grid *grid = RR_MAZES[arena->biome].maze;
       uint32_t wall_color = (arena->biome == rr_biome_id_garden) ? 0xff3b4048 : ((arena->biome == rr_biome_id_pvp) ? 0xff1c0e06 : (arena->biome == rr_biome_id_plains ? 0xff6e4a2e : 0xff000000));
    rr_renderer_set_fill(renderer, wall_color);
    rr_renderer_set_global_alpha(renderer, (arena->biome == rr_biome_id_pvp || arena->biome == rr_biome_id_plains || arena->biome == rr_biome_id_garden) ? 1.0f : 0.5f);
    int32_t nx = floorf(leftX / grid_size);
    int32_t ny = floorf(topY / grid_size);
    for (; nx < rightX / grid_size; ++nx)
        for (int32_t currY = ny; currY < bottomY / grid_size; ++currY)
        {
            rr_renderer_set_fill(renderer, wall_color);
            uint8_t tile =
                (nx < 0 || currY < 0 || nx >= maze_dim || currY >= maze_dim)
                    ? 0
                    : grid[currY * maze_dim + nx].value;
            if (arena->biome == rr_biome_id_garden && tile == 1) {
            rr_renderer_set_fill(renderer, (nx < 160) ? 0xff2e323b : 0xff2f6b32);
            rr_renderer_fill_rect(renderer, nx * grid_size, currY * grid_size, grid_size + 1.0f, grid_size + 1.0f);
        }
        if (tile != 1)
            {
                rr_renderer_begin_path(renderer);
                if (tile == 0) {
                        float wx = nx * grid_size;
                        float wy = currY * grid_size;
                        rr_renderer_set_fill(renderer, wall_color);
                        rr_renderer_fill_rect(renderer, wx, wy, grid_size, grid_size);
                        if (arena->biome == rr_biome_id_plains) {
                            uint32_t h = (uint32_t)(nx * 73856093u ^ currY * 19349663u);
                            rr_renderer_set_fill(renderer, 0xff52351e);
                            rr_renderer_begin_path(renderer);
                            rr_renderer_arc(renderer, wx + 220.0f + (h % 220), wy + 240.0f + ((h >> 3) % 220), 65.0f + (h % 45));
                            rr_renderer_arc(renderer, wx + 680.0f + ((h >> 6) % 180), wy + 310.0f + ((h >> 9) % 240), 50.0f + ((h >> 5) % 40));
                            rr_renderer_arc(renderer, wx + 420.0f + ((h >> 11) % 260), wy + 720.0f + ((h >> 14) % 160), 75.0f + ((h >> 7) % 45));
                            rr_renderer_arc(renderer, wx + 760.0f + ((h >> 16) % 120), wy + 760.0f + ((h >> 18) % 120), 38.0f + ((h >> 10) % 25));
                            rr_renderer_fill(renderer);
                            bool p_l = (nx > 0 && grid[currY * maze_dim + (nx - 1)].value == 1);
                            bool p_r = (nx + 1 < (int32_t)maze_dim && grid[currY * maze_dim + (nx + 1)].value == 1);
                            bool p_t = (currY > 0 && grid[(currY - 1) * maze_dim + nx].value == 1);
                            bool p_b = (currY + 1 < (int32_t)maze_dim && grid[(currY + 1) * maze_dim + nx].value == 1);
                            if (p_l) {
                                float j1 = ((h & 7) - 3.5f) * 16.0f, j2 = (((h >> 3) & 7) - 3.5f) * 16.0f;
                                rr_renderer_set_fill(renderer, 0xff6e4a2e); rr_renderer_set_stroke(renderer, 0xff3b2513); rr_renderer_set_line_width(renderer, 22.0f);
                                rr_renderer_begin_path(renderer); rr_renderer_move_to(renderer, wx, wy);
                                rr_renderer_line_to(renderer, wx - 42.0f + j1, wy + grid_size * 0.33f);
                                rr_renderer_line_to(renderer, wx - 22.0f + j2, wy + grid_size * 0.67f);
                                rr_renderer_line_to(renderer, wx, wy + grid_size);
                                rr_renderer_fill(renderer); rr_renderer_stroke(renderer);
                            }
                            if (p_r) {
                                float j1 = (((h >> 2) & 7) - 3.5f) * 16.0f, j2 = (((h >> 5) & 7) - 3.5f) * 16.0f;
                                rr_renderer_set_fill(renderer, 0xff6e4a2e); rr_renderer_set_stroke(renderer, 0xff3b2513); rr_renderer_set_line_width(renderer, 22.0f);
                                rr_renderer_begin_path(renderer); rr_renderer_move_to(renderer, wx + grid_size, wy);
                                rr_renderer_line_to(renderer, wx + grid_size + 42.0f + j1, wy + grid_size * 0.33f);
                                rr_renderer_line_to(renderer, wx + grid_size + 22.0f + j2, wy + grid_size * 0.67f);
                                rr_renderer_line_to(renderer, wx + grid_size, wy + grid_size);
                                rr_renderer_fill(renderer); rr_renderer_stroke(renderer);
                            }
                            if (p_t) {
                                float j1 = (((h >> 4) & 7) - 3.5f) * 16.0f, j2 = (((h >> 7) & 7) - 3.5f) * 16.0f;
                                rr_renderer_set_fill(renderer, 0xff6e4a2e); rr_renderer_set_stroke(renderer, 0xff3b2513); rr_renderer_set_line_width(renderer, 22.0f);
                                rr_renderer_begin_path(renderer); rr_renderer_move_to(renderer, wx, wy);
                                rr_renderer_line_to(renderer, wx + grid_size * 0.33f, wy - 42.0f + j1);
                                rr_renderer_line_to(renderer, wx + grid_size * 0.67f, wy - 22.0f + j2);
                                rr_renderer_line_to(renderer, wx + grid_size, wy);
                                rr_renderer_fill(renderer); rr_renderer_stroke(renderer);
                            }
                            if (p_b) {
                                float j1 = (((h >> 6) & 7) - 3.5f) * 16.0f, j2 = (((h >> 9) & 7) - 3.5f) * 16.0f;
                                rr_renderer_set_fill(renderer, 0xff6e4a2e); rr_renderer_set_stroke(renderer, 0xff3b2513); rr_renderer_set_line_width(renderer, 22.0f);
                                rr_renderer_begin_path(renderer); rr_renderer_move_to(renderer, wx, wy + grid_size);
                                rr_renderer_line_to(renderer, wx + grid_size * 0.33f, wy + grid_size + 42.0f + j1);
                                rr_renderer_line_to(renderer, wx + grid_size * 0.67f, wy + grid_size + 22.0f + j2);
                                rr_renderer_line_to(renderer, wx + grid_size, wy + grid_size);
                                rr_renderer_fill(renderer); rr_renderer_stroke(renderer);
                            }
                        }
                    }
                    else
                {
                    uint8_t left = (tile >> 1) & 1;
                    uint8_t top = tile & 1;
                    uint8_t inverse = 1 - ((tile >> 3) & 1);
                    rr_renderer_move_to(renderer,
                                        (nx + inverse ^ left) * grid_size,
                                        (currY + inverse ^ top) * grid_size);
                    float start_angle = 0;
                    if (top == 0 && left == 1)
                        start_angle = M_PI / 2;
                    else if (top == 1 && left == 1)
                        start_angle = M_PI;
                    else if (top == 1 && left == 0)
                        start_angle = M_PI * 3 / 2;
                    rr_renderer_partial_arc(renderer, (nx + left) * grid_size,
                                            (currY + top) * grid_size,
                                            grid_size, start_angle,
                                            start_angle + M_PI / 2, 0);
                    rr_renderer_fill(renderer); if (arena->biome == rr_biome_id_plains) { rr_renderer_set_stroke(renderer, 0xff3b2513); rr_renderer_set_line_width(renderer, 22.0f); rr_renderer_stroke(renderer); } if (arena->biome == rr_biome_id_plains) { rr_renderer_set_stroke(renderer, 0xff3b2513); rr_renderer_set_line_width(renderer, 30.0f); rr_renderer_stroke(renderer); }
                }
            }

            if (nx >= 0 && nx < maze_dim && currY >= 0 && currY < maze_dim && grid[currY * maze_dim + nx].value == 1)
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
                    rr_renderer_set_global_alpha(renderer, 0.85f);
                    rr_renderer_set_line_width(renderer, 18.0f);
                    rr_renderer_begin_path(renderer);
                    rr_renderer_move_to(renderer, lx, ly);
                    rr_renderer_line_to(renderer, lx, ly + grid_size);
                    rr_renderer_stroke(renderer);

                    rr_renderer_set_fill(renderer, RR_RARITY_COLORS[hi]);
                    rr_renderer_set_stroke(renderer, 0xff1a1a1a);
                    rr_renderer_set_line_width(renderer, 12.0f);
                    rr_renderer_set_text_size(renderer, 180);
                    rr_renderer_set_text_align(renderer, 1);
                    rr_renderer_set_text_baseline(renderer, 1);
                    float tx = (r_cur > r_left) ? (lx + grid_size * 0.45f) : (lx - grid_size * 0.45f);
                    float ty = ly + grid_size * 0.5f;
                    rr_renderer_stroke_text(renderer, RR_RARITY_NAMES[hi], tx, ty);
                    rr_renderer_fill_text(renderer, RR_RARITY_NAMES[hi], tx, ty);
                    rr_renderer_set_global_alpha(renderer, 0.5f);
                }
                if (r_cur != r_top)
                {
                    uint8_t hi = r_cur > r_top ? r_cur : r_top;
                    float lx = nx * grid_size;
                    float ly = currY * grid_size;
                    rr_renderer_set_stroke(renderer, RR_RARITY_COLORS[hi]);
                    rr_renderer_set_global_alpha(renderer, 0.85f);
                    rr_renderer_set_line_width(renderer, 18.0f);
                    rr_renderer_begin_path(renderer);
                    rr_renderer_move_to(renderer, lx, ly);
                    rr_renderer_line_to(renderer, lx + grid_size, ly);
                    rr_renderer_stroke(renderer);

                    rr_renderer_set_fill(renderer, RR_RARITY_COLORS[hi]);
                    rr_renderer_set_stroke(renderer, 0xff1a1a1a);
                    rr_renderer_set_line_width(renderer, 12.0f);
                    rr_renderer_set_text_size(renderer, 180);
                    rr_renderer_set_text_align(renderer, 1);
                    rr_renderer_set_text_baseline(renderer, 1);
                    float tx = lx + grid_size * 0.5f;
                    float ty = (r_cur > r_top) ? (ly + grid_size * 0.45f) : (ly - grid_size * 0.45f);
                    rr_renderer_stroke_text(renderer, RR_RARITY_NAMES[hi], tx, ty);
                    rr_renderer_fill_text(renderer, RR_RARITY_NAMES[hi], tx, ty);
                    rr_renderer_set_global_alpha(renderer, 0.5f);
                }
            }
            if (this->cache.show_coordinates && nx % 2 && currY % 2)
            {
                char pos[10];
                sprintf(pos, "%d %d", (nx - 1) / 2, (currY - 1) / 2);
                rr_renderer_set_text_size(renderer, 64);
                rr_renderer_set_text_align(renderer, 1);
                rr_renderer_set_text_baseline(renderer, 1);
                rr_renderer_fill_text(renderer, pos, nx * grid_size, currY * grid_size);
            }
        }
}

uint8_t rr_auto_enter_portal = 0;
void rr_component_arena_render(EntityIdx entity, struct rr_game *this,
                               struct rr_simulation *simulation)
{
    struct rr_renderer_context_state state2;
    struct rr_component_player_info *player_info = this->player_info;

    struct rr_component_arena *arena =
        rr_simulation_get_arena(this->simulation, player_info->arena);
    rr_renderer_context_state_init(this->renderer, &state2);
    render_background(player_info, this);

        // Воронка-телепорт между Hell Creek и Ant Hell
    if (arena != NULL && player_info->flower_id != RR_NULL_ENTITY &&
        (arena->biome == rr_biome_id_hell_creek || arena->biome == rr_biome_id_pvp))
    {
        float portal_x = 58.0f * 2048.0f;
        float portal_y = 5.0f * 2048.0f;
        float portal_r = 140.0f;

        struct rr_renderer *renderer = this->renderer;
        rr_renderer_set_global_alpha(renderer, 1.0f);

        // Внешний обod норы
        rr_renderer_set_fill(renderer, arena->biome == rr_biome_id_hell_creek ? 0xff4a2e18 : 0xff7eef6d);
        rr_renderer_set_stroke(renderer, 0xff2b1a0e);
        rr_renderer_set_line_width(renderer, 10);
        rr_renderer_begin_path(renderer);
        rr_renderer_arc(renderer, portal_x, portal_y, portal_r);
        rr_renderer_fill(renderer);
        rr_renderer_stroke(renderer);

        // Внутренняя темнота туннеля
        rr_renderer_set_fill(renderer, arena->biome == rr_biome_id_hell_creek ? 0xff1c1008 : 0xff4eb842);
        rr_renderer_begin_path(renderer);
        rr_renderer_arc(renderer, portal_x, portal_y, portal_r * 0.6f);
        rr_renderer_fill(renderer);

        // Подпись над порталом
        rr_renderer_set_fill(renderer, 0xffffffff);
        rr_renderer_set_stroke(renderer, 0xff111111);
        rr_renderer_set_line_width(renderer, 4);
        rr_renderer_set_text_size(renderer, 28);
        rr_renderer_set_text_align(renderer, 1);
        rr_renderer_set_text_baseline(renderer, 1);
        char const *label = (arena->biome == rr_biome_id_hell_creek) ? "Ant Hell" : "Hell Creek";
        rr_renderer_stroke_text(renderer, label, portal_x, portal_y - portal_r - 20);
        rr_renderer_fill_text(renderer, label, portal_x, portal_y - portal_r - 20);

        // Проверка наезда игрока на воронку
        static uint32_t portal_cooldown = 0;
        if (portal_cooldown > 0)
        {
            --portal_cooldown;
        }
        else
        {
            struct rr_component_physical *flower_phys =
                rr_simulation_get_physical(this->simulation, player_info->flower_id);
            if (flower_phys != NULL)
            {
                float dx = flower_phys->x - portal_x;
                float dy = flower_phys->y - portal_y;
                if (dx * dx + dy * dy < (portal_r * 0.75f) * (portal_r * 0.75f))
                {
                    portal_cooldown = 180; // ~3 секунды защиты от повторного телепорта
                    uint8_t target_biome = (arena->biome == rr_biome_id_hell_creek)
                        ? rr_biome_id_pvp
                        : rr_biome_id_hell_creek;
                    rr_game_select_biome(this, target_biome);
                    rr_auto_enter_portal = 1;
                }
            }
        }
    }


        if (arena->biome == rr_biome_id_plains) {
        struct rr_maze_declaration const *mdecl = &RR_MAZES[arena->biome];
        for (uint32_t ci = 0; ci < mdecl->checkpoint_count; ++ci) {
            float cx = mdecl->checkpoints[ci].spawn_x * mdecl->grid_size;
            float cy = mdecl->checkpoints[ci].spawn_y * mdecl->grid_size;
            rr_renderer_set_fill(this->renderer, 0x55ffaa22);
            rr_renderer_set_stroke(this->renderer, 0xffffaa22);
            rr_renderer_set_line_width(this->renderer, 16.0f);
            rr_renderer_begin_path(this->renderer);
            rr_renderer_arc(this->renderer, cx, cy, 180.0f);
            rr_renderer_fill(this->renderer);
            rr_renderer_stroke(this->renderer);
        }
    }
    
    // === JAIL COMPLEX RENDER (Gray Block -> Green Yard + Red Button) ===
    {
        // 1. Gray concrete prison building (-18320 .. -17920, -18240 .. -17760)
        rr_renderer_set_fill(this->renderer, 0xff2c3036);
        rr_renderer_begin_path(this->renderer);
        rr_renderer_move_to(this->renderer, -18320.0f, -18240.0f);
        rr_renderer_line_to(this->renderer, -17920.0f, -18240.0f);
        rr_renderer_line_to(this->renderer, -17920.0f, -17760.0f);
        rr_renderer_line_to(this->renderer, -18320.0f, -17760.0f);
        rr_renderer_fill(this->renderer);

        // 2. Green grass prison yard (-17920 .. -17200, -18240 .. -17760)
        rr_renderer_set_fill(this->renderer, 0xff2f6b32);
        rr_renderer_begin_path(this->renderer);
        rr_renderer_move_to(this->renderer, -17920.0f, -18240.0f);
        rr_renderer_line_to(this->renderer, -17200.0f, -18240.0f);
        rr_renderer_line_to(this->renderer, -17200.0f, -17760.0f);
        rr_renderer_line_to(this->renderer, -17920.0f, -17760.0f);
        rr_renderer_fill(this->renderer);

        // Threshold strip between gray floor and green yard
        rr_renderer_set_stroke(this->renderer, 0xff8c949e);
        rr_renderer_set_line_width(this->renderer, 10.0f);
        rr_renderer_begin_path(this->renderer);
        rr_renderer_move_to(this->renderer, -17920.0f, -18240.0f);
        rr_renderer_line_to(this->renderer, -17920.0f, -17760.0f);
        rr_renderer_stroke(this->renderer);

        // 3. Cell 160x160 around (-18160, -18000) with iron bars
        float cx = -18160.0f, cy = -18000.0f, cr = 80.0f;
        rr_renderer_set_fill(this->renderer, 0xff202328);
        rr_renderer_begin_path(this->renderer);
        rr_renderer_move_to(this->renderer, cx - cr, cy - cr);
        rr_renderer_line_to(this->renderer, cx + cr, cy - cr);
        rr_renderer_line_to(this->renderer, cx + cr, cy + cr);
        rr_renderer_line_to(this->renderer, cx - cr, cy + cr);
        rr_renderer_fill(this->renderer);
        rr_renderer_set_stroke(this->renderer, 0x889aa5b4);
        rr_renderer_set_line_width(this->renderer, 5.0f);
        for (float bx = cx - cr + 20.0f; bx < cx + cr; bx += 20.0f) {
            rr_renderer_begin_path(this->renderer);
            rr_renderer_move_to(this->renderer, bx, cy - cr);
            rr_renderer_line_to(this->renderer, bx, cy + cr);
            rr_renderer_stroke(this->renderer);
        }

        // 4. Red Escape Button in the green yard (-17300, -18000)
        rr_renderer_set_fill(this->renderer, 0xff42474f);
        rr_renderer_begin_path(this->renderer);
        rr_renderer_arc(this->renderer, -17300.0f, -18000.0f, 52.0f);
        rr_renderer_fill(this->renderer);
        rr_renderer_set_fill(this->renderer, 0xffe62e2e);
        rr_renderer_set_stroke(this->renderer, 0xffff8888);
        rr_renderer_set_line_width(this->renderer, 5.0f);
        rr_renderer_begin_path(this->renderer);
        rr_renderer_arc(this->renderer, -17300.0f, -18000.0f, 36.0f);
        rr_renderer_fill(this->renderer);
        rr_renderer_stroke(this->renderer);

        // 5. Outer prison perimeter wall
        rr_renderer_set_stroke(this->renderer, 0xff555961);
        rr_renderer_set_line_width(this->renderer, 24.0f);
        rr_renderer_begin_path(this->renderer);
        rr_renderer_move_to(this->renderer, -18320.0f, -18240.0f);
        rr_renderer_line_to(this->renderer, -17200.0f, -18240.0f);
        rr_renderer_line_to(this->renderer, -17200.0f, -17760.0f);
        rr_renderer_line_to(this->renderer, -18320.0f, -17760.0f);
        rr_renderer_line_to(this->renderer, -18320.0f, -18240.0f);
        rr_renderer_stroke(this->renderer);
    }
    if (arena->biome == rr_biome_id_garden) {
        float bx = 138.0f * 2.0f * 2048.0f, by = 80.0f * 2.0f * 2048.0f;
        rr_renderer_set_fill(this->renderer, 0xff42474f);
        rr_renderer_begin_path(this->renderer); rr_renderer_arc(this->renderer, bx, by, 240.0f); rr_renderer_fill(this->renderer);
        rr_renderer_set_fill(this->renderer, 0xffe62e2e); rr_renderer_set_stroke(this->renderer, 0xffff9999); rr_renderer_set_line_width(this->renderer, 16.0f);
        rr_renderer_begin_path(this->renderer); rr_renderer_arc(this->renderer, bx, by, 160.0f); rr_renderer_fill(this->renderer); rr_renderer_stroke(this->renderer);
    }
    rr_renderer_context_state_free(this->renderer, &state2);
}