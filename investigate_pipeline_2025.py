#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append('backend')

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
from routes.settings import get_db_connection
import sqlite3
from datetime import datetime

def investigate_pipeline():
    """Investigar a Pipeline #2025-09-09-009"""
    try:
        # Conectar ao banco SQLite principal
        import sqlite3
        db_path = os.path.join(os.path.dirname(__file__), 'backend', 'auto_video_producer.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔍 Buscando Pipeline #2025-09-09-009...")
        
        # Buscar pipeline específica
        cursor.execute("""
        SELECT pipeline_id, display_name, title, status, current_step, progress, 
               started_at, completed_at, tts_results, images_results
        FROM pipeline 
        WHERE display_name LIKE '%2025-09-09-009%' OR pipeline_id LIKE '%2025-09-09-009%' OR title LIKE '%2025-09-09-009%'
        ORDER BY started_at DESC
        """)
        
        pipelines = cursor.fetchall()
        print(f"📋 Pipelines encontradas: {len(pipelines)}")
        
        if not pipelines:
            print("❌ Nenhuma pipeline encontrada com esse identificador")
            
            # Buscar pipelines recentes (últimas 24 horas)
            cursor.execute("""
                SELECT id, title, status, current_step, progress, created_at, updated_at 
                FROM pipelines 
                WHERE datetime(created_at) >= datetime('now', '-1 day')
                ORDER BY created_at DESC
                LIMIT 10
            """)
            
            recent_pipelines = cursor.fetchall()
            print(f"\n📅 Pipelines recentes (últimas 24h): {len(recent_pipelines)}")
            
            for pipeline in recent_pipelines:
                print(f"\n🔸 ID: {pipeline[0]}")
                print(f"   Título: {pipeline[1]}")
                print(f"   Status: {pipeline[2]}")
                print(f"   Etapa: {pipeline[3]}")
                print(f"   Progresso: {pipeline[4]}%")
                print(f"   Criado: {pipeline[5]}")
                print(f"   Atualizado: {pipeline[6]}")
        else:
            for pipeline in pipelines:
                pipeline_id = pipeline[0]
                print(f"\n✅ PIPELINE ENCONTRADA")
                print(f"🔸 ID: {pipeline_id}")
                print(f"   Título: {pipeline[1]}")
                print(f"   Status: {pipeline[2]}")
                print(f"   Etapa: {pipeline[3]}")
                print(f"   Progresso: {pipeline[4]}%")
                print(f"   Criado: {pipeline[5]}")
                print(f"   Atualizado: {pipeline[6]}")
                
                # Buscar logs da pipeline
                cursor.execute("""
                    SELECT level, message, data, timestamp 
                    FROM pipeline_logs 
                    WHERE pipeline_id = ?
                    ORDER BY timestamp DESC
                    LIMIT 50
                """, (pipeline_id,))
                
                logs = cursor.fetchall()
                print(f"\n📝 Logs encontrados: {len(logs)}")
                
                # Filtrar logs relacionados a áudio e vídeo
                audio_video_logs = []
                for log in logs:
                    message = log[1].lower()
                    if any(keyword in message for keyword in ['tts', 'audio', 'video', 'imagem', 'image', 'geração']):
                        audio_video_logs.append(log)
                
                print(f"🎵 Logs de áudio/vídeo: {len(audio_video_logs)}")
                
                if audio_video_logs:
                    print("\n🔍 LOGS RELEVANTES (áudio/vídeo):")
                    for log in audio_video_logs[:20]:  # Mostrar apenas os 20 mais recentes
                        print(f"   [{log[3]}] {log[0].upper()}: {log[1]}")
                        if log[2]:  # Se há dados adicionais
                            print(f"      Dados: {log[2][:100]}..." if len(str(log[2])) > 100 else f"      Dados: {log[2]}")
                
                # Verificar se há duplicação de etapas
                cursor.execute("""
                    SELECT message, COUNT(*) as count, GROUP_CONCAT(timestamp) as timestamps
                    FROM pipeline_logs 
                    WHERE pipeline_id = ? AND (message LIKE '%TTS%' OR message LIKE '%áudio%' OR message LIKE '%vídeo%' OR message LIKE '%imagem%')
                    GROUP BY message
                    HAVING COUNT(*) > 1
                    ORDER BY count DESC
                """, (pipeline_id,))
                
                duplicates = cursor.fetchall()
                if duplicates:
                    print(f"\n⚠️  POSSÍVEIS DUPLICAÇÕES DETECTADAS: {len(duplicates)}")
                    for dup in duplicates:
                        print(f"   📌 '{dup[0]}' executado {dup[1]} vezes")
                        timestamps = dup[2].split(',')
                        print(f"      Timestamps: {', '.join(timestamps[:3])}{'...' if len(timestamps) > 3 else ''}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro durante investigação: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    investigate_pipeline()