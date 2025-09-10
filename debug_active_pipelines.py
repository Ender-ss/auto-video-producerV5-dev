#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 Debug Active Pipelines
Script para investigar o estado atual dos pipelines ativos em memória
"""

import sys
import os
import json
from datetime import datetime

# Adicionar o diretório backend ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def debug_active_pipelines():
    """Debugar pipelines ativos em memória"""
    print("🔍 [DEBUG] Investigando pipelines ativos em memória...")
    print("=" * 60)
    
    try:
        # Importar a variável global active_pipelines
        from routes.pipeline_complete import active_pipelines, pipeline_logs
        
        print(f"📊 Total de pipelines ativos em memória: {len(active_pipelines)}")
        print(f"📊 Total de logs de pipelines: {len(pipeline_logs)}")
        print()
        
        if not active_pipelines:
            print("✅ Nenhum pipeline ativo encontrado em memória")
        else:
            print("📋 Pipelines ativos encontrados:")
            print("-" * 40)
            
            for pipeline_id, pipeline_data in active_pipelines.items():
                print(f"🔹 Pipeline ID: {pipeline_id}")
                print(f"   Status: {pipeline_data.get('status', 'N/A')}")
                print(f"   Iniciado em: {pipeline_data.get('started_at', 'N/A')}")
                print(f"   Progresso: {pipeline_data.get('progress', 0)}%")
                print(f"   Etapa atual: {pipeline_data.get('current_step', 'N/A')}")
                
                # Verificar se é a pipeline específica
                if '2025-09-09-009' in pipeline_id:
                    print(f"   ⚠️  PIPELINE ENCONTRADA: {pipeline_id}")
                    print(f"   📄 Dados completos:")
                    print(json.dumps(pipeline_data, indent=4, default=str, ensure_ascii=False))
                
                print()
        
        # Verificar logs específicos
        if pipeline_logs:
            print("📝 Logs de pipelines:")
            print("-" * 40)
            
            for pipeline_id, logs in pipeline_logs.items():
                if '2025-09-09-009' in pipeline_id:
                    print(f"🔹 Logs para {pipeline_id}: {len(logs)} entradas")
                    if logs:
                        print("   Últimos 3 logs:")
                        for log in logs[-3:]:
                            print(f"     - {log}")
                    print()
        
    except ImportError as e:
        print(f"❌ Erro ao importar módulos: {e}")
        print("   Tentando abordagem alternativa...")
        
        # Tentar verificar se há arquivos de estado persistente
        check_persistent_state()
    
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()

def check_persistent_state():
    """Verificar se há estado persistente em arquivos"""
    print("\n🔍 Verificando estado persistente...")
    
    # Verificar se há arquivos de cache ou estado
    possible_cache_files = [
        'pipeline_state.json',
        'active_pipelines.json',
        'cache/pipelines.json',
        'temp/pipeline_state.json',
        'backend/pipeline_state.json',
        'backend/cache/pipelines.json'
    ]
    
    for cache_file in possible_cache_files:
        full_path = os.path.join(os.path.dirname(__file__), cache_file)
        if os.path.exists(full_path):
            print(f"📁 Arquivo de cache encontrado: {cache_file}")
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if '2025-09-09-009' in str(data):
                        print(f"   ⚠️  Pipeline #2025-09-09-009 encontrada no arquivo!")
                        print(f"   📄 Conteúdo: {json.dumps(data, indent=2, default=str, ensure_ascii=False)}")
            except Exception as e:
                print(f"   ❌ Erro ao ler arquivo: {e}")
    
    # Verificar se há variáveis de ambiente
    env_vars = [key for key in os.environ.keys() if 'pipeline' in key.lower()]
    if env_vars:
        print(f"🌍 Variáveis de ambiente relacionadas a pipeline: {env_vars}")
        for var in env_vars:
            if '2025-09-09-009' in os.environ.get(var, ''):
                print(f"   ⚠️  Pipeline encontrada em {var}: {os.environ[var]}")

def check_database_with_context():
    """Verificar estado no banco de dados com contexto da aplicação"""
    print("\n🗄️  Verificando estado no banco de dados...")
    
    try:
        # Importar app e criar contexto
        from app import app, db, Pipeline
        
        with app.app_context():
            if Pipeline:
                # Buscar pipeline específica por display_name
                pipeline = Pipeline.query.filter(
                    Pipeline.display_name.like('%2025-09-09-009%')
                ).first()
                
                if pipeline:
                    print(f"📋 Pipeline encontrada no banco por display_name:")
                    print(f"   ID: {pipeline.pipeline_id}")
                    print(f"   Display Name: {pipeline.display_name}")
                    print(f"   Status: {pipeline.status}")
                    print(f"   Criada em: {pipeline.created_at}")
                    print(f"   Iniciada em: {pipeline.started_at}")
                    return
                
                # Buscar por pipeline_id
                pipeline = Pipeline.query.filter(
                    Pipeline.pipeline_id.like('%2025-09-09-009%')
                ).first()
                
                if pipeline:
                    print(f"📋 Pipeline encontrada no banco por pipeline_id:")
                    print(f"   ID: {pipeline.pipeline_id}")
                    print(f"   Display Name: {pipeline.display_name}")
                    print(f"   Status: {pipeline.status}")
                    print(f"   Criada em: {pipeline.created_at}")
                    print(f"   Iniciada em: {pipeline.started_at}")
                    return
                
                # Buscar todas as pipelines recentes
                recent_pipelines = Pipeline.query.order_by(
                    Pipeline.created_at.desc()
                ).limit(10).all()
                
                print(f"📋 Últimas 10 pipelines no banco:")
                for p in recent_pipelines:
                    print(f"   - {p.display_name or p.pipeline_id} ({p.status}) - {p.created_at}")
                    if '2025-09-09-009' in (p.display_name or '') or '2025-09-09-009' in (p.pipeline_id or ''):
                        print(f"     ⚠️  PIPELINE ENCONTRADA!")
                
                print("\n✅ Pipeline #2025-09-09-009 não encontrada no banco")
            else:
                print("❌ Modelo Pipeline não disponível")
    
    except Exception as e:
        print(f"❌ Erro ao verificar banco: {e}")
        import traceback
        traceback.print_exc()

def check_frontend_localStorage():
    """Verificar se há dados no localStorage do frontend"""
    print("\n🌐 Verificando possível persistência no frontend...")
    
    # Verificar se há arquivos HTML de debug
    debug_files = [
        'debug_localStorage.html',
        'test_localStorage.html',
        'tests/debug_localStorage.html',
        'tests/test_localStorage.html'
    ]
    
    for debug_file in debug_files:
        full_path = os.path.join(os.path.dirname(__file__), debug_file)
        if os.path.exists(full_path):
            print(f"📁 Arquivo de debug localStorage encontrado: {debug_file}")
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if '2025-09-09-009' in content:
                        print(f"   ⚠️  Pipeline #2025-09-09-009 encontrada no arquivo!")
                        # Extrair linhas relevantes
                        lines = content.split('\n')
                        for i, line in enumerate(lines):
                            if '2025-09-09-009' in line:
                                print(f"   Linha {i+1}: {line.strip()}")
            except Exception as e:
                print(f"   ❌ Erro ao ler arquivo: {e}")

if __name__ == "__main__":
    print(f"🚀 Iniciando debug em {datetime.now()}")
    debug_active_pipelines()
    check_persistent_state()
    check_database_with_context()
    check_frontend_localStorage()
    print("\n✅ Debug concluído")
    
    print("\n💡 CONCLUSÕES:")
    print("   1. Se a pipeline aparece no polling mas não está em memória,")
    print("      pode estar sendo carregada do banco de dados ou localStorage")
    print("   2. Verifique os logs do frontend para entender de onde vem")
    print("   3. A pipeline pode ter sido criada mas não removida adequadamente")