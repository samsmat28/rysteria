import re

# 1. Shared/StaticData.h: добавляем 6 мобов (30..35)
with open("Shared/StaticData.h", "r") as f:
    h = f.read()

if "rr_mob_id_ant_egg" not in h:
    h = re.sub(
        r"(rr_mob_id_worm\s*,[^\n]*\n)\s*rr_mob_id_max\s*,[^\n]*",
        r"""\1    rr_mob_id_ant_egg,               // 30
    rr_mob_id_fire_ant_egg,          // 31
    rr_mob_id_termite_egg,           // 32
    rr_mob_id_queen_ant,             // 33
    rr_mob_id_queen_fire_ant,        // 34
    rr_mob_id_queen_termite,         // 35

    rr_mob_id_max,                   // 36""",
        h,
        count=1
    )
    with open("Shared/StaticData.h", "w") as f:
        f.write(h)

# 2. Shared/StaticData.c: статы, имена и нули для Hell Creek
with open("Shared/StaticData.c", "r") as f:
    c = f.read()

if "rr_mob_id_ant_egg" not in c:
    c = re.sub(
        r'(\{rr_mob_id_worm\b.*?\},\s*\n)(\};)',
        r"""\1    {rr_mob_id_ant_egg,          rr_rarity_id_common, rr_rarity_id_ultimate, 18,  0, 16.0f, rr_rarity_id_max, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_leaf, 0.25},{rr_petal_id_clover, 0.10}}},
    {rr_mob_id_fire_ant_egg,     rr_rarity_id_common, rr_rarity_id_ultimate, 24,  0, 17.0f, rr_rarity_id_max, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_stinger, 0.25},{rr_petal_id_pellet, 0.15}}},
    {rr_mob_id_termite_egg,      rr_rarity_id_common, rr_rarity_id_ultimate, 22,  0, 17.0f, rr_rarity_id_max, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_sand, 0.25},{rr_petal_id_pellet, 0.15}}},
    {rr_mob_id_queen_ant,        rr_rarity_id_common, rr_rarity_id_ultimate, 140, 28, 36.0f, rr_rarity_id_max, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_clover, 0.40},{rr_petal_id_rice, 0.35}}},
    {rr_mob_id_queen_fire_ant,   rr_rarity_id_common, rr_rarity_id_ultimate, 180, 36, 38.0f, rr_rarity_id_max, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_mandible, 0.40},{rr_petal_id_stinger, 0.35}}},
    {rr_mob_id_queen_termite,    rr_rarity_id_common, rr_rarity_id_ultimate, 165, 32, 37.0f, rr_rarity_id_max, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_mandible, 0.40},{rr_petal_id_sand, 0.35}}},
\2""",
        c,
        count=1
    )
    c = c.replace('"Worm"\n};', '"Worm", "Ant Egg", "Fire Ant Egg", "Termite Egg", "Queen Ant", "Queen Fire Ant", "Queen Termite"\n};', 1)
    c = c.replace("    0, 0, 0, 0, 0, 0, 0\n};", "    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0\n};", 1)
    with open("Shared/StaticData.c", "w") as f:
        f.write(c)

# 3. Server/Waves.c: спавним в Ant Hell также яйца и королев
with open("Server/Waves.c", "r") as f:
    w = f.read()

if "rr_mob_id_queen_ant" not in w:
    old_block = """        if (r_ant ticks_until_next_action == 0) ai->ticks_until_next_action = 125; // ~5 сек до вылупления
    if (ai->ticks_until_next_action == 1)
    {
        uint8_t hatch_id = (rr_frand() < 0.65) ? worker_id : soldier_id;
        rr_simulation_allocate_mob(sim, phys->arena, hatch_id, mob->rarity, phys->x, phys->y);
        rr_simulation_request_entity_deletion(sim, entity);
    }
}

static void tick_ai_ant_queen(EntityIdx entity, struct rr_simulation *sim, uint8_t egg_id)
{
    struct rr_component_ai *ai = rr_simulation_get_ai(sim, entity);
    struct rr_component_physical *phys = rr_simulation_get_physical(sim, entity);
    struct rr_component_mob *mob = rr_simulation_get_mob(sim, entity);
    if (!ai || !phys || !mob) return;
    ai->ai_type = rr_ai_type_aggro;
    tick_ai_aggro_default(entity, sim, RR_PLAYER_SPEED * 0.95f);
    if (ai->ticks_until_next_action <= 0)
    {
        float ang = rr_frand() * 6.28318f;
        rr_simulation_allocate_mob(sim, phys->arena, egg_id, mob->rarity, phys->x + cosf(ang) * 45.0f, phys->y + sinf(ang) * 45.0f);
        ai->ticks_until_next_action = 100; // раз в 4 сек откладывает яйцо
    }
}
"""
    ai = ai.replace("void rr_system_ai_tick(", eq_ai + "\nvoid rr_system_ai_tick(", 1)
    old_w = "        case rr_mob_id_worm: tick_ai_worm_underground(entity, this); break;"
    new_w = old_w + """
        case rr_mob_id_ant_egg: tick_ai_ant_egg(entity, this, rr_mob_id_worker_ant, rr_mob_id_soldier_ant); break;
        case rr_mob_id_fire_ant_egg: tick_ai_ant_egg(entity, this, rr_mob_id_fire_worker_ant, rr_mob_id_fire_soldier_ant); break;
        case rr_mob_id_termite_egg: tick_ai_ant_egg(entity, this, rr_mob_id_termite_worker, rr_mob_id_termite_soldier); break;
        case rr_mob_id_queen_ant: tick_ai_ant_queen(entity, this, rr_mob_id_ant_egg); break;
        case rr_mob_id_queen_fire_ant: tick_ai_ant_queen(entity, this, rr_mob_id_fire_ant_egg); break;
        case rr_mob_id_queen_termite: tick_ai_ant_queen(entity, this, rr_mob_id_termite_egg); break;"""
    ai = ai.replace(old_w, new_w, 1)
    with open("Server/System/_Ai.c", "w") as f:
        f.write(ai)

# 5. Client/Assets/RenderMobs.c: отрисовка яиц и королев с коронами
with open("Client/Assets/RenderMobs.c", "r") as f:
    rm = f.read()

if "rr_egg_draw_helper" not in rm:
    eq_draw = """
static void rr_egg_draw_helper(struct rr_renderer *r, uint32_t fill_c, uint32_t stroke_c) {
    struct rr_renderer_context_state st; rr_renderer_context_state_init(r, &st);
    rr_renderer_set_fill(r, fill_c); rr_renderer_set_stroke(r, stroke_c); rr_renderer_set_line_width(r, 8);
    rr_renderer_begin_path(r); rr_renderer_arc(r, -14.0f, 0.0f, 46.0f); rr_renderer_arc(r, 18.0f, 0.0f, 38.0f);
    rr_renderer_fill(r); rr_renderer_stroke(r);
    rr_renderer_context_state_free(r, &st);
}
static void rr_queen_draw_helper(struct rr_renderer *r, uint32_t b, uint32_t h, uint32_t s) {
    rr_custom_ant_draw(r, b, h, s, 1);
    struct rr_renderer_context_state st; rr_renderer_context_state_init(r, &st);
    rr_renderer_set_fill(r, 0xffffd700); rr_renderer_set_stroke(r, 0xff9e7b00); rr_renderer_set_line_width(r, 4);
    rr_renderer_begin_path(r);
    rr_renderer_move_to(r, -16, -18); rr_renderer_line_to(r, 12, -24); rr_renderer_line_to(r, 4, -8);
    rr_renderer_line_to(r, 18, 0); rr_renderer_line_to(r, 4, 8); rr_renderer_line_to(r, 12, 24);
    rr_renderer_line_to(r, -16, 18); rr_renderer_line_to(r, -16, -18);
    rr_renderer_fill(r); rr_renderer_stroke(r);
    rr_renderer_context_state_free(r, &st);
}
static void rr_ae_d(struct rr_renderer *r){rr_egg_draw_helper(r, 0xfff5f0e1, 0xffb8ae93);}
static void rr_fae_d(struct rr_renderer *r){rr_egg_draw_helper(r, 0xfff5a895, 0xffb84b32);}
static void rr_te_d(struct rr_renderer *r){rr_egg_draw_helper(r, 0xffe8d5b5, 0xff8c5828);}
static void rr_qa_d(struct rr_renderer *r){rr_queen_draw_helper(r, 0xff3d3d3d, 0xff2b2b2b, 0xff141414);}
static void rr_qfa_d(struct rr_renderer *r){rr_queen_draw_helper(r, 0xffc73218, 0xff9e1f09, 0xff590f03);}
static void rr_qt_d(struct rr_renderer *r){rr_queen_draw_helper(r, 0xffdec49b, 0xff703f15, 0xff3d2007);}
"""
    rm = rm.replace("void rr_renderer_mob_cache_init()", eq_draw + "\nvoid rr_renderer_mob_cache_init()", 1)
    inits = """
    rr_renderer_spritesheet_init(&mob_sprites, NULL, 240, 240, rr_ae_d, 0);
    rr_renderer_spritesheet_init(&mob_sprites, NULL, 240, 240, rr_fae_d, 0);
    rr_renderer_spritesheet_init(&mob_sprites, NULL, 240, 240, rr_te_d, 0);
    rr_renderer_spritesheet_init(&mob_sprites, NULL, 240, 240, rr_qa_d, 0);
    rr_renderer_spritesheet_init(&mob_sprites, NULL, 240, 240, rr_qfa_d, 0);
    rr_renderer_spritesheet_init(&mob_sprites, NULL, 240, 240, rr_qt_d, 0);
"""
    lb = rm.rfind("}")
    rm = rm[:lb] + inits + "}\n"
    rm = rm.replace("case rr_mob_id_worm:", "case rr_mob_id_worm: case rr_mob_id_ant_egg: case rr_mob_id_fire_ant_egg: case rr_mob_id_termite_egg: case rr_mob_id_queen_ant: case rr_mob_id_queen_fire_ant: case rr_mob_id_queen_termite:", 1)
    with open("Client/Assets/RenderMobs.c", "w") as f:
        f.write(rm)

print("Яйца и Королевы всех 3 видов готовы!")
