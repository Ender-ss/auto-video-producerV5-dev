import sys
import os

print("===== Iniciando reinstalação completa do MoviePy =====")
print(f"Usando Python: {sys.executable}")

# Define o caminho do pip
pip_path = [sys.executable, '-m', 'pip']

# Função para executar comandos pip
def executar_pip(comando):
    comando_str = f'"{sys.executable}" -m pip ' + ' '.join(comando)
    print(f"\nExecutando: {comando_str}")
    try:
        resultado = os.system(comando_str)
        if resultado != 0:
            print(f"❌ Erro ao executar comando. Código de saída: {resultado}")
        return resultado == 0
    except Exception as e:
        print(f"❌ Exceção: {e}")
        return False

# Passo 1: Atualizar pip
executar_pip(['install', '--upgrade', 'pip'])

# Passo 2: Desinstalar todas as dependências existentes
executar_pip(['uninstall', '-y', 'moviepy', 'imageio', 'imageio-ffmpeg', 'numpy', 'pillow', 'decorator', 'proglog', 'tqdm'])

# Passo 3: Instalar dependências na ordem correta
print("\nInstalando dependências na ordem correta...")
dependencias = [
    ['install', 'numpy==1.26.4'],  # Versão estável compatível
    ['install', 'pillow>=9.0.0'],
    ['install', 'decorator>=4.0.0'],
    ['install', 'proglog>=0.1.0'],
    ['install', 'tqdm>=4.11.0'],
    ['install', 'imageio>=2.5.0'],
    ['install', 'imageio-ffmpeg>=0.4.0'],
    ['install', 'moviepy==2.2.1']  # Última versão estável
]

for dep in dependencias:
    if not executar_pip(dep):
        print(f"⚠️  Não foi possível instalar {dep[-1]}. Tentando com --no-cache-dir...")
        executar_pip(dep + ['--no-cache-dir'])

# Passo 4: Verificar a instalação
try:
    print("\n===== Verificando a instalação final =====")
    import moviepy
    print(f"✅ MoviePy importado com sucesso! Versão: {moviepy.__version__}")
    
    # Tentar importar o editor
    try:
        from moviepy.editor import VideoFileClip, AudioFileClip
        print("✅ Módulo moviepy.editor importado com sucesso!")
        print(f"✅ Método 'with_audio' existe: {'with_audio' in dir(VideoFileClip)}")
        print(f"✅ Método 'set_audio' existe: {'set_audio' in dir(VideoFileClip)}")
        
        # Verificar FFmpeg
        try:
            from moviepy.config import get_setting
            ffmpeg_path = get_setting("FFMPEG_BINARY")
            print(f"✅ FFmpeg configurado em: {ffmpeg_path}")
        except Exception as e:
            print(f"⚠️  Problema com o FFmpeg: {e}")
            print("   Execute: python -m pip install imageio-ffmpeg")
    except ImportError as e:
        print(f"❌ Erro ao importar moviepy.editor: {e}")
        print("   Provável causa: dependências faltando ou corrompidas.")
        print("   Tente executar: python -m pip install moviepy --force-reinstall --no-cache-dir")
        
    print("\n===== Instalação concluída =====")
    print("Após essa reinstalação, execute novamente o arquivo verificar_moviepy.py")
except ImportError as e:
    print(f"❌ Erro fatal: {e}")
    print("\nSoluções sugeridas:")
    print("1. Execute este script como administrador")
    print("2. Certifique-se de que o Python está no PATH do sistema")
    print("3. Verifique se você tem permissões para instalar pacotes")
    print("4. Tente reinstalar o Python completamente")