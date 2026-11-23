with open("Client/Main.c", "r", encoding="utf-8") as f:
    mc = f.read()

capture_hook = """
        window.addEventListener('pointerdown', function(e) {
            var id = e.target && e.target.id;
            if (id === 'rr-m-shop') {
                e.stopImmediatePropagation();
                ws.style.display = (ws.style.display === 'flex') ? 'none' : 'flex';
                wq.style.display = 'none';
                window.rrMenuCmd('/balance');
            } else if (id === 'rr-m-quest') {
                e.stopImmediatePropagation();
                wq.style.display = (wq.style.display === 'flex') ? 'none' : 'flex';
                ws.style.display = 'none';
                window.rrMenuCmd('/quest');
            } else if (id === 'rr-x-shop') {
                ws.style.display = 'none';
            } else if (id === 'rr-x-quest') {
                wq.style.display = 'none';
            }
        }, true);
"""

if "addEventListener('pointerdown'" not in mc:
    mc = mc.replace("document.body.appendChild(wq);", "document.body.appendChild(wq);\n" + capture_hook)
    with open("Client/Main.c", "w", encoding="utf-8") as f:
        f.write(mc)
    print("[OK] Capture-перехватчик кликов добавлен на window")
