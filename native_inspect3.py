with open("Client/Game.h", "r", encoding="utf-8") as f:
    gh = f.read()
for line in gh.splitlines():
    if "menu" in line.lower() or "top_ui" in line.lower() or "changelog" in line.lower() or "account" in line.lower():
        print("Game.h:", line)

with open("Client/Ui/Engine.c", "r", encoding="utf-8") as f:
    print("=== Engine.c ===")
    print(f.read()[:1800])
