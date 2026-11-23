import re

with open("Client/Main.c", "r", encoding="utf-8") as f:
    mc = f.read()

c_fn = """
EMSCRIPTEN_KEEPALIVE void rr_exec_shop_cmd(const char *cmd) {
    if (!cmd || !cmd) return;
    struct proto_bug encoder;
    proto_bug_init(&encoder, RR_OUTGOING_PACKET);
    proto_bug_write_uint8(&encoder, game.socket.quick_verification, "qv");
    proto_bug_write_uint8(&encoder, rr_serverbound_chat, "header");
    proto_bug_write_string(&encoder, cmd, 64, "chat");
    rr_websocket_send(&game.socket, encoder.current - encoder.start);
}
"""

# Проверяем, game — это структура (game.socket) или указатель (game->socket)
if re.search(r"struct\s+rr_game\s*\*\s*game\b", mc):
    c_fn = c_fn.replace("game.socket", "game->socket")

if "rr_exec_shop_cmd" not in mc:
    mc = re.sub(r"(int\s+main\s*\()", c_fn + r"\n\1", mc, count=1)
    mc = mc.replace(
        "window.rrMenuCmd = function(cmd) {",
        "window.rrMenuCmd = function(cmd) {\n            if (typeof Module !== 'undefined' && Module.ccall) { Module.ccall('rr_exec_shop_cmd', null, ['string'], [cmd]); }"
    )
    with open("Client/Main.c", "w", encoding="utf-8") as f:
        f.write(mc)
    print("[OK] proto_bug отправка встроена в Client/Main.c")

# Перехватываем входящий пакет rr_clientbound_chat в Client/Socket.c
with open("Client/Socket.c", "r", encoding="utf-8") as f:
    sc = f.read()

if "<emscripten.h>" not in sc:
    sc = "#include <emscripten.h>\n" + sc

m_cb = re.search(r"case\s+rr_clientbound_chat\s*:(.{1,600})", sc, re.DOTALL)
if m_cb and "rr-r-bal" not in sc:
    # Находим переменную буфера/декодера в case rr_clientbound_chat
    m_buf = re.search(r"\b(data|buf|packet|msg|decoder\.start)\b", m_cb.group(1))
    buf_expr = m_buf.group(1) if m_buf else "data"
    hook = f"""
        {{
            const char *raw_p = (const char *){buf_expr};
            for (int k = 0; k < 240; k++) {{
                if (strncmp(raw_p + k, "Баланс:", 13) == 0 || strncmp(raw_p + k, "Квест:", 11) == 0 ||
                    strncmp(raw_p + k, "Продано!", 15) == 0 || strncmp(raw_p + k, "Куплено", 14) == 0 ||
                    strncmp(raw_p + k, "Недостаточно", 24) == 0 || strncmp(raw_p + k, "У вас нет", 17) == 0) {{
                    EM_ASM({{
                        var s = UTF8ToString($0);
                        var mb = s.match(/Баланс:\\s*(\\d+)\\s*R/);
                        if (mb) {{ var el = document.getElementById('rr-r-bal'); if (el) el.textContent = 'R: ' + mb; }}
                        var mq = s.match(/Квест:[^\\n\\r]+/);
                        if (mq) {{ var qe = document.getElementById('rr-q-info'); if (qe) qe.textContent = mq; }}
                        var st = document.getElementById('rr-m-status');
                        if (st) st.textContent = s;
                    }}, raw_p + k);
                    break;
                }}
            }}
        }}
"""
    sc = re.sub(r"(case\s+rr_clientbound_chat\s*:)", r"\1\n" + hook, sc, count=1)
    with open("Client/Socket.c", "w", encoding="utf-8") as f:
        f.write(sc)
    print("[OK] Перехват ответов сервера встроен в Client/Socket.c")
