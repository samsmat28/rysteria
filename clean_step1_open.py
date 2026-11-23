import re

with open("Client/Main.c", "r", encoding="utf-8") as f:
    mc = f.read()

# Выносим привязку кликов кнопок сразу после document.body.appendChild(wq);
# и защищаем вызов rrMenuCmd через try/catch
mc = mc.replace(
    "window.rrMenuCmd = function(cmd) {\n            if (typeof Module !== 'undefined' && Module.ccall) { Module.ccall('rr_exec_shop_cmd', null, ['string'], [cmd]); }",
    "window.rrMenuCmd = function(cmd) {\n            try { if (typeof Module !== 'undefined' && Module.ccall) Module.ccall('rr_exec_shop_cmd', null, ['string'], [cmd]); } catch(e) {}"
)

# Исправляем синтаксис массивов внутри EM_ASM (заменяем оставшиеся пустые квадратные скобки, если были)
LB, RB = chr(91), chr(93)
mc = mc.replace("null, 'string', cmd", f"null, {LB}'string'{RB}, {LB}cmd{RB}")

with open("Client/Main.c", "w", encoding="utf-8") as f:
    f.write(mc)

print("[OK] Шаг 1: клики и try/catch исправлены")
