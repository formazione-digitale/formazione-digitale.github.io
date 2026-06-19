# TEMPLATE SESSIONE — Formazione Digitale
# Usa questo file all'inizio di ogni nuova chat NEL PROGETTO Claude già configurato
# (le Istruzioni di progetto sono già caricate — qui aggiungi solo lo stato
# corrente e il task specifico).
# Compila le sezioni [IN MAIUSCOLO] e incolla tutto come primo messaggio.
# Ultimo aggiornamento: 19/06/2026

---

## STATO ATTUALE DEL REPOSITORY

> Aggiorna questa sezione se hai aggiunto nuove cartelle, hub o file
> dall'ultima sessione. Lo stato sotto riflette il repository al 19/06/2026.

```
formazione-digitale.github.io/
├── index.html
├── mappa-risorse.html
├── mappa-aree.html              (navigazione a due livelli, hash URL)
├── mappa-framework.html
├── manifest.json                (31 risorse, 2 hub: database, programmazione)
├── aree.json                    (11 aree, hasHub su database/programmazione)
├── database/                    HUB — 3 guide
├── programmazione/               HUB — 2 guide
├── project-management/
│   ├── guida-gestione-progetti/
│   ├── kanban-tool/
│   └── gantt-planner/
├── intelligenza-artificiale/
├── competenze-digitali/
├── sicurezza/
├── marketing/
├── networking/
├── sistemi/
├── foglio-di-calcolo/
└── elaborazione-testi/
```

---

## FILE ALLEGATI IN QUESTA SESSIONE

I seguenti file sono allegati al progetto e disponibili per la lettura:

- `index.html` — versione attuale della homepage
- `manifest.json` — catalogo risorse aggiornato
- `aree.json` — definizione aree con hasHub

> Se stai lavorando su una guida o hub specifica, allega anche quel file
> e aggiungilo qui.

---

## TASK

[DESCRIVI QUI COSA VUOI FARE IN QUESTA SESSIONE]

---

### Esempi di task pronti da copiare:

**Aggiungere una nuova scheda (card singola):**
```
Aggiungi una nuova card nella sezione [Guide|Strumenti|Pillole]
con questi dati:
- Titolo: [TITOLO]
- Descrizione: [DESCRIZIONE BREVE]
- Cartella: [nome-area]/[nome-risorsa]/
- Tag per la ricerca: [parola1 parola2 parola3]
- Tipo: [card-active | card.coming]
Aggiorna anche manifest.json con il mapping DigComp/DigCompEdu pertinente.
```

**Convertire una card.coming in card-active:**
```
La risorsa "[TITOLO]" è ora disponibile.
Converti la sua card da card.coming a card-active.
Il file si trova in: [area]/[nome-risorsa]/
Aggiorna manifest.json: active: true.
```

**Creare una nuova hub:**
```
L'area "[NOME AREA]" ha raggiunto [N] risorse correlate.
Valuta se trasformarla in hub di sezione seguendo il pattern
di database/ e programmazione/ (header due colonne, mappa D3,
percorso consigliato). Se sì, prepara:
1. [area]/index.html
2. Aggiornamento aree.json (hasHub: true)
3. Aggiornamento manifest.json (campo hub + order sulle risorse)
4. Card-area in home, rimozione delle card singole equivalenti
```

**Creare una nuova guida HTML:**
```
Crea una nuova guida HTML su [ARGOMENTO].
Usa la stessa grafica e struttura delle guide esistenti in [area]/.
La guida deve contenere: [DESCRIVI SEZIONI E CONTENUTO]
Cartella: [nome-area]/[nome-guida]/
```

**Modificare una card esistente:**
```
Modifica la card di "[TITOLO RISORSA]" nell'index.html:
[DESCRIVI COSA CAMBIARE — es. aggiorna la descrizione,
cambia i tag, aggiorna il link, ecc.]
Restituisci solo il blocco HTML modificato (delta).
```

**Mapping DigComp/DigCompEdu per nuova risorsa:**
```
Analizza la risorsa "[TITOLO]" — [BREVE DESCRIZIONE DI COSA FA
E CHI LA USA, studenti/docenti, in che contesto].
Proponi il mapping DigComp 2.2 e DigCompEdu più pertinente,
verificando prima quali competenze sono già coperte da altre
risorse del portale per evitare sovrapposizioni inutili.
```

---

## NOTE OPZIONALI

> Aggiungi qui qualsiasi contesto aggiuntivo utile per questa sessione:
> - Modifiche fatte manualmente ai file dall'ultima sessione
> - Preferenze specifiche per questa risorsa
> - Vincoli particolari (lunghezza descrizione, tag obbligatori, ecc.)
> - Esito dell'ultimo deploy/test se rilevante per il task di oggi
