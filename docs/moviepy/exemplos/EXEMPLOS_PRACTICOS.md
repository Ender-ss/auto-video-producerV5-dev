# Exemplos Práticos do MoviePy

## Índice
1. [Introdução](#introdução)
2. [Exemplos Básicos](#exemplos-básicos)
3. [Exemplos de Edição](#exemplos-de-edição)
4. [Exemplos de Efeitos](#exemplos-de-efeitos)
5. [Exemplos de Texto](#exemplos-de-texto)
6. [Exemplos de Áudio](#exemplos-de-áudio)
7. [Exemplos de Composição](#exemplos-de-composição)
8. [Exemplos Avançados](#exemplos-avançados)
9. [Exemplos do Projeto](#exemplos-do-projeto)
10. [Execução dos Exemplos](#execução-dos-exemplos)

## Introdução

Este documento contém exemplos práticos de uso do MoviePy no projeto auto-video-producerV5-dev. Os exemplos cobrem desde operações básicas até técnicas avançadas de edição de vídeo, com foco na versão 2.1.2 do MoviePy.

### Objetivos dos Exemplos
- Demonstrar o uso prático do MoviePy
- Fornecer código pronto para uso
- Ilustrar as novas funcionalidades da versão 2.1.2
- Servir como referência para desenvolvimento

## Exemplos Básicos

### Exemplo 1: Criar um Vídeo Simples
```python
# exemplo_01_video_simples.py
from moviepy.editor import *
import os

def criar_video_simples():
    """Cria um vídeo simples com uma cor sólida"""
    # Criar um clip de cor sólida
    clip = ColorClip(size=(640, 480), color=(255, 0, 0), duration=10)
    
    # Exportar o vídeo
    output_path = os.path.join(os.getcwd(), 'temp', 'video_simples.mp4')
    clip.write_videofile(output_path, fps=24)
    
    print(f"Vídeo simples criado: {output_path}")
    return output_path

if __name__ == "__main__":
    criar_video_simples()
```

### Exemplo 2: Carregar e Editar um Vídeo
```python
# exemplo_02_carregar_editar.py
from moviepy.editor import *
import os

def carregar_editar_video(input_path=None):
    """Carrega um vídeo existente e aplica edições básicas"""
    # Se não fornecer um vídeo, criar um de teste
    if input_path is None:
        test_clip = ColorClip(size=(640, 480), color=(0, 255, 0), duration=10)
        input_path = os.path.join(os.getcwd(), 'temp', 'video_teste.mp4')
        test_clip.write_videofile(input_path, fps=24)
    
    # Carregar o vídeo
    clip = VideoFileClip(input_path)
    
    # Aplicar edições
    clip_editado = clip.subclip(2, 8)  # Cortar dos 2s aos 8s
    clip_editado = clip_editado.resize(width=320)  # Redimensionar
    clip_editado = clip_editado.speedx(factor=1.5)  # Acelerar 1.5x
    
    # Exportar
    output_path = os.path.join(os.getcwd(), 'temp', 'video_editado.mp4')
    clip_editado.write_videofile(output_path, fps=24)
    
    print(f"Vídeo editado: {output_path}")
    return output_path

if __name__ == "__main__":
    carregar_editar_video()
```

### Exemplo 3: Criar um Vídeo com Texto
```python
# exemplo_03_video_com_texto.py
from moviepy.editor import *
import os

def criar_video_com_texto():
    """Cria um vídeo com texto sobreposto"""
    # Criar fundo
    background = ColorClip(size=(640, 480), color=(0, 0, 0), duration=10)
    
    # Criar texto
    txt_clip = TextClip(
        text="Exemplo de Texto",
        font_size=48,
        color='white',
        font='C:/Windows/Fonts/arial.ttf'
    )
    txt_clip = txt_clip.with_position(('center', 'center')).with_duration(10)
    
    # Combinar
    final = CompositeVideoClip([background, txt_clip])
    
    # Exportar
    output_path = os.path.join(os.getcwd(), 'temp', 'video_com_texto.mp4')
    final.write_videofile(output_path, fps=24)
    
    print(f"Vídeo com texto criado: {output_path}")
    return output_path

if __name__ == "__main__":
    criar_video_com_texto()
```

## Exemplos de Edição

### Exemplo 4: Cortar e Juntar Vídeos
```python
# exemplo_04_cortar_juntar.py
from moviepy.editor import *
import os

def cortar_juntar_videos():
    """Corta partes de um vídeo e as junta em ordem diferente"""
    # Criar vídeo de teste
    original = ColorClip(size=(640, 480), color=(100, 100, 100), duration=20)
    
    # Cortar em partes
    parte1 = original.subclip(0, 5)
    parte2 = original.subclip(10, 15)
    parte3 = original.subclip(5, 10)
    
    # Juntar em ordem diferente
    final = concatenate_videoclips([parte1, parte3, parte2])
    
    # Exportar
    output_path = os.path.join(os.getcwd(), 'temp', 'video_cortado_juntado.mp4')
    final.write_videofile(output_path, fps=24)
    
    print(f"Vídeo cortado e juntado: {output_path}")
    return output_path

if __name__ == "__main__":
    cortar_juntar_videos()
```

### Exemplo 5: Redimensionar e Rotacionar
```python
# exemplo_05_redimensionar_rotacionar.py
from moviepy.editor import *
import os

def redimensionar_rotacionar():
    """Aplica redimensionamento e rotação a um vídeo"""
    # Criar vídeo de teste
    original = ColorClip(size=(640, 480), color=(0, 100, 200), duration=10)
    
    # Aplicar transformações
    transformado = original.resize(width=320)  # Redimensionar
    transformado = transformado.rotate(45)  # Rotacionar 45 graus
    transformado = transformado.crop(x1=50, y1=50, x2=270, y2=270)  # Cortar bordas
    
    # Exportar
    output_path = os.path.join(os.getcwd(), 'temp', 'video_transformado.mp4')
    transformado.write_videofile(output_path, fps=24)
    
    print(f"Vídeo transformado: {output_path}")
    return output_path

if __name__ == "__main__":
    redimensionar_rotacionar()
```

### Exemplo 6: Ajustar Velocidade
```python
# exemplo_06_ajustar_velocidade.py
from moviepy.editor import *
import os

def ajustar_velocidade():
    """Cria um vídeo com diferentes velocidades de reprodução"""
    # Criar vídeo de teste
    original = ColorClip(size=(640, 480), color=(200, 100, 0), duration=15)
    
    # Criar partes com diferentes velocidades
    parte_normal = original.subclip(0, 5)
    parte_rapida = original.subclip(5, 10).speedx(factor=2.0)  # 2x mais rápido
    parte_lenta = original.subclip(10, 15).speedx(factor=0.5)  # 2x mais lento
    
    # Juntar partes
    final = concatenate_videoclips([parte_normal, parte_rapida, parte_lenta])
    
    # Adicionar texto indicando a velocidade
    txt_normal = TextClip(
        text="Velocidade Normal",
        font_size=36,
        color='white',
        font='C:/Windows/Fonts/arial.ttf'
    ).with_position(('center', 50)).with_start(0).with_duration(5)
    
    txt_rapida = TextClip(
        text="2x Mais Rápido",
        font_size=36,
        color='white',
        font='C:/Windows/Fonts/arial.ttf'
    ).with_position(('center', 50)).with_start(5).with_duration(5)
    
    txt_lenta = TextClip(
        text="2x Mais Lento",
        font_size=36,
        color='white',
        font='C:/Windows/Fonts/arial.ttf'
    ).with_position(('center', 50)).with_start(10).with_duration(5)
    
    # Combinar tudo
    final_com_texto = CompositeVideoClip([final, txt_normal, txt_rapida, txt_lenta])
    
    # Exportar
    output_path = os.path.join(os.getcwd(), 'temp', 'video_velocidade.mp4')
    final_com_texto.write_videofile(output_path, fps=24)
    
    print(f"Vídeo com velocidades ajustadas: {output_path}")
    return output_path

if __name__ == "__main__":
    ajustar_velocidade()
```

## Exemplos de Efeitos

### Exemplo 7: Efeitos de Fade
```python
# exemplo_07_efeitos_fade.py
from moviepy.editor import *
from moviepy.video.fx import FadeIn, FadeOut
import os

def efeitos_fade():
    """Aplica efeitos de fade in e fade out"""
    # Criar vídeo de teste
    original = ColorClip(size=(640, 480), color=(150, 0, 150), duration=10)
    
    # Aplicar efeitos de fade (nova API do MoviePy 2.1.2)
    com_fade = original.with_effects([FadeIn(2), FadeOut(2)])
    
    # Exportar
    output_path = os.path.join(os.getcwd(), 'temp', 'video_fade.mp4')
    com_fade.write_videofile(output_path, fps=24)
    
    print(f"Vídeo com efeitos de fade: {output_path}")
    return output_path

if __name__ == "__main__":
    efeitos_fade()
```

### Exemplo 8: Efeitos de Transição
```python
# exemplo_08_efeitos_transicao.py
from moviepy.editor import *
from moviepy.video.fx import FadeIn, FadeOut
import os

def efeitos_transicao():
    """Cria transições entre diferentes clipes"""
    # Criar clipes de cores diferentes
    clip1 = ColorClip(size=(640, 480), color=(255, 0, 0), duration=5)
    clip2 = ColorClip(size=(640, 480), color=(0, 255, 0), duration=5)
    clip3 = ColorClip(size=(640, 480), color=(0, 0, 255), duration=5)
    
    # Adicionar transições
    clip1 = clip1.with_effects([FadeOut(1)])
    clip2 = clip2.with_effects([FadeIn(1)])
    clip2 = clip2.with_effects([FadeOut(1)])
    clip3 = clip3.with_effects([FadeIn(1)])
    
    # Concatenar com transições
    final = concatenate_videoclips([clip1, clip2, clip3])
    
    # Exportar
    output_path = os.path.join(os.getcwd(), 'temp', 'video_transicao.mp4')
    final.write_videofile(output_path, fps=24)
    
    print(f"Vídeo com transições: {output_path}")
    return output_path

if __name__ == "__main__":
    efeitos_transicao()
```

### Exemplo 9: Efeitos de Cor
```python
# exemplo_09_efeitos_cor.py
from moviepy.editor import *
from moviepy.video.fx import blackwhite, lum_contrast, mask_color
import os

def efeitos_cor():
    """Aplica efeitos de cor a um vídeo"""
    # Criar vídeo colorido
    original = ColorClip(size=(640, 480), color=(100, 150, 200), duration=10)
    
    # Aplicar diferentes efeitos de cor
    parte1 = original.subclip(0, 3.33)
    parte2 = original.subclip(3.33, 6.66)
    parte3 = original.subclip(6.66, 10)
    
    # Efeito preto e branco
    parte_bw = blackwhite(parte1)
    
    # Efeito de contraste
    parte_contraste = lum_contrast(parte2, lum=0.5, contrast=1.5)
    
    # Efeito de máscara de cor
    parte_mask = mask_color(parte3, color=[100, 150, 200], thr=100)
    
    # Juntar partes
    final = concatenate_videoclips([parte_bw, parte_contraste, parte_mask])
    
    # Adicionar texto explicativo
    txt_bw = TextClip(
        text="Preto e Branco",
        font_size=36,
        color='white',
        font='C:/Windows/Fonts/arial.ttf'
    ).with_position(('center', 50)).with_start(0).with_duration(3.33)
    
    txt_contraste = TextClip(
        text="Alto Contraste",
        font_size=36,
        color='white',
        font='C:/Windows/Fonts/arial.ttf'
    ).with_position(('center', 50)).with_start(3.33).with_duration(3.33)
    
    txt_mask = TextClip(
        text="Máscara de Cor",
        font_size=36,
        color='white',
        font='C:/Windows/Fonts/arial.ttf'
    ).with_position(('center', 50)).with_start(6.66).with_duration(3.34)
    
    # Combinar tudo
    final_com_texto = CompositeVideoClip([final, txt_bw, txt_contraste, txt_mask])
    
    # Exportar
    output_path = os.path.join(os.getcwd(), 'temp', 'video_efeitos_cor.mp4')
    final_com_texto.write_videofile(output_path, fps=24)
    
    print(f"Vídeo com efeitos de cor: {output_path}")
    return output_path

if __name__ == "__main__":
    efeitos_cor()
```

## Exemplos de Texto

### Exemplo 10: Texto Animado
```python
# exemplo_10_texto_animado.py
from moviepy.editor import *
import os

def texto_animado():
    """Cria um vídeo com texto animado"""
    # Criar fundo
    background = ColorClip(size=(640, 480), color=(0, 0, 0), duration=10)
    
    # Criar texto
    txt_clip = TextClip(
        text="Texto Animado",
        font_size=48,
        color='yellow',
        font='C:/Windows/Fonts/arial.ttf'
    )
    
    # Animar posição (movimento horizontal)
    def animate_pos(t):
        return (50 + t * 50, 240)  # Move da esquerda para direita
    
    txt_clip = txt_clip.with_position(animate_pos).with_duration(10)
    
    # Combinar
    final = CompositeVideoClip([background, txt_clip])
    
    # Exportar
    output_path = os.path.join(os.getcwd(), 'temp', 'video_texto_animado.mp4')
    final.write_videofile(output_path, fps=24)
    
    print(f"Vídeo com texto animado: {output_path}")
    return output_path

if __name__ == "__main__":
    texto_animado()
```

### Exemplo 11: Texto com Efeitos
```python
# exemplo_11_texto_efeitos.py
from moviepy.editor import *
from moviepy.video.fx import FadeIn, FadeOut
import os

def texto_com_efeitos():
    """Cria um vídeo com texto e efeitos"""
    # Criar fundo
    background = ColorClip(size=(640, 480), color=(0, 0, 0), duration=15)
    
    # Criar textos com diferentes efeitos
    textos = [
        {
            "text": "Fade In",
            "start": 0,
            "duration": 5,
            "color": "red",
            "efeito": "fadein"
        },
        {
            "text": "Fade Out",
            "start": 5,
            "duration": 5,
            "color": "green",
            "efeito": "fadeout"
        },
        {
            "text": "Fade In + Out",
            "start": 10,
            "duration": 5,
            "color": "blue",
            "efeito": "fadeinout"
        }
    ]
    
    clips = [background]
    for txt_info in textos:
        # Criar texto
        txt_clip = TextClip(
            text=txt_info["text"],
            font_size=48,
            color=txt_info["color"],
            font='C:/Windows/Fonts/arial.ttf'
        )
        txt_clip = txt_clip.with_position(('center', 'center'))
        txt_clip = txt_clip.with_start(txt_info["start"])
        txt_clip = txt_clip.with_duration(txt_info["duration"])
        
        # Aplicar efeitos
        if txt_info["efeito"] == "fadein":
            txt_clip = txt_clip.with_effects([FadeIn(1)])
        elif txt_info["efeito"] == "fadeout":
            txt_clip = txt_clip.with_effects([FadeOut(1)])
        elif txt_info["efeito"] == "fadeinout":
            txt_clip = txt_clip.with_effects([FadeIn(1), FadeOut(1)])
        
        clips.append(txt_clip)
    
    # Combinar
    final = CompositeVideoClip(clips)
    
    # Exportar
    output_path = os.path.join(os.getcwd(), 'temp', 'video_texto_efeitos.mp4')
    final.write_videofile(output_path, fps=24)
    
    print(f"Vídeo com texto e efeitos: {output_path}")
    return output_path

if __name__ == "__main__":
    texto_com_efeitos()
```

### Exemplo 12: Múltiplos Textos
```python
# exemplo_12_multiplos_textos.py
from moviepy.editor import *
import os

def multiplos_textos():
    """Cria um vídeo com múltiplos textos em diferentes posições"""
    # Criar fundo
    background = ColorClip(size=(640, 480), color=(0, 0, 0), duration=10)
    
    # Criar textos em diferentes posições
    txt_superior = TextClip(
        text="Texto Superior",
        font_size=36,
        color='white',
        font='C:/Windows/Fonts/arial.ttf'
    )
    txt_superior = txt_superior.with_position(('center', 50)).with_duration(10)
    
    txt_central = TextClip(
        text="Texto Central",
        font_size=48,
        color='yellow',
        font='C:/Windows/Fonts/arial.ttf'
    )
    txt_central = txt_central.with_position(('center', 'center')).with_duration(10)
    
    txt_inferior = TextClip(
        text="Texto Inferior",
        font_size=36,
        color='cyan',
        font='C:/Windows/Fonts/arial.ttf'
    )
    txt_inferior = txt_inferior.with_position(('center', 430)).with_duration(10)
    
    txt_esquerda = TextClip(
        text="Esquerda",
        font_size=30,
        color='red',
        font='C:/Windows/Fonts/arial.ttf'
    )
    txt_esquerda = txt_esquerda.with_position((50, 'center')).with_duration(10)
    
    txt_direita = TextClip(
        text="Direita",
        font_size=30,
        color='green',
        font='C:/Windows/Fonts/arial.ttf'
    )
    txt_direita = txt_direita.with_position((590, 'center')).with_duration(10)
    
    # Combinar
    final = CompositeVideoClip([
        background, 
        txt_superior, 
        txt_central, 
        txt_inferior,
        txt_esquerda,
        txt_direita
    ])
    
    # Exportar
    output_path = os.path.join(os.getcwd(), 'temp', 'video_multiplos_textos.mp4')
    final.write_videofile(output_path, fps=24)
    
    print(f"Vídeo com múltiplos textos: {output_path}")
    return output_path

if __name__ == "__main__":
    multiplos_textos()
```

## Exemplos de Áudio

### Exemplo 13: Adicionar Áudio a um Vídeo
```python
# exemplo_13_adicionar_audio.py
from moviepy.editor import *
import numpy as np
import os

def adicionar_audio():
    """Adiciona uma trilha sonora a um vídeo"""
    # Criar vídeo
    video = ColorClip(size=(640, 480), color=(100, 100, 200), duration=10)
    
    # Criar áudio simples (sine wave)
    duration = 10
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Criar uma melodia simples
    frequencies = [440, 494, 523, 587, 659, 698, 784, 880]  # Notas musicais
    audio_data = np.zeros_like(t)
    
    for i, freq in enumerate(frequencies):
        start_time = i * (duration / len(frequencies))
        end_time = (i + 1) * (duration / len(frequencies))
        mask = (t >= start_time) & (t < end_time)
        audio_data[mask] = np.sin(2 * np.pi * freq * t[mask])
    
    # Normalizar
    audio_data = audio_data / np.max(np.abs(audio_data)) * 0.5
    
    # Criar clip de áudio
    audio_clip = AudioArrayClip(audio_data, fps=sample_rate)
    
    # Adicionar áudio ao vídeo
    video_com_audio = video.set_audio(audio_clip)
    
    # Exportar
    output_path = os.path.join(os.getcwd(), 'temp', 'video_com_audio.mp4')
    video_com_audio.write_videofile(output_path, fps=24)
    
    print(f"Vídeo com áudio: {output_path}")
    return output_path

if __name__ == "__main__":
    adicionar_audio()
```

### Exemplo 14: Misturar Áudios
```python
# exemplo_14_misturar_audios.py
from moviepy.editor import *
import numpy as np
import os

def misturar_audios():
    """Mistura múltiplas trilhas de áudio"""
    # Criar vídeo
    video = ColorClip(size=(640, 480), color=(200, 100, 100), duration=10)
    
    # Criar primeiro áudio (frequência baixa)
    duration = 10
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration))
    audio1_data = np.sin(2 * np.pi * 220 * t) * 0.3  # 220 Hz
    
    # Criar segundo áudio (frequência alta)
    audio2_data = np.sin(2 * np.pi * 880 * t) * 0.3  # 880 Hz
    
    # Misturar áudios
    audio_misturado_data = audio1_data + audio2_data
    
    # Normalizar
    audio_misturado_data = audio_misturado_data / np.max(np.abs(audio_misturado_data)) * 0.5
    
    # Criar clip de áudio
    audio_clip = AudioArrayClip(audio_misturado_data, fps=sample_rate)
    
    # Adicionar áudio ao vídeo
    video_com_audio = video.set_audio(audio_clip)
    
    # Exportar
    output_path = os.path.join(os.getcwd(), 'temp', 'video_audios_misturados.mp4')
    video_com_audio.write_videofile(output_path, fps=24)
    
    print(f"Vídeo com áudios misturados: {output_path}")
    return output_path

if __name__ == "__main__":
    misturar_audios()
```

### Exemplo 15: Ajustar Volume do Áudio
```python
# exemplo_15_ajustar_volume.py
from moviepy.editor import *
import numpy as np
import os

def ajustar_volume():
    """Cria um vídeo com áudio com volume variável"""
    # Criar vídeo
    video = ColorClip(size=(640, 480), color=(100, 200, 100), duration=15)
    
    # Criar áudio
    duration = 15
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration))
    audio_data = np.sin(2 * np.pi * 440 * t)  # 440 Hz
    
    # Dividir em partes com diferentes volumes
    parte1_data = audio_data[:int(sample_rate * 5)] * 0.2  # 20% do volume
    parte2_data = audio_data[int(sample_rate * 5):int(sample_rate * 10)] * 0.5  # 50% do volume
    parte3_data = audio_data[int(sample_rate * 10):] * 1.0  # 100% do volume
    
    # Juntar partes
    audio_final_data = np.concatenate([parte1_data, parte2_data, parte3_data])
    
    # Criar clip de áudio
    audio_clip = AudioArrayClip(audio_final_data, fps=sample_rate)
    
    # Adicionar áudio ao vídeo
    video_com_audio = video.set_audio(audio_clip)
    
    # Adicionar texto indicando o volume
    txt_baixo = TextClip(
        text="Volume: 20%",
        font_size=36,
        color='white',
        font='C:/Windows/Fonts/arial.ttf'
    ).with_position(('center', 50)).with_start(0).with_duration(5)
    
    txt_medio = TextClip(
        text="Volume: 50%",
        font_size=36,
        color='white',
        font='C:/Windows/Fonts/arial.ttf'
    ).with_position(('center', 50)).with_start(5).with_duration(5)
    
    txt_alto = TextClip(
        text="Volume: 100%",
        font_size=36,
        color='white',
        font='C:/Windows/Fonts/arial.ttf'
    ).with_position(('center', 50)).with_start(10).with_duration(5)
    
    # Combinar
    final = CompositeVideoClip([video_com_audio, txt_baixo, txt_medio, txt_alto])
    
    # Exportar
    output_path = os.path.join(os.getcwd(), 'temp', 'video_volume_variavel.mp4')
    final.write_videofile(output_path, fps=24)
    
    print(f"Vídeo com volume variável: {output_path}")
    return output_path

if __name__ == "__main__":
    ajustar_volume()
```

## Exemplos de Composição

### Exemplo 16: Vídeo com Múltiplas Camadas
```python
# exemplo_16_multiplas_camadas.py
from moviepy.editor import *
import os

def multiplas_camadas():
    """Cria um vídeo com múltiplas camadas sobrepostas"""
    # Criar fundo
    background = ColorClip(size=(640, 480), color=(0, 0, 0), duration=10)
    
    # Criar camadas sobrepostas
    camada1 = ColorClip(size=(200, 200), color=(255, 0, 0), duration=10)
    camada1 = camada1.with_position((50, 50))
    
    camada2 = ColorClip(size=(200, 200), color=(0, 255, 0), duration=10)
    camada2 = camada2.with_position((250, 150))
    
    camada3 = ColorClip(size=(200, 200), color=(0, 0, 255), duration=10)
    camada3 = camada3.with_position((150, 250))
    
    # Criar texto
    txt_clip = TextClip(
        text="Múltiplas Camadas",
        font_size=36,
        color='white',
        font='C:/Windows/Fonts/arial.ttf'
    )
    txt_clip = txt_clip.with_position(('center', 20)).with_duration(10)
    
    # Combinar tudo
    final = CompositeVideoClip([
        background, 
        camada1, 
        camada2, 
        camada3,
        txt_clip
    ])
    
    # Exportar
    output_path = os.path.join(os.getcwd(), 'temp', 'video_multiplas_camadas.mp4')
    final.write_videofile(output_path, fps=24)
    
    print(f"Vídeo com múltiplas camadas: {output_path}")
    return output_path

if __name__ == "__main__":
    multiplas_camadas()
```

### Exemplo 17: Vídeo com Sobreposição de Imagens
```python
# exemplo_17_sobreposicao_imagens.py
from moviepy.editor import *
import numpy as np
from PIL import Image
import os

def sobreposicao_imagens():
    """Cria um vídeo com sobreposição de imagens"""
    # Criar fundo
    background = ColorClip(size=(640, 480), color=(50, 50, 50), duration=10)
    
    # Criar imagens temporárias
    imagens = []
    for i, cor in enumerate([(255, 0, 0), (0, 255, 0), (0, 0, 255)]):
        # Criar imagem
        img_array = np.zeros((100, 100, 3), dtype=np.uint8)
        img_array[:, :] = cor
        img = Image.fromarray(img_array)
        img_path = os.path.join(os.getcwd(), 'temp', f'temp_image_{i}.png')
        img.save(img_path)
        
        # Criar ImageClip
        img_clip = ImageClip(img_path, duration=10)
        
        # Posicionar
        x_pos = 100 + i * 150
        y_pos = 150 + i * 50
        img_clip = img_clip.with_position((x_pos, y_pos))
        
        imagens.append(img_clip)
    
    # Criar texto
    txt_clip = TextClip(
        text="Sobreposição de Imagens",
        font_size=36,
        color='white',
        font='C:/Windows/Fonts/arial.ttf'
    )
    txt_clip = txt_clip.with_position(('center', 50)).with_duration(10)
    
    # Combinar tudo
    final = CompositeVideoClip([background] + imagens + [txt_clip])
    
    # Exportar
    output_path = os.path.join(os.getcwd(), 'temp', 'video_sobreposicao_imagens.mp4')
    final.write_videofile(output_path, fps=24)
    
    print(f"Vídeo com sobreposição de imagens: {output_path}")
    return output_path

if __name__ == "__main__":
    sobreposicao_imagens()
```

### Exemplo 18: Vídeo com Animação Complexa
```python
# exemplo_18_animacao_complexa.py
from moviepy.editor import *
import os

def animacao_complexa():
    """Cria um vídeo com animação complexa de múltiplos elementos"""
    # Criar fundo
    background = ColorClip(size=(640, 480), color=(0, 0, 0), duration=15)
    
    # Criar círculos animados
    circulos = []
    cores = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]
    
    for i, cor in enumerate(cores):
        # Criar círculo (usando ColorClip com máscara circular)
        circle = ColorClip(size=(100, 100), color=cor, duration=15)
        
        # Animar posição (movimento circular)
        def make_circle_animation(center_x, center_y, radius, speed, phase):
            def animate_pos(t):
                angle = speed * t + phase
                x = center_x + radius * np.cos(angle)
                y = center_y + radius * np.sin(angle)
                return (x, y)
            return animate_pos
        
        anim_func = make_circle_animation(320, 240, 150, 0.5, i * 2 * np.pi / 5)
        circle = circle.with_position(anim_func)
        
        circulos.append(circle)
    
    # Criar texto central
    txt_clip = TextClip(
        text="Animação Complexa",
        font_size=48,
        color='white',
        font='C:/Windows/Fonts/arial.ttf'
    )
    txt_clip = txt_clip.with_position(('center', 'center')).with_duration(15)
    
    # Combinar tudo
    final = CompositeVideoClip([background] + circulos + [txt_clip])
    
    # Exportar
    output_path = os.path.join(os.getcwd(), 'temp', 'video_animacao_complexa.mp4')
    final.write_videofile(output_path, fps=24)
    
    print(f"Vídeo com animação complexa: {output_path}")
    return output_path

if __name__ == "__main__":
    animacao_complexa()
```

## Exemplos Avançados

### Exemplo 19: Vídeo com Efeitos de Tela
```python
# exemplo_19_efeitos_tela.py
from moviepy.editor import *
from moviepy.video.fx import FadeIn, FadeOut
import os

def efeitos_tela():
    """Cria um vídeo com efeitos de tela (split screen)"""
    # Criar clipes para diferentes partes da tela
    clip_superior_esquerda = ColorClip(size=(320, 240), color=(255, 0, 0), duration=10)
    clip_superior_esquerda = clip_superior_esquerda.with_position((0, 0))
    
    clip_superior_direita = ColorClip(size=(320, 240), color=(0, 255, 0), duration=10)
    clip_superior_direita = clip_superior_direita.with_position((320, 0))
    
    clip_inferior_esquerda = ColorClip(size=(320, 240), color=(0, 0, 255), duration=10)
    clip_inferior_esquerda = clip_inferior_esquerda.with_position((0, 240))
    
    clip_inferior_direita = ColorClip(size=(320, 240), color=(255, 255, 0), duration=10)
    clip_inferior_direita = clip_inferior_direita.with_position((320, 240))
    
    # Adicionar textos
    txt_se = TextClip(
        text="Superior Esquerdo",
        font_size=24,
        color='white',
        font='C:/Windows/Fonts/arial.ttf'
    )
    txt_se = txt_se.with_position((160, 120)).with_duration(10)
    
    txt_sd = TextClip(
        text="Superior Direito",
        font_size=24,
        color='white',
        font='C:/Windows/Fonts/arial.ttf'
    )
    txt_sd = txt_sd.with_position((480, 120)).with_duration(10)
    
    txt_ie = TextClip(
        text="Inferior Esquerdo",
        font_size=24,
        color='white',
        font='C:/Windows/Fonts/arial.ttf'
    )
    txt_ie = txt_ie.with_position((160, 360)).with_duration(10)
    
    txt_id = TextClip(
        text="Inferior Direito",
        font_size=24,
        color='white',
        font='C:/Windows/Fonts/arial.ttf'
    )
    txt_id = txt_id.with_position((480, 360)).with_duration(10)
    
    # Combinar tudo
    final = CompositeVideoClip([
        clip_superior_esquerda,
        clip_superior_direita,
        clip_inferior_esquerda,
        clip_inferior_direita,
        txt_se,
        txt_sd,
        txt_ie,
        txt_id
    ])
    
    # Exportar
    output_path = os.path.join(os.getcwd(), 'temp', 'video_efeitos_tela.mp4')
    final.write_videofile(output_path, fps=24)
    
    print(f"Vídeo com efeitos de tela: {output_path}")
    return output_path

if __name__ == "__main__":
    efeitos_tela()
```

### Exemplo 20: Vídeo com Marca d'Água
```python
# exemplo_20_marca_dagua.py
from moviepy.editor import *
import os

def marca_dagua():
    """Adiciona uma marca d'água a um vídeo"""
    # Criar vídeo principal
    main_video = ColorClip(size=(640, 480), color=(100, 150, 200), duration=10)
    
    # Criar marca d'água (texto)
    watermark = TextClip(
        text="MARCA D'ÁGUA",
        font_size=24,
        color='white',
        font='C:/Windows/Fonts/arial.ttf'
    )
    
    # Tornar a marca d'água semi-transparente
    watermark = watermark.with_position(('right', 'bottom')).with_duration(10)
    
    # Criar texto explicativo
    txt_clip = TextClip(
        text="Vídeo com Marca d'Água",
        font_size=36,
        color='white',
        font='C:/Windows/Fonts/arial.ttf'
    )
    txt_clip = txt_clip.with_position(('center', 50)).with_duration(10)
    
    # Combinar
    final = CompositeVideoClip([main_video, watermark, txt_clip])
    
    # Exportar
    output_path = os.path.join(os.getcwd(), 'temp', 'video_marca_dagua.mp4')
    final.write_videofile(output_path, fps=24)
    
    print(f"Vídeo com marca d'água: {output_path}")
    return output_path

if __name__ == "__main__":
    marca_dagua()
```

### Exemplo 21: Vídeo com Progresso
```python
# exemplo_21_video_progresso.py
from moviepy.editor import *
import os

def video_com_progresso():
    """Cria um vídeo mostrando uma barra de progresso animada"""
    # Criar fundo
    background = ColorClip(size=(640, 480), color=(0, 0, 0), duration=10)
    
    # Criar barra de progresso (fundo)
    progress_bg = ColorClip(size=(500, 30), color=(50, 50, 50), duration=10)
    progress_bg = progress_bg.with_position((70, 400))
    
    # Criar barra de progresso (preenchimento)
    def make_progress_animation():
        def animate_progress(t):
            # Calcular largura com base no tempo
            width = int(500 * (t / 10))
            return ColorClip(size=(width, 30), color=(0, 255, 0), duration=0.1)
        return animate_progress
    
    # Criar texto de porcentagem
    def make_percentage_text():
        def animate_text(t):
            percentage = int(100 * (t / 10))
            txt = TextClip(
                text=f"{percentage}%",
                font_size=24,
                color='white',
                font='C:/Windows/Fonts/arial.ttf'
            )
            return txt.with_position((320, 350))
        return animate_text
    
    # Criar título
    title = TextClip(
        text="Barra de Progresso",
        font_size=48,
        color='white',
        font='C:/Windows/Fonts/arial.ttf'
    )
    title = title.with_position(('center', 100)).with_duration(10)
    
    # Criar vídeo com progresso
    clips = [background, progress_bg, title]
    
    # Adicionar barra de progresso animada
    for i in range(10):
        t = i
        progress_fill = ColorClip(size=(int(500 * (t / 10)), 30), color=(0, 255, 0), duration=1)
        progress_fill = progress_fill.with_position((70, 400)).with_start(t)
        clips.append(progress_fill)
        
        # Adicionar texto de porcentagem
        percentage = int(100 * (t / 10))
        txt = TextClip(
            text=f"{percentage}%",
            font_size=24,
            color='white',
            font='C:/Windows/Fonts/arial.ttf'
        )
        txt = txt.with_position((320, 350)).with_start(t).with_duration(1)
        clips.append(txt)
    
    # Combinar
    final = CompositeVideoClip(clips)
    
    # Exportar
    output_path = os.path.join(os.getcwd(), 'temp', 'video_progresso.mp4')
    final.write_videofile(output_path, fps=24)
    
    print(f"Vídeo com barra de progresso: {output_path}")
    return output_path

if __name__ == "__main__":
    video_com_progresso()
```

## Exemplos do Projeto

### Exemplo 22: Integração com o Sistema
```python
# exemplo_22_integracao_sistema.py
from moviepy.editor import *
import os
import sys

# Adicionar o diretório do projeto ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

def integracao_com_sistema():
    """Exemplo de integração do MoviePy com o sistema existente"""
    try:
        # Tentar importar módulos do sistema
        from video_processor import VideoProcessor
        from text_generator import TextGenerator
        
        # Criar processador de vídeo
        processor = VideoProcessor()
        
        # Criar gerador de texto
        text_gen = TextGenerator()
        
        # Gerar texto
        texto = text_gen.generate_text("exemplo de integração")
        
        # Criar vídeo com o texto gerado
        background = ColorClip(size=(640, 480), color=(50, 50, 100), duration=10)
        
        txt_clip = TextClip(
            text=texto,
            font_size=36,
            color='white',
            font='C:/Windows/Fonts/arial.ttf'
        )
        txt_clip = txt_clip.with_position(('center', 'center')).with_duration(10)
        
        # Combinar
        final = CompositeVideoClip([background, txt_clip])
        
        # Exportar
        output_path = os.path.join(os.getcwd(), 'temp', 'video_integracao.mp4')
        final.write_videofile(output_path, fps=24)
        
        print(f"Vídeo de integração criado: {output_path}")
        return output_path
        
    except ImportError as e:
        print(f"Módulos do sistema não encontrados: {e}")
        print("Criando exemplo simulado...")
        
        # Criar exemplo simulado
        background = ColorClip(size=(640, 480), color=(50, 50, 100), duration=10)
        
        txt_clip = TextClip(
            text="Exemplo de Integração (Simulado)",
            font_size=36,
            color='white',
            font='C:/Windows/Fonts/arial.ttf'
        )
        txt_clip = txt_clip.with_position(('center', 'center')).with_duration(10)
        
        # Combinar
        final = CompositeVideoClip([background, txt_clip])
        
        # Exportar
        output_path = os.path.join(os.getcwd(), 'temp', 'video_integracao_simulado.mp4')
        final.write_videofile(output_path, fps=24)
        
        print(f"Vídeo de integração simulado criado: {output_path}")
        return output_path

if __name__ == "__main__":
    integracao_com_sistema()
```

### Exemplo 23: Processamento em Lote
```python
# exemplo_23_processamento_lote.py
from moviepy.editor import *
import os

def processamento_lote():
    """Processa múltiplos vídeos em lote"""
    # Criar diretório para os vídeos de exemplo
    batch_dir = os.path.join(os.getcwd(), 'temp', 'batch')
    os.makedirs(batch_dir, exist_ok=True)
    
    # Criar vídeos de exemplo
    videos = []
    for i, cor in enumerate([(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]):
        clip = ColorClip(size=(320, 240), color=cor, duration=5)
        video_path = os.path.join(batch_dir, f'video_{i}.mp4')
        clip.write_videofile(video_path, fps=24)
        videos.append(video_path)
    
    # Processar vídeos em lote
    processed_videos = []
    for video_path in videos:
        # Carregar vídeo
        clip = VideoFileClip(video_path)
        
        # Aplicar processamento
        processed = clip.resize(width=160)  # Redimensionar
        processed = processed.speedx(factor=2.0)  # Acelerar
        
        # Adicionar texto
        txt_clip = TextClip(
            text=f"Processado {os.path.basename(video_path)}",
            font_size=20,
            color='white',
            font='C:/Windows/Fonts/arial.ttf'
        )
        txt_clip = txt_clip.with_position(('center', 20)).with_duration(2.5)
        
        # Combinar
        final = CompositeVideoClip([processed, txt_clip])
        
        # Exportar
        output_path = os.path.join(batch_dir, f'processed_{os.path.basename(video_path)}')
        final.write_videofile(output_path, fps=24)
        processed_videos.append(output_path)
    
    # Concatenar todos os vídeos processados
    clips_to_concat = []
    for video_path in processed_videos:
        clip = VideoFileClip(video_path)
        clips_to_concat.append(clip)
    
    final_concat = concatenate_videoclips(clips_to_concat)
    
    # Exportar vídeo final
    output_path = os.path.join(os.getcwd(), 'temp', 'video_lote_final.mp4')
    final_concat.write_videofile(output_path, fps=24)
    
    print(f"Vídeo de processamento em lote criado: {output_path}")
    return output_path

if __name__ == "__main__":
    processamento_lote()
```

### Exemplo 24: Template de Vídeo
```python
# exemplo_24_template_video.py
from moviepy.editor import *
from moviepy.video.fx import FadeIn, FadeOut
import os

def template_video():
    """Cria um template de vídeo reutilizável"""
    def criar_video_template(titulo, subtitulo, cor_fundo=(50, 50, 100), duracao=10):
        # Criar fundo
        background = ColorClip(size=(640, 480), color=cor_fundo, duration=duracao)
        
        # Criar título
        titulo_clip = TextClip(
            text=titulo,
            font_size=48,
            color='white',
            font='C:/Windows/Fonts/arial.ttf'
        )
        titulo_clip = titulo_clip.with_position(('center', 150)).with_duration(duracao)
        titulo_clip = titulo_clip.with_effects([FadeIn(1), FadeOut(1)])
        
        # Criar subtítulo
        subtitulo_clip = TextClip(
            text=subtitulo,
            font_size=24,
            color='white',
            font='C:/Windows/Fonts/arial.ttf'
        )
        subtitulo_clip = subtitulo_clip.with_position(('center', 250)).with_duration(duracao)
        subtitulo_clip = subtitulo_clip.with_effects([FadeIn(1), FadeOut(1)])
        
        # Combinar
        final = CompositeVideoClip([background, titulo_clip, subtitulo_clip])
        
        return final
    
    # Criar vídeos usando o template
    videos = [
        {"titulo": "Template 1", "subtitulo": "Primeiro exemplo", "cor": (100, 50, 50)},
        {"titulo": "Template 2", "subtitulo": "Segundo exemplo", "cor": (50, 100, 50)},
        {"titulo": "Template 3", "subtitulo": "Terceiro exemplo", "cor": (50, 50, 100)}
    ]
    
    clips = []
    for i, video_info in enumerate(videos):
        video = criar_video_template(
            video_info["titulo"],
            video_info["subtitulo"],
            video_info["cor"],
            duracao=5
        )
        clips.append(video)
    
    # Concatenar todos os vídeos
    final_concat = concatenate_videoclips(clips)
    
    # Exportar
    output_path = os.path.join(os.getcwd(), 'temp', 'video_template.mp4')
    final_concat.write_videofile(output_path, fps=24)
    
    print(f"Vídeo de template criado: {output_path}")
    return output_path

if __name__ == "__main__":
    template_video()
```

## Execução dos Exemplos

### Script para Executar Todos os Exemplos
```python
# executar_todos_exemplos.py
import os
import subprocess
import sys

def executar_exemplo(nome_arquivo):
    """Executa um arquivo de exemplo e retorna o resultado"""
    try:
        print(f"\n--- Executando {nome_arquivo} ---")
        result = subprocess.run([sys.executable, nome_arquivo], 
                              capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            print(f"✓ {nome_arquivo}: EXECUTADO COM SUCESSO")
            return True
        else:
            print(f"✗ {nome_arquivo}: FALHA NA EXECUÇÃO")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
    except Exception as e:
        print(f"✗ Erro ao executar {nome_arquivo}: {e}")
        return False

def main():
    """Executa todos os exemplos"""
    print("=== Iniciando Execução dos Exemplos do MoviePy ===")
    
    # Lista de exemplos
    exemplos = [
        "exemplo_01_video_simples.py",
        "exemplo_02_carregar_editar.py",
        "exemplo_03_video_com_texto.py",
        "exemplo_04_cortar_juntar.py",
        "exemplo_05_redimensionar_rotacionar.py",
        "exemplo_06_ajustar_velocidade.py",
        "exemplo_07_efeitos_fade.py",
        "exemplo_08_efeitos_transicao.py",
        "exemplo_09_efeitos_cor.py",
        "exemplo_10_texto_animado.py",
        "exemplo_11_texto_efeitos.py",
        "exemplo_12_multiplos_textos.py",
        "exemplo_13_adicionar_audio.py",
        "exemplo_14_misturar_audios.py",
        "exemplo_15_ajustar_volume.py",
        "exemplo_16_multiplas_camadas.py",
        "exemplo_17_sobreposicao_imagens.py",
        "exemplo_18_animacao_complexa.py",
        "exemplo_19_efeitos_tela.py",
        "exemplo_20_marca_dagua.py",
        "exemplo_21_video_progresso.py",
        "exemplo_22_integracao_sistema.py",
        "exemplo_23_processamento_lote.py",
        "exemplo_24_template_video.py"
    ]
    
    # Executar exemplos
    resultados = {}
    for exemplo in exemplos:
        resultados[exemplo] = executar_exemplo(exemplo)
    
    # Resumo
    print("\n=== Resumo da Execução ===")
    passed = sum(resultados.values())
    total = len(resultados)
    
    for exemplo, resultado in resultados.items():
        status = "SUCESSO" if resultado else "FALHA"
        print(f"{exemplo}: {status}")
    
    print(f"\nTotal: {passed}/{total} exemplos executados com sucesso")
    
    if passed == total:
        print("✓ Todos os exemplos executados com sucesso!")
        return 0
    else:
        print("✗ Alguns exemplos falharam na execução!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

### Script para Executar Exemplo Individual
```python
# executar_exemplo_individual.py
import os
import subprocess
import sys

def executar_exemplo_individual(nome_exemplo):
    """Executa um exemplo específico"""
    # Mapear nomes para arquivos
    exemplos = {
        "video_simples": "exemplo_01_video_simples.py",
        "carregar_editar": "exemplo_02_carregar_editar.py",
        "video_com_texto": "exemplo_03_video_com_texto.py",
        "cortar_juntar": "exemplo_04_cortar_juntar.py",
        "redimensionar_rotacionar": "exemplo_05_redimensionar_rotacionar.py",
        "ajustar_velocidade": "exemplo_06_ajustar_velocidade.py",
        "efeitos_fade": "exemplo_07_efeitos_fade.py",
        "efeitos_transicao": "exemplo_08_efeitos_transicao.py",
        "efeitos_cor": "exemplo_09_efeitos_cor.py",
        "texto_animado": "exemplo_10_texto_animado.py",
        "texto_efeitos": "exemplo_11_texto_efeitos.py",
        "multiplos_textos": "exemplo_12_multiplos_textos.py",
        "adicionar_audio": "exemplo_13_adicionar_audio.py",
        "misturar_audios": "exemplo_14_misturar_audios.py",
        "ajustar_volume": "exemplo_15_ajustar_volume.py",
        "multiplas_camadas": "exemplo_16_multiplas_camadas.py",
        "sobreposicao_imagens": "exemplo_17_sobreposicao_imagens.py",
        "animacao_complexa": "exemplo_18_animacao_complexa.py",
        "efeitos_tela": "exemplo_19_efeitos_tela.py",
        "marca_dagua": "exemplo_20_marca_dagua.py",
        "video_progresso": "exemplo_21_video_progresso.py",
        "integracao_sistema": "exemplo_22_integracao_sistema.py",
        "processamento_lote": "exemplo_23_processamento_lote.py",
        "template_video": "exemplo_24_template_video.py"
    }
    
    if nome_exemplo not in exemplos:
        print(f"Exemplo '{nome_exemplo}' não encontrado.")
        print("Exemplos disponíveis:")
        for nome in exemplos.keys():
            print(f"  - {nome}")
        return 1
    
    arquivo_exemplo = exemplos[nome_exemplo]
    
    try:
        print(f"--- Executando exemplo: {nome_exemplo} ---")
        result = subprocess.run([sys.executable, arquivo_exemplo], 
                              capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            print(f"✓ Exemplo '{nome_exemplo}': EXECUTADO COM SUCESSO")
            return 0
        else:
            print(f"✗ Exemplo '{nome_exemplo}': FALHA NA EXECUÇÃO")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return 1
    except Exception as e:
        print(f"✗ Erro ao executar exemplo '{nome_exemplo}': {e}")
        return 1

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python executar_exemplo_individual.py <nome_exemplo>")
        print("Exemplo: python executar_exemplo_individual.py video_simples")
        sys.exit(1)
    
    nome_exemplo = sys.argv[1]
    sys.exit(executar_exemplo_individual(nome_exemplo))
```

---

Esta coleção de exemplos práticos do MoviePy foi projetada para fornecer referências imediatas para o desenvolvimento no projeto auto-video-producerV5-dev, cobrindo desde operações básicas até técnicas avançadas de edição de vídeo.