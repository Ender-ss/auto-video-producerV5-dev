import sys
import os
import traceback

# Add the backend directory to the path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from app import app

def debug_blueprint_registration():
    print('=== Blueprint Registration Debug ===')
    
    # Check what blueprints are already registered
    print('Already registered blueprints:')
    for name, blueprint in app.blueprints.items():
        print(f'  {name}: {blueprint}')
    
    print('\nTrying to register blueprints one by one...')
    
    # Try importing and registering each blueprint
    blueprints_to_register = [
        ('automations', 'routes.automations', 'automations_bp', '/api/automations'),
        ('settings', 'routes.settings', 'settings_bp', '/api/settings'),
        ('premise', 'routes.premise', 'premise_bp', '/api/premise'),
        ('scripts', 'routes.scripts', 'scripts_bp', '/api/scripts'),
        ('workflow', 'routes.workflow', 'workflow_bp', '/api/workflow'),
        ('channels', 'routes.channels', 'channels_bp', '/api/channels'),
        ('pipelines', 'routes.pipelines', 'pipelines_bp', '/api/pipelines'),
        ('pipeline_complete', 'routes.pipeline_complete', 'pipeline_complete_bp', '/api/pipeline'),
        ('videos', 'routes.videos', 'videos_bp', '/api/videos'),
        ('system', 'routes.system', 'system_bp', '/api/system'),
        ('tests', 'routes.tests', 'tests_bp', '/api/tests'),
        ('images', 'routes.images', 'images_bp', '/api/images'),
        ('image_queue', 'routes.image_queue', 'image_queue_bp', '/api/image-queue'),
        ('prompts_config', 'routes.prompts_config', 'prompts_config_bp', '/api'),
        ('storyteller', 'routes.storyteller', 'storyteller_bp', None)  # Already has url_prefix
    ]
    
    for bp_name, module_path, bp_var, url_prefix in blueprints_to_register:
        try:
            print(f'\nTrying to register {bp_name}...')
            
            # Import the blueprint
            module = __import__(module_path, fromlist=[bp_var])
            blueprint = getattr(module, bp_var)
            
            print(f'  Blueprint name: {blueprint.name}')
            print(f'  Blueprint variable: {bp_var}')
            
            # Check if already registered
            if blueprint.name in app.blueprints:
                print(f'  ❌ Blueprint {blueprint.name} already registered!')
                continue
            
            # Register the blueprint
            if url_prefix:
                app.register_blueprint(blueprint, url_prefix=url_prefix)
            else:
                app.register_blueprint(blueprint)
                
            print(f'  ✅ Registered {blueprint.name} successfully')
            
        except Exception as e:
            print(f'  ❌ Error with {bp_name}: {e}')
            traceback.print_exc()

if __name__ == '__main__':
    with app.app_context():
        debug_blueprint_registration()
        
        # List all registered routes after registration attempt
        print('\n=== Registered Routes ===')
        settings_routes = []
        for rule in app.url_map.iter_rules():
            if rule.rule.startswith('/api/settings'):
                settings_routes.append(rule.rule)
                
        if settings_routes:
            print('Settings routes found:')
            for route in settings_routes:
                print(f'  {route}')
        else:
            print('No settings routes found')