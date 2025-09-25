# coding: utf-8
# Teste ultra simples do MoviePy - versão 2
import os

# Usando caminho absoluto para garantir que o arquivo seja salvo
log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'moviepy_ultra_test.txt')

with open(log_path, 'w', encoding='utf-8') as f:
    try:
        # Tentando importar MoviePy
        import moviepy
        f.write("MOVIEPY INSTALADO: True\n")
        
        # Tentando importar VideoFileClip
        try:
            from moviepy import VideoFileClip
            f.write("VIDEOFILECLIP IMPORTADO: True\n")
            
            # Verificando métodos
            has_with_audio = hasattr(VideoFileClip, 'with_audio')
            has_set_audio = hasattr(VideoFileClip, 'set_audio')
            f.write(f"HAS_WITH_AUDIO: {has_with_audio}\n")
            f.write(f"HAS_SET_AUDIO: {has_set_audio}\n")
        except Exception as e:
            f.write(f"VIDEOFILECLIP IMPORTADO: False - {str(e)}\n")
    except Exception as e:
        f.write(f"MOVIEPY INSTALADO: False - {str(e)}\n")
    
    # Verificando video_creation_service.py
    try:
        service_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'services', 'video_creation_service.py')
        if os.path.exists(service_path):
            with open(service_path, 'r', encoding='utf-8') as svc:
                content = svc.read()
                f.write(f"SET_AUDIO_NO_SERVICO: {'set_audio' in content}\n")
                f.write(f"WITH_AUDIO_NO_SERVICO: {'with_audio' in content}\n")
        else:
            f.write(f"VIDEO_CREATION_SERVICE: NAO_ENCONTRADO - {service_path}\n")
    except Exception as e:
        f.write(f"ERRO_VERIFICAR_SERVICO: {str(e)}\n")
    
print(f"Resultado do teste salvo em {log_path}")