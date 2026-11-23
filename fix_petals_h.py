import re
with open("Shared/StaticData.h", "r") as f: h = f.read()
if "rr_petal_id_claw" not in h:
    p = "    rr_petal_id_yggdrasil,      // 42\n" + "".join(
        f"    rr_petal_id_{n},\n" for n in ["claw","fang","tooth","horn","thagomizer","scythe","magma","obsidian","plate","scale","amber","branch","pearl","tail","frill","venom","sail","ash","crown","relic"]
    ) + "    rr_petal_id_max,"
    h = re.sub(r'    rr_petal_id_yggdrasil,\s*//\s*42\s*\n+\s*rr_petal_id_max,\s*//\s*43', p, h, count=1)
    with open("Shared/StaticData.h", "w") as f: f.write(h)
print("Petals in StaticData.h fixed!")
