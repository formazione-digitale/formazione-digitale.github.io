# trova_anomali.ps1
# Elenca file anomali nel repo. READ-ONLY, non modifica nulla.
# Posizionare in scripts/ e lanciare da li':
#   cd scripts
#   powershell -ExecutionPolicy Bypass -File .\trova_anomali.ps1

$root = Split-Path -Parent $PSScriptRoot

Get-ChildItem -Path $root -Recurse -File -Force |
Where-Object { $_.FullName -notmatch '\\\.git\\' } |
Where-Object { $_.Name -match '\.(bak|old|orig)$|[-_]\.[^.]+$|\(\s*\d+\s*\)|\s|\.(zip|7z|rar)$|^~\$|\.(tmp|swp)$' } |
Select-Object `
    @{N='Percorso'; E={ $_.FullName.Replace($root, '.') }},
    @{N='KB';       E={ [math]::Round($_.Length / 1KB, 1) }},
    @{N='Motivo';   E={
        $n = $_.Name
        if     ($n -match '\.(bak|old|orig)$')  { 'Backup' }
        elseif ($n -match '[-_]\.[^.]+$')        { 'Trattino spurio' }
        elseif ($n -match '\(\s*\d+\s*\)')       { 'Duplicato (N)' }
        elseif ($n -match '\.(zip|7z|rar)$')     { 'Archivio' }
        elseif ($n -match '\s')                  { 'Spazio nel nome' }
        else                                     { 'Temp/sistema' }
    }} |
Format-Table -AutoSize
