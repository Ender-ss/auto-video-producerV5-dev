import os
import sys
import subprocess
import shutil
import tempfile
import time
import urllib.request
import zipfile
from datetime import datetime

# Configurações
PYTHON_EXE = r"C:\Program Files\Python313\python.exe"
TARGET_VERSION = "2.2.1"
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "moviepy_structure_analysis_log.txt")
TEMP_DIR = os.path.join(tempfile.gettempdir(), "moviepy_analysis")
GITHUB_URL = f"https://github.com/Zulko/moviepy/archive/refs/tags/v{TARGET_VERSION}.zip"

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
log("            ANÁLISE DA ESTRUTURA DO MOVIEPY            ")
log("=" * 50)
log(f"Python: {PYTHON_EXE}")
log(f"Versão-alvo: {TARGET_VERSION}")
log("=" * 50)

# Criar diretório temporário
os.makedirs(TEMP_DIR, exist_ok=True)
log(f"Diretório temporário criado: {TEMP_DIR}")

# Passo 1: Baixar o código-fonte do MoviePy 2.2.1 do GitHub
log("\n[1/3] BAIXANDO O CÓDIGO-FONTE DO MOVIEPY 2.2.1 DO GITHUB...")
zip_path = os.path.join(TEMP_DIR, f"moviepy-{TARGET_VERSION}.zip")

try:
    log(f"Baixando de: {GITHUB_URL}")
    urllib.request.urlretrieve(GITHUB_URL, zip_path)
    log("Download concluído com sucesso!")
except Exception as e:
    log(f"ERRO FATAL: Falha no download do código-fonte: {e}")
    sys.exit(1)

# Passo 2: Extrair o arquivo ZIP
log("\n[2/3] EXTRINDO O ARQUIVO ZIP...")
extract_dir = os.path.join(TEMP_DIR, f"moviepy-{TARGET_VERSION}")

try:
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(TEMP_DIR)
    log("Extração concluída com sucesso!")
except Exception as e:
    log(f"ERRO FATAL: Falha na extração do arquivo ZIP: {e}")
    sys.exit(1)

# Verificar se o diretório extraído existe
if not os.path.exists(extract_dir):
    log(f"ERRO FATAL: Diretório extraído não encontrado: {extract_dir}")
    sys.exit(1)

# Passo 3: Analisar a estrutura do MoviePy
log("\n[3/3] ANALISANDO A ESTRUTURA DO MOVIEPY...")
moviepy_dir = os.path.join(extract_dir, "moviepy")

# Verificar conteúdo do diretório principal
log(f"\nConteúdo do diretório principal ({moviepy_dir}):")
for item in os.listdir(moviepy_dir):
    item_path = os.path.join(moviepy_dir, item)
    if os.path.isdir(item_path):
        log(f"- {item}/ (diretório)")
    else:
        log(f"- {item} (arquivo)")

# Verificar conteúdo do arquivo __init__.py
init_file = os.path.join(moviepy_dir, "__init__.py")
if os.path.exists(init_file):
    log(f"\nConteúdo do arquivo __init__.py:")
    with open(init_file, "r", encoding="utf-8") as f:
        init_content = f.read()
        log(init_content)

# Verificar conteúdo do diretório video
video_dir = os.path.join(moviepy_dir, "video")
if os.path.exists(video_dir):
    log(f"\nConteúdo do diretório video ({video_dir}):")
    for item in os.listdir(video_dir):
        item_path = os.path.join(video_dir, item)
        if os.path.isdir(item_path):
            log(f"- {item}/ (diretório)")
        else:
            log(f"- {item} (arquivo)")
    
    # Verificar conteúdo do arquivo __init__.py do diretório video
    video_init_file = os.path.join(video_dir, "__init__.py")
    if os.path.exists(video_init_file):
        log(f"\nConteúdo do arquivo video/__init__.py:")
        with open(video_init_file, "r", encoding="utf-8") as f:
            video_init_content = f.read()
            log(video_init_content)

# Verificar conteúdo do diretório audio
audio_dir = os.path.join(moviepy_dir, "audio")
if os.path.exists(audio_dir):
    log(f"\nConteúdo do diretório audio ({audio_dir}):")
    for item in os.listdir(audio_dir):
        item_path = os.path.join(audio_dir, item)
        if os.path.isdir(item_path):
            log(f"- {item}/ (diretório)")
        else:
            log(f"- {item} (arquivo)")
    
    # Verificar conteúdo do arquivo __init__.py do diretório audio
    audio_init_file = os.path.join(audio_dir, "__init__.py")
    if os.path.exists(audio_init_file):
        log(f"\nConteúdo do arquivo audio/__init__.py:")
        with open(audio_init_file, "r", encoding="utf-8") as f:
            audio_init_content = f.read()
            log(audio_init_content)

# Verificar se existe um arquivo editor.py em algum subdiretório
log("\nProcurando por arquivos editor.py em toda a estrutura do MoviePy...")
editor_files = []
for root, dirs, files in os.walk(moviepy_dir):
    for file in files:
        if file == "editor.py":
            editor_files.append(os.path.join(root, file))

if editor_files:
    log(f"\nArquivos editor.py encontrados:")
    for file in editor_files:
        log(f"- {file}")
else:
    log("\nNenhum arquivo editor.py encontrado em toda a estrutura do MoviePy.")

# Verificar se existem arquivos que contenham "VideoFileClip"
log("\nProcurando por arquivos que contenham 'VideoFileClip'...")
videoclip_files = []
for root, dirs, files in os.walk(moviepy_dir):
    for file in files:
        if file.endswith(".py"):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    if "class VideoFileClip" in content or "def VideoFileClip" in content:
                        videoclip_files.append(file_path)
            except Exception as e:
                log(f"  - Erro ao ler arquivo {file_path}: {e}")

if videoclip_files:
    log(f"\nArquivos que contêm 'VideoFileClip':")
    for file in videoclip_files:
        log(f"- {file}")
else:
    log("\nNenhum arquivo contendo 'VideoFileClip' encontrado.")

# Verificar se existem arquivos que contenham "with_audio" ou "set_audio"
log("\nProcurando por arquivos que contenham 'with_audio' ou 'set_audio'...")
audio_methods_files = []
for root, dirs, files in os.walk(moviepy_dir):
    for file in files:
        if file.endswith(".py"):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    if "def with_audio" in content or "def set_audio" in content:
                        audio_methods_files.append(file_path)
            except Exception as e:
                log(f"  - Erro ao ler arquivo {file_path}: {e}")

if audio_methods_files:
    log(f"\nArquivos que contêm 'with_audio' ou 'set_audio':")
    for file in audio_methods_files:
        log(f"- {file}")
else:
    log("\nNenhum arquivo contendo 'with_audio' ou 'set_audio' encontrado.")

# Criar script para testar a importação do MoviePy e verificar como acessar as funcionalidades
test_script = os.path.join(TEMP_DIR, "test_moviepy_import.py")
with open(test_script, "w", encoding="utf-8") as f:
    f.write("""
import sys
import os
import importlib

print("===== TESTE DE IMPORTAÇÃO DO MOVIEPY =====")

# Verificar caminho do Python
print(f"Caminho do Python: {sys.executable}")

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
    
    # Verificar atributos do módulo moviepy
    print(f"\\nAtributos do módulo moviepy:")
    for attr in dir(moviepy):
        if not attr.startswith('_'):
            print(f"- {attr}")
    
    # Tentar importar submódulos
    print(f"\\nTentando importar submódulos:")
    
    try:
        from moviepy import video
        print("- video: SUCESSO")
        
        # Verificar atributos do submódulo video
        print("  Atributos do submódulo video:")
        for attr in dir(video):
            if not attr.startswith('_'):
                print(f"  - {attr}")
    except ImportError as e:
        print(f"- video: FALHA - {e}")
    
    try:
        from moviepy import audio
        print("- audio: SUCESSO")
        
        # Verificar atributos do submódulo audio
        print("  Atributos do submódulo audio:")
        for attr in dir(audio):
            if not attr.startswith('_'):
                print(f"  - {attr}")
    except ImportError as e:
        print(f"- audio: FALHA - {e}")
    
    try:
        from moviepy import editor
        print("- editor: SUCESSO")
        
        # Verificar atributos do submódulo editor
        print("  Atributos do submódulo editor:")
        for attr in dir(editor):
            if not attr.startswith('_'):
                print(f"  - {attr}")
    except ImportError as e:
        print(f"- editor: FALHA - {e}")
    
    # Tentar importar VideoFileClip diretamente
    try:
        from moviepy.video.io.VideoFileClip import VideoFileClip
        print("- VideoFileClip (diretamente): SUCESSO")
    except ImportError as e:
        print(f"- VideoFileClip (diretamente): FALHA - {e}")
    
    # Tentar importar VideoFileClip a partir do módulo video
    try:
        from moviepy.video.io import VideoFileClip
        print("- VideoFileClip (a partir de video.io): SUCESSO")
    except ImportError as e:
        print(f"- VideoFileClip (a partir de video.io): FALHA - {e}")
    
    # Tentar importar VideoFileClip a partir do módulo principal
    try:
        from moviepy import VideoFileClip
        print("- VideoFileClip (a partir do módulo principal): SUCESSO")
    except ImportError as e:
        print(f"- VideoFileClip (a partir do módulo principal): FALHA - {e}")
    
except ImportError as e:
    print(f"\\nERRO: Não foi possível importar o MoviePy!")
    print(f"Detalhes: {str(e)}")
    sys.exit(1)
""")

# Executar script de teste
log("\nEXECUTANDO SCRIPT DE TESTE DE IMPORTAÇÃO...")
try:
    result = subprocess.run([PYTHON_EXE, test_script], capture_output=True, text=True)
    
    # Salvar saída do teste no log
    log("\nSaída do script de teste:")
    log(result.stdout)
    if result.stderr:
        log("\nErros no script de teste:")
        log(result.stderr)
        
except Exception as e:
    log(f"ERRO: Não foi possível executar o script de teste: {e}")

# Limpar diretório temporário
try:
    shutil.rmtree(TEMP_DIR)
    log("\nDiretório temporário limpo.")
except Exception as e:
    log(f"\nErro ao limpar diretório temporário: {e}")

print("\nAnálise concluída. Verifique o arquivo de log para mais detalhes:")
print(f"  {LOG_FILE}")

print("\nPressione Enter para sair...")
input()