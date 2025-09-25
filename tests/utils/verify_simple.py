# Verifica se o MoviePy está instalado corretamente
try:
    import moviepy
    print(f"MoviePy importado com sucesso! Versão: {moviepy.__version__}")
    
    try:
        from moviepy.editor import VideoFileClip
        print("Módulo moviepy.editor importado com sucesso!")
        
        # Verifica se os métodos comuns existem
        print(f"Método 'with_audio' existe: {'with_audio' in dir(VideoFileClip)}")
        print(f"Método 'set_audio' existe: {'set_audio' in dir(VideoFileClip)}")
        
        # Verifica a versão do Python
        import sys
        print(f"Versão do Python: {sys.version}")
        
    except ImportError as e:
        print(f"Erro ao importar moviepy.editor: {e}")
        
except ImportError as e:
    print(f"Erro ao importar MoviePy: {e}")
    print("Execute: pip install moviepy")

print("Verificação concluída!")