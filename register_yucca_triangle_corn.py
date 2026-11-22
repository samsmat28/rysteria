import re

# 1. Shared/StaticData.h: регистрируем Yucca, Triangle, Corn в enum rr_petal_id
with open("Shared/StaticData.h", "r") as f:
    h = f.read()

if "rr_petal_id_yucca" not in h:
    h = re.sub(
        r"(rr_petal_id_light\s*,[^\n]*\n)\s*rr_petal_id_max\s*,[^\n]*",
        r"""\1    rr_petal_id_yucca,               // 39
    rr_petal_id_triangle,            // 40
    rr_petal_id_corn,                // 41

    rr_petal_id_max,                 // 42""",
        h,
        count=1
    )
    with open("Shared/StaticData.h", "w") as f:
        f.write(h)

# 2. Shared/StaticData.c: статы и имена для Yucca, Triangle, Corn
with open("Shared/StaticData.c", "r") as f:
    c = f.read()

if "rr_petal_id_yucca," not in c.split("RR_MOB_DATA")[0]:
    c = re.sub(
        r'(\{rr_petal_id_light\b.*?\},\s*\n)(\};)',
        r"""\1    {rr_petal_id_yucca,              rr_rarity_id_common,    defensive,  6.0f,  15.0f,  8.0f,  45,  0, {1,1,1,1,1,1,1}},
    {rr_petal_id_triangle,           rr_rarity_id_unusual,   offensive, 14.0f,   6.0f,  0.0f,  30,  0, {1,1,1,1,1,1,1}},
    {rr_petal_id_corn,               rr_rarity_id_common,    offensive, 12.0f,  65.0f,  0.0f,  35,  0, {1,1,1,1,1,1,1}},
\2""",
        c,
        count=1
    )
    c = c.replace('"Light"\n};', '"Light", "Yucca", "Triangle", "Corn"\n};', 1)
    with open("Shared/StaticData.c", "w") as f:
        f.write(c)

print("Yucca, Triangle и Corn зарегистрированы в StaticData!")
