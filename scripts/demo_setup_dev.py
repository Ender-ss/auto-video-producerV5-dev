#!/usr/bin/env python3
"""
Script de demonstração para configurar repositório de desenvolvimento
Auto Video Producer - Configuração de Múltiplos Repositórios
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, check=True):
    """Executa comando e retorna resultado"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=check)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.CalledProcessError as e:
        return e.stdout.strip(), e.stderr.strip(), e.returncode

def demo_setup():
    """Demonstra como configurar repositório de desenvolvimento"""
    print("🎯 DEMONSTRAÇÃO - Configuração de Repositório de Desenvolvimento")
    print("=" * 70)
    
    # URL de exemplo para o repositório de desenvolvimento
    dev_repo_url = "https://github.com/Ender-ss/auto-video-producerV5-dev.git"
    
    print(f"\n📋 Configuração que será aplicada:")
    print(f"   🏭 Produção: https://github.com/Ender-ss/auto-video-producerV5.git")
    print(f"   🔬 Desenvolvimento: {dev_repo_url}")
    
    print("\n🔧 Comandos que serão executados:")
    print("\n1️⃣ Verificar status atual:")
    print("   git remote -v")
    print("   git status")
    
    print("\n2️⃣ Adicionar remote de desenvolvimento:")
    print(f"   git remote add dev {dev_repo_url}")
    
    print("\n3️⃣ Criar branch de desenvolvimento:")
    print("   git checkout -b develop")
    
    print("\n4️⃣ Push inicial para desenvolvimento:")
    print("   git push dev develop")
    
    print("\n5️⃣ Voltar para branch main:")
    print("   git checkout main")
    
    print("\n📝 Scripts que serão criados:")
    print("   📄 push_both.bat - Push para ambos os repositórios")
    print("   📄 sync_dev.bat - Sincronizar desenvolvimento")
    
    print("\n🎉 Resultado final:")
    print("   ✅ Dois repositórios configurados")
    print("   ✅ Branch develop criada")
    print("   ✅ Scripts de workflow disponíveis")
    print("   ✅ Workflow de desenvolvimento profissional")
    
    print("\n📚 Para executar a configuração real:")
    print("   1. Crie o repositório no GitHub primeiro")
    print("   2. Execute: python setup_dev_repository.py")
    print("   3. Siga as instruções interativas")
    
    return True

def create_example_scripts():
    """Cria scripts de exemplo"""
    print("\n📝 Criando scripts de exemplo...")
    
    # Script para push em ambos os repositórios
    push_script = '''@echo off
echo 🚀 Fazendo push para ambos os repositórios...
echo.
echo 📤 Push para produção (origin):
git push origin main
if %errorlevel% neq 0 (
    echo ❌ Erro no push para produção
    pause
    exit /b 1
)
echo ✅ Push para produção concluído!
echo.
echo 📤 Push para desenvolvimento (dev):
git push dev main
if %errorlevel% neq 0 (
    echo ❌ Erro no push para desenvolvimento
    pause
    exit /b 1
)
echo ✅ Push para desenvolvimento concluído!
echo.
echo 🎉 Push concluído em ambos os repositórios!
pause
'''
    
    with open('push_both_example.bat', 'w', encoding='utf-8') as f:
        f.write(push_script)
    
    # Script para sincronizar desenvolvimento
    sync_script = '''@echo off
echo 🔄 Sincronizando repositório de desenvolvimento...
echo.
echo 📥 Fazendo pull do repositório principal:
git pull origin main
if %errorlevel% neq 0 (
    echo ❌ Erro no pull de produção
    pause
    exit /b 1
)
echo ✅ Pull de produção concluído!
echo.
echo 📤 Fazendo push para desenvolvimento:
git push dev main
if %errorlevel% neq 0 (
    echo ❌ Erro no push para desenvolvimento
    pause
    exit /b 1
)
echo ✅ Push para desenvolvimento concluído!
echo.
echo 🎉 Sincronização concluída!
pause
'''
    
    with open('sync_dev_example.bat', 'w', encoding='utf-8') as f:
        f.write(sync_script)
    
    # Script para workflow de desenvolvimento
    dev_workflow_script = '''@echo off
echo 🔬 Workflow de Desenvolvimento
echo ============================
echo.
echo 1. Mudando para branch develop
git checkout develop
if %errorlevel% neq 0 (
    echo ⚠️  Branch develop não existe. Criando...
    git checkout -b develop
)
echo.
echo 2. Fazendo pull das últimas mudanças
git pull dev develop
echo.
echo 3. Pronto para desenvolvimento!
echo.
echo 📝 Próximos passos:
echo    - Faça suas mudanças
echo    - git add .
echo    - git commit -m "Sua mensagem"
echo    - git push dev develop
echo.
pause
'''
    
    with open('start_dev_example.bat', 'w', encoding='utf-8') as f:
        f.write(dev_workflow_script)
    
    print("✅ Scripts de exemplo criados:")
    print("   📄 push_both_example.bat")
    print("   📄 sync_dev_example.bat")
    print("   📄 start_dev_example.bat")

def main():
    """Função principal"""
    demo_setup()
    create_example_scripts()
    
    print("\n" + "=" * 70)
    print("🎊 DEMONSTRAÇÃO CONCLUÍDA!")
    print("\n📋 Arquivos criados nesta demonstração:")
    print("   📄 setup_dev_repository.py - Script de configuração interativo")
    print("   📄 GUIA_REPOSITORIO_DESENVOLVIMENTO.md - Documentação completa")
    print("   📄 push_both_example.bat - Script de push duplo")
    print("   📄 sync_dev_example.bat - Script de sincronização")
    print("   📄 start_dev_example.bat - Script de início de desenvolvimento")
    
    print("\n🚀 Para implementar:")
    print("   1. Crie o repositório 'auto-video-producerV5-dev' no GitHub")
    print("   2. Execute: python setup_dev_repository.py")
    print("   3. Siga o guia em GUIA_REPOSITORIO_DESENVOLVIMENTO.md")
    
    print("\n✨ Benefícios:")
    print("   🛡️  Código de produção protegido")
    print("   🧪 Ambiente seguro para testes")
    print("   🔄 Workflow profissional")
    print("   📈 Melhor organização do projeto")

if __name__ == "__main__":
    main()