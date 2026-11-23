import re

with open("Client/Ui/Ui.h", "r", encoding="utf-8") as f:
    uh = f.read()

m = re.search(r"struct\s+rr_ui_element\s*\*\s*rr_ui_container_init\s*\(([^)]*)\)", uh)
params = m.group(1) if m else ""
args = ", ".join(["0"] * len([p for p in params.split(",") if p.strip()])) if params.strip() else ""

with open("Client/Ui/TitleScreen/Shop.c", "r", encoding="utf-8") as f:
    sc = f.read()

sc = sc.replace(
    "struct rr_ui_element *rr_ui_shop_container_init(struct rr_game *g) {\n    (void)g; struct rr_ui_element *this = rr_ui_element_init();",
    f"struct rr_ui_element *rr_ui_shop_container_init(struct rr_game *g) {{\n    (void)g; struct rr_ui_element *this = rr_ui_container_init({args});"
)
sc = sc.replace(
    "struct rr_ui_element *rr_ui_quests_container_init(struct rr_game *g) {\n    (void)g; struct rr_ui_element *this = rr_ui_element_init();",
    f"struct rr_ui_element *rr_ui_quests_container_init(struct rr_game *g) {{\n    (void)g; struct rr_ui_element *this = rr_ui_container_init({args});"
)

with open("Client/Ui/TitleScreen/Shop.c", "w", encoding="utf-8") as f:
    f.write(sc)

print(f"[OK] Контейнеры переведены на rr_ui_container_init({args})")
