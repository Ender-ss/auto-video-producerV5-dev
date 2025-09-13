#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de instalação e configuração para MoviePy no projeto auto-video-producerV5-dev

Este script ajuda a instalar e configurar o MoviePy e suas dependências.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_header(title):
    """Imprime um cabeçalho"""
    print("=" * 60)
    print(title.center(60))
    print("=" * 60)
    print()

def print_section(title):
    """Imprime uma seção"""
    print("-" * 40)
    print(title)
    print("-" * 40)
    print()

def run_command(command, description):
    """Executa um comando e exibe o resultado"""
    print(f"Executando: {description}")
    print(f"Comando: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"✓ Sucesso: {description}")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Falha: {description}")
        print(f"Erro: {e.stderr}")
        return False

def install_moviepy():
    """Instala o MoviePy na versão correta"""
    print_section("Instalando MoviePy 2.1.2")
    
    # Comando para instalar o MoviePy
    command = "pip install moviepy==2.1.2"
    success = run_command(command, "Instalar MoviePy 2.1.2")
    
    if success:
        print("MoviePy 2.1.2 instalado com sucesso!")
    else:
        print("Falha ao instalar MoviePy 2.1.2")
    
    return success

def install_ffmpeg():
    """Instala o FFmpeg"""
    print_section("Instalando FFmpeg")
    
    # Verificar o sistema operacional
    system = platform.system().lower()
    
    if system == "windows":
        print("Sistema: Windows")
        print("Para instalar o FFmpeg no Windows:")
        print("1. Baixe o FFmpeg de: https://ffmpeg.org/download.html")
        print("2. Extraia o arquivo em um local permanente (ex: C:\\ffmpeg)")
        print("3. Adicione o diretório bin ao PATH do sistema")
        print("   - Ex: C:\\ffmpeg\\bin")
        print("\nVocê pode usar o Chocolatey para instalar:")
        print("choco install ffmpeg")
        
        # Tentar instalar com Chocolatey se disponível
        return run_command("choco install ffmpeg", "Instalar FFmpeg com Chocolatey")
    
    elif system == "linux":
        print("Sistema: Linux")
        
        # Tentar diferentes gerenciadores de pacotes
        if run_command("which apt-get", "Verificar apt-get"):
            return run_command("sudo apt-get update && sudo apt-get install -y ffmpeg", "Instalar FFmpeg com apt-get")
        elif run_command("which yum", "Verificar yum"):
            return run_command("sudo yum install -y ffmpeg", "Instalar FFmpeg com yum")
        elif run_command("which dnf", "Verificar dnf"):
            return run_command("sudo dnf install -y ffmpeg", "Instalar FFmpeg com dnf")
        else:
            print("Gerenciador de pacotes não reconhecido")
            return False
    
    elif system == "darwin":
        print("Sistema: macOS")
        
        # Tentar instalar com Homebrew
        if run_command("which brew", "Verificar Homebrew"):
            return run_command("brew install ffmpeg", "Instalar FFmpeg com Homebrew")
        else:
            print("Homebrew não encontrado")
            return False
    
    else:
        print(f"Sistema não reconhecido: {system}")
        return False

def verify_installation():
    """Verifica se a instalação foi bem-sucedida"""
    print_section("Verificando instalação")
    
    # Verificar MoviePy
    try:
        import moviepy
        print(f"✓ MoviePy instalado: {moviepy.__version__}")
        
        if moviepy.__version__ == "2.1.2":
            print("✓ Versão correta do MoviePy")
        else:
            print(f"✗ Versão incorreta do MoviePy: {moviepy.__version__} (esperado: 2.1.2)")
            return False
    except ImportError:
        print("✗ MoviePy não está instalado")
        return False
    
    # Verificar moviepy.editor
    try:
        from moviepy.editor import *
        print("✓ moviepy.editor está disponível")
    except ImportError:
        print("✗ moviepy.editor não está disponível")
        return False
    
    # Verificar FFmpeg
    if run_command("ffmpeg -version", "Verificar FFmpeg"):
        print("✓ FFmpeg está instalado e disponível")
    else:
        print("✗ FFmpeg não está instalado ou não está no PATH")
        return False
    
    return True

def main():
    """Função principal"""
    print_header("INSTALAÇÃO E CONFIGURAÇÃO DO MOVIEPY")
    
    # Instalar MoviePy
    moviepy_installed = install_moviepy()
    
    # Instalar FFmpeg
    ffmpeg_installed = install_ffmpeg()
    
    # Verificar instalação
    if moviepy_installed and ffmpeg_installed:
        print("\n" + "=" * 60)
        print("INSTALAÇÃO CONCLUÍDA".center(60))
        print("=" * 60)
        
        if verify_installation():
            print("\n✓ Tudo está instalado e configurado corretamente!")
            print("\nAgora você pode executar o script de diagnóstico:")
            print("python diagnose.ps1 complete")
        else:
            print("\n✗ Alguns componentes não foram instalados corretamente")
    else:
        print("\n" + "=" * 60)
        print("FALHA NA INSTALAÇÃO".center(60))
        print("=" * 60)
        print("\nAlguns componentes não foram instalados corretamente")
        print("Verifique as mensagens de erro acima e tente novamente")

if __name__ == "__main__":
    main()