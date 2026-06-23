const form          = document.getElementById("searchForm");
const btnSearch     = document.getElementById("btnSearch");
const btnText       = btnSearch.querySelector(".btn-text");
const btnLoader     = btnSearch.querySelector(".btn-loader");
const resultsSection = document.getElementById("resultsSection");
const errorBox      = document.getElementById("errorBox");
const errorMsg      = document.getElementById("errorMsg");
const cardsGrid     = document.getElementById("cardsGrid");
const refTitle      = document.getElementById("refTitle");
const refMeta       = document.getElementById("refMeta");
const refTags       = document.getElementById("refTags");
const resultsTitle  = document.getElementById("resultsTitle");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const titulo  = document.getElementById("titulo").value.trim();
  const artista = document.getElementById("artista").value.trim();
  const n       = document.getElementById("n").value;

  if (!titulo) return;

  // Estado de carga
  setLoading(true);
  hideResults();
  hideError();

  try {
    const params = new URLSearchParams({ titulo, n });
    if (artista) params.append("artista", artista);

    const res  = await fetch(`/recomendar?${params}`);
    const data = await res.json();

    if (!res.ok) {
      showError(data.error || "Error al obtener recomendaciones.");
      return;
    }

    renderResults(data);

  } catch (err) {
    showError("No se pudo conectar con el servidor. Comprueba que la API está activa.");
  } finally {
    setLoading(false);
  }
});

// ── Render ────────────────────────────────────────────────────
function renderResults(data) {
  const { referencia, recomendaciones } = data;

  // Canción de referencia
  refTitle.textContent = referencia.track_name;
  refMeta.textContent  = referencia.artists;
  refTags.innerHTML    = `
    <span class="tag">${referencia.track_genre}</span>
    <span class="tag">${referencia.cluster_nombre}</span>
    <span class="tag">Popularidad ${referencia.popularity}</span>
  `;

  // Título sección
  resultsTitle.innerHTML = `
    <span>${recomendaciones.length}</span> canciones similares encontradas
  `;

  // Tarjetas con animación escalonada
  cardsGrid.innerHTML = "";
  recomendaciones.forEach((track, i) => {
    const card = buildCard(track, i + 1);
    card.style.animationDelay = `${i * 60}ms`;
    cardsGrid.appendChild(card);
  });

  // Animar barras de similitud tras render
  requestAnimationFrame(() => {
    document.querySelectorAll(".card__bar").forEach(bar => {
      const pct = parseFloat(bar.dataset.sim) * 100;
      bar.style.width = `${pct}%`;
    });
  });

  resultsSection.hidden = false;
  resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });
}

function buildCard(track, index) {
  const card = document.createElement("div");
  card.className = "card";
  card.innerHTML = `
    <span class="card__number">#${String(index).padStart(2, "0")}</span>
    <p class="card__title" title="${escHtml(track.track_name)}">${escHtml(track.track_name)}</p>
    <p class="card__artist" title="${escHtml(track.artists)}">${escHtml(track.artists)}</p>
    <div class="card__bar-wrap">
      <div class="card__bar" data-sim="${track.similitud}"></div>
    </div>
    <p class="card__sim">${(track.similitud * 100).toFixed(1)}% similitud</p>
  `;
  return card;
}

// ── Helpers ───────────────────────────────────────────────────
function setLoading(state) {
  btnSearch.disabled = state;
  btnText.hidden     = state;
  btnLoader.hidden   = !state;
}

function hideResults() { resultsSection.hidden = true; }
function hideError()   { errorBox.hidden = true; }

function showError(msg) {
  errorMsg.textContent = msg;
  errorBox.hidden      = false;
}

function escHtml(str) {
  return str.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
}