#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar status detalhado das chaves Gemini (versao sem Unicode)
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
    print("VERIFICACAO DETALHADA DAS CHAVES GEMINI")
    print("=" * 60)
    
    # Carregar chaves
    keys = load_gemini_keys()
    print(f"Total de chaves carregadas: {len(keys)}")
    
    # Verificar data de reset
    today = datetime.now().date()
    last_reset = GEMINI_KEYS_ROTATION['last_reset']
    print(f"Data atual: {today}")
    print(f"Ultimo reset: {last_reset}")
    print(f"Reset necessario: {'Sim' if last_reset != today else 'Nao'}")
    
    # Verificar contadores de uso
    print("\nSTATUS DETALHADO DAS CHAVES:")
    print("-" * 60)
    
    total_usage = 0
    available_keys = 0
    
    for i, key in enumerate(keys):
        usage = GEMINI_KEYS_ROTATION['usage_count'].get(key, 0)
        total_usage += usage
        
        # Verificar se a chave ainda esta disponivel
        is_available = usage < 250
        if is_available:
            available_keys += 1
        
        status = "Disponivel" if is_available else "Esgotada"
        
        print(f"Chave {i+1:2d}: {key[:20]}... | Uso: {usage:3d}/250 | Status: {status}")
    
    print("-" * 60)
    print(f"Uso total: {total_usage} requisicoes")
    print(f"Chaves disponiveis: {available_keys}/{len(keys)}")
    
    # Verificar se ha fallback disponivel
    try:
        from routes.automations import get_fallback_provider_info
        fallback = get_fallback_provider_info()
        if fallback:
            print(f"Fallback disponivel: {fallback['provider']} (prioridade {fallback['priority']})")
        else:
            print("Nenhum fallback disponivel")
    except Exception as e:
        print(f"Erro ao verificar fallback: {e}")
    
    print("=" * 60)
    
    # Verificar status do sistema
    print("\nVERIFICACAO DO SISTEMA:")
    print("-" * 30)
    
    # Verificar disponibilidade do Gemini
    try:
        from routes.automations import check_gemini_availability
        gemini_available = check_gemini_availability()
        print(f"Gemini disponivel: {'Sim' if gemini_available else 'Nao'}")
    except Exception as e:
        print(f"Erro ao verificar disponibilidade do Gemini: {e}")
    
    # Verificar quantidade de chaves
    try:
        key_count = get_gemini_keys_count()
        print(f"Quantidade de chaves: {key_count}")
    except Exception as e:
        print(f"Erro ao contar chaves: {e}")
    
    print("=" * 60)
    
except Exception as e:
    print(f"Erro ao executar script: {e}")
    import traceback
    traceback.print_exc()