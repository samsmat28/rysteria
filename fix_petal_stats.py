import re

with open("Shared/StaticData.c", "r", encoding="utf-8") as f:
    c = f.read()

pattern = re.compile(r'(\{rr_petal_id_corn,[^\n]+\}\s*,\s*\n\};)')
m = pattern.search(c)
assert m, "Не найден блок corn в Shared/StaticData.c"

p_rows = [
    ("yggdrasil","defensive",8,10,0,60,1),
    ("claw","offensive",14,18,0,25,1),("fang","offensive",16,22,0,30,1),("tooth","offensive",15,26,0,32,1),
    ("horn","offensive",18,24,0,35,1),("thagomizer","offensive",11,15,0,30,4),("scythe","offensive",22,32,0,40,1),
    ("magma","offensive",20,28,0,38,1),("obsidian","offensive",35,45,0,55,1),("plate","defensive",28,8,0,40,1),
    ("scale","defensive",22,12,0,35,2),("amber","defensive",18,8,8,45,1),("branch","defensive",16,10,6,35,1),
    ("pearl","defensive",14,6,10,40,1),("tail","defensive",12,10,0,25,1),("frill","defensive",16,11,0,30,1),
    ("venom","offensive",10,24,0,32,2),("sail","defensive",15,9,0,30,1),("ash","defensive",12,14,0,28,3),
    ("crown","defensive",30,25,12,50,1),("relic","offensive",32,38,8,48,1)
]

added = "".join(
    f"    {{rr_petal_id_{n}, rr_rarity_id_common, {t}, {hp}.0f, {dmg}.0f, {hl}.0f, {rl}, 0, {{{','.join([str(cnt)]*11)}}}}},\n"
    for n, t, hp, dmg, hl, rl, cnt in p_rows
)

new_block = m.group(1).replace("};", added + "};")
c = c[:m.start()] + new_block + c[m.end():]

with open("Shared/StaticData.c", "w", encoding="utf-8") as f:
    f.write(c)
print("Характеристики всех 20 новых лепестков и Yggdrasil записаны!")
