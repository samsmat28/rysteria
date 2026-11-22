with open("Server/System/_Ai.c", "r") as f: ai = f.read()
if "tick_ai_worm_underground" not in ai:
    worm_ai = """static void tick_ai_worm_underground(EntityIdx entity, struct rr_simulation *sim)
{
    struct rr_component_ai *ai = rr_simulation_get_ai(sim, entity);
    struct rr_component_physical *phys = rr_simulation_get_physical(sim, entity);
    struct rr_component_health *health = rr_simulation_get_health(sim, entity);
    struct rr_component_centipede *cent = rr_simulation_get_centipede(sim, entity);
    if (!ai || !phys || !health) return;
    if (cent && !cent->is_head) {
        EntityIdx parent = rr_simulation_resolve_entity_hash(sim, cent->parent_node);
        if (parent != RR_NULL_ENTITY) {
            struct rr_component_health *ph = rr_simulation_get_health(sim, parent);
            struct rr_component_physical *pp = rr_simulation_get_physical(sim, parent);
            if (ph && pp) {
                health->damage = ph->damage;
                if (pp->flags & 16) phys->flags |= 16; else phys->flags &= ~16;
            }
        }
        return;
    }
    tick_ai_aggro_default(entity, sim, RR_PLAYER_SPEED * 1.15f);
    float dmg = RR_MOB_DATA[rr_mob_id_worm].damage * RR_MOB_RARITY_SCALING[rr_simulation_get_mob(sim, entity)->rarity].damage;
    if (phys->flags & 16) {
        if (ai->ticks_until_next_action > 0) { health->damage = dmg; return; }
        phys->flags &= ~16; health->damage = 0; ai->ticks_until_next_action = 50; return;
    }
    health->damage = 0;
    if (ai->ticks_until_next_action target);
        if (t != RR_NULL_ENTITY) {
            struct rr_component_physical *tp = rr_simulation_get_physical(sim, t);
            if (tp && (tp->x - phys->x)*(tp->x - phys->x) + (tp->y - phys->y)*(tp->y - phys->y) < 3025.0f) {
                phys->flags |= 16; health->damage = dmg; ai->ticks_until_next_action = 35;
            }
        }
    }
}
"""
    ai = ai.replace("void rr_system_ai_tick(", worm_ai + "void rr_system_ai_tick(", 1)
    old_c = "        case rr_mob_id_rock: tick_ai_aggro_default(entity, this, RR_PLAYER_SPEED * 1.05); break;"
    new_c = old_c + """
        case rr_mob_id_worker_ant: if (ai->ai_type != rr_ai_type_aggro) ai->ai_type = rr_ai_type_neutral; tick_ai_aggro_default(entity, this, RR_PLAYER_SPEED * 1.05); break;
        case rr_mob_id_soldier_ant: ai->ai_type = rr_ai_type_aggro; tick_ai_aggro_default(entity, this, RR_PLAYER_SPEED * 1.25); break;
        case rr_mob_id_fire_worker_ant: if (ai->ai_type != rr_ai_type_aggro) ai->ai_type = rr_ai_type_neutral; tick_ai_aggro_default(entity, this, RR_PLAYER_SPEED * 1.15); break;
        case rr_mob_id_fire_soldier_ant: ai->ai_type = rr_ai_type_aggro; tick_ai_aggro_default(entity, this, RR_PLAYER_SPEED * 1.35); break;
        case rr_mob_id_termite_worker: if (ai->ai_type != rr_ai_type_aggro) ai->ai_type = rr_ai_type_neutral; tick_ai_aggro_default(entity, this, RR_PLAYER_SPEED * 1.05); break;
        case rr_mob_id_termite_soldier: ai->ai_type = rr_ai_type_aggro; tick_ai_aggro_default(entity, this, RR_PLAYER_SPEED * 1.25); break;
        case rr_mob_id_worm: tick_ai_worm_underground(entity, this); break;"""
    ai = ai.replace(old_c, new_c, 1)
    with open("Server/System/_Ai.c", "w") as f: f.write(ai)

with open("Client/Assets/RenderMobs.c", "r") as f: rm = f.read()
if "rr_custom_ant_draw" not in rm:
    helpers = """
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
"""
    rm = rm.replace("void rr_renderer_mob_cache_init()", helpers + "\nvoid rr_renderer_mob_cache_init()", 1)
    inits = """
    rr_renderer_spritesheet_init(&mob_sprites[23], NULL, 240, 240, rr_wa_d, 0);
    rr_renderer_spritesheet_init(&mob_sprites[24], NULL, 240, 240, rr_sa_d, 0);
    rr_renderer_spritesheet_init(&mob_sprites[25], NULL, 240, 240, rr_fwa_d, 0);
    rr_renderer_spritesheet_init(&mob_sprites[26], NULL, 240, 240, rr_fsa_d, 0);
    rr_renderer_spritesheet_init(&mob_sprites[27], NULL, 240, 240, rr_tw_d, 0);
    rr_renderer_spritesheet_init(&mob_sprites[28], NULL, 240, 240, rr_ts_d, 0);
    rr_renderer_spritesheet_init(&mob_sprites[29], NULL, 240, 240, rr_wm_d, 0);
"""
    lb = rm.rfind("}")
    rm = rm[:lb] + inits + "}\n"
    rm = rm.replace("case rr_mob_id_rock:", "case rr_mob_id_worker_ant: case rr_mob_id_soldier_ant: case rr_mob_id_fire_worker_ant: case rr_mob_id_fire_soldier_ant: case rr_mob_id_termite_worker: case rr_mob_id_termite_soldier: case rr_mob_id_worm: render_sprite(renderer, id, 0, flags); break;\n        case rr_mob_id_rock:", 1)
    with open("Client/Assets/RenderMobs.c", "w") as f: f.write(rm)

print("PART 2 OK")
