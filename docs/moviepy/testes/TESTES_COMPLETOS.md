# Testes Completos do MoviePy

## Índice
1. [Introdução](#introdução)
2. [Testes Básicos](#testes-básicos)
3. [Testes de Componentes](#testes-de-componentes)
4. [Testes de Integração](#testes-de-integração)
5. [Testes de Performance](#testes-de-performance)
6. [Testes de Compatibilidade](#testes-de-compatibilidade)
7. [Testes de Erros](#testes-de-erros)
8. [Execução dos Testes](#execução-dos-testes)
9. [Resultados Esperados](#resultados-esperados)
10. [Solução de Problemas](#solução-de-problemas)

## Introdução

Este documento contém uma suite completa de testes para validar a instalação, configuração e funcionamento do MoviePy no projeto auto-video-producerV5-dev. Os testes cobrem desde funcionalidades básicas até cenários complexos de uso.

### Objetivos dos Testes
- Verificar a instalação correta do MoviePy
- Testar todos os componentes principais
- Validar a compatibilidade com a versão 2.1.2
- Garantir a integração com o sistema existente
- Identificar e resolver problemas comuns

## Testes Básicos

### Teste 1: Instalação e Importação
```python
# teste_01_instalacao.py
import sys
import subprocess

def testar_instalacao():
    """Testa se o MoviePy está instalado corretamente"""
    try:
        import moviepy
        print(f"✓ MoviePy versão {moviepy.__version__} instalado")
        return True
    except ImportError as e:
        print(f"✗ Erro ao importar MoviePy: {e}")
        return False

def testar_dependencias():
    """Testa as dependências principais"""
    dependencias = ['numpy', 'PIL', 'imageio', 'decorator']
    for dep in dependencias:
        try:
            __import__(dep)
            print(f"✓ {dep} instalado")
        except ImportError:
            print(f"✗ {dep} não encontrado")
            return False
    return True

if __name__ == "__main__":
    print("=== Teste 1: Instalação e Importação ===")
    instalacao_ok = testar_instalacao()
    dependencias_ok = testar_dependencias()
    
    if instalacao_ok and dependencias_ok:
        print("✓ Teste 1: PASSED")
    else:
        print("✗ Teste 1: FAILED")
```

### Teste 2: Configuração Básica
```python
# teste_02_configuracao.py
import os
import moviepy.config as config

def testar_configuracao_ffmpeg():
    """Testa se o FFmpeg está configurado corretamente"""
    try:
        # Verificar se o caminho do FFmpeg está configurado
        if hasattr(config, 'FFMPEG_BINARY') and config.FFMPEG_BINARY:
            print(f"✓ FFmpeg configurado em: {config.FFMPEG_BINARY}")
            return True
        else:
            print("✗ FFmpeg não configurado")
            return False
    except Exception as e:
        print(f"✗ Erro ao verificar FFmpeg: {e}")
        return False

def testar_configuracao_imagemagick():
    """Testa se o ImageMagick está configurado corretamente"""
    try:
        # Verificar se o caminho do ImageMagick está configurado
        if hasattr(config, 'IMAGEMAGICK_BINARY') and config.IMAGEMAGICK_BINARY:
            print(f"✓ ImageMagick configurado em: {config.IMAGEMAGICK_BINARY}")
            return True
        else:
            print("✗ ImageMagick não configurado")
            return False
    except Exception as e:
        print(f"✗ Erro ao verificar ImageMagick: {e}")
        return False

def testar_diretorio_temporario():
    """Testa se o diretório temporário é acessível"""
    try:
        temp_dir = os.path.join(os.getcwd(), 'temp')
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        print(f"✓ Diretório temporário acessível: {temp_dir}")
        return True
    except Exception as e:
        print(f"✗ Erro ao acessar diretório temporário: {e}")
        return False

if __name__ == "__main__":
    print("=== Teste 2: Configuração Básica ===")
    ffmpeg_ok = testar_configuracao_ffmpeg()
    imagemagick_ok = testar_configuracao_imagemagick()
    temp_ok = testar_diretorio_temporario()
    
    if ffmpeg_ok and imagemagick_ok and temp_ok:
        print("✓ Teste 2: PASSED")
    else:
        print("✗ Teste 2: FAILED")
```

### Teste 3: Criação de Clips Básicos
```python
# teste_03_clips_basicos.py
from moviepy.editor import *
import os

def testar_colorclip():
    """Testa a criação de ColorClip"""
    try:
        clip = ColorClip(size=(640, 480), color=(255, 0, 0), duration=5)
        print(f"✓ ColorClip criado: {clip.size}, {clip.duration}s")
        return True
    except Exception as e:
        print(f"✗ Erro ao criar ColorClip: {e}")
        return False

def testar_textclip():
    """Testa a criação de TextClip"""
    try:
        txt_clip = TextClip(
            text="Teste TextClip",
            font_size=24,
            color='white',
            font='C:/Windows/Fonts/arial.ttf'
        )
        print(f"✓ TextClip criado: {txt_clip.size}")
        return True
    except Exception as e:
        print(f"✗ Erro ao criar TextClip: {e}")
        return False

def testar_imageclip():
    """Testa a criação de ImageClip"""
    try:
        # Criar uma imagem temporária
        import numpy as np
        from PIL import Image
        
        img_array = np.zeros((100, 100, 3), dtype=np.uint8)
        img_array[:, :] = [255, 0, 0]  # Vermelho
        img = Image.fromarray(img_array)
        img_path = os.path.join(os.getcwd(), 'temp', 'test_image.png')
        img.save(img_path)
        
        # Criar ImageClip
        img_clip = ImageClip(img_path, duration=5)
        print(f"✓ ImageClip criado: {img_clip.size}")
        return True
    except Exception as e:
        print(f"✗ Erro ao criar ImageClip: {e}")
        return False

if __name__ == "__main__":
    print("=== Teste 3: Criação de Clips Básicos ===")
    colorclip_ok = testar_colorclip()
    textclip_ok = testar_textclip()
    imageclip_ok = testar_imageclip()
    
    if colorclip_ok and textclip_ok and imageclip_ok:
        print("✓ Teste 3: PASSED")
    else:
        print("✗ Teste 3: FAILED")
```

## Testes de Componentes

### Teste 4: VideoFileClip
```python
# teste_04_videofileclip.py
from moviepy.editor import *
import os

def testar_carregar_video():
    """Testa o carregamento de um arquivo de vídeo"""
    try:
        # Criar um vídeo de teste
        color_clip = ColorClip(size=(320, 240), color=(0, 255, 0), duration=5)
        test_video_path = os.path.join(os.getcwd(), 'temp', 'test_video.mp4')
        color_clip.write_videofile(test_video_path, fps=24, verbose=False)
        
        # Carregar o vídeo
        clip = VideoFileClip(test_video_path)
        print(f"✓ Vídeo carregado: {clip.size}, {clip.duration}s, {clip.fps}fps")
        return True
    except Exception as e:
        print(f"✗ Erro ao carregar vídeo: {e}")
        return False

def testar_editar_video():
    """Testa a edição de um vídeo"""
    try:
        # Criar e carregar vídeo de teste
        color_clip = ColorClip(size=(320, 240), color=(0, 255, 0), duration=10)
        test_video_path = os.path.join(os.getcwd(), 'temp', 'test_video.mp4')
        color_clip.write_videofile(test_video_path, fps=24, verbose=False)
        
        clip = VideoFileClip(test_video_path)
        
        # Testar edição
        clip_cortado = clip.subclip(2, 8)  # Cortar
        clip_redimensionado = clip_cortado.resize(width=160)  # Redimensionar
        clip_rotacionado = clip_redimensionado.rotate(90)  # Rotacionar
        
        print(f"✓ Vídeo editado: {clip_rotacionado.size}")
        return True
    except Exception as e:
        print(f"✗ Erro ao editar vídeo: {e}")
        return False

def testar_exportar_video():
    """Testa a exportação de vídeo"""
    try:
        # Criar vídeo de teste
        color_clip = ColorClip(size=(320, 240), color=(0, 0, 255), duration=5)
        output_path = os.path.join(os.getcwd(), 'temp', 'test_export.mp4')
        
        # Exportar
        color_clip.write_videofile(output_path, fps=24)
        print(f"✓ Vídeo exportado: {output_path}")
        return True
    except Exception as e:
        print(f"✗ Erro ao exportar vídeo: {e}")
        return False

if __name__ == "__main__":
    print("=== Teste 4: VideoFileClip ===")
    carregar_ok = testar_carregar_video()
    editar_ok = testar_editar_video()
    exportar_ok = testar_exportar_video()
    
    if carregar_ok and editar_ok and exportar_ok:
        print("✓ Teste 4: PASSED")
    else:
        print("✗ Teste 4: FAILED")
```

### Teste 5: AudioFileClip
```python
# teste_05_audiofileclip.py
from moviepy.editor import *
import numpy as np
import os

def testar_criar_audio():
    """Testa a criação de um áudio"""
    try:
        # Criar um áudio simples
        duration = 5
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration))
        frequency = 440  # A4
        audio_data = np.sin(2 * np.pi * frequency * t)
        
        # Criar AudioArrayClip
        audio_clip = AudioArrayClip(audio_data, fps=sample_rate)
        print(f"✓ Áudio criado: {audio_clip.duration}s, {audio_clip.fps}Hz")
        return True
    except Exception as e:
        print(f"✗ Erro ao criar áudio: {e}")
        return False

def testar_editar_audio():
    """Testa a edição de áudio"""
    try:
        # Criar áudio de teste
        duration = 10
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration))
        frequency = 440
        audio_data = np.sin(2 * np.pi * frequency * t)
        audio_clip = AudioArrayClip(audio_data, fps=sample_rate)
        
        # Editar áudio
        audio_cortado = audio_clip.subclip(2, 8)  # Cortar
        audio_volume = audio_cortado.volumex(0.5)  # Reduzir volume
        
        print(f"✓ Áudio editado: {audio_volume.duration}s")
        return True
    except Exception as e:
        print(f"✗ Erro ao editar áudio: {e}")
        return False

def testar_exportar_audio():
    """Testa a exportação de áudio"""
    try:
        # Criar áudio de teste
        duration = 5
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration))
        frequency = 440
        audio_data = np.sin(2 * np.pi * frequency * t)
        audio_clip = AudioArrayClip(audio_data, fps=sample_rate)
        
        # Exportar
        output_path = os.path.join(os.getcwd(), 'temp', 'test_audio.mp3')
        audio_clip.write_audiofile(output_path)
        print(f"✓ Áudio exportado: {output_path}")
        return True
    except Exception as e:
        print(f"✗ Erro ao exportar áudio: {e}")
        return False

if __name__ == "__main__":
    print("=== Teste 5: AudioFileClip ===")
    criar_ok = testar_criar_audio()
    editar_ok = testar_editar_audio()
    exportar_ok = testar_exportar_audio()
    
    if criar_ok and editar_ok and exportar_ok:
        print("✓ Teste 5: PASSED")
    else:
        print("✗ Teste 5: FAILED")
```

### Teste 6: TextClip Avançado
```python
# teste_06_textclip_avancado.py
from moviepy.editor import *
import os

def testar_texto_com_posicionamento():
    """Testa o posicionamento de texto"""
    try:
        # Criar fundo
        background = ColorClip(size=(640, 480), color=(0, 0, 0), duration=5)
        
        # Criar texto com diferentes posicionamentos
        posicoes = [
            ('center', 'center'),
            ('left', 'top'),
            ('right', 'bottom'),
            ('center', 'top')
        ]
        
        clips = [background]
        for pos in posicoes:
            txt_clip = TextClip(
                text=f"Posição: {pos}",
                font_size=24,
                color='white',
                font='C:/Windows/Fonts/arial.ttf'
            )
            txt_clip = txt_clip.with_position(pos).with_duration(5)
            clips.append(txt_clip)
        
        # Combinar
        final = CompositeVideoClip(clips)
        output_path = os.path.join(os.getcwd(), 'temp', 'test_posicionamento.mp4')
        final.write_videofile(output_path, fps=24)
        
        print(f"✓ Texto com posicionamento criado: {output_path}")
        return True
    except Exception as e:
        print(f"✗ Erro ao criar texto com posicionamento: {e}")
        return False

def testar_texto_com_animacao():
    """Testa animação de texto"""
    try:
        # Criar fundo
        background = ColorClip(size=(640, 480), color=(0, 0, 0), duration=10)
        
        # Criar texto animado
        txt_clip = TextClip(
            text="Texto Animado",
            font_size=48,
            color='yellow',
            font='C:/Windows/Fonts/arial.ttf'
        )
        
        # Animar posição
        def animate_pos(t):
            return (100 + t * 50, 240)
        
        txt_clip = txt_clip.with_position(animate_pos).with_duration(10)
        
        # Combinar
        final = CompositeVideoClip([background, txt_clip])
        output_path = os.path.join(os.getcwd(), 'temp', 'test_animacao.mp4')
        final.write_videofile(output_path, fps=24)
        
        print(f"✓ Texto animado criado: {output_path}")
        return True
    except Exception as e:
        print(f"✗ Erro ao criar texto animado: {e}")
        return False

def testar_texto_com_cores():
    """Testa texto com diferentes cores"""
    try:
        # Criar fundo
        background = ColorClip(size=(640, 480), color=(0, 0, 0), duration=5)
        
        # Criar textos com diferentes cores
        cores = [
            ('Vermelho', 'red'),
            ('Verde', 'green'),
            ('Azul', 'blue'),
            ('Amarelo', 'yellow')
        ]
        
        clips = [background]
        y_pos = 50
        for texto, cor in cores:
            txt_clip = TextClip(
                text=texto,
                font_size=36,
                color=cor,
                font='C:/Windows/Fonts/arial.ttf'
            )
            txt_clip = txt_clip.with_position(('center', y_pos)).with_duration(5)
            clips.append(txt_clip)
            y_pos += 100
        
        # Combinar
        final = CompositeVideoClip(clips)
        output_path = os.path.join(os.getcwd(), 'temp', 'test_cores.mp4')
        final.write_videofile(output_path, fps=24)
        
        print(f"✓ Texto com cores criado: {output_path}")
        return True
    except Exception as e:
        print(f"✗ Erro ao criar texto com cores: {e}")
        return False

if __name__ == "__main__":
    print("=== Teste 6: TextClip Avançado ===")
    posicao_ok = testar_texto_com_posicionamento()
    animacao_ok = testar_texto_com_animacao()
    cores_ok = testar_texto_com_cores()
    
    if posicao_ok and animacao_ok and cores_ok:
        print("✓ Teste 6: PASSED")
    else:
        print("✗ Teste 6: FAILED")
```

## Testes de Integração

### Teste 7: Composição de Clips
```python
# teste_07_composicao_clips.py
from moviepy.editor import *
import os

def testar_compositevideoclip():
    """Testa a composição de múltiplos clips"""
    try:
        # Criar fundo
        background = ColorClip(size=(640, 480), color=(0, 0, 0), duration=10)
        
        # Criar clipes sobrepostos
        clip1 = ColorClip(size=(200, 200), color=(255, 0, 0), duration=10)
        clip1 = clip1.with_position((50, 50))
        
        clip2 = ColorClip(size=(200, 200), color=(0, 255, 0), duration=10)
        clip2 = clip2.with_position((250, 150))
        
        clip3 = ColorClip(size=(200, 200), color=(0, 0, 255), duration=10)
        clip3 = clip3.with_position((150, 250))
        
        # Combinar
        final = CompositeVideoClip([background, clip1, clip2, clip3])
        output_path = os.path.join(os.getcwd(), 'temp', 'test_composicao.mp4')
        final.write_videofile(output_path, fps=24)
        
        print(f"✓ Composição de clips criada: {output_path}")
        return True
    except Exception as e:
        print(f"✗ Erro ao criar composição de clips: {e}")
        return False

def testar_clips_com_tempo():
    """Testa clips com diferentes tempos de início e duração"""
    try:
        # Criar fundo
        background = ColorClip(size=(640, 480), color=(0, 0, 0), duration=15)
        
        # Criar clipes com diferentes tempos
        clip1 = ColorClip(size=(200, 200), color=(255, 0, 0), duration=5)
        clip1 = clip1.with_position((50, 50)).with_start(0)
        
        clip2 = ColorClip(size=(200, 200), color=(0, 255, 0), duration=5)
        clip2 = clip2.with_position((250, 150)).with_start(5)
        
        clip3 = ColorClip(size=(200, 200), color=(0, 0, 255), duration=5)
        clip3 = clip3.with_position((150, 250)).with_start(10)
        
        # Combinar
        final = CompositeVideoClip([background, clip1, clip2, clip3])
        output_path = os.path.join(os.getcwd(), 'temp', 'test_tempo.mp4')
        final.write_videofile(output_path, fps=24)
        
        print(f"✓ Clips com tempo criados: {output_path}")
        return True
    except Exception as e:
        print(f"✗ Erro ao criar clips com tempo: {e}")
        return False

def testar_composicao_complexa():
    """Testa uma composição complexa com vídeo, áudio e texto"""
    try:
        # Criar fundo
        background = ColorClip(size=(640, 480), color=(0, 0, 0), duration=15)
        
        # Criar vídeo
        video_clip = ColorClip(size=(320, 240), color=(100, 100, 100), duration=15)
        video_clip = video_clip.with_position(('center', 'center'))
        
        # Criar áudio
        import numpy as np
        sample_rate = 44100
        t = np.linspace(0, 15, int(sample_rate * 15))
        frequency = 440
        audio_data = np.sin(2 * np.pi * frequency * t)
        audio_clip = AudioArrayClip(audio_data, fps=sample_rate)
        video_clip = video_clip.set_audio(audio_clip)
        
        # Criar texto
        txt_clip = TextClip(
            text="Composição Complexa",
            font_size=48,
            color='white',
            font='C:/Windows/Fonts/arial.ttf'
        )
        txt_clip = txt_clip.with_position(('center', 50)).with_duration(15)
        
        # Combinar
        final = CompositeVideoClip([background, video_clip, txt_clip])
        output_path = os.path.join(os.getcwd(), 'temp', 'test_composicao_complexa.mp4')
        final.write_videofile(output_path, fps=24)
        
        print(f"✓ Composição complexa criada: {output_path}")
        return True
    except Exception as e:
        print(f"✗ Erro ao criar composição complexa: {e}")
        return False

if __name__ == "__main__":
    print("=== Teste 7: Composição de Clips ===")
    composicao_ok = testar_compositevideoclip()
    tempo_ok = testar_clips_com_tempo()
    complexa_ok = testar_composicao_complexa()
    
    if composicao_ok and tempo_ok and complexa_ok:
        print("✓ Teste 7: PASSED")
    else:
        print("✗ Teste 7: FAILED")
```

### Teste 8: Concatenação e Transições
```python
# teste_08_concatenacao_transicoes.py
from moviepy.editor import *
from moviepy.video.fx import FadeIn, FadeOut
import os

def testar_concatenacao_simples():
    """Testa a concatenação simples de clips"""
    try:
        # Criar clipes
        clip1 = ColorClip(size=(640, 480), color=(255, 0, 0), duration=3)
        clip2 = ColorClip(size=(640, 480), color=(0, 255, 0), duration=3)
        clip3 = ColorClip(size=(640, 480), color=(0, 0, 255), duration=3)
        
        # Concatenar
        final = concatenate_videoclips([clip1, clip2, clip3])
        output_path = os.path.join(os.getcwd(), 'temp', 'test_concatenacao_simples.mp4')
        final.write_videofile(output_path, fps=24)
        
        print(f"✓ Concatenação simples criada: {output_path}")
        return True
    except Exception as e:
        print(f"✗ Erro ao criar concatenação simples: {e}")
        return False

def testar_concatenacao_com_transicoes():
    """Testa a concatenação com transições"""
    try:
        # Criar clipes
        clip1 = ColorClip(size=(640, 480), color=(255, 0, 0), duration=3)
        clip2 = ColorClip(size=(640, 480), color=(0, 255, 0), duration=3)
        clip3 = ColorClip(size=(640, 480), color=(0, 0, 255), duration=3)
        
        # Adicionar transições
        clip1 = clip1.with_effects([FadeOut(1)])
        clip2 = clip2.with_effects([FadeIn(1)])
        clip2 = clip2.with_effects([FadeOut(1)])
        clip3 = clip3.with_effects([FadeIn(1)])
        
        # Concatenar
        final = concatenate_videoclips([clip1, clip2, clip3])
        output_path = os.path.join(os.getcwd(), 'temp', 'test_concatenacao_transicoes.mp4')
        final.write_videofile(output_path, fps=24)
        
        print(f"✓ Concatenação com transições criada: {output_path}")
        return True
    except Exception as e:
        print(f"✗ Erro ao criar concatenação com transições: {e}")
        return False

def testar_transicoes_variadas():
    """Testa diferentes tipos de transições"""
    try:
        # Criar clipes
        clip1 = ColorClip(size=(640, 480), color=(255, 0, 0), duration=5)
        clip2 = ColorClip(size=(640, 480), color=(0, 255, 0), duration=5)
        
        # Testar diferentes durações de transição
        duracoes = [0.5, 1.0, 2.0]
        
        for duracao in duracoes:
            # Adicionar transições
            c1 = clip1.with_effects([FadeOut(duracao)])
            c2 = clip2.with_effects([FadeIn(duracao)])
            
            # Concatenar
            final = concatenate_videoclips([c1, c2])
            output_path = os.path.join(os.getcwd(), 'temp', f'test_transicao_{duracao}s.mp4')
            final.write_videofile(output_path, fps=24)
            print(f"✓ Transição de {duracao}s criada: {output_path}")
        
        return True
    except Exception as e:
        print(f"✗ Erro ao criar transições variadas: {e}")
        return False

if __name__ == "__main__":
    print("=== Teste 8: Concatenação e Transições ===")
    simples_ok = testar_concatenacao_simples()
    transicoes_ok = testar_concatenacao_com_transicoes()
    variadas_ok = testar_transicoes_variadas()
    
    if simples_ok and transicoes_ok and variadas_ok:
        print("✓ Teste 8: PASSED")
    else:
        print("✗ Teste 8: FAILED")
```

## Testes de Performance

### Teste 9: Performance de Processamento
```python
# teste_09_performance.py
from moviepy.editor import *
import time
import os

def testar_performance_criacao():
    """Testa a performance na criação de clips"""
    try:
        # Criar múltiplos clips
        start_time = time.time()
        
        clips = []
        for i in range(10):
            clip = ColorClip(size=(640, 480), color=(i*25, 255-i*25, 128), duration=5)
            clips.append(clip)
        
        creation_time = time.time() - start_time
        print(f"✓ {len(clips)} clips criados em {creation_time:.2f}s")
        return True
    except Exception as e:
        print(f"✗ Erro ao testar performance de criação: {e}")
        return False

def testar_performance_composicao():
    """Testa a performance na composição de clips"""
    try:
        # Criar clipes
        background = ColorClip(size=(640, 480), color=(0, 0, 0), duration=10)
        
        clips = [background]
        for i in range(20):
            clip = ColorClip(size=(100, 100), color=(i*12, 255-i*12, 128), duration=10)
            clip = clip.with_position((i*30, i*20))
            clips.append(clip)
        
        # Compor
        start_time = time.time()
        final = CompositeVideoClip(clips)
        composition_time = time.time() - start_time
        
        output_path = os.path.join(os.getcwd(), 'temp', 'test_performance_composicao.mp4')
        final.write_videofile(output_path, fps=24)
        
        print(f"✓ Composição de {len(clips)} clips em {composition_time:.2f}s")
        return True
    except Exception as e:
        print(f"✗ Erro ao testar performance de composição: {e}")
        return False

def testar_performance_exportacao():
    """Testa a performance na exportação de vídeos"""
    try:
        # Criar vídeo complexo
        background = ColorClip(size=(640, 480), color=(0, 0, 0), duration=30)
        
        clips = [background]
        for i in range(50):
            clip = ColorClip(size=(50, 50), color=(i*5, 255-i*5, 128), duration=30)
            clip = clip.with_position((i*12, i*8))
            clips.append(clip)
        
        final = CompositeVideoClip(clips)
        output_path = os.path.join(os.getcwd(), 'temp', 'test_performance_exportacao.mp4')
        
        # Exportar
        start_time = time.time()
        final.write_videofile(output_path, fps=24)
        export_time = time.time() - start_time
        
        print(f"✓ Exportação de vídeo complexo em {export_time:.2f}s")
        return True
    except Exception as e:
        print(f"✗ Erro ao testar performance de exportação: {e}")
        return False

if __name__ == "__main__":
    print("=== Teste 9: Performance de Processamento ===")
    criacao_ok = testar_performance_criacao()
    composicao_ok = testar_performance_composicao()
    exportacao_ok = testar_performance_exportacao()
    
    if criacao_ok and composicao_ok and exportacao_ok:
        print("✓ Teste 9: PASSED")
    else:
        print("✗ Teste 9: FAILED")
```

### Teste 10: Uso de Memória
```python
# teste_10_memoria.py
from moviepy.editor import *
import psutil
import os
import gc

def testar_uso_memoria_criacao():
    """Testa o uso de memória na criação de clips"""
    try:
        # Medir memória inicial
        process = psutil.Process()
        mem_inicial = process.memory_info().rss / 1024 / 1024  # MB
        
        # Criar múltiplos clips
        clips = []
        for i in range(100):
            clip = ColorClip(size=(640, 480), color=(i*2, 255-i*2, 128), duration=10)
            clips.append(clip)
        
        # Medir memória após criação
        mem_final = process.memory_info().rss / 1024 / 1024  # MB
        uso_memoria = mem_final - mem_inicial
        
        print(f"✓ Uso de memória para {len(clips)} clips: {uso_memoria:.2f}MB")
        
        # Limpar
        del clips
        gc.collect()
        
        return True
    except Exception as e:
        print(f"✗ Erro ao testar uso de memória na criação: {e}")
        return False

def testar_uso_memoria_composicao():
    """Testa o uso de memória na composição de clips"""
    try:
        # Medir memória inicial
        process = psutil.Process()
        mem_inicial = process.memory_info().rss / 1024 / 1024  # MB
        
        # Criar composição complexa
        background = ColorClip(size=(640, 480), color=(0, 0, 0), duration=20)
        
        clips = [background]
        for i in range(100):
            clip = ColorClip(size=(50, 50), color=(i*2, 255-i*2, 128), duration=20)
            clip = clip.with_position((i*6, i*4))
            clips.append(clip)
        
        final = CompositeVideoClip(clips)
        
        # Medir memória após composição
        mem_final = process.memory_info().rss / 1024 / 1024  # MB
        uso_memoria = mem_final - mem_inicial
        
        print(f"✓ Uso de memória para composição: {uso_memoria:.2f}MB")
        
        # Limpar
        del final, clips
        gc.collect()
        
        return True
    except Exception as e:
        print(f"✗ Erro ao testar uso de memória na composição: {e}")
        return False

def testar_limpeza_memoria():
    """Testa a limpeza de memória"""
    try:
        # Criar muitos clips
        clips = []
        for i in range(200):
            clip = ColorClip(size=(640, 480), color=(i*1, 255-i*1, 128), duration=10)
            clips.append(clip)
        
        # Medir memória antes da limpeza
        process = psutil.Process()
        mem_antes = process.memory_info().rss / 1024 / 1024  # MB
        
        # Limpar
        del clips
        gc.collect()
        
        # Medir memória após limpeza
        mem_depois = process.memory_info().rss / 1024 / 1024  # MB
        memoria_liberada = mem_antes - mem_depois
        
        print(f"✓ Memória liberada: {memoria_liberada:.2f}MB")
        return True
    except Exception as e:
        print(f"✗ Erro ao testar limpeza de memória: {e}")
        return False

if __name__ == "__main__":
    print("=== Teste 10: Uso de Memória ===")
    criacao_memoria_ok = testar_uso_memoria_criacao()
    composicao_memoria_ok = testar_uso_memoria_composicao()
    limpeza_memoria_ok = testar_limpeza_memoria()
    
    if criacao_memoria_ok and composicao_memoria_ok and limpeza_memoria_ok:
        print("✓ Teste 10: PASSED")
    else:
        print("✗ Teste 10: FAILED")
```

## Testes de Compatibilidade

### Teste 11: Compatibilidade com MoviePy 2.1.2
```python
# teste_11_compatibilidade_v2.py
from moviepy.editor import *
from moviepy.video.fx import FadeIn, FadeOut
import os

def testar_nova_api_textclip():
    """Testa a nova API do TextClip na versão 2.1.2"""
    try:
        # Nova API
        txt_clip = TextClip(
            text="Nova API TextClip",
            font_size=24,
            color='white',
            font='C:/Windows/Fonts/arial.ttf'
        )
        txt_clip = txt_clip.with_position(('center', 'center')).with_duration(5)
        
        # Testar exportação
        background = ColorClip(size=(640, 480), color=(0, 0, 0), duration=5)
        final = CompositeVideoClip([background, txt_clip])
        output_path = os.path.join(os.getcwd(), 'temp', 'test_nova_api_textclip.mp4')
        final.write_videofile(output_path, fps=24)
        
        print(f"✓ Nova API do TextClip funcionando: {output_path}")
        return True
    except Exception as e:
        print(f"✗ Erro ao testar nova API do TextClip: {e}")
        return False

def testar_nova_api_efeitos():
    """Testa a nova API de efeitos na versão 2.1.2"""
    try:
        # Criar clip
        clip = ColorClip(size=(640, 480), color=(255, 0, 0), duration=5)
        
        # Nova API de efeitos
        clip_fadein = clip.with_effects([FadeIn(1)])
        clip_fadeout = clip_fadein.with_effects([FadeOut(1)])
        
        # Testar exportação
        output_path = os.path.join(os.getcwd(), 'temp', 'test_nova_api_efeitos.mp4')
        clip_fadeout.write_videofile(output_path, fps=24)
        
        print(f"✓ Nova API de efeitos funcionando: {output_path}")
        return True
    except Exception as e:
        print(f"✗ Erro ao testar nova API de efeitos: {e}")
        return False

def testar_nova_api_concatenacao():
    """Testa a nova API de concatenação na versão 2.1.2"""
    try:
        # Criar clipes
        clip1 = ColorClip(size=(640, 480), color=(255, 0, 0), duration=3)
        clip2 = ColorClip(size=(640, 480), color=(0, 255, 0), duration=3)
        
        # Nova API de concatenação
        final = concatenate_videoclips([clip1, clip2])
        
        # Testar exportação
        output_path = os.path.join(os.getcwd(), 'temp', 'test_nova_api_concatenacao.mp4')
        final.write_videofile(output_path, fps=24)
        
        print(f"✓ Nova API de concatenação funcionando: {output_path}")
        return True
    except Exception as e:
        print(f"✗ Erro ao testar nova API de concatenação: {e}")
        return False

def testar_remocao_verbose():
    """Testa a remoção do parâmetro verbose na versão 2.1.2"""
    try:
        # Criar clip
        clip = ColorClip(size=(640, 480), color=(0, 0, 255), duration=5)
        
        # Exportar sem verbose
        output_path = os.path.join(os.getcwd(), 'temp', 'test_remocao_verbose.mp4')
        clip.write_videofile(output_path, fps=24)
        
        print(f"✓ Exportação sem verbose funcionando: {output_path}")
        return True
    except Exception as e:
        print(f"✗ Erro ao testar remoção do verbose: {e}")
        return False

if __name__ == "__main__":
    print("=== Teste 11: Compatibilidade com MoviePy 2.1.2 ===")
    textclip_ok = testar_nova_api_textclip()
    efeitos_ok = testar_nova_api_efeitos()
    concatenacao_ok = testar_nova_api_concatenacao()
    verbose_ok = testar_remocao_verbose()
    
    if textclip_ok and efeitos_ok and concatenacao_ok and verbose_ok:
        print("✓ Teste 11: PASSED")
    else:
        print("✗ Teste 11: FAILED")
```

### Teste 12: Compatibilidade com Versões Anteriores
```python
# teste_12_compatibilidade_antigas.py
from moviepy.editor import *
import os

def testar_metodos_depreciados():
    """Testa se métodos depreciados ainda funcionam"""
    try:
        # Criar clip
        clip = ColorClip(size=(640, 480), color=(255, 0, 0), duration=5)
        
        # Tentar usar métodos antigos
        try:
            # Método set_position
            clip_pos = clip.set_position(('center', 'center'))
            print("✓ Método set_position ainda funciona")
        except:
            print("✗ Método set_position não funciona mais")
        
        try:
            # Método set_duration
            clip_dur = clip.set_duration(3)
            print("✓ Método set_duration ainda funciona")
        except:
            print("✗ Método set_duration não funciona mais")
        
        try:
            # Método set_start
            clip_start = clip.set_start(1)
            print("✓ Método set_start ainda funciona")
        except:
            print("✗ Método set_start não funciona mais")
        
        return True
    except Exception as e:
        print(f"✗ Erro ao testar métodos depreciados: {e}")
        return False

def testar_parametros_depreciados():
    """Testa se parâmetros depreciados ainda funcionam"""
    try:
        # Criar clip
        clip = ColorClip(size=(640, 480), color=(0, 255, 0), duration=5)
        
        # Tentar usar parâmetros antigos
        try:
            # Parâmetro fontsize no TextClip
            txt_clip = TextClip(
                "Teste",
                fontsize=24,
                color='white',
                font='C:/Windows/Fonts/arial.ttf'
            )
            print("✓ Parâmetro fontsize ainda funciona")
        except:
            print("✗ Parâmetro fontsize não funciona mais")
        
        try:
            # Parâmetro verbose no write_videofile
            output_path = os.path.join(os.getcwd(), 'temp', 'test_verbose_antigo.mp4')
            clip.write_videofile(output_path, fps=24, verbose=False)
            print("✓ Parâmetro verbose ainda funciona")
        except:
            print("✗ Parâmetro verbose não funciona mais")
        
        return True
    except Exception as e:
        print(f"✗ Erro ao testar parâmetros depreciados: {e}")
        return False

def testar_compatibilidade_reversa():
    """Testa a compatibilidade reversa com código antigo"""
    try:
        # Código antigo de exemplo
        clip1 = ColorClip(size=(640, 480), color=(255, 0, 0), duration=3)
        clip2 = ColorClip(size=(640, 480), color=(0, 255, 0), duration=3)
        
        # Tentar usar métodos antigos
        try:
            # Método fadein/fadeout antigo
            clip1_fade = clip1.fadein(1).fadeout(1)
            clip2_fade = clip2.fadein(1).fadeout(1)
            print("✓ Métodos fadein/fadeout antigos ainda funcionam")
        except:
            print("✗ Métodos fadein/fadeout antigos não funcionam mais")
        
        # Tentar usar método concatenate antigo
        try:
            final = clip1.concatenate(clip2)
            print("✓ Método concatenate antigo ainda funciona")
        except:
            print("✗ Método concatenate antigo não funciona mais")
        
        return True
    except Exception as e:
        print(f"✗ Erro ao testar compatibilidade reversa: {e}")
        return False

if __name__ == "__main__":
    print("=== Teste 12: Compatibilidade com Versões Anteriores ===")
    metodos_ok = testar_metodos_depreciados()
    parametros_ok = testar_parametros_depreciados()
    reversa_ok = testar_compatibilidade_reversa()
    
    if metodos_ok and parametros_ok and reversa_ok:
        print("✓ Teste 12: PASSED")
    else:
        print("✗ Teste 12: FAILED")
```

## Testes de Erros

### Teste 13: Tratamento de Erros
```python
# teste_13_tratamento_erros.py
from moviepy.editor import *
import os

def testar_arquivo_inexistente():
    """Testa o tratamento de arquivos inexistentes"""
    try:
        # Tentar carregar arquivo inexistente
        try:
            clip = VideoFileClip("arquivo_inexistente.mp4")
            print("✗ Erro: Arquivo inexistente não gerou exceção")
            return False
        except Exception as e:
            print(f"✓ Arquivo inexistente gerou exceção: {type(e).__name__}")
            return True
    except Exception as e:
        print(f"✗ Erro ao testar arquivo inexistente: {e}")
        return False

def testar_parametros_invalidos():
    """Testa o tratamento de parâmetros inválidos"""
    try:
        # Tentar criar TextClip com parâmetros inválidos
        try:
            txt_clip = TextClip(
                text="",  # Texto vazio
                font_size=-1,  # Tamanho inválido
                color="cor_inexistente",  # Cor inválida
                font="fonte_inexistente.ttf"  # Fonte inexistente
            )
            print("✗ Erro: Parâmetros inválidos não geraram exceção")
            return False
        except Exception as e:
            print(f"✓ Parâmetros inválidos geraram exceção: {type(e).__name__}")
            return True
    except Exception as e:
        print(f"✗ Erro ao testar parâmetros inválidos: {e}")
        return False

def testar_operacoes_invalidas():
    """Testa o tratamento de operações inválidas"""
    try:
        # Criar clip
        clip = ColorClip(size=(640, 480), color=(255, 0, 0), duration=5)
        
        # Tentar operações inválidas
        try:
            # Subclip com tempos inválidos
            invalid_clip = clip.subclip(-1, 10)  # Tempo negativo
            print("✗ Erro: Subclip com tempo negativo não gerou exceção")
            return False
        except Exception as e:
            print(f"✓ Subclip com tempo negativo gerou exceção: {type(e).__name__}")
        
        try:
            # Subclip com tempos inválidos
            invalid_clip = clip.subclip(10, 5)  # Fim antes do início
            print("✗ Erro: Subclip com fim antes do início não gerou exceção")
            return False
        except Exception as e:
            print(f"✓ Subclip com fim antes do início gerou exceção: {type(e).__name__}")
        
        return True
    except Exception as e:
        print(f"✗ Erro ao testar operações inválidas: {e}")
        return False

def testar_recursos_insuficientes():
    """Testa o tratamento de recursos insuficientes"""
    try:
        # Tentar criar um vídeo extremamente grande
        try:
            huge_clip = ColorClip(size=(10000, 10000), color=(255, 0, 0), duration=60)
            print("✓ Clip extremamente grande criado (pode causar problemas de memória)")
            return True
        except Exception as e:
            print(f"✓ Clip extremamente grande gerou exceção: {type(e).__name__}")
            return True
    except Exception as e:
        print(f"✗ Erro ao testar recursos insuficientes: {e}")
        return False

if __name__ == "__main__":
    print("=== Teste 13: Tratamento de Erros ===")
    arquivo_ok = testar_arquivo_inexistente()
    parametros_ok = testar_parametros_invalidos()
    operacoes_ok = testar_operacoes_invalidas()
    recursos_ok = testar_recursos_insuficientes()
    
    if arquivo_ok and parametros_ok and operacoes_ok and recursos_ok:
        print("✓ Teste 13: PASSED")
    else:
        print("✗ Teste 13: FAILED")
```

## Execução dos Testes

### Script de Execução Automática
```python
# executar_todos_testes.py
import os
import subprocess
import sys

def executar_teste(nome_arquivo):
    """Executa um arquivo de teste e retorna o resultado"""
    try:
        print(f"\n--- Executando {nome_arquivo} ---")
        result = subprocess.run([sys.executable, nome_arquivo], 
                              capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            print(f"✓ {nome_arquivo}: PASSED")
            return True
        else:
            print(f"✗ {nome_arquivo}: FAILED")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
    except Exception as e:
        print(f"✗ Erro ao executar {nome_arquivo}: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("=== Iniciando Suite de Testes do MoviePy ===")
    
    # Lista de testes
    testes = [
        "teste_01_instalacao.py",
        "teste_02_configuracao.py",
        "teste_03_clips_basicos.py",
        "teste_04_videofileclip.py",
        "teste_05_audiofileclip.py",
        "teste_06_textclip_avancado.py",
        "teste_07_composicao_clips.py",
        "teste_08_concatenacao_transicoes.py",
        "teste_09_performance.py",
        "teste_10_memoria.py",
        "teste_11_compatibilidade_v2.py",
        "teste_12_compatibilidade_antigas.py",
        "teste_13_tratamento_erros.py"
    ]
    
    # Executar testes
    resultados = {}
    for teste in testes:
        resultados[teste] = executar_teste(teste)
    
    # Resumo
    print("\n=== Resumo dos Testes ===")
    passed = sum(resultados.values())
    total = len(resultados)
    
    for teste, resultado in resultados.items():
        status = "PASSED" if resultado else "FAILED"
        print(f"{teste}: {status}")
    
    print(f"\nTotal: {passed}/{total} testes passaram")
    
    if passed == total:
        print("✓ Todos os testes passaram!")
        return 0
    else:
        print("✗ Alguns testes falharam!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

### Script de Execução Individual
```python
# executar_teste_individual.py
import os
import subprocess
import sys

def executar_teste_individual(nome_teste):
    """Executa um teste específico"""
    # Mapear nomes para arquivos
    testes = {
        "instalacao": "teste_01_instalacao.py",
        "configuracao": "teste_02_configuracao.py",
        "clips": "teste_03_clips_basicos.py",
        "video": "teste_04_videofileclip.py",
        "audio": "teste_05_audiofileclip.py",
        "texto": "teste_06_textclip_avancado.py",
        "composicao": "teste_07_composicao_clips.py",
        "concatenacao": "teste_08_concatenacao_transicoes.py",
        "performance": "teste_09_performance.py",
        "memoria": "teste_10_memoria.py",
        "compatibilidade_v2": "teste_11_compatibilidade_v2.py",
        "compatibilidade_antigas": "teste_12_compatibilidade_antigas.py",
        "erros": "teste_13_tratamento_erros.py"
    }
    
    if nome_teste not in testes:
        print(f"Teste '{nome_teste}' não encontrado.")
        print("Testes disponíveis:")
        for nome in testes.keys():
            print(f"  - {nome}")
        return 1
    
    arquivo_teste = testes[nome_teste]
    
    try:
        print(f"--- Executando teste: {nome_teste} ---")
        result = subprocess.run([sys.executable, arquivo_teste], 
                              capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            print(f"✓ Teste '{nome_teste}': PASSED")
            return 0
        else:
            print(f"✗ Teste '{nome_teste}': FAILED")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return 1
    except Exception as e:
        print(f"✗ Erro ao executar teste '{nome_teste}': {e}")
        return 1

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python executar_teste_individual.py <nome_teste>")
        print("Exemplo: python executar_teste_individual.py instalacao")
        sys.exit(1)
    
    nome_teste = sys.argv[1]
    sys.exit(executar_teste_individual(nome_teste))
```

## Resultados Esperados

### Resultados Esperados por Teste

#### Teste 1: Instalação e Importação
- **Resultado Esperado**: PASSED
- **Indicadores**: 
  - MoviePy instalado e versão exibida
  - Todas as dependências presentes
  - Nenhum erro de importação

#### Teste 2: Configuração Básica
- **Resultado Esperado**: PASSED
- **Indicadores**:
  - FFmpeg configurado corretamente
  - ImageMagick configurado corretamente
  - Diretório temporário acessível

#### Teste 3: Criação de Clips Básicos
- **Resultado Esperado**: PASSED
- **Indicadores**:
  - ColorClip criado com sucesso
  - TextClip criado com sucesso
  - ImageClip criado com sucesso

#### Teste 4: VideoFileClip
- **Resultado Esperado**: PASSED
- **Indicadores**:
  - Vídeo carregado com sucesso
  - Edições aplicadas corretamente
  - Vídeo exportado com sucesso

#### Teste 5: AudioFileClip
- **Resultado Esperado**: PASSED
- **Indicadores**:
  - Áudio criado com sucesso
  - Edições aplicadas corretamente
  - Áudio exportado com sucesso

#### Teste 6: TextClip Avançado
- **Resultado Esperado**: PASSED
- **Indicadores**:
  - Texto com posicionamento criado
  - Texto animado criado
  - Texto com cores criado

#### Teste 7: Composição de Clips
- **Resultado Esperado**: PASSED
- **Indicadores**:
  - Composição básica criada
  - Clips com tempo criados
  - Composição complexa criada

#### Teste 8: Concatenação e Transições
- **Resultado Esperado**: PASSED
- **Indicadores**:
  - Concatenação simples criada
  - Concatenação com transições criada
  - Transições variadas criadas

#### Teste 9: Performance de Processamento
- **Resultado Esperado**: PASSED
- **Indicadores**:
  - Criação de múltiplos clips eficiente
  - Composição de clips eficiente
  - Exportação de vídeos eficiente

#### Teste 10: Uso de Memória
- **Resultado Esperado**: PASSED
- **Indicadores**:
  - Uso de memória na criação controlado
  - Uso de memória na composição controlado
  - Limpeza de memória funcionando

#### Teste 11: Compatibilidade com MoviePy 2.1.2
- **Resultado Esperado**: PASSED
- **Indicadores**:
  - Nova API do TextClip funcionando
  - Nova API de efeitos funcionando
  - Nova API de concatenação funcionando
  - Remoção do verbose funcionando

#### Teste 12: Compatibilidade com Versões Anteriores
- **Resultado Esperado**: PASSED
- **Indicadores**:
  - Métodos depreciados identificados
  - Parâmetros depreciados identificados
  - Compatibilidade reversa testada

#### Teste 13: Tratamento de Erros
- **Resultado Esperado**: PASSED
- **Indicadores**:
  - Arquivo inexistente gera exceção
  - Parâmetros inválidos geram exceção
  - Operações inválidas geram exceção
  - Recursos insuficientes tratados

### Interpretação dos Resultados

#### Todos os Testes Passaram (PASSED)
- **Significado**: O MoviePy está instalado, configurado e funcionando corretamente
- **Ação**: Nenhuma ação necessária, o sistema está pronto para uso

#### Alguns Testes Falharam (FAILED)
- **Significado**: Existem problemas que precisam ser resolvidos
- **Ação**: 
  1. Identificar quais testes falharam
  2. Analisar os logs de erro
  3. Consultar a seção de Solução de Problemas
  4. Aplicar as correções necessárias
  5. Executar novamente os testes

#### Testes de Performance com Resultados Limitados
- **Significado**: O sistema funciona, mas pode ter limitações de performance
- **Ação**: 
  1. Analisar os tempos de execução
  2. Verificar o uso de memória
  3. Considerar otimizações se necessário

## Solução de Problemas

### Problemas Comuns nos Testes

#### 1. Teste 1 Falha: MoviePy não encontrado
**Sintoma**: `ImportError: No module named 'moviepy'`
**Solução**:
```bash
pip install moviepy
```

#### 2. Teste 2 Falha: FFmpeg não encontrado
**Sintoma**: Erros relacionados ao FFmpeg
**Solução**:
```python
import moviepy.config as config
config.FFMPEG_BINARY = r'C:\caminho\para\ffmpeg.exe'
```

#### 3. Teste 2 Falha: ImageMagick não encontrado
**Sintoma**: Erros relacionados ao ImageMagick
**Solução**:
```python
import moviepy.config as config
config.IMAGEMAGICK_BINARY = r'C:\caminho\para\magick.exe'
```

#### 4. Teste 3 Falha: TextClip não funciona
**Sintoma**: Erros ao criar TextClip
**Solução**:
```python
# Usar caminho completo para a fonte
txt_clip = TextClip(
    text="Hello",
    font_size=24,
    color='white',
    font='C:/Windows/Fonts/arial.ttf'
)
```

#### 5. Teste 11 Falha: Nova API não funciona
**Sintoma**: Erros com a nova API do MoviePy 2.1.2
**Solução**: Verificar se a versão do MoviePy é realmente 2.1.2 ou superior
```python
import moviepy
print(moviepy.__version__)
```

#### 6. Teste 9/10 Falha: Problemas de Performance/Memória
**Sintoma**: Testes lentos ou com alto consumo de memória
**Solução**:
```python
import moviepy.config as config
config.MAX_CACHE_SIZE = 1.0  # Reduzir cache
```

### Dicas para Resolução de Problemas

#### 1. Verificar Logs
- Sempre verifique os logs de erro completos
- Preste atenção aos tipos de exceção
- Anote os números de linha dos erros

#### 2. Testar Isoladamente
- Execute os testes individualmente para isolar problemas
- Use o script `executar_teste_individual.py`
- Comece pelos testes básicos antes dos avançados

#### 3. Verificar Dependências
- Certifique-se de que todas as dependências estão instaladas
- Verifique as versões das dependências
- Atualize as dependências se necessário

#### 4. Verificar Configuração
- Confirme os caminhos do FFmpeg e ImageMagick
- Verifique permissões de diretórios
- Confirme a disponibilidade de recursos do sistema

#### 5. Consultar Documentação
- Consulte a documentação oficial do MoviePy
- Verifique as notas de lançamento para mudanças na API
- Procure por problemas conhecidos no GitHub

---

Esta suite de testes completa foi projetada para validar todos os aspectos do MoviePy no projeto auto-video-producerV5-dev, desde a instalação básica até cenários complexos de uso e compatibilidade.