import re

with open("Server/System/Health.c", "r", encoding="utf-8") as f:
    code = f.read()

pattern = re.compile(
    r'(\n([ \t]*)else if \(petal->id == rr_petal_id_beak\)\s*\{.*?\n\2\})',
    re.DOTALL
)

m = pattern.search(code)
assert m, "Не найден блок rr_petal_id_beak в Server/System/Health.c"

indent = m.group(2)
extra = f"""
{indent}else if (petal->id == rr_petal_id_triangle)
{indent}{{
{indent}    struct rr_component_health *health =
{indent}        rr_simulation_get_health(simulation, attacker);
{indent}    struct rr_component_relations *relations =
{indent}        rr_simulation_get_relations(simulation, attacker);
{indent}    if (rr_simulation_has_player_info(simulation, relations->owner))
{indent}    {{
{indent}        struct rr_component_player_info *pinfo =
{indent}            rr_simulation_get_player_info(simulation, relations->owner);
{indent}        uint32_t tri_count = 0;
{indent}        for (uint64_t i = 0; i < pinfo->slot_count; ++i)
{indent}        {{
{indent}            if (pinfo->slots[i].id == rr_petal_id_triangle)
{indent}                ++tri_count;
{indent}        }}
{indent}        if (tri_count < 1)
{indent}            tri_count = 1;
{indent}        float mult = 1.0f + 0.25f * (float)(tri_count - 1);
{indent}        float base_dmg =
{indent}            RR_PETAL_DATA[petal->id].damage *
{indent}            RR_PETAL_DATA[petal->id].scale[petal->rarity].damage /
{indent}            RR_PETAL_DATA[petal->id].count[petal->rarity];
{indent}        health->damage = base_dmg * mult;
{indent}    }}
{indent}}}"""

if "rr_petal_id_triangle" not in code:
    code = code[:m.end()] + extra + code[m.end():]
    with open("Server/System/Health.c", "w", encoding="utf-8") as f:
        f.write(code)
    print("Уникальная механика Triangle успешно добавлена!")
else:
    print("Механика Triangle уже присутствует.")
