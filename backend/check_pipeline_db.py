#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar pipelines no banco de dados
"""

import os
import sys

# Adicionar o diretório backend ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configurar Flask app context
try:
    from app import app, db, Pipeline
except ImportError as e:
    print(f"❌ Erro ao importar módulos: {e}")
    sys.exit(1)

def check_all_pipelines():
    """Verificar todas as pipelines no banco de dados"""
    with app.app_context():
        try:
            pipelines = Pipeline.query.all()
            print(f"📊 Total de pipelines no banco: {len(pipelines)}")
            print("\n📋 Lista de pipelines:")
            print("-" * 80)
            
            for pipeline in pipelines:
                print(f"ID: {pipeline.pipeline_id}")
                print(f"   Nome: {pipeline.display_name or 'N/A'}")
                print(f"   Status: {pipeline.status}")
                print(f"   Progresso: {pipeline.progress}%")
                print(f"   Erro: {pipeline.error_message or 'Nenhum'}")
                print("-" * 40)
            
            # Verificar especificamente a pipeline 2025-09-09-009
            target_pipeline = Pipeline.query.filter_by(pipeline_id="2025-09-09-009").first()
            if target_pipeline:
                print(f"\n✅ Pipeline 2025-09-09-009 encontrada!")
                print(f"   Status: {target_pipeline.status}")
                print(f"   Progresso: {target_pipeline.progress}%")
                print(f"   Configuração: {target_pipeline.config_json}")
            else:
                print(f"\n❌ Pipeline 2025-09-09-009 NÃO encontrada")
                
        except Exception as e:
            print(f"❌ Erro ao consultar banco: {e}")
            import traceback
            traceback.print_exc()

def check_moviepy():
    """Verificar se MoviePy está disponível"""
    try:
        import moviepy
        print(f"✅ MoviePy disponível - versão: {moviepy.__version__}")
        return True
    except ImportError as e:
        print(f"❌ MoviePy não disponível: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Verificação de Pipelines e MoviePy")
    print("=" * 50)
    
    # Verificar MoviePy
    print("\n🎬 Verificando MoviePy...")
    moviepy_ok = check_moviepy()
    
    # Verificar pipelines
    print("\n📊 Verificando pipelines no banco...")
    check_all_pipelines()
    
    print("\n✅ Verificação concluída")