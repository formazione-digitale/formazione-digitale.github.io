# trova_override_layout.ps1
# Trova pagine con override CSS inline su guide-main, guide-layout,
# guide-sidebar, #main, #sidebar nei blocchi <style>.
# READ-ONLY. Output: console + override_report.txt in scripts/
# Uso: powershell -ExecutionPolicy Bypass -File .\trova_override_layout.ps1

$root   = Split-Path -Parent $PSScriptRoot
$output = Join-Path $PSScriptRoot "override_report.txt"

$cartelleDaIgnorare = @('\.git', 'node_modules', 'docs')

$files = Get-ChildItem -Path $root -Recurse -Filter "*.html" -File |
    Where-Object {
        $p = $_.FullName
        -not ($cartelleDaIgnorare | Where-Object { $p -match [regex]::Escape($_) })
    }

$risultati = foreach ($f in $files) {
    $content = Get-Content $f.FullName -Raw -Encoding UTF8
    $rel = $f.FullName.Replace($root + '\', '')

    # Estrae i blocchi <style>...</style>
    $styleMatches = [regex]::Matches($content, '(?is)<style[^>]*>(.*?)</style>')
    
    $overrides = @()
    foreach ($m in $styleMatches) {
        $css = $m.Groups[1].Value
        # Cerca override su classi/ID di layout
        if ($css -match '\.guide-main\s*\{')    { $overrides += 'guide-main' }
        if ($css -match '\.guide-layout\s*\{')  { $overrides += 'guide-layout' }
        if ($css -match '\.guide-sidebar\s*\{') { $overrides += 'guide-sidebar' }
        if ($css -match '#main\s*\{')            { $overrides += '#main' }
        if ($css -match '#sidebar\s*\{')         { $overrides += '#sidebar' }
    }

    if ($overrides.Count -gt 0) {
        [PSCustomObject]@{
            File     = $rel
            Override = ($overrides | Sort-Object -Unique) -join ', '
        }
    }
}

# Salva report
$risultati | ForEach-Object {
    "═══════════════════════════════════════"
    "FILE:     $($_.File)"
    "OVERRIDE: $($_.Override)"
    ""
} | Out-File -FilePath $output -Encoding UTF8

# Console
Write-Host ""
Write-Host "═══════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host " FILE CON OVERRIDE CSS DI LAYOUT" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════" -ForegroundColor Cyan

if (-not $risultati) {
    Write-Host " Nessun override trovato." -ForegroundColor Green
} else {
    $risultati | Format-Table -AutoSize
    Write-Host " Totale: $(@($risultati).Count) file" -ForegroundColor Yellow
}

Write-Host " Report: $output" -ForegroundColor DarkGray
Write-Host ""
