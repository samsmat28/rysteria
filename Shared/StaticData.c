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

#include <Shared/StaticData.h>

#include <math.h>
#include <stdio.h>

#include <Shared/Utilities.h>

// clang-format off
struct rr_petal_base_stat_scale const offensive[rr_rarity_id_max] = {
    {1.0, 1.0},
    {1.7, 2.0},
    {2.9, 4.0},
    {5.0, 8.0},
    {8.5,  16},
    {14.5, 48},
    {24.6,144},
    {42.0,432},
    {72.0, 1296},
    {125.0, 3888},
    {220.0, 11664}
};

struct rr_petal_base_stat_scale const defensive[rr_rarity_id_max] = {
    {1.0, 1.0},
    {2.0, 1.7},
    {4.0, 2.9},
    {8.0, 5.0},
    {16,  8.5},
    {48, 14.5},
    {144,24.6},
    {432,42.0},
    {1296, 72.0},
    {3888, 125.0},
    {11664, 220.0}
};

struct rr_petal_data RR_PETAL_DATA[rr_petal_id_max] = {
//   id                     min_rarity              scale        dmg      hp   clump   cd 2cd  count
    {rr_petal_id_none,      rr_rarity_id_common,    offensive,  0.0f,   0.0f,   0.0f,   0,  0, {0,0,0,0,0,0,0,0,0,0}},
    {rr_petal_id_basic,     rr_rarity_id_common,    offensive, 10.0f,  15.0f,   0.0f,  50,  0, {1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_pellet,    rr_rarity_id_common,    offensive,  8.0f,   5.0f,   0.0f,  13,  0, {1,2,2,3,3,5,6,6,6,6}},
    {rr_petal_id_fossil,    rr_rarity_id_common,    offensive,  5.0f, 150.0f,   0.0f, 100,  0, {1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_stinger,   rr_rarity_id_common,    offensive, 70.0f,   3.0f,  10.0f, 150,  0, {1,1,1,1,1,3,5,5,5,5}},
    {rr_petal_id_berry,     rr_rarity_id_rare,      offensive,  5.0f,   5.0f,  12.0f,  13,  0, {1,1,1,1,1,2,3,3,3,3}},
    {rr_petal_id_shell,     rr_rarity_id_rare,      offensive, 10.0f,  16.0f,   0.0f,  50, 13, {1,1,1,1,1,2,3,3,3,3}},
    {rr_petal_id_peas,      rr_rarity_id_rare,      offensive, 22.0f,  12.0f,   8.0f,  13, 12, {4,4,4,4,4,4,5,5,5,5}},
    {rr_petal_id_leaf,      rr_rarity_id_unusual,   offensive,  9.0f,   8.0f,   8.0f,  38,  0, {1,1,1,1,1,2,2,2,2,2}},
    {rr_petal_id_egg,       rr_rarity_id_unusual,   defensive,  1.0f,  75.0f,  10.0f,  25,100, {3,3,3,2,2,2,1,1,1,1}},
    {rr_petal_id_magnet,    rr_rarity_id_unusual,   defensive,  2.0f,  25.0f,   0.0f,  38,  0, {1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_uranium,   rr_rarity_id_rare,      offensive,  3.0f,  40.0f,   0.0f,  25, 25, {1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_feather,   rr_rarity_id_common,    defensive,  1.0f,   3.0f,   0.0f,  25,  0, {1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_azalea,    rr_rarity_id_common,    defensive,  5.0f,  15.0f,  10.0f,  25, 50, {1,1,1,1,1,1,3,3,3,3}},
    {rr_petal_id_bone,      rr_rarity_id_common,    defensive,  2.5f,  25.0f,   0.0f,  68,  0, {1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_web,       rr_rarity_id_rare,      defensive,  5.0f,   5.0f,   0.0f,  50, 13, {1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_seed,      rr_rarity_id_legendary, defensive,  1.0f,  75.0f,   0.0f,  63, 13, {1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_gravel,    rr_rarity_id_unusual,   offensive,  9.0f,  20.0f,   0.0f,  20, 10, {1,2,2,2,3,3,4,4,4,4}},
    {rr_petal_id_club,      rr_rarity_id_common,    offensive,  2.0f,1200.0f,   0.0f, 200,  0, {1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_crest,     rr_rarity_id_rare,      offensive,  0.0f,   0.0f,   0.0f,   0,  0, {0,0,0,0,0,0,0,0,0,0}},
    {rr_petal_id_droplet,   rr_rarity_id_common,    offensive, 15.0f,   5.0f,   0.0f,  37,  0, {1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_beak,      rr_rarity_id_unusual,   defensive,  5.0f,   5.0f,   0.0f,  55,  0, {1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_lightning, rr_rarity_id_unusual,   offensive,  7.0f,   1.0f,   0.0f,  63,  0, {1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_third_eye, rr_rarity_id_legendary, offensive,  0.0f,   0.0f,   0.0f,   0,  0, {0,0,0,0,0,0,0,0,0,0}},
    {rr_petal_id_nest,      rr_rarity_id_legendary, defensive,  5.0f,  25.0f,   0.0f, 250, 13, {1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_fireball,  rr_rarity_id_unusual,   offensive,260.0f,   1.0f,   0.0f, 600,  0, {1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_meat,      rr_rarity_id_common,    offensive,  0.0f,1600.0f,   0.0f, 188, 13, {1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_bubble,    rr_rarity_id_common,    defensive,  1.0f,  25.0f,   0.0f, 150,  3, {1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_meteor,    rr_rarity_id_unusual,   defensive,  0.0f,   0.0f,   0.0f,  75,  0, {1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_mandible,  rr_rarity_id_common,    offensive,  5.0f,  10.0f,   0.0f,  75,  0, {1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_wax,       rr_rarity_id_unusual,   offensive, 10.0f,  10.0f,  10.0f,  38,  0, {2,2,2,2,2,2,2,2,2,2}},
    {rr_petal_id_sand,      rr_rarity_id_common,    offensive, 15.0f,  10.0f,  10.0f,  37,  0, {4,4,4,4,4,4,4,4,4,4}},
    {rr_petal_id_mint,      rr_rarity_id_unusual,   offensive,  5.0f,  10.0f,  10.0f,  50, 25, {1,1,1,1,1,1,1,1,1,1}},
     {rr_petal_id_rose,      rr_rarity_id_common,    defensive,  5.0f,  15.0f,  10.0f,  25, 50, {1,1,1,1,1,1,3,3,3,3}},
    {rr_petal_id_rock,      rr_rarity_id_common,    defensive, 15.0f, 350.0f,   0.0f, 120,  0, {1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_grass,              rr_rarity_id_common,    defensive,  5.0f,  15.0f, 10.0f,  50,  0, {1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_rice,               rr_rarity_id_common,    offensive,  6.0f,   5.0f,  0.0f,   5,  0, {1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_clover,             rr_rarity_id_unusual,   defensive,  4.0f,  10.0f,  0.0f,  50,  0, {1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_light,              rr_rarity_id_common,    offensive,  8.0f,   6.0f,  0.0f,  15,  0, {1,2,3,3,5,6,6,6,6,6}},
    {rr_petal_id_yucca,              rr_rarity_id_common,    defensive,  6.0f,  15.0f,  8.0f,  45,  0, {1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_triangle,           rr_rarity_id_unusual,   offensive, 14.0f,   6.0f,  0.0f,  30,  0, {1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_corn,               rr_rarity_id_common,    offensive, 12.0f,  65.0f,  0.0f,  35,  0, {1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_yggdrasil, rr_rarity_id_common, defensive, 8.0f, 10.0f, 0.0f, 60, 0, {1,1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_claw, rr_rarity_id_common, offensive, 14.0f, 18.0f, 0.0f, 25, 0, {1,1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_fang, rr_rarity_id_common, offensive, 16.0f, 22.0f, 0.0f, 30, 0, {1,1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_tooth, rr_rarity_id_common, offensive, 15.0f, 26.0f, 0.0f, 32, 0, {1,1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_horn, rr_rarity_id_common, offensive, 18.0f, 24.0f, 0.0f, 35, 0, {1,1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_thagomizer, rr_rarity_id_common, offensive, 11.0f, 15.0f, 0.0f, 30, 0, {4,4,4,4,4,4,4,4,4,4,4}},
    {rr_petal_id_scythe, rr_rarity_id_common, offensive, 22.0f, 32.0f, 0.0f, 40, 0, {1,1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_magma, rr_rarity_id_common, offensive, 20.0f, 28.0f, 0.0f, 38, 0, {1,1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_obsidian, rr_rarity_id_common, offensive, 35.0f, 45.0f, 0.0f, 55, 0, {1,1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_plate, rr_rarity_id_common, defensive, 28.0f, 8.0f, 0.0f, 40, 0, {1,1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_scale, rr_rarity_id_common, defensive, 22.0f, 12.0f, 0.0f, 35, 0, {2,2,2,2,2,2,2,2,2,2,2}},
    {rr_petal_id_amber, rr_rarity_id_common, defensive, 18.0f, 8.0f, 8.0f, 45, 0, {1,1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_branch, rr_rarity_id_common, defensive, 16.0f, 10.0f, 6.0f, 35, 0, {1,1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_pearl, rr_rarity_id_common, defensive, 14.0f, 6.0f, 10.0f, 40, 0, {1,1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_tail, rr_rarity_id_common, defensive, 12.0f, 10.0f, 0.0f, 25, 0, {1,1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_frill, rr_rarity_id_common, defensive, 16.0f, 11.0f, 0.0f, 30, 0, {1,1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_venom, rr_rarity_id_common, offensive, 10.0f, 24.0f, 0.0f, 32, 0, {2,2,2,2,2,2,2,2,2,2,2}},
    {rr_petal_id_sail, rr_rarity_id_common, defensive, 15.0f, 9.0f, 0.0f, 30, 0, {1,1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_ash, rr_rarity_id_common, defensive, 12.0f, 14.0f, 0.0f, 28, 0, {3,3,3,3,3,3,3,3,3,3,3}},
    {rr_petal_id_crown, rr_rarity_id_common, defensive, 30.0f, 25.0f, 12.0f, 50, 0, {1,1,1,1,1,1,1,1,1,1,1}},
    {rr_petal_id_relic, rr_rarity_id_common, offensive, 32.0f, 38.0f, 8.0f, 48, 0, {1,1,1,1,1,1,1,1,1,1,1}},
};    

char const *RR_PETAL_NAMES[rr_petal_id_max] = {
    "Secret",   "Petal",     "Pellet",    "Fossil", "Stinger",  "Berry",   "Shell",
    "Peas",     "Leaf",      "Egg",       "Magnet", "Uranium",  "Feather", "Azalea",
    "Bone",     "Web",       "Seed",      "Gravel", "Club",     "Crest",   "Droplet",
    "Beak",     "Lightning", "Third Eye", "Nest",   "Fireball", "Meat",    "Bubble",
    "Meteor",   "Mandible",  "Wax",       "Sand",   "Mint",     "Rose",     "Rock", "Grass", "Rice", "Clover", "Light", "Yucca", "Triangle", "Corn", "Yggdrasil", "Claw", "Fang", "Tooth", "Horn", "Thagomizer", "Scythe", "Magma", "Obsidian", "Plate", "Scale", "Amber", "Branch", "Pearl", "Tail", "Frill", "Venom", "Sail", "Ash", "Crown", "Relic"
};
    
char const *RR_PETAL_DESCRIPTIONS[rr_petal_id_max] = {
    0,
    "It's just a petal",
    "Low damage, but there's lots",
    "It came from a dino",
    "Ow that hurts",
    "Gives your other petals more energy",
    "Poor snail",
    "Splits in 4. Or maybe 5 if you're a pro",
    "Heals you gradually",
    "Spawns a pet dinosaur to protect you",
    "Increases loot pickup radius. Stacks diminishingly",
    "Does damage to the owner and enemies in a large range",
    "It's so light it increases your movement speed. Stacks diminishingly",
    "It heals you",
    "Gives the player armor. Stacks diminishingly",
    "It slows everything down",
    "What does this one do",
    "Tiny rocks that stay on the ground and trip dinos",
    "Heavy and sturdy",
    "Increases your maximum vision range. Stacks diminishingly",
    "This mysterious petal reverses your petal rotation",
    "Stuns mobs and prevents them from moving",
    "A stunning display",
    "Your petals hate it and want to move further away. Stacks diminishingly",
    "Home sweet home",
    "Nice ball bro",
    "Meat meta",
    "Pop and you're gone. Does not stack",
    "Spawns a pet meteor to protect you",
    "Does more damage if target hp is below 50%",
    "Made by the bees",
    "Very fine",
    "Remember to feed your pets"
     "Its healing properties are amazing",
    "Extremely heavy and durable"
};

struct rr_mob_data RR_MOB_DATA[rr_mob_id_max] = {
//   id                                     min_rarity  max_rarity              hp dmg    rad  ai_passive_rarity    ai_neutral_rarity    ai_aggro_rarity       loot
    {rr_mob_id_triceratops,        rr_rarity_id_common, rr_rarity_id_gods,  45, 15, 30.0f, rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_max,     {{rr_petal_id_leaf,    0.15},{rr_petal_id_fossil,    0.05}}},
    {rr_mob_id_trex,               rr_rarity_id_common, rr_rarity_id_gods,  40, 25, 32.0f, rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_unusual, {{rr_petal_id_stinger, 0.03},{rr_petal_id_egg,       0.05},{rr_petal_id_meat,      0.01}}},
    {rr_mob_id_fern,               rr_rarity_id_common, rr_rarity_id_gods,  10,  5, 24.0f, rr_rarity_id_max,    rr_rarity_id_max,    rr_rarity_id_max,     {{rr_petal_id_leaf,     0.1},{rr_petal_id_azalea,    0.25}}},
    {rr_mob_id_tree,               rr_rarity_id_common, rr_rarity_id_gods, 100,  5, 64.0f, rr_rarity_id_max,    rr_rarity_id_max,    rr_rarity_id_max,     {{rr_petal_id_leaf,     2.5},{rr_petal_id_peas,       2.5},{rr_petal_id_seed,      0.05}}},
    {rr_mob_id_pteranodon,         rr_rarity_id_common, rr_rarity_id_gods,  40, 15, 20.0f, rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_rare,    {{rr_petal_id_shell,   0.05},{rr_petal_id_beak,      0.15},{rr_petal_id_nest,      0.01}}},
    {rr_mob_id_dakotaraptor,       rr_rarity_id_common, rr_rarity_id_gods,  35, 10, 25.0f, rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_epic,    {{rr_petal_id_crest,    0.1},{rr_petal_id_feather,    0.1},{rr_petal_id_pellet,    0.05}}},
    {rr_mob_id_pachycephalosaurus, rr_rarity_id_common, rr_rarity_id_gods,  35, 20, 20.0f, rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_common,  {{rr_petal_id_fossil,   0.1},{rr_petal_id_berry,      0.1},{rr_petal_id_web,       0.05}}},
    {rr_mob_id_ornithomimus,       rr_rarity_id_common, rr_rarity_id_gods,  25, 10, 20.0f, rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_max,     {{rr_petal_id_feather,  0.1},{rr_petal_id_droplet,   0.05},{rr_petal_id_pellet,     0.1}}},
    {rr_mob_id_ankylosaurus,       rr_rarity_id_common, rr_rarity_id_gods,  50, 10, 30.0f, rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_max,     {{rr_petal_id_club,    0.15},{rr_petal_id_gravel,    0.05},{rr_petal_id_bubble,     0.1}}},
    {rr_mob_id_meteor,             rr_rarity_id_common, rr_rarity_id_gods, 100, 10, 32.0f, rr_rarity_id_common, rr_rarity_id_max,    rr_rarity_id_max,     {{rr_petal_id_magnet,   0.5},{rr_petal_id_uranium,   0.05},{rr_petal_id_fireball,   1.0},{rr_petal_id_meteor, 2.0}}},
    {rr_mob_id_quetzalcoatlus,     rr_rarity_id_common, rr_rarity_id_gods,  65, 20, 28.0f, rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_common,  {{rr_petal_id_beak,    0.05},{rr_petal_id_fossil,     0.1},{rr_petal_id_lightning, 0.01}}},
    {rr_mob_id_edmontosaurus,      rr_rarity_id_common, rr_rarity_id_gods,  50, 15, 30.0f, rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_max,     {{rr_petal_id_bone,    0.01},{rr_petal_id_fossil,     0.1},{rr_petal_id_third_eye, 0.05}}},
    {rr_mob_id_ant,                rr_rarity_id_common, rr_rarity_id_gods,  10, 10, 20.0f, rr_rarity_id_common, rr_rarity_id_max,    rr_rarity_id_max,     {{rr_petal_id_pellet,   0.1},{rr_petal_id_leaf,       0.1},{rr_petal_id_mandible,  0.05}}},
    {rr_mob_id_hornet,             rr_rarity_id_common, rr_rarity_id_gods,  28, 25, 25.0f, rr_rarity_id_common, rr_rarity_id_max,    rr_rarity_id_max,     {{rr_petal_id_stinger,  0.1},{rr_petal_id_crest,     0.05}}},
    {rr_mob_id_dragonfly,          rr_rarity_id_common, rr_rarity_id_gods,  20, 10, 25.0f, rr_rarity_id_common, rr_rarity_id_max,    rr_rarity_id_max,     {{rr_petal_id_pellet,   0.1},{rr_petal_id_magnet,    0.05}}},
    {rr_mob_id_honeybee,           rr_rarity_id_common, rr_rarity_id_gods,  12, 25, 22.0f, rr_rarity_id_common, rr_rarity_id_max,    rr_rarity_id_max,     {{rr_petal_id_wax,     0.05},{rr_petal_id_stinger,   0.05}}},
    {rr_mob_id_beehive,            rr_rarity_id_common, rr_rarity_id_gods,   0,  0, 45.0f, rr_rarity_id_common, rr_rarity_id_max,    rr_rarity_id_max,     {{rr_petal_id_wax,     0.05},{rr_petal_id_azalea,    0.05}}},
    {rr_mob_id_spider,             rr_rarity_id_common, rr_rarity_id_gods,  20, 25, 25.0f, rr_rarity_id_common, rr_rarity_id_max,    rr_rarity_id_max,     {{rr_petal_id_web,      0.1},{rr_petal_id_third_eye, 0.01}}},
    {rr_mob_id_house_centipede,    rr_rarity_id_common, rr_rarity_id_gods,  25, 10, 23.0f, rr_rarity_id_common, rr_rarity_id_max,    rr_rarity_id_max,     {{rr_petal_id_peas,     0.1},{rr_petal_id_sand,      0.05}}},
    {rr_mob_id_lanternfly,         rr_rarity_id_common, rr_rarity_id_gods,  20, 10, 25.0f, rr_rarity_id_common, rr_rarity_id_max,    rr_rarity_id_max,     {{rr_petal_id_mint,     0.1},{rr_petal_id_sand,      0.05}}},
    {rr_mob_id_fat_bee, rr_rarity_id_common, rr_rarity_id_gods, 60, 45, 34.0f, rr_rarity_id_max, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_stinger, 0.25},{rr_petal_id_wax, 0.20},{rr_petal_id_berry, 0.05}}},
    {rr_mob_id_ladybug, rr_rarity_id_common, rr_rarity_id_gods, 35, 10, 26.0f, rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_rose, 0.35},{rr_petal_id_leaf, 0.15}}},
    {rr_mob_id_rock,    rr_rarity_id_common, rr_rarity_id_gods, 150, 10, 38.0f, rr_rarity_id_max,    rr_rarity_id_max,    rr_rarity_id_max, {{rr_petal_id_rock, 0.35},{rr_petal_id_magnet, 0.25}}},
    {rr_mob_id_worker_ant,       rr_rarity_id_common, rr_rarity_id_gods, 22, 10, 26.0f, rr_rarity_id_max, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_leaf, 0.25},{rr_petal_id_grass, 0.25},{rr_petal_id_rice, 0.20},{rr_petal_id_light, 0.20},{rr_petal_id_clover, 0.08}}},
    {rr_mob_id_soldier_ant,      rr_rarity_id_common, rr_rarity_id_gods, 40, 16, 31.0f, rr_rarity_id_max, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_leaf, 0.25},{rr_petal_id_grass, 0.25},{rr_petal_id_rice, 0.20},{rr_petal_id_light, 0.20},{rr_petal_id_clover, 0.12}}},
        {rr_mob_id_fire_worker_ant,  rr_rarity_id_common, rr_rarity_id_gods, 30, 14, 27.0f, rr_rarity_id_max, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_yucca, 0.35},{rr_petal_id_corn, 0.30},{rr_petal_id_triangle, 0.20}}},
        {rr_mob_id_fire_soldier_ant, rr_rarity_id_common, rr_rarity_id_gods, 55, 22, 32.0f, rr_rarity_id_max, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_triangle, 0.35},{rr_petal_id_corn, 0.30},{rr_petal_id_yucca, 0.25}}},
        {rr_mob_id_termite_worker,   rr_rarity_id_common, rr_rarity_id_gods, 28, 12, 27.0f, rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_bone, 0.30},{rr_petal_id_sand, 0.25},{rr_petal_id_pellet, 0.15}}},
        {rr_mob_id_termite_soldier,  rr_rarity_id_common, rr_rarity_id_gods, 50, 20, 32.0f, rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_bone, 0.35},{rr_petal_id_mandible, 0.30},{rr_petal_id_sand, 0.20},{rr_petal_id_egg, 0.12}}},
    {rr_mob_id_worm,             rr_rarity_id_common, rr_rarity_id_gods, 45, 24, 21.0f, rr_rarity_id_max, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_sand, 0.35},{rr_petal_id_peas, 0.25},{rr_petal_id_gravel, 0.20},{rr_petal_id_bone, 0.15}}},
    {rr_mob_id_ant_egg,          rr_rarity_id_common, rr_rarity_id_gods, 18,  0, 24.0f, rr_rarity_id_max, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_egg, 0.35},{rr_petal_id_leaf, 0.25},{rr_petal_id_clover, 0.10}}},
        {rr_mob_id_fire_ant_egg,     rr_rarity_id_common, rr_rarity_id_gods, 24,  0, 25.0f, rr_rarity_id_max, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_yucca, 0.35},{rr_petal_id_corn, 0.30},{rr_petal_id_triangle, 0.20}}},
        {rr_mob_id_termite_egg,      rr_rarity_id_common, rr_rarity_id_gods, 22,  0, 25.0f, rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_egg, 0.35},{rr_petal_id_bone, 0.25},{rr_petal_id_sand, 0.20}}},
        {rr_mob_id_queen_ant,        rr_rarity_id_common, rr_rarity_id_gods, 3500, 35, 185.0f, rr_rarity_id_max, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_egg, 1.0},{rr_petal_id_clover, 0.60},{rr_petal_id_light, 0.75},{rr_petal_id_yggdrasil, 0.45}}},
            {rr_mob_id_queen_fire_ant,   rr_rarity_id_common, rr_rarity_id_gods, 4500, 45, 190.0f, rr_rarity_id_max, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_triangle, 0.85},{rr_petal_id_corn, 0.85},{rr_petal_id_yucca, 0.85},{rr_petal_id_yggdrasil, 0.45}}},
            {rr_mob_id_queen_termite,    rr_rarity_id_common, rr_rarity_id_gods, 4000, 40, 185.0f, rr_rarity_id_max, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_egg, 0.95},{rr_petal_id_bone, 0.85},{rr_petal_id_mandible, 0.85},{rr_petal_id_yggdrasil, 0.45}}},
    {rr_mob_id_compsognathus, rr_rarity_id_common, rr_rarity_id_gods, 22, 12, 18.0f, rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_claw, 0.35},{rr_petal_id_tail, 0.3}}},
    {rr_mob_id_stegosaurus, rr_rarity_id_common, rr_rarity_id_gods, 85, 18, 38.0f, rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_thagomizer, 0.35},{rr_petal_id_plate, 0.35}}},
    {rr_mob_id_dilophosaurus, rr_rarity_id_common, rr_rarity_id_gods, 48, 22, 26.0f, rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_venom, 0.35},{rr_petal_id_frill, 0.3}}},
    {rr_mob_id_spinosaurus, rr_rarity_id_common, rr_rarity_id_gods, 140, 32, 46.0f, rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_sail, 0.4},{rr_petal_id_tooth, 0.35}}},
    {rr_mob_id_carnotaurus, rr_rarity_id_common, rr_rarity_id_gods, 110, 30, 36.0f, rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_horn, 0.4},{rr_petal_id_claw, 0.35}}},
    {rr_mob_id_brachiosaurus, rr_rarity_id_common, rr_rarity_id_gods, 320, 15, 68.0f, rr_rarity_id_max, rr_rarity_id_max, rr_rarity_id_max, {{rr_petal_id_amber, 0.45},{rr_petal_id_branch, 0.45}}},
    {rr_mob_id_therizinosaurus, rr_rarity_id_common, rr_rarity_id_gods, 180, 42, 44.0f, rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_scythe, 0.45},{rr_petal_id_feather, 0.4}}},
    {rr_mob_id_mosasaurus, rr_rarity_id_common, rr_rarity_id_gods, 260, 45, 56.0f, rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_pearl, 0.45},{rr_petal_id_scale, 0.45}}},
    {rr_mob_id_volcano, rr_rarity_id_common, rr_rarity_id_gods, 500, 35, 64.0f, rr_rarity_id_max, rr_rarity_id_max, rr_rarity_id_max, {{rr_petal_id_magma, 0.5},{rr_petal_id_obsidian, 0.45}}},
    {rr_mob_id_titanoboa, rr_rarity_id_common, rr_rarity_id_gods, 1600, 55, 72.0f, rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_crown, 0.65},{rr_petal_id_relic, 0.65}}},
};

char const *RR_MOB_NAMES[rr_mob_id_max] = {
"Triceratops","T-Rex","Fern","Tree","Pteranodon","Dakotaraptor",
"Pachycephalosaurus","Ornithomimus","Ankylosaurus","Meteor",
"Quetzalcoatlus","Edmontosaurus","Ant","Hornet","Dragonfly",
"Honeybee","Beehive","Spider","House Centipede","Lanternfly",
"Fat Bee","Ladybug","Rock", "Worker Ant", "Soldier Ant", "Fire Worker Ant", "Fire Soldier Ant", "Termite Worker", "Termite Soldier", "Worm", "Ant Egg", "Fire Ant Egg", "Termite Egg", "Queen Ant", "Queen Fire Ant", "Queen Termite", "Compsognathus", "Stegosaurus", "Dilophosaurus", "Spinosaurus", "Carnotaurus", "Brachiosaurus", "Therizinosaurus", "Mosasaurus", "Volcano", "Titanoboa"
};

uint32_t RR_MOB_DIFFICULTY_COEFFICIENTS[rr_mob_id_max] = {
    3, //tric
    4, //trex
    1, //fern
    2, //tree
    5, //pter
    5, //dako
    3, //pachy
    2, //ornith
    4, //anky
    1, //meteor
    5, //quetz
    3, //edmo
};

double RR_HELL_CREEK_MOB_ID_RARITY_COEFFICIENTS[rr_mob_id_max] = {
    50,   //tric
    100,  //trex
    15,   //fern
    0.25, //tree
    75,   //pter
    50,   //dako
    25,   //pachy
    40,   //ornith
    25,   //anky
    1,    //meteor
    75,   //quetz
    25,   //edmo
    50, //fat_bee
    60, //ladybug
    45, //rock
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
};

double RR_GARDEN_MOB_ID_RARITY_COEFFICIENTS[rr_mob_id_max] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 10, 30};

struct rr_petal_rarity_scale RR_PETAL_RARITY_SCALE[rr_rarity_id_max] = {
    {1,    240, 45 },
    {1.8,  120, 60 },
    {3.5,  60,  75 },
    {6.8,  30,  100},
    {12.5, 15,  125},
    {24.5, 7.5, 150},
    {60,   2.5, 200},
    {180,  0.5, 250},
    {540,  0.2, 310},
    {1620, 0.1, 380},
    {4860, 0.05, 460},
};

struct rr_mob_rarity_scale RR_MOB_RARITY_SCALING[rr_rarity_id_max] = {
    {1,      1,    1  },
    {2.4,    1.7,  1.2},
    {6,      2.9,  1.5}, 
    {14.4,   5,    2  },
    {40,     8.5,  2.8},
    {1000,    30, 10  },
    {25000,   80, 18},
    {500000,  200,   30  },
};
// clang-format on

uint32_t RR_RARITY_COLORS[rr_rarity_id_max] = {
    0xff7eef6d, 0xffffe65d, 0xff4d52e3, 0xff861fde,
    0xffde1f1f, 0xff1fdbde, 0xffff2b75, 0xff2bffa3, 0xff9b30ff, 0xff8e99a4, 0xffffffff};

char const *RR_RARITY_NAMES[rr_rarity_id_max] = {
    "Common",    "Unusual", "Rare",   "Epic",
    "Legendary", "Mythic",  "Exotic", "Ancient"};

#ifdef PVP
uint64_t RR_PVP_POINTS_PER_RARITY[rr_rarity_id_max] = {
    20, 100, 1000, 10000, 150000, 2250000, 45000000, 900000000, 5000000000ULL, 25000000000ULL, 100000000000ULL};
#endif

double RR_MOB_WAVE_RARITY_COEFFICIENTS[rr_rarity_id_max + 1] = {
    0, 1, 6, 10, 15, 25, 160, 1200, 250, 180, 140, 100};

double RR_DROP_RARITY_COEFFICIENTS[rr_rarity_id_max] = {
    0, 1, 8, 15, 40, 150, 500, 2500, 12000, 60000, 300000};
double RR_MOB_LOOT_RARITY_COEFFICIENTS[rr_rarity_id_max] = {2.5, 4,  6,   15,
                                                            35,  50, 125, 150, 200, 260, 350};

static void init_game_coefficients()
{
    double sum = 1;
    double sum2 = 1;
    for (uint64_t a = 1; a < rr_rarity_id_max; ++a)
        RR_MOB_LOOT_RARITY_COEFFICIENTS[a] *=
            RR_MOB_LOOT_RARITY_COEFFICIENTS[a - 1];
    for (uint64_t a = 1; a <= rr_rarity_id_exotic; ++a)
    {
        sum += (RR_DROP_RARITY_COEFFICIENTS[a + 1] =
                    RR_DROP_RARITY_COEFFICIENTS[a] /
                    RR_DROP_RARITY_COEFFICIENTS[a + 1]);
    }
    for (uint64_t a = 1; a <= rr_rarity_id_exotic + 1; ++a)
    {
        RR_DROP_RARITY_COEFFICIENTS[a] = RR_DROP_RARITY_COEFFICIENTS[a] / sum +
                                         RR_DROP_RARITY_COEFFICIENTS[a - 1];
    }
    RR_DROP_RARITY_COEFFICIENTS[rr_rarity_id_exotic + 1] = 1;
    for (uint64_t a = 1; a <= rr_rarity_id_ultimate; ++a)
    {
        sum2 += (RR_MOB_WAVE_RARITY_COEFFICIENTS[a + 1] =
                     RR_MOB_WAVE_RARITY_COEFFICIENTS[a] /
                     RR_MOB_WAVE_RARITY_COEFFICIENTS[a + 1]);
    }
    for (uint64_t a = 1; a <= rr_rarity_id_ultimate + 1; ++a)
    {
        RR_MOB_WAVE_RARITY_COEFFICIENTS[a] =
            RR_MOB_WAVE_RARITY_COEFFICIENTS[a] / sum2 +
            RR_MOB_WAVE_RARITY_COEFFICIENTS[a - 1];
    }
    RR_MOB_WAVE_RARITY_COEFFICIENTS[rr_rarity_id_ultimate + 1] = 1;
    for (uint64_t mob = 1; mob < rr_mob_id_max; ++mob)
    {
        RR_HELL_CREEK_MOB_ID_RARITY_COEFFICIENTS[mob] +=
            RR_HELL_CREEK_MOB_ID_RARITY_COEFFICIENTS[mob - 1];
        RR_GARDEN_MOB_ID_RARITY_COEFFICIENTS[mob] +=
            RR_GARDEN_MOB_ID_RARITY_COEFFICIENTS[mob - 1];
    }
    for (uint64_t mob = 0; mob < rr_mob_id_max; ++mob)
    {
        RR_HELL_CREEK_MOB_ID_RARITY_COEFFICIENTS[mob] /=
            RR_HELL_CREEK_MOB_ID_RARITY_COEFFICIENTS[rr_mob_id_max - 1];
        RR_GARDEN_MOB_ID_RARITY_COEFFICIENTS[mob] /=
            RR_GARDEN_MOB_ID_RARITY_COEFFICIENTS[rr_mob_id_max - 1];
    }
}

#define offset(a, b)                                                           \
    ((x + a < 0 || y + b < 0 || x + a >= size / 2 || y + b >= size / 2)        \
         ? 0                                                                   \
         : template[(y + b) * size / 2 + x + a])
#define maze_grid(x, y) maze[(y)*size + (x)]

static void init_maze(uint32_t size, uint8_t *template,
                      struct rr_maze_grid *maze)
{
    for (int32_t y = 0; y < size / 2; ++y)
    {
        for (int32_t x = 0; x < size / 2; ++x)
        {
            uint8_t this_tile = offset(0, 0);
            maze_grid(x * 2, y * 2).difficulty = this_tile;
            maze_grid(x * 2 + 1, y * 2).difficulty = this_tile;
            maze_grid(x * 2, y * 2 + 1).difficulty = this_tile;
            maze_grid(x * 2 + 1, y * 2 + 1).difficulty = this_tile;
            this_tile = this_tile != 0;
            // top left
            uint8_t top = offset(0, -1);
            uint8_t bottom = offset(0, 1);
            if (this_tile)
            {
                if (top == 0)
                {
                    if (offset(-1, 0) == 0)
                        maze_grid(x * 2, y * 2).value = 7;
                    else
                        maze_grid(x * 2, y * 2).value = this_tile;
                    if (offset(1, 0) == 0)
                        maze_grid(x * 2 + 1, y * 2).value = 5;
                    else
                        maze_grid(x * 2 + 1, y * 2).value = this_tile;
                }
                else
                {
                    maze_grid(x * 2, y * 2).value = this_tile;
                    maze_grid(x * 2 + 1, y * 2).value = this_tile;
                }
                if (bottom == 0)
                {
                    if (offset(-1, 0) == 0)
                        maze_grid(x * 2, y * 2 + 1).value = 6;
                    else
                        maze_grid(x * 2, y * 2 + 1).value = this_tile;
                    if (offset(1, 0) == 0)
                        maze_grid(x * 2 + 1, y * 2 + 1).value = 4;
                    else
                        maze_grid(x * 2 + 1, y * 2 + 1).value = this_tile;
                }
                else
                {
                    maze_grid(x * 2, y * 2 + 1).value = this_tile;
                    maze_grid(x * 2 + 1, y * 2 + 1).value = this_tile;
                }
            }
            else
            {
                if (top)
                {
                    if (offset(-1, 0) && offset(-1, -1))
                        maze_grid(x * 2, y * 2).value = 15;
                    else
                        maze_grid(x * 2, y * 2).value = this_tile;
                    if (offset(1, 0) && offset(1, -1))
                        maze_grid(x * 2 + 1, y * 2).value = 13;
                    else
                        maze_grid(x * 2 + 1, y * 2).value = this_tile;
                }
                else
                {
                    maze_grid(x * 2, y * 2).value = this_tile;
                    maze_grid(x * 2 + 1, y * 2).value = this_tile;
                }
                if (bottom)
                {
                    if (offset(-1, 0) && offset(-1, 1))
                        maze_grid(x * 2, y * 2 + 1).value = 14;
                    else
                        maze_grid(x * 2, y * 2 + 1).value = this_tile;
                    if (offset(1, 0) && offset(1, 1))
                        maze_grid(x * 2 + 1, y * 2 + 1).value = 12;
                    else
                        maze_grid(x * 2 + 1, y * 2 + 1).value = this_tile;
                }
                else
                {
                    maze_grid(x * 2, y * 2 + 1).value = this_tile;
                    maze_grid(x * 2 + 1, y * 2 + 1).value = this_tile;
                }
            }
        }
    }
}

static void print_chances(float difficulty)
{
    printf("-----Chances for %.0f-----\n", difficulty);
    uint32_t rarity_cap = rr_rarity_id_common + (difficulty + 7) / 8;
    if (rarity_cap > rr_rarity_id_gods)
        rarity_cap = rr_rarity_id_gods;
    uint32_t rarity = rarity_cap >= 2 ? rarity_cap - 2 : 0;
    for (; rarity <= rarity_cap; ++rarity)
    {
        float start =
            rarity == 0
                ? 0
                : pow(1 - (1 - RR_MOB_WAVE_RARITY_COEFFICIENTS[rarity]) * 0.3,
                      pow(1.5, difficulty));
        float end =
            rarity == rarity_cap
                ? 1
                : pow(1 - (1 - RR_MOB_WAVE_RARITY_COEFFICIENTS[rarity + 1]) *
                              0.3,
                      pow(1.5, difficulty));
        printf("%s: %.9f (1 per %.4f)\n", RR_RARITY_NAMES[rarity], end - start,
               1 / (end - start));
    }
}

double RR_BASE_CRAFT_CHANCES[rr_rarity_id_max - 1] = {0.5,  0.3,  0.15, 0.05,
                                                      0.03, 0.02, 0.015, 0.01, 0.007, 0.005};
double RR_CRAFT_CHANCES[rr_rarity_id_max - 1];

static double from_prd_base(double C)
{
    double pProcOnN = 0;
    double pProcByN = 0;
    double sumNpProcOnN = 0;

    double maxFails = ceil(1 / C);
    for (uint32_t N = 1; N <= maxFails; ++N)
    {
        pProcOnN = fmin(1, N * C) * (1 - pProcByN);
        pProcByN += pProcOnN;
        sumNpProcOnN += N * pProcOnN;
    }
    return (1 / sumNpProcOnN);
}

static double get_prd_base(double p)
{
    if (p == 0)
        return 0;
    double Cupper = p;
    double Clower = 0;
    double Cmid = p / 2;
    double p1 = 0;
    double p2 = 1;
    while (1)
    {
        Cmid = (Cupper + Clower) / 2;
        p1 = from_prd_base(Cmid);
        if (fabs(p1 - p2) <= 0)
            break;

        if (p1 > p)
            Cupper = Cmid;
        else
            Clower = Cmid;
        p2 = p1;
    }
    return Cmid;
}

#define init(MAZE)                                                             \
    init_maze(sizeof(RR_MAZE_##MAZE[0]) / sizeof(struct rr_maze_grid),         \
              &RR_MAZE_TEMPLATE_##MAZE[0][0], &RR_MAZE_##MAZE[0][0]);

void rr_static_data_init()
{
    for (uint32_t r = 0; r < rr_rarity_id_max - 1; ++r)
        RR_CRAFT_CHANCES[r] = get_prd_base(RR_BASE_CRAFT_CHANCES[r]);
    init_game_coefficients();
    init(HELL_CREEK);
    init(BURROW);
    init(PVP);
    init(NETHER);
    init(OCEAN);
    init(PLAINS);
#ifdef RR_SERVER
    print_chances(1);  // c
    print_chances(4);  // C
    print_chances(8);  // u
    print_chances(12); // U
    print_chances(16); // r
    print_chances(20); // R
    print_chances(24); // e
    print_chances(28); // E
    print_chances(32); // l
    print_chances(36); // L
    print_chances(40); // m
    print_chances(44); // M
    print_chances(48); // x
    print_chances(52); // X
    print_chances(56); // a
    print_chances(60); // A
#endif
}

double xp_to_reach_level(uint32_t level)
{
    if (level <= 60)
        return (level + 5) * pow(1.175, level);
    double base = (level + 5) * pow(1.175, 60);
    for (uint32_t i = 60; i < level; ++i)
        base *= rr_fclamp(1.18 - 0.0075 * (i - 60), 1.1, 1.18);
    return base;
}

uint32_t level_from_xp(double xp)
{
    uint32_t level = 1;
    while (xp >= xp_to_reach_level(level + 1))
        xp -= xp_to_reach_level(++level);
    return level;
}

#define _ 0
#define c 1
#define C 4
#define u 8
#define U 12
#define r 16
#define R 20
#define e 24
#define E 28
#define l 32
#define L 36
#define m 40
#define M 44
#define x 48
#define X 52
#define a 56
#define A 60
#define o 64
#define O 64
#define h 68
#define H 68
#define g 72
#define G 72

#define RR_DEFINE_MAZE(name, size)                                             \
    struct rr_maze_grid RR_MAZE_##name[size][size];                            \
    uint8_t RR_MAZE_TEMPLATE_##name[size / 2][size / 2]
// clang-format off
RR_DEFINE_MAZE(HELL_CREEK, 160) = {
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 0
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 1
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 2
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 3
    {_,_,_,_,_,_,_,_,_,_,_,c,c,c,c,c,c,c,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 4
    {_,_,_,_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 5
    {_,_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,_,_,_,_,_,_,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 6
    {_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,_,_,_,_,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 7
    {_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,_,_,_,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 8
    {_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,_,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 9
    {_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,_,_,_,_,_,_,_,_,_,e,e,e,e,e,e,e,_,_,_,_,_,_,_,_,_,_,_}, // 10
    {_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,C,C,C,C,C,C,C,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,_,_,_,_,_,_,_,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_,_,_,_}, // 11
    {_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,C,C,C,C,C,C,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,_,_,_,_,_,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_,_,_}, // 12
    {_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,C,C,C,C,C,C,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,_,_,_,_,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_,_}, // 13
    {_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,C,C,C,C,C,C,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,_,_,_,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_}, // 14
    {_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,C,C,C,C,C,C,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,R,R,R,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_}, // 15
    {_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,C,C,C,C,C,C,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,R,R,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_}, // 16
    {_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,C,C,C,C,C,C,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,R,R,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_}, // 17
    {_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,_,_,C,C,C,C,C,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,R,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_}, // 18
    {_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,R,R,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_}, // 19
    {_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,_,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,R,R,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_}, // 20
    {_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,_,_,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,R,R,R,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_}, // 21
    {_,_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,_,_,_,_,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,R,R,R,R,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_}, // 22
    {_,_,_,_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,_,_,_,_,R,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_}, // 23
    {_,_,_,_,_,_,_,_,_,_,_,c,c,c,c,c,c,c,E,E,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,_,_,_,_,_,_,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_}, // 24
    {_,_,_,_,_,_,_,_,_,_,_,_,_,E,E,E,E,E,E,E,E,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,L,L,_,_,_,_,_,_,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_}, // 25
    {_,_,_,_,_,_,_,_,_,_,_,_,_,E,E,E,E,E,E,E,E,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,L,L,L,L,L,L,L,L,_,_,_,_,_,_,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_}, // 26
    {_,_,_,_,_,_,_,_,_,_,_,_,_,E,E,E,E,E,E,E,E,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,L,L,L,L,L,L,L,L,L,_,_,_,_,_,_,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_}, // 27
    {_,_,_,_,_,_,_,_,_,_,_,_,_,E,E,E,E,E,E,E,E,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,L,L,L,L,L,L,L,L,L,_,_,_,_,_,_,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_}, // 28
    {_,_,_,_,_,_,_,_,_,_,_,_,_,E,E,E,E,E,E,E,E,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,L,L,L,L,L,L,L,L,_,_,_,_,_,_,_,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_}, // 29
    {_,_,_,_,_,_,_,_,_,_,_,_,_,E,E,E,E,E,E,E,E,E,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,L,L,L,L,L,L,L,L,_,_,_,_,_,_,_,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_}, // 30
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,E,E,E,E,E,E,E,E,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,L,L,L,L,L,L,L,L,L,_,_,_,_,_,_,_,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_,_}, // 31
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,E,E,E,E,E,E,E,E,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,L,L,L,L,L,L,L,L,L,_,_,_,_,_,_,_,_,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_,_,_}, // 32
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,E,E,E,E,E,E,E,E,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,L,L,L,L,L,L,L,L,_,_,_,_,_,_,_,_,_,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_,_,_,_}, // 33
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,E,E,E,E,E,E,E,E,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,L,L,L,L,L,L,L,L,_,_,_,_,_,_,_,_,_,_,_,e,e,e,e,e,e,e,_,_,_,_,_,_,_,_,_,_,_}, // 34
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,E,E,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,L,L,L,L,L,L,L,L,L,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 35
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,L,L,L,L,L,L,L,L,L,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 36
    {_,_,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,L,L,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 37
    {_,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 38
    {_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 39
    {_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 40
    {_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 41
    {_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 42
    {_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 43
    {_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,M,M,M,M,M,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 44
    {_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,M,M,M,M,M,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 45
    {_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,M,M,M,M,M,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 46
    {_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,M,M,M,M,M,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 47
    {_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,M,M,M,M,M,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 48
    {_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,M,M,M,M,M,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 49
    {_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,M,M,M,M,M,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 50
    {_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 51
    {_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 52
    {_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 53
    {_,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 54
    {_,_,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 55
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 56
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 57
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,a,a,a,o,o,h,g,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,o,o,o,o,o,h,h,h,h,h,h,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 58
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,a,a,o,o,h,g,g,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,m,m,m,m,o,o,o,o,o,o,o,o,h,h,h,h,h,h,h,h,h,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 59
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,a,o,o,o,o,o,o,o,o,o,o,h,h,h,h,h,h,h,h,h,g,g,g,_,_,_,_,_,_,_,_,_,_}, // 60
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,a,a,o,o,o,o,o,o,o,o,o,o,h,h,h,h,h,h,h,h,h,g,g,g,g,_,_,_,_,_,_,_,_,_}, // 61
    {_,_,_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_,_,_,_,_,_,_,_,a,a,a,o,o,o,o,o,o,o,o,o,o,h,h,h,h,h,h,h,h,h,g,g,g,g,g,_,_,_,_,_,_,_,_}, // 62
    {_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_,_,_,_,_,a,a,a,a,o,o,o,o,o,o,o,o,o,o,h,h,h,h,h,h,h,h,h,g,g,g,g,g,g,_,_,_,_,_,_,_}, // 63
    {_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,_,_,_,a,a,a,a,a,a,a,a,a,a,o,o,o,o,o,o,o,o,o,o,h,h,h,h,h,h,h,h,h,g,g,g,g,g,g,g,_,_,_,_,_,_}, // 64
    {_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,a,a,a,a,a,a,a,a,a,a,a,a,o,o,o,o,o,o,o,o,o,o,h,h,h,h,h,h,h,h,h,g,g,g,g,g,g,g,_,_,_,_,_,_}, // 65
    {_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,a,a,a,a,a,a,a,a,a,a,a,a,o,o,o,o,o,o,o,o,o,o,h,h,h,h,h,h,h,h,h,g,g,g,g,g,g,g,_,_,_,_,_,_}, // 66
    {_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,a,a,a,a,a,a,a,a,a,a,a,a,o,o,o,o,o,o,o,o,o,o,h,h,h,h,h,h,h,h,h,g,g,g,g,g,g,g,_,_,_,_,_,_}, // 67
    {_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,a,a,a,a,a,a,a,a,a,a,a,a,o,o,o,o,o,o,o,o,o,o,h,h,h,h,h,h,h,h,h,g,g,g,g,g,g,g,_,_,_,_,_,_}, // 68
    {_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,a,a,a,a,a,a,a,a,a,a,a,a,o,o,o,o,o,o,o,o,o,o,h,h,h,h,h,h,h,h,h,g,g,g,g,g,g,g,_,_,_,_,_,_}, // 69
    {_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,a,a,a,a,a,a,a,a,a,a,a,a,o,o,o,o,o,o,o,o,o,o,h,h,h,h,h,h,h,h,h,g,g,g,g,g,g,g,_,_,_,_,_,_}, // 70
    {_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,a,a,a,a,a,a,a,a,a,a,a,a,o,o,o,o,o,o,o,o,o,o,h,h,h,h,h,h,h,h,h,g,g,g,g,g,g,_,_,_,_,_,_,_}, // 71
    {_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_,_,_,_,_,a,a,a,o,o,o,o,o,o,o,o,o,o,h,h,h,h,h,h,h,h,h,g,g,g,g,g,_,_,_,_,_,_,_,_}, // 72
    {_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_,_,_,_,_,_,_,a,a,o,o,o,o,o,o,o,o,o,o,h,h,h,h,h,h,h,h,h,g,g,g,g,_,_,_,_,_,_,_,_,_}, // 73
    {_,_,_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,a,o,o,o,o,o,o,o,o,o,o,h,h,h,h,h,h,h,h,h,g,g,g,_,_,_,_,_,_,_,_,_,_}, // 74
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,o,o,o,o,o,o,o,o,h,h,h,h,h,h,h,h,h,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 75
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,o,o,o,o,o,h,h,h,h,h,h,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 76
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 77
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 78
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 79
};

RR_DEFINE_MAZE(PVP, 160) = {
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 0
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 1
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,r,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 2
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 3
    {_,_,_,_,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 4
    {_,_,_,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 5
    {_,_,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 6
    {_,_,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 7
    {_,_,_,_,_,_,_,_,_,_,_,r,r,r,r,r,r,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_}, // 8
    {_,_,_,_,_,_,_,_,_,_,_,r,r,r,u,u,u,u,u,u,u,u,u,u,u,u,u,u,r,u,u,u,u,u,u,u,u,r,r,_,_,_,_,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_}, // 9
    {_,_,_,_,_,_,_,_,_,_,r,r,r,r,u,u,u,u,u,u,u,u,u,u,u,u,u,u,_,_,u,u,u,u,u,u,u,r,r,r,r,r,_,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,m,m,m,m,m,m,m,m,m,x,x,_,_,_,_,_,_,_,_}, // 10
    {_,_,_,_,_,_,_,_,_,r,r,r,r,u,u,u,u,u,u,u,u,u,u,u,u,u,u,_,_,_,u,u,u,u,u,u,u,r,r,r,r,r,r,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,m,m,m,m,m,m,m,m,m,x,x,_,_,_,_,_,_,_,_}, // 11
    {_,_,_,_,_,_,_,r,r,r,r,r,r,u,u,u,u,u,u,u,u,u,u,u,u,u,_,_,_,_,_,u,u,u,u,u,u,r,r,r,r,r,r,r,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,m,m,m,m,m,m,m,m,m,x,x,x,_,_,_,_,_,_,_}, // 12
    {_,_,_,_,_,_,r,r,r,r,r,r,r,u,u,u,_,u,u,u,u,u,u,u,_,_,_,_,_,u,u,u,u,u,u,u,u,r,r,r,r,r,r,r,_,_,_,_,_,l,l,l,l,l,l,l,l,_,_,_,l,m,m,m,m,m,m,m,m,m,x,x,x,_,_,_,_,_,_,_}, // 13
    {_,_,_,_,_,_,r,r,r,r,r,r,r,u,u,u,u,u,_,u,_,_,u,_,_,_,_,u,u,u,u,u,u,u,u,u,_,_,_,r,r,r,r,r,_,_,_,_,_,l,l,l,l,l,l,l,_,_,_,_,m,m,m,m,m,m,m,m,m,m,x,x,x,_,_,_,_,_,_,_}, // 14
    {_,_,_,_,_,_,_,r,r,r,r,r,r,u,u,u,u,u,u,u,u,u,_,u,u,u,u,u,u,u,u,u,u,u,u,u,_,_,_,r,r,r,r,r,_,_,_,_,l,l,l,l,l,l,l,_,_,_,_,_,_,m,m,m,m,m,m,_,m,m,x,x,x,x,_,_,_,_,_,_}, // 15
    {_,_,_,_,_,_,_,r,r,r,r,r,r,_,u,u,u,u,u,u,c,c,c,c,c,c,c,c,c,c,u,u,u,u,u,u,u,_,_,_,_,r,_,_,_,_,_,_,_,l,l,l,l,l,l,_,_,_,_,_,_,_,_,m,_,_,_,_,_,m,x,x,x,x,_,_,_,_,_,_}, // 16
    {_,_,_,_,_,_,_,r,r,r,r,r,u,_,_,u,u,u,u,u,c,c,c,c,c,c,c,c,c,c,u,u,u,u,u,u,u,u,u,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,_,_,_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,_,_,_,_,_}, // 17
    {_,_,_,_,_,_,_,r,r,r,r,r,u,u,u,u,u,u,u,u,c,c,c,c,c,c,c,c,c,c,u,u,u,u,u,u,u,u,u,r,_,_,_,_,_,_,_,_,_,e,e,e,e,e,e,l,l,_,_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,_,_,_,_,_}, // 18
    {_,_,_,_,_,_,_,_,r,r,r,r,u,u,u,u,_,u,_,u,c,c,c,c,c,c,c,c,c,c,_,_,_,_,u,u,u,u,u,r,_,_,_,r,r,r,e,_,_,_,e,e,e,e,e,l,_,_,_,_,_,_,_,_,_,_,x,_,x,x,x,x,x,x,x,_,_,_,_,_}, // 19
    {_,_,_,_,_,_,_,_,_,r,r,r,u,u,u,u,_,_,_,u,_,_,c,c,c,c,_,_,_,_,_,_,_,_,u,u,u,u,u,r,_,_,r,r,r,r,e,_,_,_,_,e,e,e,e,l,l,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_}, // 20
    {_,_,_,_,_,_,_,_,_,r,r,r,u,u,u,u,u,u,u,_,_,_,_,_,_,c,c,c,c,c,_,_,u,u,u,u,u,u,u,_,_,r,r,r,r,r,e,_,_,_,e,e,e,e,e,l,l,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,x,x,_,_,_,_,_,_}, // 21
    {_,_,_,_,_,_,_,_,_,_,_,r,u,u,u,u,u,u,u,u,_,_,_,_,_,c,c,c,c,c,c,c,u,u,u,u,u,u,u,_,r,r,r,r,r,r,e,_,_,e,e,e,e,e,e,l,l,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,x,_,_,_,_,_,_,_}, // 22
    {_,_,_,_,_,_,_,_,_,_,_,_,u,u,u,u,u,u,u,c,_,_,_,_,c,c,c,c,c,c,c,c,u,u,u,u,u,u,u,r,r,r,r,r,r,r,_,_,_,e,e,e,e,e,e,l,l,l,_,_,_,_,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_}, // 23
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,u,u,u,u,u,c,c,c,_,c,c,c,c,c,c,c,c,c,u,u,u,u,u,u,u,r,r,r,r,r,r,_,e,e,e,e,e,e,e,e,e,l,l,l,_,_,_,_,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_}, // 24
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,u,u,u,u,c,c,c,c,c,c,c,c,c,c,c,c,c,u,u,u,u,u,u,u,r,r,r,r,r,r,r,e,e,e,e,e,e,e,e,e,l,l,l,l,_,_,_,_,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_}, // 25
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,u,_,u,c,c,c,c,c,c,c,c,c,_,_,_,c,u,u,u,u,u,u,u,r,r,r,r,r,r,r,e,e,e,e,e,e,e,e,e,l,l,l,l,_,_,_,_,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_}, // 26
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,u,c,c,c,c,c,c,c,c,_,_,_,_,_,_,u,_,u,u,u,u,r,r,r,r,r,r,r,e,e,e,e,e,e,e,_,e,l,l,l,l,l,_,_,_,_,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_}, // 27
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,u,c,c,c,c,c,c,c,c,_,_,_,_,_,_,_,_,_,_,_,_,_,r,r,r,r,r,r,e,e,e,e,e,e,_,_,_,l,l,l,l,l,l,_,_,_,_,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_}, // 28
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,u,u,u,u,u,u,u,u,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,r,e,e,e,e,e,_,_,_,_,l,l,l,l,l,_,l,_,l,m,_,m,m,m,m,m,m,m,_,_,_,_,_,_,_}, // 29
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,u,u,u,u,u,u,u,u,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,m,m,_,m,m,m,m,m,m,_,_,_,_,_,_,_}, // 30
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,u,u,u,u,u,u,u,u,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,m,m,m,m,m,m,m,m,m,x,_,_,_,_,_,_}, // 31
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,u,u,u,u,u,u,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,m,m,m,m,m,m,m,m,m,x,_,_,_,_,_,_}, // 32
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,u,u,u,u,u,u,u,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,m,m,m,_,m,m,m,m,m,x,_,_,_,_,_,_}, // 33
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,u,u,u,u,u,u,u,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,m,m,m,_,m,m,m,m,m,x,_,_,_,_,_,_}, // 34
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,u,u,u,u,u,u,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,m,m,_,_,m,m,m,m,m,_,_,_,_,_,_,_}, // 35
    {_,_,_,_,_,_,_,_,_,_,_,r,_,r,r,r,r,r,r,r,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,_,_,l,l,l,l,l,l,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_}, // 36
    {_,_,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,_,_,_,_,_,m,m,m,m,m,_,m,m,m,m,m,m,_,_,_,_,_,_,_,_}, // 37
    {_,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,m,m,m,m,m,_,_,_,_,_,_,_,_,_}, // 38
    {_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,_,_,_,_,e,e,e,e,e,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,m,m,m,m,m,_,_,_,_,_,_,_,_,_}, // 39
    {_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,e,e,e,e,e,e,e,e,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,_,_,_,_,_,_,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_}, // 40
    {_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,e,e,e,e,e,e,e,e,e,l,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_}, // 41
    {_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_}, // 42
    {_,_,_,_,_,_,_,_,_,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,l,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_}, // 43
    {_,_,_,_,_,_,_,_,_,e,e,e,e,e,e,e,e,e,e,_,e,e,e,e,e,e,e,e,e,e,e,l,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,x,x,x,x,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 44
    {_,_,_,_,_,_,_,_,_,_,e,e,e,e,e,e,_,_,_,_,_,_,e,e,e,e,e,e,e,e,e,l,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,_,x,_,x,x,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 45
    {_,_,_,_,_,_,_,_,_,_,e,e,e,e,e,e,_,_,_,_,_,_,_,e,e,e,e,e,e,e,e,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_,_,_,_,_,a,a,_,_,_,_,_,_,_,_}, // 46
    {_,_,_,_,_,_,_,_,_,e,e,e,e,e,_,_,_,_,_,_,_,_,_,e,e,e,e,e,e,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,_,x,x,x,_,x,x,_,_,_,_,a,a,a,a,_,_,_,_,_,_,_}, // 47
    {_,_,_,_,_,_,_,_,_,e,e,e,e,e,_,_,_,_,_,_,_,_,_,e,e,e,e,e,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,_,x,x,x,x,x,x,x,_,_,_,a,a,a,a,a,_,_,_,_,_,_,_}, // 48
    {_,_,_,_,_,_,_,_,_,e,e,e,e,e,_,_,_,_,_,_,_,_,_,_,e,e,e,e,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,_,a,a,a,a,a,a,a,_,_,_,_,_,_}, // 49
    {_,_,_,_,_,_,_,_,e,e,e,e,e,e,_,_,_,_,_,_,_,_,_,e,e,e,e,e,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,_,_,_,x,x,x,x,x,x,x,x,x,_,x,a,a,a,a,a,a,_,_,_,_,_,_}, // 50
    {_,_,_,_,_,_,_,e,e,e,e,e,e,e,e,_,_,_,_,_,_,_,_,e,e,e,e,e,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,_,_,_,x,x,x,x,x,x,x,x,x,x,_,a,a,a,a,a,_,_,_,_,_,_,_}, // 51
    {_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,l,l,l,l,l,l,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,_,_,_,x,x,x,x,x,x,x,x,x,x,x,a,a,a,a,a,_,_,_,_,_,_,_}, // 52
    {_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,l,l,l,l,l,l,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,_,_,_,x,x,x,x,x,x,x,x,x,x,a,a,a,a,_,_,_,_,_,_,_,_}, // 53
    {_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,_,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,a,_,x,x,x,x,x,x,x,x,x,x,a,a,a,a,_,_,_,_,_,_,_,_}, // 54
    {_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,a,a,a,a,a,a,a,_,_,a,a,a,a,a,a,a,a,a,a,a,a,_,_,_,_,_,_,_,_,_}, // 55
    {_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,a,a,a,a,a,a,a,a,_,a,a,a,a,a,a,a,a,a,a,a,a,_,_,_,_,_,_,_,_,_}, // 56
    {_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,_,_,_,_,_,_,_,_,_}, // 57
    {_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,_,_,_,_,_,_,_,_,_,_}, // 58
    {_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,_,_,_,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,_,_,_,_,_,_,_,_,_}, // 59
    {_,_,_,_,_,_,_,l,l,l,l,l,l,_,l,_,_,_,_,_,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,a,a,a,a,a,a,a,a,a,a,a,_,_,a,a,a,a,a,a,_,_,_,_,_,_,_,_}, // 60
    {_,_,_,_,_,_,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,a,a,a,a,a,a,a,a,_,_,_,_,_,_,a,a,a,a,a,a,_,_,_,_,_,_,_,_}, // 61
    {_,_,_,_,_,_,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,o,o,o,o,o,o,_,_,_,_,_,_,_,_,_,o,o,o,o,o,o,_,_,_,_,_,_,_}, // 62
    {_,_,_,_,_,_,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,o,o,o,o,o,o,_,_,_,_,_,_,_,_,_,_,o,o,o,o,o,o,_,_,_,_,_,_,_}, // 63
    {_,_,_,_,_,_,m,m,m,m,m,m,_,_,m,m,_,_,_,_,_,_,_,_,_,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,o,o,o,o,o,o,o,_,_,_,_,_,_,_,_,_,_,_,o,o,o,o,o,_,_,_,_,_,_,_}, // 64
    {_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,_,x,x,_,_,_,_,_,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,o,o,o,o,o,o,_,_,_,_,_,_,_,h,h,_,_,_,o,o,o,o,o,o,_,_,_,_,_,_}, // 65
    {_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,x,x,_,_,_,_,_,_,m,m,m,m,m,m,m,m,_,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,o,o,o,o,o,_,_,_,_,g,g,g,g,h,h,h,_,_,o,o,o,o,o,o,_,_,_,_,_,_}, // 66
    {_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,x,x,x,x,_,_,_,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,o,o,o,o,o,o,_,_,_,h,g,g,g,g,h,h,h,o,o,o,o,o,o,o,o,_,_,_,_,_,_}, // 67
    {_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,x,x,x,x,x,m,m,m,m,m,m,m,m,m,m,m,m,m,x,_,_,_,_,_,_,_,_,_,_,_,_,_,o,o,o,o,o,o,o,h,h,h,g,g,g,g,h,h,h,o,o,o,o,o,o,o,o,_,_,_,_,_,_}, // 68
    {_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,x,x,x,x,x,_,m,m,m,m,m,m,m,m,m,m,m,m,x,_,_,_,_,_,_,_,_,_,_,_,_,_,h,h,h,h,h,h,h,h,h,h,g,g,g,g,h,h,h,h,h,h,h,h,h,h,h,_,_,_,_,_,_}, // 69
    {_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_,_,_,_,_,_,_,h,h,h,h,h,h,h,h,h,h,g,g,g,g,h,h,h,h,h,h,h,h,h,h,h,_,_,_,_,_,_}, // 70
    {_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_,_,_,_,_,_,_,_,_,h,h,h,h,h,h,h,h,g,g,g,g,h,h,h,h,h,h,h,h,h,h,_,_,_,_,_,_,_}, // 71
    {_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,_,_,_,_,_,_,_,_,_}, // 72
    {_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,g,g,g,g,g,g,g,g,g,g,g,g,g,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 73
    {_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,g,g,g,g,g,g,g,g,g,g,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 74
    {_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,g,g,g,g,g,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 75
    {_,_,_,_,_,_,_,_,_,_,_,_,_,x,_,x,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,_,x,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 76
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,x,_,_,x,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 77
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 78
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}, // 79
};

// clang-format on
RR_DEFINE_MAZE(ESCAPE, 64) = {
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,g,g,g,g,g,g,g,g,g,g,_,_,m,m,m,m,m,m,m,m,m,m,_,_,X,X,X,X,X,X,X,X,X,X,_,_,a,a,a,a,a,a,a,a,a,a,_,_,o,o,o,o,o,o,o,o,o,o,o,o,_,_},
    {_,_,g,g,g,g,g,g,g,g,g,g,_,_,m,m,m,m,m,m,m,m,m,m,_,_,X,X,X,X,X,X,X,X,X,X,_,_,a,a,a,a,a,a,a,a,a,a,_,_,o,o,o,o,o,o,o,o,o,o,o,o,_,_},
    {_,_,g,g,g,g,g,g,g,g,g,g,_,_,m,m,m,m,m,m,m,m,m,m,_,_,X,X,X,X,X,X,X,X,X,X,_,_,a,a,a,a,a,a,a,a,a,a,_,_,o,o,o,o,o,o,o,o,o,o,o,o,_,_},
    {_,_,g,g,g,g,g,g,g,g,g,g,_,_,m,m,m,m,m,m,m,m,m,m,_,_,X,X,X,X,X,X,X,X,X,X,_,_,a,a,a,a,a,a,a,a,a,a,_,_,o,o,o,o,o,o,o,o,o,o,o,o,_,_},
    {_,_,g,g,g,g,g,g,g,g,g,g,_,_,m,m,m,m,m,m,m,m,m,m,_,_,X,X,X,X,X,X,X,X,X,X,_,_,a,a,a,a,a,a,a,a,a,a,_,_,o,o,o,o,o,o,o,o,o,o,o,o,_,_},
    {_,_,g,g,g,g,g,g,g,g,g,g,_,_,m,m,m,m,m,m,m,m,m,m,_,_,X,X,X,X,X,X,X,X,X,X,_,_,a,a,a,a,a,a,a,a,a,a,_,_,o,o,o,o,o,o,o,o,o,o,o,o,_,_},
    {_,_,g,g,g,g,g,g,g,g,g,g,_,_,m,m,m,m,m,m,m,m,m,m,_,_,X,X,X,X,X,X,X,X,X,X,_,_,a,a,a,a,a,a,a,a,a,a,_,_,o,o,o,o,o,o,o,o,o,o,o,o,_,_},
    {_,_,g,g,g,g,g,g,g,g,g,g,_,_,m,m,m,m,m,m,m,m,m,m,_,_,X,X,X,X,X,X,X,X,X,X,_,_,a,a,a,a,a,a,a,a,a,a,_,_,o,o,o,o,o,o,o,o,o,o,o,o,_,_},
    {_,_,g,g,g,g,g,g,g,g,g,g,_,_,m,m,m,m,m,m,m,m,m,m,_,_,X,X,X,X,X,X,X,X,X,X,_,_,a,a,a,a,a,a,a,a,a,a,_,_,o,o,o,o,o,o,o,o,o,o,o,o,_,_},
    {_,_,g,g,g,g,g,g,g,g,g,g,_,_,m,m,m,m,m,m,m,m,m,m,_,_,X,X,X,X,X,X,X,X,X,X,_,_,a,a,a,a,a,a,a,a,a,a,_,_,o,o,o,o,o,o,o,o,o,o,o,o,_,_},
    {_,_,g,g,g,g,g,g,g,g,g,g,g,g,m,m,m,m,m,m,m,m,m,m,g,g,X,X,X,X,X,X,X,X,X,X,g,g,a,a,a,a,a,a,a,a,a,a,g,g,o,o,o,o,o,o,o,o,o,o,o,o,_,_},
    {_,_,g,g,g,g,g,g,g,g,g,g,g,g,m,m,m,m,m,m,m,m,m,m,g,g,X,X,X,X,X,X,X,X,X,X,g,g,a,a,a,a,a,a,a,a,a,a,g,g,o,o,o,o,o,o,o,o,o,o,o,o,_,_},
    {_,_,g,g,g,g,g,g,g,g,g,g,g,g,m,m,m,m,m,m,m,m,m,m,g,g,X,X,X,X,X,X,X,X,X,X,g,g,a,a,a,a,a,a,a,a,a,a,g,g,o,o,o,o,o,o,o,o,o,o,o,o,_,_},
    {_,_,g,g,g,g,g,g,g,g,g,g,_,_,m,m,m,m,m,m,m,m,m,m,_,_,X,X,X,X,X,X,X,X,X,X,_,_,a,a,a,a,a,a,a,a,a,a,_,_,o,o,o,o,o,o,o,o,o,o,o,o,_,_},
    {_,_,g,g,g,g,g,g,g,g,g,g,_,_,m,m,m,m,m,m,m,m,m,m,_,_,X,X,X,X,X,X,X,X,X,X,_,_,a,a,a,a,a,a,a,a,a,a,_,_,o,o,o,o,o,o,o,o,o,o,o,o,_,_},
    {_,_,g,g,g,g,g,g,g,g,g,g,_,_,m,m,m,m,m,m,m,m,m,m,_,_,X,X,X,X,X,X,X,X,X,X,_,_,a,a,a,a,a,a,a,a,a,a,_,_,o,o,o,o,o,o,o,o,o,o,o,o,_,_},
    {_,_,g,g,g,g,g,g,g,g,g,g,_,_,m,m,m,m,m,m,m,m,m,m,_,_,X,X,X,X,X,X,X,X,X,X,_,_,a,a,a,a,a,a,a,a,a,a,_,_,o,o,o,o,o,o,o,o,o,o,o,o,_,_},
    {_,_,g,g,g,g,g,g,g,g,g,g,_,_,m,m,m,m,m,m,m,m,m,m,_,_,X,X,X,X,X,X,X,X,X,X,_,_,a,a,a,a,a,a,a,a,a,a,_,_,o,o,o,o,o,o,o,o,o,o,o,o,_,_},
    {_,_,g,g,g,g,g,g,g,g,g,g,_,_,m,m,m,m,m,m,m,m,m,m,_,_,X,X,X,X,X,X,X,X,X,X,_,_,a,a,a,a,a,a,a,a,a,a,_,_,o,o,o,o,o,o,o,o,o,o,o,o,_,_},
    {_,_,g,g,g,g,g,g,g,g,g,g,_,_,m,m,m,m,m,m,m,m,m,m,_,_,X,X,X,X,X,X,X,X,X,X,_,_,a,a,a,a,a,a,a,a,a,a,_,_,o,o,o,o,o,o,o,o,o,o,o,o,_,_},
    {_,_,g,g,g,g,g,g,g,g,g,g,_,_,m,m,m,m,m,m,m,m,m,m,_,_,X,X,X,X,X,X,X,X,X,X,_,_,a,a,a,a,a,a,a,a,a,a,_,_,o,o,o,o,o,o,o,o,o,o,o,o,_,_},
    {_,_,g,g,g,g,g,g,g,g,g,g,_,_,m,m,m,m,m,m,m,m,m,m,_,_,X,X,X,X,X,X,X,X,X,X,_,_,a,a,a,a,a,a,a,a,a,a,_,_,o,o,o,o,o,o,o,o,o,o,o,o,_,_},
    {_,_,g,g,g,g,g,g,g,g,g,g,_,_,m,m,m,m,m,m,m,m,m,m,_,_,X,X,X,X,X,X,X,X,X,X,_,_,a,a,a,a,a,a,a,a,a,a,_,_,o,o,o,o,o,o,o,o,o,o,o,o,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_}
};
RR_DEFINE_MAZE(BURROW, 4) = {{1, 1}, {0,1,1,1,1,1,1,1,1,1}};

#define MAZE_ENTRY(MAZE, GRID_SIZE)                                            \
    (sizeof(RR_MAZE_##MAZE[0]) / sizeof(struct rr_maze_grid)), GRID_SIZE,      \
        &RR_MAZE_##MAZE[0][0]


RR_DEFINE_MAZE(NETHER, 160) = {
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,c,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,r,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,_,_,_,_,_,_,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,_,_,_,_,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,C,C,_,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,C,C,C,C,C,C,C,C,C,C,C,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,C,C,C,C,C,C,C,C,C,C,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,C,C,C,C,C,C,C,C,C,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,_,_,_,_,_,_,_,_,_,_,_,_,e,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,C,C,C,C,C,C,C,C,C,C,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,_,_,_,_,_,_,_,_,_,e,e,e,e,e,e,e,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,C,C,C,C,C,C,C,C,C,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,R,R,_,_,_,_,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,C,C,C,C,C,C,C,C,C,C,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,R,R,R,R,R,R,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,C,C,C,C,C,C,C,C,C,C,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,R,R,R,R,R,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,_,_,_,_,_,_,_,_,_,_,C,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,R,R,R,R,R,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,_,_,_,_,_,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,R,R,R,R,R,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,_,_,_,_,_,_,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,R,R,R,R,R,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,E,E,_,_,_,_,_,_,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,R,R,R,R,R,R,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,E,c,E,E,E,E,E,E,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,R,R,R,R,R,R,R,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,E,E,E,E,E,E,E,E,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,L,L,_,_,_,R,R,R,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,E,E,E,E,E,E,E,E,E,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,L,r,L,L,L,L,L,L,L,_,_,_,_,_,R,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,E,E,E,E,E,E,E,E,E,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,L,L,L,L,L,L,L,L,L,_,_,_,_,_,_,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,E,E,E,E,E,E,E,E,E,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,L,L,L,L,L,L,L,L,L,_,_,_,_,_,_,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,E,E,E,E,E,E,E,E,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,L,L,L,L,L,L,L,L,L,_,_,_,_,_,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,E,E,E,E,E,E,E,E,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,L,L,L,L,L,L,L,L,L,_,_,_,_,_,_,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,E,E,E,E,E,E,E,E,E,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,L,L,L,L,L,L,L,L,L,_,_,_,_,_,_,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,E,E,E,E,E,E,E,E,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,L,L,L,L,L,L,L,L,L,_,_,_,_,_,_,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,E,E,E,E,E,E,E,E,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,L,L,L,L,L,L,L,L,L,_,_,_,_,_,_,_,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,E,E,E,E,E,E,E,E,E,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,L,L,L,L,L,L,L,L,L,_,_,_,_,_,_,_,_,_,e,e,e,e,e,e,e,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,E,E,E,E,E,E,E,E,E,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,L,L,L,L,L,L,L,L,L,_,_,_,_,_,_,_,_,_,_,_,e,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,E,E,E,E,E,E,E,E,E,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,L,L,L,L,L,L,L,L,L,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,E,E,E,E,E,E,l,E,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,L,L,L,L,L,L,L,L,L,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,E,E,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,L,L,L,L,L,L,L,L,L,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,L,L,L,L,L,L,L,m,L,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,L,L,L,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,M,M,M,M,M,M,M,M,M,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,M,M,M,M,M,M,M,M,M,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,M,M,M,M,M,M,M,M,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,M,M,M,M,M,M,M,M,M,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,M,M,M,M,M,M,M,M,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,M,M,M,M,M,M,M,M,M,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,M,M,M,M,M,M,M,M,M,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,a,a,l,a,a,a,a,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,A,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,a,a,a,a,a,a,a,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,A,A,A,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,a,a,a,a,x,a,a,a,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,A,m,A,A,A,A,A,U,A,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,U,U,U,U,U,U,U,U,U,U,U,U,U,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_,_,_,_,_,_,_,_,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,u,u,u,u,u,u,u,u,u,u,u,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,u,u,u,u,u,u,u,u,u,u,u,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,u,u,u,u,u,u,u,u,u,u,u,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,u,u,u,u,u,u,u,u,u,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,u,u,u,u,u,u,u,u,u,u,u,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,u,u,u,u,u,u,u,u,u,u,u,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,u,u,u,u,u,u,u,u,u,u,u,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_,_,_,_,_,_,_,_,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,U,U,U,U,U,U,U,U,U,U,U,U,U,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,x,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,U,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
};
RR_DEFINE_MAZE(OCEAN, 160) = {
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,c,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,C,C,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,R,R,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,r,_,_,_,_,_,_,C,C,C,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,R,R,R,_,_,_,_,_,_,e,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,C,C,C,C,C,C,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,R,R,R,R,R,R,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,C,C,C,C,C,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,R,R,R,R,R,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,C,C,C,C,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,R,R,R,R,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,C,C,C,C,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,R,R,R,R,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,C,C,C,C,C,C,c,c,c,c,c,c,c,c,c,c,c,R,R,R,R,R,R,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,C,C,C,C,C,C,C,C,_,_,_,c,_,_,_,R,R,R,R,R,R,R,R,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,C,C,C,C,C,C,_,_,_,_,_,_,_,_,_,R,R,R,R,R,R,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,C,C,C,C,_,_,_,_,_,_,_,_,_,_,_,_,_,R,R,R,R,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,C,C,C,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,R,R,R,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,C,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,R,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_},
    {_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_},
    {_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,E,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,L,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,E,E,E,_,_,_,_,_,_,_,l,_,_,_,_,_,_,_,L,L,L,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,E,E,E,E,_,l,l,l,l,l,l,l,l,l,l,l,_,L,L,L,L,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,E,E,E,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,L,L,L,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,E,E,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,L,L,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,E,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,L,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,E,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,L,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,E,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,L,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,E,E,E,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,L,L,L,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,E,E,E,E,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,L,L,L,L,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,r,_,_,_,_,_,_,E,E,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,L,L,_,_,_,_,_,_,e,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,E,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,L,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,M,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,a,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,M,M,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,a,a,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,m,_,_,_,_,M,M,M,M,M,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,a,a,a,a,a,_,_,_,_,x,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,M,M,M,M,M,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,a,a,a,a,a,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,M,M,M,M,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,a,a,a,a,x,x,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,M,M,M,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,a,a,a,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,M,M,M,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,a,a,a,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,M,M,M,M,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,a,a,a,a,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,M,M,M,M,M,M,l,l,l,l,l,l,l,l,l,l,l,a,a,a,a,a,a,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,M,M,M,M,_,_,_,_,_,_,l,_,_,_,_,_,_,a,a,a,a,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,M,M,M,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,a,a,a,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,M,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,a,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_},
    {_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,A,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,u,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_},
    {_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,A,A,A,A,A,_,_,_,_,_,_,_,_,_,_,_,u,u,u,u,u,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,A,A,A,A,A,A,A,_,_,_,U,_,_,_,u,u,u,u,u,u,u,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,A,A,A,A,U,U,U,U,U,U,U,U,U,U,U,U,U,u,u,u,u,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,A,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,u,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,A,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,u,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,A,A,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,u,u,x,x,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,_,_,_,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,_,_,_,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,m,_,_,_,_,_,_,_,_,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,_,_,_,_,_,_,_,_,x,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,U,U,U,U,U,U,U,U,U,U,U,U,U,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,U,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
};
RR_DEFINE_MAZE(PLAINS, 160) = {
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,c,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,r,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,_,_,_,_,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,_,_,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,C,C,C,C,C,C,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,C,C,C,C,C,C,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,C,C,C,C,C,C,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,C,C,C,C,C,C,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,C,C,C,C,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,C,C,C,C,C,C,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,C,C,C,C,C,C,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,R,R,_,_,_,_,_,_,e,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,C,C,C,C,C,C,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,R,R,R,_,_,e,e,e,e,e,e,e,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,C,C,C,C,C,C,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,R,R,R,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,R,R,R,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,R,R,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,_,_,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,R,R,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,_,_,_,_,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,R,R,R,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,c,c,c,c,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,r,r,r,r,R,R,R,R,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,c,c,c,c,c,c,c,c,c,E,E,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,r,r,r,r,r,r,r,r,r,L,R,R,R,R,R,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,E,E,E,c,E,E,E,E,E,E,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,L,L,L,r,L,L,L,L,L,R,R,R,R,R,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,E,E,E,E,E,E,E,E,E,E,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,L,L,L,L,L,L,L,L,L,L,R,R,R,R,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,E,E,E,E,E,E,E,E,E,E,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,L,L,L,L,L,L,L,L,L,L,_,_,R,R,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,E,E,E,E,E,E,E,E,E,E,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,L,L,L,L,L,L,L,L,L,L,_,_,_,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,E,E,E,E,E,E,E,E,E,E,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,L,L,L,L,L,L,L,L,L,L,_,_,_,_,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,E,E,E,E,E,E,E,E,E,E,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,L,L,L,L,L,L,L,L,L,L,_,_,_,_,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,E,E,E,E,E,E,l,E,E,E,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,L,L,L,L,L,L,L,L,L,L,_,_,_,_,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,E,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,L,L,L,L,L,L,m,L,L,L,_,_,_,_,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,_,_,_,_,_,_,_,_,L,m,m,m,m,m,m,m,m,m,m,m,_,_,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,e,e,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,e,e,e,e,e,e,e,e,e,e,e,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,M,M,M,M,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,e,e,e,e,e,e,e,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,M,M,M,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,e,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,M,M,M,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,M,M,M,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,M,M,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,M,M,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,M,M,M,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,M,M,M,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,M,M,M,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,M,M,M,M,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,A,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,l,l,l,l,l,l,l,l,l,l,l,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,A,A,A,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,a,a,a,l,a,a,a,a,a,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,m,m,m,m,m,m,m,m,m,m,m,A,A,U,A,A,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,a,a,a,a,a,a,a,a,a,a,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,A,m,A,U,U,U,U,U,U,U,U,U,U,U,U,U,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,a,a,a,a,a,x,a,a,a,a,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,_,_,_,u,u,u,u,u,u,u,u,u,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,u,u,u,u,u,u,u,u,u,u,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,u,u,u,u,u,u,u,u,u,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,u,u,u,u,u,u,u,u,u,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,u,u,u,u,u,u,u,u,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,u,u,u,u,u,u,u,u,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,u,u,u,u,u,u,u,u,u,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,u,u,u,u,u,u,u,u,u,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,u,u,u,u,u,u,u,u,u,u,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,u,u,u,u,u,u,u,u,u,u,_,_,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_,_,_,_,_,_,_,_,_,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,x,x,x,x,x,x,x,x,x,x,x,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,U,U,U,U,U,U,U,U,U,U,U,U,U,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,x,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,U,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_},
};

struct rr_maze_declaration RR_MAZES[rr_biome_id_max] = {
    {MAZE_ENTRY(HELL_CREEK, 2048), 7, {
        {12, 12, 4, 4, 14, 14, 1},   // Зал 1 (старт)
        {40, 13, 4, 4, 42, 15, 15},  // Зал 2
        {63, 20, 4, 4, 65, 22, 30},  // Зал 3
        {18, 44, 4, 4, 20, 46, 45},  // Зал 4
        {48, 46, 4, 4, 50, 48, 60},  // Зал 5
        {20, 66, 4, 4, 22, 68, 75},  // Зал 6
        {56, 65, 4, 4, 58, 67, 90},  // Зал 7 (Ultra)
    }},
    {MAZE_ENTRY(PVP, 2048), 7, {
        {38, 10, 4, 4, 40, 12, 1},   // Вход в Ant Hell
        {14, 24, 4, 4, 16, 26, 15},  // Левая камера
        {62, 24, 4, 4, 64, 26, 30},  // Правая камера
        {38, 38, 4, 4, 40, 40, 45},  // Центр
        {14, 56, 4, 4, 16, 58, 60},  // Термиты
        {62, 56, 4, 4, 64, 58, 75},  // Солдаты
        {38, 66, 4, 4, 40, 68, 90},  // Зал королевы / червей
    }},

    {MAZE_ENTRY(ESCAPE, 2048), 5, {
        {6, 30, 3, 3, 7, 31, 1},    // Комната 1 (Старт и 3 Кристалла)
        {18, 30, 3, 3, 19, 31, 10}, // Комната 2 (Иллюзорный лабиринт)
        {30, 30, 3, 3, 31, 31, 20}, // Комната 3 (Нажимная плита)
        {42, 30, 3, 3, 43, 31, 35}, // Комната 4 (3 Древних Тотема)
        {54, 30, 3, 3, 55, 31, 50}, // Комната 5 (Финал и Сокровищница)
    }},
    {MAZE_ENTRY(BURROW, 512), 0},
    {MAZE_ENTRY(NETHER, 2048), 7, {{12,12,4,4,14,14,1},{40,14,4,4,42,16,15},{62,22,4,4,64,24,30},{20,44,4,4,22,46,45},{50,46,4,4,52,48,60},{22,64,4,4,24,66,75},{56,64,4,4,58,66,90}}},
    {MAZE_ENTRY(OCEAN, 2048), 7, {{38,12,4,4,40,14,1},{16,26,4,4,18,28,15},{60,26,4,4,62,28,30},{38,40,4,4,40,42,45},{16,56,4,4,18,58,60},{60,56,4,4,62,58,75},{38,66,4,4,40,68,90}}},
    {MAZE_ENTRY(PLAINS, 2048), 7, {{14,14,4,4,16,16,1},{43,14,4,4,45,16,15},{63,28,4,4,65,30,30},{18,43,4,4,20,45,45},{46,44,4,4,48,46,60},{20,65,4,4,22,67,75},{54,64,4,4,56,66,90}}},
};

struct rr_biome_server RR_BIOME_SERVERS[rr_biome_id_max] = {{"default",1234,"hc"},{"pvp",1235,"ant"},{NULL,0,NULL},{NULL,0,NULL},{"nether",1236,"neth"},{"ocean",1237,"ocn"},{"plains",1238,"pln"}};

uint8_t RR_GLOBAL_BIOME = rr_biome_id_hell_creek;

#undef _
#undef c
#undef C
#undef u
#undef U
#undef r
#undef R
#undef e
#undef E
#undef l
#undef L
#undef m
#undef M
#undef x
#undef X
#undef a
#undef A
