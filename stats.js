// ── GOATCOUNTER STATS ───────────────────────────────────────────
// Aggiorna questo array ogni volta che aggiungi una nuova pagina.
// Non toccare il resto.

const gcPagine = [
  '/',
  '/index.html',
  '/intelligenza-artificiale/Guida_Prompting.html',
  '/intelligenza-artificiale/prompt-builder.html',
  '/database/LibreOfficeBase_Query/Guida_LibreOfficeBase_Query.html',
  '/marketing/Guida_Marketing.html'
];

// ── Non modificare da qui in poi ────────────────────────────────
async function loadGoatStats() {
  const base = 'https://formazionedigitale.goatcounter.com/counter/';
  try {
    const risposte = await Promise.all(
      gcPagine.map(p =>
        fetch(base + encodeURIComponent(p) + '.json')
          .then(r => r.json())
          .catch(() => ({ count: 0, count_unique: 0 }))
      )
    );
    const totVisite   = risposte.reduce((s, d) => s + parseInt(d.count_unique || 0), 0);
    const totPageview = risposte.reduce((s, d) => s + parseInt(d.count        || 0), 0);
    const el1 = document.getElementById('gc-visits');
    if (el1) el1.textContent = totVisite.toLocaleString('it-IT');
    const el2 = document.getElementById('gc-pageviews');
    if (el2) el2.textContent = totPageview.toLocaleString('it-IT');
  } catch(e) {
    // Silenzioso — i trattini restano se qualcosa va storto
  }
}

loadGoatStats();
