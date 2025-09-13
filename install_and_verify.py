# Script para instalar e verificar o MoviePy após reinstalação do Python
import subprocess
import sys
import os

print("=== Iniciando verificação e instalação do MoviePy ===")

# Forçar o uso do caminho correto do Python
sys.stdout.write(f"Python executando este script: {sys.executable}\n")

# Função para executar comandos
def run_command(command):
    print(f"Executando: {' '.join(command)}")
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        print("Saída:", result.stdout[:200] + ("..." if len(result.stdout) > 200 else ""))
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Erro: {e.stderr}")
        return False, e.stderr
    except FileNotFoundError as e:
        print(f"Arquivo não encontrado: {e}")
        return False, str(e)

# 1. Verificar a versão do pip usando o Python atual
print("\n1. Verificando pip...")
# Sempre usar o pip do Python atual para evitar problemas com caminhos
sys.stdout.write("Usando o pip associado ao Python atual...\n")
pip_path = [sys.executable, '-m', 'pip']
    
success, output = run_command(pip_path + ['--version'])
if not success:
    print("Pip não encontrado. Tentando instalar pip...")
    try:
        import ensurepip
        ensurepip.bootstrap()
        print("Pip instalado com sucesso!")
    except Exception as e:
        print(f"Falha ao instalar pip: {e}")

# 2. Instalar ou atualizar o MoviePy
print("\n2. Instalando/atualizando MoviePy...")
run_command(pip_path + ['install', 'moviepy', '--upgrade'])

# 3. Verificar se o MoviePy está instalado corretamente
try:
    print("\n3. Verificando instalação do MoviePy...")
    import moviepy
    print(f"MoviePy importado com sucesso! Versão: {moviepy.__version__}")
    
    try:
        from moviepy.editor import VideoFileClip
        print("Módulo moviepy.editor importado com sucesso!")
        
        # Verificar métodos essenciais
        print(f"Método 'with_audio' existe: {'with_audio' in dir(VideoFileClip)}")
        print(f"Método 'set_audio' existe: {'set_audio' in dir(VideoFileClip)}")
        
        # Verificar dependências
        print("\n4. Verificando dependências...")
        dependencies = ['imageio', 'numpy', 'pillow', 'proglog', 'tqdm']
        for dep in dependencies:
            try:
                mod = __import__(dep)
                print(f"{dep} importado com sucesso! Versão: {getattr(mod, '__version__', 'desconhecida')}")
            except ImportError:
                print(f"{dep} não está instalado. Tentando instalar...")
                run_command(pip_path + ['install', dep])
        
        # Verificar FFmpeg
        print("\n5. Verificando FFmpeg...")
        try:
            from moviepy.config import get_setting
            ffmpeg_path = get_setting("FFMPEG_BINARY")
            if ffmpeg_path:
                print(f"FFMPEG configurado em: {ffmpeg_path}")
            else:
                print("FFMPEG não está configurado. Tentando instalar via imageio-ffmpeg...")
                run_command(pip_path + ['install', 'imageio-ffmpeg'])
                import imageio_ffmpeg
                print(f"imageio-ffmpeg instalado. Caminho: {imageio_ffmpeg.get_ffmpeg_exe()}")
        except Exception as e:
            print(f"Erro ao verificar FFmpeg: {e}")
            print("Recomendação: Instale o FFmpeg manualmente ou execute 'pip install imageio-ffmpeg'")
            
        print("\n✅ Verificação concluída com sucesso! MoviePy está funcionando corretamente.")
        
    except ImportError as e:
        print(f"Erro ao importar moviepy.editor: {e}")
        print("Tentando reinstalar o MoviePy com dependências completas...")
        run_command(pip_path + ['install', 'moviepy', '--no-cache-dir', '--force-reinstall'])
        print("\n❌ Houve problemas com a instalação. Por favor, verifique o log acima.")
        
except ImportError as e:
    print(f"Erro ao importar MoviePy: {e}")
    print("\n❌ MoviePy não está instalado corretamente.")
    
print("\n=== Fim da verificação ===")