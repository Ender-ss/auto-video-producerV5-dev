#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script principal para executar todas as ferramentas de documentação e testes do MoviePy

Este script executa todos os scripts de documentação, testes, exemplos e utilitários
do MoviePy em sequência.
"""

import os
import sys
import subprocess
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

class MoviePyDocumentationManager:
    """Classe para gerenciar a documentação e testes do MoviePy"""
    
    def __init__(self):
        self.results = []
        self.start_time = None
        self.project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        self.docs_dir = os.path.join(self.project_dir, "docs", "moviepy")
        self.python_executable = sys.executable
        
        # Lista de scripts para executar
        self.scripts = [
            {
                "name": "Instalação e Configuração",
                "path": "guias/SCRIPT_INSTALACAO_CONFIGURACAO.py",
                "description": "Instala e configura o MoviePy e suas dependências"
            },
            {
                "name": "Diagnóstico Completo",
                "path": "testes/SCRIPT_DIAGNOSTICO_COMPLETO.py",
                "description": "Executa um diagnóstico completo do ambiente MoviePy"
            },
            {
                "name": "Testes Completos",
                "path": "testes/SCRIPT_TESTES_COMPLETO.py",
                "description": "Executa todos os testes do MoviePy"
            },
            {
                "name": "Exemplos Práticos",
                "path": "exemplos/SCRIPT_EXEMPLOS_PRACTICOS.py",
                "description": "Executa exemplos práticos do MoviePy"
            },
            {
                "name": "Executar Todos os Testes",
                "path": "SCRIPT_RUN_ALL_TESTS.py",
                "description": "Executa todos os testes e exemplos em sequência"
            },
            {
                "name": "Gerar Relatório",
                "path": "SCRIPT_GERAR_RELATORIO.py",
                "description": "Gera um relatório completo da documentação e testes"
            }
        ]
        
        # Opções de execução
        self.options = {
            "install": False,
            "diagnose": False,
            "test": False,
            "examples": False,
            "all": False,
            "report": False,
            "clean": False,
            "update": False
        }
    
    def add_result(self, step_name, success, message=""):
        """Adiciona um resultado de passo"""
        self.results.append((step_name, success, message))
        print_result(step_name, success, message)
    
    def parse_arguments(self):
        """Analisa os argumentos da linha de comando"""
        if len(sys.argv) > 1:
            for arg in sys.argv[1:]:
                if arg == "--install":
                    self.options["install"] = True
                elif arg == "--diagnose":
                    self.options["diagnose"] = True
                elif arg == "--test":
                    self.options["test"] = True
                elif arg == "--examples":
                    self.options["examples"] = True
                elif arg == "--all":
                    self.options["all"] = True
                elif arg == "--report":
                    self.options["report"] = True
                elif arg == "--clean":
                    self.options["clean"] = True
                elif arg == "--update":
                    self.options["update"] = True
                elif arg == "--help" or arg == "-h":
                    self.print_help()
                    sys.exit(0)
                else:
                    color_print(f"Opção desconhecida: {arg}", Colors.RED)
                    self.print_help()
                    sys.exit(1)
        else:
            # Se nenhum argumento for fornecido, executar tudo
            self.options["all"] = True
    
    def print_help(self):
        """Imprime a ajuda"""
        print_header("Ajuda do MoviePy Documentation Manager")
        
        color_print("Uso:", Colors.WHITE)
        color_print(f"  python {os.path.basename(__file__)} [opções]", Colors.CYAN)
        
        color_print("\nOpções:", Colors.WHITE)
        color_print("  --install     Executa o script de instalação e configuração", Colors.CYAN)
        color_print("  --diagnose    Executa o script de diagnóstico", Colors.CYAN)
        color_print("  --test        Executa os testes do MoviePy", Colors.CYAN)
        color_print("  --examples    Executa os exemplos do MoviePy", Colors.CYAN)
        color_print("  --all         Executa todos os scripts (padrão)", Colors.CYAN)
        color_print("  --report      Gera um relatório completo", Colors.CYAN)
        color_print("  --clean       Limpa arquivos temporários", Colors.CYAN)
        color_print("  --update      Atualiza a documentação", Colors.CYAN)
        color_print("  --help, -h    Mostra esta ajuda", Colors.CYAN)
        
        color_print("\nExemplos:", Colors.WHITE)
        color_print(f"  python {os.path.basename(__file__)} --all", Colors.CYAN)
        color_print(f"  python {os.path.basename(__file__)} --test --examples", Colors.CYAN)
        color_print(f"  python {os.path.basename(__file__)} --clean --report", Colors.CYAN)
    
    def run_all(self):
        """Executa todos os scripts conforme as opções"""
        self.start_time = time.time()
        
        print_header("MOVIEPY DOCUMENTATION MANAGER")
        
        # Analisar argumentos
        self.parse_arguments()
        
        # Verificar ambiente
        self.check_environment()
        
        # Executar scripts conforme as opções
        if self.options["install"] or self.options["all"]:
            self.run_script("Instalação e Configuração", "guias/SCRIPT_INSTALACAO_CONFIGURACAO.py")
        
        if self.options["diagnose"] or self.options["all"]:
            self.run_script("Diagnóstico Completo", "testes/SCRIPT_DIAGNOSTICO_COMPLETO.py")
        
        if self.options["test"] or self.options["all"]:
            self.run_script("Testes Completos", "testes/SCRIPT_TESTES_COMPLETO.py")
        
        if self.options["examples"] or self.options["all"]:
            self.run_script("Exemplos Práticos", "exemplos/SCRIPT_EXEMPLOS_PRACTICOS.py")
        
        if self.options["all"]:
            self.run_script("Executar Todos os Testes", "SCRIPT_RUN_ALL_TESTS.py")
        
        if self.options["report"] or self.options["all"]:
            self.run_script("Gerar Relatório", "SCRIPT_GERAR_RELATORIO.py")
        
        if self.options["clean"]:
            self.run_script("Limpar Arquivos Temporários", "SCRIPT_CLEAN_TEMP_FILES.py")
        
        if self.options["update"]:
            self.run_script("Atualizar Documentação", "SCRIPT_ATUALIZAR_DOCUMENTACAO.py")
        
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
    
    def run_script(self, script_name, script_path):
        """Executa um script específico"""
        print_section(f"Executar {script_name}")
        
        full_path = os.path.join(self.docs_dir, script_path)
        
        if not os.path.exists(full_path):
            self.add_result(f"Executar {script_name}", False, f"Arquivo não encontrado: {full_path}")
            return
        
        try:
            # Executar o script
            result = subprocess.run([self.python_executable, full_path], 
                                  cwd=self.docs_dir, 
                                  capture_output=True, 
                                  text=True)
            
            # Verificar resultado
            if result.returncode == 0:
                self.add_result(f"Executar {script_name}", True, "Script executado com sucesso")
                
                # Imprimir saída se não for muito longa
                if result.stdout:
                    lines = result.stdout.split('\n')
                    if len(lines) <= 20:
                        color_print("Saída do script:", Colors.YELLOW)
                        color_print(result.stdout, Colors.WHITE)
                    else:
                        color_print("Saída do script (primeiras 20 linhas):", Colors.YELLOW)
                        color_print('\n'.join(lines[:20]), Colors.WHITE)
                        color_print(f"... ({len(lines) - 20} linhas restantes)", Colors.YELLOW)
            else:
                self.add_result(f"Executar {script_name}", False, f"Erro ao executar script (código: {result.returncode})")
                
                # Imprimir erro
                if result.stderr:
                    color_print("Erro do script:", Colors.RED)
                    color_print(result.stderr, Colors.RED)
                
                if result.stdout:
                    color_print("Saída do script:", Colors.YELLOW)
                    color_print(result.stdout, Colors.YELLOW)
        except Exception as e:
            self.add_result(f"Executar {script_name}", False, str(e))
    
    def print_summary(self):
        """Imprime um resumo da execução"""
        print_section("Resumo da Execução")
        
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
            color_print("\n✓ Execução concluída com sucesso!", Colors.GREEN)
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
        
        color_print("1. Verifique os relatórios gerados:", Colors.WHITE)
        color_print(f"   - {os.path.join(self.docs_dir, 'RELATORIO_COMPLETO.html')}", Colors.CYAN)
        color_print(f"   - {os.path.join(self.docs_dir, 'RELATORIO_COMPLETO.json')}", Colors.CYAN)
        
        color_print("\n2. Verifique a documentação:", Colors.WHITE)
        color_print(f"   - {os.path.join(self.docs_dir, 'README.md')}", Colors.CYAN)
        
        color_print("\n3. Execute scripts individuais:", Colors.WHITE)
        color_print(f"   python {os.path.join(self.docs_dir, 'SCRIPT_RUN_ALL_TESTS.py')}", Colors.CYAN)
        color_print(f"   python {os.path.join(self.docs_dir, 'SCRIPT_GERAR_RELATORIO.py')}", Colors.CYAN)
        color_print(f"   python {os.path.join(self.docs_dir, 'SCRIPT_CLEAN_TEMP_FILES.py')}", Colors.CYAN)
        
        color_print("\n4. Para ajuda:", Colors.WHITE)
        color_print(f"   python {os.path.join(self.docs_dir, os.path.basename(__file__))} --help", Colors.CYAN)

def main():
    """Função principal"""
    try:
        # Criar gerenciador
        manager = MoviePyDocumentationManager()
        
        # Executar todos os scripts
        success = manager.run_all()
        
        # Retornar código de saída
        return 0 if success else 1
    except KeyboardInterrupt:
        color_print("\nExecução interrompida pelo usuário", Colors.YELLOW)
        return 1
    except Exception as e:
        color_print(f"\nErro inesperado: {e}", Colors.RED)
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())