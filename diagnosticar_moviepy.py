import sys
import os

print("===== Diagnóstico do MoviePy =====")
print(f"Python executável: {sys.executable}")
print(f"Versão do Python: {sys.version}")
print(f"Caminho de instalação do Python: {sys.prefix}")

# Imprime todos os caminhos de importação
def print_import_paths():
    print("\n===== Caminhos de importação do Python =====")
    for i, path in enumerate(sys.path):
        print(f"{i}: {path}")

# Tenta importar o MoviePy e localizar seu caminho
def localizar_moviepy():
    print("\n===== Localizando instalações do MoviePy =====")
    
    try:
        # Remove do cache se já estiver importado
        if 'moviepy' in sys.modules:
            del sys.modules['moviepy']
        
        import moviepy
        print(f"MoviePy importado da localização: {moviepy.__file__}")
        print(f"Versão do MoviePy: {moviepy.__version__}")
        
        # Tenta importar o editor
        try:
            from moviepy import editor
            print(f"Módulo 'moviepy.editor' importado da localização: {editor.__file__}")
        except ImportError:
            print("❌ Não foi possível importar 'moviepy.editor'")
            
            # Procura por arquivos do editor no diretório do MoviePy
            moviepy_dir = os.path.dirname(moviepy.__file__)
            editor_path = os.path.join(moviepy_dir, 'editor.py')
            editor_dir = os.path.join(moviepy_dir, 'editor')
            
            print(f"\nVerificando diretórios no MoviePy:")
            print(f"Diretório base do MoviePy: {moviepy_dir}")
            print(f"Arquivo editor.py existe? {os.path.exists(editor_path)}")
            print(f"Diretório editor existe? {os.path.exists(editor_dir)}")
            
            # Lista os arquivos no diretório do MoviePy
            if os.path.exists(moviepy_dir):
                print("\nConteúdo do diretório do MoviePy:")
                for item in os.listdir(moviepy_dir):
                    item_path = os.path.join(moviepy_dir, item)
                    item_type = "diretório" if os.path.isdir(item_path) else "arquivo"
                    print(f"- {item} ({item_type})")
            
    except ImportError as e:
        print(f"❌ Erro ao importar MoviePy: {e}")
        
        # Procura por diretórios do MoviePy em todos os caminhos de importação
        print("\nProcurando por diretórios 'moviepy' nos caminhos de importação:")
        for path in sys.path:
            if os.path.exists(path):
                moviepy_path = os.path.join(path, 'moviepy')
                if os.path.exists(moviepy_path):
                    print(f"Encontrado em: {moviepy_path}")
                    print(f"   Tipo: {'diretório' if os.path.isdir(moviepy_path) else 'arquivo'}")

# Verifica a instalação do pip e do MoviePy
def verificar_pip():
    print("\n===== Verificando instalações via pip =====")
    try:
        # Executa pip list para verificar instalações
        print("\nExecutando: pip list | findstr moviepy")
        os.system(f'"{sys.executable}" -m pip list | findstr moviepy')
        
        print("\nExecutando: pip show moviepy")
        os.system(f'"{sys.executable}" -m pip show moviepy')
    except Exception as e:
        print(f"❌ Erro ao executar comando pip: {e}")

# Executa todos os testes
if __name__ == "__main__":
    print_import_paths()
    localizar_moviepy()
    verificar_pip()
    
    print("\n===== Fim do diagnóstico =====")
    print("Baseado nos resultados, podemos determinar onde está o problema e como corrigi-lo.")