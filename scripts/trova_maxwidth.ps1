# trova_maxwidth.ps1
# Trova tutti i valori di max-width nei blocchi <style> inline delle pagine.
# READ-ONLY. Output: console + maxwidth_report.txt in scripts/

$root   = Split-Path -Parent $PSScriptRoot
$output = Join-Path $PSScriptRoot "maxwidth_report.txt"

$cartelleDaIgnorare = @('\.git', 'node_modules', 'docs')

$files = Get-ChildItem -Path $root -Recurse -Filter "*.html" -File |
    Where-Object {
        $p = $_.FullName
        -not ($cartelleDaIgnorare | Where-Object { $p -match [regex]::Escape($_) })
    }

$risultati = foreach ($f in $files) {
    $content = Get-Content $f.FullName -Raw -Encoding UTF8
    $rel = $f.FullName.Replace($root + '\', '')

    $styleMatches = [regex]::Matches($content, '(?is)<style[^>]*>(.*?)</style>')
    $valori = @()
    foreach ($m in $styleMatches) {
        $css = $m.Groups[1].Value
        # Trova tutte le occorrenze max-width con valore px
        $mw = [regex]::Matches($css, 'max-width\s*:\s*(\d+px)')
        foreach ($hit in $mw) { $valori += $hit.Groups[1].Value }
    }

    if ($valori.Count -gt 0) {
        [PSCustomObject]@{
            File   = $rel
            Valori = ($valori | Sort-Object -Unique) -join ', '
        }
    }
}

$risultati | ForEach-Object {
    "FILE:   $($_.File)"
    "VALORI: $($_.Valori)"
    ""
} | Out-File -FilePath $output -Encoding UTF8

Write-Host ""
$risultati | Format-Table -AutoSize
Write-Host " Report: $output" -ForegroundColor DarkGray
Write-Host ""
