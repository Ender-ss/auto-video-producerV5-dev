#!/usr/bin/env python3

import requests
import json
import base64

def debug_kokoro_response():
    base_url = "http://localhost:8880"
    
    print("🔍 Debug detalhado da resposta do Kokoro...")
    
    test_payload = {
        "model": "kokoro-v0_19",
        "input": "Hello, this is a test.",
        "voice": "af_bella",
        "response_format": "wav",
        "speed": 1.0,
        "language": "en"
    }
    
    try:
        response = requests.post(
            f"{base_url}/v1/audio/speech",
            json=test_payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"📊 Status: {response.status_code}")
        print(f"📏 Tamanho: {len(response.content)} bytes")
        print(f"🔍 Content-Type: {response.headers.get('content-type', 'N/A')}")
        
        if response.status_code == 200:
            # Tentar decodificar como JSON
            try:
                response_data = response.json()
                print(f"✅ Resposta JSON válida")
                print(f"🔑 Chaves disponíveis: {list(response_data.keys())}")
                
                if 'audio' in response_data:
                    audio_base64 = response_data['audio']
                    print(f"📏 Base64 length: {len(audio_base64)}")
                    print(f"🔍 Primeiros 100 chars: {audio_base64[:100]}")
                    print(f"🔍 Últimos 50 chars: {audio_base64[-50:]}")
                    
                    # Verificar se é só zeros em base64
                    if audio_base64.replace('A', '').replace('=', '') == '':
                        print("❌ PROBLEMA: Base64 contém apenas zeros (AAAA...)")
                    else:
                        print("✅ Base64 parece conter dados válidos")
                    
                    # Decodificar base64
                    try:
                        audio_bytes = base64.b64decode(audio_base64)
                        print(f"📏 Áudio decodificado: {len(audio_bytes)} bytes")
                        print(f"🔍 Primeiros 20 bytes: {audio_bytes[:20]}")
                        
                        # Verificar se são todos zeros
                        if all(b == 0 for b in audio_bytes[:100]):
                            print("❌ PROBLEMA: Áudio decodificado são todos zeros")
                        else:
                            print("✅ Áudio decodificado contém dados não-zero")
                            
                        # Verificar header WAV
                        if len(audio_bytes) >= 12:
                            if audio_bytes[:4] == b'RIFF' and audio_bytes[8:12] == b'WAVE':
                                print("✅ Header WAV válido detectado")
                            else:
                                print(f"❌ Header WAV inválido: {audio_bytes[:12]}")
                        
                    except Exception as decode_error:
                        print(f"❌ Erro ao decodificar base64: {decode_error}")
                        
                else:
                    print("❌ Chave 'audio' não encontrada na resposta")
                    print(f"📄 Resposta completa: {json.dumps(response_data, indent=2)[:500]}...")
                    
            except json.JSONDecodeError:
                print("❌ Resposta não é JSON válido")
                print(f"🔍 Primeiros 200 chars: {response.content[:200]}")
                
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            print(f"📄 Resposta: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
    
    # Testar com diferentes parâmetros
    print("\n🔄 Testando com parâmetros diferentes...")
    
    # Teste sem modelo específico
    test_payload_simple = {
        "input": "Test audio generation",
        "voice": "af_bella"
    }
    
    try:
        response = requests.post(
            f"{base_url}/v1/audio/speech",
            json=test_payload_simple,
            timeout=30
        )
        
        print(f"📊 Teste simples - Status: {response.status_code}")
        if response.status_code == 200:
            try:
                data = response.json()
                if 'audio' in data:
                    audio_b64 = data['audio']
                    if audio_b64 and not audio_b64.replace('A', '').replace('=', ''):
                        print("❌ Teste simples também retorna zeros")
                    else:
                        print("✅ Teste simples retorna dados válidos")
            except:
                pass
                
    except Exception as e:
        print(f"❌ Erro no teste simples: {e}")

if __name__ == "__main__":
    debug_kokoro_response()