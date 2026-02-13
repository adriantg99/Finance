"""
CONFIGURACIÓN PERSONALIZADA
Ajusta aquí todos los parámetros según tus preferencias
"""

# ═══════════════════════════════════════════════════════════════════════════
# 🎯 LISTA DE ACCIONES
# ═══════════════════════════════════════════════════════════════════════════

# Define tus acciones favoritas aquí
MIS_ACCIONES = [
    # Tecnología
    'TSLA', 'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'AMD',
    
    # Puedes agregar más sectores:
     'JPM', 'V', 'MA',        # Finanzas
    # 'JNJ', 'PFE', 'UNH',     # Salud
    # 'XOM', 'CVX',            # Energía
    # 'WMT', 'HD', 'NKE',      # Retail
]

# ═══════════════════════════════════════════════════════════════════════════
# ⏱️ PARÁMETROS DE TIEMPO
# ═══════════════════════════════════════════════════════════════════════════

# Horizonte de predicción (días hacia adelante)
HORIZONTE_DIAS = 15  # Valores comunes: 5, 10, 15, 30

# Período de datos históricos a analizar
PERIODO_HISTORICO = "10y"  # Opciones: "1y", "2y", "5y", "10y", "max"

# ═══════════════════════════════════════════════════════════════════════════
# 📊 FILTROS DE SEÑALES
# ═══════════════════════════════════════════════════════════════════════════

# Probabilidad mínima para mostrar una señal (%)
PROBABILIDAD_MINIMA = 50  # Valores recomendados: 50-70

# Riesgo máximo aceptable (%)
RIESGO_MAXIMO = 20  # Valores recomendados: 10-20

# Retorno esperado mínimo (%)
RETORNO_MINIMO = 0  # Si quieres filtrar por retorno esperado

# Número mínimo de muestras históricas requeridas
MUESTRAS_MINIMAS = 10  # Para tener suficiente data histórica

# ═══════════════════════════════════════════════════════════════════════════
# 📈 PARÁMETROS DE INDICADORES TÉCNICOS
# ═══════════════════════════════════════════════════════════════════════════

# RSI
RSI_PERIODO = 14
RSI_SOBREVENDIDO = 35  # Valores comunes: 30-35
RSI_SOBRECOMPRADO = 70  # Valores comunes: 70-75

# Medias Móviles
MA_CORTA = 20
MA_MEDIA = 50
MA_LARGA = 200

# Bollinger Bands
BB_PERIODO = 20
BB_DESVIACIONES = 2

# MACD
MACD_RAPIDA = 12
MACD_LENTA = 26
MACD_SEÑAL = 9

# ═══════════════════════════════════════════════════════════════════════════
# 🎨 OPCIONES DE VISUALIZACIÓN
# ═══════════════════════════════════════════════════════════════════════════

# Mostrar colores en consola
USAR_COLORES = True

# Guardar resultados automáticamente
GUARDAR_CSV = True

# Nombre del archivo CSV
NOMBRE_CSV = "mis_recomendaciones.csv"

# Mostrar detalles completos o resumen
MODO_DETALLADO = True  # False para resumen más corto

# Número máximo de señales a mostrar (None para todas)
MAX_SEÑALES = None  # O un número como 10

# ═══════════════════════════════════════════════════════════════════════════
# 🔔 ALERTAS Y NOTIFICACIONES
# ═══════════════════════════════════════════════════════════════════════════

# Condiciones para alertas especiales
ALERTA_PROBABILIDAD_ALTA = 75  # Notificar si prob > este valor
ALERTA_RIESGO_BAJO = 8  # Notificar si riesgo < este valor

# ═══════════════════════════════════════════════════════════════════════════
# 🎯 PERFILES PREDEFINIDOS
# ═══════════════════════════════════════════════════════════════════════════

PERFILES = {
    'conservador': {
        'probabilidad_minima': 70,
        'riesgo_maximo': 10,
        'retorno_minimo': 3,
        'descripcion': 'Alta probabilidad, bajo riesgo'
    },
    'moderado': {
        'probabilidad_minima': 60,
        'riesgo_maximo': 15,
        'retorno_minimo': 2,
        'descripcion': 'Balance entre riesgo y retorno'
    },
    'agresivo': {
        'probabilidad_minima': 55,
        'riesgo_maximo': 20,
        'retorno_minimo': 0,
        'descripcion': 'Mayor tolerancia al riesgo'
    },
    'day_trader': {
        'probabilidad_minima': 65,
        'riesgo_maximo': 12,
        'retorno_minimo': 5,
        'descripcion': 'Trading de corto plazo'
    }
}

# Selecciona tu perfil aquí (o usa None para usar valores personalizados)
PERFIL_ACTIVO = None  # Opciones: 'conservador', 'moderado', 'agresivo', 'day_trader', None

# ═══════════════════════════════════════════════════════════════════════════
# 🚀 FUNCIÓN PARA APLICAR CONFIGURACIÓN
# ═══════════════════════════════════════════════════════════════════════════

def aplicar_perfil(perfil_nombre):
    """Aplica un perfil predefinido"""
    global PROBABILIDAD_MINIMA, RIESGO_MAXIMO, RETORNO_MINIMO
    
    if perfil_nombre and perfil_nombre in PERFILES:
        perfil = PERFILES[perfil_nombre]
        PROBABILIDAD_MINIMA = perfil['probabilidad_minima']
        RIESGO_MAXIMO = perfil['riesgo_maximo']
        RETORNO_MINIMO = perfil['retorno_minimo']
        print(f"\n✅ Perfil '{perfil_nombre}' aplicado: {perfil['descripcion']}\n")


def mostrar_configuracion():
    """Muestra la configuración actual"""
    print("\n" + "═"*80)
    print("⚙️  CONFIGURACIÓN ACTUAL")
    print("═"*80)
    print(f"\n📊 Acciones: {len(MIS_ACCIONES)} seleccionadas")
    print(f"⏱️  Horizonte: {HORIZONTE_DIAS} días")
    print(f"📅 Histórico: {PERIODO_HISTORICO}")
    print(f"\n🎯 Filtros:")
    print(f"   • Probabilidad mínima: {PROBABILIDAD_MINIMA}%")
    print(f"   • Riesgo máximo: {RIESGO_MAXIMO}%")
    print(f"   • Retorno mínimo: {RETORNO_MINIMO}%")
    print(f"   • Muestras mínimas: {MUESTRAS_MINIMAS}")
    
    if PERFIL_ACTIVO:
        print(f"\n👤 Perfil activo: {PERFIL_ACTIVO}")
        print(f"   {PERFILES[PERFIL_ACTIVO]['descripcion']}")
    
    print("\n" + "═"*80 + "\n")


# ═══════════════════════════════════════════════════════════════════════════
# 📝 EJEMPLO DE USO
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n🎨 Este es el archivo de configuración.")
    print("📝 Edítalo para personalizar tu análisis.\n")
    
    # Aplicar perfil si está configurado
    if PERFIL_ACTIVO:
        aplicar_perfil(PERFIL_ACTIVO)
    
    # Mostrar configuración
    mostrar_configuracion()
    
    print("💡 Para usar esta configuración, importa este archivo en tus scripts:")
    print("   from config import MIS_ACCIONES, HORIZONTE_DIAS, etc.\n")
