import requests
import json
import base64

def test_kokoro_endpoints():
    """Testar diferentes endpoints do Kokoro"""
    base_url = 'http://localhost:8880'
    
    endpoints = [
        '/health',
        '/v1/audio/voices',
        '/v1/models',
        '/docs',
        '/openapi.json'
    ]
    
    print("🔍 Testando endpoints do Kokoro...\n")
    
    for endpoint in endpoints:
        try:
            url = f"{base_url}{endpoint}"
            response = requests.get(url, timeout=5)
            print(f"✅ {endpoint}: {response.status_code}")
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')
                if 'json' in content_type:
                    try:
                        data = response.json()
                        print(f"   📄 JSON keys: {list(data.keys()) if isinstance(data, dict) else 'Array'}")
                    except:
                        print(f"   📄 JSON parse error")
                else:
                    print(f"   📄 Content type: {content_type}")
        except Exception as e:
            print(f"❌ {endpoint}: {e}")
        print()

def test_different_voices():
    """Testar diferentes vozes"""
    voices = ['af_bella', 'am_adam', 'pf_dora', 'af_sarah']
    
    print("🎵 Testando diferentes vozes...\n")
    
    for voice in voices:
        try:
            url = 'http://localhost:8880/v1/audio/speech'
            payload = {
                'model': 'kokoro',
                'input': f'Testing voice {voice}',
                'voice': voice,
                'response_format': 'wav'
            }
            
            response = requests.post(url, json=payload, timeout=10)
            print(f"🔍 Voice {voice}: Status {response.status_code}")
            
            if response.status_code == 200:
                if 'json' in response.headers.get('content-type', ''):
                    data = response.json()
                    if 'audio' in data:
                        audio_b64 = data['audio']
                        audio_bytes = base64.b64decode(audio_b64)
                        
                        # Verificar se é só zeros
                        is_all_zeros = all(b == 0 for b in audio_bytes)
                        print(f"   📊 Audio length: {len(audio_bytes)} bytes")
                        print(f"   📊 All zeros: {is_all_zeros}")
                        print(f"   📊 First 10 bytes: {audio_bytes[:10]}")
                        
                        if not is_all_zeros:
                            print(f"   ✅ Audio válido encontrado!")
                        else:
                            print(f"   ❌ Audio vazio (só zeros)")
            else:
                print(f"   ❌ Error: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        print()

def test_different_formats():
    """Testar diferentes formatos de resposta"""
    formats = ['wav', 'mp3', 'ogg', 'flac']
    
    print("🎵 Testando diferentes formatos...\n")
    
    for fmt in formats:
        try:
            url = 'http://localhost:8880/v1/audio/speech'
            payload = {
                'model': 'kokoro',
                'input': 'Testing format',
                'voice': 'af_bella',
                'response_format': fmt
            }
            
            response = requests.post(url, json=payload, timeout=10)
            print(f"🔍 Format {fmt}: Status {response.status_code}")
            
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')
                print(f"   📄 Content-Type: {content_type}")
                print(f"   📊 Content length: {len(response.content)}")
                
                if 'json' in content_type:
                    data = response.json()
                    if 'audio' in data:
                        audio_bytes = base64.b64decode(data['audio'])
                        is_all_zeros = all(b == 0 for b in audio_bytes)
                        print(f"   📊 Decoded length: {len(audio_bytes)}")
                        print(f"   📊 All zeros: {is_all_zeros}")
            else:
                print(f"   ❌ Error: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        print()

if __name__ == '__main__':
    print("🔧 Diagnóstico completo do servidor Kokoro\n")
    print("=" * 50)
    
    test_kokoro_endpoints()
    print("=" * 50)
    
    test_different_voices()
    print("=" * 50)
    
    test_different_formats()
    print("=" * 50)
    
    print("✅ Diagnóstico concluído!")