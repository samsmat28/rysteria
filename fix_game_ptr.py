import re

with open("Client/Main.c", "r", encoding="utf-8") as f:
    mc = f.read()

# 1. Заменяем game->socket на g_rr_game->socket внутри rr_exec_shop_cmd и добавляем проверку if (!g_rr_game) return;
mc = mc.replace(
    "EMSCRIPTEN_KEEPALIVE void rr_exec_shop_cmd(const char *cmd) {",
    "static struct rr_game *g_rr_game = NULL;\nEMSCRIPTEN_KEEPALIVE void rr_exec_shop_cmd(const char *cmd) {\n    if (!g_rr_game) return;"
)
mc = mc.replace("game->socket", "g_rr_game->socket")
mc = mc.replace("game.socket", "g_rr_game->socket")

# 2. Внутри main() сразу после объявления struct rr_game game... присваиваем g_rr_game = &game; (или g_rr_game = game;)
if "g_rr_game =" not in mc:
    if re.search(r"struct\s+rr_game\s*\*\s*game\b", mc):
        mc = re.sub(r"(struct\s+rr_game\s*\*\s*game[^;]*;)", r"\1\n    g_rr_game = game;", mc, count=1)
    else:
        mc = re.sub(r"(struct\s+rr_game\s+game[^;]*;)", r"\1\n    g_rr_game = &game;", mc, count=1)

with open("Client/Main.c", "w", encoding="utf-8") as f:
    f.write(mc)

print("[OK] Указатель g_rr_game привязан")
