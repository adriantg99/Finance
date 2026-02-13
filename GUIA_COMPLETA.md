# 🚀 Guía Completa - Analizador de Acciones

## 📚 TABLA DE CONTENIDOS
1. [Introducción](#introducción)
2. [Archivos del Proyecto](#archivos-del-proyecto)
3. [Cómo Empezar](#cómo-empezar)
4. [Ejemplos de Uso](#ejemplos-de-uso)
5. [Personalización](#personalización)
6. [Interpretación de Resultados](#interpretación-de-resultados)
7. [Preguntas Frecuentes](#preguntas-frecuentes)

---

## 🎯 INTRODUCCIÓN

Este sistema analiza acciones del mercado de valores y te proporciona recomendaciones de compra basadas en:
- ✅ Probabilidades históricas
- ✅ Análisis técnico (RSI, MACD, Bollinger, etc.)
- ✅ 5 estrategias diferentes de trading
- ✅ Evaluación de riesgo

**Ejemplo de resultado:**
```
Según esta estrategia, GOOGL tiene 75% probabilidad histórica de 
subir en los próximos 15 días, con un riesgo del 5.1%.
```

---

## 📁 ARCHIVOS DEL PROYECTO

### 🎬 Para Empezar
| Archivo | Descripción | ⏱️ Tiempo | 👍 Recomendado |
|---------|-------------|-----------|----------------|
| **inicio_rapido.py** | Tutorial guiado paso a paso | 2 min | ⭐⭐⭐ Principiantes |
| **buscar_acciones.py** | Análisis rápido de 8 acciones | 1 min | ⭐⭐⭐ Uso diario |

### 📊 Análisis Avanzado
| Archivo | Descripción | ⏱️ Tiempo |
|---------|-------------|-----------|
| **dashboard.py** | Vista resumida de 23+ acciones | 3-5 min |
| **stock_analyzer.py** | Análisis completo de 30+ acciones | 5-7 min |
| **ejemplos_avanzados.py** | Menú interactivo con 7 ejemplos | Variable |

### ⚙️ Configuración
| Archivo | Descripción |
|---------|-------------|
| **config.py** | Configuración personalizable (perfiles, filtros, etc.) |
| **analizar_personalizado.py** | Usa tu configuración de config.py |

---

## 🚀 CÓMO EMPEZAR

### Paso 1: Instalar Dependencias
```bash
pip install yfinance pandas numpy
```

### Paso 2: Primera Ejecución
```bash
python inicio_rapido.py
```

O directamente:
```bash
python buscar_acciones.py
```

### Paso 3: Ver Resultados
El sistema mostrará en pantalla las recomendaciones y guardará un archivo CSV con los detalles.

---

## 💡 EJEMPLOS DE USO

### Ejemplo 1: Análisis Rápido Diario
```bash
python buscar_acciones.py
```
✅ Rápido (1 minuto)  
✅ Analiza tus acciones favoritas  
✅ Perfecto para revisar cada mañana

### Ejemplo 2: Dashboard Completo
```bash
python dashboard.py
```
✅ Vista general del mercado  
✅ Top 5 oportunidades  
✅ Resumen por acción

### Ejemplo 3: Con Configuración Personalizada
```bash
# 1. Edita config.py con tus preferencias
# 2. Ejecuta:
python analizar_personalizado.py
```
✅ Usa perfiles predefinidos (conservador, moderado, agresivo)  
✅ Filtra por tus criterios  
✅ Máxima flexibilidad

### Ejemplo 4: Explorar Opciones
```bash
python ejemplos_avanzados.py
```
Menú interactivo con:
- Análisis de una acción específica
- Filtrar por probabilidad alta (>70%)
- Filtrar por bajo riesgo (<10%)
- Comparar horizontes de tiempo
- Y más...

---

## 🎨 PERSONALIZACIÓN

### Cambiar las Acciones a Analizar
Edita `buscar_acciones.py`:
```python
mis_acciones = [
    'TSLA',   # Tesla
    'AAPL',   # Apple
    'NVDA',   # Nvidia
    # Agrega las que quieras
]
```

### Usar Perfiles Predefinidos
Edita `config.py`:
```python
PERFIL_ACTIVO = 'conservador'  # o 'moderado', 'agresivo', 'day_trader'
```

**Perfiles disponibles:**
- **Conservador**: Alta probabilidad (≥70%), bajo riesgo (<10%)
- **Moderado**: Probabilidad ≥60%, riesgo <15%
- **Agresivo**: Probabilidad ≥55%, riesgo <20%
- **Day Trader**: Probabilidad ≥65%, riesgo <12%, retorno ≥5%

### Ajustar Horizonte de Tiempo
```python
horizonte = 15  # Días hacia adelante
```
Valores comunes: 5 (corto plazo), 10, 15, 30 (mediano plazo)

### Filtros Personalizados
En `config.py`:
```python
PROBABILIDAD_MINIMA = 65  # % mínimo
RIESGO_MAXIMO = 12        # % máximo
RETORNO_MINIMO = 3        # % mínimo esperado
```

---

## 📈 INTERPRETACIÓN DE RESULTADOS

### Componentes de una Recomendación

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

### Qué Significa Cada Elemento

| Elemento | Significado |
|----------|-------------|
| **Probabilidad** | % de veces que la acción subió históricamente en esta situación |
| **Riesgo** | Promedio de pérdidas cuando la estrategia falla |
| **Retorno promedio** | Ganancia media esperada si sube |
| **Pérdida máxima** | Peor escenario histórico registrado |
| **Muestras históricas** | Cantidad de datos (más = más confiable) |
| **RSI** | Momentum (< 30 = sobrevendido, > 70 = sobrecomprado) |

### Niveles de Recomendación

| Indicador | Significado |
|-----------|-------------|
| 🟢 **COMPRA FUERTE** | Probabilidad ≥ 70% Y Riesgo < 10% |
| 🟡 **COMPRA MODERADA** | Probabilidad ≥ 65% Y Riesgo < 15% |
| 🟠 **COMPRA CAUTELOSA** | Otras combinaciones (prob ≥ 50%) |

### Estrategias Explicadas

1. **RSI Sobrevendido**: Busca acciones que cayeron mucho pero tienen tendencia alcista
2. **Cruce Dorado**: Detecta cuando la tendencia cambia de bajista a alcista
3. **MACD Alcista**: Identifica momentum ascendente fuerte
4. **Rebote Bollinger**: Encuentra rebotes en soportes técnicos
5. **Momentum Fuerte**: Detecta tendencias alcistas consolidadas

---

## ❓ PREGUNTAS FRECUENTES

### ¿Los resultados son una garantía?
**No.** El sistema usa datos históricos para calcular probabilidades. Los mercados cambian y el pasado no garantiza el futuro.

### ¿Cuándo debo ejecutar el análisis?
- **Diariamente**: Por la mañana antes de que abra el mercado
- **Semanalmente**: Los domingos para planificar la semana
- **Antes de comprar**: Para validar tu decisión

### ¿Qué hacer si no encuentro señales?
Es normal. No siempre hay oportunidades. Puedes:
1. Reducir `PROBABILIDAD_MINIMA` en `config.py`
2. Aumentar `RIESGO_MAXIMO`
3. Agregar más acciones a la lista
4. Intentar con diferentes horizontes (5, 10, 30 días)

### ¿Cómo sé si una señal es buena?
Busca:
- ✅ Probabilidad ≥ 70%
- ✅ Riesgo < 10%
- ✅ Muestras históricas ≥ 30
- ✅ Retorno esperado ≥ 5%

### ¿Puedo analizar acciones de otros países?
Sí, pero usa los símbolos correctos de Yahoo Finance. Por ejemplo:
- USA: `AAPL`, `TSLA`
- México: `AMXL.MX`, `WALMEX.MX`
- España: `TEF.MC`, `SAN.MC`

### ¿Cuánto capital necesito?
El sistema solo analiza. Tú decides cuánto invertir. Regla general:
- No inviertas más del 2-5% de tu capital por operación
- Siempre usa stop-loss
- Diversifica tu portafolio

### ¿Qué hago con los archivos CSV?
Los CSV contienen todos los detalles. Puedes:
1. Abrirlos en Excel para análisis
2. Hacer seguimiento de recomendaciones pasadas
3. Comparar resultados entre días
4. Crear tu propia base de datos

### Error: "No module named yfinance"
```bash
pip install yfinance pandas numpy
```

### Las descargas son muy lentas
- Es normal con muchas acciones
- Reduce la lista en `buscar_acciones.py`
- Usa `dashboard.py` que optimiza las descargas

---

## ⚠️ ADVERTENCIAS IMPORTANTES

### 1. No es Asesoría Financiera
Este es un sistema educativo. No reemplaza la asesoría de un profesional.

### 2. Gestión de Riesgo
Siempre:
- 📊 Diversifica tu portafolio
- 💰 Solo invierte lo que puedes perder
- 🛡️ Usa stop-loss
- 📚 Investiga cada empresa

### 3. Contexto del Mercado
Las probabilidades históricas no consideran:
- Noticias recientes
- Earnings reports
- Crisis económicas
- Cambios regulatorios

**Conclusión**: Usa este sistema como una herramienta más en tu análisis, no como la única.

---

## 🔧 SOLUCIÓN DE PROBLEMAS

### Problema: Sin señales encontradas
**Solución**: Ajusta filtros en `config.py` o agrega más acciones

### Problema: Errores al descargar datos
**Solución**: Verifica internet, algunos símbolos pueden estar delisted

### Problema: Resultados inconsistentes
**Solución**: Los mercados cambian. Ejecuta el análisis regularmente

### Problema: Muy lento
**Solución**: Reduce número de acciones o usa `buscar_acciones.py` en lugar de `stock_analyzer.py`

---

## 📞 PRÓXIMOS PASOS

1. ✅ Ejecuta `inicio_rapido.py` para familiarizarte
2. ✅ Prueba `buscar_acciones.py` con tus acciones favoritas
3. ✅ Personaliza `config.py` según tu perfil
4. ✅ Usa `dashboard.py` cada mañana
5. ✅ Explora `ejemplos_avanzados.py` para casos específicos

---

## 🎓 APRENDIZAJE CONTINUO

### Recursos Recomendados
- Aprende análisis técnico (RSI, MACD, Bollinger)
- Estudia gestión de riesgo
- Practica con paper trading primero
- Lee sobre value investing

### Mejora el Sistema
- Agrega tus propias estrategias en `stock_analyzer.py`
- Crea alertas por email o Telegram
- Implementa backtesting más detallado
- Añade análisis fundamental

---

**¡Feliz Trading! 📈💰**

*Recuerda: La disciplina y la gestión de riesgo son más importantes que cualquier estrategia.*
