@echo off
if "%1"=="/silent" goto silent

echo ===================================================
echo   ATUALIZANDO ARQUIVOS E TAREFAS DO GITHUB...
echo ===================================================
echo.
git pull origin main
echo.
echo ===================================================
echo   PROCESSO CONCLUIDO! Pressione qualquer tecla...
echo ===================================================
pause
goto end

:silent
git pull origin main

:end
