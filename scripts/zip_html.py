"""
zip_html.py — Formazione Digitale
Crea uno ZIP "leggero" del portale con SOLO le pagine HTML (alberatura compresa)
più i pochi file globali che servono ad analizzarle: manifest, CSS condivisi, ui.js, sw.js.
Serve per mandare a Claude una fotografia aggiornata del sito in un solo file.

Uso (dalla root o da /scripts/):
    python scripts\\zip_html.py           # crea formazione-digitale_html_AAAAMMGG_HHMM.zip nella root
    python scripts\\zip_html.py --prova   # mostra l'elenco dei file, senza creare lo ZIP

Le pagine sono selezionate con la stessa logica di controlla_pagine.py
(stesse cartelle escluse, stesse copie di backup ignorate).
"""

import argparse
import zipfile
from datetime import datetime
from pathlib import Path

from controlla_pagine import trova_pagine

# ─────────────────────────────────────────────
# CONFIGURAZIONE — modifica qui
# ─────────────────────────────────────────────

# File globali da includere oltre alle pagine (percorsi relativi alla root)
FILE_GLOBALI = [
    "manifest.json",
    "css/shared.css",
    "css/shared-extended.css",
    "scripts/ui.js",
    "sw.js",
]

PREFISSO_ZIP = "formazione-digitale_html_"

# ─────────────────────────────────────────────
# LOGICA — non modificare sotto questa riga
# ─────────────────────────────────────────────


def raccogli_file(root):
    """Pagine HTML + file globali esistenti, senza duplicati, in ordine."""
    pagine = trova_pagine(root)
    globali = [root / g for g in FILE_GLOBALI if (root / g).exists()]
    mancanti = [g for g in FILE_GLOBALI if not (root / g).exists()]
    return sorted(set(pagine + globali)), mancanti


def dimensione_leggibile(byte):
    """Converte byte in KB/MB per il riepilogo."""
    return f"{byte / 1024:.0f} KB" if byte < 1024 * 1024 else f"{byte / 1024 / 1024:.2f} MB"


def crea_zip(root, file_list, destinazione):
    """Scrive lo ZIP mantenendo i percorsi relativi alla root."""
    with zipfile.ZipFile(destinazione, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in file_list:
            zf.write(f, f.relative_to(root).as_posix())


def main():
    parser = argparse.ArgumentParser(description="ZIP con le sole pagine HTML del portale.")
    parser.add_argument("--prova", action="store_true", help="mostra l'elenco senza creare lo ZIP")
    args = parser.parse_args()

    qui = Path(__file__).resolve().parent
    root = qui.parent if qui.name == "scripts" else qui
    file_list, mancanti = raccogli_file(root)
    n_html = sum(1 for f in file_list if f.suffix == ".html")
    peso = sum(f.stat().st_size for f in file_list)

    if args.prova:
        for f in file_list:
            print(f"  {f.relative_to(root).as_posix()}")
    for g in mancanti:
        print(f"  (non trovato, saltato: {g})")
    print(f"\nPagine HTML: {n_html} · altri file: {len(file_list) - n_html} · dati: {dimensione_leggibile(peso)}")

    if args.prova:
        print("PROVA: nessuno ZIP creato.")
        return
    nome = PREFISSO_ZIP + datetime.now().strftime("%Y%m%d_%H%M") + ".zip"
    crea_zip(root, file_list, root / nome)
    print(f"✅ Creato {nome} ({dimensione_leggibile((root / nome).stat().st_size)})")


if __name__ == "__main__":
    main()
