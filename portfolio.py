"""
Seguimiento de inversiones reales ("las que decidí invertir").

Guarda en la misma base SQLite (finance.db) una tabla `investments`:
- Cuando "marcas" una acción se guarda el precio de ese momento (precio de entrada).
- Al consultar, se descarga el precio actual y se calcula cuánto vas ganando o perdiendo.
- Puedes "cerrar" la inversión (cuando vendes) para congelar el resultado final.
"""

from __future__ import annotations

import sqlite3
import threading
import time
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional

from database import DEFAULT_DB_PATH, RecommendationStore

# ─────────────────────────────────────────────────────────────────────────────
# Precios (con caché para no saturar a Yahoo Finance)
# ─────────────────────────────────────────────────────────────────────────────

PRICE_CACHE_SECONDS = 60
HISTORY_CACHE_SECONDS = 300

_price_cache: Dict[str, tuple] = {}
_history_cache: Dict[tuple, tuple] = {}
_cache_lock = threading.Lock()


def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def get_live_price(symbol: str) -> Optional[Dict]:
    """
    Precio más reciente disponible de un símbolo.
    Devuelve {'price', 'previous_close', 'currency', 'fetched_at'} o None.
    """
    symbol = symbol.upper().strip()
    now = time.time()
    with _cache_lock:
        hit = _price_cache.get(symbol)
        if hit and now - hit[0] < PRICE_CACHE_SECONDS:
            return hit[1]

    data = _download_live_price(symbol)
    if data:
        with _cache_lock:
            _price_cache[symbol] = (now, data)
    return data


def _download_live_price(symbol: str) -> Optional[Dict]:
    try:
        import yfinance as yf
    except ImportError:
        return None

    try:
        ticker = yf.Ticker(symbol)
        price = prev = None
        currency = "USD"
        try:
            fi = ticker.fast_info
            price = fi.get("lastPrice") or fi.get("last_price")
            prev = fi.get("previousClose") or fi.get("previous_close")
            currency = fi.get("currency") or currency
        except Exception:
            pass

        if not price:
            hist = ticker.history(period="5d")
            if hist is None or hist.empty:
                return None
            price = float(hist["Close"].iloc[-1])
            if len(hist) > 1:
                prev = float(hist["Close"].iloc[-2])

        return {
            "price": float(price),
            "previous_close": float(prev) if prev else None,
            "currency": currency,
            "fetched_at": utc_now().isoformat(),
        }
    except Exception:
        return None


def get_price_history(symbol: str, since: datetime) -> List[Dict]:
    """
    Historial de precios desde `since` hasta hoy (para la gráfica de progreso).
    Si la inversión tiene menos de 7 días se usan velas de 30 minutos, si no, diarias.
    """
    symbol = symbol.upper().strip()
    if since.tzinfo is None:
        since = since.replace(tzinfo=timezone.utc)
    days = (utc_now() - since).days
    intraday = days < 7
    key = (symbol, since.date().isoformat(), intraday)

    now = time.time()
    with _cache_lock:
        hit = _history_cache.get(key)
        if hit and now - hit[0] < HISTORY_CACHE_SECONDS:
            return hit[1]

    points: List[Dict] = []
    try:
        import yfinance as yf

        ticker = yf.Ticker(symbol)
        if intraday:
            hist = ticker.history(period="10d", interval="30m")
        else:
            start = (since - timedelta(days=1)).date().isoformat()
            hist = ticker.history(start=start, interval="1d")
        if hist is not None and not hist.empty:
            for idx, row in hist.iterrows():
                ts = idx.to_pydatetime()
                if ts.tzinfo is None:
                    ts = ts.replace(tzinfo=timezone.utc)
                # Para diarias comparamos por fecha; para intradía por instante
                if intraday and ts < since - timedelta(minutes=30):
                    continue
                if not intraday and ts.date() < since.date():
                    continue
                points.append({"t": ts.astimezone(timezone.utc).isoformat(),
                               "close": float(row["Close"])})
    except Exception:
        points = []

    with _cache_lock:
        _history_cache[key] = (now, points)
    return points


# ─────────────────────────────────────────────────────────────────────────────
# Base de datos de inversiones
# ─────────────────────────────────────────────────────────────────────────────


class PortfolioStore:
    def __init__(self, db_path: Optional[str | Path] = None):
        self.db_path = Path(db_path) if db_path else DEFAULT_DB_PATH
        # Asegura que exista también la tabla de recomendaciones
        self.recs = RecommendationStore(self.db_path)
        self.init_db()

    @contextmanager
    def _connect(self):
        conn = sqlite3.connect(self.db_path, timeout=15)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS investments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    recommendation_id INTEGER,
                    strategy TEXT,
                    marked_at TEXT NOT NULL,          -- UTC ISO: momento en que la señalaste
                    entry_price REAL NOT NULL,        -- precio al momento de señalarla
                    market_price_at_mark REAL,        -- precio de mercado en ese instante
                    shares REAL,                      -- número de acciones (opcional)
                    amount_invested REAL,             -- dinero invertido (opcional)
                    notes TEXT,
                    status TEXT NOT NULL DEFAULT 'open',  -- open | closed
                    closed_at TEXT,
                    exit_price REAL
                )
                """
            )

    # ── escritura ────────────────────────────────────────────────────────────

    def add(
        self,
        symbol: str,
        entry_price: Optional[float] = None,
        shares: Optional[float] = None,
        amount: Optional[float] = None,
        recommendation_id: Optional[int] = None,
        notes: Optional[str] = None,
    ) -> Dict:
        symbol = (symbol or "").upper().strip()
        strategy = None
        if recommendation_id:
            rec = self.get_recommendation(recommendation_id)
            if not rec:
                raise ValueError(f"No existe la recomendación #{recommendation_id}")
            symbol = rec["symbol"]
            strategy = rec["strategy"]
        if not symbol:
            raise ValueError("Falta el símbolo de la acción")

        live = get_live_price(symbol)
        market_price = live["price"] if live else None
        if entry_price is None:
            if market_price is None:
                raise ValueError(
                    f"No se pudo obtener el precio actual de {symbol}. "
                    "Verifica el símbolo o escribe el precio manualmente."
                )
            entry_price = market_price

        entry_price = float(entry_price)
        if entry_price <= 0:
            raise ValueError("El precio de entrada debe ser mayor que 0")

        # Si das el monto pero no las acciones, se calculan
        if shares is None and amount:
            shares = float(amount) / entry_price
        if amount is None and shares:
            amount = float(shares) * entry_price

        with self._connect() as conn:
            cur = conn.execute(
                """
                INSERT INTO investments (symbol, recommendation_id, strategy, marked_at,
                    entry_price, market_price_at_mark, shares, amount_invested, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    symbol, recommendation_id, strategy, utc_now().isoformat(),
                    entry_price, market_price,
                    float(shares) if shares else None,
                    float(amount) if amount else None,
                    (notes or "").strip() or None,
                ),
            )
            new_id = cur.lastrowid
        return self.get(new_id)

    def close(self, inv_id: int, exit_price: Optional[float] = None) -> Dict:
        inv = self.get(inv_id)
        if not inv:
            raise ValueError("No existe esa inversión")
        if exit_price is None:
            live = get_live_price(inv["symbol"])
            if not live:
                raise ValueError("No se pudo obtener el precio actual; escríbelo manualmente")
            exit_price = live["price"]
        with self._connect() as conn:
            conn.execute(
                "UPDATE investments SET status='closed', closed_at=?, exit_price=? WHERE id=?",
                (utc_now().isoformat(), float(exit_price), inv_id),
            )
        return self.get(inv_id)

    def reopen(self, inv_id: int) -> Dict:
        with self._connect() as conn:
            conn.execute(
                "UPDATE investments SET status='open', closed_at=NULL, exit_price=NULL WHERE id=?",
                (inv_id,),
            )
        return self.get(inv_id)

    def delete(self, inv_id: int) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM investments WHERE id=?", (inv_id,))

    # ── lectura ──────────────────────────────────────────────────────────────

    def get(self, inv_id: int) -> Optional[Dict]:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM investments WHERE id=?", (inv_id,)).fetchone()
        return dict(row) if row else None

    def list(self, status: Optional[str] = None) -> List[Dict]:
        sql = "SELECT * FROM investments"
        params: tuple = ()
        if status:
            sql += " WHERE status=?"
            params = (status,)
        sql += " ORDER BY status ASC, marked_at DESC"
        with self._connect() as conn:
            rows = conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]

    def get_recommendation(self, rec_id: int) -> Optional[Dict]:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM recommendations WHERE id=?", (rec_id,)).fetchone()
        return dict(row) if row else None

    def list_recommendations(self, limit: int = 300) -> List[Dict]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT r.*,
                       (SELECT COUNT(*) FROM investments i WHERE i.recommendation_id = r.id) AS invested_count
                FROM recommendations r
                ORDER BY r.recommended_at DESC, r.probability DESC
                LIMIT ?
                """,
                (int(limit),),
            ).fetchall()
        return [dict(r) for r in rows]

    # ── cálculo de resultados ────────────────────────────────────────────────

    def with_performance(self, inv: Dict) -> Dict:
        """Añade precio actual, ganancia/pérdida y datos de la recomendación."""
        out = dict(inv)
        entry = float(inv["entry_price"])
        if inv["status"] == "closed" and inv.get("exit_price"):
            current = float(inv["exit_price"])
            out["price_source"] = "cierre"
            out["previous_close"] = None
        else:
            live = get_live_price(inv["symbol"])
            current = live["price"] if live else None
            out["price_source"] = "en_vivo" if live else "no_disponible"
            out["previous_close"] = live.get("previous_close") if live else None
            out["price_fetched_at"] = live.get("fetched_at") if live else None

        out["current_price"] = current
        shares = inv.get("shares")
        if current is not None:
            diff = current - entry
            out["change_per_share"] = diff
            out["change_pct"] = (current / entry - 1.0) * 100.0
            out["profit"] = diff * shares if shares else None
            out["current_value"] = current * shares if shares else None
            prev = out.get("previous_close")
            out["day_change_pct"] = ((current / prev - 1.0) * 100.0) if prev else None
        else:
            out.update(change_per_share=None, change_pct=None, profit=None,
                       current_value=None, day_change_pct=None)

        marked = datetime.fromisoformat(inv["marked_at"])
        if marked.tzinfo is None:
            marked = marked.replace(tzinfo=timezone.utc)
        end = datetime.fromisoformat(inv["closed_at"]) if inv.get("closed_at") else utc_now()
        if end.tzinfo is None:
            end = end.replace(tzinfo=timezone.utc)
        out["days_held"] = round((end - marked).total_seconds() / 86400.0, 1)

        rec = self.get_recommendation(inv["recommendation_id"]) if inv.get("recommendation_id") else None
        if rec:
            due = datetime.fromisoformat(rec["evaluation_due_at"])
            out["recommendation"] = {
                "id": rec["id"],
                "strategy": rec["strategy"],
                "probability": rec["probability"],
                "risk": rec["risk"],
                "avg_return": rec["avg_return"],
                "max_loss": rec["max_loss"],
                "samples": rec["samples"],
                "horizon_days": rec["horizon_days"],
                "recommended_at": rec["recommended_at"],
                "evaluation_due_at": rec["evaluation_due_at"],
                "entry_price_signal": rec["entry_price"],
                "recommendation_level": rec["recommendation_level"],
                "days_left": (due.date() - datetime.now().date()).days,
            }
        else:
            out["recommendation"] = None
        return out

    def portfolio_summary(self, items: List[Dict]) -> Dict:
        open_items = [i for i in items if i["status"] == "open"]
        closed_items = [i for i in items if i["status"] == "closed"]

        def totals(group):
            invested = sum(i["amount_invested"] or 0 for i in group if i.get("shares"))
            value = sum(i["current_value"] or 0 for i in group if i.get("current_value") is not None)
            profit = sum(i["profit"] or 0 for i in group if i.get("profit") is not None)
            pcts = [i["change_pct"] for i in group if i.get("change_pct") is not None]
            winners = sum(1 for p in pcts if p > 0)
            losers = sum(1 for p in pcts if p < 0)
            return {
                "count": len(group),
                "invested": invested,
                "current_value": value,
                "profit": profit,
                "profit_pct": (profit / invested * 100.0) if invested else None,
                "avg_change_pct": (sum(pcts) / len(pcts)) if pcts else None,
                "winners": winners,
                "losers": losers,
            }

        return {"open": totals(open_items), "closed": totals(closed_items)}
