# 🖼️ Geração de Imagens e Mídia

## Visão Geral
Sistema automatizado de criação de imagens para vídeos educacionais usando IA.

## Arquivos Envolvidos
- `backend/routes/images.py` - Rotas de geração
- `backend/services/image_service.py` - Serviço principal
- `backend/services/image_queue.py` - Fila de processamento

## Processo de Geração

### 1. Análise de Roteiro
```python
# backend/services/image_service.py
def analyze_script_for_images(script):
    # Identifica cenas principais
    scenes = extract_key_scenes(script)
    
    # Gera prompts para cada cena
    prompts = []
    for scene in scenes:
        prompt = generate_image_prompt(scene)
        prompts.append({
            'scene': scene,
            'prompt': prompt,
            'style': 'educational'
        })
    
    return prompts
```

### 2. Tipos de Imagens Geradas

#### Thumbnails de Capítulos
- **Tamanho**: 1920x1080 (16:9)
- **Estilo**: Clean, texto minimalista
- **Cores**: Paleta consistente com marca

#### Imagens de Transição
- **Função**: Transição entre tópicos
- **Estilo**: Abstrato ou simbólico
- **Duração**: 2-3 segundos no vídeo

#### Imagens de Apoio Visual
- **Função**: Ilustrar conceitos complexos
- **Estilo**: Infográfico ou diagrama
- **Exemplos**: Gráficos, fluxogramas, estatísticas

### 3. Prompts por Agente

#### Agente Milionário
```
Crie uma imagem inspiradora sobre:
[CONCEITO]

Estilo: Clean, profissional, cores quentes
Elementos: Brasileiro bem-sucedido, ambiente moderno
Cores: Dourado, azul escuro, branco
Evitar: Estereótipos, clichês
```

#### Storyteller
```
Crie uma imagem educativa ilustrando:
[CONCEITO]

Estilo: Infográfico clean, cores vibrantes
Elementos: Ícones, diagramas, texto mínimo
Cores: Azul, verde, laranja
Foco: Clareza e compreensão
```

### 4. Integração com Pipeline

#### Fluxo Completo
1. Recebe roteiro completo
2. Analisa e identifica cenas
3. Gera prompts personalizados
4. Cria imagens via IA
5. Organiza sequencialmente
6. Prepara para montagem

#### API de Geração
```python
# backend/routes/images.py
@app.route('/api/generate-images', methods=['POST'])
def generate_images():
    data = request.json
    script = data.get('script')
    agent_type = data.get('agent_type', 'storyteller')
    
    images = image_service.generate_script_images(script, agent_type)
    
    return jsonify({
        'images': images,
        'count': len(images),
        'total_cost': sum(img['cost'] for img in images)
    })
```

### 5. Configurações de Qualidade

#### Resoluções Suportadas
- **HD**: 1920x1080 (padrão)
- **4K**: 3840x2160 (premium)
- **Social**: 1080x1080 (Instagram)
- **Story**: 1080x1920 (reels)

#### Estilos Visuais
- **Minimalista**: Fundos limpos, texto destacado
- **Infográfico**: Diagramas, estatísticas visuais
- **Realista**: Fotos estilo stock, pessoas reais
- **Abstrato**: Formas geométricas, gradientes

## Frontend - Interface de Visualização

### Componente ImageGallery
```javascript
// frontend/components/ImageGallery.jsx
const ImageGallery = ({ images, onSelect }) => {
  return (
    <div className="image-gallery">
      {images.map((image, index) => (
        <div key={index} className="image-card">
          <img 
            src={image.url} 
            alt={image.description}
            className="generated-image"
          />
          <div className="image-info">
            <p>{image.prompt}</p>
            <span>Custo: ${image.cost}</span>
            <button onClick={() => onSelect(image)}>
              Selecionar
            </button>
          </div>
        </div>
      ))}
    </div>
  );
};
```

## Sistema de Fila

### Processamento Assíncrono
```python
# backend/services/image_queue.py
class ImageQueue:
    def add_to_queue(self, request):
        job = {
            'id': str(uuid.uuid4()),
            'prompt': request['prompt'],
            'style': request['style'],
            'priority': request.get('priority', 'normal')
        }
        self.redis_client.lpush('image_queue', json.dumps(job))
        return job['id']
    
    def process_queue(self):
        while True:
            job_data = self.redis_client.brpop('image_queue')
            job = json.loads(job_data[1])
            self.generate_single_image(job)
```

### Status de Processamento
```json
{
  "job_id": "uuid-123",
  "status": "processing|completed|failed",
  "progress": 75,
  "estimated_time": 30,
  "result": {
    "url": "https://...",
    "cost": 0.02
  }
}
```

## Otimizações de Custo

### Cache de Imagens
- **Cache**: 7 dias para prompts idênticos
- **Deduplicação**: Detecta imagens similares
- **Rate Limiting**: Respeita limites de API

### Estratégias de Redução
- **Prompt Reutilização**: Mesmo prompt = mesma imagem
- **Batch Processing**: Processa múltiplas de uma vez
- **Qualidade Ajustável**: HD vs 4K conforme necessidade

## Métricas de Performance

### KPIs Monitorados
- **Tempo Médio**: 15-30 segundos por imagem
- **Taxa de Sucesso**: 95%+ de gerações bem-sucedidas
- **Custo Total**: $0.01-0.04 por imagem
- **Cache Hit Rate**: 30-40% de reutilização

### Dashboard de Monitoramento
```javascript
// frontend/components/ImageMetrics.jsx
const ImageMetrics = ({ stats }) => {
  return (
    <div className="metrics-dashboard">
      <div className="metric-card">
        <h3>Imagens Geradas</h3>
        <p>{stats.total_generated}</p>
      </div>
      <div className="metric-card">
        <h3>Custo Total</h3>
        <p>${stats.total_cost.toFixed(2)}</p>
      </div>
      <div className="metric-card">
        <h3>Taxa de Sucesso</h3>
        <p>{(stats.success_rate * 100).toFixed(1)}%</p>
      </div>
    </div>
  );
};
```