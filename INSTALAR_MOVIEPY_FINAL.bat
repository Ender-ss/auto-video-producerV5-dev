@echo off
cls
echo =======================================================================
echo               INSTALAÇÃO FINAL E COMPLETA DO MOVIEPY                  
echo =======================================================================
echo.
echo ATENÇÃO: Este script deve ser executado com PERMISSÕES DE ADMINISTRADOR
echo.
echo. & pause

REM 1. Parar todos os processos Python que possam estar usando o MoviePy
echo [1/6] Parando processos Python...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im pythonw.exe >nul 2>&1
echo.

REM 2. Remover completamente o diretório do MoviePy e seus vestígios
echo [2/6] Removendo todos os vestígios do MoviePy...
set "MOVIEPY_DIR=C:\Users\Enderson\AppData\Roaming\Python\Python313\site-packages\moviepy"
set "SITE_PACKAGES=C:\Users\Enderson\AppData\Roaming\Python\Python313\site-packages"

echo   Removendo diretório principal do MoviePy...
if exist "%MOVIEPY_DIR%" (
    takeown /f "%MOVIEPY_DIR%" /r /d y >nul 2>&1
    icacls "%MOVIEPY_DIR%" /grant administrators:F /t >nul 2>&1
    rd /s /q "%MOVIEPY_DIR%"
    echo   - Diretório removido com sucesso
) else (
    echo   - Diretório não encontrado
)

echo   Removendo arquivos .egg-info e .dist-info...
pushd "%SITE_PACKAGES%"
for /d %%d in (moviepy-*.egg-info moviepy-*.dist-info) do (
    echo   - Removendo: %%d
    rd /s /q "%%d"
)
popd

echo   Removendo outros arquivos relacionados...
del /f /q "%SITE_PACKAGES%\moviepy*.py" >nul 2>&1
del /f /q "%SITE_PACKAGES%\moviepy*.pyc" >nul 2>&1

echo.

REM 3. Atualizar o pip para a versão mais recente
echo [3/6] Atualizando o pip...
python -m pip install --upgrade pip --user
echo.

REM 4. Instalar dependências essenciais
echo [4/6] Instalando dependências essenciais...
echo   Instalando pillow (faltando)...
python -m pip install pillow==11.3.0 --force-reinstall --no-cache-dir --user
echo   Instalando outras dependências...
python -m pip install numpy==2.3.3 imageio==2.37.0 imageio-ffmpeg==0.6.0 decorator==5.2.1 proglog==0.1.12 tqdm==4.67.1 colorama==0.4.6 --force-reinstall --no-cache-dir --user
echo.

REM 5. Instalar o MoviePy 2.2.1 corretamente
echo [5/6] Instalando o MoviePy 2.2.1 corretamente...
python -m pip install moviepy==2.2.1 --force-reinstall --no-cache-dir --user
echo.

REM 6. Verificar a instalação final
echo [6/6] Verificando a instalação final...
echo.
echo Testando importação do MoviePy e do submódulo editor...
echo.
python -c "import sys; print('Python:', sys.version); try: import moviepy; print('MoviePy versão:', moviepy.__version__); print('Localização:', moviepy.__file__); try: from moviepy import editor; print('✓ Módulo editor importado com sucesso!'); from moviepy.editor import VideoFileClip; print('✓ Classe VideoFileClip importada!'); print('✓ Métodos: with_audio='+str(hasattr(VideoFileClip, 'with_audio'))+', set_audio='+str(hasattr(VideoFileClip, 'set_audio'))); except ImportError as e: print('✗ Erro editor:', e); except Exception as e: print('✗ Erro geral:', e); else: print('\n🎉 INSTALAÇÃO CONCLUÍDA COM SUCESSO! 🎉');" > verificacao_result.txt

type verificacao_result.txt

echo.
echo =======================================================================
echo                           RESULTADO FINAL

echo. & pause
cls
echo =======================================================================
echo                        INSTRUÇÕES FINAIS

echo.
IF EXIST "verificacao_result.txt" (
    FINDSTR /C:"INSTALAÇÃO CONCLUÍDA COM SUCESSO" verificacao_result.txt >nul
    IF %ERRORLEVEL% EQU 0 (
        echo 🎉 PARABÉNS! A INSTALAÇÃO DO MOVIEPY FOI CONCLUÍDA COM SUCESSO!
        echo.
        echo O MoviePy 2.2.1 está funcionando corretamente e o submódulo editor está disponível.
        echo Você pode prosseguir com a execução da sua pipeline de produção de vídeo.
    ) ELSE (
        echo ❌ AINDA HÁ PROBLEMAS COM A INSTALAÇÃO DO MOVIEPY.
        echo.
        echo Recomendamos:
        echo 1. Reinstalar o Python completamente
        echo 2. Usar um ambiente virtual limpo
        echo 3. Instalar o MoviePy com: pip install moviepy==2.2.1 --user
    )
)

echo.
echo Pressione qualquer tecla para sair...
DEL /F /Q verificacao_result.txt >nul 2>&1
pause >nul