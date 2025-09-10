# 🚀 Guia de Configuração - Repositório de Desenvolvimento

## 📋 Visão Geral

Este guia explica como configurar um repositório de desenvolvimento separado para o projeto Auto Video Producer, permitindo trabalhar com segurança sem afetar o código de produção.

## 🎯 Objetivos

- ✅ Manter código de produção estável
- ✅ Permitir experimentação segura
- ✅ Facilitar colaboração
- ✅ Implementar workflow de desenvolvimento profissional

## 🔧 Configuração Automática

### Passo 1: Executar Script de Configuração

```bash
python setup_dev_repository.py
```

O script irá:
1. Verificar o status atual do Git
2. Solicitar a URL do repositório de desenvolvimento
3. Configurar o remote 'dev'
4. Criar branch 'develop'
5. Fazer push inicial
6. Criar scripts de workflow

### Passo 2: Criar Repositório no GitHub

1. Acesse [GitHub](https://github.com)
2. Clique em "New repository"
3. Nome sugerido: `auto-video-producerV5-dev`
4. Deixe público ou privado conforme preferência
5. **NÃO** inicialize com README (usaremos o existente)
6. Clique em "Create repository"

## 📊 Estrutura de Repositórios

```
🏭 PRODUÇÃO (origin)
├── Repositório: auto-video-producerV5
├── Branch: main
├── Código: Estável e testado
└── Deploy: Ambiente de produção

🔬 DESENVOLVIMENTO (dev)
├── Repositório: auto-video-producerV5-dev
├── Branch: develop
├── Código: Experimental e em desenvolvimento
└── Deploy: Ambiente de teste
```

## 🔄 Workflow de Desenvolvimento

### Desenvolvimento Diário

```bash
# 1. Trabalhar na branch develop
git checkout develop

# 2. Fazer mudanças e commits
git add .
git commit -m "Implementar nova funcionalidade"

# 3. Push para repositório de desenvolvimento
git push dev develop
```

### Deploy para Produção

```bash
# 1. Testar tudo no ambiente de desenvolvimento
# 2. Fazer merge para main
git checkout main
git merge develop

# 3. Push para produção
git push origin main

# 4. Sincronizar desenvolvimento
git push dev main
```

## 🛠️ Scripts Disponíveis

### `push_both.bat`
Faz push para ambos os repositórios simultaneamente:
```bash
push_both.bat
```

### `sync_dev.bat`
Sincroniza o repositório de desenvolvimento com produção:
```bash
sync_dev.bat
```

## 📋 Comandos Úteis

### Verificar Remotes
```bash
git remote -v
```

### Listar Branches
```bash
git branch -a
```

### Push Específico
```bash
# Para produção
git push origin main

# Para desenvolvimento
git push dev develop
```

### Pull de Ambos
```bash
# De produção
git pull origin main

# De desenvolvimento
git pull dev develop
```

## 🔒 Configurações de Segurança

### Repositório de Produção
- ✅ Branch protection em `main`
- ✅ Require pull request reviews
- ✅ Require status checks
- ✅ Restrict direct pushes

### Repositório de Desenvolvimento
- ✅ Mais flexível para experimentação
- ✅ Permite pushes diretos
- ✅ Testes automatizados opcionais

## 🚨 Cenários de Emergência

### Reverter Mudanças
```bash
# Voltar para último commit estável
git reset --hard HEAD~1

# Ou voltar para commit específico
git reset --hard <commit-id>
```

### Sincronizar Forçado
```bash
# Forçar push (cuidado!)
git push --force-with-lease dev develop
```

### Remover Remote
```bash
# Se precisar reconfigurar
git remote remove dev
```

## 📈 Boas Práticas

### ✅ Faça
- Sempre teste no ambiente de desenvolvimento primeiro
- Use commits descritivos
- Mantenha branches sincronizadas
- Faça backup antes de mudanças grandes
- Use pull requests quando possível

### ❌ Evite
- Push direto para produção sem testes
- Commits com mensagens vagas
- Trabalhar diretamente na branch main
- Ignorar conflitos de merge
- Fazer force push em produção

## 🔍 Troubleshooting

### Problema: Remote já existe
```bash
git remote remove dev
git remote add dev <nova-url>
```

### Problema: Branch não existe
```bash
git checkout -b develop
git push dev develop
```

### Problema: Conflitos de merge
```bash
git status
git add .
git commit -m "Resolver conflitos"
```

## 📞 Suporte

Se encontrar problemas:
1. Verifique o status com `git status`
2. Consulte os logs com `git log --oneline`
3. Execute o script de configuração novamente
4. Consulte a documentação do Git

---

**🎉 Configuração completa! Agora você pode desenvolver com segurança!**