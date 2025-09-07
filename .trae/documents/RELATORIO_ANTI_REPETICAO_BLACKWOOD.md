# 🔍 Relatório Técnico: Problema de Repetição "Blackwood" e Sistema Anti-Repetição

## 📋 Sumário Executivo

Este relatório analisa o problema de repetição do nome "Blackwood" nas premissas e roteiros gerados pelo Auto Video Producer, identificando as causas raiz e propondo soluções técnicas para garantir unicidade de personagens e histórias.

## 🎯 Problema Identificado

### Sintomas Observados
- Nome "Arthur Blackwood" aparece repetidamente nas premissas geradas
- Personagens e cenários similares em diferentes roteiros
- Falta de diversidade narrativa nos conteúdos gerados

### Análise da Causa Raiz

#### 1. **Viés da IA Generativa**
- As IAs (Gemini, OpenAI, Claude) tendem a usar padrões comuns em seus dados de treinamento
- "Blackwood" é um sobrenome frequente em ficção empresarial/milionário
- Ausência de instruções específicas contra repetição de nomes

#### 2. **Falta de Sistema de Memória**
- Não há verificação de nomes/personagens já utilizados
- Cada geração é independente, sem contexto histórico
- Sistema MemoryBridge atual foca apenas em capítulos, não em histórico global

## 🔧 Análise Técnica do Sistema Atual

### Fluxo de Geração de Premissas

```
1. Título → Prompt Padrão → IA → Premissa
2. Premissa → StorytellerService → Roteiro
3. Roteiro → Capítulos (com MemoryBridge local)
```

### Pontos Críticos de Repetição

#### **Arquivo: `routes/premise.py`**
- **Função**: `get_default_premise_prompt()`
- **Problema**: Prompt genérico sem instruções anti-repetição
- **Localização**: Linhas 29-51

#### **Arquivo: `services/storyteller_service.py`**
- **Classe**: `PromptVariator`
- **Problema**: Variações limitadas, sem controle de nomes
- **Localização**: Linhas 320-450

#### **Arquivo: `config/prompts_config.json`**
- **Seção**: `premises.prompt`
- **Problema**: Não inclui instruções de diversidade

## 🛠️ Soluções Técnicas Propostas

### 1. **Sistema de Banco de Nomes Únicos**

#### Implementação
```python
# Novo arquivo: services/name_diversity_service.py
class NameDiversityService:
    def __init__(self):
        self.used_names = set()
        self.name_pools = {
            'male_first': ['Marcus', 'David', 'Rafael', 'Carlos', 'Eduardo'],
            'female_first': ['Ana', 'Sofia', 'Isabella', 'Camila', 'Lucia'],
            'surnames': ['Silva', 'Santos', 'Oliveira', 'Costa', 'Ferreira']
        }
    
    def get_unique_character_name(self, gender='male'):
        # Gera combinação única não utilizada
        pass
    
    def register_used_name(self, name):
        # Registra nome como usado
        pass
```

### 2. **Prompt Anti-Repetição Aprimorado**

#### Modificação em `get_default_premise_prompt()`
```python
def get_default_premise_prompt():
    return """# Gerador de Premissas Profissionais para Vídeos

Você é um especialista em criação de conteúdo e storytelling para YouTube.

## INSTRUÇÕES CRÍTICAS DE DIVERSIDADE:
1. NUNCA use nomes como "Blackwood", "Johnson", "Smith" ou outros clichês
2. Crie personagens com nomes ÚNICOS e DIVERSOS
3. Varie nacionalidades, backgrounds e contextos
4. Use nomes brasileiros autênticos quando apropriado
5. Evite padrões repetitivos de personalidade

## BANCO DE NOMES SUGERIDOS:
- Masculinos: Rafael Mendes, Carlos Andrade, Eduardo Ribeiro
- Femininos: Ana Beatriz, Sofia Carvalho, Isabella Rocha

## Sua tarefa é criar premissas envolventes e ÚNICAS..."""
```

### 3. **Sistema de Verificação Histórica**

#### Nova Classe: `HistoryTracker`
```python
class HistoryTracker:
    def __init__(self):
        self.redis_client = self._init_redis()
        self.history_key = "avp:generation_history"
    
    def check_content_similarity(self, new_content):
        # Verifica similaridade com conteúdos anteriores
        pass
    
    def extract_character_names(self, content):
        # Extrai nomes de personagens usando NLP
        pass
    
    def is_name_overused(self, name, threshold=3):
        # Verifica se nome foi usado mais que o limite
        pass
```

### 4. **Integração com StorytellerService**

#### Modificação na Classe `PromptVariator`
```python
class PromptVariator:
    def __init__(self):
        # ... código existente ...
        self.name_service = NameDiversityService()
        self.history_tracker = HistoryTracker()
    
    def generate_varied_prompt(self, title, premise, agent_type, ...):
        # Verificar histórico antes de gerar
        if self.history_tracker.is_content_similar(premise):
            # Forçar regeneração com mais diversidade
            pass
        
        # Injetar nomes únicos no prompt
        unique_names = self.name_service.get_character_suggestions()
        
        # ... resto do código ...
```

## 📊 Implementação por Fases

### **Fase 1: Correção Imediata (1-2 dias)**
1. Atualizar `get_default_premise_prompt()` com instruções anti-repetição
2. Modificar `prompts_config.json` com diversidade obrigatória
3. Adicionar validação de nomes no `parse_premises_response()`

### **Fase 2: Sistema de Memória (3-5 dias)**
1. Implementar `NameDiversityService`
2. Criar `HistoryTracker` com Redis
3. Integrar verificação no fluxo de geração

### **Fase 3: Otimização Avançada (1 semana)**
1. Implementar NLP para detecção de similaridade
2. Sistema de feedback automático
3. Dashboard de diversidade de conteúdo

## 🔧 Configurações Recomendadas

### **Arquivo: `config/diversity_config.json`**
```json
{
  "anti_repetition": {
    "enabled": true,
    "name_reuse_limit": 2,
    "similarity_threshold": 0.7,
    "force_diversity": true
  },
  "name_pools": {
    "brazilian_male": ["Rafael", "Carlos", "Eduardo", "Thiago", "Bruno"],
    "brazilian_female": ["Ana", "Sofia", "Isabella", "Camila", "Lucia"],
    "surnames": ["Silva", "Santos", "Oliveira", "Costa", "Ferreira"]
  },
  "forbidden_names": ["Blackwood", "Johnson", "Smith", "Williams"]
}
```

### **Variáveis de Ambiente**
```env
# Anti-repetição
ENABLE_DIVERSITY_CHECK=true
MAX_NAME_REUSE=2
SIMILARITY_THRESHOLD=0.7

# Redis para histórico
REDIS_HISTORY_TTL=2592000  # 30 dias
```

## 🎯 Pontos de Implementação Específicos

### **1. Modificar `routes/premise.py`**
```python
# Linha ~200: Adicionar verificação antes da geração
def generate_premises():
    # ... código existente ...
    
    # NOVO: Verificar diversidade
    diversity_service = NameDiversityService()
    if diversity_service.should_regenerate(titles):
        final_prompt += "\n\nIMPORTANTE: Use nomes completamente diferentes dos anteriores."
```

### **2. Atualizar `services/storyteller_service.py`**
```python
# Linha ~400: Injetar diversidade no prompt
def generate_varied_prompt(self, ...):
    # ... código existente ...
    
    # NOVO: Adicionar instruções de diversidade
    diversity_instructions = self._get_diversity_instructions()
    prompt = f"{prompt}\n\n{diversity_instructions}"
```

### **3. Criar `services/content_validator.py`**
```python
class ContentValidator:
    def validate_uniqueness(self, content):
        # Validar se conteúdo é suficientemente único
        pass
    
    def extract_entities(self, content):
        # Extrair nomes, lugares, empresas
        pass
```

## 📈 Métricas de Sucesso

### **KPIs de Diversidade**
1. **Taxa de Repetição de Nomes**: < 5%
2. **Diversidade de Personagens**: > 90% únicos
3. **Similaridade de Enredos**: < 30%
4. **Tempo de Geração**: Impacto < 10%

### **Monitoramento**
```python
# Dashboard de métricas
class DiversityMetrics:
    def calculate_name_diversity_score(self):
        # Calcular score de diversidade
        pass
    
    def generate_diversity_report(self):
        # Relatório semanal de diversidade
        pass
```

## 🚀 Próximos Passos

### **Implementação Imediata**
1. ✅ Atualizar prompts com instruções anti-repetição
2. ✅ Criar lista de nomes proibidos
3. ✅ Implementar validação básica

### **Desenvolvimento Futuro**
1. 🔄 Sistema completo de memória histórica
2. 🔄 NLP para análise de similaridade
3. 🔄 Dashboard de diversidade
4. 🔄 API de sugestões de nomes

## 💡 Conclusão

O problema de repetição do "Blackwood" é causado pela ausência de instruções específicas de diversidade nos prompts e falta de sistema de memória histórica. As soluções propostas garantirão:

- ✅ **Eliminação** da repetição de nomes
- ✅ **Diversidade** narrativa aumentada
- ✅ **Qualidade** de conteúdo melhorada
- ✅ **Escalabilidade** do sistema

A implementação em fases permitirá correção imediata do problema com evolução gradual para um sistema robusto de anti-repetição.