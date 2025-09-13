#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup script para MoviePy 2.1.2

Este script configura o ambiente para o MoviePy e suas dependências.
"""

import os
import sys
import subprocess
import platform
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

def run_command(command, description="", check=True):
    """Executa um comando e retorna o resultado"""
    try:
        color_print(f"Executando: {command}", Colors.YELLOW)
        if description:
            color_print(f"Descrição: {description}", Colors.YELLOW)
        
        result = subprocess.run(command, shell=True, check=check, 
                              capture_output=True, text=True)
        
        if result.stdout:
            color_print("Saída:", Colors.GREEN)
            color_print(result.stdout, Colors.WHITE)
        
        if result.stderr:
            color_print("Erros:", Colors.RED)
            color_print(result.stderr, Colors.RED)
        
        return result
    except subprocess.CalledProcessError as e:
        color_print(f"Erro ao executar comando: {e}", Colors.RED)
        if e.stdout:
            color_print("Saída:", Colors.YELLOW)
            color_print(e.stdout, Colors.WHITE)
        if e.stderr:
            color_print("Erros:", Colors.RED)
            color_print(e.stderr, Colors.RED)
        return None

def check_python_version():
    """Verifica a versão do Python"""
    print_section("Verificar Versão do Python")
    
    version = sys.version_info
    color_print(f"Versão do Python: {version.major}.{version.minor}.{version.micro}", Colors.WHITE)
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        color_print("Python 3.7 ou superior é necessário!", Colors.RED)
        return False
    
    color_print("Versão do Python compatível!", Colors.GREEN)
    return True

def check_pip():
    """Verifica se o pip está instalado"""
    print_section("Verificar Pip")
    
    result = run_command("pip --version", "Verificar versão do pip")
    
    if result and result.returncode == 0:
        color_print("Pip está instalado!", Colors.GREEN)
        return True
    
    color_print("Pip não está instalado!", Colors.RED)
    return False

def install_dependencies():
    """Instala as dependências do MoviePy"""
    print_section("Instalar Dependências")
    
    # Obter o diretório atual
    current_dir = os.path.dirname(os.path.abspath(__file__))
    requirements_file = os.path.join(current_dir, "requirements.txt")
    
    if not os.path.exists(requirements_file):
        color_print(f"Arquivo requirements.txt não encontrado: {requirements_file}", Colors.RED)
        return False
    
    # Instalar dependências
    result = run_command(f"pip install -r {requirements_file}", 
                        "Instalar dependências do MoviePy")
    
    if result and result.returncode == 0:
        color_print("Dependências instaladas com sucesso!", Colors.GREEN)
        return True
    
    color_print("Falha ao instalar dependências!", Colors.RED)
    return False

def check_ffmpeg():
    """Verifica se o FFmpeg está instalado"""
    print_section("Verificar FFmpeg")
    
    result = run_command("ffmpeg -version", "Verificar versão do FFmpeg", check=False)
    
    if result and result.returncode == 0:
        color_print("FFmpeg está instalado!", Colors.GREEN)
        return True
    
    color_print("FFmpeg não está instalado!", Colors.RED)
    color_print("Por favor, instale o FFmpeg:", Colors.YELLOW)
    color_print("1. Baixe do site: https://ffmpeg.org/download.html", Colors.WHITE)
    color_print("2. Adicione ao PATH do sistema", Colors.WHITE)
    color_print("3. Verifique com: ffmpeg -version", Colors.WHITE)
    return False

def check_imagemagick():
    """Verifica se o ImageMagick está instalado"""
    print_section("Verificar ImageMagick")
    
    # Verificar diferentes comandos dependendo do SO
    system = platform.system()
    
    if system == "Windows":
        commands = ["magick -version", "convert -version"]
    else:
        commands = ["convert -version"]
    
    for cmd in commands:
        result = run_command(cmd, f"Verificar versão do ImageMagick com {cmd}", check=False)
        if result and result.returncode == 0:
            color_print("ImageMagick está instalado!", Colors.GREEN)
            return True
    
    color_print("ImageMagick não está instalado!", Colors.RED)
    color_print("Por favor, instale o ImageMagick:", Colors.YELLOW)
    color_print("1. Baixe do site: https://imagemagick.org/script/download.php", Colors.WHITE)
    color_print("2. Adicione ao PATH do sistema", Colors.WHITE)
    color_print("3. Verifique com: magick -version (Windows) ou convert -version (Linux/Mac)", Colors.WHITE)
    return False

def test_moviepy():
    """Testa a instalação do MoviePy"""
    print_section("Testar MoviePy")
    
    test_code = """
import moviepy.editor as mpy
import os

# Criar um clipe de teste
clip = mpy.ColorClip(size=(100, 100), color=(255, 0, 0), duration=1)
output_file = "test_moviepy.mp4"

try:
    # Tentar escrever o clipe
    clip.write_videofile(output_file, fps=24, verbose=False)
    
    # Verificar se o arquivo foi criado
    if os.path.exists(output_file):
        print("MoviePy está funcionando corretamente!")
        # Limpar arquivo de teste
        os.remove(output_file)
    else:
        print("Falha ao criar arquivo de teste!")
except Exception as e:
    print(f"Erro ao testar MoviePy: {e}")
"""
    
    # Criar arquivo de teste temporário
    test_file = "test_moviepy_setup.py"
    with open(test_file, "w") as f:
        f.write(test_code)
    
    # Executar teste
    result = run_command(f"python {test_file}", "Testar instalação do MoviePy")
    
    # Limpar arquivo de teste
    try:
        os.remove(test_file)
    except:
        pass
    
    if result and result.returncode == 0:
        color_print("MoviePy está funcionando corretamente!", Colors.GREEN)
        return True
    
    color_print("Falha ao testar MoviePy!", Colors.RED)
    return False

def create_directories():
    """Cria diretórios necessários"""
    print_section("Criar Diretórios")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Lista de diretórios a criar
    directories = [
        "temp",
        "output",
        "logs",
        "cache",
        "examples_output"
    ]
    
    for directory in directories:
        dir_path = os.path.join(current_dir, directory)
        try:
            os.makedirs(dir_path, exist_ok=True)
            color_print(f"Diretório criado: {dir_path}", Colors.GREEN)
        except Exception as e:
            color_print(f"Falha ao criar diretório {dir_path}: {e}", Colors.RED)
            return False
    
    color_print("Todos os diretórios foram criados!", Colors.GREEN)
    return True

def main():
    """Função principal"""
    print_header("SETUP DO MOVIEPY 2.1.2")
    
    # Verificar Python
    if not check_python_version():
        return 1
    
    # Verificar pip
    if not check_pip():
        return 1
    
    # Instalar dependências
    if not install_dependencies():
        return 1
    
    # Verificar FFmpeg
    if not check_ffmpeg():
        color_print("AVISO: FFmpeg não está instalado. Alguns recursos podem não funcionar!", Colors.YELLOW)
    
    # Verificar ImageMagick
    if not check_imagemagick():
        color_print("AVISO: ImageMagick não está instalado. Recursos de texto podem não funcionar!", Colors.YELLOW)
    
    # Criar diretórios
    if not create_directories():
        return 1
    
    # Testar MoviePy
    if not test_moviepy():
        color_print("AVISO: MoviePy pode não estar funcionando corretamente!", Colors.YELLOW)
    
    # Resumo
    print_section("Resumo")
    color_print("Setup do MoviePy concluído!", Colors.GREEN)
    color_print("Próximos passos:", Colors.WHITE)
    color_print("1. Execute o script de diagnóstico: python testes/SCRIPT_DIAGNOSTICO_COMPLETO.py", Colors.CYAN)
    color_print("2. Execute os testes: python testes/SCRIPT_TESTES_COMPLETO.py", Colors.CYAN)
    color_print("3. Execute os exemplos: python exemplos/SCRIPT_EXEMPLOS_PRACTICOS.py", Colors.CYAN)
    color_print("4. Execute todos os scripts: python SCRIPT_MAIN.py --all", Colors.CYAN)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())