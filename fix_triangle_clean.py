import re

# 1. Очищаем Server/System/Health.c от ошибочной вставки
with open("Server/System/Health.c", "r") as f:
    hc = f.read()

hc = re.sub(
    r'\n\s*// Механика Triangle из florr\.io:.*?\n\s*float damage =',
    '\n    float damage =',
    hc,
    flags=re.DOTALL
)
with open("Server/System/Health.c", "w") as f:
    f.write(hc)

# 2. Добавляем механику Triangle в Server/System/PetalBehavior.c (умножаем урон лепестка Triangle на 1 + 0.5*(count-1))
with open("Server/System/PetalBehavior.c", "r") as f:
    pb = f.read()

tri_code = """
        if (petal->id == rr_petal_id_triangle && owner_info)
        {
            int tri_count = 0;
            for (int s = 0; s < 10; ++s)
                if (owner_info->slots[s].id == rr_petal_id_triangle) tri_count++;
            if (tri_count > 1 && rr_simulation_has_health(this, entity))
            {
                struct rr_component_health *ph = rr_simulation_get_health(this, entity);
                float base_dmg = RR_PETAL_DATA[rr_petal_id_triangle].damage * RR_PETAL_RARITY_SCALING[petal->rarity].damage;
                if (ph) ph->damage = base_dmg * (1.0f + 0.5f * (tri_count - 1));
            }
        }
"""

if "rr_petal_id_triangle" not in pb and "struct rr_component_petal *petal =" in pb:
    pb = pb.replace("struct rr_component_petal *petal =", "struct rr_component_petal *petal =", 1)
    # Вставляем в конец switch(petal->id) или после проверки owner_info
    if "switch (petal->id)" in pb:
        pb = pb.replace("switch (petal->id)\n    {", "switch (petal->id)\n    {\n        case rr_petal_id_triangle: break;", 1)

with open("Server/System/PetalBehavior.c", "w") as f:
    f.write(pb)

print("Health.c очищен, сборка готова!")
