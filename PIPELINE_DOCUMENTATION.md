# 🎬 Documentação Completa da Pipeline - Auto Video Producer

## 📋 Índice

1. [Visão Geral da Pipeline](#visão-geral-da-pipeline)
2. [Arquitetura do Sistema](#arquitetura-do-sistema)
3. [Componentes Backend](#componentes-backend)
4. [Componentes Frontend](#componentes-frontend)
5. [Fluxo Detalhado da Pipeline](#fluxo-detalhado-da-pipeline)
6. [Diagnóstico e Troubleshooting](#diagnóstico-e-troubleshooting)
7. [Configurações e Dependências](#configurações-e-dependências)

---

## 🎯 Visão Geral da Pipeline

O Auto Video Producer é um sistema automatizado de criação de vídeos que processa conteúdo do YouTube através de uma pipeline completa, desde a extração até a geração do vídeo final.

### Estados da Pipeline
- **pending**: Aguardando início
- **running**: Em execução
- **completed**: Concluída com sucesso
- **failed**: Falhou durante execução
- **cancelled**: Cancelada pelo usuário

### Etapas Principais
1. **Extração** - Coleta de dados do YouTube
2. **Geração de Títulos** - Criação de títulos virais
3. **Geração de Premissa** - Criação da premissa do vídeo
4. **Geração de Roteiro** - Criação do script detalhado
5. **Geração de Áudio (TTS)** - Conversão texto para fala
6. **Geração de Imagens** - Criação de imagens para o vídeo
7. **Criação de Vídeo** - Montagem final do vídeo

---

## 🏗️ Arquitetura do Sistema

### Backend (Python/Flask)
```
backend/
├── app.py                 # Aplicação principal Flask
├── routes/
│   ├── automations.py     # Rotas de automação
│   ├── images.py          # Rotas de geração de imagens
│   ├── videos.py          # Rotas de gerenciamento de vídeos
│   ├── scripts.py         # Rotas de geração de roteiros
│   └── pipeline_complete.py # Pipeline completa
├── services/
│   ├── pipeline_service.py      # Serviço principal da pipeline
│   ├── video_creation_service.py # Criação de vídeos
│   ├── storyteller_service.py   # Geração de roteiros
│   ├── tts_service.py           # Text-to-Speech
│   └── title_generator.py       # Geração de títulos
└── temp/                  # Arquivos temporários
```

### Frontend (React/Vite)
```
frontend/
├── src/
│   ├── pages/
│   │   ├── Dashboard.jsx          # Dashboard principal
│   │   ├── Pipeline.jsx           # Monitoramento da pipeline
│   │   ├── ConteudosGerados.jsx   # Conteúdos gerados
│   │   └── Settings.jsx           # Configurações
│   ├── components/
│   │   ├── PipelineProgress.jsx   # Progresso da pipeline
│   │   ├── AutomationCompleteForm.jsx # Formulário de automação
│   │   ├── VideoPreview.jsx       # Preview de vídeos
│   │   └── ImageGenerationStep.jsx # Geração de imagens
│   └── App.jsx            # Componente principal
```

---

## 🔧 Componentes Backend

### 1. Extração de Dados (YouTube)

**Arquivo**: `routes/automations.py`
**Função**: `extract_youtube_data()`

**Funcionalidades**:
- Extração de metadados de canais YouTube
- Coleta de títulos de vídeos
- Análise de padrões virais
- Suporte a múltiplos formatos de URL

**Dependências**:
- `yt-dlp`: Extração de dados do YouTube
- `requests`: Requisições HTTP

**Processo**:
1. Valida URL do canal
2. Extrai informações do canal
3. Coleta títulos dos vídeos
4. Analisa padrões de engagement
5. Retorna dados estruturados

**Possíveis Problemas**:
- Rate limiting do YouTube
- URLs inválidas
- Canais privados/inexistentes
- Problemas de conectividade

### 2. Geração de Títulos

**Arquivo**: `services/title_generator.py`
**Classe**: `TitleGenerator`

**Provedores Suportados**:
- **OpenAI**: GPT-3.5/GPT-4
- **Google Gemini**: gemini-1.5-flash/pro
- **OpenRouter**: Claude, Llama, etc.

**Funcionalidades**:
- Análise de padrões virais
- Geração de títulos personalizados
- Scoring de qualidade
- Prompts customizáveis

**Processo**:
1. Analisa títulos de referência
2. Identifica padrões virais
3. Gera prompts otimizados
4. Chama API da IA escolhida
5. Processa e pontua resultados

**Configurações**:
```python
{
    'provider': 'gemini|openai|openrouter',
    'model': 'modelo_específico',
    'count': 10,  # Número de títulos
    'style': 'viral|educational|entertainment'
}
```

### 3. Geração de Premissa

**Arquivo**: `routes/automations.py`
**Função**: `generate_premise()`

**Funcionalidades**:
- Criação de premissas baseadas em títulos
- Análise de contexto
- Otimização para engajamento

**Processo**:
1. Recebe título selecionado
2. Analisa contexto do canal
3. Gera premissa estruturada
4. Valida coerência

### 4. Geração de Roteiro

**Arquivo**: `services/storyteller_service.py`
**Classe**: `StorytellerService`

**Características**:
- **Pipeline de 3 prompts** para qualidade
- **Detecção de repetições** inteligente
- **Quebra inteligente de capítulos**
- **Validação de conteúdo**
- **Cache Redis** para otimização

**Agentes Disponíveis**:
- `storyteller`: Narrativas envolventes
- `educational`: Conteúdo educativo
- `viral`: Foco em viralização

**Processo Detalhado**:
1. **Prompt 1**: Estrutura inicial
2. **Prompt 2**: Desenvolvimento e detalhamento
3. **Prompt 3**: Refinamento e polimento
4. **Validação**: Verificação de qualidade
5. **Formatação**: Estruturação final

**Classes Auxiliares**:
- `RepetitionDetector`: Detecta conteúdo repetitivo
- `SmartChapterBreaker`: Quebra inteligente de capítulos
- `StoryValidator`: Validação de qualidade
- `TokenChunker`: Gerenciamento de tokens

### 5. Geração de Áudio (TTS)

**Arquivo**: `services/tts_service.py`
**Classe**: `TTSService`

**Provedores Suportados**:
- **Google Gemini TTS**: Vozes naturais
- **ElevenLabs**: Vozes premium
- **Kokoro**: Vozes sintéticas

**Funcionalidades**:
- Segmentação inteligente de texto
- Sincronização com vídeo
- Controle de qualidade
- Múltiplos formatos de saída

**Processo**:
1. Segmenta texto em chunks
2. Gera áudio para cada segmento
3. Sincroniza timing
4. Combina segmentos
5. Otimiza qualidade final

**Configurações de Voz**:
```python
{
    'provider': 'gemini|elevenlabs|kokoro',
    'voice_id': 'id_da_voz',
    'speed': 1.0,
    'pitch': 0,
    'stability': 0.5,
    'clarity': 0.75
}
```

### 6. Geração de Imagens

**Arquivo**: `routes/images.py`
**Blueprint**: `images_bp`

**Provedores Suportados**:
- **Together AI**: Modelos diversos
- **Google Gemini**: Imagen
- **Pollinations**: Gratuito

**Funcionalidades**:
- Geração baseada em roteiro
- Prompts personalizados
- IA Agent para prompts automáticos
- Distribuição uniforme de cenas

**Processo**:
1. Analisa roteiro
2. Identifica cenas-chave
3. Gera prompts visuais
4. Cria imagens via API
5. Otimiza para vídeo

**Configurações**:
```python
{
    'provider': 'together|gemini|pollinations',
    'model': 'modelo_específico',
    'style': 'realistic|cartoon|artistic',
    'format': 'landscape|portrait|square',
    'quality': 'standard|hd|ultra'
}
```

### 7. Criação de Vídeo

**Arquivo**: `services/video_creation_service.py`
**Classe**: `VideoCreationService`

**Dependências**:
- **MoviePy**: Edição de vídeo
- **PIL**: Processamento de imagens
- **FFmpeg**: Codificação

**Funcionalidades**:
- Sincronização áudio/vídeo
- Transições suaves
- Legendas automáticas
- Múltiplas resoluções
- Efeitos visuais

**Processo**:
1. Carrega áudio e imagens
2. Sincroniza timing
3. Aplica transições
4. Adiciona legendas
5. Renderiza vídeo final

**Configurações de Vídeo**:
```python
{
    'resolution': '1920x1080|1280x720|3840x2160',
    'fps': 30,
    'quality': 'high|medium|low',
    'transitions': True,
    'subtitles': True
}
```

### 8. Pipeline Service (Orquestrador)

**Arquivo**: `services/pipeline_service.py`
**Classe**: `PipelineService`

**Responsabilidades**:
- Coordenação de todas as etapas
- Gerenciamento de estado
- Tratamento de erros
- Logging detalhado
- Cleanup de recursos

**Estados Gerenciados**:
- Progresso de cada etapa
- Logs de execução
- Resultados intermediários
- Configurações ativas

---

## 🎨 Componentes Frontend

### 1. Dashboard Principal

**Arquivo**: `pages/Dashboard.jsx`

**Funcionalidades**:
- Visão geral do sistema
- Pipelines ativas
- Estatísticas em tempo real
- Status das APIs
- Ações rápidas

**Componentes**:
- Cards de estatísticas
- Lista de pipelines ativas
- Indicadores de status
- Botões de ação rápida

### 2. Monitoramento da Pipeline

**Arquivo**: `pages/Pipeline.jsx`

**Funcionalidades**:
- Monitoramento em tempo real
- Logs detalhados
- Controle de execução
- Visualização de resultados

**Componentes Principais**:
- `PipelineProgress`: Barra de progresso
- `AutomationCompleteForm`: Formulário de configuração
- `VideoPreview`: Preview dos vídeos
- `ImageGenerationStep`: Geração de imagens

### 3. Formulário de Automação

**Arquivo**: `components/AutomationCompleteForm.jsx`

**Funcionalidades**:
- Configuração completa da pipeline
- Gerenciamento de canais salvos
- Prompts personalizados
- Validação de entrada

**Seções**:
- Configuração do canal
- Configuração de IA
- Configuração de TTS
- Configuração de imagens
- Configuração de vídeo

### 4. Progresso da Pipeline

**Arquivo**: `components/PipelineProgress.jsx`

**Funcionalidades**:
- Visualização de etapas
- Logs em tempo real
- Indicadores de status
- Resultados parciais

**Estados Visuais**:
- ✅ Concluído
- 🔄 Em progresso
- ⏳ Aguardando
- ❌ Erro

### 5. Gerenciamento de Conteúdo

**Arquivo**: `pages/ConteudosGerados.jsx`

**Funcionalidades**:
- Biblioteca de conteúdos
- Preview de vídeos
- Download de arquivos
- Organização por data

---

## 🔄 Fluxo Detalhado da Pipeline

### Fase 1: Inicialização
```
1. Usuário configura pipeline no frontend
2. Frontend envia requisição para /api/pipeline/complete
3. Backend valida configurações
4. Pipeline é criada com status 'pending'
5. Retorna pipeline_id para monitoramento
```

### Fase 2: Extração
```
1. Extrai dados do canal YouTube
2. Coleta títulos e metadados
3. Analisa padrões de engajamento
4. Salva dados para próximas etapas
```

### Fase 3: Geração de Títulos
```
1. Analisa títulos extraídos
2. Identifica padrões virais
3. Gera prompts otimizados
4. Chama API da IA configurada
5. Processa e pontua resultados
6. Seleciona melhor título
```

### Fase 4: Geração de Premissa
```
1. Usa título selecionado
2. Analisa contexto do canal
3. Gera premissa estruturada
4. Valida coerência com título
```

### Fase 5: Geração de Roteiro
```
1. Pipeline de 3 prompts:
   - Prompt 1: Estrutura inicial
   - Prompt 2: Desenvolvimento
   - Prompt 3: Refinamento
2. Validação de qualidade
3. Detecção de repetições
4. Formatação final
```

### Fase 6: Geração de Áudio
```
1. Segmenta roteiro em chunks
2. Para cada segmento:
   - Gera áudio via TTS
   - Calcula timing
   - Salva arquivo temporário
3. Combina todos os segmentos
4. Otimiza qualidade final
```

### Fase 7: Geração de Imagens
```
1. Analisa roteiro para cenas
2. Gera prompts visuais
3. Para cada cena:
   - Cria prompt específico
   - Gera imagem via API
   - Otimiza para vídeo
4. Organiza sequência temporal
```

### Fase 8: Criação de Vídeo
```
1. Carrega áudio e imagens
2. Calcula timing de sincronização
3. Aplica transições entre cenas
4. Adiciona legendas (se configurado)
5. Renderiza vídeo final
6. Salva em múltiplas resoluções
```

### Fase 9: Finalização
```
1. Cleanup de arquivos temporários
2. Atualiza status para 'completed'
3. Salva metadados do resultado
4. Notifica frontend via logs
```

---

## 🔍 Diagnóstico e Troubleshooting

### Problemas Comuns na Extração

**Erro**: "Canal não encontrado"
- **Causa**: URL inválida ou canal privado
- **Solução**: Verificar URL e permissões do canal

**Erro**: "Rate limit exceeded"
- **Causa**: Muitas requisições ao YouTube
- **Solução**: Implementar delay entre requisições

**Erro**: "Timeout na extração"
- **Causa**: Canal muito grande ou conexão lenta
- **Solução**: Aumentar timeout ou limitar número de vídeos

### Problemas na Geração de Títulos

**Erro**: "API key inválida"
- **Causa**: Chave de API incorreta ou expirada
- **Solução**: Verificar e atualizar chaves nas configurações

**Erro**: "Quota exceeded"
- **Causa**: Limite de uso da API atingido
- **Solução**: Aguardar reset ou usar provider alternativo

**Erro**: "Títulos de baixa qualidade"
- **Causa**: Prompts inadequados ou dados insuficientes
- **Solução**: Melhorar prompts ou usar mais dados de referência

### Problemas na Geração de Roteiro

**Erro**: "Roteiro muito repetitivo"
- **Causa**: Detector de repetições não funcionando
- **Solução**: Ajustar parâmetros do RepetitionDetector

**Erro**: "Roteiro muito curto/longo"
- **Causa**: Configuração inadequada de caracteres
- **Solução**: Ajustar target_chars na configuração

**Erro**: "Timeout na geração"
- **Causa**: Roteiro muito complexo ou API lenta
- **Solução**: Dividir em chunks menores ou usar modelo mais rápido

### Problemas no TTS

**Erro**: "Arquivo de áudio corrompido"
- **Causa**: Falha na geração ou transferência
- **Solução**: Regenerar áudio ou verificar conexão

**Erro**: "Sincronização incorreta"
- **Causa**: Cálculo de timing incorreto
- **Solução**: Verificar segmentação do texto

**Erro**: "Qualidade de voz ruim"
- **Causa**: Configurações inadequadas
- **Solução**: Ajustar parâmetros de voz (speed, pitch, clarity)

### Problemas na Geração de Imagens

**Erro**: "Imagens não relacionadas ao roteiro"
- **Causa**: Prompts inadequados
- **Solução**: Melhorar geração de prompts ou usar IA Agent

**Erro**: "Falha na geração"
- **Causa**: API indisponível ou prompt inválido
- **Solução**: Verificar status da API e validar prompts

**Erro**: "Imagens de baixa qualidade"
- **Causa**: Configurações inadequadas
- **Solução**: Ajustar qualidade e modelo usado

### Problemas na Criação de Vídeo

**Erro**: "MoviePy não instalado"
- **Causa**: Dependência não instalada
- **Solução**: `pip install moviepy`

**Erro**: "Erro de codificação"
- **Causa**: FFmpeg não configurado
- **Solução**: Instalar e configurar FFmpeg

**Erro**: "Vídeo dessincronizado"
- **Causa**: Timing incorreto entre áudio e imagens
- **Solução**: Verificar duração dos segmentos TTS

**Erro**: "Falha na renderização"
- **Causa**: Memória insuficiente ou arquivos corrompidos
- **Solução**: Reduzir resolução ou verificar arquivos de entrada

### Monitoramento e Logs

**Logs da Pipeline**:
- Acessível via `/api/pipeline/{id}/logs`
- Níveis: info, warning, error
- Timestamp e dados estruturados

**Logs do Sistema**:
- Arquivo: `backend/logs/app.log`
- Rotação automática
- Filtros por nível e componente

**Métricas de Performance**:
- Tempo por etapa
- Uso de recursos
- Taxa de sucesso
- Qualidade dos resultados

---

## ⚙️ Configurações e Dependências

### Backend Dependencies

**Core**:
```
Flask==2.3.3
Flask-CORS==4.0.0
requests==2.31.0
yt-dlp==2023.7.6
```

**IA e APIs**:
```
openai==1.3.0
google-generativeai==0.3.0
elevenlabs==0.2.24
```

**Processamento**:
```
moviepy==1.0.3
Pillow==10.0.0
redis==4.6.0
tiktoken==0.5.1
```

### Frontend Dependencies

**Core**:
```
react==18.2.0
react-dom==18.2.0
react-router-dom==6.8.1
vite==4.3.2
```

**UI e Animações**:
```
framer-motion==10.12.4
lucide-react==0.263.1
tailwindcss==3.3.0
```

**Utilitários**:
```
axios==1.4.0
date-fns==4.1.0
react-hot-toast==2.4.0
```

### Variáveis de Ambiente

**Backend** (`.env`):
```
# APIs de IA
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...
ELEVENLABS_API_KEY=...
OPENROUTER_API_KEY=...

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Configurações
DEBUG=True
FLASK_ENV=development
```

### Estrutura de Diretórios

```
auto-video-producer/
├── backend/
│   ├── temp/              # Arquivos temporários
│   ├── outputs/           # Vídeos finalizados
│   ├── logs/              # Logs do sistema
│   └── static/            # Arquivos estáticos
├── frontend/
│   ├── dist/              # Build de produção
│   └── public/            # Arquivos públicos
└── docs/                  # Documentação
```

### Comandos de Execução

**Backend**:
```bash
cd backend
pip install -r requirements.txt
python app.py
```

**Frontend**:
```bash
cd frontend
npm install
npm run dev
```

**Produção**:
```bash
# Frontend
npm run build

# Backend
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## 📊 Monitoramento e Métricas

### KPIs da Pipeline
- **Taxa de Sucesso**: % de pipelines concluídas
- **Tempo Médio**: Duração média por etapa
- **Qualidade**: Score de qualidade dos resultados
- **Uso de Recursos**: CPU, memória, storage

### Alertas Configuráveis
- Pipeline travada por mais de X minutos
- Taxa de erro acima de Y%
- Uso de API próximo do limite
- Espaço em disco baixo

### Dashboard de Monitoramento
- Pipelines ativas em tempo real
- Histórico de execuções
- Estatísticas de performance
- Status das APIs externas

---

*Documentação atualizada em: Janeiro 2024*
*Versão: 5.0*