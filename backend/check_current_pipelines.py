#!/usr/bin/env python3
"""Verificar pipelines atuais e status do TTS"""

import requests
import json
import time

def check_pipelines():
    print('🔍 VERIFICANDO PIPELINES ATUAIS')
    print('=' * 50)
    
    try:
        # Verificar pipelines ativas
        response = requests.get('/api/pipeline/active')
        
        if response.status_code == 200:
            data = response.json()
            pipelines = data.get('data', [])
            
            print(f'📊 Pipelines ativas: {len(pipelines)}')
            
            if not pipelines:
                print('   Nenhuma pipeline ativa encontrada')
                return
            
            for pipeline in pipelines:
                pipeline_id = pipeline.get('pipeline_id', 'N/A')
                status = pipeline.get('status', 'N/A')
                current_step = pipeline.get('current_step', 'N/A')
                progress = pipeline.get('progress', 0)
                
                print(f'\n🎬 Pipeline: {pipeline_id[:8]}...')
                print(f'   Status: {status}')
                print(f'   Etapa atual: {current_step}')
                print(f'   Progresso: {progress}%')
                
                # Verificar detalhes do TTS
                print('\n🎤 Verificando TTS...')
                
                # Obter status detalhado
                detail_response = requests.get(f'/api/pipeline/status/{pipeline_id}')
                
                if detail_response.status_code == 200:
                    detail_data = detail_response.json()
                    pipeline_detail = detail_data.get('data', {})
                    
                    # Verificar configuração TTS
                    config = pipeline_detail.get('config', {})
                    tts_config = config.get('tts', {})
                    
                    print(f'   TTS Habilitado: {tts_config.get("enabled", False)}')
                    print(f'   TTS Provedor: {tts_config.get("provider", "N/A")}')
                    print(f'   TTS Voz: {tts_config.get("voice", "N/A")}')
                    
                    # Verificar etapas
                    steps = pipeline_detail.get('steps', {})
                    if 'tts' in steps:
                        tts_step = steps['tts']
                        print(f'   TTS Status: {tts_step.get("status", "N/A")}')
                        print(f'   TTS Progresso: {tts_step.get("progress", 0)}%')
                        print(f'   TTS Erro: {tts_step.get("error", "Nenhum")}')
                    
                    # Verificar resultados
                    results = pipeline_detail.get('results', {})
                    if 'tts' in results:
                        tts_result = results['tts']
                        print(f'\n✅ TTS RESULTADO ENCONTRADO!')
                        print(f'   Arquivo: {tts_result.get("audio_file_path", "N/A")}')
                        print(f'   Duração: {tts_result.get("duration", "N/A")}s')
                        print(f'   Provedor usado: {tts_result.get("provider_used", "N/A")}')
                    else:
                        print(f'   ❌ Nenhum resultado TTS encontrado')
                        
                        # Verificar se há script para processar
                        if 'scripts' in results:
                            script_result = results['scripts']
                            script_content = script_result.get('full_script', '')
                            print(f'   📝 Script disponível: {len(script_content)} caracteres')
                            
                            if len(script_content) > 0:
                                print(f'   ⚠️ Script existe mas TTS não foi executado')
                        else:
                            print(f'   📝 Nenhum script encontrado para processar')
                
                print('\n' + '-' * 50)
                
        else:
            print(f'❌ Erro ao obter pipelines: {response.status_code}')
            
    except Exception as e:
        print(f'❌ Erro: {str(e)}')
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    check_pipelines()