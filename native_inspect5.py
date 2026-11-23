with open("Client/Game.c", "r", encoding="utf-8") as f:
    lines = f.read().splitlines()
for i, l in enumerate(lines):
    if "rr_ui_account_container_init" in l or "rr_ui_mob_gallery_toggle_button_init" in l:
        print(f"=== Game.c вокруг строки {i+1} ===")
        print("\n".join(lines[max(0, i-10):min(len(lines), i+25)]))
        break
