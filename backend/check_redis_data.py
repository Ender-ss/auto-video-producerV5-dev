#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar dados do Redis que possam conter "Arthur Blackwood"
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import redis
    import json
    from services.redis_cache_service import cache_service
except ImportError as e:
    print(f"❌ Erro de importação: {e}")
    print("💡 Tentando verificação sem Redis...")
    cache_service = None

def check_redis_for_arthur():
    """Verifica se há dados no Redis contendo Arthur Blackwood"""
    print("🔍 VERIFICANDO DADOS DO REDIS")
    print("=" * 50)
    
    if not cache_service or not cache_service.connected:
        print("❌ Redis não está conectado")
        print("💡 Verificando cache em memória...")
        
        if hasattr(cache_service, '_memory_cache'):
            memory_cache = cache_service._memory_cache
            print(f"📊 Cache em memória tem {len(memory_cache)} entradas")
            
            arthur_found = False
            for key, value in memory_cache.items():
                value_str = str(value).lower()
                if 'arthur' in value_str or 'blackwood' in value_str:
                    print(f"⚠️  ENCONTRADO em cache de memória:")
                    print(f"   Chave: {key}")
                    print(f"   Valor: {value}")
                    arthur_found = True
            
            if not arthur_found:
                print("✅ Nenhuma referência a Arthur Blackwood no cache de memória")
        else:
            print("✅ Nenhum cache em memória encontrado")
        return
    
    try:
        # Conecta ao Redis
        redis_client = cache_service.redis_client
        
        # Lista todas as chaves
        all_keys = redis_client.keys('*')
        print(f"📊 Total de chaves no Redis: {len(all_keys)}")
        
        arthur_found = False
        
        for key in all_keys:
            try:
                # Obtém o valor
                value = redis_client.get(key)
                if value:
                    # Verifica se contém Arthur Blackwood
                    value_str = str(value).lower()
                    if 'arthur' in value_str or 'blackwood' in value_str:
                        print(f"⚠️  ENCONTRADO no Redis:")
                        print(f"   Chave: {key}")
                        print(f"   Valor: {value[:200]}...")  # Primeiros 200 chars
                        arthur_found = True
                        
                        # Tenta fazer parse JSON para ver estrutura
                        try:
                            parsed = json.loads(value)
                            print(f"   Estrutura JSON: {type(parsed)}")
                            if isinstance(parsed, dict):
                                for k, v in parsed.items():
                                    if 'arthur' in str(v).lower() or 'blackwood' in str(v).lower():
                                        print(f"     Campo '{k}': {v}")
                        except:
                            pass
                        print()
            except Exception as e:
                print(f"❌ Erro ao verificar chave {key}: {e}")
        
        if not arthur_found:
            print("✅ Nenhuma referência a Arthur Blackwood encontrada no Redis")
            
        # Mostra estatísticas do cache
        stats = cache_service.get_cache_stats()
        print(f"\n📊 ESTATÍSTICAS DO CACHE:")
        for key, value in stats.items():
            print(f"   {key}: {value}")
            
    except Exception as e:
        print(f"❌ Erro ao verificar Redis: {e}")

def check_specific_patterns():
    """Verifica padrões específicos que podem conter dados antigos"""
    print("\n🔍 VERIFICANDO PADRÕES ESPECÍFICOS")
    print("=" * 50)
    
    if not cache_service or not cache_service.connected:
        print("❌ Redis não conectado, pulando verificação de padrões")
        return
        
    patterns_to_check = [
        'premise:*',
        'story:*', 
        'breakpoints:*',
        'chapter:*',
        'context:*',
        'cache:*'
    ]
    
    try:
        redis_client = cache_service.redis_client
        
        for pattern in patterns_to_check:
            keys = redis_client.keys(pattern)
            print(f"📋 Padrão '{pattern}': {len(keys)} chaves")
            
            for key in keys[:5]:  # Verifica apenas as primeiras 5 de cada padrão
                try:
                    value = redis_client.get(key)
                    if value and ('arthur' in str(value).lower() or 'blackwood' in str(value).lower()):
                        print(f"   ⚠️  ENCONTRADO em {key}")
                        print(f"      Valor: {str(value)[:100]}...")
                except Exception as e:
                    print(f"   ❌ Erro ao verificar {key}: {e}")
                    
    except Exception as e:
        print(f"❌ Erro ao verificar padrões: {e}")

def clear_suspicious_data():
    """Limpa dados suspeitos se encontrados"""
    print("\n🧹 LIMPEZA DE DADOS SUSPEITOS")
    print("=" * 50)
    
    if not cache_service or not cache_service.connected:
        print("❌ Redis não conectado, limpeza limitada")
        
        # Limpa cache em memória se existir
        if hasattr(cache_service, '_memory_cache'):
            cache_service._memory_cache.clear()
            print("✅ Cache em memória limpo")
        return
    
    try:
        # Limpa todos os caches relacionados a histórias/premissas
        patterns_to_clear = [
            'premise:*',
            'story:*', 
            'context:*'
        ]
        
        total_cleared = 0
        redis_client = cache_service.redis_client
        
        for pattern in patterns_to_clear:
            keys = redis_client.keys(pattern)
            if keys:
                deleted = redis_client.delete(*keys)
                total_cleared += deleted
                print(f"🗑️  Padrão '{pattern}': {deleted} chaves removidas")
        
        print(f"\n✅ Total de {total_cleared} chaves removidas do Redis")
        
        # Também limpa o cache de breakpoints por segurança
        breakpoints_cleared = cache_service.clear_cache()
        print(f"✅ Cache de breakpoints limpo: {breakpoints_cleared} chaves")
        
    except Exception as e:
        print(f"❌ Erro na limpeza: {e}")

if __name__ == "__main__":
    print("🚀 VERIFICAÇÃO COMPLETA DO REDIS")
    print("=" * 50)
    
    # 1. Verifica dados atuais
    check_redis_for_arthur()
    
    # 2. Verifica padrões específicos
    check_specific_patterns()
    
    # 3. Limpa dados suspeitos
    clear_suspicious_data()
    
    print("\n🎉 VERIFICAÇÃO CONCLUÍDA!")
    print("💡 Se o problema persistir, pode ser:")
    print("   1. Dados vindos da API externa (Gemini/OpenAI)")
    print("   2. Exemplos em prompts de sistema não detectados")
    print("   3. Cache de modelo de linguagem")
    print("   4. Dados persistentes em banco de dados")