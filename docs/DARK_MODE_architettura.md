# Dark Mode — Analisi Architetturale
**Formazione Digitale · Maggio 2026 · Aggiornato 09/06/2026**

---

## 1. Vale la pena farlo?

**Sì, con un asterisco.**

Il pubblico del portale (studenti, docenti) usa il sito spesso su mobile e in orari serali. Il dark mode è ormai un'aspettativa di qualità percepita, non un orpello opzionale.

Lo stack statico (HTML + CSS + JS vanilla) non è un ostacolo: il pattern descritto in questo documento è **zero-dipendenze, zero build step**, coerente con l'architettura esistente.

Il costo reale non è tecnico — è di **manutenzione CSS**: ogni nuovo componente aggiunto in futuro deve prevedere la variante dark. Se il portale cresce velocemente, questo overhead si sente.

**Raccomandazione: farlo, centralizzando tutto in `shared.css`. Non toccare mai i singoli file delle guide per il tema.**

---

## 2. Classificazione delle pagine (Tier)

Le pagine del portale non sono omogenee rispetto al sistema di design. Vanno trattate in tre gruppi distinti.

### Tier 1 — Risposta automatica
Pagine che usano `shared.css` come fonte principale di stile. Risponderanno alle variabili dark quasi senza intervento manuale.

| Pagina | Note |
|--------|-------|
| `index.html` | CSS inline + shared.css — target principale |
| `mappa.html` | CSS inline + shared.css |
| Guide IA (prompting, peer-review) | Struttura shared, pochi override inline |
| Subnet calculator, BEP tool | Idem |

### Tier 2 — Intervento mirato
Pagine con `<style>` inline esteso che usa variabili proprie o colori hardcoded. Richiedono un passaggio di revisione colore per colore.

| Pagina | Problema tipico |
|--------|-----------------|
| `marketing/guida-marketing/` | Colori inline non mappati su variabili CSS |
| `networking/hfs-server/` | Stile molto custom |
| `sistemi/codifica-binaria/` | Componenti interattivi con colori fissi |

### Tier 3 — Escludere con data-theme-lock
Pagine con design system proprietario, scollegato da `shared.css`. Usano `shared-extended.css` (palette scura propria) o hanno identità cromatica vincolata.

| Pagina | Situazione | Strategia |
|--------|------------|-----------|
| `database/guida-libreoffice-base-query/` | Usa `shared-extended.css` — sistema autonomo, già prevalentemente scuro | Escludere con `data-theme-lock="true"` |
| `database/guida-modello-logico/` | Usa `shared-extended.css` | Escludere con `data-theme-lock="true"` |
| `database/guida-database/` | Usa `shared-extended.css` (refactored 08/06/2026) | Escludere con `data-theme-lock="true"` |
| `elaborazione-testi/guida-word/` | Identità cromatica Microsoft (blu #0078D4) | Valutare se il toggle ha senso — potrebbe rompersi |

> **Esclusione onesta:** aggiungere `data-theme-lock="true"` sull'`<html>` delle pagine Tier 3 e ignorarle nel JS del toggle. L'utente non vede il bottone su quelle pagine. Comportamento trasparente, zero rework.

---

## 3. Architettura del sistema

### Pattern scelto: `prefers-color-scheme` + attributo manuale + localStorage

```
1. Default         → rispetta la preferenza del sistema operativo
2. Toggle manuale  → aggiunge data-theme="dark"|"light" su <html>
3. Persistenza     → localStorage (chiave: fd-theme)
4. Anti-flash      → script sincrono in <head> prima di qualsiasi CSS
```

**Perché `data-theme` su `<html>` e non una classe su `<body>`?**
- Evita conflitti con le animazioni `.card` e le classi di stato esistenti
- Selettori CSS più puliti e prevedibili
- Standard de facto nei design system moderni

**Perché localStorage e non Supabase?**
- Non richiede login — la preferenza del tema è una scelta visuale, non un dato utente
- È sincrono — fondamentale per l'anti-flash
- Zero latenza, zero dipendenze di rete

---

## 4. Implementazione

### 4.1 Script anti-flash

Va inserito in `<head>` **prima di qualsiasi `<link>` o `<style>`**, inline, in ogni pagina. Deve essere sincrono (il comportamento bloccante è intenzionale).

```html
<!-- ANTI-FLASH: leggere prima del render -->
<script>
  (function() {
    const saved = localStorage.getItem('fd-theme');
    if (saved) {
      document.documentElement.setAttribute('data-theme', saved);
    }
  })();
</script>
```

> ⚠️ Non spostare questo script in fondo alla pagina. Causerebbe un flash bianco→nero visibile ad ogni caricamento in dark mode.

---

### 4.2 Variabili dark in `shared.css`

Aggiungere in fondo a `shared.css`, dopo tutte le regole esistenti (sezione 17 — attualmente placeholder).

```css
/* ════════════════════════════════════════════════════════════════
   DARK MODE
   Attivato da: prefers-color-scheme (sistema) o data-theme="dark"
   Disattivato da: data-theme="light" (override manuale)
   ════════════════════════════════════════════════════════════════ */

@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --blue-dark:    #90CAF9;
    --blue-mid:     #64B5F6;
    --blue-light:   #1E3A5F;
    --blue-pale:    #132338;
    --green-dark:   #81C784;
    --green-light:  #1B3A27;
    --amber-dark:   #FFB74D;
    --amber-light:  #3A2800;
    --gray-dark:    #E8EAED;
    --gray-mid:     #9AA0A6;
    --gray-light:   #1E1E1E;
    --white:        #1A1A2E;
  }
  :root:not([data-theme="light"]) body { background: #0F1624; }
}

[data-theme="dark"] {
  --blue-dark:    #90CAF9;
  --blue-mid:     #64B5F6;
  --blue-light:   #1E3A5F;
  --blue-pale:    #132338;
  --green-dark:   #81C784;
  --green-light:  #1B3A27;
  --amber-dark:   #FFB74D;
  --amber-light:  #3A2800;
  --gray-dark:    #E8EAED;
  --gray-mid:     #9AA0A6;
  --gray-light:   #1E1E1E;
  --white:        #1A1A2E;
}
[data-theme="dark"] body { background: #0F1624; }
```

> **Nota sui colori dark:** Le variabili dark non sono semplici inversioni — sono bilanciate per leggibilità e contrasto.

---

## 5. Stima del lavoro

| Attività | Tempo stimato |
|---|---|
| Variabili dark in `shared.css` + override componenti | 1–2 ore |
| `ui.js` + bottone nell'header di index e mappa | 30 min |
| Anti-flash in tutte le pagine (con `replace_in_files.py`) | 15 min |
| Test Tier 1 (index, mappa, guide IA) | 1–2 ore |
| Revisione Tier 2 (pagine con CSS inline custom) | 2–4 ore |
| Decisione e lock Tier 3 (database, Word) | 30 min |
| **Totale** | **5–9 ore** |

La parte più lunga non è il codice — è verificare che ogni componente specifico di pagina (hero, sidebar, box callout, tabelle, componenti interattivi) risponda correttamente alle variabili dark.

---

*Documento aggiornato 09/06/2026 · Formazione Digitale*
