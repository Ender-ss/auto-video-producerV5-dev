# Script PowerShell para MoviePy Documentation Manager
# Este script facilita a execução dos scripts de documentação e testes do MoviePy no Windows

# Definir variáveis
$PYTHON = "python"
$DOCS_DIR = "docs\moviepy"
$SCRIPTS_DIR = $DOCS_DIR
$CONFIG_FILE = "$DOCS_DIR\CONFIG.json"
$REQUIREMENTS_FILE = "$DOCS_DIR\requirements.txt"
$SETUP_SCRIPT = "$DOCS_DIR\setup.py"
$MAIN_SCRIPT = "$DOCS_DIR\SCRIPT_MAIN.py"

# Funções
function Print-Header {
    param([string]$title)
    Write-Host "=============================================================" -ForegroundColor Cyan
    Write-Host $title -ForegroundColor Cyan
    Write-Host "=============================================================" -ForegroundColor Cyan
    Write-Host ""
}

function Print-Section {
    param([string]$title)
    Write-Host "----------------------------------------" -ForegroundColor Yellow
    Write-Host $title -ForegroundColor Yellow
    Write-Host "----------------------------------------" -ForegroundColor Yellow
    Write-Host ""
}

# Verificar argumentos
if ($args.Count -eq 0) {
    Show-Help
    exit
}

$command = $args[0]

# Definir funções antes de usá-las
function Show-Help {
    Print-Header "Makefile para MoviePy Documentation Manager"
    Write-Host "Uso:"
    Write-Host "  .\run.ps1 [comando]"
    Write-Host ""
    Write-Host "Comandos disponíveis:"
    Write-Host "  help          Mostra esta ajuda"
    Write-Host "  all           Executa todos os scripts"
    Write-Host "  install       Executa o script de instalação"
    Write-Host "  diagnose      Executa o script de diagnóstico"
    Write-Host "  diagnose-simple Executa o script de diagnóstico simplificado"
    Write-Host "  test          Executa os testes do MoviePy"
    Write-Host "  examples      Executa os exemplos do MoviePy"
    Write-Host "  report        Gera um relatório completo"
    Write-Host "  clean         Limpa arquivos temporários"
    Write-Host "  update        Atualiza a documentação"
    Write-Host "  setup         Configura o ambiente do MoviePy"
    Write-Host "  check         Verifica o ambiente"
    Write-Host "  run           Executa o script principal"
    Write-Host "  install-deps  Instala dependências"
    Write-Host "  check-python  Verifica Python"
    Write-Host "  check-ffmpeg  Verifica FFmpeg"
    Write-Host "  check-imagemagick Verifica ImageMagick"
    Write-Host "  test-moviepy  Testa MoviePy"
    Write-Host "  create-dirs   Cria diretórios"
    Write-Host "  clean-dirs    Limpa diretórios"
    Write-Host "  check-structure Verifica estrutura"
    Write-Host "  full-diagnose Executa diagnóstico completo"
    Write-Host "  full-workflow Executa workflow completo"
    Write-Host ""
}

function Run-Diagnose-Simple {
    Print-Header "Diagnóstico Simplificado do MoviePy"
    Write-Host "Executando diagnóstico simplificado..."
    Push-Location $DOCS_DIR
    Write-Host "Diretório atual: $(Get-Location)"
    Write-Host "Executando: $PYTHON solucoes\SCRIPT_DIAGNOSTICO_SIMPLIFICADO.py"
    & $PYTHON solucoes\SCRIPT_DIAGNOSTICO_SIMPLIFICADO.py
    Pop-Location
}

switch ($command) {
    "help" { Show-Help; break }
    "all" { Run-All; break }
    "install" { Run-Install; break }
    "diagnose" { Run-Diagnose; break }
    "diagnose-simple" { Run-Diagnose-Simple; break }
    "test" { Run-Test; break }
    "examples" { Run-Examples; break }
    "report" { Run-Report; break }
    "clean" { Run-Clean; break }
    "update" { Run-Update; break }
    "setup" { Run-Setup; break }
    "check" { Run-Check; break }
    "run" { Run-Run; break }
    "install-deps" { Run-Install-Deps; break }
    "check-python" { Run-Check-Python; break }
    "check-ffmpeg" { Run-Check-FFmpeg; break }
    "check-imagemagick" { Run-Check-ImageMagick; break }
    "test-moviepy" { Run-Test-MoviePy; break }
    "create-dirs" { Run-Create-Dirs; break }
    "clean-dirs" { Run-Clean-Dirs; break }
    "check-structure" { Run-Check-Structure; break }
    "full-diagnose" { Run-Full-Diagnose; break }
    "full-workflow" { Run-Full-Workflow; break }
    default { 
        Write-Host "Comando não reconhecido: $command" -ForegroundColor Red
        Show-Help
        break
    }
}

function Show-Help {
    Print-Header "Makefile para MoviePy Documentation Manager"
    Write-Host "Uso:"
    Write-Host "  .\run.ps1 [comando]"
    Write-Host ""
    Write-Host "Comandos disponíveis:"
    Write-Host "  help          Mostra esta ajuda"
    Write-Host "  all           Executa todos os scripts"
    Write-Host "  install       Executa o script de instalação"
    Write-Host "  diagnose      Executa o script de diagnóstico"
    Write-Host "  diagnose-simple Executa o script de diagnóstico simplificado"
    Write-Host "  test          Executa os testes do MoviePy"
    Write-Host "  examples      Executa os exemplos do MoviePy"
    Write-Host "  report        Gera um relatório completo"
    Write-Host "  clean         Limpa arquivos temporários"
    Write-Host "  update        Atualiza a documentação"
    Write-Host "  setup         Configura o ambiente do MoviePy"
    Write-Host "  check         Verifica o ambiente"
    Write-Host "  run           Executa o script principal"
    Write-Host "  install-deps  Instala dependências"
    Write-Host "  check-python  Verifica Python"
    Write-Host "  check-ffmpeg  Verifica FFmpeg"
    Write-Host "  check-imagemagick Verifica ImageMagick"
    Write-Host "  test-moviepy  Testa MoviePy"
    Write-Host "  create-dirs   Cria diretórios"
    Write-Host "  clean-dirs    Limpa diretórios"
    Write-Host "  check-structure Verifica estrutura"
    Write-Host "  full-diagnose Executa diagnóstico completo"
    Write-Host "  full-workflow Executa workflow completo"
    Write-Host ""
}

function Run-All {
    Print-Header "Executar Todos os Scripts"
    & $PYTHON $MAIN_SCRIPT --all
}

function Run-Install {
    Print-Header "Instalar e Configurar MoviePy"
    & $PYTHON $MAIN_SCRIPT --install
}

function Run-Diagnose {
    Print-Header "Diagnóstico do MoviePy"
    & $PYTHON $MAIN_SCRIPT --diagnose
}

function Run-Diagnose-Simple {
    Print-Header "Diagnóstico Simplificado do MoviePy"
    Write-Host "Executando diagnóstico simplificado..."
    Push-Location $DOCS_DIR
    Write-Host "Diretório atual: $(Get-Location)"
    Write-Host "Executando: $PYTHON solucoes\SCRIPT_DIAGNOSTICO_SIMPLIFICADO.py"
    & $PYTHON solucoes\SCRIPT_DIAGNOSTICO_SIMPLIFICADO.py
    Pop-Location
}

function Run-Test {
    Print-Header "Testes do MoviePy"
    & $PYTHON $MAIN_SCRIPT --test
}

function Run-Examples {
    Print-Header "Exemplos do MoviePy"
    & $PYTHON $MAIN_SCRIPT --examples
}

function Run-Report {
    Print-Header "Relatório do MoviePy"
    & $PYTHON $MAIN_SCRIPT --report
}

function Run-Clean {
    Print-Header "Limpar Arquivos Temporários"
    & $PYTHON $MAIN_SCRIPT --clean
}

function Run-Update {
    Print-Header "Atualizar Documentação"
    & $PYTHON $MAIN_SCRIPT --update
}

function Run-Setup {
    Print-Header "Configurar Ambiente do MoviePy"
    & $PYTHON $SETUP_SCRIPT
}

function Run-Check {
    Print-Header "Verificar Ambiente"
    if (-not (Test-Path $CONFIG_FILE)) {
        Write-Host "Arquivo de configuração não encontrado: $CONFIG_FILE" -ForegroundColor Red
        exit 1
    }
    if (-not (Test-Path $REQUIREMENTS_FILE)) {
        Write-Host "Arquivo requirements.txt não encontrado: $REQUIREMENTS_FILE" -ForegroundColor Red
        exit 1
    }
    if (-not (Test-Path $SETUP_SCRIPT)) {
        Write-Host "Script setup.py não encontrado: $SETUP_SCRIPT" -ForegroundColor Red
        exit 1
    }
    if (-not (Test-Path $MAIN_SCRIPT)) {
        Write-Host "Script principal não encontrado: $MAIN_SCRIPT" -ForegroundColor Red
        exit 1
    }
    Write-Host "Todos os arquivos necessários estão presentes!" -ForegroundColor Green
}

function Run-Run {
    Print-Header "Executar Script Principal"
    & $PYTHON $MAIN_SCRIPT
}

function Run-Install-Deps {
    Print-Header "Instalar Dependências"
    Write-Host "Instalando dependências do requirements.txt..."
    & $PYTHON -m pip install -r $REQUIREMENTS_FILE
    Write-Host "Dependências instaladas com sucesso!" -ForegroundColor Green
}

function Run-Check-Python {
    Print-Section "Verificar Python"
    & $PYTHON --version
}

function Run-Check-FFmpeg {
    Print-Section "Verificar FFmpeg"
    ffmpeg -version
}

function Run-Check-ImageMagick {
    Print-Section "Verificar ImageMagick"
    magick -version
}

function Run-Test-MoviePy {
    Print-Section "Testar MoviePy"
    & $PYTHON -c "import moviepy.editor as mpy; print('MoviePy está funcionando!')"
}

function Run-Create-Dirs {
    Print-Section "Criar Diretórios"
    $dirs = @("$DOCS_DIR\temp", "$DOCS_DIR\output", "$DOCS_DIR\logs", "$DOCS_DIR\cache", "$DOCS_DIR\examples_output")
    foreach ($dir in $dirs) {
        if (-not (Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir | Out-Null
        }
    }
    Write-Host "Diretórios criados com sucesso!" -ForegroundColor Green
}

function Run-Clean-Dirs {
    Print-Section "Limpar Diretórios"
    $dirs = @("$DOCS_DIR\temp", "$DOCS_DIR\output", "$DOCS_DIR\logs", "$DOCS_DIR\cache", "$DOCS_DIR\examples_output")
    foreach ($dir in $dirs) {
        if (Test-Path $dir) {
            Remove-Item "$dir\*" -Recurse -Force -ErrorAction SilentlyContinue
        }
    }
    Write-Host "Diretórios limpos com sucesso!" -ForegroundColor Green
}

function Run-Check-Structure {
    Print-Section "Verificar Estrutura"
    Get-ChildItem $DOCS_DIR | Format-Table Name, Mode
    Get-ChildItem "$DOCS_DIR\documentacao" | Format-Table Name, Mode
    Get-ChildItem "$DOCS_DIR\exemplos" | Format-Table Name, Mode
    Get-ChildItem "$DOCS_DIR\guias" | Format-Table Name, Mode
    Get-ChildItem "$DOCS_DIR\solucoes" | Format-Table Name, Mode
    Get-ChildItem "$DOCS_DIR\testes" | Format-Table Name, Mode
}

function Run-Full-Diagnose {
    Print-Header "Diagnóstico Completo"
    Run-Check
    Run-Check-Python
    Run-Check-FFmpeg
    Run-Check-ImageMagick
    Run-Test-MoviePy
    Run-Check-Structure
    Run-Diagnose-Simple
    Run-Diagnose
}

function Run-Full-Workflow {
    Print-Header "Workflow Completo"
    Run-Setup
    Run-Install-Deps
    Run-Create-Dirs
    Run-Full-Diagnose
    Run-Test
    Run-Examples
    Run-Report
    Write-Host "Workflow completo executado com sucesso!" -ForegroundColor Green
}