import re

with open("Server/Waves.c", "r") as f: w = f.read()

new_hc = """    if (biome == rr_biome_id_hell_creek)
    {
        float diff = zone ? zone->difficulty : 1.0f;
        double r = rr_frand();
        if (diff <= 18.0f) {
            if (r < 0.24) return rr_mob_id_compsognathus;
            if (r < 0.46) return rr_mob_id_stegosaurus;
            if (r < 0.65) return rr_mob_id_triceratops;
            if (r < 0.84) return rr_mob_id_dilophosaurus;
            return rr_mob_id_fern;
        } else if (diff <= 38.0f) {
            if (r < 0.24) return rr_mob_id_spinosaurus;
            if (r < 0.46) return rr_mob_id_carnotaurus;
            if (r < 0.68) return rr_mob_id_brachiosaurus;
            if (r < 0.86) return rr_mob_id_dakotaraptor;
            return rr_mob_id_pteranodon;
        } else if (diff <= 56.0f) {
            if (r < 0.28) return rr_mob_id_therizinosaurus;
            if (r < 0.56) return rr_mob_id_mosasaurus;
            if (r < 0.80) return rr_mob_id_quetzalcoatlus;
            return rr_mob_id_trex;
        } else {
            if (r < 0.30) return rr_mob_id_titanoboa;
            if (r < 0.58) return rr_mob_id_volcano;
            if (r < 0.82) return rr_mob_id_trex;
            return rr_mob_id_meteor;
        }
    }"""

w = re.sub(r'    if \(biome == rr_biome_id_hell_creek\)\s*\{.*?\n    \}', new_hc, w, count=1, flags=re.DOTALL)
with open("Server/Waves.c", "w") as f: f.write(w)
print("s2_waves OK")
