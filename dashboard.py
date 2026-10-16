"""
DASHBOARD SIMPLE - Vista resumida de las mejores oportunidades
"""

from stock_analyzer import StockRecommender
from datetime import datetime


def print_dashboard():
    """Imprime un dashboard simple con las mejores oportunidades"""
    
    print("\n" + "╔" + "═"*78 + "╗")
    print("║" + " "*20 + "📊 DASHBOARD DE TRADING" + " "*27 + "║")
    print("║" + " "*20 + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " "*28 + "║")
    print("╚" + "═"*78 + "╝\n")
    
    # Acciones a monitorear
    symbols = [
        # Tech Giants
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'TSLA',
        # Semiconductores
        'AMD', 'INTC', 'QCOM', 'MU',
        # Finanzas
        'JPM', 'V', 'MA', 'BAC',
        # E-commerce y Servicios
        'SHOP', 'PYPL', 'SQ',
        # Entertainment
        'DIS', 'NFLX',
        # Otros
        'CRM', 'ADBE', 'ORCL'
    ]
    
    print(f"🔍 Escaneando {len(symbols)} acciones...\n")
    
    try:
        import config
        horizon = getattr(config, "HORIZONTE_DIAS", 30)
        save_db = getattr(config, "GUARDAR_BD", True)
        db_path = getattr(config, "RUTA_BD", None)
    except ImportError:
        horizon = 30
        save_db = True
        db_path = None

    recommender = StockRecommender(save_to_db=save_db, db_path=db_path)
    signals = recommender.analyze_multiple_stocks(symbols, horizon=horizon)
    
    if not signals:
        print("┌" + "─"*78 + "┐")
        print("│" + " "*20 + "❌ No hay señales en este momento" + " "*18 + "│")
        print("│" + " "*15 + "Intenta de nuevo más tarde o ajusta los parámetros" + " "*6 + "│")
        print("└" + "─"*78 + "┘\n")
        return
    
    # Separar por nivel de recomendación
    compra_fuerte = [s for s in signals if s['probability'] >= 70 and s['risk'] < 10]
    compra_moderada = [s for s in signals if s['probability'] >= 65 and s['risk'] < 15 
                       and s not in compra_fuerte]
    compra_cautelosa = [s for s in signals if s not in compra_fuerte 
                        and s not in compra_moderada]
    
    # Resumen
    print("┌" + "─"*78 + "┐")
    print("│  📊 RESUMEN GENERAL" + " "*54 + "│")
    print("├" + "─"*78 + "┤")
    print(f"│  Total de señales: {len(signals):<61}│")
    print(f"│  🟢 Compra Fuerte: {len(compra_fuerte):<61}│")
    print(f"│  🟡 Compra Moderada: {len(compra_moderada):<59}│")
    print(f"│  🟠 Compra Cautelosa: {len(compra_cautelosa):<58}│")
    print("└" + "─"*78 + "┘\n")
    
    # Mejores 5 oportunidades
    print("┌" + "─"*78 + "┐")
    print("│  🏆 TOP 5 OPORTUNIDADES" + " "*50 + "│")
    print("└" + "─"*78 + "┘\n")
    
    top_5 = sorted(signals, key=lambda x: (x['probability'], -x['risk']), reverse=True)[:5]
    
    for i, signal in enumerate(top_5, 1):
        # Emoji según nivel
        if signal['probability'] >= 70 and signal['risk'] < 10:
            emoji = "🟢"
        elif signal['probability'] >= 65 and signal['risk'] < 15:
            emoji = "🟡"
        else:
            emoji = "🟠"
        
        print(f"{emoji} {i}. {signal['symbol']:<8} ${signal['current_price']:>8.2f}")
        print(f"   Estrategia: {signal['strategy']}")
        print(f"   Probabilidad: {signal['probability']:.0f}% | Riesgo: {signal['risk']:.1f}% | Retorno esperado: {signal['avg_return']:+.2f}%")
        print()
    
    # Por sector/categoría
    print("\n┌" + "─"*78 + "┐")
    print("│  📈 SEÑALES POR ACCIÓN" + " "*50 + "│")
    print("└" + "─"*78 + "┘\n")
    
    # Agrupar por símbolo
    by_symbol = {}
    for signal in signals:
        if signal['symbol'] not in by_symbol:
            by_symbol[signal['symbol']] = []
        by_symbol[signal['symbol']].append(signal)
    
    # Ordenar por número de estrategias
    sorted_symbols = sorted(by_symbol.items(), key=lambda x: len(x[1]), reverse=True)
    
    for symbol, symbol_signals in sorted_symbols:
        best = max(symbol_signals, key=lambda x: x['probability'])
        count = len(symbol_signals)
        
        print(f"  {symbol:<8} {count} estrategia(s) activa(s) | "
              f"Mejor: {best['probability']:.0f}% prob, {best['risk']:.1f}% riesgo")
    
    print("\n" + "─"*80)
    print("💾 Detalles completos en CSV + BD (finance.db)")
    print("─"*80 + "\n")
    
    # Guardar CSV + base de datos para seguimiento del acierto
    recommender.persist_results(
        signals,
        horizon=horizon,
        csv_filename="dashboard_signals.csv",
        notes="dashboard",
    )


if __name__ == "__main__":
    try:
        print_dashboard()
    except KeyboardInterrupt:
        print("\n\n👋 Análisis cancelado\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
