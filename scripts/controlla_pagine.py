"""
controlla_pagine.py — Formazione Digitale  (v1.1)
Controllo di qualità delle pagine HTML del portale, da lanciare PRIMA del commit
(insieme a genera_sitemap.py). Non modifica nessun file: stampa solo un report.

Uso (dalla cartella /scripts/ oppure dalla root):
    python controlla_pagine.py                  # controlla tutto il portale
    python controlla_pagine.py --solo-errori    # mostra solo gli errori
    python controlla_pagine.py --percorso informatica-base   # solo una sottocartella
    python controlla_pagine.py --md report.md   # salva anche il report in Markdown

Codice di uscita: 0 = nessun errore, 1 = almeno un errore (utile in CI).
Solo libreria standard Python: nessuna dipendenza.
"""

import argparse
import json
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

# ─────────────────────────────────────────────
# CONFIGURAZIONE — modifica qui
# ─────────────────────────────────────────────

DOMINIO = "https://formazione-digitale.it"

# Cartelle da non esplorare (nome esatto, qualsiasi livello)
CARTELLE_ESCLUSE = {".git", "node_modules", "scripts", "docs", "data-src", ".github", ".vercel"}

# File da ignorare: copie di lavoro e backup
FILE_ESCLUSI_REGEX = re.compile(r"(_old|-old|_bak|\.bak|index-\.html$)", re.IGNORECASE)

# Pagine che non devono stare nel manifest (root, pagine legali, mappe, 404)
PAGINE_FUORI_MANIFEST = {
    "/", "/404.html", "/cookie-policy.html", "/privacy-policy.html",
    "/mappa-aree.html", "/mappa-framework.html", "/mappa-risorse.html", "/sistemi_index.html",
    "/stats/",
}

# Pagine di servizio: og:url non richiesto
PAGINE_SERVIZIO = PAGINE_FUORI_MANIFEST - {"/"}

# Pagine senza canonical (non devono essere indicizzate)
PAGINE_SENZA_CANONICAL = {"/404.html"}

# Versione attesa di shared.css (None = usa la più alta trovata nel portale)
VERSIONE_CSS_ATTESA = None

# Tag di cui si controlla l'apertura/chiusura
TAG_BILANCIATI = {"div", "section", "main", "article", "aside", "nav", "header", "footer",
                  "ul", "ol", "table", "a", "button", "form", "details"}

TAG_VUOTI = {"meta", "link", "br", "hr", "img", "input", "source", "area", "base",
             "col", "embed", "param", "track", "wbr"}

# ─────────────────────────────────────────────
# LOGICA — non modificare sotto questa riga
# ─────────────────────────────────────────────

ERRORE, AVVISO = "ERRORE", "AVVISO"


class AnalizzatoreHTML(HTMLParser):
    """Raccoglie in un solo passaggio: tag aperti/chiusi, id, link, meta utili."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.pila, self.sbilanci = [], []
        self.ids = Counter()
        self.ancore, self.risorse = [], []
        self.canonical = self.og_url = None
        self.script_src, self.css_href = [], []
        self.back_to_top_altro = False
        self.blank = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        riga = self.getpos()[0]
        self._raccogli_attributi(tag, a, riga)
        if tag in TAG_BILANCIATI:
            self.pila.append((tag, riga))

    def handle_startendtag(self, tag, attrs):
        self._raccogli_attributi(tag, dict(attrs), self.getpos()[0])

    def handle_endtag(self, tag):
        if tag not in TAG_BILANCIATI:
            return
        riga = self.getpos()[0]
        if self.pila and self.pila[-1][0] == tag:
            self.pila.pop()
            return
        aperti = [t for t, _ in self.pila]
        if tag in aperti:
            i = len(aperti) - 1 - aperti[::-1].index(tag)
            lasciati = ", ".join(f"<{t}> riga {r}" for t, r in self.pila[i + 1:])
            self.sbilanci.append(f"riga {riga}: </{tag}> chiude lasciando aperti {lasciati}")
            del self.pila[i:]
        else:
            self.sbilanci.append(f"riga {riga}: </{tag}> senza apertura corrispondente")

    def _raccogli_attributi(self, tag, a, riga):
        """Estrae dagli attributi tutto ciò che serve ai controlli."""
        if a.get("id"):
            self.ids[a["id"]] += 1
        if a.get("target") == "_blank":
            self.blank += 1
        # ui.js (con la guardia) non inietta il suo pulsante se esiste già #back-to-top:
        # resta un doppione solo se la pagina usa un id diverso (es. #back-top)
        classi = (a.get("class") or "").split()
        if a.get("id") == "back-top" or ("back-to-top" in classi and a.get("id") != "back-to-top"):
            self.back_to_top_altro = True
        if tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href")
        if tag == "link" and "stylesheet" in (a.get("rel") or ""):
            self.css_href.append(a.get("href") or "")
        if tag == "meta" and a.get("property") == "og:url":
            self.og_url = a.get("content")
        if tag == "script" and a.get("src"):
            self.script_src.append(a["src"])
        for attr in ("href", "src"):
            valore = a.get(attr)
            if valore:
                (self.ancore if valore.startswith("#") else self.risorse).append((valore, riga, tag))


def url_pagina(file_html, root):
    """URL pubblico atteso della pagina (pretty URL con slash finale)."""
    rel = file_html.relative_to(root).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def trova_pagine(root, sottocartella=None):
    """Elenco dei file HTML da controllare, escluse cartelle e copie di backup."""
    base = root / sottocartella if sottocartella else root
    pagine = []
    for f in sorted(base.rglob("*.html")):
        parti = f.relative_to(root).parts
        if any(p in CARTELLE_ESCLUSE for p in parti[:-1]):
            continue
        if FILE_ESCLUSI_REGEX.search(f.name):
            continue
        pagine.append(f)
    return pagine


def carica_manifest(root):
    """Restituisce (percorsi delle risorse, percorsi degli hub) dal manifest.json."""
    file_m = root / "manifest.json"
    if not file_m.exists():
        return None, set()
    dati = json.loads(file_m.read_text(encoding="utf-8"))
    percorsi = {r["path"]: r for r in dati if "path" in r}
    hub = {r["hub"] for r in dati if r.get("hub")}
    return percorsi, hub


def versione_css(href):
    """Estrae il numero di versione da 'shared.css?v=N' (None se assente)."""
    m = re.search(r"shared\.css\?v=(\d+)", href)
    return int(m.group(1)) if m else None


# ── CONTROLLI SUL SINGOLO FILE ───────────────────────────────
# Ogni funzione riceve i dati della pagina e restituisce una lista di (livello, messaggio).

def controlla_seo(url, an):
    """Canonical e og:url devono puntare all'indirizzo reale della pagina."""
    esiti, atteso = [], DOMINIO + url
    if url in PAGINE_SENZA_CANONICAL:
        return esiti
    if not an.canonical:
        esiti.append((ERRORE, "canonical mancante"))
    elif an.canonical != atteso:
        esiti.append((ERRORE, f"canonical errato: {an.canonical} (atteso {atteso})"))
    if an.og_url and an.og_url != atteso:
        esiti.append((AVVISO, f"og:url errato: {an.og_url} (atteso {atteso})"))
    elif not an.og_url and url not in PAGINE_SERVIZIO:
        esiti.append((AVVISO, "og:url mancante"))
    return esiti


def controlla_script(testo, an):
    """ui.js obbligatorio (una volta), GoatCounter presente, niente pulsante 'torna su' proprio."""
    esiti = []
    n_ui = sum(1 for s in an.script_src if s.endswith("/ui.js"))
    if n_ui == 0:
        esiti.append((ERRORE, "manca <script src=\"/scripts/ui.js\" defer>"))
    elif n_ui > 1:
        esiti.append((AVVISO, f"ui.js incluso {n_ui} volte"))
    if "goatcounter" not in testo:
        esiti.append((AVVISO, "GoatCounter assente: le visite non vengono contate"))
    if an.back_to_top_altro and n_ui:
        esiti.append((AVVISO, "pulsante 'torna su' con id diverso da #back-to-top + ui.js: doppio pulsante"))
    return esiti


def controlla_regole(testo, an):
    """Regole assolute del portale: niente _blank, niente github.io, niente 'in arrivo'."""
    esiti = []
    if an.blank:
        esiti.append((ERRORE, f"target=\"_blank\" presente {an.blank} volte (vietato)"))
    if re.search(r"formazione-digitale\.github\.io", testo):
        esiti.append((ERRORE, "URL hardcoded a github.io"))
    visibile = re.sub(r"<script.*?</script>|<!--.*?-->", "", testo, flags=re.S)
    if re.search(r"in arrivo", visibile, re.IGNORECASE):
        esiti.append((AVVISO, "testo 'in arrivo' (usare una formula neutra)"))
    return esiti


def controlla_css(an, versione_attesa):
    """Versione di shared.css allineata e mai insieme a shared-extended.css."""
    esiti = []
    shared = [h for h in an.css_href if "shared.css" in h]
    extended = [h for h in an.css_href if "shared-extended.css" in h]
    if shared and extended:
        esiti.append((ERRORE, "shared.css e shared-extended.css caricati insieme"))
    for h in shared:
        v = versione_css(h)
        if v is None:
            esiti.append((AVVISO, f"shared.css senza versione: {h}"))
        elif versione_attesa and v != versione_attesa:
            esiti.append((AVVISO, f"shared.css?v={v} (attesa v={versione_attesa}): possibile copia vecchia in cache"))
    return esiti


def controlla_struttura(an):
    """Tag bilanciati, id duplicati, ancore interne rotte."""
    esiti = [(ERRORE, "tag non bilanciato — " + s) for s in an.sbilanci[:5]]
    if len(an.sbilanci) > 5:
        esiti.append((ERRORE, f"… altri {len(an.sbilanci) - 5} problemi di tag"))
    for t, r in an.pila:
        esiti.append((ERRORE, f"<{t}> aperto a riga {r} e mai chiuso"))
    for i, n in an.ids.items():
        if n > 1:
            esiti.append((ERRORE, f"id duplicato: '{i}' ({n} volte)"))
    for href, riga, _ in an.ancore:
        if len(href) > 1 and href[1:] not in an.ids:
            esiti.append((AVVISO, f"riga {riga}: ancora {href} senza elemento con quell'id"))
    return esiti


def risolvi_locale(valore, file_html, root):
    """Percorso su disco di un link locale, oppure None se esterno/dinamico."""
    if re.match(r"^(https?:|mailto:|tel:|data:|javascript:|//)", valore) or "${" in valore:
        return None
    pulito = valore.split("#")[0].split("?")[0]
    if not pulito:
        return None
    dest = root / pulito.lstrip("/") if pulito.startswith("/") else file_html.parent / pulito
    return dest / "index.html" if pulito.endswith("/") else dest


def controlla_link(an, file_html, root):
    """Link e immagini locali: esistono? usano la barra giusta?"""
    esiti, visti = [], set()
    for valore, riga, tag in an.risorse:
        if "\\" in valore:
            esiti.append((AVVISO, f"riga {riga}: percorso con barra rovesciata '{valore}' (usare /)"))
            continue
        dest = risolvi_locale(valore, file_html, root)
        if dest is None or valore in visti:
            continue
        visti.add(valore)
        if not dest.exists():
            esiti.append((ERRORE, f"riga {riga}: <{tag}> punta a un file inesistente: {valore}"))
    return esiti


def controlla_manifest(url, manifest, hub):
    """La pagina di una risorsa deve essere registrata nel manifest."""
    if manifest is None or url in PAGINE_FUORI_MANIFEST or url in hub:
        return []
    if url.endswith(".html"):
        return []
    if url not in manifest:
        return [(AVVISO, "pagina assente da manifest.json (non compare in ricerca e statistiche)")]
    return []


# ── ORCHESTRAZIONE ───────────────────────────────────────────

def analizza_file(file_html, root):
    """Legge e analizza una pagina; restituisce (testo, analizzatore) o un errore di lettura."""
    try:
        testo = file_html.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None, None
    an = AnalizzatoreHTML()
    an.feed(testo)
    return testo, an


def controlla_pagina(file_html, root, ctx):
    """Esegue tutti i controlli su una pagina e restituisce la lista degli esiti."""
    testo, an = analizza_file(file_html, root)
    if an is None:
        return [(ERRORE, "file non leggibile in UTF-8")]
    url = url_pagina(file_html, root)
    esiti = []
    esiti += controlla_seo(url, an)
    esiti += controlla_script(testo, an)
    esiti += controlla_regole(testo, an)
    esiti += controlla_css(an, ctx["versione_css"])
    esiti += controlla_struttura(an)
    esiti += controlla_link(an, file_html, root)
    esiti += controlla_manifest(url, ctx["manifest"], ctx["hub"])
    return esiti


def versione_css_portale(pagine):
    """Versione di shared.css da considerare corretta (configurata o la più alta trovata)."""
    if VERSIONE_CSS_ATTESA:
        return VERSIONE_CSS_ATTESA
    trovate = set()
    for f in pagine:
        for v in re.findall(r"shared\.css\?v=(\d+)", f.read_text(encoding="utf-8", errors="ignore")):
            trovate.add(int(v))
    return max(trovate) if trovate else None


def controlla_manifest_inverso(manifest, root):
    """Ogni risorsa attiva del manifest deve avere la sua pagina su disco."""
    esiti = []
    for path, r in (manifest or {}).items():
        if not r.get("active", True):
            continue
        dest = root / path.strip("/") / "index.html" if path.endswith("/") else root / path.lstrip("/")
        if not dest.exists():
            esiti.append((ERRORE, f"manifest: {path} è attiva ma la pagina non esiste"))
    return esiti


# ── REPORT ───────────────────────────────────────────────────

def formatta_report(risultati, globali, solo_errori, markdown=False):
    """Costruisce il testo del report (console o Markdown)."""
    righe, n_err, n_avv = [], 0, 0
    blocchi = ([("manifest.json", globali)] if globali else []) + risultati
    for nome, esiti in blocchi:
        mostrati = [e for e in esiti if not solo_errori or e[0] == ERRORE]
        n_err += sum(1 for l, _ in esiti if l == ERRORE)
        n_avv += sum(1 for l, _ in esiti if l == AVVISO)
        if not mostrati:
            continue
        righe.append(f"\n### {nome}" if markdown else f"\n{nome}")
        for livello, msg in mostrati:
            icona = "❌" if livello == ERRORE else "⚠️ "
            righe.append(f"- {icona} {msg}" if markdown else f"   {icona} {msg}")
    return righe, n_err, n_avv


def main():
    parser = argparse.ArgumentParser(description="Controllo qualità delle pagine di Formazione Digitale.")
    parser.add_argument("--solo-errori", action="store_true", help="mostra solo gli errori")
    parser.add_argument("--percorso", help="controlla solo questa sottocartella (es. informatica-base)")
    parser.add_argument("--md", help="salva il report anche in questo file Markdown")
    args = parser.parse_args()

    # Lo script sta in /scripts/: la root è un livello sopra (funziona anche se lanciato dalla root)
    qui = Path(__file__).resolve().parent
    root = qui.parent if qui.name == "scripts" else qui
    pagine = trova_pagine(root, args.percorso)
    manifest, hub = carica_manifest(root)
    ctx = {"manifest": manifest, "hub": hub, "versione_css": versione_css_portale(pagine)}

    risultati = [(url_pagina(f, root), controlla_pagina(f, root, ctx)) for f in pagine]
    globali = [] if args.percorso else controlla_manifest_inverso(manifest, root)
    if manifest is None:
        globali.append((AVVISO, "manifest.json non trovato: controlli sul manifest saltati"))

    righe, n_err, n_avv = formatta_report(risultati, globali, args.solo_errori)
    print(f"Root: {root}\nPagine controllate: {len(pagine)} · shared.css atteso: v={ctx['versione_css']}")
    print("\n".join(righe) if righe else "\nNessun problema trovato. ✅")
    print(f"\n{'─' * 50}\nTotale: {n_err} errori, {n_avv} avvisi")

    if args.md:
        md, _, _ = formatta_report(risultati, globali, args.solo_errori, markdown=True)
        testa = f"# Report controlla_pagine\n\nPagine: {len(pagine)} · errori: {n_err} · avvisi: {n_avv}\n"
        Path(args.md).write_text(testa + "\n".join(md) + "\n", encoding="utf-8")
        print(f"Report salvato in {args.md}")
    sys.exit(1 if n_err else 0)


if __name__ == "__main__":
    main()
