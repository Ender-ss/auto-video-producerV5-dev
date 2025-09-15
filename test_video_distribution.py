import os
import sys
import logging
from datetime import datetime

# Adicionando o diretório backend ao path
sys.path.append(r'c:\Users\Enderson\Documents\APP 2\auto-video-producerV5-dev\backend')  # Usando string raw para evitar erros de escape

# Importar configurações
try:
    from video_distribution_config import DURATION_TOLERANCE, TRANSITION_DURATION
    print(f"[OK] Importando configurações de distribuição de vídeo:")
    print(f"   - DURATION_TOLERANCE: {DURATION_TOLERANCE}s")
    print(f"   - TRANSITION_DURATION: {TRANSITION_DURATION}s")
except ImportError:
    print(f"[ERRO] Arquivo de configuração não encontrado, usando valores padrão.")
    DURATION_TOLERANCE = 0.5
    TRANSITION_DURATION = 0.3

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_video_distribution.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def setup_test_environment():
    """Configura o ambiente de teste"""
    # Criar diretórios necessários
    test_output_dir = r'c:\Users\Enderson\Documents\APP 2\auto-video-producerV5-dev\test_output'  # Usando string raw para evitar erros de escape
    if not os.path.exists(test_output_dir):
        os.makedirs(test_output_dir)
        logger.info(f'Diretório de saída de testes criado: {test_output_dir}')
    
    # Verificar se o serviço de criação de vídeo está disponível
    try:
        from services.video_creation_service import VideoCreationService
        logger.info('VideoCreationService importado com sucesso')
        return VideoCreationService, test_output_dir
    except ImportError as e:
        logger.error(f'Erro ao importar VideoCreationService: {e}')
        sys.exit(1)
    except Exception as e:
        logger.error(f'Erro inesperado: {e}')
        sys.exit(1)

def create_test_video(VideoCreationService, output_dir, num_images=10, audio_duration=60):
    """Cria um vídeo de teste com a distribuição de imagens uniforme"""
    try:
        # Inicializar o serviço de criação de vídeos com pipeline_id
        pipeline_id = 'test_distribution'
        service = VideoCreationService(pipeline_id=pipeline_id)
        logger.info(f'Serviço de criação de vídeo inicializado com pipeline_id: {pipeline_id}')
        
        # Configurar parâmetros de teste
        # Nota: Estes são exemplos - você precisará substituir por caminhos reais
        test_audio_path = r'c:\Users\Enderson\Documents\APP 2\auto-video-producerV5-dev\test_output\test_audio.mp3'  # Substitua por um arquivo de áudio real
        test_script = "Este é um script de teste para verificar a distribuição uniforme de imagens no vídeo. " * 5
        
        # Verificar se o arquivo de áudio existe, se não, tentar criar um ou sair
        if not os.path.exists(test_audio_path):
            logger.warning(f'Arquivo de áudio de teste não encontrado: {test_audio_path}')
            logger.info('Gerando um arquivo de áudio de teste automaticamente...')
            
            # Tentar importar a biblioteca wave para gerar um áudio de teste
            try:
                import wave
                import struct
                
                # Configurações do áudio
                sample_rate = 44100  # Taxa de amostragem
                duration = 30  # Duração em segundos (ajustar conforme necessário)
                frequency = 440  # Frequência em Hz (Lá central)
                amplitude = 32767  # Amplitude máxima (16-bit)
                
                # Criar arquivo WAV
                with wave.open(test_audio_path, 'w') as wav_file:
                    wav_file.setnchannels(1)  # Mono
                    wav_file.setsampwidth(2)  # 16-bit
                    wav_file.setframerate(sample_rate)
                    
                    # Gerar dados de áudio (senoide)
                    for i in range(int(sample_rate * duration)):
                        value = int(amplitude * 0.5 * (1 + (i % sample_rate) / sample_rate))  # Ruído branco simplificado
                        data = struct.pack('<h', value)
                        wav_file.writeframes(data)
                
                logger.info(f'Arquivo de áudio de teste gerado com sucesso: {test_audio_path}')
            except Exception as e:
                logger.error(f'Erro ao gerar arquivo de áudio de teste: {e}')
                return None
        
        # Configurar caminho das imagens
        image_dir = os.path.join(output_dir, 'test_images')
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
            
        # Gerar imagens de teste automaticamente
        logger.info(f'Gerando {num_images} imagens de teste automaticamente...')
        
        try:
            from PIL import Image, ImageDraw, ImageFont
            import random
            
            # Criar imagens coloridas com números
            test_images = []
            for i in range(num_images):
                # Criar imagem (1920x1080)
                img = Image.new('RGB', (1920, 1080), color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
                draw = ImageDraw.Draw(img)
                
                # Tentar carregar uma fonte, se não conseguir, usar o padrão
                try:
                    font = ImageFont.truetype("arial.ttf", 150)
                except:
                    font = ImageFont.load_default()
                
                # Adicionar número da imagem
                text = f'Imagem {i+1}'
                
                # Usar método compatível com versões mais recentes do Pillow
                try:
                    # Para Pillow >= 9.1.0
                    text_width = draw.textlength(text, font=font)
                    # Estimar altura com font.getbbox
                    bbox = font.getbbox(text)
                    text_height = bbox[3] - bbox[1]  # Inferior - Superior
                except AttributeError:
                    # Fallback para versões mais antigas do Pillow
                    text_width, text_height = draw.textsize(text, font=font)
                
                position = ((1920 - text_width) // 2, (1080 - text_height) // 2)
                draw.text(position, text, font=font, fill=(255, 255, 255))
                
                # Salvar imagem
                image_path = os.path.join(image_dir, f'test_image_{i+1}.png')
                img.save(image_path)
                test_images.append({'file_path': image_path})
            
            logger.info(f'{num_images} imagens de teste geradas com sucesso em: {image_dir}')
        except Exception as e:
            logger.error(f'Erro ao gerar imagens de teste: {e}')
            return None
        
        logger.info(f'Criando vídeo de teste com {len(test_images)} imagens')
        
        # Executar a criação do vídeo
        result = service.create_video(
            audio_path=test_audio_path,
            images=test_images,
            script_text=test_script,
            resolution='1920x1080',
            fps=30,
            quality='high',
            transitions=True,
            subtitles=True
        )
        
        if result:
            logger.info(f'Vídeo de teste criado com sucesso: {result["video_path"]}')
            logger.info(f'Duração: {result["duration"]:.2f}s, Tamanho: {result["file_size"]/1024/1024:.2f}MB')
            logger.info(f'Para analisar a distribuição, execute: python check_video.py --path "{result["video_path"]}"')
            return result["video_path"]
        else:
            logger.error('Falha ao criar o vídeo de teste')
            return None
            
    except Exception as e:
        logger.error(f'Erro durante a criação do vídeo de teste: {str(e)}')
        import traceback
        logger.error(traceback.format_exc())
        return None

def main():
    """Função principal"""
    logger.info('Iniciando teste de distribuição uniforme de imagens')
    
    # Configurar ambiente de teste
    VideoCreationService, output_dir = setup_test_environment()
    
    # Parâmetros do teste
    try:
        num_images = int(input('Quantas imagens deseja usar no teste? '))
        if num_images <= 0:
            num_images = 10
            logger.warning('Número de imagens inválido, usando 10 imagens')
    except ValueError:
        num_images = 10
        logger.warning('Entrada inválida, usando 10 imagens')
    
    # Criar vídeo de teste
    video_path = create_test_video(VideoCreationService, output_dir, num_images)
    
    if video_path:
        logger.info('Teste concluído com sucesso!')
        print(f"\nPara analisar a distribuição de imagens no vídeo, execute:")
        print(f"python check_video.py --path \"{video_path}\"")
    else:
        logger.error('Teste concluído com falhas')
        print("\nO teste não pôde ser concluído com sucesso. Verifique os logs para mais informações.")

if __name__ == "__main__":
    main()