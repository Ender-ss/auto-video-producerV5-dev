import os
import sys
import argparse
from datetime import timedelta

# Adicionando o diretório backend ao path
sys.path.append(r'c:\Users\Enderson\Documents\APP 2\auto-video-producerV5-dev\backend')
# Usando string raw (r'...') para evitar erros de escape de unicode nas barras invertidas

def analyze_video_distribution(video_path, num_expected_images=10):
    """Analisa a distribuição de imagens no vídeo"""
    try:
        from moviepy import VideoFileClip
        
        if not os.path.exists(video_path):
            print(f"ERRO: Arquivo de vídeo não encontrado: {video_path}")
            return False
        
        print(f"\n=== ANÁLISE DO VÍDEO ===")
        print(f"Caminho: {video_path}")
        
        clip = VideoFileClip(video_path)
        video_duration = clip.duration
        
        # Propriedades básicas
        print(f"Duração total do vídeo: {timedelta(seconds=video_duration)}")
        print(f"Resolução: {clip.w}x{clip.h}")
        print(f"FPS: {clip.fps}")
        print(f"Possui áudio: {'Sim' if clip.audio else 'Não'}")
        
        if clip.audio:
            audio_duration = clip.audio.duration
            print(f"Duração do áudio: {timedelta(seconds=audio_duration)}")
            duration_diff = abs(video_duration - audio_duration)
            print(f"Diferença entre vídeo e áudio: {duration_diff:.2f} segundos")
        
        # Estimativa de distribuição de imagens (baseado em quadros-chave)
        # Nota: MoviePy não oferece uma maneira direta de detectar mudanças de cena
        # Esta é uma estimativa baseada na duração total e no número de imagens esperado
        
        # Usar o número de imagens fornecido ou o padrão
        if num_expected_images <= 0:
            print("Número de imagens inválido, usando 10 imagens como padrão.")
            num_expected_images = 10
        
        ideal_duration_per_image = video_duration / num_expected_images
        print(f"\n=== ANÁLISE DE DISTRIBUIÇÃO ===")
        print(f"Número de imagens esperadas: {num_expected_images}")
        print(f"Duração ideal por imagem: {ideal_duration_per_image:.2f} segundos")
        print(f"Cada imagem deveria aparecer a cada: {timedelta(seconds=ideal_duration_per_image)}")
        
        # Sugestão de pontos para verificação manual
        print(f"\n=== PONTOS SUGERIDOS PARA VERIFICAÇÃO MANUAL ===")
        for i in range(num_expected_images):
            timestamp = i * ideal_duration_per_image
            print(f"Imagem {i+1}: {timedelta(seconds=timestamp)}")
        
        clip.close()
        print(f"\n=== ANÁLISE CONCLUÍDA ===")
        return True
        
    except ImportError as e:
        print(f"ERRO: MoviePy não está instalado corretamente: {e}")
        print("Por favor, instale o MoviePy com: pip install moviepy")
        return False
    except Exception as e:
        print(f"ERRO: Ocorreu um erro durante a análise do vídeo: {e}")
        return False

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description='Analisa um vídeo e verifica a distribuição de imagens')
    parser.add_argument('--path', type=str, help='Caminho para o arquivo de vídeo')
    parser.add_argument('--num-images', type=int, default=10, help='Número de imagens esperadas no vídeo (padrão: 10)')
    args = parser.parse_args()
    
    # Caminho padrão se não for fornecido
    default_path = r'c:\Users\Enderson\Documents\APP 2\auto-video-producerV5-dev\backend\projects\a98c0799-b28c-4ead-8c85-4a4758855b0c\video\video_final.mp4'
    video_path = args.path if args.path else default_path
    
    # Se o arquivo padrão não existir, perguntar ao usuário
    if not args.path and not os.path.exists(default_path):
        video_path = input("\nArquivo de vídeo padrão não encontrado. Informe o caminho do vídeo: ")
    
    analyze_video_distribution(video_path, args.num_images)

if __name__ == "__main__":
    main()