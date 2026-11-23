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

#include <Server/Waves.h>

#include <math.h>
#include <stdlib.h>

#include <Server/Simulation.h>
#include <Shared/StaticData.h>
#include <Shared/Utilities.h>

uint32_t get_spawn_rarity(float difficulty)
{
    if (difficulty < 1)
        difficulty = 1;
    double rarity_seed = rr_frand();
    uint32_t rarity_cap = rr_rarity_id_common + (difficulty + 7) / 8;
    if (rarity_cap > rr_rarity_id_gods)
        rarity_cap = rr_rarity_id_gods;
    uint32_t rarity = rarity_cap >= 2 ? rarity_cap - 2 : 0;
    for (; rarity < rarity_cap; ++rarity)
        if (pow(1 - (1 - RR_MOB_WAVE_RARITY_COEFFICIENTS[rarity + 1]) * 0.3,
                pow(1.5, difficulty)) >= rarity_seed)
            break;
    return rarity;
}

uint8_t get_spawn_id(uint8_t biome, struct rr_maze_grid *zone)
{
    if (biome == rr_biome_id_pvp)
    {
        long idx = zone - (const struct rr_maze_grid *)RR_MAZE_PVP;
        int gx = (idx >= 0 && idx < 160 * 160) ? (int)(idx % 160) : 44;
        int gy = (idx >= 0 && idx < 160 * 160) ? (int)(idx / 160) : 56;
        double r_ant = rr_frand();

        // ПРАВЫЙ СЕКТОР (gx >= 85): Лабиринт Термитов + глубокие Черви (gy >= 122)
        if (gx >= 85)
        {
            if (gy >= 122 && r_ant < 0.35) return rr_mob_id_worm;
            if (r_ant < 0.55) return rr_mob_id_termite_worker;
            if (r_ant < 0.88) return rr_mob_id_termite_soldier;
            if (r_ant < 0.98) return rr_mob_id_termite_egg;
            return rr_mob_id_queen_termite;
        }
        // ВЕРХНИЙ СЕКТОР (gx < 85 && gy < 64): Тоннели Обычных Муравьёв
        if (gy < 64)
        {
            if (r_ant < 0.55) return rr_mob_id_worker_ant;
            if (r_ant < 0.88) return rr_mob_id_soldier_ant;
            if (r_ant < 0.98) return rr_mob_id_ant_egg;
            return rr_mob_id_queen_ant;
        }
        // НИЖНИЙ-ЛЕВЫЙ СЕКТОР (gx < 85 && gy >= 64): Пещеры Огненных Муравьёв
        if (r_ant < 0.55) return rr_mob_id_fire_worker_ant;
        if (r_ant < 0.88) return rr_mob_id_fire_soldier_ant;
        if (r_ant < 0.98) return rr_mob_id_fire_ant_egg;
        return rr_mob_id_queen_fire_ant;
    }
     double r = rr_frand();
    if (r < 0.25)
        return rr_mob_id_fat_bee;
    if (r < 0.50)
        return rr_mob_id_ladybug;
    if (r < 0.75)
        return rr_mob_id_rock;
    if (r < 0.85)
        return rr_mob_id_dragonfly;
    double *table =
        biome < rr_biome_id_garden ? RR_HELL_CREEK_MOB_ID_RARITY_COEFFICIENTS
                                   : RR_GARDEN_MOB_ID_RARITY_COEFFICIENTS;
    double seed = rr_frand();
    uint8_t id = 0;
    for (; id < rr_mob_id_max - 1; ++id)
        if (seed <= table[id])
            break;
    return id;
}

int should_spawn_at(uint8_t id, uint8_t rarity)
{
    return rarity >= RR_MOB_DATA[id].min_rarity &&
           rarity <= RR_MOB_DATA[id].max_rarity;
}