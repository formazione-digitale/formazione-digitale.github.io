# Integrazione Badge DigComp/DigCompEdu
## Portale Formazione Digitale — Guida operativa

> **Versione:** 2.0 · Maggio 2026  
> **Basata su:** Report di analisi DigComp/DigCompEdu v1.0 (maggio 2026)  
> **Stato:** Documento pro-futuro — implementazione prevista settembre 2026  
> **Prerequisiti:** accesso al repository GitHub · file `manifest_digcomp.json` e `badge_digcomp_snippet.html`  
> **Tempo stimato:** 15–20 minuti  
> **File da modificare:** `manifest.json`, `index.html`

---

## Panoramica

Questa guida aggiunge tre funzionalità al portale:

1. **Badge DigComp/DigCompEdu** in ogni card — codici DC e DCEdu, livello (Foundation / Intermediate / Advanced)
2. **Filtro per Area DigComp** — seconda barra di filtri sotto quella principale
3. **Dati strutturati nel manifest** — base per future feature (profilo competenze, percorsi, Supabase)

L'implementazione è **completamente retrocompatibile**: il portale funziona normalmente anche durante la modifica.

---

## Rubrica livelli — come assegnare digcomp_level

| Livello nel portale | Corrispondenza DigComp | digcomp_level |
|---|---|---|
| Livello base | Foundation (1–2) | `"foundation"` |
| Livello base–intermedio | Intermediate (3–4) | `"intermediate"` |
| Livello intermedio | Intermediate (3–4) | `"intermediate"` |
| Livello intermedio-avanzato | Advanced (5–6) | `"advanced"` |

> Il livello si assegna in base al livello dichiarato nella card-meta della risorsa, non a una valutazione soggettiva del contenuto.

---

## Criteri di mappatura DigComp

### Principio generale
L'analisi è per **inferenza semantica**: partendo da titoli, descrizioni, tag e struttura della risorsa, si identifica quale competenza DigComp ogni risorsa sviluppa o supporta. Una risorsa può coprire più competenze ma va evitato l'over-tagging — massimo 3 codici DC per risorsa.

### Regole operative

| Regola | Descrizione |
|---|---|
| Primario vs parziale | Assegna solo le competenze che la risorsa sviluppa *primariamente*, non quelle che tocca di passaggio |
| Max 3 codici DC | Oltre 3 codici diluisce il segnale e rende i badge illeggibili |
| Area sicurezza | DC 4.x va assegnato solo a risorse che trattano esplicitamente sicurezza, privacy o protezione dati |
| DC 3.4 (programmazione) | Riservato a risorse con componente logico-algoritmica reale (SQL, binario, subnetting) |
| DC 2.1 | "Interagire con tecnologie digitali" — assegnarlo solo se l'interazione è il focus, non un prerequisito |

---

## Mappatura attuale — sintesi copertura DigComp 2.2

| Area DigComp | Copertura attuale | Priorità integrazione |
|---|---|---|
| 1. Info & Dati | ~20% | ALTA |
| 2. Comunicazione | ~35% | MEDIA |
| 3. Creazione | ~55% | BASSA |
| 4. Sicurezza | ~10% | ALTA ⚠ |
| 5. Problem Solving | ~60% | BASSA |

> **Nota critica Area 4:** nessuna risorsa attiva copre DC 4.x. Le risorse pianificate (Cybersicurezza, Password, Triade CIA) hanno alta priorità strategica per colmare questa lacuna.

## Mappatura attuale — sintesi copertura DigCompEdu

| Area DigCompEdu | Copertura attuale |
|---|---|
| 2. Risorse digitali | ~50% |
| 3. Insegnamento e apprendimento | ~35% |
| 4. Valutazione | ~30% |
| 5. Empowerment studenti | ~20% |
| 6. Competenza digitale studenti | ~55% |

---

## Lacune identificate — roadmap contenuti

In ordine di priorità strategica DigComp:

1. **Cybersicurezza personale** (DC 4.1 + 4.2) — già pianificata come 'coming', avanzarla
2. **Valutare fonti online / fact-checking** (DC 1.2) — già 'coming' come Strumento, estendere a Guida
3. **Privacy e identità digitale** (DC 2.6 + 4.2) — non presente né pianificata
4. **Copyright e licenze** (DC 3.3) — non presente; particolarmente rilevante per DigCompEdu 2.3
5. **Benessere digitale** (DC 4.3) — assente

---

## File coinvolti

| File | Azione | Sezione snippet |
|---|---|---|
| `manifest.json` | Sostituire interamente | — (usa `manifest_digcomp.json`) |
| `index.html` → `<style>` | Incollare CSS badge | Sezione 1 |
| `index.html` → body | Incollare HTML filtro | Sezione 2 |
| `index.html` → `<script>` | Sostituire `filterAll()` + aggiungere JS | Sezione 3 |

---

## Passo 1 — Aggiorna `manifest.json`

### 1.1 Apri il file su GitHub

```
Repository → manifest.json → icona matita (Edit this file)
```

### 1.2 Sostituisci il contenuto

Seleziona tutto il testo nell'editor (`Ctrl+A`) e incolla il contenuto del file `manifest_digcomp.json`.

### 1.3 Verifica i nuovi campi

Ogni risorsa nel nuovo manifest ha questi quattro campi aggiuntivi:

```json
{
  "digcomp":       ["DC 3.1", "DC 3.2"],
  "digcomp_level": "foundation",
  "digcompedu":    ["DCEdu 2.2", "DCEdu 6.3"],
  "digcomp_areas": ["creazione"]
}
```

| Campo | Tipo | Valori possibili |
|---|---|---|
| `digcomp` | array di stringhe | `"DC 1.1"` … `"DC 5.4"` · max 3 valori |
| `digcomp_level` | stringa | `"foundation"` · `"intermediate"` · `"advanced"` |
| `digcompedu` | array di stringhe | `"DCEdu 2.1"` … `"DCEdu 6.5"` |
| `digcomp_areas` | array di stringhe | `"informazioni"` · `"comunicazione"` · `"creazione"` · `"sicurezza"` · `"problem-solving"` |

### 1.4 Commit

```
Commit changes → messaggio: "feat: add DigComp/DigCompEdu fields to manifest"
```

> ⚠️ **Non aspettare il deploy di GitHub Pages** — prosegui subito con il Passo 2. I due commit (manifest + index.html) possono essere fatti in sequenza e GitHub Pages li pubblica insieme.

---

## Passo 2 — Apri `index.html` in modifica

```
Repository → index.html → icona matita (Edit this file)
```

Lascia questa scheda aperta: farai tre inserimenti nello stesso file prima di fare commit.

---

## Passo 3 — Incolla il CSS (Sezione 1 dello snippet)

### 3.1 Individua il punto di inserimento

Usa `Ctrl+F` nell'editor GitHub e cerca:

```
/* ── ANIMATIONS
```

Il punto di inserimento è **immediatamente prima** di questa riga.

### 3.2 Incolla il CSS

Dal file `badge_digcomp_snippet.html`, copia il blocco compreso tra:

```
/* ── BADGE DIGCOMP ───────────────────────────────────────────── */
```

…fino alla chiusura dell'ultima regola:

```css
.dc-level.advanced { color: #7D4E00; background: #FFF3CD; }
```

### 3.3 Risultato atteso

Il `<style>` conterrà — nell'ordine — le regole esistenti, poi il nuovo blocco badge, poi le animazioni. Nessuna regola esistente viene toccata.

---

## Passo 4 — Incolla l'HTML del filtro (Sezione 2 dello snippet)

### 4.1 Individua il punto di inserimento

Cerca nell'editor:

```html
<div id="no-results">
```

Il punto di inserimento è **immediatamente prima** di questa riga.

### 4.2 Incolla l'HTML

```html
<div class="filter-bar-dc" id="filter-bar-dc" style="display:none;">
  <span class="filter-dc-label">Area DigComp:</span>
  <button class="filter-btn-dc active" onclick="setDCFilter('all',this)">Tutte</button>
  <button class="filter-btn-dc" onclick="setDCFilter('informazioni',this)">📋 Informazioni</button>
  <button class="filter-btn-dc" onclick="setDCFilter('comunicazione',this)">💬 Comunicazione</button>
  <button class="filter-btn-dc" onclick="setDCFilter('creazione',this)">✏️ Creazione</button>
  <button class="filter-btn-dc" onclick="setDCFilter('sicurezza',this)">🔒 Sicurezza</button>
  <button class="filter-btn-dc" onclick="setDCFilter('problem-solving',this)">⚙️ Problem Solving</button>
</div>
```

### 4.3 Note importanti

Il `<div>` ha `style="display:none;"` — è intenzionale. La barra viene mostrata automaticamente dal JS solo dopo che `injectDCBadges()` ha caricato il manifest con successo. Se il manifest non viene trovato, la barra resta nascosta e il portale appare identico a prima.

> ⚠️ **Area Sicurezza:** nessuna risorsa attiva ha `"sicurezza"` in `digcomp_areas`. Il filtro "Sicurezza" restituisce zero card finché non sarà pubblicata la guida Cybersicurezza. Valutare se nasconderlo temporaneamente.

---

## Passo 5 — Aggiorna il JavaScript (Sezione 3 dello snippet)

### 5.1 Sostituisci la funzione `filterAll()`

Cerca nell'editor:

```
function filterAll() {
```

Seleziona tutta la funzione (dalla riga `function filterAll() {` fino alla `}` di chiusura inclusa) e sostituiscila con la versione estesa del file snippet (Sezione 3).

**Differenze rispetto alla versione originale:**

| Riga | Prima | Dopo |
|---|---|---|
| nuova variabile | — | `const areas = card.dataset.dcAreas \|\| ''` |
| nuovo check | — | `const matchDC = activeDCFilter === 'all' \|\| areas.includes(activeDCFilter)` |
| condizione `show` | `matchCat && matchQ` | `matchCat && matchQ && matchDC` |
| no-results | solo su `q` | su `q` oppure `activeDCFilter !== 'all'` |

### 5.2 Aggiungi il blocco JS completo

Incolla alla fine del `<script>` esistente, prima del tag `</script>`, il resto del codice della Sezione 3 (`injectDCBadges`, `setDCFilter`, listener DOMContentLoaded).

---

## Passo 6 — Commit e deploy

```
Commit changes → messaggio: "feat: add DigComp badges, DC area filter, extended filterAll"
```

Aspetta **1–2 minuti** per il deploy di GitHub Pages.

---

## Passo 7 — Verifica sul portale live

### ✅ Check 1 — Filtro DigComp visibile

Sotto la riga `[Tutto] [Guide] [Strumenti] [Pillole]` deve comparire:

```
Area DigComp: [Tutte] [Informazioni] [Comunicazione] [Creazione] [Sicurezza] [Problem Solving]
```

Se non appare → vai al Troubleshooting A.

### ✅ Check 2 — Badge nelle card

In ogni card attiva (non "coming"), tra la descrizione e il footer, deve comparire una riga con:
- una pillola colorata del livello (es. `Intermediate 3–4`)
- uno o più badge blu con i codici DigComp (es. `DC 3.1`)
- uno o più badge verdi con i codici DigCompEdu (es. `DCEdu 2.2`)

Se non appaiono → vai al Troubleshooting B.

### ✅ Check 3 — Filtro DigComp funzionante

Clicca **Creazione** nella barra DigComp. Devono restare visibili: Word, Guida Marketing, Guida Prompting, Peer-review IA, Prompt Builder, Subnet Calculator, Codifica Binaria.

### ✅ Check 4 — Filtri combinati

Con **Strumenti** + **Problem Solving** attivi contemporaneamente, devono restare visibili solo: Break-Even Point, Subnet Calculator, Codifica Binaria, Analizzatore SEO.

### ✅ Check 5 — Ricerca compatibile

Con la barra di ricerca attiva (es. cerca `"ia"`), il filtro DigComp deve continuare a funzionare in AND con il testo cercato.

---

## Troubleshooting

### A — Il filtro DigComp non appare

La barra è controllata da `injectDCBadges()`. Se non appare, la funzione non ha completato con successo.

**Causa più comune:** il `manifest.json` non è stato aggiornato o GitHub Pages non ha ancora pubblicato la versione nuova.

**Verifica diretta:** apri nel browser `https://formazione-digitale.github.io/manifest.json` e controlla che il JSON contenga il campo `digcomp` nella prima risorsa. Se vedi ancora il vecchio manifest, aspetta qualche minuto o fai un hard refresh (`Ctrl+Shift+R`).

### B — I badge non appaiono ma il filtro sì

Il manifest è corretto, ma `injectDCBadges()` non riesce ad abbinare i path delle card ai path del manifest.

**Causa più comune:** il valore dell'attributo `href` di una card non corrisponde esattamente al campo `path` nel manifest.

**Come diagnosticare:** apri la console del browser (`F12` → Console) e incolla:

```javascript
document.querySelectorAll('.card:not(.coming) a').forEach(a => {
  let href = a.getAttribute('href') || '';
  if (!href.startsWith('/')) href = '/' + href;
  if (!href.endsWith('/')) href = href + '/';
  console.log(href);
});
```

Confronta i path stampati con i valori `path` nel manifest. Ogni path deve corrispondere esattamente, incluso il trailing slash.

### C — La `filterAll` non filtra per area DigComp

Il check `matchDC` usa `card.dataset.dcAreas`, scritto da `injectDCBadges()`. Se clicchi un filtro DC prima che la funzione async abbia completato, l'attributo non esiste ancora e tutte le card passano il check.

**In pratica questo non dovrebbe accadere** perché `injectDCBadges()` viene chiamata al `DOMContentLoaded`, che precede qualsiasi click utente. Se accade in fase di sviluppo locale su file system (senza server), il `fetch('manifest.json')` può fallire con un errore CORS — usa sempre un server locale (`python -m http.server 8000`) per testare.

### D — Le card "coming" mostrano badge

Le card `.coming` sono escluse dal selettore `document.querySelectorAll('.card:not(.coming)')` — non ricevono badge. Se li vedi, verifica che la classe della card sia esattamente `coming` (senza prefisso `card-`).

---

## Aggiungere una nuova risorsa dopo questa integrazione

Il workflow rimane identico a quello documentato nella `Guida_Collaboratori`, con un solo passo aggiuntivo: nel blocco JSON da aggiungere a `manifest.json`, includere i quattro nuovi campi seguendo la rubrica livelli e i criteri di mappatura documentati sopra.

**Esempio per una nuova guida sulla Cybersicurezza:**

```json
{
  "path": "/cybersicurezza/guida-cybersicurezza/",
  "label": "Cybersicurezza personale",
  "short": "Cybersicurezza",
  "cat": "guide",
  "emoji": "🔒",
  "tags": ["cybersicurezza", "password", "phishing", "privacy", "autenticazione"],
  "meta": "Livello base · 20 min",
  "description": "Password, phishing, autenticazione a due fattori. Come proteggere i propri account e dati personali.",
  "featured": false,
  "active": true,
  "digcomp":       ["DC 4.1", "DC 4.2"],
  "digcomp_level": "foundation",
  "digcompedu":    ["DCEdu 6.4"],
  "digcomp_areas": ["sicurezza"]
}
```

I badge appaiono automaticamente nella card senza modificare il codice HTML di `index.html`.

---

## Riferimento rapido — codici DigComp 2.2

| Codice | Competenza | Area |
|---|---|---|
| DC 1.1 | Navigare, cercare, filtrare | Informazioni |
| DC 1.2 | Valutare dati e contenuti | Informazioni |
| DC 1.3 | Gestire dati e contenuti | Informazioni |
| DC 2.1 | Interagire con tecnologie digitali | Comunicazione |
| DC 2.2 | Condividere con tecnologie digitali | Comunicazione |
| DC 2.6 | Gestire l'identità digitale | Comunicazione |
| DC 3.1 | Sviluppare contenuti digitali | Creazione |
| DC 3.2 | Integrare e rielaborare contenuti | Creazione |
| DC 3.3 | Copyright e licenze | Creazione |
| DC 3.4 | Programmazione | Creazione |
| DC 4.1 | Proteggere i dispositivi | Sicurezza |
| DC 4.2 | Proteggere dati e privacy | Sicurezza |
| DC 4.3 | Tutelare la salute e il benessere | Sicurezza |
| DC 5.1 | Risolvere problemi tecnici | Problem Solving |
| DC 5.2 | Identificare bisogni e soluzioni | Problem Solving |
| DC 5.3 | Usare creativamente le tecnologie | Problem Solving |
| DC 5.4 | Identificare divari di competenza | Problem Solving |

## Riferimento rapido — codici DigCompEdu (22 competenze complete)

**Area 1 — Coinvolgimento e valorizzazione professionale**

| Codice | Competenza |
|---|---|
| DCEdu 1.1 | Comunicazione organizzativa |
| DCEdu 1.2 | Collaborazione professionale |
| DCEdu 1.3 | Pratica riflessiva |
| DCEdu 1.4 | Aggiornamento professionale continuo |

**Area 2 — Risorse digitali**

| Codice | Competenza |
|---|---|
| DCEdu 2.1 | Selezionare risorse digitali |
| DCEdu 2.2 | Creare e modificare risorse digitali |
| DCEdu 2.3 | Gestire, proteggere e condividere risorse |

**Area 3 — Pratiche di insegnamento e apprendimento**

| Codice | Competenza |
|---|---|
| DCEdu 3.1 | Insegnare con le tecnologie digitali |
| DCEdu 3.2 | Guidare e supportare l'apprendimento |
| DCEdu 3.3 | Apprendimento collaborativo |
| DCEdu 3.4 | Apprendimento auto-regolato |

**Area 4 — Valutazione dell'apprendimento**

| Codice | Competenza |
|---|---|
| DCEdu 4.1 | Strategie di valutazione |
| DCEdu 4.2 | Analizzare le prove di apprendimento |
| DCEdu 4.3 | Feedback e pianificazione |

**Area 5 — Valorizzazione delle potenzialità degli studenti**

| Codice | Competenza |
|---|---|
| DCEdu 5.1 | Accessibilità e inclusione |
| DCEdu 5.2 | Differenziazione e personalizzazione |
| DCEdu 5.3 | Coinvolgimento attivo degli studenti |

**Area 6 — Favorire lo sviluppo delle competenze digitali degli studenti**

| Codice | Competenza |
|---|---|
| DCEdu 6.1 | Alfabetizzazione su informazioni e dati |
| DCEdu 6.2 | Comunicazione e collaborazione digitale |
| DCEdu 6.3 | Creazione di contenuti digitali |
| DCEdu 6.4 | Uso responsabile e sicuro delle tecnologie |
| DCEdu 6.5 | Problem solving digitale |

> Fonte: Redecker, C. (2017). *European Framework for the Digital Competence of Educators: DigCompEdu*. JRC Science for Policy Report. Traduzione italiana: Bocconi, Earp, Panesi (2018), CNR-ITD.

---

*Documento aggiornato in maggio 2026 sulla base del Report di analisi DigComp/DigCompEdu v1.0.*  
*Da aggiornare quando vengono aggiunte nuove risorse o modificata la struttura del manifest.*
