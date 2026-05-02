// ── GOATCOUNTER STATS ────────────────────────────────────────────
// Le pagine attive vengono lette da manifest.json — non modificare
// questo file quando aggiungi una risorsa: aggiorna solo manifest.json.
//
// Aggiungi qui SOLO i path legacy (vecchi URL prima della migrazione
// pretty-link) che vuoi continuare a sommare nelle statistiche.

const gcLegacy = [
  // Home — sommate al totale, non entrano nel ranking
  { path: '/',           label: 'Home', isHome: true },
  { path: '/index.html', label: 'Home', isHome: true },

  // Vecchi path — mergeWith indica il path attivo a cui sommare le visite
  { path: '/intelligenza-artificiale/Guida_Prompting.html',                   mergeWith: '/intelligenza-artificiale/guida-prompting/' },
  { path: '/intelligenza-artificiale/prompt-builder.html',                    mergeWith: '/intelligenza-artificiale/prompt-builder/' },
  { path: '/intelligenza-artificiale/prompt-builder',                         mergeWith: '/intelligenza-artificiale/prompt-builder/' },
  { path: '/intelligenza-artificiale/Guida_PeerReview_IA.html',               mergeWith: '/intelligenza-artificiale/guida-peer-review-ia/' },
  { path: '/database/LibreOfficeBase_Query/Guida_LibreOfficeBase_Query.html', mergeWith: '/database/guida-libreoffice-base-query/' },
  { path: '/database/LibreOfficeBase_Query',                                  mergeWith: '/database/guida-libreoffice-base-query/' },
  { path: '/marketing/Guida_Marketing.html',                                  mergeWith: '/marketing/guida-marketing/' },
  { path: '/marketing/guida-marketing',                                       mergeWith: '/marketing/guida-marketing/' },
  { path: '/marketing/bep-tool.html',                                         mergeWith: '/marketing/break-even-point-tool/' },
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
      ...active.map(r => ({ path: r.path, label: r.short, isHome: false })),
      ...gcLegacy,
    ];

    // 3. Fetch parallelo su tutti i path
    const risposte = await Promise.all(
      allPaths.map(p =>
        fetch(base + p.path.replace(/^\//, '').replace(/\/$/, '') + '.json')
          .then(r => r.ok ? r.json() : { count: 0 })
          .catch(() => ({ count: 0 }))
      )
    );

    // 4. Aggrega
    //    - Home (isHome): sommate al totale, non entrano nel ranking
    //    - Legacy (mergeWith): sommate al conteggio del path attivo corrispondente
    //    - Attive: entrano nel ranking top 3
    let homeCount = 0;
    const pageMap = {}; // path → { label, count }

    // Inizializza pageMap con i path attivi
    active.forEach(r => {
      pageMap[r.path] = { label: r.short, count: 0 };
    });

    risposte.forEach((d, i) => {
      const pv   = parseInt(d.count || 0);
      const item = allPaths[i];

      if (item.isHome) {
        homeCount += pv;
        return;
      }
      if (item.mergeWith) {
        // Somma al path attivo corrispondente
        if (pageMap[item.mergeWith]) {
          pageMap[item.mergeWith].count += pv;
        } else {
          homeCount += pv; // fallback: somma al totale se il path non esiste
        }
        return;
      }
      // Path attivo
      if (pageMap[item.path]) {
        pageMap[item.path].count += pv;
      }
    });

    const pages  = Object.values(pageMap);
    const totale = pages.reduce((s, p) => s + p.count, 0) + homeCount;

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

// ── SCHEMA.ORG ITEMLIST — generato da manifest.json ─────────────
// Si aggiorna automaticamente ad ogni nuova risorsa nel manifest.
// Non modificare questo blocco: aggiorna solo manifest.json.
async function injectItemListSchema() {
  try {
    const res = await fetch('manifest.json');
    if (!res.ok) return;
    const manifest = await res.json();
    const active = manifest.filter(r => r.active);

    const schema = {
      "@context": "https://schema.org",
      "@type": "ItemList",
      "name": "Risorse di Formazione Digitale",
      "url": "https://formazione-digitale.github.io/",
      "numberOfItems": active.length,
      "itemListElement": active.map((r, i) => ({
        "@type": "ListItem",
        "position": i + 1,
        "name": r.label,
        "url": "https://formazione-digitale.github.io" + r.path,
        ...(r.description && { "description": r.description })
      }))
    };

    const el = document.createElement('script');
    el.type = 'application/ld+json';
    el.textContent = JSON.stringify(schema);
    document.head.appendChild(el);
  } catch(e) {
    // Silenzioso — schema non iniettato
  }
}

injectItemListSchema();
