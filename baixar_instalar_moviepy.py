import os
import sys
import subprocess
import tempfile
import shutil
import urllib.request
import zipfile

print("Baixando e instalando MoviePy 2.2.1 diretamente do GitHub...")

# URL para download do MoviePy 2.2.1 do GitHub
url = "https://github.com/Zulko/moviepy/archive/refs/tags/v2.2.1.zip"

# Criar diretório temporário
temp_dir = tempfile.mkdtemp()
print(f"Diretório temporário criado: {temp_dir}")

try:
    # Baixar o arquivo zip
    zip_path = os.path.join(temp_dir, "moviepy-2.2.1.zip")
    print(f"Baixando MoviePy 2.2.1 de {url}...")
    urllib.request.urlretrieve(url, zip_path)
    print("Download concluído!")
    
    # Extrair o arquivo zip
    print("Extraindo arquivos...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
    
    # Encontrar o diretório extraído
    extracted_dir = None
    for item in os.listdir(temp_dir):
        if item.startswith("moviepy-2.2.1"):
            extracted_dir = os.path.join(temp_dir, item)
            break
    
    if not extracted_dir:
        raise Exception("Não foi possível encontrar o diretório extraído do MoviePy")
    
    print(f"Diretório extraído: {extracted_dir}")
    
    # Verificar se o subdiretório editor existe
    editor_dir = os.path.join(extracted_dir, "moviepy", "editor")
    if os.path.exists(editor_dir):
        print(f"Subdiretório editor encontrado em: {editor_dir}")
    else:
        print(f"Subdiretório editor NÃO encontrado em: {editor_dir}")
    
    # Instalar o MoviePy a partir do código fonte
    print("Instalando MoviePy a partir do código fonte...")
    result = subprocess.run([
        sys.executable, "-m", "pip", "install", 
        "--force-reinstall", "--no-cache-dir", extracted_dir
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("Instalação concluída com sucesso!")
        print("Saída da instalação:")
        print(result.stdout)
    else:
        print("Erro durante a instalação!")
        print("Erro:")
        print(result.stderr)
        
finally:
    # Limpar o diretório temporário
    print("Limpando diretório temporário...")
    shutil.rmtree(temp_dir)
    print("Processo concluído!")