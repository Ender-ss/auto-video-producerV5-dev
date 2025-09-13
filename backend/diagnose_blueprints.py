from app import app
import inspect

print("=== Blueprint Registration Diagnosis ===")
print(f"Total blueprints registered: {len(app.blueprints)}")
print("Blueprint names:", list(app.blueprints.keys()))

# Check if settings blueprint is registered
if 'settings' in app.blueprints:
    print("\nSettings blueprint is registered")
    settings_bp = app.blueprints['settings']
    print(f"Settings blueprint object: {settings_bp}")
    print(f"Settings blueprint name: {settings_bp.name}")
    
    # Check routes in settings blueprint
    print("\nRoutes in settings blueprint:")
    count = 0
    for rule in app.url_map.iter_rules():
        if rule.endpoint.startswith('settings.'):
            print(f"  {rule.rule} -> {rule.endpoint}")
            count += 1
    print(f"Total settings routes found: {count}")
else:
    print("\nSettings blueprint is NOT registered")

# Check all routes with their endpoints
print("\n=== All Routes with Endpoints ===")
for rule in app.url_map.iter_rules():
    if 'settings' in rule.endpoint:
        print(f"  {rule.rule} -> {rule.endpoint}")