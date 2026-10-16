"""
Evalúa recomendaciones vencidas y muestra el historial de aciertos.

Uso:
  python evaluar_recomendaciones.py              # evalúa solo las vencidas
  python evaluar_recomendaciones.py --list       # lista pendientes
  python evaluar_recomendaciones.py --history    # historial evaluado
  python evaluar_recomendaciones.py --summary    # resumen de precisión
  python evaluar_recomendaciones.py --import-csv mis_recomendaciones.csv --horizon 30
  python evaluar_recomendaciones.py --force      # evalúa todas las pending (útil para pruebas)
"""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

from database import (
    RecommendationStore,
    print_evaluation_results,
    print_pending_table,
)


def cmd_list(store: RecommendationStore, only_due: bool) -> None:
    rows = store.get_pending(only_due=only_due)
    label = "vencidas" if only_due else "pendientes"
    print(f"\n📋 Recomendaciones {label}: {len(rows)}")
    print_pending_table(rows)


def cmd_evaluate(store: RecommendationStore, force: bool) -> None:
    print("\n⏳ Evaluando recomendaciones" + (" (todas las pending)" if force else " vencidas") + "...")
    results = store.evaluate_due(force_all_pending=force)
    print_evaluation_results(results)
    cmd_summary(store)


def cmd_history(store: RecommendationStore, limit: int) -> None:
    rows = store.get_all(status="evaluated", limit=limit)
    if not rows:
        print("\nAún no hay recomendaciones evaluadas.")
        return

    print(f"\n📚 Últimas {len(rows)} evaluaciones:\n")
    print(f"{'ID':>4}  {'Fecha rec.':<19} {'Símbolo':<8} {'Estrategia':<18} "
          f"{'Entrada':>9} {'Salida':>9} {'Real%':>8} {'Resultado'}")
    print("-" * 100)
    for r in rows:
        mark = "ACIERTO" if r.get("was_correct") else "FALLO"
        print(
            f"{r['id']:>4}  {r['recommended_at']:<19} {r['symbol']:<8} {r['strategy']:<18} "
            f"${r['entry_price']:>8.2f} ${r['exit_price']:>8.2f} "
            f"{r['actual_return_pct']:>+7.2f}% {mark}"
        )


def cmd_summary(store: RecommendationStore) -> None:
    s = store.performance_summary()
    print("\n" + "═" * 80)
    print("📊 RESUMEN DE PRECISIÓN")
    print("═" * 80)
    print(f"  Total guardadas : {s['total']}")
    print(f"  Pendientes      : {s['pending']}")
    print(f"  Evaluadas       : {s['evaluated']}")
    if s["evaluated"]:
        print(f"  Aciertos        : {s['correct']} ({s['accuracy_pct']:.1f}%)")
        avg = s["avg_actual_return"]
        if avg is not None:
            print(f"  Retorno real medio: {avg:+.2f}%")
        if s["avg_predicted_prob"] is not None:
            print(f"  Prob. histórica media (predicha): {s['avg_predicted_prob']:.1f}%")

        if s["by_strategy"]:
            print("\n  Por estrategia:")
            for row in s["by_strategy"]:
                acc = (row["correct"] / row["evaluated"] * 100.0) if row["evaluated"] else 0
                print(
                    f"    • {row['strategy']:<20} "
                    f"{row['correct']}/{row['evaluated']} aciertos ({acc:.0f}%) | "
                    f"retorno medio {row['avg_actual_return']:+.2f}%"
                )
    else:
        print("  Todavía no hay datos evaluados. Vuelve cuando venza el horizonte.")
    print("═" * 80 + "\n")


def cmd_import_csv(store: RecommendationStore, csv_path: str, horizon: int) -> None:
    path = Path(csv_path)
    print(f"\n📥 Importando {path} con horizonte {horizon} días...")
    stats = store.import_csv(
        path,
        horizon_days=horizon,
        recommended_at=datetime.now(),
        notes=f"import:{path.name}",
    )
    print(f"  Insertadas: {stats['inserted']} | Omitidas (duplicado mismo día): {stats['skipped']}")
    cmd_list(store, only_due=False)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Evaluar y consultar recomendaciones guardadas")
    p.add_argument("--db", default=None, help="Ruta al archivo SQLite (default: finance.db)")
    p.add_argument("--list", action="store_true", help="Listar recomendaciones pendientes")
    p.add_argument("--due", action="store_true", help="Con --list, solo las ya vencidas")
    p.add_argument("--history", action="store_true", help="Mostrar historial evaluado")
    p.add_argument("--limit", type=int, default=30, help="Límite para --history")
    p.add_argument("--summary", action="store_true", help="Mostrar resumen de precisión")
    p.add_argument("--force", action="store_true", help="Evaluar todas las pending (no solo vencidas)")
    p.add_argument("--import-csv", dest="import_csv", help="Importar CSV de señales a la BD")
    p.add_argument("--horizon", type=int, default=30, help="Horizonte en días al importar CSV")
    p.add_argument("--evaluate", action="store_true", help="Evaluar recomendaciones vencidas")
    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    store = RecommendationStore(db_path=args.db)

    # Si no se pasa ninguna acción, evaluar vencidas + resumen
    no_action = not any(
        [args.list, args.history, args.summary, args.import_csv, args.evaluate, args.force]
    )

    if args.import_csv:
        cmd_import_csv(store, args.import_csv, args.horizon)

    if args.list:
        cmd_list(store, only_due=args.due)

    if args.history:
        cmd_history(store, limit=args.limit)

    if args.evaluate or args.force or no_action:
        # no_action => comportamiento por defecto: evaluar vencidas
        if args.evaluate or args.force or no_action:
            # Si solo pidieron summary/list/history no evaluar
            if args.evaluate or args.force or (
                no_action and not args.summary and not args.list and not args.history
            ):
                cmd_evaluate(store, force=args.force)
                return

    if args.summary or no_action:
        cmd_summary(store)


if __name__ == "__main__":
    main()
