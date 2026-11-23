import glob

with open("Client/Ui/Ui.h", "r", encoding="utf-8") as f:
    lines = f.read().splitlines()
    print("=== Ui.h (конец) ===")
    print("\n".join(lines[-45:]))

for fn in glob.glob("Client/**/*.[ch]", recursive=True):
    with open(fn, "r", encoding="utf-8") as f:
        txt = f.read()
    if "rr_game_menu_account" in txt:
        print(f"=== {fn} ===")
        for i, l in enumerate(txt.splitlines()):
            if "rr_game_menu_account" in l or "account_container" in l:
                print(f"  L{i+1}: {l}")
