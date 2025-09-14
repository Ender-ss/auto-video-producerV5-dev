"""🎬 Video Creation Service
Serviço de criação de vídeo usando MoviePy
"""

import os
import sys
import json
import time
import logging
import subprocess
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

# Adicionar diretório routes ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'routes'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Imports do MoviePy com fallback
MOVIEPY_AVAILABLE = False
try:
    from moviepy import (
        VideoFileClip, ImageClip, AudioFileClip, CompositeVideoClip,
        TextClip, concatenate_videoclips, ColorClip
    )
    from moviepy.video.fx import Resize
    from moviepy.video.fx import FadeIn
    from moviepy.video.fx import FadeOut
    from moviepy.audio.fx import MultiplyVolume
    
    # Criar aliases para compatibilidade com código existente
    resize = Resize
    fadein = FadeIn
    fadeout = FadeOut
    volumex = MultiplyVolume
    
    MOVIEPY_AVAILABLE = True
    
    # Fix para PIL.Image.ANTIALIAS depreciado
    try:
        from PIL import Image
        if not hasattr(Image, 'ANTIALIAS'):
            Image.ANTIALIAS = Image.LANCZOS
    except ImportError:
        pass
        
except ImportError as e:
    # MoviePy não está instalado - será tratado no método de criação
    print(f"⚠️ MoviePy não disponível: {e}")
    # Definir classes vazias para evitar erros de importação
    VideoFileClip = ImageClip = AudioFileClip = CompositeVideoClip = None
    TextClip = concatenate_videoclips = ColorClip = None
    resize = fadein = fadeout = volumex = None

logger = logging.getLogger(__name__)

class VideoCreationService:
    """Serviço de criação de vídeo"""
    
    def __init__(self, pipeline_id: str):
        self.pipeline_id = pipeline_id
        self.temp_dir = os.path.join('temp', f'video_{pipeline_id}')
        
        # Criar diretório do projeto se não existir
        project_dir = os.path.join(os.path.dirname(__file__), '..', 'projects', pipeline_id)
        self.output_dir = os.path.join(project_dir, 'video')
        
        # Criar diretórios necessários
        os.makedirs(self.temp_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
    
    def _log(self, level: str, message: str, data: Optional[Dict] = None):
        """Adicionar log ao pipeline"""
        try:
            from routes.pipeline_complete import add_pipeline_log
            add_pipeline_log(self.pipeline_id, level, message, data)
        except Exception as e:
            logger.error(f"Erro ao adicionar log: {str(e)}")
    
    def _normalize_resolution(self, resolution: str) -> str:
        """Normalizar resolução convertendo qualidades para resoluções válidas"""
        # Mapeamento de qualidades para resoluções
        quality_to_resolution = {
            '720p': '1280x720',
            '1080p': '1920x1080',
            '4k': '3840x2160',
            'hd': '1280x720',
            'full_hd': '1920x1080',
            'ultra_hd': '3840x2160'
        }
        
        # Se já é uma resolução válida (formato WxH), retornar como está
        if 'x' in resolution and resolution.replace('x', '').replace('0', '').replace('1', '').replace('2', '').replace('3', '').replace('4', '').replace('5', '').replace('6', '').replace('7', '').replace('8', '').replace('9', '') == '':
            return resolution
        
        # Converter qualidade para resolução
        normalized = quality_to_resolution.get(resolution.lower(), '1920x1080')
        self._log('info', f'Resolução normalizada: {resolution} -> {normalized}')
        return normalized
    
    def create_video(self, audio_path: str, images: List[Dict[str, Any]], 
                    script_text: str, resolution: str = '1920x1080', 
                    fps: int = 30, quality: str = 'high', 
                    transitions: bool = True, subtitles: bool = True,
                    tts_segments: List[Dict] = None) -> Dict[str, Any]:
        """Criar vídeo final"""
        try:
            self._log('info', 'Iniciando criação do vídeo final')
            
            # Normalizar resolução (converter qualidades para resoluções válidas)
            resolution = self._normalize_resolution(resolution)
            
            # Verificar se MoviePy está disponível
            self._check_moviepy_availability()
            
            # Verificar arquivos de entrada
            self._validate_input_files(audio_path, images)
            
            # Obter duração do áudio
            audio_duration = self._get_audio_duration(audio_path)
            self._log('info', f'Duração do áudio: {audio_duration:.2f} segundos')
            
            # Calcular timing das imagens com base no script
            self._log('info', f'Calculando timing para {len(images)} imagens')
            image_timings = self._calculate_image_timings(images, audio_duration, script_text)
            
            # Criar clipes de imagem
            self._log('info', 'Criando clipes de imagem')
            image_clips = self._create_image_clips(images, image_timings, resolution)
            
            # Verificar se os clipes foram criados corretamente
            if not image_clips:
                raise Exception('Nenhum clipe de imagem foi criado')
            
            self._log('info', f'{len(image_clips)} clipes de imagem criados com sucesso')
            
            # Log informações sobre os clipes criados
            for i, clip in enumerate(image_clips):
                self._log('info', f'Clip {i+1}: duração={clip.duration:.2f}s, tamanho={clip.w if hasattr(clip, "w") else "N/A"}x{clip.h if hasattr(clip, "h") else "N/A"}')
            
            # Adicionar transições se solicitado
            if transitions:
                self._log('info', 'Adicionando transições entre imagens')
                original_clips = image_clips
                image_clips = self._add_transitions(image_clips)
                
                # Verificar se as transições foram aplicadas corretamente
                if len(image_clips) != len(original_clips):
                    self._log('warning', f'O número de clipes mudou após as transições: {len(original_clips)} -> {len(image_clips)}')
                
                # Log informações sobre os clipes com transições
                for i, clip in enumerate(image_clips):
                    self._log('info', f'Clip com transição {i+1}: duração={clip.duration:.2f}s, tamanho={clip.w if hasattr(clip, "w") else "N/A"}x{clip.h if hasattr(clip, "h") else "N/A"}')
            
            # Combinar clipes de imagem
            self._log('info', 'Combinando clipes de imagem')
            try:
                # Tentar concatenar com método chain
                video_clip = concatenate_videoclips(image_clips, method='chain')
                self._log('info', f'Clipes concatenados com método chain, duração total: {video_clip.duration:.2f}s, tamanho: {video_clip.w if hasattr(video_clip, "w") else "N/A"}x{video_clip.h if hasattr(video_clip, "h") else "N/A"}')
            except Exception as e:
                self._log('warning', f'Erro ao concatenar com método chain: {str(e)}')
                try:
                    # Fallback para método compose
                    video_clip = concatenate_videoclips(image_clips, method='compose')
                    self._log('info', f'Clipes concatenados com método compose, duração total: {video_clip.duration:.2f}s, tamanho: {video_clip.w if hasattr(video_clip, "w") else "N/A"}x{video_clip.h if hasattr(video_clip, "h") else "N/A"}')
                except Exception as e2:
                    self._log('error', f'Erro ao concatenar com método compose: {str(e2)}')
                    # Último recurso: usar o primeiro clipe
                    video_clip = image_clips[0] if image_clips else None
                    if video_clip:
                        self._log('warning', f'Usando apenas o primeiro clipe como fallback, duração: {video_clip.duration:.2f}s, tamanho: {video_clip.w if hasattr(video_clip, "w") else "N/A"}x{video_clip.h if hasattr(video_clip, "h") else "N/A"}')
                    else:
                        raise Exception('Não foi possível criar o vídeo final - nenhum clipe disponível')
            
            # Verificar se o vídeo clip foi criado corretamente
            if video_clip is None:
                raise Exception('Vídeo clip não foi criado corretamente')
            
            # Adicionar áudio
            self._log('info', 'Adicionando áudio ao vídeo')
            audio_clip = AudioFileClip(audio_path)
            self._log('info', f'Áudio carregado com duração: {audio_clip.duration:.2f}s')
            
            # Verificar se o vídeo clip tem a duração esperada
            if video_clip.duration == 0:
                self._log('error', 'O vídeo clip tem duração zero')
                raise Exception('O vídeo clip tem duração zero')
            
            # Ajustar duração do vídeo para corresponder ao áudio se necessário
            if abs(video_clip.duration - audio_clip.duration) > 0.1:  # Diferença maior que 0.1s
                self._log('info', f'Ajustando duração do vídeo: {video_clip.duration:.2f}s -> {audio_clip.duration:.2f}s')
                
                # Se o vídeo é mais curto, estender o último clipe
                if video_clip.duration < audio_clip.duration:
                    # Calcular quanto tempo precisamos adicionar
                    extra_time = audio_clip.duration - video_clip.duration
                    
                    # Estender o último clipe
                    if image_clips:
                        last_clip_duration = image_clips[-1].duration + extra_time
                        image_clips[-1] = image_clips[-1].with_duration(last_clip_duration)
                        
                        # Recriar o vídeo com os clipes ajustados
                        try:
                            video_clip = concatenate_videoclips(image_clips, method='chain')
                        except Exception as e:
                            self._log('warning', f'Erro ao concatenar com método chain após ajuste: {str(e)}')
                            video_clip = concatenate_videoclips(image_clips, method='compose')
                        
                        self._log('info', f'Duração do vídeo ajustada para: {video_clip.duration:.2f}s')
                else:
                    # Se o vídeo é mais longo, cortar para corresponder ao áudio
                    video_clip = video_clip.subclipped(0, audio_clip.duration)
                    self._log('info', f'Duração do vídeo cortada para: {video_clip.duration:.2f}s')
            
            # Adicionar áudio ao vídeo
            video_clip = video_clip.with_audio(audio_clip)
            self._log('info', f'Áudio adicionado ao vídeo, duração final: {video_clip.duration:.2f}s')
            
            # Adicionar legendas se solicitado
            if subtitles:
                self._log('info', 'Adicionando legendas ao vídeo')
                original_duration = video_clip.duration
                video_clip = self._add_subtitles(video_clip, script_text, audio_duration, tts_segments)
                self._log('info', f'Legendas adicionadas ao vídeo, duração antes: {original_duration:.2f}s, depois: {video_clip.duration:.2f}s')
            
            # Definir configurações de qualidade adaptativas
            codec_settings = self._get_adaptive_codec_settings(quality, resolution, audio_duration)
            
            # Renderizar vídeo final
            output_filename = f"video_final.mp4"
            output_path = os.path.join(self.output_dir, output_filename)
            
            self._log('info', 'Iniciando renderização do vídeo')
            self._log('info', f'Informações do vídeo antes da renderização: duração={video_clip.duration:.2f}s, tamanho={video_clip.w if hasattr(video_clip, "w") else "N/A"}x{video_clip.h if hasattr(video_clip, "h") else "N/A"}')
            
            # Renderização otimizada com configurações avançadas
            self._render_video_optimized(
                video_clip, output_path, fps, codec_settings
            )
            
            # Obter informações do arquivo final
            file_size = os.path.getsize(output_path)
            final_duration = video_clip.duration
            
            # Limpar recursos
            self._log('info', 'Limpando recursos')
            video_clip.close()
            audio_clip.close()
            for i, clip in enumerate(image_clips):
                try:
                    clip.close()
                    self._log('info', f'Clipe {i+1} fechado com sucesso')
                except Exception as e:
                    self._log('warning', f'Erro ao fechar clipe {i+1}: {str(e)}')
            
            self._log('info', 'Vídeo criado com sucesso', {
                'output_path': output_path,
                'duration': final_duration,
                'file_size': file_size
            })
            
            return {
                'video_path': output_path,
                'filename': output_filename,
                'duration': final_duration,
                'file_size': file_size,
                'resolution': resolution,
                'fps': fps,
                'quality': quality,
                'creation_time': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            self._log('error', f'Erro na criação do vídeo: {str(e)}')
            raise
    
    def _check_moviepy_availability(self):
        """Verificar se MoviePy está disponível"""
        if not MOVIEPY_AVAILABLE:
            error_msg = "MoviePy não está instalado ou não foi importado corretamente. Execute: pip install moviepy"
            self._log('error', error_msg)
            raise Exception(error_msg)
        
        try:
            import moviepy
            self._log('info', f'MoviePy disponível - versão: {moviepy.__version__}')
        except ImportError:
            error_msg = "MoviePy não está instalado. Execute: pip install moviepy"
            self._log('error', error_msg)
            raise Exception(error_msg)
    
    def _validate_input_files(self, audio_path: str, images: List[Dict[str, Any]]):
        """Validar arquivos de entrada"""
        self._log('info', 'Iniciando validação de arquivos de entrada')
        
        # Verificar áudio
        self._log('info', f'Verificando arquivo de áudio: {audio_path}')
        if not os.path.exists(audio_path):
            raise Exception(f"Arquivo de áudio não encontrado: {audio_path}")
        
        # Verificar tamanho do arquivo de áudio
        audio_size = os.path.getsize(audio_path)
        if audio_size == 0:
            raise Exception(f"Arquivo de áudio está vazio: {audio_path}")
        
        self._log('info', f'Arquivo de áudio válido: {audio_size} bytes')
        
        # Verificar imagens
        if not images:
            raise Exception("Nenhuma imagem fornecida")
        
        self._log('info', f'Verificando {len(images)} imagens')
        missing_images = []
        valid_images = 0
        
        for i, img in enumerate(images):
            img_path = img.get('file_path', '')
            if not img_path:
                self._log('warning', f'Imagem {i+1}: caminho não especificado')
                missing_images.append(f'Imagem {i+1}: sem caminho')
            elif not os.path.exists(img_path):
                self._log('warning', f'Imagem {i+1}: arquivo não encontrado - {img_path}')
                missing_images.append(img_path)
            else:
                img_size = os.path.getsize(img_path)
                if img_size == 0:
                    self._log('warning', f'Imagem {i+1}: arquivo vazio - {img_path}')
                    missing_images.append(f'{img_path} (vazio)')
                else:
                    valid_images += 1
        
        if missing_images:
            raise Exception(f"Problemas com imagens: {missing_images}")
        
        self._log('info', f'Validação concluída: {valid_images} imagens válidas')
    
    def _get_audio_duration(self, audio_path: str) -> float:
        """Obter duração do áudio"""
        try:
            audio_clip = AudioFileClip(audio_path)
            duration = audio_clip.duration
            audio_clip.close()
            return duration
        except Exception as e:
            # Fallback: usar ffprobe se disponível
            try:
                result = subprocess.run([
                    'ffprobe', '-v', 'quiet', '-show_entries', 
                    'format=duration', '-of', 'csv=p=0', audio_path
                ], capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    return float(result.stdout.strip())
            except:
                pass
            
            # Fallback final: estimar baseado no tamanho do arquivo
            file_size = os.path.getsize(audio_path)
            estimated_duration = file_size / (44100 * 2 * 2)  # Estimativa grosseira
            
            self._log('warning', f'Não foi possível obter duração exata do áudio. Estimativa: {estimated_duration:.2f}s')
            return max(60, estimated_duration)  # Mínimo de 1 minuto
    
    def _calculate_image_timings(self, images: List[Dict[str, Any]], 
                               total_duration: float, script_text: str = "") -> List[Tuple[float, float]]:
        """Calcular timing de cada imagem com base no conteúdo e estrutura do roteiro"""
        num_images = len(images)
        
        if num_images == 0:
            return []
        
        # Se temos apenas uma imagem, ela ocupa toda a duração
        if num_images == 1:
            return [(0.0, total_duration)]
        
        # Usar timing uniforme como padrão para distribuir as imagens por todo o vídeo
        timings = self._calculate_uniform_timings(images, total_duration)
        
        self._log('info', f'Timing calculado para {num_images} imagens - usando distribuição uniforme')
        return timings
    
    def _calculate_intelligent_timings(self, images: List[Dict[str, Any]], 
                                     total_duration: float, script_text: str) -> List[Tuple[float, float]]:
        """Calcular timing inteligente baseado no conteúdo do script"""
        try:
            # Dividir script em segmentos lógicos
            script_segments = self._analyze_script_segments(script_text)
            num_images = len(images)
            
            if len(script_segments) != num_images:
                # Se não há correspondência 1:1, usar método adaptativo
                return self._calculate_adaptive_timings(images, total_duration)
            
            # Calcular duração baseada no comprimento e complexidade de cada segmento
            segment_weights = []
            for segment in script_segments:
                # Peso baseado no comprimento do texto
                text_weight = len(segment.strip())
                
                # Peso adicional para segmentos com pontuação (pausas naturais)
                punctuation_weight = segment.count('.') + segment.count('!') + segment.count('?')
                
                # Peso final
                total_weight = text_weight + (punctuation_weight * 50)
                segment_weights.append(max(total_weight, 100))  # Mínimo de 100
            
            # Normalizar pesos para distribuir o tempo total
            total_weight = sum(segment_weights)
            timings = []
            current_time = 0.0
            
            for i, weight in enumerate(segment_weights):
                duration = (weight / total_weight) * total_duration
                # Garantir duração mínima e máxima
                duration = max(2.0, min(duration, total_duration * 0.4))
                
                start_time = current_time
                end_time = current_time + duration
                timings.append((start_time, end_time))
                current_time = end_time
            
            # Ajustar último timing para corresponder à duração total
            if timings and current_time != total_duration:
                last_start, _ = timings[-1]
                timings[-1] = (last_start, total_duration)
            
            self._log('info', f'Timing inteligente calculado baseado no script')
            return timings
            
        except Exception as e:
            self._log('warning', f'Erro no cálculo inteligente: {str(e)}')
            return []
    
    def _calculate_adaptive_timings(self, images: List[Dict[str, Any]], 
                                  total_duration: float) -> List[Tuple[float, float]]:
        """Calcular timing adaptativo baseado no tipo e características das imagens"""
        num_images = len(images)
        
        # Analisar características das imagens
        image_weights = []
        for img_data in images:
            weight = 1.0  # Peso base
            
            # Ajustar peso baseado no tipo de imagem (se disponível)
            img_type = img_data.get('type', 'unknown')
            if img_type in ['title', 'intro']:
                weight = 1.3  # Imagens de título ficam mais tempo
            elif img_type in ['transition', 'outro']:
                weight = 0.8  # Transições ficam menos tempo
            elif img_type in ['detail', 'close-up']:
                weight = 1.1  # Detalhes ficam um pouco mais
            
            # Ajustar baseado na descrição (se disponível)
            description = img_data.get('description', '').lower()
            if any(word in description for word in ['complex', 'detailed', 'chart', 'graph']):
                weight *= 1.2  # Imagens complexas precisam de mais tempo
            elif any(word in description for word in ['simple', 'logo', 'icon']):
                weight *= 0.9  # Imagens simples precisam de menos tempo
            
            image_weights.append(weight)
        
        # Normalizar pesos
        total_weight = sum(image_weights)
        timings = []
        current_time = 0.0
        
        # Calcular duração mínima baseada no número de imagens e duração total
        # Garantir que todas as imagens sejam distribuídas uniformemente
        min_duration_per_image = total_duration / num_images * 0.8  # 80% da duração uniforme como mínimo
        
        for i, weight in enumerate(image_weights):
            # Calcular duração proporcional ao peso
            duration = (weight / total_weight) * total_duration
            
            # Garantir duração mínima baseada na distribuição uniforme
            # e duração máxima mais flexível para melhor distribuição
            min_duration = max(min_duration_per_image, 2.0)  # Mínimo de 2 segundos ou a duração uniforme
            max_duration = total_duration / num_images * 2.0  # Máximo de 2x a duração uniforme
            
            duration = max(min_duration, min(duration, max_duration))
            
            start_time = current_time
            end_time = current_time + duration
            timings.append((start_time, end_time))
            current_time = end_time
        
        # Ajustar último timing para corresponder à duração total
        if timings and current_time != total_duration:
            last_start, _ = timings[-1]
            timings[-1] = (last_start, total_duration)
        
        self._log('info', f'Timing adaptativo calculado - duração média por imagem: {total_duration/num_images:.2f}s')
        return timings
    
    def _calculate_uniform_timings(self, images: List[Dict[str, Any]], 
                                 total_duration: float) -> List[Tuple[float, float]]:
        """Calcular timing uniforme para distribuir as imagens por todo o vídeo"""
        num_images = len(images)
        
        if num_images == 0:
            return []
        
        # Se temos apenas uma imagem, ela ocupa toda a duração
        if num_images == 1:
            return [(0.0, total_duration)]
        
        # Calcular duração uniforme para cada imagem
        uniform_duration = total_duration / num_images
        
        timings = []
        current_time = 0.0
        
        for i in range(num_images):
            start_time = current_time
            end_time = current_time + uniform_duration
            timings.append((start_time, end_time))
            current_time = end_time
        
        # Ajustar último timing para corresponder exatamente à duração total
        # (compensar possíveis arredondamentos)
        if timings:
            last_start, _ = timings[-1]
            timings[-1] = (last_start, total_duration)
        
        self._log('info', f'Timing uniforme calculado - {num_images} imagens com {uniform_duration:.2f}s cada')
        return timings
    
    def _analyze_script_segments(self, script_text: str) -> List[str]:
        """Analisar script e dividir em segmentos lógicos"""
        import re
        
        # Dividir por pontos, exclamações e interrogações
        segments = re.split(r'[.!?]+', script_text)
        
        # Limpar e filtrar segmentos
        cleaned_segments = []
        for segment in segments:
            segment = segment.strip()
            if segment and len(segment) > 10:  # Mínimo 10 caracteres
                cleaned_segments.append(segment)
        
        # Se temos poucos segmentos, dividir por vírgulas também
        if len(cleaned_segments) < 3:
            all_segments = []
            for segment in cleaned_segments:
                sub_segments = [s.strip() for s in segment.split(',') if s.strip()]
                all_segments.extend(sub_segments)
            if len(all_segments) > len(cleaned_segments):
                cleaned_segments = all_segments
        
        return cleaned_segments
    
    def _create_image_clips(self, images: List[Dict[str, Any]], 
                          timings: List[Tuple[float, float]], 
                          resolution: str) -> List:
        """Criar clipes de imagem"""
        image_clips = []
        width, height = map(int, resolution.split('x'))
        
        for i, (img_data, (start_time, end_time)) in enumerate(zip(images, timings)):
            try:
                img_path = img_data['file_path']
                duration = end_time - start_time
                
                self._log('info', f'Processando imagem {i + 1}/{len(images)}: {os.path.basename(img_path)}')
                
                # Verificar se o arquivo existe antes de tentar carregar
                if not os.path.exists(img_path):
                    self._log('warning', f'Arquivo de imagem não encontrado: {img_path}')
                    # Tentar caminhos alternativos
                    alternative_paths = [
                        os.path.join(os.path.dirname(__file__), '..', 'output', 'images', os.path.basename(img_path)),
                        os.path.join('output', 'images', os.path.basename(img_path)),
                        os.path.join('outputs', 'images', os.path.basename(img_path))
                    ]
                    
                    found = False
                    for alt_path in alternative_paths:
                        if os.path.exists(alt_path):
                            img_path = alt_path
                            found = True
                            self._log('info', f'Arquivo encontrado em caminho alternativo: {img_path}')
                            break
                    
                    if not found:
                        raise Exception(f'Arquivo de imagem não encontrado em nenhum caminho: {img_path}')
                
                # Criar clipe de imagem
                try:
                    from moviepy import ImageClip as MoviePyImageClip
                    img_clip = MoviePyImageClip(img_path)
                    img_clip = img_clip.with_duration(duration)
                    self._log('info', f'Clipe de imagem criado com duração: {duration:.2f}s, tamanho: {img_clip.w}x{img_clip.h}')
                    
                    # Verificar se a imagem foi carregada corretamente
                    if img_clip.w == 0 or img_clip.h == 0:
                        raise Exception(f'Imagem com dimensões inválidas: {img_clip.w}x{img_clip.h}')
                        
                except ImportError:
                    raise Exception('ImageClip não disponível - MoviePy não está instalado corretamente')
                except Exception as e:
                    self._log('error', f'Erro ao criar clipe de imagem: {str(e)}')
                    raise
                
                # Redimensionar mantendo proporção - usar método mais robusto
                if img_clip.h > img_clip.w:  # Imagem vertical
                    # Redimensionar pela altura
                    img_clip = img_clip.resized(height=height)
                    self._log('info', f'Imagem vertical redimensionada para altura {height}, novo tamanho: {img_clip.w}x{img_clip.h}')
                    
                    # Se ainda for mais larga que o vídeo, redimensionar pela largura
                    if img_clip.w > width:
                        img_clip = img_clip.resized(width=width)
                        self._log('info', f'Imagem redimensionada para largura {width}, novo tamanho: {img_clip.w}x{img_clip.h}')
                else:  # Imagem horizontal ou quadrada
                    # Redimensionar pela largura
                    img_clip = img_clip.resized(width=width)
                    self._log('info', f'Imagem horizontal redimensionada para largura {width}, novo tamanho: {img_clip.w}x{img_clip.h}')
                    
                    # Se ainda for mais alta que o vídeo, redimensionar pela altura
                    if img_clip.h > height:
                        img_clip = img_clip.resized(height=height)
                        self._log('info', f'Imagem redimensionada para altura {height}, novo tamanho: {img_clip.w}x{img_clip.h}')
                
                # Centralizar imagem
                img_clip = img_clip.with_position('center')
                self._log('info', f'Imagem centralizada')
                
                # Adicionar fundo preto se necessário - garantir que todas as imagens tenham fundo
                try:
                    from moviepy import ColorClip as MoviePyColorClip, CompositeVideoClip as MoviePyCompositeVideoClip
                    background = MoviePyColorClip(size=(width, height), color=(0, 0, 0), duration=duration)
                    img_clip = MoviePyCompositeVideoClip([background, img_clip.with_position('center')])
                    self._log('info', f'Fundo preto adicionado para imagem {i+1} (tamanho ajustado)')
                except ImportError:
                    self._log('warning', 'ColorClip/CompositeVideoClip não disponível, usando imagem sem fundo')
                except Exception as e:
                    self._log('error', f'Erro ao adicionar fundo preto: {str(e)}')
                
                image_clips.append(img_clip)
                
                self._log('info', f'Imagem {i + 1}/{len(images)} processada com sucesso (duração: {duration:.2f}s, tamanho final: {img_clip.w}x{img_clip.h})')
                
            except Exception as e:
                self._log('warning', f'Erro ao criar clipe {i+1}: {str(e)}')
                # Criar clipe de cor sólida como fallback
                try:
                    from moviepy import ColorClip as MoviePyColorClip
                    fallback_clip = MoviePyColorClip(
                        size=(width, height), 
                        color=(64, 64, 64),  # Usar cinza escuro em vez de preto para melhor visualização
                        duration=end_time - start_time
                    )
                    self._log('warning', f'Usando clipe de fallback cinza para imagem {i+1}')
                    image_clips.append(fallback_clip)
                except ImportError:
                    self._log('error', 'Não foi possível criar clipe de fallback - ColorClip não disponível')
                    continue
        
        return image_clips
    
    def _add_transitions(self, clips: List) -> List:
        """Adicionar transições entre clipes"""
        if len(clips) <= 1:
            return clips
        
        transition_duration = 0.5  # 0.5 segundos de transição
        
        transitioned_clips = []
        
        for i, clip in enumerate(clips):
            # Verificar se o clipe é um CompositeVideoClip
            if hasattr(clip, 'fadein'):
                # Clip normal: aplicar transições
                if i == 0:
                    # Primeiro clipe: apenas fade in
                    clip = clip.fadein(transition_duration)
                elif i == len(clips) - 1:
                    # Último clipe: apenas fade out
                    clip = clip.fadeout(transition_duration)
                else:
                    # Clipes do meio: fade in e fade out
                    clip = clip.fadein(transition_duration).fadeout(transition_duration)
            else:
                # CompositeVideoClip: não aplicar transições diretamente
                self._log('warning', f'Clip {i+1} é um CompositeVideoClip, transições não aplicadas')
            
            transitioned_clips.append(clip)
        
        self._log('info', f'Transições processadas para {len(clips)} clipes')
        return transitioned_clips
    
    def _add_subtitles(self, video_clip, script_text: str, duration: float, tts_segments: List[Dict] = None):
        """Adicionar legendas ao vídeo com sincronização baseada em TTS"""
        try:
            # Usar segmentos TTS se disponíveis para sincronização precisa
            if tts_segments:
                segments = self._create_tts_based_subtitle_segments(script_text, tts_segments)
            else:
                # Fallback para método tradicional
                segments = self._create_subtitle_segments(script_text, duration)
            
            subtitle_clips = []
            
            for segment in segments:
                try:
                    # Criar clipe de texto
                    txt_clip = TextClip(
                        text=segment['text'],
                        font_size=24,
                        color='white',
                        stroke_color='black',
                        stroke_width=2,
                        font='C:/Windows/Fonts/arial.ttf'
                    )
                    txt_clip = txt_clip.with_position(('center', 'bottom')).with_start(segment['start']).with_duration(segment['duration'])
                    
                    subtitle_clips.append(txt_clip)
                    
                except Exception as e:
                    self._log('warning', f'Erro ao criar legenda: {str(e)}')
                    continue
            
            if subtitle_clips:
                # Combinar vídeo com legendas
                final_video = CompositeVideoClip([video_clip] + subtitle_clips)
                self._log('info', f'Legendas adicionadas: {len(subtitle_clips)} segmentos')
                return final_video
            
        except Exception as e:
            self._log('warning', f'Erro ao adicionar legendas: {str(e)}')
        
        return video_clip
    
    def _create_tts_based_subtitle_segments(self, script_text: str, tts_segments: List[Dict]) -> List[Dict[str, Any]]:
        """Criar segmentos de legenda baseados nos segmentos TTS"""
        segments = []
        current_time = 0.0
        
        # Dividir texto em sentenças
        sentences = self._split_into_sentences(script_text)
        
        if not sentences:
            return []
        
        # Calcular duração total dos segmentos TTS
        total_tts_duration = sum(seg.get('duration', 0) for seg in tts_segments if seg.get('duration'))
        
        if total_tts_duration > 0:
            # Distribuir sentenças baseado na duração dos segmentos TTS
            sentences_per_segment = max(1, len(sentences) // len(tts_segments))
            
            sentence_index = 0
            for i, tts_segment in enumerate(tts_segments):
                segment_duration = tts_segment.get('duration', 3.0)
                
                # Determinar quantas sentenças cabem neste segmento
                end_sentence_index = min(sentence_index + sentences_per_segment, len(sentences))
                
                # Se é o último segmento TTS, incluir todas as sentenças restantes
                if i == len(tts_segments) - 1:
                    end_sentence_index = len(sentences)
                
                # Combinar sentenças para este segmento
                segment_sentences = sentences[sentence_index:end_sentence_index]
                if segment_sentences:
                    combined_text = ' '.join(segment_sentences)
                    
                    # Dividir texto longo em múltiplas legendas
                    if len(combined_text) > 80:  # Máximo 80 caracteres por legenda
                        sub_segments = self._split_long_subtitle(combined_text, segment_duration, current_time)
                        segments.extend(sub_segments)
                    else:
                        segments.append({
                            'text': combined_text,
                            'start': current_time,
                            'duration': segment_duration
                        })
                    
                    sentence_index = end_sentence_index
                
                current_time += segment_duration
        else:
            # Fallback para método tradicional
            return self._create_subtitle_segments(script_text, current_time or 60.0)
        
        return segments
    
    def _split_long_subtitle(self, text: str, total_duration: float, start_time: float) -> List[Dict[str, Any]]:
        """Dividir legenda longa em múltiplos segmentos"""
        words = text.split()
        segments = []
        
        # Dividir em chunks de ~12-15 palavras
        chunk_size = 12
        num_chunks = max(1, len(words) // chunk_size)
        duration_per_chunk = total_duration / num_chunks
        
        current_start = start_time
        for i in range(0, len(words), chunk_size):
            chunk_words = words[i:i + chunk_size]
            chunk_text = ' '.join(chunk_words)
            
            segments.append({
                'text': chunk_text,
                'start': current_start,
                'duration': min(duration_per_chunk, 4.0)  # Máximo 4 segundos por chunk
            })
            
            current_start += duration_per_chunk
        
        return segments
    
    def _create_subtitle_segments(self, script_text: str, duration: float) -> List[Dict[str, Any]]:
        """Criar segmentos de legenda (método tradicional)"""
        # Dividir texto em sentenças
        sentences = self._split_into_sentences(script_text)
        
        if not sentences:
            return []
        
        # Calcular timing para cada sentença
        time_per_sentence = duration / len(sentences)
        
        segments = []
        for i, sentence in enumerate(sentences):
            start_time = i * time_per_sentence
            segment_duration = min(time_per_sentence, 5.0)  # Máximo 5 segundos por legenda
            
            segments.append({
                'text': sentence.strip(),
                'start': start_time,
                'duration': segment_duration
            })
        
        return segments
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Dividir texto em sentenças"""
        import re
        
        # Dividir por pontos, exclamações e interrogações
        sentences = re.split(r'[.!?]+', text)
        
        # Limpar e filtrar sentenças vazias
        cleaned_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and len(sentence) > 10:  # Mínimo 10 caracteres
                # Limitar tamanho da legenda
                if len(sentence) > 100:
                    # Dividir sentenças muito longas
                    words = sentence.split()
                    chunk_size = 15  # ~15 palavras por legenda
                    
                    for i in range(0, len(words), chunk_size):
                        chunk = ' '.join(words[i:i + chunk_size])
                        if chunk.strip():
                            cleaned_sentences.append(chunk.strip())
                else:
                    cleaned_sentences.append(sentence)
        
        return cleaned_sentences
    
    def _get_codec_settings(self, quality: str) -> Dict[str, Any]:
        """Obter configurações de codec otimizadas baseadas na qualidade"""
        quality_settings = {
            'low': {
                'bitrate': '1200k',
                'preset': 'ultrafast',
                'crf': 28,
                'threads': 4,
                'tune': 'fastdecode'
            },
            'medium': {
                'bitrate': '2800k',
                'preset': 'fast',
                'crf': 23,
                'threads': 6,
                'tune': 'film'
            },
            'high': {
                'bitrate': '5500k',
                'preset': 'medium',
                'crf': 20,
                'threads': 8,
                'tune': 'film'
            },
            'ultra': {
                'bitrate': '9000k',
                'preset': 'slow',
                'crf': 18,
                'threads': 8,
                'tune': 'film'
            }
        }
        
        return quality_settings.get(quality, quality_settings['high'])
    
    def _get_adaptive_codec_settings(self, quality: str, resolution: str, duration: float) -> Dict[str, Any]:
        """Obter configurações adaptativas baseadas na qualidade, resolução e duração"""
        # Configurações base
        base_settings = self._get_codec_settings(quality)
        
        # Adaptações baseadas na resolução
        width, height = map(int, resolution.split('x'))
        pixel_count = width * height
        
        # Ajustar bitrate baseado na resolução
        if pixel_count <= 921600:  # 720p ou menor
            bitrate_multiplier = 0.7
        elif pixel_count <= 2073600:  # 1080p
            bitrate_multiplier = 1.0
        elif pixel_count <= 3686400:  # 1440p
            bitrate_multiplier = 1.4
        else:  # 4K ou maior
            bitrate_multiplier = 2.0
        
        # Ajustar bitrate baseado na duração
        if duration < 60:  # Vídeos curtos (< 1 min)
            duration_multiplier = 1.2
        elif duration < 300:  # Vídeos médios (< 5 min)
            duration_multiplier = 1.0
        elif duration < 900:  # Vídeos longos (< 15 min)
            duration_multiplier = 0.9
        else:  # Vídeos muito longos
            duration_multiplier = 0.8
        
        # Calcular bitrate adaptativo
        base_bitrate = int(base_settings['bitrate'].replace('k', ''))
        adaptive_bitrate = int(base_bitrate * bitrate_multiplier * duration_multiplier)
        
        # Aplicar limites mínimos e máximos
        adaptive_bitrate = max(800, min(adaptive_bitrate, 15000))
        
        # Atualizar configurações
        adaptive_settings = base_settings.copy()
        adaptive_settings['bitrate'] = f'{adaptive_bitrate}k'
        
        # Ajustar preset baseado na resolução para otimizar tempo vs qualidade
        if pixel_count >= 3686400:  # 1440p ou maior
            if adaptive_settings['preset'] == 'slow':
                adaptive_settings['preset'] = 'medium'  # Mais rápido para resoluções altas
            elif adaptive_settings['preset'] == 'veryslow':
                adaptive_settings['preset'] = 'slow'
        
        self._log('info', f'Configurações adaptativas: bitrate={adaptive_bitrate}k, preset={adaptive_settings["preset"]}')
        
        return adaptive_settings
    
    def _render_video_optimized(self, video_clip, output_path: str, fps: int, codec_settings: Dict[str, Any]):
        """Renderização otimizada de vídeo com configurações avançadas"""
        try:
            import multiprocessing
            
            # Detectar número de cores disponíveis
            cpu_count = multiprocessing.cpu_count()
            threads = min(int(codec_settings.get('threads', 4)), cpu_count)
            
            # Configurações otimizadas de renderização
            render_params = {
                'fps': int(fps),
                'codec': 'libx264',
                'audio_codec': 'aac',
                'bitrate': codec_settings.get('bitrate', '5500k'),
                'preset': codec_settings.get('preset', 'medium'),
                'threads': threads,
                'logger': None,
                'temp_audiofile': os.path.join(self.temp_dir, 'temp_audio.m4a'),
                'remove_temp': True
            }
            
            # Adicionar configurações avançadas se disponíveis
            if 'crf' in codec_settings:
                render_params['ffmpeg_params'] = ['-crf', str(codec_settings['crf'])]
                
            if 'tune' in codec_settings:
                if 'ffmpeg_params' not in render_params:
                    render_params['ffmpeg_params'] = []
                render_params['ffmpeg_params'].extend(['-tune', codec_settings['tune']])
            
            # Otimizações adicionais para performance
            if 'ffmpeg_params' not in render_params:
                render_params['ffmpeg_params'] = []
            
            render_params['ffmpeg_params'].extend([
                '-movflags', '+faststart',  # Otimização para streaming
                '-pix_fmt', 'yuv420p',      # Compatibilidade máxima
                '-profile:v', 'high',       # Perfil H.264 otimizado
                '-level', '4.0'             # Nível de compatibilidade
            ])
            
            self._log('info', f'Renderizando com {threads} threads, preset: {codec_settings.get("preset", "medium")}')
            
            # Renderizar vídeo
            video_clip.write_videofile(output_path, **render_params)
            
            self._log('info', 'Renderização otimizada concluída')
            
        except Exception as e:
            error_msg = str(e)
            self._log('error', f'Erro na renderização otimizada: {error_msg}')
            
            # Verificar se é erro de FFmpeg
            if 'ffmpeg' in error_msg.lower() or 'codec' in error_msg.lower():
                self._log('warning', 'Erro relacionado ao FFmpeg detectado')
            
            # Fallback para renderização básica
            self._log('info', 'Tentando renderização básica como fallback')
            try:
                video_clip.write_videofile(
                    output_path,
                    fps=int(fps),
                    codec='libx264',
                    audio_codec='aac',
                    bitrate=codec_settings.get('bitrate', '5500k'),
                    preset=codec_settings.get('preset', 'medium'),
                    logger=None
                )
                self._log('info', 'Renderização básica concluída com sucesso')
            except Exception as fallback_error:
                self._log('error', f'Falha também na renderização básica: {str(fallback_error)}')
                raise
    
    def create_preview(self, video_path: str, duration: int = 30) -> Optional[str]:
        """Criar preview do vídeo"""
        try:
            self._log('info', 'Criando preview do vídeo')
            
            # Carregar vídeo
            video = VideoFileClip(video_path)
            
            # Criar preview dos primeiros X segundos
            preview_duration = min(duration, video.duration)
            preview = video.subclipped(0, preview_duration)
            
            # Salvar preview
            preview_filename = f"preview_{self.pipeline_id}.mp4"
            preview_path = os.path.join(self.output_dir, preview_filename)
            
            preview.write_videofile(
                preview_path,
                fps=15,  # FPS menor para preview
                codec='libx264',
                bitrate='1000k',
                logger=None
            )
            
            # Limpar recursos
            preview.close()
            video.close()
            
            self._log('info', f'Preview criado: {preview_path}')
            return preview_path
            
        except Exception as e:
            self._log('error', f'Erro ao criar preview: {str(e)}')
            return None
    
    def cleanup_temp_files(self):
        """Limpar arquivos temporários"""
        try:
            import shutil
            
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
                self._log('info', 'Arquivos temporários removidos')
                
        except Exception as e:
            self._log('warning', f'Erro ao limpar arquivos temporários: {str(e)}')