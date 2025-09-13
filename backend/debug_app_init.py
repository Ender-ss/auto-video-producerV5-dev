import sys
import os
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Add the backend directory to the path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

# Import app but patch the register_blueprints function to show errors
from app import app

# Save the original register_blueprints function
from app import register_blueprints as original_register_blueprints

def debug_register_blueprints():
    """Debug version of register_blueprints that shows detailed errors"""
    print("=== Debug Register Blueprints ===")
    
    try:
        from routes.automations import automations_bp, load_rapidapi_keys, load_gemini_keys
        from routes.premise import premise_bp
        from routes.scripts import scripts_bp
        from routes.workflow import workflow_bp
        from routes.channels import channels_bp
        from routes.pipelines import pipelines_bp
        from routes.pipeline_complete import pipeline_complete_bp
        from routes.videos import videos_bp
        from routes.settings import settings_bp
        from routes.system import system_bp
        from routes.tests import tests_bp
        from routes.images import images_bp
        from routes.image_queue import image_queue_bp
        from routes.prompts_config import prompts_config_bp
        from routes.storyteller import storyteller_bp

        print("✅ All blueprints imported successfully")
        
        # Carregar chaves na inicialização
        load_rapidapi_keys()
        print("✅ Chaves RapidAPI carregadas na inicialização!")
        
        load_gemini_keys()
        print("✅ Chaves Gemini carregadas na inicialização!")

        # Register blueprints one by one to identify which one fails
        blueprints = [
            (automations_bp, '/api/automations', 'automations'),
            (premise_bp, '/api/premise', 'premise'),
            (scripts_bp, '/api/scripts', 'scripts'),
            (workflow_bp, '/api/workflow', 'workflow'),
            (channels_bp, '/api/channels', 'channels'),
            (pipelines_bp, '/api/pipelines', 'pipelines'),
            (pipeline_complete_bp, '/api/pipeline', 'pipeline_complete'),
            (videos_bp, '/api/videos', 'videos'),
            (settings_bp, '/api/settings', 'settings'),
            (system_bp, '/api/system', 'system'),
            (tests_bp, '/api/tests', 'tests'),
            (images_bp, '/api/images', 'images'),
            (image_queue_bp, '/api/image-queue', 'image_queue'),
            (prompts_config_bp, '/api', 'prompts_config'),
            (storyteller_bp, None, 'storyteller'),  # já tem url_prefix='/api/storyteller' definido
        ]
        
        registered_count = 0
        for blueprint, url_prefix, name in blueprints:
            try:
                if url_prefix:
                    app.register_blueprint(blueprint, url_prefix=url_prefix)
                else:
                    app.register_blueprint(blueprint)
                print(f"✅ Registered {name} blueprint")
                registered_count += 1
            except Exception as e:
                print(f"❌ Failed to register {name} blueprint: {e}")
                import traceback
                traceback.print_exc()
        
        print(f"✅ {registered_count}/{len(blueprints)} blueprints registered successfully!")
        
    except Exception as e:
        print(f"❌ Error importing blueprints: {e}")
        import traceback
        traceback.print_exc()

# Replace the original function with our debug version
import app as app_module
app_module.register_blueprints = debug_register_blueprints

if __name__ == '__main__':
    print("=== App Initialization Debug ===")
    
    # Initialize database
    from app import init_database
    init_database()
    
    # Register blueprints with debug version
    debug_register_blueprints()
    
    # Check what routes are available
    print("\n=== Available Routes ===")
    settings_routes = []
    for rule in app.url_map.iter_rules():
        if rule.rule.startswith('/api/settings'):
            settings_routes.append(rule.rule)
    
    if settings_routes:
        print("Settings routes found:")
        for route in settings_routes:
            print(f"  {route}")
    else:
        print("No settings routes found")