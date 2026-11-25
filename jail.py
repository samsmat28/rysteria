import shutil, re
for p in ["Shared/StaticData.h","Shared/StaticData.c","Server/Client.c","Server/Server.c","Client/Renderer/RenderArena.c","Client/Ui/InGame/Minimap.c"]:
    shutil.copy2(p, p+".bak")

open("Shared/StaticData.h","w").write(open("Shared/StaticData.h").read().replace("RR_DECLARE_MAZE(PLAINS, 160)","RR_DECLARE_MAZE(PLAINS, 160)\nRR_DECLARE_MAZE(JAIL, 160)",1))

g = [['_']*80 for _ in range(80)]
for y in range(37,43):
    for x in range(4,43): g[y][x]='1'
for gx in (13,25,36):
    for y in range(10,70): g[y][gx]='1'
for gy in (18,28,51,61):
    for x in range(6,37): g[gy][x]='1'
tiers = ['1','g','m','a','o','h']
for bi,(y0,y1,dy) in enumerate([(11,16,18),(21,26,28),(31,35,37),(44,48,43),(53,58,52),(63,68,62)]):
    for ci,(x0,x1,dx) in enumerate([(6,11,8),(16,23,19),(28,34,30)]):
        for y in range(y0,y1+1):
            for x in range(x0,x1+1): g[y][x]=tiers[(bi+ci)%6]
        s = 1 if dy>y1 else -1
        for k in range(y1 if s==1 else y0, dy+s, s): g[k][dx]=g[k][dx+1]='1'
for y in range(37,43):
    for x in range(39,42): g[y][x]='a'
for y in range(8,72):
    for x in range(43,77): g[y][x] = 'o' if x>=68 else ('g' if (x>=58 or y<=14 or y>=65) else '1')
for y in range(37,43):
    for x in range(72,77): g[y][x]='h'

maze = "RR_DEFINE_MAZE(JAIL, 160) = {\n" + "\n".join("    {"+",".join(f"'{c}'" for c in r)+"}," for r in g) + "\n};\n\n"
sc = open("Shared/StaticData.c").read()
sc = sc.replace("struct rr_maze_declaration RR_MAZES[rr_biome_id_max] = {", maze+"struct rr_maze_declaration RR_MAZES[rr_biome_id_max] = {",1)
sc = sc.replace("init(PLAINS);","init(PLAINS);\n    init(JAIL);",1)
sc = re.sub(r"\{MAZE_ENTRY\(ESCAPE,\s*2048\)[^\n]*\}", "{MAZE_ENTRY(JAIL, 2048), 5, {{11,38,5,4,13,40},{23,38,4,4,25,40},{39,37,3,6,40,40},{54,37,6,6,56,40},{72,37,5,6,74,40}}}", sc, 1)
open("Shared/StaticData.c","w").write(sc)

cc = open("Server/Client.c").read()
cc = cc.replace("(RR_GLOBAL_BIOME == rr_biome_id_plains) ? 11.0f : decl->checkpoints[checkpoint].spawn_x", "(RR_GLOBAL_BIOME == rr_biome_id_plains) ? 11.0f : ((RR_GLOBAL_BIOME == rr_biome_id_garden) ? 13.0f : decl->checkpoints[checkpoint].spawn_x)")
cc = cc.replace("(RR_GLOBAL_BIOME == rr_biome_id_plains) ? 11.0f : decl->checkpoints[checkpoint].spawn_y", "(RR_GLOBAL_BIOME == rr_biome_id_plains) ? 11.0f : ((RR_GLOBAL_BIOME == rr_biome_id_garden) ? 40.0f : decl->checkpoints[checkpoint].spawn_y)")
open("Server/Client.c","w").write(cc)

ra = open("Client/Renderer/RenderArena.c").read()
ra = ra.replace("uint32_t bg = (this->selected_biome == rr_biome_id_nether) ? 0xff3b1414 : ((this->selected_biome == rr_biome_id_ocean) ? 0xff154360 : 0xff3e8e41);", "uint32_t bg = (this->selected_biome == rr_biome_id_garden) ? 0xff2c333d : ((this->selected_biome == rr_biome_id_nether) ? 0xff3b1414 : ((this->selected_biome == rr_biome_id_ocean) ? 0xff154360 : 0xff3e8e41));")
ra = re.sub(r"if \(arena->biome == rr_biome_id_garden && tile == 1\)\s*\{[^}]*\}", "", ra, 1)
ra = ra.replace("float bx = 138.0f * 2.0f * 2048.0f, by = 80.0f * 2.0f * 2048.0f;", "float bx = 74.0f * 2.0f * 2048.0f, by = 40.0f * 2.0f * 2048.0f;")
open("Client/Renderer/RenderArena.c","w").write(ra)

mm = re.sub(r"if \(arena->biome == rr_biome_id_garden\)\s*\{[^}]*\}", "", open("Client/Ui/InGame/Minimap.c").read(), 1)
open("Client/Ui/InGame/Minimap.c","w").write(mm)

sv = open("Server/Server.c").read()
sv = sv.replace("#ifdef PVP\n    RR_GLOBAL_BIOME = rr_biome_id_pvp;\n#endif", "#ifdef JAIL\n    RR_GLOBAL_BIOME = rr_biome_id_garden;\n#endif\n#ifdef PVP\n    RR_GLOBAL_BIOME = rr_biome_id_pvp;\n#endif", 1)
hook = """if (RR_GLOBAL_BIOME == rr_biome_id_garden && client->verified && client->player_info && client->player_info->flower_id != RR_NULL_ENTITY) {
    struct rr_component_physical *fp = rr_simulation_get_physical(&this->simulation, client->player_info->flower_id);
    if (fp && fp->arena != RR_NULL_ENTITY) {
        static uint32_t p_init = 0; static uint64_t r_cd = 0; float gs = 2.0f * 2048.0f;
        if (!p_init) { p_init = 1;
            float pts[6][3] = {{25,40,rr_mob_id_ant_baby},{36,30,rr_mob_id_ant_baby},{40,40,rr_mob_id_rock},{55,34,rr_mob_id_ant_soldier},{55,46,rr_mob_id_ant_soldier},{70,40,rr_mob_id_rock}};
            for (int i=0;i<6;i++) rr_simulation_alloc_mob(&this->simulation, fp->arena, pts[i][0]*gs, pts[i][1]*gs, (uint8_t)pts[i][2], 3, rr_simulation_team_id_mobs);
        }
        float dx = fp->x - 74.0f*gs, dy = fp->y - 40.0f*gs;
        if (dx*dx + dy*dy < 360.0f*360.0f && this->ticks > r_cd) {
            r_cd = this->ticks + 300; client->jail_until = 0; rr_jail_save(client->ip_address, client->logged_user, 0);
            if (this->simulation.animation_length < sizeof(this->simulation.animations)/sizeof(this->simulation.animations[0])) {
                struct rr_simulation_animation *an = &this->simulation.animations[this->simulation.animation_length++];
                memset(an,0,sizeof(*an)); an->type=rr_animation_type_chat; an->owner=client->player_info->parent_id;
                strcpy(an->name,"[RIOT ALARM!]"); strcpy(an->message,"Jailbreak! Sentence cleared, guards incoming!");
            }
            for (int i=0;i<4;i++) rr_simulation_alloc_mob(&this->simulation, fp->arena, (65+i*2)*gs, (37+i*2)*gs, (i%2)?rr_mob_id_rock:rr_mob_id_ant_soldier, 4, rr_simulation_team_id_mobs);
        }
    }
}
"""
sv = sv.replace("if (client->jail_until == 0) {", hook + "            if (client->jail_until == 0) {", 1)
open("Server/Server.c","w").write(sv)
print("OK")
