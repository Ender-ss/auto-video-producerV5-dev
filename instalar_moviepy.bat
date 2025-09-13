@echo off
setlocal enabledelayedexpansion

REM Defina o caminho do Python (ajuste se necessário)
SET PYTHON_EXE="C:\Program Files\Python313\python.exe"

REM Verifique se o Python existe
IF NOT EXIST %PYTHON_EXE% (
    echo Python não encontrado em %PYTHON_EXE%
    echo Procurando por outras instalações...
    WHERE python > python_path.txt 2>nul
    IF NOT ERRORLEVEL 1 (
        SET /P PYTHON_PATH=<python_path.txt
        DEL python_path.txt
        SET PYTHON_EXE="!PYTHON_PATH!"
        echo Python encontrado em: !PYTHON_EXE!
    ) ELSE (
        echo Python não está instalado corretamente!
        PAUSE
        EXIT /B 1
    )
)

REM Atualiza o pip
echo Atualizando o pip...
%PYTHON_EXE% -m pip install --upgrade pip

REM Instala dependências

echo Instalando dependências essenciais...
%PYTHON_EXE% -m pip install decorator imageio imageio-ffmpeg numpy pillow proglog tqdm

REM Instala o MoviePy

echo Instalando o MoviePy...
%PYTHON_EXE% -m pip install moviepy --force-reinstall --no-cache-dir

REM Configura o FFmpeg

echo Configurando o FFmpeg...
echo import imageio; imageio.plugins.ffmpeg.download() > download_ffmpeg.py
%PYTHON_EXE% download_ffmpeg.py
DEL download_ffmpeg.py

REM Verifica a instalação
echo.
echo Executando verificação final...
echo import moviepy; from moviepy.editor import VideoFileClip; print("Instalação concluída com sucesso!"); > verify_final.py
%PYTHON_EXE% verify_final.py
DEL verify_final.py

echo.
echo ===================================================
echo Instalação do MoviePy concluída!
echo Por favor, verifique se não houve erros acima.
echo Após a conclusão, execute o arquivo verificar_moviepy.py para uma verificação mais completa.
echo ===================================================
PAUSE