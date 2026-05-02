"""
inject_after.py
Esplora l'albero del progetto, trova tutti i file HTML e inserisce
una stringa NEW subito dopo ogni occorrenza della stringa DOVE.

Uso:
    python inject_after.py

Personalizza DOVE e NEW nelle costanti qui sotto.
Lo script è idempotente: se NEW è già presente subito dopo DOVE, salta il file.
"""

import os
import sys

# ── CONFIGURAZIONE ────────────────────────────────────────────────
DOVE = '<link rel="icon" type="image/webp" href="https://formazione-digitale.github.io/img/formazione-digitale-logo.webp">'

NEW  = '\n<link rel="icon" type="image/png" href="https://formazione-digitale.github.io/img/formazione-digitale-logo.png">'

# Cartelle da escludere dall'esplorazione
EXCLUDE_DIRS = {'.git', 'node_modules', '.github', '.cache', 'docs'}

# Estensioni da processare
EXTENSIONS = {'.html', '.htm'}

# Root del progetto — risale da scripts/ alla root
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# ─────────────────────────────────────────────────────────────────


def find_html_files(root):
    """Restituisce tutti i file HTML nell'albero, escludendo le cartelle in EXCLUDE_DIRS."""
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        # Rimuove le cartelle escluse in-place (os.walk le salterà)
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for filename in filenames:
            if os.path.splitext(filename)[1].lower() in EXTENSIONS:
                found.append(os.path.join(dirpath, filename))
    return sorted(found)


def process_file(filepath):
    """
    Cerca DOVE nel file e inserisce NEW subito dopo.
    Restituisce: 'ok', 'skip' (già presente), 'not_found', 'error'
    """
    try:
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            content = f.read()
    except Exception as e:
        return 'error', str(e)

    # Controlla se DOVE è presente
    if DOVE not in content:
        return 'not_found', None

    # Controlla se NEW è già presente subito dopo DOVE (idempotenza)
    insertion_point = content.find(DOVE) + len(DOVE)
    after = content[insertion_point:insertion_point + len(NEW)]
    if after.strip().startswith(NEW.strip()):
        return 'skip', None

    # Inserisce NEW subito dopo DOVE
    new_content = content.replace(DOVE, DOVE + NEW, 1)

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
    except Exception as e:
        return 'error', str(e)

    return 'ok', None


def main():
    print(f"Root: {ROOT}")
    print(f"DOVE: {DOVE[:60]}...")
    print(f"NEW:  {NEW.strip()[:60]}...")
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
            print(f"  ⏭   SKIP      {rel}  (già presente)")
        elif result == 'not_found':
            print(f"  ⚠️   NOT FOUND  {rel}  (DOVE non trovato)")
        elif result == 'error':
            print(f"  ❌  ERROR     {rel}  → {detail}")

        stats[result] += 1

    print("-" * 70)
    print(f"Riepilogo: {stats['ok']} OK · {stats['skip']} SKIP · "
          f"{stats['not_found']} NOT FOUND · {stats['error']} ERROR")

    if stats['not_found'] > 0:
        print("\n⚠️  I file NOT FOUND non hanno la stringa DOVE — verifica se mancano i meta SEO.")
    if stats['error'] > 0:
        print("\n❌  Alcuni file hanno generato errori — controlla i permessi.")
    if stats['ok'] == 0 and stats['not_found'] == 0:
        print("\nℹ️  Nessuna modifica necessaria — tutto già aggiornato.")


if __name__ == '__main__':
    main()
