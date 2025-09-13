#!/usr/bin/env python3
"""Corrigir etapa TTS da pipeline"""

import requests
import json

def fix_tts_step():
    pipeline_id = 'c2bb551e-2ca3-4de0-82da-e23a4b086b13'
    
    print('🔧 CORRIGINDO ETAPA TTS DA PIPELINE')
    print('=' * 50)
    
    try:
        # 1. Verificar status atual
        print('📊 Status atual da pipeline:')
        response = requests.get(f'/api/pipeline/status/{pipeline_id}')
        
        if response.status_code != 200:
            print(f'❌ Erro ao buscar status: {response.status_code}')
            return
            
        data = response.json()
        pipeline = data.get('data', {})
        steps = pipeline.get('steps', {})
        tts_step = steps.get('tts', {})
        
        print(f'   TTS Status: {tts_step.get("status", "N/A")}')
        print(f'   TTS Progress: {tts_step.get("progress", "N/A")}%')
        print(f'   TTS Result: {"Presente" if tts_step.get("result") else "Ausente"}')
        
        # 2. Verificar se há resultados de TTS
        results = pipeline.get('results', {})
        tts_results = results.get('tts')
        
        if tts_results:
            print('✅ Resultados TTS encontrados!')
            print(f'   Arquivo: {tts_results.get("audio_file_path", "N/A")}')
            print(f'   Duração: {tts_results.get("duration", "N/A")}s')
            print('   ✅ TTS já está funcionando corretamente!')
            return
        else:
            print('❌ Nenhum resultado TTS encontrado')
        
        # 3. Verificar se pipeline está pausada ou pode ser pausada
        current_status = pipeline.get('status', '')
        print(f'\n📋 Status da pipeline: {current_status}')
        
        if current_status == 'processing':
            print('⏸️ Pausando pipeline para correção...')
            pause_response = requests.post(f'/api/pipeline/pause/{pipeline_id}')
            
            if pause_response.status_code == 200:
                print('✅ Pipeline pausada com sucesso')
            else:
                print(f'❌ Erro ao pausar pipeline: {pause_response.status_code}')
                return
        
        # 4. Tentar retomar a pipeline (isso pode reexecutar etapas pendentes)
        print('\n🚀 Retomando pipeline...')
        resume_response = requests.post(f'/api/pipeline/resume/{pipeline_id}')
        
        if resume_response.status_code == 200:
            print('✅ Pipeline retomada com sucesso')
            print('⏳ Aguarde alguns segundos e verifique o status novamente')
        else:
            print(f'❌ Erro ao retomar pipeline: {resume_response.status_code}')
            if resume_response.status_code == 400:
                print('   Pipeline pode não estar pausada')
        
        # 5. Verificar status após retomada
        print('\n📊 Verificando status após retomada...')
        import time
        time.sleep(3)
        
        final_response = requests.get(f'/api/pipeline/status/{pipeline_id}')
        if final_response.status_code == 200:
            final_data = final_response.json()
            final_pipeline = final_data.get('data', {})
            final_results = final_pipeline.get('results', {})
            final_tts = final_results.get('tts')
            
            if final_tts:
                print('✅ TTS corrigido com sucesso!')
                print(f'   Arquivo: {final_tts.get("audio_file_path", "N/A")}')
            else:
                print('❌ TTS ainda não foi corrigido')
                print('   Pode ser necessário aguardar mais tempo ou verificar logs')
        
    except Exception as e:
        print(f'❌ Erro durante correção: {str(e)}')
        import traceback
        traceback.print_exc()
        
if __name__ == '__main__':
    fix_tts_step()