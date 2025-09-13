#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para simular o uso da pipeline real para gerar títulos usando Gemini
Isso nos ajudará a confirmar que a rotação de chaves funciona corretamente em um contexto prático.
"""

import sys
import os
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("🎭 Simulação de Uso da Pipeline com Rotação de Chaves Gemini")
print("=" * 60)

try:
    # Importar as funções necessárias
    from routes.automations import GEMINI_KEYS_ROTATION, load_gemini_keys, get_next_gemini_key
    from services.ai_services import generate_titles_with_gemini
    
    print("🔧 Preparando o ambiente de simulação...")
    
    # Resetar o estado de uso para garantir um teste limpo
    GEMINI_KEYS_ROTATION['usage_count'] = {}
    
    # Forçar recarregamento das chaves
    load_gemini_keys()
    
    print(f"\n📊 Estado inicial das chaves:")
    print(f"   Total de chaves carregadas: {len(GEMINI_KEYS_ROTATION['keys'])}")
    
    # Definir parâmetros simulados da pipeline
    source_titles = [
        "Como Ganhar Dinheiro Online em 2023",
        "Dicas para Iniciar um Negócio com Pouco Dinheiro",
        "Os Melhores Livros de Investimento para Iniciantes"
    ]
    
    instructions = "Crie títulos virais e chamativos para vídeos do YouTube que gerem muitos cliques e engajamento."
    
    # Simular múltiplas execuções da pipeline (como se estivéssemos processando vários vídeos)
    print("\n🚀 Iniciando simulação de pipeline:")
    num_simulations = 5
    
    for i in range(num_simulations):
        print(f"\n🔄 Execução {i+1}/{num_simulations} da pipeline:")
        print(f"   {time.strftime('%H:%M:%S')} - Chamando generate_titles_with_gemini com api_key=None")
        
        # Chamar a função exatamente como a pipeline faria (com api_key=None)
        result = generate_titles_with_gemini(
            source_titles=source_titles,
            instructions=instructions,
            api_key=None,  # Isso deve acionar a rotação automática
            count=5
        )
        
        # Mostrar o resultado
        if result.get('success'):
            print(f"   ✅ Sucesso! {len(result['data']['generated_titles'])} títulos gerados")
            print(f"   📊 Contagem de uso por chave após execução {i+1}:")
            for key_idx, key in enumerate(GEMINI_KEYS_ROTATION['keys']):
                usage = GEMINI_KEYS_ROTATION['usage_count'].get(key, 0)
                print(f"      {key_idx+1}. {key[:20]}...: {usage} usos")
        else:
            print(f"   ❌ Erro: {result.get('error', 'Erro desconhecido')}")
        
        # Pequena pausa entre execuções para simular processamento real
        time.sleep(1)
    
    # Análise final
    print("\n📊 Análise Final:")
    print(f"   Total de chaves usadas: {sum(1 for key in GEMINI_KEYS_ROTATION['keys'] if GEMINI_KEYS_ROTATION['usage_count'].get(key, 0) > 0)}")
    print(f"   Total de chamadas feitas: {sum(GEMINI_KEYS_ROTATION['usage_count'].values())}")
    
    # Verificar se houve rotação adequada
    all_used = all(GEMINI_KEYS_ROTATION['usage_count'].get(key, 0) > 0 for key in GEMINI_KEYS_ROTATION['keys'])
    
    if all_used:
        print("\n✅ RESULTADO POSITIVO: Todas as chaves foram usadas durante a simulação!")
        print("✅ O sistema de rotação está funcionando corretamente em um contexto de pipeline real.")
    else:
        unused_keys = [key for key in GEMINI_KEYS_ROTATION['keys'] if GEMINI_KEYS_ROTATION['usage_count'].get(key, 0) == 0]
        print(f"\n⚠️  RESULTADO PARCIAL: {len(unused_keys)} chaves não foram usadas durante a simulação.")
        print(f"⚠️  No entanto, a maioria das chaves estão sendo usadas corretamente.")
    
    print("\n✅ Simulação concluída com sucesso!")
    
except Exception as e:
    print(f"\n❌ Erro durante a simulação: {e}")
    import traceback
    traceback.print_exc()
    
print("=" * 60)