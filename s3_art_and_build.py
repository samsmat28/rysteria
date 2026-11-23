with open("Client/Assets/RenderPetals.c", "r") as f: rp = f.read()
if "rr_petal_id_claw" not in rp:
    p_styles = [
        ("claw",0xffe9ecef,0xff495057,"spike"),("fang",0xfff8f9fa,0xff868e96,"spike"),("tooth",0xfffff3bf,0xffadb5bd,"spike"),
        ("horn",0xffd8c3a5,0xff6c584c,"spike"),("thagomizer",0xffadb5bd,0xff343a40,"spike"),("scythe",0xfff1f3f5,0xff212529,"spike"),
        ("magma",0xffff5400,0xff9e0000,"orb"),("obsidian",0xff3c096c,0xff10002b,"diamond"),("plate",0xff52b788,0xff1b4332,"diamond"),
        ("scale",0xff2d6a4f,0xff081c15,"diamond"),("amber",0xffffb703,0xffbb3e03,"orb"),("branch",0xff8d5b4c,0xff4a2c2a,"diamond"),
        ("pearl",0xffcaf0f8,0xff0096c7,"orb"),("tail",0xff74c69d,0xff2d6a4f,"spike"),("frill",0xfff77f00,0xff9b2226,"diamond"),
        ("venom",0xff80ed99,0xff22577a,"orb"),("sail",0xffe63946,0xff6a040f,"diamond"),("ash",0xff6c757d,0xff212529,"orb"),
        ("crown",0xffffd60a,0xffb5651d,"diamond"),("relic",0xff9d4edd,0xff3c096c,"diamond")
    ]
    cases = ""
    for name, fill, stroke, shape in p_styles:
        if shape == "spike":
            path = "rr_renderer_move_to(renderer,0,-14);rr_renderer_line_to(renderer,9,11);rr_renderer_line_to(renderer,0,6);rr_renderer_line_to(renderer,-9,11);"
        elif shape == "diamond":
            path = "rr_renderer_move_to(renderer,0,-13);rr_renderer_line_to(renderer,11,0);rr_renderer_line_to(renderer,0,13);rr_renderer_line_to(renderer,-11,0);"
        else:
            path = "rr_renderer_arc(renderer,0,0,11.0f);"
        cases += f"    case rr_petal_id_{name}: rr_renderer_set_fill(renderer,0x{fill:08x});rr_renderer_set_stroke(renderer,0x{stroke:08x});rr_renderer_set_line_width(renderer,2.5f);rr_renderer_begin_path(renderer);{path}rr_renderer_fill(renderer);rr_renderer_stroke(renderer);break;\n"
    rp = rp.replace("    case rr_petal_id_rock:", cases + "    case rr_petal_id_rock:", 1)
    with open("Client/Assets/RenderPetals.c", "w") as f: f.write(rp)

with open("Client/Assets/RenderMobs.c", "r") as f: rm = f.read()
if "rr_mob_id_compsognathus" not in rm:
    m_cases = """    case rr_mob_id_compsognathus: rr_renderer_scale(renderer, 0.75f); render_sprite(renderer, rr_mob_id_dakotaraptor, 0, flags); break;
    case rr_mob_id_stegosaurus: rr_renderer_scale(renderer, 1.25f); render_sprite(renderer, rr_mob_id_ankylosaurus, 0, flags); break;
    case rr_mob_id_dilophosaurus: rr_renderer_scale(renderer, 1.05f); render_sprite(renderer, rr_mob_id_ornithomimus, 0, flags); break;
    case rr_mob_id_spinosaurus: rr_renderer_scale(renderer, 1.45f); render_sprite(renderer, rr_mob_id_trex, 0, flags); break;
    case rr_mob_id_carnotaurus: rr_renderer_scale(renderer, 1.25f); render_sprite(renderer, rr_mob_id_trex, 0, flags); break;
    case rr_mob_id_brachiosaurus: rr_renderer_scale(renderer, 1.85f); render_sprite(renderer, rr_mob_id_edmontosaurus, 0, flags); break;
    case rr_mob_id_therizinosaurus: rr_renderer_scale(renderer, 1.40f); render_sprite(renderer, rr_mob_id_dakotaraptor, 0, flags); break;
    case rr_mob_id_mosasaurus: rr_renderer_scale(renderer, 1.65f); render_sprite(renderer, rr_mob_id_quetzalcoatlus, 0, flags); break;
    case rr_mob_id_volcano:
        rr_renderer_set_fill(renderer, 0xff4a3525); rr_renderer_set_stroke(renderer, 0xff2b1d12); rr_renderer_set_line_width(renderer, 5.0f);
        rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, 0, 0, 58.0f); rr_renderer_fill(renderer); rr_renderer_stroke(renderer);
        rr_renderer_set_fill(renderer, 0xffff5400); rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, 0, 0, 24.0f); rr_renderer_fill(renderer); break;
    case rr_mob_id_titanoboa:
        rr_renderer_set_fill(renderer, 0xff2d6a4f); rr_renderer_set_stroke(renderer, 0xff081c15); rr_renderer_set_line_width(renderer, 6.0f);
        rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, -22, 0, 44.0f); rr_renderer_arc(renderer, 22, 0, 38.0f); rr_renderer_fill(renderer); rr_renderer_stroke(renderer);
        rr_renderer_set_fill(renderer, 0xffffd60a); rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, 38, -10, 6.0f); rr_renderer_arc(renderer, 38, 10, 6.0f); rr_renderer_fill(renderer); break;
    case rr_mob_id_queen_ant:"""
    rm = rm.replace("    case rr_mob_id_queen_ant:", m_cases, 1)
    with open("Client/Assets/RenderMobs.c", "w") as f: f.write(rm)
print("s3_art OK! Собираем...")
