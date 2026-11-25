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

#include <Client/Game.h>
#include <Client/Renderer/Renderer.h>
#include <Client/Simulation.h>
#include <Shared/StaticData.h>

#include <Client/Assets/RenderFunctions.h>

void rr_component_mob_render(EntityIdx entity, struct rr_game *game,
                             struct rr_simulation *simulation)
{
    struct rr_renderer *renderer = game->renderer;
    struct rr_component_physical *physical =
        rr_simulation_get_physical(simulation, entity);
    struct rr_component_mob *mob = rr_simulation_get_mob(simulation, entity);
        struct rr_component_physical *j_phys = physical;
    struct rr_component_arena *j_arena = j_phys ? rr_simulation_get_arena(simulation, game->player_info ? game->player_info->arena : RR_NULL_ENTITY) : NULL;
    if (j_arena && j_arena->biome == rr_biome_id_garden && j_phys) {
        float r = j_phys->radius > 10.0f ? j_phys->radius : 32.0f;
        struct rr_renderer_context_state jst;
        rr_renderer_context_state_init(renderer, &jst);
        rr_renderer_translate(renderer, j_phys->x, j_phys->y);
        bool is_cage = (mob->id == rr_mob_id_rock || mob->id == rr_mob_id_mantis || mob->id == rr_mob_id_ladybug || mob->id == rr_mob_id_dandelion);
        if (is_cage) {
            rr_renderer_set_fill(renderer, 0xff22252a);
            rr_renderer_set_stroke(renderer, 0xff6b7280);
            rr_renderer_set_line_width(renderer, 6.0f);
            rr_renderer_fill_rect(renderer, -r, -r, r * 2.0f, r * 2.0f);
            rr_renderer_stroke_rect(renderer, -r, -r, r * 2.0f, r * 2.0f);
            rr_renderer_set_stroke(renderer, 0xff9ca3af);
            rr_renderer_set_line_width(renderer, 4.0f);
            for (float bx = -r * 0.6f; bx <= r * 0.65f; bx += r * 0.4f) {
                rr_renderer_begin_path(renderer);
                rr_renderer_move_to(renderer, bx, -r);
                rr_renderer_line_to(renderer, bx, r);
                rr_renderer_stroke(renderer);
            }
            rr_renderer_set_fill(renderer, 0xffef4444);
            rr_renderer_begin_path(renderer);
            rr_renderer_arc(renderer, 0.0f, 0.0f, r * 0.25f);
            rr_renderer_fill(renderer);
        } else {
            rr_renderer_rotate(renderer, j_phys->angle);
            rr_renderer_set_fill(renderer, 0xff111827);
            rr_renderer_fill_rect(renderer, -r * 0.9f, -r * 0.85f, r * 0.5f, r * 0.25f);
            rr_renderer_fill_rect(renderer, r * 0.4f, -r * 0.85f, r * 0.5f, r * 0.25f);
            rr_renderer_fill_rect(renderer, -r * 0.9f, r * 0.6f, r * 0.5f, r * 0.25f);
            rr_renderer_fill_rect(renderer, r * 0.4f, r * 0.6f, r * 0.5f, r * 0.25f);
            rr_renderer_set_fill(renderer, 0xff1d4ed8);
            rr_renderer_set_stroke(renderer, 0xff0f172a);
            rr_renderer_set_line_width(renderer, 4.0f);
            rr_renderer_fill_rect(renderer, -r * 1.25f, -r * 0.68f, r * 2.5f, r * 1.36f);
            rr_renderer_stroke_rect(renderer, -r * 1.25f, -r * 0.68f, r * 2.5f, r * 1.36f);
            rr_renderer_set_fill(renderer, 0xfff8fafc);
            rr_renderer_fill_rect(renderer, -r * 0.55f, -r * 0.62f, r * 1.1f, r * 1.24f);
            int blink = ((int)(j_phys->x + j_phys->y) / 40) & 1;
            rr_renderer_set_fill(renderer, blink ? 0xffef4444 : 0xff3b82f6);
            rr_renderer_fill_rect(renderer, -r * 0.18f, -r * 0.45f, r * 0.36f, r * 0.42f);
            rr_renderer_set_fill(renderer, blink ? 0xff3b82f6 : 0xffef4444);
            rr_renderer_fill_rect(renderer, -r * 0.18f, r * 0.03f, r * 0.36f, r * 0.42f);
        }
        rr_renderer_context_state_free(renderer, &jst);
        return;
    }


    uint8_t is_friendly =
        mob->player_spawned &&
        game->player_info != NULL &&
        game->player_info->flower_id != RR_NULL_ENTITY &&
        is_same_team(
            rr_simulation_get_relations(simulation,
                                        game->player_info->flower_id)->team,
            rr_simulation_get_relations(simulation, entity)->team);
    if ((mob->id == rr_mob_id_trex || mob->id == rr_mob_id_meteor) &&
        is_friendly)
        rr_renderer_add_color_filter(renderer, 0xffffff63, 0.3);
    uint8_t has_arena = rr_simulation_has_arena(simulation, entity);
    struct rr_component_health *health;
    if (!has_arena)
    {
        health = rr_simulation_get_health(simulation, entity);
        rr_renderer_add_color_filter(renderer, 0xffff0000,
                                     0.5 * health->damage_animation);
    }
    rr_renderer_set_global_alpha(renderer, 1 - physical->deletion_animation);
    rr_renderer_scale(renderer, 1 + physical->deletion_animation * 0.5);
    rr_renderer_rotate(renderer, physical->lerp_angle);
    rr_renderer_scale(renderer, RR_MOB_RARITY_SCALING[mob->rarity].radius);
    if (mob->id == rr_mob_id_meteor)
    {
        struct rr_simulation_animation *particle =
            rr_particle_alloc(&game->default_particle_manager,
                              rr_animation_type_default);
        float angle =
            rr_vector_theta(&physical->lerp_velocity) + M_PI - 0.5 + rr_frand();
        float dist = rr_frand() * 50;
        rr_vector_from_polar(&particle->velocity,
                             (rr_frand() * 5 + 5) *
                                 RR_MOB_RARITY_SCALING[mob->rarity].radius,
                             angle);
        particle->friction = 0.9;
        particle->x = physical->lerp_x + cosf(angle) * dist;
        particle->y = physical->lerp_y + sinf(angle) * dist;
        particle->size =
            (4 + rr_frand() * 2) * RR_MOB_RARITY_SCALING[mob->rarity].radius;
        particle->opacity = 0.8;
        particle->disappearance = 6;
        particle->color = 0xffab3423;
    }
    if (physical->animation_timer > 2 * M_PI)
        physical->animation_timer = fmod(physical->animation_timer, 2 * M_PI);
    physical->animation =
        rr_lerp(physical->animation, sinf(physical->animation_timer),
                30 * game->lerp_delta);

    uint8_t use_cache = has_arena || health->damage_animation < 0.1 ||
                        game->cache.low_performance_mode;
    uint8_t is_centi_body =
        !rr_simulation_has_centipede(simulation, entity) ||
        !rr_simulation_get_centipede(simulation, entity)->is_head;
    rr_renderer_draw_mob(renderer, mob->id, physical->animation_timer,
                         physical->turning_animation - physical->lerp_angle,
                         use_cache | (is_friendly << 1) | (is_centi_body << 2));
    if (health->damage_animation > 0.08f)
    {
        float dmg_a = health->damage_animation;
        float wave_r = 22.0f + (1.0f - dmg_a) * 28.0f;
        rr_renderer_set_global_alpha(renderer, dmg_a * 0.75f);
        rr_renderer_set_stroke(renderer, 0xffffa94d);
        rr_renderer_set_line_width(renderer, 3.0f * dmg_a + 1.0f);
        rr_renderer_begin_path(renderer);
        rr_renderer_arc(renderer, 0, 0, wave_r);
        rr_renderer_stroke(renderer);

        rr_renderer_set_stroke(renderer, 0xffffec99);
        rr_renderer_set_line_width(renderer, 2.5f);
        for (int s = 0; s < 6; ++s)
        {
            float ang = s * 1.047f + dmg_a * 3.0f;
            float r1 = 14.0f + (1.0f - dmg_a) * 16.0f;
            float r2 = r1 + 10.0f * dmg_a;
            rr_renderer_begin_path(renderer);
            rr_renderer_move_to(renderer, cosf(ang) * r1, sinf(ang) * r1);
            rr_renderer_line_to(renderer, cosf(ang) * r2, sinf(ang) * r2);
            rr_renderer_stroke(renderer);
        }
    }
}
