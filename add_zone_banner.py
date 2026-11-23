import re

with open("Client/Ui/InGame/Minimap.c", "r", encoding="utf-8") as f:
    mm = f.read()

pattern = re.compile(r'(\s*if \(i == 1\)\s*\{\s*rr_renderer_set_fill\(renderer, 0xff0080ff\);.*?\})', re.DOTALL)
m = pattern.search(mm)
assert m, "Не найден блок игрока i == 1 в Minimap.c"

banner_code = m.group(1) + """
            if (i == 1)
            {
                int32_t gx = (int32_t)(physical->lerp_x / grid_size);
                int32_t gy = (int32_t)(physical->lerp_y / grid_size);
                if (gx >= 0 && gx < maze_dim && gy >= 0 && gy < maze_dim)
                {
                    uint8_t rarity = grid[gy * maze_dim + gx].difficulty / 8;
                    if (rarity >= rr_rarity_id_max) rarity = rr_rarity_id_max - 1;
                    static uint8_t last_zone_rarity = 255;
                    if (rarity != last_zone_rarity)
                    {
                        last_zone_rarity = rarity;
                        const char *zname = RR_RARITY_NAMES[rarity];
                        uint32_t zcol = RR_RARITY_COLORS[rarity];
                        EM_ASM({
                            const name = UTF8ToString($0) + " Zone";
                            const col = $1 >>> 0;
                            const hex = "#" + ("000000" + (col & 0xffffff).toString(16)).slice(-6);
                            let el = document.getElementById("rr-zone-toast");
                            if (el) el.remove();
                            el = document.createElement("div");
                            el.id = "rr-zone-toast";
                            el.textContent = name;
                            el.style.cssText = "position:fixed;left:50%;bottom:135px;transform:translate(-50%, 30px);opacity:0;pointer-events:none;z-index:9999;font-family:Ubuntu,sans-serif;font-size:32px;font-weight:900;letter-spacing:1px;color:" + hex + ";-webkit-text-stroke:2px #1a1a1a;text-shadow:0 3px 8px rgba(0,0,0,0.65);transition:transform 0.35s cubic-bezier(0.22,1,0.36,1),opacity 0.35s ease;";
                            document.body.appendChild(el);
                            requestAnimationFrame(() => {
                                el.style.transform = "translate(-50%, 0px)";
                                el.style.opacity = "1";
                            });
                            setTimeout(() => {
                                el.style.transform = "translate(-50%, -18px)";
                                el.style.opacity = "0";
                            }, 1150);
                            setTimeout(() => { if (el) el.remove(); }, 1550);
                        }, zname, zcol);
                    }
                }
            }"""

if "rr-zone-toast" not in mm:
    mm = "#include <emscripten.h>\n" + mm[:m.start()] + banner_code + mm[m.end():]
    with open("Client/Ui/InGame/Minimap.c", "w", encoding="utf-8") as f:
        f.write(mm)
print("Плавный баннер названия зоны добавлен!")
