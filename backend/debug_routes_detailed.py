#!/usr/bin/env python3
"""
Script para debug detalhado das rotas do Flask
"""
import sys
import os

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

def list_all_routes():
    """Listar todas as rotas registradas no Flask"""
    print("=== ROTAS REGISTRADAS ===")
    
    with app.app_context():
        rules = list(app.url_map.iter_rules())
        
        if not rules:
            print("❌ Nenhuma rota encontrada!")
            return
            
        print(f"Total de rotas: {len(rules)}")
        print()
        
        for rule in rules:
            methods = ','.join(sorted(rule.methods))
            print(f"{rule.endpoint:30} {methods:20} {rule}")

def test_settings_routes():
    """Verificar rotas específicas de settings"""
    print("\n=== VERIFICANDO ROTAS DE SETTINGS ===")
    
    with app.app_context():
        # Buscar rotas que contenham "settings"
        settings_routes = []
        for rule in app.url_map.iter_rules():
            if 'settings' in str(rule) or 'settings' in rule.endpoint:
                settings_routes.append(rule)
        
        if settings_routes:
            print(f"Encontradas {len(settings_routes)} rotas de settings:")
            for rule in settings_routes:
                methods = ','.join(sorted(rule.methods))
                print(f"  {rule.endpoint:30} {methods:20} {rule}")
        else:
            print("❌ Nenhuma rota de settings encontrada!")
            
        # Verificar se há blueprints registrados
        print(f"\nBlueprints registrados: {list(app.blueprints.keys())}")
        
        # Verificar imports de settings
        try:
            from routes.settings import settings_bp
            print(f"✅ settings_bp importado com sucesso")
            print(f"   Nome do blueprint: {settings_bp.name}")
            print(f"   URL prefix: {settings_bp.url_prefix}")
        except ImportError as e:
            print(f"❌ Erro ao importar settings_bp: {e}")

if __name__ == '__main__':
    print("Iniciando debug de rotas...")
    list_all_routes()
    test_settings_routes()
    print("\n=== FIM DO DEBUG ===")