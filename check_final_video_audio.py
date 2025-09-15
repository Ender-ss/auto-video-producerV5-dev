import os
from moviepy import VideoFileClip

# Caminho do vídeo final gerado pelo sistema
video_path = r'c:\Users\Enderson\Documents\APP 2\auto-video-producerV5-dev\backend\projects\a98c0799-b28c-4ead-8c85-4a4758855b0c\video\video_final.mp4'

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
        print(f"FPS do áudio: {video.audio.fps}")
        print(f"Taxa de bits do áudio: {video.audio.bitrate if hasattr(video.audio, 'bitrate') else 'N/A'}")
    
    # Fechar o vídeo
    video.close()
    
    print("\nVídeo final verificado com sucesso!")
    
except Exception as e:
    print(f"Erro ao verificar o vídeo: {str(e)}")
    import traceback
    traceback.print_exc()