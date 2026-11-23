with open("Server/Server.c", "r", encoding="utf-8") as f:
    s = f.read()

s = s.replace("char cmd = {0}, user = {0}, pass = {0};", "char cmd[16] = {0}, user[32] = {0}, pass[32] = {0};")
s = s.replace("char path;", "char path[96];")
s = s.replace("char saved_pass = {0};", "char saved_pass[32] = {0};")

with open("Server/Server.c", "w", encoding="utf-8") as f:
    f.write(s)
print("Arrays fixed!")
