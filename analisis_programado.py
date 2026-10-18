"""
ANÁLISIS AUTOMÁTICO (sin preguntas)

Pensado para ejecutarse solo: desde la interfaz web (botón "Ejecutar análisis"),
desde el Programador de tareas de Windows o desde cron en el servidor.

Hace dos cosas:
  1. Analiza las acciones de config.MIS_ACCIONES con los filtros de config.py
     y guarda las señales nuevas en finance.db.
  2. Evalúa las recomendaciones cuyo plazo ya venció (compara con el precio real).

Uso:
  python analisis_programado.py              # lista completa de config.MIS_ACCIONES
  python analisis_programado.py --rapido     # solo las 8 acciones de buscar_acciones.py
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime

import config
from stock_analyzer import StockRecommender
from database import RecommendationStore

LISTA_RAPIDA = ['TSLA', 'AAPL', 'MSFT', 'NVDA', 'GOOGL', 'AMZN', 'META', 'AMD']


def run(rapido: bool = False, log=print) -> dict:
    if getattr(config, "PERFIL_ACTIVO", None):
        config.aplicar_perfil(config.PERFIL_ACTIVO)

    symbols = LISTA_RAPIDA if rapido else list(dict.fromkeys(config.MIS_ACCIONES))
    horizon = getattr(config, "HORIZONTE_DIAS", 30)
    db_path = getattr(config, "RUTA_BD", None)

    log(f"[{datetime.now():%Y-%m-%d %H:%M}] Analizando {len(symbols)} acciones "
        f"(horizonte {horizon} días)...")

    rec = StockRecommender(save_to_db=True, db_path=db_path)
    rec.analyzer.period = getattr(config, "PERIODO_HISTORICO", "10y")

    signals = []
    for i, symbol in enumerate(symbols, 1):
        try:
            found = rec.analyzer.get_current_signals(symbol, horizon)
        except Exception as e:  # una acción con error no detiene el resto
            log(f"  {i}/{len(symbols)} {symbol}: error ({e})")
            continue
        enriched = [StockRecommender._enrich_signal(s, horizon) for s in found]
        signals.extend(enriched)
        if found:
            log(f"  {i}/{len(symbols)} {symbol}: {len(found)} señal(es)")
        elif i % 10 == 0:
            log(f"  {i}/{len(symbols)} procesadas...")

    filtered = [
        s for s in signals
        if s['probability'] >= config.PROBABILIDAD_MINIMA
        and s['risk'] <= config.RIESGO_MAXIMO
        and s['avg_return'] >= config.RETORNO_MINIMO
        and s['samples'] >= config.MUESTRAS_MINIMAS
    ]
    filtered.sort(key=lambda x: (x['probability'], -x['risk']), reverse=True)
    max_s = getattr(config, "MAX_SEÑALES", None)
    if max_s:
        filtered = filtered[:max_s]

    stats = {"inserted": 0, "skipped": 0}
    if filtered:
        stats = rec._get_store().save_recommendations(
            filtered, horizon_days=horizon, notes="analisis_programado"
        )
    log(f"Señales encontradas: {len(signals)} | pasan filtros: {len(filtered)} | "
        f"nuevas en BD: {stats['inserted']} | repetidas hoy: {stats['skipped']}")

    store = RecommendationStore(db_path=db_path)
    evaluated = store.evaluate_due()
    ok = [r for r in evaluated if r.get("status") == "evaluated"]
    log(f"Recomendaciones vencidas evaluadas: {len(ok)}")
    log("Listo.")
    return {"signals": len(signals), "filtered": len(filtered), **stats,
            "evaluated": len(ok)}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--rapido", action="store_true", help="Solo 8 acciones (1 minuto)")
    args = p.parse_args()
    try:
        run(rapido=args.rapido, log=lambda m: print(m, flush=True))
    except KeyboardInterrupt:
        sys.exit(1)
