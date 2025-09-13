@echo off
SET "PYTHON_EXE=C:\Program Files\Python313\python.exe"
SET "PIP_EXE=%PYTHON_EXE% -m pip"
SET "TARGET_VERSION=2.2.1"

:: Verificar se está sendo executado como administrador
NET SESSION >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    ECHO ERRO: Este script precisa ser executado como ADMINISTRADOR!
    ECHO Por favor, clique com o botão direito e selecione "Executar como administrador"
    PAUSE
    EXIT /B 1
)

ECHO ====================================================
ECHO           REINSTALAÇÃO COMPLETA DO MOVIEPY
ECHO ====================================================
ECHO Data/Hora: %DATE% %TIME%
ECHO Executando com permissões de administrador
ECHO Python: %PYTHON_EXE%
ECHO ====================================================

:: Parar todos os processos Python
ECHO.
ECHO [1/6] PARANDO PROCESSOS PYTHON...
TASKKILL /F /IM python.exe >nul 2>&1
TASKKILL /F /IM pythonw.exe >nul 2>&1
ECHO Processos Python encerrados.

:: Localizar e remover instalações do MoviePy
ECHO.
ECHO [2/6] REMOVENDO INSTALAÇÕES EXISTENTES DO MOVIEPY...

:: Listar todos os diretórios Python
FOR %%G IN ("C:\Users\%USERNAME%\AppData\Roaming\Python\Python313\site-packages", "C:\Program Files\Python313\Lib\site-packages") DO (
    IF EXIST "%%G" (
        ECHO Verificando diretório: %%G
        
        :: Remover diretório do MoviePy
        IF EXIST "%%G\moviepy" (
            ECHO Removendo diretório: %%G\moviepy
            RMDIR /S /Q "%%G\moviepy" >nul 2>&1
            IF %ERRORLEVEL% EQU 0 (
                ECHO   - Removido com sucesso
            ) ELSE (
                ECHO   - ERRO ao remover
            )
        )
        
        :: Remover arquivos .egg-info e .dist-info
        FOR %%F IN ("%%G\moviepy-*.egg-info", "%%G\moviepy-*.dist-info") DO (
            IF EXIST "%%F" (
                ECHO Removendo: %%F
                RMDIR /S /Q "%%F" >nul 2>&1
                IF %ERRORLEVEL% EQU 0 (
                    ECHO   - Removido com sucesso
                ) ELSE (
                    ECHO   - ERRO ao remover
                )
            )
        )
    )
)

:: Limpar cache do pip
ECHO.
ECHO [3/6] LIMPAR CACHE DO PIP...
%PIP_EXE% cache purge >nul 2>&1
ECHO Cache do pip limpo.

:: Atualizar o pip
ECHO.
ECHO [4/6] ATUALIZANDO O PIP...
%PIP_EXE% install --upgrade pip >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    ECHO Pip atualizado com sucesso.
) ELSE (
    ECHO ATENÇÃO: Não foi possível atualizar o pip, mas continuando com a instalação.
)

:: Instalar dependências essenciais
ECHO.
ECHO [5/6] INSTALANDO DEPENDÊNCIAS ESSENCIAIS...
%PIP_EXE% install --force-reinstall --no-cache-dir numpy imageio pillow decorator proglog tqdm >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    ECHO Dependências instaladas com sucesso.
) ELSE (
    ECHO ATENÇÃO: Erro na instalação de dependências, mas continuando.
)

:: Instalar a versão correta do MoviePy
ECHO.
ECHO [6/6] INSTALANDO MOVIEPY VERSÃO %TARGET_VERSION%...
%PIP_EXE% install --force-reinstall --no-cache-dir moviepy==%TARGET_VERSION% >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    ECHO MoviePy %TARGET_VERSION% instalado com sucesso!
) ELSE (
    ECHO ERRO: Falha na instalação do MoviePy %TARGET_VERSION%!
)

:: Criar script de verificação final
ECHO.
ECHO CRIANDO SCRIPT DE VERIFICAÇÃO FINAL...
> "%~dp0\verificar_instalacao_definitiva.py" (
    ECHO import sys
    ECHO import os
    ECHO
    ECHO print("===== VERIFICAÇÃO DEFINITIVA DO MOVIEPY =====")
    ECHO
    ECHO try:
    ECHO     import moviepy
    ECHO     print(f"MoviePy importado com sucesso! Versão: {{moviepy.__version__}}")
    ECHO     print(f"Localização: {{os.path.dirname(moviepy.__file__)}}")
    ECHO     
    ECHO     try:
    ECHO         from moviepy import editor
    ECHO         print("\n✅ SUBMÓDULO 'EDITOR' IMPORTADO COM SUCESSO!")
    ECHO         print("🎉 A INSTALAÇÃO DO MOVIEPY ESTÁ COMPLETA E FUNCIONANDO!")
    ECHO         print("\nVocê pode agora executar sua aplicação auto-video-producerV5-dev.")
    ECHO         sys.exit(0)
    ECHO     except ImportError as e:
    ECHO         print("\n❌ ERRO: Não foi possível importar o submódulo 'editor'!")
    ECHO         print(f"Detalhes: {{str(e)}}")
    ECHO         moviepy_dir = os.path.dirname(moviepy.__file__)
    ECHO         print(f"\nConteúdo do diretório {{moviepy_dir}}:")
    ECHO         for item in os.listdir(moviepy_dir):
    ECHO             print(f"- {{item}}")
    ECHO         sys.exit(1)
    ECHO except ImportError as e:
    ECHO     print("\n❌ ERRO: Não foi possível importar o MoviePy!")
    ECHO     print(f"Detalhes: {{str(e)}}")
    ECHO     sys.exit(1)
)

:: Executar verificação final
ECHO.
ECHO EXECUTANDO VERIFICAÇÃO DEFINITIVA...
%PYTHON_EXE% "%~dp0\verificar_instalacao_definitiva.py"
SET "VERIFY_RESULT=%ERRORLEVEL%"

:: Exibir resultados finais
ECHO.
ECHO ====================================================
ECHO                  RESULTADO FINAL
ECHO ====================================================
IF %VERIFY_RESULT% EQU 0 (
    ECHO 🎊 SUCCESSO! A instalação do MoviePy %TARGET_VERSION% está completa e funcionando.
    ECHO O submódulo 'editor' está disponível para uso.
) ELSE (
    ECHO ❌ FALHA! A instalação do MoviePy ainda está com problemas.
    ECHO Sugestão: Reinicie o computador e execute este script novamente como ADMINISTRADOR.
)
ECHO ====================================================
PAUSE