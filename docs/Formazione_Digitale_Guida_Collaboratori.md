# Formazione Digitale — Guida per i collaboratori
**Aggiungere nuove risorse al portale**
*Per chi vuole contribuire in autonomia · Aggiornata 19/06/2026*

---

## A chi serve questo documento

Questa guida spiega come preparare una nuova risorsa (guida, strumento o pillola) e
come integrarla nel portale **Formazione Digitale**. Non richiede competenze di
programmazione avanzate — solo HTML di base e familiarità con GitHub.

---

## 1. Struttura del portale

Il portale è un repository GitHub composto da file HTML e cartelle, pubblicato
automaticamente su **Vercel** ad ogni modifica sul branch `main`. Ogni risorsa vive
nella propria cartella, completamente indipendente dalle altre.

```
formazione-digitale.github.io/
├── index.html                    ← homepage del portale (NON modificare la struttura)
├── manifest.json                 ← elenco di tutte le risorse (vedi punto 6 — passo obbligatorio)
├── intelligenza-artificiale/
│   ├── guida-prompting/
│   │   └── index.html
│   └── prompt-builder/
│       └── index.html
├── database/
│   ├── guida-database/
│   │   └── index.html
│   └── ...
└── nuova-area-o-risorsa/         ← la tua nuova cartella
    ├── index.html
    └── img/                      ← se ci sono immagini
```

> **Regola fondamentale:** ogni risorsa vive nella propria cartella, con un file
> `index.html` al suo interno. I file di risorse diverse non si mescolano mai nella
> stessa cartella. L'unico file nella root è `index.html` (la homepage del portale).

---

## 2. Convenzioni di denominazione

I nomi di file e cartelle devono seguire queste convenzioni — Vercel (come GitHub)
è case-sensitive: distingue maiuscole e minuscole, e gli spazi rompono i link.

| Cosa | Regola | Esempio |
|---|---|---|
| **Nome cartella** | Tutto minuscolo, parole separate da trattino (kebab-case) | `guida-cybersicurezza` |
| **File principale** | Sempre `index.html` dentro la cartella della risorsa | `guida-cybersicurezza/index.html` |
| **Immagini** | In una sottocartella `/img` dentro la cartella della risorsa | `guida-cybersicurezza/img/screenshot1.png` |
| **File aggiuntivi** | DB, Excel, PDF, allegati: tutti nella stessa cartella della risorsa | `gantt-planner/gantt-planner.xlsx` |
| **Link interni** | I link dentro la guida devono essere relativi, non assoluti a localhost | `<a href="../altra-guida/">` |
| **Link esterni/interni al portale** | **Mai `target="_blank"`** — la navigazione resta sempre nella stessa scheda | `<a href="/database/">` (senza target) |
| **Test locale** | Apri il file HTML nel browser prima di proporlo | — |

**✅ Esempi corretti:**
```
sicurezza/guida-cybersicurezza/index.html
foglio-di-calcolo/guida-funzioni-excel/index.html
```

**❌ Esempi da evitare:**
```
Guida Cybersicurezza (con spazi)/index.html
GUIDA_EXCEL_FINALE_v2.html  (maiuscole, underscore, versione nel nome)
```

---

## 3. I quattro tipi di scheda

La homepage usa quattro tipi di scheda (card), ognuno con comportamento visivo diverso.

| Tipo | Aspetto | Comportamento hover | Uso |
|---|---|---|---|
| **card-featured** | Sfondo blu scuro | Gradiente più scuro, titolo resta bianco | Risorsa di punta, massimo una per sezione |
| **card-active** | Sfondo azzurro chiaro | Azzurro più saturo, titolo diventa blu-mid | Tutte le risorse disponibili standard — **questo è il tipo che userai quasi sempre** |
| **card.coming** | Sfondo grigio tratteggiato | Nessun hover (non cliccabile) | Risorse in preparazione, non ancora pronte |
| **card-area** | Banda colorata, formato largo | Si solleva leggermente | Solo per aree che raggruppano 3+ risorse correlate (le "hub" — vedi punto 7, di solito gestite direttamente con Claude) |

> **Regola pratica:** per una nuova risorsa singola, usa quasi sempre **card-active**.
> Se non è ancora pronta, usa **card.coming** come segnaposto e la converti in
> card-active quando è completa.

---

## 4. Il codice HTML di una scheda

Ogni scheda è un blocco HTML da incollare dentro la sezione giusta dell'`index.html`.

### Template A — card-active (risorsa disponibile)

Usa questo per la maggior parte delle nuove risorse.

```html
<!-- CARD: [NOME RISORSA] -->
<div class="card card-active" data-cat="[CATEGORIA]" data-tags="[parola1 parola2 parola3]">
  <div class="card-badge-strip badge-[COLORE]"></div>
  <a href="[area]/[nome-risorsa]/">
    <div class="card-body">
      <div class="card-icon">[EMOJI]</div>
      <div class="card-category cat-[CATEGORIA]">Guida completa</div>
      <div class="card-title">[TITOLO DELLA RISORSA]</div>
      <div class="card-tags">
        <span class="tag tag-blue">[Tag 1]</span>
        <span class="tag tag-blue">[Tag 2]</span>
      </div>
      <div class="card-desc">[DESCRIZIONE BREVE — 1-2 righe]</div>
    </div>
    <div class="card-footer">
      <div class="card-meta">[NOTE — es. Con esempi · Livello base]</div>
      <div class="card-cta">Apri la guida <span class="arrow">→</span></div>
    </div>
  </a>
</div>
```

> Nota il link: `href="[area]/[nome-risorsa]/"` — punta alla **cartella**, non a un
> file `.html` specifico, perché dentro c'è sempre un `index.html`.

### Template B — card.coming (in preparazione)

Usa questo come segnaposto per risorse non ancora pronte. Non è cliccabile.

```html
<!-- CARD: [NOME RISORSA] — in preparazione -->
<div class="card coming" data-cat="[CATEGORIA]" data-tags="">
  <div class="card-badge-strip"></div>
  <div class="card-body">
    <div class="card-icon">[EMOJI]</div>
    <div class="card-category cat-coming">Prossimamente</div>
    <div class="card-title">[TITOLO DELLA RISORSA]</div>
    <div class="card-desc">[DESCRIZIONE BREVE]</div>
  </div>
  <div class="card-footer">
    <div class="card-meta">In preparazione</div>
    <div class="card-cta">Disponibile presto</div>
  </div>
</div>
```

### Valori da compilare

| Placeholder | Valori possibili | Note |
|---|---|---|
| `[CATEGORIA]` | `guide` / `strumento` / `pillola` | Determina il filtro e il colore della label |
| `[COLORE]` nel badge | `blue` / `green` / `amber` / `purple` | blue per guide, green per strumenti, amber per pillole |
| `[EMOJI]` | Qualsiasi emoji Unicode | 🤖 IA · 🗄️ DB · 🔒 sicurezza · 📊 dati · 📝 testo |
| `[area]` | Nome della cartella area (es. `sicurezza`, `database`) | Deve corrispondere esattamente alla cartella reale |
| `[nome-risorsa]` | Nome della cartella della risorsa | kebab-case, vedi punto 2 |
| `data-tags` | Parole chiave separate da spazio | Usate dalla ricerca — metti termini che l'utente potrebbe cercare |

---

## 5. Dove incollare la card nell'index.html

L'`index.html` ha tre sezioni principali, ognuna con il proprio ID.

```html
<!-- SEZIONE GUIDE — cerca questo commento nell'index.html -->
<div class="cards cards-2" id="cards-guide">
  <!-- incolla qui le card di tipo GUIDE -->
</div>

<!-- SEZIONE STRUMENTI -->
<div class="cards cards-3" id="cards-strumento">
  <!-- incolla qui le card di tipo STRUMENTI -->
</div>

<!-- SEZIONE PILLOLE -->
<div class="cards cards-3" id="cards-pillola">
  <!-- incolla qui le card di tipo PILLOLE -->
</div>
```

> **Ordine delle card dentro una sezione:** 1. card-featured (al massimo una) →
> 2. card-active (tutte le risorse disponibili) → 3. card.coming (segnaposto in fondo).

---

## 6. manifest.json — passo obbligatorio, non saltarlo

A differenza di prima, oggi il portale ha un file **`manifest.json`** nella root che
è la fonte di verità per tutte le risorse — alimenta le mappe interattive, la ricerca,
le statistiche e la sitemap per Google. **Ogni nuova risorsa deve avere una voce qui,
altrimenti esiste solo nella home e in nessun altro posto del portale.**

Aggiungi un blocco così, in coda all'array nel file:

```json
{
  "path": "/[area]/[nome-risorsa]/",
  "label": "[Titolo completo]",
  "short": "[Titolo breve]",
  "cat": "guide",
  "emoji": "🔒",
  "tags": ["parola1", "parola2", "parola3"],
  "meta": "[Testo secondario, es. 10 sezioni · Livello base]",
  "description": "[Descrizione breve, 1-2 frasi]",
  "featured": false,
  "active": true,
  "digcomp": [],
  "digcompedu": []
}
```

I campi `digcomp` e `digcompedu` (mapping alle competenze digitali europee) si
possono lasciare vuoti — chi coordina il portale li compila in un secondo momento.

---

## 7. Aree con tante risorse — le "hub"

Se un'area tematica (es. "Database") raggiunge 3 o più risorse correlate, può
diventare una **hub di sezione**: una pagina dedicata con mappa interattiva e percorso
consigliato, invece di card singole sparse in home. Questa trasformazione è più
articolata (tocca `manifest.json`, `aree.json`, la home e una pagina nuova) — se pensi
che un'area sia arrivata a questo punto, segnalalo a chi coordina il portale invece di
farlo autonomamente.

---

## 8. Procedura completa, passo per passo

1. **Prepara la risorsa**: HTML (+ eventuali immagini in `/img`, file allegati).
2. **Testa il file localmente** aprendo l'HTML nel browser e verificando che tutto funzioni.
3. **Crea la cartella** nel posto giusto del repository, seguendo le convenzioni del
   punto 2. Puoi farlo:
   - **con Git/GitHub Desktop**: crea un branch, aggiungi i file, fai commit e push;
   - **dall'interfaccia web di GitHub**: *Add file → Upload files*, digitando il
     percorso completo della cartella prima del nome file.
4. **Aggiorna `manifest.json`** con il blocco del punto 6 — non è opzionale.
5. **Apri `index.html`** (via Git o dall'icona matita su GitHub) e incolla il
   template card del punto 4 nella sezione giusta (punto 5).
6. **Salva le modifiche**:
   - con Git: commit + push, poi apri una Pull Request se lavori su un branch separato;
   - da web: *Commit changes* — se non hai accesso diretto a `main`, GitHub propone
     automaticamente di creare un branch e una Pull Request.
7. **Attendi il deploy** — Vercel pubblica automaticamente entro 1-2 minuti dal merge
   su `main`. Verifica sul portale live.

> **Verifica finale.** Dopo il deploy, controlla che: (1) la card appare nella sezione
> corretta, (2) il filtro per categoria funziona, (3) la ricerca trova la risorsa
> digitando una delle parole in `data-tags` **o** una parola della descrizione (la
> ricerca del portale cerca anche dentro `manifest.json`, non solo tra le card visibili
> in home), (4) il click apre la risorsa corretta, restando nella stessa scheda.

---

## Appendice — Riferimento rapido

### Emoji consigliate per tipo di risorsa

| Emoji | Argomento | Esempio di uso |
|---|---|---|
| 🤖 | Intelligenza Artificiale | Guide su IA, ChatGPT, prompting |
| 🗄️ | Database | LibreOffice Base, SQL, Access |
| 💻 | Programmazione | Algoritmi, C++, strutture dati |
| 🔒 | Cybersicurezza | Password, phishing, privacy |
| 📊 | Dati e fogli di calcolo | Excel, Calc, analisi dati |
| 📝 | Scrittura e testo | Word, Writer, documenti |
| 🌐 | Web e internet | Browser, ricerca online, social |
| 📱 | Smartphone e app | Guide mobile, app Android/iOS |
| 🔍 | Ricerca e verifica | Fact-checking, fonti online |
| ⚙️ | Strumenti generici | Tool, utility, configurazioni |
| 📅 | Pianificazione | Gantt, Kanban, project management |
| 💡 | Pillole e consigli | Hint rapidi, suggerimenti brevi |

### In caso di dubbi

Se qualcosa non funziona dopo il deploy, controlla in quest'ordine:

1. Il nome della cartella nel link `href` corrisponde **esattamente** (incluse
   maiuscole/minuscole) alla cartella reale nel repository
2. Non ci sono spazi nei nomi di file o cartelle
3. C'è davvero un file `index.html` dentro la cartella della risorsa
4. La voce in `manifest.json` ha il `path` scritto esattamente come la cartella,
   comprese le barre `/` iniziale e finale
5. Nessun link nella pagina usa `target="_blank"`

Vercel è case-sensitive come GitHub: `Guida.html` e `guida.html` sono file diversi.
