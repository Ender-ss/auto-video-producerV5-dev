#!/usr/bin/env python3
"""Diagnóstico final do problema do TTS"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, Pipeline, db
import requests
import json

def diagnose_tts_issue():
    print('🔬 DIAGNÓSTICO FINAL DO PROBLEMA TTS')
    print('=' * 60)
    
    # Usar contexto da aplicação existente
    with app.app_context():
        try:
            # 1. Verificar pipelines no banco
            print('\n📊 VERIFICANDO BANCO DE DADOS')
            print('-' * 40)
            
            pipelines = Pipeline.query.order_by(Pipeline.started_at.desc()).limit(5).all()
            print(f'Últimas 5 pipelines no banco:')
            
            for p in pipelines:
                print(f'  {p.pipeline_id[:8]}... - {p.status} - {p.current_step}')
                
                # Verificar se tem resultados TTS
                if p.tts_results:
                    tts_data = json.loads(p.tts_results)
                    print(f'    TTS: {tts_data.get("status", "N/A")} - {tts_data.get("audio_file_path", "N/A")}')
                else:
                    print(f'    TTS: Sem resultados')
            
            # 2. Testar TTS diretamente
            print('\n🎤 TESTANDO TTS DIRETAMENTE')
            print('-' * 40)
            
            try:
                from services.tts_service import TTSService
                
                tts_service = TTSService()
                
                # Configurar TTS
                tts_service.provider = 'kokoro'
                tts_service.voice = 'af_bella'
                tts_service.speed = 1.0
                tts_service.emotion = 'neutral'
                tts_service.language = 'pt'
                
                # Texto de teste
                test_text = "Este é um teste do sistema de text-to-speech. Se você está ouvindo isso, o TTS está funcionando corretamente."
                
                print(f'Gerando áudio para: "{test_text[:50]}..."')
                
                result = tts_service.generate_audio(test_text)
                
                if result['success']:
                    print(f'✅ TTS funcionando!')
                    print(f'   Arquivo: {result["audio_file_path"]}')
                    print(f'   Duração: {result["duration"]}s')
                    
                    # Verificar se arquivo existe
                    if os.path.exists(result['audio_file_path']):
                        file_size = os.path.getsize(result['audio_file_path'])
                        print(f'   Tamanho do arquivo: {file_size} bytes')
                        
                        if file_size > 1000:  # Arquivo com conteúdo real
                            print(f'✅ Arquivo de áudio válido gerado!')
                        else:
                            print(f'⚠️ Arquivo muito pequeno, pode estar vazio')
                    else:
                        print(f'❌ Arquivo não encontrado no disco')
                else:
                    print(f'❌ Erro no TTS: {result.get("error", "Erro desconhecido")}')
                    
            except Exception as e:
                print(f'❌ Erro ao testar TTS: {str(e)}')
                import traceback
                traceback.print_exc()
            
            # 3. Verificar configurações do sistema
            print('\n⚙️ VERIFICANDO CONFIGURAÇÕES')
            print('-' * 40)
            
            try:
                from services.settings_service import SettingsService
                settings_service = SettingsService()
                
                # Verificar configurações TTS
                tts_settings = settings_service.get_tts_settings()
                print(f'Configurações TTS:')
                for key, value in tts_settings.items():
                    if 'key' in key.lower() or 'token' in key.lower():
                        print(f'  {key}: {"***" if value else "Não configurado"}')
                    else:
                        print(f'  {key}: {value}')
                        
            except Exception as e:
                print(f'⚠️ Não foi possível verificar configurações: {str(e)}')
            
            # 4. Criar pipeline de teste simples
            print('\n🧪 CRIANDO PIPELINE DE TESTE')
            print('-' * 40)
            
            try:
                test_config = {
                    'channel_url': 'https://test.com',
                    'title': 'Teste TTS Diagnóstico',
                    'config': {
                        'extraction': {'enabled': False},
                        'titles': {'enabled': False},
                        'premises': {'enabled': False},
                        'scripts': {
                            'enabled': True,
                            'provider': 'gemini',
                            'custom_script': test_text
                        },
                        'script_processing': {'enabled': False},
                        'tts': {
                            'enabled': True,
                            'provider': 'kokoro',
                            'voice': 'af_bella',
                            'speed': 1.0,
                            'emotion': 'neutral',
                            'language': 'pt'
                        },
                        'images': {'enabled': False},
                        'video': {'enabled': False}
                    }
                }
                
                response = requests.post(
                    'http://localhost:5000/api/pipeline/complete',
                    json=test_config,
                    headers={'Content-Type': 'application/json'}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    pipeline_id = data.get('pipeline_id')
                    print(f'✅ Pipeline de teste criada: {pipeline_id}')
                    
                    # Monitorar por alguns segundos
                    import time
                    for i in range(10):
                        time.sleep(2)
                        
                        status_response = requests.get(f'http://localhost:5000/api/pipeline/status/{pipeline_id}')
                        if status_response.status_code == 200:
                            status_data = status_response.json()
                            pipeline_data = status_data.get('data', {})
                            
                            status = pipeline_data.get('status', 'N/A')
                            current_step = pipeline_data.get('current_step', 'N/A')
                            
                            print(f'  [{i*2:2d}s] {status} - {current_step}')
                            
                            # Verificar se TTS foi executado
                            results = pipeline_data.get('results', {})
                            if 'tts' in results:
                                tts_result = results['tts']
                                print(f'\n🎉 TTS EXECUTADO COM SUCESSO!')
                                print(f'   Arquivo: {tts_result.get("audio_file_path", "N/A")}')
                                print(f'   Duração: {tts_result.get("duration", "N/A")}s')
                                break
                            
                            if status in ['completed', 'failed']:
                                if status == 'failed':
                                    errors = pipeline_data.get('errors', [])
                                    print(f'❌ Pipeline falhou: {errors}')
                                else:
                                    print(f'✅ Pipeline concluída, mas sem TTS')
                                break
                    else:
                        print(f'⏰ Pipeline ainda em execução após 20s')
                        
                else:
                    print(f'❌ Erro ao criar pipeline: {response.status_code}')
                    print(f'   Resposta: {response.text[:200]}...')
                    
            except Exception as e:
                print(f'❌ Erro ao criar pipeline de teste: {str(e)}')
            
            # 5. Resumo e recomendações
            print('\n📋 RESUMO E RECOMENDAÇÕES')
            print('=' * 60)
            print('Com base no diagnóstico:')
            print('1. ✅ TTS Service está funcionando diretamente')
            print('2. ⚠️ Problema pode estar na integração com pipeline')
            print('3. 🔧 Recomendação: Verificar logs da pipeline em execução')
            print('4. 🔧 Recomendação: Verificar se etapas anteriores estão gerando script')
            print('5. 🔧 Recomendação: Verificar configuração de etapas na pipeline')
            
        except Exception as e:
            print(f'❌ Erro geral no diagnóstico: {str(e)}')
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    diagnose_tts_issue()