# Catalogo script — `scripts/`
**Formazione Digitale · aggiornato 09/06/2026**

---

## Python

### `aggiorna_dominio.py`
Sostituisce `formazione-digitale.github.io` → `formazione-digitale.it` in tutti gli HTML/XML.
> 🟡 Usa unica — già eseguito, conservare per emergenze

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

### `struttura.bat`
Genera `struttura.txt` con l'albero delle cartelle del repo.
> 🟡 Utility occasionale — tenere

---

## JavaScript

### `ui.js`
Logica UI condivisa: hamburger, scroll-spy, back-to-top, overlay sidebar. Caricato da tutte le pagine via `<script src="/scripts/ui.js" defer>`.
> ✅ Attivo — non è uno script di manutenzione
