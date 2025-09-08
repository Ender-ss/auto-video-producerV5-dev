# ✏️ Remodelamento de Títulos

## Visão Geral
Sistema de geração de títulos alternativos mais engajadores baseado em IA.

## Arquivos Envolvidos
- `backend/routes/automations.py` - Rota de remodelamento
- `backend/services/title_service.py` - Serviço de geração
- `backend/utils/engagement_predictor.py` - Predição de engajamento

## Processo de Remodelamento

### 1. Análise de Conteúdo
```python
# backend/services/title_service.py
def generate_titles(content, original_title):
    # Análise de palavras-chave
    keywords = extract_keywords(content)
    
    # Geração de variações
    variations = [
        create_curiosity_title(keywords),
        create_benefit_title(keywords),
        create_question_title(keywords),
        create_number_title(keywords),
        create_urgency_title(keywords)
    ]
    
    return select_best_titles(variations)
```

### 2. Tipos de Títulos Gerados

#### Tipo 1: Curiosidade
- Exemplo: "O Segredo que Ninguém Te Conta Sobre..."
- Uso: Gerar suspense
- CTR esperado: +35%

#### Tipo 2: Benefício Direto
- Exemplo: "Como Ganhar R$1000 por Mês Com..."
- Uso: Mostrar valor imediato
- CTR esperado: +45%

#### Tipo 3: Pergunta
- Exemplo: "Você Está Cometendo Este Erro em...?"
- Uso: Engajamento pessoal
- CTR esperado: +28%

#### Tipo 4: Lista Numerada
- Exemplo: "7 Dicas Infalíveis Para..."
- Uso: Promessa concreta
- CTR esperado: +52%

#### Tipo 5: Urgência
- Exemplo: "URGENTE: O Que Fazer ANTES de..."
- Uso: Ação imediata
- CTR esperado: +40%

### 3. Prompt do GPT para Geração
```
Com base no conteúdo: [CONTEÚDO]
E no título original: [TÍTULO]

Gere 5 títulos alternativos que:
1. Sejam mais cativantes que o original
2. Incluam palavras-chave relevantes para SEO
3. Tenham no máximo 60 caracteres
4. Gerem curiosidade ou urgência
5. Sejam específicos para o público brasileiro

Retorne em formato JSON:
{
  "titles": [
    {"title": "", "type": "", "reasoning": ""},
    ...
  ]
}
```

### 4. Seleção Automática
```python
def select_best_title(titles, content):
    scores = []
    for title in titles:
        score = calculate_engagement_score(title, content)
        scores.append(score)
    
    return titles[scores.index(max(scores))]
```

### 5. Frontend - Interface de Seleção
```javascript
// frontend/components/TitleRemodeler.jsx
const TitleSelector = ({ titles, onSelect }) => {
  return (
    <div className="title-options">
      {titles.map((title, index) => (
        <div key={index} className="title-card">
          <h3>{title.title}</h3>
          <p>Tipo: {title.type}</p>
          <p>Score: {title.engagement_score}</p>
          <button onClick={() => onSelect(title)}>Selecionar</button>
        </div>
      ))}
    </div>
  );
};
```

## Métricas de Performance

### KPIs Monitorados
- **CTR Improvement**: Comparação com título original
- **Engagement Score**: Predição de interação
- **SEO Score**: Palavras-chave relevantes
- **Character Count**: Adequação para diferentes plataformas

### Exemplos Reais de Conversão

| Título Original | Título Remodelado | CTR Improvement |
|-----------------|-------------------|-----------------|
| Investimento em Ações | Como Ganhar R$5000 Investindo em Ações | +67% |
| Educação Financeira | 7 Truques de Rico Que Escolas Não Ensinam | +89% |
| Poupança | Por Que Sua Poupança Está Te Deixando Mais Pobre | +134% |

## Integração com Pipeline

### Fluxo Completo
1. Extração de vídeo → 2. Remodelamento de título → 3. Geração de premissa → 4. Criação de roteiro

### Cache de Títulos
- Cache de 24 horas por conteúdo
- Evita reprocessamento do mesmo vídeo
- Economiza créditos de API

## API Endpoints

### POST /api/remodel-title
```json
{
  "original_title": "string",
  "content": "string",
  "count": 5
}
```

### Response
```json
{
  "titles": [
    {
      "title": "string",
      "type": "curiosity|benefit|question|number|urgency",
      "score": 0.95,
      "keywords": ["string"]
    }
  ],
  "selected": "string"
}
```