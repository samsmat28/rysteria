with open("Client/Main.c", "r", encoding="utf-8") as f:
    mc = f.read()

LB, RB = chr(91), chr(93)
prices_str = f"var S = {LB}5, 15, 40, 120, 350, 1000, 3000, 9000, 25000, 75000, 200000{RB};"

mc = mc.replace("var S =;", prices_str)
mc = mc.replace("var S = [];", prices_str)

with open("Client/Main.c", "w", encoding="utf-8") as f:
    f.write(mc)

print("[OK] Массив цен S исправлен:", prices_str)
