#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar status detalhado das chaves Gemini
"""

import os
import sys
import json
from datetime import datetime

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from routes.automations import GEMINI_KEYS_ROTATION, load_gemini_keys, get_gemini_keys_count
    
    print("=" * 60)
    print("🔍 VERIFICAÇÃO DETALHADA DAS CHAVES GEMINI")
    print("=" * 60)
    
    # Carregar chaves
    keys = load_gemini_keys()
    print(f"✅ Total de chaves carregadas: {len(keys)}")
    
    # Verificar data de reset
    today = datetime.now().date()
    last_reset = GEMINI_KEYS_ROTATION['last_reset']
    print(f"📅 Data atual: {today}")
    print(f"📅 Último reset: {last_reset}")
    print(f"🔄 Reset necessário: {'Sim' if last_reset != today else 'Não'}")
    
    # Verificar contadores de uso
    print("\n📊 STATUS DETALHADO DAS CHAVES:")
    print("-" * 60)
    
    total_usage = 0
    available_keys = 0
    
    for i, key in enumerate(keys):
        usage = GEMINI_KEYS_ROTATION['usage_count'].get(key, 0)
        total_usage += usage
        
        # Verificar se a chave ainda está disponível
        is_available = usage < 250
        if is_available:
            available_keys += 1
        
        status = "✅ Disponível" if is_available else "❌ Esgotada"
        
        print(f"Chave {i+1:2d}: {key[:20]}... | Uso: {usage:3d}/250 | Status: {status}")
    
    print("-" * 60)
    print(f"📈 Uso total: {total_usage} requisições")
    print(f"🔑 Chaves disponíveis: {available_keys}/{len(keys)}")
    
    # Verificar se há fallback disponível
    try:
        from routes.automations import get_fallback_provider_info
        fallback = get_fallback_provider_info()
        if fallback:
            print(f"🔄 Fallback disponível: {fallback['provider']} (prioridade {fallback['priority']})")
        else:
            print("❌ Nenhum fallback disponível")
    except Exception as e:
        print(f"❌ Erro ao verificar fallback: {e}")
    
    print("=" * 60)
    
except Exception as e:
    print(f"❌ Erro ao executar script: {e}")
    import traceback
    traceback.print_exc()