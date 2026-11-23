LB, RB = chr(91), chr(93)
with open("Server/Server.c", "r", encoding="utf-8") as f:
    sc = f.read()
sc = sc.replace("static const uint64_t sell_p =", f"static const uint64_t sell_p{LB}11{RB} =")
sc = sc.replace("static const uint64_t q_rew =", f"static const uint64_t q_rew{LB}11{RB} =")
with open("Server/Server.c", "w", encoding="utf-8") as f:
    f.write(sc)
