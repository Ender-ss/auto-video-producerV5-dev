import os
from moviepy import VideoFileClip

# Caminho do vídeo gerado
video_path = r'c:\Users\Enderson\Documents\APP 2\auto-video-producerV5-dev\test_output\test_concatenated.mp4'

try:
    # Carregar o vídeo
    video = VideoFileClip(video_path)
    
    # Exibir informações
    print(f"Duração: {video.duration} segundos")
    print(f"Tamanho: {video.w}x{video.h} pixels")
    print(f"FPS: {video.fps}")
    print(f"Tem áudio: {video.audio is not None}")
    
    if video.audio:
        print(f"Duração do áudio: {video.audio.duration} segundos")
    
    # Fechar o vídeo
    video.close()
    
    print("\nVídeo concatenado verificado com sucesso!")
    
except Exception as e:
    print(f"Erro ao verificar o vídeo: {str(e)}")
    import traceback
    traceback.print_exc()