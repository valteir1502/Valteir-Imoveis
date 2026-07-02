$ScriptDir = $PSScriptRoot
if (-not $ScriptDir) {
    $ScriptDir = Get-Location
}

$SalvarPath = Join-Path $ScriptDir "salvar_progresso.bat"
$PuxarPath = Join-Path $ScriptDir "puxar_progresso.bat"

Write-Host "Configurando agendamentos no Windows..." -ForegroundColor Cyan

# 1. Configurando o Puxar no Logon via Pasta de Inicialização do Windows (não exige privilégios de Admin)
$StartupDir = [System.IO.Path]::Combine($env:APPDATA, "Microsoft\Windows\Start Menu\Programs\Startup")
$StartupBat = [System.IO.Path]::Combine($StartupDir, "Valteir_Imoveis_Puxar.bat")

$StartupContent = "@echo off`r`ncall `"$PuxarPath`" /silent"

try {
    Set-Content -Path $StartupBat -Value $StartupContent -Encoding ASCII
    Write-Host "SUCESSO: Inicializacao configurada na pasta de Inicializacao do Windows." -ForegroundColor Green
} catch {
    Write-Host "ERRO: Nao foi possivel criar o arquivo na pasta de Inicializacao: $_" -ForegroundColor Red
}

# 2. Configurando o Salvar Diário às 18:00 via Task Scheduler (não exige Admin)
$SalvarCmd = "schtasks /create /tn `"Valteir_Imoveis_Salvar_Diario`" /tr `"\`"$SalvarPath\`" /silent`" /sc daily /st 18:00 /f"
$SalvarResult = cmd /c $SalvarCmd
Write-Host $SalvarResult

Write-Host "`nAgendamentos criados com sucesso!" -ForegroundColor Green
Write-Host "A sincronizacao agora ocorrera automaticamente:" -ForegroundColor Yellow
Write-Host "1. Ao iniciar a sessao (logon) - puxar alteracoes" -ForegroundColor White
Write-Host "2. Todos os dias as 18:00 - salvar alteracoes" -ForegroundColor White
