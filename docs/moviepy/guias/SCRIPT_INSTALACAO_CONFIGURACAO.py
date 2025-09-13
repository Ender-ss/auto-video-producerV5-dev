#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de instalação e configuração do MoviePy para o projeto auto-video-producerV5-dev

Este script instala e configura o MoviePy 2.1.2 e suas dependências,
verificando a compatibilidade com o sistema e o projeto.
"""

import os
import sys
import subprocess
import platform
import tempfile
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

class MoviePyInstaller:
    """Classe para instalação e configuração do MoviePy"""
    
    def __init__(self):
        self.results = []
        self.start_time = None
        self.temp_dir = tempfile.mkdtemp()
        self.python_version = sys.version
        self.os_info = platform.platform()
        self.project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
        self.requirements_file = os.path.join(self.project_dir, "requirements.txt")
        self.virtual_env = None
        self.moviepy_version = "2.1.2"
    
    def add_result(self, step_name, success, message=""):
        """Adiciona um resultado de passo"""
        self.results.append((step_name, success, message))
        print_result(step_name, success, message)
    
    def run_installation(self):
        """Executa a instalação completa"""
        self.start_time = time.time()
        
        print_header("INSTALAÇÃO E CONFIGURAÇÃO DO MOVIEPY")
        
        # Informações do sistema
        self.check_system_info()
        
        # Verificar ambiente Python
        self.check_python_environment()
        
        # Verificar ambiente virtual
        self.check_virtual_environment()
        
        # Criar ambiente virtual (se necessário)
        self.create_virtual_environment()
        
        # Ativar ambiente virtual
        self.activate_virtual_environment()
        
        # Atualizar pip
        self.update_pip()
        
        # Instalar dependências básicas
        self.install_basic_dependencies()
        
        # Instalar FFmpeg
        self.install_ffmpeg()
        
        # Instalar MoviePy
        self.install_moviepy()
        
        # Verificar instalação
        self.verify_installation()
        
        # Configurar MoviePy
        self.configure_moviepy()
        
        # Testar instalação
        self.test_installation()
        
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
        color_print(f"Diretório do projeto: {self.project_dir}", Colors.WHITE)
        
        # Verificar se requirements.txt existe
        if os.path.exists(self.requirements_file):
            color_print(f"Arquivo requirements.txt encontrado: {self.requirements_file}", Colors.GREEN)
        else:
            color_print(f"Arquivo requirements.txt não encontrado: {self.requirements_file}", Colors.YELLOW)
        
        print()
    
    def check_python_environment(self):
        """Verifica o ambiente Python"""
        print_section("Ambiente Python")
        
        # Verificar versão do Python
        python_version = sys.version_info
        if python_version.major >= 3 and python_version.minor >= 6:
            self.add_result("Versão do Python", True, f"Python {python_version.major}.{python_version.minor}.{python_version.micro}")
        else:
            self.add_result("Versão do Python", False, f"Python {python_version.major}.{python_version.minor}.{python_version.micro} (requerido: 3.6+)")
        
        # Verificar pip
        try:
            result = subprocess.run([sys.executable, "-m", "pip", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                pip_version = result.stdout.strip()
                self.add_result("Pip", True, pip_version)
            else:
                self.add_result("Pip", False, "Pip não está disponível")
        except Exception as e:
            self.add_result("Pip", False, str(e))
        
        # Verificar ambiente virtual
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            self.add_result("Ambiente Virtual", True, "Já está em um ambiente virtual")
        else:
            self.add_result("Ambiente Virtual", False, "Não está em um ambiente virtual")
    
    def check_virtual_environment(self):
        """Verifica se há um ambiente virtual existente"""
        print_section("Verificar Ambiente Virtual")
        
        # Verificar se há um ambiente virtual no diretório do projeto
        venv_dirs = [
            os.path.join(self.project_dir, "venv"),
            os.path.join(self.project_dir, "env"),
            os.path.join(self.project_dir, ".venv")
        ]
        
        for venv_dir in venv_dirs:
            if os.path.exists(venv_dir):
                self.virtual_env = venv_dir
                self.add_result("Ambiente Virtual Existente", True, f"Encontrado em: {venv_dir}")
                return
        
        self.add_result("Ambiente Virtual Existente", False, "Nenhum ambiente virtual encontrado")
    
    def create_virtual_environment(self):
        """Cria um ambiente virtual"""
        print_section("Criar Ambiente Virtual")
        
        if self.virtual_env:
            color_print("Ambiente virtual já existe, pulando criação", Colors.YELLOW)
            return
        
        try:
            # Criar ambiente virtual
            venv_path = os.path.join(self.project_dir, "venv")
            result = subprocess.run([sys.executable, "-m", "venv", venv_path], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.virtual_env = venv_path
                self.add_result("Criar Ambiente Virtual", True, f"Criado em: {venv_path}")
            else:
                self.add_result("Criar Ambiente Virtual", False, result.stderr)
        except Exception as e:
            self.add_result("Criar Ambiente Virtual", False, str(e))
    
    def activate_virtual_environment(self):
        """Ativa o ambiente virtual"""
        print_section("Ativar Ambiente Virtual")
        
        if not self.virtual_env:
            self.add_result("Ativar Ambiente Virtual", False, "Nenhum ambiente virtual disponível")
            return
        
        # Determinar o executável Python do ambiente virtual
        if platform.system() == "Windows":
            python_executable = os.path.join(self.virtual_env, "Scripts", "python.exe")
        else:
            python_executable = os.path.join(self.virtual_env, "bin", "python")
        
        if os.path.exists(python_executable):
            self.add_result("Ativar Ambiente Virtual", True, f"Executável: {python_executable}")
            # Atualizar o executável Python para uso futuro
            self.python_executable = python_executable
        else:
            self.add_result("Ativar Ambiente Virtual", False, f"Executável não encontrado: {python_executable}")
    
    def update_pip(self):
        """Atualiza o pip"""
        print_section("Atualizar Pip")
        
        if not hasattr(self, 'python_executable'):
            self.add_result("Atualizar Pip", False, "Ambiente virtual não ativado")
            return
        
        try:
            result = subprocess.run([self.python_executable, "-m", "pip", "install", "--upgrade", "pip"], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.add_result("Atualizar Pip", True)
            else:
                self.add_result("Atualizar Pip", False, result.stderr)
        except Exception as e:
            self.add_result("Atualizar Pip", False, str(e))
    
    def install_basic_dependencies(self):
        """Instala dependências básicas"""
        print_section("Instalar Dependências Básicas")
        
        if not hasattr(self, 'python_executable'):
            self.add_result("Instalar Dependências Básicas", False, "Ambiente virtual não ativado")
            return
        
        # Lista de dependências básicas
        dependencies = [
            "numpy",
            "Pillow",
            "imageio",
            "imageio-ffmpeg",
            "decorator",
            "proglog",
            "tqdm"
        ]
        
        for dep in dependencies:
            try:
                result = subprocess.run([self.python_executable, "-m", "pip", "install", dep], capture_output=True, text=True)
                
                if result.returncode == 0:
                    self.add_result(f"Instalar {dep}", True)
                else:
                    self.add_result(f"Instalar {dep}", False, result.stderr)
            except Exception as e:
                self.add_result(f"Instalar {dep}", False, str(e))
    
    def install_ffmpeg(self):
        """Instala o FFmpeg"""
        print_section("Instalar FFmpeg")
        
        # Verificar se FFmpeg já está instalado
        try:
            result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
            if result.returncode == 0:
                ffmpeg_version = result.stdout.split('\n')[0]
                self.add_result("FFmpeg", True, f"Já instalado: {ffmpeg_version}")
                return
        except FileNotFoundError:
            pass
        
        # Instalar FFmpeg via pip (imageio-ffmpeg)
        if hasattr(self, 'python_executable'):
            try:
                result = subprocess.run([self.python_executable, "-m", "pip", "install", "imageio-ffmpeg"], capture_output=True, text=True)
                
                if result.returncode == 0:
                    self.add_result("FFmpeg (via pip)", True)
                else:
                    self.add_result("FFmpeg (via pip)", False, result.stderr)
            except Exception as e:
                self.add_result("FFmpeg (via pip)", False, str(e))
        else:
            self.add_result("FFmpeg", False, "Ambiente virtual não ativado")
        
        # Recomendar instalação manual
        color_print("Recomendação: Instale o FFmpeg manualmente para melhor compatibilidade", Colors.YELLOW)
        color_print("Windows: Baixe de https://ffmpeg.org/download.html", Colors.YELLOW)
        color_print("Linux: sudo apt-get install ffmpeg", Colors.YELLOW)
        color_print("macOS: brew install ffmpeg", Colors.YELLOW)
    
    def install_moviepy(self):
        """Instala o MoviePy"""
        print_section("Instalar MoviePy")
        
        if not hasattr(self, 'python_executable'):
            self.add_result("Instalar MoviePy", False, "Ambiente virtual não ativado")
            return
        
        try:
            # Instalar MoviePy 2.1.2
            result = subprocess.run([self.python_executable, "-m", "pip", "install", f"moviepy=={self.moviepy_version}"], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.add_result("Instalar MoviePy", True, f"Versão {self.moviepy_version}")
            else:
                self.add_result("Instalar MoviePy", False, result.stderr)
        except Exception as e:
            self.add_result("Instalar MoviePy", False, str(e))
    
    def verify_installation(self):
        """Verifica a instalação do MoviePy"""
        print_section("Verificar Instalação")
        
        if not hasattr(self, 'python_executable'):
            self.add_result("Verificar Instalação", False, "Ambiente virtual não ativado")
            return
        
        try:
            # Verificar se MoviePy foi instalado
            result = subprocess.run([self.python_executable, "-c", "import moviepy; print(moviepy.__version__)"], capture_output=True, text=True)
            
            if result.returncode == 0:
                installed_version = result.stdout.strip()
                if installed_version == self.moviepy_version:
                    self.add_result("Verificar Versão do MoviePy", True, f"Versão {installed_version}")
                else:
                    self.add_result("Verificar Versão do MoviePy", False, f"Versão instalada: {installed_version}, esperada: {self.moviepy_version}")
            else:
                self.add_result("Verificar Versão do MoviePy", False, result.stderr)
        except Exception as e:
            self.add_result("Verificar Versão do MoviePy", False, str(e))
        
        # Verificar módulos principais
        modules_to_check = [
            "moviepy.editor",
            "moviepy.audio.io.AudioFileClip",
            "moviepy.video.io.VideoFileClip",
            "moviepy.video.compositing.CompositeVideoClip",
            "moviepy.video.fx",
            "moviepy.audio.fx"
        ]
        
        for module_name in modules_to_check:
            try:
                result = subprocess.run([self.python_executable, "-c", f"import {module_name}"], capture_output=True, text=True)
                
                if result.returncode == 0:
                    self.add_result(f"Módulo {module_name}", True)
                else:
                    self.add_result(f"Módulo {module_name}", False, result.stderr)
            except Exception as e:
                self.add_result(f"Módulo {module_name}", False, str(e))
    
    def configure_moviepy(self):
        """Configura o MoviePy"""
        print_section("Configurar MoviePy")
        
        # Criar arquivo de configuração
        try:
            config_dir = os.path.join(self.project_dir, "config")
            os.makedirs(config_dir, exist_ok=True)
            
            config_file = os.path.join(config_dir, "moviepy_config.py")
            
            with open(config_file, 'w', encoding='utf-8') as f:
                f.write("# Configuração do MoviePy\n")
                f.write(f"# Versão: {self.moviepy_version}\n")
                f.write(f"# Data: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                # Configurações de FFmpeg
                f.write("# Configurações de FFmpeg\n")
                f.write("import os\n")
                f.write("from moviepy.config import get_setting\n")
                f.write("\n")
                f.write("# Definir caminho do FFmpeg (se necessário)\n")
                f.write("# FFMPEG_BINARY = '/caminho/para/ffmpeg'\n")
                f.write("# if FFMPEG_BINARY:\n")
                f.write("#     os.environ['FFMPEG_BINARY'] = FFMPEG_BINARY\n")
                f.write("\n")
                
                # Configurações de cache
                f.write("# Configurações de cache\n")
                f.write("TEMP_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'temp')\n")
                f.write("os.makedirs(TEMP_DIR, exist_ok=True)\n")
                f.write("\n")
                
                # Configurações de log
                f.write("# Configurações de log\n")
                f.write("import logging\n")
                f.write("logging.basicConfig(level=logging.INFO)\n")
                f.write("logger = logging.getLogger('moviepy')\n")
                f.write("\n")
                
                # Funções auxiliares
                f.write("# Funções auxiliares\n")
                f.write("def get_moviepy_version():\n")
                f.write(f"    return '{self.moviepy_version}'\n")
                f.write("\n")
                f.write("def check_dependencies():\n")
                f.write("    import moviepy\n")
                f.write("    return moviepy.__version__\n")
                f.write("\n")
                
                # Configurações específicas para MoviePy 2.1.2
                f.write("# Configurações específicas para MoviePy 2.1.2\n")
                f.write("def configure_moviepy_212():\n")
                f.write("    \"\"\"Configurações específicas para MoviePy 2.1.2\"\"\"\n")
                f.write("    # Importar as novas classes de efeitos\n")
                f.write("    from moviepy.video.fx import FadeIn, FadeOut\n")
                f.write("    \n")
                f.write("    # Configurar parâmetros padrão\n")
                f.write("    DEFAULT_FPS = 24\n")
                f.write("    DEFAULT_CODEC = 'libx264'\n")
                f.write("    \n")
                f.write("    return {\n")
                f.write("        'fade_in': FadeIn,\n")
                f.write("        'fade_out': FadeOut,\n")
                f.write("        'default_fps': DEFAULT_FPS,\n")
                f.write("        'default_codec': DEFAULT_CODEC\n")
                f.write("    }\n")
            
            self.add_result("Criar Arquivo de Configuração", True, f"Arquivo: {config_file}")
        except Exception as e:
            self.add_result("Criar Arquivo de Configuração", False, str(e))
        
        # Criar arquivo de inicialização
        try:
            init_file = os.path.join(config_dir, "moviepy_init.py")
            
            with open(init_file, 'w', encoding='utf-8') as f:
                f.write("# Inicialização do MoviePy\n")
                f.write(f"# Versão: {self.moviepy_version}\n")
                f.write(f"# Data: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                f.write("import os\n")
                f.write("import sys\n")
                f.write("from pathlib import Path\n")
                f.write("\n")
                f.write("# Adicionar diretório de configuração ao path\n")
                f.write("config_dir = Path(__file__).parent\n")
                f.write("sys.path.insert(0, str(config_dir))\n")
                f.write("\n")
                f.write("# Importar configurações\n")
                f.write("from moviepy_config import *\n")
                f.write("\n")
                f.write("# Inicializar MoviePy\n")
                f.write("try:\n")
                f.write("    import moviepy\n")
                f.write("    print(f'MoviePy {moviepy.__version__} inicializado com sucesso')\n")
                f.write("except ImportError as e:\n")
                f.write("    print(f'Erro ao inicializar MoviePy: {e}')\n")
                f.write("    sys.exit(1)\n")
                f.write("\n")
                f.write("# Configurar MoviePy 2.1.2\n")
                f.write("if moviepy.__version__ == '2.1.2':\n")
                f.write("    moviepy_config = configure_moviepy_212()\n")
                f.write("    print('Configurações específicas para MoviePy 2.1.2 aplicadas')\n")
            
            self.add_result("Criar Arquivo de Inicialização", True, f"Arquivo: {init_file}")
        except Exception as e:
            self.add_result("Criar Arquivo de Inicialização", False, str(e))
    
    def test_installation(self):
        """Testa a instalação do MoviePy"""
        print_section("Testar Instalação")
        
        if not hasattr(self, 'python_executable'):
            self.add_result("Testar Instalação", False, "Ambiente virtual não ativado")
            return
        
        # Criar script de teste
        test_script = os.path.join(self.temp_dir, "test_moviepy.py")
        
        try:
            with open(test_script, 'w', encoding='utf-8') as f:
                f.write("#!/usr/bin/env python3\n")
                f.write("# -*- coding: utf-8 -*-\n")
                f.write("\n")
                f.write("import sys\n")
                f.write("import os\n")
                f.write("import tempfile\n")
                f.write("import numpy as np\n")
                f.write("\n")
                f.write("# Adicionar diretório de configuração ao path\n")
                f.write(f"sys.path.insert(0, r'{os.path.join(self.project_dir, 'config')}')\n")
                f.write("\n")
                f.write("try:\n")
                f.write("    from moviepy.editor import *\n")
                f.write("    from moviepy.video.fx import FadeIn, FadeOut\n")
                f.write("    print('MoviePy importado com sucesso')\n")
                f.write("    \n")
                f.write("    # Testar criação de clipes\n")
                f.write("    clip = ColorClip(size=(100, 100), color=(255, 0, 0), duration=1)\n")
                f.write("    print('ColorClip criado com sucesso')\n")
                f.write("    \n")
                f.write("    # Testar efeitos\n")
                f.write("    faded_clip = clip.with_effects([FadeIn(0.5), FadeOut(0.5)])\n")
                f.write("    print('Efeitos aplicados com sucesso')\n")
                f.write("    \n")
                f.write("    # Testar exportação\n")
                f.write("    temp_dir = tempfile.gettempdir()\n")
                f.write("    output_path = os.path.join(temp_dir, 'test_moviepy.mp4')\n")
                f.write("    faded_clip.write_videofile(output_path, fps=24, logger=None)\n")
                f.write("    print('Vídeo exportado com sucesso')\n")
                f.write("    \n")
                f.write("    # Verificar se o arquivo foi criado\n")
                f.write("    if os.path.exists(output_path):\n")
                f.write("        print('Teste concluído com sucesso!')\n")
                f.write("        sys.exit(0)\n")
                f.write("    else:\n")
                f.write("        print('Erro: Arquivo não foi criado')\n")
                f.write("        sys.exit(1)\n")
                f.write("    \n")
                f.write("except Exception as e:\n")
                f.write("    print(f'Erro no teste: {e}')\n")
                f.write("    import traceback\n")
                f.write("    traceback.print_exc()\n")
                f.write("    sys.exit(1)\n")
            
            # Executar script de teste
            result = subprocess.run([self.python_executable, test_script], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.add_result("Testar Instalação", True, result.stdout)
            else:
                self.add_result("Testar Instalação", False, f"{result.stdout}\n{result.stderr}")
        except Exception as e:
            self.add_result("Testar Instalação", False, str(e))
    
    def print_summary(self):
        """Imprime um resumo da instalação"""
        print_section("Resumo da Instalação")
        
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
            color_print("\n✓ Instalação concluída com sucesso!", Colors.GREEN)
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
        
        color_print("1. Ative o ambiente virtual:", Colors.WHITE)
        if platform.system() == "Windows":
            color_print(f"   {self.virtual_env}\\Scripts\\activate", Colors.CYAN)
        else:
            color_print(f"   source {self.virtual_env}/bin/activate", Colors.CYAN)
        
        color_print("\n2. Execute o script de inicialização:", Colors.WHITE)
        color_print(f"   python {os.path.join(self.project_dir, 'config', 'moviepy_init.py')}", Colors.CYAN)
        
        color_print("\n3. Execute os testes:", Colors.WHITE)
        color_print(f"   python {os.path.join(self.project_dir, 'docs', 'moviepy', 'testes', 'SCRIPT_TESTES_COMPLETO.py')}", Colors.CYAN)
        
        color_print("\n4. Execute os exemplos:", Colors.WHITE)
        color_print(f"   python {os.path.join(self.project_dir, 'docs', 'moviepy', 'exemplos', 'SCRIPT_EXEMPLOS_PRACTICOS.py')}", Colors.CYAN)
        
        color_print("\n5. Execute o diagnóstico:", Colors.WHITE)
        color_print(f"   python {os.path.join(self.project_dir, 'docs', 'moviepy', 'testes', 'SCRIPT_DIAGNOSTICO_COMPLETO.py')}", Colors.CYAN)
    
    def save_results(self):
        """Salva os resultados em um arquivo"""
        try:
            results_file = os.path.join(self.temp_dir, "installation_results.txt")
            
            with open(results_file, 'w', encoding='utf-8') as f:
                f.write("=== RESULTADOS DA INSTALAÇÃO DO MOVIEPY ===\n\n")
                
                # Informações gerais
                f.write(f"Data: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Python: {self.python_version}\n")
                f.write(f"Sistema: {self.os_info}\n")
                f.write(f"Versão do MoviePy: {self.moviepy_version}\n")
                f.write(f"Diretório do projeto: {self.project_dir}\n")
                f.write(f"Ambiente virtual: {self.virtual_env}\n\n")
                
                # Resultados
                f.write("=== RESULTADOS DETALHADOS ===\n\n")
                
                for step_name, success, message in self.results:
                    status = "SUCESSO" if success else "FALHA"
                    f.write(f"{step_name}: {status}")
                    if message:
                        f.write(f" - {message}")
                    f.write("\n")
                
                # Estatísticas
                total_steps = len(self.results)
                successful_steps = sum(1 for _, success, _ in self.results if success)
                failed_steps = total_steps - successful_steps
                
                f.write(f"\n=== ESTATÍSTICAS ===\n")
                f.write(f"Total de passos: {total_steps}\n")
                f.write(f"Passos bem-sucedidos: {successful_steps}\n")
                f.write(f"Passos falhos: {failed_steps}\n")
                
                if total_steps > 0:
                    percentage = (successful_steps / total_steps) * 100
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
        
        # Criar instalador
        installer = MoviePyInstaller()
        
        # Executar instalação
        success = installer.run_installation()
        
        # Retornar código de saída
        return 0 if success else 1
    except KeyboardInterrupt:
        color_print("\nInstalação interrompida pelo usuário", Colors.YELLOW)
        return 1
    except Exception as e:
        color_print(f"\nErro inesperado: {e}", Colors.RED)
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())