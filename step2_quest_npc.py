path = "Client/Renderer/RenderArena.c"
with open(path, "r", encoding="utf-8") as f:
    code = f.read()

npc_js = """
        // 4. Квестовый НПС-цветочек рядом с магазином (мир: x=170, y=-185)
        var npcX = 170.0;
        var npcY = -185.0;
        var inNpcZone = Math.hypot(camX - npcX, camY - npcY) <= 72.0;
        window.__rrInNpcZone = inNpcZone;

        ctx.save();
        ctx.translate(canvas.width * 0.5, canvas.height * 0.5);
        ctx.scale(zoom, zoom);
        ctx.translate(-camX, -camY);

        // Зона взаимодействия вокруг НПС
        ctx.fillStyle = inNpcZone ? 'rgba(126, 239, 109, 0.35)' : 'rgba(126, 239, 109, 0.16)';
        ctx.strokeStyle = '#7eef6d';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.arc(npcX, npcY, 58, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();

        // Тело цветочка-НПС (жёлтый круг с обводкой и милым личиком как у игрока)
        var t = performance.now() * 0.004;
        var bobY = Math.sin(t) * 2.5;
        ctx.fillStyle = '#ffe763';
        ctx.strokeStyle = '#cfb73c';
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.arc(npcX, npcY + bobY, 26, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();

        // Глазки и улыбка
        ctx.fillStyle = '#1f1f1f';
        ctx.beginPath();
        ctx.arc(npcX - 8, npcY - 5 + bobY, 3.5, 0, Math.PI * 2);
        ctx.arc(npcX + 8, npcY - 5 + bobY, 3.5, 0, Math.PI * 2);
        ctx.fill();

        // Блики в глазах
        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.arc(npcX - 9, npcY - 6.5 + bobY, 1.3, 0, Math.PI * 2);
        ctx.arc(npcX + 7, npcY - 6.5 + bobY, 1.3, 0, Math.PI * 2);
        ctx.fill();

        // Улыбочка
        ctx.strokeStyle = '#1f1f1f';
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        ctx.arc(npcX, npcY + 2 + bobY, 7, 0.15 * Math.PI, 0.85 * Math.PI);
        ctx.stroke();

        // Восклицательный знак и подпись над головой
        ctx.fillStyle = '#7eef6d';
        ctx.font = 'bold 16px Ubuntu, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('! КВЕСТЫ [R] !', npcX, npcY - 38 + bobY);

        ctx.restore();

        // Окно квестов при подходе к НПС-цветочку
        if (!window.__rrQuestModalInit) {
            window.__rrQuestModalInit = true;
            window.__rrQuestDismissed = false;

            var qm = document.createElement('div');
            qm.id = 'rr-quest-modal';
            qm.style.cssText = 'display:none;position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);width:420px;max-width:90vw;background:rgba(24,36,20,0.96);border:3px solid #7eef6d;border-radius:14px;z-index:10001;color:#fff;font-family:Ubuntu,sans-serif;flex-direction:column;overflow:hidden;box-shadow:0 10px 30px rgba(0,0,0,0.7);';
            qm.innerHTML =
                '<div style="display:flex;justify-content:space-between;align-items:center;padding:12px 16px;background:#162412;border-bottom:2px solid #4a7c3a;">' +
                    '<b style="color:#7eef6d;font-size:18px;">🌼 Охотник Rysteria</b>' +
                    '<button id="rr-close-quest" style="background:#8b2525;color:#fff;border:none;border-radius:6px;padding:2px 9px;cursor:pointer;">✕</button>' +
                '</div>' +
                '<div style="padding:16px;display:flex;flex-direction:column;gap:12px;">' +
                    '<div id="rr-quest-text" style="background:#121c0f;border:1px solid #4a7c3a;border-radius:8px;padding:12px;font-size:15px;color:#eaffdf;line-height:1.4;">Нажми «Обновить задание», чтобы увидеть текущую цель!</div>' +
                    '<div style="display:flex;gap:8px;">' +
                        '<button id="rr-q-check" style="flex:1;padding:10px;background:#3a6b2c;color:#fff;border:none;border-radius:8px;font-weight:700;cursor:pointer;">🔄 Обновить задание</button>' +
                        '<button id="rr-q-claim" style="flex:1;padding:10px;background:#d98a1c;color:#1a0f05;border:none;border-radius:8px;font-weight:700;cursor:pointer;">💰 Забрать награду R</button>' +
                    '</div>' +
                '</div>';
            document.body.appendChild(qm);

            document.getElementById('rr-close-quest').onclick = function() { window.__rrQuestDismissed = true; qm.style.display = 'none'; };
            document.getElementById('rr-q-check').onclick = function() { if (window.rrSendShopCmd) window.rrSendShopCmd('/quest'); };
            document.getElementById('rr-q-claim').onclick = function() { if (window.rrSendShopCmd) window.rrSendShopCmd('/claim'); };

            setInterval(function() {
                var txt = document.body ? document.body.innerText : '';
                var m = txt.match(/Квест:[^\n]+/g);
                if (m && m.length > 0) {
                    var el = document.getElementById('rr-quest-text');
                    if (el) el.textContent = m[m.length - 1];
                }
            }, 500);
        }

        var qModal = document.getElementById('rr-quest-modal');
        if (qModal) {
            if (window.__rrInNpcZone) {
                if (!window.__rrQuestDismissed && qModal.style.display !== 'flex') {
                    qModal.style.display = 'flex';
                    if (window.rrSendShopCmd) window.rrSendShopCmd('/quest');
                }
            } else {
                window.__rrQuestDismissed = false;
                qModal.style.display = 'none';
            }
        }
"""

if "window.__rrQuestModalInit" not in code:
    code = code.replace("    }, cam_x, cam_y, zoom);", npc_js + "\n    }, cam_x, cam_y, zoom);")
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)
    print("[OK] Квестовый НПС-цветочек встроен")
