// ── GOATCOUNTER STATS ────────────────────────────────────────────
// Aggiorna questo array ogni volta che aggiungi una nuova pagina.
// 'label' è il nome breve mostrato in homepage.

const gcPagine = [
  { path: '/',                                                                   label: 'Home' },
  { path: '/index.html',                                                         label: 'Home' },
  { path: '/database/LibreOfficeBase_Query/',    								 label: 'LibreOffice Base' },
  { path: '/sistemi/codifica-binaria/', 										 label: 'Bin-Digit Decoder' },
  { path: '/intelligenza-artificiale/guida-prompting/',             	         label: 'Guida Prompting' },
  { path: '/intelligenza-artificiale/prompt-builder/',                      	 label: 'Prompt Builder' },
  { path: '/intelligenza-artificiale/guida-peer-review-ia/',           	         label: 'Peer Review IA' },
  { path: '/intelligenza-artificiale/Guida_Prompting.html',                      label: 'Guida Prompting (o)' },
  { path: '/intelligenza-artificiale/prompt-builder.html',                       label: 'Prompt Builder (o)' },
  { path: '/intelligenza-artificiale/Guida_PeerReview_IA.html',                  label: 'Peer Review IA (o)' },
  { path: '/database/LibreOfficeBase_Query/Guida_LibreOfficeBase_Query.html',    label: 'LibreOffice Base (o)' },
  { path: '/marketing/guida-marketing/',                                   		 label: 'Guida Marketing' },
  { path: '/marketing/calcolo-break-even-point/',         						 label: 'BEP Tool' },
  { path: '/marketing/Guida_Marketing.html',                                     label: 'Marketing (o)' },
  { path: '/marketing/bep-tool.html',         									 label: 'BEP Tool (o)' },
  { path: '/networking/hfs-server.html', 										 label: 'Pillola HFS' },
  { path: '/networking/subnet-calculator.html', 								 label: 'Subnet Calculator' },
  { path: '/word/Guida_Word.html',                                               label: 'Guida Word' },
];

// ── Non modificare da qui in poi ────────────────────────────────
async function loadGoatStats() {
  const base = 'https://formazionedigitale.goatcounter.com/counter/';

  try {
    const risposte = await Promise.all(
      gcPagine.map(p =>
        fetch(base + encodeURIComponent(p.path) + '.json')
          .then(r => r.ok ? r.json() : { count: 0 })
          .catch(() => ({ count: 0 }))
      )
    );

    // Aggrega home (/ e /index.html) sommando i count
    const aggregated = [];
    const homePaths  = ['/', '/index.html'];
    let   homeCount  = 0;

    risposte.forEach((d, i) => {
      const pv = parseInt(d.count || 0);
      if (homePaths.includes(gcPagine[i].path)) {
        homeCount += pv;
      } else {
        aggregated.push({ label: gcPagine[i].label, count: pv });
      }
    });
    // ESCLUDO LA HOME DALLE TOP VIEWS
	// aggregated.unshift({ label: 'Home', count: homeCount });

    // Totale pageview
    const totale = aggregated.reduce((s, p) => s + p.count, 0) + homeCount;
    const elTot  = document.getElementById('gc-total');
    if (elTot) elTot.textContent = totale >= 1000
      ? (totale / 1000).toFixed(1) + 'k'
      : totale.toLocaleString('it-IT');

    // Top 3 pagine per pageview
    const top3 = [...aggregated]
       .sort((a, b) => b.count - a.count)
      .slice(0, 3);

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
