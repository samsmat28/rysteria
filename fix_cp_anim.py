import re
with open("Server/System/PetalBehavior.c", "r", encoding="utf-8") as f:
    pb = f.read()

if "<string.h>" not in pb:
    pb = "#include <string.h>\n" + pb

old_blk = re.compile(r'if \(simulation->animation_length < RR_MAX_ANIMATION_COUNT\).*?\}', re.DOTALL)
new_blk = """if (simulation->animation_length < 256) {
                    struct rr_simulation_animation *anim = &simulation->animations[simulation->animation_length++];
                    memset(anim, 0, sizeof(*anim));
                    anim->type = rr_animation_type_chat;
                    strcpy(anim->name, "[Checkpoint]");
                    strcpy(anim->message, "New zone progress saved!");
                }"""

assert old_blk.search(pb), "Не найден блок анимации"
pb = old_blk.sub(new_blk, pb, count=1)

with open("Server/System/PetalBehavior.c", "w", encoding="utf-8") as f:
    f.write(pb)
print("Анимация чекпоинта исправлена!")
