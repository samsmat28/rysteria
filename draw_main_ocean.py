import re

code = """    if (mob && physical && mob->id >= rr_mob_id_bubble && mob->id <= rr_mob_id_thalassa_core) {
        float r = physical->radius > 8.0f ? physical->radius : 24.0f;
        struct rr_renderer_context_state ost;
        rr_renderer_context_state_init(renderer, &ost);
        rr_renderer_translate(renderer, physical->x, physical->y);
        rr_renderer_rotate(renderer, physical->angle);

        if (mob->id == rr_mob_id_bubble) {
            rr_renderer_set_fill(renderer, 0x66f8e5b5u);
            rr_renderer_set_stroke(renderer, 0xdde8c882u);
            rr_renderer_set_line_width(renderer, 3.5f);
            rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, 0, 0, r); rr_renderer_fill(renderer); rr_renderer_stroke(renderer);
            rr_renderer_set_fill(renderer, 0xccffffffu);
            rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, -r*0.33f, -r*0.33f, r*0.24f); rr_renderer_arc(renderer, -r*0.1f, -r*0.52f, r*0.11f); rr_renderer_fill(renderer);
        } else if (mob->id == rr_mob_id_crab || mob->id == rr_mob_id_hermit_crab || mob->id == rr_mob_id_king_crab || mob->id == rr_mob_id_trident_guardian) {
            uint32_t body = (mob->id == rr_mob_id_king_crab) ? 0xff1b1b99u : ((mob->id == rr_mob_id_trident_guardian) ? 0xffd84e1du : 0xff2b44c9u);
            uint32_t dark = 0xff1b2b85u;
            rr_renderer_set_stroke(renderer, dark); rr_renderer_set_line_width(renderer, 4.5f);
            for (int k = -1; k <= 1; k++) { rr_renderer_begin_path(renderer); rr_renderer_move_to(renderer, k*r*0.32f, -r*0.6f); rr_renderer_line_to(renderer, k*r*0.32f-r*0.15f, -r*1.12f); rr_renderer_move_to(renderer, k*r*0.32f, r*0.6f); rr_renderer_line_to(renderer, k*r*0.32f-r*0.15f, r*1.12f); rr_renderer_stroke(renderer); }
            rr_renderer_set_fill(renderer, 0xff445effu); rr_renderer_set_stroke(renderer, dark); rr_renderer_set_line_width(renderer, 3.5f);
            rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, r*0.82f, -r*0.58f, r*0.34f); rr_renderer_arc(renderer, r*0.82f, r*0.58f, r*0.34f); rr_renderer_fill(renderer); rr_renderer_stroke(renderer);
            rr_renderer_set_fill(renderer, body); rr_renderer_set_stroke(renderer, dark); rr_renderer_set_line_width(renderer, 4.5f);
            rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, 0, 0, r*0.78f); rr_renderer_fill(renderer); rr_renderer_stroke(renderer);
            if (mob->id == rr_mob_id_king_crab || mob->id == rr_mob_id_trident_guardian) { rr_renderer_set_fill(renderer, 0xff15ccfau); rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, 0, 0, r*0.3f); rr_renderer_fill(renderer); }
            rr_renderer_set_fill(renderer, 0xff111111u); rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, r*0.54f, -r*0.24f, r*0.12f); rr_renderer_arc(renderer, r*0.54f, r*0.24f, r*0.12f); rr_renderer_fill(renderer);
        } else if (mob->id == rr_mob_id_jellyfish || mob->id == rr_mob_id_octopus || mob->id == rr_mob_id_kraken_spawn || mob->id == rr_mob_id_storm_kraken) {
            uint32_t bell = (mob->id == rr_mob_id_jellyfish) ? 0xbbd98ae8u : ((mob->id == rr_mob_id_octopus) ? 0xffea3393u : 0xff871c58u);
            uint32_t tent = (mob->id == rr_mob_id_jellyfish) ? 0xaae6a8f5u : 0xfff979e8u;
            rr_renderer_set_stroke(renderer, tent); rr_renderer_set_line_width(renderer, 3.5f);
            for (int k = -2; k <= 2; k++) { float yy = k*r*0.25f; rr_renderer_begin_path(renderer); rr_renderer_move_to(renderer, -r*0.2f, yy); rr_renderer_line_to(renderer, -r*1.3f, yy); rr_renderer_stroke(renderer); }
            rr_renderer_set_fill(renderer, bell); rr_renderer_set_stroke(renderer, 0xff6b21a8u); rr_renderer_set_line_width(renderer, 4.0f);
            rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, r*0.12f, 0, r*0.82f); rr_renderer_fill(renderer); rr_renderer_stroke(renderer);
            rr_renderer_set_fill(renderer, tent); rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, r*0.24f, 0, r*0.42f); rr_renderer_fill(renderer);
        } else if (mob->id == rr_mob_id_starfish) {
            rr_renderer_set_fill(renderer, 0xff5a68e0u); rr_renderer_set_stroke(renderer, 0xff3b47adu); rr_renderer_set_line_width(renderer, 4.0f);
            rr_renderer_begin_path(renderer);
            for (int k = 0; k < 10; k++) { float a = k*0.628318f, rd = (k%2==0) ? r*1.05f : r*0.42f; if (k==0) rr_renderer_move_to(renderer, rd*cosf(a), rd*sinf(a)); else rr_renderer_line_to(renderer, rd*cosf(a), rd*sinf(a)); }
            rr_renderer_fill(renderer); rr_renderer_stroke(renderer);
            rr_renderer_set_fill(renderer, 0xff9aa5f5u);
            for (int arm = 0; arm < 5; arm++) { float a = arm*1.256637f; for (int d = 1; d <= 3; d++) { rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, r*0.24f*d*cosf(a), r*0.24f*d*sinf(a), r*0.07f); rr_renderer_fill(renderer); } }
        } else if (mob->id == rr_mob_id_shell || mob->id == rr_mob_id_nautilus || mob->id == rr_mob_id_coral_golem) {
            uint32_t shc = (mob->id == rr_mob_id_nautilus) ? 0xff0677d9u : ((mob->id == rr_mob_id_coral_golem) ? 0xff5e3ff4u : 0xff9ec2dbu);
            rr_renderer_set_fill(renderer, shc); rr_renderer_set_stroke(renderer, 0xff5c4033u); rr_renderer_set_line_width(renderer, 4.5f);
            rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, 0, 0, r*0.9f); rr_renderer_fill(renderer); rr_renderer_stroke(renderer);
            rr_renderer_set_stroke(renderer, 0xff7fa3bdu); rr_renderer_set_line_width(renderer, 3.0f);
            for (int k = -2; k <= 2; k++) { rr_renderer_begin_path(renderer); rr_renderer_move_to(renderer, -r*0.72f, 0); rr_renderer_line_to(renderer, r*0.76f, k*r*0.28f); rr_renderer_stroke(renderer); }
        } else if (mob->id == rr_mob_id_pufferfish) {
            rr_renderer_set_stroke(renderer, 0xff0f3578u); rr_renderer_set_line_width(renderer, 4.0f);
            for (int k = 0; k < 10; k++) { float a = k*0.628318f; rr_renderer_begin_path(renderer); rr_renderer_move_to(renderer, r*0.55f*cosf(a), r*0.55f*sinf(a)); rr_renderer_line_to(renderer, r*1.15f*cosf(a), r*1.15f*sinf(a)); rr_renderer_stroke(renderer); }
            rr_renderer_set_fill(renderer, 0xff24bffbu); rr_renderer_set_stroke(renderer, 0xff0f3578u); rr_renderer_set_line_width(renderer, 4.0f);
            rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, 0, 0, r*0.78f); rr_renderer_fill(renderer); rr_renderer_stroke(renderer);
            rr_renderer_set_fill(renderer, 0xffffffffu); rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, r*0.42f, -r*0.28f, r*0.16f); rr_renderer_arc(renderer, r*0.42f, r*0.28f, r*0.16f); rr_renderer_fill(renderer);
            rr_renderer_set_fill(renderer, 0xff111111u); rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, r*0.46f, -r*0.28f, r*0.08f); rr_renderer_arc(renderer, r*0.46f, r*0.28f, r*0.08f); rr_renderer_fill(renderer);
        } else if (mob->id == rr_mob_id_sea_turtle) {
            rr_renderer_set_fill(renderer, 0xffacef86u); rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, r*0.4f, -r*0.85f, r*0.26f); rr_renderer_arc(renderer, r*0.4f, r*0.85f, r*0.26f); rr_renderer_arc(renderer, -r*0.45f, -r*0.75f, r*0.22f); rr_renderer_arc(renderer, -r*0.45f, r*0.75f, r*0.22f); rr_renderer_fill(renderer);
            rr_renderer_set_fill(renderer, 0xff346516u); rr_renderer_set_stroke(renderer, 0xff052e16u); rr_renderer_set_line_width(renderer, 4.5f);
            rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, 0, 0, r*0.84f); rr_renderer_fill(renderer); rr_renderer_stroke(renderer);
            rr_renderer_set_fill(renderer, 0xff4d7c0fu); rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, 0, 0, r*0.45f); rr_renderer_fill(renderer);
        } else {
            uint32_t fc = (mob->id == rr_mob_id_clownfish) ? 0xff1673f9u : ((mob->id == rr_mob_id_seahorse) ? 0xff15ccfau : ((mob->id == rr_mob_id_great_white || mob->id == rr_mob_id_megalodon || mob->id == rr_mob_id_omega_shark) ? 0xff554133u : 0xff3b82f6u));
            uint32_t tail = (mob->id == rr_mob_id_clownfish) ? 0xffffffffu : ((mob->id == rr_mob_id_megalodon || mob->id == rr_mob_id_omega_shark) ? 0xff4444efu : 0xff93c5fdu);
            rr_renderer_set_fill(renderer, tail); rr_renderer_begin_path(renderer); rr_renderer_move_to(renderer, -r*0.65f, 0); rr_renderer_line_to(renderer, -r*1.35f, -r*0.55f); rr_renderer_line_to(renderer, -r*1.35f, r*0.55f); rr_renderer_fill(renderer);
            rr_renderer_set_fill(renderer, fc); rr_renderer_set_stroke(renderer, 0xff1e293bu); rr_renderer_set_line_width(renderer, 4.0f);
            rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, r*0.1f, 0, r*0.82f); rr_renderer_fill(renderer); rr_renderer_stroke(renderer);
            if (mob->id == rr_mob_id_clownfish) { rr_renderer_set_fill(renderer, 0xffffffffu); rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, -r*0.05f, 0, r*0.35f); rr_renderer_fill(renderer); }
            rr_renderer_set_fill(renderer, 0xffffffffu); rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, r*0.48f, -r*0.28f, r*0.15f); rr_renderer_arc(renderer, r*0.48f, r*0.28f, r*0.15f); rr_renderer_fill(renderer);
            rr_renderer_set_fill(renderer, 0xff111111u); rr_renderer_begin_path(renderer); rr_renderer_arc(renderer, r*0.52f, -r*0.28f, r*0.08f); rr_renderer_arc(renderer, r*0.52f, r*0.28f, r*0.08f); rr_renderer_fill(renderer);
        }
        rr_renderer_context_state_free(renderer, &ost);
        return;
    }"""

rm = open("Client/Renderer/RenderMob.c").read()
rm = re.sub(r"    if \(mob && physical && mob->id >= rr_mob_id_bubble && mob->id <= rr_mob_id_thalassa_core\) \{[\s\S]*?\n    \}", code, rm, count=1)
open("Client/Renderer/RenderMob.c", "w").write(rm)
print("MAIN_OCEAN_MOBS_DRAWN")
