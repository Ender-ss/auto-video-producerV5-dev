# Script PowerShell simples para executar o diagnóstico do MoviePy
param(
    [string]$command = "help"
)

# Função para mostrar ajuda
function Show-Help {
    Write-Host "Script de Diagnóstico do MoviePy" -ForegroundColor Cyan
    Write-Host "Uso: .\diagnose.ps1 [comando]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Comandos disponíveis:" -ForegroundColor Green
    Write-Host "  help          - Mostra esta ajuda"
    Write-Host "  simple        - Executa o diagnóstico simplificado"
    Write-Host "  complete      - Executa o diagnóstico completo"
    Write-Host ""
}

# Executar comando baseado no parâmetro
switch ($command) {
    "help" { Show-Help; break }
    "simple" { 
        Write-Host "Executando diagnóstico simplificado do MoviePy..." -ForegroundColor Cyan
        python solucoes\SCRIPT_DIAGNOSTICO_SIMPLIFICADO.py
        break
    }
    "complete" { 
        Write-Host "Executando diagnóstico completo do MoviePy..." -ForegroundColor Cyan
        python testes\SCRIPT_DIAGNOSTICO_COMPLETO.py
        break
    }
    default { 
        Write-Host "Comando não reconhecido: $command" -ForegroundColor Red
        Show-Help
        break
    }
}