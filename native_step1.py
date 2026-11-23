import re

# 1. Очищаем Main.c от старых HTML-вставок
with open("Client/Main.c", "r", encoding="utf-8") as f:
    mc = f.read()

mc = re.sub(r"static struct rr_game \*g_rr_game = NULL;.*?EMSCRIPTEN_KEEPALIVE void rr_exec_shop_cmd\(const char \*cmd\) \{.*?\n\}\n", "", mc, flags=re.DOTALL)
mc = re.sub(r"\n\s*EM_ASM\(\{\s*if \(window\.__rrMenuShopReady\).*?\n\s*\}\);\n", "\n", mc, flags=re.DOTALL)
mc = re.sub(r"\n\s*g_rr_game = &?game;\n", "\n", mc)

with open("Client/Main.c", "w", encoding="utf-8") as f:
    f.write(mc)

# 2. Смотрим как устроен Client/Ui/TitleScreen/Changelog.c и Changelog.h, чтобы сделать 1-в-1 нативное окно
with open("Client/Ui/TitleScreen/Changelog.h", "r", encoding="utf-8") as f:
    print("=== Changelog.h ===")
    print(f.read())

with open("Client/Ui/TitleScreen/Changelog.c", "r", encoding="utf-8") as f:
    print("=== Changelog.c (первые 45 строк) ===")
    print("\n".join(f.read().splitlines()[:45]))
