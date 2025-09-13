#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para debug do sistema de rotação de chaves Gemini
Mostra o estado atual das chaves carregadas e ajuda a diagnosticar problemas.
"""

import sys
import os
import json
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("🔍 Debug do Sistema de Rotação de Chaves Gemini")
print("=" * 60)

# Tentar importar e verificar o estado das chaves
try:
    from routes.automations import GEMINI_KEYS_ROTATION, load_gemini_keys, get_next_gemini_key, get_gemini_keys_count
    
    print("\n📊 Estado atual da rotação:")
    print(f"   Total de chaves carregadas: {len(GEMINI_KEYS_ROTATION['keys'])}")
    print(f"   Índice atual: {GEMINI_KEYS_ROTATION['current_index']}")
    print(f"   Último reset: {GEMINI_KEYS_ROTATION['last_reset']}")
    print(f"   Contagem de uso: {GEMINI_KEYS_ROTATION['usage_count']}")
    
    # Mostrar todas as chaves carregadas (ocultando a maioria do valor para segurança)
    if GEMINI_KEYS_ROTATION['keys']:
        print("\n🔑 Chaves carregadas:")
        for i, key in enumerate(GEMINI_KEYS_ROTATION['keys']):
            usage = GEMINI_KEYS_ROTATION['usage_count'].get(key, 0)
            print(f"   {i+1}. {key[:20]}... (uso: {usage})")
    else:
        print("\n⚠️ Nenhuma chave carregada na rotação!")
    
    # Verificar se podemos obter a próxima chave
    print("\n🔄 Testando obtenção da próxima chave...")
    next_key = get_next_gemini_key()
    if next_key:
        print(f"   ✅ Próxima chave obtida: {next_key[:20]}...")
        print(f"   Contagem de uso após obtenção: {GEMINI_KEYS_ROTATION['usage_count'].get(next_key, 0)}")
    else:
        print("   ❌ Não foi possível obter a próxima chave")
    
    # Forçar recarregamento das chaves
    print("\n🔄 Forçando recarregamento das chaves...")
    reloaded_keys = load_gemini_keys()
    print(f"   Total de chaves recarregadas: {len(reloaded_keys)}")
    
    # Mostrar resultado do recarregamento
    if reloaded_keys:
        print("\n🔑 Chaves após recarregamento:")
        for i, key in enumerate(reloaded_keys):
            usage = GEMINI_KEYS_ROTATION['usage_count'].get(key, 0)
            print(f"   {i+1}. {key[:20]}... (uso: {usage})")
    
    # Verificar o arquivo api_keys.json diretamente
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'api_keys.json')
    print(f"\n📄 Verificando arquivo {config_path}...")
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            api_keys = json.load(f)
        
        # Contar chaves Gemini no arquivo
        gemini_file_keys = [key for key in api_keys if 'gemini' in key.lower() and isinstance(api_keys[key], str) and len(api_keys[key]) > 10 and api_keys[key].startswith('AIza')]
        print(f"   Total de chaves Gemini válidas no arquivo: {len(gemini_file_keys)}")
        
        # Verificar se todas as chaves do arquivo estão sendo carregadas
        missing_keys = []
        for key_name in api_keys:
            if 'gemini' in key_name.lower() and isinstance(api_keys[key_name], str) and len(api_keys[key_name]) > 10 and api_keys[key_name].startswith('AIza'):
                if api_keys[key_name] not in GEMINI_KEYS_ROTATION['keys']:
                    missing_keys.append(key_name)
        
        if missing_keys:
            print(f"   ⚠️ Chaves no arquivo mas não carregadas: {missing_keys}")
        else:
            print(f"   ✅ Todas as chaves válidas do arquivo estão carregadas")
    else:
        print(f"   ❌ Arquivo {config_path} não encontrado!")
    
    print("\n✅ Debug concluído com sucesso!")
    
except Exception as e:
    print(f"\n❌ Erro durante o debug: {e}")
    import traceback
    traceback.print_exc()
    
print("=" * 60)