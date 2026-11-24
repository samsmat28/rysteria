#include <Server/Server.h>
#include <Server/Simulation.h>
#include <Server/Client.h>
#include <Shared/StaticData.h>
#include <Shared/Utilities.h>
#include <stdio.h>
#include <string.h>

#ifdef ESCAPE
static int esc_stage = 0, esc_sub = 0;
static uint8_t esc_init_done = 0;
extern void rr_send_shop_msg(struct rr_server_client *client, const char *text);

static void esc_broadcast(struct rr_server *srv, const char *txt) {
    for (uint32_t i = 0; i < srv->clients_capacity; ++i)
        if (srv->clients[i].verified && srv->clients[i].player_info)
            rr_send_shop_msg(&srv->clients[i], txt);
}

static void esc_clear_mobs(struct rr_simulation *sim) {
    for (EntityIdx e = 1; e < sim->entities_capacity; ++e)
        if (rr_simulation_has_mob(sim, e))
            rr_simulation_free_entity(sim, e);
}

static int esc_count_mob(struct rr_simulation *sim, enum rr_mob_id id) {
    int c = 0;
    for (EntityIdx e = 1; e < sim->entities_capacity; ++e)
        if (rr_simulation_has_mob(sim, e) && rr_simulation_get_mob(sim, e)->id == id)
            c++;
    return c;
}
static void esc_setup_room(struct rr_server *srv, int stage) {
    struct rr_simulation *sim = &srv->simulation;
    EntityIdx aid = sim->arena;
    float gs = rr_simulation_get_arena(sim, aid)->maze->grid_size * 2.0f;
    esc_clear_mobs(sim); esc_stage = stage; esc_sub = 0;
    float sx = (6.0f + stage * 12.0f) * gs, sy = 31.0f * gs;
    for (uint32_t i = 0; i < srv->clients_capacity; ++i) {
        struct rr_server_client *cl = &srv->clients[i];
        if (!cl->verified || !cl->player_info) continue;
        cl->checkpoint[RR_GLOBAL_BIOME] = (uint8_t)(stage < 5 ? stage : 4);
        if (cl->player_info->flower_id != RR_NULL_ENTITY) {
            struct rr_component_physical *ph = rr_simulation_get_physical(sim, cl->player_info->flower_id);
            if (ph) { rr_component_physical_set_x(ph, sx); rr_component_physical_set_y(ph, sy); }
        }
    }
    if (stage == 0) {
        rr_simulation_alloc_mob(sim, aid, 8.0f*gs, 25.0f*gs, rr_mob_id_meteor, rr_rarity_id_common, rr_simulation_team_id_mobs);
        rr_simulation_alloc_mob(sim, aid, 8.0f*gs, 31.0f*gs, rr_mob_id_lanternfly, rr_rarity_id_common, rr_simulation_team_id_mobs);
        rr_simulation_alloc_mob(sim, aid, 8.0f*gs, 37.0f*gs, rr_mob_id_fern, rr_rarity_id_common, rr_simulation_team_id_mobs);
        esc_broadcast(srv, "[Escape 1/5] Сломай по порядку: 1) Meteor -> 2) Lanternfly -> 3) Fern!");
    } else if (stage == 1) {
        rr_simulation_alloc_mob(sim, aid, 20.0f*gs, 22.0f*gs, rr_mob_id_lanternfly, rr_rarity_id_rare, rr_simulation_team_id_mobs);
        rr_simulation_alloc_mob(sim, aid, 20.0f*gs, 31.0f*gs, rr_mob_id_spider, rr_rarity_id_uncommon, rr_simulation_team_id_mobs);
        esc_broadcast(srv, "[Escape 2/5] Иллюзия: сломай северный маяк Lanternfly у верхней стены!");
    } else if (stage == 2) {
        rr_simulation_alloc_mob(sim, aid, 32.0f*gs, 26.0f*gs, rr_mob_id_dakotaraptor, rr_rarity_id_epic, rr_simulation_team_id_mobs);
        rr_simulation_alloc_mob(sim, aid, 32.0f*gs, 36.0f*gs, rr_mob_id_dakotaraptor, rr_rarity_id_epic, rr_simulation_team_id_mobs);
        esc_broadcast(srv, "[Escape 3/5] Нажимная плита: дойди в правый нижний угол комнаты!");
    }
    else if (stage == 3) {
        for (int k = 0; k < 3; k++) {
            float ry = (24.0f + k * 7.0f) * gs;
            rr_simulation_alloc_mob(sim, aid, 44.0f*gs, ry, rr_mob_id_rock, rr_rarity_id_rare, rr_simulation_team_id_mobs);
            rr_simulation_alloc_mob(sim, aid, 45.0f*gs, ry, rr_mob_id_ant_egg, rr_rarity_id_epic, rr_simulation_team_id_mobs);
        }
        esc_broadcast(srv, "[Escape 4/5] Древние печати: разбей валуны и уничтожь 3 яйца-тотема!");
    } else if (stage == 4) {
        rr_simulation_alloc_mob(sim, aid, 57.0f*gs, 31.0f*gs, rr_mob_id_trex, rr_rarity_id_legendary, rr_simulation_team_id_mobs);
        esc_broadcast(srv, "[Escape 5/5] ФИНАЛ: победи Хранителя T-Rex (+1500 R)!");
    } else {
        esc_broadcast(srv, "[Escape ПОБЕДА!] Все 5 комнат пройдены! Выдано +1500 R!");
        for (uint32_t i = 0; i < srv->clients_capacity; ++i) {
            struct rr_server_client *cl = &srv->clients[i];
            if (!cl->verified || !cl->player_info) continue;
            cl->r_coins += 1500; cl->checkpoint[RR_GLOBAL_BIOME] = 0;
            rr_server_client_write_account(cl);
        }
        esc_sub = 250;
    }
}

void rr_escape_room_tick(struct rr_server *srv) {
    struct rr_simulation *sim = &srv->simulation;
    int players = 0; float px = 0, py = 0;
    for (uint32_t i = 0; i < srv->clients_capacity; ++i)
        if (srv->clients[i].verified && srv->clients[i].player_info && srv->clients[i].player_info->flower_id != RR_NULL_ENTITY) {
            players++;
            struct rr_component_physical *ph = rr_simulation_get_physical(sim, srv->clients[i].player_info->flower_id);
            if (ph) { px = ph->x; py = ph->y; }
        }
    if (players == 0) { esc_init_done = 0; return; }
    if (!esc_init_done) { esc_init_done = 1; esc_setup_room(srv, 0); return; }
    float gs = rr_simulation_get_arena(sim, sim->arena)->maze->grid_size * 2.0f;
    if (esc_stage == 0) {
        int m = esc_count_mob(sim, rr_mob_id_meteor), l = esc_count_mob(sim, rr_mob_id_lanternfly), f = esc_count_mob(sim, rr_mob_id_fern);
        if ((m > 0 && (l == 0 || f == 0)) || (l > 0 && f == 0)) { esc_broadcast(srv, "[Escape 1/5] Неверный порядок! Meteor -> Lanternfly -> Fern."); esc_setup_room(srv, 0); }
        else if (m == 0 && l == 0 && f == 0) esc_setup_room(srv, 1);
    } else if (esc_stage == 1 && esc_count_mob(sim, rr_mob_id_lanternfly) == 0) esc_setup_room(srv, 2);
    else if (esc_stage == 2 && px >= 34.0f * gs && py >= 38.0f * gs) esc_setup_room(srv, 3);
    else if (esc_stage == 3 && esc_count_mob(sim, rr_mob_id_ant_egg) == 0) esc_setup_room(srv, 4);
    else if (esc_stage == 4 && esc_count_mob(sim, rr_mob_id_trex) == 0) esc_setup_room(srv, 5);
    else if (esc_stage == 5 && --esc_sub <= 0) esc_setup_room(srv, 0);
}
#endif
