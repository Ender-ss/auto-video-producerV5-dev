#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Investigação da Pipeline #2025-09-09-009
Problemas identificados:
1. Pipeline aparece no layout mas não é encontrada no sistema
2. Logs detalhados sendo sobrescritos
"""

import sqlite3
import os
import json
from datetime import datetime

def investigate_pipeline_issue():
    """Investigar problemas com Pipeline #2025-09-09-009"""
    
    print("🔍 INVESTIGAÇÃO: Pipeline #2025-09-09-009")
    print("=" * 60)
    
    # Verificar todos os bancos de dados disponíveis
    db_paths = [
        'backend/instance/auto_video_producer.db',
        'backend/var/app-instance/auto_video_producer.db',
        'instance/auto_video_producer.db',
        'backend/config/channels.db',
        'backend/config/prompts.db'
    ]
    
    found_pipelines = []
    
    for db_path in db_paths:
        if os.path.exists(db_path):
            print(f"\n📂 Verificando banco: {db_path}")
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                # Listar tabelas
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = [table[0] for table in cursor.fetchall()]
                print(f"   Tabelas: {', '.join(tables)}")
                
                # Buscar em tabelas relacionadas a pipelines
                pipeline_tables = [t for t in tables if 'pipeline' in t.lower()]
                
                for table in pipeline_tables:
                    print(f"\n   🔍 Buscando em tabela: {table}")
                    try:
                        # Buscar por 2025-09-09-009
                        cursor.execute(f"SELECT * FROM {table} WHERE CAST({table} AS TEXT) LIKE '%2025-09-09-009%'")
                        results = cursor.fetchall()
                        
                        if results:
                            print(f"   ✅ Encontrado {len(results)} registros em {table}")
                            
                            # Obter nomes das colunas
                            cursor.execute(f"PRAGMA table_info({table})")
                            columns = [col[1] for col in cursor.fetchall()]
                            
                            for row in results:
                                pipeline_data = dict(zip(columns, row))
                                found_pipelines.append({
                                    'database': db_path,
                                    'table': table,
                                    'data': pipeline_data
                                })
                                
                                print(f"   📋 Dados encontrados:")
                                for key, value in pipeline_data.items():
                                    if value and '2025-09-09-009' in str(value):
                                        print(f"      {key}: {value}")
                        
                        # Buscar pipelines recentes para comparação
                        cursor.execute(f"SELECT * FROM {table} ORDER BY rowid DESC LIMIT 5")
                        recent = cursor.fetchall()
                        
                        if recent:
                            print(f"   📅 Últimos 5 registros em {table}:")
                            cursor.execute(f"PRAGMA table_info({table})")
                            columns = [col[1] for col in cursor.fetchall()]
                            
                            for row in recent:
                                data = dict(zip(columns, row))
                                # Mostrar apenas campos relevantes
                                relevant_fields = ['id', 'pipeline_id', 'display_name', 'title', 'status', 'created_at', 'started_at']
                                row_info = {k: v for k, v in data.items() if k in relevant_fields and v}
                                if row_info:
                                    print(f"      {row_info}")
                    
                    except Exception as e:
                        print(f"   ❌ Erro ao buscar em {table}: {e}")
                
                conn.close()
                
            except Exception as e:
                print(f"   ❌ Erro ao acessar {db_path}: {e}")
        else:
            print(f"\n❌ Banco não encontrado: {db_path}")
    
    print("\n" + "=" * 60)
    print("📊 RESUMO DA INVESTIGAÇÃO")
    print("=" * 60)
    
    if found_pipelines:
        print(f"✅ Pipeline #2025-09-09-009 encontrada em {len(found_pipelines)} local(is):")
        for pipeline in found_pipelines:
            print(f"\n📍 Local: {pipeline['database']} -> {pipeline['table']}")
            data = pipeline['data']
            
            # Mostrar informações principais
            if 'display_name' in data:
                print(f"   Display Name: {data['display_name']}")
            if 'title' in data:
                print(f"   Título: {data['title']}")
            if 'status' in data:
                print(f"   Status: {data['status']}")
            if 'pipeline_id' in data:
                print(f"   Pipeline ID: {data['pipeline_id']}")
    else:
        print("❌ Pipeline #2025-09-09-009 NÃO encontrada em nenhum banco de dados")
        print("\n🔍 POSSÍVEIS CAUSAS:")
        print("   1. Pipeline existe apenas em memória (Redis/cache)")
        print("   2. Pipeline foi removida do banco de dados")
        print("   3. Problema de sincronização entre frontend e backend")
        print("   4. Pipeline está em outro local não verificado")
    
    # Investigar problema dos logs
    print("\n" + "=" * 60)
    print("📝 INVESTIGAÇÃO: Logs Detalhados")
    print("=" * 60)
    
    print("\n🔍 Analisando implementação dos logs no frontend...")
    
    # Verificar arquivo de logs do frontend
    frontend_log_file = 'frontend/src/components/PipelineProgress.jsx'
    if os.path.exists(frontend_log_file):
        with open(frontend_log_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Buscar pela implementação dos logs
        if 'slice(-10)' in content:
            print("❌ PROBLEMA IDENTIFICADO: Logs limitados a últimos 10 registros")
            print("   Linha encontrada: pipeline.logs.slice(-10)")
            print("   Isso explica por que logs antigos desaparecem")
        
        if 'max-h-40 overflow-y-auto' in content:
            print("❌ PROBLEMA IDENTIFICADO: Container de logs com altura limitada")
            print("   Classe CSS: max-h-40 overflow-y-auto")
            print("   Isso limita a visualização dos logs")
    
    print("\n💡 SOLUÇÕES RECOMENDADAS:")
    print("\n1. Para o problema da Pipeline #2025-09-09-009:")
    print("   - Verificar cache Redis")
    print("   - Implementar busca por display_name no frontend")
    print("   - Adicionar endpoint específico para busca por nome")
    
    print("\n2. Para o problema dos logs detalhados:")
    print("   - Remover limitação slice(-10) para mostrar todos os logs")
    print("   - Aumentar altura do container ou torná-lo expansível")
    print("   - Adicionar opção de download/exportação dos logs completos")
    print("   - Implementar paginação ou scroll infinito")

if __name__ == "__main__":
    investigate_pipeline_issue()