#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de diagnóstico para MoviePy no projeto auto-video-producerV5-dev

Este script realiza um diagnóstico completo do MoviePy, verificando
instalação, dependências, compatibilidade e funcionalidades.
"""

import os
import sys
import subprocess
import platform
import tempfile
import traceback
import time
from pathlib import Path

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
    """Imprime um resultado de teste"""
    if success:
        color_print(f"✓ {test_name}: SUCESSO", Colors.GREEN)
    else:
        color_print(f"✗ {test_name}: FALHA", Colors.RED)
    
    if message:
        print(f"  {message}")
    
    print()

class MoviePyDiagnostic:
    """Classe para diagnóstico do MoviePy"""
    
    def __init__(self):
        self.results = []
        self.start_time = None
        self.temp_dir = tempfile.mkdtemp()
        self.moviepy_version = None
        self.python_version = sys.version
        self.os_info = platform.platform()
        self.dependencies = {}
    
    def add_result(self, test_name, success, message=""):
        """Adiciona um resultado de teste"""
        self.results.append((test_name, success, message))
        print_result(test_name, success, message)
    
    def run_diagnostic(self):
        """Executa o diagnóstico completo"""
        self.start_time = time.time()
        
        print_header("DIAGNÓSTICO COMPLETO DO MOVIEPY")
        
        # Informações do sistema
        self.check_system_info()
        
        # Verificar instalação
        self.check_moviepy_installation()
        
        # Verificar dependências
        self.check_dependencies()
        
        # Verificar compatibilidade com MoviePy 2.1.2
        self.check_moviepy_212_compatibility()
        
        # Verificar funcionalidades básicas
        self.check_basic_functionality()
        
        # Verificar exportação
        self.check_export_functionality()
        
        # Verificar áudio
        self.check_audio_functionality()
        
        # Verificar texto
        self.check_text_functionality()
        
        # Verificar efeitos
        self.check_effects_functionality()
        
        # Verificar composição
        self.check_composition_functionality()
        
        # Verificar performance
        self.check_performance()
        
        # Resumo
        self.print_summary()
        
        # Salvar resultados
        self.save_results()
        
        return True
    
    def check_system_info(self):
        """Verifica informações do sistema"""
        print_section("Informações do Sistema")
        
        # Python
        color_print(f"Python: {self.python_version}", Colors.WHITE)
        
        # Sistema operacional
        color_print(f"Sistema: {self.os_info}", Colors.WHITE)
        
        # Arquitetura
        color_print(f"Arquitetura: {platform.machine()}", Colors.WHITE)
        
        # Diretório temporário
        color_print(f"Diretório temporário: {self.temp_dir}", Colors.WHITE)
        
        # Diretório do projeto
        project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
        color_print(f"Diretório do projeto: {project_dir}", Colors.WHITE)
        
        print()
    
    def check_moviepy_installation(self):
        """Verifica a instalação do MoviePy"""
        print_section("Instalação do MoviePy")
        
        try:
            import moviepy
            self.moviepy_version = moviepy.__version__
            color_print(f"MoviePy instalado: {self.moviepy_version}", Colors.GREEN)
            
            # Verificar se é a versão 2.1.2
            if self.moviepy_version == "2.1.2":
                color_print("Versão correta (2.1.2)", Colors.GREEN)
                self.add_result("Instalação do MoviePy", True, f"Versão {self.moviepy_version}")
            else:
                color_print(f"Versão incorreta (esperada: 2.1.2, atual: {self.moviepy_version})", Colors.YELLOW)
                self.add_result("Instalação do MoviePy", False, f"Versão incorreta: {self.moviepy_version}")
            
        except ImportError:
            color_print("MoviePy não está instalado", Colors.RED)
            self.add_result("Instalação do MoviePy", False, "MoviePy não está instalado")
            return
        
        # Verificar módulos principais
        modules_to_check = [
            ("moviepy.editor", "Editor principal"),
            ("moviepy.audio.io.AudioFileClip", "Áudio"),
            ("moviepy.video.io.VideoFileClip", "Vídeo"),
            ("moviepy.video.compositing.CompositeVideoClip", "Composição"),
            ("moviepy.video.fx", "Efeitos de vídeo"),
            ("moviepy.audio.fx", "Efeitos de áudio")
        ]
        
        for module_name, description in modules_to_check:
            try:
                __import__(module_name)
                self.add_result(f"Módulo {description}", True)
            except ImportError as e:
                self.add_result(f"Módulo {description}", False, str(e))
    
    def check_dependencies(self):
        """Verifica as dependências do MoviePy"""
        print_section("Dependências do MoviePy")
        
        # Lista de dependências
        dependencies = [
            ("numpy", "NumPy"),
            ("PIL", "Pillow"),
            ("imageio", "ImageIO"),
            ("imageio_ffmpeg", "ImageIO-FFmpeg"),
            ("decorator", "Decorator"),
            ("proglog", "Proglog"),
            ("tqdm", "TQDM")
        ]
        
        for module_name, description in dependencies:
            try:
                module = __import__(module_name)
                version = getattr(module, "__version__", "Desconhecida")
                self.dependencies[module_name] = version
                self.add_result(f"Dependência {description}", True, f"Versão {version}")
            except ImportError as e:
                self.add_result(f"Dependência {description}", False, str(e))
        
        # Verificar FFmpeg
        try:
            result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
            if result.returncode == 0:
                ffmpeg_version = result.stdout.split('\n')[0]
                self.add_result("FFmpeg", True, ffmpeg_version)
            else:
                self.add_result("FFmpeg", False, "FFmpeg não encontrado no PATH")
        except FileNotFoundError:
            self.add_result("FFmpeg", False, "FFmpeg não encontrado no PATH")
        except Exception as e:
            self.add_result("FFmpeg", False, str(e))
    
    def check_moviepy_212_compatibility(self):
        """Verifica a compatibilidade com MoviePy 2.1.2"""
        print_section("Compatibilidade com MoviePy 2.1.2")
        
        if self.moviepy_version != "2.1.2":
            self.add_result("Compatibilidade com 2.1.2", False, f"Versão atual: {self.moviepy_version}")
            return
        
        # Verificar mudanças na API 2.1.2
        try:
            # Importar no topo da função para evitar erro de sintaxe
            from moviepy.editor import ColorClip, TextClip, ImageClip, VideoFileClip, AudioArrayClip
            from moviepy.video.fx import FadeIn, FadeOut
            
            # Verificar se FadeIn e FadeOut estão disponíveis
            self.add_result("API FadeIn/FadeOut", True, "FadeIn e FadeOut disponíveis")
            
            # Verificar método write_videofile
            clip = ColorClip(size=(100, 100), color=(255, 0, 0), duration=1)
            
            # Verificar se write_videofile não tem parâmetro verbose
            import inspect
            sig = inspect.signature(clip.write_videofile)
            params = list(sig.parameters.keys())
            
            if 'verbose' in params:
                self.add_result("API write_videofile", False, "Parâmetro verbose ainda existe")
            else:
                self.add_result("API write_videofile", True, "Parâmetro verbose removido")
            
            # Verificar método concatenate
            if hasattr(clip, 'concatenate'):
                self.add_result("API concatenate", False, "Método concatenate ainda existe")
            else:
                self.add_result("API concatenate", True, "Método concatenate removido")
            
            # Verificar função concatenate_videoclips
            try:
                from moviepy.video.compositing.concatenate import concatenate_videoclips
                self.add_result("API concatenate_videoclips", True, "Função concatenate_videoclips disponível")
            except ImportError:
                self.add_result("API concatenate_videoclips", False, "Função concatenate_videoclips não disponível")
            
            # Verificar API do TextClip
            try:
                txt = TextClip(text="Teste", font_size=24, color='white')
                self.add_result("API TextClip", True, "TextClip funciona corretamente")
            except Exception as e:
                self.add_result("API TextClip", False, str(e))
            
        except Exception as e:
            self.add_result("Compatibilidade com 2.1.2", False, str(e))
    
    def check_basic_functionality(self):
        """Verifica funcionalidades básicas do MoviePy"""
        print_section("Funcionalidades Básicas")
        
        try:
            # Importar no topo da função para evitar erro de sintaxe
            from moviepy.editor import ColorClip, TextClip, ImageClip, VideoFileClip, AudioArrayClip
            
            # Criar um clipe de cor
            clip = ColorClip(size=(100, 100), color=(255, 0, 0), duration=1)
            self.add_result("Criar ColorClip", True)
            
            # Criar um clipe de texto
            try:
                txt = TextClip(text="Teste", font_size=24, color='white')
                self.add_result("Criar TextClip", True)
            except Exception as e:
                self.add_result("Criar TextClip", False, str(e))
            
            # Criar um clipe de imagem
            try:
                import numpy as np
                img_array = np.zeros((100, 100, 3), dtype=np.uint8)
                img_array[:, :, 0] = 255  # Canal vermelho
                img_clip = ImageClip(img_array, duration=1)
                self.add_result("Criar ImageClip", True)
            except Exception as e:
                self.add_result("Criar ImageClip", False, str(e))
            
            # Criar um clipe de áudio
            try:
                import numpy as np
                sample_rate = 44100
                duration = 1
                t = np.linspace(0, duration, int(duration * sample_rate), False)
                audio_data = np.sin(2 * np.pi * 440 * t)
                audio_data = audio_data / np.max(np.abs(audio_data))
                audio_clip = AudioArrayClip(audio_data, fps=sample_rate)
                self.add_result("Criar AudioClip", True)
            except Exception as e:
                self.add_result("Criar AudioClip", False, str(e))
            
            # Criar um clipe de vídeo
            try:
                video_clip = VideoFileClip.__new__(VideoFileClip)
                self.add_result("Criar VideoFileClip", True, "Classe VideoFileClip disponível")
            except Exception as e:
                self.add_result("Criar VideoFileClip", False, str(e))
            
        except Exception as e:
            self.add_result("Funcionalidades Básicas", False, str(e))
    
    def check_export_functionality(self):
        """Verifica funcionalidades de exportação"""
        print_section("Funcionalidades de Exportação")
        
        try:
            # Importar no topo da função para evitar erro de sintaxe
            from moviepy.editor import ColorClip
            
            # Criar um clipe simples
            clip = ColorClip(size=(100, 100), color=(255, 0, 0), duration=1)
            
            # Exportar para MP4
            try:
                output_path = os.path.join(self.temp_dir, "test_export.mp4")
                clip.write_videofile(output_path, fps=24, logger=None)
                
                if os.path.exists(output_path):
                    self.add_result("Exportar MP4", True)
                else:
                    self.add_result("Exportar MP4", False, "Arquivo não foi criado")
            except Exception as e:
                self.add_result("Exportar MP4", False, str(e))
            
            # Exportar para diferentes formatos
            formats = ["webm", "avi", "mov"]
            
            for fmt in formats:
                try:
                    output_path = os.path.join(self.temp_dir, f"test_export.{fmt}")
                    clip.write_videofile(output_path, fps=24, logger=None)
                    
                    if os.path.exists(output_path):
                        self.add_result(f"Exportar {fmt.upper()}", True)
                    else:
                        self.add_result(f"Exportar {fmt.upper()}", False, "Arquivo não foi criado")
                except Exception as e:
                    self.add_result(f"Exportar {fmt.upper()}", False, str(e))
            
        except Exception as e:
            self.add_result("Funcionalidades de Exportação", False, str(e))
    
    def check_audio_functionality(self):
        """Verifica funcionalidades de áudio"""
        print_section("Funcionalidades de Áudio")
        
        try:
            # Importar no topo da função para evitar erro de sintaxe
            from moviepy.editor import AudioClip, AudioFileClip, ColorClip, AudioArrayClip
            from moviepy.audio.fx import volumex, audio_fadein, audio_fadeout
            
            # Criar um áudio sintético
            import numpy as np
            sample_rate = 44100
            duration = 1
            t = np.linspace(0, duration, int(duration * sample_rate), False)
            audio_data = np.sin(2 * np.pi * 440 * t)
            audio_data = audio_data / np.max(np.abs(audio_data))
            audio_clip = AudioArrayClip(audio_data, fps=sample_rate)
            
            # Exportar áudio
            try:
                output_path = os.path.join(self.temp_dir, "test_audio.mp3")
                audio_clip.write_audiofile(output_path, fps=sample_rate, logger=None)
                
                if os.path.exists(output_path):
                    self.add_result("Exportar Áudio", True)
                else:
                    self.add_result("Exportar Áudio", False, "Arquivo não foi criado")
            except Exception as e:
                self.add_result("Exportar Áudio", False, str(e))
            
            # Aplicar efeitos de áudio
            try:
                # Efeito de volume
                volume_clip = audio_clip.fx(volumex, 2.0)
                self.add_result("Efeito de Volume", True)
            except Exception as e:
                self.add_result("Efeito de Volume", False, str(e))
            
            try:
                # Efeito de fade in
                fadein_clip = audio_clip.fx(audio_fadein, 0.5)
                self.add_result("Efeito de Fade In", True)
            except Exception as e:
                self.add_result("Efeito de Fade In", False, str(e))
            
            try:
                # Efeito de fade out
                fadeout_clip = audio_clip.fx(audio_fadeout, 0.5)
                self.add_result("Efeito de Fade Out", True)
            except Exception as e:
                self.add_result("Efeito de Fade Out", False, str(e))
            
            # Adicionar áudio a vídeo
            try:
                video_clip = ColorClip(size=(100, 100), color=(255, 0, 0), duration=1)
                video_with_audio = video_clip.set_audio(audio_clip)
                
                output_path = os.path.join(self.temp_dir, "test_video_with_audio.mp4")
                video_with_audio.write_videofile(output_path, fps=24, logger=None)
                
                if os.path.exists(output_path):
                    self.add_result("Adicionar Áudio a Vídeo", True)
                else:
                    self.add_result("Adicionar Áudio a Vídeo", False, "Arquivo não foi criado")
            except Exception as e:
                self.add_result("Adicionar Áudio a Vídeo", False, str(e))
            
        except Exception as e:
            self.add_result("Funcionalidades de Áudio", False, str(e))
    
    def check_text_functionality(self):
        """Verifica funcionalidades de texto"""
        print_section("Funcionalidades de Texto")
        
        try:
            # Importar no topo da função para evitar erro de sintaxe
            from moviepy.editor import TextClip, ColorClip
            
            # Criar um texto básico
            try:
                txt = TextClip(text="Teste", font_size=24, color='white')
                self.add_result("Criar Texto Básico", True)
            except Exception as e:
                self.add_result("Criar Texto Básico", False, str(e))
            
            # Criar um texto com fonte específica
            try:
                txt = TextClip(
                    text="Teste com Fonte",
                    font_size=24,
                    color='white',
                    font='C:/Windows/Fonts/arial.ttf'
                )
                self.add_result("Criar Texto com Fonte", True)
            except Exception as e:
                self.add_result("Criar Texto com Fonte", False, str(e))
            
            # Criar um texto estilizado
            try:
                txt = TextClip(
                    text="Teste Estilizado",
                    font_size=24,
                    color='white',
                    stroke_color='black',
                    stroke_width=1
                )
                self.add_result("Criar Texto Estilizado", True)
            except Exception as e:
                self.add_result("Criar Texto Estilizado", False, str(e))
            
            # Exportar texto
            try:
                txt = TextClip(text="Teste Exportação", font_size=24, color='white')
                output_path = os.path.join(self.temp_dir, "test_text.mp4")
                txt.write_videofile(output_path, fps=24, logger=None)
                
                if os.path.exists(output_path):
                    self.add_result("Exportar Texto", True)
                else:
                    self.add_result("Exportar Texto", False, "Arquivo não foi criado")
            except Exception as e:
                self.add_result("Exportar Texto", False, str(e))
            
        except Exception as e:
            self.add_result("Funcionalidades de Texto", False, str(e))
    
    def check_effects_functionality(self):
        """Verifica funcionalidades de efeitos"""
        print_section("Funcionalidades de Efeitos")
        
        try:
            # Importar no topo da função para evitar erro de sintaxe
            from moviepy.editor import ColorClip
            from moviepy.video.fx import FadeIn, FadeOut, blackwhite, lum_contrast, resize, crop
            
            # Criar um clipe base
            clip = ColorClip(size=(100, 100), color=(255, 0, 0), duration=1)
            
            # Aplicar fade in/out
            try:
                faded_clip = clip.with_effects([FadeIn(0.5), FadeOut(0.5)])
                self.add_result("Efeito Fade In/Out", True)
            except Exception as e:
                self.add_result("Efeito Fade In/Out", False, str(e))
            
            # Aplicar efeito preto e branco
            try:
                bw_clip = clip.fx(blackwhite)
                self.add_result("Efeito Preto e Branco", True)
            except Exception as e:
                self.add_result("Efeito Preto e Branco", False, str(e))
            
            # Aplicar efeito de brilho e contraste
            try:
                contrast_clip = clip.fx(lum_contrast, lum=0.5, contrast=1.5)
                self.add_result("Efeito Brilho/Contraste", True)
            except Exception as e:
                self.add_result("Efeito Brilho/Contraste", False, str(e))
            
            # Aplicar efeito de redimensionamento
            try:
                resized_clip = clip.resize((50, 50))
                self.add_result("Efeito Redimensionamento", True)
            except Exception as e:
                self.add_result("Efeito Redimensionamento", False, str(e))
            
            # Aplicar efeito de corte
            try:
                cropped_clip = crop(clip, x_center=50, y_center=50, width=50, height=50)
                self.add_result("Efeito Corte", True)
            except Exception as e:
                self.add_result("Efeito Corte", False, str(e))
            
        except Exception as e:
            self.add_result("Funcionalidades de Efeitos", False, str(e))
    
    def check_composition_functionality(self):
        """Verifica funcionalidades de composição"""
        print_section("Funcionalidades de Composição")
        
        try:
            # Importar no topo da função para evitar erro de sintaxe
            from moviepy.editor import ColorClip, CompositeVideoClip, concatenate_videoclips, clips_array
            
            # Criar clipes para composição
            background = ColorClip(size=(200, 200), color=(0, 0, 0), duration=1)
            clip1 = ColorClip(size=(50, 50), color=(255, 0, 0), duration=1)
            clip2 = ColorClip(size=(50, 50), color=(0, 255, 0), duration=1)
            
            # Posicionar clipes
            clip1 = clip1.with_position((25, 25))
            clip2 = clip2.with_position((125, 125))
            
            # Criar composição
            try:
                composition = CompositeVideoClip([background, clip1, clip2])
                self.add_result("Criar Composição", True)
            except Exception as e:
                self.add_result("Criar Composição", False, str(e))
            
            # Concatenar clipes
            try:
                concatenated = concatenate_videoclips([clip1, clip2])
                self.add_result("Concatenar Clipes", True)
            except Exception as e:
                self.add_result("Concatenar Clipes", False, str(e))
            
            # Criar array de clipes
            try:
                array_clip = clips_array([[clip1, clip2]])
                self.add_result("Criar Array de Clipes", True)
            except Exception as e:
                self.add_result("Criar Array de Clipes", False, str(e))
            
        except Exception as e:
            self.add_result("Funcionalidades de Composição", False, str(e))
    
    def check_performance(self):
        """Verifica performance do MoviePy"""
        print_section("Performance")
        
        try:
            import time
            # Importar no topo da função para evitar erro de sintaxe
            from moviepy.editor import ColorClip
            
            # Teste de criação de clipes
            start_time = time.time()
            
            for i in range(10):
                clip = ColorClip(size=(100, 100), color=(255, 0, 0), duration=1)
            
            creation_time = time.time() - start_time
            self.add_result("Performance - Criação de Clipes", True, f"10 clipes em {creation_time:.3f}s")
            
            # Teste de exportação
            clip = ColorClip(size=(100, 100), color=(255, 0, 0), duration=1)
            
            start_time = time.time()
            output_path = os.path.join(self.temp_dir, "test_performance.mp4")
            clip.write_videofile(output_path, fps=24, logger=None)
            export_time = time.time() - start_time
            
            if os.path.exists(output_path):
                self.add_result("Performance - Exportação", True, f"Exportação em {export_time:.3f}s")
            else:
                self.add_result("Performance - Exportação", False, "Arquivo não foi criado")
            
        except Exception as e:
            self.add_result("Performance", False, str(e))
    
    def print_summary(self):
        """Imprime um resumo do diagnóstico"""
        print_section("Resumo do Diagnóstico")
        
        # Calcular estatísticas
        total_tests = len(self.results)
        successful_tests = sum(1 for _, success, _ in self.results if success)
        failed_tests = total_tests - successful_tests
        
        # Imprimir estatísticas
        color_print(f"Total de testes: {total_tests}", Colors.WHITE)
        color_print(f"Testes bem-sucedidos: {successful_tests}", Colors.GREEN)
        color_print(f"Testes falhos: {failed_tests}", Colors.RED)
        
        # Calcular porcentagem
        if total_tests > 0:
            percentage = (successful_tests / total_tests) * 100
            color_print(f"Taxa de sucesso: {percentage:.1f}%", Colors.WHITE)
        
        # Tempo total
        total_time = time.time() - self.start_time
        color_print(f"Tempo total de execução: {total_time:.2f}s", Colors.WHITE)
        
        # Verificar se todos os testes foram bem-sucedidos
        if failed_tests == 0:
            color_print("\n✓ Todos os testes foram bem-sucedidos!", Colors.GREEN)
        else:
            color_print(f"\n✗ {failed_tests} teste(s) falharam!", Colors.RED)
            
            # Listar testes falhos
            color_print("\nTestes falhos:", Colors.RED)
            for test_name, success, message in self.results:
                if not success:
                    color_print(f"- {test_name}: {message}", Colors.RED)
        
        # Recomendações
        self.print_recommendations()
    
    def print_recommendations(self):
        """Imprime recomendações com base nos resultados"""
        print_section("Recomendações")
        
        # Verificar se MoviePy está instalado
        moviepy_installed = any("Instalação do MoviePy" in result[0] and result[1] for result in self.results)
        
        if not moviepy_installed:
            color_print("- Instale o MoviePy usando: pip install moviepy", Colors.YELLOW)
            return
        
        # Verificar versão
        if self.moviepy_version != "2.1.2":
            color_print(f"- Atualize para o MoviePy 2.1.2 usando: pip install moviepy==2.1.2", Colors.YELLOW)
        
        # Verificar dependências
        failed_deps = [result[0] for result in self.results if "Dependência" in result[0] and not result[1]]
        
        if failed_deps:
            color_print("- Instale as dependências faltantes:", Colors.YELLOW)
            for dep in failed_deps:
                color_print(f"  - {dep}", Colors.YELLOW)
        
        # Verificar FFmpeg
        ffmpeg_ok = any("FFmpeg" in result[0] and result[1] for result in self.results)
        
        if not ffmpeg_ok:
            color_print("- Instale o FFmpeg e adicione-o ao PATH do sistema", Colors.YELLOW)
        
        # Verificar funcionalidades críticas
        critical_failures = [
            result for result in self.results 
            if not result[1] and any(keyword in result[0] for keyword in [
                "Exportar", "Criar", "API", "Compatibilidade"
            ])
        ]
        
        if critical_failures:
            color_print("- Verifique as funcionalidades críticas que falharam:", Colors.YELLOW)
            for failure in critical_failures:
                color_print(f"  - {failure[0]}: {failure[2]}", Colors.YELLOW)
    
    def save_results(self):
        """Salva os resultados em um arquivo"""
        try:
            results_file = os.path.join(self.temp_dir, "diagnostic_results.txt")
            
            with open(results_file, 'w', encoding='utf-8') as f:
                f.write("=== RESULTADOS DO DIAGNÓSTICO DO MOVIEPY ===\n\n")
                
                # Informações gerais
                f.write(f"Data: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Python: {self.python_version}\n")
                f.write(f"Sistema: {self.os_info}\n")
                f.write(f"Versão do MoviePy: {self.moviepy_version}\n\n")
                
                # Dependências
                f.write("=== DEPENDÊNCIAS ===\n")
                for dep_name, dep_version in self.dependencies.items():
                    f.write(f"{dep_name}: {dep_version}\n")
                f.write("\n")
                
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
                successful_tests = sum(1 for _, success, _ in self.results if success)
                failed_tests = total_tests - successful_tests
                
                f.write(f"\n=== ESTATÍSTICAS ===\n")
                f.write(f"Total de testes: {total_tests}\n")
                f.write(f"Testes bem-sucedidos: {successful_tests}\n")
                f.write(f"Testes falhos: {failed_tests}\n")
                
                if total_tests > 0:
                    percentage = (successful_tests / total_tests) * 100
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
        
        # Criar executor de diagnóstico
        diagnostic = MoviePyDiagnostic()
        
        # Executar diagnóstico
        success = diagnostic.run_diagnostic()
        
        # Retornar código de saída
        return 0 if success else 1
    except KeyboardInterrupt:
        color_print("\nDiagnóstico interrompido pelo usuário", Colors.YELLOW)
        return 1
    except Exception as e:
        color_print(f"\nErro inesperado: {e}", Colors.RED)
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())