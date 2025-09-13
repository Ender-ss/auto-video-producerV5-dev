#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar um relatório completo da documentação e testes do MoviePy

Este script gera um relatório HTML completo com todas as informações sobre
a documentação, testes, exemplos e soluções do MoviePy.
"""

import os
import sys
import json
import time
import datetime
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

class MoviePyReportGenerator:
    """Classe para gerar relatórios do MoviePy"""
    
    def __init__(self):
        self.results = []
        self.start_time = None
        self.project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        self.docs_dir = os.path.join(self.project_dir, "docs", "moviepy")
        self.report_file = os.path.join(self.docs_dir, "RELATORIO_COMPLETO.html")
        self.json_report_file = os.path.join(self.docs_dir, "RELATORIO_COMPLETO.json")
        
        # Seções do relatório
        self.sections = {
            "documentacao": {
                "title": "Documentação",
                "files": [
                    "documentacao/DOCUMENTACAO_COMPLETA.md",
                    "guias/GUIA_REFERENCIA_RAPIDA.md",
                    "guias/SCRIPT_INSTALACAO_CONFIGURACAO.py",
                    "solucoes/SOLUCOES_PROBLEMAS_COMUNS.md"
                ]
            },
            "testes": {
                "title": "Testes",
                "files": [
                    "testes/TESTES_COMPLETOS.md",
                    "testes/SCRIPT_TESTES_COMPLETO.py",
                    "testes/SCRIPT_DIAGNOSTICO_COMPLETO.py"
                ]
            },
            "exemplos": {
                "title": "Exemplos",
                "files": [
                    "exemplos/EXEMPLOS_PRACTICOS.md",
                    "exemplos/SCRIPT_EXEMPLOS_PRACTICOS.py"
                ]
            },
            "scripts": {
                "title": "Scripts",
                "files": [
                    "SCRIPT_RUN_ALL_TESTS.py",
                    "SCRIPT_CLEAN_TEMP_FILES.py"
                ]
            }
        }
        
        # Informações do relatório
        self.report_info = {
            "title": "Relatório Completo do MoviePy",
            "subtitle": "Documentação, Testes, Exemplos e Soluções",
            "version": "2.1.2",
            "date": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "author": "Auto Video Producer V5",
            "description": "Relatório completo da documentação, testes, exemplos e soluções do MoviePy"
        }
    
    def add_result(self, step_name, success, message=""):
        """Adiciona um resultado de passo"""
        self.results.append((step_name, success, message))
        print_result(step_name, success, message)
    
    def generate_report(self):
        """Gera o relatório completo"""
        self.start_time = time.time()
        
        print_header("GERAÇÃO DE RELATÓRIO COMPLETO DO MOVIEPY")
        
        # Verificar ambiente
        self.check_environment()
        
        # Coletar informações dos arquivos
        self.collect_file_info()
        
        # Gerar relatório HTML
        self.generate_html_report()
        
        # Gerar relatório JSON
        self.generate_json_report()
        
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
        
        # Verificar se os arquivos de documentação existem
        for section_name, section_info in self.sections.items():
            for file_path in section_info["files"]:
                full_path = os.path.join(self.docs_dir, file_path)
                if os.path.exists(full_path):
                    self.add_result(f"Arquivo {file_path}", True, "Encontrado")
                else:
                    self.add_result(f"Arquivo {file_path}", False, "Não encontrado")
    
    def collect_file_info(self):
        """Coleta informações sobre os arquivos"""
        print_section("Coletar Informações dos Arquivos")
        
        self.file_info = {}
        
        for section_name, section_info in self.sections.items():
            self.file_info[section_name] = {
                "title": section_info["title"],
                "files": []
            }
            
            for file_path in section_info["files"]:
                full_path = os.path.join(self.docs_dir, file_path)
                
                if os.path.exists(full_path):
                    file_stat = os.stat(full_path)
                    file_info = {
                        "path": file_path,
                        "full_path": full_path,
                        "size": file_stat.st_size,
                        "size_human": self.format_size(file_stat.st_size),
                        "modified": datetime.datetime.fromtimestamp(file_stat.st_mtime).strftime("%d/%m/%Y %H:%M:%S"),
                        "created": datetime.datetime.fromtimestamp(file_stat.st_ctime).strftime("%d/%m/%Y %H:%M:%S"),
                        "extension": os.path.splitext(file_path)[1]
                    }
                    
                    # Se for um arquivo de texto, ler o conteúdo
                    if file_info["extension"] in [".md", ".py", ".txt", ".html"]:
                        try:
                            with open(full_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                file_info["content"] = content
                                file_info["lines"] = len(content.split('\n'))
                        except Exception as e:
                            file_info["error"] = str(e)
                    
                    self.file_info[section_name]["files"].append(file_info)
                    self.add_result(f"Coletar informações de {file_path}", True, f"Tamanho: {file_info['size_human']}")
                else:
                    self.add_result(f"Coletar informações de {file_path}", False, "Arquivo não encontrado")
    
    def generate_html_report(self):
        """Gera o relatório em HTML"""
        print_section("Gerar Relatório HTML")
        
        try:
            # Criar conteúdo HTML
            html_content = self.create_html_content()
            
            # Salvar arquivo HTML
            with open(self.report_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.add_result("Gerar Relatório HTML", True, f"Arquivo salvo: {self.report_file}")
        except Exception as e:
            self.add_result("Gerar Relatório HTML", False, str(e))
    
    def generate_json_report(self):
        """Gera o relatório em JSON"""
        print_section("Gerar Relatório JSON")
        
        try:
            # Preparar dados JSON
            json_data = {
                "info": self.report_info,
                "file_info": self.file_info,
                "results": self.results,
                "generated_at": datetime.datetime.now().isoformat()
            }
            
            # Salvar arquivo JSON
            with open(self.json_report_file, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
            
            self.add_result("Gerar Relatório JSON", True, f"Arquivo salvo: {self.json_report_file}")
        except Exception as e:
            self.add_result("Gerar Relatório JSON", False, str(e))
    
    def create_html_content(self):
        """Cria o conteúdo HTML do relatório"""
        html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.report_info["title"]}</title>
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
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        header {{
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #eee;
        }}
        h1 {{
            color: #333;
            margin-bottom: 10px;
        }}
        h2 {{
            color: #444;
            margin-top: 30px;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid #ddd;
        }}
        h3 {{
            color: #555;
            margin-top: 20px;
            margin-bottom: 10px;
        }}
        .info {{
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .file {{
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .file-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}
        .file-name {{
            font-weight: bold;
            color: #333;
        }}
        .file-meta {{
            font-size: 0.9em;
            color: #666;
        }}
        .file-content {{
            background-color: #f0f0f0;
            padding: 10px;
            border-radius: 3px;
            overflow-x: auto;
            font-family: monospace;
            font-size: 0.9em;
            max-height: 300px;
            overflow-y: auto;
        }}
        pre {{
            margin: 0;
            white-space: pre-wrap;
        }}
        .success {{
            color: #28a745;
        }}
        .error {{
            color: #dc3545;
        }}
        .summary {{
            background-color: #e9f7ef;
            padding: 15px;
            border-radius: 5px;
            margin-top: 30px;
        }}
        .toc {{
            background-color: #f0f8ff;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 30px;
        }}
        .toc ul {{
            margin: 0;
            padding-left: 20px;
        }}
        .toc a {{
            color: #0066cc;
            text-decoration: none;
        }}
        .toc a:hover {{
            text-decoration: underline;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            color: #666;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{self.report_info["title"]}</h1>
            <p>{self.report_info["subtitle"]}</p>
            <div class="info">
                <p><strong>Versão:</strong> {self.report_info["version"]}</p>
                <p><strong>Data:</strong> {self.report_info["date"]}</p>
                <p><strong>Autor:</strong> {self.report_info["author"]}</p>
                <p><strong>Descrição:</strong> {self.report_info["description"]}</p>
            </div>
        </header>
        
        <div class="toc">
            <h2>Índice</h2>
            <ul>
"""
        
        # Adicionar índice
        for section_name, section_info in self.file_info.items():
            html += f'                <li><a href="#{section_name}">{section_info["title"]}</a></li>\n'
        
        html += """            </ul>
        </div>
"""
        
        # Adicionar seções
        for section_name, section_info in self.file_info.items():
            html += f'        <section id="{section_name}">\n'
            html += f'            <h2>{section_info["title"]}</h2>\n'
            
            for file_info in section_info["files"]:
                html += '            <div class="file">\n'
                html += '                <div class="file-header">\n'
                html += f'                    <div class="file-name">{file_info["path"]}</div>\n'
                html += '                    <div class="file-meta">\n'
                html += f'                        <span>Tamanho: {file_info["size_human"]}</span> | \n'
                html += f'                        <span>Modificado: {file_info["modified"]}</span> | \n'
                html += f'                        <span>Linhas: {file_info.get("lines", "N/A")}</span>\n'
                html += '                    </div>\n'
                html += '                </div>\n'
                
                if "content" in file_info:
                    html += '                <div class="file-content">\n'
                    html += f'                    <pre>{self.escape_html(file_info["content"][:2000])}'
                    if len(file_info["content"]) > 2000:
                        html += '\n... (conteúdo truncado)'
                    html += '</pre>\n'
                    html += '                </div>\n'
                elif "error" in file_info:
                    html += f'                <div class="error">Erro ao ler conteúdo: {file_info["error"]}</div>\n'
                
                html += '            </div>\n'
            
            html += '        </section>\n'
        
        # Adicionar resumo
        total_files = sum(len(section_info["files"]) for section_info in self.file_info.values())
        total_size = sum(file_info["size"] for section_info in self.file_info.values() for file_info in section_info["files"])
        
        html += f"""
        <div class="summary">
            <h2>Resumo</h2>
            <p><strong>Total de arquivos:</strong> {total_files}</p>
            <p><strong>Tamanho total:</strong> {self.format_size(total_size)}</p>
            <p><strong>Data de geração:</strong> {datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</p>
        </div>
        
        <div class="footer">
            <p>Relatório gerado automaticamente pelo Auto Video Producer V5</p>
        </div>
    </div>
</body>
</html>
"""
        
        return html
    
    def escape_html(self, text):
        """Escapa caracteres HTML"""
        return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')
    
    def format_size(self, size_bytes):
        """Formata tamanho em bytes para formato legível"""
        if size_bytes == 0:
            return "0B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.2f} {size_names[i]}"
    
    def print_summary(self):
        """Imprime um resumo do relatório"""
        print_section("Resumo do Relatório")
        
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
            color_print("\n✓ Relatório gerado com sucesso!", Colors.GREEN)
            color_print(f"Arquivo HTML: {self.report_file}", Colors.WHITE)
            color_print(f"Arquivo JSON: {self.json_report_file}", Colors.WHITE)
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
        
        color_print("1. Abra o relatório HTML no navegador:", Colors.WHITE)
        color_print(f"   {self.report_file}", Colors.CYAN)
        
        color_print("\n2. Execute os testes:", Colors.WHITE)
        color_print(f"   python {os.path.join(self.project_dir, 'docs', 'moviepy', 'SCRIPT_RUN_ALL_TESTS.py')}", Colors.CYAN)
        
        color_print("\n3. Limpe os arquivos temporários:", Colors.WHITE)
        color_print(f"   python {os.path.join(self.project_dir, 'docs', 'moviepy', 'SCRIPT_CLEAN_TEMP_FILES.py')}", Colors.CYAN)
        
        color_print("\n4. Verifique a documentação:", Colors.WHITE)
        color_print(f"   Leia {os.path.join(self.project_dir, 'docs', 'moviepy', 'README.md')} para mais informações", Colors.CYAN)

def main():
    """Função principal"""
    try:
        # Criar gerador de relatório
        generator = MoviePyReportGenerator()
        
        # Gerar relatório
        success = generator.generate_report()
        
        # Retornar código de saída
        return 0 if success else 1
    except KeyboardInterrupt:
        color_print("\nGeração de relatório interrompida pelo usuário", Colors.YELLOW)
        return 1
    except Exception as e:
        color_print(f"\nErro inesperado: {e}", Colors.RED)
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())