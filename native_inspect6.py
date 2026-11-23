with open("Client/Ui/TitleScreen/Crafting.c", "r", encoding="utf-8") as f:
    lines = f.read().splitlines()
print("=== Crafting.c (начало и конец) ===")
print("\n".join(lines[:35]))
print("---")
print("\n".join(lines[-35:]))
