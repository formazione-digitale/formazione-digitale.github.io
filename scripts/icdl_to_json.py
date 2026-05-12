#!/usr/bin/env python3
"""
icdl_to_json.py — Converte i report Excel ICDL in data.json anonimizzato.

Uso:
    python scripts/icdl_to_json.py

Cerca automaticamente tutti i file export_*.xlsx in data-src/,
li unisce e scrive icdl/statistiche/data.json.

La cartella data-src/ è in .gitignore — gli Excel non vanno mai sul repo.
I dati personali (Candidato, Codice Fiscale, Codice Skillscard) vengono rimossi.
"""

import json
import os
import glob
from datetime import datetime, date

try:
    import pandas as pd
except ImportError:
    print("Errore: pandas non installato. Esegui: pip install pandas openpyxl")
    raise SystemExit(1)

# Root del repo = cartella padre di scripts/
ROOT     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORGENTE = os.path.join(ROOT, "data-src", "export_*.xlsx")
OUTPUT   = os.path.join(ROOT, "icdl", "statistiche", "data.json")

COLONNE = {
    "Certificazione":   "certificazione",
    "Modulo":           "modulo",
    "Punteggio":        "punteggio",
    "Punteggio minimo": "punteggio_minimo",
    "Esito":            "esito",
    "Completato il":    "data",
}


def parse_data(valore):
    if isinstance(valore, (datetime, date)):
        return valore.strftime("%Y-%m-%d")
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(str(valore).strip(), fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return str(valore).strip()


def leggi_excel(percorso):
    df = pd.read_excel(percorso)
    mancanti = [c for c in COLONNE if c not in df.columns]
    if mancanti:
        print(f"  ⚠ Colonne mancanti in {percorso}: {mancanti} — file ignorato")
        return None
    df = df[list(COLONNE.keys())].rename(columns=COLONNE)
    df["data"] = df["data"].apply(parse_data)
    return df


def main():
    file_trovati = sorted(glob.glob(SORGENTE))

    if not file_trovati:
        print(f"Nessun file trovato in {SORGENTE}")
        print("Assicurati che la cartella data-src/ esista e contenga i file export_*.xlsx")
        raise SystemExit(1)

    print(f"File trovati: {len(file_trovati)}")
    frames = []
    for f in file_trovati:
        print(f"  Lettura: {f}")
        df = leggi_excel(f)
        if df is not None:
            frames.append(df)

    if not frames:
        print("Nessun file valido da processare.")
        raise SystemExit(1)

    tutto = pd.concat(frames, ignore_index=True)
    tutto = tutto.sort_values("data").reset_index(drop=True)

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    output = {
        "generato_il": datetime.today().strftime("%Y-%m-%d"),
        "esami": tutto.to_dict(orient="records"),
    }
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nOK: {len(tutto)} esami scritti in {OUTPUT}")
    print(f"    Periodo: {tutto['data'].min()} → {tutto['data'].max()}")


if __name__ == "__main__":
    main()
