#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para reiniciar a Pipeline #2025-09-09-009 que estava com erro do MoviePy
"""

import os
import sys
import threading
from datetime import datetime

# Adicionar o diretório backend ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configurar Flask app context
try:
    from app import app, db, Pipeline
    from routes.pipeline_complete import process_complete_pipeline, active_pipelines, add_pipeline_log
    from services.pipeline_service import PipelineService
except ImportError as e:
    print(f"❌ Erro ao importar módulos: {e}")
    print("💡 Certifique-se de que está executando no diretório backend")
    sys.exit(1)

def restart_pipeline_2025_09_09_009():
    """Reiniciar a pipeline específica que estava com erro do MoviePy"""
    # O ID real da pipeline no banco é diferente do display_name
    pipeline_id = "aca7fdeb-a9ea-4083-9315-fc16d03798f1"  # Pipeline com display_name 2025-09-09-009
    
    print(f"🔄 Reiniciando Pipeline {pipeline_id}...")
    
    with app.app_context():
        try:
            # 1. Buscar pipeline no banco de dados
            pipeline = Pipeline.query.filter_by(pipeline_id=pipeline_id).first()
            if not pipeline:
                print(f"❌ Pipeline {pipeline_id} não encontrada no banco de dados")
                return False
            
            print(f"✅ Pipeline encontrada: {pipeline.pipeline_id}")
            print(f"   Status atual: {pipeline.status}")
            print(f"   Progresso: {pipeline.progress}%")
            
            # 2. Verificar se MoviePy está disponível agora
            try:
                import moviepy
                print(f"✅ MoviePy disponível - versão: {moviepy.__version__}")
            except ImportError as e:
                print(f"❌ MoviePy ainda não está disponível: {e}")
                return False
            
            # 3. Resetar status da pipeline para reprocessamento
            pipeline.status = "processing"
            pipeline.progress = 0
            pipeline.error_message = None
            db.session.commit()
            print(f"✅ Status da pipeline resetado para 'processing'")
            
            # 4. Adicionar pipeline ao estado ativo em memória
            if pipeline_id not in active_pipelines:
                # Reconstruir estado da pipeline baseado no banco de dados
                config = pipeline.config_json if pipeline.config_json else {}
                
                active_pipelines[pipeline_id] = {
                    'pipeline_id': pipeline_id,
                    'status': 'processing',
                    'progress': 0,
                    'config': config,
                    'steps': {
                        'script_processing': {'status': 'completed', 'progress': 100},
                        'audio_generation': {'status': 'completed', 'progress': 100},
                        'image_generation': {'status': 'completed', 'progress': 100},
                        'video_creation': {'status': 'pending', 'progress': 0}  # Esta etapa falhou
                    },
                    'created_at': datetime.utcnow().isoformat(),
                    'results': {}
                }
                print(f"✅ Pipeline adicionada ao estado ativo em memória")
            
            # 5. Adicionar log de reinício
            add_pipeline_log(pipeline_id, 'info', f'Pipeline reiniciada após instalação do MoviePy v{moviepy.__version__}')
            add_pipeline_log(pipeline_id, 'info', 'Iniciando reprocessamento da etapa de criação de vídeo...')
            
            # 6. Executar pipeline em thread separada
            print(f"🚀 Iniciando processamento da pipeline em thread separada...")
            thread = threading.Thread(
                target=process_complete_pipeline,
                args=(pipeline_id,),
                daemon=True
            )
            thread.start()
            
            print(f"✅ Pipeline {pipeline_id} reiniciada com sucesso!")
            print(f"📊 Acompanhe o progresso em: http://localhost:5000/api/pipelines/{pipeline_id}/status")
            print(f"📋 Logs em tempo real: http://localhost:5000/api/pipelines/{pipeline_id}/logs")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao reiniciar pipeline: {e}")
            import traceback
            traceback.print_exc()
            return False

def check_pipeline_status():
    """Verificar status atual da pipeline"""
    pipeline_id = "aca7fdeb-a9ea-4083-9315-fc16d03798f1"  # Pipeline com display_name 2025-09-09-009
    
    with app.app_context():
        try:
            pipeline = Pipeline.query.filter_by(pipeline_id=pipeline_id).first()
            if pipeline:
                print(f"\n📊 Status atual da Pipeline {pipeline_id}:")
                print(f"   Status: {pipeline.status}")
                print(f"   Progresso: {pipeline.progress}%")
                print(f"   Erro: {pipeline.error_message or 'Nenhum'}")
                
                # Verificar se está em memória
                if pipeline_id in active_pipelines:
                    memory_state = active_pipelines[pipeline_id]
                    print(f"   Em memória: Sim (status: {memory_state.get('status', 'unknown')})")
                else:
                    print(f"   Em memória: Não")
            else:
                print(f"❌ Pipeline {pipeline_id} não encontrada")
                
        except Exception as e:
            print(f"❌ Erro ao verificar status: {e}")

if __name__ == "__main__":
    print("🎬 Script de Reinício da Pipeline com MoviePy")
    print("=" * 50)
    
    # Verificar status atual
    check_pipeline_status()
    
    # Perguntar se deve reiniciar
    print("\n❓ Deseja reiniciar a pipeline? (s/n): ", end="")
    response = input().lower().strip()
    
    if response in ['s', 'sim', 'y', 'yes']:
        success = restart_pipeline_2025_09_09_009()
        if success:
            print("\n🎉 Pipeline reiniciada com sucesso!")
            print("\n💡 Dicas:")
            print("   - Monitore os logs no terminal do backend")
            print("   - Verifique o progresso na interface web")
            print("   - A criação de vídeo agora deve funcionar com MoviePy instalado")
        else:
            print("\n❌ Falha ao reiniciar pipeline")
    else:
        print("\n🚫 Operação cancelada")
    
    print("\n✅ Script finalizado")