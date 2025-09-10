# 🔧 Processos Detalhados da Pipeline - Auto Video Producer

## 📋 Índice

1. [Processo de Extração](#1-processo-de-extração)
2. [Processo de Geração de Títulos](#2-processo-de-geração-de-títulos)
3. [Processo de Geração de Premissa](#3-processo-de-geração-de-premissa)
4. [Processo de Geração de Roteiro](#4-processo-de-geração-de-roteiro)
5. [Processo de Geração de Áudio (TTS)](#5-processo-de-geração-de-áudio-tts)
6. [Processo de Geração de Imagens](#6-processo-de-geração-de-imagens)
7. [Processo de Criação de Vídeo](#7-processo-de-criação-de-vídeo)
8. [Processo de Orquestração](#8-processo-de-orquestração)

---

## 1. 📺 Processo de Extração

### Localização
- **Arquivo**: `backend/routes/automations.py`
- **Função**: `extract_youtube_data()`
- **Endpoint**: `POST /api/extract-youtube`

### Dependências Técnicas
```python
import yt_dlp
import requests
import json
import re
from urllib.parse import urlparse
```

### Fluxo Detalhado

#### Etapa 1: Validação da URL
```python
def validate_youtube_url(url):
    patterns = [
        r'youtube\.com/channel/([a-zA-Z0-9_-]+)',
        r'youtube\.com/c/([a-zA-Z0-9_-]+)',
        r'youtube\.com/@([a-zA-Z0-9_-]+)',
        r'youtube\.com/user/([a-zA-Z0-9_-]+)'
    ]
    # Valida formato e extrai ID do canal
```

#### Etapa 2: Configuração do yt-dlp
```python
ydl_opts = {
    'quiet': True,
    'no_warnings': True,
    'extract_flat': True,
    'playlist_items': '1:50',  # Limita a 50 vídeos
    'ignoreerrors': True
}
```

#### Etapa 3: Extração de Metadados
```python
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(channel_url, download=False)
    
    # Extrai informações do canal
    channel_info = {
        'name': info.get('uploader', ''),
        'id': info.get('channel_id', ''),
        'subscriber_count': info.get('subscriber_count', 0),
        'video_count': info.get('playlist_count', 0)
    }
    
    # Extrai títulos dos vídeos
    video_titles = []
    for entry in info.get('entries', []):
        if entry and entry.get('title'):
            video_titles.append({
                'title': entry['title'],
                'view_count': entry.get('view_count', 0),
                'upload_date': entry.get('upload_date', ''),
                'duration': entry.get('duration', 0)
            })
```

#### Etapa 4: Análise de Padrões
```python
def analyze_viral_patterns(titles):
    patterns = {
        'emotional_triggers': [],
        'numbers': [],
        'power_words': [],
        'length_stats': {}
    }
    
    for title in titles:
        # Detecta gatilhos emocionais
        emotional_words = ['incrível', 'chocante', 'segredo', 'revelado']
        
        # Detecta números
        numbers = re.findall(r'\d+', title)
        
        # Calcula estatísticas de comprimento
        # ...
    
    return patterns
```

### Estrutura de Retorno
```json
{
    "success": true,
    "data": {
        "channel_info": {
            "name": "Nome do Canal",
            "id": "UCxxxxx",
            "subscriber_count": 100000,
            "video_count": 250
        },
        "video_titles": [
            {
                "title": "Título do Vídeo",
                "view_count": 50000,
                "upload_date": "20240115",
                "duration": 600
            }
        ],
        "viral_patterns": {
            "emotional_triggers": ["incrível", "segredo"],
            "numbers": ["10", "2024"],
            "power_words": ["como", "melhor"],
            "length_stats": {
                "avg_length": 45,
                "min_length": 20,
                "max_length": 80
            }
        }
    }
}
```

### Tratamento de Erros
- **URL inválida**: Retorna erro 400 com mensagem específica
- **Canal não encontrado**: Retorna erro 404
- **Rate limiting**: Implementa retry com backoff exponencial
- **Timeout**: Configura timeout de 30 segundos

---

## 2. 🎯 Processo de Geração de Títulos

### Localização
- **Arquivo**: `backend/services/title_generator.py`
- **Classe**: `TitleGenerator`
- **Endpoint**: `POST /api/generate-titles`

### Provedores Suportados

#### OpenAI
```python
def configure_openai(self, api_key):
    from openai import OpenAI
    self.openai_client = OpenAI(api_key=api_key)
    
    # Teste de conexão
    models = self.openai_client.models.list()
```

#### Google Gemini
```python
def configure_gemini(self, api_key):
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
```

#### OpenRouter
```python
def configure_openrouter(self, api_key):
    self.openrouter_api_key = api_key
    # Suporta múltiplos modelos: Claude, Llama, etc.
```

### Análise de Padrões Virais

```python
def analyze_viral_patterns(self, titles):
    patterns = {
        'emotional_triggers': [],
        'numbers': [],
        'power_words': [],
        'structures': [],
        'length_stats': {}
    }
    
    # Gatilhos emocionais
    emotional_words = [
        'incrível', 'chocante', 'segredo', 'revelado',
        'nunca', 'sempre', 'todos', 'ninguém',
        'melhor', 'pior', 'único', 'especial'
    ]
    
    # Palavras de poder
    power_words = [
        'como', 'por que', 'quando', 'onde',
        'dicas', 'truques', 'hacks', 'segredos',
        'método', 'técnica', 'estratégia'
    ]
    
    # Estruturas comuns
    structures = [
        r'^\d+\s+\w+',  # "10 Dicas"
        r'Como\s+\w+',  # "Como Fazer"
        r'Por que\s+\w+',  # "Por que Você"
        r'O que\s+\w+'   # "O que Acontece"
    ]
    
    for title in titles:
        # Análise de cada padrão
        # ...
    
    return patterns
```

### Geração de Prompts

#### Prompt para OpenAI
```python
def create_openai_prompt(self, source_titles, topic, patterns, style, count):
    prompt = f"""
    Você é um especialista em criação de títulos virais para YouTube.
    
    TÍTULOS DE REFERÊNCIA:
    {chr(10).join(source_titles[:10])}
    
    PADRÕES IDENTIFICADOS:
    - Gatilhos emocionais: {', '.join(patterns['emotional_triggers'][:5])}
    - Palavras de poder: {', '.join(patterns['power_words'][:5])}
    - Comprimento médio: {patterns['length_stats'].get('avg', 50)} caracteres
    
    TÓPICO: {topic}
    ESTILO: {style}
    
    Crie {count} títulos únicos e virais seguindo os padrões identificados.
    
    REGRAS:
    1. Use gatilhos emocionais
    2. Inclua números quando apropriado
    3. Mantenha entre 40-60 caracteres
    4. Seja específico e intrigante
    5. Evite clickbait enganoso
    
    FORMATO: Liste apenas os títulos, um por linha.
    """
    return prompt
```

#### Prompt para Gemini
```python
def create_gemini_prompt(self, source_titles, topic, patterns, style, count):
    prompt = f"""
    ## Contexto
    Você é um especialista em marketing digital e criação de conteúdo viral.
    
    ## Dados de Entrada
    **Títulos de Referência:**
    {chr(10).join([f"- {title}" for title in source_titles[:10]])}
    
    **Padrões Virais Identificados:**
    - Gatilhos emocionais mais usados: {', '.join(patterns['emotional_triggers'][:5])}
    - Palavras de poder: {', '.join(patterns['power_words'][:5])}
    - Estruturas comuns: {', '.join(patterns['structures'][:3])}
    
    ## Tarefa
    Crie {count} títulos únicos para o tópico: "{topic}"
    Estilo desejado: {style}
    
    ## Diretrizes
    1. **Emoção**: Use gatilhos emocionais identificados
    2. **Clareza**: Seja específico sobre o benefício
    3. **Urgência**: Crie senso de urgência quando apropriado
    4. **Curiosidade**: Desperte curiosidade sem ser clickbait
    5. **Comprimento**: Entre 40-60 caracteres idealmente
    
    ## Formato de Saída
    Retorne apenas os títulos, um por linha, sem numeração.
    """
    return prompt
```

### Processamento de Respostas

```python
def parse_generated_titles(self, content):
    # Remove numeração e formatação
    lines = content.strip().split('\n')
    titles = []
    
    for line in lines:
        # Remove numeração (1., 2., etc.)
        clean_line = re.sub(r'^\d+\.?\s*', '', line.strip())
        # Remove aspas
        clean_line = clean_line.strip('"\'')
        # Remove marcadores
        clean_line = re.sub(r'^[-*]\s*', '', clean_line)
        
        if clean_line and len(clean_line) > 10:
            titles.append(clean_line)
    
    return titles
```

### Sistema de Pontuação

```python
def score_title_quality(self, title, patterns):
    score = 0
    
    # Comprimento ideal (40-60 caracteres)
    length = len(title)
    if 40 <= length <= 60:
        score += 20
    elif 30 <= length <= 70:
        score += 10
    
    # Presença de gatilhos emocionais
    for trigger in patterns['emotional_triggers']:
        if trigger.lower() in title.lower():
            score += 15
            break
    
    # Presença de números
    if re.search(r'\d+', title):
        score += 10
    
    # Palavras de poder
    for word in patterns['power_words']:
        if word.lower() in title.lower():
            score += 10
            break
    
    # Estruturas virais
    for structure in patterns['structures']:
        if re.search(structure, title, re.IGNORECASE):
            score += 15
            break
    
    # Penalidades
    if len(title) > 80:  # Muito longo
        score -= 20
    if len(title) < 20:  # Muito curto
        score -= 15
    
    return min(100, max(0, score))
```

---

## 3. 💡 Processo de Geração de Premissa

### Localização
- **Arquivo**: `backend/routes/automations.py`
- **Função**: `generate_premise()`
- **Endpoint**: `POST /api/generate-premise`

### Fluxo de Geração

```python
def generate_premise():
    data = request.get_json()
    title = data.get('title')
    channel_context = data.get('channel_context', {})
    ai_provider = data.get('ai_provider', 'gemini')
    
    # Construir contexto
    context = build_premise_context(title, channel_context)
    
    # Gerar prompt
    prompt = create_premise_prompt(title, context)
    
    # Chamar IA
    premise = call_ai_for_premise(prompt, ai_provider)
    
    # Validar e formatar
    formatted_premise = format_premise(premise)
    
    return formatted_premise
```

### Construção de Contexto

```python
def build_premise_context(title, channel_context):
    context = {
        'channel_name': channel_context.get('name', ''),
        'channel_niche': analyze_channel_niche(channel_context),
        'target_audience': infer_target_audience(channel_context),
        'content_style': analyze_content_style(channel_context)
    }
    
    # Análise do título
    title_analysis = {
        'main_topic': extract_main_topic(title),
        'emotional_hook': identify_emotional_hook(title),
        'target_benefit': identify_target_benefit(title)
    }
    
    context['title_analysis'] = title_analysis
    return context
```

### Template de Prompt

```python
def create_premise_prompt(title, context):
    prompt = f"""
    ## Contexto do Canal
    - Nome: {context['channel_name']}
    - Nicho: {context['channel_niche']}
    - Público-alvo: {context['target_audience']}
    - Estilo: {context['content_style']}
    
    ## Título do Vídeo
    "{title}"
    
    ## Análise do Título
    - Tópico principal: {context['title_analysis']['main_topic']}
    - Gancho emocional: {context['title_analysis']['emotional_hook']}
    - Benefício prometido: {context['title_analysis']['target_benefit']}
    
    ## Tarefa
    Crie uma premissa envolvente para este vídeo que:
    
    1. **Estabeleça o problema/oportunidade** que o vídeo vai abordar
    2. **Prometa uma solução específica** alinhada com o título
    3. **Crie curiosidade** sobre como a solução será revelada
    4. **Seja relevante** para o público-alvo do canal
    5. **Mantenha coerência** com o estilo do canal
    
    ## Estrutura Desejada
    - **Hook inicial**: Frase que captura atenção imediatamente
    - **Problema/Oportunidade**: O que será abordado
    - **Promessa**: O que o espectador vai aprender/ganhar
    - **Curiosidade**: Como isso será revelado no vídeo
    
    ## Formato
    Retorne apenas a premissa, sem explicações adicionais.
    Máximo 200 palavras.
    """
    return prompt
```

### Validação da Premissa

```python
def validate_premise(premise, title):
    validation = {
        'length_ok': 50 <= len(premise) <= 1000,
        'has_hook': check_for_hook(premise),
        'aligns_with_title': check_title_alignment(premise, title),
        'has_promise': check_for_promise(premise),
        'creates_curiosity': check_for_curiosity(premise)
    }
    
    validation['score'] = sum(validation.values()) / len(validation) * 100
    return validation
```

---

## 4. 📝 Processo de Geração de Roteiro

### Localização
- **Arquivo**: `backend/services/storyteller_service.py`
- **Classe**: `StorytellerService`
- **Endpoint**: `POST /api/generate-script`

### Pipeline de 3 Prompts

#### Prompt 1: Estrutura Inicial
```python
def execute_prompt_1(self, title, premise, agent_type, target_chars):
    prompt = f"""
    ## Contexto
    Você é um {self.agent_configs[agent_type]['description']}
    
    ## Informações do Vídeo
    **Título:** {title}
    **Premissa:** {premise}
    **Duração alvo:** {target_chars} caracteres
    
    ## Tarefa - Prompt 1: Estrutura Inicial
    Crie a estrutura base do roteiro com:
    
    1. **Abertura impactante** (10% do conteúdo)
       - Hook que prende atenção nos primeiros 15 segundos
       - Apresentação clara do que será abordado
    
    2. **Desenvolvimento principal** (70% do conteúdo)
       - Divisão em 3-5 pontos principais
       - Cada ponto com explicação e exemplo
       - Transições suaves entre pontos
    
    3. **Fechamento forte** (20% do conteúdo)
       - Resumo dos pontos principais
       - Call-to-action claro
       - Gancho para próximo vídeo (se aplicável)
    
    ## Diretrizes
    - Use linguagem {self.agent_configs[agent_type]['tone']}
    - Mantenha {self.agent_configs[agent_type]['style']}
    - Inclua momentos de interação com o público
    - Evite repetições desnecessárias
    
    ## Formato
    Retorne o roteiro estruturado com marcações de seção.
    """
    
    return self._call_llm_api(prompt, self._get_next_gemini_key(), 'gemini')
```

#### Prompt 2: Desenvolvimento e Detalhamento
```python
def execute_prompt_2(self, prompt_1_result, title, premise, agent_type):
    prompt = f"""
    ## Roteiro Base (Prompt 1)
    {prompt_1_result}
    
    ## Tarefa - Prompt 2: Desenvolvimento e Detalhamento
    Expanda o roteiro base adicionando:
    
    1. **Detalhamento de cada seção**
       - Adicione exemplos específicos
       - Inclua dados e estatísticas relevantes
       - Desenvolva analogias e metáforas
    
    2. **Elementos de engajamento**
       - Perguntas retóricas estratégicas
       - Momentos de pausa para reflexão
       - Chamadas para interação
    
    3. **Narrativa fluida**
       - Conectores entre ideias
       - Variação no ritmo da narração
       - Momentos de tensão e alívio
    
    4. **Personalização**
       - Histórias pessoais ou casos reais
       - Referências culturais apropriadas
       - Linguagem do público-alvo
    
    ## Foco Especial
    - Mantenha coerência com o título: "{title}"
    - Cumpra a promessa da premissa: "{premise}"
    - Use o estilo {agent_type}
    
    ## Formato
    Retorne o roteiro expandido mantendo a estrutura original.
    """
    
    return self._call_llm_api(prompt, self._get_next_gemini_key(), 'gemini')
```

#### Prompt 3: Refinamento e Polimento
```python
def execute_prompt_3(self, prompt_2_result, title, premise, agent_type):
    prompt = f"""
    ## Roteiro Desenvolvido (Prompt 2)
    {prompt_2_result}
    
    ## Tarefa - Prompt 3: Refinamento e Polimento
    Finalize o roteiro com foco em:
    
    1. **Otimização da linguagem**
       - Simplifique frases complexas
       - Elimine redundâncias
       - Melhore a fluidez da narração
    
    2. **Timing e ritmo**
       - Ajuste pausas estratégicas
       - Varie o ritmo conforme o conteúdo
       - Otimize para retenção de audiência
    
    3. **Impacto emocional**
       - Intensifique momentos-chave
       - Adicione elementos de surpresa
       - Reforce o valor entregue
    
    4. **Chamadas para ação**
       - Posicione CTAs estrategicamente
       - Torne-as naturais e persuasivas
       - Varie o tipo de interação solicitada
    
    5. **Verificação final**
       - Confirme alinhamento com título
       - Valide cumprimento da premissa
       - Assegure qualidade do conteúdo
    
    ## Resultado Final
    Entregue um roteiro polido, envolvente e pronto para produção.
    """
    
    return self._call_llm_api(prompt, self._get_next_gemini_key(), 'gemini')
```

### Detecção de Repetições

```python
class RepetitionDetector:
    def __init__(self):
        self.similarity_threshold = 0.7
        self.phrase_min_length = 10
    
    def detect_repetitions(self, chapters):
        repetitions = []
        
        # Detecta capítulos similares
        for i, chapter1 in enumerate(chapters):
            for j, chapter2 in enumerate(chapters[i+1:], i+1):
                similarity = self._calculate_similarity(chapter1, chapter2)
                if similarity > self.similarity_threshold:
                    repetitions.append({
                        'chapter1': i+1,
                        'chapter2': j+1,
                        'similarity': similarity
                    })
        
        # Detecta frases repetidas
        repeated_phrases = self._find_repeated_phrases(chapters)
        
        return {
            'similar_chapters': repetitions,
            'repeated_phrases': repeated_phrases,
            'repetition_score': len(repetitions) + len(repeated_phrases)
        }
    
    def _calculate_similarity(self, text1, text2):
        from difflib import SequenceMatcher
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
    
    def _find_repeated_phrases(self, chapters):
        phrases = []
        all_sentences = []
        
        # Extrai sentenças
        for i, chapter in enumerate(chapters):
            sentences = re.split(r'[.!?]+', chapter)
            for sentence in sentences:
                sentence = sentence.strip()
                if len(sentence) >= self.phrase_min_length:
                    all_sentences.append({
                        'text': sentence.lower(),
                        'chapter': i+1,
                        'original': sentence
                    })
        
        # Encontra duplicatas
        seen = {}
        for sentence in all_sentences:
            text = sentence['text']
            if text in seen:
                phrases.append({
                    'phrase': sentence['original'],
                    'chapters': [seen[text]['chapter'], sentence['chapter']]
                })
            else:
                seen[text] = sentence
        
        return phrases
```

### Quebra Inteligente de Capítulos

```python
class SmartChapterBreaker:
    def __init__(self):
        self.break_indicators = [
            r'\.\s*\n+',  # Fim de parágrafo
            r'\n\s*\n',   # Linha em branco
            r'[.!?]\s+[A-Z]',  # Fim de frase + nova frase
            r'\b(Agora|Então|Portanto|Além disso|Por outro lado)\b',
            r'\b(Primeiro|Segundo|Terceiro|Finalmente)\b',
            r'\b(Vamos|Agora vamos|Próximo)\b'
        ]
    
    def find_natural_breaks(self, text, target_length):
        # Encontra pontos naturais de quebra
        break_points = []
        
        for pattern in self.break_indicators:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                break_points.append(match.start())
        
        # Ordena e remove duplicatas
        break_points = sorted(set(break_points))
        
        # Seleciona pontos próximos ao comprimento alvo
        optimal_breaks = []
        current_pos = 0
        
        for target_pos in range(target_length, len(text), target_length):
            # Encontra o ponto de quebra mais próximo
            best_break = min(break_points, 
                           key=lambda x: abs(x - target_pos) if x > current_pos else float('inf'))
            
            if best_break > current_pos:
                optimal_breaks.append(best_break)
                current_pos = best_break
        
        return optimal_breaks
```

### Validação de Qualidade

```python
class StoryValidator:
    def __init__(self, config):
        self.config = config
        self.repetition_detector = RepetitionDetector()
    
    def validate_chapter(self, chapter, chapter_num):
        validation = {
            'length_ok': self._check_length(chapter),
            'has_hook': self._check_hook(chapter, chapter_num),
            'has_content': self._check_content_quality(chapter),
            'has_transition': self._check_transitions(chapter),
            'language_quality': self._check_language(chapter)
        }
        
        validation['score'] = sum(validation.values()) / len(validation) * 100
        return validation
    
    def _check_length(self, chapter):
        min_chars = self.config.get('min_chars', 500)
        max_chars = self.config.get('max_chars', 2000)
        return min_chars <= len(chapter) <= max_chars
    
    def _check_hook(self, chapter, chapter_num):
        if chapter_num == 1:  # Primeiro capítulo deve ter hook forte
            hook_patterns = [
                r'^(Você já|Imagine|E se|Sabia que)',
                r'\?',  # Pergunta
                r'(incrível|surpreendente|chocante)'
            ]
            return any(re.search(pattern, chapter[:200], re.IGNORECASE) 
                      for pattern in hook_patterns)
        return True
    
    def _check_content_quality(self, chapter):
        # Verifica se tem conteúdo substantivo
        sentences = re.split(r'[.!?]+', chapter)
        substantial_sentences = [s for s in sentences if len(s.strip()) > 20]
        return len(substantial_sentences) >= 3
    
    def _check_transitions(self, chapter):
        transition_words = [
            'além disso', 'portanto', 'então', 'agora',
            'por outro lado', 'em seguida', 'finalmente'
        ]
        return any(word in chapter.lower() for word in transition_words)
    
    def _check_language(self, chapter):
        # Verifica qualidade básica da linguagem
        issues = 0
        
        # Frases muito longas
        sentences = re.split(r'[.!?]+', chapter)
        long_sentences = [s for s in sentences if len(s.split()) > 30]
        if len(long_sentences) > len(sentences) * 0.3:
            issues += 1
        
        # Repetições de palavras
        words = re.findall(r'\b\w+\b', chapter.lower())
        word_freq = {}
        for word in words:
            if len(word) > 4:  # Ignora palavras muito curtas
                word_freq[word] = word_freq.get(word, 0) + 1
        
        repeated_words = [w for w, freq in word_freq.items() if freq > 5]
        if len(repeated_words) > 3:
            issues += 1
        
        return issues == 0
```

---

## 5. 🎵 Processo de Geração de Áudio (TTS)

### Localização
- **Arquivo**: `backend/services/tts_service.py`
- **Classe**: `TTSService`
- **Endpoint**: `POST /api/generate-tts`

### Provedores Suportados

#### Google Gemini TTS
```python
def generate_tts_with_gemini(text, voice_settings):
    import google.generativeai as genai
    
    # Configuração do modelo
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Parâmetros de voz
    voice_config = {
        'voice_name': voice_settings.get('voice_id', 'pt-BR-Standard-A'),
        'language_code': 'pt-BR',
        'speaking_rate': voice_settings.get('speed', 1.0),
        'pitch': voice_settings.get('pitch', 0.0),
        'volume_gain_db': voice_settings.get('volume', 0.0)
    }
    
    # Gerar áudio
    response = model.generate_content(
        text,
        generation_config={
            'audio_config': voice_config
        }
    )
    
    return response.audio_data
```

#### ElevenLabs
```python
def generate_tts_with_elevenlabs(text, voice_settings):
    import requests
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_settings['voice_id']}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": voice_settings['api_key']
    }
    
    data = {
        "text": text,
        "model_id": voice_settings.get('model_id', 'eleven_monolingual_v1'),
        "voice_settings": {
            "stability": voice_settings.get('stability', 0.5),
            "similarity_boost": voice_settings.get('clarity', 0.75),
            "style": voice_settings.get('style', 0.0),
            "use_speaker_boost": voice_settings.get('speaker_boost', True)
        }
    }
    
    response = requests.post(url, json=data, headers=headers)
    return response.content
```

#### Kokoro TTS
```python
def generate_tts_with_kokoro(text, voice_settings):
    import requests
    
    # Kokoro é um modelo local/open-source
    url = voice_settings.get('kokoro_url', 'http://localhost:8080/tts')
    
    data = {
        'text': text,
        'voice': voice_settings.get('voice_id', 'kokoro'),
        'speed': voice_settings.get('speed', 1.0),
        'pitch': voice_settings.get('pitch', 0.0)
    }
    
    response = requests.post(url, json=data)
    return response.content
```

### Segmentação Inteligente

```python
def _segment_text(self, text, max_chars_per_segment):
    # Divide texto em segmentos respeitando limites naturais
    segments = []
    current_segment = ""
    
    # Divide por sentenças primeiro
    sentences = re.split(r'[.!?]+', text)
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
            
        # Se adicionar esta sentença ultrapassar o limite
        if len(current_segment + sentence) > max_chars_per_segment:
            if current_segment:  # Se já tem conteúdo, salva o segmento
                segments.append(current_segment.strip())
                current_segment = sentence
            else:  # Sentença muito longa, divide por palavras
                words = sentence.split()
                for word in words:
                    if len(current_segment + " " + word) > max_chars_per_segment:
                        if current_segment:
                            segments.append(current_segment.strip())
                            current_segment = word
                        else:
                            # Palavra muito longa, força divisão
                            segments.append(word)
                    else:
                        current_segment += " " + word if current_segment else word
        else:
            current_segment += ". " + sentence if current_segment else sentence
    
    # Adiciona último segmento
    if current_segment:
        segments.append(current_segment.strip())
    
    return segments
```

### Sincronização e Timing

```python
def _calculate_timing(self, text_segments, audio_files):
    timing_data = []
    cumulative_time = 0
    
    for i, (text, audio_file) in enumerate(zip(text_segments, audio_files)):
        # Calcula duração do áudio
        duration = self._get_audio_duration(audio_file)
        
        # Calcula palavras por segundo
        word_count = len(text.split())
        wps = word_count / duration if duration > 0 else 0
        
        timing_data.append({
            'segment_index': i,
            'text': text,
            'audio_file': audio_file,
            'start_time': cumulative_time,
            'end_time': cumulative_time + duration,
            'duration': duration,
            'word_count': word_count,
            'words_per_second': wps
        })
        
        cumulative_time += duration
    
    return timing_data

def _get_audio_duration(self, audio_file):
    try:
        from moviepy.editor import AudioFileClip
        with AudioFileClip(audio_file) as audio:
            return audio.duration
    except Exception as e:
        # Fallback usando ffprobe
        import subprocess
        result = subprocess.run([
            'ffprobe', '-v', 'quiet', '-show_entries',
            'format=duration', '-of', 'csv=p=0', audio_file
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            return float(result.stdout.strip())
        return 0
```

### Combinação de Segmentos

```python
def _combine_audio_segments(self, audio_files, output_path):
    try:
        from moviepy.editor import AudioFileClip, concatenate_audioclips
        
        # Carrega todos os clipes de áudio
        audio_clips = []
        for audio_file in audio_files:
            if os.path.exists(audio_file):
                clip = AudioFileClip(audio_file)
                audio_clips.append(clip)
        
        if not audio_clips:
            raise Exception("Nenhum arquivo de áudio válido encontrado")
        
        # Concatena todos os clipes
        final_audio = concatenate_audioclips(audio_clips)
        
        # Salva o áudio final
        final_audio.write_audiofile(output_path, verbose=False, logger=None)
        
        # Limpa recursos
        for clip in audio_clips:
            clip.close()
        final_audio.close()
        
        return output_path
        
    except Exception as e:
        # Fallback usando ffmpeg
        return self._combine_with_ffmpeg(audio_files, output_path)

def _combine_with_ffmpeg(self, audio_files, output_path):
    import subprocess
    
    # Cria lista de arquivos para ffmpeg
    file_list_path = output_path + '.txt'
    with open(file_list_path, 'w') as f:
        for audio_file in audio_files:
            if os.path.exists(audio_file):
                f.write(f"file '{audio_file}'\n")
    
    # Executa ffmpeg
    cmd = [
        'ffmpeg', '-f', 'concat', '-safe', '0',
        '-i', file_list_path, '-c', 'copy', output_path, '-y'
    ]
    
    result = subprocess.run(cmd, capture_output=True)
    
    # Remove arquivo temporário
    os.remove(file_list_path)
    
    if result.returncode == 0:
        return output_path
    else:
        raise Exception(f"Erro no ffmpeg: {result.stderr.decode()}")
```

---

## 6. 🎨 Processo de Geração de Imagens

### Localização
- **Arquivo**: `backend/routes/images.py`
- **Blueprint**: `images_bp`
- **Endpoint**: `POST /api/images/generate`

### Provedores Suportados

#### Together AI
```python
def generate_image_together(prompt, model, style_settings):
    import requests
    
    url = "https://api.together.xyz/v1/images/generations"
    
    headers = {
        "Authorization": f"Bearer {style_settings['api_key']}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,  # ex: "black-forest-labs/FLUX.1-schnell"
        "prompt": prompt,
        "width": style_settings.get('width', 1024),
        "height": style_settings.get('height', 1024),
        "steps": style_settings.get('steps', 20),
        "n": 1,
        "response_format": "b64_json"
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        result = response.json()
        return result['data'][0]['b64_json']
    else:
        raise Exception(f"Erro Together AI: {response.text}")
```

#### Google Gemini (Imagen)
```python
def generate_image_gemini(prompt, style_settings):
    import google.generativeai as genai
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Gemini usa prompt textual para gerar imagem
    image_prompt = f"""
    Gere uma imagem baseada na seguinte descrição:
    {prompt}
    
    Estilo: {style_settings.get('style', 'realistic')}
    Qualidade: {style_settings.get('quality', 'high')}
    Formato: {style_settings.get('format', 'landscape')}
    """
    
    response = model.generate_content(
        image_prompt,
        generation_config={
            'image_config': {
                'width': style_settings.get('width', 1024),
                'height': style_settings.get('height', 1024)
            }
        }
    )
    
    return response.image_data
```

#### Pollinations (Gratuito)
```python
def generate_image_pollinations(prompt, style_settings):
    import requests
    from urllib.parse import quote
    
    # Pollinations usa URL simples
    encoded_prompt = quote(prompt)
    width = style_settings.get('width', 1024)
    height = style_settings.get('height', 1024)
    
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Erro Pollinations: {response.status_code}")
```

### Análise de Roteiro para Cenas

```python
def analyze_script_for_scenes(script_text):
    # Identifica cenas baseadas em estrutura do roteiro
    scenes = []
    
    # Divide por parágrafos ou seções
    paragraphs = script_text.split('\n\n')
    
    for i, paragraph in enumerate(paragraphs):
        if len(paragraph.strip()) < 50:  # Muito curto, pula
            continue
            
        # Extrai conceitos visuais
        visual_concepts = extract_visual_concepts(paragraph)
        
        # Identifica momento narrativo
        narrative_moment = identify_narrative_moment(paragraph, i, len(paragraphs))
        
        scene = {
            'index': i,
            'text': paragraph,
            'visual_concepts': visual_concepts,
            'narrative_moment': narrative_moment,
            'duration_estimate': estimate_duration(paragraph)
        }
        
        scenes.append(scene)
    
    return scenes

def extract_visual_concepts(text):
    # Identifica elementos visuais mencionados
    visual_keywords = {
        'pessoas': ['pessoa', 'homem', 'mulher', 'criança', 'jovem', 'adulto'],
        'objetos': ['computador', 'celular', 'livro', 'carro', 'casa'],
        'lugares': ['escritório', 'casa', 'rua', 'parque', 'praia'],
        'ações': ['trabalhando', 'estudando', 'correndo', 'sorrindo'],
        'emoções': ['feliz', 'triste', 'surpreso', 'concentrado']
    }
    
    concepts = []
    text_lower = text.lower()
    
    for category, keywords in visual_keywords.items():
        found_keywords = [kw for kw in keywords if kw in text_lower]
        if found_keywords:
            concepts.append({
                'category': category,
                'keywords': found_keywords
            })
    
    return concepts

def identify_narrative_moment(text, index, total):
    # Identifica o tipo de momento narrativo
    if index == 0:
        return 'opening'  # Abertura
    elif index == total - 1:
        return 'closing'  # Fechamento
    elif index < total * 0.3:
        return 'introduction'  # Introdução
    elif index > total * 0.7:
        return 'conclusion'  # Conclusão
    else:
        return 'development'  # Desenvolvimento
```

### Geração de Prompts Visuais

```python
def generate_scene_prompts_with_ai(scenes, script_context):
    prompts = []
    
    for scene in scenes:
        # Prompt para IA gerar descrição visual
        ai_prompt = f"""
        ## Contexto do Vídeo
        Tópico: {script_context.get('topic', '')}
        Estilo: {script_context.get('style', 'educational')}
        Público: {script_context.get('audience', 'geral')}
        
        ## Texto da Cena
        "{scene['text'][:200]}..."
        
        ## Conceitos Visuais Identificados
        {json.dumps(scene['visual_concepts'], indent=2)}
        
        ## Momento Narrativo
        {scene['narrative_moment']}
        
        ## Tarefa
        Crie uma descrição visual detalhada para esta cena que:
        
        1. **Represente visualmente** o conteúdo falado
        2. **Seja apropriada** para o público-alvo
        3. **Mantenha consistência** com o estilo do vídeo
        4. **Seja específica** o suficiente para gerar uma imagem
        5. **Evite elementos** que possam ser controversos
        
        ## Formato
        Retorne apenas a descrição visual, máximo 100 palavras.
        Use linguagem descritiva e específica.
        
        Exemplo: "Uma pessoa jovem sorrindo enquanto usa um laptop moderno em um escritório bem iluminado, com plantas ao fundo e uma xícara de café na mesa, ambiente profissional e acolhedor"
        """
        
        # Chama IA para gerar prompt
        visual_prompt = call_ai_for_visual_prompt(ai_prompt)
        
        # Adiciona modificadores de estilo
        styled_prompt = apply_style_modifiers(visual_prompt, script_context)
        
        prompts.append({
            'scene_index': scene['index'],
            'original_text': scene['text'],
            'visual_prompt': styled_prompt,
            'narrative_moment': scene['narrative_moment']
        })
    
    return prompts

def apply_style_modifiers(base_prompt, context):
    style = context.get('image_style', 'realistic')
    
    style_modifiers = {
        'realistic': ', fotografia profissional, alta qualidade, iluminação natural',
        'cartoon': ', estilo cartoon, cores vibrantes, ilustração digital',
        'artistic': ', arte digital, estilo artístico, composição criativa',
        'minimalist': ', estilo minimalista, cores suaves, composição limpa',
        'corporate': ', ambiente corporativo, profissional, moderno'
    }
    
    modifier = style_modifiers.get(style, '')
    
    # Adiciona qualidade e formato
    quality_modifier = ', 4K, alta resolução'
    format_modifier = context.get('format', 'landscape')
    
    if format_modifier == 'landscape':
        format_mod = ', formato paisagem 16:9'
    elif format_modifier == 'portrait':
        format_mod = ', formato retrato 9:16'
    else:
        format_mod = ', formato quadrado 1:1'
    
    return base_prompt + modifier + quality_modifier + format_mod
```

### Distribuição Temporal de Cenas

```python
def distribute_scenes_evenly(scenes, total_duration):
    # Distribui cenas ao longo da duração total do vídeo
    if not scenes:
        return []
    
    scene_duration = total_duration / len(scenes)
    distributed_scenes = []
    
    for i, scene in enumerate(scenes):
        start_time = i * scene_duration
        end_time = (i + 1) * scene_duration
        
        distributed_scenes.append({
            **scene,
            'start_time': start_time,
            'end_time': end_time,
            'duration': scene_duration
        })
    
    return distributed_scenes
```

---

## 7. 🎬 Processo de Criação de Vídeo

### Localização
- **Arquivo**: `backend/services/video_creation_service.py`
- **Classe**: `VideoCreationService`
- **Endpoint**: `POST /api/videos/create`

### Dependências e Configuração

```python
# Imports principais
from moviepy.editor import (
    VideoFileClip, ImageClip, AudioFileClip, CompositeVideoClip,
    TextClip, concatenate_videoclips, ColorClip
)
from moviepy.video.fx.resize import resize
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout
from moviepy.audio.fx.volumex import volumex

# Configuração PIL para compatibilidade
from PIL import Image
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.LANCZOS
```

### Normalização de Resolução

```python
def _normalize_resolution(self, resolution):
    # Converte qualidades para resoluções específicas
    quality_to_resolution = {
        '720p': '1280x720',
        '1080p': '1920x1080',
        '4k': '3840x2160',
        'hd': '1280x720',
        'full_hd': '1920x1080',
        'ultra_hd': '3840x2160'
    }
    
    # Se já é uma resolução válida (formato WxH)
    if 'x' in resolution and self._is_valid_resolution(resolution):
        return resolution
    
    # Converte qualidade para resolução
    normalized = quality_to_resolution.get(resolution.lower(), '1920x1080')
    self._log('info', f'Resolução normalizada: {resolution} -> {normalized}')
    return normalized

def _is_valid_resolution(self, resolution):
    try:
        width, height = resolution.split('x')
        return width.isdigit() and height.isdigit()
    except:
        return False
```

### Sincronização Áudio-Vídeo

```python
def _synchronize_audio_video(self, audio_path, images, tts_segments):
    # Carrega áudio principal
    audio_clip = AudioFileClip(audio_path)
    total_duration = audio_clip.duration
    
    # Se temos segmentos TTS, usa timing preciso
    if tts_segments:
        return self._sync_with_tts_segments(images, tts_segments, total_duration)
    else:
        return self._sync_evenly(images, total_duration)

def _sync_with_tts_segments(self, images, tts_segments, total_duration):
    video_clips = []
    
    # Calcula quantas imagens por segmento
    images_per_segment = len(images) / len(tts_segments)
    
    for i, segment in enumerate(tts_segments):
        # Determina quais imagens usar neste segmento
        start_img_idx = int(i * images_per_segment)
        end_img_idx = int((i + 1) * images_per_segment)
        segment_images = images[start_img_idx:end_img_idx]
        
        if not segment_images:
            continue
            
        # Duração do segmento
        segment_duration = segment['end_time'] - segment['start_time']
        
        # Cria clipes para as imagens do segmento
        segment_clips = self._create_image_clips(
            segment_images, 
            segment_duration, 
            segment['start_time']
        )
        
        video_clips.extend(segment_clips)
    
    return video_clips

def _sync_evenly(self, images, total_duration):
    # Distribui imagens uniformemente
    if not images:
        return []
    
    duration_per_image = total_duration / len(images)
    video_clips = []
    
    for i, image_data in enumerate(images):
        start_time = i * duration_per_image
        clip = self._create_single_image_clip(
            image_data, 
            duration_per_image, 
            start_time
        )
        video_clips.append(clip)
    
    return video_clips
```

### Criação de Clipes de Imagem

```python
def _create_image_clips(self, images, total_duration, start_time):
    clips = []
    duration_per_image = total_duration / len(images) if images else 0
    
    for i, image_data in enumerate(images):
        image_start = start_time + (i * duration_per_image)
        clip = self._create_single_image_clip(
            image_data, 
            duration_per_image, 
            image_start
        )
        clips.append(clip)
    
    return clips

def _create_single_image_clip(self, image_data, duration, start_time):
    image_path = image_data.get('file_path') or image_data.get('path')
    
    if not image_path or not os.path.exists(image_path):
        # Cria imagem placeholder
        return self._create_placeholder_clip(duration, start_time)
    
    try:
        # Carrega imagem
        clip = ImageClip(image_path, duration=duration)
        
        # Redimensiona para resolução alvo
        target_width, target_height = self._get_target_dimensions()
        clip = clip.resize((target_width, target_height))
        
        # Define tempo de início
        clip = clip.set_start(start_time)
        
        # Adiciona efeitos de transição
        if self.transitions_enabled:
            clip = self._add_transition_effects(clip)
        
        return clip
        
    except Exception as e:
        self._log('warning', f'Erro ao processar imagem {image_path}: {str(e)}')
        return self._create_placeholder_clip(duration, start_time)

def _create_placeholder_clip(self, duration, start_time):
    # Cria clip colorido como placeholder
    color = (50, 50, 50)  # Cinza escuro
    target_width, target_height = self._get_target_dimensions()
    
    clip = ColorClip(
        size=(target_width, target_height), 
        color=color, 
        duration=duration
    ).set_start(start_time)
    
    return clip
```

### Efeitos de Transição

```python
def _add_transition_effects(self, clip):
    # Adiciona fade in/out suave
    fade_duration = min(0.5, clip.duration / 4)  # Máximo 0.5s ou 1/4 da duração
    
    if clip.duration > fade_duration * 2:
        clip = fadein(clip, fade_duration)
        clip = fadeout(clip, fade_duration)
    
    return clip

def _add_advanced_transitions(self, clips):
    # Transições mais avançadas entre clipes
    if len(clips) < 2:
        return clips
    
    transition_clips = []
    transition_duration = 0.3
    
    for i in range(len(clips) - 1):
        current_clip = clips[i]
        next_clip = clips[i + 1]
        
        # Ajusta timing para sobreposição
        overlap_start = current_clip.end - transition_duration
        next_clip = next_clip.set_start(overlap_start)
        
        # Adiciona fade out ao clip atual
        current_clip = fadeout(current_clip, transition_duration)
        
        # Adiciona fade in ao próximo clip
        next_clip = fadein(next_clip, transition_duration)
        
        transition_clips.extend([current_clip, next_clip])
    
    return transition_clips
```

### Geração de Legendas

```python
def _add_subtitles(self, video_clip, script_text, tts_segments):
    if not self.subtitles_enabled:
        return video_clip
    
    subtitle_clips = []
    
    if tts_segments:
        # Usa timing preciso dos segmentos TTS
        for segment in tts_segments:
            subtitle_clip = self._create_subtitle_clip(
                segment['text'],
                segment['start_time'],
                segment['duration']
            )
            subtitle_clips.append(subtitle_clip)
    else:
        # Distribui texto uniformemente
        sentences = self._split_text_for_subtitles(script_text)
        duration_per_sentence = video_clip.duration / len(sentences)
        
        for i, sentence in enumerate(sentences):
            start_time = i * duration_per_sentence
            subtitle_clip = self._create_subtitle_clip(
                sentence,
                start_time,
                duration_per_sentence
            )
            subtitle_clips.append(subtitle_clip)
    
    # Combina legendas com vídeo
    if subtitle_clips:
        return CompositeVideoClip([video_clip] + subtitle_clips)
    
    return video_clip

def _create_subtitle_clip(self, text, start_time, duration):
    # Configurações de estilo das legendas
    font_size = self._calculate_font_size()
    font_color = 'white'
    stroke_color = 'black'
    stroke_width = 2
    
    # Cria clip de texto
    txt_clip = TextClip(
        text,
        fontsize=font_size,
        color=font_color,
        stroke_color=stroke_color,
        stroke_width=stroke_width,
        font='Arial-Bold'
    ).set_position(('center', 'bottom')).set_duration(duration).set_start(start_time)
    
    return txt_clip

def _calculate_font_size(self):
    # Calcula tamanho da fonte baseado na resolução
    width, height = self._get_target_dimensions()
    
    if height >= 2160:  # 4K
        return 72
    elif height >= 1080:  # Full HD
        return 48
    elif height >= 720:  # HD
        return 36
    else:  # SD
        return 24
```

### Renderização Final

```python
def _render_final_video(self, video_clips, audio_clip, output_path):
    try:
        # Combina todos os clipes de vídeo
        if len(video_clips) > 1:
            final_video = CompositeVideoClip(video_clips)
        else:
            final_video = video_clips[0]
        
        # Adiciona áudio
        final_video = final_video.with_audio(audio_clip)
        
        # Configurações de renderização
        render_settings = self._get_render_settings()
        
        # Renderiza vídeo
        final_video.write_videofile(
            output_path,
            **render_settings,
            verbose=False,
            logger=None
        )
        
        # Limpa recursos
        final_video.close()
        audio_clip.close()
        for clip in video_clips:
            clip.close()
        
        return output_path
        
    except Exception as e:
        self._log('error', f'Erro na renderização: {str(e)}')
        raise

def _get_render_settings(self):
    return {
        'codec': 'libx264',
        'audio_codec': 'aac',
        'temp_audiofile': 'temp-audio.m4a',
        'remove_temp': True,
        'fps': 30,
        'bitrate': '5000k'
    }
```

---

## 8. 🎯 Processo de Orquestração

### Localização
- **Arquivo**: `backend/services/pipeline_service.py`
- **Classe**: `PipelineService`
- **Arquivo**: `backend/pipeline_complete.py`

### Estados da Pipeline

```python
class PipelineState(Enum):
    IDLE = "idle"
    EXTRACTING = "extracting"
    GENERATING_TITLES = "generating_titles"
    GENERATING_PREMISE = "generating_premise"
    GENERATING_SCRIPT = "generating_script"
    PROCESSING_SCRIPT = "processing_script"
    GENERATING_TTS = "generating_tts"
    GENERATING_IMAGES = "generating_images"
    CREATING_VIDEO = "creating_video"
    COMPLETED = "completed"
    ERROR = "error"
```

### Fluxo Principal

```python
def execute_complete_pipeline(self, config):
    pipeline_id = str(uuid.uuid4())
    
    try:
        # Inicializa pipeline
        self._update_pipeline_status(pipeline_id, PipelineState.EXTRACTING)
        
        # Etapa 1: Extração
        extraction_result = self._execute_extraction(config)
        
        # Etapa 2: Geração de Títulos
        self._update_pipeline_status(pipeline_id, PipelineState.GENERATING_TITLES)
        titles_result = self._execute_title_generation(extraction_result, config)
        
        # Etapa 3: Geração de Premissa
        self._update_pipeline_status(pipeline_id, PipelineState.GENERATING_PREMISE)
        premise_result = self._execute_premise_generation(titles_result, config)
        
        # Etapa 4: Geração de Roteiro
        self._update_pipeline_status(pipeline_id, PipelineState.GENERATING_SCRIPT)
        script_result = self._execute_script_generation(premise_result, config)
        
        # Etapa 5: Processamento de Roteiro
        self._update_pipeline_status(pipeline_id, PipelineState.PROCESSING_SCRIPT)
        processed_script = self._execute_script_processing(script_result, config)
        
        # Etapa 6: Geração de TTS
        self._update_pipeline_status(pipeline_id, PipelineState.GENERATING_TTS)
        tts_result = self._execute_tts_generation(processed_script, config)
        
        # Etapa 7: Geração de Imagens
        self._update_pipeline_status(pipeline_id, PipelineState.GENERATING_IMAGES)
        images_result = self._execute_image_generation(processed_script, config)
        
        # Etapa 8: Criação de Vídeo
        self._update_pipeline_status(pipeline_id, PipelineState.CREATING_VIDEO)
        video_result = self._execute_video_creation(
            tts_result, images_result, processed_script, config
        )
        
        # Finalização
        self._update_pipeline_status(pipeline_id, PipelineState.COMPLETED)
        
        return {
            'pipeline_id': pipeline_id,
            'status': 'completed',
            'results': {
                'extraction': extraction_result,
                'titles': titles_result,
                'premise': premise_result,
                'script': script_result,
                'tts': tts_result,
                'images': images_result,
                'video': video_result
            }
        }
        
    except Exception as e:
        self._update_pipeline_status(pipeline_id, PipelineState.ERROR)
        self._log_error(pipeline_id, str(e))
        raise
```

### Monitoramento e Logs

```python
def _update_pipeline_status(self, pipeline_id, state, progress=None, message=None):
    status_update = {
        'pipeline_id': pipeline_id,
        'state': state.value,
        'timestamp': datetime.now().isoformat(),
        'progress': progress,
        'message': message
    }
    
    # Salva no banco/cache
    self._save_pipeline_status(pipeline_id, status_update)
    
    # Emite evento para frontend (WebSocket)
    self._emit_status_update(status_update)

def _log_error(self, pipeline_id, error_message):
    error_log = {
        'pipeline_id': pipeline_id,
        'error': error_message,
        'timestamp': datetime.now().isoformat(),
        'stack_trace': traceback.format_exc()
    }
    
    # Salva log de erro
    self._save_error_log(error_log)
    
    # Notifica sistema de monitoramento
    self._notify_error(error_log)
```

---

## 🔧 Configurações e Dependências

### Variáveis de Ambiente

```bash
# APIs de IA
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...
OPENROUTER_API_KEY=...
TOGETHER_API_KEY=...
ELEVENLABS_API_KEY=...

# Configurações de TTS
TTS_PROVIDER=gemini
TTS_VOICE_ID=pt-BR-Standard-A
TTS_SPEED=1.0
TTS_PITCH=0.0

# Configurações de Imagem
IMAGE_PROVIDER=together
IMAGE_MODEL=black-forest-labs/FLUX.1-schnell
IMAGE_STYLE=realistic
IMAGE_QUALITY=high

# Configurações de Vídeo
VIDEO_RESOLUTION=1920x1080
VIDEO_FPS=30
VIDEO_BITRATE=5000k
SUBTITLES_ENABLED=true
TRANSITIONS_ENABLED=true

# Configurações de Pipeline
MAX_CONCURRENT_PIPELINES=3
PIPELINE_TIMEOUT=3600
AUTO_CLEANUP=true
```

### Dependências Python

```txt
# Core
Flask==2.3.3
Flask-CORS==4.0.0
requests==2.31.0

# IA e APIs
openai==1.3.0
google-generativeai==0.3.0

# Processamento de Mídia
moviepy==1.0.3
Pillow==10.0.0
pydub==0.25.1

# Extração de Dados
yt-dlp==2023.9.24
beautifulsoup4==4.12.2

# Utilitários
python-dotenv==1.0.0
psutil==5.9.5
colorama==0.4.6
```

### Estrutura de Arquivos

```
backend/
├── services/
│   ├── pipeline_service.py      # Orquestração principal
│   ├── storyteller_service.py   # Geração de roteiros
│   ├── tts_service.py           # Text-to-Speech
│   ├── video_creation_service.py # Criação de vídeos
│   └── title_generator.py       # Geração de títulos
├── routes/
│   ├── automations.py           # Rotas de automação
│   ├── images.py                # Rotas de imagens
│   ├── videos.py                # Rotas de vídeos
│   └── scripts.py               # Rotas de roteiros
├── utils/
│   ├── ai_clients.py            # Clientes de IA
│   ├── file_manager.py          # Gerenciamento de arquivos
│   └── validators.py            # Validações
└── pipeline_complete.py         # Pipeline completa
```

---

## 🚨 Diagnóstico e Troubleshooting

### Logs de Sistema

```python
# Configuração de logging
import logging
from datetime import datetime

class PipelineLogger:
    def __init__(self, pipeline_id):
        self.pipeline_id = pipeline_id
        self.logger = logging.getLogger(f'pipeline_{pipeline_id}')
        
        # Configurar handler para arquivo
        handler = logging.FileHandler(f'logs/pipeline_{pipeline_id}.log')
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def log_step(self, step, status, details=None):
        message = f'Step: {step} | Status: {status}'
        if details:
            message += f' | Details: {details}'
        
        if status == 'error':
            self.logger.error(message)
        elif status == 'warning':
            self.logger.warning(message)
        else:
            self.logger.info(message)
```

### Verificações de Saúde

```python
def health_check():
    checks = {
        'apis': check_api_connectivity(),
        'storage': check_storage_space(),
        'dependencies': check_dependencies(),
        'services': check_services_status()
    }
    
    overall_health = all(checks.values())
    
    return {
        'healthy': overall_health,
        'checks': checks,
        'timestamp': datetime.now().isoformat()
    }

def check_api_connectivity():
    apis_to_check = [
        ('OpenAI', 'https://api.openai.com/v1/models'),
        ('Gemini', 'https://generativelanguage.googleapis.com'),
        ('ElevenLabs', 'https://api.elevenlabs.io/v1/voices')
    ]
    
    results = {}
    for name, url in apis_to_check:
        try:
            response = requests.get(url, timeout=5)
            results[name] = response.status_code < 400
        except:
            results[name] = False
    
    return all(results.values())
```

### Códigos de Erro Comuns

| Código | Descrição | Solução |
|--------|-----------|----------|
| E001 | API Key inválida | Verificar variáveis de ambiente |
| E002 | Quota de API excedida | Aguardar reset ou trocar provider |
| E003 | Arquivo não encontrado | Verificar paths e permissões |
| E004 | Erro de renderização | Verificar FFmpeg e dependências |
| E005 | Timeout na pipeline | Aumentar timeout ou otimizar processo |
| E006 | Memória insuficiente | Reduzir qualidade ou liberar recursos |
| E007 | Formato não suportado | Converter arquivo para formato válido |

---

## 📊 Métricas e Performance

### Tempos Médios por Etapa

- **Extração**: 10-30 segundos
- **Geração de Títulos**: 15-45 segundos
- **Geração de Premissa**: 10-30 segundos
- **Geração de Roteiro**: 60-180 segundos
- **Processamento TTS**: 30-120 segundos
- **Geração de Imagens**: 60-300 segundos
- **Criação de Vídeo**: 120-600 segundos

**Total**: 5-20 minutos (dependendo da complexidade)

### Otimizações Implementadas

1. **Cache de Resultados**: Evita reprocessamento
2. **Processamento Paralelo**: TTS e imagens em paralelo
3. **Compressão de Imagens**: Reduz uso de storage
4. **Cleanup Automático**: Remove arquivos temporários
5. **Rate Limiting**: Evita bloqueios de API
6. **Retry Logic**: Recuperação automática de falhas

---

Este documento fornece uma visão completa e detalhada de cada processo da pipeline, permitindo diagnóstico preciso e manutenção eficiente do sistema.