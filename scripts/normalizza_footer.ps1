# normalizza_footer.ps1
# Sostituisce il blocco <footer>...</footer> in tutti i file HTML del repo
# con il template canonico, rispettando i casi speciali.
# Crea backup .bak prima di ogni modifica.
# Uso: powershell -ExecutionPolicy Bypass -File .\normalizza_footer.ps1

$root = Split-Path -Parent $PSScriptRoot

# ── File da NON toccare (percorsi relativi ESATTI dalla root) ─────
$escludi = @(
    'index.html',
    'privacy-policy.html',
    'cookie-policy.html',
    'mappa-aree.html',
    'icdl\index.html',
    'icdl\statistiche\index.html',
    'database\guida-libreoffice-base-query\index.html',
    'database\guida-modello-logico\index.html'
)

# ── Path che sono "strumento" ma il nome cartella non lo rivela
#    (il regex sotto non può indovinarlo dal nome) — aggiungere qui
#    ogni volta che un nuovo strumento ha un path "non parlante" ─────
$strumentiEspliciti = @(
    'sistemi\logica-booleana\index.html',
    'sistemi\alberi-di-parsing\index.html'
)

# ── Determina tipo risorsa → descrizione ─────────────────────────
function Get-Descrizione($percorsoRelativo) {
    if ($strumentiEspliciti -contains $percorsoRelativo) {
        return 'Strumento didattico libero e gratuito. I dati inseriti non vengono salvati né trasmessi.'
    }
    if ($percorsoRelativo -match 'strumento|tool|calculator|kanban|analizzatore|builder|subnet') {
        return 'Strumento didattico libero e gratuito. I dati inseriti non vengono salvati né trasmessi.'
    }
    if ($percorsoRelativo -match 'pillola') {
        return 'Pillola digitale libera e gratuita. Contenuti aggiornati al 2026.'
    }
    return 'Guida digitale libera e gratuita. Contenuti aggiornati al 2026.'
}

# ── Template canonico ─────────────────────────────────────────────
function Get-FooterCanonico($descrizione) {
    return @"
<footer>
  <strong>Formazione Digitale</strong> &middot; <a href="/">Torna alla home</a><br>
  $descrizione
  <p style="margin-top:.5rem;font-size:.78rem;">
    <a href="/privacy-policy.html">Privacy Policy</a> &nbsp;&middot;&nbsp;
    <a href="/cookie-policy.html">Cookie Policy</a>
  </p>
</footer>
"@
}

# ── Raccolta file ─────────────────────────────────────────────────
$cartelleDaIgnorare = @('\.git', 'node_modules', 'docs')

$files = Get-ChildItem -Path $root -Recurse -Filter "*.html" -File |
    Where-Object {
        $p = $_.FullName
        -not ($cartelleDaIgnorare | Where-Object { $p -match [regex]::Escape($_) })
    }

# ── Elaborazione ──────────────────────────────────────────────────
$modificati  = 0
$saltati     = 0
$senzaFooter = 0

foreach ($f in $files) {
    # Percorso relativo dalla root, senza backslash iniziale
    $relativo = $f.FullName.Replace($root + '\', '')

    # Confronto ESATTO con la lista esclusioni
    if ($escludi -contains $relativo) {
        Write-Host "  SKIP  $relativo" -ForegroundColor DarkGray
        $saltati++
        continue
    }

    $content = Get-Content $f.FullName -Raw -Encoding UTF8

    # Verifica presenza footer
    if ($content -notmatch '(?is)<footer[^>]*>.*?</footer>') {
        Write-Host "  WARN  Nessun footer: $relativo" -ForegroundColor Yellow
        $senzaFooter++
        continue
    }

    # Calcola descrizione e footer canonico
    $desc   = Get-Descrizione $relativo
    $nuovo  = Get-FooterCanonico $desc

    # Sostituisce il footer
    $nuovo_content = [regex]::Replace($content, '(?is)<footer[^>]*>.*?</footer>', $nuovo)

    if ($nuovo_content -eq $content) {
        Write-Host "  SAME  $relativo" -ForegroundColor DarkGray
        $saltati++
        continue
    }

    # Backup
    Copy-Item $f.FullName ($f.FullName + '.bak') -Force

    # Scrittura UTF-8 senza BOM
    [System.IO.File]::WriteAllText($f.FullName, $nuovo_content, [System.Text.UTF8Encoding]::new($false))

    Write-Host "  OK    $relativo" -ForegroundColor Green
    $modificati++
}

# ── Riepilogo ─────────────────────────────────────────────────────
Write-Host ""
Write-Host "═══════════════════════════════════════" -ForegroundColor Cyan
Write-Host " Modificati:      $modificati" -ForegroundColor Green
Write-Host " Saltati/uguali:  $saltati"    -ForegroundColor DarkGray
Write-Host " Senza footer:    $senzaFooter" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host " Backup .bak creati per ogni file modificato." -ForegroundColor DarkGray
Write-Host " Verifica il risultato, poi elimina i .bak con trova_anomali.bat" -ForegroundColor DarkGray
Write-Host ""
