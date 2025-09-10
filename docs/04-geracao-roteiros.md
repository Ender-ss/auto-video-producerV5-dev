# 📝 Geração de Roteiros

## Visão Geral
Sistema automatizado de criação de roteiros baseados em premissas geradas.

## Arquivos Envolvidos
- `backend/routes/scripts.py` - Rotas de geração
- `backend/services/storyteller_service.py` - Serviço principal
- `backend/services/script_generator.py` - Gerador de conteúdo

## Processo de Geração

### 1. Estrutura do Roteiro
```javascript
{
  "title": "string",
  "duration": 420, // segundos
  "chapters": [
    {
      "chapter_number": 1,
      "title": "string",
      "content": "string",
      "duration": 60,
      "hook": "string"
    }
  ],
  "metadata": {
    "word_count": 500,
    "reading_time": 7,
    "keywords": ["string"]
  }
}
```

### 2. Divisão em Capítulos
**Padrão:** 5 capítulos para vídeos de 5-7 minutos

#### Capítulo 1: Gancho (Hook)
- **Duração**: 30-45 segundos
- **Função**: Prender atenção imediatamente
- **Técnicas**: Pergunta intrigante, estatística chocante

#### Capítulo 2: Contexto
- **Duração**: 60-90 segundos
- **Função**: Estabelecer problema/situação
- **Técnicas**: Storytelling pessoal

#### Capítulo 3: Desenvolvimento
- **Duração**: 90-120 segundos
- **Função**: Apresentar solução principal
- **Técnicas**: Exemplos práticos

#### Capítulo 4: Aplicação
- **Duração**: 60-90 segundos
- **Função**: Como aplicar no dia a dia
- **Técnicas**: Passo a passo

#### Capítulo 5: Conclusão + CTA
- **Duração**: 30-60 segundos
- **Função**: Finalizar e convidar para ação
- **Técnicas**: Recap + call-to-action

### 3. Prompt de Geração por Agente

#### Agente Milionário
```
Crie um roteiro inspirador baseado na premissa:
[PREMISSA]

ESTRUTURA:
1. Hook: Comece com uma pergunta provocativa
2. Contexto: Apresente o desafio financeiro
3. Solução: Mostre a virada de jogo
4. Aplicação: Dê 3 dicas práticas
5. Final: Inspire ação imediata

TOM: Inspirador e motivacional
DURAÇÃO: 6 minutos
```

#### Storyteller
```
Crie um roteiro educativo baseado na premissa:
[PREMISSA]

ESTRUTURA:
1. Introdução: Contexto do tema
2. Desenvolvimento: Profundidade no assunto
3. Exemplos: Casos práticos
4. Conclusão: Síntese dos aprendizados

TOM: Didático e acessível
DURAÇÃO: 8 minutos
```

### 4. Cálculo de Duração
```python
def estimate_duration(script, words_per_minute=150):
    word_count = len(script.split())
    minutes = word_count / words_per_minute
    return int(minutes * 60)  # Retorna em segundos
```

### 5. Ganchos de Engajamento

#### Tipos de Ganchos
1. **Pergunta Provocativa**: "Você sabia que 90% das pessoas...?"
2. **Estatística Impactante**: "A cada 5 minutos, uma pessoa..."
3. **Promessa de Valor**: "Em 7 minutos, você vai descobrir..."
4. **Contraste**: "O que ricos fazem diferente..."
5. **Urgência**: "Se você não fizer isso agora..."

#### Exemplos por Tema
| Tema | Gancho Milionário | Gancho Storyteller |
|------|-------------------|-------------------|
| Investimentos | "O que 1% faz que 99% não sabe" | "Como investimentos mudam vidas" |
| Educação | "Por que escolas não ensinam isso" | "O poder do conhecimento financeiro" |
| Empreendedorismo | "De zero a 100 mil em 6 meses" | "A jornada do empreendedor" |

## API de Geração

### POST /api/generate-scripts
```json
{
  "premise": "string",
  "title": "string",
  "agent_type": "millionaire_stories|storyteller",
  "chapters": 5,
  "duration_target": 420,
  "include_hooks": true,
  "style": "inspirational|educational|casual"
}
```

### Response
```json
{
  "script": {
    "title": "Como Rafael Mendes Sair das Dívidas em 90 Dias",
    "duration": 420,
    "chapters": [
      {
        "chapter_number": 1,
        "title": "O Dia em que Tudo Mudou",
        "content": "Rafael Mendes estava no fundo do poço...",
        "duration": 45,
        "hook": "Você já se sentiu assim?"
      }
    ]
  },
  "metadata": {
    "total_words": 630,
    "estimated_cost": 0.02,
    "processing_time": 3.5
  }
}
```

## Frontend - Interface de Edição

### Componente ScriptEditor
```javascript
// frontend/components/ScriptEditor.jsx
const ScriptEditor = ({ script, onUpdate }) => {
  return (
    <div className="script-editor">
      <h2>{script.title}</h2>
      <div className="duration-display">
        Duração: {Math.floor(script.duration / 60)}min {script.duration % 60}s
      </div>
      
      {script.chapters.map(chapter => (
        <div key={chapter.chapter_number} className="chapter-card">
          <h3>Capítulo {chapter.chapter_number}: {chapter.title}</h3>
          <textarea 
            value={chapter.content}
            onChange={(e) => onUpdate(chapter.chapter_number, e.target.value)}
          />
          <div className="chapter-duration">
            {chapter.duration}s
          </div>
        </div>
      ))}
    </div>
  );
};
```

## Otimizações

### 1. Cache de Roteiros
- Cache de 48 horas para mesma premissa
- Key baseada em: hash(premissa + agente + configurações)

### 2. Ajuste Dinâmico de Duração
```python
def adjust_script_length(script, target_duration):
    current_duration = script['duration']
    ratio = target_duration / current_duration
    
    # Ajusta cada capítulo proporcionalmente
    for chapter in script['chapters']:
        chapter['duration'] = int(chapter['duration'] * ratio)
    
    return script
```

### 3. Análise de Sentimento
- Verifica tonalidade do texto
- Sugere ajustes se muito negativo
- Mantém consistência com marca

## Testes de Qualidade

### 1. Testes de Clareza
- Flesch Reading Ease para português
- Evita jargões técnicos excessivos
- Verifica comprimento de frases

### 2. Testes de Engajamento
- Análise de ganchos
- Verificação de CTA presente
- Balanceamento de storytelling vs informação

### 3. Métricas de Performance
```json
{
  "quality_score": 0.92,
  "engagement_prediction": 0.85,
  "readability_score": 78,
  "keyword_density": 2.1,
  "processing_time": 3.2
}
```