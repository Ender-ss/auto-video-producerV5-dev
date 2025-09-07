#!/usr/bin/env python3
"""Verificar logs da pipeline específica"""

import requests
import json

def check_pipeline_logs():
    pipeline_id = 'c2bb551e-2ca3-4de0-82da-e23a4b086b13'
    
    print(f'📝 LOGS DA PIPELINE {pipeline_id}')
    print('=' * 60)
    
    try:
        # Buscar logs
        response = requests.get(f'http://localhost:5000/api/pipeline/{pipeline_id}/logs?limit=30')
        
        if response.status_code != 200:
            print(f'❌ Erro ao buscar logs: {response.status_code}')
            return
            
        data = response.json()
        logs = data.get('logs', [])
        
        print(f'✅ Encontrados {len(logs)} logs')
        
        # Filtrar logs relacionados ao áudio/TTS
        audio_keywords = ['tts', 'audio', 'sound', 'concatena', 'erro', 'error', 'falha', 'fail']
        
        print('\n🎵 LOGS RELACIONADOS AO ÁUDIO:')
        audio_logs = []
        
        for log in logs:
            message = log.get('message', '').lower()
            if any(keyword in message for keyword in audio_keywords):
                audio_logs.append(log)
                
        if audio_logs:
            for log in audio_logs[-10:]:  # Últimos 10 logs relacionados
                level = log.get('level', 'INFO')
                message = log.get('message', '')
                timestamp = log.get('timestamp', '')
                print(f'[{level}] {message}')
        else:
            print('⚠️ Nenhum log relacionado ao áudio encontrado')
            
        # Mostrar todos os logs recentes
        print('\n📋 LOGS RECENTES (TODOS):')
        for log in logs[-15:]:  # Últimos 15 logs
            level = log.get('level', 'INFO')
            message = log.get('message', '')
            timestamp = log.get('timestamp', '')
            print(f'[{level}] {message}')
            
    except Exception as e:
        print(f'❌ Erro: {str(e)}')
        
if __name__ == '__main__':
    check_pipeline_logs()