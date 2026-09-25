@echo off
echo ===================================================
echo   RECONECTANDO GITHUB COM O SEU NOTEBOOK...
echo ===================================================
git fetch origin
git branch -M main
git reset --mixed origin/main
echo.
echo ===================================================
echo   Reconexao Concluida! Pode fechar esta janela.
echo ===================================================
pause
