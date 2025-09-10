# 🎬 Auto Video Producer

> Sistema completo de geração automática de vídeos com Inteligência Artificial

## 📋 Descrição

O Auto Video Producer é uma plataforma completa que automatiza todo o processo de criação de vídeos, desde a geração de roteiros até a produção final, utilizando tecnologias de IA avançadas.

## ✨ Funcionalidades Principais

- 🤖 **Geração de Roteiros com IA**: Criação automática de histórias e roteiros
- 🎨 **Geração de Imagens**: Criação de imagens personalizadas para cada cena
- 🔊 **Text-to-Speech**: Conversão de texto em áudio com vozes naturais
- 🎞️ **Montagem Automática**: Combinação de áudio, imagens e efeitos
- 📊 **Pipeline Inteligente**: Processamento automatizado completo
- 🎯 **Múltiplos Agentes**: Diferentes tipos de conteúdo (romance, terror, etc.)

## 🏗️ Arquitetura

### Backend (Python/Flask)
- **API REST** para gerenciamento de pipelines
- **Serviços de IA** integrados (OpenAI, Gemini, etc.)
- **Sistema de Filas** para processamento assíncrono
- **Banco de Dados** SQLite para persistência

### Frontend (React/Vite)
- **Interface Moderna** com Tailwind CSS
- **Dashboard Interativo** para monitoramento
- **Controle de Pipelines** em tempo real
- **Visualização de Resultados**

## 🚀 Instalação Rápida

### Pré-requisitos
- Python 3.8+
- Node.js 18+
- Git

### 1. Clone o Repositório
```bash
git clone https://github.com/SEU_USUARIO/auto-video-producer.git
cd auto-video-producer
```

### 2. Configure o Backend
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Configure suas chaves de API no arquivo .env
python app.py
```

### 3. Configure o Frontend
```bash
cd frontend
npm install
npm run dev
```

### 4. Acesse a Aplicação
- Frontend: http://localhost:5173
- Backend API: http://localhost:5000

## ⚙️ Configuração

### Chaves de API Necessárias
- **OpenAI**: Para geração de texto e roteiros
- **Gemini**: Alternativa para geração de conteúdo
- **Kokoro TTS**: Para síntese de voz
- **Stable Diffusion**: Para geração de imagens

### Arquivo .env
```env
OPENAI_API_KEY=sua_chave_aqui
GEMINI_API_KEY=sua_chave_aqui
KOKORO_API_KEY=sua_chave_aqui
# ... outras configurações
```

## 📖 Como Usar

1. **Acesse o Dashboard** no frontend
2. **Escolha um Agente** (tipo de conteúdo)
3. **Configure os Parâmetros** do vídeo
4. **Inicie o Pipeline** de produção
5. **Monitore o Progresso** em tempo real
6. **Baixe o Vídeo** quando concluído

## 🛠️ Desenvolvimento

### Estrutura do Projeto
```
├── backend/          # API Python/Flask
│   ├── routes/       # Endpoints da API
│   ├── services/     # Lógica de negócio
│   ├── config/       # Configurações
│   └── output/       # Arquivos gerados
├── frontend/         # Interface React
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── utils/
└── docs/            # Documentação
```

### Scripts Úteis
```bash
# Backend
python app.py                    # Iniciar servidor
python -m pytest               # Executar testes

# Frontend
npm run dev                     # Servidor de desenvolvimento
npm run build                   # Build para produção
npm run test                    # Executar testes
```

## 📊 Status do Projeto

- ✅ **Core System**: Funcional
- ✅ **API Backend**: Completa
- ✅ **Frontend UI**: Implementado
- ✅ **Pipeline Automation**: Ativo
- 🔄 **Melhorias Contínuas**: Em andamento

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🆘 Suporte

- 📖 **Documentação**: Veja a pasta `/docs`
- 🐛 **Issues**: Reporte bugs no GitHub Issues
- 💬 **Discussões**: Use GitHub Discussions

## 🙏 Agradecimentos

- OpenAI pela API GPT
- Google pelo Gemini
- Comunidade open source
- Todos os contribuidores

---

**Feito com ❤️ para automatizar a criação de conteúdo**