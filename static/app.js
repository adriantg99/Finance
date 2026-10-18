(() => {
  "use strict";
  const G = window.GLOSSARY || {};
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

  // ───────── formato ─────────
  const money = (v, signed = false) => {
    if (v === null || v === undefined || isNaN(v)) return "—";
    const s = new Intl.NumberFormat("es-MX", { style: "currency", currency: "USD", minimumFractionDigits: 2, maximumFractionDigits: Math.abs(v) < 1 && v !== 0 ? 4 : 2 }).format(Math.abs(v));
    if (!signed) return (v < 0 ? "−" : "") + s;
    return (v > 0 ? "+" : v < 0 ? "−" : "") + s;
  };
  const pct = (v, signed = true, d = 2) => {
    if (v === null || v === undefined || isNaN(v)) return "—";
    const s = Math.abs(v).toFixed(d) + "%";
    return signed ? (v > 0 ? "+" : v < 0 ? "−" : "") + s : (v < 0 ? "−" : "") + s;
  };
  const num = (v, d = 2) => (v === null || v === undefined || isNaN(v) ? "—" : Number(v).toLocaleString("es-MX", { maximumFractionDigits: d }));
  const tone = (v) => (v > 0 ? "good" : v < 0 ? "bad" : "");
  const dt = (iso, withTime = true) => {
    if (!iso) return "—";
    const hasTz = /[zZ]|[+-]\d\d:\d\d$/.test(iso);
    const d = new Date(hasTz ? iso : iso.replace(" ", "T"));
    if (isNaN(d)) return iso;
    return d.toLocaleString("es-MX", withTime ? { dateStyle: "medium", timeStyle: "short" } : { dateStyle: "medium" });
  };
  const ago = (iso) => {
    if (!iso) return "";
    const s = (Date.now() - new Date(iso).getTime()) / 1000;
    if (s < 90) return "hace un momento";
    if (s < 3600) return `hace ${Math.round(s / 60)} min`;
    return `hace ${Math.round(s / 3600)} h`;
  };
  const help = (term) => (G[term] ? `<span class="help" data-term="${term}" tabindex="0" aria-label="¿Qué es ${esc(G[term].title)}?">?</span>` : "");

  // ───────── API ─────────
  async function api(path, body) {
    const opt = body === undefined ? {} : { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) };
    const r = await fetch(path, opt);
    if (r.status === 401) { location.href = "/login"; throw new Error("Sesión expirada"); }
    const data = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(data.error || `Error ${r.status}`);
    return data;
  }
  function toast(msg) {
    const t = $("#toast"); t.textContent = msg; t.classList.remove("hidden");
    clearTimeout(toast._t); toast._t = setTimeout(() => t.classList.add("hidden"), 3500);
  }

  // ───────── tooltips ─────────
  const tip = $("#tip");
  let tipFor = null;
  function showTip(el) {
    const g = G[el.dataset.term]; if (!g) return;
    tip.innerHTML = `<b>${esc(g.title)}</b>${esc(g.text)}`;
    tip.classList.remove("hidden");
    const r = el.getBoundingClientRect();
    const w = Math.min(320, window.innerWidth - 24);
    tip.style.maxWidth = w + "px";
    let left = Math.min(Math.max(12, r.left + r.width / 2 - w / 2), window.innerWidth - w - 12);
    tip.style.left = left + "px";
    const below = r.bottom + 8;
    tip.style.top = below + "px";
    const h = tip.offsetHeight;
    if (below + h > window.innerHeight - 8) tip.style.top = Math.max(8, r.top - h - 8) + "px";
    tipFor = el;
  }
  const hideTip = () => { tip.classList.add("hidden"); tipFor = null; };
  document.addEventListener("mouseover", (e) => { const h = e.target.closest(".help[data-term]"); if (h) showTip(h); });
  document.addEventListener("mouseout", (e) => { if (e.target.closest(".help[data-term]")) hideTip(); });
  document.addEventListener("click", (e) => {
    const h = e.target.closest(".help[data-term]");
    if (h) { e.preventDefault(); e.stopPropagation(); tipFor === h ? hideTip() : showTip(h); return; }
    hideTip();
  }, true);
  document.addEventListener("focusin", (e) => { const h = e.target.closest?.(".help[data-term]"); if (h) showTip(h); });
  window.addEventListener("scroll", hideTip, { passive: true });

  // ───────── pestañas ─────────
  function setTab(name) {
    $$(".tab").forEach((t) => t.classList.toggle("active", t.dataset.tab === name));
    $$(".tab-panel").forEach((p) => p.classList.toggle("active", p.id === "tab-" + name));
    try { localStorage.setItem("finance.tab", name); } catch (_) {}
    if (name === "recs" && !state.recsLoaded) loadRecs();
  }
  $$(".tab").forEach((t) => t.addEventListener("click", () => setTab(t.dataset.tab)));

  // ───────── estado ─────────
  const state = { items: [], openDetail: new Set(), charts: {}, recs: [], recsLoaded: false };

  // ═════════════ MIS INVERSIONES ═════════════
  function tile(label, term, value, cls, desc) {
    return `<div class="tile"><div class="tile-label">${esc(label)} ${help(term)}</div>
      <div class="tile-value ${cls || ""}">${value}</div><div class="tile-desc">${esc(desc)}</div></div>`;
  }

  function renderSummary(sum) {
    const o = sum.open;
    $("#summary").innerHTML = [
      tile("Inversiones abiertas", "abierta", o.count, "", "Acciones que aún tienes."),
      tile("Dinero invertido", "dinero_invertido", o.invested ? money(o.invested) : "—", "", o.invested ? "Suma de lo que pagaste (abiertas)." : "Registra acciones o monto para verlo."),
      tile("Valor actual", "valor_actual", o.invested ? money(o.current_value) : "—", "", "Lo que valen hoy esas acciones."),
      tile("Ganancia / pérdida", "ganancia", o.invested ? money(o.profit, true) : "—", tone(o.profit), o.invested ? `${pct(o.profit_pct)} sobre lo invertido.` : "Requiere acciones o monto."),
      tile("Cambio promedio", "cambio_promedio", pct(o.avg_change_pct), tone(o.avg_change_pct), "Promedio del % de cada inversión."),
      tile("Ganadoras / perdedoras", "ganadoras", `<span class="good">${o.winners}</span> / <span class="bad">${o.losers}</span>`, "", "Arriba vs. abajo de tu precio de entrada."),
      sum.closed.count ? tile("Resultado ya vendido", "cerrada", sum.closed.invested ? money(sum.closed.profit, true) : pct(sum.closed.avg_change_pct), tone(sum.closed.invested ? sum.closed.profit : sum.closed.avg_change_pct), `${sum.closed.count} inversión(es) cerrada(s).`) : "",
    ].join("");
  }

  function kv(label, term, value, desc, cls = "") {
    return `<div class="kv-item"><div class="k">${esc(label)} ${help(term)}</div><div class="v ${cls}">${value}</div>${desc ? `<div class="d">${desc}</div>` : ""}</div>`;
  }

  function progressBlocks(it) {
    const r = it.recommendation;
    if (!r) return `<p class="tiny muted">Inversión agregada manualmente: no tiene una recomendación asociada, por eso no hay objetivo ni plazo de referencia.</p>`;
    let html = "";
    if (r.avg_return && it.change_pct !== null) {
      const p = (it.change_pct / r.avg_return) * 100;
      const w = Math.max(0, Math.min(100, p));
      html += `<div class="progress-block">
        <div class="progress-label"><span>Avance hacia el retorno esperado (${pct(r.avg_return)}) ${help("avance_objetivo")}</span><b class="${tone(p)}">${p.toFixed(0)}%</b></div>
        <div class="bar ${p >= 100 ? "good" : p < 0 ? "bad" : ""}"><span style="width:${p < 0 ? Math.min(100, -p) : w}%"></span></div>
        <div class="tiny muted">${p < 0 ? "Vas en dirección contraria al objetivo (en pérdida)." : p >= 100 ? "Ya superaste el retorno promedio histórico de esta señal." : `Te falta ${pct(r.avg_return - it.change_pct, false)} para llegar al promedio histórico.`}</div>
      </div>`;
    }
    const dp = Math.max(0, Math.min(100, (it.days_held / r.horizon_days) * 100));
    html += `<div class="progress-block">
      <div class="progress-label"><span>Tiempo transcurrido del plazo de ${r.horizon_days} días ${help("tiempo_plazo")}</span><b>${dp.toFixed(0)}%</b></div>
      <div class="bar"><span style="width:${dp}%"></span></div>
      <div class="tiny muted">${r.days_left > 0 ? `Faltan ${r.days_left} día(s) para la fecha de evaluación (${dt(r.evaluation_due_at, false)}).` : "El plazo de la recomendación ya terminó."}</div>
    </div>`;
    return html;
  }

  function invCard(it) {
    const closed = it.status === "closed";
    const r = it.recommendation;
    const levelCls = r && /FUERTE/.test(r.recommendation_level) ? "good" : r && /MODERADA/.test(r.recommendation_level) ? "warn" : "";
    const priceNote = closed ? `Precio de venta (${dt(it.closed_at)})` : it.price_source === "en_vivo" ? `Consultado ${ago(it.price_fetched_at)}` : "No disponible ahora (Yahoo no respondió)";
    const open = state.openDetail.has(it.id);
    return `<article class="inv" data-id="${it.id}">
      <div class="inv-main">
        <div>
          <div class="inv-sym">${esc(it.symbol)} ${help("simbolo")}</div>
          <div class="inv-meta">Señalada el ${dt(it.marked_at)}</div>
          <div>
            <span class="badge ${closed ? "" : "good"}">${closed ? "CERRADA" : "ABIERTA"}</span>
            ${r ? `<span class="badge">${esc(r.strategy)}</span><span class="badge ${levelCls}">${esc(r.recommendation_level || "")}</span>` : `<span class="badge">Manual</span>`}
          </div>
        </div>
        <div class="kv">
          ${kv("Precio al señalar", "precio_entrada", money(it.entry_price), it.market_price_at_mark && Math.abs(it.market_price_at_mark - it.entry_price) > 0.005 ? `Mercado en ese momento: ${money(it.market_price_at_mark)}` : "Tu punto de partida")}
          ${kv(closed ? "Precio de venta" : "Precio actual", closed ? "precio_salida" : "precio_actual", money(it.current_price), priceNote)}
          ${kv("Cambio por acción", "cambio_por_accion", money(it.change_per_share, true), "Actual − entrada", tone(it.change_per_share))}
          ${!closed ? kv("Cambio del día", "cambio_dia", pct(it.day_change_pct), "vs. cierre anterior", tone(it.day_change_pct)) : ""}
          ${kv("Acciones", "acciones", it.shares ? num(it.shares, 4) : "—", it.shares ? "" : "No registradas")}
          ${kv("Dinero invertido", "dinero_invertido", it.amount_invested ? money(it.amount_invested) : "—")}
          ${kv("Valor actual", "valor_actual", it.current_value !== null ? money(it.current_value) : "—")}
          ${kv("Días", "dias", num(it.days_held, 1), closed ? "hasta que vendiste" : "desde que la señalaste")}
        </div>
        <div class="inv-result">
          <div class="lbl">${closed ? "Resultado final" : "Vas"} ${help("cambio_pct")}</div>
          <div class="big ${tone(it.change_pct)}">${pct(it.change_pct)}</div>
          <div class="sub ${tone(it.profit)}">${it.profit !== null && it.profit !== undefined ? money(it.profit, true) : ""}</div>
          <div class="lbl">${it.profit !== null && it.profit !== undefined ? (it.profit >= 0 ? "ganancia" : "pérdida") + " en dólares " + help("ganancia") : "Agrega acciones o monto para ver $"}</div>
        </div>
      </div>
      <div class="inv-foot">
        <button class="btn btn-sm" data-act="detail">${open ? "▲ Ocultar" : "▼ Ver gráfica y detalles"}</button>
        <div class="btn-row">
          ${closed ? `<button class="btn btn-sm btn-ghost" data-act="reopen">Reabrir</button>` : `<button class="btn btn-sm" data-act="close">Cerrar (ya vendí)</button>`}
          <button class="btn btn-sm btn-ghost btn-danger" data-act="delete">Eliminar</button>
        </div>
      </div>
      <div class="inv-detail ${open ? "" : "hidden"}">
        <h3>Precio desde que la señalaste</h3>
        <p class="tiny muted">Línea azul = precio de la acción. Línea punteada = tu precio de entrada (${money(it.entry_price)}). Si la azul está por encima, vas ganando.</p>
        <div class="chart-box"><canvas></canvas></div>
        <div class="tiny muted chart-msg"></div>
        ${progressBlocks(it)}
        ${r ? `<h3 style="margin-top:16px">Datos de la recomendación original</h3>
          <div class="kv">
            ${kv("Fecha de la señal", "fecha_rec", dt(r.recommended_at))}
            ${kv("Precio de la señal", "precio_senal", money(r.entry_price_signal))}
            ${kv("Probabilidad", "probabilidad", pct(r.probability, false, 0))}
            ${kv("Riesgo", "riesgo", pct(r.risk, false, 1))}
            ${kv("Retorno promedio", "retorno_promedio", pct(r.avg_return))}
            ${kv("Pérdida máxima", "perdida_maxima", pct(r.max_loss), "", "bad")}
            ${kv("Muestras", "muestras", num(r.samples, 0))}
            ${kv("Plazo", "horizonte", r.horizon_days + " días")}
          </div>` : ""}
        ${it.notes ? `<div class="notes"><b>Notas:</b> ${esc(it.notes)}</div>` : ""}
      </div>
    </article>`;
  }

  function renderInvestments() {
    const open = state.items.filter((i) => i.status === "open");
    const closed = state.items.filter((i) => i.status === "closed");
    $("#openList").innerHTML = open.length ? open.map(invCard).join("") :
      `<div class="empty">Aún no marcas ninguna inversión.<br>Ve a <b>Recomendaciones del analizador</b> y presiona <b>"Invertí en esta"</b>, o usa <b>"+ Agregar inversión manualmente"</b>.</div>`;
    $("#closedList").innerHTML = closed.length ? closed.map(invCard).join("") : `<div class="empty">No tienes inversiones cerradas.</div>`;
    Object.values(state.charts).forEach((c) => c.destroy());
    state.charts = {};
    state.openDetail.forEach((id) => drawChart(id));
  }

  async function loadInvestments() {
    const btn = $("#refreshBtn");
    btn.disabled = true; btn.textContent = "⟳ Actualizando…";
    try {
      const data = await api("/api/investments");
      state.items = data.items;
      renderSummary(data.summary);
      renderInvestments();
      $("#lastUpdate").textContent = "Precios actualizados: " + new Date().toLocaleTimeString("es-MX", { timeStyle: "short" });
    } catch (e) {
      toast("No se pudieron cargar las inversiones: " + e.message);
    } finally {
      btn.disabled = false; btn.textContent = "⟳ Actualizar precios";
    }
  }

  async function drawChart(id) {
    const card = $(`.inv[data-id="${id}"]`); if (!card) return;
    const canvas = $("canvas", card), msg = $(".chart-msg", card);
    msg.textContent = "Cargando historial de precios…";
    try {
      const h = await api(`/api/investments/${id}/history`);
      const it = state.items.find((x) => x.id === id);
      let pts = h.points;
      if (it && it.current_price && it.status === "open") pts = pts.concat([{ t: new Date().toISOString(), close: it.current_price }]);
      if (!pts.length) { msg.textContent = "Aún no hay historial (la señalaste hace muy poco o el mercado está cerrado). Vuelve más tarde."; return; }
      msg.textContent = "";
      const intraday = (Date.now() - new Date(h.marked_at).getTime()) < 7 * 864e5;
      const labels = pts.map((p) => new Date(p.t).toLocaleString("es-MX", intraday ? { day: "2-digit", month: "short", hour: "2-digit", minute: "2-digit" } : { day: "2-digit", month: "short" }));
      const css = getComputedStyle(document.documentElement);
      const c = (v) => css.getPropertyValue(v).trim();
      if (!window.Chart) { msg.textContent = "No se pudo cargar la librería de gráficas (sin internet)."; return; }
      state.charts[id]?.destroy();
      state.charts[id] = new Chart(canvas, {
        type: "line",
        data: { labels, datasets: [
          { label: "Precio", data: pts.map((p) => p.close), borderColor: c("--primary"), backgroundColor: "transparent", pointRadius: 0, borderWidth: 2, tension: .2 },
          { label: "Tu precio de entrada", data: pts.map(() => h.entry_price), borderColor: c("--muted"), borderDash: [6, 5], pointRadius: 0, borderWidth: 1.5 },
        ] },
        options: {
          responsive: true, maintainAspectRatio: false, interaction: { mode: "index", intersect: false },
          plugins: { legend: { labels: { color: c("--muted") } },
            tooltip: { callbacks: { label: (ctx) => {
              const v = ctx.parsed.y;
              if (ctx.datasetIndex === 1) return ` Entrada: ${money(v)}`;
              return ` Precio: ${money(v)}  (${pct((v / h.entry_price - 1) * 100)} vs. entrada)`;
            } } } },
          scales: {
            x: { ticks: { color: c("--muted"), maxTicksLimit: 8 }, grid: { color: c("--border") } },
            y: { ticks: { color: c("--muted"), callback: (v) => "$" + v }, grid: { color: c("--border") } },
          },
        },
      });
    } catch (e) { msg.textContent = "No se pudo cargar el historial: " + e.message; }
  }

  document.addEventListener("click", async (e) => {
    const b = e.target.closest(".inv [data-act]"); if (!b) return;
    const card = b.closest(".inv"), id = Number(card.dataset.id);
    const it = state.items.find((x) => x.id === id);
    const act = b.dataset.act;
    if (act === "detail") {
      const d = $(".inv-detail", card);
      const show = d.classList.contains("hidden");
      d.classList.toggle("hidden", !show);
      b.textContent = show ? "▲ Ocultar" : "▼ Ver gráfica y detalles";
      show ? (state.openDetail.add(id), drawChart(id)) : state.openDetail.delete(id);
    } else if (act === "close") {
      const f = $("#closeForm"); f.reset(); f.id.value = id;
      f.exit_price.placeholder = it.current_price ? `Vacío = ${money(it.current_price)} (precio actual)` : "Precio de venta";
      $("#closeError").classList.add("hidden");
      openModal("#closeModal");
    } else if (act === "reopen") {
      await api(`/api/investments/${id}/reopen`, {}); toast("Inversión reabierta"); loadInvestments();
    } else if (act === "delete") {
      if (!confirm(`¿Eliminar el registro de ${it.symbol}? Esto no se puede deshacer.\n(Si ya vendiste, mejor usa "Cerrar" para conservar el resultado.)`)) return;
      await api(`/api/investments/${id}/delete`, {}); toast("Registro eliminado"); loadInvestments();
    }
  });

  // ═════════════ MODALES ═════════════
  function openModal(sel) { $(sel).classList.remove("hidden"); setTimeout(() => $(sel + " input:not([type=hidden]):not([readonly])")?.focus(), 30); }
  $$(".modal").forEach((m) => {
    m.addEventListener("click", (e) => { if (e.target === m || e.target.closest("[data-close]")) m.classList.add("hidden"); });
  });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") $$(".modal").forEach((m) => m.classList.add("hidden")); });

  let previewTimer;
  async function previewPrice(sym) {
    const box = $("#pricePreview");
    if (!sym) { box.textContent = ""; return; }
    box.textContent = "Buscando precio actual…";
    try {
      const p = await api(`/api/price/${encodeURIComponent(sym)}`);
      box.innerHTML = `Precio actual de <b>${esc(p.symbol)}</b>: <b>${money(p.price)}</b> <span class="muted">— es el que se guardará si dejas vacío "Precio al que compraste".</span>`;
    } catch (e) { box.innerHTML = `<span class="bad">${esc(e.message)}. Revisa el símbolo (como aparece en Yahoo Finance).</span>`; }
  }

  function openAdd(rec) {
    const f = $("#addForm"); f.reset();
    f.recommendation_id.value = rec ? rec.id : "";
    f.symbol.value = rec ? rec.symbol : "";
    f.symbol.readOnly = !!rec;
    $("#addTitle").textContent = rec ? `Invertí en ${rec.symbol}` : "Agregar inversión manualmente";
    $("#addSubtitle").innerHTML = rec
      ? `Recomendación #${rec.id} · ${esc(rec.strategy)} · ${pct(rec.probability, false, 0)} de probabilidad. Se guardará <b>este momento</b> como la fecha en que la señalaste.`
      : "Para acciones que compraste por tu cuenta. Se guardará este momento como fecha de inicio.";
    $("#addError").classList.add("hidden");
    openModal("#addModal");
    previewPrice(f.symbol.value);
  }
  $("#addManualBtn").addEventListener("click", () => openAdd(null));
  $("#addForm").symbol.addEventListener("input", (e) => {
    e.target.value = e.target.value.toUpperCase().replace(/\s/g, "");
    clearTimeout(previewTimer); previewTimer = setTimeout(() => previewPrice(e.target.value), 600);
  });
  $("#addForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const f = e.target, err = $("#addError");
    if (f.shares.value && f.amount.value) { err.textContent = "Llena solo uno: número de acciones o dinero invertido."; err.classList.remove("hidden"); return; }
    const btn = $("button[type=submit]", f); btn.disabled = true; btn.textContent = "Guardando…";
    try {
      await api("/api/investments", {
        symbol: f.symbol.value, recommendation_id: f.recommendation_id.value || null,
        shares: f.shares.value, amount: f.amount.value, entry_price: f.entry_price.value, notes: f.notes.value,
      });
      $("#addModal").classList.add("hidden");
      toast("✅ Inversión registrada. Ya aparece en Mis inversiones.");
      state.recsLoaded = false;
      setTab("inv");
      loadInvestments();
    } catch (ex) { err.textContent = ex.message; err.classList.remove("hidden"); }
    finally { btn.disabled = false; btn.textContent = "Guardar inversión"; }
  });
  $("#closeForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const f = e.target;
    try {
      await api(`/api/investments/${f.id.value}/close`, { exit_price: f.exit_price.value });
      $("#closeModal").classList.add("hidden"); toast("Inversión cerrada"); loadInvestments();
    } catch (ex) { $("#closeError").textContent = ex.message; $("#closeError").classList.remove("hidden"); }
  });

  // ═════════════ RECOMENDACIONES ═════════════
  function levelBadge(level) {
    const cls = /FUERTE/.test(level) ? "good" : /MODERADA/.test(level) ? "warn" : "";
    const icon = /FUERTE/.test(level) ? "🟢" : /MODERADA/.test(level) ? "🟡" : "🟠";
    return level ? `<span class="badge ${cls}">${icon} ${esc(level.replace("COMPRA ", ""))}</span>` : "";
  }
  function resultCell(r) {
    if (r.status === "evaluated") {
      return `${r.was_correct ? '<span class="badge good">✅ ACIERTO</span>' : '<span class="badge bad">❌ FALLO</span>'} <span class="${tone(r.actual_return_pct)}">${pct(r.actual_return_pct)}</span>`;
    }
    const due = new Date(r.evaluation_due_at.replace(" ", "T"));
    const days = Math.ceil((due - Date.now()) / 864e5);
    return days > 0 ? `<span class="badge">PENDIENTE · faltan ${days} d</span>` : `<span class="badge warn">VENCIDA · por evaluar</span>`;
  }
  function renderRecs() {
    const f = $("#recFilter").value, q = $("#recSearch").value.trim().toUpperCase();
    const rows = state.recs.filter((r) => (f === "all" || r.status === f) && (!q || r.symbol.includes(q)));
    $("#recTable tbody").innerHTML = rows.length ? rows.map((r) => `<tr>
      <td>${dt(r.recommended_at)}</td>
      <td class="sym">${esc(r.symbol)}</td>
      <td>${esc(r.strategy)}</td>
      <td>${levelBadge(r.recommendation_level)}</td>
      <td class="num">${pct(r.probability, false, 0)}</td>
      <td class="num">${pct(r.risk, false, 1)}</td>
      <td class="num ${tone(r.avg_return)}">${pct(r.avg_return)}</td>
      <td class="num bad">${pct(r.max_loss)}</td>
      <td class="num">${num(r.samples, 0)}</td>
      <td class="num">${num(r.rsi, 1)}</td>
      <td class="num">${money(r.entry_price)}</td>
      <td>${dt(r.evaluation_due_at, false)}</td>
      <td>${resultCell(r)}</td>
      <td>${r.invested_count ? `<span class="badge good">✔ Invertida</span> ` : ""}<button class="btn btn-sm ${r.invested_count ? "btn-ghost" : "btn-primary"}" data-rec="${r.id}">${r.invested_count ? "Invertir otra vez" : "Invertí en esta"}</button></td>
    </tr>`).join("") : `<tr><td colspan="14" class="muted" style="text-align:center;padding:20px">No hay recomendaciones con este filtro. Ejecuta un análisis arriba o cambia el filtro.</td></tr>`;
  }
  function renderRecSummary(s) {
    $("#recSummary").innerHTML = [
      tile("Recomendaciones guardadas", "resultado", s.total, "", "Total en la base de datos."),
      tile("Pendientes", "fecha_evaluacion", s.pending, "", "Aún dentro de su plazo."),
      tile("Evaluadas", "resultado", s.evaluated, "", "Plazo vencido y comparadas."),
      tile("Precisión real", "precision", s.accuracy_pct === null ? "—" : pct(s.accuracy_pct, false, 0), "", s.evaluated ? `${s.correct} de ${s.evaluated} acertaron.` : "Se calcula al evaluar las vencidas."),
      tile("Retorno real medio", "retorno_promedio", pct(s.avg_actual_return), tone(s.avg_actual_return), "Promedio real de las evaluadas."),
      tile("Prob. histórica media", "probabilidad", s.avg_predicted_prob ? pct(s.avg_predicted_prob, false, 0) : "—", "", "Lo que predecían (evaluadas)."),
    ].join("");
  }
  async function loadRecs() {
    try {
      const data = await api("/api/recommendations");
      state.recs = data.items; state.recsLoaded = true;
      renderRecSummary(data.summary); renderRecs();
    } catch (e) { toast("No se pudieron cargar las recomendaciones: " + e.message); }
  }
  $("#recFilter").addEventListener("change", renderRecs);
  $("#recSearch").addEventListener("input", renderRecs);
  $("#recTable").addEventListener("click", (e) => {
    const b = e.target.closest("[data-rec]"); if (!b) return;
    openAdd(state.recs.find((r) => r.id === Number(b.dataset.rec)));
  });

  // ───────── análisis en segundo plano ─────────
  let pollTimer;
  async function pollJob() {
    try {
      const s = await api("/api/analysis/status");
      const log = $("#jobLog");
      if (s.started_at) { log.classList.remove("hidden"); log.textContent = s.log.join("\n") || "Iniciando…"; log.scrollTop = log.scrollHeight; }
      $("#runQuick").disabled = $("#runFull").disabled = s.running;
      if (s.running) { pollTimer = setTimeout(pollJob, 2500); }
      else if (pollJob.wasRunning) { toast(s.error ? "El análisis terminó con error" : "✅ Análisis terminado"); loadRecs(); }
      pollJob.wasRunning = s.running;
    } catch (_) {}
  }
  async function runJob(rapido) {
    try { await api("/api/analysis/run", { rapido }); pollJob.wasRunning = true; toast("Análisis iniciado"); clearTimeout(pollTimer); pollJob(); }
    catch (e) { toast(e.message); }
  }
  $("#runQuick").addEventListener("click", () => runJob(true));
  $("#runFull").addEventListener("click", () => { if (confirm("El análisis completo revisa todas las acciones de config.py y puede tardar 10–25 minutos. ¿Continuar?")) runJob(false); });
  $("#evalBtn").addEventListener("click", async () => {
    try { const r = await api("/api/recommendations/evaluate", {}); toast(`Evaluadas: ${r.evaluated}`); loadRecs(); } catch (e) { toast(e.message); }
  });

  // ═════════════ GLOSARIO ═════════════
  function renderGlossary() {
    const q = $("#glosSearch").value.trim().toLowerCase();
    const groups = {};
    Object.entries(G).forEach(([k, g]) => {
      if (q && !(g.title + " " + g.text).toLowerCase().includes(q)) return;
      (groups[g.group] = groups[g.group] || []).push(g);
    });
    $("#glossary").innerHTML = Object.keys(groups).length ? Object.entries(groups).map(([name, items]) => `
      <div class="glos-group"><h2>${esc(name)}</h2><div class="glos-grid">
        ${items.map((g) => `<div class="glos-item"><h3>${esc(g.title)}</h3><p>${esc(g.text)}</p></div>`).join("")}
      </div></div>`).join("") : `<div class="empty">Ningún término coincide con "${esc(q)}".</div>`;
  }
  $("#glosSearch").addEventListener("input", renderGlossary);

  // ═════════════ inicio ═════════════
  $("#refreshBtn").addEventListener("click", () => { loadInvestments(); if (state.recsLoaded) loadRecs(); });
  renderGlossary();
  let saved = "inv"; try { saved = localStorage.getItem("finance.tab") || "inv"; } catch (_) {}
  setTab(saved);
  loadInvestments();
  pollJob();
  // refresco automático cada 2 minutos mientras la pestaña esté visible
  setInterval(() => { if (!document.hidden && !$$(".modal").some((m) => !m.classList.contains("hidden"))) loadInvestments(); }, 120000);
})();
