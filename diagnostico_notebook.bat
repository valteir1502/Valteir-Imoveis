@echo off
echo ===================================================
echo   DIAGNOSTICO DE SINCRONIZACAO DO VALTEIR PROJETOS
echo ===================================================
echo.
set LOG_FILE=resultado_diagnostico.txt
echo Gerando relatorio em %LOG_FILE%...
echo === RELATORIO DE DIAGNOSTICO === > "%LOG_FILE%"
echo Data: %date% %time% >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

echo 1. Verificando se o Git esta instalado...
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERRO] O Git nao esta instalado ou nao esta nas variaveis de ambiente (PATH) do sistema do notebook. >> "%LOG_FILE%"
    echo O script 'puxar_progresso.bat' nao vai funcionar sem o Git. >> "%LOG_FILE%"
    goto end_diag
) else (
    echo [OK] Git instalado. >> "%LOG_FILE%"
    git --version >> "%LOG_FILE%"
)

echo 2. Verificando a pasta do repositorio...
if not exist .git (
    echo [ERRO] Esta pasta nao eh um repositorio Git valido no notebook. >> "%LOG_FILE%"
    echo Verifique se voce clonou a pasta corretamente no notebook. >> "%LOG_FILE%"
    goto end_diag
) else (
    echo [OK] Pasta Git identificada. >> "%LOG_FILE%"
)

echo 3. Verificando o repositorio remoto configurado...
git remote -v >> "%LOG_FILE%" 2>&1

echo 4. Verificando conexao com o GitHub e atualizacoes...
git fetch origin main > "%LOG_FILE%.tmp" 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Falha ao se conectar ao GitHub a partir do notebook. >> "%LOG_FILE%"
    type "%LOG_FILE%.tmp" >> "%LOG_FILE%"
    del "%LOG_FILE%.tmp"
) else (
    echo [OK] Conexao com GitHub estabelecida com sucesso. >> "%LOG_FILE%"
    del "%LOG_FILE%.tmp"
)

echo 5. Verificando status local (alteracoes pendentes ou conflitos)...
git status >> "%LOG_FILE%" 2>&1

echo 6. Verificando diferencas entre local e remote...
git log HEAD..origin/main --oneline >> "%LOG_FILE%" 2>&1

:end_diag
echo.
echo ===================================================
echo   DIAGNOSTICO CONCLUIDO!
echo   O arquivo '%LOG_FILE%' foi criado nesta pasta.
echo   Por favor, abra esse arquivo para ver os erros,
echo   ou envie o conteudo dele para mim para que eu analise.
echo ===================================================
pause
