import re
with open("Shared/StaticData.h", "r") as f: h = f.read()
if "rr_mob_id_compsognathus" not in h:
    m = "    rr_mob_id_queen_termite,    // 35\n" + "".join(
        f"    rr_mob_id_{n},\n" for n in ["compsognathus","stegosaurus","dilophosaurus","spinosaurus","carnotaurus","brachiosaurus","therizinosaurus","mosasaurus","volcano","titanoboa"]
    ) + "    rr_mob_id_max,"
    h = re.sub(r'    rr_mob_id_queen_termite,\s*//\s*35\s*\n+\s*rr_mob_id_max,\s*//\s*36', m, h, count=1)
    with open("Shared/StaticData.h", "w") as f: f.write(h)
print("StaticData.h fixed!")
