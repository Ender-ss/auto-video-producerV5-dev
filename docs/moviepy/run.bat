@echo off
rem Script em lote para MoviePy Documentation Manager
rem Este script facilita a execução dos scripts de documentação e testes do MoviePy no Windows

rem Definir variáveis
set PYTHON=python
set DOCS_DIR=docs\moviepy
set SCRIPTS_DIR=%DOCS_DIR%
set CONFIG_FILE=%DOCS_DIR%\CONFIG.json
set REQUIREMENTS_FILE=%DOCS_DIR%\requirements.txt
set SETUP_SCRIPT=%DOCS_DIR%\setup.py
set MAIN_SCRIPT=%DOCS_DIR%\SCRIPT_MAIN.py

rem Funções
:print_header
echo ==============================================================
echo %~1
echo ==============================================================
echo.
goto :eof

:print_section
echo ----------------------------------------
echo %~1
echo ----------------------------------------
echo.
goto :eof

:color_print
for /f "tokens=1,2 delims=#" %%a in ('"prompt #$H#$E# & echo on & for %%b in (1) do rem"') do (
  set "DEL=%%a"
)
<nul set /p ".=%DEL%" > "%~2"
findstr /v /a:%~1 /R "^$" "%~2" nul
del "%~2" > nul 2>&1
goto :eof

rem Verificar argumentos
if "%~1"=="" goto help
if "%~1"=="help" goto help
if "%~1"=="all" goto all
if "%~1"=="install" goto install
if "%~1"=="diagnose" goto diagnose
if "%~1"=="diagnose-simple" goto diagnose-simple
if "%~1"=="test" goto test
if "%~1"=="examples" goto examples
if "%~1"=="report" goto report
if "%~1"=="clean" goto clean
if "%~1"=="update" goto update
if "%~1"=="setup" goto setup
if "%~1"=="check" goto check
if "%~1"=="run" goto run
if "%~1"=="install-deps" goto install-deps
if "%~1"=="check-python" goto check-python
if "%~1"=="check-ffmpeg" goto check-ffmpeg
if "%~1"=="check-imagemagick" goto check-imagemagick
if "%~1"=="test-moviepy" goto test-moviepy
if "%~1"=="create-dirs" goto create-dirs
if "%~1"=="clean-dirs" goto clean-dirs
if "%~1"=="check-structure" goto check-structure
if "%~1"=="full-diagnose" goto full-diagnose
if "%~1"=="full-workflow" goto full-workflow

echo Comando não reconhecido: %~1
goto help

:help
call :print_header "Makefile para MoviePy Documentation Manager"
echo Uso:
echo   %~n0 [comando]
echo.
echo Comandos disponíveis:
echo   help          Mostra esta ajuda
echo   all           Executa todos os scripts
echo   install       Executa o script de instalação
echo   diagnose      Executa o script de diagnóstico
echo   diagnose-simple Executa o script de diagnóstico simplificado
echo   test          Executa os testes do MoviePy
echo   examples      Executa os exemplos do MoviePy
echo   report        Gera um relatório completo
echo   clean         Limpa arquivos temporários
echo   update        Atualiza a documentação
echo   setup         Configura o ambiente do MoviePy
echo   check         Verifica o ambiente
echo   run           Executa o script principal
echo   install-deps  Instala dependências
echo   check-python  Verifica Python
echo   check-ffmpeg  Verifica FFmpeg
echo   check-imagemagick Verifica ImageMagick
echo   test-moviepy  Testa MoviePy
echo   create-dirs   Cria diretórios
echo   clean-dirs    Limpa diretórios
echo   check-structure Verifica estrutura
echo   full-diagnose Executa diagnóstico completo
echo   full-workflow Executa workflow completo
echo.
goto :eof

:all
call :print_header "Executar Todos os Scripts"
%PYTHON% %MAIN_SCRIPT% --all
goto :eof

:install
call :print_header "Instalar e Configurar MoviePy"
%PYTHON% %MAIN_SCRIPT% --install
goto :eof

:diagnose
call :print_header "Diagnóstico do MoviePy"
%PYTHON% %MAIN_SCRIPT% --diagnose
goto :eof

:diagnose-simple
call :print_header "Diagnóstico Simplificado do MoviePy"
echo Executando diagnóstico simplificado...
cd %DOCS_DIR%
echo Diretório atual: %CD%
echo Executando: %PYTHON% solucoes\SCRIPT_DIAGNOSTICO_SIMPLIFICADO.py
%PYTHON% solucoes\SCRIPT_DIAGNOSTICO_SIMPLIFICADO.py
cd ..\..
goto :eof

:test
call :print_header "Testes do MoviePy"
%PYTHON% %MAIN_SCRIPT% --test
goto :eof

:examples
call :print_header "Exemplos do MoviePy"
%PYTHON% %MAIN_SCRIPT% --examples
goto :eof

:report
call :print_header "Relatório do MoviePy"
%PYTHON% %MAIN_SCRIPT% --report
goto :eof

:clean
call :print_header "Limpar Arquivos Temporários"
%PYTHON% %MAIN_SCRIPT% --clean
goto :eof

:update
call :print_header "Atualizar Documentação"
%PYTHON% %MAIN_SCRIPT% --update
goto :eof

:setup
call :print_header "Configurar Ambiente do MoviePy"
%PYTHON% %SETUP_SCRIPT%
goto :eof

:check
call :print_header "Verificar Ambiente"
if not exist "%CONFIG_FILE%" (
    echo Arquivo de configuração não encontrado: %CONFIG_FILE%
    exit /b 1
)
if not exist "%REQUIREMENTS_FILE%" (
    echo Arquivo requirements.txt não encontrado: %REQUIREMENTS_FILE%
    exit /b 1
)
if not exist "%SETUP_SCRIPT%" (
    echo Script setup.py não encontrado: %SETUP_SCRIPT%
    exit /b 1
)
if not exist "%MAIN_SCRIPT%" (
    echo Script principal não encontrado: %MAIN_SCRIPT%
    exit /b 1
)
echo Todos os arquivos necessários estão presentes!
goto :eof

:run
call :print_header "Executar Script Principal"
%PYTHON% %MAIN_SCRIPT%
goto :eof

:install-deps
call :print_header "Instalar Dependências"
echo Instalando dependências do requirements.txt...
%PYTHON% -m pip install -r %REQUIREMENTS_FILE%
echo Dependências instaladas com sucesso!
goto :eof

:check-python
call :print_section "Verificar Python"
%PYTHON% --version
goto :eof

:check-ffmpeg
call :print_section "Verificar FFmpeg"
ffmpeg -version
goto :eof

:check-imagemagick
call :print_section "Verificar ImageMagick"
magick -version
goto :eof

:test-moviepy
call :print_section "Testar MoviePy"
%PYTHON% -c "import moviepy.editor as mpy; print('MoviePy está funcionando!')"
goto :eof

:create-dirs
call :print_section "Criar Diretórios"
if not exist "%DOCS_DIR%\temp" mkdir "%DOCS_DIR%\temp"
if not exist "%DOCS_DIR%\output" mkdir "%DOCS_DIR%\output"
if not exist "%DOCS_DIR%\logs" mkdir "%DOCS_DIR%\logs"
if not exist "%DOCS_DIR%\cache" mkdir "%DOCS_DIR%\cache"
if not exist "%DOCS_DIR%\examples_output" mkdir "%DOCS_DIR%\examples_output"
echo Diretórios criados com sucesso!
goto :eof

:clean-dirs
call :print_section "Limpar Diretórios"
if exist "%DOCS_DIR%\temp\*." del /Q "%DOCS_DIR%\temp\*."
if exist "%DOCS_DIR%\output\*." del /Q "%DOCS_DIR%\output\*."
if exist "%DOCS_DIR%\logs\*." del /Q "%DOCS_DIR%\logs\*."
if exist "%DOCS_DIR%\cache\*." del /Q "%DOCS_DIR%\cache\*."
if exist "%DOCS_DIR%\examples_output\*." del /Q "%DOCS_DIR%\examples_output\*."
echo Diretórios limpos com sucesso!
goto :eof

:check-structure
call :print_section "Verificar Estrutura"
dir %DOCS_DIR%
dir %DOCS_DIR%\documentacao
dir %DOCS_DIR%\exemplos
dir %DOCS_DIR%\guias
dir %DOCS_DIR%\solucoes
dir %DOCS_DIR%\testes
goto :eof

:full-diagnose
call :print_header "Diagnóstico Completo"
call :check
call :check-python
call :check-ffmpeg
call :check-imagemagick
call :test-moviepy
call :check-structure
call :diagnose-simple
call :diagnose
goto :eof

:full-workflow
call :print_header "Workflow Completo"
call :setup
call :install-deps
call :create-dirs
call :full-diagnose
call :test
call :examples
call :report
echo Workflow completo executado com sucesso!
goto :eof