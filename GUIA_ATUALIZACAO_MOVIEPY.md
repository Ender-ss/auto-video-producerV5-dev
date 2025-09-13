# Guia de Atualização para MoviePy 2.1.2

## Visão Geral
Este documento contém instruções detalhadas para atualizar o código do auto-video-producerV5-dev para funcionar com o MoviePy 2.1.2.

## Pré-requisitos
- Python 3.8+
- MoviePy 2.1.2
- Sistema Windows (para caminhos de fontes)

## Alterações Necessárias

### 1. Método `_add_transitions`
**Arquivo:** `services/video_creation_service.py`

**Problema:** Os métodos `fadein` e `fadeout` foram removidos na versão 2.1.2.

**Solução:**
```python
# Importar no início do arquivo
from moviepy.video.fx import FadeIn, FadeOut

# Substituir no método _add_transitions
# Antes:
clip = clip.fadein(transition_duration)
clip = clip.fadeout(transition_duration)

# Depois:
clip = clip.with_effects([FadeIn(transition_duration)])
clip = clip.with_effects([FadeOut(transition_duration)])
```

### 2. Método `write_videofile`
**Arquivo:** `test_video_creation_fixed.py` e outros arquivos de teste

**Problema:** O parâmetro `verbose` foi removido.

**Solução:**
```python
# Antes:
color_clip.write_videofile(output_path, fps=24, verbose=False)

# Depois:
color_clip.write_videofile(output_path, fps=24)
```

### 3. Método `concatenate`
**Arquivo:** `test_add_transitions.py` e outros arquivos que usam concatenação

**Problema:** O método `concatenate` foi removido.

**Solução:**
```python
# Importar no início do arquivo
from moviepy.editor import concatenate_videoclips

# Substituir no código
# Antes:
final_clip = clips_with_transitions[0]
for clip in clips_with_transitions[1:]:
    final_clip = final_clip.concatenate(clip)

# Depois:
final_clip = concatenate_videoclips(clips_with_transitions)
```

### 4. TextClip
**Arquivo:** `services/video_creation_service.py`

**Problema:** A API do TextClip mudou significativamente.

**Solução:**
```python
# Antes:
txt_clip = TextClip(
    segment['text'],
    fontsize=24,
    color='white',
    stroke_color='black',
    stroke_width=2,
    font='Arial-Bold'
).set_position(('center', 'bottom')).set_start(segment['start']).set_duration(segment['duration'])

# Depois:
txt_clip = TextClip(
    text=segment['text'],
    font_size=24,
    color='white',
    stroke_color='black',
    stroke_width=2,
    font='C:/Windows/Fonts/arial.ttf'
)
txt_clip = txt_clip.with_position(('center', 'bottom')).with_start(segment['start']).with_duration(segment['duration'])
```

## Testes

Execute os seguintes testes para verificar se as alterações estão funcionando:

1. **Teste básico de criação de vídeo:**
   ```bash
   python test_video_creation_fixed.py
   ```

2. **Teste de transições:**
   ```bash
   python test_add_transitions.py
   ```

3. **Teste completo do fluxo:**
   ```bash
   python test_complete_video_creation.py
   ```

## Inicialização do Sistema

Para iniciar o sistema completo:

1. **Iniciar o backend:**
   ```bash
   cd backend
   python app.py
   ```

2. **Iniciar o frontend (em outro terminal):**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Acessar o sistema:**
   - Backend: /api
   - Frontend: http://localhost:5173

## Solução de Problemas

### Fontes não encontradas
Se ocorrerem erros de fontes, verifique o caminho completo para as fontes do sistema:
- Windows: `C:/Windows/Fonts/arial.ttf`
- Linux: `/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf`
- macOS: `/System/Library/Fonts/Arial.ttf`

### Métodos não encontrados
Se ocorrerem erros de métodos não encontrados, verifique se:
1. Todos os métodos diretos foram substituídos por versões com `with_effects`
2. Todos os métodos de posicionamento usam o prefixo `with_`
3. Todos os parâmetros obsoletos foram removidos

## Conclusão

Seguindo estas instruções, o sistema será totalmente compatível com o MoviePy 2.1.2. As principais mudanças envolvem:
- Uso de efeitos com `with_effects()`
- Atualização da API do TextClip
- Substituição de métodos de posicionamento
- Remoção de parâmetros obsoletos

Mantenha este documento como referência para futuras atualizações do MoviePy.