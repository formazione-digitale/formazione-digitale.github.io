# Catalogo script — `scripts/`
**Formazione Digitale · aggiornato 09/06/2026**

---

## Python

### `aggiorna_dominio.py`
Sostituisce `formazione-digitale.github.io` → `formazione-digitale.it` in tutti gli HTML/XML.
> 🟡 Usa unica — già eseguito, conservare per emergenze

### `cerca_vecchio_dominio.py`
Cerca occorrenze di `formazione-digitale.github.io` in tutti i file del repo (HTML, XML, JS, CSS, JSON, MD, TXT, PY). Mostra file e numero di riga.
> 🟡 Utility diagnosi — usare prima di `aggiorna_dominio.py` per verificare

### `delete_converted_png.py`
Cancella i PNG originali già convertiti in WebP, leggendo i CSV di mapping generati da `png_to_webp.py`.
> ✅ Attivo — usare dopo aver verificato `png_to_webp.py`

### `find_orphan_png.py`
Trova e opzionalmente cancella PNG orfani non referenziati nell'HTML.
> ✅ Attivo — task in coda (eseguire dopo backup ZIP)

### `genera_sitemap.py`
Genera `sitemap.xml` leggendo le risorse attive da `manifest.json`. Usa date Git per `<lastmod>`.
> ✅ Attivo — lanciare dopo ogni nuova risorsa

### `icdl_to_json.py`
Anonimizza gli export Excel ICDL → `data.json` per la dashboard statistiche. Calcola certificazioni per candidato (Essentials, Base, Cyber Security, Full Standard).
> ✅ Attivo — usare ad ogni export ICDL

### `inject_after.py`
Inietta una stringa subito dopo ogni occorrenza di un pattern in tutti gli HTML. Idempotente.
> ✅ Utility generica — tenere

### `png_to_webp.py`
Converte PNG → WebP con rinomina progressiva e aggiornamento automatico dei path nell'HTML.
> ✅ Attivo — usare per nuove guide con immagini PNG

### `replace_in_files.py`
Trova e sostituisce una stringa in tutti gli HTML.
> ✅ Utility generica — tenere

### `zip_risorse.py`
Genera ZIP del progetto escludendo binari, immagini e `.git`. Utile per passare contesto alle IA.
> 🟡 Utility occasionale — tenere

---

## PowerShell

### `cerca_vecchio_dominio.ps1`
Versione PowerShell di `cerca_vecchio_dominio.py`. Cerca occorrenze del vecchio dominio in tutti i file del repo.
> 🟡 Utility diagnosi — alternativa PowerShell per utenti Windows

### `estrai_footer.ps1` + `estrai_footer.bat`
Estrae il blocco `<footer>` da tutti gli HTML. Output: `footer_report.txt` in `scripts/`.
> ✅ Attivo — utility diagnosi

### `normalizza_footer.ps1` + `normalizza_footer.bat`
Sostituisce i footer con il template canonico. Crea `.bak` prima di ogni modifica.
> ✅ Attivo — usare quando si aggiungono nuove pagine

### `trova_anomali.ps1` + `trova_anomali.bat`
Trova file anomali nel repo: backup, trattino spurio, duplicati numerici, archivi, spazi nel nome.
> ✅ Attivo — lanciare periodicamente

### `trova_maxwidth.ps1` + `trova_maxwidth.bat`
Trova tutti i valori `max-width` nei blocchi `<style>` inline delle pagine.
> ✅ Attivo — utility diagnosi layout

### `trova_override_layout.ps1` + `trova_override_layout.bat`
Trova pagine con override CSS inline su classi di layout (`.guide-main`, `.guide-layout`, `#main`, ecc.).
> ✅ Attivo — utility diagnosi layout

---

## Batch

### `check_site_links.bat`
Avvia una verifica dei link del sito in locale. Controlla che tutti i link interni non siano broken.
> ✅ Attivo — utility diagnosi, lanciare periodicamente

### `httpserver.bat`
Avvia un server HTTP locale per testare il portale senza dover installare nulla. Usa Python http.server.
> ✅ Attivo — uso quotidiano in sviluppo

### `struttura.bat`
Genera `struttura.txt` con l'albero delle cartelle del repo.
> 🟡 Utility occasionale — tenere

---

## JavaScript

### `ui.js`
Logica UI condivisa: hamburger, scroll-spy, back-to-top, overlay sidebar. Caricato da tutte le pagine via `<script src="/scripts/ui.js" defer>`.
> ✅ Attivo — non è uno script di manutenzione

---

## GitHub Actions

### `supabase-keep-alive.yml`
Workflow GitHub Actions che esegue un ping a Supabase ogni giorno alle 08:00 UTC per evitare la pausa automatica del piano free (dopo 7 giorni di inattività). Configurabile anche manualmente dal tab Actions su GitHub.
> ✅ Attivo — non toccare (gestito da GitHub, non da scripts/)
