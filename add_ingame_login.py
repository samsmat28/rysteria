# 1. MasterServer/main.js: добавляем маршрут /api/local-login
with open("MasterServer/main.js", "r", encoding="utf-8") as f:
    ms = f.read()

target_404 = 'app.use((req, res) => {\n    res.status(404).send("404 Not Found\\n");\n});'
login_route = """app.get("/api/local-login", (req, res) => {
    const username = String(req.query.username || "").trim().slice(0, 24);
    const password = String(req.query.password || "").trim().slice(0, 64);
    const curUuid = String(req.query.uuid || "").trim();
    const curToken = String(req.query.token || "").trim();
    if (username.length < 3 || password.length < 3) {
        return res.json({ ok: false, error: "Логин и пароль должны быть от 3 символов" });
    }
    if (!database.local_users) database.local_users = {};
    const key = username.toLowerCase();
    const existing = database.local_users[key];
    if (existing) {
        if (existing.password !== password) {
            return res.json({ ok: false, error: "Неверный пароль!" });
        }
        return res.json({ ok: true, uuid: existing.uuid, token: existing.token, username: existing.username, mode: "login" });
    } else {
        if (!curUuid || !curToken) {
            return res.json({ ok: false, error: "Сначала перезагрузите игру" });
        }
        database.local_users[key] = { username, password, uuid: curUuid, token: curToken };
        if (database.accounts && !database.accounts.includes(username)) database.accounts.push(username);
        changed = true;
        saveDatabaseToFile();
        return res.json({ ok: true, uuid: curUuid, token: curToken, username, mode: "register" });
    }
});

""" + target_404

assert target_404 in ms, "Не найден обработчик 404 в MasterServer/main.js"
if "/api/local-login" not in ms:
    ms = ms.replace(target_404, login_route, 1)
    with open("MasterServer/main.js", "w", encoding="utf-8") as f:
        f.write(ms)

# 2. Client/Oauth2.c: открываем красивое встроенное окно логина/регистрации вместо внешнего Discord
with open("Client/Oauth2.c", "r", encoding="utf-8") as f:
    oa = f.read()

old_fn_start = "void rr_discord_oauth2_link_account() {"
new_modal_js = """void rr_discord_oauth2_link_account() {
    EM_ASM({
        if (document.getElementById("rr-auth-modal")) return;
        const overlay = document.createElement("div");
        overlay.id = "rr-auth-modal";
        overlay.style.cssText = "position:fixed;inset:0;background:rgba(0,0,0,0.65);display:flex;align-items:center;justify-content:center;z-index:99999;font-family:Ubuntu,sans-serif;";
        overlay.innerHTML = `
            <div style="background:#5a4636;border:4px solid #3d2e22;border-radius:10px;padding:22px 26px;width:320px;color:#fff;box-shadow:0 10px 30px rgba(0,0,0,0.6);text-align:center;">
                <h2 style="margin:0 0 8px;font-size:22px;text-shadow:0 2px 0 #000;">Rysteria Account</h2>
                <p style="margin:0 0 14px;font-size:13px;color:#e6d5c3;">Вход или регистрация для сохранения прогресса</p>
                <input id="rr-auth-user" placeholder="Логин (от 3 символов)" style="width:100%;box-sizing:border-box;padding:9px 10px;margin-bottom:10px;border-radius:6px;border:2px solid #3d2e22;font-size:15px;outline:none;">
                <input id="rr-auth-pass" type="password" placeholder="Пароль (от 3 символов)" style="width:100%;box-sizing:border-box;padding:9px 10px;margin-bottom:10px;border-radius:6px;border:2px solid #3d2e22;font-size:15px;outline:none;">
                <div id="rr-auth-err" style="min-height:18px;color:#ff8787;font-size:13px;margin-bottom:10px;"></div>
                <div style="display:flex;gap:10px;justify-content:center;">
                    <button id="rr-auth-submit" style="flex:1;padding:9px;background:#51cf66;border:2px solid #2b8a3e;border-radius:6px;color:#fff;font-weight:bold;font-size:15px;cursor:pointer;">Войти / Создать</button>
                    <button id="rr-auth-close" style="padding:9px 14px;background:#ff6b6b;border:2px solid #c92a2a;border-radius:6px;color:#fff;font-weight:bold;font-size:15px;cursor:pointer;">Отмена</button>
                </div>
            </div>`;
        document.body.appendChild(overlay);
        document.getElementById("rr-auth-close").onclick = () => overlay.remove();
        document.getElementById("rr-auth-submit").onclick = async () => {
            const u = document.getElementById("rr-auth-user").value.trim();
            const p = document.getElementById("rr-auth-pass").value.trim();
            const err = document.getElementById("rr-auth-err");
            const curUuid = window.localStorage["rivet_account_uuid"] || "";
            const curToken = window.localStorage["DO_NOT_SHARE_account_token"] || "";
            try {
                const base = window.location.port === "8080" ? (window.location.protocol + "//" + window.location.hostname + ":3000") : "";
                const res = await fetch(`${base}/api/local-login?username=${encodeURIComponent(u)}&password=${encodeURIComponent(p)}&uuid=${encodeURIComponent(curUuid)}&token=${encodeURIComponent(curToken)}`);
                const data = await res.json();
                if (!data.ok) { err.textContent = data.error || "Ошибка входа"; return; }
                window.localStorage["rivet_account_uuid"] = data.uuid;
                window.localStorage["DO_NOT_SHARE_account_token"] = data.token;
                window.localStorage["rr_local_username"] = data.username;
                window.location.reload();
            } catch (e) { err.textContent = "Сервер недоступен"; }
        };
    });
    return;
"""

assert old_fn_start in oa, "Не найдена функция rr_discord_oauth2_link_account в Client/Oauth2.c"
if "rr-auth-modal" not in oa:
    oa = oa.replace(old_fn_start, new_modal_js, 1)
    with open("Client/Oauth2.c", "w", encoding="utf-8") as f:
        f.write(oa)

print("Встроенный логин и регистрация успешно добавлены!")
