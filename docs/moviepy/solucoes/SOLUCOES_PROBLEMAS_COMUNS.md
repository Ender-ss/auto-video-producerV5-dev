# Soluções de Problemas Comuns com MoviePy

## Índice
1. [Introdução](#introdução)
2. [Problemas de Instalação](#problemas-de-instalação)
3. [Problemas de Compatibilidade](#problemas-de-compatibilidade)
4. [Problemas de Performance](#problemas-de-performance)
5. [Problemas de Exportação](#problemas-de-exportação)
6. [Problemas de Áudio](#problemas-de-áudio)
7. [Problemas de Texto](#problemas-de-texto)
8. [Problemas de Efeitos](#problemas-de-efeitos)
9. [Problemas de Composição](#problemas-de-composição)
10. [Problemas de Memória](#problemas-de-memória)
11. [Problemas Específicos da Versão 2.1.2](#problemas-específicos-da-versão-212)
12. [Soluções Avançadas](#soluções-avançadas)
13. [Scripts de Diagnóstico](#scripts-de-diagnóstico)

## Introdução

Este documento contém soluções para problemas comuns encontrados ao trabalhar com MoviePy, especialmente focado na versão 2.1.2 no projeto auto-video-producerV5-dev. Cada problema inclui uma descrição, causa provável e soluções práticas.

### Objetivo
- Fornecer soluções rápidas para problemas comuns
- Documentar mudanças importantes na versão 2.1.2
- Oferecer scripts de diagnóstico
- Servir como referência para solução de problemas

## Problemas de Instalação

### Problema 1: FFmpeg não encontrado
**Descrição:** Erro ao tentar exportar vídeos, indicando que FFmpeg não está instalado ou não está no PATH.

**Causa:** MoviePy depende do FFmpeg para processamento de vídeo, mas ele não está instalado ou não está acessível.

**Soluções:**

1. **Instalar FFmpeg:**
   ```python
   # Verificar se o FFmpeg está instalado
   import subprocess
   try:
       subprocess.run(["ffmpeg", "-version"], check=True, capture_output=True)
       print("FFmpeg está instalado")
   except subprocess.CalledProcessError:
       print("FFmpeg não está instalado")
   ```

2. **Baixar FFmpeg:**
   - Windows: Baixe de https://ffmpeg.org/download.html
   - Adicione o diretório bin do FFmpeg ao PATH do sistema

3. **Instalar via conda:**
   ```bash
   conda install ffmpeg
   ```

4. **Especificar caminho do FFmpeg:**
   ```python
   import os
   os.environ["FFMPEG_BINARY"] = "c:/caminho/para/ffmpeg/bin/ffmpeg.exe"
   ```

### Problema 2: Pillow não instalado
**Descrição:** Erro ao tentar usar TextClip ou ImageClip, indicando que Pillow não está instalado.

**Causa:** MoviePy depende do Pillow para processamento de imagem, mas ele não está instalado.

**Soluções:**

1. **Instalar Pillow:**
   ```bash
   pip install pillow
   ```

2. **Instalar via conda:**
   ```bash
   conda install pillow
   ```

### Problema 3: Imagemagick não encontrado
**Descrição:** Erro ao tentar usar TextClip, indicando que Imagemagick não está instalado.

**Causa:** MoviePy depende do Imagemagick para renderização de texto, mas ele não está instalado.

**Soluções:**

1. **Instalar Imagemagick:**
   - Windows: Baixe de https://imagemagick.org/script/download.php
   - Certifique-se de marcar a opção "Add application directory to your system path"

2. **Especificar caminho do Imagemagick:**
   ```python
   import os
   os.environ["IMAGEMAGICK_BINARY"] = "c:/caminho/para/imagemagick/convert.exe"
   ```

## Problemas de Compatibilidade

### Problema 4: Erro com método fadein/fadeout
**Descrição:** AttributeError: 'VideoFileClip' object has no attribute 'fadein'/'fadeout'

**Causa:** Na versão 2.1.2, os métodos fadein/fadeout foram substituídos pelo sistema de efeitos.

**Soluções:**

1. **Usar o novo método com efeitos:**
   ```python
   # Antigo (não funciona na 2.1.2)
   clip.fadein(2)
   clip.fadeout(2)
   
   # Novo (funciona na 2.1.2)
   from moviepy.video.fx import FadeIn, FadeOut
   clip.with_effects([FadeIn(2)])
   clip.with_effects([FadeOut(2)])
   clip.with_effects([FadeIn(2), FadeOut(2)])
   ```

2. **Criar função de compatibilidade:**
   ```python
   def fadein_compat(clip, duration):
       return clip.with_effects([FadeIn(duration)])
   
   def fadeout_compat(clip, duration):
       return clip.with_effects([FadeOut(duration)])
   
   # Uso
   clip = fadein_compat(clip, 2)
   clip = fadeout_compat(clip, 2)
   ```

### Problema 5: Erro com parâmetro verbose
**Descrição:** TypeError: write_videofile() got an unexpected keyword argument 'verbose'

**Causa:** Na versão 2.1.2, o parâmetro verbose foi removido do método write_videofile.

**Soluções:**

1. **Remover o parâmetro verbose:**
   ```python
   # Antigo (não funciona na 2.1.2)
   clip.write_videofile("saida.mp4", fps=24, verbose=False)
   
   # Novo (funciona na 2.1.2)
   clip.write_videofile("saida.mp4", fps=24)
   ```

2. **Usar o parâmetro logger:**
   ```python
   # Usar None para desativar logs
   clip.write_videofile("saida.mp4", fps=24, logger=None)
   
   # Usar 'bar' para barra de progresso
   clip.write_videofile("saida.mp4", fps=24, logger='bar')
   ```

### Problema 6: Erro com método concatenate
**Descrição:** AttributeError: module 'moviepy.editor' has no attribute 'concatenate'

**Causa:** Na versão 2.1.2, o método concatenate foi substituído por concatenate_videoclips.

**Soluções:**

1. **Usar o novo método:**
   ```python
   # Antigo (não funciona na 2.1.2)
   from moviepy.editor import concatenate
   final = concatenate([clip1, clip2])
   
   # Novo (funciona na 2.1.2)
   from moviepy.editor import concatenate_videoclips
   final = concatenate_videoclips([clip1, clip2])
   ```

2. **Criar função de compatibilidade:**
   ```python
   def concatenate_compat(clips):
       return concatenate_videoclips(clips)
   
   # Uso
   final = concatenate_compat([clip1, clip2])
   ```

### Problema 7: Erro com TextClip
**Descrição:** Erros diversos ao usar TextClip, como "ValueError: Could not find the font specified"

**Causa:** Mudanças na API do TextClip na versão 2.1.2 e problemas com caminhos de fontes.

**Soluções:**

1. **Usar caminho completo para fontes:**
   ```python
   # Errado
   txt = TextClip(text="Exemplo", font_size=48, color='white', font='arial.ttf')
   
   # Correto
   txt = TextClip(
       text="Exemplo", 
       font_size=48, 
       color='white', 
       font='C:/Windows/Fonts/arial.ttf'
   )
   ```

2. **Especificar método de renderização:**
   ```python
   txt = TextClip(
       text="Exemplo", 
       font_size=48, 
       color='white', 
       font='C:/Windows/Fonts/arial.ttf',
       method='label'  # ou 'caption'
   )
   ```

3. **Definir tamanho explicitamente:**
   ```python
   txt = TextClip(
       text="Exemplo", 
       font_size=48, 
       color='white', 
       font='C:/Windows/Fonts/arial.ttf',
       size=(640, 480)
   )
   ```

## Problemas de Performance

### Problema 8: Processamento lento
**Descrição:** O processamento de vídeos está muito lento.

**Causa:** Vários fatores podem contribuir para o processamento lento, incluindo resolução alta, efeitos complexos e configurações inadequadas.

**Soluções:**

1. **Reduzir resolução durante o processamento:**
   ```python
   # Reduzir resolução
   clip = clip.resize(width=1280)  # Reduzir para 1280px de largura
   
   # Processar
   # ... aplicar efeitos ...
   
   # Redimensionar para o tamanho final se necessário
   clip = clip.resize(width=1920)
   ```

2. **Usar mais threads:**
   ```python
   clip.write_videofile("saida.mp4", fps=24, threads=4)
   ```

3. **Usar preset de codificação mais rápido:**
   ```python
   clip.write_videofile("saida.mp4", fps=24, preset='ultrafast')
   ```

4. **Desativar logs detalhados:**
   ```python
   clip.write_videofile("saida.mp4", fps=24, logger=None)
   ```

5. **Processar em partes:**
   ```python
   # Dividir o vídeo em partes
   partes = []
   duracao_parte = 30  # 30 segundos por parte
   
   for i in range(0, int(clip.duration), duracao_parte):
       parte = clip.subclip(i, min(i + duracao_parte, clip.duration))
       # Processar parte
       partes.append(parte)
   
   # Juntar partes
   final = concatenate_videoclips(partes)
   ```

### Problema 9: Alto consumo de memória
**Descrição:** O processo consome muita memória RAM durante o processamento.

**Causa:** MoviePy carrega os vídeos na memória, e vídeos longos ou de alta resolução podem consumir muita memória.

**Soluções:**

1. **Processar em partes:**
   ```python
   # Processar em partes menores
   for i in range(0, int(clip.duration), 30):  # 30 segundos por parte
       parte = clip.subclip(i, min(i + 30, clip.duration))
       # Processar parte
       parte.write_videofile(f"parte_{i}.mp4", fps=24)
       
       # Liberar memória
       del parte
       import gc
       gc.collect()
   
   # Juntar partes depois
   ```

2. **Usar geradores para processamento:**
   ```python
   def processar_em_partes(clip, duracao_parte=30):
       for i in range(0, int(clip.duration), duracao_parte):
           parte = clip.subclip(i, min(i + duracao_parte, clip.duration))
           yield parte
           del parte
           import gc
           gc.collect()
   
   # Uso
   partes = list(processar_em_partes(clip))
   final = concatenate_videoclips(partes)
   ```

3. **Reduzir resolução:**
   ```python
   # Reduzir resolução
   clip = clip.resize(width=1280)
   ```

4. **Liberar memória manualmente:**
   ```python
   # Depois de usar um clipe
   del clip
   import gc
   gc.collect()
   ```

### Problema 10: Uso elevado de CPU
**Descrição:** O processo utiliza 100% da CPU durante o processamento.

**Causa:** O processamento de vídeo é intensivo em CPU, especialmente com efeitos complexos.

**Soluções:**

1. **Limitar o número de threads:**
   ```python
   clip.write_videofile("saida.mp4", fps=24, threads=2)
   ```

2. **Usar preset de codificação mais eficiente:**
   ```python
   clip.write_videofile("saida.mp4", fps=24, preset='slow')
   ```

3. **Reduzir a complexidade dos efeitos:**
   ```python
   # Em vez de efeitos complexos, usar mais simples
   # Exemplo: em vez de gaussian_blur com sigma alto
   clip = clip.fx(vfx.gaussian_blur, sigma=2)
   
   # Usar box_blur que é mais rápido
   clip = clip.fx(vfx.box_blur, radius=5)
   ```

4. **Processar durante horários de baixo uso:**
   ```python
   # Adicionar atrasos entre operações intensivas
   import time
   time.sleep(1)  # Esperar 1 segundo entre operações
   ```

## Problemas de Exportação

### Problema 11: Erro ao exportar vídeo
**Descrição:** Erros diversos durante a exportação de vídeos, como "OSError: [WinError 6] The handle is invalid"

**Causa:** Vários fatores podem causar erros na exportação, incluindo problemas com FFmpeg, permissões de arquivo e configurações inadequadas.

**Soluções:**

1. **Verificar se o diretório de saída existe:**
   ```python
   import os
   output_dir = "caminho/para/diretorio"
   os.makedirs(output_dir, exist_ok=True)
   output_path = os.path.join(output_dir, "saida.mp4")
   clip.write_videofile(output_path, fps=24)
   ```

2. **Usar caminhos absolutos:**
   ```python
   import os
   output_path = os.path.abspath("saida.mp4")
   clip.write_videofile(output_path, fps=24)
   ```

3. **Especificar codec explicitamente:**
   ```python
   clip.write_videofile("saida.mp4", fps=24, codec='libx264')
   ```

4. **Reduzir a taxa de bits:**
   ```python
   clip.write_videofile("saida.mp4", fps=24, bitrate="1000k")
   ```

5. **Tentar diferentes formatos:**
   ```python
   # Tentar AVI
   clip.write_videofile("saida.avi", fps=24, codec='mpeg4')
   
   # Tentar MOV
   clip.write_videofile("saida.mov", fps=24, codec='libx264')
   ```

### Problema 12: Vídeo exportado com qualidade ruim
**Descrição:** O vídeo exportado tem qualidade inferior ao esperado.

**Causa:** Configurações de codificação inadequadas podem resultar em perda de qualidade.

**Soluções:**

1. **Aumentar a taxa de bits:**
   ```python
   clip.write_videofile("saida.mp4", fps=24, bitrate="5000k")
   ```

2. **Usar preset de qualidade mais alta:**
   ```python
   clip.write_videofile("saida.mp4", fps=24, preset='slow')
   ```

3. **Usar codec mais eficiente:**
   ```python
   clip.write_videofile("saida.mp4", fps=24, codec='libx265')
   ```

4. **Aumentar a resolução:**
   ```python
   # Redimensionar para resolução maior antes de exportar
   clip = clip.resize(width=1920)
   clip.write_videofile("saida.mp4", fps=24)
   ```

5. **Usar taxa de amostragem de áudio mais alta:**
   ```python
   clip.write_videofile("saida.mp4", fps=24, audio_fps=48000)
   ```

### Problema 13: Áudio e vídeo dessincronizados
**Descrição:** O áudio e o vídeo não estão sincronizados no arquivo exportado.

**Causa:** Problemas com a taxa de amostragem do áudio ou configurações de codificação.

**Soluções:**

1. **Especificar taxa de amostragem do áudio:**
   ```python
   clip.write_videofile("saida.mp4", fps=24, audio_fps=44100)
   ```

2. **Usar codec de áudio específico:**
   ```python
   clip.write_videofile("saida.mp4", fps=24, audio_codec='aac')
   ```

3. **Aumentar a taxa de bits do áudio:**
   ```python
   clip.write_videofile("saida.mp4", fps=24, audio_bitrate="192k")
   ```

4. **Normalizar o áudio antes de exportar:**
   ```python
   # Normalizar áudio
   if clip.audio:
       audio = clip.audio
       audio = audio.fx(afx.audio_normalize)
       clip = clip.set_audio(audio)
   
   clip.write_videofile("saida.mp4", fps=24)
   ```

## Problemas de Áudio

### Problema 14: Áudio não funciona
**Descrição:** O vídeo exportado não tem áudio ou o áudio está distorcido.

**Causa:** Problemas com o codec de áudio, taxa de amostragem ou configurações de volume.

**Soluções:**

1. **Verificar se o clipe tem áudio:**
   ```python
   if clip.audio is None:
       print("O clipe não tem áudio")
   else:
       print("O clipe tem áudio")
   ```

2. **Adicionar áudio explicitamente:**
   ```python
   # Criar áudio silencioso se não existir
   if clip.audio is None:
       duration = clip.duration
       sample_rate = 44100
       silence = np.zeros((int(duration * sample_rate),))
       silence_clip = AudioArrayClip(silence, fps=sample_rate)
       clip = clip.set_audio(silence_clip)
   
   clip.write_videofile("saida.mp4", fps=24)
   ```

3. **Especificar codec de áudio:**
   ```python
   clip.write_videofile("saida.mp4", fps=24, audio_codec='aac')
   ```

4. **Ajustar volume do áudio:**
   ```python
   # Ajustar volume
   if clip.audio:
       audio = clip.audio
       audio = audio.volumex(1.5)  # Aumentar volume em 50%
       clip = clip.set_audio(audio)
   
   clip.write_videofile("saida.mp4", fps=24)
   ```

### Problema 15: Erro ao criar áudio sintético
**Descrição:** Erros ao tentar criar áudio sintético com AudioArrayClip.

**Causa:** Problemas com o formato dos dados do áudio ou configurações incorretas.

**Soluções:**

1. **Verificar o formato dos dados:**
   ```python
   import numpy as np
   
   # Criar áudio sintético corretamente
   duration = 10
   sample_rate = 44100
   t = np.linspace(0, duration, int(duration * sample_rate), False)
   
   # Criar onda senoidal
   frequency = 440  # Hz
   audio_data = np.sin(2 * np.pi * frequency * t)
   
   # Normalizar para o intervalo [-1, 1]
   audio_data = audio_data / np.max(np.abs(audio_data))
   
   # Reduzir amplitude para evitar distorção
   audio_data = audio_data * 0.5
   
   # Criar clipe de áudio
   audio_clip = AudioArrayClip(audio_data, fps=sample_rate)
   ```

2. **Verificar a forma do array:**
   ```python
   # O array deve ser 1D para mono ou 2D para estéreo
   # Mono
   audio_data_mono = np.sin(2 * np.pi * 440 * t)  # Forma: (n_samples,)
   
   # Estéreo
   audio_data_stereo = np.column_stack([
       np.sin(2 * np.pi * 440 * t),  # Canal esquerdo
       np.sin(2 * np.pi * 880 * t)   # Canal direito
   ])  # Forma: (n_samples, 2)
   
   # Criar clipes
   audio_clip_mono = AudioArrayClip(audio_data_mono, fps=sample_rate)
   audio_clip_stereo = AudioArrayClip(audio_data_stereo, fps=sample_rate)
   ```

3. **Usar tipo de dados correto:**
   ```python
   # Usar float32 para melhor precisão
   audio_data = audio_data.astype(np.float32)
   audio_clip = AudioArrayClip(audio_data, fps=sample_rate)
   ```

## Problemas de Texto

### Problema 16: Texto não aparece no vídeo
**Descrição:** O texto não é renderizado no vídeo ou aparece distorcido.

**Causa:** Problemas com fontes, cores ou posicionamento do texto.

**Soluções:**

1. **Usar caminho completo para fontes:**
   ```python
   txt = TextClip(
       text="Exemplo", 
       font_size=48, 
       color='white', 
       font='C:/Windows/Fonts/arial.ttf'
   )
   ```

2. **Verificar se a fonte existe:**
   ```python
   import os
   font_path = 'C:/Windows/Fonts/arial.ttf'
   if not os.path.exists(font_path):
       print(f"Fonte não encontrada: {font_path}")
   ```

3. **Usar cores com contraste:**
   ```python
   # Criar fundo escuro e texto claro
   background = ColorClip(size=(640, 480), color=(0, 0, 0), duration=10)
   txt = TextClip(
       text="Exemplo", 
       font_size=48, 
       color='white',  # Texto branco
       font='C:/Windows/Fonts/arial.ttf'
   )
   ```

4. **Posicionar texto corretamente:**
   ```python
   # Centralizar texto
   txt = txt.with_position(('center', 'center'))
   
   # Posicionar no topo
   txt = txt.with_position(('center', 50))
   
   # Posicionar à esquerda
   txt = txt.with_position((50, 'center'))
   ```

### Problema 17: Erro ao renderizar texto com caracteres especiais
**Descrição:** Erros ao tentar renderizar texto com caracteres especiais ou acentos.

**Causa:** Problemas com codificação de caracteres ou fontes que não suportam os caracteres.

**Soluções:**

1. **Usar fontes que suportam os caracteres:**
   ```python
   # Usar fontes como Arial Unicode MS ou outras que suportam Unicode
   txt = TextClip(
       text="Exemplo com acentos: áéíóú",
       font_size=48,
       color='white',
       font='C:/Windows/Fonts/arialuni.ttf'  # Arial Unicode MS
   )
   ```

2. **Especificar codificação:**
   ```python
   # Usar codificação UTF-8
   texto = "Exemplo com acentos: áéíóú".encode('utf-8').decode('utf-8')
   txt = TextClip(
       text=texto,
       font_size=48,
       color='white',
       font='C:/Windows/Fonts/arial.ttf'
   )
   ```

3. **Usar método de renderização diferente:**
   ```python
   # Tentar diferentes métodos de renderização
   txt = TextClip(
       text="Exemplo com acentos: áéíóú",
       font_size=48,
       color='white',
       font='C:/Windows/Fonts/arial.ttf',
       method='caption'  # ou 'label'
   )
   ```

### Problema 18: Texto cortado ou com tamanho incorreto
**Descrição:** O texto aparece cortado ou com tamanho diferente do esperado.

**Causa:** Problemas com o tamanho do clipe de texto ou configurações de fonte.

**Soluções:**

1. **Definir tamanho explicitamente:**
   ```python
   # Definir tamanho do clipe de texto
   txt = TextClip(
       text="Exemplo",
       font_size=48,
       color='white',
       font='C:/Windows/Fonts/arial.ttf',
       size=(640, 100)  # Largura e altura
   )
   ```

2. **Ajustar tamanho da fonte:**
   ```python
   # Experimentar diferentes tamanhos de fonte
   txt = TextClip(
       text="Exemplo",
       font_size=36,  # Reduzir tamanho
       color='white',
       font='C:/Windows/Fonts/arial.ttf'
   )
   ```

3. **Usar espaçamento entre linhas:**
   ```python
   # Ajustar espaçamento entre linhas para texto múltiplas linhas
   txt = TextClip(
       text="Linha 1\nLinha 2\nLinha 3",
       font_size=48,
       color='white',
       font='C:/Windows/Fonts/arial.ttf',
       interline=1.5  # Espaçamento de 1.5x
   )
   ```

## Problemas de Efeitos

### Problema 19: Efeitos não funcionam
**Descrição:** Os efeitos aplicados não aparecem no vídeo ou causam erros.

**Causa:** Problemas com a importação de efeitos ou uso incorreto da API.

**Soluções:**

1. **Importar efeitos corretamente:**
   ```python
   # Importar efeitos específicos
   from moviepy.video.fx import FadeIn, FadeOut, blackwhite, lum_contrast
   
   # Usar efeitos
   clip = clip.with_effects([FadeIn(2), FadeOut(2)])
   clip = clip.fx(blackwhite)
   clip = clip.fx(lum_contrast, lum=0.5, contrast=1.5)
   ```

2. **Verificar a ordem dos efeitos:**
   ```python
   # A ordem dos efeitos importa
   # Primeiro aplicar efeitos de cor, depois de transição
   clip = clip.fx(blackwhite)  # Primeiro
   clip = clip.with_effects([FadeIn(2), FadeOut(2)])  # Depois
   ```

3. **Usar efeitos compatíveis:**
   ```python
   # Verificar se o efeito é compatível com o tipo de clipe
   # Alguns efeitos só funcionam com VideoClip, outros com AudioClip
   ```

### Problema 20: Efeitos de transição não funcionam
**Descrição:** As transições entre clipes não funcionam corretamente.

**Causa:** Problemas com a sobreposição de clipes ou configurações de tempo.

**Soluções:**

1. **Configurar tempos corretamente:**
   ```python
   # Garantir que os clipes se sobreponham para a transição
   clip1 = clip1.with_end(clip1.duration + 1)  # Estender 1 segundo
   clip2 = clip2.with_start(clip1.duration - 1)  # Começar 1 segundo antes
   
   # Aplicar efeitos de transição
   clip1 = clip1.with_effects([FadeOut(1)])
   clip2 = clip2.with_effects([FadeIn(1)])
   
   # Combinar
   final = CompositeVideoClip([clip1, clip2])
   ```

2. **Usar método de concatenação com transição:**
   ```python
   # Usar método de concatenação com transição
   from moviepy.video.compositing.transitions import crossfade
   
   # Criar transição
   transition = crossfade(clip1, clip2, duration=1)
   
   # Usar transição
   final = concatenate_videoclips([clip1, transition, clip2])
   ```

### Problema 21: Efeitos de cor não funcionam
**Descrição:** Os efeitos de cor não produzem o resultado esperado.

**Causa:** Problemas com os parâmetros dos efeitos ou ordem de aplicação.

**Soluções:**

1. **Ajustar parâmetros dos efeitos:**
   ```python
   # Ajustar parâmetros de brilho e contraste
   clip = clip.fx(lum_contrast, lum=0.5, contrast=1.5)
   
   # Ajustar parâmetros de máscara de cor
   clip = clip.fx(mask_color, color=[100, 150, 200], thr=100)
   ```

2. **Experimentar diferentes valores:**
   ```python
   # Experimentar diferentes valores para encontrar o melhor resultado
   # Brilho: valores entre 0 e 1, onde 0.5 é normal
   # Contraste: valores acima de 1 aumentam o contraste
   clip = clip.fx(lum_contrast, lum=0.7, contrast=1.2)
   ```

3. **Combinar efeitos:**
   ```python
   # Combinar múltiplos efeitos de cor
   clip = clip.fx(blackwhite)
   clip = clip.fx(lum_contrast, lum=0.5, contrast=1.5)
   clip = clip.fx(vfx.gamma_corr, gamma=1.2)
   ```

## Problemas de Composição

### Problema 22: Clipes não se sobrepõem corretamente
**Descrição:** Os clipes não se sobrepõem como esperado na composição.

**Causa:** Problemas com posicionamento, tamanho ou ordem dos clipes.

**Soluções:**

1. **Verificar a ordem dos clipes:**
   ```python
   # A ordem dos clipes importa: os últimos aparecem sobre os primeiros
   final = CompositeVideoClip([
       background,  # Fundo (primeiro)
       clip1,       # Camada intermediária
       clip2,       # Camada superior (último)
   ])
   ```

2. **Posicionar clipes corretamente:**
   ```python
   # Posicionar clipes explicitamente
   clip1 = clip1.with_position((100, 100))
   clip2 = clip2.with_position((200, 200))
   
   final = CompositeVideoClip([background, clip1, clip2])
   ```

3. **Verificar tamanhos dos clipes:**
   ```python
   # Verificar se os clipes têm o tamanho esperado
   print(f"Background size: {background.size}")
   print(f"Clip1 size: {clip1.size}")
   print(f"Clip2 size: {clip2.size}")
   
   # Ajustar tamanhos se necessário
   clip1 = clip1.resize(width=320)
   clip2 = clip2.resize(height=240)
   ```

### Problema 23: Erro ao concatenar clipes
**Descrição:** Erros ao tentar concatenar clipes com tamanhos ou FPS diferentes.

**Causa:** Os clipes precisam ter as mesmas dimensões e FPS para serem concatenados.

**Soluções:**

1. **Padronizar dimensões:**
   ```python
   # Redimensionar todos os clipes para o mesmo tamanho
   target_size = (640, 480)
   
   clip1 = clip1.resize(target_size)
   clip2 = clip2.resize(target_size)
   
   final = concatenate_videoclips([clip1, clip2])
   ```

2. **Padronizar FPS:**
   ```python
   # Garantir que todos os clipes tenham o mesmo FPS
   target_fps = 24
   
   clip1 = clip1.set_fps(target_fps)
   clip2 = clip2.set_fps(target_fps)
   
   final = concatenate_videoclips([clip1, clip2])
   ```

3. **Usar método de concatenação com tratamento de diferenças:**
   ```python
   # Usar método que lida com diferenças de tamanho
   final = concatenate_videoclips(
       [clip1, clip2],
       method="compose",  # Usar composição em vez de chain
       transition=None
   )
   ```

### Problema 24: Erro ao usar clips_array
**Descrição:** Erros ao tentar organizar clipes em uma grade com clips_array.

**Causa:** Problemas com a estrutura da matriz ou tamanhos dos clipes.

**Soluções:**

1. **Verificar a estrutura da matriz:**
   ```python
   # Garantir que a matriz seja retangular
   clips_matrix = [
       [clip1, clip2, clip3],
       [clip4, clip5, clip6],
       [clip7, clip8, clip9]
   ]
   
   # Todas as linhas devem ter o mesmo número de colunas
   ```

2. **Padronizar tamanhos dos clipes:**
   ```python
   # Redimensionar todos os clipes para o mesmo tamanho
   target_size = (320, 240)
   
   clips_matrix = [
       [clip1.resize(target_size), clip2.resize(target_size), clip3.resize(target_size)],
       [clip4.resize(target_size), clip5.resize(target_size), clip6.resize(target_size)],
       [clip7.resize(target_size), clip8.resize(target_size), clip9.resize(target_size)]
   ]
   
   final = clips_array(clips_matrix)
   ```

3. **Especificar dimensões da grade:**
   ```python
   # Especificar largura das colunas e altura das linhas
   final = clips_array(
       clips_matrix,
       rows_widths=[320, 320, 320],  # Largura de cada coluna
       cols_heights=[240, 240, 240]  # Altura de cada linha
   )
   ```

## Problemas de Memória

### Problema 25: Erro de memória insuficiente
**Descrição:** Erro "MemoryError" ou o processo é encerrado por falta de memória.

**Causa:** O vídeo é muito grande ou há muitos clipes carregados na memória.

**Soluções:**

1. **Processar em partes menores:**
   ```python
   # Dividir o vídeo em partes menores
   parte_size = 30  # 30 segundos por parte
   
   partes = []
   for i in range(0, int(clip.duration), parte_size):
       parte = clip.subclip(i, min(i + parte_size, clip.duration))
       partes.append(parte)
   
   # Processar cada parte individualmente
   for i, parte in enumerate(partes):
       # Processar parte
       parte.write_videofile(f"parte_{i}.mp4", fps=24)
       
       # Liberar memória
       del parte
       import gc
       gc.collect()
   ```

2. **Reduzir resolução:**
   ```python
   # Reduzir resolução para economizar memória
   clip = clip.resize(width=1280)  # Reduzir para 1280px de largura
   ```

3. **Liberar memória manualmente:**
   ```python
   # Liberar memória manualmente
   del clip
   import gc
   gc.collect()
   ```

4. **Usar geradores:**
   ```python
   # Usar geradores para processamento
   def processar_em_partes(clip, parte_size=30):
       for i in range(0, int(clip.duration), parte_size):
           parte = clip.subclip(i, min(i + parte_size, clip.duration))
           yield parte
           del parte
           import gc
           gc.collect()
   
   # Uso
   partes = list(processar_em_partes(clip))
   final = concatenate_videoclips(partes)
   ```

### Problema 26: Vazamento de memória
**Descrição:** O uso de memória aumenta continuamente durante o processamento.

**Causa:** Objetos não são liberados corretamente da memória.

**Soluções:**

1. **Liberar objetos explicitamente:**
   ```python
   # Liberar objetos explicitamente
   def processar_clip(clip):
       # Processar clipe
       resultado = clip.fx(vfx.blackwhite)
       
       # Liberar memória
       del clip
       import gc
       gc.collect()
       
       return resultado
   ```

2. **Usar context managers:**
   ```python
   # Usar context managers para gerenciar recursos
   from contextlib import contextmanager
   
   @contextmanager
   def gerenciar_clip(clip):
       try:
           yield clip
       finally:
           del clip
           import gc
           gc.collect()
   
   # Uso
   with gerenciar_clip(clip) as c:
       resultado = c.fx(vfx.blackwhite)
   ```

3. **Monitorar uso de memória:**
   ```python
   # Monitorar uso de memória
   import psutil
   import os
   
   def get_memory_usage():
       process = psutil.Process(os.getpid())
       return process.memory_info().rss / (1024 * 1024)  # MB
   
   # Uso
   print(f"Uso de memória: {get_memory_usage():.2f} MB")
   # Processar...
   print(f"Uso de memória: {get_memory_usage():.2f} MB")
   ```

## Problemas Específicos da Versão 2.1.2

### Problema 27: Erro com método _add_transitions
**Descrição:** AttributeError: 'VideoFileClip' object has no attribute '_add_transitions'

**Causa:** Na versão 2.1.2, o método _add_transitions foi modificado ou removido.

**Soluções:**

1. **Usar o novo método com efeitos:**
   ```python
   # Antigo (não funciona na 2.1.2)
   clip._add_transitions(fade_in=2, fade_out=2)
   
   # Novo (funciona na 2.1.2)
   from moviepy.video.fx import FadeIn, FadeOut
   clip = clip.with_effects([FadeIn(2), FadeOut(2)])
   ```

2. **Criar função de compatibilidade:**
   ```python
   def add_transitions_compat(clip, fade_in=0, fade_out=0):
       effects = []
       if fade_in > 0:
           effects.append(FadeIn(fade_in))
       if fade_out > 0:
           effects.append(FadeOut(fade_out))
       
       if effects:
           return clip.with_effects(effects)
       else:
           return clip
   
   # Uso
   clip = add_transitions_compat(clip, fade_in=2, fade_out=2)
   ```

### Problema 28: Erro com parâmetro removed_params
**Descrição:** Erros relacionados a parâmetros removidos na versão 2.1.2.

**Causa:** Vários parâmetros foram removidos ou modificados na versão 2.1.2.

**Soluções:**

1. **Verificar a documentação atualizada:**
   ```python
   # Consultar a documentação para métodos atualizados
   help(clip.write_videofile)
   ```

2. **Remover parâmetros obsoletos:**
   ```python
   # Antigo (não funciona na 2.1.2)
   clip.write_videofile("saida.mp4", fps=24, verbose=False, remove_temp=True)
   
   # Novo (funciona na 2.1.2)
   clip.write_videofile("saida.mp4", fps=24)
   ```

3. **Usar parâmetros equivalentes:**
   ```python
   # Em vez de verbose=False, usar logger=None
   clip.write_videofile("saida.mp4", fps=24, logger=None)
   ```

### Problema 29: Erro com método concatenate
**Descrição:** AttributeError: module 'moviepy.editor' has no attribute 'concatenate'

**Causa:** Na versão 2.1.2, o método concatenate foi substituído por concatenate_videoclips.

**Soluções:**

1. **Usar o novo método:**
   ```python
   # Antigo (não funciona na 2.1.2)
   from moviepy.editor import concatenate
   final = concatenate([clip1, clip2])
   
   # Novo (funciona na 2.1.2)
   from moviepy.editor import concatenate_videoclips
   final = concatenate_videoclips([clip1, clip2])
   ```

2. **Criar função de compatibilidade:**
   ```python
   def concatenate_compat(clips):
       return concatenate_videoclips(clips)
   
   # Uso
   final = concatenate_compat([clip1, clip2])
   ```

## Soluções Avançadas

### Problema 30: Processamento paralelo
**Descrição:** Como acelerar o processamento usando múltiplos núcleos.

**Causa:** O processamento de vídeo pode ser acelerado usando processamento paralelo.

**Soluções:**

1. **Usar multiprocessing para processamento paralelo:**
   ```python
   from multiprocessing import Pool
   import os
   
   def processar_parte(args):
       i, parte_path, output_path = args
       
       # Carregar parte
       parte = VideoFileClip(parte_path)
       
       # Processar parte
       parte = parte.fx(vfx.blackwhite)
       
       # Salvar parte processada
       parte_output = f"parte_processada_{i}.mp4"
       parte.write_videofile(parte_output, fps=24, logger=None)
       
       return parte_output
   
   # Dividir vídeo em partes
   partes_paths = ["parte_0.mp4", "parte_1.mp4", "parte_2.mp4"]
   
   # Processar em paralelo
   with Pool(processes=os.cpu_count()) as pool:
       partes_processadas = pool.map(processar_parte, enumerate(partes_paths))
   
   # Juntar partes processadas
   partes_clips = [VideoFileClip(p) for p in partes_processadas]
   final = concatenate_videoclips(partes_clips)
   final.write_videofile("final.mp4", fps=24)
   ```

2. **Usar threading para I/O paralelo:**
   ```python
   import threading
   import queue
   
   def processar_fila(fila_entrada, fila_saida):
       while True:
           item = fila_entrada.get()
           if item is None:  # Sinal de parada
               break
           
           # Processar item
           i, parte_path = item
           parte = VideoFileClip(parte_path)
           parte = parte.fx(vfx.blackwhite)
           
           # Colocar na fila de saída
           fila_saida.put((i, parte))
   
   # Criar filas
   fila_entrada = queue.Queue()
   fila_saida = queue.Queue()
   
   # Criar threads
   threads = []
   for _ in range(4):  # 4 threads
       t = threading.Thread(target=processar_fila, args=(fila_entrada, fila_saida))
       t.start()
       threads.append(t)
   
   # Adicionar itens à fila de entrada
   for i, parte_path in enumerate(["parte_0.mp4", "parte_1.mp4", "parte_2.mp4"]):
       fila_entrada.put((i, parte_path))
   
   # Adicionar sinais de parada
   for _ in range(4):
       fila_entrada.put(None)
   
   # Aguardar threads terminarem
   for t in threads:
       t.join()
   
   # Coletar resultados
   resultados = []
   while not fila_saida.empty():
       resultados.append(fila_saida.get())
   
   # Ordenar por índice
   resultados.sort(key=lambda x: x[0])
   
   # Juntar partes
   partes = [parte for _, parte in resultados]
   final = concatenate_videoclips(partes)
   final.write_videofile("final.mp4", fps=24)
   ```

### Problema 31: Cache de clipes processados
**Descrição:** Como evitar reprocessar os mesmos clipes múltiplas vezes.

**Causa:** O processamento de clipes pode ser otimizado usando cache.

**Soluções:**

1. **Implementar cache simples:**
   ```python
   import hashlib
   import pickle
   import os
   
   def get_clip_hash(clip):
       # Criar hash baseado nas propriedades do clipe
       hash_data = f"{clip.size}_{clip.duration}_{clip.fps}"
       return hashlib.md5(hash_data.encode()).hexdigest()
   
   def processar_com_cache(clip, operacao, cache_dir="cache"):
       # Criar diretório de cache
       os.makedirs(cache_dir, exist_ok=True)
       
       # Gerar hash do clipe
       clip_hash = get_clip_hash(clip)
       cache_file = os.path.join(cache_dir, f"{clip_hash}_{operacao}.pkl")
       
       # Verificar se o resultado está no cache
       if os.path.exists(cache_file):
           with open(cache_file, 'rb') as f:
               return pickle.load(f)
       
       # Processar clipe
       if operacao == "blackwhite":
           resultado = clip.fx(vfx.blackwhite)
       elif operacao == "resize":
           resultado = clip.resize(width=1280)
       else:
           resultado = clip
       
       # Salvar no cache
       with open(cache_file, 'wb') as f:
           pickle.dump(resultado, f)
       
       return resultado
   
   # Uso
   clip = VideoFileClip("video.mp4")
   clip = processar_com_cache(clip, "blackwhite")
   clip = processar_com_cache(clip, "resize")
   ```

2. **Usar decorador de cache:**
   ```python
   import functools
   import hashlib
   import pickle
   import os
   
   def cache_operacao(cache_dir="cache"):
       def decorator(func):
           @functools.wraps(func)
           def wrapper(clip, *args, **kwargs):
               # Criar diretório de cache
               os.makedirs(cache_dir, exist_ok=True)
               
               # Gerar hash baseado no clipe e nos argumentos
               clip_hash = get_clip_hash(clip)
               args_hash = hashlib.md5(str(args + tuple(kwargs.items())).encode()).hexdigest()
               cache_file = os.path.join(cache_dir, f"{clip_hash}_{func.__name__}_{args_hash}.pkl")
               
               # Verificar se o resultado está no cache
               if os.path.exists(cache_file):
                   with open(cache_file, 'rb') as f:
                       return pickle.load(f)
               
               # Processar clipe
               resultado = func(clip, *args, **kwargs)
               
               # Salvar no cache
               with open(cache_file, 'wb') as f:
                   pickle.dump(resultado, f)
               
               return resultado
           return wrapper
       return decorator
   
   # Uso
   @cache_operacao()
   def aplicar_blackwhite(clip):
       return clip.fx(vfx.blackwhite)
   
   @cache_operacao()
   def redimensionar(clip, width):
       return clip.resize(width=width)
   
   # Processar
   clip = VideoFileClip("video.mp4")
   clip = aplicar_blackwhite(clip)
   clip = redimensionar(clip, width=1280)
   ```

## Scripts de Diagnóstico

### Script 1: Verificar instalação do MoviePy
```python
# verificar_instalacao_moviepy.py
import sys
import subprocess
import importlib

def check_module(module_name):
    """Verifica se um módulo está instalado"""
    try:
        importlib.import_module(module_name)
        print(f"✓ {module_name}: INSTALADO")
        return True
    except ImportError:
        print(f"✗ {module_name}: NÃO INSTALADO")
        return False

def check_ffmpeg():
    """Verifica se o FFmpeg está instalado"""
    try:
        result = subprocess.run(["ffmpeg", "-version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            print(f"✓ FFmpeg: INSTALADO ({version})")
            return True
        else:
            print("✗ FFmpeg: NÃO INSTALADO")
            return False
    except FileNotFoundError:
        print("✗ FFmpeg: NÃO INSTALADO")
        return False

def check_imagemagick():
    """Verifica se o Imagemagick está instalado"""
    try:
        result = subprocess.run(["magick", "-version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            print(f"✓ Imagemagick: INSTALADO ({version})")
            return True
        else:
            print("✗ Imagemagick: NÃO INSTALADO")
            return False
    except FileNotFoundError:
        print("✗ Imagemagick: NÃO INSTALADO")
        return False

def main():
    """Função principal"""
    print("=== Verificação da Instalação do MoviePy ===")
    print()
    
    # Verificar Python
    print(f"Python: {sys.version}")
    print()
    
    # Verificar módulos
    print("Módulos Python:")
    check_module("moviepy")
    check_module("numpy")
    check_module("PIL")
    check_module("imageio")
    check_module("imageio_ffmpeg")
    print()
    
    # Verificar dependências externas
    print("Dependências Externas:")
    ffmpeg_ok = check_ffmpeg()
    imagemagick_ok = check_imagemagick()
    print()
    
    # Resumo
    print("=== Resumo ===")
    modules_ok = all([
        check_module("moviepy"),
        check_module("numpy"),
        check_module("PIL"),
        check_module("imageio"),
        check_module("imageio_ffmpeg")
    ])
    
    if modules_ok and ffmpeg_ok and imagemagick_ok:
        print("✓ Tudo está instalado corretamente!")
        return 0
    else:
        print("✗ Alguns componentes estão faltando!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

### Script 2: Testar funcionalidades básicas do MoviePy
```python
# testar_funcionalidades_moviepy.py
import os
import tempfile
import sys
from moviepy.editor import *
from moviepy.video.fx import FadeIn, FadeOut

def test_basic_clip_creation():
    """Testa criação básica de clipes"""
    try:
        # Criar clipe de cor
        clip = ColorClip(size=(320, 240), color=(255, 0, 0), duration=5)
        print("✓ Criação de clipe de cor: SUCESSO")
        return True
    except Exception as e:
        print(f"✗ Criação de clipe de cor: FALHA ({e})")
        return False

def test_text_clip():
    """Testa criação de clipe de texto"""
    try:
        # Criar clipe de texto
        txt = TextClip(
            text="Teste",
            font_size=24,
            color='white',
            font='C:/Windows/Fonts/arial.ttf'
        )
        print("✓ Criação de clipe de texto: SUCESSO")
        return True
    except Exception as e:
        print(f"✗ Criação de clipe de texto: FALHA ({e})")
        return False

def test_effects():
    """Testa efeitos"""
    try:
        # Criar clipe
        clip = ColorClip(size=(320, 240), color=(255, 0, 0), duration=5)
        
        # Aplicar efeitos (MoviePy 2.1.2)
        clip = clip.with_effects([FadeIn(1), FadeOut(1)])
        print("✓ Aplicação de efeitos: SUCESSO")
        return True
    except Exception as e:
        print(f"✗ Aplicação de efeitos: FALHA ({e})")
        return False

def test_composition():
    """Testa composição"""
    try:
        # Criar clipes
        background = ColorClip(size=(320, 240), color=(0, 0, 0), duration=5)
        clip1 = ColorClip(size=(100, 100), color=(255, 0, 0), duration=5)
        clip2 = ColorClip(size=(100, 100), color=(0, 255, 0), duration=5)
        
        # Posicionar clipes
        clip1 = clip1.with_position((50, 50))
        clip2 = clip2.with_position((170, 170))
        
        # Compor
        final = CompositeVideoClip([background, clip1, clip2])
        print("✓ Composição de clipes: SUCESSO")
        return True
    except Exception as e:
        print(f"✗ Composição de clipes: FALHA ({e})")
        return False

def test_concatenation():
    """Testa concatenação"""
    try:
        # Criar clipes
        clip1 = ColorClip(size=(320, 240), color=(255, 0, 0), duration=2)
        clip2 = ColorClip(size=(320, 240), color=(0, 255, 0), duration=3)
        
        # Concatenar (MoviePy 2.1.2)
        final = concatenate_videoclips([clip1, clip2])
        print("✓ Concatenação de clipes: SUCESSO")
        return True
    except Exception as e:
        print(f"✗ Concatenação de clipes: FALHA ({e})")
        return False

def test_export():
    """Testa exportação"""
    try:
        # Criar clipe
        clip = ColorClip(size=(320, 240), color=(255, 0, 0), duration=5)
        
        # Criar arquivo temporário
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as f:
            temp_path = f.name
        
        # Exportar (MoviePy 2.1.2)
        clip.write_videofile(temp_path, fps=24, logger=None)
        
        # Verificar se o arquivo foi criado
        if os.path.exists(temp_path):
            print("✓ Exportação de vídeo: SUCESSO")
            # Remover arquivo temporário
            os.unlink(temp_path)
            return True
        else:
            print("✗ Exportação de vídeo: FALHA (arquivo não criado)")
            return False
    except Exception as e:
        print(f"✗ Exportação de vídeo: FALHA ({e})")
        return False

def main():
    """Função principal"""
    print("=== Teste de Funcionalidades do MoviePy ===")
    print()
    
    # Executar testes
    tests = [
        test_basic_clip_creation,
        test_text_clip,
        test_effects,
        test_composition,
        test_concatenation,
        test_export
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    # Resumo
    print("\n=== Resumo ===")
    passed = sum(results)
    total = len(results)
    
    print(f"Testes passados: {passed}/{total}")
    
    if passed == total:
        print("✓ Todos os testes passaram!")
        return 0
    else:
        print("✗ Alguns testes falharam!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

### Script 3: Testar compatibilidade com MoviePy 2.1.2
```python
# testar_compatibilidade_moviepy_212.py
import sys
import moviepy
from moviepy.editor import *
from moviepy.video.fx import FadeIn, FadeOut

def test_version():
    """Testa a versão do MoviePy"""
    try:
        version = moviepy.__version__
        print(f"Versão do MoviePy: {version}")
        
        # Verificar se é a versão 2.1.2 ou superior
        version_parts = version.split('.')
        major = int(version_parts[0])
        minor = int(version_parts[1])
        
        if major > 2 or (major == 2 and minor >= 1):
            print("✓ Versão compatível com 2.1.2")
            return True
        else:
            print("✗ Versão não compatível com 2.1.2")
            return False
    except Exception as e:
        print(f"✗ Erro ao verificar versão: {e}")
        return False

def test_fade_effects():
    """Testa o novo sistema de efeitos de fade"""
    try:
        # Criar clipe
        clip = ColorClip(size=(320, 240), color=(255, 0, 0), duration=5)
        
        # Testar novo método (MoviePy 2.1.2)
        clip = clip.with_effects([FadeIn(1), FadeOut(1)])
        print("✓ Novo sistema de efeitos de fade: SUCESSO")
        return True
    except Exception as e:
        print(f"✗ Novo sistema de efeitos de fade: FALHA ({e})")
        return False

def test_old_fade_methods():
    """Testa se os métodos antigos de fade ainda funcionam"""
    try:
        # Criar clipe
        clip = ColorClip(size=(320, 240), color=(255, 0, 0), duration=5)
        
        # Tentar usar método antigo
        if hasattr(clip, 'fadein'):
            clip.fadein(1)
            print("✓ Método antigo fadein ainda existe")
        else:
            print("✓ Método antigo fadein foi removido (esperado na 2.1.2)")
        
        if hasattr(clip, 'fadeout'):
            clip.fadeout(1)
            print("✓ Método antigo fadeout ainda existe")
        else:
            print("✓ Método antigo fadeout foi removido (esperado na 2.1.2)")
        
        return True
    except Exception as e:
        print(f"✗ Erro ao testar métodos antigos de fade: {e}")
        return False

def test_write_videofile_params():
    """Testa os parâmetros do método write_videofile"""
    try:
        # Criar clipe
        clip = ColorClip(size=(320, 240), color=(255, 0, 0), duration=5)
        
        # Verificar se o parâmetro verbose ainda existe
        import inspect
        sig = inspect.signature(clip.write_videofile)
        params = list(sig.parameters.keys())
        
        if 'verbose' in params:
            print("✗ Parâmetro verbose ainda existe (deveria ser removido na 2.1.2)")
            return False
        else:
            print("✓ Parâmetro verbose foi removido (esperado na 2.1.2)")
        
        if 'logger' in params:
            print("✓ Parâmetro logger existe (esperado na 2.1.2)")
        else:
            print("✗ Parâmetro logger não existe (deveria existir na 2.1.2)")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Erro ao testar parâmetros do write_videofile: {e}")
        return False

def test_concatenate_method():
    """Testa o método de concatenação"""
    try:
        # Criar clipes
        clip1 = ColorClip(size=(320, 240), color=(255, 0, 0), duration=2)
        clip2 = ColorClip(size=(320, 240), color=(0, 255, 0), duration=3)
        
        # Verificar se o método antigo ainda existe
        if hasattr(sys.modules['moviepy.editor'], 'concatenate'):
            print("✗ Método antigo concatenate ainda existe (deveria ser removido na 2.1.2)")
            return False
        else:
            print("✓ Método antigo concatenate foi removido (esperado na 2.1.2)")
        
        # Testar novo método
        final = concatenate_videoclips([clip1, clip2])
        print("✓ Novo método concatenate_videoclips funciona")
        
        return True
    except Exception as e:
        print(f"✗ Erro ao testar método de concatenação: {e}")
        return False

def test_textclip_api():
    """Testa a API do TextClip"""
    try:
        # Testar criação básica
        txt = TextClip(
            text="Teste",
            font_size=24,
            color='white',
            font='C:/Windows/Fonts/arial.ttf'
        )
        print("✓ Criação básica de TextClip funciona")
        
        # Testar com parâmetros adicionais
        txt = TextClip(
            text="Teste",
            font_size=24,
            color='white',
            font='C:/Windows/Fonts/arial.ttf',
            stroke_color='black',
            stroke_width=1,
            method='label'
        )
        print("✓ TextClip com parâmetros adicionais funciona")
        
        return True
    except Exception as e:
        print(f"✗ Erro ao testar API do TextClip: {e}")
        return False

def main():
    """Função principal"""
    print("=== Teste de Compatibilidade com MoviePy 2.1.2 ===")
    print()
    
    # Executar testes
    tests = [
        test_version,
        test_fade_effects,
        test_old_fade_methods,
        test_write_videofile_params,
        test_concatenate_method,
        test_textclip_api
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    # Resumo
    print("\n=== Resumo ===")
    passed = sum(results)
    total = len(results)
    
    print(f"Testes passados: {passed}/{total}")
    
    if passed == total:
        print("✓ Totalmente compatível com MoviePy 2.1.2!")
        return 0
    else:
        print("✗ Alguns problemas de compatibilidade detectados!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

---

Este documento de soluções de problemas comuns foi projetado para ajudar a resolver rapidamente problemas encontrados ao trabalhar com MoviePy no projeto auto-video-producerV5-dev, especialmente focado na versão 2.1.2.