"""
EJEMPLOS AVANZADOS: Diferentes formas de usar el analizador
"""

from stock_analyzer import StockAnalyzer, StockRecommender
import pandas as pd


def ejemplo_1_analizar_una_accion():
    """Ejemplo: Analizar una sola acción en detalle"""
    print("\n" + "="*80)
    print("EJEMPLO 1: Análisis detallado de una acción (TSLA)")
    print("="*80 + "\n")
    
    analyzer = StockAnalyzer()
    signals = analyzer.get_current_signals('TSLA', horizon=15)
    
    if signals:
        for signal in signals:
            print(f"Estrategia: {signal['strategy']}")
            print(f"Probabilidad: {signal['probability']:.1f}%")
            print(f"Riesgo: {signal['risk']:.1f}%")
            print(f"Precio actual: ${signal['current_price']:.2f}")
            print("-" * 40)
    else:
        print("No se encontraron señales de compra para TSLA en este momento.")


def ejemplo_2_acciones_tech():
    """Ejemplo: Solo acciones tecnológicas"""
    print("\n" + "="*80)
    print("EJEMPLO 2: Análisis de acciones tecnológicas")
    print("="*80 + "\n")
    
    tech_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'AMD', 'INTC']
    
    recommender = StockRecommender()
    signals = recommender.analyze_multiple_stocks(tech_stocks, horizon=15)
    recommender.print_recommendations(signals, horizon=15)


def ejemplo_3_diferentes_horizontes():
    """Ejemplo: Analizar con diferentes horizontes de tiempo"""
    print("\n" + "="*80)
    print("EJEMPLO 3: Comparar horizontes de tiempo")
    print("="*80 + "\n")
    
    symbol = 'TSLA'
    horizontes = [5, 10, 15, 30]
    
    analyzer = StockAnalyzer()
    
    for horizon in horizontes:
        signals = analyzer.get_current_signals(symbol, horizon=horizon)
        
        print(f"\n📅 Horizonte: {horizon} días")
        if signals:
            best = max(signals, key=lambda x: x['probability'])
            print(f"   Mejor estrategia: {best['strategy']}")
            print(f"   Probabilidad: {best['probability']:.1f}%")
            print(f"   Retorno esperado: {best['avg_return']:.2f}%")
        else:
            print("   Sin señales")


def ejemplo_4_filtrar_por_probabilidad():
    """Ejemplo: Solo mostrar señales con alta probabilidad"""
    print("\n" + "="*80)
    print("EJEMPLO 4: Filtrar señales de alta probabilidad (>70%)")
    print("="*80 + "\n")
    
    symbols = ['TSLA', 'AAPL', 'MSFT', 'NVDA', 'AMD', 'META']
    
    recommender = StockRecommender()
    signals = recommender.analyze_multiple_stocks(symbols, horizon=15)
    
    # Filtrar solo alta probabilidad
    high_prob = [s for s in signals if s['probability'] >= 70]
    
    if high_prob:
        print(f"✅ Encontradas {len(high_prob)} señales con probabilidad ≥ 70%\n")
        recommender.print_recommendations(high_prob, horizon=15)
    else:
        print("❌ No hay señales con probabilidad ≥ 70% en este momento.")


def ejemplo_5_bajo_riesgo():
    """Ejemplo: Solo acciones con bajo riesgo"""
    print("\n" + "="*80)
    print("EJEMPLO 5: Señales de bajo riesgo (<10%)")
    print("="*80 + "\n")
    
    symbols = ['AAPL', 'MSFT', 'JNJ', 'PG', 'KO', 'PEP', 'WMT', 'V', 'MA']
    
    recommender = StockRecommender()
    signals = recommender.analyze_multiple_stocks(symbols, horizon=15)
    
    # Filtrar bajo riesgo
    low_risk = [s for s in signals if s['risk'] < 10]
    
    if low_risk:
        print(f"✅ Encontradas {len(low_risk)} señales con riesgo < 10%\n")
        recommender.print_recommendations(low_risk, horizon=15)
    else:
        print("❌ No hay señales de bajo riesgo en este momento.")


def ejemplo_6_analisis_personalizado():
    """Ejemplo: Análisis completamente personalizado"""
    print("\n" + "="*80)
    print("EJEMPLO 6: Análisis personalizado con filtros múltiples")
    print("="*80 + "\n")
    
    # Tus criterios personalizados
    PROB_MINIMA = 65
    RIESGO_MAXIMO = 12
    RETORNO_MINIMO = 5.0
    
    symbols = ['TSLA', 'AAPL', 'MSFT', 'NVDA', 'AMD', 'GOOGL', 'AMZN', 'META']
    
    recommender = StockRecommender()
    signals = recommender.analyze_multiple_stocks(symbols, horizon=15)
    
    # Aplicar filtros personalizados
    filtered = [
        s for s in signals 
        if s['probability'] >= PROB_MINIMA 
        and s['risk'] <= RIESGO_MAXIMO
        and s['avg_return'] >= RETORNO_MINIMO
    ]
    
    print(f"Criterios aplicados:")
    print(f"  • Probabilidad mínima: {PROB_MINIMA}%")
    print(f"  • Riesgo máximo: {RIESGO_MAXIMO}%")
    print(f"  • Retorno mínimo esperado: {RETORNO_MINIMO}%")
    print()
    
    if filtered:
        print(f"✅ {len(filtered)} señal(es) cumple(n) todos los criterios:\n")
        recommender.print_recommendations(filtered, horizon=15)
    else:
        print("❌ Ninguna señal cumple todos los criterios en este momento.")


def ejemplo_7_comparar_estrategias():
    """Ejemplo: Comparar todas las estrategias para una acción"""
    print("\n" + "="*80)
    print("EJEMPLO 7: Comparar todas las estrategias para TSLA")
    print("="*80 + "\n")
    
    analyzer = StockAnalyzer()
    signals = analyzer.get_current_signals('TSLA', horizon=15)
    
    if signals:
        print(f"Señales activas para TSLA: {len(signals)}\n")
        
        # Ordenar por probabilidad
        signals.sort(key=lambda x: x['probability'], reverse=True)
        
        for i, signal in enumerate(signals, 1):
            print(f"{i}. {signal['strategy']}")
            print(f"   Probabilidad: {signal['probability']:.1f}% | "
                  f"Riesgo: {signal['risk']:.1f}% | "
                  f"Retorno: {signal['avg_return']:.2f}%")
            print()
    else:
        print("No hay estrategias activas para TSLA en este momento.")


def menu_interactivo():
    """Menú interactivo para elegir ejemplos"""
    while True:
        print("\n" + "="*80)
        print("🎯 EJEMPLOS INTERACTIVOS - Analizador de Acciones")
        print("="*80)
        print("\n1. Analizar una acción específica (TSLA)")
        print("2. Analizar acciones tecnológicas")
        print("3. Comparar diferentes horizontes de tiempo")
        print("4. Filtrar por alta probabilidad (>70%)")
        print("5. Filtrar por bajo riesgo (<10%)")
        print("6. Análisis personalizado con múltiples filtros")
        print("7. Comparar estrategias para una acción")
        print("0. Salir")
        
        try:
            opcion = input("\n👉 Selecciona una opción (0-7): ").strip()
            
            if opcion == '1':
                ejemplo_1_analizar_una_accion()
            elif opcion == '2':
                ejemplo_2_acciones_tech()
            elif opcion == '3':
                ejemplo_3_diferentes_horizontes()
            elif opcion == '4':
                ejemplo_4_filtrar_por_probabilidad()
            elif opcion == '5':
                ejemplo_5_bajo_riesgo()
            elif opcion == '6':
                ejemplo_6_analisis_personalizado()
            elif opcion == '7':
                ejemplo_7_comparar_estrategias()
            elif opcion == '0':
                print("\n👋 ¡Hasta luego!\n")
                break
            else:
                print("\n❌ Opción no válida. Por favor, elige entre 0 y 7.")
            
            input("\n⏸️  Presiona Enter para continuar...")
            
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            input("\n⏸️  Presiona Enter para continuar...")


if __name__ == "__main__":
    # Ejecutar menú interactivo
    menu_interactivo()
