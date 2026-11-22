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

#include <Client/Assets/RenderFunctions.h>

#include <math.h>
#include <stdlib.h>

#include <Client/Assets/Render.h>
#include <Client/Renderer/Renderer.h>
#include <Shared/StaticData.h>

// head, body, legs, tail, IN THAT ORDER

struct rr_renderer_spritesheet mob_sprites[rr_mob_id_max];
struct rr_renderer_spritesheet friendly_mob_sprites[2];
void render_sprite(struct rr_renderer *renderer, uint8_t id, uint32_t pos,
                   uint8_t flags)
{
    if (flags & 1)
    {
        if (flags & 2)
        {
            if (id == rr_mob_id_trex)
                render_sprite_from_cache(renderer, &friendly_mob_sprites[0],
                                         pos);
            else if (id == rr_mob_id_meteor)
                render_sprite_from_cache(renderer, &friendly_mob_sprites[1],
                                         pos);
            else
                render_sprite_from_cache(renderer, &mob_sprites[id], pos);
        }
        else
            render_sprite_from_cache(renderer, &mob_sprites[id], pos);
    }
    else
        mob_sprites[id].sprites[pos].render(renderer);
}

void rr_renderer_draw_mob(struct rr_renderer *renderer, uint8_t id,
                          float raw_animation_tick, float turning_value,
                          uint8_t flags)
{
    float animation_tick = sinf(raw_animation_tick);
    struct rr_renderer_context_state original_state;
    struct rr_renderer_context_state state;

    rr_renderer_context_state_init(renderer, &original_state);
    // rr_renderer_rotate(renderer, M_PI / 2);
    /*
    function change(line) {
    const split = line.split("renderer,");
    if (split.length === 1)
        return line;
    let part = split[1].split(',').map(x => parseFloat(x));
    let final = [];
    for (let n = 0; n < part.length; n += 2)
        final.push(-part[n+1],part[n]);
    return split[0] + "renderer," + final.map(x=>x.toFixed(2)).join(',') + ");";
    }
    function convert(file) {
    console.log(file.split(";\n").map(x =>
    change(x)).join(";\n").replaceAll(";;",";"))}
    */
    switch (id)
    {
    case rr_mob_id_pachycephalosaurus:
        rr_renderer_scale(renderer, 0.75);
    case rr_mob_id_triceratops:
    case rr_mob_id_trex:
    case rr_mob_id_edmontosaurus:
        rr_renderer_scale(renderer, 0.2f);

        rr_renderer_context_state_init(renderer, &state);
        rr_renderer_translate(renderer, animation_tick * 10.0f, 0);
        render_sprite(renderer, id, 2, flags);
        rr_renderer_context_state_free(renderer, &state);

        rr_renderer_context_state_init(renderer, &state);
        rr_renderer_translate(renderer, animation_tick * -10.0f, 0);
        render_sprite(renderer, id, 3, flags);
        rr_renderer_context_state_free(renderer, &state);

        rr_renderer_context_state_init(renderer, &state);
        rr_renderer_translate(renderer, -75, 0);
        rr_renderer_rotate(renderer, turning_value);
        rr_renderer_translate(renderer, -80, 0);
        render_sprite(renderer, id, 4, flags);
        rr_renderer_context_state_free(renderer, &state);

        render_sprite(renderer, id, 1, flags);

        rr_renderer_context_state_init(renderer, &state);
        rr_renderer_translate(renderer, 145, 0);
        render_sprite(renderer, id, 0, flags);
        rr_renderer_context_state_free(renderer, &state);
        break;
    case rr_mob_id_fern:
        rr_renderer_scale(renderer, 0.3f);
    case rr_mob_id_tree:
    case rr_mob_id_meteor:
    case rr_mob_id_beehive:
        rr_renderer_scale(renderer, 0.4f);
        render_sprite(renderer, id, 0, flags);
        break;
    case rr_mob_id_pteranodon:
        rr_renderer_scale(renderer, 0.15f);

        rr_renderer_context_state_init(renderer, &state);
        rr_renderer_rotate(renderer, animation_tick * 0.1f);
        rr_renderer_translate(renderer, 0, 160);
        render_sprite(renderer, id, 1, flags);
        rr_renderer_context_state_free(renderer, &state);

        rr_renderer_context_state_init(renderer, &state);
        rr_renderer_rotate(renderer, animation_tick * -0.1f);
        rr_renderer_translate(renderer, 0, -160);
        render_sprite(renderer, id, 2, flags);
        rr_renderer_context_state_free(renderer, &state);
        render_sprite(renderer, id, 0, flags);
        break;
    case rr_mob_id_dakotaraptor:
    case rr_mob_id_ornithomimus:
        rr_renderer_scale(renderer, 0.16f);

        rr_renderer_context_state_init(renderer, &state);
        rr_renderer_translate(renderer, 0, -65);
        rr_renderer_rotate(renderer, animation_tick * 0.1f);
        render_sprite(renderer, id, 2, flags);
        rr_renderer_context_state_free(renderer, &state);

        rr_renderer_context_state_init(renderer, &state);
        rr_renderer_translate(renderer, 0, 65);
        rr_renderer_rotate(renderer, animation_tick * -0.1f);
        render_sprite(renderer, id, 3, flags);
        rr_renderer_context_state_free(renderer, &state);

        rr_renderer_context_state_init(renderer, &state);
        rr_renderer_translate(renderer, -120, 0);
        rr_renderer_rotate(renderer, turning_value);
        rr_renderer_translate(renderer, -75, 0);
        render_sprite(renderer, id, 4, flags);
        rr_renderer_context_state_free(renderer, &state);

        render_sprite(renderer, id, 1, flags);

        rr_renderer_context_state_init(renderer, &state);
        rr_renderer_translate(renderer,
                              id == rr_mob_id_ornithomimus ? 175 : 125, 0);

        render_sprite(renderer, id, 0, flags);
        rr_renderer_context_state_free(renderer, &state);
        break;
    case rr_mob_id_ankylosaurus:
        rr_renderer_scale(renderer, 0.2f);

        rr_renderer_context_state_init(renderer, &state);
        rr_renderer_translate(renderer, -155, 0);
        rr_renderer_rotate(renderer, turning_value);
        render_sprite(renderer, id, 2, flags);
        rr_renderer_context_state_free(renderer, &state);

        render_sprite(renderer, id, 1, flags);

        rr_renderer_context_state_init(renderer, &state);
        rr_renderer_translate(renderer, 145, 0);
        render_sprite(renderer, id, 0, flags);
        rr_renderer_context_state_free(renderer, &state);
        break;
    case rr_mob_id_quetzalcoatlus:
        rr_renderer_scale(renderer, 0.2f);

        rr_renderer_context_state_init(renderer, &state);
        rr_renderer_rotate(renderer, animation_tick * 0.1f);
        rr_renderer_translate(renderer, -75, 125);
        render_sprite(renderer, id, 2, flags);
        rr_renderer_context_state_free(renderer, &state);

        rr_renderer_context_state_init(renderer, &state);
        rr_renderer_rotate(renderer, animation_tick * -0.1f);
        rr_renderer_translate(renderer, -75, -125);
        render_sprite(renderer, id, 3, flags);
        rr_renderer_context_state_free(renderer, &state);
        render_sprite(renderer, id, 1, flags);

        rr_renderer_translate(renderer, 165, 0);
        render_sprite(renderer, id, 0, flags);
        break;
    case rr_mob_id_ant:
        rr_renderer_scale(renderer, 0.35f);
        rr_renderer_translate(renderer, -35, 0);
        render_sprite(renderer, id, 1, flags);
        rr_renderer_translate(renderer, 70, 0);
        render_sprite(renderer, id, 0, flags);
        break;
    case rr_mob_id_hornet:
    case rr_mob_id_honeybee:
        rr_renderer_scale(renderer, 0.2f);
        /*
        rr_renderer_context_state_init(renderer, &state);
        rr_renderer_rotate(renderer, animation_tick * 0.1f - M_PI / 6);
        rr_renderer_translate(renderer, 0, 75);
        rr_renderer_rotate(renderer, M_PI / 2);
        render_sprite(renderer, id, 3, flags);
        rr_renderer_context_state_free(renderer, &state);
        rr_renderer_context_state_init(renderer, &state);
        rr_renderer_rotate(renderer, animation_tick * -0.1f);
        rr_renderer_translate(renderer, 0, 75);
        rr_renderer_rotate(renderer, M_PI / 2);
        render_sprite(renderer, id, 3, flags);
        rr_renderer_context_state_free(renderer, &state);
        rr_renderer_context_state_init(renderer, &state);
        rr_renderer_rotate(renderer, animation_tick * 0.1f + M_PI / 6);
        rr_renderer_translate(renderer, 0, 75);
        rr_renderer_rotate(renderer, M_PI / 2);
        render_sprite(renderer, id, 3, flags);
        rr_renderer_context_state_free(renderer, &state);

        rr_renderer_context_state_init(renderer, &state);
        rr_renderer_rotate(renderer, animation_tick * 0.1f - M_PI / 6 + M_PI);
        rr_renderer_translate(renderer, 0, 75);
        rr_renderer_rotate(renderer, M_PI / 2);
        render_sprite(renderer, id, 3, flags);
        rr_renderer_context_state_free(renderer, &state);
        rr_renderer_context_state_init(renderer, &state);
        rr_renderer_rotate(renderer, animation_tick * -0.1f + M_PI);
        rr_renderer_translate(renderer, 0, 75);
        rr_renderer_rotate(renderer, M_PI / 2);
        render_sprite(renderer, id, 3, flags);
        rr_renderer_context_state_free(renderer, &state);
        rr_renderer_context_state_init(renderer, &state);
        rr_renderer_rotate(renderer, animation_tick * 0.1f + M_PI / 6 + M_PI);
        rr_renderer_translate(renderer, 0, 75);
        rr_renderer_rotate(renderer, M_PI / 2);
        render_sprite(renderer, id, 3, flags);
        rr_renderer_context_state_free(renderer, &state);
        */

        rr_renderer_translate(renderer, -90, 0);
        render_sprite(renderer, id, 2, flags);
        rr_renderer_translate(renderer, 90, 0);
        render_sprite(renderer, id, 1, flags);
        rr_renderer_context_state_init(renderer, &state);
        rr_renderer_rotate(renderer, animation_tick * 0.2f + 2 * M_PI / 3);
        rr_renderer_translate(renderer, 100, 0);
        render_sprite(renderer, id, 4, flags);
        rr_renderer_context_state_free(renderer, &state);
        rr_renderer_context_state_init(renderer, &state);
        rr_renderer_rotate(renderer, animation_tick * -0.2f - 2 * M_PI / 3);
        rr_renderer_translate(renderer, 100, 0);
        render_sprite(renderer, id, 4, flags);
        rr_renderer_context_state_free(renderer, &state);
        rr_renderer_translate(renderer, 80, 0);
        render_sprite(renderer, id, 0, flags);
        break;
           case rr_mob_id_fat_bee:
        rr_renderer_scale(renderer, 0.24f);
        rr_renderer_scale2(renderer, 1.05f, 1.85f);
        rr_renderer_translate(renderer, -85, 0);
        render_sprite(renderer, rr_mob_id_honeybee, 2, flags);
        rr_renderer_translate(renderer, 85, 0);
        render_sprite(renderer, rr_mob_id_honeybee, 1, flags);
        rr_renderer_context_state_init(renderer, &state);
        rr_renderer_rotate(renderer, animation_tick * 0.25f + 2 * M_PI / 3);
        rr_renderer_translate(renderer, 100, 0);
        render_sprite(renderer, rr_mob_id_honeybee, 4, flags);
        rr_renderer_context_state_free(renderer, &state);
        rr_renderer_context_state_init(renderer, &state);
        rr_renderer_rotate(renderer, animation_tick * -0.25f - 2 * M_PI / 3);
        rr_renderer_translate(renderer, 100, 0);
        render_sprite(renderer, rr_mob_id_honeybee, 4, flags);
        rr_renderer_context_state_free(renderer, &state);
        rr_renderer_translate(renderer, 75, 0);
        render_sprite(renderer, rr_mob_id_honeybee, 0, flags);
        break;

         case rr_mob_id_ladybug:
        rr_renderer_scale(renderer, 0.25f);
        // Голова
        rr_renderer_set_fill(renderer, 0xff222222);
        rr_renderer_set_stroke(renderer, 0xff111111);
        rr_renderer_set_line_width(renderer, 8);
        rr_renderer_begin_path(renderer);
        rr_renderer_arc(renderer, 65, 0, 45);
        rr_renderer_fill(renderer);
        rr_renderer_stroke(renderer);
        // Красное тело
        rr_renderer_set_fill(renderer, 0xffdf3030);
        rr_renderer_set_stroke(renderer, 0xff9e1b1b);
        rr_renderer_set_line_width(renderer, 10);
        rr_renderer_begin_path(renderer);
        rr_renderer_arc(renderer, -10, 0, 85);
        rr_renderer_fill(renderer);
        rr_renderer_stroke(renderer);
        // Черные пятнышки
        rr_renderer_set_fill(renderer, 0xff222222);
        rr_renderer_begin_path(renderer);
        rr_renderer_arc(renderer, -10, 0, 14);
        rr_renderer_arc(renderer, -45, -32, 13);
        rr_renderer_arc(renderer, -45, 32, 13);
        rr_renderer_arc(renderer, 18, -36, 13);
        rr_renderer_arc(renderer, 18, 36, 13);
        rr_renderer_fill(renderer);
        break;

    case rr_mob_id_worker_ant: case rr_mob_id_soldier_ant: case rr_mob_id_fire_worker_ant: case rr_mob_id_fire_soldier_ant: case rr_mob_id_termite_worker: case rr_mob_id_termite_soldier: case rr_mob_id_worm:
        render_sprite(renderer, id, 0, flags);
        break;
    case rr_mob_id_ant_egg:
    case rr_mob_id_fire_ant_egg:
    case rr_mob_id_termite_egg:
        rr_renderer_scale(renderer, 0.25f);
        rr_renderer_set_fill(renderer, id == rr_mob_id_ant_egg ? 0xfff5f0e1 : (id == rr_mob_id_fire_ant_egg ? 0xfff5a895 : 0xffe8d5b5));
        rr_renderer_set_stroke(renderer, id == rr_mob_id_ant_egg ? 0xffb8ae93 : (id == rr_mob_id_fire_ant_egg ? 0xffb84b32 : 0xff8c5828));
        rr_renderer_set_line_width(renderer, 12);
        rr_renderer_begin_path(renderer);
        rr_renderer_arc(renderer, -16.0f, 0.0f, 54.0f);
        rr_renderer_arc(renderer, 20.0f, 0.0f, 44.0f);
        rr_renderer_fill(renderer);
        rr_renderer_stroke(renderer);
        break;
    case rr_mob_id_queen_ant:
    case rr_mob_id_queen_fire_ant:
    case rr_mob_id_queen_termite:
    {
        rr_renderer_scale(renderer, 5.0f);
        uint8_t base_id = (id == rr_mob_id_queen_ant) ? rr_mob_id_soldier_ant : ((id == rr_mob_id_queen_fire_ant) ? rr_mob_id_fire_soldier_ant : rr_mob_id_termite_soldier);
        render_sprite(renderer, base_id, 0, flags);
        rr_renderer_scale(renderer, 0.25f);
        rr_renderer_set_fill(renderer, 0xffffd700);
        rr_renderer_set_stroke(renderer, 0xff9e7b00);
        rr_renderer_set_line_width(renderer, 6);
        rr_renderer_begin_path(renderer);
        rr_renderer_move_to(renderer, -22, -26);
        rr_renderer_line_to(renderer, 16, -34);
        rr_renderer_line_to(renderer, 4, -12);
        rr_renderer_line_to(renderer, 24, 0);
        rr_renderer_line_to(renderer, 4, 12);
        rr_renderer_line_to(renderer, 16, 34);
        rr_renderer_line_to(renderer, -22, 26);
        rr_renderer_line_to(renderer, -22, -26);
        rr_renderer_fill(renderer);
        rr_renderer_stroke(renderer);
        break;
    }
        case rr_mob_id_rock:
        rr_renderer_scale(renderer, 0.25f);
        rr_renderer_set_fill(renderer, 0xff777777);
        rr_renderer_set_stroke(renderer, 0xff4d4d4d);
        rr_renderer_set_line_join(renderer, 1);
        rr_renderer_set_line_width(renderer, 14);
        rr_renderer_begin_path(renderer);
        rr_renderer_move_to(renderer, 95, 0);
        rr_renderer_line_to(renderer, 55, 78);
        rr_renderer_line_to(renderer, -35, 88);
        rr_renderer_line_to(renderer, -92, 30);
        rr_renderer_line_to(renderer, -75, -62);
        rr_renderer_line_to(renderer, 15, -90);
        rr_renderer_line_to(renderer, 78, -55);
        rr_renderer_line_to(renderer, 95, 0);
        rr_renderer_fill(renderer);
        rr_renderer_stroke(renderer);
        break;
 
    case rr_mob_id_dragonfly:
        rr_renderer_scale(renderer, 0.2);
        rr_renderer_translate(renderer, -90, 0);
        render_sprite(renderer, id, 2, flags);
        rr_renderer_translate(renderer, 90, 0);
        render_sprite(renderer, id, 1, flags);
        rr_renderer_context_state_init(renderer, &state);
        rr_renderer_rotate(renderer, animation_tick * 0.2f);
        rr_renderer_translate(renderer, 0, -100);
        render_sprite(renderer, id, 3, flags);
        rr_renderer_context_state_free(renderer, &state);
        rr_renderer_context_state_init(renderer, &state);
        rr_renderer_scale2(renderer, 1, -1);
        rr_renderer_rotate(renderer, animation_tick * -0.2f);
        rr_renderer_translate(renderer, 0, -100);
        render_sprite(renderer, id, 3, flags);
        rr_renderer_context_state_free(renderer, &state);
        rr_renderer_translate(renderer, 90, 0);
        render_sprite(renderer, id, 0, flags);
        break;
    case rr_mob_id_spider:
        rr_renderer_scale(renderer, 0.2);

        rr_renderer_context_state_init(renderer, &state);
        rr_renderer_rotate(renderer, animation_tick * 0.05f + M_PI / 4);
        rr_renderer_translate(renderer, 100, 0);
        rr_renderer_scale2(renderer, 1, -1);
        render_sprite(renderer, id, 2, flags);
        rr_renderer_context_state_free(renderer, &state);
        rr_renderer_context_state_init(renderer, &state);
        rr_renderer_rotate(renderer, animation_tick * -0.05f + 5 * M_PI / 12);
        rr_renderer_translate(renderer, 100, 0);
        rr_renderer_scale2(renderer, 1, -1);
        render_sprite(renderer, id, 2, flags);
        rr_renderer_context_state_free(renderer, &state);
        rr_renderer_context_state_init(renderer, &state);
        rr_renderer_rotate(renderer, animation_tick * 0.05f + 7 * M_PI / 12);
        rr_renderer_translate(renderer, 100, 0);
        render_sprite(renderer, id, 2, flags);
        rr_renderer_context_state_free(renderer, &state);
        rr_renderer_context_state_init(renderer, &state);
        rr_renderer_rotate(renderer, animation_tick * -0.05f + 3 * M_PI / 4);
        rr_renderer_translate(renderer, 100, 0);
        render_sprite(renderer, id, 2, flags);
        rr_renderer_context_state_free(renderer, &state);

        rr_renderer_context_state_init(renderer, &state);
        rr_renderer_rotate(renderer, animation_tick * 0.05f - M_PI / 4);
        rr_renderer_translate(renderer, 100, 0);
        render_sprite(renderer, id, 2, flags);
        rr_renderer_context_state_free(renderer, &state);
        rr_renderer_context_state_init(renderer, &state);
        rr_renderer_rotate(renderer, animation_tick * -0.05f - 5 * M_PI / 12);
        rr_renderer_translate(renderer, 100, 0);
        render_sprite(renderer, id, 2, flags);
        rr_renderer_context_state_free(renderer, &state);
        rr_renderer_context_state_init(renderer, &state);
        rr_renderer_rotate(renderer, animation_tick * 0.05f - 7 * M_PI / 12);
        rr_renderer_translate(renderer, 100, 0);
        rr_renderer_scale2(renderer, 1, -1);
        render_sprite(renderer, id, 2, flags);
        rr_renderer_context_state_free(renderer, &state);
        rr_renderer_context_state_init(renderer, &state);
        rr_renderer_rotate(renderer, animation_tick * -0.05f - 3 * M_PI / 4);
        rr_renderer_translate(renderer, 100, 0);
        rr_renderer_scale2(renderer, 1, -1);
        render_sprite(renderer, id, 2, flags);
        rr_renderer_context_state_free(renderer, &state);

        // rr_renderer_translate(renderer, -120, 0);
        // render_sprite(renderer, id, 1, flags);
        rr_renderer_translate(renderer, 10, 0);
        render_sprite(renderer, id, 0, flags);
        break;
    case rr_mob_id_house_centipede:
        if (!(flags & 4))
        {
            rr_renderer_translate(renderer, 58.7, 0);
            render_sprite(renderer, id, 0, flags);
        }
        else
        {
            rr_renderer_context_state_init(renderer, &state);
            rr_renderer_rotate(renderer, animation_tick * 0.1f + M_PI / 2);
            rr_renderer_translate(renderer, 55, 0);
            render_sprite(renderer, id, 2, flags);
            rr_renderer_context_state_free(renderer, &state);
            rr_renderer_context_state_init(renderer, &state);
            rr_renderer_rotate(renderer, animation_tick * 0.1f - M_PI / 2);
            rr_renderer_translate(renderer, 55, 0);
            rr_renderer_scale2(renderer, 1, -1);
            render_sprite(renderer, id, 2, flags);
            rr_renderer_context_state_free(renderer, &state);
            render_sprite(renderer, id, 1, flags);
        }
        break;
    }

    rr_renderer_context_state_free(renderer, &original_state);
}

static void friendly_mask(struct rr_renderer *renderer)
{
    rr_renderer_add_color_filter(renderer, 0xffffff45, 0.3);
}


static void rr_custom_ant_draw(struct rr_renderer *r, uint32_t b, uint32_t h, uint32_t s, int m) {
    struct rr_renderer_context_state st; rr_renderer_context_state_init(r, &st);
    rr_renderer_set_line_width(r, 7); rr_renderer_set_stroke(r, s);
    for (int i = -1; i <= 1; ++i) {
        rr_renderer_begin_path(r); rr_renderer_move_to(r, i*24.0f, -25.0f); rr_renderer_line_to(r, i*24.0f-14.0f, -68.0f); rr_renderer_stroke(r);
        rr_renderer_begin_path(r); rr_renderer_move_to(r, i*24.0f, 25.0f); rr_renderer_line_to(r, i*24.0f-14.0f, 68.0f); rr_renderer_stroke(r);
    }
    rr_renderer_set_line_width(r, m ? 8 : 5);
    rr_renderer_begin_path(r); rr_renderer_move_to(r, 68.0f, -14.0f); rr_renderer_line_to(r, 98.0f, m ? -6.0f : -24.0f);
    rr_renderer_move_to(r, 68.0f, 14.0f); rr_renderer_line_to(r, 98.0f, m ? 6.0f : 24.0f); rr_renderer_stroke(r);
    rr_renderer_set_fill(r, b); rr_renderer_set_line_width(r, 8);
    rr_renderer_begin_path(r); rr_renderer_arc(r, -52.0f, 0.0f, 40.0f); rr_renderer_fill(r); rr_renderer_stroke(r);
    rr_renderer_begin_path(r); rr_renderer_arc(r, 0.0f, 0.0f, 27.0f); rr_renderer_fill(r); rr_renderer_stroke(r);
    rr_renderer_set_fill(r, h);
    rr_renderer_begin_path(r); rr_renderer_arc(r, 46.0f, 0.0f, 30.0f); rr_renderer_fill(r); rr_renderer_stroke(r);
    rr_renderer_context_state_free(r, &st);
}
static void rr_wa_d(struct rr_renderer *r){rr_custom_ant_draw(r,0xff454545,0xff383838,0xff1f1f1f,0);}
static void rr_sa_d(struct rr_renderer *r){rr_custom_ant_draw(r,0xff3d3d3d,0xff2b2b2b,0xff141414,1);}
static void rr_fwa_d(struct rr_renderer *r){rr_custom_ant_draw(r,0xffd94126,0xffb82c14,0xff6e1607,0);}
static void rr_fsa_d(struct rr_renderer *r){rr_custom_ant_draw(r,0xffc73218,0xff9e1f09,0xff590f03,1);}
static void rr_tw_d(struct rr_renderer *r){rr_custom_ant_draw(r,0xffe8d5b5,0xff8c5828,0xff4d2e12,0);}
static void rr_ts_d(struct rr_renderer *r){rr_custom_ant_draw(r,0xffdec49b,0xff703f15,0xff3d2007,1);}
static void rr_wm_d(struct rr_renderer *r){
    struct rr_renderer_context_state st; rr_renderer_context_state_init(r, &st);
    rr_renderer_set_fill(r, 0xffc98e7b); rr_renderer_set_stroke(r, 0xff7a4d3f); rr_renderer_set_line_width(r, 9);
    rr_renderer_begin_path(r); rr_renderer_arc(r, 0.0f, 0.0f, 68.0f); rr_renderer_fill(r); rr_renderer_stroke(r);
    rr_renderer_context_state_free(r, &st);
}

void rr_renderer_mob_cache_init()
{
    rr_renderer_spritesheet_init(
        &mob_sprites[0], NULL, 336, 192, rr_triceratops_head_draw, 336, 192,
        rr_triceratops_body_draw, 240, 240, rr_triceratops_leg1_draw, 240, 240,
        rr_triceratops_leg2_draw, 336, 192, rr_triceratops_tail_draw, 0);

    rr_renderer_spritesheet_init(
        &mob_sprites[1], NULL, 240, 144, rr_t_rex_head_draw, 336, 192,
        rr_t_rex_body_draw, 240, 240, rr_t_rex_leg1_draw, 240, 240,
        rr_t_rex_leg2_draw, 336, 192, rr_t_rex_tail_draw, 0);

    rr_renderer_spritesheet_init(
        &friendly_mob_sprites[0], friendly_mask, 240, 144, rr_t_rex_head_draw,
        336, 192, rr_t_rex_body_draw, 240, 240, rr_t_rex_leg1_draw, 240, 240,
        rr_t_rex_leg2_draw, 336, 192, rr_t_rex_tail_draw, 0);

    rr_renderer_spritesheet_init(&mob_sprites[2], NULL, 672, 672, rr_fern_draw,
                                 0);

    rr_renderer_spritesheet_init(&mob_sprites[3], NULL, 384, 384, rr_tree_draw,
                                 0);

    rr_renderer_spritesheet_init(
        &mob_sprites[4], NULL, 336, 192, rr_pteranodon_body_draw, 288, 432,
        rr_pteranodon_wing1_draw, 288, 432, rr_pteranodon_wing2_draw, 0);

    rr_renderer_spritesheet_init(
        &mob_sprites[5], NULL, 240, 144, rr_dakotaraptor_head_draw, 336, 192,
        rr_dakotaraptor_body_draw, 240, 144, rr_dakotaraptor_wing1_draw, 240,
        144, rr_dakotaraptor_wing2_draw, 336, 192, rr_dakotaraptor_tail_draw,
        0);

    rr_renderer_spritesheet_init(&mob_sprites[6], NULL, 240, 144,
                                 rr_pachycephalosaurus_head_draw, 336, 192,
                                 rr_pachycephalosaurus_body_draw, 240, 240,
                                 rr_pachycephalosaurus_leg1_draw, 240, 240,
                                 rr_pachycephalosaurus_leg2_draw, 336, 192,
                                 rr_pachycephalosaurus_tail_draw, 0);

    rr_renderer_spritesheet_init(
        &mob_sprites[7], NULL, 240, 144, rr_ornithomimus_head_draw, 336, 192,
        rr_ornithomimus_body_draw, 240, 144, rr_ornithomimus_wing1_draw, 240,
        144, rr_ornithomimus_wing2_draw, 336, 192, rr_ornithomimus_tail_draw,
        0);

    rr_renderer_spritesheet_init(
        &mob_sprites[8], NULL, 144, 144, rr_ankylosaurus_head_draw, 336, 192,
        rr_ankylosaurus_body_draw, 336, 192, rr_ankylosaurus_tail_draw, 0);

    rr_renderer_spritesheet_init(&mob_sprites[9], NULL, 240, 144,
                                 rr_meteor_draw, 0);

    rr_renderer_spritesheet_init(&friendly_mob_sprites[1], friendly_mask,
                                 240, 144, rr_meteor_draw, 0);

    rr_renderer_spritesheet_init(
        &mob_sprites[10], NULL, 336, 192, rr_quetzalcoatlus_head_draw, 336, 192,
        rr_quetzalcoatlus_body_draw, 336, 192, rr_quetzalcoatlus_wing1_draw,
        336, 192, rr_quetzalcoatlus_wing2_draw, 0);

    rr_renderer_spritesheet_init(
        &mob_sprites[11], NULL, 240, 144, rr_edmontosaurus_head_draw, 339, 192,
        rr_edmontosaurus_body_draw, 240, 240, rr_edmontosaurus_leg1_draw, 240,
        240, rr_edmontosaurus_leg2_draw, 336, 192, rr_edmontosaurus_tail_draw,
        0);
    // garden
    rr_renderer_spritesheet_init(&mob_sprites[12], NULL, 192, 192,
                                 rr_ant_head_draw, 192, 192, rr_ant_thorax_draw,
                                 192, 192, rr_ant_abdomen_draw, 192, 192,
                                 rr_ant_leg_draw, 0);

    rr_renderer_spritesheet_init(
        &mob_sprites[13], NULL, 192, 192, rr_hornet_head_draw, 192, 192,
        rr_hornet_thorax_draw, 192, 192, rr_hornet_abdomen_draw, 192, 192,
        rr_hornet_leg_draw, 192, 192, rr_hornet_wing_draw, 0);

    rr_renderer_spritesheet_init(
        &mob_sprites[14], NULL, 192, 192, rr_dragonfly_head_draw, 192, 192,
        rr_dragonfly_thorax_draw, 192, 192, rr_dragonfly_abdomen_draw, 192, 192,
        rr_dragonfly_wing_draw, 0);

    rr_renderer_spritesheet_init(
        &mob_sprites[15], NULL, 192, 192, rr_honeybee_head_draw, 192, 192,
        rr_honeybee_thorax_draw, 192, 192, rr_honeybee_abdomen_draw, 192, 192,
        rr_honeybee_leg_draw, 192, 192, rr_honeybee_wing_draw, 0);

    rr_renderer_spritesheet_init(&mob_sprites[16], NULL, 384, 384,
                                 rr_beehive_draw, 0);

    rr_renderer_spritesheet_init(
        &mob_sprites[17], NULL, 240, 240, rr_spider_head_draw, 240, 240,
        rr_spider_abdomen_draw, 240, 240, rr_spider_leg_draw, 0);

    rr_renderer_spritesheet_init(&mob_sprites[18], NULL, 240, 240,
                                 rr_house_centipede_head_draw, 240, 240,
                                 rr_house_centipede_body_draw, 240, 240,
                                 rr_house_centipede_leg_draw, 0);

    rr_renderer_spritesheet_init(&mob_sprites[23], NULL, 240, 240, rr_wa_d, 0);
    rr_renderer_spritesheet_init(&mob_sprites[24], NULL, 240, 240, rr_sa_d, 0);
    rr_renderer_spritesheet_init(&mob_sprites[25], NULL, 240, 240, rr_fwa_d, 0);
    rr_renderer_spritesheet_init(&mob_sprites[26], NULL, 240, 240, rr_fsa_d, 0);
    rr_renderer_spritesheet_init(&mob_sprites[27], NULL, 240, 240, rr_tw_d, 0);
    rr_renderer_spritesheet_init(&mob_sprites[28], NULL, 240, 240, rr_ts_d, 0);
    rr_renderer_spritesheet_init(&mob_sprites[29], NULL, 240, 240, rr_wm_d, 0);
}
