import sys
import os
import importlib.util

print("===== VERIFICAÇÃO DA INSTALAÇÃO DO MOVIEPY =====")

# Verificar caminho do Python
print(f"\nCaminho do Python: {sys.executable}")
print("Caminhos de importação:")
for path in sys.path:
    print(f"- {path}")

# Tentar importar MoviePy
try:
    import moviepy
    print(f"\n✓ MoviePy importado com sucesso!")
    print(f"Versão do MoviePy: {moviepy.__version__}")
    print(f"Localização do MoviePy: {os.path.dirname(moviepy.__file__)}")
    
    # Verificar conteúdo do diretório do MoviePy
    moviepy_dir = os.path.dirname(moviepy.__file__)
    print(f"\nConteúdo do diretório {moviepy_dir}:")
    if os.path.exists(moviepy_dir):
        for item in os.listdir(moviepy_dir):
            print(f"- {item}")
    else:
        print(f"⚠️  O diretório {moviepy_dir} não existe!")
    
    # Tentar importar submódulo editor
    try:
        from moviepy import editor
        print(f"\n✓ Submódulo 'editor' importado com sucesso!")
        
        # Verificar métodos essenciais
        has_with_audio = hasattr(editor, 'with_audio') or hasattr(editor.VideoFileClip, 'with_audio')
        has_set_audio = hasattr(editor, 'set_audio') or hasattr(editor.VideoFileClip, 'set_audio')
        
        print(f"\nVerificação de métodos essenciais:")
        print(f"- with_audio: {'✓ Disponível' if has_with_audio else '✗ Não encontrado'}")
        print(f"- set_audio: {'✓ Disponível' if has_set_audio else '✗ Não encontrado'}")
        
        print(f"\n✅ Instalação do MoviePy está funcionando corretamente!")
        print("✅ O submódulo 'editor' está disponível e pronto para uso.")
        print("✅ Você pode agora executar sua aplicação auto-video-producerV5-dev.")
        
    except ImportError as e:
        print(f"\n❌ ERRO: Não foi possível importar o submódulo 'editor'!")
        print(f"Detalhes do erro: {str(e)}")
        
        # Verificar se o arquivo editor.py existe
        editor_file = os.path.join(moviepy_dir, 'editor.py')
        if os.path.exists(editor_file):
            print(f"O arquivo editor.py existe em: {editor_file}")
        else:
            print(f"⚠️  O arquivo editor.py NÃO existe em: {editor_file}")
        
        print("\n❌ A instalação do MoviePy ainda está com problemas.")
        print("Sugestões:")
        print("1. Execute novamente o arquivo INSTALAR_MOVIEPY_FINAL.bat como ADMINISTRADOR")
        print("2. Certifique-se de fechar todos os processos Python antes da reinstalação")
        print("3. Verifique se há permissões suficientes para modificar os diretórios do Python")
    
except ImportError as e:
    print(f"\n❌ ERRO: Não foi possível importar o MoviePy!")
    print(f"Detalhes do erro: {str(e)}")
    
    # Verificar instalação via pip
    print("\nVerificando instalação via pip...")
    try:
        import subprocess
        result = subprocess.run([sys.executable, '-m', 'pip', 'list'], capture_output=True, text=True)
        if 'moviepy' in result.stdout:
            print("MoviePy está listado nas instalações do pip, mas não pode ser importado.")
            print("Isso indica um conflito de versões ou instalação corrompida.")
        else:
            print("MoviePy NÃO está listado nas instalações do pip.")
        
    except Exception as pip_error:
        print(f"Erro ao verificar instalações do pip: {str(pip_error)}")
    
    print("\n❌ A instalação do MoviePy falhou.")
    print("Sugestões:")
    print("1. Execute o arquivo INSTALAR_MOVIEPY_FINAL.bat como ADMINISTRADOR")
    print("2. Certifique-se de ter permissões suficientes")
    print("3. Verifique se o Python está corretamente instalado e configurado")

print("\n===== FIM DA VERIFICAÇÃO =====")