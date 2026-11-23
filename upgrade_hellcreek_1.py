with open("Server/Waves.c", "r", encoding="utf-8") as f:
    waves = f.read()

old_hc = """    double r = rr_frand();
    if (r < 0.25)
        return rr_mob_id_fat_bee;
    if (r < 0.50)
        return rr_mob_id_ladybug;
    if (r < 0.75)
        return rr_mob_id_rock;
    if (r < 0.85)
        return rr_mob_id_dragonfly;"""

new_hc = """    if (biome == rr_biome_id_hell_creek)
    {
        float diff = zone ? zone->difficulty : 1.0f;
        double r = rr_frand();
        if (diff <= 24.0f)
        {
            if (r < 0.22) return rr_mob_id_triceratops;
            if (r < 0.42) return rr_mob_id_ornithomimus;
            if (r < 0.60) return rr_mob_id_pachycephalosaurus;
            if (r < 0.76) return rr_mob_id_edmontosaurus;
            if (r < 0.90) return rr_mob_id_ankylosaurus;
            return rr_mob_id_fern;
        }
        else if (diff <= 48.0f)
        {
            if (r < 0.32) return rr_mob_id_dakotaraptor;
            if (r < 0.58) return rr_mob_id_pteranodon;
            if (r < 0.80) return rr_mob_id_quetzalcoatlus;
            if (r < 0.93) return rr_mob_id_ankylosaurus;
            return rr_mob_id_trex;
        }
        else
        {
            if (r < 0.45) return rr_mob_id_trex;
            if (r < 0.78) return rr_mob_id_meteor;
            if (r < 0.92) return rr_mob_id_dakotaraptor;
            return rr_mob_id_tree;
        }
    }"""

assert old_hc in waves, "Не найден старый блок спавна в Server/Waves.c"
waves = waves.replace(old_hc, new_hc, 1)
with open("Server/Waves.c", "w", encoding="utf-8") as f:
    f.write(waves)

with open("Shared/StaticData.c", "r", encoding="utf-8") as f:
    sd = f.read()

sd = sd.replace(
    "{{rr_petal_id_stinger, 0.03},{rr_petal_id_egg, 0.05},{rr_petal_id_meat, 0.01}}",
    "{{rr_petal_id_stinger, 0.35},{rr_petal_id_egg, 0.30},{rr_petal_id_meat, 0.35},{rr_petal_id_yggdrasil, 0.25}}"
)
sd = sd.replace(
    "{{rr_petal_id_leaf, 0.15},{rr_petal_id_fossil, 0.05}}",
    "{{rr_petal_id_leaf, 0.35},{rr_petal_id_fossil, 0.25}}"
)
sd = sd.replace(
    "{{rr_petal_id_beak, 0.05},{rr_petal_id_fossil, 0.1},{rr_petal_id_lightning, 0.01}}",
    "{{rr_petal_id_beak, 0.30},{rr_petal_id_fossil, 0.30},{rr_petal_id_lightning, 0.15}}"
)
with open("Shared/StaticData.c", "w", encoding="utf-8") as f:
    f.write(sd)

print("Шаг 1 (динозавры по зонам и лут Hell Creek) готов!")
