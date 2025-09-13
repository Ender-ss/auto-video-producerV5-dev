# Guia de Referência Rápida do MoviePy

## Índice
1. [Introdução](#introdução)
2. [Importação Básica](#importação-básica)
3. [Clipes de Vídeo](#clipes-de-vídeo)
4. [Clipes de Áudio](#clipes-de-áudio)
5. [Clipes de Texto](#clipes-de-texto)
6. [Clipes de Imagem](#clipes-de-imagem)
7. [Efeitos e Transições](#efeitos-e-transições)
8. [Composição](#composição)
9. [Exportação](#exportação)
10. [Métodos Úteis](#métodos-úteis)
11. [Parâmetros Comuns](#parâmetros-comuns)
12. [Exemplos Rápidos](#exemplos-rápidos)
13. [Solução de Problemas Comuns](#solução-de-problemas-comuns)

## Introdução

Este guia de referência rápida cobre os principais métodos e funcionalidades do MoviePy, especialmente focado na versão 2.1.2. É projetado para ser uma consulta rápida durante o desenvolvimento no projeto auto-video-producerV5-dev.

### Objetivo
- Fornecer acesso rápido aos métodos mais comuns
- Apresentar a sintaxe correta para cada funcionalidade
- Destacar mudanças importantes na versão 2.1.2
- Servir como referência para desenvolvimento diário

## Importação Básica

### Importação Completa
```python
from moviepy.editor import *
```

### Importações Específicas
```python
# Clipes
from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, TextClip, ColorClip

# Efeitos
from moviepy.video.fx import FadeIn, FadeOut, blackwhite, lum_contrast, mask_color

# Composição
from moviepy.editor import CompositeVideoClip, concatenate_videoclips

# Utilitários
from moviepy.editor import vfx, afx
```

## Clipes de Vídeo

### VideoFileClip
Carrega um vídeo existente.

```python
# Carregar um vídeo
clip = VideoFileClip("caminho/para/video.mp4")

# Parâmetros comuns
clip = VideoFileClip(
    "caminho/para/video.mp4",
    target_resolution=None,  # Redimensionar ao carregar
    resize_algorithm='bilinear',  # Algoritmo de redimensionamento
    audio_buffersize=200000,  # Tamanho do buffer de áudio
    audio_fps=44100,  # Taxa de amostragem do áudio
    audio_nbytes=2,  # Bytes por amostra de áudio
    verbose=False  # Exibir informações detalhadas
)
```

### ColorClip
Cria um clipe de cor sólida.

```python
# Criar um clipe de cor sólida
clip = ColorClip(size=(640, 480), color=(255, 0, 0), duration=10)

# Parâmetros comuns
clip = ColorClip(
    size=(640, 480),  # Tamanho (largura, altura)
    color=(255, 0, 0),  # Cor (R, G, B)
    duration=10,  # Duração em segundos
    is_mask=False  # Se é uma máscara
)
```

### Métodos de Manipulação de Vídeo
```python
# Cortar um clipe
clip_cortado = clip.subclip(t_start=5, t_end=15)  # Do segundo 5 ao 15

# Redimensionar
clip_redimensionado = clip.resize(width=320)  # Largura específica
clip_redimensionado = clip.resize(height=240)  # Altura específica
clip_redimensionado = clip.resize(0.5)  # Fator de escala
clip_redimensionado = clip.resize((320, 240))  # Tamanho específico

# Rotacionar
clip_rotacionado = clip.rotate(angle=45)  # Ângulo em graus

# Espelhar
clip_espelhado_x = clip.fx(vfx.mirror_x)  # Espelhar horizontalmente
clip_espelhado_y = clip.fx(vfx.mirror_y)  # Espelhar verticalmente

# Ajustar velocidade
clip_rapido = clip.speedx(factor=2.0)  # 2x mais rápido
clip_lento = clip.speedx(factor=0.5)  # 2x mais lento

# Cortar bordas
clip_cortado = clip.crop(x1=50, y1=50, x2=590, y2=430)  # Cortar 50px de cada borda

# Definir posição
clip_posicionado = clip.with_position((100, 100))  # Posição fixa
clip_posicionado = clip.with_position(('center', 'center'))  # Centralizado
clip_posicionado = clip.with_position(('left', 'top'))  # Canto superior esquerdo

# Definir duração
clip_duracao = clip.with_duration(10)  # Duração fixa

# Definir tempo de início
clip_inicio = clip.with_start(5)  # Começar no segundo 5

# Definir tempo de término
clip_termino = clip.with_end(15)  # Terminar no segundo 15
```

## Clipes de Áudio

### AudioFileClip
Carrega um áudio existente.

```python
# Carregar um áudio
audio = AudioFileClip("caminho/para/audio.mp3")

# Parâmetros comuns
audio = AudioFileClip(
    "caminho/para/audio.mp3",
    buffersize=200000,  # Tamanho do buffer
    fps=44100,  # Taxa de amostragem
    nbytes=2,  # Bytes por amostra
    verbose=False  # Exibir informações detalhadas
)
```

### AudioArrayClip
Cria um clipe de áudio a partir de um array NumPy.

```python
import numpy as np

# Criar áudio sintético
duration = 10
sample_rate = 44100
t = np.linspace(0, duration, int(sample_rate * duration))
audio_data = np.sin(2 * np.pi * 440 * t)  # Onda senoidal de 440 Hz

# Normalizar
audio_data = audio_data / np.max(np.abs(audio_data)) * 0.5

# Criar clipe
audio = AudioArrayClip(audio_data, fps=sample_rate)
```

### Métodos de Manipulação de Áudio
```python
# Cortar um áudio
audio_cortado = audio.subclip(t_start=5, t_end=15)

# Ajustar volume
audio_volume = audio.volumex(factor=2.0)  # 2x mais alto
audio_volume = audio.volumex(factor=0.5)  # 2x mais baixo

# Ajustar velocidade
audio_rapido = audio.speedx(factor=2.0)  # 2x mais rápido
audio_lento = audio.speedx(factor=0.5)  # 2x mais lento

# Loop
audio_loop = audio.loop(n=3)  # Repetir 3 vezes

# Adicionar atraso
audio_delay = audio.audio_delay(delay=2.0)  # Atraso de 2 segundos

# Aplicar efeitos
audio_stereo = audio.audio_stereo()  # Converter para estéreo
audio_fadein = audio.audio_fadein(2.0)  # Fade in de 2 segundos
audio_fadeout = audio.audio_fadeout(2.0)  # Fade out de 2 segundos
```

## Clipes de Texto

### TextClip
Cria um clipe de texto.

```python
# Criar texto simples
txt = TextClip(
    text="Exemplo de Texto",
    font_size=48,
    color='white',
    font='C:/Windows/Fonts/arial.ttf'
)

# Parâmetros comuns
txt = TextClip(
    text="Exemplo de Texto",  # Texto a ser exibido
    font_size=48,  # Tamanho da fonte
    color='white',  # Cor do texto
    font='C:/Windows/Fonts/arial.ttf',  # Caminho para a fonte
    stroke_color='black',  # Cor da borda
    stroke_width=1,  # Largura da borda
    bg_color=None,  # Cor de fundo
    transparent=True,  # Fundo transparente
    align='center',  # Alinhamento
    interline=1,  # Espaçamento entre linhas
    size=(640, 480),  # Tamanho do clipe
    method='label',  # Método de renderização
    kerning=None,  # Espaçamento entre caracteres
    transparent=True  # Fundo transparente
)
```

### Métodos de Manipulação de Texto
```python
# Definir posição
txt_posicionado = txt.with_position((100, 100))  # Posição fixa
txt_posicionado = txt.with_position(('center', 'center'))  # Centralizado
txt_posicionado = txt.with_position(('left', 'top'))  # Canto superior esquerdo

# Definir duração
txt_duracao = txt.with_duration(10)  # Duração fixa

# Definir tempo de início
txt_inicio = txt.with_start(5)  # Começar no segundo 5

# Definir tempo de término
txt_termino = txt.with_end(15)  # Terminar no segundo 15

# Animação de posição
def animate_pos(t):
    return (100 + t * 50, 100)  # Move da esquerda para direita

txt_animado = txt.with_position(animate_pos)

# Animação de tamanho
def animate_size(t):
    return (100 + t * 10, 50 + t * 5)  # Aumenta o tamanho

txt_animado = txt.with_size(animate_size)
```

## Clipes de Imagem

### ImageClip
Cria um clipe a partir de uma imagem.

```python
# Criar a partir de um arquivo de imagem
img = ImageClip("caminho/para/imagem.jpg")

# Parâmetros comuns
img = ImageClip(
    "caminho/para/imagem.jpg",
    is_mask=False,  # Se é uma máscara
    transparent=True,  # Fundo transparente
    duration=10  # Duração
)
```

### ImageSequenceClip
Cria um clipe a partir de uma sequência de imagens.

```python
# Criar a partir de uma lista de imagens
imagens = ["frame001.png", "frame002.png", "frame003.png"]
seq = ImageSequenceClip(imagens, fps=24)

# Parâmetros comuns
seq = ImageSequenceClip(
    imagens,  # Lista de caminhos para as imagens
    fps=24,  # Quadros por segundo
    durations=None,  # Lista de durações para cada imagem
    with_mask=True,  # Usar máscaras se disponíveis
    load_images=True  # Carregar imagens imediatamente
)
```

### Métodos de Manipulação de Imagem
```python
# Definir duração
img_duracao = img.with_duration(10)  # Duração fixa

# Definir tempo de início
img_inicio = img.with_start(5)  # Começar no segundo 5

# Definir tempo de término
img_termino = img.with_end(15)  # Terminar no segundo 15

# Definir posição
img_posicionado = img.with_position((100, 100))  # Posição fixa
img_posicionado = img.with_position(('center', 'center'))  # Centralizado
img_posicionado = img.with_position(('left', 'top'))  # Canto superior esquerdo

# Redimensionar
img_redimensionado = img.resize(width=320)  # Largura específica
img_redimensionado = img.resize(height=240)  # Altura específica
img_redimensionado = img.resize(0.5)  # Fator de escala
img_redimensionado = img.resize((320, 240))  # Tamanho específico

# Rotacionar
img_rotacionado = img.rotate(angle=45)  # Ângulo em graus

# Espelhar
img_espelhado_x = img.fx(vfx.mirror_x)  # Espelhar horizontalmente
img_espelhado_y = img.fx(vfx.mirror_y)  # Espelhar verticalmente
```

## Efeitos e Transições

### FadeIn e FadeOut (MoviePy 2.1.2)
```python
# Aplicar fade in (novo método na versão 2.1.2)
clip_fadein = clip.with_effects([FadeIn(2.0)])  # Fade in de 2 segundos

# Aplicar fade out (novo método na versão 2.1.2)
clip_fadeout = clip.with_effects([FadeOut(2.0)])  # Fade out de 2 segundos

# Aplicar ambos
clip_fade = clip.with_effects([FadeIn(2.0), FadeOut(2.0)])  # Fade in e out de 2 segundos
```

### Efeitos de Cor
```python
# Preto e branco
clip_bw = clip.fx(blackwhite)

# Ajustar brilho e contraste
clip_bc = clip.fx(lum_contrast, lum=0.5, contrast=1.5)

# Máscara de cor
clip_mask = clip.fx(mask_color, color=[100, 150, 200], thr=100)

# Inverter cores
clip_invert = clip.fx(vfx.invert_colors)

# Corrigir gama
clip_gamma = clip.fx(vfx.gamma_corr, gamma=1.5)

# Equalizar histograma
clip_eq = clip.fx(vfx.headblur)
```

### Efeitos de Movimento
```python
# Desfoque de movimento
clip_motion = clip.fx(vfx.motion_blur, radius=5, angle=45)

# Desfoque gaussiano
clip_gauss = clip.fx(vfx.gaussian_blur, sigma=5)

# Desfoque de caixa
clip_box = clip.fx(vfx.box_blur, radius=5)

# Nitidez
clip_sharp = clip.fx(vfx.sharpen, radius=5, sigma=1.0)
```

### Transições
```python
# Transição de fade
clip1 = clip1.with_effects([FadeOut(1.0)])
clip2 = clip2.with_effects([FadeIn(1.0)])
transicao = concatenate_videoclips([clip1, clip2])

# Transição de deslizamento
clip1 = clip1.with_position((0, 0))
clip2 = clip2.with_position((640, 0))
transicao = CompositeVideoClip([clip1, clip2])

# Transição de zoom
clip1 = clip1.with_position((0, 0))
clip2 = clip2.resize(0.5).with_position((320, 240))
transicao = CompositeVideoClip([clip1, clip2])
```

## Composição

### CompositeVideoClip
Combina múltiplos clipes em um único vídeo.

```python
# Combinar clipes
final = CompositeVideoClip([clip1, clip2, clip3])

# Parâmetros comuns
final = CompositeVideoClip(
    [clip1, clip2, clip3],  # Lista de clipes
    size=(640, 480),  # Tamanho do vídeo final
    bg_color=None,  # Cor de fundo
    use_bgclip=True,  # Usar o primeiro clipe como fundo
    masks=None,  # Máscaras para cada clipe
    is_mask=False  # Se o resultado é uma máscara
)
```

### concatenate_videoclips
Concatena múltiplos clipes em sequência.

```python
# Concatenar clipes (método atualizado na versão 2.1.2)
final = concatenate_videoclips([clip1, clip2, clip3])

# Parâmetros comuns
final = concatenate_videoclips(
    [clip1, clip2, clip3],  # Lista de clipes
    method="chain",  # Método de concatenação
    transition=None,  # Transição entre clipes
    bg_color=None,  # Cor de fundo
    padding=0,  # Espaçamento entre clipes
    is_mask=False  # Se o resultado é uma máscara
)
```

### clips_array
Organiza clipes em uma grade.

```python
# Organizar clipes em uma grade 2x2
grade = clips_array([[clip1, clip2], [clip3, clip4]])

# Parâmetros comuns
grade = clips_array(
    [[clip1, clip2], [clip3, clip4]],  # Matriz de clipes
    rows_widths=None,  # Largura das linhas
    cols_heights=None,  # Altura das colunas
    bg_color=None  # Cor de fundo
)
```

## Exportação

### write_videofile
Exporta um clipe para um arquivo de vídeo.

```python
# Exportar vídeo (método atualizado na versão 2.1.2)
clip.write_videofile("saida.mp4", fps=24)

# Parâmetros comuns
clip.write_videofile(
    "saida.mp4",  # Caminho do arquivo de saída
    fps=24,  # Quadros por segundo
    codec='libx264',  # Codec de vídeo
    audio_codec='aac',  # Codec de áudio
    bitrate=None,  # Taxa de bits
    audio_bitrate=None,  # Taxa de bits do áudio
    preset='medium',  # Predefinição de codificação
    threads=None,  # Número de threads
    ffmpeg_params=None,  # Parâmetros adicionais do FFmpeg
    verbose=False,  # Exibir informações detalhadas (removido na 2.1.2)
    logger='bar'  # Tipo de logger
)
```

### write_gif
Exporta um clipe para um arquivo GIF.

```python
# Exportar GIF
clip.write_gif("saida.gif", fps=24)

# Parâmetros comuns
clip.write_gif(
    "saida.gif",  # Caminho do arquivo de saída
    fps=24,  # Quadros por segundo
    program='imageio',  # Programa para criar o GIF
    opt='nq',  # Otimização
    fuzz=1,  # Nível de fuzz
    verbose=False,  # Exibir informações detalhadas
    colors=None,  # Número de cores
    tempfiles=False  # Usar arquivos temporários
)
```

### write_imageseq
Exporta um clipe como uma sequência de imagens.

```python
# Exportar sequência de imagens
clip.write_imageseq("frame_%03d.png", fps=24)

# Parâmetros comuns
clip.write_imageseq(
    "frame_%03d.png",  # Padrão de nome de arquivo
    fps=24,  # Quadros por segundo
    verbose=False,  # Exibir informações detalhadas
    with_mask=True  # Incluir máscaras
)
```

## Métodos Úteis

### Informações do Clipe
```python
# Duração
duracao = clip.duration

# Tamanho
largura, altura = clip.size

# FPS
fps = clip.fps

# Taxa de bits
bitrate = clip.bitrate

# Número de quadros
n_frames = int(clip.duration * clip.fps)

# Verificar se tem áudio
tem_audio = clip.audio is not None

# Verificar se é máscara
eh_mask = clip.is_mask
```

### Manipulação de Tempo
```python
# Obter quadro em um tempo específico
frame = clip.get_frame(t=5.0)  # Quadro no segundo 5

# Iterar sobre os quadros
for t, frame in clip.iter_frames(with_times=True):
    # t: tempo do quadro
    # frame: array NumPy do quadro
    pass

# Obter subclipe
subclip = clip.subclip(start=5, end=10)  # Do segundo 5 ao 10

# Repetir clipe
repetido = clip.loop(n=3)  # Repetir 3 vezes

# Inverter clipe
invertido = clip.time_mirror()  # Reproduzir de trás para frente
```

### Manipulação de Áudio
```python
# Adicionar áudio a um clipe de vídeo
clip_com_audio = clip.set_audio(audio_clip)

# Remover áudio
clip_sem_audio = clip.without_audio()

# Obter áudio de um clipe
audio = clip.audio

# Ajustar volume do áudio
clip_volume = clip.volumex(factor=2.0)  # 2x mais alto
```

### Manipulação de Máscaras
```python
# Criar máscara
mask = ColorClip(size=(640, 480), color=(255, 255, 255), duration=10)
mask = mask.with_effects([FadeIn(2), FadeOut(2)])

# Aplicar máscara
clip_com_mask = clip.with_mask(mask)

# Criar máscara a partir de texto
txt_mask = TextClip(
    text="Máscara",
    font_size=48,
    color='white',
    font='C:/Windows/Fonts/arial.ttf'
)
txt_mask = txt_mask.with_position(('center', 'center')).with_duration(10)

# Aplicar máscara de texto
clip_com_txt_mask = clip.with_mask(txt_mask)
```

## Parâmetros Comuns

### Cores
```python
# Cores RGB
vermelho = (255, 0, 0)
verde = (0, 255, 0)
azul = (0, 0, 255)
branco = (255, 255, 255)
preto = (0, 0, 0)
amarelo = (255, 255, 0)
ciano = (0, 255, 255)
magenta = (255, 0, 255)

# Cores hexadecimais
vermelho_hex = "#FF0000"
verde_hex = "#00FF00"
azul_hex = "#0000FF"
```

### Posições
```python
# Posição absoluta
posicao = (100, 100)  # x=100, y=100

# Posição relativa
posicao = ('center', 'center')  # Centralizado
posicao = ('left', 'top')  # Canto superior esquerdo
posicao = ('right', 'bottom')  # Canto inferior direito
posicao = ('center', 'top')  # Topo centralizado
posicao = ('left', 'center')  # Esquerda centralizada
```

### Tamanhos
```python
# Tamanho absoluto
tamanho = (640, 480)  # largura=640, altura=480

# Tamanho relativo
tamanho = (0.5, 0.5)  # Metade do tamanho original
```

### Fontes Comuns (Windows)
```python
# Fontes do Windows
arial = 'C:/Windows/Fonts/arial.ttf'
times = 'C:/Windows/Fonts/times.ttf'
courier = 'C:/Windows/Fonts/cour.ttf'
comic = 'C:/Windows/Fonts/comic.ttf'
impact = 'C:/Windows/Fonts/impact.ttf'
```

### Codecs Comuns
```python
# Codecs de vídeo
codec_h264 = 'libx264'
codec_mpeg4 = 'mpeg4'
codec_vp9 = 'libvpx-vp9'
codec_hevc = 'libx265'

# Codecs de áudio
codec_aac = 'aac'
codec_mp3 = 'libmp3lame'
codec_vorbis = 'libvorbis'
codec_opus = 'libopus'
```

## Exemplos Rápidos

### Vídeo Simples com Texto
```python
from moviepy.editor import *

# Criar fundo
background = ColorClip(size=(640, 480), color=(0, 0, 0), duration=10)

# Criar texto
txt = TextClip(
    text="Exemplo Rápido",
    font_size=48,
    color='white',
    font='C:/Windows/Fonts/arial.ttf'
)
txt = txt.with_position(('center', 'center')).with_duration(10)

# Combinar
final = CompositeVideoClip([background, txt])

# Exportar
final.write_videofile("exemplo_rapido.mp4", fps=24)
```

### Vídeo com Transição
```python
from moviepy.editor import *
from moviepy.video.fx import FadeIn, FadeOut

# Criar clipes
clip1 = ColorClip(size=(640, 480), color=(255, 0, 0), duration=5)
clip2 = ColorClip(size=(640, 480), color=(0, 255, 0), duration=5)

# Adicionar transições
clip1 = clip1.with_effects([FadeOut(1)])
clip2 = clip2.with_effects([FadeIn(1)])

# Concatenar
final = concatenate_videoclips([clip1, clip2])

# Exportar
final.write_videofile("exemplo_transicao.mp4", fps=24)
```

### Vídeo com Áudio
```python
from moviepy.editor import *
import numpy as np

# Criar vídeo
video = ColorClip(size=(640, 480), color=(100, 100, 200), duration=10)

# Criar áudio
duration = 10
sample_rate = 44100
t = np.linspace(0, duration, int(sample_rate * duration))
audio_data = np.sin(2 * np.pi * 440 * t)  # 440 Hz
audio_data = audio_data / np.max(np.abs(audio_data)) * 0.5
audio = AudioArrayClip(audio_data, fps=sample_rate)

# Adicionar áudio ao vídeo
video_com_audio = video.set_audio(audio)

# Exportar
video_com_audio.write_videofile("exemplo_audio.mp4", fps=24)
```

### Vídeo com Múltiplas Camadas
```python
from moviepy.editor import *

# Criar fundo
background = ColorClip(size=(640, 480), color=(0, 0, 0), duration=10)

# Criar camadas
camada1 = ColorClip(size=(200, 200), color=(255, 0, 0), duration=10)
camada1 = camada1.with_position((50, 50))

camada2 = ColorClip(size=(200, 200), color=(0, 255, 0), duration=10)
camada2 = camada2.with_position((250, 150))

camada3 = ColorClip(size=(200, 200), color=(0, 0, 255), duration=10)
camada3 = camada3.with_position((150, 250))

# Criar texto
txt = TextClip(
    text="Múltiplas Camadas",
    font_size=36,
    color='white',
    font='C:/Windows/Fonts/arial.ttf'
)
txt = txt.with_position(('center', 20)).with_duration(10)

# Combinar
final = CompositeVideoClip([background, camada1, camada2, camada3, txt])

# Exportar
final.write_videofile("exemplo_camadas.mp4", fps=24)
```

## Solução de Problemas Comuns

### Erros Comuns e Soluções

#### Erro: "AttributeError: 'VideoFileClip' object has no attribute 'fadein'"
**Problema:** Usando o método antigo de fadein na versão 2.1.2
**Solução:** Use o novo método com efeitos
```python
# Antigo (não funciona na 2.1.2)
clip.fadein(2)

# Novo (funciona na 2.1.2)
clip.with_effects([FadeIn(2)])
```

#### Erro: "TypeError: write_videofile() got an unexpected keyword argument 'verbose'"
**Problema:** Usando o parâmetro verbose na versão 2.1.2
**Solução:** Remova o parâmetro verbose
```python
# Antigo (não funciona na 2.1.2)
clip.write_videofile("saida.mp4", fps=24, verbose=False)

# Novo (funciona na 2.1.2)
clip.write_videofile("saida.mp4", fps=24)
```

#### Erro: "AttributeError: module 'moviepy.editor' has no attribute 'concatenate'"
**Problema:** Usando o método antigo de concatenação na versão 2.1.2
**Solução:** Use o novo método concatenate_videoclips
```python
# Antigo (não funciona na 2.1.2)
concatenate([clip1, clip2])

# Novo (funciona na 2.1.2)
concatenate_videoclips([clip1, clip2])
```

#### Erro: "OSError: [WinError 2] The system cannot find the file specified"
**Problema:** FFmpeg não está instalado ou não está no PATH
**Solução:** Instale o FFmpeg e adicione ao PATH
```python
# Verificar se o FFmpeg está instalado
import subprocess
try:
    subprocess.run(["ffmpeg", "-version"], check=True)
    print("FFmpeg está instalado")
except subprocess.CalledProcessError:
    print("FFmpeg não está instalado ou não está no PATH")
```

#### Erro: "ValueError: Could not find the font specified"
**Problema:** Fonte não encontrada
**Solução:** Use o caminho completo para a fonte
```python
# Errado
txt = TextClip(text="Exemplo", font_size=48, color='white', font='arial.ttf')

# Correto
txt = TextClip(text="Exemplo", font_size=48, color='white', font='C:/Windows/Fonts/arial.ttf')
```

### Dicas de Performance

#### Reduzir o Tamanho do Vídeo
```python
# Reduzir a resolução
clip = clip.resize(width=640)  # Reduzir para 640px de largura

# Reduzir a taxa de bits
clip.write_videofile("saida.mp4", fps=24, bitrate="500k")

# Usar codec mais eficiente
clip.write_videofile("saida.mp4", fps=24, codec='libx265')
```

#### Acelerar o Processamento
```python
# Reduzir a resolução durante o processamento
clip = clip.resize(width=1280)  # Processar em 1280px

# Usar mais threads
clip.write_videofile("saida.mp4", fps=24, threads=4)

# Desativar logs detalhados
clip.write_videofile("saida.mp4", fps=24, logger=None)
```

#### Economizar Memória
```python
# Processar em partes
for i in range(0, int(clip.duration), 10):
    subclip = clip.subclip(i, min(i + 10, clip.duration))
    # Processar subclip
    subclip.write_videofile(f"parte_{i}.mp4", fps=24)

# Liberar memória
del clip
import gc
gc.collect()
```

---

Este guia de referência rápida foi projetado para ser uma consulta prática durante o desenvolvimento com MoviePy no projeto auto-video-producerV5-dev, especialmente focado na versão 2.1.2.