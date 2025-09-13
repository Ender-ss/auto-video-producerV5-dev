#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from routes.automations import load_gemini_keys, GEMINI_KEYS_ROTATION
from datetime import datetime

print("==== STATUS DAS CHAVES GEMINI ====")

# Carregar chaves
load_gemini_keys()

print(f"\n📊 INFORMAÇÕES GERAIS:")
print(f"Total de chaves carregadas: {len(GEMINI_KEYS_ROTATION['keys'])}")
print(f"Data do último reset: {GEMINI_KEYS_ROTATION['last_reset']}")
print(f"Data atual: {datetime.now().date()}")

# Verificar se houve reset hoje
if GEMINI_KEYS_ROTATION['last_reset'] != datetime.now().date():
    print("⚠️  O sistema não resetou as contagens hoje!")

print(f"\n📋 DETALHES DAS CHAVES:")

# Verificar cada chave
for i, key in enumerate(GEMINI_KEYS_ROTATION['keys']):
    usage = GEMINI_KEYS_ROTATION['usage_count'].get(key, 0)
    
    # Nome da chave no arquivo de configuração
    key_name = f"gemini_{i+1}"
    
    print(f"Chave {i+1} ({key_name}): {key[:20]}... (uso: {usage})")

print(f"\n🏁 Total de chaves disponíveis: {len(GEMINI_KEYS_ROTATION['keys'])}")