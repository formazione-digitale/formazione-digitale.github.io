# rinomina_mappa.py
# Rinomina mappa-risorse.html → mappa-risorse.html e aggiorna tutti i riferimenti.
# Eseguire dalla root del repository.

import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(ROOT, '..')  # sale da scripts/ alla root

VECCHIO = 'mappa-risorse.html'
NUOVO   = 'mappa-risorse.html'

ESTENSIONI = {'.html', '.xml', '.json', '.js', '.css', '.md', '.txt', '.py'}
ESCLUDI    = {'.git', 'node_modules', '.github'}

sostituzioni = 0
file_modificati = []

for dirpath, dirnames, filenames in os.walk(ROOT):
    # Esclude cartelle indesiderate
    dirnames[:] = [d for d in dirnames if d not in ESCLUDI]

    for filename in filenames:
        ext = os.path.splitext(filename)[1].lower()
        if ext not in ESTENSIONI:
            continue

        filepath = os.path.join(dirpath, filename)
        rel = os.path.relpath(filepath, ROOT)

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            continue

        # Sostituisce tutti i riferimenti a mappa-risorse.html
        # Pattern robusto: evita di sostituire mappa-aree.html o mappa-framework.html
        nuovo_content = re.sub(
            r'(?<![a-zA-Z0-9_-])mappa\.html',
            NUOVO,
            content
        )

        if nuovo_content != content:
            n = len(re.findall(r'(?<![a-zA-Z0-9_-])mappa\.html', content))
            sostituzioni += n
            file_modificati.append((rel, n))
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(nuovo_content)
            print(f"  OK    {rel} ({n} occorrenze)")

# Rinomina il file fisico
vecchio_path = os.path.join(ROOT, VECCHIO)
nuovo_path   = os.path.join(ROOT, NUOVO)

if os.path.exists(vecchio_path):
    os.rename(vecchio_path, nuovo_path)
    print(f"\n  RINOMINATO: {VECCHIO} → {NUOVO}")
else:
    print(f"\n  ATTENZIONE: {VECCHIO} non trovato nella root — rinomina manuale necessaria")

print(f"\n{'═'*50}")
print(f" File modificati:   {len(file_modificati)}")
print(f" Sostituzioni totali: {sostituzioni}")
print(f" File rinominato:   {VECCHIO} → {NUOVO}")
print(f"{'═'*50}")
