#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para limpar arquivos temporários gerados pelos testes do MoviePy

Este script limpa os arquivos temporários gerados durante a execução
dos testes e exemplos do MoviePy.
"""

import os
import sys
import shutil
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

def print_result(step_name, success, message=""):
    """Imprime um resultado de passo"""
    if success:
        color_print(f"✓ {step_name}: SUCESSO", Colors.GREEN)
    else:
        color_print(f"✗ {step_name}: FALHA", Colors.RED)
    
    if message:
        print(f"  {message}")
    
    print()

class MoviePyCleaner:
    """Classe para limpar arquivos temporários do MoviePy"""
    
    def __init__(self):
        self.results = []
        self.start_time = None
        self.project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        self.temp_dir = os.path.join(self.project_dir, "temp")
        self.output_dir = os.path.join(self.project_dir, "outputs")
        self.logs_dir = os.path.join(self.project_dir, "logs")
        self.python_executable = sys.executable
        
        # Padrões de arquivos para limpar
        self.file_patterns = [
            "*.mp4",
            "*.avi",
            "*.mov",
            "*.mkv",
            "*.flv",
            "*.webm",
            "*.gif",
            "*.jpg",
            "*.jpeg",
            "*.png",
            "*.wav",
            "*.mp3",
            "*.aac",
            "*.flac",
            "*.log",
            "*.txt",
            "*.html",
            "*.pyc",
            "__pycache__",
            ".pytest_cache",
            ".coverage"
        ]
        
        # Diretórios específicos para limpar
        self.specific_dirs = [
            os.path.join(self.temp_dir, "moviepy"),
            os.path.join(self.temp_dir, "test_videos"),
            os.path.join(self.temp_dir, "test_audio"),
            os.path.join(self.temp_dir, "test_images"),
            os.path.join(self.temp_dir, "test_output"),
            os.path.join(self.output_dir, "test_videos"),
            os.path.join(self.output_dir, "test_audio"),
            os.path.join(self.output_dir, "test_images"),
            os.path.join(self.logs_dir, "moviepy_tests"),
            os.path.join(self.logs_dir, "moviepy_examples"),
            os.path.join(self.logs_dir, "moviepy_diagnostic")
        ]
    
    def add_result(self, step_name, success, message=""):
        """Adiciona um resultado de passo"""
        self.results.append((step_name, success, message))
        print_result(step_name, success, message)
    
    def clean_all(self):
        """Executa a limpeza completa"""
        self.start_time = time.time()
        
        print_header("LIMPEZA DE ARQUIVOS TEMPORÁRIOS DO MOVIEPY")
        
        # Verificar ambiente
        self.check_environment()
        
        # Limpar diretório temporário
        self.clean_temp_directory()
        
        # Limpar diretório de saída
        self.clean_output_directory()
        
        # Limpar diretório de logs
        self.clean_logs_directory()
        
        # Limpar arquivos específicos
        self.clean_specific_files()
        
        # Limpar diretórios específicos
        self.clean_specific_directories()
        
        # Limpar cache do Python
        self.clean_python_cache()
        
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
        
        # Verificar diretório temporário
        if os.path.exists(self.temp_dir):
            self.add_result("Diretório Temporário", True, self.temp_dir)
        else:
            self.add_result("Diretório Temporário", False, f"Não encontrado: {self.temp_dir}")
        
        # Verificar diretório de saída
        if os.path.exists(self.output_dir):
            self.add_result("Diretório de Saída", True, self.output_dir)
        else:
            self.add_result("Diretório de Saída", False, f"Não encontrado: {self.output_dir}")
        
        # Verificar diretório de logs
        if os.path.exists(self.logs_dir):
            self.add_result("Diretório de Logs", True, self.logs_dir)
        else:
            self.add_result("Diretório de Logs", False, f"Não encontrado: {self.logs_dir}")
    
    def clean_temp_directory(self):
        """Limpa o diretório temporário"""
        print_section("Limpar Diretório Temporário")
        
        if not os.path.exists(self.temp_dir):
            self.add_result("Limpar Diretório Temporário", False, f"Diretório não existe: {self.temp_dir}")
            return
        
        try:
            # Contar arquivos antes da limpeza
            file_count_before = self.count_files_in_directory(self.temp_dir)
            
            # Remover arquivos com base nos padrões
            removed_files = 0
            for pattern in self.file_patterns:
                removed_files += self.remove_files_by_pattern(self.temp_dir, pattern)
            
            # Contar arquivos após a limpeza
            file_count_after = self.count_files_in_directory(self.temp_dir)
            
            self.add_result("Limpar Diretório Temporário", True, 
                           f"Arquivos removidos: {removed_files}, "
                           f"Arquivos antes: {file_count_before}, "
                           f"Arquivos depois: {file_count_after}")
        except Exception as e:
            self.add_result("Limpar Diretório Temporário", False, str(e))
    
    def clean_output_directory(self):
        """Limpa o diretório de saída"""
        print_section("Limpar Diretório de Saída")
        
        if not os.path.exists(self.output_dir):
            self.add_result("Limpar Diretório de Saída", False, f"Diretório não existe: {self.output_dir}")
            return
        
        try:
            # Contar arquivos antes da limpeza
            file_count_before = self.count_files_in_directory(self.output_dir)
            
            # Remover arquivos com base nos padrões
            removed_files = 0
            for pattern in self.file_patterns:
                if pattern in ["*.mp4", "*.avi", "*.mov", "*.mkv", "*.flv", "*.webm", "*.gif"]:
                    removed_files += self.remove_files_by_pattern(self.output_dir, pattern)
            
            # Contar arquivos após a limpeza
            file_count_after = self.count_files_in_directory(self.output_dir)
            
            self.add_result("Limpar Diretório de Saída", True, 
                           f"Arquivos removidos: {removed_files}, "
                           f"Arquivos antes: {file_count_before}, "
                           f"Arquivos depois: {file_count_after}")
        except Exception as e:
            self.add_result("Limpar Diretório de Saída", False, str(e))
    
    def clean_logs_directory(self):
        """Limpa o diretório de logs"""
        print_section("Limpar Diretório de Logs")
        
        if not os.path.exists(self.logs_dir):
            self.add_result("Limpar Diretório de Logs", False, f"Diretório não existe: {self.logs_dir}")
            return
        
        try:
            # Contar arquivos antes da limpeza
            file_count_before = self.count_files_in_directory(self.logs_dir)
            
            # Remover arquivos com base nos padrões
            removed_files = 0
            for pattern in self.file_patterns:
                if pattern in ["*.log", "*.txt", "*.html"]:
                    removed_files += self.remove_files_by_pattern(self.logs_dir, pattern)
            
            # Contar arquivos após a limpeza
            file_count_after = self.count_files_in_directory(self.logs_dir)
            
            self.add_result("Limpar Diretório de Logs", True, 
                           f"Arquivos removidos: {removed_files}, "
                           f"Arquivos antes: {file_count_before}, "
                           f"Arquivos depois: {file_count_after}")
        except Exception as e:
            self.add_result("Limpar Diretório de Logs", False, str(e))
    
    def clean_specific_files(self):
        """Limpa arquivos específicos"""
        print_section("Limpar Arquivos Específicos")
        
        # Lista de arquivos específicos para remover
        specific_files = [
            os.path.join(self.temp_dir, "moviepy_test_report.html"),
            os.path.join(self.temp_dir, "installation_results.txt"),
            os.path.join(self.temp_dir, "diagnostic_results.txt"),
            os.path.join(self.temp_dir, "test_results.txt"),
            os.path.join(self.temp_dir, "examples_results.txt"),
            os.path.join(self.project_dir, "coverage.xml"),
            os.path.join(self.project_dir, ".coverage"),
            os.path.join(self.project_dir, "pytest.xml")
        ]
        
        removed_files = 0
        for file_path in specific_files:
            try:
                if os.path.exists(file_path):
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        removed_files += 1
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                        removed_files += 1
            except Exception as e:
                color_print(f"Erro ao remover {file_path}: {e}", Colors.RED)
        
        self.add_result("Limpar Arquivos Específicos", True, f"Arquivos removidos: {removed_files}")
    
    def clean_specific_directories(self):
        """Limpa diretórios específicos"""
        print_section("Limpar Diretórios Específicos")
        
        removed_dirs = 0
        for dir_path in self.specific_dirs:
            try:
                if os.path.exists(dir_path):
                    shutil.rmtree(dir_path)
                    removed_dirs += 1
                    color_print(f"Diretório removido: {dir_path}", Colors.GREEN)
            except Exception as e:
                color_print(f"Erro ao remover {dir_path}: {e}", Colors.RED)
        
        self.add_result("Limpar Diretórios Específicos", True, f"Diretórios removidos: {removed_dirs}")
    
    def clean_python_cache(self):
        """Limpa o cache do Python"""
        print_section("Limpar Cache do Python")
        
        # Encontrar e remover diretórios __pycache__
        removed_dirs = 0
        for root, dirs, files in os.walk(self.project_dir):
            for dir_name in dirs:
                if dir_name == "__pycache__":
                    cache_dir = os.path.join(root, dir_name)
                    try:
                        shutil.rmtree(cache_dir)
                        removed_dirs += 1
                        color_print(f"Cache removido: {cache_dir}", Colors.GREEN)
                    except Exception as e:
                        color_print(f"Erro ao remover {cache_dir}: {e}", Colors.RED)
        
        # Encontrar e remover arquivos .pyc
        removed_files = 0
        for root, dirs, files in os.walk(self.project_dir):
            for file_name in files:
                if file_name.endswith(".pyc"):
                    pyc_file = os.path.join(root, file_name)
                    try:
                        os.remove(pyc_file)
                        removed_files += 1
                        color_print(f"Arquivo .pyc removido: {pyc_file}", Colors.GREEN)
                    except Exception as e:
                        color_print(f"Erro ao remover {pyc_file}: {e}", Colors.RED)
        
        # Remover diretório .pytest_cache se existir
        pytest_cache_dir = os.path.join(self.project_dir, ".pytest_cache")
        if os.path.exists(pytest_cache_dir):
            try:
                shutil.rmtree(pytest_cache_dir)
                removed_dirs += 1
                color_print(f"Diretório pytest cache removido: {pytest_cache_dir}", Colors.GREEN)
            except Exception as e:
                color_print(f"Erro ao remover {pytest_cache_dir}: {e}", Colors.RED)
        
        self.add_result("Limpar Cache do Python", True, 
                       f"Diretórios removidos: {removed_dirs}, "
                       f"Arquivos removidos: {removed_files}")
    
    def count_files_in_directory(self, directory):
        """Conta o número de arquivos em um diretório"""
        count = 0
        for root, dirs, files in os.walk(directory):
            count += len(files)
        return count
    
    def remove_files_by_pattern(self, directory, pattern):
        """Remove arquivos com base em um padrão"""
        removed_count = 0
        
        if pattern.endswith("__pycache__") or pattern.endswith(".pytest_cache"):
            # Remover diretórios
            for root, dirs, files in os.walk(directory):
                for dir_name in dirs:
                    if dir_name == pattern.replace("*", ""):
                        dir_path = os.path.join(root, dir_name)
                        try:
                            shutil.rmtree(dir_path)
                            removed_count += 1
                            color_print(f"Diretório removido: {dir_path}", Colors.GREEN)
                        except Exception as e:
                            color_print(f"Erro ao remover {dir_path}: {e}", Colors.RED)
        else:
            # Remover arquivos
            for root, dirs, files in os.walk(directory):
                for file_name in files:
                    if self.match_pattern(file_name, pattern):
                        file_path = os.path.join(root, file_name)
                        try:
                            os.remove(file_path)
                            removed_count += 1
                            color_print(f"Arquivo removido: {file_path}", Colors.GREEN)
                        except Exception as e:
                            color_print(f"Erro ao remover {file_path}: {e}", Colors.RED)
        
        return removed_count
    
    def match_pattern(self, file_name, pattern):
        """Verifica se um nome de arquivo corresponde a um padrão"""
        if pattern.startswith("*."):
            suffix = pattern[1:]
            return file_name.endswith(suffix)
        elif pattern.endswith("*"):
            prefix = pattern[:-1]
            return file_name.startswith(prefix)
        else:
            return file_name == pattern
    
    def print_summary(self):
        """Imprime um resumo da limpeza"""
        print_section("Resumo da Limpeza")
        
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
        
        # Verificar se todos os passos foram bem-sucedidos
        if failed_steps == 0:
            color_print("\n✓ Limpeza concluída com sucesso!", Colors.GREEN)
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
        
        color_print("1. Execute os testes novamente:", Colors.WHITE)
        color_print(f"   python {os.path.join(self.project_dir, 'docs', 'moviepy', 'SCRIPT_RUN_ALL_TESTS.py')}", Colors.CYAN)
        
        color_print("\n2. Execute exemplos específicos:", Colors.WHITE)
        color_print(f"   python {os.path.join(self.project_dir, 'docs', 'moviepy', 'exemplos', 'SCRIPT_EXEMPLOS_PRACTICOS.py')}", Colors.CYAN)
        
        color_print("\n3. Verifique a documentação:", Colors.WHITE)
        color_print(f"   Leia {os.path.join(self.project_dir, 'docs', 'moviepy', 'README.md')} para mais informações", Colors.CYAN)
        
        color_print("\n4. Execute o diagnóstico:", Colors.WHITE)
        color_print(f"   python {os.path.join(self.project_dir, 'docs', 'moviepy', 'testes', 'SCRIPT_DIAGNOSTICO_COMPLETO.py')}", Colors.CYAN)

def main():
    """Função principal"""
    try:
        # Criar limpador
        cleaner = MoviePyCleaner()
        
        # Executar limpeza
        success = cleaner.clean_all()
        
        # Retornar código de saída
        return 0 if success else 1
    except KeyboardInterrupt:
        color_print("\nLimpeza interrompida pelo usuário", Colors.YELLOW)
        return 1
    except Exception as e:
        color_print(f"\nErro inesperado: {e}", Colors.RED)
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())