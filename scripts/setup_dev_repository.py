#!/usr/bin/env python3
"""
Script para configurar repositório de desenvolvimento
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

def check_git_status():
    """Verifica se estamos em um repositório Git"""
    stdout, stderr, code = run_command("git status", check=False)
    return code == 0

def get_current_remotes():
    """Obtém remotes atuais"""
    stdout, stderr, code = run_command("git remote -v")
    if code == 0:
        return stdout
    return ""

def setup_dev_repository():
    """Configura repositório de desenvolvimento"""
    print("🚀 Configurando Repositório de Desenvolvimento")
    print("=" * 50)
    
    # Verificar se estamos em um repositório Git
    if not check_git_status():
        print("❌ Erro: Este diretório não é um repositório Git!")
        return False
    
    # Mostrar remotes atuais
    print("\n📋 Remotes atuais:")
    current_remotes = get_current_remotes()
    print(current_remotes)
    
    # Solicitar URL do repositório de desenvolvimento
    print("\n🔧 Configuração do Repositório de Desenvolvimento")
    print("Exemplo: https://github.com/Ender-ss/auto-video-producerV5-dev.git")
    
    dev_repo_url = input("\n📝 Digite a URL do repositório de desenvolvimento: ").strip()
    
    if not dev_repo_url:
        print("❌ URL não fornecida. Cancelando...")
        return False
    
    # Verificar se remote 'dev' já existe
    if 'dev\t' in current_remotes:
        print("\n⚠️  Remote 'dev' já existe!")
        choice = input("Deseja substituir? (s/N): ").lower()
        if choice == 's':
            print("🔄 Removendo remote 'dev' existente...")
            run_command("git remote remove dev")
        else:
            print("❌ Cancelando configuração...")
            return False
    
    # Adicionar remote de desenvolvimento
    print(f"\n➕ Adicionando remote 'dev': {dev_repo_url}")
    stdout, stderr, code = run_command(f'git remote add dev "{dev_repo_url}"')
    
    if code != 0:
        print(f"❌ Erro ao adicionar remote: {stderr}")
        return False
    
    # Verificar se o repositório remoto existe
    print("\n🔍 Verificando conectividade com repositório remoto...")
    stdout, stderr, code = run_command("git ls-remote dev", check=False)
    
    if code != 0:
        print(f"⚠️  Aviso: Não foi possível conectar ao repositório remoto.")
        print(f"Erro: {stderr}")
        print("Certifique-se de que o repositório existe no GitHub.")
    else:
        print("✅ Conectividade com repositório remoto confirmada!")
    
    # Criar branch de desenvolvimento
    print("\n🌿 Criando branch de desenvolvimento...")
    stdout, stderr, code = run_command("git checkout -b develop", check=False)
    
    if code != 0 and "already exists" in stderr:
        print("ℹ️  Branch 'develop' já existe. Fazendo checkout...")
        run_command("git checkout develop")
    elif code != 0:
        print(f"⚠️  Aviso ao criar branch: {stderr}")
    else:
        print("✅ Branch 'develop' criada com sucesso!")
    
    # Push inicial para repositório de desenvolvimento
    print("\n📤 Fazendo push inicial para repositório de desenvolvimento...")
    stdout, stderr, code = run_command("git push dev develop", check=False)
    
    if code != 0:
        print(f"⚠️  Aviso no push inicial: {stderr}")
        print("Você pode fazer o push manualmente depois que o repositório estiver criado.")
    else:
        print("✅ Push inicial realizado com sucesso!")
    
    # Voltar para branch main
    print("\n🔄 Voltando para branch main...")
    run_command("git checkout main")
    
    # Mostrar configuração final
    print("\n✅ Configuração concluída!")
    print("\n📋 Remotes configurados:")
    final_remotes = get_current_remotes()
    print(final_remotes)
    
    return True

def create_workflow_scripts():
    """Cria scripts de workflow"""
    print("\n📝 Criando scripts de workflow...")
    
    # Script para push em ambos os repositórios
    push_script = '''@echo off
echo 🚀 Fazendo push para ambos os repositórios...
echo.
echo 📤 Push para produção (origin):
git push origin main
echo.
echo 📤 Push para desenvolvimento (dev):
git push dev main
echo.
echo ✅ Push concluído em ambos os repositórios!
pause
'''
    
    with open('push_both.bat', 'w', encoding='utf-8') as f:
        f.write(push_script)
    
    # Script para sincronizar desenvolvimento
    sync_script = '''@echo off
echo 🔄 Sincronizando repositório de desenvolvimento...
echo.
echo 📥 Fazendo pull do repositório principal:
git pull origin main
echo.
echo 📤 Fazendo push para desenvolvimento:
git push dev main
echo.
echo ✅ Sincronização concluída!
pause
'''
    
    with open('sync_dev.bat', 'w', encoding='utf-8') as f:
        f.write(sync_script)
    
    print("✅ Scripts criados:")
    print("   - push_both.bat: Push para ambos os repositórios")
    print("   - sync_dev.bat: Sincronizar desenvolvimento")

def main():
    """Função principal"""
    print("🎯 Auto Video Producer - Setup de Repositório de Desenvolvimento")
    print("=" * 70)
    
    if setup_dev_repository():
        create_workflow_scripts()
        
        print("\n🎉 Configuração completa!")
        print("\n📚 Próximos passos:")
        print("1. Crie o repositório no GitHub (se ainda não existir)")
        print("2. Use 'push_both.bat' para fazer push em ambos os repositórios")
        print("3. Use 'sync_dev.bat' para sincronizar desenvolvimento")
        print("4. Trabalhe na branch 'develop' para desenvolvimento")
        print("5. Faça merge para 'main' quando estiver pronto para produção")
    else:
        print("\n❌ Configuração não foi concluída.")

if __name__ == "__main__":
    main()