import re

def make_grid(rooms, corridors):
    W, H = 80, 80
    g = [['_' for _ in range(W)] for _ in range(H)]
    for (x1, y1), (x2, y2), rad, ch in corridors:
        steps = max(abs(x2 - x1), abs(y2 - y1), 1)
        for s in range(steps + 1):
            cx = int(round(x1 + (x2 - x1) * s / steps))
            cy = int(round(y1 + (y2 - y1) * s / steps))
            for dy in range(-rad, rad + 1):
                for dx in range(-rad, rad + 1):
                    nx, ny = cx + dx, cy + dy
                    if 2 <= nx < W - 2 and 2 <= ny < H - 2:
                        g[ny][nx] = ch
    for cx, cy, rx, ry, ch in rooms:
        for dy in range(-ry, ry + 1):
            for dx in range(-rx, rx + 1):
                if (dx * dx) / float(rx * rx) + (dy * dy) / float(ry * ry) <= 1.0:
                    nx, ny = cx + dx, cy + dy
                    if 2 <= nx < W - 2 and 2 <= ny < H - 2:
                        g[ny][nx] = ch
    return "\n".join("    {" + ",".join(row) + "}," for row in g)

nether_grid = make_grid(
    [(14,14,9,9,'c'),(42,16,10,9,'r'),(64,24,9,10,'e'),(22,46,11,10,'l'),(52,48,11,10,'m'),(24,66,11,8,'x'),(58,66,13,8,'U')],
    [((14,14),(42,16),3,'C'),((42,16),(64,24),3,'R'),((14,14),(22,46),3,'E'),((42,16),(52,48),3,'L'),((22,46),(52,48),3,'M'),((22,46),(24,66),3,'a'),((52,48),(58,66),3,'A'),((24,66),(58,66),3,'u')]
)
ocean_grid = make_grid(
    [(40,14,13,9,'c'),(18,28,12,11,'r'),(62,28,12,11,'e'),(40,42,14,12,'l'),(18,58,12,11,'m'),(62,58,12,11,'x'),(40,68,14,8,'U')],
    [((40,14),(18,28),4,'C'),((40,14),(62,28),4,'R'),((18,28),(40,42),4,'E'),((62,28),(40,42),4,'L'),((40,42),(18,58),4,'M'),((40,42),(62,58),4,'a'),((18,58),(40,68),4,'A'),((62,58),(40,68),4,'u')]
)
plains_grid = make_grid(
    [(16,16,12,11,'c'),(45,16,12,11,'r'),(65,30,10,12,'e'),(20,45,13,12,'l'),(48,46,13,12,'m'),(22,67,12,8,'x'),(56,66,14,9,'U')],
    [((16,16),(45,16),4,'C'),((45,16),(65,30),4,'R'),((16,16),(20,45),4,'E'),((45,16),(48,46),4,'L'),((20,45),(48,46),4,'M'),((20,45),(22,67),4,'a'),((48,46),(56,66),4,'A'),((22,67),(56,66),4,'u')]
)

with open("Shared/StaticData.h", "r") as f:
    sh = f.read()
if "rr_biome_id_nether" not in sh:
    sh = sh.replace(
        "    rr_biome_id_beehive,\n    rr_biome_id_max",
        "    rr_biome_id_beehive,\n    rr_biome_id_nether,\n    rr_biome_id_ocean,\n    rr_biome_id_plains,\n    rr_biome_id_max"
    )
    sh = sh.replace(
        "RR_DECLARE_MAZE(PVP, 160)",
        "RR_DECLARE_MAZE(PVP, 160)\nRR_DECLARE_MAZE(NETHER, 160)\nRR_DECLARE_MAZE(OCEAN, 160)\nRR_DECLARE_MAZE(PLAINS, 160)"
    )
    with open("Shared/StaticData.h", "w") as f:
        f.write(sh)

with open("Shared/StaticData.c", "r") as f:
    sc = f.read()
if "RR_DEFINE_MAZE(NETHER, 160)" not in sc:
    sc = sc.replace("    init(PVP);", "    init(PVP);\n    init(NETHER);\n    init(OCEAN);\n    init(PLAINS);")
    extra_mazes = f"\nRR_DEFINE_MAZE(NETHER, 160) = {{\n{nether_grid}\n}};\nRR_DEFINE_MAZE(OCEAN, 160) = {{\n{ocean_grid}\n}};\nRR_DEFINE_MAZE(PLAINS, 160) = {{\n{plains_grid}\n}};\n"
    sc = sc.replace("struct rr_maze_declaration RR_MAZES[rr_biome_id_max] = {", extra_mazes + "\nstruct rr_maze_declaration RR_MAZES[rr_biome_id_max] = {")
    sc = sc.replace(
        "    {MAZE_ENTRY(BURROW, 512), 0},\n};",
        """    {MAZE_ENTRY(BURROW, 512), 0},
    {MAZE_ENTRY(NETHER, 2048), 7, {{12,12,4,4,14,14,1},{40,14,4,4,42,16,15},{62,22,4,4,64,24,30},{20,44,4,4,22,46,45},{50,46,4,4,52,48,60},{22,64,4,4,24,66,75},{56,64,4,4,58,66,90}}},
    {MAZE_ENTRY(OCEAN, 2048), 7, {{38,12,4,4,40,14,1},{16,26,4,4,18,28,15},{60,26,4,4,62,28,30},{38,40,4,4,40,42,45},{16,56,4,4,18,58,60},{60,56,4,4,62,58,75},{38,66,4,4,40,68,90}}},
    {MAZE_ENTRY(PLAINS, 2048), 7, {{14,14,4,4,16,16,1},{43,14,4,4,45,16,15},{63,28,4,4,65,30,30},{18,43,4,4,20,45,45},{46,44,4,4,48,46,60},{20,65,4,4,22,67,75},{54,64,4,4,56,66,90}}},
};"""
    )
    sc = re.sub(
        r"struct rr_biome_server RR_BIOME_SERVERS\[rr_biome_id_max\]\s*=\s*\{.*?\};",
        'struct rr_biome_server RR_BIOME_SERVERS[rr_biome_id_max] = {{"default",1234,"hc"},{"pvp",1235,"ant"},{NULL,0,NULL},{NULL,0,NULL},{"nether",1236,"neth"},{"ocean",1237,"ocn"},{"plains",1238,"pln"}};',
        sc, flags=re.DOTALL
    )
    with open("Shared/StaticData.c", "w") as f:
        f.write(sc)

with open("Server/CMakeLists.txt", "r") as f:
    cm = f.read()
for flag in ["NETHER", "OCEAN", "PLAINS"]:
    if f"if({flag})" not in cm:
        cm += f'\nif({flag})\n    set(CMAKE_C_FLAGS "${{CMAKE_C_FLAGS}} -D{flag}")\nendif()\n'
with open("Server/CMakeLists.txt", "w") as f:
    f.write(cm)

with open("Server/Server.c", "r") as f:
    srv = f.read()
if "#ifdef NETHER" not in srv:
    srv = srv.replace(
        "#ifdef ESCAPE\n    RR_GLOBAL_BIOME = rr_biome_id_garden;\n#endif",
        "#ifdef ESCAPE\n    RR_GLOBAL_BIOME = rr_biome_id_garden;\n#endif\n#ifdef NETHER\n    RR_GLOBAL_BIOME = rr_biome_id_nether;\n#endif\n#ifdef OCEAN\n    RR_GLOBAL_BIOME = rr_biome_id_ocean;\n#endif\n#ifdef PLAINS\n    RR_GLOBAL_BIOME = rr_biome_id_plains;\n#endif"
    )
    with open("Server/Server.c", "w") as f:
        f.write(srv)

with open("Server/Waves.c", "r") as f:
    wv = f.read()
if "rr_biome_id_nether" not in wv:
    new_waves = """    if (biome == rr_biome_id_nether) {
        float diff = zone ? zone->difficulty : 1.0f; double r = rr_frand();
        if (diff <= 20.0f) return r < 0.45 ? rr_mob_id_fire_worker_ant : (r < 0.80 ? rr_mob_id_fire_soldier_ant : rr_mob_id_rock);
        if (diff <= 48.0f) return r < 0.35 ? rr_mob_id_carnotaurus : (r < 0.75 ? rr_mob_id_fire_soldier_ant : rr_mob_id_queen_fire_ant);
        return r < 0.35 ? rr_mob_id_volcano : (r < 0.68 ? rr_mob_id_titanoboa : rr_mob_id_meteor);
    }
    if (biome == rr_biome_id_ocean) {
        float diff = zone ? zone->difficulty : 1.0f; double r = rr_frand();
        if (diff <= 20.0f) return r < 0.40 ? rr_mob_id_dragonfly : (r < 0.75 ? rr_mob_id_compsognathus : rr_mob_id_fern);
        if (diff <= 48.0f) return r < 0.45 ? rr_mob_id_spinosaurus : (r < 0.80 ? rr_mob_id_pteranodon : rr_mob_id_dilophosaurus);
        return r < 0.60 ? rr_mob_id_mosasaurus : rr_mob_id_quetzalcoatlus;
    }
    if (biome == rr_biome_id_plains) {
        float diff = zone ? zone->difficulty : 1.0f; double r = rr_frand();
        if (diff <= 20.0f) return r < 0.35 ? rr_mob_id_ladybug : (r < 0.65 ? rr_mob_id_honeybee : (r < 0.85 ? rr_mob_id_fern : rr_mob_id_tree));
        if (diff <= 48.0f) return r < 0.30 ? rr_mob_id_hornet : (r < 0.55 ? rr_mob_id_fat_bee : (r < 0.80 ? rr_mob_id_triceratops : rr_mob_id_stegosaurus));
        return r < 0.45 ? rr_mob_id_brachiosaurus : (r < 0.80 ? rr_mob_id_ankylosaurus : rr_mob_id_beehive);
    }
    if (biome == rr_biome_id_pvp)"""
    wv = wv.replace("    if (biome == rr_biome_id_pvp)", new_waves, 1)
    with open("Server/Waves.c", "w") as f:
        f.write(wv)

with open("Client/Game.c", "r") as f:
    gc = f.read()
if '"Nether"' not in gc:
    gc = gc.replace(
        'rr_ui_biome_button_init("Escape Room", 0xff6a1b9a, rr_biome_id_garden),',
        'rr_ui_biome_button_init("Escape Room", 0xff6a1b9a, rr_biome_id_garden),\nrr_ui_biome_button_init("Nether", 0xffc0392b, rr_biome_id_nether),\nrr_ui_biome_button_init("Ocean", 0xff1f618d, rr_biome_id_ocean),\nrr_ui_biome_button_init("Plains", 0xff27ae60, rr_biome_id_plains),'
    )
    gc = gc.replace("this->selected_biome > rr_biome_id_garden", "this->selected_biome >= rr_biome_id_max")
    gc = gc.replace("if (biome > rr_biome_id_garden ||", "if (biome >= rr_biome_id_max ||")
    with open("Client/Game.c", "w") as f:
        f.write(gc)

with open("Client/Ui/TitleScreen/Squad.c", "r") as f:
    sq = f.read()
if "b <= rr_biome_id_garden" in sq:
    sq = sq.replace("b <= rr_biome_id_garden", "b < rr_biome_id_max")
    with open("Client/Ui/TitleScreen/Squad.c", "w") as f:
        f.write(sq)

with open("Client/Renderer/RenderArena.c", "r") as f:
    ra = f.read()
if "rr_biome_id_nether" not in ra:
    floor_patch = """        if (this->selected_biome == rr_biome_id_nether || this->selected_biome == rr_biome_id_ocean || this->selected_biome == rr_biome_id_plains) {
            uint32_t bg = (this->selected_biome == rr_biome_id_nether) ? 0xff3b1414 : ((this->selected_biome == rr_biome_id_ocean) ? 0xff154360 : 0xff3e8e41);
            rr_renderer_set_fill(renderer, bg); rr_renderer_begin_path(renderer); rr_renderer_rect(renderer, -128, -128, 256, 256); rr_renderer_fill(renderer);
        }
        if (this->selected_biome == rr_biome_id_pvp)"""
    ra = ra.replace("        if (this->selected_biome == rr_biome_id_pvp)", floor_patch, 1)
    with open("Client/Renderer/RenderArena.c", "w") as f:
        f.write(ra)

print("DONE")
