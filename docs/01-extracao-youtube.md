# 📹 Extração de Conteúdo do YouTube

## Visão Geral
Sistema de extração automatizada de conteúdo do YouTube usando yt-dlp e IA.

## Arquivos Envolvidos
- `backend/routes/automations.py` - Rotas de extração
- `backend/services/youtube_service.py` - Serviço de extração
- `backend/utils/video_processor.py` - Processamento de vídeo

## Processo Detalhado

### 1. Requisição do Usuário
```javascript
// Frontend: VideoExtractor.jsx
const extractVideo = async (url) => {
  const response = await fetch('/api/extract-youtube', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url })
  });
  return response.json();
};
```

### 2. Backend - Rota de Extração
```python
# backend/routes/automations.py
@app.route('/api/extract-youtube', methods=['POST'])
def extract_youtube():
    data = request.json
    url = data.get('url')
    
    # Extração via yt-dlp
    video_info = youtube_service.extract_video_info(url)
    transcript = youtube_service.get_transcript(url)
    
    return jsonify({
        'title': video_info['title'],
        'description': video_info['description'],
        'transcript': transcript,
        'metadata': video_info
    })
```

### 3. Dados Extraídos
- **Título**: Título original do vídeo
- **Descrição**: Descrição completa
- **Transcrição**: Texto completo em português
- **Duração**: Tempo em segundos
- **Autor**: Nome do canal
- **Thumbnail**: URL da miniatura
- **Tags**: Palavras-chave do vídeo

### 4. Tratamento de Erros
- Vídeo privado: Retorna erro 403
- Vídeo indisponível: Retorna erro 404
- Transcrição não disponível: Retorna aviso

### 5. Cache de Extração
- Cache de 1 hora para mesma URL
- Evita reprocessamento desnecessário
- Reduz custos de API

## Exemplo de Resposta Completa
```json
{
  "title": "Como Investir na Bolsa em 2024",
  "description": "Neste vídeo eu explico...",
  "transcript": "Olá, hoje vamos falar sobre investimentos...",
  "metadata": {
    "duration": 720,
    "author": "Canal Invest",
    "view_count": 150000,
    "upload_date": "2024-01-15"
  }
}
```