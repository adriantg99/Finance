"""
EJEMPLO RÁPIDO: Analizar acciones específicas
Este script te permite analizar solo las acciones que te interesan
"""

from stock_analyzer import StockRecommender

def main():
    # 🎯 Personaliza tu lista de acciones aquí
    mis_acciones = [
        'TSLA',   # Tesla
        'AAPL',   # Apple
        'MSFT',   # Microsoft
        'NVDA',   # Nvidia
        'GOOGL',  # Google
        'AMZN',   # Amazon
        'META',   # Meta
        'AMD',    # AMD
    ]
    
    # Días hacia adelante para analizar (15 días por defecto)
    horizonte = 15
    
    # Crear analizador
    print("=" * 80)
    print("🚀 BUSCADOR DE OPORTUNIDADES DE COMPRA")
    print("=" * 80)
    print(f"\n📅 Horizonte de análisis: {horizonte} días")
    print(f"📊 Acciones a analizar: {len(mis_acciones)}\n")
    
    recommender = StockRecommender()
    
    # Analizar
    signals = recommender.analyze_multiple_stocks(mis_acciones, horizonte)
    
    # Mostrar resultados
    recommender.print_recommendations(signals, horizonte)
    
    # Guardar en CSV
    if signals:
        recommender.export_to_csv(signals, "mis_recomendaciones.csv")
    
    print("\n✅ Análisis completado!")
    print("💡 Tip: Estas son probabilidades históricas. Siempre investiga antes de invertir.\n")


if __name__ == "__main__":
    main()
