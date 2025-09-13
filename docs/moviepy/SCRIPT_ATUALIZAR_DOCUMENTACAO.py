#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para atualizar a documentação do MoviePy para a versão mais recente

Este script verifica a versão mais recente do MoviePy e atualiza a documentação
conforme necessário.
"""

import os
import sys
import json
import time
import subprocess
import requests
import re
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

def print_result(step_name, success, message=""):
    """Imprime um resultado de passo"""
    if success:
        color_print(f"✓ {step_name}: SUCESSO", Colors.GREEN)
    else:
        color_print(f"✗ {step_name}: FALHA", Colors.RED)
    
    if message:
        print(f"  {message}")
    
    print()

class MoviePyDocumentationUpdater:
    """Classe para atualizar a documentação do MoviePy"""
    
    def __init__(self):
        self.results = []
        self.start_time = None
        self.project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        self.docs_dir = os.path.join(self.project_dir, "docs", "moviepy")
        self.python_executable = sys.executable
        
        # URLs para verificar a versão mais recente
        self.pypi_url = "https://pypi.org/pypi/moviepy/json"
        self.github_url = "https://api.github.com/repos/Zulko/moviepy/releases/latest"
        
        # Versão atual
        self.current_version = "2.1.2"
        
        # Arquivos a serem atualizados
        self.files_to_update = [
            "documentacao/DOCUMENTACAO_COMPLETA.md",
            "guias/GUIA_REFERENCIA_RAPIDA.md",
            "solucoes/SOLUCOES_PROBLEMAS_COMUNS.md",
            "testes/TESTES_COMPLETOS.md",
            "exemplos/EXEMPLOS_PRACTICOS.md",
            "README.md"
        ]
        
        # Scripts a serem atualizados
        self.scripts_to_update = [
            "testes/SCRIPT_TESTES_COMPLETO.py",
            "exemplos/SCRIPT_EXEMPLOS_PRACTICOS.py",
            "testes/SCRIPT_DIAGNOSTICO_COMPLETO.py",
            "guias/SCRIPT_INSTALACAO_CONFIGURACAO.py",
            "SCRIPT_RUN_ALL_TESTS.py",
            "SCRIPT_CLEAN_TEMP_FILES.py",
            "SCRIPT_GERAR_RELATORIO.py"
        ]
    
    def add_result(self, step_name, success, message=""):
        """Adiciona um resultado de passo"""
        self.results.append((step_name, success, message))
        print_result(step_name, success, message)
    
    def update_documentation(self):
        """Atualiza a documentação do MoviePy"""
        self.start_time = time.time()
        
        print_header("ATUALIZAÇÃO DA DOCUMENTAÇÃO DO MOVIEPY")
        
        # Verificar ambiente
        self.check_environment()
        
        # Verificar versão atual
        self.check_current_version()
        
        # Verificar versão mais recente
        self.check_latest_version()
        
        # Comparar versões
        self.compare_versions()
        
        # Atualizar arquivos
        self.update_files()
        
        # Atualizar scripts
        self.update_scripts()
        
        # Resumo
        self.print_summary()
        
        return True
    
    def check_environment(self):
        """Verifica o ambiente de execução"""
        print_section("Verificar Ambiente")
        
        # Verificar diretório do projeto
        if os.path.exists(self.project_dir):
            self.add_result("Diretório do Projeto", True, self.project_dir)
        else:
            self.add_result("Diretório do Projeto", False, f"Não encontrado: {self.project_dir}")
        
        # Verificar diretório de documentação
        if os.path.exists(self.docs_dir):
            self.add_result("Diretório de Documentação", True, self.docs_dir)
        else:
            self.add_result("Diretório de Documentação", False, f"Não encontrado: {self.docs_dir}")
        
        # Verificar Python
        try:
            result = subprocess.run([self.python_executable, "--version"], 
                                  capture_output=True, text=True, check=True)
            python_version = result.stdout.strip()
            self.add_result("Python", True, python_version)
        except Exception as e:
            self.add_result("Python", False, str(e))
        
        # Verificar pip
        try:
            result = subprocess.run([self.python_executable, "-m", "pip", "--version"], 
                                  capture_output=True, text=True, check=True)
            pip_version = result.stdout.strip()
            self.add_result("pip", True, pip_version)
        except Exception as e:
            self.add_result("pip", False, str(e))
        
        # Verificar MoviePy instalado
        try:
            result = subprocess.run([self.python_executable, "-c", "import moviepy; print(moviepy.__version__)"], 
                                  capture_output=True, text=True, check=True)
            installed_version = result.stdout.strip()
            self.add_result("MoviePy Instalado", True, f"Versão: {installed_version}")
            self.current_version = installed_version
        except Exception as e:
            self.add_result("MoviePy Instalado", False, str(e))
    
    def check_current_version(self):
        """Verifica a versão atual do MoviePy na documentação"""
        print_section("Verificar Versão Atual")
        
        # Verificar versão no README.md
        readme_path = os.path.join(self.docs_dir, "README.md")
        if os.path.exists(readme_path):
            try:
                with open(readme_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Procurar por versão no conteúdo
                version_pattern = r"MoviePy\s+(\d+\.\d+\.\d+)"
                match = re.search(version_pattern, content)
                if match:
                    doc_version = match.group(1)
                    self.add_result("Versão na Documentação", True, f"Versão: {doc_version}")
                    self.current_version = doc_version
                else:
                    self.add_result("Versão na Documentação", False, "Não encontrada")
            except Exception as e:
                self.add_result("Versão na Documentação", False, str(e))
        else:
            self.add_result("Versão na Documentação", False, f"Arquivo não encontrado: {readme_path}")
    
    def check_latest_version(self):
        """Verifica a versão mais recente do MoviePy"""
        print_section("Verificar Versão Mais Recente")
        
        self.latest_version = None
        
        # Tentar obter versão do PyPI
        try:
            response = requests.get(self.pypi_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.latest_version = data["info"]["version"]
                self.add_result("Versão do PyPI", True, f"Versão: {self.latest_version}")
            else:
                self.add_result("Versão do PyPI", False, f"Status: {response.status_code}")
        except Exception as e:
            self.add_result("Versão do PyPI", False, str(e))
        
        # Tentar obter versão do GitHub
        try:
            response = requests.get(self.github_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                github_version = data["tag_name"].lstrip("v")
                if not self.latest_version or github_version > self.latest_version:
                    self.latest_version = github_version
                    self.add_result("Versão do GitHub", True, f"Versão: {github_version}")
            else:
                self.add_result("Versão do GitHub", False, f"Status: {response.status_code}")
        except Exception as e:
            self.add_result("Versão do GitHub", False, str(e))
        
        if not self.latest_version:
            self.add_result("Versão Mais Recente", False, "Não foi possível determinar")
    
    def compare_versions(self):
        """Compara as versões atual e mais recente"""
        print_section("Comparar Versões")
        
        if not self.latest_version:
            self.add_result("Comparar Versões", False, "Versão mais recente não disponível")
            return
        
        # Converter versões para tuplas de inteiros
        current_parts = tuple(map(int, self.current_version.split('.')))
        latest_parts = tuple(map(int, self.latest_version.split('.')))
        
        # Comparar versões
        if current_parts == latest_parts:
            self.add_result("Comparar Versões", True, 
                           f"Versão atual ({self.current_version}) é a mais recente")
            self.update_needed = False
        elif current_parts < latest_parts:
            self.add_result("Comparar Versões", True, 
                           f"Versão atual ({self.current_version}) é mais antiga que a mais recente ({self.latest_version})")
            self.update_needed = True
        else:
            self.add_result("Comparar Versões", True, 
                           f"Versão atual ({self.current_version}) é mais recente que a versão pública ({self.latest_version})")
            self.update_needed = False
    
    def update_files(self):
        """Atualiza os arquivos de documentação"""
        print_section("Atualizar Arquivos")
        
        if not hasattr(self, 'update_needed') or not self.update_needed:
            self.add_result("Atualizar Arquivos", True, "Nenhuma atualização necessária")
            return
        
        updated_files = 0
        
        for file_path in self.files_to_update:
            full_path = os.path.join(self.docs_dir, file_path)
            
            if os.path.exists(full_path):
                try:
                    # Ler conteúdo do arquivo
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Substituir versão
                    old_content = content
                    content = re.sub(r"MoviePy\s+\d+\.\d+\.\d+", f"MoviePy {self.latest_version}", content)
                    content = re.sub(r"versão\s+\d+\.\d+\.\d+", f"versão {self.latest_version}", content)
                    content = re.sub(r"version\s+\d+\.\d+\.\d+", f"version {self.latest_version}", content)
                    
                    # Se houve mudanças, salvar o arquivo
                    if content != old_content:
                        with open(full_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        updated_files += 1
                        self.add_result(f"Atualizar {file_path}", True, f"Versão atualizada para {self.latest_version}")
                    else:
                        self.add_result(f"Atualizar {file_path}", True, "Nenhuma alteração necessária")
                except Exception as e:
                    self.add_result(f"Atualizar {file_path}", False, str(e))
            else:
                self.add_result(f"Atualizar {file_path}", False, f"Arquivo não encontrado: {full_path}")
        
        self.add_result("Atualizar Arquivos", True, f"Arquivos atualizados: {updated_files}")
    
    def update_scripts(self):
        """Atualiza os scripts"""
        print_section("Atualizar Scripts")
        
        if not hasattr(self, 'update_needed') or not self.update_needed:
            self.add_result("Atualizar Scripts", True, "Nenhuma atualização necessária")
            return
        
        updated_scripts = 0
        
        for script_path in self.scripts_to_update:
            full_path = os.path.join(self.docs_dir, script_path)
            
            if os.path.exists(full_path):
                try:
                    # Ler conteúdo do script
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Substituir versão
                    old_content = content
                    content = re.sub(r"MoviePy\s+\d+\.\d+\.\d+", f"MoviePy {self.latest_version}", content)
                    content = re.sub(r"versão\s+\d+\.\d+\.\d+", f"versão {self.latest_version}", content)
                    content = re.sub(r"version\s+\d+\.\d+\.\d+", f"version {self.latest_version}", content)
                    
                    # Se houve mudanças, salvar o arquivo
                    if content != old_content:
                        with open(full_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        updated_scripts += 1
                        self.add_result(f"Atualizar {script_path}", True, f"Versão atualizada para {self.latest_version}")
                    else:
                        self.add_result(f"Atualizar {script_path}", True, "Nenhuma alteração necessária")
                except Exception as e:
                    self.add_result(f"Atualizar {script_path}", False, str(e))
            else:
                self.add_result(f"Atualizar {script_path}", False, f"Arquivo não encontrado: {full_path}")
        
        self.add_result("Atualizar Scripts", True, f"Scripts atualizados: {updated_scripts}")
    
    def print_summary(self):
        """Imprime um resumo da atualização"""
        print_section("Resumo da Atualização")
        
        # Calcular estatísticas
        total_steps = len(self.results)
        successful_steps = sum(1 for _, success, _ in self.results if success)
        failed_steps = total_steps - successful_steps
        
        # Imprimir estatísticas
        color_print(f"Total de passos: {total_steps}", Colors.WHITE)
        color_print(f"Passos bem-sucedidos: {successful_steps}", Colors.GREEN)
        color_print(f"Passos falhos: {failed_steps}", Colors.RED)
        
        # Calcular porcentagem
        if total_steps > 0:
            percentage = (successful_steps / total_steps) * 100
            color_print(f"Taxa de sucesso: {percentage:.1f}%", Colors.WHITE)
        
        # Tempo total
        total_time = time.time() - self.start_time
        color_print(f"Tempo total de execução: {total_time:.2f}s", Colors.WHITE)
        
        # Informações de versão
        if hasattr(self, 'current_version'):
            color_print(f"Versão atual: {self.current_version}", Colors.WHITE)
        
        if hasattr(self, 'latest_version'):
            color_print(f"Versão mais recente: {self.latest_version}", Colors.WHITE)
        
        # Verificar se todos os passos foram bem-sucedidos
        if failed_steps == 0:
            color_print("\n✓ Atualização concluída com sucesso!", Colors.GREEN)
        else:
            color_print(f"\n✗ {failed_steps} passo(s) falharam!", Colors.RED)
            
            # Listar passos falhos
            color_print("\nPassos falhos:", Colors.RED)
            for step_name, success, message in self.results:
                if not success:
                    color_print(f"- {step_name}: {message}", Colors.RED)
        
        # Próximos passos
        self.print_next_steps()
    
    def print_next_steps(self):
        """Imprime os próximos passos"""
        print_section("Próximos Passos")
        
        if hasattr(self, 'update_needed') and self.update_needed:
            color_print("1. Atualize o MoviePy instalado:", Colors.WHITE)
            color_print(f"   {self.python_executable} -m pip install --upgrade moviepy", Colors.CYAN)
        
        color_print("\n2. Execute os testes:", Colors.WHITE)
        color_print(f"   python {os.path.join(self.project_dir, 'docs', 'moviepy', 'SCRIPT_RUN_ALL_TESTS.py')}", Colors.CYAN)
        
        color_print("\n3. Gere um relatório:", Colors.WHITE)
        color_print(f"   python {os.path.join(self.project_dir, 'docs', 'moviepy', 'SCRIPT_GERAR_RELATORIO.py')}", Colors.CYAN)
        
        color_print("\n4. Verifique a documentação:", Colors.WHITE)
        color_print(f"   Leia {os.path.join(self.project_dir, 'docs', 'moviepy', 'README.md')} para mais informações", Colors.CYAN)

def main():
    """Função principal"""
    try:
        # Criar atualizador
        updater = MoviePyDocumentationUpdater()
        
        # Atualizar documentação
        success = updater.update_documentation()
        
        # Retornar código de saída
        return 0 if success else 1
    except KeyboardInterrupt:
        color_print("\nAtualização interrompida pelo usuário", Colors.YELLOW)
        return 1
    except Exception as e:
        color_print(f"\nErro inesperado: {e}", Colors.RED)
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())