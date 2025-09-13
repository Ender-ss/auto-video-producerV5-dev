#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de diagnóstico para MoviePy no projeto auto-video-producerV5-dev

Este script realiza um diagnóstico completo do ambiente MoviePy, identificando
problemas de instalação, dependências, configuração e compatibilidade.
"""

import os
import sys
import subprocess
import platform
import traceback
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

class MoviePyDiagnostic:
    """Classe para diagnóstico do MoviePy"""
    
    def __init__(self):
        self.issues = []
        self.warnings = []
        self.recommendations = []
        self.start_time = time.time()
    
    def add_issue(self, category, issue, solution):
        """Adiciona um problema"""
        self.issues.append((category, issue, solution))
        color_print(f"✗ {issue}", Colors.RED)
        print(f"  Solução: {solution}")
        print()
    
    def add_warning(self, category, warning, recommendation):
        """Adiciona um aviso"""
        self.warnings.append((category, warning, recommendation))
        color_print(f"⚠ {warning}", Colors.YELLOW)
        print(f"  Recomendação: {recommendation}")
        print()
    
    def add_recommendation(self, category, recommendation):
        """Adiciona uma recomendação"""
        self.recommendations.append((category, recommendation))
        color_print(f"ℹ {recommendation}", Colors.CYAN)
        print()
    
    def run_diagnostic(self):
        """Executa o diagnóstico completo"""
        print_header("DIAGNÓSTICO COMPLETO DO MOVIEPY")
        
        # Diagnóstico do sistema
        self.diagnose_system()
        
        # Diagnóstico do Python
        self.diagnose_python()
        
        # Diagnóstico do MoviePy
        self.diagnose_moviepy()
        
        # Diagnóstico de dependências
        self.diagnose_dependencies()
        
        # Diagnóstico de ferramentas externas
        self.diagnose_external_tools()
        
        # Diagnóstico de compatibilidade
        self.diagnose_compatibility()
        
        # Diagnóstico de performance
        self.diagnose_performance()
        
        # Resumo
        self.print_summary()
        
        return True
    
    def diagnose_system(self):
        """Diagnostica o sistema operacional"""
        print_section("Diagnóstico do Sistema")
        
        # Sistema operacional
        system = platform.system()
        release = platform.release()
        version = platform.version()
        
        color_print(f"Sistema Operacional: {system} {release}", Colors.WHITE)
        color_print(f"Versão: {version}", Colors.WHITE)
        
        # Arquitetura
        arch = platform.machine()
        color_print(f"Arquitetura: {arch}", Colors.WHITE)
        
        # Verificar se é Windows
        if system == "Windows":
            color_print("Sistema: Windows", Colors.GREEN)
        elif system == "Linux":
            color_print("Sistema: Linux", Colors.GREEN)
        elif system == "Darwin":
            color_print("Sistema: macOS", Colors.GREEN)
        else:
            self.add_issue(
                "Sistema",
                f"Sistema operacional não suportado: {system}",
                "Verifique se o MoviePy é compatível com este sistema"
            )
        
        # Verificar se é 64-bit
        if "64" in arch:
            color_print("Arquitetura: 64-bit (recomendado)", Colors.GREEN)
        else:
            self.add_warning(
                "Sistema",
                "Arquitetura 32-bit detectada",
                "Considere usar um sistema 64-bit para melhor performance"
            )
        
        print()
    
    def diagnose_python(self):
        """Diagnostica o ambiente Python"""
        print_section("Diagnóstico do Python")
        
        # Versão do Python
        version = sys.version
        version_info = sys.version_info
        
        color_print(f"Python: {version}", Colors.WHITE)
        color_print(f"Versão: {version_info.major}.{version_info.minor}.{version_info.micro}", Colors.WHITE)
        
        # Verificar versão mínima
        if version_info.major < 3 or (version_info.major == 3 and version_info.minor < 6):
            self.add_issue(
                "Python",
                f"Versão do Python muito antiga: {version_info.major}.{version_info.minor}.{version_info.micro}",
                "Atualize para Python 3.6 ou superior"
            )
        else:
            color_print("Versão do Python: OK", Colors.GREEN)
        
        # Verificar ambiente virtual
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            color_print("Ambiente virtual: Ativo", Colors.GREEN)
        else:
            self.add_warning(
                "Python",
                "Ambiente virtual não detectado",
                "Considere usar um ambiente virtual para isolar dependências"
            )
        
        # Verificar caminho do Python
        python_path = sys.executable
        color_print(f"Caminho do Python: {python_path}", Colors.WHITE)
        
        # Verificar PATH
        path = os.environ.get('PATH', '')
        color_print(f"PATH: {path[:100]}...", Colors.WHITE)
        
        print()
    
    def diagnose_moviepy(self):
        """Diagnostica a instalação do MoviePy"""
        print_section("Diagnóstico do MoviePy")
        
        # Verificar se o MoviePy está instalado
        try:
            import moviepy
            version = moviepy.__version__
            color_print(f"MoviePy: Instalado", Colors.GREEN)
            color_print(f"Versão: {version}", Colors.WHITE)
            
            # Verificar versão
            version_parts = version.split('.')
            major = int(version_parts[0])
            minor = int(version_parts[1])
            
            if major < 2 or (major == 2 and minor < 1):
                self.add_issue(
                    "MoviePy",
                    f"Versão do MoviePy muito antiga: {version}",
                    "Atualize para MoviePy 2.1.2 ou superior"
                )
            elif major > 2 or (major == 2 and minor > 1):
                self.add_warning(
                    "MoviePy",
                    f"Versão do MoviePy mais recente que a testada: {version}",
                    "Verifique se há alterações na API que possam afetar o código"
                )
            else:
                color_print("Versão do MoviePy: OK", Colors.GREEN)
            
            # Verificar módulos
            modules = [
                "moviepy.editor",
                "moviepy.audio",
                "moviepy.video",
                "moviepy.video.fx",
                "moviepy.audio.fx",
                "moviepy.video.io",
                "moviepy.audio.io"
            ]
            
            for module in modules:
                try:
                    __import__(module)
                    color_print(f"Módulo {module}: OK", Colors.GREEN)
                except ImportError as e:
                    self.add_issue(
                        "MoviePy",
                        f"Módulo não encontrado: {module}",
                        f"Reinstale o MoviePy: pip install --upgrade moviepy"
                    )
            
        except ImportError as e:
            self.add_issue(
                "MoviePy",
                "MoviePy não está instalado",
                "Instale o MoviePy: pip install moviepy"
            )
        
        print()
    
    def diagnose_dependencies(self):
        """Diagnostica as dependências do MoviePy"""
        print_section("Diagnóstico de Dependências")
        
        # Lista de dependências
        dependencies = [
            ("numpy", "numpy", "1.15.0"),
            ("PIL", "Pillow", "6.0.0"),
            ("imageio", "imageio", "2.5.0"),
            ("imageio_ffmpeg", "imageio-ffmpeg", "0.4.0"),
            ("decorator", "decorator", "4.3.0"),
            ("tqdm", "tqdm", "4.30.0"),
            ("proglog", "proglog", "0.1.9"),
            ("requests", "requests", "2.20.0")
        ]
        
        for dep_name, package_name, min_version in dependencies:
            try:
                module = __import__(dep_name)
                version = getattr(module, '__version__', 'desconhecida')
                color_print(f"{package_name}: Instalado (versão: {version})", Colors.GREEN)
                
                # Verificar versão mínima
                if version != 'desconhecida':
                    try:
                        version_parts = version.split('.')
                        min_parts = min_version.split('.')
                        
                        for i in range(max(len(version_parts), len(min_parts))):
                            v_part = int(version_parts[i]) if i < len(version_parts) else 0
                            m_part = int(min_parts[i]) if i < len(min_parts) else 0
                            
                            if v_part < m_part:
                                self.add_warning(
                                    "Dependências",
                                    f"Versão de {package_name} muito antiga: {version}",
                                    f"Atualize para {package_name} {min_version} ou superior"
                                )
                                break
                            elif v_part > m_part:
                                break
                    except (ValueError, IndexError):
                        self.add_warning(
                            "Dependências",
                            f"Não foi possível verificar a versão de {package_name}",
                            f"Verifique manualmente se a versão é compatível"
                        )
                
            except ImportError:
                self.add_issue(
                    "Dependências",
                    f"Dependência não encontrada: {package_name}",
                    f"Instale: pip install {package_name}"
                )
        
        print()
    
    def diagnose_external_tools(self):
        """Diagnostica ferramentas externas necessárias"""
        print_section("Diagnóstico de Ferramentas Externas")
        
        # Verificar FFmpeg
        try:
            result = subprocess.run(
                ["ffmpeg", "-version"], 
                capture_output=True, 
                text=True
            )
            if result.returncode == 0:
                version = result.stdout.split('\n')[0]
                color_print(f"FFmpeg: Instalado", Colors.GREEN)
                color_print(f"Versão: {version.split(' ')[2]}", Colors.WHITE)
            else:
                self.add_issue(
                    "Ferramentas Externas",
                    "FFmpeg não encontrado ou erro na execução",
                    "Instale o FFmpeg e adicione ao PATH"
                )
        except FileNotFoundError:
            self.add_issue(
                "Ferramentas Externas",
                "FFmpeg não encontrado no PATH",
                "Instale o FFmpeg e adicione ao PATH"
            )
        
        # Verificar ImageMagick
        try:
            result = subprocess.run(
                ["magick", "-version"], 
                capture_output=True, 
                text=True
            )
            if result.returncode == 0:
                version = result.stdout.split('\n')[0]
                color_print(f"ImageMagick: Instalado", Colors.GREEN)
                color_print(f"Versão: {version.split(' ')[2]}", Colors.WHITE)
            else:
                self.add_warning(
                    "Ferramentas Externas",
                    "ImageMagick não encontrado ou erro na execução",
                    "Instale o ImageMagick para funcionalidades de texto"
                )
        except FileNotFoundError:
            self.add_warning(
                "Ferramentas Externas",
                "ImageMagick não encontrado no PATH",
                "Instale o ImageMagick para funcionalidades de texto"
            )
        
        # Verificar se há problemas com permissões
        try:
            # Tentar criar um arquivo temporário
            import tempfile
            with tempfile.NamedTemporaryFile(delete=True) as temp:
                temp.write(b"test")
            color_print("Permissões de escrita: OK", Colors.GREEN)
        except Exception as e:
            self.add_issue(
                "Sistema",
                f"Problemas com permissões: {e}",
                "Verifique as permissões do diretório atual"
            )
        
        # Verificar espaço em disco
        try:
            import shutil
            total, used, free = shutil.disk_usage("/")
            free_gb = free / (1024 ** 3)
            
            if free_gb < 1:
                self.add_issue(
                    "Sistema",
                    f"Espaço em disco insuficiente: {free_gb:.2f} GB",
                    "Libere espaço em disco para processamento de vídeo"
                )
            elif free_gb < 5:
                self.add_warning(
                    "Sistema",
                    f"Espaço em disco baixo: {free_gb:.2f} GB",
                    "Considere liberar mais espaço em disco"
                )
            else:
                color_print(f"Espaço em disco: {free_gb:.2f} GB (OK)", Colors.GREEN)
        except Exception as e:
            self.add_warning(
                "Sistema",
                f"Não foi possível verificar o espaço em disco: {e}",
                "Verifique manualmente o espaço em disco"
            )
        
        print()
    
    def diagnose_compatibility(self):
        """Diagnostica problemas de compatibilidade"""
        print_section("Diagnóstico de Compatibilidade")
        
        # Verificar se o MoviePy está instalado
        try:
            import moviepy
            version = moviepy.__version__
            
            # Verificar versão
            version_parts = version.split('.')
            major = int(version_parts[0])
            minor = int(version_parts[1])
            
            # Verificar se é a versão 2.1.2 ou superior
            if major > 2 or (major == 2 and minor >= 1):
                # Verificar se os métodos antigos foram removidos
                try:
                    from moviepy.editor import ColorClip
                    
                    # Criar um clipe para teste
                    clip = ColorClip(size=(100, 100), color=(255, 0, 0), duration=1)
                    
                    # Verificar se os métodos antigos de fade foram removidos
                    if hasattr(clip, 'fadein'):
                        self.add_issue(
                            "Compatibilidade",
                            "Método fadein ainda existe (deve ser removido na versão 2.1.2)",
                            "Verifique se a versão do MoviePy está correta"
                        )
                    else:
                        color_print("Método fadein: Removido (OK)", Colors.GREEN)
                    
                    if hasattr(clip, 'fadeout'):
                        self.add_issue(
                            "Compatibilidade",
                            "Método fadeout ainda existe (deve ser removido na versão 2.1.2)",
                            "Verifique se a versão do MoviePy está correta"
                        )
                    else:
                        color_print("Método fadeout: Removido (OK)", Colors.GREEN)
                    
                    # Verificar se o parâmetro verbose foi removido
                    import inspect
                    sig = inspect.signature(clip.write_videofile)
                    params = list(sig.parameters.keys())
                    
                    if 'verbose' in params:
                        self.add_issue(
                            "Compatibilidade",
                            "Parâmetro verbose ainda existe (deve ser removido na versão 2.1.2)",
                            "Verifique se a versão do MoviePy está correta"
                        )
                    else:
                        color_print("Parâmetro verbose: Removido (OK)", Colors.GREEN)
                    
                    # Verificar se o método concatenate foi removido
                    if hasattr(sys.modules['moviepy.editor'], 'concatenate'):
                        self.add_issue(
                            "Compatibilidade",
                            "Método concatenate ainda existe (deve ser removido na versão 2.1.2)",
                            "Verifique se a versão do MoviePy está correta"
                        )
                    else:
                        color_print("Método concatenate: Removido (OK)", Colors.GREEN)
                    
                    # Verificar se o método concatenate_videoclips existe
                    from moviepy.editor import concatenate_videoclips
                    color_print("Método concatenate_videoclips: Existe (OK)", Colors.GREEN)
                    
                except Exception as e:
                    self.add_issue(
                        "Compatibilidade",
                        f"Erro ao verificar compatibilidade: {e}",
                        "Verifique a instalação do MoviePy"
                    )
            else:
                self.add_issue(
                    "Compatibilidade",
                    f"Versão do MoviePy não compatível: {version}",
                    "Atualize para MoviePy 2.1.2 ou superior"
                )
                
        except ImportError:
            self.add_issue(
                "Compatibilidade",
                "MoviePy não está instalado",
                "Instale o MoviePy: pip install moviepy"
            )
        
        print()
    
    def diagnose_performance(self):
        """Diagnostica problemas de performance"""
        print_section("Diagnóstico de Performance")
        
        # Verificar se o MoviePy está instalado
        try:
            import moviepy
            from moviepy.editor import ColorClip
            import time
            
            # Testar tempo de criação de clipe
            start_time = time.time()
            clip = ColorClip(size=(1920, 1080), color=(255, 0, 0), duration=10)
            end_time = time.time()
            elapsed = end_time - start_time
            
            if elapsed > 1.0:
                self.add_warning(
                    "Performance",
                    f"Tempo de criação de clipe alto: {elapsed:.2f}s",
                    "Verifique se há problemas com o sistema ou dependências"
                )
            else:
                color_print(f"Tempo de criação de clipe: {elapsed:.2f}s (OK)", Colors.GREEN)
            
            # Testar tempo de aplicação de efeitos
            try:
                from moviepy.video.fx import blackwhite, lum_contrast
                from moviepy.video.fx import FadeIn, FadeOut
                
                start_time = time.time()
                
                # Aplicar efeitos
                clip = clip.fx(blackwhite)
                clip = clip.fx(lum_contrast, lum=0.5, contrast=1.5)
                clip = clip.with_effects([FadeIn(1), FadeOut(1)])
                
                end_time = time.time()
                elapsed = end_time - start_time
                
                if elapsed > 2.0:
                    self.add_warning(
                        "Performance",
                        f"Tempo de aplicação de efeitos alto: {elapsed:.2f}s",
                        "Verifique se há problemas com o sistema ou dependências"
                    )
                else:
                    color_print(f"Tempo de aplicação de efeitos: {elapsed:.2f}s (OK)", Colors.GREEN)
            except Exception as e:
                self.add_issue(
                    "Performance",
                    f"Erro ao testar efeitos: {e}",
                    "Verifique a instalação do MoviePy"
                )
            
            # Verificar uso de memória
            try:
                import psutil
                process = psutil.Process(os.getpid())
                memory_info = process.memory_info()
                memory_mb = memory_info.rss / (1024 * 1024)
                
                if memory_mb > 500:
                    self.add_warning(
                        "Performance",
                        f"Uso de memória alto: {memory_mb:.2f} MB",
                        "Verifique se há vazamentos de memória ou processos pesados"
                    )
                else:
                    color_print(f"Uso de memória: {memory_mb:.2f} MB (OK)", Colors.GREEN)
            except ImportError:
                self.add_warning(
                    "Performance",
                    "Não foi possível verificar o uso de memória",
                    "Instale psutil: pip install psutil"
                )
            
        except ImportError:
            self.add_issue(
                "Performance",
                "MoviePy não está instalado",
                "Instale o MoviePy: pip install moviepy"
            )
        
        print()
    
    def print_summary(self):
        """Imprime um resumo do diagnóstico"""
        print_section("Resumo do Diagnóstico")
        
        # Contar problemas
        total_issues = len(self.issues)
        total_warnings = len(self.warnings)
        total_recommendations = len(self.recommendations)
        
        # Imprimir estatísticas
        color_print(f"Total de problemas: {total_issues}", Colors.WHITE)
        color_print(f"Total de avisos: {total_warnings}", Colors.WHITE)
        color_print(f"Total de recomendações: {total_recommendations}", Colors.WHITE)
        
        # Verificar se há problemas críticos
        if total_issues > 0:
            color_print(f"\n✗ {total_issues} problema(s) crítico(s) encontrado(s)!", Colors.RED)
            
            # Listar problemas
            color_print("\nProblemas críticos:", Colors.RED)
            for category, issue, solution in self.issues:
                color_print(f"- [{category}] {issue}", Colors.RED)
                color_print(f"  Solução: {solution}", Colors.WHITE)
        else:
            color_print("\n✓ Nenhum problema crítico encontrado!", Colors.GREEN)
        
        # Verificar se há avisos
        if total_warnings > 0:
            color_print(f"\n⚠ {total_warnings} aviso(s) encontrado(s)", Colors.YELLOW)
            
            # Listar avisos
            color_print("\nAvisos:", Colors.YELLOW)
            for category, warning, recommendation in self.warnings:
                color_print(f"- [{category}] {warning}", Colors.YELLOW)
                color_print(f"  Recomendação: {recommendation}", Colors.WHITE)
        else:
            color_print("\n✓ Nenhum aviso encontrado!", Colors.GREEN)
        
        # Verificar se há recomendações
        if total_recommendations > 0:
            color_print(f"\nℹ {total_recommendations} recomendação(ões)", Colors.CYAN)
            
            # Listar recomendações
            color_print("\nRecomendações:", Colors.CYAN)
            for category, recommendation in self.recommendations:
                color_print(f"- [{category}] {recommendation}", Colors.CYAN)
        
        # Salvar resultados em arquivo
        self.save_results()
    
    def save_results(self):
        """Salva os resultados em um arquivo"""
        try:
            import tempfile
            results_file = os.path.join(tempfile.gettempdir(), "moviepy_diagnostic.txt")
            
            with open(results_file, 'w', encoding='utf-8') as f:
                f.write("=== RESULTADOS DO DIAGNÓSTICO DO MOVIEPY ===\n\n")
                
                # Informações gerais
                f.write(f"Data: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Sistema: {platform.system()} {platform.release()}\n")
                f.write(f"Python: {sys.version}\n")
                
                # Verificar se o MoviePy está instalado
                try:
                    import moviepy
                    f.write(f"MoviePy: {moviepy.__version__}\n")
                except ImportError:
                    f.write("MoviePy: Não instalado\n")
                
                f.write("\n")
                
                # Problemas
                f.write("=== PROBLEMAS CRÍTICOS ===\n\n")
                for category, issue, solution in self.issues:
                    f.write(f"[{category}] {issue}\n")
                    f.write(f"  Solução: {solution}\n\n")
                
                # Avisos
                f.write("=== AVISOS ===\n\n")
                for category, warning, recommendation in self.warnings:
                    f.write(f"[{category}] {warning}\n")
                    f.write(f"  Recomendação: {recommendation}\n\n")
                
                # Recomendações
                f.write("=== RECOMENDAÇÕES ===\n\n")
                for category, recommendation in self.recommendations:
                    f.write(f"[{category}] {recommendation}\n\n")
                
                # Estatísticas
                f.write("=== ESTATÍSTICAS ===\n")
                f.write(f"Total de problemas: {len(self.issues)}\n")
                f.write(f"Total de avisos: {len(self.warnings)}\n")
                f.write(f"Total de recomendações: {len(self.recommendations)}\n")
            
            color_print(f"\nResultados salvos em: {results_file}", Colors.CYAN)
        except Exception as e:
            color_print(f"\nErro ao salvar resultados: {e}", Colors.RED)

def main():
    """Função principal"""
    try:
        # Criar diagnosticador
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