import re

with open("Client/Ui/InGame/Chat.c", "r", encoding="utf-8") as f:
    chat_c = f.read()

with open("Client/Socket.c", "r", encoding="utf-8") as f:
    sock_c = f.read()

# 1. Ищем в Chat.c и Socket.c функцию отправки чата на сервер (обычно rr_socket_send_chat или отправка rr_serverbound_chat)
m_fn = re.search(r"([a-zA-Z0-9_]*chat[a-zA-Z0-9_]*)\s*\(\s*(?:struct\s+rr_[a-zA-Z0-9_]+\s*\*\s*[a-zA-Z0-9_]+\s*,\s*)?const\s+char\s*\*", sock_c + "\n" + chat_c, re.IGNORECASE)
send_fn = m_fn.group(1) if m_fn else ""

# Если не нашли по имени, ищем в Chat.c место использования rr_serverbound_chat
if not send_fn:
    m_sb = re.search(r"rr_serverbound_chat.{1,400}?([a-zA-Z0-9_]+)\s*\(", chat_c + "\n" + sock_c, re.DOTALL)
    send_fn = m_sb.group(1) if m_sb else ""

# 2. Добавляем в Client/Main.c экспортированную C-функцию rr_exec_shop_cmd(const char *cmd) и хук входящего чата
with open("Client/Main.c", "r", encoding="utf-8") as f:
    mc = f.read()

# Ищем в Client/Main.c глобальный указатель на клиент/сокет (обычно client или game)
m_glob = re.search(r"(?:static\s+)?struct\s+(rr_[a-zA-Z0-9_]+)\s*\*?\s*([a-zA-Z0-9_]+)\s*;", mc)
glob_type = m_glob.group(1) if m_glob else ""
glob_name = m_glob.group(2) if m_glob else ""

# Проверяем сигнатуру send_fn в Socket.h / Socket.c
with open("Client/Socket.h", "r", encoding="utf-8") as f:
    sock_h = f.read()

m_sig = re.search(r"void\s+" + re.escape(send_fn) + r"\s*\(([^)]+)\)", sock_h + "\n" + sock_c) if send_fn else None
sig_str = m_sig.group(1) if m_sig else ""

# Формируем вызов C-функции
c_bridge = ""
if send_fn and sig_str:
    if "," in sig_str:
        # Передаётся (socket/client, text) — ищем аргумент в Main.c
        arg_expr = f"&{glob_name}.socket" if f"{glob_name}.socket" in mc else (glob_name if glob_name else "NULL")
        if "socket" in sig_str.lower() and "client" in glob_name.lower() and "*" not in mc.split(glob_name)[0][-15:]:
            arg_expr = f"&{glob_name}.socket"
        elif "socket" in sig_str.lower() and "*" in mc.split(glob_name)[0][-15:]:
            arg_expr = f"&{glob_name}->socket"
        call_line = f"{send_fn}({arg_expr}, cmd);"
    else:
        call_line = f"{send_fn}(cmd);"

    c_bridge = f"""
#include "Socket.h"
EMSCRIPTEN_KEEPALIVE void rr_exec_shop_cmd(const char *cmd) {{
    if (!cmd) return;
    {call_line}
}}
"""
else:
    # Прямая упаковка пакета rr_serverbound_chat в сокет из Socket.c
    m_ws_fn = re.search(r"void\s+([a-zA-Z0-9_]*send[a-zA-Z0-9_]*)\s*\(\s*struct\s+rr_socket\s*\*\s*[a-zA-Z0-9_]+\s*,\s*(?:const\s+)?(?:void|uint8_t|char)\s*\*", sock_h + "\n" + sock_c)
    ws_fn = m_ws_fn.group(1) if m_ws_fn else ""
    print(f"[INFO] send_fn={send_fn}, sig={sig_str}, ws_fn={ws_fn}, glob={glob_type} {glob_name}")
    # Выведем Chat.c вокруг Enter / rr_serverbound_chat, если автоматический поиск не нашёл
    m_ctx = re.search(r".{0,300}rr_serverbound_chat.{0,400}", chat_c + "\n" + sock_c, re.DOTALL)
    if m_ctx:
        print("=== CHAT PACKET CONTEXT ===")
        print(m_ctx.group(0))

if c_bridge and "rr_exec_shop_cmd" not in mc:
    mc = re.sub(r"(int\s+main\s*\()", c_bridge + r"\n\1", mc, count=1)
    mc = mc.replace(
        "window.rrMenuCmd = function(cmd) {",
        "window.rrMenuCmd = function(cmd) {\n            if (typeof Module !== 'undefined' && Module.ccall) { Module.ccall('rr_exec_shop_cmd', null, ['string'], [cmd]); }"
    )
    with open("Client/Main.c", "w", encoding="utf-8") as f:
        f.write(mc)
    print(f"[OK] Прямой вызов C-функции {send_fn} привязан!")

# 3. Также перехватываем входящие пакеты чата в Socket.c, чтобы баланс R и текст квеста обновлялись мгновенно!
if "rrSetBalance" not in sock_c and "rr_clientbound_chat" in sock_c:
    hook_recv = """
        if (strstr((const char *)data, "Баланс:") || strstr((const char *)data, "Квест:")) {
            EM_ASM({
                var s = UTF8ToString($0);
                var mb = s.match(/Баланс:\\s*(\\d+)\\s*R/);
                if (mb) { var el = document.getElementById('rr-r-bal'); if (el) el.textContent = 'R: ' + mb; }
                var mq = s.match(/Квест:[^\\n\\r]+/);
                if (mq) { var qe = document.getElementById('rr-q-info'); if (qe) qe.textContent = mq; }
                var st = document.getElementById('rr-m-status');
                if (st && s.indexOf('R') !== -1) st.textContent = s.replace(/^[^\\x20-\\x7EА-Яа-яЁё]+/, '');
            }, data);
        }
"""
    if "<emscripten.h>" not in sock_c:
        sock_c = "#include <emscripten.h>\n" + sock_c
    sock_c = re.sub(r"(case\s+rr_clientbound_chat\s*:)", r"\1\n" + hook_recv, sock_c, count=1)
    with open("Client/Socket.c", "w", encoding="utf-8") as f:
        f.write(sock_c)
    print("[OK] Перехват ответов [Shop] в Socket.c добавлен!")
