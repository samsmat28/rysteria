# 1. Client/Ui/InGame/Minimap.c: убираем UTF8ToString, передаем индекс редкости числом
with open("Client/Ui/InGame/Minimap.c", "r", encoding="utf-8") as f:
    mm = f.read()

old_js = """                        const char *zname = RR_RARITY_NAMES[rarity];
                        uint32_t zcol = RR_RARITY_COLORS[rarity];
                        EM_ASM({
                            const name = UTF8ToString($0) + " Zone";"""

new_js = """                        uint32_t zcol = RR_RARITY_COLORS[rarity];
                        EM_ASM({
                            const names = ["Common","Uncommon","Rare","Epic","Legendary","Mythic","Ultra","Super","Omega","Hyper","Gods"];
                            const name = (names[$0] || "Unknown") + " Zone";"""

if old_js in mm:
    mm = mm.replace(old_js, new_js, 1).replace("}, zname, zcol);", "}, rarity, zcol);", 1)
    with open("Client/Ui/InGame/Minimap.c", "w", encoding="utf-8") as f:
        f.write(mm)

# 2. Server/System/Checkpoints.c: безопасная проверка размера массива animations
with open("Server/System/Checkpoints.c", "r", encoding="utf-8") as f:
    cp = f.read()

cp = cp.replace("this->animation_length < 256", "this->animation_length < (sizeof(this->animations) / sizeof(this->animations[0]))")
with open("Server/System/Checkpoints.c", "w", encoding="utf-8") as f:
    f.write(cp)

print("Обе возможные причины вылета исправлены!")
