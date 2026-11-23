// Copyright (C) 2024 Paul Johnson
// Copyright (C) 2024-2025 Maxim Nesterov

// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as
// published by the Free Software Foundation, either version 3 of the
// License, or (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Affero General Public License for more details.

// You should have received a copy of the GNU Affero General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.

#include <string.h>

#include <Client/Game.h>
#include <Client/Storage.h>

void rr_discord_oauth2_read_data(void *_this, void *_decoder) {
    struct rr_game *this = _this;
    struct proto_bug *decoder = _decoder;
    proto_bug_read_string(decoder, this->rivet_account.uuid,
                          sizeof this->rivet_account.uuid, "uuid");
    proto_bug_read_string(decoder, this->rivet_account.token,
                          sizeof this->rivet_account.token, "token");
    proto_bug_read_string(decoder, this->rivet_account.name,
                          sizeof this->rivet_account.name, "name");
    this->rivet_account.code[0] = 0;
    if (this->rivet_account.name[0])
        this->account_linked = 1;
    else
        strcpy(this->rivet_account.name, "Guest");
    rr_local_storage_store_string("rivet_account_uuid", this->rivet_account.uuid);
    rr_local_storage_store_string("DO_NOT_SHARE_account_token", this->rivet_account.token);
}

void rr_discord_oauth2_link_account() {
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
                const base = window.location.hostname.match(/-808[01]\./) ? (window.location.protocol + "//" + window.location.hostname.replace(/-808[01]\./, "-55554.")) : ((window.location.port === "8080" || window.location.port === "8081") ? (window.location.protocol + "//" + window.location.hostname + ":55554") : "");
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

    EM_ASM({
        const state = crypto.randomUUID();
        const url = new URL("https://discord.com/oauth2/authorize");
        url.searchParams.set("client_id", "1453525695228678349");
        url.searchParams.set("response_type", "code");
        url.searchParams.set("redirect_uri", window.location.origin + window.location.pathname);
        url.searchParams.set("scope", "identify guilds.join");
        url.searchParams.set("state", state);
        window.localStorage["oauth2_state"] = state;
        window.onbeforeunload = null;
        window.location.href = url;
    });
}

void rr_discord_oauth2_on_log_in(char *uuid, char *token, char *code, void *captures) {
    struct rr_game *this = captures;
    strcpy(this->rivet_account.uuid, uuid);
    strcpy(this->rivet_account.token, token);
    strcpy(this->rivet_account.code, code);
    free(uuid);
    free(token);
    free(code);
    rr_game_connect_socket(this);
}

void rr_discord_oauth2_init(void *captures) {
    EM_ASM({
        const url = new URL(window.location);
        let saveId = url.searchParams.get("uuid") || globalThis['localStorage'].getItem("rr_save_id") || globalThis['localStorage'].getItem("rivet_account_uuid") || "";
        if (!saveId) {
            saveId = "RR-" + Math.random().toString(36).slice(2, 10).toUpperCase();
        }
        globalThis['localStorage'].setItem("rr_save_id", saveId);
        globalThis['localStorage'].setItem("rivet_account_uuid", saveId);
        const uuid = saveId;
        const token = window.localStorage["DO_NOT_SHARE_account_token"] || "";
        const _code = url.searchParams.get("code") || "";
        const _state = url.searchParams.get("state") || "";
        const state = window.localStorage["oauth2_state"];
        const code = (state && _state && state === _state) ? _code : "";
        url.searchParams.delete("uuid");
        url.searchParams.delete("code");
        url.searchParams.delete("state");
        url.searchParams.delete("error");
        url.searchParams.delete("error_description");
        window.history.replaceState(null, null, url);
        delete window.localStorage["oauth2_state"];
        const $uuid = _malloc(uuid.length + 1);
        const $token = _malloc(token.length + 1);
        const $code = _malloc(code.length + 1);
        HEAPU8.set(new TextEncoder().encode(uuid), $uuid);
        HEAPU8.set(new TextEncoder().encode(token), $token);
        HEAPU8.set(new TextEncoder().encode(code), $code);
        HEAPU8[$uuid + uuid.length] = 0;
        HEAPU8[$token + token.length] = 0;
        HEAPU8[$code + code.length] = 0;
        _rr_discord_oauth2_on_log_in($uuid, $token, $code, $0);
    }, captures);
}
