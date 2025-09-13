@echo off

REM Script batch para verificar e instalar o MoviePy após reinstalação do Python

REM Defina o caminho do Python principal
SET PYTHON_PATH="C:\Program Files\Python313\python.exe"

REM Verifique se o Python existe
IF NOT EXIST %PYTHON_PATH% (
    ECHO Python não encontrado em %PYTHON_PATH%
    ECHO Verificando outras instalações...
    WHERE python > python_path.txt 2>nul
    IF NOT ERRORLEVEL 1 (
        SET /P PYTHON_PATH=<python_path.txt
        DEL python_path.txt
        ECHO Python encontrado em: %PYTHON_PATH%
    ) ELSE (
        ECHO Python não está instalado corretamente!
        PAUSE
        EXIT /B 1
    )
)

REM Execute o script Python de verificação
ECHO Executando verificação do MoviePy...
%PYTHON_PATH% install_and_verify.py

REM Limpeza
ECHO.
ECHO Verificação concluída. Pressione qualquer tecla para sair.
PAUSE >nul