# 🎯 GUIA COMPLETO DE IMPLEMENTAÇÃO - PROMPTS ESPECÍFICOS DE AGENTES PARA PREMISSAS

## 📋 VISÃO GERAL

Este guia detalha a implementação completa para integrar prompts específicos de agentes na geração de premissas, mantendo o sistema atual do agente milionário intacto e expandindo para outros agentes.

## 🔍 ANÁLISE DO SISTEMA ATUAL

### Estado Atual - Agente Milionário
✅ **JÁ IMPLEMENTADO E FUNCIONANDO**
- Prompt específico: "Histórias de Milionários - Premissas - narrative"
- Localização: Sistema de prompts configuráveis
- Funcionalidade: Gera premissas com contraste social e descoberta emocional
- **NÃO REQUER ALTERAÇÃO** - apenas opção de melhoria se necessário

### Fluxo Atual de Geração
```
1. Usuário seleciona agente "Histórias de Milionários"
2. Sistema usa get_default_premise_prompt() (genérico)
3. PromptVariator aplica contexto específico pós-geração
4. Resultado: Inconsistência entre prompt inicial e refinamento
```

### Problema Identificado
- **Prompt inicial genérico** não aproveita especialização do agente
- **Pós-processamento** tenta corrigir, mas é menos eficiente
- **Inconsistências** como "Arthur Blackwood" surgem dessa desconexão

## 🎯 OBJETIVOS DA IMPLEMENTAÇÃO

### Primários
1. **Integrar prompts específicos** na geração inicial de premissas
2. **Manter compatibilidade** com agente milionário existente
3. **Expandir sistema** para outros agentes (romance, horror, etc.)
4. **Eliminar inconsistências** de nomes e contextos

### Secundários
1. **Melhorar performance** (menos pós-processamento)
2. **Facilitar manutenção** (prompts centralizados)
3. **Expandir escalabilidade** (novos agentes facilmente)

## 🏗️ ARQUITETURA DA SOLUÇÃO

### Componentes Principais

#### 1. **AgentPromptManager** (Novo)
```python
class AgentPromptManager:
    """Gerencia prompts específicos por agente"""
    
    def get_premise_prompt(self, agent_type: str, style: str = 'narrative') -> str:
        """Retorna prompt específico do agente ou fallback padrão"""
    
    def has_agent_prompt(self, agent_type: str, style: str = 'narrative') -> bool:
        """Verifica se agente possui prompt específico"""
```

#### 2. **Modificação em premise.py**
```python
def get_premise_prompt_for_agent(agent_type: str = None, style: str = 'narrative') -> str:
    """Retorna prompt específico do agente ou padrão do sistema"""
    
    if agent_type:
        agent_prompt = AgentPromptManager().get_premise_prompt(agent_type, style)
        if agent_prompt:
            return agent_prompt
    
    return get_default_premise_prompt()
```

#### 3. **Integração com PromptVariator**
- Manter sistema atual de nomes específicos
- Reduzir pós-processamento (prompt já é específico)
- Focar em anti-repetição e variação

## 📝 IMPLEMENTAÇÃO DETALHADA

### ETAPA 1: Criar AgentPromptManager

#### Arquivo: `backend/services/agent_prompt_manager.py`
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerenciador de Prompts Específicos por Agente
"""

from typing import Optional, Dict
import logging

class AgentPromptManager:
    """Gerencia prompts específicos para cada tipo de agente"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._load_agent_prompts()
    
    def _load_agent_prompts(self):
        """Carrega prompts específicos de cada agente"""
        self.agent_prompts = {
            'millionaire_stories': {
                'narrative': self._get_millionaire_narrative_prompt(),
                'educational': self._get_millionaire_educational_prompt()
            },
            'romance_agent': {
                'narrative': self._get_romance_narrative_prompt(),
                'educational': self._get_romance_educational_prompt()
            },
            'horror_agent': {
                'narrative': self._get_horror_narrative_prompt(),
                'educational': self._get_horror_educational_prompt()
            },
            'motivational_agent': {
                'narrative': self._get_motivational_narrative_prompt(),
                'educational': self._get_motivational_educational_prompt()
            }
        }
    
    def get_premise_prompt(self, agent_type: str, style: str = 'narrative') -> Optional[str]:
        """Retorna prompt específico do agente"""
        try:
            return self.agent_prompts.get(agent_type, {}).get(style)
        except Exception as e:
            self.logger.error(f"Erro ao obter prompt do agente {agent_type}: {e}")
            return None
    
    def has_agent_prompt(self, agent_type: str, style: str = 'narrative') -> bool:
        """Verifica se agente possui prompt específico"""
        return bool(self.get_premise_prompt(agent_type, style))
    
    def _get_millionaire_narrative_prompt(self) -> str:
        """Prompt narrativo para histórias de milionários (EXISTENTE - NÃO ALTERAR)"""
        return """
Crie uma premissa narrativa para história de milionário sobre: {title}.

A premissa deve incluir:
- Personagem milionário/rico com vida aparentemente perfeita
- Personagem de classe baixa com qualidades humanas especiais
- Situação que os conecta (trabalho, acaso, família)
- Descoberta emocional que muda perspectivas
- Contraste entre riqueza material e riqueza humana
- Aproximadamente {word_count} palavras
- Não repita nomes que foram gerados e nem premissas que foram geradas anteriormente
- Crie nomes específicos para cada história e nunca repita nomes que já foram usados em roteiros passados

Use variáveis como {titulo}, {premissa}, {resumos[i-2]} para conteúdo dinâmico.
"""
    
    def _get_millionaire_educational_prompt(self) -> str:
        """Prompt educacional para histórias de milionários"""
        return """
Crie uma premissa educacional sobre sucesso financeiro baseada em: {title}.

A premissa deve incluir:
- Lições práticas de empreendedorismo
- Estratégias de investimento e gestão financeira
- Mindset de crescimento e superação
- Exemplos reais de transformação financeira
- Aproximadamente {word_count} palavras
- Foco em aprendizado e aplicação prática

Use variáveis como {titulo}, {premissa} para conteúdo dinâmico.
"""
    
    def _get_romance_narrative_prompt(self) -> str:
        """Prompt narrativo para histórias românticas"""
        return """
Crie uma premissa romântica envolvente baseada em: {title}.

A premissa deve incluir:
- Dois protagonistas com personalidades complementares
- Conflito inicial que os separa ou aproxima
- Desenvolvimento emocional gradual
- Obstáculos ao relacionamento
- Resolução satisfatória e esperançosa
- Aproximadamente {word_count} palavras
- Nomes únicos e memoráveis para os personagens

Use variáveis como {titulo}, {premissa} para conteúdo dinâmico.
"""
    
    def _get_horror_narrative_prompt(self) -> str:
        """Prompt narrativo para histórias de terror"""
        return """
Crie uma premissa de terror psicológico baseada em: {title}.

A premissa deve incluir:
- Protagonista em situação aparentemente normal
- Elemento sobrenatural ou psicológico perturbador
- Escalada gradual de tensão e medo
- Atmosfera sombria e opressiva
- Clímax aterrorizante com resolução ambígua
- Aproximadamente {word_count} palavras
- Nomes que evoquem mistério e inquietação

Use variáveis como {titulo}, {premissa} para conteúdo dinâmico.
"""
    
    # Implementar métodos similares para outros agentes...
```

### ETAPA 2: Modificar premise.py

#### Alterações em `backend/routes/premise.py`
```python
# Adicionar import
from services.agent_prompt_manager import AgentPromptManager

# Criar instância global
agent_prompt_manager = AgentPromptManager()

def get_premise_prompt_for_agent(agent_type: str = None, style: str = 'narrative') -> str:
    """Retorna prompt específico do agente ou padrão do sistema"""
    
    if agent_type:
        agent_prompt = agent_prompt_manager.get_premise_prompt(agent_type, style)
        if agent_prompt:
            logging.info(f"Usando prompt específico do agente {agent_type} - {style}")
            return agent_prompt
        else:
            logging.info(f"Prompt específico não encontrado para {agent_type}, usando padrão")
    
    logging.info("Usando prompt padrão do sistema")
    return get_default_premise_prompt()

# Modificar rota /generate
@premise_bp.route('/generate', methods=['POST'])
def generate_premise():
    try:
        data = request.get_json()
        titles = data.get('titles', [])
        agent_type = data.get('agent')  # Obter agente da requisição
        style = data.get('style', 'narrative')  # Obter estilo (narrative/educational)
        
        # ... código existente ...
        
        # USAR PROMPT ESPECÍFICO DO AGENTE
        prompt = get_premise_prompt_for_agent(agent_type, style)
        
        # ... resto da implementação ...
```

### ETAPA 3: Atualizar Pipeline Service

#### Modificações em `backend/services/pipeline_service.py`
```python
# Na função de geração de premissas
def generate_premises_stage(self, titles: List[str], config: Dict) -> Dict:
    """Gera premissas usando prompt específico do agente"""
    
    agent_type = config.get('agent')
    style = config.get('premise_style', 'narrative')
    
    # Usar prompt específico do agente
    from routes.premise import get_premise_prompt_for_agent
    prompt = get_premise_prompt_for_agent(agent_type, style)
    
    # ... resto da implementação ...
```

### ETAPA 4: Integração com Frontend

#### Modificações em componentes React
```javascript
// Adicionar seletor de estilo de premissa
const PremiseStyleSelector = ({ value, onChange, agentType }) => {
  const styles = {
    'millionaire_stories': ['narrative', 'educational'],
    'romance_agent': ['narrative', 'educational'],
    'horror_agent': ['narrative'],
    'motivational_agent': ['narrative', 'educational']
  };
  
  const availableStyles = styles[agentType] || ['narrative'];
  
  return (
    <select value={value} onChange={onChange}>
      {availableStyles.map(style => (
        <option key={style} value={style}>
          {style === 'narrative' ? 'Narrativa' : 'Educacional'}
        </option>
      ))}
    </select>
  );
};
```

## 🧪 TESTES E VALIDAÇÃO

### Testes Unitários
```python
# backend/tests/test_agent_prompt_manager.py
import pytest
from services.agent_prompt_manager import AgentPromptManager

class TestAgentPromptManager:
    def setup_method(self):
        self.manager = AgentPromptManager()
    
    def test_millionaire_narrative_prompt(self):
        prompt = self.manager.get_premise_prompt('millionaire_stories', 'narrative')
        assert prompt is not None
        assert 'milionário' in prompt.lower()
        assert 'classe baixa' in prompt.lower()
    
    def test_fallback_to_default(self):
        prompt = self.manager.get_premise_prompt('nonexistent_agent')
        assert prompt is None
    
    def test_has_agent_prompt(self):
        assert self.manager.has_agent_prompt('millionaire_stories', 'narrative')
        assert not self.manager.has_agent_prompt('nonexistent_agent')
```

### Testes de Integração
```python
# backend/tests/test_premise_integration.py
def test_premise_generation_with_agent():
    """Testa geração de premissa com agente específico"""
    
    response = client.post('/api/premise/generate', json={
        'titles': ['Milionário Descobre Verdade Chocante'],
        'agent': 'millionaire_stories',
        'style': 'narrative'
    })
    
    assert response.status_code == 200
    data = response.get_json()
    
    # Verificar se premissa contém elementos específicos do agente
    premise = data['premises'][0]['premise']
    assert any(keyword in premise.lower() for keyword in 
              ['milionário', 'rico', 'classe baixa', 'descoberta'])
```

## 🚀 PLANO DE ROLLOUT

### Fase 1: Implementação Base (Semana 1)
- [ ] Criar AgentPromptManager
- [ ] Modificar premise.py para usar prompts específicos
- [ ] Testes unitários básicos
- [ ] Validação com agente milionário existente

### Fase 2: Expansão de Agentes (Semana 2)
- [ ] Implementar prompts para romance_agent
- [ ] Implementar prompts para horror_agent
- [ ] Implementar prompts para motivational_agent
- [ ] Testes de integração

### Fase 3: Interface e UX (Semana 3)
- [ ] Atualizar frontend para seleção de estilo
- [ ] Indicadores visuais de prompt utilizado
- [ ] Documentação de usuário
- [ ] Testes end-to-end

### Fase 4: Otimização e Monitoramento (Semana 4)
- [ ] Cache de prompts
- [ ] Métricas de performance
- [ ] Logs detalhados
- [ ] Ajustes baseados em feedback

## ⚠️ RISCOS E MITIGAÇÕES

### Risco 1: Quebra do Sistema Existente
**Mitigação:**
- Manter get_default_premise_prompt() como fallback
- Testes extensivos antes do deploy
- Rollback plan preparado

### Risco 2: Inconsistência de Prompts
**Mitigação:**
- Validação automática de prompts
- Templates padronizados
- Revisão manual de novos prompts

### Risco 3: Performance Degradada
**Mitigação:**
- Cache de prompts carregados
- Lazy loading de AgentPromptManager
- Monitoramento de tempo de resposta

### Risco 4: Manutenção Complexa
**Mitigação:**
- Documentação detalhada
- Testes automatizados
- Interface administrativa para prompts

## 📊 MÉTRICAS DE SUCESSO

### Técnicas
- ✅ Tempo de resposta < 2s para geração de premissas
- ✅ 0% de erros na aplicação de prompts específicos
- ✅ 100% de cobertura de testes para novos componentes

### Qualitativas
- ✅ Eliminação de nomes repetitivos (ex: Arthur Blackwood)
- ✅ Maior relevância das premissas ao agente selecionado
- ✅ Feedback positivo dos usuários

### Operacionais
- ✅ Deploy sem downtime
- ✅ Rollback em < 5 minutos se necessário
- ✅ Logs claros para debugging

## 🔧 CONFIGURAÇÃO E DEPLOYMENT

### Variáveis de Ambiente
```bash
# .env
AGENT_PROMPTS_CACHE_TTL=3600  # Cache de prompts em segundos
AGENT_PROMPTS_DEBUG=false     # Logs detalhados de prompts
AGENT_PROMPTS_FALLBACK=true   # Usar fallback em caso de erro
```

### Scripts de Deploy
```bash
#!/bin/bash
# deploy_agent_prompts.sh

echo "🚀 Iniciando deploy do sistema de prompts de agentes..."

# Backup do sistema atual
cp backend/routes/premise.py backend/routes/premise.py.backup

# Executar testes
python -m pytest backend/tests/test_agent_prompt_manager.py -v

if [ $? -eq 0 ]; then
    echo "✅ Testes passaram, continuando deploy..."
    # Restart do serviço
    systemctl restart auto-video-producer
else
    echo "❌ Testes falharam, abortando deploy"
    exit 1
fi
```

## 📚 DOCUMENTAÇÃO ADICIONAL

### Para Desenvolvedores
- **API Reference**: Documentação completa da AgentPromptManager
- **Prompt Guidelines**: Padrões para criação de novos prompts
- **Testing Guide**: Como testar prompts específicos

### Para Usuários
- **User Manual**: Como selecionar agentes e estilos
- **Best Practices**: Dicas para melhores resultados
- **Troubleshooting**: Solução de problemas comuns

## 🎯 CONCLUSÃO

Esta implementação resolve definitivamente:
1. ✅ **Inconsistências de nomes** (Arthur Blackwood eliminado)
2. ✅ **Relevância das premissas** (prompts específicos por agente)
3. ✅ **Escalabilidade** (fácil adição de novos agentes)
4. ✅ **Manutenibilidade** (código organizado e testado)
5. ✅ **Performance** (menos pós-processamento necessário)

O sistema mantém total compatibilidade com o agente milionário existente enquanto expande as capacidades para outros agentes de forma robusta e escalável.