with open("Client/Main.c", "r", encoding="utf-8") as f:
    mc = f.read()

old_bind = """        document.getElementById('rr-m-shop').onclick = function() { ws.style.display = ws.style.display === 'flex' ? 'none' : 'flex'; wq.style.display = 'none'; window.rrMenuCmd('/balance'); };
        document.getElementById('rr-m-quest').onclick = function() { wq.style.display = wq.style.display === 'flex' ? 'none' : 'flex'; ws.style.display = 'none'; window.rrMenuCmd('/quest'); };"""

new_bind = """        var btnS = document.getElementById('rr-m-shop');
        var btnQ = document.getElementById('rr-m-quest');
        btnS.style.pointerEvents = 'auto';
        btnQ.style.pointerEvents = 'auto';
        btnS.onpointerdown = btnS.onclick = function(e) { e.stopPropagation(); ws.style.display = ws.style.display === 'flex' ? 'none' : 'flex'; wq.style.display = 'none'; window.rrMenuCmd('/balance'); };
        btnQ.onpointerdown = btnQ.onclick = function(e) { e.stopPropagation(); wq.style.display = wq.style.display === 'flex' ? 'none' : 'flex'; ws.style.display = 'none'; window.rrMenuCmd('/quest'); };"""

if old_bind in mc:
    mc = mc.replace(old_bind, new_bind)
    with open("Client/Main.c", "w", encoding="utf-8") as f:
        f.write(mc)
    print("[OK] Клики по кнопкам привязаны через onpointerdown")
else:
    print("[WARN] Блок привязки не найден, проверь строку в Client/Main.c")
