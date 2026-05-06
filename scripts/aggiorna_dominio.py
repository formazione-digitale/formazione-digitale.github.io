"""
aggiorna_dominio.py
Sostituisce il vecchio dominio github.io con formazione-digitale.it
in tutti i file HTML e XML del repository.

Uso: python aggiorna_dominio.py
Eseguire dalla cartella scripts/
"""

import os

# ── CONFIGURAZIONE ────────────────────────────────────────────────
TROVA       = 'formazione-digitale.github.io'
SOSTITUISCI = 'formazione-digitale.it'

EXCLUDE_DIRS = {'.git', 'node_modules', '.github', '.cache', 'docs'}
EXTENSIONS   = {'.html', '.htm', '.xml'}

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# ─────────────────────────────────────────────────────────────────


def find_files(root):
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for filename in filenames:
            if os.path.splitext(filename)[1].lower() in EXTENSIONS:
                found.append(os.path.join(dirpath, filename))
    return sorted(found)


def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            content = f.read()
    except Exception as e:
        return 'error', str(e)

    if TROVA not in content:
        return 'not_found', None

    new_content = content.replace(TROVA, SOSTITUISCI)

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
    except Exception as e:
        return 'error', str(e)

    return 'ok', None


def main():
    print(f"Root:       {ROOT}")
    print(f"TROVA:      {TROVA}")
    print(f"SOSTITUISCI:{SOSTITUISCI}")
    print("-" * 70)

    files = find_files(ROOT)
    print(f"File trovati: {len(files)}\n")

    stats = {'ok': 0, 'not_found': 0, 'error': 0}

    for filepath in files:
        rel = os.path.relpath(filepath, ROOT)
        result, detail = process_file(filepath)

        if result == 'ok':
            print(f"  ✅  OK        {rel}")
        elif result == 'not_found':
            print(f"  ⚪  SKIP      {rel}")
        elif result == 'error':
            print(f"  ❌  ERROR     {rel}  → {detail}")

        stats[result] += 1

    print("-" * 70)
    print(f"Riepilogo: {stats['ok']} modificati · "
          f"{stats['not_found']} invariati · {stats['error']} errori")

    if stats['error'] > 0:
        print("\n❌ Alcuni file hanno generato errori — controlla i permessi.")
    if stats['ok'] == 0:
        print("\nℹ️  Nessuna modifica — dominio già aggiornato ovunque.")


if __name__ == '__main__':
    main()
