with open("hook_hell_creek.py", "r", encoding="utf-8") as f:
    s = f.read()
s = s.replace("st = p_names\n", "st = next(iter(p_names))\n")
with open("hook_hell_creek.py", "w", encoding="utf-8") as f:
    f.write(s)
