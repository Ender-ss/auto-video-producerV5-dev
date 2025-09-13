# Verifica se o MoviePy está corretamente instalado
try:
    print("===== Iniciando verificação do MoviePy =====")
    
    # Importa o MoviePy
    import moviepy
    print(f"MoviePy importado com sucesso! Versão: {moviepy.__version__}")
    
    # Importa o submódulo editor (o mais comum de falhar)
    from moviepy.editor import VideoFileClip, AudioFileClip
    print("Módulo moviepy.editor importado com sucesso!")
    
    # Verifica se os métodos essenciais existem
    print(f"Método 'with_audio' existe: {'with_audio' in dir(VideoFileClip)}")
    print(f"Método 'set_audio' existe: {'set_audio' in dir(VideoFileClip)}")
    
    # Verifica a configuração do FFmpeg
    from moviepy.config import get_setting
    ffmpeg_path = get_setting("FFMPEG_BINARY")
    print(f"FFMPEG configurado em: {ffmpeg_path}")
    
    # Verifica as dependências
    import imageio
    import numpy
    import PIL
    import proglog
    print(f"Imageio versão: {imageio.__version__}")
    print(f"NumPy versão: {numpy.__version__}")
    print(f"Pillow versão: {PIL.__version__}")
    
    print("\n✅ Verificação concluída com sucesso! MoviePy está funcionando corretamente.")
    
except ImportError as e:
    print(f"❌ Erro: {e}")
    print("\nSoluções sugeridas:")
    print("1. Execute: python -m pip install moviepy --force-reinstall")
    print("2. Certifique-se de que o Python está no PATH do sistema")
    print("3. Verifique se o FFmpeg está instalado corretamente")
    print("4. Tente reinstalar as dependências: python -m pip install decorator imageio imageio-ffmpeg numpy pillow proglog tqdm")

except Exception as e:
    print(f"❌ Erro inesperado: {e}")

print("\n===== Fim da verificação =====")