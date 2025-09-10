#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧹 Script para Limpar Cache de Premissas

Este script limpa todo o cache de premissas para forçar a regeneração
com as novas validações de nomes implementadas.
"""

import sys
import os
from pathlib import Path

# Adicionar o diretório backend ao path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from services.premise_cache import PremiseCache
from services.name_validator import NameValidator

def main():
    print("🧹 LIMPANDO CACHE DE PREMISSAS")
    print("=" * 50)
    
    # Inicializar cache
    cache = PremiseCache()
    
    # Obter estatísticas antes da limpeza
    stats_before = cache.get_cache_stats()
    print(f"📊 Estatísticas antes da limpeza:")
    print(f"   - Total de entradas: {stats_before['total_entries']}")
    print(f"   - Tamanho total: {stats_before['total_size_mb']} MB")
    print(f"   - Por origem: {stats_before['by_prompt_source']}")
    
    # Limpar cache
    print("\n🗑️ Limpando cache...")
    success = cache.clear_cache()
    
    if success:
        print("✅ Cache limpo com sucesso!")
    else:
        print("❌ Erro ao limpar cache")
        return
    
    # Verificar estatísticas após limpeza
    stats_after = cache.get_cache_stats()
    print(f"\n📊 Estatísticas após limpeza:")
    print(f"   - Total de entradas: {stats_after['total_entries']}")
    print(f"   - Tamanho total: {stats_after['total_size_mb']} MB")
    
    # Também limpar cache antigo do Gemini se existir
    old_cache_dir = Path("cache/gemini_premises")
    if old_cache_dir.exists():
        print(f"\n🗑️ Limpando cache antigo do Gemini...")
        try:
            import shutil
            shutil.rmtree(old_cache_dir)
            print("✅ Cache antigo do Gemini removido")
        except Exception as e:
            print(f"⚠️ Erro ao remover cache antigo: {e}")
    
    # Verificar sistema de validação
    print(f"\n🔍 Verificando sistema de validação...")
    validator = NameValidator()
    
    # Testar com texto contendo Arthur Blackwood
    test_text = "Arthur Blackwood era um homem rico que vivia sozinho."
    validation_result = validator.validate_premise(test_text)
    
    print(f"📝 Teste de validação:")
    print(f"   - Texto: {test_text}")
    print(f"   - É válido: {validation_result['is_valid']}")
    print(f"   - Problemas: {validation_result['issues']}")
    print(f"   - Nomes proibidos: {validation_result['forbidden_names']}")
    print(f"   - Sugestões: {validation_result['suggestions']}")
    
    if not validation_result['is_valid'] and validation_result['suggestions']:
        cleaned_text = validator.clean_premise_text(
            test_text,
            validation_result['forbidden_names'],
            validation_result['suggestions']
        )
        print(f"   - Texto corrigido: {cleaned_text}")
    
    print(f"\n✅ Limpeza concluída! Agora todas as premissas serão geradas novamente com validação.")

if __name__ == "__main__":
    main()