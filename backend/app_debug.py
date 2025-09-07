from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
import logging
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'auto-video-producer-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auto_video_producer.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configurar CORS
CORS(app, origins=['http://localhost:5173'])

# Inicializar banco de dados
from database import db
db.init_app(app)

@app.route('/')
def home():
    return jsonify({'message': 'Auto Video Producer API', 'status': 'running'})

@app.route('/api/health')
def health_check():
    return jsonify({
        'success': True,
        'status': 'healthy',
        'message': 'Sistema funcionando normalmente'
    })

def register_blueprints_gradually():
    """Registrar blueprints um por vez para identificar problemas"""
    try:
        logger.info("Iniciando registro de blueprints...")
        
        # Registrar apenas system primeiro
        logger.info("Importando system blueprint...")
        from routes.system import system_bp
        app.register_blueprint(system_bp, url_prefix='/api/system')
        logger.info("✅ System blueprint registrado")
        
        # Adicionar outros gradualmente se necessário
        
    except Exception as e:
        logger.error(f"❌ Erro ao registrar blueprints: {e}")
        raise

if __name__ == '__main__':
    try:
        logger.info("Inicializando banco de dados...")
        with app.app_context():
            db.create_all()
        logger.info("✅ Banco de dados inicializado")
        
        register_blueprints_gradually()
        
        logger.info("🎬 Auto Video Producer Backend (Debug) iniciado!")
        logger.info("📡 API disponível em: http://localhost:5002")
        
        app.run(debug=False, host='0.0.0.0', port=5002, threaded=True)
        
    except Exception as e:
        logger.error(f"❌ Erro na inicialização: {e}")
        raise