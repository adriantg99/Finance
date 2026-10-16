"""
Persistencia de recomendaciones y evaluación de resultados.

Usa SQLite (archivo local) para:
- Guardar cada recomendación con precio, métricas y plazo
- Evaluar después del horizonte si el precio subió o bajó
- Reportar aciertos vs fallos de las estrategias
"""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Iterable, List, Optional

DEFAULT_DB_PATH = Path(__file__).resolve().parent / "finance.db"


def recommendation_level(probability: float, risk: float) -> str:
    """Clasifica la fuerza de la recomendación (misma lógica que StockRecommender)."""
    if probability >= 70 and risk < 10:
        return "COMPRA FUERTE"
    if probability >= 65 and risk < 15:
        return "COMPRA MODERADA"
    return "COMPRA CAUTELOSA"


class RecommendationStore:
    """CRUD y evaluación de recomendaciones en SQLite."""

    def __init__(self, db_path: Optional[str | Path] = None):
        self.db_path = Path(db_path) if db_path else DEFAULT_DB_PATH
        self.init_db()

    @contextmanager
    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
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
                CREATE TABLE IF NOT EXISTS recommendations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    strategy TEXT NOT NULL,
                    recommended_at TEXT NOT NULL,
                    horizon_days INTEGER NOT NULL,
                    evaluation_due_at TEXT NOT NULL,
                    entry_price REAL NOT NULL,
                    rsi REAL,
                    probability REAL,
                    risk REAL,
                    avg_return REAL,
                    max_loss REAL,
                    samples INTEGER,
                    recommendation_level TEXT,
                    status TEXT NOT NULL DEFAULT 'pending',
                    exit_price REAL,
                    actual_return_pct REAL,
                    was_correct INTEGER,
                    evaluated_at TEXT,
                    notes TEXT,
                    UNIQUE(symbol, strategy, recommended_at, horizon_days)
                )
                """
            )
            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_rec_status_due
                ON recommendations(status, evaluation_due_at)
                """
            )
            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_rec_symbol
                ON recommendations(symbol)
                """
            )

    def save_recommendation(
        self,
        signal: Dict,
        horizon_days: int,
        recommended_at: Optional[datetime] = None,
        notes: Optional[str] = None,
        skip_duplicates_same_day: bool = True,
    ) -> Optional[int]:
        """
        Guarda una señal. Si ya existe la misma (símbolo+estrategia+día+horizonte)
        y skip_duplicates_same_day=True, no inserta de nuevo.
        Devuelve el id insertado o None si se omitió.
        """
        now = recommended_at or datetime.now()
        due = now + timedelta(days=int(horizon_days))
        level = signal.get("recommendation_level") or recommendation_level(
            float(signal.get("probability", 0)),
            float(signal.get("risk", 0)),
        )

        symbol = str(signal["symbol"]).upper().strip()
        strategy = str(signal["strategy"]).strip()
        recommended_at_iso = now.replace(microsecond=0).isoformat(sep=" ")
        day_prefix = now.strftime("%Y-%m-%d")

        with self._connect() as conn:
            if skip_duplicates_same_day:
                existing = conn.execute(
                    """
                    SELECT id FROM recommendations
                    WHERE symbol = ?
                      AND strategy = ?
                      AND horizon_days = ?
                      AND recommended_at LIKE ?
                    """,
                    (symbol, strategy, int(horizon_days), f"{day_prefix}%"),
                ).fetchone()
                if existing:
                    return None

            cur = conn.execute(
                """
                INSERT INTO recommendations (
                    symbol, strategy, recommended_at, horizon_days, evaluation_due_at,
                    entry_price, rsi, probability, risk, avg_return, max_loss, samples,
                    recommendation_level, status, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending', ?)
                """,
                (
                    symbol,
                    strategy,
                    recommended_at_iso,
                    int(horizon_days),
                    due.replace(microsecond=0).isoformat(sep=" "),
                    float(signal["current_price"]),
                    _maybe_float(signal.get("rsi")),
                    _maybe_float(signal.get("probability")),
                    _maybe_float(signal.get("risk")),
                    _maybe_float(signal.get("avg_return")),
                    _maybe_float(signal.get("max_loss")),
                    _maybe_int(signal.get("samples")),
                    level,
                    notes,
                ),
            )
            return int(cur.lastrowid)

    def save_recommendations(
        self,
        signals: Iterable[Dict],
        horizon_days: int,
        notes: Optional[str] = None,
    ) -> Dict[str, int]:
        """Guarda un lote de señales. Retorna contadores inserted/skipped."""
        inserted = 0
        skipped = 0
        for signal in signals:
            row_id = self.save_recommendation(
                signal, horizon_days=horizon_days, notes=notes
            )
            if row_id is None:
                skipped += 1
            else:
                inserted += 1
        return {"inserted": inserted, "skipped": skipped}

    def get_pending(self, only_due: bool = False) -> List[Dict]:
        """Lista recomendaciones pendientes. only_due=True solo las ya vencidas."""
        sql = "SELECT * FROM recommendations WHERE status = 'pending'"
        params: tuple = ()
        if only_due:
            sql += " AND evaluation_due_at <= ?"
            params = (datetime.now().replace(microsecond=0).isoformat(sep=" "),)
        sql += " ORDER BY evaluation_due_at ASC, id ASC"

        with self._connect() as conn:
            rows = conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]

    def get_all(
        self,
        status: Optional[str] = None,
        symbol: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[Dict]:
        clauses = []
        params: List = []
        if status:
            clauses.append("status = ?")
            params.append(status)
        if symbol:
            clauses.append("symbol = ?")
            params.append(symbol.upper())
        sql = "SELECT * FROM recommendations"
        if clauses:
            sql += " WHERE " + " AND ".join(clauses)
        sql += " ORDER BY recommended_at DESC, id DESC"
        if limit:
            sql += f" LIMIT {int(limit)}"

        with self._connect() as conn:
            rows = conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]

    def mark_evaluated(
        self,
        rec_id: int,
        exit_price: float,
        evaluated_at: Optional[datetime] = None,
    ) -> Dict:
        """Calcula retorno real y marca la recomendación como evaluada."""
        evaluated_at = evaluated_at or datetime.now()
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM recommendations WHERE id = ?", (rec_id,)
            ).fetchone()
            if row is None:
                raise ValueError(f"Recomendación id={rec_id} no existe")

            entry = float(row["entry_price"])
            actual_return = ((exit_price / entry) - 1.0) * 100.0 if entry else 0.0
            was_correct = 1 if actual_return > 0 else 0

            conn.execute(
                """
                UPDATE recommendations
                SET status = 'evaluated',
                    exit_price = ?,
                    actual_return_pct = ?,
                    was_correct = ?,
                    evaluated_at = ?
                WHERE id = ?
                """,
                (
                    float(exit_price),
                    actual_return,
                    was_correct,
                    evaluated_at.replace(microsecond=0).isoformat(sep=" "),
                    rec_id,
                ),
            )
            updated = conn.execute(
                "SELECT * FROM recommendations WHERE id = ?", (rec_id,)
            ).fetchone()
        return dict(updated)

    def evaluate_due(self, force_all_pending: bool = False) -> List[Dict]:
        """
        Evalúa recomendaciones vencidas (o todas las pending si force_all_pending).
        Descarga el precio actual de cada símbolo y actualiza la fila.
        """
        pending = self.get_pending(only_due=not force_all_pending)
        results: List[Dict] = []
        if not pending:
            return results

        # Cache de precios por símbolo para no pedir N veces lo mismo
        price_cache: Dict[str, Optional[float]] = {}

        for rec in pending:
            symbol = rec["symbol"]
            if symbol not in price_cache:
                price_cache[symbol] = fetch_latest_price(symbol)
            price = price_cache[symbol]
            if price is None:
                results.append(
                    {
                        "id": rec["id"],
                        "symbol": symbol,
                        "error": "No se pudo obtener precio actual",
                        "status": "skipped",
                    }
                )
                continue

            updated = self.mark_evaluated(rec["id"], exit_price=price)
            results.append(updated)

        return results

    def performance_summary(self) -> Dict:
        """Resumen global y por estrategia de las recomendaciones evaluadas."""
        with self._connect() as conn:
            totals = conn.execute(
                """
                SELECT
                    COUNT(*) AS total,
                    SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) AS pending,
                    SUM(CASE WHEN status = 'evaluated' THEN 1 ELSE 0 END) AS evaluated,
                    SUM(CASE WHEN was_correct = 1 THEN 1 ELSE 0 END) AS correct,
                    AVG(CASE WHEN status = 'evaluated' THEN actual_return_pct END) AS avg_actual_return,
                    AVG(CASE WHEN status = 'evaluated' THEN probability END) AS avg_predicted_prob
                FROM recommendations
                """
            ).fetchone()

            by_strategy = conn.execute(
                """
                SELECT
                    strategy,
                    COUNT(*) AS evaluated,
                    SUM(CASE WHEN was_correct = 1 THEN 1 ELSE 0 END) AS correct,
                    AVG(actual_return_pct) AS avg_actual_return,
                    AVG(probability) AS avg_predicted_prob
                FROM recommendations
                WHERE status = 'evaluated'
                GROUP BY strategy
                ORDER BY evaluated DESC
                """
            ).fetchall()

        evaluated = int(totals["evaluated"] or 0)
        correct = int(totals["correct"] or 0)
        return {
            "total": int(totals["total"] or 0),
            "pending": int(totals["pending"] or 0),
            "evaluated": evaluated,
            "correct": correct,
            "accuracy_pct": (correct / evaluated * 100.0) if evaluated else None,
            "avg_actual_return": totals["avg_actual_return"],
            "avg_predicted_prob": totals["avg_predicted_prob"],
            "by_strategy": [dict(r) for r in by_strategy],
        }

    def import_csv(
        self,
        csv_path: str | Path,
        horizon_days: int,
        recommended_at: Optional[datetime] = None,
        notes: str = "import_csv",
    ) -> Dict[str, int]:
        """Importa un CSV de señales (mismo formato que export_to_csv)."""
        import pandas as pd

        path = Path(csv_path)
        if not path.exists():
            raise FileNotFoundError(path)

        df = pd.read_csv(path)
        signals = df.to_dict(orient="records")
        # Normalizar nombre de precio si viniera distinto
        for s in signals:
            if "current_price" not in s and "entry_price" in s:
                s["current_price"] = s["entry_price"]
        return self.save_recommendations(
            signals, horizon_days=horizon_days, notes=notes
        )


def fetch_latest_price(symbol: str) -> Optional[float]:
    """Obtiene el último precio de cierre disponible vía yfinance."""
    try:
        import yfinance as yf
    except ImportError:
        print("⚠️  yfinance no está instalado; no se puede evaluar precios.")
        return None

    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="5d")
        if hist is None or hist.empty:
            df = yf.download(symbol, period="5d", progress=False)
            if df is None or df.empty:
                return None
            if hasattr(df.columns, "get_level_values"):
                try:
                    close = df["Close"]
                    if hasattr(close, "iloc"):
                        val = close.iloc[-1]
                        if hasattr(val, "item"):
                            return float(val.item())
                        return float(val)
                except Exception:
                    pass
            return float(df["Close"].iloc[-1])
        return float(hist["Close"].iloc[-1])
    except Exception:
        return None


def _maybe_float(value) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _maybe_int(value) -> Optional[int]:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def print_pending_table(rows: List[Dict]) -> None:
    if not rows:
        print("No hay recomendaciones pendientes.")
        return
    print(f"\n{'ID':>4}  {'Símbolo':<8} {'Estrategia':<18} {'Entrada':>10} "
          f"{'Horiz.':>6} {'Evalúa el':<19} {'Nivel'}")
    print("-" * 90)
    for r in rows:
        print(
            f"{r['id']:>4}  {r['symbol']:<8} {r['strategy']:<18} "
            f"${r['entry_price']:>9.2f} {r['horizon_days']:>5}d "
            f"{r['evaluation_due_at']:<19} {r.get('recommendation_level') or ''}"
        )


def print_evaluation_results(results: List[Dict]) -> None:
    if not results:
        print("No había recomendaciones vencidas para evaluar.")
        return

    print("\n" + "=" * 80)
    print("RESULTADOS DE EVALUACIÓN")
    print("=" * 80)

    for r in results:
        if r.get("status") == "skipped" or "error" in r:
            print(f"  ⚠️  #{r.get('id')} {r.get('symbol')}: {r.get('error')}")
            continue

        ok = "✅ ACIERTO" if r.get("was_correct") else "❌ FALLO"
        predicted = r.get("avg_return")
        actual = r.get("actual_return_pct")
        print(
            f"  {ok}  #{r['id']} {r['symbol']} ({r['strategy']})\n"
            f"      Entrada ${r['entry_price']:.2f} → Salida ${r['exit_price']:.2f} | "
            f"Real {actual:+.2f}% | Esperado ~{predicted:.2f}% | "
            f"Prob. hist. {r.get('probability', 0):.0f}%"
        )


if __name__ == "__main__":
    store = RecommendationStore()
    print(f"Base de datos lista en: {store.db_path}")
    pending = store.get_pending()
    print(f"Pendientes: {len(pending)}")
    print_pending_table(pending)
    summary = store.performance_summary()
    print(f"\nResumen: {summary}")
