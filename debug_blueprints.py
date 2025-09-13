#!/usr/bin/env python3
"""
Script para depurar o registro de blueprints
"""

import sys
import os

# Adicionar o diretório backend ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

try:
    from routes.pipeline_complete import pipeline_complete_bp
    print("✅ Blueprint pipeline_complete_bp importado com sucesso")
    print(f"Nome do blueprint: {pipeline_complete_bp.name}")
    print(f"URL prefix: {pipeline_complete_bp.url_prefix}")
    print(f"Rotas registradas:")
    for rule in pipeline_complete_bp.deferred_functions:
        print(f"  - {rule}")
    
    # Verificar se a rota /active está registrada
    print("\nVerificando rotas específicas:")
    for rule in pipeline_complete_bp.deferred_functions:
        if hasattr(rule, '__code__') and rule.__code__.co_name == 'get_active_pipelines':
            print("✅ Rota /active encontrada no blueprint")
            break
    else:
        print("❌ Rota /active não encontrada no blueprint")
        
except Exception as e:
    print(f"❌ Erro ao importar pipeline_complete_bp: {e}")
    import traceback
    traceback.print_exc()

try:
    from app import app, register_blueprints
    print("\n✅ App Flask importado com sucesso")
    
    # Verificar se o blueprint está registrado ANTES de chamar register_blueprints
    with app.app_context():
        print("\nRotas registradas no app (ANTES do registro):")
        for rule in app.url_map.iter_rules():
            if 'pipeline' in rule.rule:
                print(f"  - {rule.rule} [{', '.join(rule.methods)}] -> {rule.endpoint}")
                
        # Verificar blueprints registrados
        print("\nBlueprints registrados (ANTES do registro):")
        for blueprint_name, blueprint in app.blueprints.items():
            if 'pipeline' in blueprint_name:
                print(f"  - {blueprint_name}: {blueprint.url_prefix}")
    
    # Chamar a função de registro de blueprints
    print("\nChamando register_blueprints()...")
    result = register_blueprints()
    print(f"Resultado do registro: {result}")
    
    # Verificar se o blueprint está registrado DEPOIS de chamar register_blueprints
    with app.app_context():
        print("\nRotas registradas no app (DEPOIS do registro):")
        for rule in app.url_map.iter_rules():
            if 'pipeline' in rule.rule:
                print(f"  - {rule.rule} [{', '.join(rule.methods)}] -> {rule.endpoint}")
                
        # Verificar blueprints registrados
        print("\nBlueprints registrados (DEPOIS do registro):")
        for blueprint_name, blueprint in app.blueprints.items():
            if 'pipeline' in blueprint_name:
                print(f"  - {blueprint_name}: {blueprint.url_prefix}")
                
        # Verificar especificamente a rota /api/pipeline/active
        print("\nVerificando rota /api/pipeline/active:")
        for rule in app.url_map.iter_rules():
            if rule.rule == '/api/pipeline/active':
                print(f"✅ Rota encontrada: {rule.rule} [{', '.join(rule.methods)}] -> {rule.endpoint}")
                break
        else:
            print("❌ Rota /api/pipeline/active não encontrada")
except Exception as e:
    print(f"❌ Erro ao importar app: {e}")
    import traceback
    traceback.print_exc()