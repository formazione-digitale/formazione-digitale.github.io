---
title: "Formazione Digitale — Architettura del Progetto"
author: "Cristiano De Pasquale"
date: "Maggio 2026"
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
|--- mappa-framework.html
|--- 404.html
|--- privacy-policy.html
|--- cookie-policy.html
|--- manifest.json                   <- Catalogo risorse — unica fonte di verità
|--- site.webmanifest
|--- robots.txt
|--- sitemap.xml
|--- sw.js
|--- stats.js
|--- supabase.js
|--- auth.js
|--- .gitignore
|--- css/
|   |--- shared.css
|   \--- shared-extended.css         <- CSS proprietario per guide con layout custom
|--- img/
|--- docs/
|--- scripts/
|   |--- genera_sitemap.py
|   |--- aggiorna_dominio.py
|   |--- aggiungi_footer_index.py
|   |--- aggiungi_link_footer.py
|   |--- replace_in_files.py
|   |--- inject_after.py
|   |--- icdl_to_json.py
|   |--- png_to_webp.py
|   |--- delete_converted_png.py
|   |--- find_orphan_png.py
|   |--- zip_risorse.py
|   |--- ui.js
|   \--- struttura.bat
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
|--- database/
|   \--- guida-libreoffice-base-query/   <- Usa shared-extended.css — NON shared.css
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
\--- icdl/                               <- Pagine istituzionali — noindex, active:false
    |--- index.html
    \--- statistiche/
            index.html
```

---

# Architettura CSS

## shared.css

File CSS condiviso caricato da tutte le pagine tramite path assoluto. Versione attuale: v2 (riorganizzato 14/05/2026).

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
<link rel="stylesheet" href="/css/shared.css?v=2">
```

> **Nota:** incrementare `?v=N` ad ogni modifica significativa per invalidare la cache. Versione corrente: v2.

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

File JSON unica fonte di verità per tutte le risorse del portale.

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

Consumato da: `stats.js` (GoatCounter + Schema.org), `mappa.html` (grafo), `mappa-framework.html` (navigazione per competenza), `sitemap.xml` tramite `genera_sitemap.py`.

> **Regola:** quando aggiungi una risorsa, aggiorna **manifest.json** + **index.html** (card) + rilancia `genera_sitemap.py`.

> **Pagine istituzionali invisibili:** `/icdl/` e `/icdl/statistiche/` hanno `"active": false`. Meta robots `noindex, nofollow`. Accessibili solo via path diretto.

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

> **NOTA:** Non esiste `vercel.json` nel progetto. I redirect www→non-www sono configurati nel dashboard Vercel. HTTP→HTTPS gestito automaticamente da Vercel.

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

**URL Configuration (aggiornata 22/05/2026):**

| Campo | Valore |
|---|---|
| Site URL | `https://formazione-digitale.it` |
| Redirect URLs | `https://formazione-digitale.it/**` · `https://formazione-digitale.github.io/*` (compatibilità fino a settembre 2026) |

**SMTP (Resend):**

| Campo | Valore |
|---|---|
| Host | `smtp.resend.com` |
| Port | `465` |
| Username | `resend` |
| Sender email | `info@formazione-digitale.it` |
| Sender name | `Formazione Digitale` |
| Minimum interval | 60 secondi per utente |

## Resend (email transazionale)

| Campo | Valore |
|---|---|
| Scopo | SMTP per magic link Supabase |
| Piano | Free (3.000 email/mese) |
| Mittente | `info@formazione-digitale.it` |
| Sender name | `Formazione Digitale` |
| Dominio verificato | `formazione-digitale.it` — verificato il 22/05/2026 |
| Regione | Ireland (eu-west-1) |

**Record DNS aggiunti su Aruba (22/05/2026):**

| Tipo | Nome host | Valore | TTL | Priorità |
|---|---|---|---|---|
| TXT | `resend._domainkey` | `p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC3rIaxKDJYcfgTTnfZ8Iz9MpB4GlAJAdUs5UqvdPKAcINGbg9borhQY6ntG2w+f3576wmz2qlh/FXSgMjAm02zTHg98GJuLOET+2+iH1fXZ2oEHm/YwXsyHXpoLs5HX8pSB49RiSsJFtRlq//84wMJ0K+fh5YVmcaw6jZT6SwbqQIDAQAB` | 1 Ora | — |
| MX | `send` | `feedback-smtp.eu-west-1.amazonses.com` | 1 Ora | 10 |
| TXT | `send` | `v=spf1 include:amazonses.com ~all` | 1 Ora | — |

> **Test end-to-end superato (22/05/2026):** magic link arrivato in inbox da `Formazione Digitale <info@formazione-digitale.it>` — non in spam.

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
| Sitemap inviata | https://formazione-digitale.it/sitemap.xml |
| Stato indicizzazione | In corso — crawl completo atteso entro 2-6 settimane |

## Google Fonts

| Campo | Valore |
|---|---|
| Font usati | DM Serif Display (titoli) · DM Sans (corpo testo) |
| Caricamento | Da `shared.css` |
| Preconnect | `fonts.googleapis.com` + `fonts.gstatic.com crossorigin` in ogni pagina |
| Note | Principale causa del LCP mobile (4.8s). `font-display: swap` non ancora implementato. |

---

# GDPR e Privacy

| Documento | URL | Note |
|---|---|---|
| Privacy Policy | `/privacy-policy.html` | Copre GoatCounter, Formspree, Google Fonts, Vercel |
| Cookie Policy | `/cookie-policy.html` | Nessun cookie di profilazione — banner non necessario |

---

# Progressive Web App (PWA)

| Componente | Dettaglio |
|---|---|
| `site.webmanifest` | Nome, icone, colori, display standalone, lingua it |
| `sw.js` | Cache First per assets, Network First per HTML/JSON |
| `CACHE_VERSION` | Da incrementare ad ogni deploy significativo |
| Offline | Pagine già visitate disponibili offline. Fallback alla homepage. |

---

# SEO

| Metrica | Valore |
|---|---|
| PageSpeed SEO (desktop) | 100 / 100 |
| PageSpeed Prestazioni (desktop) | 99 / 100 |
| PageSpeed Accessibilità | 94 / 100 |
| PageSpeed Best Practice | 96 / 100 |
| PageSpeed Prestazioni (mobile) | 79 / 100 — LCP 4.8s (Google Fonts) |

**Elementi SEO implementati:**

- Title tag, meta description, canonical, robots, author in ogni pagina
- Open Graph completo + Twitter/X Card
- Schema.org WebSite con SearchAction in `index.html`
- Schema.org ItemList dinamico — generato da `stats.js` via `manifest.json`
- Schema.org LearningResource nelle sottopagine guide
- `sitemap.xml` inviata a GSC
- `lang="it"` su tutti gli HTML
- `<h1>` semantico in ogni pagina

---

# Immagini — gestione WebP

Conversione PNG → WebP completata (14/05/2026) su 3 cartelle principali:

| Cartella | Risparmio | CSV mapping |
|---|---|---|
| `elaborazione-testi/guida-word/` | -28% | — |
| `database/guida-libreoffice-base-query/` | -25% | `mapping-query.csv` |
| `networking/hfs-server/` | -39% | `mapping-hfs.csv` |

**Script di manutenzione immagini:**

| Script | Funzione |
|---|---|
| `png_to_webp.py` | Converte PNG → WebP seguendo l'ordine nell'HTML, rinomina con prefisso+progressivo, aggiorna path HTML, salva CSV mapping. Supporta `--dry-run`, `--quality`, `--prefix`, `--report`. |
| `delete_converted_png.py` | Cancella i PNG originali già convertiti leggendo i CSV di mapping. Supporta `--dry-run`. |
| `find_orphan_png.py` | Trova PNG in `img/` non referenziati nell'HTML. Supporta `--delete`. |

> **16 PNG orfani** identificati in `guida-libreoffice-base-query/img/` — da cancellare dopo verifica manuale con `find_orphan_png.py --delete`.

---

# Script di manutenzione locale

| Script | Funzione |
|---|---|
| `genera_sitemap.py` | Genera `sitemap.xml` da `manifest.json`. La data `<lastmod>` viene letta dall'ultimo commit Git del file — non usa la data odierna. Lanciare dopo ogni nuova risorsa. |
| `aggiorna_dominio.py` | Sostituisce un dominio in tutti i file HTML e XML. |
| `aggiungi_footer_index.py` | Aggiunge `<footer>` con link legali ai file della root. |
| `aggiungi_link_footer.py` | Aggiunge link Privacy/Cookie ai footer di tutte le sottocartelle. |
| `replace_in_files.py` | Trova e sostituisce una stringa in tutti gli HTML. |
| `inject_after.py` | Inietta una stringa dopo un'occorrenza in tutti gli HTML. Idempotente. |
| `icdl_to_json.py` | Anonimizza export Excel ICDL → JSON per la dashboard statistiche. Calcola certificazioni per candidato (Essentials, Base, Cyber Security, Full Standard). |
| `png_to_webp.py` | Converte PNG → WebP con rinomina progressiva e aggiornamento HTML. |
| `delete_converted_png.py` | Cancella PNG originali già convertiti in WebP. |
| `find_orphan_png.py` | Trova/cancella PNG orfani non referenziati nell'HTML. |
| `struttura.bat` | Genera `struttura.txt` con albero cartelle. |
| `zip_risorse.py` | Genera ZIP del progetto escludendo binari, immagini, `.git`. Usare per passare contesto alle IA. |

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

Analisi prodotta in maggio 2026. Implementazione pianificata luglio/agosto 2026. Documento completo: `docs/DARK_MODE_architettura.md`.

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
| **Tier 3 — Escludere** | guida-libreoffice-base-query (usa `shared-extended.css`), guida-word | `data-theme-lock="true"` — il bottone toggle non appare |

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

**Prima risorsa:** `database/guida-libreoffice-base-query/` (estratto 20/05/2026).

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
- [OK] Script `icdl_to_json.py` per anonimizzazione export Excel ICDL + calcolo certificazioni (maggio 2026)
- [OK] Audit SEO completo (13/05/2026): `<br>` in H1 (4 file), `cover-title` → `<h1>` (5 file), `404.html` meta/OG, `mappa.html` footer + H1, `strumento-valutazione-fonti` footer + H1 + `ui.js`, `mappa-framework.html` `ui.js`
- [OK] Broken links risolti — tutti i link interni ed esterni (13/05/2026)
- [OK] Hamburger mobile Subnet Calculator e HFS Server — pattern `.nav-menu-btn` + `.nav-dropdown` in `shared.css` (13/05/2026)
- [OK] `mappa.html` — footer visibile, H1 nascosto per SEO (13/05/2026)
- [OK] Pagine ICDL — `noindex, nofollow` + `active: false` in manifest (13/05/2026)
- [OK] `shared.css` v2 — riorganizzato con 17 sezioni commentate, 3 fix minori (14/05/2026)
- [OK] `fw-footer` — rimosso `position:fixed` da `shared.css`, inline solo su `mappa.html` (14/05/2026)
- [OK] `analizzatore-seo` — fix JS rotto + `ui.js` corretto (14/05/2026)
- [OK] Risorse correlate IA — label corrette + `target="_blank"` rimossi su link interni (14/05/2026)
- [OK] Footer IA — `Formazione Digitale · Torna alla home` aggiunto su guida-prompting, prompt-builder, guida-peer-review-ia (14/05/2026)
- [OK] Conversione PNG → WebP: guida-word (-28%), guida-libreoffice-base-query (-25%), hfs-server (-39%) — totale ~29% risparmio (14/05/2026)
- [OK] Script `png_to_webp.py`, `delete_converted_png.py`, `find_orphan_png.py` (14/05/2026)
- [OK] 96 PNG originali cancellati dopo conversione (14/05/2026)
- [OK] `pillola-valutazione-fonti` e `pillola-aggiornamento-digitale` — eyebrow rimosso, icona inline, meta nel badge, padding hero ridotto (14/05/2026)
- [OK] `strumento-autovalutazione-digcompedu` — H2 corretti, bug animazione report risolto, bug warning domande saltate risolto (14/05/2026)
- [OK] Dashboard ICDL — certificazioni rilasciate (3/4 card dinamiche), tabella sortable (14/05/2026)
- [OK] Dashboard ICDL standalone — versione self-contained senza dipendenza da `shared.css` (14/05/2026)
- [OK] `preconnect fonts.gstatic.com crossorigin` — aggiunto in 19 file (14/05/2026)
- [OK] Variabili colori semantici in `shared.css`: `--red-mid`, `--red-accent`, `--green-mid`, `--green-accent`, `--amber-mid` (14/05/2026)
- [OK] 14 sostituzioni colori hardcoded → variabili CSS con `replace_in_files.py` (14/05/2026)
- [OK] `cover-title` → `<h1>` in `guida-marketing` (19/05/2026)
- [OK] Pillola Netiquette — DC 2.2–2.4 · DCEdu 6.4 · INDIRE A4 (20/05/2026)
- [OK] `genera_sitemap.py` — `<lastmod>` da Git invece della data odierna (20/05/2026)
- [OK] `shared-extended.css` — CSS proprietario estratto da `guida-libreoffice-base-query`, nome generico (20/05/2026)
- [OK] Supabase URL Configuration aggiornata — Site URL e Redirect URLs migrati su formazione-digitale.it (22/05/2026)
- [OK] Resend — dominio `formazione-digitale.it` verificato, SMTP collegato a Supabase, test end-to-end superato (22/05/2026)

---

## In sospeso immediato

- Cancellare 16 PNG orfani in `guida-libreoffice-base-query/img/` dopo verifica manuale (`find_orphan_png.py --delete`)
- `index.html` riga 1578 — `formazione-digitale-logo.png` → `.webp`
- Footer standard unificato — definire template e propagare con script

---

## Miglioramenti strutturali — luglio/agosto 2026

- **Dark mode** — prerequisiti completati; implementazione rimandata a luglio/agosto (vedere `docs/DARK_MODE_architettura.md`)
- **`font-display: swap`** — da aggiungere al tag Google Fonts per migliorare LCP mobile (attuale 4.8s); fare con `replace_in_files.py`
- **Migrazione JS in `/js/`** — spostare `scripts/ui.js`, `stats.js`, `auth.js`, `supabase.js` in `/js/`; aggiornare 27+ riferimenti HTML con `replace_in_files.py` (stima 3-4 ore)
- **`icdl/statistiche/`** — valutare migrazione su WordPress scolastico (standalone già pronto)

---

## Bassa urgenza — quando disponibile

- Disabilitazione GitHub Pages (dopo settembre 2026 — branch redirect necessario fino ad allora)
- `role="heading" aria-level="1"` sui `cover-title` con `replace_in_files.py`
- Nuovi contenuti: Pillola PageSpeed · Pillola Triade CIA

---

## Prima di aprire l'auth agli utenti reali

Completare **in questo ordine**:

1. ~~Aggiornare Redirect URL Supabase → formazione-digitale.it~~ **[OK — 22/05/2026]**
2. ~~Configurare dominio verificato su Resend (email magic link in spam)~~ **[OK — 22/05/2026]**
3. Login Google OAuth
4. Aggiornare Privacy Policy con sezione autenticazione + cookie sessione
5. Aggiungere banner cookie
6. Auth in tutte le sottopagine
7. Segnalibri sulle card
8. Checklist persistenti via Supabase

---

## Nuovi contenuti — priorità DigComp/INDIRE

| Priorità | Risorsa | Standard attivati |
|---|---|---|
| [OK] | Pillola netiquette / cittadinanza digitale | DC 2.2–2.4 · DCEdu 6.4 · INDIRE A4 |
| [~] 1 | Guida/strumento collaborazione scolastica | INDIRE B1·B2 · DCEdu 1.2·2.3 |
| [?] 2 | Risorsa valutazione digitale (rubric builder) | DCEdu 4.1·4.2·4.3 · INDIRE A3 |

---

## Pannelli di controllo infrastruttura

Accessi amministrativi ai servizi del progetto, in ordine di ruolo nel sistema.

| Servizio | Ruolo | URL admin |
|---|---|---|
| **Aruba** | Registrar dominio — DNS, record MX/TXT/CNAME | https://admin.aruba.it/PannelloAdmin/UI/Pages/Index.aspx |
| **Vercel** | Hosting statico, deploy automatico, preview branch | https://vercel.com/cristianodepas-projects/formazione-digitale |
| **GitHub** | Versioning, repository sorgente, GitHub Actions | https://github.com/formazione-digitale/formazione-digitale.github.io |
| **Supabase** | Database PostgreSQL, Auth, API REST, keep-alive | https://supabase.com/dashboard/org/tyzvvkqjjnijuvxltdfm |
| **Resend** | Email transazionale SMTP per magic link | https://resend.com/domains/1b4141d0-0578-4427-8b1b-86786e78c0ea |
| **GoatCounter** | Analytics privacy-first, statistiche pageview | https://formazionedigitale.goatcounter.com/ |

---

## Settembre 2026 — badge DigComp (ordine obbligatorio)

> **ATTENZIONE:** eseguire tassativamente in questo ordine. La protezione del token Supabase è prerequisito per tutto il resto.

1. Migrazione Vercel come unico hosting (GitHub Pages dismesso)
2. Configurazione variabili d'ambiente Vercel (`SUPABASE_URL`, `SUPABASE_KEY`)
3. Creazione Serverless Function `/api/competenze.js` (proxy sicuro Supabase)
4. Creazione tabella Supabase `risorse_competenze` (`slug`, `digcomp[]`, `digcompedu[]`, `indire[]`)
5. Sviluppo `competenze.js` client — chiama `/api/` non Supabase direttamente
6. Badge competenze nelle card-footer
7. Profilo competenze utente
8. Vercel Cron Job keep-alive (sostituisce GitHub Actions)
