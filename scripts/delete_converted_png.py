#!/usr/bin/env python3
"""
delete_converted_png.py — Formazione Digitale
Legge i CSV di mapping generati da png_to_webp.py e cancella
SOLO i PNG originali che sono stati convertiti con successo in WebP.

Uso:
    python scripts/delete_converted_png.py --dry-run   # preview
    python scripts/delete_converted_png.py             # cancella

I CSV di mapping devono essere nella cartella della rispettiva guida.
"""

import os
import csv
import argparse
from pathlib import Path

# ── CONFIGURAZIONE ───────────────────────────────────────────────
# Percorso root del progetto (cartella padre di scripts/)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Mapping: cartella guida → file CSV di mapping
MAPPINGS = [
    {
        "dir": "elaborazione-testi/guida-word",
        "csv": None,  # guida-word non ha CSV — usa i PNG referenziati nell'HTML
        "note": "guida-word: PNG rinominati in ordine da index.html"
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


def parse_args():
    parser = argparse.ArgumentParser(
        description="Cancella i PNG originali già convertiti in WebP"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Mostra cosa cancellerebbe senza cancellare nulla"
    )
    return parser.parse_args()


def get_png_from_csv(csv_path: Path) -> list[str]:
    """
    Legge il CSV di mapping e restituisce i nomi file PNG originali
    con stato OK (convertiti con successo).
    """
    png_files = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        seen = set()
        for row in reader:
            if row["stato"] in ("OK", "RIUSO"):
                # Estrae solo il nome file dal path (es: "img/file.png" → "file.png")
                nome = Path(row["src_originale"]).name
                if nome not in seen:
                    seen.add(nome)
                    png_files.append(nome)
    return png_files


def get_png_from_word(dir_path: Path) -> list[str]:
    """
    Per guida-word: i PNG sono image_001.png → image_061.png
    più image_032.png (orfana). Li trova tutti direttamente in img/.
    """
    img_dir = dir_path / "img"
    return [f.name for f in img_dir.glob("*.png")]


def main():
    args = parse_args()
    dry_run = args.dry_run

    print("═" * 60)
    print("  Formazione Digitale — Cancellazione PNG convertiti")
    print("═" * 60)
    print(f"  Dry-run: {'SÌ — nessuna cancellazione' if dry_run else 'NO — cancellazione reale'}")
    print("═" * 60)
    print()

    totale_cancellati = 0
    totale_mancanti   = 0
    totale_webp_miss  = 0

    for mapping in MAPPINGS:
        dir_path = Path(ROOT) / mapping["dir"]
        img_dir  = dir_path / "img"
        csv_file = mapping.get("csv")

        print(f"📁 {mapping['dir']}")

        # Ottieni lista PNG da cancellare
        if csv_file:
            csv_path = dir_path / csv_file
            if not csv_path.exists():
                print(f"  ⚠ CSV non trovato: {csv_path}")
                print()
                continue
            png_list = get_png_from_csv(csv_path)
        else:
            # guida-word: tutti i PNG in img/
            png_list = get_png_from_word(dir_path)

        cancellati = 0
        for nome_png in png_list:
            png_path  = img_dir / nome_png
            # Verifica che esista il WebP corrispondente prima di cancellare
            webp_path = img_dir / (Path(nome_png).stem + ".webp")

            # Controlla se esiste ALMENO un WebP nella cartella img/
            # (il nome WebP è diverso dall'originale — basta che esistano WebP)
            webp_presenti = list(img_dir.glob("*.webp"))

            if not png_path.exists():
                print(f"  ⚠ GIÀ ASSENTE  {nome_png}")
                totale_mancanti += 1
                continue

            if not webp_presenti:
                print(f"  ⚠ NO WEBP      {nome_png} — nessun WebP trovato, salto")
                totale_webp_miss += 1
                continue

            if dry_run:
                print(f"  DRY  🗑  {nome_png}  ({png_path.stat().st_size // 1024} KB)")
            else:
                size = png_path.stat().st_size
                png_path.unlink()
                print(f"  ✓    🗑  {nome_png}  ({size // 1024} KB) — cancellato")

            cancellati += 1
            totale_cancellati += 1

        print(f"  → {cancellati} PNG {'da cancellare' if dry_run else 'cancellati'}")
        print()

    print("═" * 60)
    print(f"  TOTALE cancellati : {totale_cancellati}")
    if totale_mancanti:
        print(f"  Già assenti       : {totale_mancanti}")
    if totale_webp_miss:
        print(f"  Saltati (no WebP) : {totale_webp_miss}")
    print("═" * 60)

    if dry_run:
        print()
        print("  Dry-run completato — nessun file cancellato.")
        print("  Lancia senza --dry-run per procedere.")


if __name__ == "__main__":
    main()
