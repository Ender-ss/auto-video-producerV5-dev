import os
import sys

print("===== Reinstalação Radical do MoviePy =====")
print(f"Python sendo usado: {sys.executable}")

# Caminho para o diretório do MoviePy
moviepy_dir = r"C:\Users\Enderson\AppData\Roaming\Python\Python313\site-packages\moviepy"
site_packages = r"C:\Users\Enderson\AppData\Roaming\Python\Python313\site-packages"

# Cria um script batch que será executado com permissões de administrador
batch_content = f'''
@echo off
cls
echo Executando limpeza radical do MoviePy com permissões de administrador...

rem 1. Parar processos Python que possam estar usando o MoviePy
echo 1. Parando processos Python que possam estar usando o MoviePy...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im pythonw.exe >nul 2>&1

echo.
echo 2. Removendo diretório do MoviePy...
if exist "{moviepy_dir}" (
    rd /s /q "{moviepy_dir}"
    if errorlevel 1 (
        echo ❌ Erro ao remover diretório. Tentando com outro método...
        takeown /f "{moviepy_dir}" /r /d y >nul 2>&1
        icacls "{moviepy_dir}" /grant administrators:F /t >nul 2>&1
        rd /s /q "{moviepy_dir}"
    )
)

echo 3. Removendo arquivos .egg-info do MoviePy...
pushd "{site_packages}"
for /d %%d in (moviepy-*.egg-info) do (
    echo   Removendo: %%d
    rd /s /q "%%d"
)
popd

echo 4. Removendo outros vestígios do MoviePy...
del /f /q "{site_packages}\moviepy*.dist-info" >nul 2>&1
del /f /q "{site_packages}\moviepy*.py" >nul 2>&1

echo.
echo 5. Reinstalando o MoviePy corretamente...
echo Executando: pip install moviepy==2.2.1 --force-reinstall --no-cache-dir --user
"{sys.executable}" -m pip install moviepy==2.2.1 --force-reinstall --no-cache-dir --user

if errorlevel 1 (
    echo.
    echo ❌ Erro na reinstalação! Verifique as permissões.
    pause
    exit /b 1
)

echo.
echo 6. Verificando a instalação...
"{sys.executable}" -c "import moviepy; print('MoviePy importado com sucesso! Versão:', moviepy.__version__); import moviepy.editor; print('Módulo editor importado com sucesso!'); from moviepy.editor import VideoFileClip; print('Métodos necessários:', 'with_audio' in dir(VideoFileClip), 'set_audio' in dir(VideoFileClip))"

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
'''

# Salva o script batch
batch_path = r"c:\Users\Enderson\Documents\APP 2\auto-video-producerV5-dev\reinstalar_moviepy_admin.bat"
with open(batch_path, 'w', encoding='utf-8') as f:
    f.write(batch_content)

print(f"✅ Script batch de reinstalação criado em: {batch_path}")
print("")
print("INSTRUÇÕES IMPORTANTES:")
print("1. O script batch será executado com permissões de administrador")
print("2. Isso é necessário para remover completamente os arquivos corrompidos")
print("3. Após a execução, o MoviePy 2.2.1 será reinstalado corretamente")
print("")
print("Executando o script batch como administrador...")

# Executa o script batch como administrador
if os.name == 'nt':  # Windows
    import ctypes
    if ctypes.windll.shell32.IsUserAnAdmin():
        # Já estamos executando como administrador
        os.system(f'"{batch_path}"')
    else:
        # Reexecuta o script batch como administrador
        print("   Solicitando permissões de administrador...")
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", "cmd.exe", f"/c \"{batch_path}\"", None, 1
        )

print("\n===== Processo de reinstalação radical iniciado =====")
print("Verifique a janela do prompt de comando em execução para ver o progresso.")
print("Após a conclusão, verifique se o MoviePy está funcionando corretamente.")