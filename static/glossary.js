/*
 * Glosario: una sola fuente de verdad.
 * Cada término se usa en los "?" (tooltips) y en la pestaña "Glosario".
 * group = sección donde aparece en el glosario.
 */
window.GLOSSARY = {
  // ───────── Tu inversión ─────────
  simbolo: {
    group: "Tu inversión", title: "Símbolo (ticker)",
    text: "Código corto con el que se identifica una acción o ETF en la bolsa. Ej.: AAPL = Apple, MSFT = Microsoft, QQQ = ETF del Nasdaq 100. Las acciones de la Bolsa Mexicana en Yahoo Finance terminan en .MX (ej. WALMEX.MX)."
  },
  precio_entrada: {
    group: "Tu inversión", title: "Precio de entrada (precio al señalar)",
    text: "El precio por acción en el momento en que marcaste la inversión. Es el punto de partida: toda ganancia o pérdida se mide contra este precio. Si al registrarla escribiste el precio real al que compraste en tu broker, se usa ese; si lo dejaste vacío, se usa el precio de mercado de ese instante."
  },
  precio_mercado_al_senalar: {
    group: "Tu inversión", title: "Precio de mercado al señalar",
    text: "El precio que tenía la acción en Yahoo Finance justo cuando presionaste \"Invertí en esta\". Puede diferir un poco del precio de entrada si escribiste manualmente el precio al que compraste."
  },
  precio_actual: {
    group: "Tu inversión", title: "Precio actual",
    text: "El último precio disponible en Yahoo Finance al momento de consultar. Puede tener hasta ~15 minutos de retraso. Fuera del horario de mercado (L–V 9:30–16:00 hora de Nueva York) es el precio de cierre más reciente. En inversiones cerradas, es el precio al que vendiste."
  },
  cambio_pct: {
    group: "Tu inversión", title: "Rendimiento / cambio %",
    text: "Cuánto ha subido (+) o bajado (−) el precio desde que señalaste la acción, en porcentaje. Fórmula: (precio actual ÷ precio de entrada − 1) × 100. Ej.: entraste a $100 y ahora vale $105 → +5%."
  },
  cambio_por_accion: {
    group: "Tu inversión", title: "Cambio por acción",
    text: "Diferencia en dólares entre el precio actual y el precio de entrada, por cada acción. Ej.: entrada $100, actual $103 → +$3.00 por acción."
  },
  ganancia: {
    group: "Tu inversión", title: "Ganancia / pérdida ($)",
    text: "Cuánto dinero vas ganando (verde, +) o perdiendo (rojo, −) en total: cambio por acción × número de acciones. Solo aparece si indicaste cuántas acciones compraste o cuánto dinero invertiste. Es una ganancia \"en papel\": no es real hasta que vendes, y no descuenta comisiones ni impuestos."
  },
  acciones: {
    group: "Tu inversión", title: "Número de acciones",
    text: "Cuántos títulos compraste. Muchos brokers permiten fracciones (ej. 0.25 acciones). Si en lugar de esto escribes el dinero invertido, se calcula solo: dinero ÷ precio de entrada."
  },
  dinero_invertido: {
    group: "Tu inversión", title: "Dinero invertido",
    text: "Cuántos dólares pusiste en esta inversión (número de acciones × precio de entrada). Es tu \"costo\"."
  },
  valor_actual: {
    group: "Tu inversión", title: "Valor actual de la posición",
    text: "Cuánto valen hoy tus acciones: número de acciones × precio actual. Si vendieras ahora (sin comisiones) recibirías aproximadamente esto."
  },
  cambio_dia: {
    group: "Tu inversión", title: "Cambio del día",
    text: "Cuánto se ha movido la acción hoy respecto al cierre del día hábil anterior. Sirve para saber si el movimiento de hoy es bueno o malo, independientemente de tu precio de entrada."
  },
  dias: {
    group: "Tu inversión", title: "Días en la inversión",
    text: "Días transcurridos desde que señalaste la acción (o hasta que la cerraste). Incluye fines de semana."
  },
  avance_objetivo: {
    group: "Tu inversión", title: "Avance hacia el retorno esperado",
    text: "Compara lo que llevas ganado con el \"retorno promedio\" histórico de la estrategia que generó la señal. 100% = ya alcanzaste lo que en promedio se ganaba en el pasado. Si es negativo, vas en contra. Solo aparece si la inversión vino de una recomendación."
  },
  tiempo_plazo: {
    group: "Tu inversión", title: "Tiempo transcurrido del plazo",
    text: "Qué porción del horizonte de la recomendación (ej. 30 días) ya pasó. Cuando llega a 100% la recomendación se puede evaluar: ¿subió o no en el plazo previsto?"
  },
  abierta: {
    group: "Tu inversión", title: "Inversión abierta",
    text: "Todavía tienes las acciones. Su ganancia/pérdida cambia con el precio del mercado cada vez que consultas."
  },
  cerrada: {
    group: "Tu inversión", title: "Inversión cerrada",
    text: "Ya vendiste. El resultado queda fijo con el precio de venta que registraste y ya no cambia. Si te equivocaste, puedes \"Reabrir\"."
  },
  precio_salida: {
    group: "Tu inversión", title: "Precio de venta (salida)",
    text: "Precio por acción al que vendiste. Si lo dejas vacío al cerrar, se usa el precio actual del mercado."
  },
  ganadoras: {
    group: "Tu inversión", title: "Ganadoras / perdedoras",
    text: "Cuántas de tus inversiones van arriba (precio actual mayor que el de entrada) y cuántas van abajo."
  },
  rendimiento_total: {
    group: "Tu inversión", title: "Rendimiento total del portafolio",
    text: "Ganancia/pérdida total en $ dividida entre el dinero total invertido. Solo cuenta las inversiones donde indicaste acciones o monto."
  },
  cambio_promedio: {
    group: "Tu inversión", title: "Cambio promedio",
    text: "Promedio simple del % de cambio de todas tus inversiones abiertas, sin importar cuánto dinero tenga cada una. Útil si no registraste montos."
  },

  // ───────── Recomendaciones ─────────
  fecha_rec: {
    group: "Recomendaciones", title: "Fecha de la recomendación",
    text: "Día y hora en que el analizador detectó la señal (hora del equipo donde se ejecutó: tu PC o el servidor)."
  },
  estrategia: {
    group: "Recomendaciones", title: "Estrategia",
    text: "La regla técnica que se cumplió hoy para esta acción. Hay 5: RSI Sobrevendido, Cruce Dorado, MACD Alcista, Rebote Bollinger y Momentum Fuerte (cada una explicada abajo). El analizador revisa cuántas veces se cumplió esa misma regla en los últimos 10 años y qué pasó después."
  },
  est_rsi: {
    group: "Estrategias", title: "RSI Sobrevendido",
    text: "Se activa cuando el RSI está por debajo de 35 (la acción cayó fuerte en poco tiempo) pero la tendencia de fondo sigue siendo alcista (media de 20 días > media de 50 días y precio > media de 20). Idea: comprar una caída temporal dentro de una tendencia sana."
  },
  est_cruce: {
    group: "Estrategias", title: "Cruce Dorado",
    text: "Se activa el día en que la media móvil de 50 días cruza hacia arriba la de 200 días, con RSI entre 40 y 70. Es una señal clásica de que la tendencia de largo plazo cambia de bajista a alcista."
  },
  est_macd: {
    group: "Estrategias", title: "MACD Alcista",
    text: "Se activa el día en que la línea MACD cruza hacia arriba su línea de señal, con RSI menor a 70 (no sobrecomprada). Indica que el impulso (momentum) se está volviendo positivo."
  },
  est_bollinger: {
    group: "Estrategias", title: "Rebote Bollinger",
    text: "Se activa cuando el precio cierra por debajo de la banda inferior de Bollinger, con RSI menor a 40 y tendencia de largo plazo alcista (media 50 > media 200). Idea: el precio se alejó demasiado hacia abajo de lo normal y suele regresar a su promedio."
  },
  est_momentum: {
    group: "Estrategias", title: "Momentum Fuerte",
    text: "Se activa cuando todo está alineado al alza: precio > media 20 > media 50 > media 200, RSI entre 50 y 75 y MACD por encima de su señal. Idea: subirse a una tendencia que ya es fuerte."
  },
  nivel: {
    group: "Recomendaciones", title: "Nivel de recomendación",
    text: "Clasificación automática según probabilidad y riesgo. 🟢 COMPRA FUERTE: probabilidad ≥ 70% y riesgo < 10%. 🟡 COMPRA MODERADA: probabilidad ≥ 65% y riesgo < 15%. 🟠 COMPRA CAUTELOSA: todo lo demás (la señal existe pero es más débil)."
  },
  probabilidad: {
    group: "Recomendaciones", title: "Probabilidad histórica",
    text: "De todas las veces en el pasado (≈10 años) en que esta acción cumplió la misma estrategia, en qué porcentaje de los casos el precio estaba más alto al terminar el plazo. Ej.: 75% = 3 de cada 4 veces subió. Es estadística del pasado, no una garantía."
  },
  riesgo: {
    group: "Recomendaciones", title: "Riesgo",
    text: "Pérdida promedio en los casos en que salió mal. Ej.: riesgo 5% = cuando la señal falló, en promedio la acción bajó 5% en el plazo. Más bajo es mejor."
  },
  retorno_promedio: {
    group: "Recomendaciones", title: "Retorno promedio esperado",
    text: "Ganancia promedio de todas las veces que se cumplió la señal en el pasado, contando aciertos y fallos. Ej.: +4% = en promedio la acción subió 4% en el plazo. Es una referencia, no una meta asegurada."
  },
  perdida_maxima: {
    group: "Recomendaciones", title: "Pérdida máxima histórica",
    text: "El peor resultado registrado en el pasado para esta señal en el plazo. Ej.: −19% = en el peor caso la acción cayó 19%. Te da una idea del escenario más feo que ya ocurrió (y podría ser peor)."
  },
  muestras: {
    group: "Recomendaciones", title: "Muestras",
    text: "Cuántas veces en el histórico se cumplió la estrategia (días analizados). Con pocas muestras (menos de ~30) la probabilidad es menos confiable; con muchas, la estadística es más sólida. Ojo: muchos días seguidos de una misma racha cuentan como muestras separadas."
  },
  precio_senal: {
    group: "Recomendaciones", title: "Precio de la señal",
    text: "Precio de cierre de la acción el día en que el analizador generó la recomendación. Se usa para evaluar si acertó al terminar el plazo. Es distinto de TU precio de entrada si invertiste otro día."
  },
  horizonte: {
    group: "Recomendaciones", title: "Horizonte / plazo",
    text: "Número de días hacia adelante que mide la estrategia (en config.py: HORIZONTE_DIAS, actualmente " + (window.HORIZONTE || 30) + "). \"Probabilidad de subir en 30 días\" significa comparar el precio de hoy con el de 30 días después."
  },
  fecha_evaluacion: {
    group: "Recomendaciones", title: "Fecha de evaluación",
    text: "Fecha de la señal + horizonte. A partir de ese día la recomendación se puede evaluar (botón \"Evaluar recomendaciones vencidas\" o el análisis automático) comparando el precio de ese momento con el precio de la señal."
  },
  resultado: {
    group: "Recomendaciones", title: "Resultado (pendiente / acierto / fallo)",
    text: "PENDIENTE: aún no termina el plazo (se indica cuántos días faltan). VENCIDA: el plazo ya terminó pero falta evaluarla (botón \"Evaluar recomendaciones vencidas\"). ✅ ACIERTO: al evaluarla el precio estaba más alto que el de la señal. ❌ FALLO: estaba igual o más bajo. Junto aparece el rendimiento real."
  },
  precision: {
    group: "Recomendaciones", title: "Precisión real",
    text: "De las recomendaciones ya evaluadas, qué porcentaje acertó de verdad. Compárala con la \"probabilidad histórica media\": si la precisión real es mucho menor, las estrategias están funcionando peor que en el pasado."
  },

  // ───────── Indicadores ─────────
  rsi: {
    group: "Indicadores técnicos", title: "RSI (Índice de Fuerza Relativa)",
    text: "Indicador de 0 a 100 que mide qué tan rápido subió o bajó el precio en los últimos 14 días. Menos de 30–35 = \"sobrevendida\" (cayó mucho, podría rebotar). Más de 70 = \"sobrecomprada\" (subió mucho, podría corregir). Entre 40 y 60 = neutral."
  },
  media_movil: {
    group: "Indicadores técnicos", title: "Media móvil (MA20, MA50, MA200)",
    text: "Promedio del precio de cierre de los últimos N días. MA20 ≈ tendencia de un mes, MA50 ≈ de un trimestre, MA200 ≈ de casi un año. Si el precio está por encima de la media, la tendencia en ese plazo es alcista."
  },
  macd: {
    group: "Indicadores técnicos", title: "MACD y línea de señal",
    text: "MACD = media exponencial de 12 días − media exponencial de 26 días; mide el impulso. La \"línea de señal\" es una media de 9 días del propio MACD. Cuando el MACD cruza por encima de la señal, el impulso se vuelve alcista."
  },
  bollinger: {
    group: "Indicadores técnicos", title: "Bandas de Bollinger",
    text: "Tres líneas: la media de 20 días y dos bandas a ±2 desviaciones estándar. Normalmente el precio se mueve dentro de las bandas; tocar la banda inferior significa que está inusualmente barato respecto a su promedio reciente."
  },
  volatilidad: {
    group: "Indicadores técnicos", title: "Volatilidad",
    text: "Qué tanto se mueve el precio de un día a otro. Una acción volátil puede subir o bajar mucho en poco tiempo: más oportunidad, pero también más riesgo."
  },

  // ───────── Conceptos generales ─────────
  etf: {
    group: "Conceptos generales", title: "ETF",
    text: "Fondo que cotiza en bolsa como una acción pero contiene muchas empresas. Ej.: QQQ (Nasdaq 100), SPY/VOO (S&P 500), SOXX (semiconductores), XLK (tecnología). Suelen ser menos riesgosos que una sola acción."
  },
  stop_loss: {
    group: "Conceptos generales", title: "Stop-loss",
    text: "Orden que pones en tu broker para vender automáticamente si el precio cae a cierto nivel (ej. −5% de tu entrada). Limita cuánto puedes perder. Esta app no lo ejecuta, pero puedes anotarlo en las notas."
  },
  ganancia_papel: {
    group: "Conceptos generales", title: "Ganancia \"en papel\" (no realizada)",
    text: "Ganancia o pérdida de una inversión que todavía no vendes. Puede cambiar en cualquier momento. Solo se vuelve real (realizada) al vender."
  },
  horario: {
    group: "Conceptos generales", title: "Horario del mercado",
    text: "La bolsa de EE. UU. opera de lunes a viernes de 9:30 a 16:00 hora de Nueva York (en Hermosillo: 6:30 a 13:00 en horario de verano de EE. UU., 7:30 a 14:00 en invierno). Fuera de ese horario los precios no se mueven (salvo pre/post-mercado)."
  },
  comisiones: {
    group: "Conceptos generales", title: "Comisiones e impuestos",
    text: "Los cálculos de esta app no incluyen comisiones del broker, tipo de cambio ni impuestos sobre ganancias. Tu ganancia neta real será algo menor."
  },
  yahoo: {
    group: "Conceptos generales", title: "Fuente de datos (Yahoo Finance)",
    text: "Todos los precios e históricos se descargan gratis de Yahoo Finance mediante la librería yfinance. Si Yahoo no responde o limita las consultas, verás \"precio no disponible\"; espera un minuto y actualiza."
  }
};
