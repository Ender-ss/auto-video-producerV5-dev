#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de exemplos práticos para MoviePy no projeto auto-video-producerV5-dev

Este script demonstra diversos exemplos práticos de uso do MoviePy,
incluindo criação, edição, efeitos, texto, áudio e composição de vídeos.
"""

import os
import sys
import numpy as np
import tempfile
from pathlib import Path

# Verificar se o MoviePy está instalado
try:
    import moviepy
    from moviepy.editor import *
    from moviepy.video.fx import FadeIn, FadeOut, blackwhite, lum_contrast, resize, crop
    from moviepy.audio.fx import volumex, audio_fadein, audio_fadeout
    MOVIEPY_INSTALLED = True
except ImportError as e:
    print(f"ERRO: MoviePy não está instalado: {e}")
    MOVIEPY_INSTALLED = False

# Configurações
TEMP_DIR = tempfile.gettempdir()
EXAMPLES_DIR = os.path.join(TEMP_DIR, "moviepy_examples")
os.makedirs(EXAMPLES_DIR, exist_ok=True)

# Cores para output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def color_print(text, color=Colors.WHITE):
    """Imprime texto com cor"""
    print(f"{color}{text}{Colors.ENDC}")

def print_header(title):
    """Imprime um cabeçalho"""
    color_print("=" * 60, Colors.CYAN)
    color_print(title.center(60), Colors.CYAN)
    color_print("=" * 60, Colors.CYAN)
    print()

def print_section(title):
    """Imprime uma seção"""
    color_print("-" * 40, Colors.BLUE)
    color_print(title, Colors.BLUE)
    color_print("-" * 40, Colors.BLUE)
    print()

def print_example(example_name, description):
    """Imprime um exemplo"""
    color_print(f"Exemplo: {example_name}", Colors.MAGENTA)
    print(f"{description}")
    print()

class MoviePyExamples:
    """Classe para exemplos do MoviePy"""
    
    def __init__(self):
        self.examples = []
        self.start_time = time.time()
    
    def add_example(self, example_name, success, message=""):
        """Adiciona um exemplo"""
        self.examples.append((example_name, success, message))
        if success:
            color_print(f"✓ {example_name}: SUCESSO", Colors.GREEN)
        else:
            color_print(f"✗ {example_name}: FALHA", Colors.RED)
        
        if message:
            print(f"  {message}")
        
        print()
    
    def run_all_examples(self):
        """Executa todos os exemplos"""
        print_header("EXEMPLOS PRÁTICOS DO MOVIEPY")
        
        if not MOVIEPY_INSTALLED:
            color_print("MoviePy não está instalado. Abortando exemplos.", Colors.RED)
            return False
        
        # Exemplos básicos
        self.example_basic_color_clip()
        self.example_basic_image_clip()
        self.example_basic_text_clip()
        self.example_basic_audio_clip()
        
        # Exemplos de edição
        self.example_editing_subclip()
        self.example_editing_resize()
        self.example_editing_crop()
        self.example_editing_rotate()
        
        # Exemplos de efeitos
        self.example_effects_fade()
        self.example_effects_color()
        self.example_effects_multiple()
        
        # Exemplos de texto
        self.example_text_basic()
        self.example_text_styled()
        self.example_text_animated()
        
        # Exemplos de áudio
        self.example_audio_basic()
        self.example_audio_effects()
        self.example_audio_video()
        
        # Exemplos de composição
        self.example_composition_basic()
        self.example_composition_concatenate()
        self.example_composition_array()
        
        # Exemplos de exportação
        self.example_export_basic()
        self.example_export_with_audio()
        self.example_export_different_formats()
        
        # Exemplo de projeto completo
        self.example_complete_project()
        
        # Resumo
        self.print_summary()
        
        return True
    
    def example_basic_color_clip(self):
        """Exemplo básico: criar um clipe de cor"""
        print_section("Exemplo Básico: Clipe de Cor")
        
        try:
            # Criar um clipe de cor vermelha
            clip = ColorClip(size=(640, 480), color=(255, 0, 0), duration=5)
            
            # Salvar o clipe
            output_path = os.path.join(EXAMPLES_DIR, "basic_color_clip.mp4")
            clip.write_videofile(output_path, fps=24, logger=None)
            
            self.add_example(
                "Clipe de Cor",
                True,
                f"Vídeo salvo em: {output_path}"
            )
        except Exception as e:
            self.add_example(
                "Clipe de Cor",
                False,
                f"Erro: {e}"
            )
    
    def example_basic_image_clip(self):
        """Exemplo básico: criar um clipe a partir de uma imagem"""
        print_section("Exemplo Básico: Clipe de Imagem")
        
        try:
            # Criar uma imagem simples com numpy
            img_array = np.zeros((480, 640, 3), dtype=np.uint8)
            img_array[:, :, 1] = 255  # Canal verde
            
            # Criar um clipe a partir da imagem
            clip = ImageClip(img_array, duration=5)
            
            # Salvar o clipe
            output_path = os.path.join(EXAMPLES_DIR, "basic_image_clip.mp4")
            clip.write_videofile(output_path, fps=24, logger=None)
            
            self.add_example(
                "Clipe de Imagem",
                True,
                f"Vídeo salvo em: {output_path}"
            )
        except Exception as e:
            self.add_example(
                "Clipe de Imagem",
                False,
                f"Erro: {e}"
            )
    
    def example_basic_text_clip(self):
        """Exemplo básico: criar um clipe de texto"""
        print_section("Exemplo Básico: Clipe de Texto")
        
        try:
            # Criar um clipe de texto
            txt = TextClip(
                text="Exemplo de Texto",
                font_size=70,
                color='white',
                font='C:/Windows/Fonts/arial.ttf'
            ).set_duration(5)
            
            # Salvar o clipe
            output_path = os.path.join(EXAMPLES_DIR, "basic_text_clip.mp4")
            txt.write_videofile(output_path, fps=24, logger=None)
            
            self.add_example(
                "Clipe de Texto",
                True,
                f"Vídeo salvo em: {output_path}"
            )
        except Exception as e:
            self.add_example(
                "Clipe de Texto",
                False,
                f"Erro: {e}"
            )
    
    def example_basic_audio_clip(self):
        """Exemplo básico: criar um clipe de áudio"""
        print_section("Exemplo Básico: Clipe de Áudio")
        
        try:
            # Criar um áudio sintético
            duration = 5
            sample_rate = 44100
            t = np.linspace(0, duration, int(duration * sample_rate), False)
            
            # Criar onda senoidal
            frequency = 440  # Hz
            audio_data = np.sin(2 * np.pi * frequency * t)
            
            # Normalizar
            audio_data = audio_data / np.max(np.abs(audio_data))
            
            # Reduzir amplitude
            audio_data = audio_data * 0.5
            
            # Criar clipe de áudio
            audio_clip = AudioArrayClip(audio_data, fps=sample_rate)
            
            # Salvar o clipe
            output_path = os.path.join(EXAMPLES_DIR, "basic_audio_clip.mp3")
            audio_clip.write_audiofile(output_path, fps=sample_rate, logger=None)
            
            self.add_example(
                "Clipe de Áudio",
                True,
                f"Áudio salvo em: {output_path}"
            )
        except Exception as e:
            self.add_example(
                "Clipe de Áudio",
                False,
                f"Erro: {e}"
            )
    
    def example_editing_subclip(self):
        """Exemplo de edição: criar um subclip"""
        print_section("Exemplo de Edição: Subclip")
        
        try:
            # Criar um clipe original
            original_clip = ColorClip(size=(640, 480), color=(255, 0, 0), duration=10)
            
            # Criar um subclip do segundo 2 ao 5
            subclip = original_clip.subclip(2, 5)
            
            # Salvar o subclip
            output_path = os.path.join(EXAMPLES_DIR, "editing_subclip.mp4")
            subclip.write_videofile(output_path, fps=24, logger=None)
            
            self.add_example(
                "Subclip",
                True,
                f"Vídeo salvo em: {output_path} (duração: 3s)"
            )
        except Exception as e:
            self.add_example(
                "Subclip",
                False,
                f"Erro: {e}"
            )
    
    def example_editing_resize(self):
        """Exemplo de edição: redimensionar um clipe"""
        print_section("Exemplo de Edição: Redimensionar")
        
        try:
            # Criar um clipe original
            original_clip = ColorClip(size=(640, 480), color=(0, 255, 0), duration=5)
            
            # Redimensionar para 320x240
            resized_clip = original_clip.resize((320, 240))
            
            # Salvar o clipe redimensionado
            output_path = os.path.join(EXAMPLES_DIR, "editing_resize.mp4")
            resized_clip.write_videofile(output_path, fps=24, logger=None)
            
            self.add_example(
                "Redimensionar",
                True,
                f"Vídeo salvo em: {output_path} (320x240)"
            )
        except Exception as e:
            self.add_example(
                "Redimensionar",
                False,
                f"Erro: {e}"
            )
    
    def example_editing_crop(self):
        """Exemplo de edição: cortar um clipe"""
        print_section("Exemplo de Edição: Cortar")
        
        try:
            # Criar um clipe original
            original_clip = ColorClip(size=(640, 480), color=(0, 0, 255), duration=5)
            
            # Cortar para 320x240 a partir do centro
            cropped_clip = crop(original_clip, x_center=320, y_center=240, width=320, height=240)
            
            # Salvar o clipe cortado
            output_path = os.path.join(EXAMPLES_DIR, "editing_crop.mp4")
            cropped_clip.write_videofile(output_path, fps=24, logger=None)
            
            self.add_example(
                "Cortar",
                True,
                f"Vídeo salvo em: {output_path} (320x240)"
            )
        except Exception as e:
            self.add_example(
                "Cortar",
                False,
                f"Erro: {e}"
            )
    
    def example_editing_rotate(self):
        """Exemplo de edição: rotacionar um clipe"""
        print_section("Exemplo de Edição: Rotacionar")
        
        try:
            # Criar um clipe original
            original_clip = ColorClip(size=(640, 480), color=(255, 255, 0), duration=5)
            
            # Rotacionar 45 graus
            rotated_clip = original_clip.rotate(45)
            
            # Salvar o clipe rotacionado
            output_path = os.path.join(EXAMPLES_DIR, "editing_rotate.mp4")
            rotated_clip.write_videofile(output_path, fps=24, logger=None)
            
            self.add_example(
                "Rotacionar",
                True,
                f"Vídeo salvo em: {output_path} (45 graus)"
            )
        except Exception as e:
            self.add_example(
                "Rotacionar",
                False,
                f"Erro: {e}"
            )
    
    def example_effects_fade(self):
        """Exemplo de efeitos: fade in/out"""
        print_section("Exemplo de Efeitos: Fade In/Out")
        
        try:
            # Criar um clipe original
            original_clip = ColorClip(size=(640, 480), color=(255, 0, 255), duration=5)
            
            # Aplicar fade in e fade out (MoviePy 2.1.2)
            faded_clip = original_clip.with_effects([FadeIn(1), FadeOut(1)])
            
            # Salvar o clipe com fade
            output_path = os.path.join(EXAMPLES_DIR, "effects_fade.mp4")
            faded_clip.write_videofile(output_path, fps=24, logger=None)
            
            self.add_example(
                "Fade In/Out",
                True,
                f"Vídeo salvo em: {output_path}"
            )
        except Exception as e:
            self.add_example(
                "Fade In/Out",
                False,
                f"Erro: {e}"
            )
    
    def example_effects_color(self):
        """Exemplo de efeitos: efeitos de cor"""
        print_section("Exemplo de Efeitos: Efeitos de Cor")
        
        try:
            # Criar um clipe original
            original_clip = ColorClip(size=(640, 480), color=(128, 128, 128), duration=5)
            
            # Aplicar efeito preto e branco
            bw_clip = original_clip.fx(blackwhite)
            
            # Aplicar efeito de brilho e contraste
            contrast_clip = original_clip.fx(lum_contrast, lum=0.5, contrast=1.5)
            
            # Combinar os efeitos
            final_clip = concatenate_videoclips([original_clip, bw_clip, contrast_clip])
            
            # Salvar o clipe com efeitos
            output_path = os.path.join(EXAMPLES_DIR, "effects_color.mp4")
            final_clip.write_videofile(output_path, fps=24, logger=None)
            
            self.add_example(
                "Efeitos de Cor",
                True,
                f"Vídeo salvo em: {output_path}"
            )
        except Exception as e:
            self.add_example(
                "Efeitos de Cor",
                False,
                f"Erro: {e}"
            )
    
    def example_effects_multiple(self):
        """Exemplo de efeitos: múltiplos efeitos"""
        print_section("Exemplo de Efeitos: Múltiplos Efeitos")
        
        try:
            # Criar um clipe original
            original_clip = ColorClip(size=(640, 480), color=(255, 128, 0), duration=5)
            
            # Aplicar múltiplos efeitos
            final_clip = original_clip
            final_clip = final_clip.fx(blackwhite)
            final_clip = final_clip.fx(lum_contrast, lum=0.5, contrast=1.5)
            final_clip = final_clip.resize(0.5)  # Reduzir para 50%
            final_clip = final_clip.with_effects([FadeIn(1), FadeOut(1)])
            
            # Salvar o clipe com múltiplos efeitos
            output_path = os.path.join(EXAMPLES_DIR, "effects_multiple.mp4")
            final_clip.write_videofile(output_path, fps=24, logger=None)
            
            self.add_example(
                "Múltiplos Efeitos",
                True,
                f"Vídeo salvo em: {output_path}"
            )
        except Exception as e:
            self.add_example(
                "Múltiplos Efeitos",
                False,
                f"Erro: {e}"
            )
    
    def example_text_basic(self):
        """Exemplo de texto: texto básico"""
        print_section("Exemplo de Texto: Texto Básico")
        
        try:
            # Criar um clipe de texto
            txt = TextClip(
                text="Texto Básico",
                font_size=70,
                color='white',
                font='C:/Windows/Fonts/arial.ttf'
            ).set_duration(5)
            
            # Salvar o clipe de texto
            output_path = os.path.join(EXAMPLES_DIR, "text_basic.mp4")
            txt.write_videofile(output_path, fps=24, logger=None)
            
            self.add_example(
                "Texto Básico",
                True,
                f"Vídeo salvo em: {output_path}"
            )
        except Exception as e:
            self.add_example(
                "Texto Básico",
                False,
                f"Erro: {e}"
            )
    
    def example_text_styled(self):
        """Exemplo de texto: texto estilizado"""
        print_section("Exemplo de Texto: Texto Estilizado")
        
        try:
            # Criar um clipe de texto estilizado
            txt = TextClip(
                text="Texto Estilizado",
                font_size=70,
                color='white',
                font='C:/Windows/Fonts/arial.ttf',
                stroke_color='black',
                stroke_width=2,
                method='label'
            ).set_duration(5)
            
            # Salvar o clipe de texto estilizado
            output_path = os.path.join(EXAMPLES_DIR, "text_styled.mp4")
            txt.write_videofile(output_path, fps=24, logger=None)
            
            self.add_example(
                "Texto Estilizado",
                True,
                f"Vídeo salvo em: {output_path}"
            )
        except Exception as e:
            self.add_example(
                "Texto Estilizado",
                False,
                f"Erro: {e}"
            )
    
    def example_text_animated(self):
        """Exemplo de texto: texto animado"""
        print_section("Exemplo de Texto: Texto Animado")
        
        try:
            # Criar um clipe de texto
            txt = TextClip(
                text="Texto Animado",
                font_size=70,
                color='white',
                font='C:/Windows/Fonts/arial.ttf'
            ).set_duration(5)
            
            # Animar o texto (mudar de posição)
            txt = txt.set_position(lambda t: (100 + t*50, 200))
            
            # Salvar o clipe de texto animado
            output_path = os.path.join(EXAMPLES_DIR, "text_animated.mp4")
            txt.write_videofile(output_path, fps=24, logger=None)
            
            self.add_example(
                "Texto Animado",
                True,
                f"Vídeo salvo em: {output_path}"
            )
        except Exception as e:
            self.add_example(
                "Texto Animado",
                False,
                f"Erro: {e}"
            )
    
    def example_audio_basic(self):
        """Exemplo de áudio: áudio básico"""
        print_section("Exemplo de Áudio: Áudio Básico")
        
        try:
            # Criar um áudio sintético
            duration = 5
            sample_rate = 44100
            t = np.linspace(0, duration, int(duration * sample_rate), False)
            
            # Criar onda senoidal
            frequency = 440  # Hz
            audio_data = np.sin(2 * np.pi * frequency * t)
            
            # Normalizar
            audio_data = audio_data / np.max(np.abs(audio_data))
            
            # Reduzir amplitude
            audio_data = audio_data * 0.5
            
            # Criar clipe de áudio
            audio_clip = AudioArrayClip(audio_data, fps=sample_rate)
            
            # Salvar o clipe de áudio
            output_path = os.path.join(EXAMPLES_DIR, "audio_basic.mp3")
            audio_clip.write_audiofile(output_path, fps=sample_rate, logger=None)
            
            self.add_example(
                "Áudio Básico",
                True,
                f"Áudio salvo em: {output_path}"
            )
        except Exception as e:
            self.add_example(
                "Áudio Básico",
                False,
                f"Erro: {e}"
            )
    
    def example_audio_effects(self):
        """Exemplo de áudio: efeitos de áudio"""
        print_section("Exemplo de Áudio: Efeitos de Áudio")
        
        try:
            # Criar um áudio sintético
            duration = 5
            sample_rate = 44100
            t = np.linspace(0, duration, int(duration * sample_rate), False)
            audio_data = np.sin(2 * np.pi * 440 * t)
            audio_data = audio_data / np.max(np.abs(audio_data))
            audio_data = audio_data * 0.5
            
            # Criar clipe de áudio
            audio_clip = AudioArrayClip(audio_data, fps=sample_rate)
            
            # Aplicar efeitos
            audio_clip = audio_clip.fx(volumex, 1.5)
            audio_clip = audio_clip.fx(audio_fadein, 1)
            audio_clip = audio_clip.fx(audio_fadeout, 1)
            
            # Salvar o clipe de áudio com efeitos
            output_path = os.path.join(EXAMPLES_DIR, "audio_effects.mp3")
            audio_clip.write_audiofile(output_path, fps=sample_rate, logger=None)
            
            self.add_example(
                "Efeitos de Áudio",
                True,
                f"Áudio salvo em: {output_path}"
            )
        except Exception as e:
            self.add_example(
                "Efeitos de Áudio",
                False,
                f"Erro: {e}"
            )
    
    def example_audio_video(self):
        """Exemplo de áudio: adicionar áudio a vídeo"""
        print_section("Exemplo de Áudio: Áudio com Vídeo")
        
        try:
            # Criar um clipe de vídeo
            video_clip = ColorClip(size=(640, 480), color=(128, 0, 128), duration=5)
            
            # Criar um áudio sintético
            duration = 5
            sample_rate = 44100
            t = np.linspace(0, duration, int(duration * sample_rate), False)
            audio_data = np.sin(2 * np.pi * 440 * t)
            audio_data = audio_data / np.max(np.abs(audio_data))
            audio_data = audio_data * 0.5
            
            # Criar clipe de áudio
            audio_clip = AudioArrayClip(audio_data, fps=sample_rate)
            
            # Adicionar áudio ao vídeo
            video_clip = video_clip.set_audio(audio_clip)
            
            # Salvar o vídeo com áudio
            output_path = os.path.join(EXAMPLES_DIR, "audio_video.mp4")
            video_clip.write_videofile(output_path, fps=24, logger=None)
            
            self.add_example(
                "Áudio com Vídeo",
                True,
                f"Vídeo salvo em: {output_path}"
            )
        except Exception as e:
            self.add_example(
                "Áudio com Vídeo",
                False,
                f"Erro: {e}"
            )
    
    def example_composition_basic(self):
        """Exemplo de composição: composição básica"""
        print_section("Exemplo de Composição: Composição Básica")
        
        try:
            # Criar um fundo
            background = ColorClip(size=(640, 480), color=(0, 0, 0), duration=5)
            
            # Criar clipes para composição
            clip1 = ColorClip(size=(100, 100), color=(255, 0, 0), duration=5)
            clip2 = ColorClip(size=(100, 100), color=(0, 255, 0), duration=5)
            clip3 = ColorClip(size=(100, 100), color=(0, 0, 255), duration=5)
            
            # Posicionar os clipes
            clip1 = clip1.with_position((50, 50))
            clip2 = clip2.with_position((170, 170))
            clip3 = clip3.with_position((290, 50))
            
            # Compor os clipes
            final_clip = CompositeVideoClip([background, clip1, clip2, clip3])
            
            # Salvar o clipe composto
            output_path = os.path.join(EXAMPLES_DIR, "composition_basic.mp4")
            final_clip.write_videofile(output_path, fps=24, logger=None)
            
            self.add_example(
                "Composição Básica",
                True,
                f"Vídeo salvo em: {output_path}"
            )
        except Exception as e:
            self.add_example(
                "Composição Básica",
                False,
                f"Erro: {e}"
            )
    
    def example_composition_concatenate(self):
        """Exemplo de composição: concatenar clipes"""
        print_section("Exemplo de Composição: Concatenar Clipes")
        
        try:
            # Criar clipes para concatenar
            clip1 = ColorClip(size=(640, 480), color=(255, 0, 0), duration=2)
            clip2 = ColorClip(size=(640, 480), color=(0, 255, 0), duration=2)
            clip3 = ColorClip(size=(640, 480), color=(0, 0, 255), duration=2)
            
            # Concatenar os clipes (MoviePy 2.1.2)
            final_clip = concatenate_videoclips([clip1, clip2, clip3])
            
            # Salvar o clipe concatenado
            output_path = os.path.join(EXAMPLES_DIR, "composition_concatenate.mp4")
            final_clip.write_videofile(output_path, fps=24, logger=None)
            
            self.add_example(
                "Concatenar Clipes",
                True,
                f"Vídeo salvo em: {output_path} (duração: 6s)"
            )
        except Exception as e:
            self.add_example(
                "Concatenar Clipes",
                False,
                f"Erro: {e}"
            )
    
    def example_composition_array(self):
        """Exemplo de composição: array de clipes"""
        print_section("Exemplo de Composição: Array de Clipes")
        
        try:
            # Criar clipes para o array
            clip1 = ColorClip(size=(100, 100), color=(255, 0, 0), duration=5)
            clip2 = ColorClip(size=(100, 100), color=(0, 255, 0), duration=5)
            clip3 = ColorClip(size=(100, 100), color=(0, 0, 255), duration=5)
            clip4 = ColorClip(size=(100, 100), color=(255, 255, 0), duration=5)
            
            # Criar matriz de clipes
            clips_matrix = [
                [clip1, clip2],
                [clip3, clip4]
            ]
            
            # Criar array de clipes
            final_clip = clips_array(clips_matrix)
            
            # Salvar o array de clipes
            output_path = os.path.join(EXAMPLES_DIR, "composition_array.mp4")
            final_clip.write_videofile(output_path, fps=24, logger=None)
            
            self.add_example(
                "Array de Clipes",
                True,
                f"Vídeo salvo em: {output_path}"
            )
        except Exception as e:
            self.add_example(
                "Array de Clipes",
                False,
                f"Erro: {e}"
            )
    
    def example_export_basic(self):
        """Exemplo de exportação: exportação básica"""
        print_section("Exemplo de Exportação: Exportação Básica")
        
        try:
            # Criar um clipe
            clip = ColorClip(size=(640, 480), color=(255, 128, 64), duration=5)
            
            # Salvar o clipe
            output_path = os.path.join(EXAMPLES_DIR, "export_basic.mp4")
            clip.write_videofile(output_path, fps=24, logger=None)
            
            self.add_example(
                "Exportação Básica",
                True,
                f"Vídeo salvo em: {output_path}"
            )
        except Exception as e:
            self.add_example(
                "Exportação Básica",
                False,
                f"Erro: {e}"
            )
    
    def example_export_with_audio(self):
        """Exemplo de exportação: exportação com áudio"""
        print_section("Exemplo de Exportação: Exportação com Áudio")
        
        try:
            # Criar um clipe de vídeo
            video_clip = ColorClip(size=(640, 480), color=(64, 128, 255), duration=5)
            
            # Criar um áudio sintético
            duration = 5
            sample_rate = 44100
            t = np.linspace(0, duration, int(duration * sample_rate), False)
            audio_data = np.sin(2 * np.pi * 440 * t)
            audio_data = audio_data / np.max(np.abs(audio_data))
            audio_data = audio_data * 0.5
            
            # Criar clipe de áudio
            audio_clip = AudioArrayClip(audio_data, fps=sample_rate)
            
            # Adicionar áudio ao vídeo
            video_clip = video_clip.set_audio(audio_clip)
            
            # Salvar o vídeo com áudio
            output_path = os.path.join(EXAMPLES_DIR, "export_with_audio.mp4")
            video_clip.write_videofile(output_path, fps=24, logger=None)
            
            self.add_example(
                "Exportação com Áudio",
                True,
                f"Vídeo salvo em: {output_path}"
            )
        except Exception as e:
            self.add_example(
                "Exportação com Áudio",
                False,
                f"Erro: {e}"
            )
    
    def example_export_different_formats(self):
        """Exemplo de exportação: exportação em diferentes formatos"""
        print_section("Exemplo de Exportação: Diferentes Formatos")
        
        try:
            # Criar um clipe
            clip = ColorClip(size=(640, 480), color=(128, 255, 128), duration=5)
            
            # Salvar em diferentes formatos
            formats = [
                ("mp4", "H.264"),
                ("webm", "VP9"),
                ("avi", "XVID"),
                ("mov", "H.264")
            ]
            
            for ext, codec in formats:
                output_path = os.path.join(EXAMPLES_DIR, f"export_format_{ext}.{ext}")
                clip.write_videofile(output_path, fps=24, codec=codec, logger=None)
                
                if os.path.exists(output_path):
                    color_print(f"✓ Exportação {ext.upper()}: SUCESSO", Colors.GREEN)
                else:
                    color_print(f"✗ Exportação {ext.upper()}: FALHA", Colors.RED)
            
            self.add_example(
                "Diferentes Formatos",
                True,
                f"Vídeos salvos em: {EXAMPLES_DIR}"
            )
        except Exception as e:
            self.add_example(
                "Diferentes Formatos",
                False,
                f"Erro: {e}"
            )
    
    def example_complete_project(self):
        """Exemplo de projeto completo"""
        print_section("Exemplo de Projeto Completo")
        
        try:
            # Criar um fundo
            background = ColorClip(size=(640, 480), color=(0, 0, 0), duration=10)
            
            # Criar um clipe de texto
            title = TextClip(
                text="Projeto Completo",
                font_size=70,
                color='white',
                font='C:/Windows/Fonts/arial.ttf'
            ).set_duration(3)
            
            # Posicionar o texto
            title = title.with_position('center')
            
            # Criar clipes coloridos
            clip1 = ColorClip(size=(200, 200), color=(255, 0, 0), duration=3)
            clip2 = ColorClip(size=(200, 200), color=(0, 255, 0), duration=3)
            clip3 = ColorClip(size=(200, 200), color=(0, 0, 255), duration=3)
            
            # Posicionar os clipes
            clip1 = clip1.with_position((50, 150))
            clip2 = clip2.with_position((220, 150))
            clip3 = clip3.with_position((390, 150))
            
            # Aplicar efeitos
            clip1 = clip1.with_effects([FadeIn(1), FadeOut(1)])
            clip2 = clip2.with_effects([FadeIn(1), FadeOut(1)])
            clip3 = clip3.with_effects([FadeIn(1), FadeOut(1)])
            
            # Criar um áudio sintético
            duration = 10
            sample_rate = 44100
            t = np.linspace(0, duration, int(duration * sample_rate), False)
            audio_data = np.sin(2 * np.pi * 440 * t)
            audio_data = audio_data / np.max(np.abs(audio_data))
            audio_data = audio_data * 0.5
            
            # Criar clipe de áudio
            audio_clip = AudioArrayClip(audio_data, fps=sample_rate)
            
            # Aplicar efeitos de áudio
            audio_clip = audio_clip.fx(volumex, 0.5)
            audio_clip = audio_clip.fx(audio_fadein, 1)
            audio_clip = audio_clip.fx(audio_fadeout, 1)
            
            # Criar a composição
            composition = CompositeVideoClip([background, title, clip1, clip2, clip3])
            
            # Adicionar áudio
            composition = composition.set_audio(audio_clip)
            
            # Salvar o projeto completo
            output_path = os.path.join(EXAMPLES_DIR, "complete_project.mp4")
            composition.write_videofile(output_path, fps=24, logger=None)
            
            self.add_example(
                "Projeto Completo",
                True,
                f"Vídeo salvo em: {output_path}"
            )
        except Exception as e:
            self.add_example(
                "Projeto Completo",
                False,
                f"Erro: {e}"
            )
    
    def print_summary(self):
        """Imprime um resumo dos exemplos"""
        print_section("Resumo dos Exemplos")
        
        # Calcular estatísticas
        total_examples = len(self.examples)
        successful_examples = sum(1 for _, success, _ in self.examples if success)
        failed_examples = total_examples - successful_examples
        
        # Imprimir estatísticas
        color_print(f"Total de exemplos: {total_examples}", Colors.WHITE)
        color_print(f"Exemplos bem-sucedidos: {successful_examples}", Colors.GREEN)
        color_print(f"Exemplos falhos: {failed_examples}", Colors.RED)
        
        # Calcular porcentagem
        if total_examples > 0:
            percentage = (successful_examples / total_examples) * 100
            color_print(f"Taxa de sucesso: {percentage:.1f}%", Colors.WHITE)
        
        # Tempo total
        total_time = time.time() - self.start_time
        color_print(f"Tempo total de execução: {total_time:.2f}s", Colors.WHITE)
        
        # Verificar se todos os exemplos foram bem-sucedidos
        if failed_examples == 0:
            color_print("\n✓ Todos os exemplos foram bem-sucedidos!", Colors.GREEN)
        else:
            color_print(f"\n✗ {failed_examples} exemplo(s) falharam!", Colors.RED)
            
            # Listar exemplos falhos
            color_print("\nExemplos falhos:", Colors.RED)
            for example_name, success, message in self.examples:
                if not success:
                    color_print(f"- {example_name}: {message}", Colors.RED)
        
        # Salvar resultados em arquivo
        self.save_results()
    
    def save_results(self):
        """Salva os resultados em um arquivo"""
        try:
            results_file = os.path.join(EXAMPLES_DIR, "examples_results.txt")
            
            with open(results_file, 'w', encoding='utf-8') as f:
                f.write("=== RESULTADOS DOS EXEMPLOS DO MOVIEPY ===\n\n")
                
                # Informações gerais
                f.write(f"Data: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Versão do MoviePy: {moviepy.__version__}\n")
                f.write(f"Python: {sys.version}\n")
                f.write(f"Sistema: {os.name}\n\n")
                
                # Resultados
                f.write("=== RESULTADOS DETALHADOS ===\n\n")
                
                for example_name, success, message in self.examples:
                    status = "SUCESSO" if success else "FALHA"
                    f.write(f"{example_name}: {status}")
                    if message:
                        f.write(f" - {message}")
                    f.write("\n")
                
                # Estatísticas
                total_examples = len(self.examples)
                successful_examples = sum(1 for _, success, _ in self.examples if success)
                failed_examples = total_examples - successful_examples
                
                f.write(f"\n=== ESTATÍSTICAS ===\n")
                f.write(f"Total de exemplos: {total_examples}\n")
                f.write(f"Exemplos bem-sucedidos: {successful_examples}\n")
                f.write(f"Exemplos falhos: {failed_examples}\n")
                
                if total_examples > 0:
                    percentage = (successful_examples / total_examples) * 100
                    f.write(f"Taxa de sucesso: {percentage:.1f}%\n")
                
                # Tempo total
                total_time = time.time() - self.start_time
                f.write(f"Tempo total de execução: {total_time:.2f}s\n")
            
            color_print(f"\nResultados salvos em: {results_file}", Colors.CYAN)
        except Exception as e:
            color_print(f"\nErro ao salvar resultados: {e}", Colors.RED)

def main():
    """Função principal"""
    try:
        # Importar time (não estava importado no início)
        import time
        
        # Criar executor de exemplos
        examples = MoviePyExamples()
        
        # Executar exemplos
        success = examples.run_all_examples()
        
        # Retornar código de saída
        return 0 if success else 1
    except KeyboardInterrupt:
        color_print("\nExemplos interrompidos pelo usuário", Colors.YELLOW)
        return 1
    except Exception as e:
        color_print(f"\nErro inesperado: {e}", Colors.RED)
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())