"""
EJEMPLO RÁPIDO: Analizar acciones específicas
Este script te permite analizar solo las acciones que te interesan
"""

from stock_analyzer import StockRecommender

try:
    import config
    HORIZONTE_DEFAULT = getattr(config, "HORIZONTE_DIAS", 30)
    GUARDAR_BD = getattr(config, "GUARDAR_BD", True)
    RUTA_BD = getattr(config, "RUTA_BD", None)
except ImportError:
    HORIZONTE_DEFAULT = 30
    GUARDAR_BD = True
    RUTA_BD = None

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
    
    # Usa el horizonte de config.py (ej. 30 días) para poder evaluar después
    horizonte = HORIZONTE_DEFAULT
    
    # Crear analizador
    print("=" * 80)
    print("🚀 BUSCADOR DE OPORTUNIDADES DE COMPRA")
    print("=" * 80)
    print(f"\n📅 Horizonte de análisis: {horizonte} días")
    print(f"📊 Acciones a analizar: {len(mis_acciones)}\n")
    
    recommender = StockRecommender(save_to_db=GUARDAR_BD, db_path=RUTA_BD)
    
    # Analizar
    signals = recommender.analyze_multiple_stocks(mis_acciones, horizonte)
    
    # Mostrar resultados
    recommender.print_recommendations(signals, horizonte)
    
    # Guardar en CSV + base de datos (para comparar precio real al vencer el plazo)
    if signals:
        recommender.persist_results(
            signals,
            horizon=horizonte,
            csv_filename="mis_recomendaciones.csv",
            notes="buscar_acciones",
        )
    
    print("\n✅ Análisis completado!")
    print("💡 Tip: Estas son probabilidades históricas. Siempre investiga antes de invertir.")
    print("🗄️  Para ver pendientes o evaluar vencidas: python evaluar_recomendaciones.py --list\n")


if __name__ == "__main__":
    main()
