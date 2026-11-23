with open("Client/Ui/Ui.h", "r", encoding="utf-8") as f:
    print("=== Ui.h (строки 35-130) ===")
    print("\n".join(f.read().splitlines()[35:130]))
with open("Client/Ui/Button.c", "r", encoding="utf-8") as f:
    print("=== Button.c (первые 35 строк) ===")
    print("\n".join(f.read().splitlines()[:35]))
