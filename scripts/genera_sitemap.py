"""
genera_sitemap.py
Genera sitemap.xml leggendo le risorse attive da manifest.json.
La data <lastmod> di ogni URL viene letta dall'ultimo commit Git
del file corrispondente — non viene usata la data odierna.

Uso: python genera_sitemap.py
Output: sitemap.xml nella root del progetto
"""

import json
import os
import subprocess
from datetime import date

# ── CONFIGURAZIONE ───────────────────────────────────────────────
BASE_URL   = "https://formazione-digitale.it"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT       = os.path.dirname(SCRIPT_DIR)  # risale da scripts/ alla root
MANIFEST   = os.path.join(ROOT, "manifest.json")
OUTPUT     = os.path.join(ROOT, "sitemap.xml")

# ── PAGINE FISSE (non nel manifest) ─────────────────────────────
PAGINE_FISSE = [
    {"loc": "/",                     "file": "index.html",        "priority": "1.0", "changefreq": "weekly"},
    {"loc": "/mappa-risorse.html",           "file": "mappa-risorse.html",        "priority": "0.5", "changefreq": "monthly"},
    {"loc": "/mappa-framework.html", "file": "mappa-framework.html", "priority": "0.5", "changefreq": "monthly"},
]

# ── LASTMOD DA GIT ───────────────────────────────────────────────
def get_lastmod(filepath):
    """Restituisce la data dell'ultimo commit Git del file, o oggi come fallback."""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", filepath],
            cwd=ROOT, capture_output=True, text=True
        )
        date_str = result.stdout.strip()
        return date_str if date_str else date.today().isoformat()
    except Exception:
        return date.today().isoformat()

# ── CARICA MANIFEST ──────────────────────────────────────────────
with open(MANIFEST, encoding="utf-8") as f:
    manifest = json.load(f)

risorse_attive = [r for r in manifest if r.get("active")]

# ── COSTRUISCI XML ───────────────────────────────────────────────
righe = ['<?xml version="1.0" encoding="UTF-8"?>']
righe.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

def url_block(loc, priority, changefreq, lastmod):
    return (
        f"  <url>\n"
        f"    <loc>{BASE_URL}{loc}</loc>\n"
        f"    <lastmod>{lastmod}</lastmod>\n"
        f"    <changefreq>{changefreq}</changefreq>\n"
        f"    <priority>{priority}</priority>\n"
        f"  </url>"
    )

# Pagine fisse
for p in PAGINE_FISSE:
    filepath = os.path.join(ROOT, p["file"])
    lastmod  = get_lastmod(filepath)
    righe.append(url_block(p["loc"], p["priority"], p["changefreq"], lastmod))

# Risorse dal manifest
for r in risorse_attive:
    filepath = os.path.join(ROOT, r["path"].lstrip("/"), "index.html")
    lastmod  = get_lastmod(filepath)
    righe.append(url_block(r["path"], "0.8", "monthly", lastmod))

righe.append("</urlset>")

# ── SCRIVI FILE ──────────────────────────────────────────────────
sitemap = "\n".join(righe) + "\n"
with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(sitemap)

print(f"sitemap.xml generata: {len(PAGINE_FISSE) + len(risorse_attive)} URL")
print(f"Output: {OUTPUT}")

# ── BUMP CACHE_VERSION IN sw.js ──────────────────────────────────
# Aggiorna CACHE_VERSION con la data odierna ad ogni lancio dello script.
# Quando sw.js verrà spostato in /scripts/, aggiorna SW_PATH di conseguenza.
import re

SW_PATH = os.path.join(ROOT, "sw.js")  # attuale: root — futuro: scripts/sw.js

if os.path.exists(SW_PATH):
    with open(SW_PATH, encoding="utf-8") as f:
        sw_content = f.read()

    nuova_versione = f"fd-v{date.today().isoformat()}"
    sw_aggiornato = re.sub(
        r"const CACHE_VERSION\s*=\s*'[^']*'",
        f"const CACHE_VERSION = '{nuova_versione}'",
        sw_content
    )

    if sw_aggiornato != sw_content:
        with open(SW_PATH, "w", encoding="utf-8") as f:
            f.write(sw_aggiornato)
        print(f"sw.js aggiornato: CACHE_VERSION = '{nuova_versione}'")
    else:
        print(f"sw.js: CACHE_VERSION già aggiornata ({nuova_versione})")
else:
    print(f"ATTENZIONE: sw.js non trovato in {SW_PATH}")
