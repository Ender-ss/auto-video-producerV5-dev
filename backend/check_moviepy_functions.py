# coding: utf-8
import sys

def check_moviepy():
    try:
        # Tentar importar o MoviePy
        import moviepy
        print(f"MoviePy versão: {moviepy.__version__}")
        
        # Tentar importar VideoFileClip
        try:
            from moviepy import VideoFileClip
            print("VideoFileClip importado com sucesso!")
            
            # Verificar se o método with_audio existe
            has_with_audio = hasattr(VideoFileClip, 'with_audio')
            print(f"Método 'with_audio' está disponível: {has_with_audio}")
            
            # Verificar se o método set_audio existe
            has_set_audio = hasattr(VideoFileClip, 'set_audio')
            print(f"Método 'set_audio' está disponível: {has_set_audio}")
            
            # Salvar resultados em um arquivo
            with open('moviepy_functions_result.txt', 'w', encoding='utf-8') as f:
                f.write(f"MoviePy versão: {moviepy.__version__}\n")
                f.write(f"VideoFileClip importado: Sim\n")
                f.write(f"with_audio disponível: {has_with_audio}\n")
                f.write(f"set_audio disponível: {has_set_audio}\n")
                f.write("Verificação concluída com sucesso!\n")
        except ImportError as e:
            print(f"Erro ao importar VideoFileClip: {str(e)}")
            with open('moviepy_functions_result.txt', 'w', encoding='utf-8') as f:
                f.write(f"MoviePy versão: {moviepy.__version__}\n")
                f.write(f"Erro ao importar VideoFileClip: {str(e)}\n")
                
    except ImportError as e:
        print(f"Erro: MoviePy não está instalado. {str(e)}")
        with open('moviepy_functions_result.txt', 'w', encoding='utf-8') as f:
            f.write(f"Erro: MoviePy não está instalado. {str(e)}\n")
    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")
        with open('moviepy_functions_result.txt', 'w', encoding='utf-8') as f:
            f.write(f"Ocorreu um erro: {str(e)}\n")

if __name__ == "__main__":
    check_moviepy()