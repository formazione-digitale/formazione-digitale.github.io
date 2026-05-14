#!/usr/bin/env python3
"""
png_to_webp.py — Formazione Digitale
Converte i PNG referenziati in un index.html in WebP, li rinomina con
prefisso+progressivo, aggiorna i path nell'HTML e produce un report.

Uso:
    python scripts/png_to_webp.py                        # chiede cartella e prefisso
    python scripts/png_to_webp.py --dir elaborazione-testi/guida-word
    python scripts/png_to_webp.py --dir elaborazione-testi/guida-word --prefix word
    python scripts/png_to_webp.py --dir elaborazione-testi/guida-word --quality 85
    python scripts/png_to_webp.py --dry-run              # preview senza modifiche

Requisiti:
    pip install pillow --break-system-packages
    
# Guida Word
python scripts/png_to_webp.py --dry-run --dir elaborazione-testi/guida-word --prefix word

# Se il dry-run ti convince:
python scripts/png_to_webp.py --dir elaborazione-testi/guida-word --prefix word

# Guida LibreOffice Base Query
python scripts/png_to_webp.py --dir database/guida-libreoffice-base-query --prefix query

DA DENTRO SCRIPTS
python png_to_webp.py --dry-run --dir ../elaborazione-testi/guida-word --prefix word
python png_to_webp.py --dir ../elaborazione-testi/guida-word --prefix word
python png_to_webp.py --dry-run --dir ../database/guida-libreoffice-base-query --prefix query --report mapping-query.csv
python png_to_webp.py --dir ../database/guida-libreoffice-base-query --prefix query --report mapping-query.csv
python png_to_webp.py --dry-run --dir ../networking/hfs-server --prefix hfs --report mapping-hfs.csv
python png_to_webp.py --dir ../networking/hfs-server --prefix hfs --report mapping-hfs.csv



"""

import os
import re
import sys
import shutil
import argparse
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Errore: Pillow non installato.")
    print("Esegui: pip install pillow --break-system-packages")
    sys.exit(1)


# ── CONFIGURAZIONE DEFAULT ───────────────────────────────────────
DEFAULT_PREFIX  = "image"
DEFAULT_QUALITY = 90
HTML_FILE       = "index.html"
IMG_DIR         = "img"


# ── ARGOMENTI CLI ────────────────────────────────────────────────
def parse_args():
    parser = argparse.ArgumentParser(
        description="Converte PNG → WebP e aggiorna index.html"
    )
    parser.add_argument(
        "--dir", "-d",
        help="Cartella contenente index.html e img/. Default: chiede interattivamente."
    )
    parser.add_argument(
        "--prefix", "-p",
        help=f"Prefisso per i file WebP (es: word, query). Default: '{DEFAULT_PREFIX}' o chiede interattivamente."
    )
    parser.add_argument(
        "--quality", "-q",
        type=int, default=DEFAULT_QUALITY,
        help=f"Qualità WebP 1-100. Default: {DEFAULT_QUALITY}"
    )
    parser.add_argument(
        "--report", "-r",
        help="Salva il mapping in un file CSV (es: --report mapping.csv)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Mostra cosa farebbe senza modificare nulla."
    )
    return parser.parse_args()


# ── TROVA TUTTI I SRC PNG NELL'HTML (in ordine di apparizione) ──
def trova_png_in_html(html_content: str) -> list[str]:
    """
    Estrae tutti i path src="..." che terminano in .png dall'HTML.
    Restituisce la lista in ordine di apparizione (con duplicati).
    """
    pattern = re.compile(
        r'src=["\']([^"\']*\.png)["\']',
        re.IGNORECASE
    )
    return pattern.findall(html_content)


# ── CONVERTE UN PNG IN WEBP ──────────────────────────────────────
def converti_png_webp(src_path: Path, dst_path: Path, quality: int) -> bool:
    """
    Converte src_path (PNG) in dst_path (WebP).
    Restituisce True se ok, False se fallisce.
    """
    try:
        img = Image.open(src_path)
        # Preserva trasparenza se presente (RGBA → WebP)
        img.save(dst_path, "WEBP", quality=quality, method=6)
        return True
    except Exception as e:
        print(f"  ⚠ Errore conversione {src_path.name}: {e}")
        return False


# ── MAIN ─────────────────────────────────────────────────────────
def main():
    args = parse_args()

    # ── Cartella di lavoro ──
    if args.dir:
        work_dir = Path(args.dir)
    else:
        risposta = input(
            "Cartella contenente index.html e img/ "
            "(invio = cartella corrente): "
        ).strip()
        work_dir = Path(risposta) if risposta else Path(".")

    work_dir = work_dir.resolve()
    html_path = work_dir / HTML_FILE
    img_dir   = work_dir / IMG_DIR

    # ── Validazione ──
    if not html_path.exists():
        print(f"Errore: {html_path} non trovato.")
        sys.exit(1)
    if not img_dir.exists():
        print(f"Errore: cartella {img_dir} non trovata.")
        sys.exit(1)

    # ── Prefisso ──
    if args.prefix:
        prefix = args.prefix.strip()
    else:
        risposta = input(
            f"Prefisso per i file WebP (invio = '{DEFAULT_PREFIX}'): "
        ).strip()
        prefix = risposta if risposta else DEFAULT_PREFIX

    # Normalizza prefisso: solo lettere, numeri, trattini
    prefix = re.sub(r"[^\w\-]", "", prefix).lower()
    if not prefix:
        prefix = DEFAULT_PREFIX

    quality  = max(1, min(100, args.quality))
    dry_run  = args.dry_run

    print()
    print("═" * 60)
    print(f"  Formazione Digitale — PNG → WebP converter")
    print("═" * 60)
    print(f"  Cartella  : {work_dir}")
    print(f"  Prefisso  : {prefix}")
    print(f"  Qualità   : {quality}")
    print(f"  Dry-run   : {'SÌ — nessuna modifica' if dry_run else 'NO — modifiche applicate'}")
    print("═" * 60)
    print()

    # ── Leggi HTML ──
    html_content = html_path.read_text(encoding="utf-8")
    html_nuovo   = html_content  # verrà modificato

    # ── Trova tutti i PNG nell'HTML in ordine ──
    png_trovati = trova_png_in_html(html_content)

    if not png_trovati:
        print("Nessun src .png trovato nell'HTML. Nulla da fare.")
        sys.exit(0)

    print(f"  PNG referenziati nell'HTML: {len(png_trovati)} occorrenze")
    print()

    # ── Stato ──
    # mapping: nome_originale → nome_webp assegnato (es: "image_005.png" → "word005.webp")
    mapping: dict[str, str] = {}
    contatore       = 1
    convertiti      = 0
    riusati         = 0
    saltati         = 0
    bytes_prima     = 0
    bytes_dopo      = 0
    report_righe    = []

    # ── Processa ogni occorrenza PNG ──
    for src_originale in png_trovati:
        # Estrae solo il nome file (es: "img/image_005.png" → "image_005.png")
        nome_file = Path(src_originale).name
        png_path  = img_dir / nome_file

        # ── File non esiste su disco ──
        if not png_path.exists():
            msg = f"  ⚠ SALTA — file non trovato su disco: {src_originale}"
            print(msg)
            report_righe.append(("SALTA", src_originale, "—", "file non trovato"))
            saltati += 1
            continue

        # ── Già processato in precedenza (duplicato nell'HTML) ──
        if nome_file in mapping:
            nome_webp    = mapping[nome_file]
            src_webp     = str(Path(src_originale).parent / nome_webp)
            print(f"  ♻ RIUSO  {nome_file:45s} → {nome_webp}")
            report_righe.append(("RIUSO", src_originale, src_webp, "già convertito"))
            html_nuovo = html_nuovo.replace(
                f'"{src_originale}"', f'"{src_webp}"',
                1  # sostituisce solo la prossima occorrenza
            ).replace(
                f"'{src_originale}'", f"'{src_webp}'",
                1
            )
            riusati += 1
            continue

        # ── Nuova immagine — assegna nome progressivo ──
        nome_webp = f"{prefix}{contatore:03d}.webp"
        webp_path = img_dir / nome_webp
        src_webp  = str(Path(src_originale).parent / nome_webp)
        contatore += 1

        dim_prima = png_path.stat().st_size
        bytes_prima += dim_prima

        if not dry_run:
            ok = converti_png_webp(png_path, webp_path, quality)
        else:
            ok = True  # dry-run: simula successo

        if ok:
            mapping[nome_file] = nome_webp
            dim_dopo = webp_path.stat().st_size if (not dry_run and webp_path.exists()) else 0
            bytes_dopo += dim_dopo

            risparmio = ""
            if dim_dopo > 0:
                pct = (1 - dim_dopo / dim_prima) * 100
                risparmio = f"{pct:+.0f}%"

            stato = "DRY  " if dry_run else "✓    "
            print(f"  {stato} {nome_file:45s} → {nome_webp}  {_fmt_bytes(dim_prima)} → {_fmt_bytes(dim_dopo) if dim_dopo else '?':>7}  {risparmio}")
            report_righe.append(("OK", src_originale, src_webp, risparmio))

            # Aggiorna HTML — prima occorrenza di questo src
            html_nuovo = html_nuovo.replace(
                f'"{src_originale}"', f'"{src_webp}"',
                1
            ).replace(
                f"'{src_originale}'", f"'{src_webp}'",
                1
            )
            convertiti += 1
        else:
            saltati += 1
            report_righe.append(("ERRORE", src_originale, "—", "conversione fallita"))

    # ── Salva HTML aggiornato ──
    if not dry_run and html_nuovo != html_content:
        # Backup dell'originale
        backup_path = html_path.with_suffix(".html.bak")
        shutil.copy2(html_path, backup_path)
        html_path.write_text(html_nuovo, encoding="utf-8")
        print()
        print(f"  Backup HTML salvato in: {backup_path.name}")
        print(f"  index.html aggiornato.")

    # ── Report finale ──
    print()
    print("═" * 60)
    print(f"  REPORT FINALE")
    print("═" * 60)
    print(f"  PNG unici convertiti : {convertiti}")
    print(f"  Occorrenze riusate   : {riusati}")
    print(f"  File saltati/errori  : {saltati}")
    if bytes_prima > 0 and bytes_dopo > 0:
        risparmio_tot = (1 - bytes_dopo / bytes_prima) * 100
        print(f"  Peso prima           : {_fmt_bytes(bytes_prima)}")
        print(f"  Peso dopo            : {_fmt_bytes(bytes_dopo)}")
        print(f"  Risparmio totale     : {risparmio_tot:.1f}%")
    print("═" * 60)

    # ── Salva report CSV se richiesto ──
    if args.report:
        report_path = work_dir / args.report
        import csv
        with open(report_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["stato", "src_originale", "src_webp", "note"])
            writer.writerows(report_righe)
        print(f"  Report CSV salvato in: {report_path}")

    if dry_run:
        print()
        print("  Dry-run completato — nessun file modificato.")
    else:
        print()
        print(f"  Prefisso usato: {prefix}NNN.webp")
        print(f"  I PNG originali sono intatti in {img_dir.name}/")
        print(f"  Verifica visivamente, poi elimina i PNG manualmente.")

    print()


# ── UTILITÀ ──────────────────────────────────────────────────────
def _fmt_bytes(b: int) -> str:
    if b == 0:
        return "—"
    if b < 1024:
        return f"{b} B"
    if b < 1024 * 1024:
        return f"{b/1024:.1f} KB"
    return f"{b/1024/1024:.1f} MB"


if __name__ == "__main__":
    main()
