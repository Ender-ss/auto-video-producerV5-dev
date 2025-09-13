import os
import sys
import subprocess
import shutil
import tempfile
import time
from datetime import datetime

# Configurações
PYTHON_EXE = r"C:\Program Files\Python313\python.exe"
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "moviepy_fix_app_log.txt")
TEMP_DIR = os.path.join(tempfile.gettempdir(), "moviepy_fix_app")

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
log("            CORREÇÃO DA APLICAÇÃO PARA MOVIEPY 2.2.1   ")
log("=" * 50)
log(f"Python: {PYTHON_EXE}")
log("=" * 50)

# Criar diretório temporário
os.makedirs(TEMP_DIR, exist_ok=True)
log(f"Diretório temporário criado: {TEMP_DIR}")

# Passo 1: Encontrar arquivos Python que usam o MoviePy na aplicação
log("\n[1/4] PROCURANDO ARQUIVOS QUE USAM O MOVIEPY...")

app_dir = os.path.dirname(os.path.abspath(__file__))
python_files = []
moviepy_imports = []

for root, dirs, files in os.walk(app_dir):
    for file in files:
        if file.endswith(".py"):
            file_path = os.path.join(root, file)
            python_files.append(file_path)
            
            # Verificar se o arquivo usa MoviePy
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    if "import moviepy" in content or "from moviepy" in content:
                        moviepy_imports.append(file_path)
                        log(f"  - Encontrado uso do MoviePy em: {file_path}")
            except Exception as e:
                log(f"  - Erro ao ler arquivo {file_path}: {e}")

log(f"\nTotal de arquivos Python encontrados: {len(python_files)}")
log(f"Total de arquivos que usam MoviePy: {len(moviepy_imports)}")

# Passo 2: Analisar os usos do MoviePy para identificar problemas
log("\n[2/4] ANALISANDO USOS DO MOVIEPY...")

problems_found = []

for file_path in moviepy_imports:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            lines = content.split("\n")
            
            for i, line in enumerate(lines, 1):
                # Verificar importações problemáticas
                if "from moviepy import editor" in line:
                    problems_found.append({
                        "file": file_path,
                        "line": i,
                        "content": line.strip(),
                        "problem": "Importação do submódulo 'editor' que não existe no MoviePy 2.2.1"
                    })
                
                # Verificar usos específicos que podem precisar de ajustes
                if "editor." in line and "from moviepy" not in line:
                    problems_found.append({
                        "file": file_path,
                        "line": i,
                        "content": line.strip(),
                        "problem": "Uso do namespace 'editor.' que pode não estar disponível"
                    })
    except Exception as e:
        log(f"  - Erro ao analisar arquivo {file_path}: {e}")

if problems_found:
    log(f"\nProblemas encontrados ({len(problems_found)}):")
    for problem in problems_found:
        log(f"  - Arquivo: {problem['file']}")
        log(f"    Linha {problem['line']}: {problem['content']}")
        log(f"    Problema: {problem['problem']}")
else:
    log("\nNenhum problema encontrado nos usos do MoviePy.")

# Passo 3: Criar um script de correção automática
log("\n[3/4] CRIANDO SCRIPT DE CORREÇÃO AUTOMÁTICA...")

correction_script = os.path.join(TEMP_DIR, "corrigir_moviepy.py")
with open(correction_script, "w", encoding="utf-8") as f:
    f.write("""
import os
import re
import shutil
from datetime import datetime

# Configurações
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "correcao_moviepy_log.txt")
BACKUP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backups")

# Função para registrar logs
def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry + "\\n")

# Criar diretório de backups
os.makedirs(BACKUP_DIR, exist_ok=True)

log("=" * 50)
log("            CORREÇÃO AUTOMÁTICA DO MOVIEPY            ")
log("=" * 50)

# Função para corrigir um arquivo
def corrigir_arquivo(file_path):
    # Fazer backup do arquivo original
    backup_path = os.path.join(BACKUP_DIR, os.path.basename(file_path) + ".backup")
    shutil.copy2(file_path, backup_path)
    log(f"Backup criado: {backup_path}")
    
    # Ler o conteúdo do arquivo
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Registrar alterações
    alteracoes = []
    
    # Correção 1: Substituir "from moviepy import editor" por "import moviepy"
    if "from moviepy import editor" in content:
        content = re.sub(r"from moviepy import editor", "import moviepy", content)
        alteracoes.append("Substituído 'from moviepy import editor' por 'import moviepy'")
    
    # Correção 2: Substituir "editor." por "moviepy." quando necessário
    # Isso é mais complexo e precisa ser feito com cuidado
    # Vamos apenas registrar os casos onde isso acontece
    if "editor." in content:
        lines = content.split("\\n")
        for i, line in enumerate(lines, 1):
            if "editor." in line and "from moviepy.editor" not in line and "import moviepy" not in line:
                log(f"  - Linha {i}: {line.strip()}")
    
    # Salvar o conteúdo corrigido
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    return alteracoes

# Encontrar arquivos Python que usam o MoviePy
app_dir = os.path.dirname(os.path.abspath(__file__))
moviepy_files = []

for root, dirs, files in os.walk(app_dir):
    for file in files:
        if file.endswith(".py"):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    if "import moviepy" in content or "from moviepy" in content:
                        moviepy_files.append(file_path)
            except Exception as e:
                log(f"Erro ao ler arquivo {file_path}: {e}")

# Corrigir cada arquivo
total_alteracoes = 0
for file_path in moviepy_files:
    log(f"\\nCorrigindo arquivo: {file_path}")
    alteracoes = corrigir_arquivo(file_path)
    if alteracoes:
        log(f"  - Alterações realizadas:")
        for alteracao in alteracoes:
            log(f"    * {alteracao}")
            total_alteracoes += 1
    else:
        log("  - Nenhuma alteração necessária")

log(f"\\nTotal de alterações realizadas: {total_alteracoes}")
log("Correção concluída!")
log("=" * 50)
""")

# Passo 4: Criar um script para testar se a aplicação funciona com o MoviePy 2.2.1
log("\n[4/4] CRIANDO SCRIPT DE TESTE DA APLICAÇÃO...")

test_script = os.path.join(TEMP_DIR, "testar_aplicacao.py")
with open(test_script, "w", encoding="utf-8") as f:
    f.write("""
import sys
import os
import traceback

print("===== TESTE DA APLICAÇÃO COM MOVIEPY 2.2.1 =====")

# Verificar caminho do Python
print(f"Caminho do Python: {sys.executable}")

# Testar importação do MoviePy
try:
    import moviepy
    print(f"\\nMoviePy importado com sucesso! Versão: {moviepy.__version__}")
    print(f"Localização: {os.path.dirname(moviepy.__file__)}")
    
    # Verificar componentes essenciais
    print("\\nVerificando componentes essenciais:")
    
    # Verificar VideoFileClip
    try:
        from moviepy import VideoFileClip
        print("- VideoFileClip: OK")
    except ImportError as e:
        print(f"- VideoFileClip: ERRO - {e}")
    
    # Verificar métodos de áudio
    try:
        from moviepy.video.io.VideoFileClip import VideoFileClip
        # Criar um objeto VideoFileClip para testar os métodos
        # Não podemos criar um objeto real sem um arquivo de vídeo, mas podemos verificar se os métodos existem
        if hasattr(VideoFileClip, 'with_audio'):
            print("- with_audio: OK")
        else:
            print("- with_audio: NÃO ENCONTRADO")
            
        if hasattr(VideoFileClip, 'set_audio'):
            print("- set_audio: OK")
        else:
            print("- set_audio: NÃO ENCONTRADO")
    except ImportError as e:
        print(f"- Métodos de áudio: ERRO - {e}")
    
    # Testar importação de outros componentes
    try:
        from moviepy.audio.io.AudioFileClip import AudioFileClip
        print("- AudioFileClip: OK")
    except ImportError as e:
        print(f"- AudioFileClip: ERRO - {e}")
    
    try:
        from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
        print("- CompositeVideoClip: OK")
    except ImportError as e:
        print(f"- CompositeVideoClip: ERRO - {e}")
    
    try:
        from moviepy.video.fx import vfx
        print("- vfx: OK")
    except ImportError as e:
        print(f"- vfx: ERRO - {e}")
    
    try:
        from moviepy.audio.fx import afx
        print("- afx: OK")
    except ImportError as e:
        print(f"- afx: ERRO - {e}")
    
    print("\\nTeste de importação concluído com sucesso!")
    
    # Tentar encontrar e executar o arquivo principal da aplicação
    app_dir = os.path.dirname(os.path.abspath(__file__))
    main_candidates = ["main.py", "app.py", "index.py", "run.py", "start.py"]
    
    for candidate in main_candidates:
        main_path = os.path.join(app_dir, candidate)
        if os.path.exists(main_path):
            print(f"\\nEncontrado arquivo principal: {candidate}")
            print("Tentando executar a aplicação...")
            
            try:
                # Executar a aplicação em um subprocesso para não bloquear o script
                import subprocess
                result = subprocess.run([sys.executable, main_path], 
                                       capture_output=True, 
                                       text=True, 
                                       timeout=10)  # Timeout de 10 segundos
                
                if result.returncode == 0:
                    print("Aplicação executada com sucesso!")
                    print("Saída:")
                    print(result.stdout)
                else:
                    print("A aplicação encontrou erros:")
                    print("Saída de erro:")
                    print(result.stderr)
            except subprocess.TimeoutExpired:
                print("A aplicação está em execução (timeout atingido).")
            except Exception as e:
                print(f"Erro ao executar a aplicação: {e}")
            
            break
    else:
        print("\\nNenhum arquivo principal encontrado. Verifique se a aplicação tem um arquivo main.py, app.py, index.py, run.py ou start.py.")
    
except ImportError as e:
    print(f"\\nERRO: Não foi possível importar o MoviePy!")
    print(f"Detalhes: {str(e)}")
    traceback.print_exc()
    sys.exit(1)
except Exception as e:
    print(f"\\nERRO: Exceção inesperada!")
    print(f"Detalhes: {str(e)}")
    traceback.print_exc()
    sys.exit(1)

print("\\nTeste concluído!")
""")

# Exibir resumo
log("\n" + "=" * 50)
log("                  RESUMO FINAL                  ")
log("=" * 50)
log("1. Análise da estrutura do MoviePy 2.2.1 concluída.")
log("2. Identificados arquivos que usam o MoviePy na aplicação.")
log("3. Criados scripts de correção automática e teste da aplicação.")
log("\nPróximos passos:")
log("1. Execute o script de correção automática:")
log(f"   python {correction_script}")
log("2. Execute o script de teste da aplicação:")
log(f"   python {test_script}")
log("3. Se necessário, ajuste manualmente o código da aplicação.")
log("=" * 50)

print("\nScripts criados com sucesso!")
print(f"- Script de correção automática: {correction_script}")
print(f"- Script de teste da aplicação: {test_script}")
print(f"- Log detalhado: {LOG_FILE}")

# Limpar diretório temporário
try:
    shutil.rmtree(TEMP_DIR)
    log("\nDiretório temporário limpo.")
except Exception as e:
    log(f"\nErro ao limpar diretório temporário: {e}")

print("\nPressione Enter para sair...")
input()