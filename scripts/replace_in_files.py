"""
replace_in_files.py
Esplora l'albero del progetto, trova tutti i file HTML e sostituisce
ogni occorrenza di TROVA con SOSTITUISCI.

Uso:
    python replace_in_files.py

Personalizza TROVA e SOSTITUISCI nelle costanti qui sotto.
Lo script è idempotente: se applicare la sostituzione non cambia il
contenuto del file, lo salta (confronto diretto, non basato su
substring-check — vedi nota più sotto).
"""

import os

# ── CONFIGURAZIONE ────────────────────────────────────────────────
TROVA       = '<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">'
SOSTITUISCI = '<link rel="preload" href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" as="style">\n<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">'

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
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for filename in filenames:
            if os.path.splitext(filename)[1].lower() in EXTENSIONS:
                found.append(os.path.join(dirpath, filename))
    return sorted(found)


def process_file(filepath):
    """
    Cerca TROVA nel file e lo sostituisce con SOSTITUISCI.
    Restituisce: 'ok', 'skip' (TROVA assente, nulla da fare), 'error'

    NOTA: l'idempotenza è verificata applicando davvero la sostituzione
    e confrontando il risultato con l'originale — NON controllando se
    SOSTITUISCI è già presente nel testo. Quel controllo si rompe ogni
    volta che SOSTITUISCI è una sottostringa di TROVA (es. TROVA='Â·',
    SOSTITUISCI='·' — '·' è sempre presente se 'Â·' lo è, quindi il
    vecchio controllo segnalava "già sostituito" anche quando non era
    mai stato sostituito nulla).
    """
    try:
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            content = f.read()
    except Exception as e:
        return 'error', str(e)

    if TROVA not in content:
        return 'skip', None

    new_content = content.replace(TROVA, SOSTITUISCI)

    if new_content == content:
        return 'skip', None

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

    stats = {'ok': 0, 'skip': 0, 'error': 0}

    for filepath in files:
        rel = os.path.relpath(filepath, ROOT)
        result, detail = process_file(filepath)

        if result == 'ok':
            print(f"  ✅  OK        {rel}")
        elif result == 'skip':
            print(f"  ⏭   SKIP      {rel}")
        elif result == 'error':
            print(f"  ❌  ERROR     {rel}  → {detail}")

        stats[result] += 1

    print("-" * 70)
    print(f"Riepilogo: {stats['ok']} OK · {stats['skip']} SKIP · {stats['error']} ERROR")

    if stats['error'] > 0:
        print("\n❌  Alcuni file hanno generato errori — controlla i permessi.")
    if stats['ok'] == 0:
        print("\nℹ️  Nessuna modifica necessaria — TROVA non presente in nessun file.")


if __name__ == '__main__':
    main()
