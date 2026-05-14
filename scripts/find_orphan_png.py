#!/usr/bin/env python3
"""
find_orphan_png.py — Formazione Digitale
Trova i PNG presenti nelle cartelle img/ ma non referenziati
nell'index.html della stessa cartella.

Usa i CSV di mapping per le cartelle già convertite in WebP,
e scansiona direttamente l'HTML per le cartelle non convertite.

Uso:
    python scripts/find_orphan_png.py           # analisi completa
    python scripts/find_orphan_png.py --delete  # cancella gli orfani (dopo verifica)

Output: lista degli orfani per cartella + report finale.
"""

import os
import re
import csv
import argparse
from pathlib import Path

# ── CONFIGURAZIONE ───────────────────────────────────────────────
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Cartelle da analizzare con il loro CSV di mapping (se disponibile)
CARTELLE = [
    {
        "dir": "elaborazione-testi/guida-word",
        "csv": None,  # nessun CSV — scansiona HTML direttamente
    },
    {
        "dir": "database/guida-libreoffice-base-query",
        "csv": "mapping-query.csv",
    },
    {
        "dir": "networking/hfs-server",
        "csv": "mapping-hfs.csv",
    },
]

# Estensioni immagine da considerare come "usate" (oltre a PNG)
IMG_EXTENSIONS = {".png", ".webp", ".jpg", ".jpeg", ".gif", ".svg"}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Trova PNG orfani non referenziati nell'HTML"
    )
    parser.add_argument(
        "--delete", action="store_true",
        help="Cancella gli orfani trovati (usare con cautela)"
    )
    return parser.parse_args()


def get_referenced_images_from_html(html_path: Path) -> set[str]:
    """
    Estrae tutti i nomi file immagine referenziati nell'HTML
    (src=, href=, url(), content=).
    """
    content = html_path.read_text(encoding="utf-8", errors="ignore")
    pattern = re.compile(
        r'(?:src|href|content|url)\s*[=:(]["\']?([^"\')\s>]+\.(?:png|webp|jpg|jpeg|gif|svg))["\']?',
        re.IGNORECASE
    )
    refs = set()
    for match in pattern.findall(content):
        # Prende solo il nome file, ignora il path
        refs.add(Path(match).name)
    return refs


def get_referenced_from_csv(csv_path: Path) -> set[str]:
    """
    Legge il CSV di mapping e restituisce i nomi file originali
    referenziati (sia PNG originali che WebP generati).
    """
    refs = set()
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            refs.add(Path(row["src_originale"]).name)
            refs.add(Path(row["src_webp"]).name)
    return refs


def main():
    args = parse_args()
    delete = args.delete

    print("═" * 60)
    print("  Formazione Digitale — PNG orfani")
    print("═" * 60)
    print(f"  Modalità: {'CANCELLAZIONE' if delete else 'ANALISI'}")
    print("═" * 60)
    print()

    totale_orfani    = 0
    totale_ok        = 0

    for cfg in CARTELLE:
        dir_path = Path(ROOT) / cfg["dir"]
        img_dir  = dir_path / "img"
        html_path = dir_path / "index.html"

        print(f"📁 {cfg['dir']}")

        if not img_dir.exists():
            print("  ⚠ Cartella img/ non trovata — salto")
            print()
            continue

        if not html_path.exists():
            print("  ⚠ index.html non trovato — salto")
            print()
            continue

        # Tutti i file immagine presenti in img/
        tutti = {f.name for f in img_dir.iterdir() if f.suffix.lower() in IMG_EXTENSIONS}

        # File referenziati
        if cfg["csv"]:
            csv_path = dir_path / cfg["csv"]
            if csv_path.exists():
                refs_csv = get_referenced_from_csv(csv_path)
            else:
                print(f"  ⚠ CSV non trovato: {cfg['csv']} — uso solo HTML")
                refs_csv = set()
            refs_html = get_referenced_images_from_html(html_path)
            referenziati = refs_csv | refs_html
        else:
            referenziati = get_referenced_images_from_html(html_path)

        # Orfani = presenti in img/ ma non referenziati
        orfani = sorted(tutti - referenziati)
        usati  = sorted(tutti & referenziati)

        print(f"  Immagini totali in img/ : {len(tutti)}")
        print(f"  Referenziate            : {len(usati)}")
        print(f"  Orfane                  : {len(orfani)}")

        if orfani:
            print()
            for nome in orfani:
                path = img_dir / nome
                size = path.stat().st_size // 1024
                if delete:
                    path.unlink()
                    print(f"  🗑  CANCELLATO  {nome}  ({size} KB)")
                else:
                    print(f"  ⚠  ORFANA      {nome}  ({size} KB)")
            totale_orfani += len(orfani)
        else:
            print("  ✅ Nessun orfano trovato")

        totale_ok += len(usati)
        print()

    print("═" * 60)
    print(f"  Immagini referenziate : {totale_ok}")
    print(f"  Orfani trovati        : {totale_orfani}")
    if totale_orfani > 0 and not delete:
        print()
        print("  Per cancellare gli orfani:")
        print("  python scripts/find_orphan_png.py --delete")
    print("═" * 60)


if __name__ == "__main__":
    main()
