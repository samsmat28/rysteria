with open("MasterServer/main.js", "r", encoding="utf-8") as f:
    ms = f.read()

LB, RB = chr(91), chr(93)
ms = ms.replace("const SELL_PRICES =;", f"const SELL_PRICES = {LB}5,15,40,120,350,1000,3000,9000,25000,75000,200000{RB};")
ms = ms.replace("const Q_REWARDS =;", f"const Q_REWARDS = {LB}40,100,250,700,2000,6000,18000,50000,150000,400000,1000000{RB};")
ms = ms.replace("/^[a-zA-Z0-9_-]{1,32}$/", "/^[a-zA-Z0-9_-]{1,64}$/")

with open("MasterServer/main.js", "w", encoding="utf-8") as f:
    f.write(ms)
