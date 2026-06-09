---
title: "Formazione Digitale — Architettura del Progetto"
author: "Cristiano De Pasquale"
date: "Giugno 2026"
geometry: "margin=2.5cm"
fontsize: 11pt
toc: true
toc-depth: 3
numbersections: true
colorlinks: true
linkcolor: "blue"
---

\newpage

# Panoramica del progetto

**Formazione Digitale** è un portale statico di alfabetizzazione digitale che eroga guide pratiche, strumenti interattivi e pillole di contenuto. Le risorse sono libere, gratuite e senza prerequisiti. Il portale è usato come riferimento didattico per studenti e docenti — portale di riferimento scolastico istituzionale (IIS Einaudi Chiari, BS).

| Campo | Valore |
|---|---|
| URL live | https://formazione-digitale.it |
| Repository | github.com/formazione-digitale/formazione-digitale.github.io |
| Visibilità repo | Pubblica |
| Deploy | Vercel Edge Network — pubblicazione automatica da branch main |
| Dominio | formazione-digitale.it — registrato su Aruba, maggio 2026 |
| Stack | HTML puro + CSS + JS vanilla — zero framework, zero build step |
| Autore | Cristiano De Pasquale — Docente di Informatica, IIS Einaudi Chiari (BS) |
| Licenza | Uso libero e non commerciale |

---

# Struttura del repository

La root contiene i file di configurazione e i JS condivisi. Ogni risorsa vive nella propria cartella autonoma.

```
formazione-digitale/
|--- index.html
|--- mappa.html
|--- mappa-aree.html
|--- mappa-framework.html
|--- 404.html
|--- privacy-policy.html
|--- cookie-policy.html
|--- manifest.json                   <- Catalogo risorse — unica fonte di verità
|--- aree.json
|--- framework.json
|--- site.webmanifest
|--- robots.txt
|--- sitemap.xml
|--- sw.js
|--- stats.js
|--- supabase.js
|--- auth.js
|--- .gitignore
|--- css/
|   |--- shared.css                  <- Layout standard (v3)
|   \--- shared-extended.css         <- CSS proprietario per guide con layout custom
|--- img/
|--- docs/
|--- scripts/
|   |--- aggiorna_dominio.py
|   |--- catalogo_scripts.md
|   |--- cerca_vecchio_dominio.ps1
|   |--- cerca_vecchio_dominio.py
|   |--- check_site_links.bat
|   |--- delete_converted_png.py
|   |--- estrai_footer.bat
|   |--- estrai_footer.ps1
|   |--- find_orphan_png.py
|   |--- genera_sitemap.py
|   |--- httpserver.bat
|   |--- icdl_to_json.py
|   |--- inject_after.py
|   |--- normalizza_footer.bat
|   |--- normalizza_footer.ps1
|   |--- png_to_webp.py
|   |--- replace_in_files.py
|   |--- struttura.bat
|   |--- trova_anomali.bat
|   |--- trova_anomali.ps1
|   |--- trova_maxwidth.bat
|   |--- trova_maxwidth.ps1
|   |--- trova_override_layout.bat
|   |--- trova_override_layout.ps1
|   |--- ui.js
|   \--- zip_risorse.py
|--- .github/
|   \--- workflows/
|       \--- supabase-keep-alive.yml
|--- sicurezza/
|   |--- pillola-cybersicurezza/
|   \--- guida-cybersicurezza/
|--- competenze-digitali/
|   |--- pillola-wikipedia-speedrun/
|   |--- pillola-valutazione-fonti/
|   |--- pillola-aggiornamento-digitale/
|   |--- pillola-netiquette/
|   |--- strumento-valutazione-fonti/
|   \--- strumento-autovalutazione-digcompedu/
|--- intelligenza-artificiale/
|   |--- guida-prompting/
|   |--- guida-peer-review-ia/
|   \--- prompt-builder/
|--- elaborazione-testi/
|   \--- guida-word/
|--- foglio-di-calcolo/
|   \--- guida-funzioni-excel/
|--- database/
|   |--- guida-database/             <- Usa shared-extended.css — NON shared.css
|   |--- guida-libreoffice-base-query/  <- Usa shared-extended.css — NON shared.css
|   \--- guida-modello-logico/       <- Usa shared-extended.css — NON shared.css
|--- marketing/
|   |--- guida-marketing/
|   |--- pillola-seo/
|   |--- analizzatore-seo/
|   \--- break-even-point-tool/
|--- networking/
|   |--- subnet-calculator/
|   \--- hfs-server/
|--- sistemi/
|   \--- codifica-binaria/
\--- icdl/                           <- Pagine istituzionali — noindex, active:false
    |--- index.html
    \--- statistiche/
            index.html
```

---

# Architettura CSS

## shared.css

File CSS condiviso caricato da tutte le pagine tramite path assoluto. Versione attuale: **v3** (aggiornato 08/06/2026).

Contiene 17 sezioni numerate e commentate:

1. Reset universale
2. Variabili `:root` — palette colori, font, token di layout
3. Base (`html`, `body`)
4. Header homepage (`#header`, `#hamburger`, nav links, pill buttons)
5. Header guide (`.guide-header`, `.hamburger`, `.header-downloads`, `.mode-toggle`)
6. Header nav custom (`.nav-menu-btn`, `.nav-dropdown`) — subnet-calculator, hfs-server
7. Sidebar homepage (`#sidebar`, `#overlay`, `.nav-item`, `.nav-num`)
8. Sidebar guide (`.guide-layout`, `.guide-sidebar`, `.sidebar-overlay`, `.sidebar-nav`)
9. Main content (`#main`, `p`, `hr`, liste)
10. Struttura sezioni (`.section-header`, `.cover-block`, `.cover-extras`)
11. Componenti guide (`.part-header`, `.highlight-grid`, `.dodont`, `.two-col`)
12. Box callout (`.box-tip`, `.box-warn`, `.box-note`, `.box-info`, `.box-red`)
13. Footer (`footer`, `.fw-footer`, `.footer-nav-link`)
14. Auth UI (`#auth-btn`, `.auth-overlay`, `.auth-panel`, `.btn-bookmark`)
15. About modal (`.about-trigger`, `.about-overlay`)
16. Lettura & utilità (`#reading-bar`, `.nav-part-label`)
17. [Placeholder] Dark mode

```html
<link rel="stylesheet" href="/css/shared.css?v=3">
```

> **Nota:** incrementare `?v=N` ad ogni modifica significativa per invalidare la cache. Versione corrente: v3.

### Layout guide standard (aggiornato 08/06/2026)

La sezione 8 usa ora un layout **block** con sidebar fixed, allineato al pattern `#sidebar`/`#main` della homepage:

- `.guide-layout` → `display: block` (non più grid)
- `.guide-sidebar` → `position: fixed; top: 56px; left: 0; bottom: 0` — arriva sempre al footer
- `.guide-main` → `margin-left: var(--nav-w); max-width: 1060px`
- `#main` → `max-width: 1060px` (allineato a `.guide-main`)

### Palette colori (`:root`)

| Famiglia | Variabili |
|---|---|
| Blu | `--blue-dark` #1F4E79 · `--blue-mid` #2E75B6 · `--blue-light` #D6E8F7 · `--blue-pale` #EBF3FC |
| Verde | `--green-dark` #1E6B3C · `--green-mid` #4CAF50 · `--green-light` #E8F5EE · `--green-accent` #2ecc71 |
| Amber | `--amber-dark` #7D4E00 · `--amber-mid` #f39c12 · `--amber-light` #FFF3CD |
| Rosso | `--red-dark` #8B1A1A · `--red-mid` #C0392B · `--red-accent` #e74c3c · `--red-light` #FDECEA |
| Viola | `--purple-dark` #4A148C · `--purple-light` #F3E5F5 |
| Grigio | `--gray-dark` #2C2C2C · `--gray-mid` #666 · `--gray-light` #F5F5F5 · `--white` #FFFFFF |

> **Regola:** usare sempre le variabili — mai hardcodare i colori nelle pagine.

## shared-extended.css

CSS per guide con layout proprietario, completamente scollegato da `shared.css`. Non è un'estensione di shared — è un sistema autonomo con palette, reset e componenti propri. Va caricato **al posto** di `shared.css`, non dopo.

```html
<link rel="stylesheet" href="/css/shared-extended.css?v=1">
```

Prima risorsa che lo usa: `database/guida-libreoffice-base-query/` (20/05/2026).

Il nome è volutamente generico — non è legato a LibreOffice. Qualsiasi guida con layout molto custom (es. simulatori UI, guide tecniche con palette propria) può usarlo come base.

**Pagine che usano shared-extended.css (Tier 3 dark mode):**
- `database/guida-libreoffice-base-query/` — prima risorsa, mock UI LibreOffice
- `database/guida-modello-logico/` — aggiunta maggio 2026
- `database/guida-database/` — refactored 08/06/2026

> **Regola:** NON caricare `shared.css` nelle pagine che usano `shared-extended.css` — i due sistemi non sono compatibili (reset `body`, `h2`, `h3` e `.section-num` in conflitto).

## Pattern header-downloads

Per pagine con file allegati scaricabili. Su desktop: inline nell'header. Su mobile (<600px): barra fissa sotto l'header, scrollabile orizzontalmente. Usare `body.aula-mode` per nasconderla in modalità presentazione.

## Pattern nav-dropdown

Per pagine con nav custom (subnet-calculator, hfs-server). Hamburger a tendina mobile: `.nav-menu-btn` + `.nav-dropdown`. JS inline nella pagina: `toggleNavMenu()`, `closeNavMenu()`.

## CSS specifico per pagina

Ogni pagina mantiene un `<style>` inline per componenti non condivisi.

---

# JavaScript — file e responsabilità

| File | Responsabilità |
|---|---|
| `sw.js` | Service Worker PWA. Cache First per CSS/img, Network First per HTML/JSON. `CACHE_VERSION` da incrementare ad ogni deploy significativo. |
| `stats.js` | Carica statistiche da GoatCounter API. Inietta Schema.org ItemList dinamico da `manifest.json`. Non modificare per aggiungere risorse — aggiornare solo `manifest.json`. |
| `supabase.js` | Client Supabase condiviso. Esporta `supabase` per import ES module. **ATTENZIONE:** contiene anon key — pianificata migrazione a variabile d'ambiente Vercel (settembre 2026). |
| `auth.js` | Gestisce login magic link, logout, stato sessione, segnalibri. Importa `supabase.js`. |
| `scripts/ui.js` | Inietta back-to-top button e gestisce theme toggle in tutte le pagine. Includere con `<script src="/scripts/ui.js" defer></script>` prima di `</body>` in ogni pagina HTML. Migrazione in `/js/` pianificata luglio/agosto 2026. |

> **Regola ui.js:** ogni file HTML del portale deve includere `<script src="/scripts/ui.js" defer></script>`. Verifica pagine mancanti (PowerShell dalla root): `ls -r *.html | ?{ !(sls "ui.js" $_.FullName -Quiet) } | % FullName`

---

# manifest.json — catalogo risorse

File JSON unica fonte di verità per tutte le risorse del portale. Include anche i mapping DigComp e DigCompEdu (manifest_digcomp.json eliminato — merge completato maggio 2026).

| Campo | Descrizione |
|---|---|
| `path` | Path assoluto della risorsa |
| `label` | Titolo completo |
| `short` | Titolo breve per statistiche e mappa |
| `cat` | Categoria: `guide` / `strumento` / `pillola` |
| `emoji` | Emoji identificativa |
| `tags` | Array di keyword per la ricerca interna |
| `meta` | Testo secondario nella card |
| `description` | Descrizione breve usata da Schema.org ItemList |
| `featured` | Boolean — card in evidenza (max 1 per sezione) |
| `active` | Boolean — `false` esclude la risorsa da stats, mappa e schema |
| `digcomp` | Array competenze DigComp (es. `["DC 4.1", "DC 4.2"]`) |
| `digcomp_level` | Livello DigComp: `foundation` / `intermediate` / `advanced` |
| `digcompedu` | Array competenze DigCompEdu (es. `["DCEdu 6.4"]`) |
| `digcomp_areas` | Array aree tematiche DigComp |

Consumato da: `stats.js` (GoatCounter + Schema.org), `mappa.html` (grafo), `mappa-aree.html` (grafo D3 per aree), `mappa-framework.html` (navigazione per competenza), `sitemap.xml` tramite `genera_sitemap.py`.

> **Regola:** quando aggiungi una risorsa, aggiorna **manifest.json** + **index.html** (card) + rilancia `genera_sitemap.py`.

> **Pagine istituzionali invisibili:** `/icdl/` e `/icdl/statistiche/` hanno `"active": false`. Meta robots `noindex, nofollow`. Accessibili solo via path diretto.

---

# Script di manutenzione

Documentazione completa in `scripts/catalogo_scripts.md`. Riepilogo principale:

| Script | Tipo | Funzione |
|---|---|---|
| `genera_sitemap.py` | Python | Genera `sitemap.xml` da `manifest.json`. Usa date Git per `<lastmod>`. |
| `cerca_vecchio_dominio.py/.ps1` | Python/PS | Cerca occorrenze del vecchio dominio github.io. |
| `aggiorna_dominio.py` | Python | Sostituisce github.io → formazione-digitale.it in tutti i file. |
| `replace_in_files.py` | Python | Trova e sostituisce una stringa in tutti gli HTML. |
| `inject_after.py` | Python | Inietta una stringa dopo un pattern in tutti gli HTML. Idempotente. |
| `icdl_to_json.py` | Python | Anonimizza export Excel ICDL → `data.json`. |
| `png_to_webp.py` | Python | Converte PNG → WebP con rinomina progressiva e aggiornamento HTML. |
| `delete_converted_png.py` | Python | Cancella PNG originali già convertiti in WebP. |
| `find_orphan_png.py` | Python | Trova/cancella PNG orfani non referenziati. |
| `zip_risorse.py` | Python | Genera ZIP del progetto per passare contesto alle IA. |
| `normalizza_footer.ps1` | PowerShell | Sostituisce i footer con il template canonico. |
| `estrai_footer.ps1` | PowerShell | Estrae il `<footer>` da tutti gli HTML. Utility diagnosi. |
| `trova_anomali.ps1` | PowerShell | Trova file anomali nel repo. |
| `trova_override_layout.ps1` | PowerShell | Trova pagine con override CSS inline su classi di layout. |
| `trova_maxwidth.ps1` | PowerShell | Trova valori `max-width` nei blocchi `<style>` inline. |
| `struttura.bat` | Batch | Genera `struttura.txt` con albero cartelle. |
| `httpserver.bat` | Batch | Avvia server HTTP locale per test (Python http.server). |
| `check_site_links.bat` | Batch | Verifica link del sito in locale. |
| `ui.js` | JavaScript | Logica UI condivisa. Caricato da tutte le pagine. |

---

# Responsive Mobile

## Workflow branch e preview Vercel

1. Creare branch dedicato in GitHub Desktop
2. Pubblicare il branch — Vercel genera automaticamente un preview URL
3. Testare il preview URL da mobile prima del merge
4. Merge su main → deploy automatico su formazione-digitale.it

## Bug mobile risolti

| Bug | Data | Stato |
|---|---|---|
| Guida Marketing — bottoni download non funzionanti su mobile | 11/05/2026 | RISOLTO — pattern `.header-downloads` |
| Guida Marketing — mode-toggle visibile su mobile (inutile) | 11/05/2026 | RISOLTO — nascosto via media query |
| LibreOffice Base Query — navbar sparisce + manca back-to-top | 11/05/2026 | RISOLTO |
| Subnet Calculator — hamburger mancante | 13/05/2026 | RISOLTO — pattern `.nav-menu-btn` + `.nav-dropdown` |
| HFS Server — nessun menu di navigazione mobile | 13/05/2026 | RISOLTO — pattern `.nav-menu-btn` + `.nav-dropdown` |

---

# Dark Mode — Analisi Architetturale

Implementazione pianificata luglio/agosto 2026. Documento completo: `docs/DARK_MODE_architettura.md`.

## Valutazione

Il dark mode è raccomandato. Il costo reale non è tecnico — è di manutenzione CSS: ogni nuovo componente deve prevedere la variante dark. Tutto centralizzato in `shared.css`, nessuna modifica ai singoli file delle guide.

## Prerequisiti — completati (14/05/2026)

- Variabili semantici aggiunte in `shared.css`: `--red-mid`, `--red-accent`, `--green-mid`, `--green-accent`, `--amber-mid`
- 14 colori hardcoded sostituiti con variabili via `replace_in_files.py`

## Classificazione pagine (Tier)

| Tier | Pagine | Strategia |
|---|---|---|
| **Tier 1 — Risposta automatica** | index.html, mappa.html, guide IA, Subnet, BEP | Variabili dark in `shared.css` |
| **Tier 2 — Intervento mirato** | guida-marketing, hfs-server, codifica-binaria | Revisione colori hardcoded inline |
| **Tier 3 — Escludere** | guida-libreoffice-base-query, guida-modello-logico, guida-database (usano `shared-extended.css`) · guida-word (tema Microsoft) | `data-theme-lock="true"` — il bottone toggle non appare |

## Pattern scelto

`prefers-color-scheme` (sistema) + attributo manuale `data-theme` su `<html>` + `localStorage`.

## Stima lavoro

| Attività | Tempo stimato |
|---|---|
| Variabili dark in `shared.css` + override componenti | 1–2 ore |
| `ui.js` + bottone header index e mappa | 30 min |
| Anti-flash in tutte le pagine (`replace_in_files.py`) | 15 min |
| Test Tier 1 | 1–2 ore |
| Revisione Tier 2 | 2–4 ore |
| Decisione e lock Tier 3 | 30 min |

---

# Architettura CSS estesa — shared-extended.css

CSS per guide con layout proprietario completamente diverso da `shared.css`. Il file è **autonomo** — non va caricato insieme a `shared.css` perché i due sistemi hanno conflitti su `body`, `h2`, `h3`, `.section-num`.

```html
<!-- Solo questo — NON aggiungere shared.css -->
<link rel="stylesheet" href="/css/shared-extended.css?v=1">
```

`shared-extended.css` definisce una palette propria (toni scuri e caldi: `--ink`, `--bg`, `--accent`, `--lo-blue` ecc.) e componenti specifici per guide tecniche (mock UI, tab, schema DB, callout, step list, field pill).

Il nome è generico per design — può essere usato da qualsiasi guida con identità visiva custom, non solo LibreOffice.

**Pagine che lo usano:** `guida-libreoffice-base-query`, `guida-modello-logico`, `guida-database`.

---

# App Desktop — Neutralino

## BEP Tool (Calcolatore Break-Even Point)

Versione desktop standalone del tool web `marketing/break-even-point-tool/`. Distribuita come installer Windows tramite Inno Setup.

Ogni modifica funzionale va replicata manualmente su entrambe le versioni.

**Differenze versione desktop vs web:**

| Elemento | Web | Desktop |
|---|---|---|
| Chart.js | CDN | Locale (`chart.umd.js`) |
| Google Fonts | Sì | No — font di sistema |
| GoatCounter | Sì | No |
| Meta SEO/OG/Schema.org | Sì | No |
| Bottone Excel | Sì | No |
| Footer web | Sì | No |
| Barra scenari | No | Sì |
| Salvataggio JSON | No | Sì (autosave + esplicito) |
| Titolo finestra dinamico | No | Sì |
| `ui.js` | Sì | No |

### Percorso progetto desktop

```
MATERIALE_DIDATTICO\NEUTRALINO\bep-tool\
|-- neutralino.config.json
|-- bep_tool_setup.iss
|-- resources\
|   |-- index.html
|   |-- bep.css
|   |-- bep.js
|   |-- chart.umd.js
|   |-- neutralino.js
|   |-- neutralino.d.ts
|   |-- icons\
|   |   |-- icona.png
|   |   \-- icona.ico
|   \-- default-data\
|       \-- scenari_default.json
|-- bin\          <- binari Neutralino v6.7.0
\-- dist\         <- output neu build + installer
```

---

# Roadmap

## Completato

- [OK] Migrazione Vercel (maggio 2026)
- [OK] Dominio formazione-digitale.it registrato su Aruba
- [OK] GSC cambio indirizzo completato (09/05/2026): github.io → formazione-digitale.it
- [OK] Sessione responsive mobile (08/05/2026)
- [OK] Pillola Valutazione Fonti + Strumento Verifica Fonti (maggio 2026)
- [OK] Unificazione manifest.json — eliminato manifest_digcomp.json (maggio 2026)
- [OK] Pattern `.header-downloads` per file allegati (11/05/2026)
- [OK] `.gitignore` creato (11/05/2026)
- [OK] `zip_risorse.py` — tool contesto per IA (11/05/2026)
- [OK] Redirect www→non-www configurato su Vercel dashboard (11/05/2026)
- [OK] Guida ICDL + Dashboard statistiche ICDL — aggiunte al portale (maggio 2026)
- [OK] GitHub Pages disabilitato (25/05/2026) — formazione-digitale.github.io → 404
- [OK] GSC indicizzazione migliorata significativamente dopo disabilitazione GitHub Pages
- [OK] Tutti i broken links risolti (14/05/2026)
- [OK] Footer canonico normalizzato su tutte le pagine (08/06/2026)
- [OK] Layout guide standard allineato al pattern marketing: sidebar fixed, max-width 1060px (08/06/2026)
- [OK] guida-database refactored al layout scuro shared-extended.css (08/06/2026)
- [OK] BEP tool desktop — dati salvati in `Documenti\BEP Tool\` via `Neutralino.os.getPath('documents')` (22/05/2026)
- [OK] BEP tool desktop — installer `BEP_Tool_Setup.exe` generato con Inno Setup (22/05/2026)
- [OK] Supabase Auth + magic link + Resend SMTP configurati (22/05/2026)

---

## In sospeso immediato

- Cancellare PNG orfani in `guida-libreoffice-base-query/img/` dopo verifica manuale (`find_orphan_png.py --delete`)
- `index.html` — verificare se `formazione-digitale-logo.png` è ancora presente o già convertito in WebP
- `genera_sitemap.py` — aggiungere `mappa-aree.html` alle pagine fisse
- BEP tool web — aggiungere bottone Manuale (modale) e bottone download app desktop nell'hero

---

## Miglioramenti strutturali — luglio/agosto 2026

- **Dark mode** — prerequisiti completati; implementazione rimandata a luglio/agosto (vedere `docs/DARK_MODE_architettura.md`)
- **`font-display: swap`** — da aggiungere al tag Google Fonts per migliorare LCP mobile; fare con `replace_in_files.py`
- **Migrazione JS in `/js/`** — spostare `scripts/ui.js`, `stats.js`, `auth.js`, `supabase.js` in `/js/`; aggiornare riferimenti HTML con `replace_in_files.py`
- **TOC normalizzazione** — portare TOC in `shared-extended.css` e migrare JS

---

## Settembre 2026 — badge DigComp e Supabase

> **ATTENZIONE:** eseguire tassativamente in questo ordine. La protezione del token Supabase è prerequisito per tutto il resto.

1. Migrazione Vercel come unico hosting
2. Configurazione variabili d'ambiente Vercel (`SUPABASE_URL`, `SUPABASE_KEY`)
3. Creazione Serverless Function `/api/competenze.js` (proxy sicuro Supabase)
4. Creazione tabella Supabase `risorse_competenze` (`slug`, `digcomp[]`, `digcompedu[]`, `indire[]`) — applicare pattern GRANT da `NOTA_Supabase_default_grants.md`
5. Sviluppo `competenze.js` client — chiama `/api/` non Supabase direttamente
6. Badge competenze nelle card-footer
7. Login Google OAuth
8. Aggiornare Privacy Policy con sezione autenticazione
9. Aggiungere banner cookie (Cookiebot — valutare se necessario con auth)
10. Vercel Cron Job keep-alive (sostituisce GitHub Actions)

---

## Nuovi contenuti — priorità DigComp/INDIRE

| Priorità | Risorsa | Standard attivati |
|---|---|---|
| [OK] | Pillola netiquette / cittadinanza digitale | DC 2.2–2.4 · DCEdu 6.4 · INDIRE A4 |
| 1 | Strumento/guida collaborazione scolastica | INDIRE B1·B2 · DCEdu 1.2·2.3 |
| 2 | Rubric builder (valutazione digitale) | DCEdu 4.1·4.2·4.3 · INDIRE A3 |

---

## Desktop suite (estate 2026)

- Monolithic Neutralinojs app: BEP calculator + Kanban + Gantt planner
- iframe-based routing; CSS separato per tool; dati in `Documenti\Formazione Digitale\[tool]\`
- Packaged con Inno Setup; caveat antivirus (unsigned) documentato

---

## Bassa urgenza — quando disponibile

- `role="heading" aria-level="1"` sui `cover-title` con `replace_in_files.py`
- Nuovi contenuti: Pillola PageSpeed · Pillola Triade CIA

---

# Integrazioni esterne

## Vercel (hosting principale)

| Campo | Valore |
|---|---|
| Scopo | Hosting statico + Serverless Functions + Preview Deployments |
| Piano | Hobby (gratuito) |
| URL produzione | https://formazione-digitale.it |
| Deploy | Automatico da push su branch main GitHub |
| Preview | Ogni branch genera URL preview univoco |
| Configurazione domini | formazione-digitale.it → Production · www → 301 redirect a non-www |

## Aruba (registrar dominio)

| Campo | Valore |
|---|---|
| Dominio | formazione-digitale.it |
| Registrato | Maggio 2026 |
| Scadenza | Maggio 2027 |
| Rinnovo automatico | Attivo |
| Email attiva | info@formazione-digitale.it |
| DNS | Record A: `@` → 216.198.79.1 · CNAME: `www` → Vercel |

## Supabase

| Campo | Valore |
|---|---|
| Scopo | Database PostgreSQL + Auth + API REST |
| Piano | Free (pausa dopo 7gg inattività) |
| Auth attiva | Magic link (OTP via email) |
| Auth in arrivo | OAuth Google |
| Tabelle | `profiles` · `bookmarks` |
| RLS | Attiva — ogni utente vede solo i propri dati |
| Keep-alive | GitHub Actions (`supabase-keep-alive.yml`) — ogni giorno alle 08:00 UTC |
| **Sicurezza** | **ATTENZIONE:** anon key in `supabase.js` (file pubblico). Migrazione a Vercel env variables — settembre 2026. |

**URL Configuration:**

| Campo | Valore |
|---|---|
| Site URL | `https://formazione-digitale.it` |
| Redirect URLs | `https://formazione-digitale.it/**` · `https://formazione-digitale.github.io/*` (compatibilità fino a settembre 2026) |

## Resend (email transazionale)

| Campo | Valore |
|---|---|
| Scopo | SMTP per magic link Supabase |
| Piano | Free (3.000 email/mese) |
| Mittente | `info@formazione-digitale.it` |
| Dominio verificato | `formazione-digitale.it` — verificato il 22/05/2026 |
| Regione | Ireland (eu-west-1) |

## GoatCounter (analytics)

| Campo | Valore |
|---|---|
| Scopo | Analytics privacy-friendly, senza cookie, GDPR compliant |
| Account | formazionedigitale.goatcounter.com |
| Integrazione | Script asincrono in `<head>` di ogni pagina |
| API | Usata da `stats.js` per pageview e top 3 pagine |

## Google Search Console

| Campo | Valore |
|---|---|
| Proprietà attiva | formazione-digitale.it |
| Cambio indirizzo | Completato il 09/05/2026: github.io → formazione-digitale.it |
| GitHub Pages disabilitato | 25/05/2026 — risolto problema canonical duplicato |
| Sitemap inviata | https://formazione-digitale.it/sitemap.xml |
| Stato indicizzazione | Migliorato significativamente dopo disabilitazione GitHub Pages |

## Google Fonts

| Campo | Valore |
|---|---|
| Font usati in shared.css | DM Serif Display (titoli) · DM Sans (corpo testo) |
| Font usati in shared-extended.css | Sora (testo) · Space Mono (codice/monospace) |
| Caricamento | Da `<link>` in `<head>` di ogni pagina |
| Preconnect | `fonts.googleapis.com` + `fonts.gstatic.com crossorigin` |
| Note | `font-display: swap` non ancora implementato — migrazione luglio/agosto 2026 |

---

## Pannelli di controllo infrastruttura

| Servizio | Ruolo | URL admin |
|---|---|---|
| **Aruba** | Registrar dominio — DNS, record MX/TXT/CNAME | https://admin.aruba.it/PannelloAdmin/UI/Pages/Index.aspx |
| **Vercel** | Hosting statico, deploy automatico, preview branch | https://vercel.com/cristianodepas-projects/formazione-digitale |
| **GitHub** | Versioning, repository sorgente, GitHub Actions | https://github.com/formazione-digitale/formazione-digitale.github.io |
| **Supabase** | Database PostgreSQL, Auth, API REST, keep-alive | https://supabase.com/dashboard/org/tyzvvkqjjnijuvxltdfm |
| **Resend** | Email transazionale SMTP per magic link | https://resend.com/domains/1b4141d0-0578-4427-8b1b-86786e78c0ea |
| **GoatCounter** | Analytics privacy-first, statistiche pageview | https://formazionedigitale.goatcounter.com/ |

---

*Documento aggiornato 09/06/2026 · Formazione Digitale*
