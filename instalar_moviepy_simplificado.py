import os
import sys
import subprocess
import shutil
import time
from datetime import datetime

# Configurações
target_version = "2.2.1"
log_file = "moviepy_simplificado_log.txt"

def log(message):
    """Registra mensagens no log e imprime no console"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"
    print(log_message)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_message + "\n")

def run_command(command, shell=True):
    """Executa um comando e retorna a saída e o código de erro"""
    try:
        result = subprocess.run(
            command, 
            shell=shell, 
            capture_output=True, 
            text=True
        )
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return "", str(e), 1

def check_admin():
    """Verifica se o script está sendo executado como administrador"""
    if os.name == 'nt':  # Windows
        try:
            # Código 0 se for admin, 1 se não
            subprocess.check_output(["net", "session"], stderr=subprocess.STDOUT, shell=True)
            return True
        except:
            return False
    return True  # No Linux/Mac, consideramos que tem permissões

def stop_python_processes():
    """Para todos os processos Python em execução"""
    log("Parando processos Python...")
    if os.name == 'nt':
        run_command("taskkill /F /IM python.exe >nul 2>&1")
        run_command("taskkill /F /IM pythonw.exe >nul 2>&1")
    log("Processos Python encerrados.")

def get_python_paths():
    """Obtém todos os caminhos de site-packages do Python"""
    python_paths = []
    
    # Adiciona caminhos comuns do site-packages
    username = os.environ.get('USERNAME', '')
    common_paths = [
        f"C:\\Users\\{username}\\AppData\\Roaming\\Python\\Python313\\site-packages",
        "C:\\Program Files\\Python313\\Lib\\site-packages",
        os.path.join(os.path.dirname(sys.executable), "Lib", "site-packages")
    ]
    
    # Adiciona caminhos do sys.path
    for path in sys.path:
        if path and os.path.exists(path) and "site-packages" in path:
            python_paths.append(path)
    
    # Adiciona caminhos comuns e remove duplicatas
    for path in common_paths:
        if path not in python_paths and os.path.exists(path):
            python_paths.append(path)
    
    return python_paths

def remove_moviepy(python_paths):
    """Remove manualmente todas as instalações do MoviePy"""
    log("Removendo instalações existentes do MoviePy...")
    
    # Primeiro tenta remover via pip
    log("Tentando remover via pip...")
    stdout, stderr, code = run_command(f"{sys.executable} -m pip uninstall -y moviepy")
    
    # Remove manualmente todos os vestígios
    for path in python_paths:
        if os.path.exists(path):
            log(f"Limpando diretório: {path}")
            
            # Remove diretório moviepy
            moviepy_dir = os.path.join(path, "moviepy")
            if os.path.exists(moviepy_dir):
                log(f"  - Removendo diretório: moviepy")
                try:
                    shutil.rmtree(moviepy_dir)
                    log("    - Removido com sucesso")
                except Exception as e:
                    log(f"    - Erro ao remover: {str(e)}")
            
            # Remove arquivos .egg-info e .dist-info
            for item in os.listdir(path):
                if (item.startswith("moviepy-") and 
                    (item.endswith(".egg-info") or item.endswith(".dist-info"))):
                    item_path = os.path.join(path, item)
                    log(f"  - Removendo: {item}")
                    try:
                        if os.path.isdir(item_path):
                            shutil.rmtree(item_path)
                        else:
                            os.remove(item_path)
                        log("    - Removido com sucesso")
                    except Exception as e:
                        log(f"    - Erro ao remover: {str(e)}")

def clean_pip_cache():
    """Limpa o cache do pip"""
    log("Limpando cache do pip...")
    run_command(f"{sys.executable} -m pip cache purge")

def update_pip():
    """Atualiza o pip para a versão mais recente"""
    log("Atualizando o pip...")
    stdout, stderr, code = run_command(f"{sys.executable} -m pip install --upgrade pip")
    if code == 0:
        log("Pip atualizado com sucesso.")
    else:
        log(f"Atenção: Não foi possível atualizar o pip: {stderr}")

def install_dependencies():
    """Instala as dependências necessárias para o MoviePy"""
    log("Instalando dependências essenciais...")
    dependencies = ["numpy", "imageio", "pillow", "decorator", "proglog", "tqdm"]
    stdout, stderr, code = run_command(
        f"{sys.executable} -m pip install --force-reinstall --no-cache-dir {' '.join(dependencies)}"
    )
    if code == 0:
        log("Dependências instaladas com sucesso.")
    else:
        log(f"Atenção: Erro na instalação de dependências: {stderr}")

def install_moviepy():
    """Instala a versão correta do MoviePy"""
    log(f"Instalando MoviePy versão {target_version}...")
    stdout, stderr, code = run_command(
        f"{sys.executable} -m pip install --force-reinstall --no-cache-dir moviepy=={target_version}"
    )
    if code == 0:
        log(f"MoviePy {target_version} instalado com sucesso!")
        return True
    else:
        log(f"Erro: Falha na instalação do MoviePy {target_version}: {stderr}")
        return False

def verify_moviepy():
    """Verifica se a instalação do MoviePy está funcionando corretamente"""
    log("Executando verificação do MoviePy...")
    
    try:
        # Cria um script de verificação
        verify_script = """import sys
import os
import moviepy
print(f"MoviePy versão: {moviepy.__version__}")
print(f"Localização: {os.path.dirname(moviepy.__file__)}")

# Verificar conteúdo do diretório
dir_content = os.listdir(os.path.dirname(moviepy.__file__))
print("Conteúdo do diretório:", ", ".join(dir_content))

# Verificar se editor.py existe
editor_path = os.path.join(os.path.dirname(moviepy.__file__), 'editor.py')
print(f"Editor.py existe: {os.path.exists(editor_path)}")

# Tentar importar editor
from moviepy import editor
print("Submódulo 'editor' importado com sucesso!")

# Verificar métodos essenciais
has_video = hasattr(editor, 'VideoFileClip')
has_with_audio = hasattr(editor, 'with_audio') or (hasattr(editor.VideoFileClip, 'with_audio') if has_video else False)
has_set_audio = hasattr(editor, 'set_audio') or (hasattr(editor.VideoFileClip, 'set_audio') if has_video else False)
print(f"VideoFileClip: {'✓' if has_video else '✗'}")
print(f"with_audio: {'✓' if has_with_audio else '✗'}")
print(f"set_audio: {'✓' if has_set_audio else '✗'}")

if has_video and has_with_audio and has_set_audio:
    sys.exit(0)  # Sucesso
else:
    sys.exit(1)  # Falha
"""
        
        with open("verify_moviepy_temp.py", "w", encoding="utf-8") as f:
            f.write(verify_script)
        
        # Executa o script de verificação
        stdout, stderr, code = run_command(f"{sys.executable} verify_moviepy_temp.py")
        log("\nResultado da verificação:\n" + stdout)
        
        # Remove o script temporário
        if os.path.exists("verify_moviepy_temp.py"):
            os.remove("verify_moviepy_temp.py")
        
        return code == 0
        
    except Exception as e:
        log(f"Erro durante a verificação: {str(e)}")
        return False

def main():
    """Função principal que executa todo o processo"""
    print("="*60)
    print("       SOLUÇÃO SIMPLIFICADA - MOVIEPY")
    print("="*60)
    print(f"Python: {sys.executable}")
    print(f"Versão-alvo: {target_version}")
    print("="*60)
    
    # Limpa log anterior
    if os.path.exists(log_file):
        os.remove(log_file)
    
    # Verifica permissões de administrador
    if not check_admin():
        log("ERRO: Execute este script como ADMINISTRADOR!")
        log("No Windows: clique com o botão direito no arquivo e selecione 'Executar como administrador'")
        input("Pressione Enter para sair...")
        return 1
    
    try:
        # Passo 1: Parar processos Python
        stop_python_processes()
        
        # Passo 2: Obter caminhos do Python
        python_paths = get_python_paths()
        log("\nDiretórios site-packages identificados:")
        for path in python_paths:
            log(f"- {path}")
        
        # Passo 3: Remover MoviePy existente
        remove_moviepy(python_paths)
        
        # Passo 4: Limpar cache do pip
        clean_pip_cache()
        
        # Passo 5: Atualizar pip
        update_pip()
        
        # Passo 6: Instalar dependências
        install_dependencies()
        
        # Passo 7: Instalar MoviePy
        if not install_moviepy():
            log("Falha na instalação do MoviePy.")
            return 1
        
        # Passo 8: Verificar instalação
        log("\n" + "="*60)
        if verify_moviepy():
            log("🎉 SUCESSO! A instalação do MoviePy está 100% funcionando!")
            log("✅ O submódulo 'editor' está totalmente disponível.")
            log("Você pode executar sua aplicação auto-video-producerV5-dev.")
        else:
            log("❌ FALHA! A instalação do MoviePy ainda está com problemas.")
            log("Sugestões:")
            log("1. Reinicie o computador e execute este script novamente como ADMINISTRADOR")
            log("2. Verifique as permissões de seus diretórios do Python")
            log(f"3. Consulte o arquivo de log para mais detalhes: {log_file}")
        log("="*60)
        
        return 0
        
    except Exception as e:
        log(f"Erro inesperado: {str(e)}")
        return 1
    finally:
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    sys.exit(main())