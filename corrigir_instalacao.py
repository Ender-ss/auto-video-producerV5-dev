import sys
import os
import shutil

print("===== Corrigindo a instalação do MoviePy =====")
print(f"Usando Python: {sys.executable}")

# Caminho do diretório corrompido do MoviePy - usando strings raw para evitar erros de escape
moviepy_path = r"C:\Users\Enderson\AppData\Roaming\Python\Python313\site-packages\moviepy"
moviepy_egg_path = r"C:\Users\Enderson\AppData\Roaming\Python\Python313\site-packages\moviepy-2.2.1-py3.13.egg-info"

# 1. Remover manualmente o diretório corrompido do MoviePy
print(f"\n1. Removendo diretório corrompido do MoviePy: {moviepy_path}")
if os.path.exists(moviepy_path):
    try:
        shutil.rmtree(moviepy_path)
        print("✅ Diretório removido com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao remover diretório: {e}")
        print("   Por favor, execute este script como administrador.")
else:
    print("ℹ️  O diretório do MoviePy não foi encontrado.")

# Remover também o arquivo .egg-info
print(f"\n2. Removendo arquivo .egg-info: {moviepy_egg_path}")
if os.path.exists(moviepy_egg_path):
    try:
        if os.path.isdir(moviepy_egg_path):
            shutil.rmtree(moviepy_egg_path)
        else:
            os.remove(moviepy_egg_path)
        print("✅ Arquivo .egg-info removido com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao remover arquivo .egg-info: {e}")
else:
    # Procura por outros arquivos .egg-info do MoviePy
    site_packages = r"C:\Users\Enderson\AppData\Roaming\Python\Python313\site-packages"
    if os.path.exists(site_packages):
        for item in os.listdir(site_packages):
            if item.startswith("moviepy-") and item.endswith(".egg-info"):
                egg_path = os.path.join(site_packages, item)
                print(f"   Encontrado outro arquivo .egg-info: {egg_path}")
                try:
                    if os.path.isdir(egg_path):
                        shutil.rmtree(egg_path)
                    else:
                        os.remove(egg_path)
                    print(f"   ✅ {item} removido com sucesso!")
                except Exception as e:
                    print(f"   ❌ Erro ao remover {item}: {e}")

# 3. Reinstalar o MoviePy de forma limpa
print("\n3. Reinstalando o MoviePy de forma limpa...")
comando_reinstalar = f'"{sys.executable}" -m pip install moviepy==2.2.1 --force-reinstall --no-cache-dir'
print(f"   Executando: {comando_reinstalar}")
os.system(comando_reinstalar)

# 4. Verificar a instalação corrigida
print("\n4. Verificando a instalação corrigida...")

try:
    # Remove do cache
    if 'moviepy' in sys.modules:
        del sys.modules['moviepy']
    
    import moviepy
    print(f"   ✅ MoviePy importado com sucesso! Versão: {moviepy.__version__}")
    print(f"   Localização: {moviepy.__file__}")
    
    # Tentar importar o editor
    try:
        from moviepy.editor import VideoFileClip
        print("   ✅ Módulo moviepy.editor importado com sucesso!")
        print(f"   ✅ Método 'with_audio' existe: {'with_audio' in dir(VideoFileClip)}")
        print(f"   ✅ Método 'set_audio' existe: {'set_audio' in dir(VideoFileClip)}")
        
        print("\n🎉 Instalação corrigida com SUCESSO! 🎉")
        print("O MoviePy agora está funcionando corretamente.")
        print("Você pode executar sua pipeline de produção de vídeo.")
    except ImportError as e:
        print(f"   ❌ Erro ao importar moviepy.editor: {e}")
        print("\nSoluções sugeridas:")
        print("1. Execute este script como administrador")
        print("2. Tente reinstalar as dependências:")
        print(f"   {sys.executable} -m pip install imageio imageio-ffmpeg numpy pillow")
        print("3. Verifique se o diretório do MoviePy contém o arquivo editor.py")
except ImportError as e:
    print(f"   ❌ Erro fatal: {e}")
    print("\nO MoviePy não foi importado corretamente.")
    print("Por favor, execute este script como administrador e tente novamente.")

print("\n===== Processo de correção concluído =====")