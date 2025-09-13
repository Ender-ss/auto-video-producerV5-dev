@echo off
:: Script para executar o instalador do MoviePy com permissões de administrador

:: Define cores para saída
set "GREEN=[92m"
set "RED=[91m"
set "BLUE=[94m"
set "RESET=[0m"

:: Exibe informações iniciais
cls
echo %BLUE%===================================================
echo                INSTALADOR MOVIEPY                
echo ===================================================%RESET%
echo 

echo %GREEN%Este script irá executar o instalador do MoviePy com permissões de administrador.
echo Isso é necessário para corrigir a instalação corrompida e garantir que o submódulo 'editor' funcione corretamente.%RESET%
echo 

echo %BLUE%Atenção:%RESET%
echo 1. Feche todas as janelas do Python, IDEs e terminais
if /i "%1" neq "-y" (
echo 2. Pressione qualquer tecla para continuar...
pause >nul
echo 
echo %RED%Aguarde enquanto o UAC solicita permissões de administrador...%RESET%
echo 
)

:: Verifica se já está em execução como administrador
NET SESSION >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    :: Já é administrador, executa o script diretamente
    echo %GREEN%Executando como administrador...%RESET%
    python instalar_moviepy_simplificado.py
) else (
    :: Não é administrador, solicita permissões
    echo %BLUE%Solicitando permissões de administrador...%RESET%
    powershell -Command "Start-Process 'cmd.exe' -ArgumentList '/c cd /d "%CD%" && python instalar_moviepy_simplificado.py' -Verb RunAs"
)

:: Aguarda o fechamento do processo
if %ERRORLEVEL% EQU 0 (
    echo %GREEN%
    echo Processo concluído. Pressione qualquer tecla para sair...%RESET%
) else (
    echo %RED%
    echo Ocorreu um erro durante a execução. Pressione qualquer tecla para sair...%RESET%
)
pause >nul