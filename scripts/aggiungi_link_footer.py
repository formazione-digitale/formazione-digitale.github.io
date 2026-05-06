"""
aggiungi_link_footer.py
Aggiunge i link Privacy Policy e Cookie Policy in tutti i file HTML
delle sottocartelle del portale.

Logica:
  - Se il file ha </footer>  → inserisce i link prima dell'ultima chiusura
  - Se il file non ha footer → inserisce un <footer> completo prima di </body>

Idempotente: se i link sono già presenti, salta il file.

Uso: python aggiungi_link_footer.py
Eseguire dalla cartella scripts/
"""

import os

# ── CONFIGURAZIONE ────────────────────────────────────────────────
LINK = '  <p style="margin-top:.5rem;font-size:.78rem;">\n    <a href="/privacy-policy.html">Privacy Policy</a> &nbsp;·&nbsp; <a href="/cookie-policy.html">Cookie Policy</a>\n  </p>\n'

FOOTER_COMPLETO = '\n<footer>\n' + LINK + '</footer>\n'

EXCLUDE_DIRS  = {'.git', 'node_modules', '.github', '.cache', 'docs'}
EXTENSIONS    = {'.html', '.htm'}
# File nella root — gestiti da aggiungi_footer_index.py
EXCLUDE_FILES = {'privacy-policy.html', 'cookie-policy.html'}

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# ─────────────────────────────────────────────────────────────────


def find_html_files(root):
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        rel = os.path.relpath(dirpath, root)
        print(f"DIR: {rel} — files: {filenames}")  # DEBUG
        if rel == '.':
            continue
        for filename in filenames:
            if os.path.splitext(filename)[1].lower() in EXTENSIONS:
                if filename not in EXCLUDE_FILES:
                    found.append(os.path.join(dirpath, filename))
    return sorted(found)


def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            content = f.read()
    except Exception as e:
        return 'error', str(e), None

    # Idempotenza
    if 'privacy-policy.html' in content and 'cookie-policy.html' in content:
        return 'skip', None, None

    # CASO 1 — ha già un <footer>
    if '</footer>' in content:
        last = content.rfind('</footer>')
        new_content = content[:last] + LINK + content[last:]
        mode = 'footer-esistente'

    # CASO 2 — non ha footer, inserisce prima di </body>
    elif '</body>' in content:
        new_content = content.replace('</body>', FOOTER_COMPLETO + '</body>', 1)
        mode = 'footer-nuovo'

    else:
        return 'not_found', None, None

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
    except Exception as e:
        return 'error', str(e), None

    return 'ok', None, mode


def main():
    print(f"Root: {ROOT}")
    print(f"Aggiunge link Privacy/Cookie in tutte le guide e pillole")
    print("-" * 70)

    files = find_html_files(ROOT)
    print(f"File HTML trovati: {len(files)}\n")
    for f in files:
        print(f)

    stats = {'ok': 0, 'skip': 0, 'not_found': 0, 'error': 0}

    for filepath in files:
        rel = os.path.relpath(filepath, ROOT)
        result, detail, mode = process_file(filepath)

        if result == 'ok':
            label = '(footer esistente)' if mode == 'footer-esistente' else '(footer nuovo)'
            print(f"  ✅  OK        {rel}  {label}")
        elif result == 'skip':
            print(f"  ⏭   SKIP      {rel}  (link già presenti)")
        elif result == 'not_found':
            print(f"  ⚠️   NOT FOUND  {rel}  (né </footer> né </body> trovati)")
        elif result == 'error':
            print(f"  ❌  ERROR     {rel}  → {detail}")

        stats[result] += 1

    print("-" * 70)
    print(f"Riepilogo: {stats['ok']} OK · {stats['skip']} SKIP · "
          f"{stats['not_found']} NOT FOUND · {stats['error']} ERROR")

    if stats['not_found'] > 0:
        print("\n⚠️  I file NOT FOUND non hanno né </footer> né </body> — verifica manualmente.")
    if stats['error'] > 0:
        print("\n❌  Alcuni file hanno generato errori.")


if __name__ == '__main__':
    main()
