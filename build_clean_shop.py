import re

with open("Client/Ui/Text.c", "r", encoding="utf-8") as f:
    tc = f.read()
print("=== Text.c (первые 35 строк) ===")
print("\n".join(tc.splitlines()[:35]))
