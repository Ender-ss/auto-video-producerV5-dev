import os
import sys
import subprocess
import shutil
import tempfile
import time
from datetime import datetime

# Configurações
PYTHON_EXE = r"C:\Program Files\Python313\python.exe"
TARGET_VERSION = "2.2.1"
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "moviepy_fix_log.txt")
TEMP_DIR = os.path.join(tempfile.gettempdir(), "moviepy_fix")

# Função para registrar logs
def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry + "\n")

# Limpar log anterior
if os.path.exists(LOG_FILE):
    os.remove(LOG_FILE)

log("=" * 50)
log("            SOLUÇÃO DEFINITIVA - MOVIEPY            ")
log("=" * 50)
log(f"Python: {PYTHON_EXE}")
log(f"Versão-alvo: {TARGET_VERSION}")
log("=" * 50)

# Verificar permissões de administrador
try:
    import ctypes
    is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    if is_admin:
        log("Executando com privilégios de administrador.")
    else:
        log("Executando sem privilégios de administrador. Algumas operações podem ser limitadas.")
except Exception as e:
    log(f"Não foi possível verificar permissões de administrador: {e}")

# Criar diretório temporário
os.makedirs(TEMP_DIR, exist_ok=True)
log(f"Diretório temporário criado: {TEMP_DIR}")

# Passo 1: Parar todos os processos Python (apenas se for administrador)
log("\n[1/8] PARANDO PROCESSOS PYTHON...")
try:
    if is_admin:
        subprocess.run(["taskkill", "/F", "/IM", "python.exe"], capture_output=True)
        subprocess.run(["taskkill", "/F", "/IM", "pythonw.exe"], capture_output=True)
        log("Processos Python encerrados.")
    else:
        log(" pulando - sem privilégios de administrador")
except Exception as e:
    log(f"Erro ao encerrar processos Python: {e}")

# Passo 2: Identificar todos os diretórios de instalação do Python
log("\n[2/8] IDENTIFICANDO DIRETÓRIOS DE INSTALAÇÃO DO PYTHON...")

# Criar script para listar todos os diretórios do site-packages
list_paths_script = os.path.join(TEMP_DIR, "list_python_paths.py")
with open(list_paths_script, "w") as f:
    f.write("""
import sys
import os
print('\\n'.join(sys.path))
""")

# Executar script e capturar saída
try:
    result = subprocess.run([PYTHON_EXE, list_paths_script], capture_output=True, text=True)
    python_paths = result.stdout.strip().split("\n")
    
    site_packages_paths = []
    for path in python_paths:
        if path.strip() and os.path.exists(os.path.join(path.strip(), "site-packages")):
            site_packages_paths.append(os.path.join(path.strip(), "site-packages"))
    
    # Adicionar caminhos comuns
    common_paths = [
        os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Python", "Python313", "site-packages"),
        r"C:\Program Files\Python313\Lib\site-packages"
    ]
    
    for path in common_paths:
        if os.path.exists(path) and path not in site_packages_paths:
            site_packages_paths.append(path)
    
    log("Diretórios site-packages identificados:")
    for path in site_packages_paths:
        log(f"- {path}")
        
except Exception as e:
    log(f"Erro ao identificar diretórios site-packages: {e}")
    # Usar caminhos padrão como fallback
    site_packages_paths = [
        os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Python", "Python313", "site-packages"),
        r"C:\Program Files\Python313\Lib\site-packages"
    ]

# Passo 3: Remover instalações existentes do MoviePy
log("\n[3/8] REMOVENDO INSTALAÇÕES EXISTENTES DO MOVIEPY...")

# Remover via pip primeiro
try:
    log("Tentando desinstalar MoviePy via pip...")
    subprocess.run([PYTHON_EXE, "-m", "pip", "uninstall", "-y", "moviepy"], capture_output=True)
    log("Tentativa de desinstalação via pip concluída.")
except Exception as e:
    log(f"Erro na desinstalação via pip: {e}")

# Remover manualmente todos os vestígios
for path in site_packages_paths:
    if os.path.exists(path):
        log(f"Limpando diretório: {path}")
        
        # Remover diretório moviepy
        moviepy_dir = os.path.join(path, "moviepy")
        if os.path.exists(moviepy_dir):
            log(f"  - Removendo diretório: moviepy")
            try:
                shutil.rmtree(moviepy_dir)
                log("    - Removido com sucesso")
            except Exception as e:
                log(f"    - ERRO ao remover: {e}")
                # Tentar com permissões elevadas (apenas se for administrador)
                if is_admin:
                    try:
                        subprocess.run(["takeown", "/F", moviepy_dir, "/R", "/D", "Y"], capture_output=True)
                        subprocess.run(["icacls", moviepy_dir, "/grant", "*S-1-5-32-544:F", "/T"], capture_output=True)
                        shutil.rmtree(moviepy_dir)
                        log("    - Removido após alteração de permissões")
                    except Exception as e2:
                        log(f"    - ERRO persistente: {e2}")
                else:
                    log("    - Não é possível remover sem privilégios de administrador")
        
        # Remover arquivos .egg-info e .dist-info
        for item in os.listdir(path):
            if item.startswith("moviepy-") and (item.endswith(".egg-info") or item.endswith(".dist-info")):
                item_path = os.path.join(path, item)
                log(f"  - Removendo: {item}")
                try:
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                    else:
                        os.remove(item_path)
                    log("    - Removido com sucesso")
                except Exception as e:
                    log(f"    - ERRO ao remover: {e}")

# Passo 4: Limpar cache do pip
log("\n[4/8] LIMPAR CACHE DO PIP...")
try:
    subprocess.run([PYTHON_EXE, "-m", "pip", "cache", "purge"], capture_output=True)
    log("Cache do pip limpo.")
except Exception as e:
    log(f"Erro ao limpar cache do pip: {e}")

# Passo 5: Atualizar o pip
log("\n[5/8] ATUALIZANDO O PIP...")
try:
    result = subprocess.run([PYTHON_EXE, "-m", "pip", "install", "--upgrade", "pip"], capture_output=True)
    if result.returncode == 0:
        log("Pip atualizado com sucesso.")
    else:
        log("ATENÇÃO: Não foi possível atualizar o pip, mas continuando.")
except Exception as e:
    log(f"ATENÇÃO: Erro na atualização do pip: {e}, mas continuando.")

# Passo 6: Instalar dependências essenciais
log("\n[6/8] INSTALANDO DEPENDÊNCIAS ESSENCIAIS...")
try:
    result = subprocess.run([
        PYTHON_EXE, "-m", "pip", "install", "--force-reinstall", "--no-cache-dir", 
        "numpy", "imageio", "pillow", "decorator", "proglog", "tqdm"
    ], capture_output=True)
    if result.returncode == 0:
        log("Dependências instaladas com sucesso.")
    else:
        log("ATENÇÃO: Erro na instalação de dependências, mas continuando.")
except Exception as e:
    log(f"ATENÇÃO: Erro na instalação de dependências: {e}, mas continuando.")

# Passo 7: Instalar a versão correta do MoviePy com caminho explícito
log("\n[7/8] INSTALANDO MOVIEPY VERSÃO 2.2.1...")
try:
    # Tentar instalar via PyPI primeiro
    result = subprocess.run([
        PYTHON_EXE, "-m", "pip", "install", "--force-reinstall", "--no-cache-dir", 
        f"moviepy=={TARGET_VERSION}"
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        log(f"MoviePy {TARGET_VERSION} instalado com sucesso!")
    else:
        log(f"ERRO: Falha na instalação do MoviePy {TARGET_VERSION} via PyPI!")
        log(f"Detalhes: {result.stderr}")
        
        # Tentar instalar diretamente do GitHub
        log("Tentando instalar diretamente do GitHub...")
        result = subprocess.run([
            PYTHON_EXE, "-m", "pip", "install", "--force-reinstall", "--no-cache-dir", 
            "git+https://github.com/Zulko/moviepy.git@v2.2.1"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            log(f"MoviePy {TARGET_VERSION} instalado com sucesso do GitHub!")
        else:
            log(f"ERRO: Falha na instalação do MoviePy {TARGET_VERSION} do GitHub!")
            log(f"Detalhes: {result.stderr}")
            
except Exception as e:
    log(f"ERRO: Exceção durante a instalação do MoviePy: {e}")

# Passo 8: Criar e executar script de verificação abrangente
log("\n[8/8] EXECUTANDO VERIFICAÇÃO DEFINITIVA...")

# Criar script de verificação
verification_script = os.path.join(TEMP_DIR, "verificacao_definitiva.py")
with open(verification_script, "w", encoding="utf-8") as f:
    f.write("""
import sys
import os
import importlib.util

print("===== VERIFICAÇÃO DEFINITIVA DO MOVIEPY =====")

# Verificar caminho do Python
print(f"Caminho do Python: {sys.executable}")
print("\\nCaminhos de importação:")
for path in sys.path:
    print(f"- {path}")

try:
    # Importar MoviePy
    import moviepy
    print(f"\\nMoviePy importado com sucesso! Versão: {moviepy.__version__}")
    print(f"Localização: {os.path.dirname(moviepy.__file__)}")
    
    # Verificar conteúdo do diretório
    moviepy_dir = os.path.dirname(moviepy.__file__)
    print(f"\\nConteúdo do diretório {moviepy_dir}:")
    for item in os.listdir(moviepy_dir):
        print(f"- {item}")
    
    # Verificar existência do arquivo editor.py
    editor_path = os.path.join(moviepy_dir, 'editor.py')
    if os.path.exists(editor_path):
        print(f"\\n✅ O arquivo editor.py existe em: {editor_path}")
    else:
        print(f"\\n❌ O arquivo editor.py NÃO existe em: {editor_path}")
        sys.exit(1)
    
    # Tentar importar submódulo editor
    try:
        from moviepy import editor
        print("\\n✅ SUBMÓDULO 'EDITOR' IMPORTADO COM SUCESSO!")
        
        # Verificar métodos essenciais
        print("\\nVerificando métodos essenciais:")
        has_video_file_clip = hasattr(editor, 'VideoFileClip')
        has_with_audio = hasattr(editor, 'with_audio') or (hasattr(editor.VideoFileClip, 'with_audio') if has_video_file_clip else False)
        has_set_audio = hasattr(editor, 'set_audio') or (hasattr(editor.VideoFileClip, 'set_audio') if has_video_file_clip else False)
        
        print(f"- VideoFileClip: {'✓' if has_video_file_clip else '✗'}")
        print(f"- with_audio: {'✓' if has_with_audio else '✗'}")
        print(f"- set_audio: {'✓' if has_set_audio else '✗'}")
        
        if has_video_file_clip and has_with_audio and has_set_audio:
            print("\\n🎉 A INSTALAÇÃO DO MOVIEPY ESTÁ 100%% FUNCIONANDO!")
            print("\\nVocê pode executar sua aplicação auto-video-producerV5-dev.")
            sys.exit(0)
        else:
            print("\\n⚠️  A instalação está parcialmente correta, mas alguns métodos estão faltando.")
            sys.exit(1)
    except ImportError as e:
        print(f"\\n❌ ERRO: Não foi possível importar o submódulo 'editor'!")
        print(f"Detalhes: {str(e)}")
        sys.exit(1)
except ImportError as e:
    print("\\n❌ ERRO: Não foi possível importar o MoviePy!")
    print(f"Detalhes: {str(e)}")
    sys.exit(1)
""")

# Executar verificação e capturar resultado
try:
    result = subprocess.run([PYTHON_EXE, verification_script], capture_output=True, text=True)
    verify_result = result.returncode
    
    # Salvar saída da verificação no log
    log("\nSaída da verificação:")
    log(result.stdout)
    if result.stderr:
        log("\nErros na verificação:")
        log(result.stderr)
        
except Exception as e:
    log(f"ERRO: Não foi possível executar a verificação: {e}")
    verify_result = 1

# Exibir resumo da verificação
log("\n" + "=" * 50)
log("                  RESULTADO FINAL                  ")
log("=" * 50)
if verify_result == 0:
    log("🎊 SUCCESSO! A instalação do MoviePy 2.2.1 está 100% funcionando!")
    log("✅ O submódulo 'editor' está totalmente disponível.")
    log("✅ Todos os métodos essenciais foram verificados.")
    log("\nAcesse o arquivo de log para mais detalhes:")
    log(f"  {LOG_FILE}")
else:
    log("❌ FALHA! A instalação do MoviePy ainda está com problemas.")
    log("\nSugestões para resolver:")
    log("1. Reinicie o computador e execute este script novamente como ADMINISTRADOR")
    log("2. Verifique as permissões de seus diretórios do Python")
    log("3. Consulte o arquivo de log para mais detalhes:")
    log(f"   {LOG_FILE}")
log("=" * 50)

# Limpar diretório temporário
try:
    shutil.rmtree(TEMP_DIR)
    log("Diretório temporário limpo.")
except Exception as e:
    log(f"Erro ao limpar diretório temporário: {e}")

print("\nPressione Enter para sair...")
input()

sys.exit(verify_result)