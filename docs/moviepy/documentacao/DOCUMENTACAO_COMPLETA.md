# Documentação Completa do MoviePy

## Índice
1. [Introdução](#introdução)
2. [Instalação](#instalação)
3. [Configuração](#configuração)
4. [API Básica](#api-básica)
5. [Componentes Principais](#componentes-principais)
6. [Exemplos de Uso](#exemplos-de-uso)
7. [Solução de Problemas](#solução-de-problemas)
8. [Atualizações e Mudanças](#atualizações-e-mudanças)
9. [Testes](#testes)
10. [Referências](#referências)

## Introdução

O MoviePy é uma biblioteca Python para edição de vídeo programática. Ele permite criar, modificar e combinar clipes de vídeo e áudio de forma eficiente. Esta documentação cobre a instalação, configuração, uso básico e avançado do MoviePy no contexto do projeto auto-video-producerV5-dev.

### Características Principais
- Edição de vídeo não-linear
- Suporte a diversos formatos de vídeo e áudio
- Efeitos e transições personalizáveis
- Integração com outras bibliotecas como NumPy e PIL
- Exportação para diversos formatos

## Instalação

### Requisitos do Sistema
- Python 3.8 ou superior
- Windows, macOS ou Linux
- Pelo menos 4GB de RAM
- Espaço em disco para instalação de dependências

### Instalação Básica
```bash
pip install moviepy
```

### Instalação com Dependências Opcionais
```bash
pip install moviepy[optional]
```

### Verificação da Instalação
```python
import moviepy
print(moviepy.__version__)
```

### Instalação no Projeto
Para o projeto auto-video-producerV5-dev, use o script de instalação dedicado:
```bash
python INSTALAR_MOVIEPY_FINAL.bat
```

## Configuração

### Configuração Básica
```python
from moviepy.editor import *
import moviepy.config as config

# Configurar diretório temporário
config.IMAGEMAGICK_BINARY = r'C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe'
config.FFMPEG_BINARY = r'C:\ffmpeg\bin\ffmpeg.exe'
```

### Configuração de Fontes
```python
# Configurar caminho para fontes
font_path = 'C:/Windows/Fonts/arial.ttf'
```

### Configuração de Performance
```python
# Aumentar limite de memória
import moviepy.config as config
config.MAX_CACHE_SIZE = 2.0  # GB
```

## API Básica

### Criando um Clip de Vídeo
```python
from moviepy.editor import VideoFileClip

# Carregar um vídeo existente
clip = VideoFileClip("video.mp4")

# Criar um clip colorido
from moviepy.editor import ColorClip
color_clip = ColorClip(size=(640, 480), color=(255, 0, 0), duration=10)
```

### Editando Clips
```python
# Cortar um clip
clip = clip.subclip(0, 10)  # Primeiros 10 segundos

# Redimensionar
clip = clip.resize(width=320)

# Rotacionar
clip = clip.rotate(90)

# Adicionar áudio
from moviepy.editor import AudioFileClip
audio = AudioFileClip("audio.mp3")
clip = clip.set_audio(audio)
```

### Exportando Vídeos
```python
# Exportar para MP4
clip.write_videofile("output.mp4", fps=24)

# Exportar com configurações específicas
clip.write_videofile(
    "output.mp4",
    fps=24,
    codec='libx264',
    audio_codec='aac',
    bitrate='8000k'
)
```

## Componentes Principais

### VideoFileClip
```python
from moviepy.editor import VideoFileClip

# Carregar vídeo
clip = VideoFileClip("video.mp4")

# Propriedades
print(f"Duração: {clip.duration} segundos")
print(f"Tamanho: {clip.size}")
print(f"FPS: {clip.fps}")

# Métodos úteis
clip = clip.subclip(start_time, end_time)  # Cortar
clip = clip.resize(width=640)  # Redimensionar
clip = clip.speedx(factor=2)  # Acelerar
```

### AudioFileClip
```python
from moviepy.editor import AudioFileClip

# Carregar áudio
audio = AudioFileClip("audio.mp3")

# Editar áudio
audio = audio.subclip(0, 10)  # Cortar
audio = audio.volumex(0.5)  # Reduzir volume
```

### TextClip
```python
from moviepy.editor import TextClip

# Criar texto
txt_clip = TextClip(
    text="Hello World",
    font_size=24,
    color='white',
    font='C:/Windows/Fonts/arial.ttf'
)

# Posicionar e definir duração
txt_clip = txt_clip.with_position(('center', 'bottom'))
txt_clip = txt_clip.with_start(0)
txt_clip = txt_clip.with_duration(5)
```

### ImageClip
```python
from moviepy.editor import ImageClip

# Criar clip a partir de imagem
img_clip = ImageClip("image.jpg", duration=5)

# Editar
img_clip = img_clip.resize(width=640)
img_clip = img_clip.set_position(('center', 'center'))
```

## Exemplos de Uso

### Exemplo 1: Vídeo Simples com Texto
```python
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

# Carregar vídeo
video = VideoFileClip("video.mp4")

# Criar texto
txt = TextClip(
    text="Título do Vídeo",
    font_size=48,
    color='white',
    font='C:/Windows/Fonts/arial.ttf'
)
txt = txt.with_position(('center', 'top')).with_duration(5)

# Combinar
final = CompositeVideoClip([video, txt])
final.write_videofile("output.mp4")
```

### Exemplo 2: Vídeo com Transições
```python
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.video.fx import FadeIn, FadeOut

# Carregar clipes
clip1 = VideoFileClip("video1.mp4").subclip(0, 10)
clip2 = VideoFileClip("video2.mp4").subclip(0, 10)

# Adicionar transições
clip1 = clip1.with_effects([FadeOut(1)])
clip2 = clip2.with_effects([FadeIn(1)])

# Concatenar
final = concatenate_videoclips([clip1, clip2])
final.write_videofile("output.mp4")
```

### Exemplo 3: Vídeo com Múltiplas Camadas
```python
from moviepy.editor import *

# Carregar vídeo base
base = VideoFileClip("background.mp4")

# Adicionar imagem sobreposta
overlay = ImageClip("overlay.png", duration=base.duration)
overlay = overlay.set_position(('center', 'center'))

# Adicionar texto
title = TextClip(
    text="Título Principal",
    font_size=60,
    color='yellow',
    font='C:/Windows/Fonts/arial.ttf'
)
title = title.with_position(('center', 'center')).with_duration(5)

# Combinar tudo
final = CompositeVideoClip([base, overlay, title])
final.write_videofile("output.mp4")
```

## Solução de Problemas

### Problemas Comuns

#### 1. Erro: "MoviePy not found"
**Solução:**
```bash
pip install moviepy
```

#### 2. Erro: "FFmpeg not found"
**Solução:**
```python
import moviepy.config as config
config.FFMPEG_BINARY = r'C:\caminho\para\ffmpeg.exe'
```

#### 3. Erro: "ImageMagick not found"
**Solução:**
```python
import moviepy.config as config
config.IMAGEMAGICK_BINARY = r'C:\caminho\para\magick.exe'
```

#### 4. Erro: "Font not found"
**Solução:**
```python
# Usar caminho completo para a fonte
font_path = 'C:/Windows/Fonts/arial.ttf'
txt_clip = TextClip(text="Hello", font=font_path)
```

#### 5. Erro: "Method not found" (MoviePy 2.1.2+)
**Solução:**
```python
# Antes (versões antigas)
clip = clip.fadein(1)
clip = clip.fadeout(1)

# Depois (versão 2.1.2+)
from moviepy.video.fx import FadeIn, FadeOut
clip = clip.with_effects([FadeIn(1)])
clip = clip.with_effects([FadeOut(1)])
```

### Dicas de Performance

#### 1. Reduzir Uso de Memória
```python
import moviepy.config as config
config.MAX_CACHE_SIZE = 1.0  # Reduzir cache
```

#### 2. Otimizar Exportação
```python
# Usar configurações otimizadas
clip.write_videofile(
    "output.mp4",
    fps=24,
    codec='libx264',
    audio_codec='aac',
    threads=4,  # Usar múltiplos threads
    preset='fast'  # Balance entre qualidade e velocidade
)
```

#### 3. Limpar Cache
```python
from moviepy.tools import delete_cache
delete_cache()
```

## Atualizações e Mudanças

### Mudanças na Versão 2.1.2

#### 1. API do TextClip
**Antes:**
```python
txt_clip = TextClip(
    "Hello World",
    fontsize=24,
    color='white'
).set_position(('center', 'bottom')).set_start(0).set_duration(5)
```

**Depois:**
```python
txt_clip = TextClip(
    text="Hello World",
    font_size=24,
    color='white',
    font='C:/Windows/Fonts/arial.ttf'
)
txt_clip = txt_clip.with_position(('center', 'bottom')).with_start(0).with_duration(5)
```

#### 2. Métodos de Efeito
**Antes:**
```python
clip = clip.fadein(1)
clip = clip.fadeout(1)
```

**Depois:**
```python
from moviepy.video.fx import FadeIn, FadeOut
clip = clip.with_effects([FadeIn(1)])
clip = clip.with_effects([FadeOut(1)])
```

#### 3. Método concatenate
**Antes:**
```python
final_clip = clip1.concatenate(clip2)
```

**Depois:**
```python
from moviepy.editor import concatenate_videoclips
final_clip = concatenate_videoclips([clip1, clip2])
```

#### 4. Parâmetro verbose
**Antes:**
```python
clip.write_videofile("output.mp4", verbose=False)
```

**Depois:**
```python
clip.write_videofile("output.mp4")
```

## Testes

### Teste Básico de Funcionalidade
```python
from moviepy.editor import ColorClip, TextClip, CompositeVideoClip

# Criar clip colorido
color_clip = ColorClip(size=(640, 480), color=(255, 0, 0), duration=5)

# Adicionar texto
txt_clip = TextClip(
    text="Teste MoviePy",
    font_size=48,
    color='white',
    font='C:/Windows/Fonts/arial.ttf'
)
txt_clip = txt_clip.with_position(('center', 'center')).with_duration(5)

# Combinar
final = CompositeVideoClip([color_clip, txt_clip])
final.write_videofile("teste_basico.mp4")
print("Teste básico concluído!")
```

### Teste de Transições
```python
from moviepy.editor import ColorClip, concatenate_videoclips
from moviepy.video.fx import FadeIn, FadeOut

# Criar clipes
clip1 = ColorClip(size=(640, 480), color=(255, 0, 0), duration=3)
clip2 = ColorClip(size=(640, 480), color=(0, 255, 0), duration=3)

# Adicionar transições
clip1 = clip1.with_effects([FadeOut(1)])
clip2 = clip2.with_effects([FadeIn(1)])

# Concatenar
final = concatenate_videoclips([clip1, clip2])
final.write_videofile("teste_transicoes.mp4")
print("Teste de transições concluído!")
```

### Teste de Texto
```python
from moviepy.editor import ColorClip, TextClip, CompositeVideoClip

# Criar fundo
background = ColorClip(size=(640, 480), color=(0, 0, 0), duration=10)

# Criar texto
textos = [
    {"text": "Primeiro Texto", "start": 0, "duration": 3},
    {"text": "Segundo Texto", "start": 3, "duration": 3},
    {"text": "Terceiro Texto", "start": 6, "duration": 4}
]

clips = [background]
for segment in textos:
    txt_clip = TextClip(
        text=segment['text'],
        font_size=36,
        color='white',
        font='C:/Windows/Fonts/arial.ttf'
    )
    txt_clip = txt_clip.with_position(('center', 'center'))
    txt_clip = txt_clip.with_start(segment['start'])
    txt_clip = txt_clip.with_duration(segment['duration'])
    clips.append(txt_clip)

# Combinar
final = CompositeVideoClip(clips)
final.write_videofile("teste_texto.mp4")
print("Teste de texto concluído!")
```

### Teste Completo
```python
from moviepy.editor import *
from moviepy.video.fx import FadeIn, FadeOut

# Criar clipes de teste
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

# Adicionar texto
txt_clip = TextClip(
    text="Teste Completo MoviePy",
    font_size=48,
    color='white',
    font='C:/Windows/Fonts/arial.ttf'
)
txt_clip = txt_clip.with_position(('center', 'center')).with_duration(9)

# Combinar tudo
final = CompositeVideoClip([final, txt_clip])
final.write_videofile("teste_completo.mp4")
print("Teste completo concluído!")
```

## Referências

### Documentação Oficial
- [MoviePy Documentation](https://zulko.github.io/moviepy/)
- [MoviePy GitHub](https://github.com/Zulko/moviepy)

### Dependências
- [FFmpeg](https://ffmpeg.org/)
- [ImageMagick](https://imagemagick.org/)
- [NumPy](https://numpy.org/)
- [PIL/Pillow](https://python-pillow.org/)

### Tutoriais e Recursos
- [MoviePy Tutorials](https://zulko.github.io/moviepy/getting_started/videoclips.html)
- [Video Editing with Python](https://www.blog.pythonlibrary.org/2021/06/23/video-editing-with-python-and-moviepy/)

### Comunidade
- [Stack Overflow](https://stackoverflow.com/questions/tagged/moviepy)
- [Reddit r/moviepy](https://www.reddit.com/r/moviepy/)
- [GitHub Issues](https://github.com/Zulko/moviepy/issues)

---

Esta documentação foi criada para o projeto auto-video-producerV5-dev e serve como referência completa para o uso do MoviePy no contexto do projeto.