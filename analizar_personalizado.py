"""
ANÁLISIS CON CONFIGURACIÓN PERSONALIZADA
Usa los parámetros definidos en config.py
"""

from stock_analyzer import StockRecommender
import config


def analizar_con_config():
    """Analiza acciones usando la configuración personalizada"""
    
    # Aplicar perfil si está configurado
    if config.PERFIL_ACTIVO:
        config.aplicar_perfil(config.PERFIL_ACTIVO)
    
    # Mostrar configuración
    config.mostrar_configuracion()
    
    print("🔍 Iniciando análisis...\n")
    
    # Crear recomendador
    recommender = StockRecommender()
    recommender.analyzer.period = config.PERIODO_HISTORICO
    
    # Analizar
    signals = recommender.analyze_multiple_stocks(
        config.MIS_ACCIONES, 
        config.HORIZONTE_DIAS
    )
    
    # Aplicar filtros personalizados
    if signals:
        signals_filtradas = [
            s for s in signals
            if s['probability'] >= config.PROBABILIDAD_MINIMA
            and s['risk'] <= config.RIESGO_MAXIMO
            and s['avg_return'] >= config.RETORNO_MINIMO
            and s['samples'] >= config.MUESTRAS_MINIMAS
        ]
        
        print("\n" + "═"*80)
        print(f"📊 RESULTADOS DEL FILTRADO")
        print("═"*80)
        print(f"\nSeñales encontradas: {len(signals)}")
        print(f"Señales que pasan los filtros: {len(signals_filtradas)}")
        
        # Alertas especiales
        alertas = [
            s for s in signals_filtradas
            if s['probability'] >= config.ALERTA_PROBABILIDAD_ALTA
            and s['risk'] <= config.ALERTA_RIESGO_BAJO
        ]
        
        if alertas:
            print(f"\n🔔 ¡ALERTAS ESPECIALES! {len(alertas)} señal(es) de alta calidad")
            for alerta in alertas:
                print(f"   🌟 {alerta['symbol']}: {alerta['probability']:.0f}% prob, "
                      f"{alerta['risk']:.1f}% riesgo")
        
        # Limitar número de señales si está configurado
        if config.MAX_SEÑALES and len(signals_filtradas) > config.MAX_SEÑALES:
            print(f"\nℹ️  Mostrando las {config.MAX_SEÑALES} mejores señales de {len(signals_filtradas)} totales")
            signals_filtradas = signals_filtradas[:config.MAX_SEÑALES]
        
        # Mostrar recomendaciones
        recommender.print_recommendations(signals_filtradas, config.HORIZONTE_DIAS)
        
        # Guardar si está configurado
        if config.GUARDAR_CSV and signals_filtradas:
            recommender.export_to_csv(signals_filtradas, config.NOMBRE_CSV)
    
    else:
        print("\n❌ No se encontraron señales de compra en este momento.")
        print("💡 Intenta:")
        print("   • Reducir PROBABILIDAD_MINIMA en config.py")
        print("   • Aumentar RIESGO_MAXIMO en config.py")
        print("   • Agregar más acciones en MIS_ACCIONES")
        print("   • Cambiar el HORIZONTE_DIAS\n")


def menu_perfiles():
    """Menú para seleccionar perfil"""
    print("\n" + "═"*80)
    print("👤 SELECCIONAR PERFIL DE TRADING")
    print("═"*80 + "\n")
    
    for i, (nombre, perfil) in enumerate(config.PERFILES.items(), 1):
        print(f"{i}. {nombre.upper()}")
        print(f"   {perfil['descripcion']}")
        print(f"   Probabilidad ≥ {perfil['probabilidad_minima']}% | "
              f"Riesgo ≤ {perfil['riesgo_maximo']}% | "
              f"Retorno ≥ {perfil['retorno_minimo']}%")
        print()
    
    print("5. PERSONALIZADO (usar valores de config.py)")
    print("0. Cancelar\n")
    
    try:
        opcion = input("👉 Selecciona un perfil (0-5): ").strip()
        
        perfiles_lista = list(config.PERFILES.keys())
        
        if opcion == '0':
            print("\n👋 Cancelado\n")
            return None
        elif opcion == '5':
            return None
        elif opcion in ['1', '2', '3', '4']:
            idx = int(opcion) - 1
            return perfiles_lista[idx]
        else:
            print("\n❌ Opción no válida")
            return None
    except:
        print("\n❌ Error en la entrada")
        return None


def main():
    """Función principal"""
    print("\n" + "╔" + "═"*78 + "╗")
    print("║" + " "*15 + "🎯 ANÁLISIS CON CONFIGURACIÓN PERSONALIZADA" + " "*15 + "║")
    print("╚" + "═"*78 + "╝")
    
    # Preguntar si quiere cambiar de perfil
    if not config.PERFIL_ACTIVO:
        print("\nActualmente no hay perfil seleccionado.")
        respuesta = input("¿Quieres usar un perfil predefinido? (s/n): ").lower()
        
        if respuesta == 's':
            perfil = menu_perfiles()
            if perfil:
                config.PERFIL_ACTIVO = perfil
    
    # Ejecutar análisis
    analizar_con_config()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Análisis cancelado\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
