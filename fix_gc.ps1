$old = '<script src="/gc.js"></script>'
$new = '<!-- GoatCounter tracking -->
<script data-goatcounter="https://formazionedigitale.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>'

Get-ChildItem -Recurse -Filter "*.html" | ForEach-Object {
    $content = Get-Content $_.FullName -Raw -Encoding UTF8
    if ($content -match [regex]::Escape($old)) {
        $content = $content.Replace($old, $new)
        Set-Content $_.FullName -Value $content -Encoding UTF8 -NoNewline
        Write-Host "Sostituito: $($_.FullName)"
    } else {
        Write-Host "Non trovato: $($_.FullName)"
    }
}

Write-Host ""
Write-Host "Fatto."
Read-Host "Premi Invio per chiudere"