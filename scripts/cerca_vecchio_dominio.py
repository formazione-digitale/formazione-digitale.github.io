"""
cerca_vecchio_dominio.py
Cerca occorrenze di formazione-digitale.github.io nel contenuto dei file.
Uso: python scripts/cerca_vecchio_dominio.py
"""

import os

TROVA        = "formazione-digitale.github.io"
EXCLUDE_DIRS = {'.git', 'node_modules', '.github', '.cache', 'docs'}
EXTENSIONS   = {'.html', '.htm', '.xml', '.js', '.css', '.json', '.md', '.txt', '.py'}

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def find_files(root):
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for filename in filenames:
            if os.path.splitext(filename)[1].lower() in EXTENSIONS:
                found.append(os.path.join(dirpath, filename))
    return sorted(found)


def main():
    print(f"Root:  {ROOT}")
    print(f"Cerca: {TROVA}")
    print("-" * 70)

    files = find_files(ROOT)
    results = []

    for filepath in files:
        rel = os.path.relpath(filepath, ROOT)
        try:
            with open(filepath, 'r', encoding='utf-8-sig') as f:
                for i, line in enumerate(f, 1):
                    if TROVA in line:
                        results.append((rel, i, line.strip()))
                        print(f"  [{i}]  {rel}")
                        print(f"         {line.strip()}")
                        print()
        except Exception as e:
            print(f"  ❌  ERRORE  {rel} → {e}")

    print("-" * 70)
    files_con_match = len({r[0] for r in results})
    print(f"Trovati: {len(results)} occorrenze in {files_con_match} file")


if __name__ == '__main__':
    main()