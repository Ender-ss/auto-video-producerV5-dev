import sys
import os
import site
import shutil

print("===== Iniciando limpeza e reinstalação do MoviePy =====")
print(f"Usando Python: {sys.executable}")

# Localiza todos os diretórios de instalação do Python
print("\nLocalizando diretórios de instalação do Python...")
print(f"Python em: {sys.executable}")
print(f"Diretório de site-packages do Python: {site.getsitepackages()}")
print(f"Diretório de site-packages do usuário: {site.getusersitepackages()}")

# Função para remover diretórios do MoviePy
def remover_moviepy():
    print("\n===== Removendo todas as instalações do MoviePy =====")
    
    # Lista de caminhos para verificar
    caminhos = []
    
    # Adiciona site-packages globais e do usuário
    caminhos.extend(site.getsitepackages())
    caminhos.append(site.getusersitepackages())
    
    # Adiciona diretório local do projeto
    caminhos.append(os.path.join(os.getcwd(), 'Lib', 'site-packages'))
    
    # Adiciona diretórios virtuais
    venv_dir = os.path.join(os.getcwd(), '.venv', 'Lib', 'site-packages')
    if os.path.exists(venv_dir):
        caminhos.append(venv_dir)
    
    # Remove diretórios do MoviePy
    removidos = False
    for caminho in caminhos:
        if not os.path.exists(caminho):
            continue
            
        moviepy_dir = os.path.join(caminho, 'moviepy')
        moviepy_egg = None
        
        # Procura por arquivo .egg-info
        for item in os.listdir(caminho):
            if item.startswith('moviepy-') and item.endswith('.egg-info'):
                moviepy_egg = os.path.join(caminho, item)
                break
        
        # Remove diretórios e arquivos
        if os.path.exists(moviepy_dir):
            print(f"Removendo: {moviepy_dir}")
            try:
                shutil.rmtree(moviepy_dir)
                removidos = True
            except Exception as e:
                print(f"❌ Erro ao remover {moviepy_dir}: {e}")
        
        if moviepy_egg and os.path.exists(moviepy_egg):
            print(f"Removendo: {moviepy_egg}")
            try:
                if os.path.isdir(moviepy_egg):
                    shutil.rmtree(moviepy_egg)
                else:
                    os.remove(moviepy_egg)
                removidos = True
            except Exception as e:
                print(f"❌ Erro ao remover {moviepy_egg}: {e}")
    
    if not removidos:
        print("ℹ️  Nenhuma instalação do MoviePy encontrada para remoção.")
    else:
        print("✅ Limpeza concluída com sucesso!")

# Função para instalar o MoviePy corretamente
def instalar_moviepy_limpo():
    print("\n===== Instalando o MoviePy de forma limpa =====")
    
    # Instala as dependências essenciais primeiro
    dependencias = [
        'numpy==1.26.4',
        'pillow>=9.2.0',
        'decorator>=4.0.0',
        'proglog>=0.1.0',
        'tqdm>=4.11.0',
        'imageio>=2.5.0',
        'imageio-ffmpeg>=0.4.0'
    ]
    
    # Instala cada dependência
    for dep in dependencias:
        comando = f'"{sys.executable}" -m pip install {dep} --force-reinstall --no-cache-dir'
        print(f"\nExecutando: {comando}")
        os.system(comando)
    
    # Finalmente, instala o MoviePy
    comando_moviepy = f'"{sys.executable}" -m pip install moviepy==2.2.1 --force-reinstall --no-cache-dir'
    print(f"\nExecutando: {comando_moviepy}")
    os.system(comando_moviepy)

# Função para verificar a instalação final
def verificar_instalacao():
    print("\n===== Verificando a instalação final =====")
    
    # Remove o MoviePy do cache do importador
    if 'moviepy' in sys.modules:
        del sys.modules['moviepy']
    
    try:
        import moviepy
        print(f"✅ MoviePy importado com sucesso! Versão: {moviepy.__version__}")
        
        # Tentar importar o editor
        try:
            from moviepy.editor import VideoFileClip, AudioFileClip
            print("✅ Módulo moviepy.editor importado com sucesso!")
            print(f"✅ Método 'with_audio' existe: {'with_audio' in dir(VideoFileClip)}")
            print(f"✅ Método 'set_audio' existe: {'set_audio' in dir(VideoFileClip)}")
            
            print("\n🎉 Instalação concluída com SUCESSO! 🎉")
            print("O MoviePy está funcionando corretamente e o módulo 'moviepy.editor' está disponível.")
            print("Você pode agora executar sua pipeline de produção de vídeo.")
        except ImportError as e:
            print(f"❌ Erro ao importar moviepy.editor: {e}")
            print("\nSoluções sugeridas:")
            print("1. Execute este script como administrador")
            print("2. Verifique se todas as dependências estão instaladas")
            print("3. Tente reinstalar o MoviePy manualmente com:")
            print(f"   {sys.executable} -m pip install moviepy==2.2.1 --force-reinstall --no-cache-dir")
    except ImportError as e:
        print(f"❌ Erro fatal: {e}")
        print("\nO MoviePy não foi importado corretamente. Por favor, reinstale-o.")

# Executa o processo completo
if __name__ == "__main__":
    # Remover todas as instalações existentes do MoviePy
    remover_moviepy()
    
    # Instalar de forma limpa
    instalar_moviepy_limpo()
    
    # Verificar a instalação
    verificar_instalacao()
    
    print("\n===== Processo concluído =====")