"""
INICIO RÁPIDO - Tutorial paso a paso
"""

print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║   📈 ANALIZADOR DE ACCIONES - GUÍA DE INICIO RÁPIDO                      ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝

🎯 ¿Qué hace este sistema?

Analiza acciones en tiempo real y te dice:
✅ Cuál es la probabilidad histórica de que suban
✅ Cuál es el riesgo de cada operación
✅ Qué estrategia usar para cada acción
✅ Cuándo comprar según patrones históricos

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 ARCHIVOS DISPONIBLES:

1️⃣  buscar_acciones.py
    → Analiza una lista personalizada de acciones
    → ⏱️ Rápido (8 acciones)
    → 👍 RECOMENDADO PARA EMPEZAR

2️⃣  stock_analyzer.py
    → Analiza 30+ acciones populares
    → ⏱️ Tarda más (3-5 minutos)
    → 👍 Para análisis completo

3️⃣  ejemplos_avanzados.py
    → Menú interactivo con 7 ejemplos
    → 🎓 Para aprender a usar el sistema
    → 👍 Recomendado después de probar los otros

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 EJECUTA TU PRIMER ANÁLISIS:

En la terminal, ejecuta:

    python buscar_acciones.py

O si tienes un entorno virtual:

    .venv/Scripts/python.exe buscar_acciones.py

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎨 PERSONALIZA TUS ACCIONES:

1. Abre: buscar_acciones.py
2. Encuentra la sección:
   
   mis_acciones = [
       'TSLA',   # Tesla
       'AAPL',   # Apple
       ...
   ]

3. Cambia las acciones por las que te interesen
4. Guarda y ejecuta de nuevo

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 EJEMPLO DE RESULTADO:

1. TSLA - Estrategia: RSI Sobrevendido
   ══════════════════════════════════════════════════════════════════
   Según esta estrategia, TSLA tiene 68% probabilidad histórica de 
   subir en los próximos 15 días, con un riesgo del 12.0%.

   📊 Detalles:
      • Precio actual: $245.50
      • RSI: 32.5
      • Retorno promedio esperado: 8.50%
      • Pérdida máxima histórica: -15.20%
      • Muestras históricas: 45

   🟢 COMPRA FUERTE

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 CONSEJOS:

✓ Ejecuta el análisis diariamente para encontrar nuevas oportunidades
✓ Los archivos CSV te permiten hacer seguimiento de las señales
✓ Usa el menú interactivo (ejemplos_avanzados.py) para experimentar
✓ Ajusta el horizonte de días según tu estrategia (5, 10, 15, 30 días)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  IMPORTANTE:

Este sistema usa datos históricos. Los resultados pasados NO garantizan
resultados futuros. Siempre:

🔍 Investiga cada empresa antes de invertir
💰 Solo invierte lo que puedas perder
📚 Diversifica tu portafolio
🤝 Considera consultar con un asesor financiero

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎓 PRÓXIMOS PASOS:

1. Ejecuta: python buscar_acciones.py
2. Revisa las recomendaciones
3. Abre el CSV generado para ver más detalles
4. Prueba ejemplos_avanzados.py para explorar opciones
5. Personaliza las estrategias según tus preferencias

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

¿Listo para empezar? 🚀

""")

print("\n👉 Presiona Enter para ejecutar tu primer análisis...")
input()

print("\n🔄 Ejecutando buscar_acciones.py...\n")

# Importar y ejecutar
from buscar_acciones import main
main()
