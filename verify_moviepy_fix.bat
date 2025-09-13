@echo off

REM Verificando instalação do MoviePy usando pip
echo Verificando instalação do MoviePy...
pip show moviepy > moviepy_check.txt 2>&1
if %errorlevel% equ 0 (
    echo ✅ MoviePy está instalado!
    echo Veja os detalhes em moviepy_check.txt
) else (
    echo ❌ MoviePy NÃO está instalado!
    echo Execute: pip install moviepy
)

echo.
REM Verificando correção no arquivo video_creation_service.py
echo Verificando correção no arquivo video_creation_service.py...
findstr /C:"with_audio" backend\services\video_creation_service.py > find_result.txt 2>&1
if %errorlevel% equ 0 (
    echo ✅ A correção WITH_AUDIO foi encontrada no arquivo!
    echo Veja a linha em find_result.txt
) else (
    echo ❌ A correção WITH_AUDIO NÃO foi encontrada!
    echo Verifique se a linha 132 foi alterada de set_audio para with_audio
)

echo.
echo Verificando se ainda existe set_audio no arquivo...
findstr /C:"set_audio" backend\services\video_creation_service.py > find_set_result.txt 2>&1
if %errorlevel% equ 0 (
    echo ⚠️ Ainda existe set_audio no arquivo!
    echo Verifique find_set_result.txt para localizações
) else (
    echo ✅ Nenhum set_audio encontrado no arquivo!
)

echo.
echo Verificação concluída.
pause