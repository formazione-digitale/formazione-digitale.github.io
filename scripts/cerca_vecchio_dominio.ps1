# Cerca tutti i riferimenti a formazione-digitale.github.io nel repo
# Uso: esegui dalla root del repository
# .\scripts\cerca_vecchio_dominio.ps1

$TROVA = "formazione-digitale.github.io"
$EXCLUDE_DIRS = @(".git", "node_modules", ".github", ".cache", "docs")
$EXTENSIONS = @("*.html", "*.htm", "*.xml", "*.js", "*.css", "*.json", "*.md", "*.txt", "*.py")

$root = Get-Location

Write-Host "Root:  $root"
Write-Host "Cerca: $TROVA"
Write-Host ("-" * 70)

$results = @()

Get-ChildItem -Path $root -Recurse -Include $EXTENSIONS |
  Where-Object {
    $parts = $_.FullName.Split([System.IO.Path]::DirectorySeparatorChar)
    -not ($parts | Where-Object { $EXCLUDE_DIRS -contains $_ })
  } |
  ForEach-Object {
    $file = $_
    $rel  = $file.FullName.Replace("$root\", "").Replace("$root/", "")

    $lines = Get-Content -Path $file.FullName -Encoding UTF8 -ErrorAction SilentlyContinue
    if (-not $lines) { return }

    for ($i = 0; $i -lt $lines.Count; $i++) {
      if ($lines[$i].Contains($TROVA)) {
        $results += [PSCustomObject]@{
          File  = $rel
          Riga  = $i + 1
          Testo = $lines[$i].Trim()
        }
        Write-Host "  [$($i + 1)]  $rel"
        Write-Host "         $($lines[$i].Trim())"
        Write-Host ""
      }
    }
  }

Write-Host ("-" * 70)
Write-Host "Trovati: $($results.Count) occorrenze in $($results | Select-Object -Unique File | Measure-Object | Select-Object -ExpandProperty Count) file"