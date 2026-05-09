# Integrazioni — Strumento DC 1.2 Verifica Fonti
**Da applicare al progetto prima del deploy**

---

## 1. manifest.json — aggiungere questa voce

Aggiungere in coda all'array (prima della `]` finale):

```json
,
{
  "path": "/competenze-digitali/strumento-valutazione-fonti/",
  "label": "Verifica Fonti Online",
  "short": "Verifica Fonti",
  "cat": "strumento",
  "emoji": "🧪",
  "tags": [
    "fonti",
    "verifica",
    "craap test",
    "lateral reading",
    "reverse image search",
    "affidabilità",
    "fact checking",
    "disinformazione",
    "media literacy",
    "competenze digitali",
    "checklist"
  ],
  "meta": "Checklist guidata · Report affidabilità · Livello base",
  "description": "Strumento guidato per valutare l'affidabilità di qualsiasi fonte online. CRAAP test, lateral reading e verifica immagini in un unico flusso interattivo. Tutto client-side.",
  "featured": false,
  "active": true,
  "digcomp": ["DC 1.2", "DC 1.1"],
  "digcomp_level": "foundation",
  "digcompedu": ["DCEdu 6.1", "DCEdu 4.1"],
  "digcomp_areas": ["informazioni"]
}
```

---

## 2. index.html — card da aggiungere in #cards-strumento

Inserire dopo la card dell'Analizzatore SEO e prima della card `coming`
"Verifica delle fonti online" (che a questo punto va **rimossa o sostituita**
con questa card attiva):

```html
<!-- CARD: Verifica Fonti Online -->
<div class="card card-active card-green" data-cat="strumento" data-tags="fonti verifica craap test lateral reading reverse image search affidabilità fact checking disinformazione media literacy competenze digitali checklist">
  <div class="card-badge-strip badge-green"></div>
  <a href="competenze-digitali/strumento-valutazione-fonti/">
    <div class="card-body">
      <div class="card-icon">🧪</div>
      <div class="card-category cat-tool">Strumento</div>
      <div class="card-title">Verifica Fonti Online</div>
      <div class="card-tags">
        <span class="tag tag-green">Media Literacy</span>
        <span class="tag tag-green">CRAAP test</span>
        <span class="tag tag-green">Interattivo</span>
      </div>
      <div class="card-desc">Checklist guidata per valutare qualsiasi fonte online. CRAAP test, lateral reading e reverse image search in un unico flusso con report finale.</div>
    </div>
    <div class="card-footer">
      <div class="card-meta">Checklist guidata · Report affidabilità · Livello base</div>
      <div class="card-cta">Apri lo strumento <span class="arrow">→</span></div>
    </div>
  </a>
</div>
```

**Nota:** la card `coming` "Verifica delle fonti online" già presente in
`#cards-strumento` è il placeholder di questo strumento. Sostituirla
con la card attiva qui sopra — non aggiungere entrambe.

---

## 3. Pillola valutazione fonti — aggiornare il link placeholder

Nel file `competenze-digitali/pillola-valutazione-fonti/index.html`,
il footer ha un link disabilitato con `aria-disabled="true"`.
Sostituirlo con il link attivo:

```html
<!-- PRIMA (placeholder disabilitato) -->
<a class="footer-nav-link" href="/" aria-disabled="true" style="opacity:.5;pointer-events:none;">
  Strumento Verifica Fonti → (prossimamente)
</a>

<!-- DOPO (link attivo) -->
<a class="footer-nav-link" href="/competenze-digitali/strumento-valutazione-fonti/">
  🧪 Metti in pratica → Verifica Fonti
</a>
```

---

## 4. Dopo aver applicato le modifiche

```bash
python scripts/genera_sitemap.py
```

Verificare che la nuova URL compaia in `sitemap.xml`:
`https://formazione-digitale.it/competenze-digitali/strumento-valutazione-fonti/`

---

## 5. Struttura cartelle da creare nel repository

```
competenze-digitali/
├── pillola-valutazione-fonti/
│   └── index.html        ← già esistente
└── strumento-valutazione-fonti/
    └── index.html        ← file generato
```

---

## 6. Riepilogo connessioni tra le tre risorse

```
Pillola Wikipedia Speedrun        Pillola Valutazione Fonti       Strumento Verifica Fonti
(DC 1.1 — navigazione)      →    (DC 1.2 — valutazione)    →    (DC 1.2 — pratica guidata)
/competenze-digitali/             /competenze-digitali/           /competenze-digitali/
pillola-wikipedia-speedrun/       pillola-valutazione-fonti/      strumento-valutazione-fonti/
```

I tre link di navigazione (← / →) devono essere coerenti in tutti e tre
i file. Verificare che:
- Footer Wikipedia Speedrun → linka la pillola valutazione
- Footer pillola valutazione → linka lo strumento (aggiornamento punto 3)
- Header strumento → banner "Leggi prima la pillola" già presente
