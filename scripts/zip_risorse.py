"""
zip_risorse.py — Formazione Digitale
Crea uno ZIP del progetto escludendo estensioni e cartelle configurabili.
Posizionare in /scripts/ — la root del progetto è un livello sopra.

Uso:
    python zip_risorse.py              # blacklist default
    python zip_risorse.py --dry-run    # mostra i file inclusi senza creare lo ZIP
"""

import os
import zipfile
import argparse
from datetime import datetime
from pathlib import Path

# ─────────────────────────────────────────────
# CONFIGURAZIONE — modifica qui
# ─────────────────────────────────────────────

# Estensioni da ESCLUDERE (aggiungi/rimuovi liberamente)
BLACKLIST_ESTENSIONI = {
    ".png",
    ".webp",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
    ".pdf",
    ".pptx",
    ".xlsx",
    ".odb",
    ".zip",
    ".docx",
    ".mp3",
    ".mp4",
    ".wav",
    ".ogg",
}

# Cartelle da ESCLUDERE — qualsiasi livello dell'albero (nome esatto, case-sensitive)
BLACKLIST_CARTELLE = {
    "img",
    ".git",
}

# ─────────────────────────────────────────────
# LOGICA — non modificare sotto questa riga
# ─────────────────────────────────────────────

def dovrebbe_escludere(path: Path, root: Path) -> bool:
    """Restituisce True se il file va escluso."""
    # Controlla se una delle parti del percorso è una cartella blacklistata
    parti_relative = path.relative_to(root).parts
    for parte in parti_relative[:-1]:  # escludi il nome file, solo cartelle
        if parte in BLACKLIST_CARTELLE:
            return True
    # Controlla estensione
    if path.suffix.lower() in BLACKLIST_ESTENSIONI:
        return True
    return False


def crea_zip(root: Path, output_path: Path, dry_run: bool = False):
    file_inclusi = []
    file_esclusi = []

    for file in sorted(root.rglob("*")):
        if not file.is_file():
            continue
        if dovrebbe_escludere(file, root):
            file_esclusi.append(file.relative_to(root))
        else:
            file_inclusi.append(file)

    if dry_run:
        print(f"\n{'─'*50}")
        print(f"DRY RUN — nessuno ZIP creato")
        print(f"{'─'*50}")
        print(f"\n✅ FILE INCLUSI ({len(file_inclusi)}):")
        for f in file_inclusi:
            print(f"   {f.relative_to(root)}")
        print(f"\n❌ FILE ESCLUSI ({len(file_esclusi)}):")
        for f in file_esclusi:
            print(f"   {f}")
        return

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in file_inclusi:
            arcname = file.relative_to(root)
            zf.write(file, arcname)

    dim_mb = output_path.stat().st_size / (1024 * 1024)

    print(f"\n{'─'*50}")
    print(f"✅ ZIP creato: {output_path.name}")
    print(f"   Percorso : {output_path}")
    print(f"   Dimensione: {dim_mb:.2f} MB")
    print(f"   File inclusi : {len(file_inclusi)}")
    print(f"   File esclusi : {len(file_esclusi)}")
    print(f"{'─'*50}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Crea ZIP del progetto Formazione Digitale escludendo binari e immagini."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Mostra i file che verrebbero inclusi senza creare lo ZIP",
    )
    args = parser.parse_args()

    # Lo script è in /scripts/ — la root è un livello sopra
    script_dir = Path(__file__).resolve().parent
    root = script_dir.parent

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    nome_zip = f"formazione-digitale_{timestamp}.zip"
    output_path = root / nome_zip

    print(f"Root progetto : {root}")
    print(f"Output ZIP    : {output_path}")

    crea_zip(root, output_path, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
