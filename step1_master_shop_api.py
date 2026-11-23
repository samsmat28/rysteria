import os, glob

# 1. Ищем файл MasterServer (обычно MasterServer/main.js)
ms_file = "MasterServer/main.js" if os.path.exists("MasterServer/main.js") else (glob.glob("MasterServer/*.js") + [None])[0]
print("[INFO] MasterServer:", ms_file)

with open(ms_file, "r", encoding="utf-8") as f:
    code = f.read()

api_addon = """
// === Rysteria Web Shop & Quests API ===
(function() {
    const http = require('http');
    const fs = require('fs');
    const path = require('path');

    const SELL_PRICES =;
    const Q_REWARDS =;
    const RARITIES = ["Common","Uncommon","Rare","Epic","Legendary","Mythic","Ultra","Super","Omega","Hyper","Gods"];

    function findSav(user) {
        if (!/^[a-zA-Z0-9_-]{1,32}$/.test(user || '')) return null;
        const dirs = [
            path.join(__dirname, '..', 'Server', 'build-default', 'accounts'),
            path.join(__dirname, '..', 'Server', 'build-pvp', 'accounts'),
            path.join(__dirname, '..', 'accounts')
        ];
        for (const d of dirs) {
            const p = path.join(d, user + '.sav');
            if (fs.existsSync(p)) return p;
        }
        return null;
    }

    // Парсим конец .sav: [inv: 63*11*4 = 2772 байт][exp: 8][r_coins: 8][q_rar: 1][q_tgt: 2][q_prg: 2]
    function readAccount(savPath) {
        const buf = fs.readFileSync(savPath);
        const invBytes = 63 * 11 * 4;
        const tailLen = invBytes + 8 + 8 + 5;
        if (buf.length < tailLen) return null;
        const base = buf.length - tailLen;
        const r_coins = Number(buf.readBigUInt64LE(base + invBytes + 8));
        const q_rar = buf.readUInt8(base + invBytes + 16);
        const q_tgt = buf.readUInt16LE(base + invBytes + 17);
        const q_prg = buf.readUInt16LE(base + invBytes + 19);
        const inv = [];
        for (let p = 1; p < 63; p++) {
            for (let r = 0; r < 11; r++) {
                const cnt = buf.readUInt32LE(base + (p * 11 + r) * 4);
                if (cnt > 0) inv.push({ pid: p, rid: r, count: cnt });
            }
        }
        return { buf, base, invBytes, r_coins, q_rar, q_tgt, q_prg, inv };
    }

    function writeAccount(savPath, acc) {
        const { buf, base, invBytes } = acc;
        buf.writeBigUInt64LE(BigInt(acc.r_coins), base + invBytes + 8);
        buf.writeUInt8(acc.q_rar, base + invBytes + 16);
        buf.writeUInt16LE(acc.q_tgt, base + invBytes + 17);
        buf.writeUInt16LE(acc.q_prg, base + invBytes + 19);
        fs.writeFileSync(savPath, buf);
    }

    const shopSrv = http.createServer((req, res) => {
        res.setHeader('Access-Control-Allow-Origin', '*');
        res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
        res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
        if (req.method === 'OPTIONS') { res.writeHead(204); return res.end(); }

        const u = new URL(req.url, 'http://localhost');
        const user = u.searchParams.get('user') || '';
        const action = u.searchParams.get('action') || 'status';
        const pid = parseInt(u.searchParams.get('pid') || '0', 10);
        const rid = parseInt(u.searchParams.get('rid') || '0', 10);

        res.setHeader('Content-Type', 'application/json; charset=utf-8');
        const sav = findSav(user);
        if (!sav) {
            res.writeHead(404);
            return res.end(JSON.stringify({ ok: false, msg: 'Аккаунт не найден! Сначала зайди в игру и введи /register или /login в чат.' }));
        }
        const acc = readAccount(sav);
        if (!acc) {
            res.writeHead(500);
            return res.end(JSON.stringify({ ok: false, msg: 'Ошибка чтения .sav (сделай /save в игре)' }));
        }

        let msg = 'OK';
        if (action === 'buy' && pid >= 1 && pid < 63 && rid >= 0 && rid < 11) {
            const cost = (pid === 62 && rid === 3) ? 100 : (SELL_PRICES[rid] * 2);
            if (acc.r_coins >= cost) {
                acc.r_coins -= cost;
                const off = acc.base + (pid * 11 + rid) * 4;
                acc.buf.writeUInt32LE(acc.buf.readUInt32LE(off) + 1, off);
                writeAccount(sav, acc);
                msg = 'Куплено за ' + cost + ' R! Перезайди в игру (/login), чтобы забрать в инвентарь.';
            } else {
                msg = 'Недостаточно R! Нужно ' + cost + ' R.';
            }
        } else if (action === 'sell' && pid >= 1 && pid < 63 && rid >= 0 && rid < 11) {
            const off = acc.base + (pid * 11 + rid) * 4;
            const cur = acc.buf.readUInt32LE(off);
            if (cur > 0) {
                acc.buf.writeUInt32LE(cur - 1, off);
                acc.r_coins += SELL_PRICES[rid];
                writeAccount(sav, acc);
                msg = 'Продано! +' + SELL_PRICES[rid] + ' R';
            } else {
                msg = 'У вас нет этого лепестка!';
            }
        } else if (action === 'claim') {
            if (acc.q_tgt > 0 && acc.q_prg >= acc.q_tgt) {
                const r = acc.q_rar < 11 ? acc.q_rar : 0;
                acc.r_coins += Q_REWARDS[r];
                acc.q_rar = (r + 1) % 7;
                acc.q_tgt = 5 + acc.q_rar * 2;
                acc.q_prg = 0;
                writeAccount(sav, acc);
                msg = 'Награда получена! +' + Q_REWARDS[r] + ' R';
            } else {
                msg = 'Квест ещё не выполнен (' + acc.q_prg + '/' + acc.q_tgt + ')';
            }
        }

        const fresh = readAccount(sav);
        const qr = fresh.q_rar < 11 ? fresh.q_rar : 0;
        res.writeHead(200);
        res.end(JSON.stringify({
            ok: true,
            msg,
            r_coins: fresh.r_coins,
            quest: { rarity: RARITIES[qr], progress: fresh.q_prg, target: fresh.q_tgt || 5, reward: Q_REWARDS[qr] },
            inventory: fresh.inv
        }));
    });
    shopSrv.listen(8085, () => console.log('[Rysteria Shop API] listening on 8085'));
})();
"""

if "Rysteria Shop API" not in code:
    code += "\n" + api_addon
    with open(ms_file, "w", encoding="utf-8") as f:
        f.write(code)
    print("[OK] API магазина добавлено в", ms_file)
