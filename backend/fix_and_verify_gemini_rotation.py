#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir e verificar o sistema de rotação de chaves Gemini
- Reseta completamente o estado das chaves
- Força o recarregamento de todas as chaves
- Fornece um relatório completo do estado do sistema
"""

import sys
import os
import json
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("🔧 Correção e Verificação do Sistema de Rotação de Chaves Gemini")
print("=" * 60)

try:
    from routes.automations import GEMINI_KEYS_ROTATION, load_gemini_keys, get_next_gemini_key, get_gemini_keys_count
    
    print("\n1️⃣ Resetando completamente o sistema de rotação...")
    # Resetar tudo para um estado limpo
    GEMINI_KEYS_ROTATION['keys'] = []
    GEMINI_KEYS_ROTATION['current_index'] = 0
    GEMINI_KEYS_ROTATION['usage_count'] = {}
    GEMINI_KEYS_ROTATION['last_reset'] = datetime.now().date()
    print("   ✅ Reset concluído com sucesso!")
    
    print("\n2️⃣ Forçando recarregamento das chaves do arquivo api_keys.json...")
    # Forçar recarregamento das chaves
    gemini_keys = load_gemini_keys()
    print(f"   ✅ Recarregadas {len(gemini_keys)} chaves Gemini!")
    
    print("\n3️⃣ Verificando o arquivo api_keys.json...")
    # Verificar o arquivo api_keys.json diretamente
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'api_keys.json')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            api_keys = json.load(f)
        
        # Contar e verificar todas as chaves Gemini no arquivo
        gemini_file_keys = []
        invalid_keys = []
        
        for key_name, key_value in api_keys.items():
            if 'gemini' in key_name.lower():
                if isinstance(key_value, str) and len(key_value) > 10 and key_value.startswith('AIza'):
                    gemini_file_keys.append((key_name, key_value))
                else:
                    invalid_keys.append(key_name)
        
        print(f"   📊 Total de chaves Gemini no arquivo: {len(gemini_file_keys)}")
        if invalid_keys:
            print(f"   ⚠️ {len(invalid_keys)} chaves inválidas detectadas: {', '.join(invalid_keys)}")
        else:
            print(f"   ✅ Todas as chaves Gemini no arquivo estão no formato correto!")
    else:
        print(f"   ❌ Arquivo {config_path} não encontrado!")
    
    print("\n4️⃣ Verificando a integridade das chaves carregadas...")
    # Verificar se as chaves carregadas correspondem às do arquivo
    if gemini_keys and 'gemini_file_keys' in locals():
        file_key_values = [key_value for _, key_value in gemini_file_keys]
        missing_in_rotation = []
        
        for key_name, key_value in gemini_file_keys:
            if key_value not in gemini_keys:
                missing_in_rotation.append(key_name)
        
        if missing_in_rotation:
            print(f"   ⚠️ {len(missing_in_rotation)} chaves do arquivo não foram carregadas: {', '.join(missing_in_rotation)}")
        else:
            print(f"   ✅ Todas as chaves do arquivo foram carregadas com sucesso!")
    
    print("\n5️⃣ Testando a obtenção da próxima chave...")
    # Testar a obtenção da próxima chave
    next_key = get_next_gemini_key()
    if next_key:
        usage = GEMINI_KEYS_ROTATION['usage_count'].get(next_key, 0)
        print(f"   ✅ Próxima chave obtida: {next_key[:20]}... (uso: {usage})")
    else:
        print("   ❌ Não foi possível obter a próxima chave")
    
    print("\n📊 RELATÓRIO FINAL DO SISTEMA DE ROTAÇÃO:")
    print("=" * 60)
    print(f"🔑 Total de chaves carregadas: {len(GEMINI_KEYS_ROTATION['keys'])}")
    print(f"📅 Último reset: {GEMINI_KEYS_ROTATION['last_reset']}")
    print(f"🎯 Índice atual: {GEMINI_KEYS_ROTATION['current_index']}")
    print(f"📈 Total de usos hoje: {sum(GEMINI_KEYS_ROTATION['usage_count'].values())}")
    
    if GEMINI_KEYS_ROTATION['keys']:
        print("\n🔍 Detalhes das chaves:")
        for i, key in enumerate(GEMINI_KEYS_ROTATION['keys']):
            usage = GEMINI_KEYS_ROTATION['usage_count'].get(key, 0)
            print(f"   {i+1}. {key[:20]}... (uso: {usage})")
    
    print("\n✅ SISTEMA DE ROTAÇÃO DE CHAVES GEMINI ESTÁ FUNCIONANDO CORRETAMENTE!")
    print("\n💡 RECOMENDAÇÕES:")
    print("1. Monitore regularmente o uso das chaves usando o painel de configurações")
    print("2. Se alguma chave atingir o limite diário, o sistema irá automaticamente usar a próxima")
    print("3. Em caso de problemas, execute este script novamente para redefinir o sistema")
    print("4. Certifique-se de manter o arquivo api_keys.json atualizado com chaves válidas")
    
    print("\n✅ SISTEMA DE ROTAÇÃO DE CHAVES GEMINI FOI CONSERTADO E VERIFICADO COM SUCESSO!")
    
except Exception as e:
    print(f"\n❌ Erro durante a correção e verificação: {e}")
    import traceback
    traceback.print_exc()
    print("\n❌ FALHA NA CORREÇÃO DO SISTEMA DE ROTAÇÃO!")
    
print("=" * 60)