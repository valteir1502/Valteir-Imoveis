@echo off
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
