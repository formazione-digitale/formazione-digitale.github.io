"""
aggiungi_footer_index.py
Inserisce il tag <footer> con link Privacy/Cookie in index.html e mappa.html
che non hanno un footer strutturato.

Uso: python aggiungi_footer_index.py
Eseguire dalla cartella scripts/
"""

import os

# ── CONFIGURAZIONE ────────────────────────────────────────────────
DOVE = '</body>'
NEW  = """<footer>
  <strong>Formazione Digitale</strong> · Risorse di alfabetizzazione digitale libere e gratuite.<br>
  <a href="/privacy-policy.html">Privacy Policy</a> &nbsp;·&nbsp; <a href="/cookie-policy.html">Cookie Policy</a>
</footer>
"""

# Solo questi file — non tutti gli HTML
TARGET_FILES = {'index.html', 'mappa.html', '404.html'}

EXCLUDE_DIRS = {'.git', 'node_modules', '.github', '.cache', 'docs'}
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# ─────────────────────────────────────────────────────────────────


def find_target_files(root):
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        # Solo file nella root del progetto con nome in TARGET_FILES
        if os.path.abspath(dirpath) == os.path.abspath(root):
            for filename in filenames:
                if filename in TARGET_FILES:
                    found.append(os.path.join(dirpath, filename))
    return sorted(found)


def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            content = f.read()
    except Exception as e:
        return 'error', str(e)

    if DOVE not in content:
        return 'not_found', None

    # Idempotenza — controlla se footer è già presente
    if '<footer>' in content:
        return 'skip', None

    new_content = content.replace(DOVE, NEW + DOVE, 1)

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
    except Exception as e:
        return 'error', str(e)

    return 'ok', None


def main():
    print(f"Root: {ROOT}")
    print(f"Target: {TARGET_FILES}")
    print("-" * 70)

    files = find_target_files(ROOT)
    print(f"File trovati: {len(files)}\n")

    stats = {'ok': 0, 'skip': 0, 'not_found': 0, 'error': 0}

    for filepath in files:
        rel = os.path.relpath(filepath, ROOT)
        result, detail = process_file(filepath)

        if result == 'ok':
            print(f"  ✅  OK        {rel}")
        elif result == 'skip':
            print(f"  ⏭   SKIP      {rel}  (footer già presente)")
        elif result == 'not_found':
            print(f"  ⚠️   NOT FOUND  {rel}  (</body> non trovato)")
        elif result == 'error':
            print(f"  ❌  ERROR     {rel}  → {detail}")

        stats[result] += 1

    print("-" * 70)
    print(f"Riepilogo: {stats['ok']} OK · {stats['skip']} SKIP · "
          f"{stats['not_found']} NOT FOUND · {stats['error']} ERROR")


if __name__ == '__main__':
    main()
