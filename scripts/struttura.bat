@echo off
cd ..

set /p IMMAGINI="Includi file immagine nell'elenco? [S/n]: "
if /i "%IMMAGINI%"=="n" goto ESCLUDI

:INCLUDI
tree /f /a > struttura.txt
goto FINE

:ESCLUDI
tree /f /a | findstr /v /i ".png .jpg .jpeg .gif .webp .svg .ico .bmp .tiff" > struttura.txt

:FINE
echo Fatto. File salvato in: %CD%\struttura.txt
