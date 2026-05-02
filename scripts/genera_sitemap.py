"""
genera_sitemap.py
Genera sitemap.xml leggendo le risorse attive da manifest.json.

Uso: python genera_sitemap.py
Output: sitemap.xml nella stessa cartella dello script

Aggiorna manifest.json quando aggiungi risorse, poi rilancia questo script.
"""

import json
import os
from datetime import date

# ── CONFIGURAZIONE ───────────────────────────────────────────────
BASE_URL   = "https://formazione-digitale.github.io"
LASTMOD    = date.today().isoformat()  # es. 2026-05-01
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT       = os.path.dirname(SCRIPT_DIR)  # risale da scripts/ alla root
MANIFEST   = os.path.join(ROOT, "manifest.json")
OUTPUT     = os.path.join(ROOT, "sitemap.xml")

# ── PAGINE FISSE (non nel manifest) ─────────────────────────────
PAGINE_FISSE = [
    {"loc": "/",          "priority": "1.0", "changefreq": "weekly"},
    {"loc": "/mappa.html","priority": "0.5", "changefreq": "monthly"},
]

# ── CARICA MANIFEST ──────────────────────────────────────────────
with open(MANIFEST, encoding="utf-8") as f:
    manifest = json.load(f)

risorse_attive = [r for r in manifest if r.get("active")]

# ── COSTRUISCI XML ───────────────────────────────────────────────
righe = ['<?xml version="1.0" encoding="UTF-8"?>']
righe.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

def url_block(loc, priority, changefreq):
    return (
        f"  <url>\n"
        f"    <loc>{BASE_URL}{loc}</loc>\n"
        f"    <lastmod>{LASTMOD}</lastmod>\n"
        f"    <changefreq>{changefreq}</changefreq>\n"
        f"    <priority>{priority}</priority>\n"
        f"  </url>"
    )

# Pagine fisse
for p in PAGINE_FISSE:
    righe.append(url_block(p["loc"], p["priority"], p["changefreq"]))

# Risorse dal manifest
for r in risorse_attive:
    righe.append(url_block(r["path"], "0.8", "monthly"))

righe.append("</urlset>")

# ── SCRIVI FILE ──────────────────────────────────────────────────
sitemap = "\n".join(righe) + "\n"
with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(sitemap)

print(f"sitemap.xml generata: {len(PAGINE_FISSE) + len(risorse_attive)} URL")
print(f"Output: {OUTPUT}")
