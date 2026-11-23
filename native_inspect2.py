with open("Client/Ui/Ui.h", "r", encoding="utf-8") as f:
    print("=== Ui.h ===")
    print(f.read()[:1500])

with open("Client/Ui/TitleScreen/Changelog.c", "r", encoding="utf-8") as f:
    lines = f.read().splitlines()
    print("=== Changelog.c (конец) ===")
    print("\n".join(lines[-45:]))

with open("Client/CMakeLists.txt", "r", encoding="utf-8") as f:
    print("=== CMakeLists.txt ===")
    print(f.read())
