with open("Client/Ui/Text.c", "r", encoding="utf-8") as f:
    print("\n".join(f.read().splitlines()[35:55]))
with open("Client/InputData.h", "r", encoding="utf-8") as f:
    print("=== InputData.h ===")
    print(f.read()[:900])
