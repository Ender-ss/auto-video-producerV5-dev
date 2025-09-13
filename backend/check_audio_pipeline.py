#!/usr/bin/env python3
"""Verificar se a geração de áudio está funcionando na pipeline"""

import requests
import json
from datetime import datetime

def check_audio_pipeline():
    """Verificar pipelines ativas e status da geração de áudio"""
    print('🎵 VERIFICAÇÃO DA GERAÇÃO DE ÁUDIO NA PIPELINE')
    print('=' * 60)
    
    try:
        # 1. Verificar pipelines ativas
        print('📊 Verificando pipelines ativas...')
        response = requests.get('/api/pipeline/active')
        
        if response.status_code != 200:
            print(f'❌ Erro ao buscar pipelines: {response.status_code}')
            return
            
        data = response.json()
        pipelines = data.get('pipelines', [])
        
        print(f'✅ Encontradas {len(pipelines)} pipelines')
        
        if not pipelines:
            print('⚠️ Nenhuma pipeline ativa encontrada')
            return
            
        # 2. Analisar cada pipeline
        for i, pipeline in enumerate(pipelines[:3]):  # Primeiras 3
            pipeline_id = pipeline.get('pipeline_id')
            display_name = pipeline.get('display_name', 'N/A')
            status = pipeline.get('status', 'N/A')
            current_step = pipeline.get('current_step', 'N/A')
            progress = pipeline.get('progress', 0)
            
            print(f'\n🔍 PIPELINE {i+1}:')
            print(f'   🆔 ID: {pipeline_id}')
            print(f'   📛 Nome: {display_name}')
            print(f'   📊 Status: {status}')
            print(f'   📋 Etapa atual: {current_step}')
            print(f'   📈 Progresso: {progress}%')
            
            # 3. Verificar detalhes da pipeline
            detail_response = requests.get(f'/api/pipeline/status/{pipeline_id}')
            
            if detail_response.status_code == 200:
                detail_data = detail_response.json()
                pipeline_detail = detail_data.get('data', {})
                
                # Verificar etapas
                steps = pipeline_detail.get('steps', {})
                results = pipeline_detail.get('results', {})
                
                print('\n   📋 ETAPAS:')
                for step_name, step_data in steps.items():
                    step_status = step_data.get('status', 'N/A')
                    step_progress = step_data.get('progress', 0)
                    print(f'      {step_name}: {step_status} ({step_progress}%)')
                
                # Verificar especificamente TTS
                if 'tts' in steps:
                    tts_step = steps['tts']
                    tts_status = tts_step.get('status', 'N/A')
                    tts_progress = tts_step.get('progress', 0)
                    
                    print(f'\n   🎵 TTS (ÁUDIO):')
                    print(f'      Status: {tts_status}')
                    print(f'      Progresso: {tts_progress}%')
                    
                    # Verificar resultados do TTS
                    if 'tts' in results:
                        tts_results = results['tts']
                        print(f'      Arquivo de áudio: {tts_results.get("audio_file_path", "N/A")}')
                        print(f'      Duração: {tts_results.get("duration", "N/A")}s')
                        print(f'      Provedor: {tts_results.get("provider_used", "N/A")}')
                        print(f'      Status TTS: {tts_results.get("status", "N/A")}')
                        
                        if tts_results.get('status') == 'skipped':
                            print('      ⚠️ TTS foi PULADO - verifique configuração!')
                        elif tts_results.get('audio_file_path'):
                            print('      ✅ Áudio gerado com sucesso!')
                        else:
                            print('      ❌ Problema na geração de áudio!')
                    else:
                        print('      ⏳ TTS ainda não executado')
                else:
                    print('\n   ⚠️ Etapa TTS não encontrada nas etapas da pipeline')
                    
                # Verificar configuração de TTS
                config = pipeline_detail.get('config', {})
                tts_config = config.get('tts', {})
                tts_enabled = tts_config.get('enabled', True)
                
                print(f'\n   ⚙️ CONFIGURAÇÃO TTS:')
                print(f'      Habilitado: {tts_enabled}')
                if not tts_enabled:
                    print('      ❌ TTS DESABILITADO na configuração!')
                    
                # Verificar logs recentes
                logs_response = requests.get(f'/api/pipeline/{pipeline_id}/logs?limit=10')
                if logs_response.status_code == 200:
                    logs_data = logs_response.json()
                    logs = logs_data.get('logs', [])
                    
                    print('\n   📝 LOGS RECENTES:')
                    for log in logs[-5:]:  # Últimos 5 logs
                        timestamp = log.get('timestamp', '')
                        level = log.get('level', 'INFO')
                        message = log.get('message', '')
                        print(f'      [{level}] {message}')
                        
                        # Procurar por mensagens relacionadas ao áudio
                        if any(keyword in message.lower() for keyword in ['tts', 'audio', 'sound', 'concatena']):
                            print(f'         🎵 Relacionado ao áudio!')
            else:
                print(f'   ❌ Erro ao buscar detalhes: {detail_response.status_code}')
                
    except Exception as e:
        print(f'❌ Erro durante verificação: {str(e)}')
        
    print('\n🏁 Verificação concluída!')

if __name__ == '__main__':
    check_audio_pipeline()