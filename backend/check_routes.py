import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app

# List all registered routes
with app.app_context():
    print("Registered routes:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.rule} -> {rule.endpoint}")