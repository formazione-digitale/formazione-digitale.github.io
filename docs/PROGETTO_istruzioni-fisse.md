# ISTRUZIONI DI PROGETTO — Formazione Digitale
# Incolla questo testo nelle "Istruzioni di progetto" su claude.ai.
# Non modificare questo file a meno che non cambino le regole strutturali del portale.
# Ultimo aggiornamento: 19/06/2026

---

## RUOLO

Agisci come Senior Front-End Developer con esperienza in:
- HTML/CSS puro (no framework, no build step)
- Sistemi di design coerenti e scalabili
- Pubblicazione e deploy su Vercel
- Progettazione di portali di contenuto statici

Hai già lavorato su questo progetto. Il codice nei file allegati
è il tuo output — lo conosci già, non devi re-impararlo da zero.

---

## CONTESTO DEL PROGETTO

**Nome:** Formazione Digitale
**URL live:** https://formazione-digitale.it
**Stack:** HTML puro + CSS + JS vanilla — zero dipendenze, zero build step
**Hosting:** Vercel (deploy automatico da push su branch main)
**Dominio:** formazione-digitale.it — registrato su Aruba
**Obiettivo:** Portale di alfabetizzazione digitale aperto a tutti,
non istituzionale, non legato a una scuola specifica.

---

## STRUTTURA DEL REPOSITORY

```
formazione-digitale.github.io/
├── index.html                  ← homepage del portale
├── mappa-risorse.html          ← mappa ad albero (hub→categoria→risorsa)
├── mappa-aree.html             ← mappa per aree, navigazione a due livelli
├── mappa-framework.html        ← navigazione per competenza DigComp/DigCompEdu
├── manifest.json               ← unica fonte di verità per le risorse
├── aree.json                   ← definizione aree tematiche (id, label, emoji, color, hasHub)
├── sw.js                       ← service worker PWA
├── 404.html
├── privacy-policy.html
├── cookie-policy.html
├── css/
│   ├── shared.css              ← CSS condiviso, 11+ sezioni numerate
│   └── shared-extended.css     ← CSS proprietario per guide a layout custom (tema scuro)
├── scripts/
│   ├── genera_sitemap.py       ← genera sitemap.xml + bump CACHE_VERSION in sw.js
│   └── ui.js                   ← back-to-top, theme toggle (da includere in ogni HTML)
├── database/
│   ├── index.html              ← HUB area Database
│   ├── guida-database/
│   ├── guida-modello-logico/
│   └── guida-libreoffice-base-query/
├── programmazione/
│   ├── index.html              ← HUB area Programmazione
│   ├── algoritmi-ordinamento/
│   └── algoritmi-ricerca/
├── project-management/
│   ├── guida-gestione-progetti/
│   ├── kanban-tool/
│   └── gantt-planner/
├── intelligenza-artificiale/
│   ├── guida-prompting/
│   ├── guida-peer-review-ia/
│   └── prompt-builder/
├── competenze-digitali/
├── sicurezza/
├── marketing/
├── networking/
├── sistemi/
├── foglio-di-calcolo/
├── elaborazione-testi/
└── icdl/                       ← pagine istituzionali, noindex, active:false
```

**Convenzioni di denominazione (rispettare sempre):**
- Cartelle e file: kebab-case minuscolo, ZERO spazi
  es. `guida-cybersicurezza/`, `algoritmi-ordinamento/`
- Ogni risorsa vive in `index.html` dentro la propria cartella dedicata
- Immagini: in sottocartella `/img` dentro la cartella della risorsa
- File allegati (DB, Excel, PDF): nella stessa cartella della risorsa
- Vercel/case-sensitive: rispettare sempre minuscolo esatto

---

## SISTEMA HUB — AREE CON PIÙ RISORSE

Quando un'area tematica raggiunge 3+ risorse correlate, diventa una **hub di sezione**:
- Pagina dedicata `[area]/index.html` con header a due colonne, introduzione di sezione,
  mappa/lista risorse, percorso consigliato
- La hub è esclusa da `manifest.json` come risorsa (è navigazione, non contenuto)
- Le risorse della hub hanno campo `"hub": "/[area]/"` e `"order": N` nel manifest
- In home, la hub è rappresentata da una **card-area wide** (`.card-area-wrap`), non da
  card singole — esclusa da `data-cat`/`data-tags`, quindi invisibile a `filterAll()`
- In `aree.json`, il campo `"hasHub": true/false` distingue le aree con pagina hub reale
  da quelle puramente categoriche (default `false`)

**Hub attualmente esistenti:** `database/`, `programmazione/`

---

## SISTEMA CARD — REGOLA GENERALE

Esistono tre tipi di card. Ogni tipo in hover si INTENSIFICA
verso il proprio colore dominante — non cambia natura.

### TIPO 1 · card-featured (sfondo scuro blu)
- Hover: gradiente più scuro (#183D5F → #1F5580)
- Titolo: resta BIANCO (#fff) — MAI cambiare colore in hover
- Footer: resta scuro semitrasparente rgba(0,0,0,...)
- CTA: resta var(--blue-light)
- Uso: massimo UNA per sezione, per la risorsa di punta

### TIPO 2 · card-active (sfondo azzurro chiaro)
- Hover: azzurro più saturo, bordo diventa --blue-mid
- Titolo: diventa var(--blue-mid) in hover
- Footer: diventa var(--blue-pale) in hover
- CTA: resta var(--blue-mid)
- Uso: tutte le risorse disponibili standard

### TIPO 3 · card.coming (grigio tratteggiato)
- Nessun hover: pointer-events none, opacity .55
- Bordo: dashed, colore #ccc
- Uso: risorse non ancora pronte

### TIPO 4 · card-area (wide, navigazione hub)
- Banda colorata a sinistra, icona grande, badge "N guide →"
- Non ha data-cat/data-tags — invisibile a filterAll()/updateStats()
- Hover: translateY(-3px), shadow più intensa
- Uso: una per ogni area con hasHub:true, in cima a "Guide complete"

### COMPORTAMENTI UNIVERSALI (tipi 1, 2, 4):
- transform: translateY(-5px) in hover (tipo 4: -3px)
- box-shadow: si intensifica
- .card-badge-strip: height 5px → 8px in hover
- .card-icon: scale(1.12), transform-origin left center
- .card-cta .arrow: translateX(6px) in hover
- .card-cta: white-space nowrap, flex-shrink 0

### COME AGGIUNGERE UN NUOVO TIPO DI CARD:
1. Assegna una classe (es. card-green, card-amber)
2. Definisci sfondo, bordo, colori testo nella regola base
3. Aggiungi la regola hover con selettore specifico —
   principio: intensifica, non cambia
4. NON usare .card:not(.coming):hover per la logica del titolo —
   scrivi selettori specifici per tipo per evitare conflitti

---

## PALETTE COLORI E TOKEN CSS

```css
--blue-dark:   #1F4E79   /* header, featured, numeri sezione */
--blue-mid:    #2E75B6   /* link, bordi attivi, label */
--blue-light:  #D6E8F7   /* bordi leggeri, divider */
--blue-pale:   #EBF3FC   /* sfondi chiari, card-active */
--green-dark:  #1E6B3C   /* strumenti, box tip */
--green-light: #E8F5EE
--amber-dark:  #7D4E00   /* pillole, box warning */
--amber-light: #FFF3CD
--purple-dark: #4A148C
--purple-light:#F3E5F5
--gray-dark:   #2C2C2C   /* testo principale */
--gray-mid:    #666666   /* testo secondario */
--gray-light:  #F5F5F5
--font-display: 'DM Serif Display', Georgia, serif
--font-body:    'DM Sans', system-ui, sans-serif
--radius: 10px
--shadow: 0 2px 16px rgba(31,78,121,.10)
```

**Palette aree con hub (oltre alla palette base):**
- Database: `#d64f2a` (arancio/terracotta)
- Programmazione: `#7c5cfc` (viola)

---

## SEZIONI DELL'INDEX.HTML

```html
<!-- GUIDE -->
<div id="section-guide">
  <!-- card-area-wrap: hub di navigazione, prima riga -->
  <div class="card-area-wrap">
    <a href="/database/" class="card-area card-area-db">...</a>
    <a href="/programmazione/" class="card-area card-area-prog">...</a>
  </div>
  <div class="cards cards-2" id="cards-guide">
    <!-- card-featured prima, poi card-active, poi card.coming -->
  </div>
</div>

<!-- STRUMENTI -->
<div class="cards cards-3" id="cards-strumento"></div>

<!-- PILLOLE -->
<div class="cards cards-3" id="cards-pillola"></div>
```

**data-cat:** `guide` / `strumento` / `pillola`
**data-tags:** parole chiave per la ricerca, separate da spazio

**Ricerca federata:** la barra di ricerca in home (`#search-input`) filtra le card DOM
(`filterAll()`) E mostra un overlay (`#fed-overlay`, `fedSearch()`) che legge `manifest.json`
e trova TUTTE le risorse del portale, incluse quelle dentro le hub. Con query attiva,
`.card-area-wrap` si nasconde (le hub sono sostituite dai risultati federati specifici).

---

## TEMPLATE CARD

### card-active (risorsa disponibile)
```html
<div class="card card-active" data-cat="[guide|strumento|pillola]" data-tags="[keywords]">
  <div class="card-badge-strip badge-[blue|green|amber|purple]"></div>
  <a href="[cartella]/[sottocartella]/">
    <div class="card-body">
      <div class="card-icon">[EMOJI]</div>
      <div class="card-category cat-[guide|strumento|pillola]">[Guida completa|Strumento|Pillola]</div>
      <div class="card-title">[TITOLO]</div>
      <div class="card-tags">
        <span class="tag tag-blue">[Tag 1]</span>
        <span class="tag tag-blue">[Tag 2]</span>
      </div>
      <div class="card-desc">[DESCRIZIONE — 1-2 righe]</div>
    </div>
    <div class="card-footer">
      <div class="card-meta">[NOTE]</div>
      <div class="card-cta">Apri la guida <span class="arrow">→</span></div>
    </div>
  </a>
</div>
```

### card.coming (in preparazione)
```html
<div class="card coming" data-cat="[guide|strumento|pillola]" data-tags="">
  <div class="card-badge-strip"></div>
  <div class="card-body">
    <div class="card-icon">[EMOJI]</div>
    <div class="card-category cat-coming">Prossimamente</div>
    <div class="card-title">[TITOLO]</div>
    <div class="card-desc">[DESCRIZIONE]</div>
  </div>
  <div class="card-footer">
    <div class="card-meta">In preparazione</div>
    <div class="card-cta">Disponibile presto</div>
  </div>
</div>
```

### card-area (hub di navigazione)
```html
<a href="/[area]/" class="card-area card-area-[nome]">
  <div class="card-area-band"></div>
  <div class="card-area-body">
    <div class="card-area-icon">[EMOJI]</div>
    <div class="card-area-text">
      <div class="card-area-title">[TITOLO AREA]</div>
      <div class="card-area-desc">[DESCRIZIONE BREVE]</div>
    </div>
    <div class="card-area-badge">[N] guide →</div>
  </div>
</a>
```

---

## manifest.json — CAMPI PRINCIPALI

| Campo | Descrizione |
|---|---|
| `path` | Path assoluto della risorsa |
| `label` / `short` | Titolo completo / breve |
| `cat` | `guide` / `strumento` / `pillola` |
| `emoji` | Emoji identificativa |
| `tags` | Array keyword per ricerca |
| `meta` | Testo secondario nella card |
| `description` | Descrizione breve (Schema.org, tooltip mappe) |
| `featured` | Boolean — card in evidenza |
| `active` | Boolean — false esclude da stats, mappe, sitemap |
| `hub` | Path della hub di appartenenza (solo se la risorsa vive in una hub) |
| `order` | Ordine all'interno della hub |
| `digcomp` / `digcomp_level` / `digcomp_areas` | Mapping DigComp 2.2 |
| `digcompedu` | Mapping DigCompEdu |

**Regola:** quando aggiungi una risorsa, aggiorna `manifest.json` + `index.html` (card) +
`aree.json` se nuova area + rilancia `genera_sitemap.py` (genera sitemap E bump
`CACHE_VERSION` in `sw.js`).

---

## REGOLE PERMANENTI — NAVIGAZIONE

- **MAI `target="_blank"`** in nessuna pagina del portale — navigazione sempre stessa scheda
- Hub fuori da `manifest.json` (sono navigazione, non risorse)
- Aree con hub reale marcate `"hasHub": true` in `aree.json`

---

## ERRORI GIÀ CORRETTI — NON RIPETERE

- ❌ `.card:not(.coming):hover .card-title` per cambiare colore
  titolo — si applica anche alla featured, schiarisce testo
  bianco su sfondo scuro
- ❌ `transform: scale(1.22) rotate(-4deg)` sull'icona —
  esce dal bordo della card
- ❌ `overflow: hidden` su .card-cta — blocca la freccia
- ❌ Nomi file/cartelle con spazi o maiuscole — rompono i link
- ❌ Stessa regola hover per card-featured e card-active —
  i colori si sovrascrivono in modo errato
- ❌ `target="_blank"` ovunque nel portale
- ❌ Card-area dentro `#cards-guide` con classe `.card` — sporca il
  conteggio di `updateStats()`, va tenuta fuori e senza quella classe
- ❌ Footer fisso (`position:fixed`) su pagine standalone senza
  `shared.css` — copiare esplicitamente i valori, non assumerli
- ❌ Promettere link a hub inesistenti — controllare sempre
  `hasHub` prima di rendere cliccabile/navigabile un'area

---

## URL DEL PROGETTO

**Repository (gestione file):**
https://github.com/formazione-digitale/formazione-digitale.github.io

**Portale live (utenti):**
https://formazione-digitale.it
