#include <time.h>
#include <strings.h>
#include <sys/stat.h>
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

#include <Server/Server.h>

#include <assert.h>
#include <ctype.h>
#include <math.h>
#include <pthread.h>
#include <string.h>
#include <sys/time.h>
#include <unistd.h>

#include <libwebsockets.h>

#include <Server/Client.h>
#include <Server/EntityAllocation.h>
#include <Server/Logs.h>
#include <Server/Simulation.h>
#include <Server/UpdateProtocol.h>
#include <Server/Waves.h>
#include <Shared/Api.h>
#include <Shared/Binary.h>
#include <Shared/Bitset.h>
#include <Shared/Component/Physical.h>
#include <Shared/Crypto.h>
#include <Shared/Rivet.h>
#include <Shared/Utilities.h>
#include <Shared/Vector.h>
#include <Shared/cJSON.h>
#include <Shared/pb.h>

uint8_t lws_message_data[MESSAGE_BUFFER_SIZE];
uint8_t *outgoing_message = lws_message_data + LWS_PRE;

struct connected_captures
{
    char *token;
    struct rr_server_client *client;
};

struct dev_cheat_captures
{
    struct rr_simulation *simulation;
    struct rr_component_player_info *player_info;
};

static void *rivet_connected_endpoint(void *_captures)
{
    struct connected_captures *captures = _captures;
    struct rr_server_client *this = captures->client;
    char *token = captures->token;
    if (!rr_rivet_players_connected(getenv("RIVET_TOKEN"), token))
        if (strcmp(token, this->rivet_account.token) == 0)
            this->pending_kick = 1;
    free(token);
    free(captures);
    return NULL;
}

static void *rivet_disconnected_endpoint(void *_captures)
{
    char *token = _captures;
    rr_rivet_players_disconnected(getenv("RIVET_TOKEN"), token);
    free(_captures);
    return NULL;
}

static void rr_server_client_create_player_info(struct rr_server *server,
                                                struct rr_server_client *client)
{
    puts("creating player info");
    struct rr_component_player_info *player_info = client->player_info =
        rr_simulation_add_player_info(
            &server->simulation,
            rr_simulation_alloc_entity(&server->simulation));
    player_info->client = client;
    rr_component_player_info_set_squad(player_info, client->squad);
    struct rr_squad_member *member = player_info->squad_member =
        rr_squad_get_client_slot(server, client);
    rr_component_player_info_set_squad_pos(player_info, client->squad_pos);
    rr_component_player_info_set_slot_count(player_info, RR_MAX_SLOT_COUNT);
    player_info->level = level_from_xp(client->experience);
    rr_component_player_info_set_slot_count(
        client->player_info, RR_SLOT_COUNT_FROM_LEVEL(player_info->level));
    struct rr_component_arena *arena =
        rr_simulation_get_arena(&server->simulation, 1);
    for (uint64_t i = 0; i < player_info->slot_count; ++i)
    {
        uint8_t id = member->loadout[i].id;
        uint8_t rarity = member->loadout[i].rarity;
        player_info->slots[i].id = id;
        player_info->slots[i].rarity = rarity;
        player_info->slots[i].count = RR_PETAL_DATA[id].count[rarity];
        for (uint64_t j = 0; j < player_info->slots[i].count; ++j)
            player_info->slots[i].petals[j].cooldown_ticks =
                RR_PETAL_DATA[id].cooldown;

        id = member->loadout[i + RR_MAX_SLOT_COUNT].id;
        rarity = member->loadout[i + RR_MAX_SLOT_COUNT].rarity;
        player_info->secondary_slots[i].id = id;
        player_info->secondary_slots[i].rarity = rarity;
    }
}

void rr_server_client_free(struct rr_server_client *this)
{
    // WARNING: ONLY TO BE USED WHEN CLIENT DISCONNECTS
    if (this->player_info != NULL)
        rr_simulation_request_entity_deletion(&this->server->simulation,
                                              this->player_info->parent_id);
    rr_client_leave_squad(this->server, this);
    uint8_t i = this - this->server->clients;
    for (uint32_t j = 0; j < this->server->simulation.drop_count; ++j)
    {
        EntityIdx drop_id = this->server->simulation.drop_vector[j];
        struct rr_component_drop *drop =
            rr_simulation_get_drop(&this->server->simulation, drop_id);
        rr_bitset_unset(drop->can_be_picked_up_by, i);
        rr_bitset_unset(drop->picked_up_by, i);
    }
    struct rr_server_client_message *message = this->message_root;
    while (message != NULL)
    {
        struct rr_server_client_message *tmp = message->next;
        free(message->packet);
        free(message);
        message = tmp;
    }
    this->message_at = this->message_root = NULL;
    this->message_length = 0;
    puts("<rr_server::client_disconnect>");
}

static void rr_send_shop_state(struct rr_server_client *client)
{
    if (!client || !client->socket_handle) return;
    uint8_t buf[64];
    struct proto_bug enc;
    proto_bug_init(&enc, buf);
    proto_bug_write_uint8(&enc, 250, "shop_sync");
    proto_bug_write_uint64(&enc, client->r_coins, "r_coins");
    proto_bug_write_uint8(&enc, client->quest_rarity, "q_rar");
    proto_bug_write_uint16(&enc, client->quest_target, "q_tgt");
    proto_bug_write_uint16(&enc, client->quest_progress, "q_prg");
    proto_bug_write_uint64(&enc, client->ch_mask_lo, "ch_lo");
    proto_bug_write_uint64(&enc, client->ch_mask_hi, "ch_hi");
    proto_bug_write_uint64(&enc, client->play_seconds, "play_sec");
    rr_server_client_write_message(client, enc.start, enc.current - enc.start);
}

static int rr_eval_q100(struct rr_server_client *c, int q, char *h, size_t hs) {
    if (!c || q < 1 || q > 100) return 0;
    uint64_t kb[12] = {0}, min_sp = UINT64_MAX;
    int sp_done = 0;
    uint64_t req_sp = (q > 90) ? (uint64_t)((q - 90) * 100) : 0;
    for (int m = 0; m < rr_mob_id_max; m++) {
        uint64_t ms = 0;
        for (int r = 0; r < rr_rarity_id_max; r++) {
            uint32_t v = c->mob_gallery[m][r];
            ms += v;
            if (r < 12) kb[r] += v;
        }
        if (ms < min_sp) min_sp = ms;
        if (req_sp > 0 && ms >= req_sp) sp_done++;
    }
    if (min_sp == UINT64_MAX) min_sp = 0;
    uint64_t ep = 0, mp = 0, uk = 0;
    for (int p = 0; p < rr_petal_id_max; p++)
        for (int r = 0; r < rr_rarity_id_max; r++) {
            if (r >= 3) ep += c->inventory[p][r];
            if (r >= 5) mp += c->inventory[p][r];
        }
    for (int r = 6; r < rr_rarity_id_max && r < 12; r++) uk += kb[r];
    static const uint64_t tr[20] = {
        60,180,300,600,1200,1800,2700,3600,7200,10800,
        18000,28800,43200,86400,259200,604800,1209600,2592000,5184000,8640000
    };
    static const uint64_t xr[20] = {
        500,1200,2500,5000,10000,18000,30000,45000,65000,90000,
        120000,160000,210000,270000,350000,450000,570000,700000,850000,1000000
    };
    static const uint64_t em[8] = {5,15,30,60,100,200,350,500};
    static const uint64_t lm[8] = {3,10,20,40,75,125,200,300};
    static const uint64_t mm[7] = {1,5,15,30,60,100,150};
    static const uint64_t um[7] = {1,3,10,20,40,70,100};
    int ok = 0;
    if (q <= 20) ok = (c->play_seconds >= tr[q - 1]);
    else if (q <= 40) ok = ((uint64_t)c->experience >= xr[q - 21]);
    else if (q <= 48) ok = (kb[3] >= em[q - 41]);
    else if (q <= 56) ok = (kb[4] >= lm[q - 49]);
    else if (q <= 63) ok = (kb[5] >= mm[q - 57]);
    else if (q <= 70) ok = (uk >= um[q - 64]);
    else if (q <= 80) ok = (ep >= (uint64_t)((q - 70) * 3));
    else if (q <= 90) ok = (mp >= (uint64_t)(q - 80));
    else ok = (min_sp >= req_sp);
    if (!ok && h && hs > 0) {
        if (q <= 20) snprintf(h, hs, "Time: %llu/%llus", (unsigned long long)c->play_seconds, (unsigned long long)tr[q-1]);
        else if (q <= 40) snprintf(h, hs, "XP: %llu/%llu", (unsigned long long)c->experience, (unsigned long long)xr[q-21]);
        else if (q <= 48) snprintf(h, hs, "Epic mobs: %llu/%llu", (unsigned long long)kb[3], (unsigned long long)em[q-41]);
        else if (q <= 56) snprintf(h, hs, "Leg mobs: %llu/%llu", (unsigned long long)kb[4], (unsigned long long)lm[q-49]);
        else if (q <= 63) snprintf(h, hs, "Myth mobs: %llu/%llu", (unsigned long long)kb[5], (unsigned long long)mm[q-57]);
        else if (q <= 70) snprintf(h, hs, "Ultra+ mobs: %llu/%llu", (unsigned long long)uk, (unsigned long long)um[q-64]);
        else if (q <= 80) snprintf(h, hs, "Epic+ petals: %llu/%d", (unsigned long long)ep, (q-70)*3);
        else if (q <= 90) snprintf(h, hs, "Myth+ petals: %llu/%d", (unsigned long long)mp, q-80);
        else snprintf(h, hs, "All species %llu: %d/%d (min %llu)", (unsigned long long)req_sp, sp_done, rr_mob_id_max, (unsigned long long)min_sp);
    }
    return ok;
}

static void write_animation_function(struct rr_simulation *simulation,
                                     struct proto_bug *encoder,
                                     struct rr_server_client *client,
                                     uint32_t pos)
{
    struct rr_simulation_animation *animation = &simulation->animations[pos];
    if (animation->type != rr_animation_type_chat &&
        client->player_info == NULL)
        return;
    EntityIdx p_info_id;
    if (animation->type == rr_animation_type_chat)
        p_info_id = animation->owner;
    else
        p_info_id = rr_simulation_get_relations(simulation,
                                                animation->owner)->root_owner;
    if (animation->type != rr_animation_type_chat &&
        p_info_id != client->player_info->parent_id)
    {
        if (animation->type == rr_animation_type_damagenumber &&
            animation->color_type == rr_animation_color_type_heal)
            return;
        if (dev_cheat_enabled(simulation, animation->owner, invisible))
            return;
    }
    if (animation->type == rr_animation_type_damagenumber &&
        animation->color_type != rr_animation_color_type_heal &&
        animation->squad != client->squad)
        return;
    if (animation->type == rr_animation_type_chat)
    {
        struct rr_server_client *sender =
            rr_simulation_get_player_info(simulation, p_info_id)->client;
        for (uint8_t i = 0; i < RR_MAX_CLIENT_COUNT; ++i)
            if (strcmp(client->blocked_clients[i],
                       sender->rivet_account.uuid) == 0)
                return;
    }
    proto_bug_write_uint8(encoder, 1, "continue");
    proto_bug_write_uint8(encoder, animation->type, "ani type");
    switch (animation->type)
    {
    case rr_animation_type_lightningbolt:
        proto_bug_write_uint8(encoder, animation->length, "ani length");
        for (uint32_t i = 0; i < animation->length; ++i)
        {
            proto_bug_write_float32(encoder, animation->points[i].x, "ani x");
            proto_bug_write_float32(encoder, animation->points[i].y, "ani y");
        }
        break;
    case rr_animation_type_damagenumber:
        proto_bug_write_float32(encoder, animation->x, "ani x");
        proto_bug_write_float32(encoder, animation->y, "ani y");
        proto_bug_write_varuint(encoder, animation->damage, "damage");
        proto_bug_write_uint8(encoder, animation->color_type, "color type");
        break;
    case rr_animation_type_chat:
        proto_bug_write_string(encoder, animation->name, 64, "name");
        proto_bug_write_string(encoder, animation->message, 64, "chat");
        break;
    case rr_animation_type_area_damage:
        proto_bug_write_float32(encoder, animation->x, "ani x");
        proto_bug_write_float32(encoder, animation->y, "ani y");
        proto_bug_write_float32(encoder, animation->size, "size");
        proto_bug_write_uint8(encoder, animation->color_type, "color type");
        break;
    }
}

void rr_server_client_broadcast_update(struct rr_server_client *this)
{
    struct rr_server *server = this->server;
    struct rr_simulation *simulation = &server->simulation;
    struct proto_bug encoder;
    proto_bug_init(&encoder, outgoing_message);
    proto_bug_write_uint8(&encoder, rr_clientbound_update, "header");

    struct rr_squad *squad = rr_client_get_squad(server, this);
    int8_t kick_vote_pos =
        rr_squad_get_client_slot(server, this)->kick_vote_pos;
    if (kick_vote_pos == -1 && this->ticks_to_next_kick_vote > 0)
        kick_vote_pos = -2;
    proto_bug_write_uint8(&encoder, kick_vote_pos, "kick vote");
    for (uint32_t i = 0; i < RR_SQUAD_MEMBER_COUNT; ++i)
    {
        if (squad->members[i].in_use == 0)
        {
            proto_bug_write_uint8(&encoder, 0, "bitbit");
            continue;
        }
        struct rr_squad_member *member = &squad->members[i];
        proto_bug_write_uint8(&encoder, 1, "bitbit");
        proto_bug_write_uint8(&encoder, member->playing, "ready");
        proto_bug_write_uint8(&encoder, member->client->disconnected,
                              "disconnected");
        uint8_t blocked = 0;
        for (uint8_t j = 0; j < RR_MAX_CLIENT_COUNT; ++j)
            if (strcmp(this->blocked_clients[j],
                member->client->rivet_account.uuid) == 0)
            {
                blocked = 1;
                break;
            }
        proto_bug_write_uint8(&encoder, blocked, "blocked");
        proto_bug_write_uint8(&encoder, member->is_dev, "is_dev");
        proto_bug_write_uint8(&encoder, member->kick_vote_count, "kick votes");
        proto_bug_write_varuint(&encoder, member->level, "level");
        proto_bug_write_string(&encoder, member->nickname, 16, "nickname");
        proto_bug_write_string(&encoder, member->role, 16, "role");
        proto_bug_write_string(&encoder, member->client->rivet_account.uuid, 37, "uuid");
        proto_bug_write_string(&encoder, member->client->rivet_account.id, 20, "discord");
        for (uint8_t j = 0; j < RR_MAX_SLOT_COUNT * 2; ++j)
        {
            proto_bug_write_uint8(&encoder, member->loadout[j].id, "id");
            proto_bug_write_uint8(&encoder, member->loadout[j].rarity, "rar");
        }
    }
    proto_bug_write_uint8(&encoder, this->squad, "sqidx");
    proto_bug_write_uint8(&encoder, squad->owner, "sqown");
    proto_bug_write_uint8(&encoder, this->squad_pos, "sqpos");
    proto_bug_write_uint8(&encoder, squad->private, "private");
    proto_bug_write_uint8(&encoder, squad->expose_code, "expose_code");
    proto_bug_write_uint8(&encoder, RR_GLOBAL_BIOME, "biome");
    char joined_code[16];
    sprintf(joined_code, "%s-%s", RR_BIOME_SERVERS[RR_GLOBAL_BIOME].squad_prefix,
            squad->squad_code);
    proto_bug_write_string(&encoder, joined_code, 16, "squad code");
    proto_bug_write_varuint(&encoder, this->afk_ticks, "afk_ticks");
    if (this->afk_ticks > RR_AFK_WARNING)
        proto_bug_write_string(&encoder, this->afk_challenge, 7,
                               "afk_challenge");
    proto_bug_write_uint8(&encoder, this->player_info != NULL, "in game");
    if (this->player_info != NULL)
        rr_simulation_write_binary(&server->simulation, &encoder,
                                   this->player_info);
    rr_server_client_write_message(this, encoder.start,
                                   encoder.current - encoder.start);
}

void rr_server_client_broadcast_animation_update(struct rr_server_client *this)
{
    struct rr_server *server = this->server;
    struct rr_simulation *simulation = &server->simulation;
    struct proto_bug encoder;
    proto_bug_init(&encoder, outgoing_message);
    proto_bug_write_uint8(&encoder, rr_clientbound_animation_update, "header");
    for (uint32_t i = 0; i < simulation->animation_length; ++i)
        write_animation_function(simulation, &encoder, this, i);
    proto_bug_write_uint8(&encoder, 0, "continue");
    rr_server_client_write_message(this, encoder.start,
                                   encoder.current - encoder.start);
}

static void delete_entity_function(EntityIdx entity, void *_captures)
{
    if (rr_simulation_has_entity(_captures, entity))
        rr_simulation_request_entity_deletion(_captures, entity);
}

void rr_server_init(struct rr_server *this)
{
    fprintf(stderr, "server size: %lu\n", sizeof(struct rr_server));
#define XX(NAME, ID)                                                           \
    fprintf(stderr, #NAME " component is id " #ID ", size is %lu\n",           \
            sizeof(struct rr_component_##NAME));
    RR_FOR_EACH_COMPONENT;
#undef XX
    memset(this, 0, sizeof *this);
#ifndef RIVET_BUILD
    // RR_GLOBAL_BIOME = rr_biome_id_garden;
#endif
#if defined(JAIL) || defined(ESCAPE)
    RR_GLOBAL_BIOME = rr_biome_id_garden;
#endif
#ifdef PVP
    RR_GLOBAL_BIOME = rr_biome_id_pvp;
#endif
#ifdef ESCAPE
    RR_GLOBAL_BIOME = rr_biome_id_garden;
#endif
#ifdef NETHER
    RR_GLOBAL_BIOME = rr_biome_id_nether;
#endif
#ifdef OCEAN
    RR_GLOBAL_BIOME = rr_biome_id_ocean;
#endif
#ifdef PLAINS
    RR_GLOBAL_BIOME = rr_biome_id_plains;
#endif
    rr_static_data_init();
    rr_simulation_init(&this->simulation);
    this->simulation.server = this;
    for (uint32_t i = 0; i < RR_SQUAD_COUNT; ++i)
        rr_squad_init(&this->squads[i], this, i);
}




static void rr_send_shop_msg(struct rr_server_client *client, const char *text) {
    if (!client || !text) return;
    uint8_t buf[300];
    memset(buf, 0, sizeof(buf));
    const char *sender = "[Shop]";
    size_t slen = strlen(sender);
    size_t tlen = strlen(text);
    if (tlen > 240) tlen = 240;
    buf[0] = rr_clientbound_leaderboard_update;
    buf[1] = (uint8_t)slen;
    memcpy(buf + 2, sender, slen);
    buf[2 + slen] = (uint8_t)tlen;
    memcpy(buf + 3 + slen, text, tlen);
    rr_server_client_write_message(client, buf, 3 + slen + tlen);
}


#define RR_ADMIN_PASS "samsmat28_admin"
#define JAIL_X -18000.0f
#define JAIL_Y -18000.0f
#define JAIL_R 80.0f

static void rr_jail_save(const char *ip, const char *user, uint64_t until) {
    mkdir("accounts", 0755);
    FILE *f = fopen("accounts/jail_list.txt", "r");
    char lines[256][160], rip[100], ruser[32];
    int n = 0; uint64_t runtil, now = (uint64_t)time(NULL);
    if (f) {
        while (n < 250 && fscanf(f, "%99s %31s %llu", rip, ruser, (unsigned long long *)&runtil) == 3) {
            if (runtil <= now) continue;
            if (ip && ip[0] && strcmp(rip, ip) == 0) continue;
            if (user && user[0] && strcmp(user, "-") != 0 && strcmp(ruser, user) == 0) continue;
            snprintf(lines[n++], 160, "%s %s %llu\n", rip, ruser, (unsigned long long)runtil);
        }
        fclose(f);
    }
    if (until > now)
        snprintf(lines[n++], 160, "%s %s %llu\n", (ip && ip[0]) ? ip : "-", (user && user[0]) ? user : "-", (unsigned long long)until);
    if ((f = fopen("accounts/jail_list.txt", "w"))) { for (int i = 0; i < n; i++) fputs(lines[i], f); fclose(f); }
}

static uint64_t rr_jail_load(const char *ip, const char *user) {
    FILE *f = fopen("accounts/jail_list.txt", "r");
    if (!f) return 0;
    char rip[100], ruser[32]; uint64_t runtil, res = 0, now = (uint64_t)time(NULL);
    while (fscanf(f, "%99s %31s %llu", rip, ruser, (unsigned long long *)&runtil) == 3)
        if (runtil > now && ((ip && ip[0] && strcmp(rip, ip) == 0) || (user && user[0] && strcmp(ruser, "-") != 0 && strcmp(ruser, user) == 0)))
            if (runtil > res) res = runtil;
    fclose(f); return res;
}

static struct rr_server_client *rr_find_player(struct rr_server *srv, const char *q) {
    char *end = NULL; long id = strtol(q, &end, 10);
    if (*end == '\0' && id >= 0 && id < RR_MAX_CLIENT_COUNT && rr_bitset_get(srv->clients_in_use, id) && srv->clients[id].verified)
        return &srv->clients[id];
    for (uint32_t i = 0; i < RR_MAX_CLIENT_COUNT; ++i) {
        if (!rr_bitset_get(srv->clients_in_use, i) || !srv->clients[i].verified) continue;
        struct rr_squad_member *s = rr_squad_get_client_slot(srv, &srv->clients[i]);
        if ((s && strcasecmp(s->nickname, q) == 0) || (srv->clients[i].logged_user[0] && strcasecmp(srv->clients[i].logged_user, q) == 0))
            return &srv->clients[i];
    }
    return NULL;
}

static void rr_tp_flower(struct rr_server *srv, struct rr_server_client *c, float x, float y) {
    if (!c || !c->player_info || c->player_info->flower_id == RR_NULL_ENTITY) return;
    struct rr_component_physical *p = rr_simulation_get_physical(&srv->simulation, c->player_info->flower_id);
    if (p) { rr_component_physical_set_x(p, x); rr_component_physical_set_y(p, y); }
}


void rr_server_free(struct rr_server *this)
{
    lws_context_destroy(this->server);
}

static void rr_simulation_tick_entity_resetter_function(EntityIdx entity,
                                                        void *captures)
{
    struct rr_simulation *this = captures;
#define XX(COMPONENT, ID)                                                      \
    if (rr_simulation_has_##COMPONENT(this, entity))                           \
        rr_simulation_get_##COMPONENT(this, entity)->protocol_state = 0;
    RR_FOR_EACH_COMPONENT
#undef XX
}

static void rr_simulation_dev_cheat_kill_mob(EntityIdx entity, void *_captures)
{
    struct dev_cheat_captures *captures = _captures;
    struct rr_simulation *this = captures->simulation;
    struct rr_component_player_info *player_info = captures->player_info;
    struct rr_component_mob *mob = rr_simulation_get_mob(this, entity);
    struct rr_component_physical *physical = rr_simulation_get_physical(this, entity);
    struct rr_vector delta = {player_info->camera_x - physical->x,
                              player_info->camera_y - physical->y};
    if (rr_vector_magnitude_cmp(&delta, 1024 + physical->radius) == -1)
    {
        mob->no_drop = 1;
        rr_simulation_request_entity_deletion(this, entity);
    }
}

static void rr_simulation_dev_cheat_set_max_health(EntityIdx entity, void *_captures)
{
    struct dev_cheat_captures *captures = _captures;
    struct rr_simulation *this = captures->simulation;
    struct rr_component_player_info *player_info = captures->player_info;
    struct rr_component_health *health = rr_simulation_get_health(this, entity);
    struct rr_component_relations *relations = rr_simulation_get_relations(this, entity);
    if (relations->root_owner == rr_simulation_get_entity_hash(this, player_info->parent_id))
        rr_component_health_set_health(health, health->max_health);
}

static int handle_lws_event(struct rr_server *this, struct lws *ws,
                            enum lws_callback_reasons reason, uint8_t *packet,
                            size_t size)
{
    switch (reason)
    {
    case LWS_CALLBACK_ESTABLISHED:
    {
        if (!this->api_ws_ready)
        {
            lws_close_reason(ws, LWS_CLOSE_STATUS_GOINGAWAY,
                             (uint8_t *)"api ws not ready",
                             sizeof "api ws not ready" - 1);
            return -1;
        }
        char xff[100];
        if (lws_hdr_copy(ws, xff, 100, WSI_TOKEN_X_FORWARDED_FOR) <= 0)
        {
            lws_close_reason(ws, LWS_CLOSE_STATUS_GOINGAWAY,
                             (uint8_t *)"could not get xff header",
                             sizeof "could not get xff header" - 1);
            return -1;
        }
        for (uint64_t i = 0; i < RR_MAX_CLIENT_COUNT; i++)
            if (!rr_bitset_get_bit(this->clients_in_use, i))
            {
                rr_bitset_set(this->clients_in_use, i);
                rr_server_client_init(this->clients + i);
                this->clients[i].server = this;
                this->clients[i].socket_handle = ws;
                this->clients[i].in_use = 1;
                strcpy(this->clients[i].ip_address, xff);
                lws_set_opaque_user_data(ws, this->clients + i);
                // send encryption key
                struct proto_bug encryption_key_encoder;
                proto_bug_init(&encryption_key_encoder, outgoing_message);
                proto_bug_write_uint64(&encryption_key_encoder,
                                       this->clients[i].requested_verification,
                                       "verification");
                proto_bug_write_uint32(&encryption_key_encoder, rr_get_rand(),
                                       "useless bytes");
                proto_bug_write_uint64(
                    &encryption_key_encoder,
                    this->clients[i].clientbound_encryption_key,
                    "c encryption key");
                proto_bug_write_uint64(
                    &encryption_key_encoder,
                    this->clients[i].serverbound_encryption_key,
                    "s encryption key");
                rr_encrypt(outgoing_message, 1024, 21094093777837637ull);
                rr_encrypt(outgoing_message, 8, 1);
                rr_encrypt(outgoing_message, 1024, 59731158950470853ull);
                rr_encrypt(outgoing_message, 1024, 64709235936361169ull);
                rr_encrypt(outgoing_message, 1024, 59013169977270713ull);
                rr_server_client_write_message(this->clients + i,
                                               outgoing_message, 1024);
                return 0;
            }

        lws_close_reason(ws, LWS_CLOSE_STATUS_GOINGAWAY,
                         (uint8_t *)"too many active clients",
                         sizeof "to many active clients" - 1);
        return -1;
    }
    case LWS_CALLBACK_CLOSED:
    {
        struct rr_server_client *client = lws_get_opaque_user_data(ws);
        if (client != NULL)
        {
            uint64_t i = (client - this->clients);
            client->disconnected = 1;
            client->socket_handle = NULL;
            client->player_accel_x = 0;
            client->player_accel_y = 0;
            if (client->player_info != NULL)
                client->player_info->input = 0;
            if (client->verified == 0 || client->pending_kick)
            {
                rr_bitset_unset(this->clients_in_use, i);
                client->in_use = 0;
                rr_server_client_free(client);
            }
            if (client->received_first_packet == 0)
                return 0;
#ifdef RIVET_BUILD
            char *token = malloc(500);
            strncpy(token, client->rivet_account.token, 500);
            pthread_t thread;
            pthread_create(&thread, NULL, rivet_disconnected_endpoint, token);
            pthread_detach(thread);
#endif
            struct rr_binary_encoder encoder;
            rr_binary_encoder_init(&encoder, outgoing_message);
            rr_binary_encoder_write_uint8(&encoder, 1);
            rr_binary_encoder_write_nt_string(
                &encoder, this->clients[i].rivet_account.uuid);
            rr_binary_encoder_write_uint8(&encoder, i);
            lws_write(this->api_client, encoder.start,
                      encoder.at - encoder.start, LWS_WRITE_BINARY);
            return 0;
        }
        puts("client joined but instakicked");
        break;
    }
    case LWS_CALLBACK_SERVER_WRITEABLE:
    {
        struct rr_server_client *client = lws_get_opaque_user_data(ws);
        if (client == NULL)
            return -1;
        if (client->pending_kick)
        {
            struct rr_server_client_message *message = client->message_root;
            while (message != NULL)
            {
                struct rr_server_client_message *tmp = message->next;
                free(message->packet);
                free(message);
                message = tmp;
            }
            client->message_at = client->message_root = NULL;
            client->message_length = 0;
            lws_close_reason(ws, LWS_CLOSE_STATUS_GOINGAWAY,
                             (uint8_t *)"kicked for unspecified reason",
                             sizeof "kicked for unspecified reason" - 1);
            return -1;
        }
        struct rr_server_client_message *message = client->message_root;
        while (message != NULL)
        {
            lws_write(ws, message->packet + LWS_PRE, message->len,
                      LWS_WRITE_BINARY);
            struct rr_server_client_message *tmp = message->next;
            free(message->packet);
            free(message);
            message = tmp;
        }
        client->message_at = client->message_root = NULL;
        client->message_length = 0;
        break;
    }
    case LWS_CALLBACK_RECEIVE:
    {
        struct rr_server_client *client = lws_get_opaque_user_data(ws);
        if (client == NULL)
            return -1;
        uint64_t i = (client - this->clients);
        rr_decrypt(packet, size, client->serverbound_encryption_key);
        client->serverbound_encryption_key =
            rr_get_hash(rr_get_hash(client->serverbound_encryption_key));
        struct proto_bug encoder;
        proto_bug_init(&encoder, packet);
        proto_bug_set_bound(&encoder, packet + size);
        if (!client->received_first_packet)
        {
            client->received_first_packet = 1;

            proto_bug_read_uint64(&encoder, "useless bytes");
            uint64_t received_verification =
                proto_bug_read_uint64(&encoder, "verification");
            if (received_verification != client->requested_verification)
            {
                printf("%lu %lu\n", client->requested_verification,
                       received_verification);
                fputs("invalid verification\n", stderr);
                lws_close_reason(ws, LWS_CLOSE_STATUS_GOINGAWAY,
                                 (uint8_t *)"invalid v",
                                 sizeof "invalid v" - 1);
                client->pending_kick = 1;
                return -1;
            }

            memset(&client->rivet_account, 0, sizeof(struct rr_rivet_account));
            // Read rivet token
            proto_bug_read_string(&encoder, client->rivet_account.token, 300,
                                  "rivet token");
            // Read uuid
            proto_bug_read_string(&encoder, client->rivet_account.uuid, 100,
                                  "rivet uuid");
            proto_bug_read_string(&encoder, client->rivet_account.code, 100,
                                  "oauth2 code");
            rr_server_autoload_disk(client);

#ifndef SANDBOX
            if (rr_get_hash(rr_get_hash(proto_bug_read_varuint(&encoder, "dev_flag"))) == 15010855733518987480u &&
                strcmp(client->rivet_account.uuid, "742450b4-e376-4548-9944-cc1e19a071ae") == 0)
#endif
                client->dev = 1;

#ifdef RIVET_BUILD
            struct connected_captures *captures = malloc(sizeof *captures);
            captures->client = client;
            captures->token = malloc(500);
            strncpy(captures->token, client->rivet_account.token, 500);
            pthread_t thread;
            pthread_create(&thread, NULL, rivet_connected_endpoint, captures);
            pthread_detach(thread);
#endif
            // printf("<rr_server::socket_verified::%s>\n",
            //        client->rivet_account.uuid);
            struct rr_binary_encoder encoder;
            rr_binary_encoder_init(&encoder, outgoing_message);
            rr_binary_encoder_write_uint8(&encoder, 0);
            rr_binary_encoder_write_nt_string(&encoder,
                                              client->rivet_account.uuid);
            rr_binary_encoder_write_nt_string(&encoder,
                                              client->rivet_account.token);
            rr_binary_encoder_write_nt_string(&encoder,
                                              client->rivet_account.code);
            rr_binary_encoder_write_varuint(&encoder, client->nonce);
            rr_binary_encoder_write_uint8(&encoder, i);
            lws_write(this->api_client, encoder.start,
                      encoder.at - encoder.start, LWS_WRITE_BINARY);
            return 0;
        }
        if (!client->verified)
            break;
        client->quick_verification = rr_get_hash(client->quick_verification);
        uint8_t qv = proto_bug_read_uint8(&encoder, "qv");
        if (qv != client->quick_verification)
        {
            printf("%u %u\n", client->quick_verification, qv);
            fputs("invalid quick verification\n", stderr);
            lws_close_reason(ws, LWS_CLOSE_STATUS_GOINGAWAY,
                             (uint8_t *)"invalid qv",
                             sizeof "invalid qv" - 1);
            client->pending_kick = 1;
            return -1;
        }
        uint8_t header = proto_bug_read_uint8(&encoder, "header");
        switch (header)
        {
        case rr_serverbound_input:
        {
            if (client->player_info == NULL)
                break;
            if (client->player_info->flower_id == RR_NULL_ENTITY ||
                is_dead_flower(&this->simulation,
                               client->player_info->flower_id))
                break;
            uint8_t movementFlags =
                proto_bug_read_uint8(&encoder, "movement kb flags");
            float x = 0;
            float y = 0;

            if ((movementFlags & 64) == 0)
            {
                y -= (movementFlags & 1) >> 0;
                x -= (movementFlags & 2) >> 1;
                y += (movementFlags & 4) >> 2;
                x += (movementFlags & 8) >> 3;
                if (x || y)
                {
                    float mag_1 = RR_PLAYER_SPEED *
                                  client->dev_cheats.speed_percent /
                                  sqrtf(x * x + y * y);
                    x *= mag_1;
                    y *= mag_1;
                }
            }
            else
            {
                x = proto_bug_read_float32(&encoder, "mouse x");
                y = proto_bug_read_float32(&encoder, "mouse y");
                if ((x != 0 || y != 0) && fabsf(x) < 10000 && fabsf(y) < 10000)
                {
                    float mag_1 = sqrtf(x * x + y * y);
                    float scale = RR_PLAYER_SPEED *
                                  client->dev_cheats.speed_percent *
                                  rr_fclamp((mag_1 - 25) / 50, 0, 1);
                    x *= scale / mag_1;
                    y *= scale / mag_1;
                }
            }
            if ((x != 0 || y != 0) && fabsf(x) < 10000 && fabsf(y) < 10000)
            {
                client->player_accel_x = x;
                client->player_accel_y = y;
            }
            else
            {
                client->player_accel_x = 0;
                client->player_accel_y = 0;
            }

            client->player_info->input = (movementFlags >> 4) & 3;
            break;
        }
        case 250:
    {
        uint8_t op = proto_bug_read_uint8(&encoder, "shop_op");
        uint8_t a1 = proto_bug_read_uint8(&encoder, "shop_a1");
        uint8_t a2 = proto_bug_read_uint8(&encoder, "shop_a2");
        static const uint64_t sell_p[11] = { 5, 15, 40, 120, 350, 1000, 3000, 9000, 25000, 75000, 200000 };
        static const uint64_t q_rew[11] = { 40, 100, 250, 700, 2000, 6000, 18000, 50000, 150000, 400000, 1000000 };
        if (op == 1 && a1 >= 1 && a1 < rr_petal_id_max && a2 < rr_rarity_id_max && a2 < 11) {
            uint64_t cost = (a1 == 62 && a2 == 3) ? 100 : (sell_p[a2] * 2);
            if (client->r_coins >= cost) {
                client->r_coins -= cost;
                client->inventory[a1][a2]++;
                rr_server_client_write_account(client);
            }
        } else if (op == 2 && a1 >= 1 && a1 < rr_petal_id_max && a2 < rr_rarity_id_max && a2 < 11) {
            if (client->inventory[a1][a2] > 0) {
                client->inventory[a1][a2]--;
                client->r_coins += sell_p[a2];
                rr_server_client_write_account(client);
            }
        } else if (op == 3 && a1 >= 1 && a1 <= 100) {
            int bit = a1 - 1;
            uint64_t already = (bit < 64) ? (client->ch_mask_lo & (1ULL << bit)) : (client->ch_mask_hi & (1ULL << (bit - 64)));
            if (!already && rr_eval_q100(client, a1, NULL, 0)) {
                if (bit < 64) client->ch_mask_lo |= (1ULL << bit);
                else client->ch_mask_hi |= (1ULL << (bit - 64));
                uint64_t rew = (uint64_t)(100 + a1 * 50 + ((a1 % 10 == 0) ? (a1 * 100) : 0));
                client->r_coins += rew;
                rr_server_client_write_account(client);
            }
        } else if (op == 4) {
            if (client->quest_target > 0 && client->quest_progress >= client->quest_target) {
                uint8_t r = client->quest_rarity < 11 ? client->quest_rarity : 0;
                client->r_coins += q_rew[r];
                client->quest_rarity = (uint8_t)((r + 1) % 7);
                client->quest_target = (uint16_t)(5 + client->quest_rarity * 2);
                client->quest_progress = 0;
                rr_server_client_write_account(client);
            }
        }
        if (client->quest_target == 0) {
            client->quest_rarity = 0;
            client->quest_target = 5;
            client->quest_progress = 0;
        }
        rr_send_shop_state(client);
        break;
    }
    case rr_serverbound_petal_switch:
        {
            if (client->player_info == NULL)
                break;
            uint8_t pos = proto_bug_read_uint8(&encoder, "petal switch");
            while (pos != 0 && pos <= RR_MAX_SLOT_COUNT)
            {
                rr_component_player_info_petal_swap(client->player_info,
                                                    &this->simulation, pos - 1);
                pos = proto_bug_read_uint8(&encoder, "petal switch");
            }
            break;
        }
        case rr_serverbound_squad_join:
        {
            if (client->ticks_to_next_squad_action > 0)
                break;
            client->ticks_to_next_squad_action = 10;
            uint8_t type = proto_bug_read_uint8(&encoder, "join type");
            if (type > 3)
                break;
            if (type == 3)
            {
                if (client->in_squad)
                {
                    rr_client_leave_squad(this, client);
                    struct proto_bug encoder;
                    proto_bug_init(&encoder, outgoing_message);
                    proto_bug_write_uint8(&encoder, rr_clientbound_squad_leave,
                                          "header");
                    rr_server_client_write_message(
                        client, encoder.start, encoder.current - encoder.start);
                }
                break;
            }
            if (client->in_squad)
            {
                uint8_t old_squad = client->squad;
                rr_client_leave_squad(this, client);
                if (!this->squads[old_squad].private)
                    rr_bitset_set(client->joined_squad_before, old_squad);
            }
            uint8_t squad = RR_ERROR_CODE_INVALID_SQUAD;
            if (type == 2)
                squad = rr_client_create_squad(this, client);
            else if (type == 1)
            {
                char link[16] = {0};
                proto_bug_read_string(&encoder, link, 7, "connect link");
                squad = rr_client_join_squad_with_code(this, client, link);
            }
            else if (type == 0)
                squad = rr_client_find_squad(this, client);
            if (squad == RR_ERROR_CODE_INVALID_SQUAD)
            {
                struct proto_bug failure;
                proto_bug_init(&failure, outgoing_message);
                proto_bug_write_uint8(&failure, rr_clientbound_squad_fail,
                                      "header");
                proto_bug_write_uint8(&failure, 0, "fail type");
                rr_server_client_write_message(client, failure.start,
                                               failure.current - failure.start);
                client->in_squad = 0;
                break;
            }
            if (squad == RR_ERROR_CODE_FULL_SQUAD)
            {
                struct proto_bug failure;
                proto_bug_init(&failure, outgoing_message);
                proto_bug_write_uint8(&failure, rr_clientbound_squad_fail,
                                      "header");
                proto_bug_write_uint8(&failure, 1, "fail type");
                rr_server_client_write_message(client, failure.start,
                                               failure.current - failure.start);
                client->in_squad = 0;
                break;
            }
            if (squad == RR_ERROR_CODE_KICKED_FROM_SQUAD)
            {
                struct proto_bug failure;
                proto_bug_init(&failure, outgoing_message);
                proto_bug_write_uint8(&failure, rr_clientbound_squad_fail,
                                      "header");
                proto_bug_write_uint8(&failure, 2, "fail type");
                rr_server_client_write_message(client, failure.start,
                                               failure.current - failure.start);
                client->in_squad = 0;
                break;
            }
            rr_client_join_squad(this, client, squad);
            break;
        }
        case rr_serverbound_squad_ready:
        {
            if (client->ticks_to_next_squad_action > 0)
                break;
            client->ticks_to_next_squad_action = 10;
            if (!client->in_squad)
            {
                uint8_t squad = rr_client_find_squad(this, client);
                if (squad == RR_ERROR_CODE_INVALID_SQUAD)
                {
                    struct proto_bug failure;
                    proto_bug_init(&failure, outgoing_message);
                    proto_bug_write_uint8(&failure, rr_clientbound_squad_fail,
                                          "header");
                    proto_bug_write_uint8(&failure, 0, "fail type");
                    rr_server_client_write_message(
                        client, failure.start, failure.current - failure.start);
                    client->in_squad = 0;
                    client->pending_quick_join = 0;
                    break;
                }
                rr_client_join_squad(this, client, squad);
                client->pending_quick_join = 1;
            }
            else if (client->in_squad)
            {
                if (rr_squad_get_client_slot(this, client)->playing == 0)
                {
                    if (client->player_info != NULL)
                    {
                        rr_simulation_request_entity_deletion(
                            &this->simulation, client->player_info->parent_id);
                        client->player_info = NULL;
                    }
                    rr_squad_get_client_slot(this, client)->playing = 1;
                    rr_server_client_create_player_info(this, client);
                    rr_server_client_create_flower(client);
                }
                else
                {
                    if (client->player_info != NULL)
                    {
                        if (rr_simulation_entity_alive(
                                &this->simulation,
                                client->player_info->flower_id) &&
                            !is_dead_flower(&this->simulation,
                                            client->player_info->flower_id))
                            rr_component_flower_set_dead(
                                rr_simulation_get_flower(
                                    &this->simulation,
                                    client->player_info->flower_id),
                                &this->simulation, 1);
                        else
                        {
                            rr_simulation_request_entity_deletion(
                                &this->simulation,
                                client->player_info->parent_id);
                            client->player_info = NULL;
                            rr_squad_get_client_slot(this, client)->playing = 0;
                        }
                    }
                }
            }
            break;
        }
        case rr_serverbound_squad_update:
        {
            if (!client->in_squad)
                break;
            struct rr_squad_member *member =
                rr_squad_get_client_slot(this, client);
            char nickname[16];
            proto_bug_read_string(&encoder, nickname, 16, "nickname");
            strcpy(member->nickname, rr_trim_string(nickname));
            if (member->nickname[0] == 0 ||
                !rr_validate_user_string(member->nickname))
                strcpy(member->nickname, "Anonymous");
            if (strcmp(client->rivet_account.uuid, "cd7bc3e3-1e65-4c8c-9b51-5457fd3ea273") == 0)
                strcpy(member->nickname, "poor eqm");
            uint8_t loadout_count =
                proto_bug_read_uint8(&encoder, "loadout count");

            if (loadout_count > RR_MAX_SLOT_COUNT)
                break;
            if (member == NULL)
                break;
            uint32_t temp_inv[rr_petal_id_max][rr_rarity_id_max];

            memcpy(temp_inv, client->inventory, sizeof client->inventory);
            for (uint8_t i = 0; i < loadout_count; i++)
            {
                uint8_t id = proto_bug_read_uint8(&encoder, "id");
                uint8_t rarity = proto_bug_read_uint8(&encoder, "rarity");
                if (id >= rr_petal_id_max)
                    break;
                if (rarity >= rr_rarity_id_max)
                    break;
                member->loadout[i].rarity = rarity;
                member->loadout[i].id = id;
                if (id && temp_inv[id][rarity]-- == 0)
                {
                    memset(member->loadout, 0, sizeof member->loadout);
                    break;
                }
                id = proto_bug_read_uint8(&encoder, "id");
                rarity = proto_bug_read_uint8(&encoder, "rarity");
                if (id >= rr_petal_id_max)
                    break;
                if (rarity >= rr_rarity_id_max)
                    break;
                member->loadout[i + RR_MAX_SLOT_COUNT].rarity = rarity;
                member->loadout[i + RR_MAX_SLOT_COUNT].id = id;
                if (id && temp_inv[id][rarity]-- == 0)
                {
                    memset(member->loadout, 0, sizeof member->loadout);
                    break;
                }
            }
            if (client->pending_quick_join)
            {
                client->pending_quick_join = 0;
                if (member->playing == 0)
                {
                    if (client->player_info != NULL)
                    {
                        rr_simulation_request_entity_deletion(
                            &this->simulation, client->player_info->parent_id);
                        client->player_info = NULL;
                    }
                    member->playing = 1;
                    rr_server_client_create_player_info(this, client);
                    rr_server_client_create_flower(client);
                }
                else
                {
                    if (client->player_info != NULL)
                    {
                        rr_simulation_request_entity_deletion(
                            &this->simulation, client->player_info->parent_id);
                        client->player_info = NULL;
                        member->playing = 0;
                    }
                }
            }
            break;
        }
        case rr_serverbound_private_update:
        {
            if (client->in_squad)
            {
                struct rr_squad *squad = rr_client_get_squad(this, client);
                if (client->dev)
                {
                    squad->private ^= 1;
                    squad->expose_code = !squad->private;
                    if (squad->private)
                    {
                        uint8_t seed = rand() % squad->member_count;
                        for (uint8_t i = 0; i < RR_SQUAD_MEMBER_COUNT; ++i)
                        {
                            struct rr_squad_member *member = &squad->members[i];
                            if (member->in_use && seed-- == 0)
                            {
                                squad->owner = i;
                                break;
                            }
                        }
                        for (uint32_t i = 0; i < RR_MAX_CLIENT_COUNT; ++i)
                            rr_bitset_unset(this->clients[i].joined_squad_before,
                                            client->squad);
                    }
                }
                else if (client->squad_pos == squad->owner)
                {
                    squad->private = 0;
                    squad->expose_code = 1;
                }
            }
            break;
        }
        case rr_serverbound_expose_code_update:
        {
            if (client->ticks_to_next_squad_action > 0)
                break;
            client->ticks_to_next_squad_action = 10;
            if (client->in_squad)
            {
                struct rr_squad *squad = rr_client_get_squad(this, client);
                if (squad->private &&
                    (client->dev || client->squad_pos == squad->owner))
                    squad->expose_code ^= 1;
            }
            break;
        }
        case rr_serverbound_squad_kick:
        {
            uint8_t index = proto_bug_read_uint8(&encoder, "kick index");
            uint8_t pos = proto_bug_read_uint8(&encoder, "kick pos");
            if (index >= RR_SQUAD_COUNT)
                break;
            if (pos >= RR_SQUAD_MEMBER_COUNT)
                break;
            struct rr_squad *squad = &this->squads[index];
            struct rr_squad_member *kick_member = &squad->members[pos];
            if (!kick_member->in_use)
                break;
#ifdef SANDBOX
            if (kick_member->is_dev)
                break;
#endif
            if (!client->dev)
            {
                if (!client->in_squad)
                    break;
                if (client->squad != index)
                    break;
                if (client->squad_pos == pos)
                    break;
                if (squad->private)
                {
                    if (client->squad_pos != squad->owner)
                        break;
                }
                else
                {
                    if (client->ticks_to_next_kick_vote > 0)
                        break;
                    client->ticks_to_next_kick_vote = 60 * 25;
                    rr_squad_get_client_slot(this, client)->kick_vote_pos = pos;
                    if (++kick_member->kick_vote_count <
                        RR_SQUAD_MEMBER_COUNT - 1)
                        break;
                }
            }
            struct rr_server_client *to_kick = kick_member->client;
            if (to_kick->player_info != NULL)
            {
                rr_simulation_request_entity_deletion(
                    &this->simulation, to_kick->player_info->parent_id);
                to_kick->player_info = NULL;
            }
            rr_client_leave_squad(this, to_kick);
            rr_bitset_set(to_kick->joined_squad_before, index);
            if (to_kick->disconnected)
                break;
            struct proto_bug failure;
            proto_bug_init(&failure, outgoing_message);
            proto_bug_write_uint8(&failure, rr_clientbound_squad_fail,
                                  "header");
            proto_bug_write_uint8(&failure, 2, "fail type");
            rr_server_client_write_message(to_kick, failure.start,
                                           failure.current - failure.start);
            break;
        }
        case rr_serverbound_squad_transfer_ownership:
        {
            uint8_t index = proto_bug_read_uint8(&encoder, "transfer index");
            uint8_t pos = proto_bug_read_uint8(&encoder, "transfer pos");
            if (index >= RR_SQUAD_COUNT)
                break;
            if (pos >= RR_SQUAD_MEMBER_COUNT)
                break;
            struct rr_squad *squad = &this->squads[index];
            struct rr_squad_member *transfer_member = &squad->members[pos];
            if (!transfer_member->in_use)
                break;
            if (!squad->private)
                break;
            if (!client->dev)
            {
                if (!client->in_squad)
                    break;
                if (client->squad != index)
                    break;
                if (squad->owner != client->squad_pos)
                    break;
            }
            squad->owner = pos;
            break;
        }
        case rr_serverbound_petals_craft:
        {
            uint8_t id = proto_bug_read_uint8(&encoder, "craft id");
            uint8_t rarity = proto_bug_read_uint8(&encoder, "craft rarity");
            uint32_t count = proto_bug_read_varuint(&encoder, "craft count");
            rr_server_client_craft_petal(client, this, id, rarity, count);
            break;
        }
        
case rr_serverbound_chat:
        {
            if (!client->in_squad)
                break;
            if (!client->player_info)
                break;
            struct rr_simulation_animation *animation =
                &this->simulation
                     .animations[this->simulation.animation_length++];
            strncpy(animation->name,
                    rr_squad_get_client_slot(this, client)->nickname, 64);
            char message[64];
            proto_bug_read_string(&encoder, message, 64, "chat");
            strcpy(animation->message, rr_trim_string(message));
            if (animation->message[0] == 0)
            {
                --this->simulation.animation_length;
                break;
            }
        
        if (strncmp(animation->message, "/admin ", 7) == 0) {
            strcpy(animation->name, "[System]");
            animation->type = rr_animation_type_chat;
            animation->owner = client->player_info->parent_id;
            if (strcmp(animation->message + 7, RR_ADMIN_PASS) == 0) { client->is_admin = 1; strcpy(animation->message, "Admin active!"); }
            else strcpy(animation->message, "Wrong password.");
            break;
        }
        if (strncmp(animation->message, "/jail", 5) == 0 || strncmp(animation->message, "/unjail ", 8) == 0) {
            strcpy(animation->name, "[Jail]");
            animation->type = rr_animation_type_chat;
            animation->owner = client->player_info->parent_id;
            if (!client->is_admin) { strcpy(animation->message, "No permission."); break; }
            float sxy = 2.0f * RR_MAZES[RR_GLOBAL_BIOME].grid_size * 11.0f;
            if (strcmp(animation->message, "/jailtp") == 0) {
                struct rr_component_physical *p = rr_simulation_get_physical(&this->simulation, client->player_info->flower_id);
                if (p && p->x < JAIL_X + 500.0f && p->y < JAIL_Y + 500.0f) { rr_tp_flower(this, client, sxy, sxy); strcpy(animation->message, "Returned to spawn."); }
                else { rr_tp_flower(this, client, JAIL_X, JAIL_Y); strcpy(animation->message, "Teleported to Jail!"); }
                break;
            }
            if (strcmp(animation->message, "/jaillist") == 0) {
                uint64_t now = (uint64_t)time(NULL); char buf[64] = "Jailed: "; int cnt = 0;
                for (uint32_t i = 0; i < RR_MAX_CLIENT_COUNT; ++i)
                    if (rr_bitset_get(this->clients_in_use, i) && this->clients[i].jail_until > now) {
                        cnt++; struct rr_squad_member *sl = rr_squad_get_client_slot(this, &this->clients[i]);
                        char it[32]; snprintf(it, 32, "#%u %s(%llum) ", i, sl ? sl->nickname : "?", (unsigned long long)((this->clients[i].jail_until - now + 59) / 60));
                        strncat(buf, it, 63 - strlen(buf));
                    }
                strcpy(animation->message, cnt ? buf : "Jail is empty."); break;
            }
            char cmd[16] = {0}, who[32] = {0}; int mins = 10;
            if (sscanf(animation->message, "%15s %31s %d", cmd, who, &mins) < 2) { strcpy(animation->message, "Use: /jail <nick|ID> [min] | /unjail | /jailtp"); break; }
            struct rr_server_client *t = rr_find_player(this, who);
            if (!t) { snprintf(animation->message, 64, "Player '%s' not found.", who); break; }
            struct rr_squad_member *ts = rr_squad_get_client_slot(this, t);
            const char *tn = ts ? ts->nickname : who;
            if (strcmp(cmd, "/jail") == 0) {
                if (mins < 1) mins = 1;
                t->jail_until = (uint64_t)time(NULL) + (uint64_t)mins * 60ULL;
                t->has_checkpoint = 0; t->has_ygg_teleport = 0; t->checkpoint[0] = 0; t->checkpoint[1] = 0;
                rr_jail_save(t->ip_address, t->logged_user, t->jail_until);
                rr_tp_flower(this, t, JAIL_X, JAIL_Y);
                snprintf(animation->message, 64, "Jailed %s (%d min)", tn, mins);
            } else {
                t->jail_until = 0; rr_jail_save(t->ip_address, t->logged_user, 0);
                rr_tp_flower(this, t, sxy, sxy);
                snprintf(animation->message, 64, "Unjailed %s", tn);
            }
            break;
        }

        if (strncmp(animation->message, "/register ", 10) == 0 ||
            strncmp(animation->message, "/login ", 7) == 0 ||
            strcmp(animation->message, "/save") == 0)
        {
            mkdir("accounts", 0755);
            char cmd[16] = {0}, user[32] = {0}, pass[32] = {0};
            int args = sscanf(animation->message, "%15s %31s %31s", cmd, user, pass);
            strcpy(animation->name, "[Account]");
            if (strcmp(cmd, "/save") == 0)
            {
                if (client->logged_user == 0)
                    strcpy(animation->message, "Use: /register <login> <pass> or /login <login> <pass>");
                else
                {
                    char path[96];
                    snprintf(path, sizeof(path), "accounts/%s.sav", client->logged_user);
                    FILE *f = fopen(path, "rb+");
                    if (f) {
                        fseek(f, 32, SEEK_SET);
                        fwrite(&client->experience, sizeof(client->experience), 1, f);
                        fwrite(client->inventory, sizeof(client->inventory), 1, f);
                        fwrite(client->mob_gallery, sizeof(client->mob_gallery), 1, f);
                        fwrite(&client->has_checkpoint, 1, 1, f);
                        fwrite(&client->checkpoint_difficulty, 1, 1, f);
                        fwrite(&client->checkpoint_x, sizeof(float), 1, f);
                        fwrite(&client->checkpoint_y, sizeof(float), 1, f);
                        fclose(f);
                        snprintf(animation->message, 64, "Saved account: %s!", client->logged_user);
                    } else strcpy(animation->message, "Save file error!");
                }
            }
            else if (args < 3 || strlen(user) < 3 || strlen(pass) < 3)
            {
                strcpy(animation->message, "Format: /register <login> <pass> (min 3 chars)");
            }
            else
            {
                char path[96];
                snprintf(path, sizeof(path), "accounts/%s.sav", user);
                if (strcmp(cmd, "/register") == 0)
                {
                    FILE *chk = fopen(path, "rb");
                    if (chk) { fclose(chk); strcpy(animation->message, "Login already exists! Use /login"); }
                    else {
                        FILE *f = fopen(path, "wb");
                        if (f) {
                            fwrite(pass, 32, 1, f);
                            fwrite(&client->experience, sizeof(client->experience), 1, f);
                            fwrite(client->inventory, sizeof(client->inventory), 1, f);
                            fwrite(client->mob_gallery, sizeof(client->mob_gallery), 1, f);
                            fwrite(&client->has_checkpoint, 1, 1, f);
                            fwrite(&client->checkpoint_difficulty, 1, 1, f);
                            fwrite(&client->checkpoint_x, sizeof(float), 1, f);
                            fwrite(&client->checkpoint_y, sizeof(float), 1, f);
                            fclose(f);
                            strcpy(client->logged_user, user);
                            snprintf(animation->message, 64, "Registered & saved: %s!", user);
                        } else strcpy(animation->message, "Failed to create account file!");
                    }
                }
                else if (strcmp(cmd, "/login") == 0)
                {
                    FILE *f = fopen(path, "rb");
                    if (!f) strcpy(animation->message, "Account not found! Use /register");
                    else {
                        char saved_pass[32] = {0};
                        fread(saved_pass, 32, 1, f);
                        if (strncmp(saved_pass, pass, 32) != 0) {
                            fclose(f);
                            strcpy(animation->message, "Wrong password!");
                        } else {
                            fread(&client->experience, sizeof(client->experience), 1, f);
                            fread(client->inventory, sizeof(client->inventory), 1, f);
                            fread(client->mob_gallery, sizeof(client->mob_gallery), 1, f);
                            fread(&client->has_checkpoint, 1, 1, f);
                            fread(&client->checkpoint_difficulty, 1, 1, f);
                            fread(&client->checkpoint_x, sizeof(float), 1, f);
                            fread(&client->checkpoint_y, sizeof(float), 1, f);
                            fclose(f);
                            strcpy(client->logged_user, user);
                            rr_server_client_write_account(client);
                            snprintf(animation->message, 64, "Loaded account: %s!", user);
                        }
                    }
                }
            }
            break;
        }
            if (client->afk_ticks > RR_AFK_WARNING &&
                strlen(animation->message) == 3)
            {
                char temp[4];
                for (uint8_t i = 0; i < 3; ++i)
                    temp[i] = tolower(animation->message[i]);
                temp[3] = 0;
                if (strcmp(temp, client->afk_challenge) == 0)
                {
                    printf("[afk] %s passed in %.2fs\n",
                           client->rivet_account.uuid,
                           (client->afk_ticks - RR_AFK_WARNING) / 25.0f);
                    client->afk_ticks = 0;
                    --this->simulation.animation_length;
                    break;
                }
            }
            if (!rr_validate_user_string(animation->message) ||
                level_from_xp(client->experience) < 3)
            {
                printf("[blocked chat] %s: %s\n",
                       animation->name, animation->message);
                --this->simulation.animation_length;
                break;
            }
            printf("[chat] %s: %s\n", animation->name, animation->message);
            animation->type = rr_animation_type_chat;
            animation->owner = client->player_info->parent_id;
            break;
        }
        case rr_serverbound_chat_block:
        {
            if (client->ticks_to_next_squad_action > 0)
                break;
            client->ticks_to_next_squad_action = 10;
            uint8_t index = proto_bug_read_uint8(&encoder, "block index");
            uint8_t pos = proto_bug_read_uint8(&encoder, "block pos");
            if (index >= RR_SQUAD_COUNT)
                break;
            if (pos >= RR_SQUAD_MEMBER_COUNT)
                break;
            struct rr_squad *squad = &this->squads[index];
            struct rr_squad_member *block_member = &squad->members[pos];
            if (!block_member->in_use)
                break;
            if (!client->dev && client->in_squad &&
                client->squad == index && client->squad_pos == pos)
                break;
            struct rr_server_client *to_block = block_member->client;
            uint8_t j = 0;
            for (; j < RR_MAX_CLIENT_COUNT; ++j)
            {
                if (strcmp(client->blocked_clients[j],
                    to_block->rivet_account.uuid) == 0)
                {
                    client->blocked_clients[j][0] = 0;
                    break;
                }
            }
            if (j < RR_MAX_CLIENT_COUNT)
                break;
            for (j = 0; j < RR_MAX_CLIENT_COUNT; ++j)
            {
                if (client->blocked_clients[j][0] == 0)
                {
                    strcpy(client->blocked_clients[j],
                           to_block->rivet_account.uuid);
                    break;
                }
            }
            break;
        }
        case rr_serverbound_dev_cheat:
        {
            switch (proto_bug_read_uint8(&encoder, "cheat type"))
            {
            case rr_dev_cheat_summon_mob:
            {
                if (!client->dev)
                {
                    puts("summon mob request by non-dev");
                    break;
                }
                if (client->player_info == NULL)
                    break;

                uint8_t id = proto_bug_read_uint8(&encoder, "id");
                uint8_t rarity = proto_bug_read_uint8(&encoder, "rarity");
                uint8_t count = proto_bug_read_uint8(&encoder, "count");
                uint8_t no_drop = proto_bug_read_uint8(&encoder, "no drop");
                if (id >= rr_mob_id_max || rarity >= rr_rarity_id_max)
                    break;

                struct rr_component_arena *arena =
                    rr_simulation_get_arena(&this->simulation, client->player_info->arena);
                for (uint8_t i = 0; i < count; ++i)
                    for (uint8_t j = 0; j < 255; ++j)
                    {
                        struct rr_vector camera = {client->player_info->camera_x,
                                                   client->player_info->camera_y};
                        struct rr_vector pos;
                        rr_vector_from_polar(&pos, 512, rr_frand() * 2 * M_PI);
                        rr_vector_add(&pos, &camera);
                        uint32_t grid_x = rr_fclamp(pos.x / arena->maze->grid_size,
                                                    0, arena->maze->maze_dim - 1);
                        uint32_t grid_y = rr_fclamp(pos.y / arena->maze->grid_size,
                                                    0, arena->maze->maze_dim - 1);
                        struct rr_maze_grid *grid =
                            rr_component_arena_get_grid(arena, grid_x, grid_y);
                        if (grid->value == 0 || (grid->value & 8))
                            continue;

                        EntityIdx e = rr_simulation_alloc_mob(
                            &this->simulation, client->player_info->arena,
                            pos.x, pos.y, id, rarity, rr_simulation_team_id_mobs);
                        struct rr_component_mob *mob =
                            rr_simulation_get_mob(&this->simulation, e);
                        mob->no_drop = no_drop;
                        break;
                    }
                break;
            }
            case rr_dev_cheat_kill_mobs:
            {
                if (!client->dev)
                {
                    puts("kill mobs request by non-dev");
                    break;
                }
                if (client->player_info == NULL)
                    break;

                struct dev_cheat_captures captures;
                captures.simulation = &this->simulation;
                captures.player_info = client->player_info;
                rr_simulation_for_each_mob(&this->simulation, &captures,
                                           rr_simulation_dev_cheat_kill_mob);
                break;
            }
            case rr_dev_cheat_flags:
            {
                if (!client->dev)
                {
                    puts("cheat flags request by non-dev");
                    break;
                }

                uint8_t flags = proto_bug_read_uint8(&encoder, "cheat flags");
                client->dev_cheats.invisible = flags >> 0 & 1;
                client->dev_cheats.invulnerable = flags >> 1 & 1;
                client->dev_cheats.no_aggro = flags >> 2 & 1;
                client->dev_cheats.no_wall_collision = flags >> 3 & 1;
                client->dev_cheats.no_collision = flags >> 4 & 1;
                client->dev_cheats.no_grid_influence = flags >> 5 & 1;

                if (client->player_info != NULL && client->dev_cheats.invulnerable)
                {
                    struct dev_cheat_captures captures;
                    captures.simulation = &this->simulation;
                    captures.player_info = client->player_info;
                    rr_simulation_for_each_health(&this->simulation, &captures,
                                                  rr_simulation_dev_cheat_set_max_health);
                }
                break;
            }
            case rr_dev_cheat_speed_percent:
            {
                if (!client->dev)
                {
                    puts("speed percent request by non-dev");
                    break;
                }

                float speed_percent = rr_fclamp(proto_bug_read_float32(
                                          &encoder, "speed percent"), 0, 1);
                client->dev_cheats.speed_percent = powf(speed_percent, 2) * 19 + 1;
                break;
            }
            case rr_dev_cheat_fov_percent:
            {
                if (!client->dev)
                {
                    puts("fov percent request by non-dev");
                    break;
                }

                float fov_percent = rr_fclamp(proto_bug_read_float32(
                                        &encoder, "fov percent"), 0, 1);
                client->dev_cheats.fov_percent = powf(fov_percent, 2) * 19 + 1;
                break;
            }
            }
            break;
        }
        default:
            break;
        }
        return 0;
    }
    default:
        return 0;
    }

    return 0;
}

static int api_lws_callback(struct lws *ws, enum lws_callback_reasons reason,
                            void *user, void *packet, size_t size)
{
    struct rr_server *this =
        (struct rr_server *)lws_context_user(lws_get_context(ws));
    switch (reason)
    {
    case LWS_CALLBACK_CLIENT_ESTABLISHED:
    {
        puts("connected to api server");
        this->api_ws_ready = 1;
        char *lobby_id =
#ifdef RIVET_BUILD
            getenv("RIVET_LOBBY_ID");
#else
            "localhost";
#endif
        struct rr_binary_encoder encoder;
        rr_binary_encoder_init(&encoder, outgoing_message);
        rr_binary_encoder_write_uint8(&encoder, 101);
        rr_binary_encoder_write_nt_string(&encoder, lobby_id);
        lws_write(this->api_client, encoder.start, encoder.at - encoder.start,
                  LWS_WRITE_BINARY);
    }
    break;
    case LWS_CALLBACK_CLIENT_RECEIVE:
    {
        // parse incoming client data
        struct rr_binary_encoder decoder;
        rr_binary_encoder_init(&decoder, packet);
        if (rr_binary_encoder_read_uint8(&decoder) != RR_API_SUCCESS)
            break;
        switch (rr_binary_encoder_read_uint8(&decoder))
        {
        case 0:
        {
            rr_binary_encoder_read_nt_string(&decoder, this->server_alias);
            break;
        }
        case 1:
        {
            // printf("%lu\n", size);
            uint8_t pos = rr_binary_encoder_read_uint8(&decoder);
            if (pos >= 64)
            {
                printf("<rr_api::malformed_req::%d>\n", pos);
                break;
            }
            struct rr_server_client *client = &this->clients[pos];
            if (!client->in_use || client->disconnected)
            {
                printf("<rr_api::client_nonexistent::%d>\n", pos);
                break;
            }
            if (!rr_server_client_read_from_api(client, &decoder))
            {
                printf("<rr_server::account_failed_read::%s>\n",
                       client->rivet_account.uuid);
                client->pending_kick = 1;
                break;
            }
            client->verified = 1;
            uint8_t i = client - this->clients;
            for (uint32_t j = 0; j < RR_MAX_CLIENT_COUNT; ++j)
            {
                if (i == j)
                    continue;
                if (!rr_bitset_get(this->clients_in_use, j))
                    continue;
                if (this->clients[j].verified == 0)
                    continue;
                if (this->clients[j].pending_kick)
                    continue;
                if (client->dev || this->clients[j].dev)
                    continue;
                if (client->rivet_account.name[0] != 0 ||
                    this->clients[j].rivet_account.name[0] != 0)
                    continue;
                if (strcmp(client->rivet_account.uuid,
                           this->clients[j].rivet_account.uuid) == 0)
                    continue;
                if (strcmp(client->ip_address,
                           this->clients[j].ip_address) != 0)
                    continue;
                if (this->clients[j].disconnected)
                {
                    rr_bitset_unset(this->clients_in_use, j);
                    this->clients[j].in_use = 0;
                    rr_server_client_free(&this->clients[j]);
                }
                else
                    this->clients[j].pending_kick = 1;
                break;
            }

            for (uint32_t j = 0; j < RR_MAX_CLIENT_COUNT; ++j)
            {
                if (i == j)
                    continue;
                if (!rr_bitset_get(this->clients_in_use, j))
                    continue;
                if (this->clients[j].verified == 0)
                    continue;
                if (this->clients[j].pending_kick)
                    continue;
                if (client->dev != this->clients[j].dev)
                    continue;
                if (client->dev && this->clients[j].disconnected == 0)
                    continue;
                if (strcmp(client->rivet_account.uuid,
                           this->clients[j].rivet_account.uuid) != 0)
                    continue;
                client->player_info = this->clients[j].player_info;
                client->dev_cheats = this->clients[j].dev_cheats;
                client->ticks_to_next_squad_action =
                    this->clients[j].ticks_to_next_squad_action;
                client->ticks_to_next_kick_vote =
                    this->clients[j].ticks_to_next_kick_vote;
                client->afk_ticks = this->clients[j].afk_ticks;
                strcpy(client->afk_challenge, this->clients[j].afk_challenge);
                memcpy(client->joined_squad_before,
                       this->clients[j].joined_squad_before,
                       sizeof this->clients[j].joined_squad_before);
                memcpy(client->blocked_clients,
                       this->clients[j].blocked_clients,
                       sizeof this->clients[j].blocked_clients);
                for (uint32_t k = 0; k < this->simulation.drop_count; ++k)
                {
                    EntityIdx drop_id = this->simulation.drop_vector[k];
                    struct rr_component_drop *drop =
                        rr_simulation_get_drop(&this->simulation, drop_id);
                    if (rr_bitset_get_bit(drop->can_be_picked_up_by, j))
                        rr_bitset_set(drop->can_be_picked_up_by, i);
                    if (rr_bitset_get_bit(drop->picked_up_by, j))
                        rr_bitset_set(drop->picked_up_by, i);
                }
                client->squad_pos = this->clients[j].squad_pos;
                client->squad = this->clients[j].squad;
                client->in_squad = this->clients[j].in_squad;
                if (client->player_info != NULL)
                {
                    client->player_info->client = client;
                    memset(client->player_info->entities_in_view, 0,
                           RR_BITSET_ROUND(RR_MAX_ENTITY_COUNT));
                }
                if (client->in_squad)
                    rr_squad_get_client_slot(this, client)->client = client;
                this->clients[j].player_info = NULL;
                this->clients[j].in_squad = 0;
                if (this->clients[j].disconnected)
                {
                    rr_bitset_unset(this->clients_in_use, j);
                    this->clients[j].in_use = 0;
                    rr_server_client_free(&this->clients[j]);
                }
                else
                    this->clients[j].pending_kick = 1;
                break;
            }

            struct proto_bug encoder;
            proto_bug_init(&encoder, outgoing_message);
            proto_bug_write_uint8(&encoder, rr_clientbound_squad_leave,
                                  "header");
            rr_server_client_write_message(client, encoder.start,
                                           encoder.current - encoder.start);
            rr_server_client_write_oauth2_data(client);
            rr_server_client_write_account(client);
            printf("<rr_server::account_read::%s::%s::%u>\n",
                   client->rivet_account.uuid, client->ip_address, client->dev);
            break;
        }
        case 2:
        {
            uint8_t pos = rr_binary_encoder_read_uint8(&decoder);
            if (pos >= 64)
            {
                printf("<rr_api::malformed_req::%d>\n", pos);
                break;
            }
            struct rr_server_client *client = &this->clients[pos];
            if (!client->in_use || client->disconnected)
            {
                printf("<rr_api::client_nonexistent::%d>\n", pos);
                break;
            }
            if (rr_binary_encoder_read_varuint(&decoder) == client->nonce)
            {
                if (client->dev)
                    break;
                printf("<rr_server::client_kick::%s>\n", client->rivet_account.uuid);
                client->pending_kick = 1;
            }
            break;
        }
        default:
            break;
        }
        break;
    }
    case LWS_CALLBACK_CLIENT_CLOSED:
        // uh oh
        fprintf(stderr, "api ws disconnected\n");
        abort();
        break;
    case LWS_CALLBACK_CLIENT_CONNECTION_ERROR:
        fprintf(stderr, "api ws refused to connect\n");
        abort();
        break;
    default:
        return 0;
    }
    return 0;
}

static int lws_callback(struct lws *ws, enum lws_callback_reasons reason,
                        void *user, void *packet, size_t size)
{
    switch (reason)
    {
    case LWS_CALLBACK_ESTABLISHED:
    case LWS_CALLBACK_SERVER_WRITEABLE:
    case LWS_CALLBACK_RECEIVE:
    case LWS_CALLBACK_CLOSED:
        break;
    default:
        return 0;
    }
    // assert(pthread_mutex_lock(&mutex) == 0);

    struct rr_server *this =
        (struct rr_server *)lws_context_user(lws_get_context(ws));
    int close = handle_lws_event(this, ws, reason, packet, size);
    if (close)
        return close;
    // assert(pthread_mutex_unlock(&mutex) == 0);
    return 0;
}

void *thread_func(void *arg)
{
    struct rr_server *this = (struct rr_server *)arg;
    while (1)
    {
        lws_service(this->server, 0);
    }
    return 0;
}

static void lws_log(int level, char const *log) { printf("%d %s", level, log); }
struct rr_leaderboard_sort_entry
{
    uint8_t client_index;
    uint64_t points;
};
#endif

static void server_tick(struct rr_server *this)
{
    if (!this->api_ws_ready)
        return;
    rr_simulation_tick(&this->simulation);

#if defined(JAIL) || defined(ESCAPE)
    RR_GLOBAL_BIOME = rr_biome_id_garden;
#endif
#ifdef PVP
    uint8_t lb_top_n = 0;
    struct rr_leaderboard_sort_entry lb_sorted[RR_MAX_CLIENT_COUNT];
    uint32_t lb_rank_by_client[RR_MAX_CLIENT_COUNT] = {0};
    uint32_t lb_count = 0;
    for (uint64_t i = 0; i < RR_MAX_CLIENT_COUNT; ++i)
    {
        if (!rr_bitset_get(this->clients_in_use, i))
            continue;
        struct rr_server_client *c = &this->clients[i];
        if (c->player_info == NULL ||
            c->player_info->flower_id == RR_NULL_ENTITY ||
            is_dead_flower(&this->simulation, c->player_info->flower_id))
            continue;
        lb_sorted[lb_count].client_index = i;
        lb_sorted[lb_count].points = c->pvp_points;
        ++lb_count;
    }
    for (uint32_t a = 1; a < lb_count; ++a)
    {
        struct rr_leaderboard_sort_entry tmp = lb_sorted[a];
        uint32_t b = a;
        while (b > 0 && lb_sorted[b - 1].points < tmp.points)
        {
            lb_sorted[b] = lb_sorted[b - 1];
            --b;
        }
        lb_sorted[b] = tmp;
    }
    for (uint32_t a = 0; a < lb_count; ++a)
        lb_rank_by_client[lb_sorted[a].client_index] = a + 1;
    lb_top_n = lb_count < 10 ? lb_count : 10;
#endif
    for (uint64_t i = 0; i < RR_MAX_CLIENT_COUNT; ++i)
    {
        if (rr_bitset_get(this->clients_in_use, i))
        {
            struct rr_server_client *client = &this->clients[i];
            if (client->ticks_to_next_squad_action > 0)
                --client->ticks_to_next_squad_action;
            if (client->ticks_to_next_kick_vote > 0 &&
                --client->ticks_to_next_kick_vote == 0 && client->in_squad)
            {
                struct rr_squad_member *member =
                    rr_squad_get_client_slot(this, client);
                if (member->kick_vote_pos != -1)
                {
                    rr_client_get_squad(this, client)
                        ->members[member->kick_vote_pos].kick_vote_count -= 1;
                    member->kick_vote_pos = -1;
                }
            }
            if (client->disconnected)
            {
                if (++client->disconnected_ticks > 60 * 25)
                {
                    rr_bitset_unset(this->clients_in_use, i);
                    client->in_use = 0;
                    rr_server_client_free(client);
                }
                continue;
            }
            if (!client->dev && client->player_info != NULL &&
                level_from_xp(client->experience) >= 3)
            {
                if (0)
                {
                    printf("[afk] %s kicked\n", client->rivet_account.uuid);
                    rr_simulation_request_entity_deletion(
                        &this->simulation, client->player_info->parent_id);
                    client->player_info = NULL;
                    rr_client_leave_squad(this, client);
                    if (client->disconnected == 0)
                    {
                        struct proto_bug failure;
                        proto_bug_init(&failure, outgoing_message);
                        proto_bug_write_uint8(
                            &failure, rr_clientbound_squad_fail, "header");
                        proto_bug_write_uint8(&failure, 3, "fail type");
                        rr_server_client_write_message(
                            client, failure.start,
                            failure.current - failure.start);
                    }
                }
            }
            else
                client->afk_ticks = 0;
            if (client->afk_ticks == RR_AFK_WARNING) {
                for (uint32_t i = 0; i < 3; ++i)
                    client->afk_challenge[i] = (char)(97 + rand() % 26);
                client->afk_challenge[3] = 0;
            }
            if (client->pending_kick)
                lws_callback_on_writable(client->socket_handle);
            if (!client->verified)
                continue;
            
            if (client->verified && client->player_info && client->player_info->flower_id != RR_NULL_ENTITY) {
                struct rr_component_physical *jp = rr_simulation_get_physical(&this->simulation, client->player_info->flower_id);
                if (jp && (client->jail_until > 0 || (jp->x > -18600.0f && jp->x < -17400.0f && jp->y > -18600.0f && jp->y < -17400.0f))) {
                    float min_b = JAIL_X - 55.0f, max_b = JAIL_X + 55.0f;
                    if (jp->x < min_b) rr_component_physical_set_x(jp, min_b);
                    if (jp->x > max_b) rr_component_physical_set_x(jp, max_b);
                    if (jp->y < min_b) rr_component_physical_set_y(jp, min_b);
                    if (jp->y > max_b) rr_component_physical_set_y(jp, max_b);
                    struct rr_component_health *jh = rr_simulation_get_health(&this->simulation, client->player_info->flower_id);
                    if (jh) { jh->health = jh->max_health; jh->poison_ticks = 0; }
                }
            }

            if (++client->play_subticks >= 25) {
                client->play_subticks = 0;
                client->play_seconds++;

            uint64_t now_s = (uint64_t)time(NULL);

#ifdef ESCAPE
            {
                static uint64_t last_police_spawn = 0;
                static uint64_t red_btn_cd = 0;
                if (now_s - last_police_spawn >= 8 && client->player_info && client->player_info->flower_id != RR_NULL_ENTITY) {
                    struct rr_component_physical *sfp = rr_simulation_get_physical(&this->simulation, client->player_info->flower_id);
                    last_police_spawn = now_s;
                    float pts[6][2] = {{38*2048.f,76*2048.f},{46*2048.f,84*2048.f},{62*2048.f,76*2048.f},{85*2048.f,80*2048.f},{118*2048.f,80*2048.f},{138*2048.f,80*2048.f}};
                    for (int k = 0; k < 12; k++) {
                        if (sfp) rr_simulation_alloc_mob(&this->simulation, sfp->arena, pts[k][0], pts[k][1], (k % 2 == 0) ? rr_mob_id_hornet : rr_mob_id_rock, rr_rarity_id_rare, rr_simulation_team_id_mobs);
                    }
                }
                if (client->player_info && client->player_info->flower_id != RR_NULL_ENTITY) {
                    struct rr_component_physical *fp = rr_simulation_get_physical(&this->simulation, client->player_info->flower_id);
                    if (fp) {
                        float dx = fp->x - 142.0f * 2048.0f, dy = fp->y - 80.0f * 2048.0f;
                        if (dx * dx + dy * dy < 150.0f * 150.0f && now_s >= red_btn_cd) {
                            red_btn_cd = now_s + 25;
                            client->jail_until = 0;
                            rr_jail_save(client->ip_address, client->logged_user, 0);
                            struct rr_squad_member *ms = rr_squad_get_client_slot(this, client);
                            for (uint32_t i = 0; i < RR_MAX_CLIENT_COUNT; ++i) {
                                if (!rr_bitset_get(this->clients_in_use, i) || !this->clients[i].player_info) continue;
                                if (this->simulation.animation_length < (sizeof(this->simulation.animations) / sizeof(this->simulation.animations[0]))) {
                                    struct rr_simulation_animation *an = &this->simulation.animations[this->simulation.animation_length++];
                                    memset(an, 0, sizeof(*an)); an->type = rr_animation_type_chat; an->owner = this->clients[i].player_info->parent_id;
                                    strcpy(an->name, "[RIOT ALARM]"); snprintf(an->message, 64, "%s hit the RED BUTTON! ESCAPE!", ms ? ms->nickname : "Prisoner");
                                }
                            }
                            for (int k = 0; k < 6; k++)
                                rr_simulation_alloc_mob(&this->simulation, fp->arena, (135 + k) * 2048.0f, (76 + (k % 3) * 4) * 2048.0f, rr_mob_id_hornet, rr_rarity_id_epic, rr_simulation_team_id_mobs);
                        }
                    }
                }
            }
#endif

            if (client->jail_until == 0) {
                uint64_t su = rr_jail_load(client->ip_address, client->logged_user);
                if (su > now_s) client->jail_until = su;
            }
            if (client->jail_until > 0) {
                if (now_s >= client->jail_until) {
                    client->jail_until = 0; rr_jail_save(client->ip_address, client->logged_user, 0);
                    float sxy = 2.0f * RR_MAZES[RR_GLOBAL_BIOME].grid_size * 11.0f;
                    rr_tp_flower(this, client, sxy, sxy);
                } else {
                    client->has_checkpoint = 0; client->has_ygg_teleport = 0; client->checkpoint[0] = 0; client->checkpoint[1] = 0;
                    if (client->player_info && client->player_info->flower_id != RR_NULL_ENTITY) {
                        struct rr_component_physical *p = rr_simulation_get_physical(&this->simulation, client->player_info->flower_id);
                        if (p && (p->x < JAIL_X - JAIL_R || p->x > JAIL_X + JAIL_R || p->y < JAIL_Y - JAIL_R || p->y > JAIL_Y + JAIL_R))
                            rr_tp_flower(this, client, JAIL_X, JAIL_Y);
                        if ((client->play_seconds % 5) == 0 && this->simulation.animation_length < (sizeof(this->simulation.animations) / sizeof(this->simulation.animations[0]))) {
                            uint64_t rem = client->jail_until - now_s;
                            struct rr_simulation_animation *an = &this->simulation.animations[this->simulation.animation_length++];
                            memset(an, 0, sizeof(*an)); an->type = rr_animation_type_chat; an->owner = client->player_info->parent_id;
                            strcpy(an->name, "[JAIL]"); snprintf(an->message, 64, "Jailed! Left: %llum %llus", (unsigned long long)(rem / 60), (unsigned long long)(rem % 60));
                        }
                    }
                }
            }

                if (client->player_info != NULL) {
                    for (int qid = 1; qid <= 100; qid++) {
                        int b = qid - 1;
                        uint64_t dn = (b < 64) ? (client->ch_mask_lo & (1ULL << b)) : (client->ch_mask_hi & (1ULL << (b - 64)));
                        uint64_t sn = (b < 64) ? (client->ch_notified_lo & (1ULL << b)) : (client->ch_notified_hi & (1ULL << (b - 64)));
                        if (!dn && !sn && rr_eval_q100(client, qid, NULL, 0)) {
                            if (b < 64) client->ch_notified_lo |= (1ULL << b);
                            else client->ch_notified_hi |= (1ULL << (b - 64));
                            if (this->simulation.animation_length < (sizeof(this->simulation.animations) / sizeof(this->simulation.animations[0]))) {
                                struct rr_simulation_animation *an = &this->simulation.animations[this->simulation.animation_length++];
                                memset(an, 0, sizeof(*an));
                                an->type = rr_animation_type_chat;
                                an->owner = client->player_info->parent_id;
                                strcpy(an->name, "[Quest]");
                                snprintf(an->message, 64, "Quest #%d done! Open SHOP & QUEST!", qid);
                            }
                            rr_server_client_write_account(client);
                            for (int q2 = qid + 1; q2 <= 100; q2++) {
                                int b2 = q2 - 1;
                                uint64_t dn2 = (b2 < 64) ? (client->ch_mask_lo & (1ULL << b2)) : (client->ch_mask_hi & (1ULL << (b2 - 64)));
                                if (!dn2 && rr_eval_q100(client, q2, NULL, 0)) {
                                    if (b2 < 64) client->ch_notified_lo |= (1ULL << b2);
                                    else client->ch_notified_hi |= (1ULL << (b2 - 64));
                                }
                            }
                            break;
                        }
                    }
                }
            }
            
            if (client->verified && client->player_info && client->player_info->flower_id != RR_NULL_ENTITY) {
                struct rr_component_physical *jp = rr_simulation_get_physical(&this->simulation, client->player_info->flower_id);
                if (jp && (client->jail_until > 0 || (jp->x > -18600.0f && jp->x < -17400.0f && jp->y > -18600.0f && jp->y < -17400.0f))) {
                    float min_b = JAIL_X - 55.0f, max_b = JAIL_X + 55.0f;
                    if (jp->x < min_b) rr_component_physical_set_x(jp, min_b);
                    if (jp->x > max_b) rr_component_physical_set_x(jp, max_b);
                    if (jp->y < min_b) rr_component_physical_set_y(jp, min_b);
                    if (jp->y > max_b) rr_component_physical_set_y(jp, max_b);
                    struct rr_component_health *jh = rr_simulation_get_health(&this->simulation, client->player_info->flower_id);
                    if (jh) { jh->health = jh->max_health; jh->poison_ticks = 0; }
                }
            }

            if (++client->play_subticks >= 25) {
                client->play_subticks = 0;
                client->play_seconds++;

            uint64_t now_s = (uint64_t)time(NULL);

#ifdef ESCAPE
            {
                static uint64_t last_police_spawn = 0;
                static uint64_t red_btn_cd = 0;
                if (now_s - last_police_spawn >= 8 && client->player_info && client->player_info->flower_id != RR_NULL_ENTITY) {
                    struct rr_component_physical *sfp = rr_simulation_get_physical(&this->simulation, client->player_info->flower_id);
                    last_police_spawn = now_s;
                    float pts[6][2] = {{38*2048.f,76*2048.f},{46*2048.f,84*2048.f},{62*2048.f,76*2048.f},{85*2048.f,80*2048.f},{118*2048.f,80*2048.f},{138*2048.f,80*2048.f}};
                    for (int k = 0; k < 12; k++) {
                        if (sfp) rr_simulation_alloc_mob(&this->simulation, sfp->arena, pts[k][0], pts[k][1], (k % 2 == 0) ? rr_mob_id_hornet : rr_mob_id_rock, rr_rarity_id_rare, rr_simulation_team_id_mobs);
                    }
                }
                if (client->player_info && client->player_info->flower_id != RR_NULL_ENTITY) {
                    struct rr_component_physical *fp = rr_simulation_get_physical(&this->simulation, client->player_info->flower_id);
                    if (fp) {
                        float dx = fp->x - 142.0f * 2048.0f, dy = fp->y - 80.0f * 2048.0f;
                        if (dx * dx + dy * dy < 150.0f * 150.0f && now_s >= red_btn_cd) {
                            red_btn_cd = now_s + 25;
                            client->jail_until = 0;
                            rr_jail_save(client->ip_address, client->logged_user, 0);
                            struct rr_squad_member *ms = rr_squad_get_client_slot(this, client);
                            for (uint32_t i = 0; i < RR_MAX_CLIENT_COUNT; ++i) {
                                if (!rr_bitset_get(this->clients_in_use, i) || !this->clients[i].player_info) continue;
                                if (this->simulation.animation_length < (sizeof(this->simulation.animations) / sizeof(this->simulation.animations[0]))) {
                                    struct rr_simulation_animation *an = &this->simulation.animations[this->simulation.animation_length++];
                                    memset(an, 0, sizeof(*an)); an->type = rr_animation_type_chat; an->owner = this->clients[i].player_info->parent_id;
                                    strcpy(an->name, "[RIOT ALARM]"); snprintf(an->message, 64, "%s hit the RED BUTTON! ESCAPE!", ms ? ms->nickname : "Prisoner");
                                }
                            }
                            for (int k = 0; k < 6; k++)
                                rr_simulation_alloc_mob(&this->simulation, fp->arena, (135 + k) * 2048.0f, (76 + (k % 3) * 4) * 2048.0f, rr_mob_id_hornet, rr_rarity_id_epic, rr_simulation_team_id_mobs);
                        }
                    }
                }
            }
#endif

            if (client->jail_until == 0) {
                uint64_t su = rr_jail_load(client->ip_address, client->logged_user);
                if (su > now_s) client->jail_until = su;
            }
            if (client->jail_until > 0) {
                if (now_s >= client->jail_until) {
                    client->jail_until = 0; rr_jail_save(client->ip_address, client->logged_user, 0);
                    float sxy = 2.0f * RR_MAZES[RR_GLOBAL_BIOME].grid_size * 11.0f;
                    rr_tp_flower(this, client, sxy, sxy);
                } else {
                    client->has_checkpoint = 0; client->has_ygg_teleport = 0; client->checkpoint[0] = 0; client->checkpoint[1] = 0;
                    if (client->player_info && client->player_info->flower_id != RR_NULL_ENTITY) {
                        struct rr_component_physical *p = rr_simulation_get_physical(&this->simulation, client->player_info->flower_id);
                        if (p && (p->x < JAIL_X - JAIL_R || p->x > JAIL_X + JAIL_R || p->y < JAIL_Y - JAIL_R || p->y > JAIL_Y + JAIL_R))
                            rr_tp_flower(this, client, JAIL_X, JAIL_Y);
                        if ((client->play_seconds % 5) == 0 && this->simulation.animation_length < (sizeof(this->simulation.animations) / sizeof(this->simulation.animations[0]))) {
                            uint64_t rem = client->jail_until - now_s;
                            struct rr_simulation_animation *an = &this->simulation.animations[this->simulation.animation_length++];
                            memset(an, 0, sizeof(*an)); an->type = rr_animation_type_chat; an->owner = client->player_info->parent_id;
                            strcpy(an->name, "[JAIL]"); snprintf(an->message, 64, "Jailed! Left: %llum %llus", (unsigned long long)(rem / 60), (unsigned long long)(rem % 60));
                        }
                    }
                }
            }

            }
            if (client->player_info != NULL)
            {
                if (rr_simulation_entity_alive(
                        &this->simulation, client->player_info->flower_id) &&
                    !is_dead_flower(&this->simulation,
                                    client->player_info->flower_id) &&
                    !rr_simulation_get_physical(
                        &this->simulation,
                        client->player_info->flower_id)->bubbling_to_death)
                    rr_vector_set(
                        &rr_simulation_get_physical(
                             &this->simulation, client->player_info->flower_id)
                             ->acceleration,
                        client->player_accel_x, client->player_accel_y);
                if (client->player_info->drops_this_tick_size > 0)
                {
                    for (uint32_t i = 0;
                         i < client->player_info->drops_this_tick_size; ++i)
                    {
                        uint8_t id = client->player_info->drops_this_tick[i].id;
                        uint8_t rarity =
                            client->player_info->drops_this_tick[i].rarity;
                        client->inventory[id][rarity] +=100;
                    }
                    rr_server_client_write_to_api(client);
                    rr_server_client_write_account(client);
                    client->player_info->drops_this_tick_size = 0;
                }
            }
            if (client->in_squad)
                rr_server_client_broadcast_update(client);
            rr_server_client_broadcast_animation_update(client);
            // if (!client->dev)
            //     continue;
            struct proto_bug encoder;
            proto_bug_init(&encoder, outgoing_message);
            proto_bug_write_uint8(&encoder, rr_clientbound_squad_dump,
                                  "header");
            proto_bug_write_uint8(&encoder, client->dev, "is_dev");
            int8_t kick_vote_pos = -3;
            if (client->in_squad)
            {
                kick_vote_pos =
                    rr_squad_get_client_slot(this, client)->kick_vote_pos;
                if (kick_vote_pos == -1 && client->ticks_to_next_kick_vote > 0)
                    kick_vote_pos = -2;
            }
            proto_bug_write_uint8(&encoder, kick_vote_pos, "kick vote");
            for (uint32_t s = 0; s < RR_SQUAD_COUNT; ++s)
            {
                struct rr_squad *squad = &this->squads[s];
                for (uint32_t i = 0; i < RR_SQUAD_MEMBER_COUNT; ++i)
                {
                    if (squad->members[i].in_use == 0)
                    {
                        proto_bug_write_uint8(&encoder, 0, "bitbit");
                        continue;
                    }
                    struct rr_squad_member *member = &squad->members[i];
                    proto_bug_write_uint8(&encoder, 1, "bitbit");
                    proto_bug_write_uint8(&encoder, member->playing, "ready");
                    proto_bug_write_uint8(&encoder,
                                          member->client->disconnected,
                                          "disconnected");
                    uint8_t blocked = 0;
                    for (uint8_t j = 0; j < RR_MAX_CLIENT_COUNT; ++j)
                        if (strcmp(client->blocked_clients[j],
                            member->client->rivet_account.uuid) == 0)
                        {
                            blocked = 1;
                            break;
                        }
                    proto_bug_write_uint8(&encoder, blocked, "blocked");
                    proto_bug_write_uint8(&encoder, member->is_dev, "is_dev");
                    proto_bug_write_uint8(&encoder, member->kick_vote_count,
                                          "kick votes");
                    proto_bug_write_varuint(&encoder, member->level, "level");
                    proto_bug_write_string(&encoder, member->nickname, 16,
                                           "nickname");
                    proto_bug_write_string(&encoder, member->role, 16,
                                           "role");
                    proto_bug_write_string(&encoder, member->client->rivet_account.uuid, 37,
                                           "uuid");
                    proto_bug_write_string(&encoder, member->client->rivet_account.id, 20,
                                           "discord");
                    for (uint8_t j = 0; j < RR_MAX_SLOT_COUNT * 2; ++j)
                    {
                        proto_bug_write_uint8(&encoder, member->loadout[j].id,
                                              "id");
                        proto_bug_write_uint8(&encoder,
                                              member->loadout[j].rarity, "rar");
                    }
                }
                proto_bug_write_uint8(&encoder, squad->owner, "sqown");
                proto_bug_write_uint8(&encoder, squad->private, "private");
                proto_bug_write_uint8(&encoder, squad->expose_code,
                                      "expose_code");
                proto_bug_write_uint8(&encoder, RR_GLOBAL_BIOME, "biome");
                char joined_code[16];
                if (client->dev || squad->expose_code ||
                    (client->in_squad && client->squad == s))
                    sprintf(joined_code, "%s-%s",
                            RR_BIOME_SERVERS[RR_GLOBAL_BIOME].squad_prefix,
                            squad->squad_code);
                else
                    strcpy(joined_code, "(private)");
                proto_bug_write_string(&encoder, joined_code, 16, "squad code");
            }
            rr_server_client_write_message(client, encoder.start,
                                           encoder.current - encoder.start);
#if defined(JAIL) || defined(ESCAPE)
    RR_GLOBAL_BIOME = rr_biome_id_garden;
#endif
#ifdef PVP
            struct proto_bug lb_encoder;
            proto_bug_init(&lb_encoder, outgoing_message);
            proto_bug_write_uint8(&lb_encoder, rr_clientbound_leaderboard_update,
                                  "header");
            proto_bug_write_uint8(&lb_encoder, lb_top_n, "leaderboard count");
            for (uint8_t a = 0; a < lb_top_n; ++a)
            {
                struct rr_server_client *entry_client =
                    &this->clients[lb_sorted[a].client_index];
                proto_bug_write_string(
                    &lb_encoder,
                    this->squads[entry_client->squad]
                        .members[entry_client->squad_pos]
                        .nickname,
                    16, "nickname");
                proto_bug_write_varuint(&lb_encoder, lb_sorted[a].points,
                                        "points");
            }
            proto_bug_write_varuint(&lb_encoder, lb_rank_by_client[i],
                                    "own rank");
            proto_bug_write_varuint(&lb_encoder, client->pvp_points,
                                    "own points");
            rr_server_client_write_message(
                client, lb_encoder.start, lb_encoder.current - lb_encoder.start);
#endif
        }
    }
    rr_simulation_for_each_entity(&this->simulation, &this->simulation,
                                  rr_simulation_tick_entity_resetter_function);
}

void rr_server_run(struct rr_server *this)
{
    {
        struct lws_context_creation_info info = {0};

        info.protocols =
            (struct lws_protocols[]){{"g", lws_callback, sizeof(uint8_t),
                                      MESSAGE_BUFFER_SIZE, 0, NULL, 0},
                                     {0}};

        info.port = RR_BIOME_SERVERS[RR_GLOBAL_BIOME].port;
        info.user = this;
        info.pt_serv_buf_size = MESSAGE_BUFFER_SIZE;

        this->server = lws_create_context(&info);
        assert(this->server);
    }
    {
        struct lws_context_creation_info info = {0};
        struct lws_client_connect_info client_info = {0};

        struct lws_protocols protocols[] = {
            {
                "g",
                api_lws_callback,
                0,
                128 * 1024,
            },
            {NULL, NULL, 0, 0} // terminator
        };
        info.port = CONTEXT_PORT_NO_LISTEN;
        info.protocols = protocols;
        info.gid = -1;
        info.uid = -1;
        info.user = this;

        this->api_client_context = lws_create_context(&info);
        if (!this->api_client_context)
        {
            puts("couldn't create api server context");
            exit(1);
        }
        client_info.context = this->api_client_context;
        client_info.address =
#ifndef RIVET_BUILD
            "localhost";
#else
            "45.79.197.197";
#endif
        client_info.port = 55554;
        client_info.path = "/api/" RR_API_SECRET;
        client_info.host = client_info.address;
        client_info.origin = client_info.address;
        client_info.protocol = protocols[0].name;
        this->api_client = lws_client_connect_via_info(&client_info);
        if (!this->api_client)
        {
            puts("couldn't create api client");
            exit(1);
        }
    }
    struct timeval start;
    struct timeval end;
    while (1)
    {
        gettimeofday(&start, NULL);
        lws_service(this->server, -1);
        lws_service(this->api_client_context, -1);
        server_tick(this);
        this->simulation.animation_length = 0;
        gettimeofday(&end, NULL);

        uint64_t elapsed_time = (end.tv_sec - start.tv_sec) * 1000000 +
                                (end.tv_usec - start.tv_usec);
        if (elapsed_time > 25000)
            fprintf(stderr, "tick took %lu microseconds\n", elapsed_time);
        int64_t to_sleep = 40000 - elapsed_time;
        if (to_sleep > 0)
            usleep(to_sleep);
    }
}
