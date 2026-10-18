"""
INTERFAZ WEB - Finance

Abre en el navegador:
  - En tu PC:      http://127.0.0.1:5000
  - En el servidor: http://IP_DEL_SERVIDOR  (detrás de nginx)

Configuración por variables de entorno o archivo .env (ver .env.example):
  FINANCE_PASSWORD  contraseña para entrar (obligatoria si se expone a internet)
  HOST              127.0.0.1 (solo esta PC) o 0.0.0.0 (cualquier equipo de la red)
  PORT              puerto, por defecto 5000
"""

from __future__ import annotations

import hmac
import os
import secrets
import sys
import threading
import time
from collections import deque
from datetime import datetime, timedelta, timezone
from functools import wraps
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def load_env_file(path: Path) -> None:
    """Lee un archivo .env sencillo (CLAVE=valor) sin dependencias extra."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key.strip(), value)


load_env_file(BASE_DIR / ".env")

from flask import Flask, jsonify, redirect, render_template, request, session, url_for  # noqa: E402

from portfolio import PortfolioStore, get_live_price, get_price_history  # noqa: E402

try:
    import config
    DB_PATH = getattr(config, "RUTA_BD", None)
    HORIZONTE = getattr(config, "HORIZONTE_DIAS", 30)
except Exception:  # pragma: no cover
    DB_PATH, HORIZONTE = None, 30

PASSWORD = os.environ.get("FINANCE_PASSWORD", "")
HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", "5000"))


def _secret_key() -> str:
    key = os.environ.get("SECRET_KEY")
    if key:
        return key
    f = BASE_DIR / ".secret_key"
    if f.exists():
        return f.read_text().strip()
    key = secrets.token_hex(32)
    f.write_text(key)
    return key


app = Flask(__name__)
app.config.update(
    SECRET_KEY=_secret_key(),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.environ.get("COOKIE_SECURE", "0") == "1",
    PERMANENT_SESSION_LIFETIME=timedelta(days=30),
)

store = PortfolioStore(DB_PATH)

# ─────────────────────────────────────────────────────────────────────────────
# Login
# ─────────────────────────────────────────────────────────────────────────────

_failed: dict = {}  # ip -> [intentos, hasta_cuando_bloqueado]


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if PASSWORD and not session.get("ok"):
            if request.path.startswith("/api/"):
                return jsonify(error="Sesión expirada, vuelve a entrar"), 401
            return redirect(url_for("login"))
        return fn(*args, **kwargs)
    return wrapper


def json_only(fn):
    """Las acciones que modifican datos solo aceptan JSON (protege contra formularios de otros sitios)."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if request.method == "POST" and not request.is_json:
            return jsonify(error="Se esperaba JSON"), 415
        return fn(*args, **kwargs)
    return wrapper


@app.route("/login", methods=["GET", "POST"])
def login():
    if not PASSWORD:
        return redirect(url_for("index"))
    ip = request.headers.get("X-Forwarded-For", request.remote_addr or "").split(",")[0].strip()
    error = None
    tries, until = _failed.get(ip, [0, 0])
    if request.method == "POST":
        if time.time() < until:
            error = "Demasiados intentos. Espera unos minutos."
        elif hmac.compare_digest(request.form.get("password", ""), PASSWORD):
            session.clear()
            session["ok"] = True
            session.permanent = True
            _failed.pop(ip, None)
            return redirect(url_for("index"))
        else:
            tries += 1
            until = time.time() + 300 if tries >= 5 else 0
            _failed[ip] = [0 if until else tries, until]
            error = "Contraseña incorrecta."
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login") if PASSWORD else url_for("index"))


# ─────────────────────────────────────────────────────────────────────────────
# Páginas
# ─────────────────────────────────────────────────────────────────────────────


@app.route("/")
@login_required
def index():
    return render_template("index.html", horizonte=HORIZONTE, has_password=bool(PASSWORD))


# ─────────────────────────────────────────────────────────────────────────────
# API: inversiones
# ─────────────────────────────────────────────────────────────────────────────


def _num(value):
    if value in (None, ""):
        return None
    try:
        return float(str(value).replace(",", ""))
    except ValueError:
        raise ValueError(f"Valor numérico inválido: {value}")


@app.get("/api/investments")
@login_required
def api_investments():
    items = [store.with_performance(i) for i in store.list()]
    return jsonify(items=items, summary=store.portfolio_summary(items),
                   server_time=datetime.now(timezone.utc).isoformat())


@app.post("/api/investments")
@login_required
@json_only
def api_add_investment():
    data = request.get_json() or {}
    try:
        inv = store.add(
            symbol=data.get("symbol", ""),
            entry_price=_num(data.get("entry_price")),
            shares=_num(data.get("shares")),
            amount=_num(data.get("amount")),
            recommendation_id=int(data["recommendation_id"]) if data.get("recommendation_id") else None,
            notes=data.get("notes"),
        )
    except ValueError as e:
        return jsonify(error=str(e)), 400
    return jsonify(item=store.with_performance(inv))


@app.post("/api/investments/<int:inv_id>/close")
@login_required
@json_only
def api_close(inv_id):
    data = request.get_json() or {}
    try:
        inv = store.close(inv_id, _num(data.get("exit_price")))
    except ValueError as e:
        return jsonify(error=str(e)), 400
    return jsonify(item=store.with_performance(inv))


@app.post("/api/investments/<int:inv_id>/reopen")
@login_required
@json_only
def api_reopen(inv_id):
    return jsonify(item=store.with_performance(store.reopen(inv_id)))


@app.post("/api/investments/<int:inv_id>/delete")
@login_required
@json_only
def api_delete(inv_id):
    store.delete(inv_id)
    return jsonify(ok=True)


@app.get("/api/investments/<int:inv_id>/history")
@login_required
def api_history(inv_id):
    inv = store.get(inv_id)
    if not inv:
        return jsonify(error="No existe"), 404
    marked = datetime.fromisoformat(inv["marked_at"])
    points = get_price_history(inv["symbol"], marked)
    if inv.get("closed_at"):
        closed = datetime.fromisoformat(inv["closed_at"])
        points = [p for p in points if datetime.fromisoformat(p["t"]) <= closed + timedelta(days=1)]
    return jsonify(points=points, entry_price=inv["entry_price"], marked_at=inv["marked_at"])


@app.get("/api/price/<symbol>")
@login_required
def api_price(symbol):
    live = get_live_price(symbol)
    if not live:
        return jsonify(error=f"No se encontró precio para {symbol.upper()}"), 404
    return jsonify(symbol=symbol.upper(), **live)


# ─────────────────────────────────────────────────────────────────────────────
# API: recomendaciones generadas por el analizador
# ─────────────────────────────────────────────────────────────────────────────


@app.get("/api/recommendations")
@login_required
def api_recommendations():
    return jsonify(items=store.list_recommendations(),
                   summary=store.recs.performance_summary())


# ─────────────────────────────────────────────────────────────────────────────
# API: ejecutar análisis en segundo plano
# ─────────────────────────────────────────────────────────────────────────────

_job = {"running": False, "log": deque(maxlen=400), "started_at": None,
        "finished_at": None, "result": None, "error": None}
_job_lock = threading.Lock()


def _run_job(rapido: bool):
    import analisis_programado

    def log(msg):
        _job["log"].append(str(msg))

    try:
        _job["result"] = analisis_programado.run(rapido=rapido, log=log)
    except Exception as e:  # pragma: no cover
        _job["error"] = str(e)
        log(f"ERROR: {e}")
    finally:
        _job["running"] = False
        _job["finished_at"] = datetime.now(timezone.utc).isoformat()


@app.post("/api/analysis/run")
@login_required
@json_only
def api_run_analysis():
    rapido = bool((request.get_json() or {}).get("rapido"))
    with _job_lock:
        if _job["running"]:
            return jsonify(error="Ya hay un análisis en curso"), 409
        _job.update(running=True, started_at=datetime.now(timezone.utc).isoformat(),
                    finished_at=None, result=None, error=None)
        _job["log"].clear()
        threading.Thread(target=_run_job, args=(rapido,), daemon=True).start()
    return jsonify(ok=True)


@app.get("/api/analysis/status")
@login_required
def api_analysis_status():
    return jsonify(running=_job["running"], log=list(_job["log"])[-60:],
                   started_at=_job["started_at"], finished_at=_job["finished_at"],
                   result=_job["result"], error=_job["error"])


@app.post("/api/recommendations/evaluate")
@login_required
@json_only
def api_evaluate():
    results = store.recs.evaluate_due()
    return jsonify(evaluated=len([r for r in results if r.get("status") == "evaluated"]))


# ─────────────────────────────────────────────────────────────────────────────


def main():
    if not PASSWORD and HOST not in ("127.0.0.1", "localhost"):
        print("❌ Estás abriendo la app a la red (HOST=%s) sin contraseña." % HOST)
        print("   Define FINANCE_PASSWORD en el archivo .env y vuelve a intentar.")
        sys.exit(1)

    print("=" * 70)
    print("  📈 Finance - Interfaz web")
    print(f"  Abre en el navegador: http://{'127.0.0.1' if HOST == '0.0.0.0' else HOST}:{PORT}")
    print(f"  Contraseña: {'activada' if PASSWORD else 'desactivada (solo uso local)'}")
    print("  Para detenerla: Ctrl + C")
    print("=" * 70)

    try:
        from waitress import serve
        serve(app, host=HOST, port=PORT, threads=8)
    except ImportError:
        app.run(host=HOST, port=PORT)


if __name__ == "__main__":
    main()
