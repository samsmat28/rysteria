with open("Client/Game.h", "r", encoding="utf-8") as f:
    gh = f.read()
if "rr_game_menu_shop" not in gh:
    gh = gh.replace("rr_game_menu_account,", "rr_game_menu_account,\n    rr_game_menu_shop,\n    rr_game_menu_quests,")
    with open("Client/Game.h", "w", encoding="utf-8") as f:
        f.write(gh)

with open("Client/Ui/Ui.h", "r", encoding="utf-8") as f:
    uh = f.read()
if "rr_ui_shop_toggle_button_init" not in uh:
    uh += "\nextern struct rr_ui_element *rr_ui_shop_toggle_button_init();\nextern struct rr_ui_element *rr_ui_shop_container_init(struct rr_game *);\nextern struct rr_ui_element *rr_ui_quests_toggle_button_init();\nextern struct rr_ui_element *rr_ui_quests_container_init(struct rr_game *);\n"
    with open("Client/Ui/Ui.h", "w", encoding="utf-8") as f:
        f.write(uh)

with open("Client/CMakeLists.txt", "r", encoding="utf-8") as f:
    cm = f.read()
if "Ui/TitleScreen/Shop.c" not in cm:
    cm = cm.replace("Ui/TitleScreen/Crafting.c", "Ui/TitleScreen/Crafting.c\n    Ui/TitleScreen/Shop.c")
    with open("Client/CMakeLists.txt", "w", encoding="utf-8") as f:
        f.write(cm)

with open("Client/Game.c", "r", encoding="utf-8") as f:
    gc = f.read()
if "rr_ui_shop_toggle_button_init" not in gc:
    gc = gc.replace("rr_ui_crafting_toggle_button_init(),", "rr_ui_crafting_toggle_button_init(),\n                            rr_ui_shop_toggle_button_init(),\n                            rr_ui_quests_toggle_button_init(),")
    gc = gc.replace("rr_ui_container_add_element(this->window, rr_ui_container_add_element(rr_ui_crafting_container_init(this), close_menu_button_init(25))->container);", "rr_ui_container_add_element(this->window, rr_ui_container_add_element(rr_ui_crafting_container_init(this), close_menu_button_init(25))->container);\n    rr_ui_container_add_element(this->window, rr_ui_container_add_element(rr_ui_shop_container_init(this), close_menu_button_init(25))->container);\n    rr_ui_container_add_element(this->window, rr_ui_container_add_element(rr_ui_quests_container_init(this), close_menu_button_init(25))->container);")
    with open("Client/Game.c", "w", encoding="utf-8") as f:
        f.write(gc)

print("[OK] Шаг 1 выполнен")
