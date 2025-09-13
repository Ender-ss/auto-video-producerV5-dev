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
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "moviepy_manual_install_log.txt")
TEMP_DIR = os.path.join(tempfile.gettempdir(), "moviepy_manual_install")
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
log("            INSTALAÇÃO MANUAL DO MOVIEPY 2.2.1          ")
log("=" * 50)
log(f"Python: {PYTHON_EXE}")
log(f"Versão-alvo: {TARGET_VERSION}")
log(f"URL do GitHub: {GITHUB_URL}")
log("=" * 50)

# Criar diretório temporário
os.makedirs(TEMP_DIR, exist_ok=True)
log(f"Diretório temporário criado: {TEMP_DIR}")

# Passo 1: Baixar o código-fonte do MoviePy 2.2.1 do GitHub
log("\n[1/5] BAIXANDO O CÓDIGO-FONTE DO MOVIEPY 2.2.1 DO GITHUB...")
zip_path = os.path.join(TEMP_DIR, f"moviepy-{TARGET_VERSION}.zip")

try:
    log(f"Baixando de: {GITHUB_URL}")
    urllib.request.urlretrieve(GITHUB_URL, zip_path)
    log("Download concluído com sucesso!")
except Exception as e:
    log(f"ERRO FATAL: Falha no download do código-fonte: {e}")
    sys.exit(1)

# Passo 2: Extrair o arquivo ZIP
log("\n[2/5] EXTRINDO O ARQUIVO ZIP...")
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

# Passo 3: Verificar se o arquivo editor.py existe no código-fonte
log("\n[3/5] VERIFICANDO EXISTÊNCIA DO ARQUIVO EDITOR.PY...")
editor_path = os.path.join(extract_dir, "moviepy", "editor.py")

if os.path.exists(editor_path):
    log(f"✅ O arquivo editor.py existe no código-fonte: {editor_path}")
else:
    log(f"❌ O arquivo editor.py NÃO existe no código-fonte: {editor_path}")
    log("Listando conteúdo do diretório moviepy extraído:")
    moviepy_dir = os.path.join(extract_dir, "moviepy")
    if os.path.exists(moviepy_dir):
        for item in os.listdir(moviepy_dir):
            log(f"- {item}")
    sys.exit(1)

# Passo 4: Identificar diretórios site-packages
log("\n[4/5] IDENTIFICANDO DIRETÓRIOS SITE-PACKAGES...")

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

# Passo 5: Instalar manualmente o MoviePy 2.2.1
log("\n[5/5] INSTALANDO MANUALMENTE O MOVIEPY 2.2.1...")

# Remover instalações existentes
for path in site_packages_paths:
    if os.path.exists(path):
        log(f"Limpando instalação existente em: {path}")
        
        # Remover diretório moviepy
        moviepy_dir = os.path.join(path, "moviepy")
        if os.path.exists(moviepy_dir):
            try:
                shutil.rmtree(moviepy_dir)
                log("  - Diretório moviepy removido com sucesso")
            except Exception as e:
                log(f"  - ERRO ao remover diretório moviepy: {e}")
        
        # Remover arquivos .egg-info e .dist-info
        for item in os.listdir(path):
            if item.startswith("moviepy-") and (item.endswith(".egg-info") or item.endswith(".dist-info")):
                item_path = os.path.join(path, item)
                try:
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                    else:
                        os.remove(item_path)
                    log(f"  - Arquivo {item} removido com sucesso")
                except Exception as e:
                    log(f"  - ERRO ao remover arquivo {item}: {e}")

# Copiar o código-fonte para o site-packages do usuário
user_site_packages = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Python", "Python313", "site-packages")
source_dir = os.path.join(extract_dir, "moviepy")
target_dir = os.path.join(user_site_packages, "moviepy")

try:
    log(f"Copiando código-fonte de {source_dir} para {target_dir}")
    shutil.copytree(source_dir, target_dir)
    log("Código-fonte copiado com sucesso!")
except Exception as e:
    log(f"ERRO FATAL: Falha ao copiar código-fonte: {e}")
    sys.exit(1)

# Verificar se o arquivo editor.py foi copiado corretamente
editor_target_path = os.path.join(target_dir, "editor.py")
if os.path.exists(editor_target_path):
    log(f"✅ O arquivo editor.py foi copiado com sucesso: {editor_target_path}")
else:
    log(f"❌ O arquivo editor.py NÃO foi copiado corretamente: {editor_target_path}")
    sys.exit(1)

# Atualizar o arquivo version.py para garantir que a versão correta seja exibida
version_file = os.path.join(target_dir, "version.py")
try:
    with open(version_file, "w") as f:
        f.write(f'__version__ = "{TARGET_VERSION}"\n')
    log(f"Arquivo version.py atualizado com a versão {TARGET_VERSION}")
except Exception as e:
    log(f"ERRO ao atualizar arquivo version.py: {e}")

# Criar script de verificação
verification_script = os.path.join(TEMP_DIR, "verificacao_manual.py")
with open(verification_script, "w", encoding="utf-8") as f:
    f.write(f"""
import sys
import os
import importlib

print("===== VERIFICAÇÃO MANUAL DO MOVIEPY =====")

# Verificar caminho do Python
print(f"Caminho do Python: {{sys.executable}}")

try:
    # Importar MoviePy
    import moviepy
    print(f"\\nMoviePy importado com sucesso! Versão: {{moviepy.__version__}}")
    print(f"Localização: {{os.path.dirname(moviepy.__file__)}}")
    
    # Verificar conteúdo do diretório
    moviepy_dir = os.path.dirname(moviepy.__file__)
    print(f"\\nConteúdo do diretório {{moviepy_dir}}:")
    for item in os.listdir(moviepy_dir):
        print(f"- {{item}}")
    
    # Verificar existência do arquivo editor.py
    editor_path = os.path.join(moviepy_dir, 'editor.py')
    if os.path.exists(editor_path):
        print(f"\\nOK: O arquivo editor.py existe em: {{editor_path}}")
    else:
        print(f"\\nERRO: O arquivo editor.py NÃO existe em: {{editor_path}}")
        sys.exit(1)
    
    # Tentar importar submódulo editor
    try:
        from moviepy import editor
        print("\\nOK: SUBMÓDULO 'EDITOR' IMPORTADO COM SUCESSO!")
        
        # Verificar métodos essenciais
        print("\\nVerificando métodos essenciais:")
        has_video_file_clip = hasattr(editor, 'VideoFileClip')
        has_with_audio = hasattr(editor, 'with_audio') or (hasattr(editor.VideoFileClip, 'with_audio') if has_video_file_clip else False)
        has_set_audio = hasattr(editor, 'set_audio') or (hasattr(editor.VideoFileClip, 'set_audio') if has_video_file_clip else False)
        
        print(f"- VideoFileClip: {{'SIM' if has_video_file_clip else 'NAO'}}")
        print(f"- with_audio: {{'SIM' if has_with_audio else 'NAO'}}")
        print(f"- set_audio: {{'SIM' if has_set_audio else 'NAO'}}")
        
        if has_video_file_clip and has_with_audio and has_set_audio:
            print("\\nSUCESSO: A instalação do MoviePy está 100% funcionando!")
            print("\\nVocê pode executar sua aplicação auto-video-producerV5-dev.")
            sys.exit(0)
        else:
            print("\\nATENCAO: A instalação está parcialmente correta, mas alguns métodos estão faltando.")
            sys.exit(1)
    except ImportError as e:
        print(f"\\nERRO: Não foi possível importar o submódulo 'editor'!")
        print(f"Detalhes: {{str(e)}}")
        sys.exit(1)
except ImportError as e:
    print("\\nERRO: Não foi possível importar o MoviePy!")
    print(f"Detalhes: {{str(e)}}")
    sys.exit(1)
""")

# Executar verificação e capturar resultado
log("\nEXECUTANDO VERIFICAÇÃO MANUAL...")
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
    log("SUCCESSO! A instalação manual do MoviePy 2.2.1 está 100% funcionando!")
    log("O submódulo 'editor' está totalmente disponível.")
    log("Todos os métodos essenciais foram verificados.")
    log("\nAcesse o arquivo de log para mais detalhes:")
    log(f"  {LOG_FILE}")
else:
    log("FALHA! A instalação manual do MoviePy ainda está com problemas.")
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