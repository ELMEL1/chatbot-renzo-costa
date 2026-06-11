const metricas = [
  { clave: "saludo", etiqueta: "Saludos" },
  { clave: "productos", etiqueta: "Productos" },
  { clave: "precios", etiqueta: "Precios" },
  { clave: "promociones", etiqueta: "Promociones" },
  { clave: "delivery", etiqueta: "Delivery" },
  { clave: "seguimiento_pedido", etiqueta: "Seguimiento de pedido" },
  { clave: "reclamos", etiqueta: "Reclamos" },
  { clave: "garantia", etiqueta: "Garantia" },
  { clave: "tallas", etiqueta: "Tallas" },
  { clave: "materiales", etiqueta: "Materiales" },
  { clave: "horarios", etiqueta: "Horarios" },
  { clave: "ubicacion", etiqueta: "Ubicacion" },
  { clave: "devoluciones", etiqueta: "Cambios y devoluciones" },
  { clave: "contacto", etiqueta: "Contacto" },
  { clave: "pagos", etiqueta: "Pagos" },
  { clave: "despedida", etiqueta: "Despedidas" },
  { clave: "desconocido", etiqueta: "No entendidas" }
];

const formatearNumero = numero => new Intl.NumberFormat("es-PE").format(numero ?? 0);

function obtenerRanking(data) {
  return metricas
    .map(metrica => ({
      ...metrica,
      valor: data[metrica.clave] ?? 0
    }))
    .sort((a, b) => b.valor - a.valor);
}

function renderResumen(data, ranking) {
  const total = data.total_consultas ?? 0;
  const principal = ranking[0] ?? { etiqueta: "Sin datos", valor: 0 };
  const noEntendidas = data.desconocido ?? 0;
  const entendidas = Math.max(total - noEntendidas, 0);
  const tasaEntendidas = total > 0 ? Math.round((entendidas / total) * 100) : 0;

  document.getElementById("resumenMetricas").innerHTML = `
    <article class="metric-card featured">
      <span>Total consultas</span>
      <strong>${formatearNumero(total)}</strong>
      <small>Interacciones registradas por el chatbot</small>
    </article>
    <article class="metric-card">
      <span>Mas consultado</span>
      <strong>${principal.etiqueta}</strong>
      <small>${formatearNumero(principal.valor)} consultas detectadas</small>
    </article>
    <article class="metric-card">
      <span>Consultas entendidas</span>
      <strong>${tasaEntendidas}%</strong>
      <small>${formatearNumero(entendidas)} de ${formatearNumero(total)} clasificadas</small>
    </article>
  `;
}

function renderRanking(data, ranking) {
  const maximo = Math.max(...ranking.map(item => item.valor), 1);

  document.getElementById("rankingMetricas").innerHTML = ranking
    .slice(0, 8)
    .map((item, index) => {
      const porcentaje = Math.round((item.valor / maximo) * 100);

      return `
        <div class="ranking-item">
          <div class="ranking-topline">
            <span>${index + 1}. ${item.etiqueta}</span>
            <strong>${formatearNumero(item.valor)}</strong>
          </div>
          <div class="ranking-bar" aria-label="${item.etiqueta}: ${item.valor}">
            <span style="width: ${porcentaje}%"></span>
          </div>
        </div>
      `;
    })
    .join("");
}

function renderDetalle(data) {
  document.getElementById("stats").innerHTML = metricas
    .map(item => `
      <article class="mini-metric">
        <span>${item.etiqueta}</span>
        <strong>${formatearNumero(data[item.clave] ?? 0)}</strong>
      </article>
    `)
    .join("");
}

fetch("/metrics")
  .then(response => {
    if (!response.ok) {
      throw new Error("No se pudo cargar metrics.json");
    }

    return response.json();
  })
  .then(data => {
    const ranking = obtenerRanking(data);

    document.getElementById("estadoDashboard").textContent = "Datos actualizados";
    renderResumen(data, ranking);
    renderRanking(data, ranking);
    renderDetalle(data);
  })
  .catch(() => {
    document.getElementById("estadoDashboard").textContent = "Servidor no disponible";
    document.getElementById("resumenMetricas").innerHTML = `
      <article class="metric-card featured">
        <span>Sin conexion</span>
        <strong>Flask</strong>
        <small>Inicia el backend en http://127.0.0.1:5000 para ver las metricas.</small>
      </article>
    `;
    document.getElementById("rankingMetricas").innerHTML = "";
    document.getElementById("stats").innerHTML = "";
  });
