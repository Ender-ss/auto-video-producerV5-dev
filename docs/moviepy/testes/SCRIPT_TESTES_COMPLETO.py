#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script completo de testes para MoviePy no projeto auto-video-producerV5-dev

Este script executa uma série de testes abrangentes para verificar a instalação,
funcionalidades e compatibilidade do MoviePy, especialmente focado na versão 2.1.2.
"""

import os
import sys
import tempfile
import time
import traceback
import numpy as np
from pathlib import Path

# Verificar se o MoviePy está instalado
try:
    import moviepy
    from moviepy.editor import *
    from moviepy.video.fx import FadeIn, FadeOut, blackwhite, lum_contrast
    from moviepy.audio.fx import volumex, audio_fadein, audio_fadeout
    MOVIEPY_INSTALLED = True
except ImportError as e:
    print(f"ERRO: MoviePy não está instalado: {e}")
    MOVIEPY_INSTALLED = False

# Configurações
TEMP_DIR = tempfile.gettempdir()
TEST_OUTPUT_DIR = os.path.join(TEMP_DIR, "moviepy_tests")
os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)

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

def print_result(test_name, success, message=""):
    """Imprime o resultado de um teste"""
    if success:
        color_print(f"✓ {test_name}: SUCESSO", Colors.GREEN)
    else:
        color_print(f"✗ {test_name}: FALHA", Colors.RED)
    
    if message:
        print(f"  {message}")
    
    print()

class MoviePyTester:
    """Classe para testar o MoviePy"""
    
    def __init__(self):
        self.results = []
        self.start_time = time.time()
    
    def add_result(self, test_name, success, message=""):
        """Adiciona um resultado"""
        self.results.append((test_name, success, message))
        print_result(test_name, success, message)
    
    def run_all_tests(self):
        """Executa todos os testes"""
        print_header("TESTE COMPLETO DO MOVIEPY")
        
        if not MOVIEPY_INSTALLED:
            color_print("MoviePy não está instalado. Abortando testes.", Colors.RED)
            return False
        
        # Testes de instalação
        self.test_installation()
        
        # Testes de funcionalidades básicas
        self.test_basic_functionality()
        
        # Testes de efeitos
        self.test_effects()
        
        # Testes de composição
        self.test_composition()
        
        # Testes de texto
        self.test_text()
        
        # Testes de áudio
        self.test_audio()
        
        # Testes de exportação
        self.test_export()
        
        # Testes de compatibilidade com 2.1.2
        self.test_compatibility()
        
        # Testes de performance
        self.test_performance()
        
        # Resumo
        self.print_summary()
        
        return True
    
    def test_installation(self):
        """Testa a instalação do MoviePy e dependências"""
        print_section("Testes de Instalação")
        
        # Testar versão do MoviePy
        try:
            version = moviepy.__version__
            self.add_result(
                "Versão do MoviePy", 
                True, 
                f"Versão: {version}"
            )
        except Exception as e:
            self.add_result(
                "Versão do MoviePy", 
                False, 
                f"Erro: {e}"
            )
        
        # Testar dependências Python
        dependencies = [
            ("numpy", "numpy"),
            ("PIL", "Pillow"),
            ("imageio", "imageio"),
            ("imageio_ffmpeg", "imageio-ffmpeg"),
            ("decorator", "decorator"),
            ("tqdm", "tqdm")
        ]
        
        for dep_name, package_name in dependencies:
            try:
                __import__(dep_name)
                self.add_result(
                    f"Dependência: {package_name}", 
                    True
                )
            except ImportError:
                self.add_result(
                    f"Dependência: {package_name}", 
                    False, 
                    "Não instalada"
                )
        
        # Testar FFmpeg
        try:
            import subprocess
            result = subprocess.run(
                ["ffmpeg", "-version"], 
                capture_output=True, 
                text=True
            )
            if result.returncode == 0:
                version = result.stdout.split('\n')[0]
                self.add_result(
                    "FFmpeg", 
                    True, 
                    f"Versão: {version.split(' ')[2]}"
                )
            else:
                self.add_result(
                    "FFmpeg", 
                    False, 
                    "Não encontrado ou erro na execução"
                )
        except FileNotFoundError:
            self.add_result(
                "FFmpeg", 
                False, 
                "Não encontrado no PATH"
            )
        
        # Testar ImageMagick
        try:
            result = subprocess.run(
                ["magick", "-version"], 
                capture_output=True, 
                text=True
            )
            if result.returncode == 0:
                version = result.stdout.split('\n')[0]
                self.add_result(
                    "ImageMagick", 
                    True, 
                    f"Versão: {version.split(' ')[2]}"
                )
            else:
                self.add_result(
                    "ImageMagick", 
                    False, 
                    "Não encontrado ou erro na execução"
                )
        except FileNotFoundError:
            self.add_result(
                "ImageMagick", 
                False, 
                "Não encontrado no PATH"
            )
    
    def test_basic_functionality(self):
        """Testa funcionalidades básicas do MoviePy"""
        print_section("Testes de Funcionalidades Básicas")
        
        # Testar criação de clipe de cor
        try:
            clip = ColorClip(size=(320, 240), color=(255, 0, 0), duration=5)
            self.add_result(
                "Criação de ColorClip", 
                True
            )
        except Exception as e:
            self.add_result(
                "Criação de ColorClip", 
                False, 
                f"Erro: {e}"
            )
        
        # Testar criação de clipe de imagem
        try:
            # Criar uma imagem simples com numpy
            img_array = np.zeros((240, 320, 3), dtype=np.uint8)
            img_array[:, :, 0] = 255  # Canal vermelho
            
            clip = ImageClip(img_array, duration=5)
            self.add_result(
                "Criação de ImageClip", 
                True
            )
        except Exception as e:
            self.add_result(
                "Criação de ImageClip", 
                False, 
                f"Erro: {e}"
            )
        
        # Testar criação de clipe de vídeo a partir de arquivo
        try:
            # Criar um vídeo simples para teste
            temp_video = os.path.join(TEST_OUTPUT_DIR, "temp_video.mp4")
            if os.path.exists(temp_video):
                os.remove(temp_video)
            
            # Criar um clipe de cor e exportar
            color_clip = ColorClip(size=(320, 240), color=(0, 255, 0), duration=5)
            color_clip.write_videofile(temp_video, fps=24, logger=None)
            
            # Tentar carregar o vídeo
            clip = VideoFileClip(temp_video)
            self.add_result(
                "Criação de VideoFileClip", 
                True
            )
        except Exception as e:
            self.add_result(
                "Criação de VideoFileClip", 
                False, 
                f"Erro: {e}"
            )
        
        # Testar subclip
        try:
            clip = ColorClip(size=(320, 240), color=(255, 0, 0), duration=10)
            sub = clip.subclip(2, 5)
            self.add_result(
                "Criação de subclip", 
                True
            )
        except Exception as e:
            self.add_result(
                "Criação de subclip", 
                False, 
                f"Erro: {e}"
            )
        
        # Testar resize
        try:
            clip = ColorClip(size=(320, 240), color=(255, 0, 0), duration=5)
            resized = clip.resize(width=640)
            self.add_result(
                "Resize de clipe", 
                True
            )
        except Exception as e:
            self.add_result(
                "Resize de clipe", 
                False, 
                f"Erro: {e}"
            )
    
    def test_effects(self):
        """Testa efeitos do MoviePy"""
        print_section("Testes de Efeitos")
        
        # Testar efeitos de fade (MoviePy 2.1.2)
        try:
            clip = ColorClip(size=(320, 240), color=(255, 0, 0), duration=5)
            
            # Testar novo sistema de efeitos
            clip = clip.with_effects([FadeIn(1), FadeOut(1)])
            self.add_result(
                "Efeitos de Fade (novo sistema)", 
                True
            )
        except Exception as e:
            self.add_result(
                "Efeitos de Fade (novo sistema)", 
                False, 
                f"Erro: {e}"
            )
        
        # Testar efeitos de cor
        try:
            clip = ColorClip(size=(320, 240), color=(255, 0, 0), duration=5)
            clip = clip.fx(blackwhite)
            self.add_result(
                "Efeito blackwhite", 
                True
            )
        except Exception as e:
            self.add_result(
                "Efeito blackwhite", 
                False, 
                f"Erro: {e}"
            )
        
        # Testar efeito de brilho e contraste
        try:
            clip = ColorClip(size=(320, 240), color=(255, 0, 0), duration=5)
            clip = clip.fx(lum_contrast, lum=0.5, contrast=1.5)
            self.add_result(
                "Efeito lum_contrast", 
                True
            )
        except Exception as e:
            self.add_result(
                "Efeito lum_contrast", 
                False, 
                f"Erro: {e}"
            )
        
        # Testar múltiplos efeitos
        try:
            clip = ColorClip(size=(320, 240), color=(255, 0, 0), duration=5)
            clip = clip.fx(blackwhite)
            clip = clip.fx(lum_contrast, lum=0.5, contrast=1.5)
            clip = clip.with_effects([FadeIn(1), FadeOut(1)])
            self.add_result(
                "Múltiplos efeitos", 
                True
            )
        except Exception as e:
            self.add_result(
                "Múltiplos efeitos", 
                False, 
                f"Erro: {e}"
            )
    
    def test_composition(self):
        """Testa composição de clipes"""
        print_section("Testes de Composição")
        
        # Testar composição básica
        try:
            background = ColorClip(size=(640, 480), color=(0, 0, 0), duration=5)
            clip1 = ColorClip(size=(100, 100), color=(255, 0, 0), duration=5)
            clip2 = ColorClip(size=(100, 100), color=(0, 255, 0), duration=5)
            
            # Posicionar clipes
            clip1 = clip1.with_position((50, 50))
            clip2 = clip2.with_position((170, 170))
            
            # Compor
            final = CompositeVideoClip([background, clip1, clip2])
            self.add_result(
                "Composição básica", 
                True
            )
        except Exception as e:
            self.add_result(
                "Composição básica", 
                False, 
                f"Erro: {e}"
            )
        
        # Testar concatenação (MoviePy 2.1.2)
        try:
            clip1 = ColorClip(size=(320, 240), color=(255, 0, 0), duration=2)
            clip2 = ColorClip(size=(320, 240), color=(0, 255, 0), duration=3)
            
            # Concatenar
            final = concatenate_videoclips([clip1, clip2])
            self.add_result(
                "Concatenação de clipes", 
                True
            )
        except Exception as e:
            self.add_result(
                "Concatenação de clipes", 
                False, 
                f"Erro: {e}"
            )
        
        # Testar clips_array
        try:
            clip1 = ColorClip(size=(100, 100), color=(255, 0, 0), duration=5)
            clip2 = ColorClip(size=(100, 100), color=(0, 255, 0), duration=5)
            clip3 = ColorClip(size=(100, 100), color=(0, 0, 255), duration=5)
            clip4 = ColorClip(size=(100, 100), color=(255, 255, 0), duration=5)
            
            # Criar matriz
            clips_matrix = [
                [clip1, clip2],
                [clip3, clip4]
            ]
            
            # Criar array
            final = clips_array(clips_matrix)
            self.add_result(
                "Clips array", 
                True
            )
        except Exception as e:
            self.add_result(
                "Clips array", 
                False, 
                f"Erro: {e}"
            )
    
    def test_text(self):
        """Testa funcionalidades de texto"""
        print_section("Testes de Texto")
        
        # Testar criação básica de TextClip
        try:
            txt = TextClip(
                text="Teste",
                font_size=24,
                color='white',
                font='C:/Windows/Fonts/arial.ttf'
            )
            self.add_result(
                "Criação básica de TextClip", 
                True
            )
        except Exception as e:
            self.add_result(
                "Criação básica de TextClip", 
                False, 
                f"Erro: {e}"
            )
        
        # Testar TextClip com parâmetros adicionais
        try:
            txt = TextClip(
                text="Teste com parâmetros",
                font_size=24,
                color='white',
                font='C:/Windows/Fonts/arial.ttf',
                stroke_color='black',
                stroke_width=1,
                method='label'
            )
            self.add_result(
                "TextClip com parâmetros adicionais", 
                True
            )
        except Exception as e:
            self.add_result(
                "TextClip com parâmetros adicionais", 
                False, 
                f"Erro: {e}"
            )
        
        # Testar TextClip com método caption
        try:
            txt = TextClip(
                text="Texto longo com método caption para testar quebra automática de linha",
                font_size=24,
                color='white',
                font='C:/Windows/Fonts/arial.ttf',
                method='caption',
                size=(400, 200)
            )
            self.add_result(
                "TextClip com método caption", 
                True
            )
        except Exception as e:
            self.add_result(
                "TextClip com método caption", 
                False, 
                f"Erro: {e}"
            )
        
        # Testar texto com caracteres especiais
        try:
            txt = TextClip(
                text="Teste com acentos: áéíóú",
                font_size=24,
                color='white',
                font='C:/Windows/Fonts/arial.ttf'
            )
            self.add_result(
                "TextClip com caracteres especiais", 
                True
            )
        except Exception as e:
            self.add_result(
                "TextClip com caracteres especiais", 
                False, 
                f"Erro: {e}"
            )
    
    def test_audio(self):
        """Testa funcionalidades de áudio"""
        print_section("Testes de Áudio")
        
        # Testar criação de áudio sintético
        try:
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
            self.add_result(
                "Criação de áudio sintético", 
                True
            )
        except Exception as e:
            self.add_result(
                "Criação de áudio sintético", 
                False, 
                f"Erro: {e}"
            )
        
        # Testar efeitos de áudio
        try:
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
            
            self.add_result(
                "Efeitos de áudio", 
                True
            )
        except Exception as e:
            self.add_result(
                "Efeitos de áudio", 
                False, 
                f"Erro: {e}"
            )
        
        # Testar adicionar áudio a vídeo
        try:
            # Criar clipe de vídeo
            video_clip = ColorClip(size=(320, 240), color=(255, 0, 0), duration=5)
            
            # Criar clipe de áudio
            duration = 5
            sample_rate = 44100
            t = np.linspace(0, duration, int(duration * sample_rate), False)
            audio_data = np.sin(2 * np.pi * 440 * t)
            audio_data = audio_data / np.max(np.abs(audio_data))
            audio_data = audio_data * 0.5
            
            audio_clip = AudioArrayClip(audio_data, fps=sample_rate)
            
            # Adicionar áudio ao vídeo
            video_clip = video_clip.set_audio(audio_clip)
            self.add_result(
                "Adicionar áudio a vídeo", 
                True
            )
        except Exception as e:
            self.add_result(
                "Adicionar áudio a vídeo", 
                False, 
                f"Erro: {e}"
            )
    
    def test_export(self):
        """Testa exportação de vídeos"""
        print_section("Testes de Exportação")
        
        # Testar exportação básica
        try:
            clip = ColorClip(size=(320, 240), color=(255, 0, 0), duration=5)
            
            output_path = os.path.join(TEST_OUTPUT_DIR, "test_export.mp4")
            if os.path.exists(output_path):
                os.remove(output_path)
            
            # Exportar (MoviePy 2.1.2)
            clip.write_videofile(output_path, fps=24, logger=None)
            
            # Verificar se o arquivo foi criado
            if os.path.exists(output_path):
                self.add_result(
                    "Exportação básica", 
                    True
                )
            else:
                self.add_result(
                    "Exportação básica", 
                    False, 
                    "Arquivo não foi criado"
                )
        except Exception as e:
            self.add_result(
                "Exportação básica", 
                False, 
                f"Erro: {e}"
            )
        
        # Testar exportação com áudio
        try:
            # Criar clipe de vídeo
            video_clip = ColorClip(size=(320, 240), color=(255, 0, 0), duration=5)
            
            # Criar clipe de áudio
            duration = 5
            sample_rate = 44100
            t = np.linspace(0, duration, int(duration * sample_rate), False)
            audio_data = np.sin(2 * np.pi * 440 * t)
            audio_data = audio_data / np.max(np.abs(audio_data))
            audio_data = audio_data * 0.5
            
            audio_clip = AudioArrayClip(audio_data, fps=sample_rate)
            
            # Adicionar áudio ao vídeo
            video_clip = video_clip.set_audio(audio_clip)
            
            output_path = os.path.join(TEST_OUTPUT_DIR, "test_export_audio.mp4")
            if os.path.exists(output_path):
                os.remove(output_path)
            
            # Exportar
            video_clip.write_videofile(output_path, fps=24, logger=None)
            
            # Verificar se o arquivo foi criado
            if os.path.exists(output_path):
                self.add_result(
                    "Exportação com áudio", 
                    True
                )
            else:
                self.add_result(
                    "Exportação com áudio", 
                    False, 
                    "Arquivo não foi criado"
                )
        except Exception as e:
            self.add_result(
                "Exportação com áudio", 
                False, 
                f"Erro: {e}"
            )
        
        # Testar exportação com diferentes codecs
        try:
            clip = ColorClip(size=(320, 240), color=(255, 0, 0), duration=5)
            
            output_path = os.path.join(TEST_OUTPUT_DIR, "test_export_codec.mp4")
            if os.path.exists(output_path):
                os.remove(output_path)
            
            # Exportar com codec específico
            clip.write_videofile(output_path, fps=24, codec='libx264', logger=None)
            
            # Verificar se o arquivo foi criado
            if os.path.exists(output_path):
                self.add_result(
                    "Exportação com codec específico", 
                    True
                )
            else:
                self.add_result(
                    "Exportação com codec específico", 
                    False, 
                    "Arquivo não foi criado"
                )
        except Exception as e:
            self.add_result(
                "Exportação com codec específico", 
                False, 
                f"Erro: {e}"
            )
    
    def test_compatibility(self):
        """Testa compatibilidade com MoviePy 2.1.2"""
        print_section("Testes de Compatibilidade com MoviePy 2.1.2")
        
        # Testar versão
        try:
            version = moviepy.__version__
            version_parts = version.split('.')
            major = int(version_parts[0])
            minor = int(version_parts[1])
            
            if major > 2 or (major == 2 and minor >= 1):
                self.add_result(
                    "Versão compatível com 2.1.2", 
                    True, 
                    f"Versão: {version}"
                )
            else:
                self.add_result(
                    "Versão compatível com 2.1.2", 
                    False, 
                    f"Versão: {version}"
                )
        except Exception as e:
            self.add_result(
                "Versão compatível com 2.1.2", 
                False, 
                f"Erro: {e}"
            )
        
        # Testar se os métodos antigos de fade foram removidos
        try:
            clip = ColorClip(size=(320, 240), color=(255, 0, 0), duration=5)
            
            if hasattr(clip, 'fadein'):
                self.add_result(
                    "Método fadein removido", 
                    False, 
                    "Método fadein ainda existe"
                )
            else:
                self.add_result(
                    "Método fadein removido", 
                    True
                )
            
            if hasattr(clip, 'fadeout'):
                self.add_result(
                    "Método fadeout removido", 
                    False, 
                    "Método fadeout ainda existe"
                )
            else:
                self.add_result(
                    "Método fadeout removido", 
                    True
                )
        except Exception as e:
            self.add_result(
                "Métodos de fade removidos", 
                False, 
                f"Erro: {e}"
            )
        
        # Testar se o parâmetro verbose foi removido
        try:
            import inspect
            clip = ColorClip(size=(320, 240), color=(255, 0, 0), duration=5)
            sig = inspect.signature(clip.write_videofile)
            params = list(sig.parameters.keys())
            
            if 'verbose' in params:
                self.add_result(
                    "Parâmetro verbose removido", 
                    False, 
                    "Parâmetro verbose ainda existe"
                )
            else:
                self.add_result(
                    "Parâmetro verbose removido", 
                    True
                )
        except Exception as e:
            self.add_result(
                "Parâmetro verbose removido", 
                False, 
                f"Erro: {e}"
            )
        
        # Testar se o método concatenate foi removido
        try:
            if hasattr(sys.modules['moviepy.editor'], 'concatenate'):
                self.add_result(
                    "Método concatenate removido", 
                    False, 
                    "Método concatenate ainda existe"
                )
            else:
                self.add_result(
                    "Método concatenate removido", 
                    True
                )
        except Exception as e:
            self.add_result(
                "Método concatenate removido", 
                False, 
                f"Erro: {e}"
            )
        
        # Testar se o método concatenate_videoclips existe
        try:
            clip1 = ColorClip(size=(320, 240), color=(255, 0, 0), duration=2)
            clip2 = ColorClip(size=(320, 240), color=(0, 255, 0), duration=3)
            
            final = concatenate_videoclips([clip1, clip2])
            self.add_result(
                "Método concatenate_videoclips existe", 
                True
            )
        except Exception as e:
            self.add_result(
                "Método concatenate_videoclips existe", 
                False, 
                f"Erro: {e}"
            )
    
    def test_performance(self):
        """Testa performance do MoviePy"""
        print_section("Testes de Performance")
        
        # Testar tempo de criação de clipe
        try:
            start_time = time.time()
            
            # Criar clipe grande
            clip = ColorClip(size=(1920, 1080), color=(255, 0, 0), duration=10)
            
            end_time = time.time()
            elapsed = end_time - start_time
            
            self.add_result(
                "Tempo de criação de clipe", 
                True, 
                f"Tempo: {elapsed:.2f}s"
            )
        except Exception as e:
            self.add_result(
                "Tempo de criação de clipe", 
                False, 
                f"Erro: {e}"
            )
        
        # Testar tempo de aplicação de efeitos
        try:
            clip = ColorClip(size=(1920, 1080), color=(255, 0, 0), duration=10)
            
            start_time = time.time()
            
            # Aplicar efeitos
            clip = clip.fx(blackwhite)
            clip = clip.fx(lum_contrast, lum=0.5, contrast=1.5)
            clip = clip.with_effects([FadeIn(1), FadeOut(1)])
            
            end_time = time.time()
            elapsed = end_time - start_time
            
            self.add_result(
                "Tempo de aplicação de efeitos", 
                True, 
                f"Tempo: {elapsed:.2f}s"
            )
        except Exception as e:
            self.add_result(
                "Tempo de aplicação de efeitos", 
                False, 
                f"Erro: {e}"
            )
        
        # Testar tempo de exportação
        try:
            clip = ColorClip(size=(320, 240), color=(255, 0, 0), duration=5)
            
            output_path = os.path.join(TEST_OUTPUT_DIR, "test_performance.mp4")
            if os.path.exists(output_path):
                os.remove(output_path)
            
            start_time = time.time()
            
            # Exportar
            clip.write_videofile(output_path, fps=24, logger=None)
            
            end_time = time.time()
            elapsed = end_time - start_time
            
            self.add_result(
                "Tempo de exportação", 
                True, 
                f"Tempo: {elapsed:.2f}s"
            )
        except Exception as e:
            self.add_result(
                "Tempo de exportação", 
                False, 
                f"Erro: {e}"
            )
    
    def print_summary(self):
        """Imprime um resumo dos testes"""
        print_section("Resumo dos Testes")
        
        # Calcular estatísticas
        total_tests = len(self.results)
        passed_tests = sum(1 for _, success, _ in self.results if success)
        failed_tests = total_tests - passed_tests
        
        # Imprimir estatísticas
        color_print(f"Total de testes: {total_tests}", Colors.WHITE)
        color_print(f"Testes passados: {passed_tests}", Colors.GREEN)
        color_print(f"Testes falhos: {failed_tests}", Colors.RED)
        
        # Calcular porcentagem
        if total_tests > 0:
            percentage = (passed_tests / total_tests) * 100
            color_print(f"Taxa de sucesso: {percentage:.1f}%", Colors.WHITE)
        
        # Tempo total
        total_time = time.time() - self.start_time
        color_print(f"Tempo total de execução: {total_time:.2f}s", Colors.WHITE)
        
        # Verificar se todos os testes passaram
        if failed_tests == 0:
            color_print("\n✓ Todos os testes passaram!", Colors.GREEN)
        else:
            color_print(f"\n✗ {failed_tests} teste(s) falharam!", Colors.RED)
            
            # Listar testes falhos
            color_print("\nTestes falhos:", Colors.RED)
            for test_name, success, message in self.results:
                if not success:
                    color_print(f"- {test_name}: {message}", Colors.RED)
        
        # Salvar resultados em arquivo
        self.save_results()
    
    def save_results(self):
        """Salva os resultados em um arquivo"""
        try:
            results_file = os.path.join(TEST_OUTPUT_DIR, "test_results.txt")
            
            with open(results_file, 'w', encoding='utf-8') as f:
                f.write("=== RESULTADOS DOS TESTES DO MOVIEPY ===\n\n")
                
                # Informações gerais
                f.write(f"Data: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Versão do MoviePy: {moviepy.__version__}\n")
                f.write(f"Python: {sys.version}\n")
                f.write(f"Sistema: {os.name}\n\n")
                
                # Resultados
                f.write("=== RESULTADOS DETALHADOS ===\n\n")
                
                for test_name, success, message in self.results:
                    status = "SUCESSO" if success else "FALHA"
                    f.write(f"{test_name}: {status}")
                    if message:
                        f.write(f" - {message}")
                    f.write("\n")
                
                # Estatísticas
                total_tests = len(self.results)
                passed_tests = sum(1 for _, success, _ in self.results if success)
                failed_tests = total_tests - passed_tests
                
                f.write(f"\n=== ESTATÍSTICAS ===\n")
                f.write(f"Total de testes: {total_tests}\n")
                f.write(f"Testes passados: {passed_tests}\n")
                f.write(f"Testes falhos: {failed_tests}\n")
                
                if total_tests > 0:
                    percentage = (passed_tests / total_tests) * 100
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
        # Criar tester
        tester = MoviePyTester()
        
        # Executar testes
        success = tester.run_all_tests()
        
        # Retornar código de saída
        return 0 if success else 1
    except KeyboardInterrupt:
        color_print("\nTestes interrompidos pelo usuário", Colors.YELLOW)
        return 1
    except Exception as e:
        color_print(f"\nErro inesperado: {e}", Colors.RED)
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())