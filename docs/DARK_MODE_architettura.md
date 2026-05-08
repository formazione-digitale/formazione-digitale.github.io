# Dark Mode — Analisi Architetturale
**Formazione Digitale · Maggio 2026**

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

### Tier 3 — Valutare caso per caso
Pagine con design system proprietario, parzialmente o totalmente scollegato da `shared.css`.

| Pagina | Situazione | Strategia consigliata |
|--------|------------|----------------------|
| `database/guida-libreoffice-base-query/` | Già prevalentemente scura | Escludere dal toggle (`data-theme-lock`) |
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

Aggiungere in fondo a `shared.css`, dopo tutte le regole esistenti.

```css
/* ════════════════════════════════════════════════════════════════
   DARK MODE
   Attivato da: prefers-color-scheme (sistema) o data-theme="dark"
   Disattivato da: data-theme="light" (override manuale)
   ════════════════════════════════════════════════════════════════ */

/* Preferenza di sistema — si attiva solo se l'utente
   non ha sovrascritta manualmente con data-theme="light" */
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
  :root:not([data-theme="light"]) body {
    background: #0F1624;
  }
}

/* Override manuale — si attiva quando il JS scrive data-theme="dark"
   indipendentemente dalla preferenza di sistema */
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
[data-theme="dark"] body {
  background: #0F1624;
}

/* Componenti che non seguono le variabili e richiedono override esplicito */
[data-theme="dark"] .card {
  border-color: var(--blue-light);
}
[data-theme="dark"] .card-footer {
  background: #151F2E;
  border-color: var(--blue-light);
}
[data-theme="dark"] .stats-bar {
  background: #131C2B;
  border-color: var(--blue-light);
}
[data-theme="dark"] .hero-search {
  background: #1E2D42;
}
[data-theme="dark"] .hero-search input {
  color: var(--gray-dark);
  background: transparent;
}
[data-theme="dark"] .filter-btn {
  background: #131C2B;
  color: var(--gray-mid);
  border-color: var(--blue-light);
}
[data-theme="dark"] .filter-btn.active {
  background: var(--blue-mid);
  color: #fff;
}
[data-theme="dark"] .modal-panel,
[data-theme="dark"] .auth-panel {
  background: #1A2638;
}
[data-theme="dark"] .cf-input {
  background: #131C2B;
  border-color: var(--blue-light);
  color: var(--gray-dark);
}
```

> **Nota sui colori dark:** Le variabili dark non sono semplici inversioni. Il `--blue-dark` originale (#1F4E79) era usato come colore di sfondo scuro — in dark mode diventa un colore chiaro (#90CAF9) per testo e accenti su sfondi molto scuri. Testare sempre su ogni componente prima del deploy.

---

### 4.3 `ui.js` — file JS condiviso

Creare `/ui.js` in root, accanto a `auth.js` e `stats.js`.

```javascript
/* ════════════════════════════════════════════════════════════════
   ui.js — Comportamenti UI condivisi
   Formazione Digitale · v1.0
   
   Responsabilità:
   - Theme toggle (dark/light mode)
   - Espandibile con altri comportamenti UI futuri
   
   Non modificare per aggiungere logica di contenuto.
   ════════════════════════════════════════════════════════════════ */

// ── THEME TOGGLE ────────────────────────────────────────────────

function initThemeToggle() {
  const btn = document.getElementById('theme-toggle');
  
  // Pagine con data-theme-lock: nessun toggle
  if (document.documentElement.hasAttribute('data-theme-lock')) return;
  if (!btn) return;

  /**
   * Determina il tema corrente:
   * 1. localStorage (scelta esplicita dell'utente)
   * 2. prefers-color-scheme (preferenza del sistema)
   * 3. fallback: light
   */
  function getEffectiveTheme() {
    const saved = localStorage.getItem('fd-theme');
    if (saved) return saved;
    return window.matchMedia('(prefers-color-scheme: dark)').matches
      ? 'dark'
      : 'light';
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('fd-theme', theme);
    updateButton(theme);
  }

  function updateButton(theme) {
    if (theme === 'dark') {
      btn.textContent = '☀️';
      btn.title = 'Passa al tema chiaro';
      btn.setAttribute('aria-label', 'Passa al tema chiaro');
    } else {
      btn.textContent = '🌙';
      btn.title = 'Passa al tema scuro';
      btn.setAttribute('aria-label', 'Passa al tema scuro');
    }
  }

  btn.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme')
                    || getEffectiveTheme();
    applyTheme(current === 'dark' ? 'light' : 'dark');
  });

  // Sincronizza il bottone con il tema già applicato dall'anti-flash
  updateButton(getEffectiveTheme());

  // Ascolta i cambiamenti di sistema operativo (es. auto dark al tramonto)
  window.matchMedia('(prefers-color-scheme: dark)')
    .addEventListener('change', e => {
      // Rispetta solo se l'utente non ha scelto manualmente
      if (!localStorage.getItem('fd-theme')) {
        applyTheme(e.matches ? 'dark' : 'light');
      }
    });
}

document.addEventListener('DOMContentLoaded', initThemeToggle);
```

---

### 4.4 Bottone nell'header

In ogni pagina, dentro l'`<header>`, aggiungere il bottone toggle. La classe `.mode-toggle` è già definita in `shared.css`.

```html
<button
  id="theme-toggle"
  class="mode-toggle"
  title="Passa al tema scuro"
  aria-label="Passa al tema scuro">
  🌙
</button>
```

E prima di `</body>` in ogni pagina:

```html
<script src="/ui.js" defer></script>
```

> `defer` è corretto qui — `ui.js` può aspettare il DOM. Solo l'anti-flash in `<head>` deve essere sincrono.

---

### 4.5 Esclusione pagine Tier 3

Per le pagine che non devono rispondere al toggle (LibreOffice Base, Word):

```html
<html lang="it" data-theme-lock="true">
```

Il JS di `ui.js` controlla questo attributo e non inizializza il toggle. Il bottone nell'header può essere omesso o nascosto via CSS:

```css
/* In shared.css, solo per pagine locked */
[data-theme-lock] #theme-toggle {
  display: none;
}
```

---

## 5. Checklist di deploy

Per ogni pagina che aggiungi al sistema dark mode:

- [ ] Script anti-flash aggiunto in `<head>` prima dei CSS
- [ ] `<script src="/ui.js" defer></script>` aggiunto prima di `</body>`
- [ ] Bottone `#theme-toggle` aggiunto nell'header
- [ ] Testato in dark mode su desktop Chrome
- [ ] Testato in dark mode su mobile (Safari iOS + Chrome Android)
- [ ] Testato il flash al reload in dark mode (deve essere assente)
- [ ] Testato il cambio preferenza sistema operativo (deve seguire automaticamente se non c'è scelta manuale)
- [ ] Colori hardcoded nel `<style>` inline della pagina convertiti in variabili CSS dove possibile

---

## 6. Cosa NON fare

| ❌ Da evitare | Motivo |
|---|---|
| Script del tema in fondo alla pagina | Causa flash bianco→nero visibile |
| `class="dark"` su `<body>` | Interferisce con le animazioni `.card` e le classi di stato |
| Variabili dark duplicate in ogni pagina | Impossibile da mantenere — tutto in `shared.css` |
| Salvare il tema su Supabase | Richiede login, latenza di rete, attrito inutile per una preferenza visuale |
| Invertire semplicemente i colori | I ruoli semantici cambiano in dark mode — non è una semplice inversione |

---

## 7. Stima del lavoro

| Attività | Tempo stimato |
|---|---|
| Variabili dark in `shared.css` + override componenti | 1–2 ore |
| `ui.js` + bottone nell'header di index e mappa | 30 min |
| Anti-flash in tutte le pagine (con replace_in_files.py) | 15 min |
| Test Tier 1 (index, mappa, guide IA) | 1–2 ore |
| Revisione Tier 2 (pagine con CSS inline custom) | 2–4 ore |
| Decisione e lock Tier 3 (LibreOffice, Word) | 30 min |
| **Totale** | **5–9 ore** |

La parte più lunga non è il codice — è verificare che ogni componente specifico di pagina (hero, sidebar, box callout, tabelle, componenti interattivi) risponda correttamente alle variabili dark.

---

*Documento generato in sessione · Formazione Digitale · Maggio 2026*
