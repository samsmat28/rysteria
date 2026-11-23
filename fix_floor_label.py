with open("Client/Renderer/RenderArena.c", "r", encoding="utf-8") as f:
    ra = f.read()

ra = ra.replace("rr_renderer_set_line_width(renderer, 10.0f);", "rr_renderer_set_global_alpha(renderer, 0.85f);\n                    rr_renderer_set_line_width(renderer, 18.0f);")
ra = ra.replace("rr_renderer_set_text_size(renderer, 68);", "rr_renderer_set_text_size(renderer, 180);")
ra = ra.replace("rr_renderer_set_line_width(renderer, 6.0f);", "rr_renderer_set_line_width(renderer, 12.0f);")
ra = ra.replace("rr_renderer_fill_text(renderer, RR_RARITY_NAMES[hi], tx, ty);", "rr_renderer_fill_text(renderer, RR_RARITY_NAMES[hi], tx, ty);\n                    rr_renderer_set_global_alpha(renderer, 0.5f);")

with open("Client/Renderer/RenderArena.c", "w", encoding="utf-8") as f:
    f.write(ra)
print("Крупные надписи зон (180px) и толстые линии редкости готовы!")
