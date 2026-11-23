with open("Client/Ui/TitleScreen/Changelog.c", "r", encoding="utf-8") as f:
    print("=== Changelog.c ===")
    print("\n".join(f.read().splitlines()[:60]))

with open("Client/Ui/TitleScreen/Account.c", "r", encoding="utf-8") as f:
    print("=== Account.c (первые 35 строк) ===")
    print("\n".join(f.read().splitlines()[:35]))
