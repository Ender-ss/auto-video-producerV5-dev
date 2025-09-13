import sys
import os

print("===== Verificação Final da Instalação do MoviePy =====")
print(f"Python sendo usado: {sys.executable}")
print(f"Versão do Python: {sys.version}")

# Função para verificar se o MoviePy está instalado corretamente
def verificar_moviepy():
    print("\n===== Testando a importação do MoviePy =====")
    
    # Tentar importar o MoviePy
    try:
        import moviepy
        print(f"✅ MoviePy importado com sucesso!")
        print(f"   Versão: {moviepy.__version__}")
        print(f"   Localização: {moviepy.__file__}")
        
        # Tentar importar o submódulo editor
        try:
            from moviepy import editor
            print(f"✅ Módulo 'moviepy.editor' importado com sucesso!")
            print(f"   Localização: {editor.__file__}")
            
            # Tentar importar VideoFileClip e verificar os métodos necessários
            try:
                from moviepy.editor import VideoFileClip
                print(f"✅ Classe 'VideoFileClip' importada com sucesso!")
                
                # Verificar se os métodos necessários existem
                print(f"\n===== Verificando métodos necessários =====")
                
                # Método with_audio
                if hasattr(VideoFileClip, 'with_audio'):
                    print(f"✅ Método 'with_audio' está disponível!")
                else:
                    print(f"❌ Método 'with_audio' NÃO está disponível!")
                    print("   Isso pode ser um problema para sua pipeline.")
                    
                # Método set_audio
                if hasattr(VideoFileClip, 'set_audio'):
                    print(f"✅ Método 'set_audio' está disponível!")
                else:
                    print(f"❌ Método 'set_audio' NÃO está disponível!")
                    print("   Isso pode ser um problema para sua pipeline.")
                
                # Listar alguns atributos importantes
                print(f"\n===== Informações adicionais =====")
                print(f"Módulos disponíveis no moviepy: {[attr for attr in dir(moviepy) if not attr.startswith('__')]}")
                print(f"Módulos disponíveis no moviepy.editor: {[attr for attr in dir(editor) if not attr.startswith('__') and not callable(getattr(editor, attr))]}")
                
                print("\n🎉🎉🎉 INSTALAÇÃO DO MOVIEPY CONCLUÍDA COM SUCESSO! 🎉🎉🎉")
                print("O MoviePy está funcionando corretamente e pronto para ser usado.")
                print("Você pode prosseguir com a execução da sua pipeline de produção de vídeo.")
                
            except ImportError as e:
                print(f"❌ Erro ao importar VideoFileClip: {e}")
        except ImportError as e:
            print(f"❌ Erro ao importar moviepy.editor: {e}")
            print("   Verifique se o diretório do MoviePy contém o arquivo editor.py")
    except ImportError as e:
        print(f"❌ Erro ao importar MoviePy: {e}")
        print("   A instalação não foi concluída corretamente.")
        print("\nSoluções sugeridas:")
        print("1. Certifique-se de ter executado o script batch como administrador")
        print(f"2. Tente reinstalar: {sys.executable} -m pip install moviepy==2.2.1 --force-reinstall --no-cache-dir")
        print("3. Verifique se o Python está usando o caminho correto")

# Verificar dependências importantes

def verificar_dependencias():
    print("\n===== Verificando dependências importantes =====")
    dependencias = ["numpy", "imageio", "imageio_ffmpeg", "pillow", "decorator", "proglog"]
    
    for dep in dependencias:
        try:
            modulo = __import__(dep)
            versao = getattr(modulo, "__version__", "Desconhecida")
            print(f"✅ {dep} (versão: {versao})")
        except ImportError:
            print(f"❌ {dep} - NÃO INSTALADA!")

# Verificar se o FFmpeg está configurado corretamente

def verificar_ffmpeg():
    print("\n===== Verificando o FFmpeg =====")
    try:
        import imageio_ffmpeg
        print(f"✅ imageio_ffmpeg importado com sucesso!")
        print(f"   Versão: {imageio_ffmpeg.__version__}")
        print(f"   Localização do binário: {imageio_ffmpeg.get_ffmpeg_exe()}")
        
        # Testar se o FFmpeg pode ser executado
        try:
            import subprocess
            resultado = subprocess.run(
                [imageio_ffmpeg.get_ffmpeg_exe(), "-version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=5
            )
            if resultado.returncode == 0:
                print("✅ FFmpeg está funcionando corretamente!")
                print(f"   Versão do FFmpeg: {resultado.stdout.splitlines()[0]}")
            else:
                print(f"❌ FFmpeg não está funcionando: {resultado.stderr}")
        except Exception as e:
            print(f"❌ Erro ao executar FFmpeg: {e}")
    except ImportError as e:
        print(f"❌ imageio_ffmpeg não está instalado: {e}")

# Executar todas as verificações
if __name__ == "__main__":
    verificar_moviepy()
    verificar_dependencias()
    verificar_ffmpeg()
    
    print("\n===== Fim da verificação =====")
    print("Caso tenha problemas persistentes, entre em contato com o suporte.")