# 📈 Finance - Analizador de Acciones

Sistema inteligente para encontrar oportunidades de compra en el mercado de valores basado en probabilidades históricas y análisis técnico.

## 🚀 Inicio Rápido

```bash
# Navegar al proyecto
cd C:\laragon\www\Finance

# Activar entorno virtual (si es necesario)
.venv\Scripts\Activate.ps1

# Ejecutar análisis rápido
python buscar_acciones.py
```

## 📁 Archivos Principales

| Archivo | Descripción | Uso |
|---------|-------------|-----|
| **buscar_acciones.py** | Análisis rápido de tus acciones favoritas | Uso diario (1 min) ⭐ |
| **dashboard.py** | Vista general de 23+ acciones | Análisis completo (3-5 min) |
| **inicio_rapido.py** | Tutorial interactivo paso a paso | Primera vez |
| **ejemplos_avanzados.py** | Menú con 7 ejemplos diferentes | Aprendizaje |
| **analizar_personalizado.py** | Usa configuración personalizada | Avanzado |

## ⚙️ Configuración

Edita **config.py** para personalizar:
- Lista de acciones a analizar
- Horizonte de tiempo (5, 10, 15, 30 días)
- Filtros de probabilidad y riesgo
- Perfiles de trading (conservador, moderado, agresivo)

## 📊 Ejemplo de Resultado

```
1. GOOGL - Estrategia: Rebote Bollinger
   ══════════════════════════════════════════════════════════════════
   Según esta estrategia, GOOGL tiene 75% probabilidad histórica de 
   subir en los próximos 15 días, con un riesgo del 5.1%.

   📊 Detalles:
      • Precio actual: $307.17
      • RSI: 24.1
      • Retorno promedio esperado: 3.87%
      • Pérdida máxima histórica: -19.35%
      • Muestras históricas: 57

   🟢 COMPRA FUERTE
```

## 📚 Documentación

- **[LEEME.txt](LEEME.txt)** - Resumen rápido del proyecto
- **[GUIA_COMPLETA.md](GUIA_COMPLETA.md)** - Guía detallada paso a paso
- **[README_STOCKS.md](README_STOCKS.md)** - Documentación técnica completa

## 🎯 Estrategias Implementadas

1. **RSI Sobrevendido** - Detecta acciones caídas con potencial de recuperación
2. **Cruce Dorado** - Identifica cambios de tendencia bajista a alcista
3. **MACD Alcista** - Detecta momentum ascendente fuerte
4. **Rebote Bollinger** - Encuentra rebotes en soportes técnicos
5. **Momentum Fuerte** - Identifica tendencias alcistas consolidadas

## 💡 Casos de Uso

### Análisis Diario (Recomendado)
```bash
python buscar_acciones.py
```
⏱️ 1 minuto | Perfecto cada mañana

### Vista del Mercado
```bash
python dashboard.py
```
⏱️ 3-5 minutos | Vista general completa

### Análisis Personalizado
```bash
# 1. Editar config.py con tus preferencias
# 2. Ejecutar:
python analizar_personalizado.py
```
⏱️ Variable | Máxima flexibilidad

### Explorar Opciones
```bash
python ejemplos_avanzados.py
```
⏱️ Interactivo | 7 ejemplos para aprender

## ⚠️ Advertencias

- ❌ **NO es asesoría financiera**
- ❌ Los resultados pasados **NO garantizan** resultados futuros
- ✅ Solo invierte lo que puedas perder
- ✅ Siempre investiga antes de comprar
- ✅ Usa stop-loss y gestiona tu riesgo

## 📦 Dependencias

```bash
pip install yfinance pandas numpy
```

## 🎨 Personalización Rápida

Edita `buscar_acciones.py` para cambiar las acciones:

```python
mis_acciones = [
    'TSLA',   # Tesla
    'AAPL',   # Apple
    'NVDA',   # Nvidia
    # Agrega las que quieras...
]
```

## 📈 Archivos Generados

- `mis_recomendaciones.csv` - Resultados de buscar_acciones.py
- `dashboard_signals.csv` - Resultados de dashboard.py
- `recomendaciones.csv` - Resultados de stock_analyzer.py

## 🔧 Solución de Problemas

**Sin señales encontradas:**
- Ajusta `PROBABILIDAD_MINIMA` en config.py
- Aumenta `RIESGO_MAXIMO` en config.py
- Prueba con más acciones

**Errores al descargar:**
- Verifica tu conexión a internet
- Algunos símbolos pueden no estar disponibles

**Muy lento:**
- Reduce el número de acciones
- Usa `buscar_acciones.py` en lugar de `stock_analyzer.py`

---

**Creado con ❤️ para traders inteligentes**
