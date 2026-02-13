"""
═══════════════════════════════════════════════════════════════════════════════
                     📈 PROYECTO: ANALIZADOR DE ACCIONES
═══════════════════════════════════════════════════════════════════════════════

🎯 OBJETIVO:
   Encontrar oportunidades de compra en el mercado de valores basándose en
   probabilidades históricas y análisis técnico.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 ARCHIVOS CREADOS (9 archivos):

┌─ PRINCIPALES ────────────────────────────────────────────────────────────┐
│                                                                          │
│  1. 🎬 inicio_rapido.py           - Tutorial guiado (EMPIEZA AQUÍ)      │
│  2. 🚀 buscar_acciones.py         - Análisis rápido diario              │
│  3. 📊 dashboard.py               - Vista general del mercado           │
│  4. 🧠 stock_analyzer.py          - Motor principal (30+ acciones)      │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘

┌─ CONFIGURACIÓN Y EJEMPLOS ───────────────────────────────────────────────┐
│                                                                          │
│  5. ⚙️  config.py                  - Configuración personalizable        │
│  6. 🎯 analizar_personalizado.py  - Usa tu config personalizada         │
│  7. 🎓 ejemplos_avanzados.py      - 7 ejemplos interactivos             │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘

┌─ DOCUMENTACIÓN ──────────────────────────────────────────────────────────┐
│                                                                          │
│  8. 📖 README_STOCKS.md           - README del proyecto                 │
│  9. 📚 GUIA_COMPLETA.md           - Guía detallada de uso               │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ CARACTERÍSTICAS PRINCIPALES:

   ✅ Analiza múltiples acciones simultáneamente
   ✅ 5 estrategias de trading diferentes
   ✅ Calcula probabilidad histórica de éxito
   ✅ Evalúa riesgo de cada operación
   ✅ Genera recomendaciones claras y accionables
   ✅ Exporta resultados a CSV
   ✅ Perfiles predefinidos (conservador, moderado, agresivo)
   ✅ Completamente personalizable

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 5 ESTRATEGIAS IMPLEMENTADAS:

   1. 📉 RSI Sobrevendido       - Detecta acciones caídas con potencial
   2. 🌟 Cruce Dorado           - Cambio de tendencia bajista a alcista
   3. 📈 MACD Alcista           - Momentum ascendente fuerte
   4. 🎯 Rebote Bollinger       - Rebotes en soportes técnicos
   5. 🚀 Momentum Fuerte        - Tendencias alcistas consolidadas

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 EJEMPLO DE SALIDA:

   ┌──────────────────────────────────────────────────────────────────────┐
   │                                                                      │
   │  1. GOOGL - Estrategia: Rebote Bollinger                            │
   │     ══════════════════════════════════════════════════════════       │
   │     Según esta estrategia, GOOGL tiene 75% probabilidad             │
   │     histórica de subir en los próximos 15 días, con un              │
   │     riesgo del 5.1%.                                                │
   │                                                                      │
   │     📊 Detalles:                                                     │
   │        • Precio actual: $307.17                                     │
   │        • RSI: 24.1                                                  │
   │        • Retorno promedio esperado: 3.87%                           │
   │        • Pérdida máxima histórica: -19.35%                          │
   │        • Muestras históricas: 57                                    │
   │                                                                      │
   │     🟢 COMPRA FUERTE                                                │
   │                                                                      │
   └──────────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 INICIO RÁPIDO (3 PASOS):

   1. Instalar dependencias:
      pip install yfinance pandas numpy

   2. Ejecutar primer análisis:
      python inicio_rapido.py

   3. Personalizar y usar:
      python buscar_acciones.py

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎨 CASOS DE USO:

   ✦ Análisis Diario Rápido
     → python buscar_acciones.py (1 minuto)

   ✦ Vista General del Mercado
     → python dashboard.py (3-5 minutos)

   ✦ Análisis Personalizado
     → Edita config.py + ejecuta analizar_personalizado.py

   ✦ Explorar y Aprender
     → python ejemplos_avanzados.py (menú interactivo)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚙️  PERFILES PREDEFINIDOS:

   🛡️  CONSERVADOR      Prob ≥70%, Riesgo <10%  (Seguridad)
   ⚖️  MODERADO         Prob ≥60%, Riesgo <15%  (Balance)
   🎯 AGRESIVO         Prob ≥55%, Riesgo <20%  (Alto retorno)
   ⚡ DAY TRADER       Prob ≥65%, Riesgo <12%  (Corto plazo)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 INDICADORES TÉCNICOS USADOS:

   • RSI (Relative Strength Index)
   • Medias Móviles (MA20, MA50, MA200)
   • MACD (Moving Average Convergence Divergence)
   • Bandas de Bollinger
   • Volatilidad histórica

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💾 ARCHIVOS GENERADOS:

   • mis_recomendaciones.csv    - Tus análisis personalizados
   • dashboard_signals.csv      - Análisis del dashboard
   • recomendaciones.csv        - Análisis completo

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  ADVERTENCIAS IMPORTANTES:

   🔴 Este sistema NO es asesoría financiera
   🔴 Los resultados pasados NO garantizan resultados futuros
   🔴 Solo invierte lo que puedas perder
   🔴 Siempre investiga antes de comprar
   🔴 Usa stop-loss y gestiona tu riesgo
   🔴 Diversifica tu portafolio

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎓 RECURSOS ADICIONALES:

   📖 Lee README_STOCKS.md        - Introducción al proyecto
   📚 Lee GUIA_COMPLETA.md        - Guía paso a paso detallada
   🎯 Ejecuta ejemplos_avanzados.py - Aprende con ejemplos

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔮 PRÓXIMAS MEJORAS POSIBLES:

   ⬜ Interfaz web con Flask/Streamlit
   ⬜ Alertas por email/Telegram
   ⬜ Backtesting detallado
   ⬜ Análisis fundamental
   ⬜ Machine Learning para predicciones
   ⬜ Integración con brokers
   ⬜ Análisis de sentimiento de noticias

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 CONSEJOS PARA EL ÉXITO:

   ✓ Ejecuta el análisis diariamente
   ✓ Combina con tu propio análisis
   ✓ No te bases solo en probabilidades
   ✓ Lee noticias de las empresas
   ✓ Aprende de cada operación
   ✓ Mantén un diario de trading
   ✓ Sé paciente y disciplinado

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎉 ¡LISTO PARA USAR!

   Tu proyecto está completamente configurado y funcional.
   
   👉 Siguiente paso: python inicio_rapido.py

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                         Creado con ❤️ para traders inteligentes
                         
═══════════════════════════════════════════════════════════════════════════════
"""

if __name__ == "__main__":
    print(__doc__)
    
    import os
    print("\n📁 Archivos del proyecto creados:\n")
    
    archivos = [
        'inicio_rapido.py',
        'buscar_acciones.py',
        'dashboard.py',
        'stock_analyzer.py',
        'config.py',
        'analizar_personalizado.py',
        'ejemplos_avanzados.py',
        'README_STOCKS.md',
        'GUIA_COMPLETA.md'
    ]
    
    for archivo in archivos:
        existe = "✅" if os.path.exists(archivo) else "❌"
        print(f"   {existe} {archivo}")
    
    print("\n" + "="*80)
    print("\n🚀 Todo listo! Ejecuta: python inicio_rapido.py\n")
