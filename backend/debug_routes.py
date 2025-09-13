import sys
import os

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from flask import url_for

# Registrar blueprints
from app import register_blueprints
register_blueprints()

print("=== Rotas registradas no Flask ===")
with app.app_context():
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule.rule} - {list(rule.methods)}")

print("\n=== Tentando gerar URL para get_saved_channels ===")
try:
    with app.app_context():
        url = url_for('settings.get_saved_channels')
        print(f"URL gerada: {url}")
except Exception as e:
    print(f"Erro ao gerar URL: {e}")