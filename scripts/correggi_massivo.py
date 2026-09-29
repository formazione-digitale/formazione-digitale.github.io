"""
correggi_massivo.py — Formazione Digitale
Corregge in blocco i problemi ripetuti segnalati da controlla_pagine.py:

  1. shared.css?v=N  → versione unica (la più alta del portale, o --css N)
  2. target="_blank" e rel="noopener/noreferrer" rimossi dai link
  3. barre rovesciate nei percorsi (img\\file.webp → img/file.webp)
  4. <script src="/scripts/ui.js"> incluso più volte → resta solo il primo

Uso (dalla root o da /scripts/):
    python scripts\\correggi_massivo.py              # PROVA: mostra cosa cambierebbe, non scrive nulla
    python scripts\\correggi_massivo.py --applica    # applica le modifiche
    python scripts\\correggi_massivo.py --percorso sicurezza --applica
    python scripts\\correggi_massivo.py --css 5 --applica

Idempotente: rilanciandolo dopo --applica non trova più nulla da cambiare.
Fai un commit PRIMA di --applica, così con git puoi vedere o annullare tutto.
"""

import argparse
import re
from pathlib import Path

from controlla_pagine import trova_pagine, versione_css_portale

RE_CSS = re.compile(r"(shared\.css\?v=)(\d+)")
RE_TAG_A = re.compile(r"<a\b[^>]*>", re.IGNORECASE | re.S)
RE_BLANK = re.compile(r"\s+target\s*=\s*([\"'])_blank\1", re.IGNORECASE)
RE_REL = re.compile(r"(\s+rel\s*=\s*)([\"'])([^\"']*)\2", re.IGNORECASE)
RE_SRC_HREF = re.compile(r"(\s(?:src|href)\s*=\s*)([\"'])([^\"']*\\[^\"']*)\2", re.IGNORECASE)
RE_IMG_JS = re.compile(r"(['\"])img\\(?=[\w.-])")
RE_UI = re.compile(r"[ \t]*<script\s+src=[\"']/scripts/ui\.js[\"'][^>]*>\s*</script>[ \t]*\r?\n?", re.IGNORECASE)


def correggi_css(testo, versione):
    """Allinea shared.css?v=N alla versione indicata."""
    n = 0

    def sost(m):
        nonlocal n
        if int(m.group(2)) == versione:
            return m.group(0)
        n += 1
        return f"{m.group(1)}{versione}"
    return RE_CSS.sub(sost, testo), n


def pulisci_rel(tag):
    """Toglie noopener/noreferrer da rel; se rel resta vuoto lo elimina."""
    def sost(m):
        valori = [v for v in m.group(3).split() if v.lower() not in ("noopener", "noreferrer")]
        return f"{m.group(1)}{m.group(2)}{' '.join(valori)}{m.group(2)}" if valori else ""
    return RE_REL.sub(sost, tag)


def correggi_blank(testo):
    """Rimuove target="_blank" (e i rel collegati) dai tag <a>."""
    n = 0

    def sost(m):
        nonlocal n
        tag = m.group(0)
        if not RE_BLANK.search(tag):
            return tag
        n += 1
        return pulisci_rel(RE_BLANK.sub("", tag))
    return RE_TAG_A.sub(sost, testo), n


def correggi_barre(testo):
    """Barre rovesciate → barre nei src/href locali e nei percorsi 'img\\…' dentro gli attributi JS."""
    n = 0

    def sost(m):
        nonlocal n
        if re.match(r"^(https?:|mailto:|data:)", m.group(3)):
            return m.group(0)
        n += 1
        return f"{m.group(1)}{m.group(2)}{m.group(3).replace(chr(92), '/')}{m.group(2)}"
    testo = RE_SRC_HREF.sub(sost, testo)
    testo, n_js = RE_IMG_JS.subn(r"\1img/", testo)
    return testo, n + n_js


def correggi_ui_doppio(testo):
    """Se ui.js è incluso più volte, lascia solo la prima inclusione."""
    trovati = list(RE_UI.finditer(testo))
    if len(trovati) < 2:
        return testo, 0
    for m in reversed(trovati[1:]):
        testo = testo[:m.start()] + testo[m.end():]
    return testo, len(trovati) - 1


def correggi_file(f, versione):
    """Applica tutte le correzioni a un file; restituisce (nuovo testo, conteggi)."""
    with open(f, encoding="utf-8", newline="") as fh:   # newline="" conserva i CRLF
        testo = fh.read()
    conteggi = {}
    testo, conteggi["css"] = correggi_css(testo, versione) if versione else (testo, 0)
    testo, conteggi["_blank"] = correggi_blank(testo)
    testo, conteggi["barre"] = correggi_barre(testo)
    testo, conteggi["ui.js doppio"] = correggi_ui_doppio(testo)
    return testo, conteggi


def main():
    parser = argparse.ArgumentParser(description="Correzioni in blocco per Formazione Digitale.")
    parser.add_argument("--applica", action="store_true", help="scrive le modifiche (senza: solo prova)")
    parser.add_argument("--percorso", help="solo questa sottocartella")
    parser.add_argument("--css", type=int, help="versione di shared.css da usare (default: la più alta)")
    args = parser.parse_args()

    qui = Path(__file__).resolve().parent
    root = qui.parent if qui.name == "scripts" else qui
    pagine = trova_pagine(root, args.percorso)
    versione = args.css or versione_css_portale(trova_pagine(root))
    print(f"{'APPLICAZIONE' if args.applica else 'PROVA (nessun file modificato)'} · shared.css → v={versione}\n")

    totale, file_mod = {}, 0
    for f in pagine:
        nuovo, conteggi = correggi_file(f, versione)
        if not any(conteggi.values()):
            continue
        file_mod += 1
        dettaglio = ", ".join(f"{k}: {v}" for k, v in conteggi.items() if v)
        print(f"  {f.relative_to(root).as_posix():60} {dettaglio}")
        for k, v in conteggi.items():
            totale[k] = totale.get(k, 0) + v
        if args.applica:
            with open(f, "w", encoding="utf-8", newline="") as fh:
                fh.write(nuovo)

    riepilogo = ", ".join(f"{k}: {v}" for k, v in totale.items() if v) or "niente da correggere"
    print(f"\n{'─' * 50}\nFile {'modificati' if args.applica else 'da modificare'}: {file_mod} · {riepilogo}")
    if not args.applica and file_mod:
        print("Per applicare: aggiungi --applica (consigliato: fai prima un commit).")


if __name__ == "__main__":
    main()
