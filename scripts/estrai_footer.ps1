# estrai_footer.ps1
# Estrae il contenuto del <footer> da ogni file HTML del repo.
# Output: tabella a console + file footer_report.txt nella stessa cartella scripts/
# Uso: powershell -ExecutionPolicy Bypass -File .\estrai_footer.ps1

$root   = Split-Path -Parent $PSScriptRoot
$output = Join-Path $PSScriptRoot "footer_report.txt"

# Cartelle da ignorare
$escludi = @('\.git', 'node_modules', 'docs')

$files = Get-ChildItem -Path $root -Recurse -Filter "*.html" -File |
    Where-Object {
        $p = $_.FullName
        -not ($escludi | Where-Object { $p -match [regex]::Escape($_) })
    }

$risultati = foreach ($f in $files) {
    $content = Get-Content $f.FullName -Raw -Encoding UTF8

    # Estrae tutto ciò che sta tra <footer e </footer>
    if ($content -match '(?is)<footer[^>]*>(.*?)</footer>') {
        $footer = $matches[1].Trim()
        # Compatta spazi/newline per leggibilità
        $footer = $footer -replace '\s+', ' '
        # Tronca a 300 caratteri per non ingolfare il report
        $anteprima = if ($footer.Length -gt 300) { $footer.Substring(0,300) + ' [...]' } else { $footer }

        [PSCustomObject]@{
            File    = $f.FullName.Replace($root, '.')
            Footer  = $anteprima
        }
    } else {
        [PSCustomObject]@{
            File    = $f.FullName.Replace($root, '.')
            Footer  = '⚠️  NESSUN <footer> TROVATO'
        }
    }
}

# Salva su file
$risultati | ForEach-Object {
    "═══════════════════════════════════════"
    "FILE: $($_.File)"
    "FOOTER: $($_.Footer)"
    ""
} | Out-File -FilePath $output -Encoding UTF8

Write-Host ""
Write-Host "Report salvato in: $output" -ForegroundColor Green
Write-Host "File analizzati:   $(@($risultati).Count)" -ForegroundColor Cyan
Write-Host ""

# Anteprima console — solo file senza footer o con footer anomalo
$anomali = $risultati | Where-Object { $_.Footer -match 'NESSUN' }
if ($anomali) {
    Write-Host "⚠️  File SENZA footer:" -ForegroundColor Yellow
    $anomali | ForEach-Object { Write-Host "  $($_.File)" }
} else {
    Write-Host "✅ Tutti i file hanno un <footer>." -ForegroundColor Green
}
Write-Host ""
