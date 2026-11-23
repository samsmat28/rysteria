import re

# 1. Shared/StaticData.h: добавляем Omega, Hyper, Gods в enum rr_rarity_id
with open("Shared/StaticData.h", "r") as f:
    h = f.read()

if "rr_rarity_id_omega" not in h:
    h = h.replace(
        "    rr_rarity_id_ultimate,\n    rr_rarity_id_max\n};",
        "    rr_rarity_id_ultimate,\n    rr_rarity_id_omega,\n    rr_rarity_id_hyper,\n    rr_rarity_id_gods,\n    rr_rarity_id_max\n};",
        1
    )
    with open("Shared/StaticData.h", "w") as f:
        f.write(h)

# 2. Shared/StaticData.c: обновляем все массивы редкостей, капы редкости мобов и лут термитов
with open("Shared/StaticData.c", "r") as f:
    c = f.read()

if '"Omega"' not in c:
    # offensive
    c = c.replace(
        "    {42.0,432}\n};",
        "    {42.0,432},\n    {72.0, 1296},\n    {125.0, 3888},\n    {220.0, 11664}\n};",
        1
    )
    # defensive
    c = c.replace(
        "    {432,42.0}\n};",
        "    {432,42.0},\n    {1296, 72.0},\n    {3888, 125.0},\n    {11664, 220.0}\n};",
        1
    )
    # Расширяем списки количества лепестков {1,1,1,1,1,1,1} -> 10 элементов (для rarities 1..10)
    def pad_counts(m):
        nums = [x.strip() for x in m.group(1).split(",")]
        while len(nums) < 10:
            nums.append(nums[-1])
        return "{" + ",".join(nums) + "}}"
    c = re.sub(r'\{([0-9,\s]+)\}\}', pad_counts, c)

    # RR_PETAL_RARITY_SCALE
    c = c.replace(
        "    {180,  0.5, 250},\n};",
        "    {180,  0.5, 250},\n    {540,  0.2, 310},\n    {1620, 0.1, 380},\n    {4860, 0.05, 460},\n};",
        1
    )
    # RR_MOB_RARITY_SCALING
    c = c.replace(
        "    {500000,   200,   30  },\n};",
        "    {500000,   200,   30  },\n    {2500000,  500,   42  },\n    {12000000, 1250,  56  },\n    {60000000, 3200,  72  },\n};",
        1
    )
    # RR_RARITY_COLORS: Omega (фиолетовый 0xff9b30ff), Hyper (серый 0xff8e99a4), Gods (белый 0xffffffff)
    c = c.replace(
        "0xffff2b75, 0xff2bffa3};",
        "0xffff2b75, 0xff2bffa3, 0xff9b30ff, 0xff8e99a4, 0xffffffff};",
        1
    )
    # RR_RARITY_NAMES
    c = c.replace(
        '"Legendary", "Mythic", "Exotic", "Ancient"};',
        '"Legendary", "Mythic", "Exotic", "Ancient", "Omega", "Hyper", "Gods"};',
        1
    )
    # RR_PVP_POINTS_PER_RARITY
    c = c.replace(
        "45000000, 900000000};",
        "45000000, 900000000, 5000000000ULL, 25000000000ULL, 100000000000ULL};",
        1
    )
    # RR_MOB_WAVE_RARITY_COEFFICIENTS
    c = c.replace(
        "0, 1, 6, 10, 15, 25, 160, 1200, 250};",
        "0, 1, 6, 10, 15, 25, 160, 1200, 250, 180, 140, 100};",
        1
    )
    # RR_DROP_RARITY_COEFFICIENTS
    c = c.replace(
        "0, 1, 8, 15, 40, 150, 500, 2500};",
        "0, 1, 8, 15, 40, 150, 500, 2500, 12000, 60000, 300000};",
        1
    )
    # RR_MOB_LOOT_RARITY_COEFFICIENTS
    c = c.replace(
        "35,  50, 125, 150};",
        "35,  50, 125, 150, 200, 260, 350};",
        1
    )
    # RR_BASE_CRAFT_CHANCES (10 элементов)
    c = c.replace(
        "0.03, 0.02, 0.015};",
        "0.03, 0.02, 0.015, 0.01, 0.007, 0.005};",
        1
    )

# Поднимаем максимальную редкость всех мобов до rr_rarity_id_gods
c = c.replace("rr_rarity_id_ultimate,", "rr_rarity_id_gods,")
c = c.replace("rarity_cap > rr_rarity_id_ultimate", "rarity_cap > rr_rarity_id_gods")
c = c.replace("rarity_cap = rr_rarity_id_ultimate;", "rarity_cap = rr_rarity_id_gods;")

# Тематический лут термитов: Bone (броня), Mandible (челюсти), Sand (песок) и Egg
c = re.sub(
    r'\{rr_mob_id_termite_worker,.*?\n',
    '    {rr_mob_id_termite_worker,   rr_rarity_id_common, rr_rarity_id_gods, 28, 12, 27.0f, rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_bone, 0.30},{rr_petal_id_sand, 0.25},{rr_petal_id_pellet, 0.15}}},\n',
    c
)
c = re.sub(
    r'\{rr_mob_id_termite_soldier,.*?\n',
    '    {rr_mob_id_termite_soldier,  rr_rarity_id_common, rr_rarity_id_gods, 50, 20, 32.0f, rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_bone, 0.35},{rr_petal_id_mandible, 0.30},{rr_petal_id_sand, 0.20},{rr_petal_id_egg, 0.12}}},\n',
    c
)
c = re.sub(
    r'\{rr_mob_id_termite_egg,.*?\n',
    '    {rr_mob_id_termite_egg,      rr_rarity_id_common, rr_rarity_id_gods, 22,  0, 25.0f, rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_egg, 0.35},{rr_petal_id_bone, 0.25},{rr_petal_id_sand, 0.20}}},\n',
    c
)
c = re.sub(
    r'\{rr_mob_id_queen_termite,.*?\n',
    '    {rr_mob_id_queen_termite,    rr_rarity_id_common, rr_rarity_id_gods, 4000, 40, 185.0f, rr_rarity_id_common, rr_rarity_id_common, rr_rarity_id_max, {{rr_petal_id_bone, 0.70},{rr_petal_id_mandible, 0.70},{rr_petal_id_egg, 0.85}}},\n',
    c
)

with open("Shared/StaticData.c", "w") as f:
    f.write(c)

# 3. Server/Waves.c: разрешаем спавн мобов до редкости rr_rarity_id_gods
with open("Server/Waves.c", "r") as f:
    w = f.read()
w = w.replace("rr_rarity_id_ultimate", "rr_rarity_id_gods")
with open("Server/Waves.c", "w") as f:
    f.write(w)

# 4. Client/Renderer/RenderArena.c: добавляем ещё больше деталей и узоров на пол Ant Hell
with open("Client/Renderer/RenderArena.c", "r") as f:
    ra = f.read()

extra_floor = """            // Тонкие трещинки в грунте (на каждом втором тайле)
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
            }"""

old_crack = re.search(r'            // Тонкие трещинки в грунте.*?rr_renderer_stroke\(renderer\);\s*\}', ra, flags=re.DOTALL)
if old_crack:
    ra = ra[:old_crack.start()] + extra_floor + ra[old_crack.end():]
    with open("Client/Renderer/RenderArena.c", "w") as f:
        f.write(ra)

print("Готово: Omega (фиолетовый), Hyper (серый), Gods (белый), лут термитов и богатый узор пола!")
