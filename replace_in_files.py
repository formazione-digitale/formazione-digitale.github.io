"""
replace_in_files.py
Esplora l'albero del progetto, trova tutti i file HTML e sostituisce
ogni occorrenza di TROVA con SOSTITUISCI.

Uso:
    python replace_in_files.py

Personalizza TROVA e SOSTITUISCI nelle costanti qui sotto.
Lo script è idempotente: se TROVA non è presente ma SOSTITUISCI sì, salta il file.
"""

import os

# ── CONFIGURAZIONE ────────────────────────────────────────────────
TROVA = '<link rel="icon" href="https://formazione-digitale.github.io/img/formazione-digitale-logo.png">'

SOSTITUISCI = '<link rel="icon" type="image/webp" href="https://formazione-digitale.github.io/img/formazione-digitale-logo.webp">'

# Cartelle da escludere dall'esplorazione
EXCLUDE_DIRS = {'.git', 'node_modules', '.github', '.cache', 'docs'}

# Estensioni da processare
EXTENSIONS = {'.html', '.htm'}

# Root del progetto — cartella dove si trova questo script
ROOT = os.path.dirname(os.path.abspath(__file__))
# ─────────────────────────────────────────────────────────────────


def find_html_files(root):
    """Restituisce tutti i file HTML nell'albero, escludendo le cartelle in EXCLUDE_DIRS."""
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for filename in filenames:
            if os.path.splitext(filename)[1].lower() in EXTENSIONS:
                found.append(os.path.join(dirpath, filename))
    return sorted(found)


def process_file(filepath):
    """
    Cerca TROVA nel file e lo sostituisce con SOSTITUISCI.
    Restituisce: 'ok', 'skip' (già sostituito), 'not_found', 'error'
    """
    try:
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            content = f.read()
    except Exception as e:
        return 'error', str(e)

    # Già sostituito — idempotenza
    if SOSTITUISCI in content:
        return 'skip', None

    # TROVA non presente
    if TROVA not in content:
        return 'not_found', None

    # Sostituisce
    new_content = content.replace(TROVA, SOSTITUISCI)

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
    except Exception as e:
        return 'error', str(e)

    return 'ok', None


def main():
    print(f"Root: {ROOT}")
    print(f"TROVA:      {TROVA[:70]}...")
    print(f"SOSTITUISCI:{SOSTITUISCI[:70]}...")
    print("-" * 70)

    files = find_html_files(ROOT)
    print(f"File HTML trovati: {len(files)}\n")

    stats = {'ok': 0, 'skip': 0, 'not_found': 0, 'error': 0}

    for filepath in files:
        rel = os.path.relpath(filepath, ROOT)
        result, detail = process_file(filepath)

        if result == 'ok':
            print(f"  ✅  OK        {rel}")
        elif result == 'skip':
            print(f"  ⏭   SKIP      {rel}  (già sostituito)")
        elif result == 'not_found':
            print(f"  ⚠️   NOT FOUND  {rel}  (TROVA non trovato)")
        elif result == 'error':
            print(f"  ❌  ERROR     {rel}  → {detail}")

        stats[result] += 1

    print("-" * 70)
    print(f"Riepilogo: {stats['ok']} OK · {stats['skip']} SKIP · "
          f"{stats['not_found']} NOT FOUND · {stats['error']} ERROR")

    if stats['not_found'] > 0:
        print("\n⚠️  I file NOT FOUND non contengono TROVA — verifica manualmente.")
    if stats['error'] > 0:
        print("\n❌  Alcuni file hanno generato errori — controlla i permessi.")
    if stats['ok'] == 0 and stats['not_found'] == 0:
        print("\nℹ️  Nessuna modifica necessaria — tutto già aggiornato.")


if __name__ == '__main__':
    main()
