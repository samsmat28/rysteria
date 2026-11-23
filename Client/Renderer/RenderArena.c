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
            rr_renderer_draw_tile_hell_creek(renderer, tile_index);
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
       uint32_t wall_color = (arena->biome == rr_biome_id_pvp) ? 0xff1c0e06 : 0xff000000;
    rr_renderer_set_fill(renderer, wall_color);
    rr_renderer_set_global_alpha(renderer, (arena->biome == rr_biome_id_pvp) ? 0.88f : 0.5f);
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
            if (tile != 1)
            {
                rr_renderer_begin_path(renderer);
                if (tile == 0)
                    rr_renderer_fill_rect(renderer, nx * grid_size,
                                          currY * grid_size, grid_size,
                                          grid_size);
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
                    rr_renderer_fill(renderer);
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

                // Оранжевая линия-указатель от игрока к воронке
        struct rr_component_physical *flower_ptr =
            rr_simulation_get_physical(this->simulation, player_info->flower_id);
        if (flower_ptr != NULL)
        {
            rr_renderer_set_stroke(renderer, 0xffffaa00);
            rr_renderer_set_line_width(renderer, 6);
            rr_renderer_begin_path(renderer);
            rr_renderer_move_to(renderer, flower_ptr->x, flower_ptr->y);
            rr_renderer_line_to(renderer, portal_x, portal_y);
            rr_renderer_stroke(renderer);
        }

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


    rr_renderer_context_state_free(this->renderer, &state2);
}