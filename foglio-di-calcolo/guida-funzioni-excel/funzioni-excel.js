/* ════════════════════════════════════════════════════════════════
   FORMAZIONE DIGITALE — funzioni-excel.js
   ════════════════════════════════════════════════════════════════ */

"use strict";

/* ──────────────────────────────────────────────────────────────
   DATASET CONDIVISI
   ────────────────────────────────────────────────────────────── */

/* Tabella "Vendite" — righe MESCOLATE (non ordinate per venditore):
   R·B·R·V·N·R·N·B·R·V·N·B·V  — le funzioni condizionali devono
   "pescare" righe non adiacenti per mostrare la loro utilità. */
const DATI_VENDITE = [
  { venditore: "Rossi",   regione: "Lombardia", settore: "Informatica", fatturato: 10160 },
  { venditore: "Bianchi", regione: "Veneto",    settore: "Cancelleria", fatturato: 1200 },
  { venditore: "Rossi",   regione: "Veneto",    settore: "Cancelleria", fatturato: 840 },
  { venditore: "Verdi",   regione: "Emilia",    settore: "Informatica", fatturato: 4800 },
  { venditore: "Neri",    regione: "Veneto",    settore: "Informatica", fatturato: 280 },
  { venditore: "Rossi",   regione: "Lombardia", settore: "Cancelleria", fatturato: 3400 },
  { venditore: "Neri",    regione: "Lombardia", settore: "Cancelleria", fatturato: 7500 },
  { venditore: "Bianchi", regione: "Lombardia", settore: "Cancelleria", fatturato: 2240 },
  { venditore: "Rossi",   regione: "Emilia",    settore: "Informatica", fatturato: 6200 },
  { venditore: "Verdi",   regione: "Veneto",    settore: "Cancelleria", fatturato: 1650 },
  { venditore: "Neri",    regione: "Friuli",    settore: "Informatica", fatturato: 580 },
  { venditore: "Bianchi", regione: "Lombardia", settore: "Informatica", fatturato: 1650 },
  { venditore: "Verdi",   regione: "Friuli",    settore: "Cancelleria", fatturato: 302 }
];

/* Anagrafica prodotti — codici alfanumerici ORDINATI (requisito VERO). */
const DATI_PRODOTTI = [
  { codice: "C101", categoria: "Cancelleria", prodotto: "Risme carta A4",   prezzo: 4.50 },
  { codice: "C102", categoria: "Cancelleria", prodotto: "Penne (conf. 50)", prezzo: 8.90 },
  { codice: "C103", categoria: "Cancelleria", prodotto: "Raccoglitori",     prezzo: 3.20 },
  { codice: "C104", categoria: "Cancelleria", prodotto: "Toner laser",      prezzo: 62.00 },
  { codice: "I201", categoria: "Informatica", prodotto: "Mouse ottico",     prezzo: 12.50 },
  { codice: "I202", categoria: "Informatica", prodotto: "Tastiera USB",     prezzo: 24.90 },
  { codice: "I203", categoria: "Informatica", prodotto: "Monitor 24\"",     prezzo: 149.00 },
  { codice: "I204", categoria: "Informatica", prodotto: "Stampante laser",  prezzo: 89.00 },
  { codice: "I205", categoria: "Informatica", prodotto: "Notebook 15\"",    prezzo: 540.00 }
];

/* Esempi per TESTO.FORMULA. */
const DATI_FORMULE = [
  { cella: "F2", mostra: "20.600,00 \u20ac", formula: '=SOMMA.SE(A:A;"Rossi";D:D)' },
  { cella: "F3", mostra: "3",                formula: '=CONTA.SE(A:A;"Verdi")' },
  { cella: "F4", mostra: "Premio",           formula: '=SE(D2>=1000;"Premio";"Standard")' },
  { cella: "F5", mostra: "1",                formula: '=RANGO(B2;$B$2:$B$5;0)' }
];

/* Tre codici identici per formato — usati dalla mini-tabella di STRINGA.ESTRAI.
   Tutti hanno 15 caratteri; inizio=5 / num=2 estrae la sigla regione (pos 5-6). */
const CODICI_ESEMPIO = [
  "AFM-VE-2024-017",
  "ITC-LO-2023-045",
  "RIM-BO-2022-088"
];
const CODICE_ESEMPIO = CODICI_ESEMPIO[0]; /* usato dalla formula-box */

const EURO = new Intl.NumberFormat("it-IT", { style: "currency", currency: "EUR" });


/* ──────────────────────────────────────────────────────────────
   UTILITÀ CONDIVISE
   ────────────────────────────────────────────────────────────── */

function valoriUnici(dati, campo) {
  return [...new Set(dati.map(r => r[campo]))];
}

function renderTabellaVendite(tbodyId) {
  const tbody = document.getElementById(tbodyId);
  if (!tbody) return;
  tbody.innerHTML = DATI_VENDITE.map((r, i) => `
    <tr>
      <th class="cella-rownum">${i + 2}</th>
      <td>${r.venditore}</td>
      <td>${r.regione}</td>
      <td>${r.settore}</td>
      <td class="cella-num">${EURO.format(r.fatturato)}</td>
    </tr>`).join("");
}

function evidenziaRighe(tbodyId, corrisponde) {
  document.querySelectorAll(`#${tbodyId} tr`).forEach((tr, i) => {
    tr.classList.toggle("riga-match", corrisponde(DATI_VENDITE[i]));
  });
}

function popolaSelect(selectId, valori) {
  const sel = document.getElementById(selectId);
  if (!sel) return null;
  valori.forEach(v => {
    const opt = document.createElement("option");
    opt.value = v; opt.textContent = v; sel.appendChild(opt);
  });
  return sel;
}

function etichettaRighe(n) {
  return n + (n === 1 ? " riga" : " righe");
}


/* ──────────────────────────────────────────────────────────────
   WIDGET 1 — SOMMA.SE
   ────────────────────────────────────────────────────────────── */

function sommaSe(dati, vend) {
  return dati.filter(r => r.venditore === vend).reduce((t, r) => t + r.fatturato, 0);
}

function aggiornaSommaSe(vend) {
  evidenziaRighe("ss-tabella-body", r => r.venditore === vend);
  document.getElementById("ss-formula").innerHTML =
    '=SOMMA.SE(<span class="arg-int">A:A</span>;<span class="arg-crit">"' + vend + '"</span>;<span class="arg-somma">D:D</span>)';
  document.getElementById("ss-risultato").textContent = EURO.format(sommaSe(DATI_VENDITE, vend));
}

function initSommaSe() {
  const sel = popolaSelect("ss-criterio", valoriUnici(DATI_VENDITE, "venditore"));
  if (!sel) return;
  sel.addEventListener("change", e => aggiornaSommaSe(e.target.value));
  aggiornaSommaSe(sel.value);
}


/* ──────────────────────────────────────────────────────────────
   WIDGET 2 — SOMMA.PIÙ.SE
   ────────────────────────────────────────────────────────────── */

function sommaPiuSe(dati, vend, reg) {
  return dati.filter(r => r.venditore === vend && r.regione === reg)
             .reduce((t, r) => t + r.fatturato, 0);
}

function aggiornaSommaPiuSe(vend, reg) {
  evidenziaRighe("sps-tabella-body", r => r.venditore === vend && r.regione === reg);
  document.getElementById("sps-formula").innerHTML =
    '=SOMMA.PIÙ.SE(<span class="arg-somma">D:D</span>;' +
    '<span class="arg-int">A:A</span>;<span class="arg-crit">"' + vend + '"</span>;' +
    '<span class="arg-int">B:B</span>;<span class="arg-crit">"' + reg + '"</span>)';
  document.getElementById("sps-risultato").textContent = EURO.format(sommaPiuSe(DATI_VENDITE, vend, reg));
}

function initSommaPiuSe() {
  const v = popolaSelect("sps-venditore", valoriUnici(DATI_VENDITE, "venditore"));
  const r = popolaSelect("sps-regione", valoriUnici(DATI_VENDITE, "regione"));
  if (!v || !r) return;
  const agg = () => aggiornaSommaPiuSe(v.value, r.value);
  v.addEventListener("change", agg); r.addEventListener("change", agg); agg();
}


/* ──────────────────────────────────────────────────────────────
   WIDGET 3 — CONTA.SE
   ────────────────────────────────────────────────────────────── */

function contaSe(dati, vend) {
  return dati.filter(r => r.venditore === vend).length;
}

function aggiornaContaSe(vend) {
  evidenziaRighe("cs-tabella-body", r => r.venditore === vend);
  document.getElementById("cs-formula").innerHTML =
    '=CONTA.SE(<span class="arg-int">A:A</span>;<span class="arg-crit">"' + vend + '"</span>)';
  document.getElementById("cs-risultato").textContent = etichettaRighe(contaSe(DATI_VENDITE, vend));
}

function initContaSe() {
  const sel = popolaSelect("cs-criterio", valoriUnici(DATI_VENDITE, "venditore"));
  if (!sel) return;
  sel.addEventListener("change", e => aggiornaContaSe(e.target.value));
  aggiornaContaSe(sel.value);
}


/* ──────────────────────────────────────────────────────────────
   WIDGET 4 — CONTA.PIÙ.SE
   ────────────────────────────────────────────────────────────── */

function contaPiuSe(dati, vend, reg) {
  return dati.filter(r => r.venditore === vend && r.regione === reg).length;
}

function aggiornaContaPiuSe(vend, reg) {
  evidenziaRighe("cps-tabella-body", r => r.venditore === vend && r.regione === reg);
  document.getElementById("cps-formula").innerHTML =
    '=CONTA.PIÙ.SE(<span class="arg-int">A:A</span>;<span class="arg-crit">"' + vend + '"</span>;' +
    '<span class="arg-int">B:B</span>;<span class="arg-crit">"' + reg + '"</span>)';
  document.getElementById("cps-risultato").textContent = etichettaRighe(contaPiuSe(DATI_VENDITE, vend, reg));
}

function initContaPiuSe() {
  const v = popolaSelect("cps-venditore", valoriUnici(DATI_VENDITE, "venditore"));
  const r = popolaSelect("cps-regione", valoriUnici(DATI_VENDITE, "regione"));
  if (!v || !r) return;
  const agg = () => aggiornaContaPiuSe(v.value, r.value);
  v.addEventListener("change", agg); r.addEventListener("change", agg); agg();
}


/* ──────────────────────────────────────────────────────────────
   WIDGET 5 — CERCA.VERT
   ────────────────────────────────────────────────────────────── */

function campoProdotto(indice) {
  return { 2: "categoria", 3: "prodotto", 4: "prezzo" }[indice];
}

function trovaProdotto(prodotti, valore, esatta) {
  if (esatta) return prodotti.find(p => p.codice === valore) || null;
  let trovato = null;
  prodotti.forEach(p => { if (p.codice <= valore) trovato = p; });
  return trovato;
}

function cercaVert(prodotti, valore, indice, esatta) {
  const p = trovaProdotto(prodotti, valore, esatta);
  return p ? p[campoProdotto(indice)] : "#N/D";
}

function renderTabellaProdotti(tbodyId) {
  const tbody = document.getElementById(tbodyId);
  if (!tbody) return;
  tbody.innerHTML = DATI_PRODOTTI.map((p, i) => `
    <tr>
      <th class="cella-rownum">${i + 2}</th>
      <td>${p.codice}</td>
      <td>${p.categoria}</td>
      <td>${p.prodotto}</td>
      <td class="cella-num">${EURO.format(p.prezzo)}</td>
    </tr>`).join("");
}

function aggiornaCercaVert(valore, indice, esatta) {
  const p = trovaProdotto(DATI_PRODOTTI, valore, esatta);
  document.querySelectorAll("#cv-tabella-body tr").forEach((tr, i) => {
    const match = p && DATI_PRODOTTI[i] === p;
    tr.classList.toggle("riga-match", match);
    tr.querySelectorAll("td").forEach((td, c) => {
      td.classList.toggle("cella-result", match && c === indice - 1);
    });
  });
  document.getElementById("cv-formula").innerHTML =
    '=CERCA.VERT(<span class="arg-crit">"' + valore + '"</span>;' +
    '<span class="arg-int">A:D</span>;<span class="arg-somma">' + indice + '</span>;' +
    (esatta ? "FALSO" : "VERO") + ')';
  const ris = cercaVert(DATI_PRODOTTI, valore, indice, esatta);
  document.getElementById("cv-risultato").textContent =
    ris === "#N/D" ? "#N/D" : (indice === 4 ? EURO.format(ris) : ris);
}

function initCercaVert() {
  const sel = document.getElementById("cv-valore");
  const ind = document.getElementById("cv-indice");
  const esa = document.getElementById("cv-esatta");
  if (!sel || !ind || !esa) return;
  [...DATI_PRODOTTI.map(p => p.codice), "I210"].forEach(c => {
    const opt = document.createElement("option");
    opt.value = c;
    opt.textContent = c === "I210" ? "I210 (codice inesistente)" : c;
    sel.appendChild(opt);
  });
  const agg = () => aggiornaCercaVert(sel.value, +ind.value, esa.checked);
  sel.addEventListener("change", agg);
  ind.addEventListener("change", agg);
  esa.addEventListener("change", agg);
  agg();
}


/* ──────────────────────────────────────────────────────────────
   WIDGET 6 — SE
   ────────────────────────────────────────────────────────────── */

function renderTabellaSe(tbodyId, soglia) {
  const tbody = document.getElementById(tbodyId);
  if (!tbody) return;
  tbody.innerHTML = DATI_VENDITE.map((r, i) => {
    const premio = r.fatturato >= soglia;
    return `<tr class="${premio ? "riga-match" : ""}">
      <th class="cella-rownum">${i + 2}</th>
      <td>${r.venditore}</td>
      <td>${r.regione}</td>
      <td>${r.settore}</td>
      <td class="cella-num">${EURO.format(r.fatturato)}</td>
      <td class="cella-esito ${premio ? "esito-si" : "esito-no"}">${premio ? "Premio" : "Standard"}</td>
    </tr>`;
  }).join("");
}

function aggiornaSe(soglia) {
  renderTabellaSe("se-tabella-body", soglia);
  document.getElementById("se-soglia-val").textContent = EURO.format(soglia);
  document.getElementById("se-formula").innerHTML =
    '=SE(<span class="arg-int">D2&gt;=' + soglia + '</span>;' +
    '<span class="arg-somma">"Premio"</span>;<span class="arg-crit">"Standard"</span>)';
  const n = DATI_VENDITE.filter(r => r.fatturato >= soglia).length;
  document.getElementById("se-conteggio").textContent = etichettaRighe(n) + " con \u00abPremio\u00bb";
}

function initSe() {
  const slider = document.getElementById("se-soglia");
  if (!slider) return;
  slider.addEventListener("input", e => aggiornaSe(+e.target.value));
  aggiornaSe(+slider.value);
}


/* ──────────────────────────────────────────────────────────────
   WIDGET 7 — SE annidata (traccia sequenziale · esempio voti)
   ────────────────────────────────────────────────────────────── */

/* Valuta il voto con due condizioni nidificate:
   =10 → Con lode   >6 → Promosso   altrimenti Bocciato. */
function valutaVoto(voto) {
  if (voto === 10) return "Con lode";
  if (voto > 6)   return "Promosso";
  return "Bocciato";
}

function setBadgeCond(id, stato) {
  const el = document.getElementById(id);
  if (stato === "neutro") { el.textContent = "\u2014"; el.className = "cond-badge cond-neutro"; return; }
  el.textContent = stato ? "VERO" : "FALSO";
  el.className = "cond-badge " + (stato ? "cond-vero" : "cond-falso");
}

function setStep(stepId, esitoId, stato, testo) {
  document.getElementById(stepId).className = "traccia-step step-" + stato;
  document.getElementById(esitoId).textContent = "\u2192 " + testo;
}

/* Mappa risultato → classe CSS del badge finale. */
const CLASSI_ESITO_VOTO = {
  "Con lode":  "fascia-conlode",
  "Promosso":  "fascia-promosso",
  "Bocciato":  "fascia-bocciato"
};

function aggiornaSeAnnidata(voto) {
  const c1 = (voto === 10);
  const c2 = (voto > 6);
  const ris = valutaVoto(voto);

  setBadgeCond("sea-cond1", c1);
  setStep("sea-step1", "sea-esito1", c1 ? "vince" : "falso",
          c1 ? "\u2713 risultato: \u00abCon lode\u00bb"
             : "no, scendo al controllo successivo");

  if (c1) {
    setBadgeCond("sea-cond2", "neutro");
    setStep("sea-step2", "sea-esito2", "spento", "non valutato (la 1\u00aa condizione ha gi\u00e0 vinto)");
  } else {
    setBadgeCond("sea-cond2", c2);
    setStep("sea-step2", "sea-esito2", c2 ? "vince" : "falso",
            c2 ? "\u2713 risultato: \u00abPromosso\u00bb"
               : "no \u2192 \u00abBocciato\u00bb");
  }

  const badge = document.getElementById("sea-risultato");
  badge.textContent = "\u00ab " + ris + " \u00bb";
  badge.className = "traccia-badge " + CLASSI_ESITO_VOTO[ris];

  document.getElementById("sea-valore-val").textContent = voto + " / 10";
  document.getElementById("sea-formula").innerHTML =
    '=SE(<span class="arg-int">B2=10</span>;<span class="arg-somma">"Con lode"</span>;' +
    'SE(<span class="arg-int">B2&gt;6</span>;<span class="arg-somma">"Promosso"</span>;<span class="arg-crit">"Bocciato"</span>))';
}

function initSeAnnidata() {
  const slider = document.getElementById("sea-valore");
  if (!slider) return;
  slider.addEventListener("input", e => aggiornaSeAnnidata(+e.target.value));
  aggiornaSeAnnidata(+slider.value);
}


/* ──────────────────────────────────────────────────────────────
   WIDGET 8 — RANGO
   ────────────────────────────────────────────────────────────── */

function totaliPerVenditore(dati) {
  return valoriUnici(dati, "venditore").map(v => ({ venditore: v, totale: sommaSe(dati, v) }));
}

function rango(valore, valori, ordine) {
  return ordine === 0
    ? valori.filter(x => x > valore).length + 1
    : valori.filter(x => x < valore).length + 1;
}

function aggiornaRango(ordine) {
  const tot = totaliPerVenditore(DATI_VENDITE);
  const valori = tot.map(t => t.totale);
  document.getElementById("rg-tabella-body").innerHTML = tot.map((t, i) => {
    const pos = rango(t.totale, valori, ordine);
    return `<tr class="${pos === 1 ? "riga-match" : ""}">
      <th class="cella-rownum">${i + 2}</th>
      <td>${t.venditore}</td>
      <td class="cella-num">${EURO.format(t.totale)}</td>
      <td class="cella-num">${pos}</td>
    </tr>`;
  }).join("");
  document.getElementById("rg-formula").innerHTML =
    '=RANGO(<span class="arg-crit">B2</span>;<span class="arg-int">$B$2:$B$5</span>;<span class="arg-somma">' + ordine + '</span>)';
}

function initRango() {
  const sel = document.getElementById("rg-ordine");
  if (!sel) return;
  sel.addEventListener("change", e => aggiornaRango(+e.target.value));
  aggiornaRango(+sel.value);
}


/* ──────────────────────────────────────────────────────────────
   WIDGET 9 — STRINGA.ESTRAI
   ────────────────────────────────────────────────────────────── */

function stringaEstrai(testo, inizio, num) {
  return testo.slice(inizio - 1, inizio - 1 + num);
}

function renderCaratteri(contId, testo) {
  const cont = document.getElementById(contId);
  if (!cont) return;
  cont.innerHTML = [...testo].map((ch, i) => `
    <div class="carattere">
      <div class="car-ch">${ch}</div>
      <div class="car-pos">${i + 1}</div>
    </div>`).join("");
}

/* Disegna la mini-tabella contesto: col A = codici digitati,
   col B = risultato STRINGA.ESTRAI (celle "formula", badge fx). */
function renderTabellaSt(tbodyId, inizio, num) {
  const tbody = document.getElementById(tbodyId);
  if (!tbody) return;
  tbody.innerHTML = CODICI_ESEMPIO.map((cod, i) => {
    const ris = stringaEstrai(cod, inizio, num);
    return `<tr class="${i === 0 ? "riga-match" : ""}">
      <th class="cella-rownum">${i + 2}</th>
      <td>${cod}</td>
      <td class="cella-fx"><span class="fx-badge">fx</span>&nbsp;${ris}</td>
    </tr>`;
  }).join("");
}

function aggiornaStringaEstrai(inizio, num) {
  renderTabellaSt("st-tabella-body", inizio, num);
  document.querySelectorAll("#st-caratteri .carattere").forEach((el, i) => {
    const pos = i + 1;
    el.classList.toggle("car-attivo", pos >= inizio && pos < inizio + num);
  });
  document.getElementById("st-inizio-val").textContent = inizio;
  document.getElementById("st-num-val").textContent = num;
  document.getElementById("st-formula").innerHTML =
    '=STRINGA.ESTRAI(<span class="arg-int">"' + CODICE_ESEMPIO + '"</span>;' +
    '<span class="arg-crit">' + inizio + '</span>;<span class="arg-somma">' + num + '</span>)';
  document.getElementById("st-risultato").textContent =
    '"' + stringaEstrai(CODICE_ESEMPIO, inizio, num) + '"';
}

function initStringaEstrai() {
  renderCaratteri("st-caratteri", CODICE_ESEMPIO);
  const ini = document.getElementById("st-inizio");
  const num = document.getElementById("st-num");
  if (!ini || !num) return;
  const len = CODICE_ESEMPIO.length;
  ini.max = len; num.max = len;
  const agg = () => {
    let i = Math.max(1, Math.min(+ini.value, len));
    let n = Math.max(1, Math.min(+num.value, len - i + 1));
    ini.value = i; num.value = n;
    aggiornaStringaEstrai(i, n);
  };
  ini.addEventListener("input", agg);
  num.addEventListener("input", agg);
  agg();
}


/* ──────────────────────────────────────────────────────────────
   WIDGET 10 — TESTO.FORMULA
   ────────────────────────────────────────────────────────────── */

function escHtml(s) {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function renderTabellaFormule(tbodyId) {
  const tbody = document.getElementById(tbodyId);
  if (!tbody) return;
  tbody.innerHTML = DATI_FORMULE.map(f => `
    <tr><td class="cella-num">${f.cella}</td><td class="cella-fx"><span class="fx-badge">fx</span>&nbsp;${f.mostra}</td></tr>`).join("");
}

function aggiornaTestoFormula(cella) {
  const f = DATI_FORMULE.find(x => x.cella === cella);
  document.querySelectorAll("#tf-tabella-body tr").forEach((tr, i) => {
    tr.classList.toggle("riga-match", DATI_FORMULE[i].cella === cella);
  });
  document.getElementById("tf-formula").innerHTML =
    '=TESTO.FORMULA(<span class="arg-int">' + cella + '</span>)';
  document.getElementById("tf-risultato").innerHTML =
    '<code class="fx">' + escHtml(f.formula) + '</code>';
}

function initTestoFormula() {
  const sel = popolaSelect("tf-cella", DATI_FORMULE.map(f => f.cella));
  if (!sel) return;
  sel.addEventListener("change", e => aggiornaTestoFormula(e.target.value));
  aggiornaTestoFormula(sel.value);
}


/* ──────────────────────────────────────────────────────────────
   AVVIO
   ────────────────────────────────────────────────────────────── */
document.addEventListener("DOMContentLoaded", () => {
  ["ss-tabella-body", "sps-tabella-body", "cs-tabella-body", "cps-tabella-body"]
    .forEach(renderTabellaVendite);
  renderTabellaProdotti("cv-tabella-body");
  renderTabellaFormule("tf-tabella-body");
  initSommaSe();
  initSommaPiuSe();
  initContaSe();
  initContaPiuSe();
  initCercaVert();
  initSe();
  initSeAnnidata();
  initRango();
  initStringaEstrai();
  initTestoFormula();
});
