import os
import subprocess

def get_video_properties(video_path):
    """
    Obtém as propriedades do vídeo usando MoviePy.
    """
    try:
        # Importar MoviePy
        from moviepy.editor import VideoFileClip
        
        # Carregar o vídeo
        video = VideoFileClip(video_path)
        
        # Extrair informações
        video_info = {
            'width': video.w,
            'height': video.h,
            'duration': video.duration,
            'fps': video.fps,
            'file_size': os.path.getsize(video_path)
        }
        
        # Fechar o vídeo
        video.close()
        
        return video_info
        
    except Exception as e:
        print(f"Erro ao obter propriedades do vídeo: {str(e)}")
        return None

def main():
    # Caminho para o vídeo
    video_path = r"c:\Users\Enderson\Documents\APP 2\auto-video-producerV5-dev\backend\projects\a98c0799-b28c-4ead-8c85-4a4758855b0c\video\video_final.mp4"
    
    # Verificar se o arquivo existe
    if not os.path.exists(video_path):
        print(f"Arquivo de vídeo não encontrado: {video_path}")
        return False
    
    print(f"Analisando vídeo: {video_path}")
    
    # Obter propriedades do vídeo
    video_info = get_video_properties(video_path)
    
    if video_info:
        print("\nPropriedades do vídeo:")
        print(f"Resolução: {video_info['width']}x{video_info['height']}")
        print(f"Duração: {video_info['duration']:.2f} segundos")
        print(f"FPS: {video_info['fps']}")
        print(f"Tamanho do arquivo: {video_info['file_size']} bytes")
        
        # Verificar se a resolução é a esperada
        if video_info['width'] == 1920 and video_info['height'] == 1080:
            print("\n✅ Resolução correta (1920x1080)")
        else:
            print(f"\n❌ Resolução incorreta. Esperado: 1920x1080, Atual: {video_info['width']}x{video_info['height']}")
        
        # Verificar se a duração é a esperada (aproximadamente 10 segundos)
        if 9 <= video_info['duration'] <= 11:
            print("✅ Duração correta (aproximadamente 10 segundos)")
        else:
            print(f"❌ Duração incorreta. Esperado: ~10 segundos, Atual: {video_info['duration']:.2f} segundos")
        
        # Verificar se o FPS é o esperado
        if video_info['fps'] == 30:
            print("✅ FPS correto (30)")
        else:
            print(f"❌ FPS incorreto. Esperado: 30, Atual: {video_info['fps']}")
        
        print("\nPara verificar se as imagens estão sendo exibidas corretamente, por favor, abra o vídeo em um player de vídeo e observe se:")
        print("1. As imagens são exibidas corretamente (sem tela preta ou cinza)")
        print("2. As imagens são redimensionadas adequadamente para 1920x1080")
        print("3. As imagens são centralizadas no vídeo")
        print("4. Não há distorções nas imagens")
        
        print("\nCaminho do vídeo para visualização manual:")
        print(video_path)
        
        return True
    else:
        print("\n❌ Não foi possível obter as propriedades do vídeo")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ Análise concluída com sucesso!")
    else:
        print("\n❌ Falha na análise do vídeo.")