
@echo off
cls
echo Executando limpeza radical do MoviePy com permissões de administrador...

rem 1. Parar processos Python que possam estar usando o MoviePy
echo 1. Parando processos Python que possam estar usando o MoviePy...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im pythonw.exe >nul 2>&1

echo.
echo 2. Removendo diretório do MoviePy...
if exist "C:\Users\Enderson\AppData\Roaming\Python\Python313\site-packages\moviepy" (
    rd /s /q "C:\Users\Enderson\AppData\Roaming\Python\Python313\site-packages\moviepy"
    if errorlevel 1 (
        echo ❌ Erro ao remover diretório. Tentando com outro método...
        takeown /f "C:\Users\Enderson\AppData\Roaming\Python\Python313\site-packages\moviepy" /r /d y >nul 2>&1
        icacls "C:\Users\Enderson\AppData\Roaming\Python\Python313\site-packages\moviepy" /grant administrators:F /t >nul 2>&1
        rd /s /q "C:\Users\Enderson\AppData\Roaming\Python\Python313\site-packages\moviepy"
    )
)

echo 3. Removendo arquivos .egg-info do MoviePy...
pushd "C:\Users\Enderson\AppData\Roaming\Python\Python313\site-packages"
for /d %%d in (moviepy-*.egg-info) do (
    echo   Removendo: %%d
    rd /s /q "%%d"
)
popd

echo 4. Removendo outros vestígios do MoviePy...
del /f /q "C:\Users\Enderson\AppData\Roaming\Python\Python313\site-packages\moviepy*.dist-info" >nul 2>&1
del /f /q "C:\Users\Enderson\AppData\Roaming\Python\Python313\site-packages\moviepy*.py" >nul 2>&1

echo.
echo 5. Reinstalando o MoviePy corretamente...
echo Executando: pip install moviepy==2.2.1 --force-reinstall --no-cache-dir --user
"C:\Program Files\Python313\python.exe" -m pip install moviepy==2.2.1 --force-reinstall --no-cache-dir --user

if errorlevel 1 (
    echo.
    echo ❌ Erro na reinstalação! Verifique as permissões.
    pause
    exit /b 1
)

echo.
echo 6. Verificando a instalação...
"C:\Program Files\Python313\python.exe" -c "import moviepy; print('MoviePy importado com sucesso! Versão:', moviepy.__version__); import moviepy.editor; print('Módulo editor importado com sucesso!'); from moviepy.editor import VideoFileClip; print('Métodos necessários:', 'with_audio' in dir(VideoFileClip), 'set_audio' in dir(VideoFileClip))"

if errorlevel 1 (
    echo.
    echo ❌ Ainda há problemas com a instalação do MoviePy.
    pause
    exit /b 1
)

echo.
echo 🎉 Instalação do MoviePy concluída com SUCESSO! 🎉
echo O MoviePy 2.2.1 está funcionando corretamente.
echo.
echo Pressione qualquer tecla para sair...
pause >nul
