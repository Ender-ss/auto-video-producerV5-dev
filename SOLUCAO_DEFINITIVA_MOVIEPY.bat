@echo off
SETLOCAL ENABLEEXTENSIONS ENABLEDELAYEDEXPANSION

:: Configurações
SET "PYTHON_EXE=C:\Program Files\Python313\python.exe"
SET "PIP_EXE=%PYTHON_EXE% -m pip"
SET "TARGET_VERSION=2.2.1"
SET "LOG_FILE=%~dp0\moviepy_fix_log.txt"
SET "TEMP_DIR=%TEMP%\moviepy_fix"

:: Limpar log anterior
IF EXIST "%LOG_FILE%" (DEL "%LOG_FILE%" /Q >nul 2>&1)

:: Função para registrar logs
:LOG
ECHO [%DATE% %TIME%] %* >> "%LOG_FILE%"
ECHO %* 
GOTO :EOF

:: Verificar permissões de administrador
NET SESSION >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    CALL :LOG "ERRO: Execute como ADMINISTRADOR!"
    CALL :LOG "Clique com o botão direito e selecione 'Executar como administrador'"
    PAUSE
    EXIT /B 1
)

CALL :LOG "==================================================="
CALL :LOG "            SOLUÇÃO DEFINITIVA - MOVIEPY            "
CALL :LOG "==================================================="
CALL :LOG "Python: %PYTHON_EXE%"
CALL :LOG "Versão-alvo: %TARGET_VERSION%"
CALL :LOG "==================================================="

:: Criar diretório temporário
MKDIR "%TEMP_DIR%" >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    CALL :LOG "ATENÇÃO: Não foi possível criar diretório temporário. Continuando..."
)

:: Passo 1: Parar todos os processos Python
CALL :LOG ""
CALL :LOG "[1/8] PARANDO PROCESSOS PYTHON..."
TASKKILL /F /IM python.exe >nul 2>&1
TASKKILL /F /IM pythonw.exe >nul 2>&1
CALL :LOG "Processos Python encerrados."

:: Passo 2: Identificar todos os diretórios de instalação do Python
CALL :LOG ""
CALL :LOG "[2/8] IDENTIFICANDO DIRETÓRIOS DE INSTALAÇÃO DO PYTHON..."

:: Criar script para listar todos os diretórios do site-packages
> "%TEMP_DIR%\list_python_paths.py" (
    ECHO import sys
    ECHO import os
    ECHO print('\n'.join(sys.path))
)

:: Executar script e capturar saída
FOR /F "tokens=* delims=" %%G IN ('%PYTHON_EXE% "%TEMP_DIR%\list_python_paths.py" 2^>^&1') DO (
    IF "%%G" NEQ "" (
        SET "PYTHON_PATH=%%G"
        IF EXIST "!PYTHON_PATH!\site-packages" (
            SET "SITE_PACKAGES_PATHS=!SITE_PACKAGES_PATHS!"!PYTHON_PATH!\site-packages" "
        )
    )
)

:: Adicionar caminhos comuns
SET "SITE_PACKAGES_PATHS=%SITE_PACKAGES_PATHS%"C:\Users\%USERNAME%\AppData\Roaming\Python\Python313\site-packages" "C:\Program Files\Python313\Lib\site-packages" ""

CALL :LOG "Diretórios site-packages identificados:" 
FOR %%G IN (%SITE_PACKAGES_PATHS%) DO (
    IF EXIST "%%~G" (
        CALL :LOG "- %%~G"
    )
)

:: Passo 3: Remover instalações existentes do MoviePy
CALL :LOG ""
CALL :LOG "[3/8] REMOVENDO INSTALAÇÕES EXISTENTES DO MOVIEPY..."

:: Remover via pip primeiro
%PIP_EXE% uninstall -y moviepy >nul 2>&1
CALL :LOG "Tentativa de desinstalação via pip concluída."

:: Remover manualmente todos os vestígios
FOR %%G IN (%SITE_PACKAGES_PATHS%) DO (
    IF EXIST "%%~G" (
        CALL :LOG "Limpando diretório: %%~G"
        
        :: Remover diretório moviepy
        IF EXIST "%%~G\moviepy" (
            CALL :LOG "  - Removendo diretório: moviepy"
            RMDIR /S /Q "%%~G\moviepy" >nul 2>&1
            IF !ERRORLEVEL! EQU 0 (
                CALL :LOG "    - Removido com sucesso"
            ) ELSE (
                CALL :LOG "    - ERRO ao remover (permissões?)"
                TAKEOWN /F "%%~G\moviepy" /R /D Y >nul 2>&1
                ICACLS "%%~G\moviepy" /GRANT *S-1-5-32-544:F /T >nul 2>&1
                RMDIR /S /Q "%%~G\moviepy" >nul 2>&1
                IF !ERRORLEVEL! EQU 0 (
                    CALL :LOG "    - Removido após alteração de permissões"
                )
            )
        )
        
        :: Remover arquivos .egg-info e .dist-info
        FOR %%F IN ("%%~G\moviepy-*.egg-info", "%%~G\moviepy-*.dist-info") DO (
            IF EXIST "%%~F" (
                CALL :LOG "  - Removendo: %%~nxF"
                RMDIR /S /Q "%%~F" >nul 2>&1
                IF !ERRORLEVEL! EQU 0 (
                    CALL :LOG "    - Removido com sucesso"
                ) ELSE (
                    CALL :LOG "    - ERRO ao remover"
                )
            )
        )
    )
)

:: Passo 4: Limpar cache do pip
CALL :LOG ""
CALL :LOG "[4/8] LIMPAR CACHE DO PIP..."
%PIP_EXE% cache purge >nul 2>&1
CALL :LOG "Cache do pip limpo."

:: Passo 5: Atualizar o pip
CALL :LOG ""
CALL :LOG "[5/8] ATUALIZANDO O PIP..."
%PIP_EXE% install --upgrade pip >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    CALL :LOG "Pip atualizado com sucesso."
) ELSE (
    CALL :LOG "ATENÇÃO: Não foi possível atualizar o pip, mas continuando."
)

:: Passo 6: Instalar dependências essenciais
CALL :LOG ""
CALL :LOG "[6/8] INSTALANDO DEPENDÊNCIAS ESSENCIAIS..."
%PIP_EXE% install --force-reinstall --no-cache-dir numpy imageio pillow decorator proglog tqdm >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    CALL :LOG "Dependências instaladas com sucesso."
) ELSE (
    CALL :LOG "ATENÇÃO: Erro na instalação de dependências, mas continuando."
)

:: Passo 7: Instalar a versão correta do MoviePy com caminho explícito
CALL :LOG ""
CALL :LOG "[7/8] INSTALANDO MOVIEPY VERSÃO %TARGET_VERSION%..."
%PIP_EXE% install --force-reinstall --no-cache-dir moviepy==%TARGET_VERSION% >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    CALL :LOG "MoviePy %TARGET_VERSION% instalado com sucesso!"
) ELSE (
    CALL :LOG "ERRO: Falha na instalação do MoviePy %TARGET_VERSION%!"
)

:: Passo 8: Criar e executar script de verificação abrangente
CALL :LOG ""
CALL :LOG "[8/8] EXECUTANDO VERIFICAÇÃO DEFINITIVA..."

:: Criar script de verificação
> "%TEMP_DIR%\verificacao_definitiva.py" (
    ECHO import sys
    ECHO import os
    ECHO import importlib.util
    ECHO
    ECHO print("===== VERIFICAÇÃO DEFINITIVA DO MOVIEPY =====")
    ECHO
    ECHO # Verificar caminho do Python
    ECHO print(f"Caminho do Python: {{sys.executable}}")
    ECHO print("\nCaminhos de importação:")
    ECHO for path in sys.path:
    ECHO     print(f"- {{path}}")
    ECHO
    ECHO try:
    ECHO     # Importar MoviePy
    ECHO     import moviepy
    ECHO     print(f"\nMoviePy importado com sucesso! Versão: {{moviepy.__version__}}")
    ECHO     print(f"Localização: {{os.path.dirname(moviepy.__file__)}}")
    ECHO     
    ECHO     # Verificar conteúdo do diretório
    ECHO     moviepy_dir = os.path.dirname(moviepy.__file__)
    ECHO     print(f"\nConteúdo do diretório {{moviepy_dir}}:")
    ECHO     for item in os.listdir(moviepy_dir):
    ECHO         print(f"- {{item}}")
    ECHO     
    ECHO     # Verificar existência do arquivo editor.py
    ECHO     editor_path = os.path.join(moviepy_dir, 'editor.py')
    ECHO     if os.path.exists(editor_path):
    ECHO         print(f"\n✅ O arquivo editor.py existe em: {{editor_path}}")
    ECHO     else:
    ECHO         print(f"\n❌ O arquivo editor.py NÃO existe em: {{editor_path}}")
    ECHO         sys.exit(1)
    ECHO     
    ECHO     # Tentar importar submódulo editor
    ECHO     try:
    ECHO         from moviepy import editor
    ECHO         print("\n✅ SUBMÓDULO 'EDITOR' IMPORTADO COM SUCESSO!")
    ECHO         
    ECHO         # Verificar métodos essenciais
    ECHO         print("\nVerificando métodos essenciais:")
    ECHO         has_video_file_clip = hasattr(editor, 'VideoFileClip')
    ECHO         has_with_audio = hasattr(editor, 'with_audio') or (hasattr(editor.VideoFileClip, 'with_audio') if has_video_file_clip else False)
    ECHO         has_set_audio = hasattr(editor, 'set_audio') or (hasattr(editor.VideoFileClip, 'set_audio') if has_video_file_clip else False)
    ECHO         
    ECHO         print(f"- VideoFileClip: {{'✓' if has_video_file_clip else '✗'}}")
    ECHO         print(f"- with_audio: {{'✓' if has_with_audio else '✗'}}")
    ECHO         print(f"- set_audio: {{'✓' if has_set_audio else '✗'}}")
    ECHO         
    ECHO         if has_video_file_clip and has_with_audio and has_set_audio:
    ECHO             print("\n🎉 A INSTALAÇÃO DO MOVIEPY ESTÁ 100%% FUNCIONANDO!")
    ECHO             print("\nVocê pode executar sua aplicação auto-video-producerV5-dev.")
    ECHO             sys.exit(0)
    ECHO         else:
    ECHO             print("\n⚠️  A instalação está parcialmente correta, mas alguns métodos estão faltando.")
    ECHO             sys.exit(1)
    ECHO     except ImportError as e:
    ECHO         print(f"\n❌ ERRO: Não foi possível importar o submódulo 'editor'!")
    ECHO         print(f"Detalhes: {{str(e)}}")
    ECHO         sys.exit(1)
    ECHO except ImportError as e:
    ECHO     print("\n❌ ERRO: Não foi possível importar o MoviePy!")
    ECHO     print(f"Detalhes: {{str(e)}}")
    ECHO     sys.exit(1)
)

:: Executar verificação e capturar resultado
%PYTHON_EXE% "%TEMP_DIR%\verificacao_definitiva.py" >> "%LOG_FILE%" 2>&1
SET "VERIFY_RESULT=%ERRORLEVEL%"

:: Exibir resumo da verificação
CALL :LOG ""
CALL :LOG "==================================================="
CALL :LOG "                  RESULTADO FINAL                  "
CALL :LOG "==================================================="
IF %VERIFY_RESULT% EQU 0 (
    CALL :LOG "🎊 SUCCESSO! A instalação do MoviePy %TARGET_VERSION% está 100%% funcionando!"
    CALL :LOG "✅ O submódulo 'editor' está totalmente disponível."
    CALL :LOG "✅ Todos os métodos essenciais foram verificados."
    CALL :LOG "\nAcesse o arquivo de log para mais detalhes:"
    CALL :LOG "  %LOG_FILE%"
) ELSE (
    CALL :LOG "❌ FALHA! A instalação do MoviePy ainda está com problemas."
    CALL :LOG "\nSugestões para resolver:":
    CALL :LOG "1. Reinicie o computador e execute este script novamente como ADMINISTRADOR"
    CALL :LOG "2. Verifique as permissões de seus diretórios do Python"
    CALL :LOG "3. Consulte o arquivo de log para mais detalhes:"
    CALL :LOG "   %LOG_FILE%"
)
CALL :LOG "==================================================="

:: Limpar diretório temporário
RMDIR /S /Q "%TEMP_DIR%" >nul 2>&1

ECHO.
ECHO Pressione qualquer tecla para sair...
PAUSE >nul
EXIT /B %VERIFY_RESULT%