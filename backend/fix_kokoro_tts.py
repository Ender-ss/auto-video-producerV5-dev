#!/usr/bin/env python3
"""
Script para corrigir a função generate_tts_with_kokoro
"""

import os
import json
import base64
import requests
import time

def test_and_fix_kokoro_tts():
    """Testa e corrige a função Kokoro TTS"""
    
    # Primeiro, vamos testar a API Kokoro diretamente
    kokoro_url = 'http://localhost:8880'
    url = f"{kokoro_url}/v1/audio/speech"
    
    payload = {
        "model": "kokoro",
        "input": "Hello, this is a test.",
        "voice": "af_bella",
        "response_format": "wav",
        "speed": 1.0,
        "language": "en"
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    print("🔍 Testando API Kokoro diretamente...")
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type', 'N/A')}")
        print(f"Content-Length: {len(response.content)} bytes")
        
        # Verificar se é JSON
        try:
            response_data = response.json()
            print("✅ Resposta é JSON")
            print(f"Keys: {list(response_data.keys())}")
            
            if 'audio' in response_data:
                audio_base64 = response_data['audio']
                print(f"Campo 'audio' encontrado com {len(audio_base64)} caracteres")
                print(f"Primeiros 50 chars: {audio_base64[:50]}")
                
                # Tentar decodificar base64
                try:
                    audio_bytes = base64.b64decode(audio_base64)
                    print(f"✅ Base64 decodificado: {len(audio_bytes)} bytes")
                    
                    # Salvar arquivo de teste
                    test_file = 'temp/test_kokoro_fixed.wav'
                    os.makedirs('temp', exist_ok=True)
                    
                    with open(test_file, 'wb') as f:
                        f.write(audio_bytes)
                    
                    print(f"✅ Arquivo de teste salvo: {test_file}")
                    
                    # Verificar se o arquivo é válido
                    try:
                        import soundfile as sf
                        data, samplerate = sf.read(test_file)
                        print(f"✅ Arquivo WAV válido: {len(data)} samples, {samplerate} Hz")
                        return True
                    except Exception as e:
                        print(f"❌ Arquivo WAV inválido: {e}")
                        return False
                        
                except Exception as e:
                    print(f"❌ Erro ao decodificar base64: {e}")
                    return False
            else:
                print("❌ Campo 'audio' não encontrado na resposta JSON")
                return False
                
        except Exception as e:
            print(f"❌ Resposta não é JSON válido: {e}")
            print(f"Primeiros 200 chars da resposta: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return False

def create_fixed_kokoro_function():
    """Cria uma versão corrigida da função generate_tts_with_kokoro"""
    
    fixed_function = '''
def generate_tts_with_kokoro_fixed(text, kokoro_url='http://localhost:8880', voice_name='af_bella', language='en', job_id=None, **kwargs):
    """Versão corrigida da função generate_tts_with_kokoro"""
    import requests
    import json
    import base64
    import os
    import time
    
    try:
        print(f"🎵 Iniciando TTS com Kokoro - Texto: {len(text)} chars, Voz: {voice_name}, Idioma: {language}")
        
        # Configurar URL da API Kokoro
        url = f"{kokoro_url}/v1/audio/speech"
        
        # Preparar payload compatível com OpenAI
        payload = {
            "model": "kokoro",
            "input": text,
            "voice": voice_name,
            "response_format": "wav",
            "speed": kwargs.get('speed', 1.0),
            "language": language
        }
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        print(f"🔍 Enviando requisição para Kokoro TTS API...")
        print(f"🔍 URL: {url}")
        print(f"🔍 Voz: {voice_name}")
        
        # Fazer requisição
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        
        print(f"🔍 Status da resposta: {response.status_code}")
        
        if response.status_code != 200:
            error_msg = f"Erro da API Kokoro TTS: {response.status_code} - {response.text}"
            print(f"❌ {error_msg}")
            raise Exception(error_msg)
        
        # CORREÇÃO: Processar resposta JSON corretamente
        try:
            response_data = response.json()
            print(f"🔍 Resposta JSON keys: {list(response_data.keys())}")
            
            if 'audio' not in response_data:
                raise Exception("Resposta da API Kokoro não contém dados de áudio")
            
            # Decodificar áudio base64
            audio_base64 = response_data['audio']
            print(f"🔍 Base64 length: {len(audio_base64)}")
            
            if not audio_base64 or audio_base64.strip() == "":
                raise Exception("Dados de áudio base64 estão vazios")
            
            # CORREÇÃO: Decodificar base64 corretamente
            audio_bytes = base64.b64decode(audio_base64)
            print(f"🔍 Áudio decodificado: {len(audio_bytes)} bytes")
            
        except json.JSONDecodeError as e:
            # Fallback: tentar usar resposta como áudio binário direto
            print(f"⚠️ Erro ao decodificar JSON, tentando áudio binário direto: {e}")
            audio_bytes = response.content
        
        # Verificar se o áudio contém apenas zeros
        if len(audio_bytes) > 50 and all(b == 0 for b in audio_bytes[:50]):
            print("⚠️ Áudio Kokoro contém apenas zeros")
            raise Exception("Áudio Kokoro contém apenas zeros - fallback necessário")
        
        # Salvar arquivo
        temp_dir = os.path.join(os.path.dirname(__file__), '..', 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        
        timestamp = int(time.time())
        filename = f"tts_kokoro_{timestamp}.wav"
        filepath = os.path.join(temp_dir, filename)
        
        print(f"🔍 Salvando áudio em: {filepath}")
        
        # CORREÇÃO: Salvar bytes de áudio, não JSON
        with open(filepath, 'wb') as f:
            f.write(audio_bytes)
        
        print(f"✅ Áudio TTS Kokoro gerado com sucesso: {filepath}")
        
        return {
            'success': True,
            'data': {
                'audio_url': f'/api/automations/audio/{filename}',
                'filename': filename,
                'voice_used': voice_name,
                'language_used': language,
                'text_length': len(text),
                'kokoro_url': kokoro_url,
                'size': len(audio_bytes),
                'duration': 0
            },
            'message': 'Áudio gerado com sucesso usando Kokoro TTS'
        }
        
    except Exception as e:
        error_msg = f"Erro no TTS Kokoro: {str(e)}"
        print(f"❌ {error_msg}")
        return {
            'success': False,
            'error': error_msg
        }
'''
    
    with open('kokoro_function_fixed.py', 'w', encoding='utf-8') as f:
        f.write(fixed_function)
    
    print("✅ Função corrigida salva em kokoro_function_fixed.py")

if __name__ == '__main__':
    print("=== Testando e Corrigindo Kokoro TTS ===")
    
    # Testar API
    if test_and_fix_kokoro_tts():
        print("\n✅ API Kokoro está funcionando corretamente")
        create_fixed_kokoro_function()
    else:
        print("\n❌ Problema com a API Kokoro")