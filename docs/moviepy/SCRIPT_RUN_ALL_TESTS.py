#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para executar todos os testes e exemplos do MoviePy

Este script executa todos os testes e exemplos do MoviePy,
gerando um relatório completo dos resultados.
"""

import os
import sys
import subprocess
import time
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

def print_result(step_name, success, message=""):
    """Imprime um resultado de passo"""
    if success:
        color_print(f"✓ {step_name}: SUCESSO", Colors.GREEN)
    else:
        color_print(f"✗ {step_name}: FALHA", Colors.RED)
    
    if message:
        print(f"  {message}")
    
    print()

class MoviePyTestRunner:
    """Classe para executar testes e exemplos do MoviePy"""
    
    def __init__(self):
        self.results = []
        self.start_time = None
        self.project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
        self.docs_dir = os.path.join(self.project_dir, "docs", "moviepy")
        self.temp_dir = os.path.join(self.project_dir, "temp")
        self.python_executable = sys.executable
        self.report_file = os.path.join(self.temp_dir, "moviepy_test_report.html")
        
        # Garantir que o diretório temporário existe
        os.makedirs(self.temp_dir, exist_ok=True)
    
    def add_result(self, step_name, success, message="", output=""):
        """Adiciona um resultado de passo"""
        self.results.append({
            "step_name": step_name,
            "success": success,
            "message": message,
            "output": output,
            "timestamp": time.time()
        })
        print_result(step_name, success, message)
    
    def run_all_tests(self):
        """Executa todos os testes e exemplos"""
        self.start_time = time.time()
        
        print_header("EXECUÇÃO COMPLETA DE TESTES E EXEMPLOS DO MOVIEPY")
        
        # Verificar ambiente
        self.check_environment()
        
        # Executar diagnóstico
        self.run_diagnostic()
        
        # Executar testes
        self.run_tests()
        
        # Executar exemplos
        self.run_examples()
        
        # Gerar relatório
        self.generate_report()
        
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
        
        # Verificar scripts
        scripts_to_check = [
            ("Script de Diagnóstico", os.path.join(self.docs_dir, "testes", "SCRIPT_DIAGNOSTICO_COMPLETO.py")),
            ("Script de Testes", os.path.join(self.docs_dir, "testes", "SCRIPT_TESTES_COMPLETO.py")),
            ("Script de Exemplos", os.path.join(self.docs_dir, "exemplos", "SCRIPT_EXEMPLOS_PRACTICOS.py"))
        ]
        
        for script_name, script_path in scripts_to_check:
            if os.path.exists(script_path):
                self.add_result(script_name, True, script_path)
            else:
                self.add_result(script_name, False, f"Não encontrado: {script_path}")
        
        # Verificar MoviePy
        try:
            import moviepy
            self.add_result("MoviePy", True, f"Versão: {moviepy.__version__}")
        except ImportError:
            self.add_result("MoviePy", False, "MoviePy não está instalado")
    
    def run_diagnostic(self):
        """Executa o diagnóstico completo"""
        print_section("Executar Diagnóstico")
        
        script_path = os.path.join(self.docs_dir, "testes", "SCRIPT_DIAGNOSTICO_COMPLETO.py")
        
        if not os.path.exists(script_path):
            self.add_result("Executar Diagnóstico", False, f"Script não encontrado: {script_path}")
            return
        
        try:
            # Executar script de diagnóstico
            result = subprocess.run([self.python_executable, script_path], capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                self.add_result("Executar Diagnóstico", True, "Diagnóstico concluído com sucesso", result.stdout)
            else:
                self.add_result("Executar Diagnóstico", False, f"Erro na execução: {result.stderr}", result.stdout)
        except subprocess.TimeoutExpired:
            self.add_result("Executar Diagnóstico", False, "Timeout: O diagnóstico demorou muito tempo")
        except Exception as e:
            self.add_result("Executar Diagnóstico", False, str(e))
    
    def run_tests(self):
        """Executa os testes completos"""
        print_section("Executar Testes")
        
        script_path = os.path.join(self.docs_dir, "testes", "SCRIPT_TESTES_COMPLETO.py")
        
        if not os.path.exists(script_path):
            self.add_result("Executar Testes", False, f"Script não encontrado: {script_path}")
            return
        
        try:
            # Executar script de testes
            result = subprocess.run([self.python_executable, script_path], capture_output=True, text=True, timeout=600)
            
            if result.returncode == 0:
                self.add_result("Executar Testes", True, "Testes concluídos com sucesso", result.stdout)
            else:
                self.add_result("Executar Testes", False, f"Erro na execução: {result.stderr}", result.stdout)
        except subprocess.TimeoutExpired:
            self.add_result("Executar Testes", False, "Timeout: Os testes demoraram muito tempo")
        except Exception as e:
            self.add_result("Executar Testes", False, str(e))
    
    def run_examples(self):
        """Executa os exemplos práticos"""
        print_section("Executar Exemplos")
        
        script_path = os.path.join(self.docs_dir, "exemplos", "SCRIPT_EXEMPLOS_PRACTICOS.py")
        
        if not os.path.exists(script_path):
            self.add_result("Executar Exemplos", False, f"Script não encontrado: {script_path}")
            return
        
        try:
            # Executar script de exemplos
            result = subprocess.run([self.python_executable, script_path], capture_output=True, text=True, timeout=600)
            
            if result.returncode == 0:
                self.add_result("Executar Exemplos", True, "Exemplos concluídos com sucesso", result.stdout)
            else:
                self.add_result("Executar Exemplos", False, f"Erro na execução: {result.stderr}", result.stdout)
        except subprocess.TimeoutExpired:
            self.add_result("Executar Exemplos", False, "Timeout: Os exemplos demoraram muito tempo")
        except Exception as e:
            self.add_result("Executar Exemplos", False, str(e))
    
    def generate_report(self):
        """Gera um relatório HTML completo"""
        print_section("Gerar Relatório")
        
        try:
            # Criar conteúdo HTML
            html_content = self.generate_html_report()
            
            # Escrever arquivo HTML
            with open(self.report_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.add_result("Gerar Relatório", True, f"Relatório gerado: {self.report_file}")
        except Exception as e:
            self.add_result("Gerar Relatório", False, str(e))
    
    def generate_html_report(self):
        """Gera o conteúdo HTML do relatório"""
        # Calcular estatísticas
        total_steps = len(self.results)
        successful_steps = sum(1 for r in self.results if r["success"])
        failed_steps = total_steps - successful_steps
        
        # Início do HTML
        html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Testes e Exemplos do MoviePy</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        h1, h2, h3 {{
            color: #333;
        }}
        h1 {{
            text-align: center;
            border-bottom: 2px solid #007bff;
            padding-bottom: 10px;
        }}
        .stats {{
            display: flex;
            justify-content: space-around;
            margin: 20px 0;
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
        }}
        .stat {{
            text-align: center;
        }}
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
        }}
        .success {{
            color: #28a745;
        }}
        .failure {{
            color: #dc3545;
        }}
        .results {{
            margin-top: 30px;
        }}
        .result {{
            margin-bottom: 15px;
            padding: 15px;
            border-radius: 5px;
            border-left: 5px solid;
        }}
        .result.success {{
            background-color: #d4edda;
            border-color: #28a745;
        }}
        .result.failure {{
            background-color: #f8d7da;
            border-color: #dc3545;
        }}
        .result-name {{
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .result-message {{
            margin-bottom: 10px;
        }}
        .result-output {{
            background-color: #f8f9fa;
            padding: 10px;
            border-radius: 5px;
            font-family: monospace;
            white-space: pre-wrap;
            max-height: 200px;
            overflow-y: auto;
        }}
        .timestamp {{
            font-size: 0.8em;
            color: #6c757d;
            text-align: right;
        }}
        .footer {{
            margin-top: 30px;
            text-align: center;
            color: #6c757d;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Relatório de Testes e Exemplos do MoviePy</h1>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-value">{total_steps}</div>
                <div>Total de Passos</div>
            </div>
            <div class="stat">
                <div class="stat-value success">{successful_steps}</div>
                <div>Sucessos</div>
            </div>
            <div class="stat">
                <div class="stat-value failure">{failed_steps}</div>
                <div>Falhas</div>
            </div>
            <div class="stat">
                <div class="stat-value">{(successful_steps/total_steps*100):.1f}%</div>
                <div>Taxa de Sucesso</div>
            </div>
        </div>
        
        <div class="results">
            <h2>Resultados Detalhados</h2>
"""
        
        # Adicionar resultados
        for result in self.results:
            status_class = "success" if result["success"] else "failure"
            status_text = "SUCESSO" if result["success"] else "FALHA"
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(result["timestamp"]))
            
            html += f"""
            <div class="result {status_class}">
                <div class="result-name">{result["step_name"]}: {status_text}</div>
                <div class="result-message">{result["message"]}</div>
"""
            
            if result["output"]:
                html += f"""
                <div class="result-output">{result["output"]}</div>
"""
            
            html += f"""
                <div class="timestamp">{timestamp}</div>
            </div>
"""
        
        # Final do HTML
        html += f"""
        </div>
        
        <div class="footer">
            <p>Relatório gerado em {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>Tempo total de execução: {time.time() - self.start_time:.2f} segundos</p>
            <p>Projeto: auto-video-producerV5-dev</p>
        </div>
    </div>
</body>
</html>
"""
        
        return html
    
    def print_summary(self):
        """Imprime um resumo da execução"""
        print_section("Resumo da Execução")
        
        # Calcular estatísticas
        total_steps = len(self.results)
        successful_steps = sum(1 for r in self.results if r["success"])
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
            color_print("\n✓ Todos os testes e exemplos foram executados com sucesso!", Colors.GREEN)
        else:
            color_print(f"\n✗ {failed_steps} passo(s) falharam!", Colors.RED)
            
            # Listar passos falhos
            color_print("\nPassos falhos:", Colors.RED)
            for result in self.results:
                if not result["success"]:
                    color_print(f"- {result['step_name']}: {result['message']}", Colors.RED)
        
        # Informações do relatório
        color_print(f"\nRelatório HTML gerado: {self.report_file}", Colors.CYAN)
        color_print("Abra o arquivo HTML no navegador para ver o relatório completo.", Colors.CYAN)
        
        # Próximos passos
        self.print_next_steps()
    
    def print_next_steps(self):
        """Imprime os próximos passos"""
        print_section("Próximos Passos")
        
        color_print("1. Verifique o relatório HTML para detalhes:", Colors.WHITE)
        color_print(f"   Abra {self.report_file} no navegador", Colors.CYAN)
        
        color_print("\n2. Execute scripts individuais se necessário:", Colors.WHITE)
        color_print(f"   Diagnóstico: python {os.path.join(self.docs_dir, 'testes', 'SCRIPT_DIAGNOSTICO_COMPLETO.py')}", Colors.CYAN)
        color_print(f"   Testes: python {os.path.join(self.docs_dir, 'testes', 'SCRIPT_TESTES_COMPLETO.py')}", Colors.CYAN)
        color_print(f"   Exemplos: python {os.path.join(self.docs_dir, 'exemplos', 'SCRIPT_EXEMPLOS_PRACTICOS.py')}", Colors.CYAN)
        
        color_print("\n3. Consulte a documentação:", Colors.WHITE)
        color_print(f"   Leia {os.path.join(self.docs_dir, 'README.md')} para mais informações", Colors.CYAN)
        
        color_print("\n4. Verifique os arquivos gerados:", Colors.WHITE)
        color_print(f"   Arquivos temporários: {self.temp_dir}", Colors.CYAN)

def main():
    """Função principal"""
    try:
        # Criar executor de testes
        runner = MoviePyTestRunner()
        
        # Executar todos os testes
        success = runner.run_all_tests()
        
        # Retornar código de saída
        return 0 if success else 1
    except KeyboardInterrupt:
        color_print("\nExecução interrompida pelo usuário", Colors.YELLOW)
        return 1
    except Exception as e:
        color_print(f"\nErro inesperado: {e}", Colors.RED)
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())