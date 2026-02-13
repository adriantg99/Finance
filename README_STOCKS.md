# 📈 Analizador de Acciones - Recomendaciones de Compra

Sistema inteligente para encontrar oportunidades de compra en el mercado de valores basado en probabilidades históricas y análisis técnico.

## 🎯 Características

- ✅ Analiza múltiples acciones simultáneamente
- ✅ 5 estrategias de trading diferentes
- ✅ Calcula probabilidad histórica de éxito
- ✅ Evalúa el riesgo de cada operación
- ✅ Genera recomendaciones claras
- ✅ Exporta resultados a CSV

## 🚀 Instalación

```bash
pip install yfinance pandas numpy
```

## 📖 Uso Rápido

### Opción 1: Análisis Simple
```bash
python buscar_acciones.py
```

### Opción 2: Análisis Completo (30+ acciones)
```bash
python stock_analyzer.py
```

## 🎨 Personalización

Edita el archivo `buscar_acciones.py` para analizar tus acciones favoritas:

```python
mis_acciones = [
    'TSLA',   # Tesla
    'AAPL',   # Apple
    'MSFT',   # Microsoft
    # Agrega más aquí...
]
```

## 📊 Estrategias Implementadas

1. **RSI Sobrevendido**: Detecta acciones sobrevendidas con tendencia alcista
2. **Cruce Dorado**: Identifica cuando MA50 cruza por encima de MA200
3. **MACD Alcista**: Detecta señales de compra en el MACD
4. **Rebote Bollinger**: Encuentra rebotes en la banda inferior
5. **Momentum Fuerte**: Identifica tendencias alcistas fuertes

## 📈 Ejemplo de Salida

```
1. TSLA - Estrategia: RSI Sobrevendido
   ======================================================================
   Según esta estrategia, TSLA tiene 68% probabilidad histórica de subir
   en los próximos 15 días, con un riesgo del 12.0%.

   📊 Detalles:
      • Precio actual: $245.50
      • RSI: 32.5
      • Retorno promedio esperado: 8.50%
      • Pérdida máxima histórica: -15.20%
      • Muestras históricas: 45

   🟢 COMPRA FUERTE
```

## ⚙️ Parámetros Ajustables

En el código puedes modificar:

- `horizon`: Días hacia adelante (por defecto: 15)
- `period`: Período de datos históricos (por defecto: "10y")
- Umbral de RSI, periodos de medias móviles, etc.

## 📁 Archivos Generados

- `recomendaciones.csv`: Todas las señales detectadas (stock_analyzer.py)
- `mis_recomendaciones.csv`: Señales de tus acciones (buscar_acciones.py)

## 🎯 Interpretación de Resultados

### Probabilidad
- **70%+**: Alta probabilidad de éxito
- **60-70%**: Probabilidad moderada
- **50-60%**: Probabilidad baja

### Riesgo
- **< 10%**: Riesgo bajo
- **10-15%**: Riesgo moderado
- **> 15%**: Riesgo alto

### Recomendaciones
- 🟢 **COMPRA FUERTE**: Prob ≥ 70% y Riesgo < 10%
- 🟡 **COMPRA MODERADA**: Prob ≥ 65% y Riesgo < 15%
- 🟠 **COMPRA CAUTELOSA**: Otras combinaciones

## ⚠️ Advertencia

Este sistema usa **datos históricos** para calcular probabilidades. Los resultados pasados no garantizan resultados futuros. Siempre:

- 🔍 Investiga cada empresa
- 💰 Invierte solo lo que puedas perder
- 📚 Diversifica tu portafolio
- 🤝 Consulta con un asesor financiero

## 🛠️ Solución de Problemas

### Error: "No module named 'yfinance'"
```bash
pip install yfinance
```

### Error al descargar datos
- Verifica tu conexión a internet
- Algunos símbolos pueden no estar disponibles
- Yahoo Finance puede tener límites de tasa

### Sin señales encontradas
- Es normal, no siempre hay oportunidades
- Prueba con más acciones
- Ajusta los parámetros de las estrategias

## 📝 Próximas Mejoras

- [ ] Interfaz web con Flask/Streamlit
- [ ] Alertas por email
- [ ] Backtesting más detallado
- [ ] Más estrategias
- [ ] Análisis fundamental
- [ ] Machine Learning para predicciones

## 📄 Licencia

Uso libre para fines educativos y personales.

---

**Creado con ❤️ para traders inteligentes**
