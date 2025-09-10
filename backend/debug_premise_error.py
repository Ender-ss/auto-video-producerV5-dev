#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para debugar o erro 'premise' na geração de roteiros
"""

import sys
import os
import json
import traceback
from datetime import datetime

# Adicionar o diretório backend ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.pipeline_service import PipelineService

def debug_premise_error():
    """Debugar o erro de premise na pipeline"""
    print("🔍 INICIANDO DEBUG DO ERRO 'PREMISE'")
    print("=" * 50)
    
    try:
        # Configuração de teste
        config = {
            'extraction': {
                'method': 'manual',
                'provided_titles': ['Faxineira Descalça Vira Milionária? O Segredo do Bilhete Anônimo!']
            },
            'premises': {
                'enabled': True,
                'style': 'educational',
                'word_count': 200
            },
            'scripts': {
                'enabled': True,
                'chapters': 5,
                'style': 'inicio',
                'duration_target': '5-7 minutes',
                'include_hooks': True
            }
        }
        
        # Criar instância do pipeline service
        pipeline_id = f"debug-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        print(f"📋 Pipeline ID: {pipeline_id}")
        
        # Criar pipeline service sem carregar estado existente
        ps = PipelineService.__new__(PipelineService)
        ps.pipeline_id = pipeline_id
        ps.config = config
        ps.results = {}
        ps.pipeline_state = {
            'channel_url': 'debug-test',
            'config': config,
            'created_at': datetime.now().isoformat()
        }
        
        # Executar extração
        print("\n1️⃣ EXECUTANDO EXTRAÇÃO...")
        extraction_result = ps.run_extraction()
        print(f"✅ Extração concluída: {len(extraction_result.get('titles', []))} títulos")
        
        # Executar geração de títulos (necessário para premissas)
        print("\n2️⃣ EXECUTANDO GERAÇÃO DE TÍTULOS...")
        titles_result = ps.run_titles_generation()
        print(f"✅ Títulos gerados: {len(titles_result.get('generated_titles', []))}")
        
        # Executar geração de premissas
        print("\n3️⃣ EXECUTANDO GERAÇÃO DE PREMISSAS...")
        premises_result = ps.run_premises_generation()
        print(f"✅ Premissas concluídas")
        
        # Verificar estrutura dos resultados
        print("\n🔍 VERIFICANDO ESTRUTURA DOS RESULTADOS:")
        print(f"📊 Chaves em ps.results: {list(ps.results.keys())}")
        
        if 'premises' in ps.results:
            premises_data = ps.results['premises']
            print(f"📊 Chaves em premises: {list(premises_data.keys())}")
            
            # Verificar se 'premise' existe
            if 'premise' in premises_data:
                print(f"✅ 'premise' encontrado: {premises_data['premise'][:100]}...")
            else:
                print("❌ 'premise' NÃO encontrado!")
                
            # Verificar estrutura de 'premises' (array)
            if 'premises' in premises_data and isinstance(premises_data['premises'], list):
                if len(premises_data['premises']) > 0:
                    first_premise = premises_data['premises'][0]
                    print(f"📊 Chaves no primeiro item de premises: {list(first_premise.keys())}")
                    if 'premise' in first_premise:
                        print(f"✅ 'premise' encontrado no array: {first_premise['premise'][:100]}...")
                    else:
                        print("❌ 'premise' NÃO encontrado no array!")
        
        # Tentar executar geração de roteiros
        print("\n4️⃣ EXECUTANDO GERAÇÃO DE ROTEIROS...")
        try:
            scripts_result = ps.run_scripts_generation()
            print(f"✅ Roteiros concluídos com sucesso!")
            print(f"📊 Chaves no resultado: {list(scripts_result.keys())}")
        except Exception as e:
            print(f"❌ ERRO na geração de roteiros: {str(e)}")
            print(f"🔍 Tipo do erro: {type(e).__name__}")
            
            # Mostrar traceback completo
            print("\n📋 TRACEBACK COMPLETO:")
            traceback.print_exc()
            
            # Tentar acessar a premissa manualmente
            print("\n🔧 TENTANDO ACESSAR PREMISSA MANUALMENTE:")
            try:
                premise_data = ps.results['premises']
                title = premise_data['selected_title']
                print(f"📝 Título: {title}")
                
                # Testar diferentes formas de acessar a premissa
                premise_methods = [
                    ("premise_data.get('premise')", lambda: premise_data.get('premise')),
                    ("premise_data.get('premises', [{}])[0].get('premise')", lambda: premise_data.get('premises', [{}])[0].get('premise')),
                    ("title (fallback)", lambda: title)
                ]
                
                for method_name, method_func in premise_methods:
                    try:
                        result = method_func()
                        if result:
                            print(f"✅ {method_name}: {result[:100]}...")
                            break
                        else:
                            print(f"❌ {method_name}: None ou vazio")
                    except Exception as method_error:
                        print(f"❌ {method_name}: ERRO - {str(method_error)}")
                        
            except Exception as access_error:
                print(f"❌ Erro ao acessar dados: {str(access_error)}")
    
    except Exception as e:
        print(f"❌ ERRO GERAL: {str(e)}")
        traceback.print_exc()
    
    print("\n" + "=" * 50)
    print("🏁 DEBUG CONCLUÍDO")

if __name__ == "__main__":
    debug_premise_error()