#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de diagnóstico simplificado para MoviePy no projeto auto-video-producerV5-dev

Este script realiza um diagnóstico simplificado do MoviePy, verificando
instalação, dependências e funcionalidades básicas.
"""

import os
import sys
import subprocess
import platform
import time
import traceback

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

class SimpleMoviePyDiagnostic:
    """Classe para diagnóstico simplificado do MoviePy"""
    
    def __init__(self):
        self.issues = []
        self.warnings = []
        self.recommendations = []
        self.moviepy_version = None
    
    def add_issue(self, category, issue, solution):
        """Adiciona um problema"""
        self.issues.append((category, issue, solution))
        color_print(f"✗ {issue}", Colors.RED)
        color_print(f"  Solução: {solution}", Colors.WHITE)
        print()
    
    def add_warning(self, category, warning, recommendation):
        """Adiciona um aviso"""
        self.warnings.append((category, warning, recommendation))
        color_print(f"⚠ {warning}", Colors.YELLOW)
        color_print(f"  Recomendação: {recommendation}", Colors.WHITE)
        print()
    
    def add_recommendation(self, category, recommendation):
        """Adiciona uma recomendação"""
        self.recommendations.append((category, recommendation))
        color_print(f"ℹ {recommendation}", Colors.CYAN)
        print()
    
    def run_diagnostic(self):
        """Executa o diagnóstico simplificado"""
        print_header("DIAGNÓSTICO SIMPLIFICADO DO MOVIEPY")
        
        # Verificar Python
        self.check_python()
        
        # Verificar pip
        self.check_pip()
        
        # Verificar MoviePy
        self.check_moviepy()
        
        # Verificar dependências
        self.check_dependencies()
        
        # Verificar FFmpeg
        self.check_ffmpeg()
        
        # Verificar ImageMagick
        self.check_imagemagick()
        
        # Verificar funcionalidades básicas
        self.check_basic_functionality()
        
        # Resumo
        self.print_summary()
        
        # Retornar True se não houver problemas críticos
        return len(self.issues) == 0
    
    def check_python(self):
        """Verifica a instalação do Python"""
        print_section("Verificação do Python")
        
        version = sys.version
        color_print(f"Python: {version}", Colors.WHITE)
        
        # Verificar versão mínima
        version_parts = version.split()[0].split('.')
        major = int(version_parts[0])
        minor = int(version_parts[1])
        
        if major < 3 or (major == 3 and minor < 7):
            self.add_issue(
                "Python",
                f"Versão do Python muito antiga: {major}.{minor}",
                "Atualize para Python 3.7 ou superior"
            )
        else:
            color_print("Versão do Python: OK", Colors.GREEN)
        
        print()
    
    def check_pip(self):
        """Verifica a instalação do pip"""
        print_section("Verificação do pip")
        
        try:
            result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                version = result.stdout.split()[1]
                color_print(f"pip: {version}", Colors.GREEN)
            else:
                self.add_issue(
                    "pip",
                    "pip não está disponível",
                    "Instale o pip: python -m ensurepip --upgrade"
                )
        except Exception as e:
            self.add_issue(
                "pip",
                f"Erro ao verificar pip: {e}",
                "Verifique a instalação do Python e pip"
            )
        
        print()
    
    def check_moviepy(self):
        """Verifica a instalação do MoviePy"""
        print_section("Verificação do MoviePy")
        
        try:
            import moviepy
            self.moviepy_version = moviepy.__version__
            color_print(f"MoviePy: {self.moviepy_version}", Colors.GREEN)
            
            # Verificar versão
            version_parts = self.moviepy_version.split('.')
            major = int(version_parts[0])
            minor = int(version_parts[1])
            
            if major < 2 or (major == 2 and minor < 1):
                self.add_issue(
                    "MoviePy",
                    f"Versão do MoviePy muito antiga: {self.moviepy_version}",
                    "Atualize para MoviePy 2.1.2 ou superior"
                )
            elif major > 2 or (major == 2 and minor > 1):
                self.add_warning(
                    "MoviePy",
                    f"Versão do MoviePy mais recente que a testada: {self.moviepy_version}",
                    "Verifique se há alterações na API que possam afetar o código"
                )
            else:
                color_print("Versão do MoviePy: OK", Colors.GREEN)
            
            # Verificar módulos principais
            modules = [
                "moviepy.editor",
                "moviepy.audio",
                "moviepy.video",
                "moviepy.video.fx",
                "moviepy.audio.fx"
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
    
    def check_dependencies(self):
        """Verifica as dependências do MoviePy"""
        print_section("Verificação de Dependências")
        
        # Lista de dependências
        dependencies = [
            ("numpy", "numpy", "1.15.0"),
            ("PIL", "Pillow", "6.0.0"),
            ("imageio", "imageio", "2.5.0"),
            ("decorator", "decorator", "4.3.0"),
            ("tqdm", "tqdm", "4.30.0")
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
    
    def check_ffmpeg(self):
        """Verifica a instalação do FFmpeg"""
        print_section("Verificação do FFmpeg")
        
        try:
            result = subprocess.run(
                ["ffmpeg", "-version"], 
                capture_output=True, 
                text=True
            )
            if result.returncode == 0:
                version = result.stdout.split('\n')[0]
                color_print("FFmpeg: Instalado", Colors.GREEN)
                color_print(f"Versão: {version.split(' ')[2]}", Colors.WHITE)
            else:
                self.add_issue(
                    "FFmpeg",
                    "FFmpeg não encontrado ou erro na execução",
                    "Instale o FFmpeg e adicione ao PATH"
                )
        except FileNotFoundError:
            self.add_issue(
                "FFmpeg",
                "FFmpeg não encontrado no PATH",
                "Instale o FFmpeg e adicione ao PATH"
            )
        
        print()
    
    def check_imagemagick(self):
        """Verifica a instalação do ImageMagick"""
        print_section("Verificação do ImageMagick")
        
        try:
            result = subprocess.run(
                ["magick", "-version"], 
                capture_output=True, 
                text=True
            )
            if result.returncode == 0:
                version = result.stdout.split('\n')[0]
                color_print("ImageMagick: Instalado", Colors.GREEN)
                color_print(f"Versão: {version.split(' ')[2]}", Colors.WHITE)
            else:
                self.add_warning(
                    "ImageMagick",
                    "ImageMagick não encontrado ou erro na execução",
                    "Instale o ImageMagick para funcionalidades de texto"
                )
        except FileNotFoundError:
            self.add_warning(
                "ImageMagick",
                "ImageMagick não encontrado no PATH",
                "Instale o ImageMagick para funcionalidades de texto"
            )
        
        print()
    
    def check_basic_functionality(self):
        """Verifica funcionalidades básicas do MoviePy"""
        print_section("Verificação de Funcionalidades Básicas")
        
        if self.moviepy_version is None:
            self.add_issue(
                "Funcionalidades",
                "MoviePy não está instalado",
                "Instale o MoviePy: pip install moviepy"
            )
            return
        
        try:
            from moviepy.editor import ColorClip, TextClip, concatenate_videoclips
            
            # Testar criação de clipe de cor
            try:
                clip = ColorClip(size=(100, 100), color=(255, 0, 0), duration=1)
                color_print("Criação de ColorClip: OK", Colors.GREEN)
            except Exception as e:
                self.add_issue(
                    "Funcionalidades",
                    f"Erro ao criar ColorClip: {e}",
                    "Verifique a instalação do MoviePy"
                )
            
            # Testar criação de texto
            try:
                txt = TextClip(text="Teste", font_size=24, color='white')
                color_print("Criação de TextClip: OK", Colors.GREEN)
            except Exception as e:
                self.add_warning(
                    "Funcionalidades",
                    f"Erro ao criar TextClip: {e}",
                    "Verifique a instalação do ImageMagick"
                )
            
            # Testar concatenação
            try:
                clip1 = ColorClip(size=(100, 100), color=(255, 0, 0), duration=1)
                clip2 = ColorClip(size=(100, 100), color=(0, 255, 0), duration=1)
                concatenated = concatenate_videoclips([clip1, clip2])
                color_print("Concatenação de clipes: OK", Colors.GREEN)
            except Exception as e:
                self.add_issue(
                    "Funcionalidades",
                    f"Erro ao concatenar clipes: {e}",
                    "Verifique a instalação do MoviePy"
                )
            
        except Exception as e:
            self.add_issue(
                "Funcionalidades",
                f"Erro ao verificar funcionalidades: {e}",
                "Verifique a instalação do MoviePy"
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
            results_file = os.path.join(tempfile.gettempdir(), "moviepy_diagnostic_simples.txt")
            
            with open(results_file, 'w', encoding='utf-8') as f:
                f.write("=== RESULTADOS DO DIAGNÓSTICO SIMPLIFICADO DO MOVIEPY ===\n\n")
                
                # Informações gerais
                f.write(f"Data: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Sistema: {platform.system()} {platform.release()}\n")
                f.write(f"Python: {sys.version}\n")
                
                # Verificar se o MoviePy está instalado
                if self.moviepy_version:
                    f.write(f"MoviePy: {self.moviepy_version}\n")
                else:
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
        diagnostic = SimpleMoviePyDiagnostic()
        
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