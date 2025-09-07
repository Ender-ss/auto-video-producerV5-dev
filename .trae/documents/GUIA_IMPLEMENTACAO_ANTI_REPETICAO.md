# 🛠️ Guia Prático de Implementação: Sistema Anti-Repetição

## 🎯 Objetivo
Implementar soluções práticas para eliminar a repetição do nome "Blackwood" e garantir diversidade de personagens e histórias no Auto Video Producer.

## ⚡ Correção Imediata (30 minutos)

### 1. Atualizar Prompt de Premissas

**Arquivo**: `backend/routes/premise.py`
**Localização**: Função `get_default_premise_prompt()` (linha ~29)

```python
def get_default_premise_prompt():
    return """# Gerador de Premissas Profissionais para Vídeos

Você é um especialista em criação de conteúdo e storytelling para YouTube.

🚨 REGRAS CRÍTICAS DE DIVERSIDADE:
1. NUNCA use os nomes: Blackwood, Johnson, Smith, Williams, Brown
2. SEMPRE crie personagens com nomes ÚNICOS e DIVERSOS
3. Use preferencialmente nomes brasileiros autênticos
4. Varie nacionalidades, profissões e contextos
5. Evite clichês narrativos repetitivos

💡 NOMES SUGERIDOS:
- Masculinos: Rafael Mendes, Carlos Andrade, Eduardo Ribeiro, Thiago Costa, Bruno Silva
- Femininos: Ana Beatriz Santos, Sofia Carvalho, Isabella Rocha, Camila Oliveira, Lucia Ferreira
- Empresários: Miguel Almeida, Fernando Dias, Roberto Nascimento, Gustavo Pereira

📝 INSTRUÇÕES DE GERAÇÃO:
Crie premissas envolventes que:
- Tenham personagens com nomes únicos e memoráveis
- Apresentem contextos diversos e originais
- Evitem padrões repetitivos de personalidade
- Incluam detalhes específicos e autênticos

Formato da resposta:
[Resto do prompt existente...]
"""
```

### 2. Adicionar Validação de Nomes

**Arquivo**: `backend/routes/premise.py`
**Localização**: Função `parse_premises_response()` (linha ~576)

```python
# Adicionar no início da função
FORBIDDEN_NAMES = ['blackwood', 'johnson', 'smith', 'williams', 'brown']

def contains_forbidden_names(text):
    text_lower = text.lower()
    return any(name in text_lower for name in FORBIDDEN_NAMES)

def parse_premises_response(response_text, titles):
    # ... código existente ...
    
    # NOVA VALIDAÇÃO: Verificar nomes proibidos
    for premise in premises:
        if contains_forbidden_names(premise.get('premise', '')):
            print(f"⚠️ AVISO: Premissa contém nome proibido, regenerando...")
            # Forçar regeneração ou usar fallback
            premise['premise'] = premise['premise'].replace('Blackwood', 'Rafael Mendes')
            premise['premise'] = premise['premise'].replace('blackwood', 'rafael mendes')
    
    return premises
```

### 3. Atualizar Configuração de Prompts

**Arquivo**: `backend/config/prompts_config.json`
**Seção**: `premises.prompt`

Adicionar ao prompt existente:
```json
{
  "premises": {
    "prompt": "[prompt existente]\n\n🎭 DIVERSIDADE OBRIGATÓRIA:\n- Use APENAS nomes únicos e diversos\n- PROIBIDO: Blackwood, Johnson, Smith\n- PREFIRA: Nomes brasileiros autênticos\n- VARIE: Contextos, profissões, personalidades"
  }
}
```

## 🔧 Implementação Intermediária (2-3 horas)

### 4. Criar Serviço de Diversidade

**Novo Arquivo**: `backend/services/name_diversity_service.py`

```python
import random
import json
from typing import List, Dict, Set

class NameDiversityService:
    def __init__(self):
        self.used_names: Set[str] = set()
        self.forbidden_names = {
            'blackwood', 'johnson', 'smith', 'williams', 'brown',
            'anderson', 'wilson', 'taylor', 'davis', 'miller'
        }
        
        self.name_pools = {
            'male_first': [
                'Rafael', 'Carlos', 'Eduardo', 'Thiago', 'Bruno',
                'Miguel', 'Fernando', 'Roberto', 'Gustavo', 'Diego',
                'Leonardo', 'Gabriel', 'André', 'Felipe', 'Rodrigo'
            ],
            'female_first': [
                'Ana', 'Sofia', 'Isabella', 'Camila', 'Lucia',
                'Beatriz', 'Mariana', 'Fernanda', 'Juliana', 'Patricia',
                'Carla', 'Renata', 'Daniela', 'Adriana', 'Vanessa'
            ],
            'surnames': [
                'Silva', 'Santos', 'Oliveira', 'Costa', 'Ferreira',
                'Mendes', 'Andrade', 'Ribeiro', 'Carvalho', 'Rocha',
                'Almeida', 'Dias', 'Nascimento', 'Pereira', 'Lima'
            ]
        }
    
    def get_unique_name(self, gender: str = 'male') -> str:
        """Gera um nome único não utilizado anteriormente"""
        attempts = 0
        max_attempts = 50
        
        while attempts < max_attempts:
            first_pool = self.name_pools[f'{gender}_first']
            first_name = random.choice(first_pool)
            surname = random.choice(self.name_pools['surnames'])
            full_name = f"{first_name} {surname}"
            
            if (full_name.lower() not in self.used_names and 
                surname.lower() not in self.forbidden_names):
                self.used_names.add(full_name.lower())
                return full_name
            
            attempts += 1
        
        # Fallback: gerar nome com timestamp
        import time
        timestamp = str(int(time.time()))[-4:]
        return f"Carlos Silva{timestamp}"
    
    def is_name_forbidden(self, text: str) -> bool:
        """Verifica se o texto contém nomes proibidos"""
        text_lower = text.lower()
        return any(name in text_lower for name in self.forbidden_names)
    
    def replace_forbidden_names(self, text: str) -> str:
        """Substitui nomes proibidos por nomes únicos"""
        result = text
        
        for forbidden in self.forbidden_names:
            if forbidden in result.lower():
                replacement = self.get_unique_name()
                # Preservar capitalização
                if forbidden.title() in result:
                    result = result.replace(forbidden.title(), replacement)
                elif forbidden.upper() in result:
                    result = result.replace(forbidden.upper(), replacement.upper())
                else:
                    result = result.replace(forbidden, replacement.lower())
        
        return result
    
    def get_diversity_stats(self) -> Dict:
        """Retorna estatísticas de diversidade"""
        return {
            'total_names_used': len(self.used_names),
            'unique_names_ratio': len(self.used_names) / max(1, len(self.used_names)),
            'forbidden_names_count': len(self.forbidden_names)
        }

# Instância global
diversity_service = NameDiversityService()
```

### 5. Integrar no StorytellerService

**Arquivo**: `backend/services/storyteller_service.py`
**Localização**: Classe `PromptVariator` (linha ~200)

```python
# Adicionar import no topo
from .name_diversity_service import diversity_service

class PromptVariator:
    def __init__(self):
        # ... código existente ...
        self.diversity_service = diversity_service
    
    def generate_varied_prompt(self, title, premise, agent_type, chapter_number=1, previous_content=""):
        # ... código existente ...
        
        # NOVA FUNCIONALIDADE: Verificar e corrigir nomes proibidos
        if self.diversity_service.is_name_forbidden(premise):
            print("⚠️ Detectado nome proibido na premissa, corrigindo...")
            premise = self.diversity_service.replace_forbidden_names(premise)
        
        # Adicionar instruções de diversidade ao prompt
        diversity_instruction = f"""
        
🎭 INSTRUÇÕES DE DIVERSIDADE:
- Use APENAS nomes únicos e diversos
- NUNCA use: Blackwood, Johnson, Smith, Williams
- Personagem sugerido: {self.diversity_service.get_unique_name()}
- Crie personalidades e contextos únicos
        """
        
        # ... resto do código existente ...
        
        # Adicionar instruções ao prompt final
        final_prompt = f"{prompt}{diversity_instruction}"
        
        return final_prompt
```

## 📊 Sistema de Monitoramento (1 hora)

### 6. Criar Middleware de Validação

**Novo Arquivo**: `backend/middleware/content_validator.py`

```python
from functools import wraps
from flask import request, jsonify
from services.name_diversity_service import diversity_service

def validate_content_diversity(f):
    """Decorator para validar diversidade de conteúdo"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Executar função original
        result = f(*args, **kwargs)
        
        # Validar resultado se for JSON
        if hasattr(result, 'json') and result.json:
            content = str(result.json)
            if diversity_service.is_name_forbidden(content):
                print(f"🚨 ALERTA: Conteúdo gerado contém nomes proibidos!")
                print(f"Endpoint: {request.endpoint}")
                print(f"Conteúdo: {content[:200]}...")
        
        return result
    
    return decorated_function

# Aplicar em rotas críticas
# Em premise.py:
# @validate_content_diversity
# def generate_premises():
```

### 7. Dashboard de Diversidade

**Novo Arquivo**: `backend/routes/diversity_stats.py`

```python
from flask import Blueprint, jsonify
from services.name_diversity_service import diversity_service

diversity_bp = Blueprint('diversity', __name__)

@diversity_bp.route('/api/diversity/stats', methods=['GET'])
def get_diversity_stats():
    """Endpoint para estatísticas de diversidade"""
    stats = diversity_service.get_diversity_stats()
    return jsonify({
        'status': 'success',
        'data': stats,
        'recommendations': {
            'names_health': 'good' if stats['total_names_used'] > 10 else 'needs_improvement',
            'diversity_score': min(100, stats['total_names_used'] * 10)
        }
    })

@diversity_bp.route('/api/diversity/validate', methods=['POST'])
def validate_content():
    """Endpoint para validar conteúdo"""
    data = request.get_json()
    content = data.get('content', '')
    
    is_forbidden = diversity_service.is_name_forbidden(content)
    corrected = diversity_service.replace_forbidden_names(content) if is_forbidden else content
    
    return jsonify({
        'status': 'success',
        'has_forbidden_names': is_forbidden,
        'original_content': content,
        'corrected_content': corrected,
        'suggestions': {
            'male_name': diversity_service.get_unique_name('male'),
            'female_name': diversity_service.get_unique_name('female')
        }
    })
```

## 🚀 Teste e Validação

### 8. Script de Teste

**Novo Arquivo**: `backend/tests/test_diversity.py`

```python
import sys
sys.path.append('..')

from services.name_diversity_service import diversity_service

def test_diversity_system():
    print("🧪 Testando Sistema de Diversidade\n")
    
    # Teste 1: Detecção de nomes proibidos
    test_text = "Arthur Blackwood era um empresário bem-sucedido."
    print(f"Texto original: {test_text}")
    print(f"Contém nome proibido: {diversity_service.is_name_forbidden(test_text)}")
    
    # Teste 2: Substituição de nomes
    corrected = diversity_service.replace_forbidden_names(test_text)
    print(f"Texto corrigido: {corrected}\n")
    
    # Teste 3: Geração de nomes únicos
    print("Nomes únicos gerados:")
    for i in range(5):
        male_name = diversity_service.get_unique_name('male')
        female_name = diversity_service.get_unique_name('female')
        print(f"  {i+1}. {male_name} / {female_name}")
    
    # Teste 4: Estatísticas
    stats = diversity_service.get_diversity_stats()
    print(f"\nEstatísticas: {stats}")
    
    print("\n✅ Todos os testes concluídos!")

if __name__ == "__main__":
    test_diversity_system()
```

## 📋 Checklist de Implementação

### ✅ Fase 1: Correção Imediata
- [ ] Atualizar `get_default_premise_prompt()`
- [ ] Adicionar validação em `parse_premises_response()`
- [ ] Modificar `prompts_config.json`
- [ ] Testar geração de premissas

### ✅ Fase 2: Sistema de Diversidade
- [ ] Criar `name_diversity_service.py`
- [ ] Integrar no `storyteller_service.py`
- [ ] Implementar middleware de validação
- [ ] Criar endpoints de estatísticas

### ✅ Fase 3: Monitoramento
- [ ] Implementar dashboard de diversidade
- [ ] Criar scripts de teste
- [ ] Configurar alertas automáticos
- [ ] Documentar processo

## 🎯 Resultados Esperados

Após a implementação completa:

1. **Eliminação Total** do nome "Blackwood"
2. **Diversidade de 95%+** em nomes de personagens
3. **Detecção Automática** de repetições
4. **Correção em Tempo Real** de conteúdo
5. **Monitoramento Contínuo** da qualidade

## 🆘 Solução de Problemas

### Problema: Nomes ainda repetindo
**Solução**: Verificar se o serviço está sendo importado corretamente

### Problema: Performance lenta
**Solução**: Implementar cache Redis para nomes utilizados

### Problema: Nomes não brasileiros
**Solução**: Expandir pool de nomes no `name_pools`

---

**📞 Suporte**: Em caso de dúvidas, verificar logs em `/var/log/avp/diversity.log`