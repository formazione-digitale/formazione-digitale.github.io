// ── GOATCOUNTER STATS ────────────────────────────────────────────
// Le pagine attive vengono lette da manifest.json — non modificare
// questo file quando aggiungi una risorsa: aggiorna solo manifest.json.
//
// Aggiungi qui SOLO i path legacy (vecchi URL prima della migrazione
// pretty-link) che vuoi continuare a sommare nelle statistiche.

const gcLegacy = [
  // Home
  { path: '/',           label: 'Home', isHome: true },
  { path: '/index.html', label: 'Home', isHome: true },

  // Vecchi path flat — sommate al totale, non entrano nel ranking top 3
  { path: '/intelligenza-artificiale/Guida_Prompting.html',                  label: 'Guida Prompting (o)' },
  { path: '/intelligenza-artificiale/prompt-builder.html',                   label: 'Prompt Builder (o)' },
  { path: '/intelligenza-artificiale/Guida_PeerReview_IA.html',              label: 'Peer Review IA (o)' },
  { path: '/database/LibreOfficeBase_Query/Guida_LibreOfficeBase_Query.html',label: 'LibreOffice Base (o)' },
  { path: '/marketing/Guida_Marketing.html',                                 label: 'Marketing (o)' },
  { path: '/marketing/bep-tool.html',                                        label: 'BEP Tool (o)' },
];

// ── Non modificare da qui in poi ────────────────────────────────
async function loadGoatStats() {
  const base = 'https://formazionedigitale.goatcounter.com/counter/';

  try {
    // 1. Carica manifest (pagine attive)
    const manifestRes = await fetch('manifest.json');
    const manifest    = manifestRes.ok ? await manifestRes.json() : [];
    const active      = manifest.filter(r => r.active);

    // 2. Lista completa: attive + legacy
    const allPaths = [
      ...active.map(r => ({ path: r.path, label: r.short, isHome: false, isLegacy: false })),
      ...gcLegacy.map(r => ({ ...r, isLegacy: !r.isHome })),
    ];

    // 3. Fetch parallelo su tutti i path
    const risposte = await Promise.all(
      allPaths.map(p =>
        fetch(base + encodeURIComponent(p.path.replace(/^\//, '')) + '.json')
          .then(r => r.ok ? r.json() : { count: 0 })
          .catch(() => ({ count: 0 }))
      )
    );

    // 4. Aggrega
    //    - Home (/ e /index.html): sommate, non entrano in top
    //    - Legacy (o): sommate al totale, non entrano in top
    //    - Attive: entrano nel ranking top 3
    let homeCount   = 0;
    let legacyCount = 0;
    const pageMap   = {}; // path → { label, count }

    risposte.forEach((d, i) => {
      const pv   = parseInt(d.count || 0);
      const item = allPaths[i];

      if (item.isHome) {
        homeCount += pv;
        return;
      }
      if (item.isLegacy) {
        legacyCount += pv;
        return;
      }
      if (!pageMap[item.path]) {
        pageMap[item.path] = { label: item.label, count: 0 };
      }
      pageMap[item.path].count += pv;
    });

    const pages  = Object.values(pageMap);
    const totale = pages.reduce((s, p) => s + p.count, 0) + homeCount + legacyCount;

    // 5. Aggiorna DOM — totale pageview
    const elTot = document.getElementById('gc-total');
    if (elTot) elTot.textContent = totale >= 1000
      ? (totale / 1000).toFixed(1) + 'k'
      : totale.toLocaleString('it-IT');

    // 6. Top 3 pagine per pageview
    const top3  = [...pages].sort((a, b) => b.count - a.count).slice(0, 3);
    const elTop = document.getElementById('gc-top');
    if (elTop) {
      elTop.innerHTML = top3.map(p => `
        <div class="gc-top-item">
          <span class="gc-top-label">${p.label}</span>
          <span class="gc-top-count">${p.count.toLocaleString('it-IT')}</span>
        </div>
      `).join('');
    }

  } catch(e) {
    // Silenzioso — i trattini restano
  }
}

loadGoatStats();
