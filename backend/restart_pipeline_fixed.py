#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app, db, Pipeline
    from routes.pipeline_complete import process_complete_pipeline, active_pipelines, add_pipeline_log
except ImportError as e:
    print(f"Erro ao importar modulos: {e}")
    sys.exit(1)

def restart_pipeline_with_moviepy():
    """Reiniciar a pipeline com MoviePy corrigido"""
    pipeline_id = "aca7fdeb-a9ea-4083-9315-fc16d03798f1"  # ID real da pipeline
    
    with app.app_context():
        try:
            # Buscar a pipeline no banco
            pipeline = Pipeline.query.filter_by(pipeline_id=pipeline_id).first()
            if not pipeline:
                print(f"❌ Pipeline {pipeline_id} não encontrada")
                return False
                
            print(f"✅ Pipeline encontrada: {pipeline.display_name}")
            print(f"   Status atual: {pipeline.status}")
            print(f"   Progresso: {pipeline.progress}%")
            
            # Verificar se MoviePy está funcionando
            try:
                import moviepy
                from moviepy import VideoFileClip, ImageClip
                print(f"✅ MoviePy está disponível e funcionando! Versão: {moviepy.__version__}")
            except ImportError as e:
                print(f"❌ MoviePy ainda não está disponível: {e}")
                return False
            
            # Resetar status para processing se necessário
            if pipeline.status != 'processing':
                pipeline.status = 'processing'
                pipeline.error_message = None
                db.session.commit()
                print(f"✅ Status da pipeline resetado para 'processing'")
            
            # Adicionar ao estado ativo em memória
            active_pipelines[pipeline_id] = {
                'status': 'processing',
                'progress': pipeline.progress,
                'current_step': 'video',  # Retomar na etapa de vídeo
                'error': None,
                'started_at': time.time()
            }
            
            # Log de reinicialização
            add_pipeline_log(pipeline_id, 'info', f'Pipeline reiniciada com MoviePy v1.0.3 funcionando')
            add_pipeline_log(pipeline_id, 'info', 'Retomando processamento na etapa de criação de vídeo...')
            
            # Executar em thread separada
            thread = threading.Thread(
                target=process_complete_pipeline,
                args=(pipeline_id,),
                daemon=True
            )
            thread.start()
            
            print(f"🚀 Pipeline reiniciada com sucesso!")
            print(f"📋 Logs em tempo real: http://localhost:5000/api/pipeline/logs/{pipeline_id}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao reiniciar pipeline: {e}")
            return False

def check_pipeline_status():
    """Verificar status atual da pipeline"""
    pipeline_id = "aca7fdeb-a9ea-4083-9315-fc16d03798f1"
    
    with app.app_context():
        try:
            pipeline = Pipeline.query.filter_by(pipeline_id=pipeline_id).first()
            if pipeline:
                print(f"📊 Status da Pipeline {pipeline.display_name}:")
                print(f"   Status: {pipeline.status}")
                print(f"   Progresso: {pipeline.progress}%")
                print(f"   Erro: {pipeline.error_message or 'Nenhum'}")
                
                # Verificar se está ativa em memória
                if pipeline_id in active_pipelines:
                    active_status = active_pipelines[pipeline_id]
                    print(f"   Estado ativo: {active_status['status']}")
                    print(f"   Etapa atual: {active_status.get('current_step', 'N/A')}")
                else:
                    print(f"   Estado ativo: Não está em memória")
            else:
                print(f"❌ Pipeline não encontrada")
                
        except Exception as e:
            print(f"❌ Erro ao verificar status: {e}")

if __name__ == "__main__":
    print("🔧 Reinicializador de Pipeline com MoviePy Corrigido")
    print("="*50)
    
    # Verificar status atual
    check_pipeline_status()
    print()
    
    # Perguntar se deve reiniciar
    resposta = input("Deseja reiniciar a pipeline? (s/n): ").lower().strip()
    
    if resposta in ['s', 'sim', 'y', 'yes']:
        print("\n🚀 Reiniciando pipeline...")
        if restart_pipeline_with_moviepy():
            print("\n✅ Pipeline reiniciada com sucesso!")
            print("\n⏳ Aguardando alguns segundos para verificar o progresso...")
            time.sleep(5)
            print("\n📊 Status após reinicialização:")
            check_pipeline_status()
        else:
            print("\n❌ Falha ao reiniciar a pipeline")
    else:
        print("\n❌ Reinicialização cancelada")
    
    print("\n🏁 Concluído!")