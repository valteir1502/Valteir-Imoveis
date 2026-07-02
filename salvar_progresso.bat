@echo off
if "%1"=="/silent" goto silent

echo ===================================================
echo   SALVANDO PROGRESSO E ENVIANDO PARA O GITHUB...
echo ===================================================
echo.
git add .
git commit -m "Progresso sincronizado em %date% %time%"
git push origin main
echo.
echo ===================================================
echo   PROCESSO CONCLUIDO! Pressione qualquer tecla...
echo ===================================================
pause
goto end

:silent
git add .
git commit -m "Sincronizacao automatica - %date% %time%"
git push origin main

:end
