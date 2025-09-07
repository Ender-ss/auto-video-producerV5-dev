#!/usr/bin/env python3
"""
Diagnóstico detalhado do servidor Kokoro TTS
"""

import requests
import json
import base64
import os
import sys
from pathlib import Path

# Adicionar o diretório backend ao path
sys.path.append(str(Path(__file__).parent))

from routes.automations import generate_tts_with_kokoro

def test_kokoro_server_health():
    """Testa se o servidor Kokoro está respondendo"""
    print("=== Testando saúde do servidor Kokoro ===")
    try:
        response = requests.get("http://localhost:8880/health", timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Resposta: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Erro ao conectar: {e}")
        return False

def test_kokoro_direct_api():
    """Testa a API do Kokoro diretamente"""
    print("\n=== Testando API direta do Kokoro ===")
    
    payload = {
        "model": "kokoro",
        "input": "Hello, this is a test.",
        "voice": "af_bella",
        "response_format": "wav",
        "speed": 1.0
    }
    
    try:
        response = requests.post(
            "http://localhost:8880/v1/audio/speech",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type')}")
        print(f"Tamanho da resposta: {len(response.content)} bytes")
        
        if response.status_code == 200:
            # Verificar se é JSON
            try:
                data = response.json()
                if 'audio' in data:
                    audio_b64 = data['audio']
                    print(f"Áudio base64 (primeiros 50 chars): {audio_b64[:50]}...")
                    
                    # Decodificar e verificar
                    audio_data = base64.b64decode(audio_b64)
                    print(f"Tamanho do áudio decodificado: {len(audio_data)} bytes")
                    print(f"Primeiros 20 bytes: {audio_data[:20]}")
                    
                    # Verificar se são todos zeros
                    if all(b == 0 for b in audio_data[:100]):
                        print("⚠️  PROBLEMA: Áudio contém apenas zeros!")
                        return False
                    else:
                        print("✅ Áudio parece válido")
                        return True
                else:
                    print("❌ Resposta JSON não contém campo 'audio'")
                    return False
            except json.JSONDecodeError:
                print("❌ Resposta não é JSON válido")
                return False
        else:
            print(f"❌ Erro na API: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return False

def test_backend_tts_function():
    """Testa a função TTS do backend"""
    print("\n=== Testando função TTS do backend ===")
    
    try:
        # Configuração de teste
        tts_config = {
            'provider': 'kokoro',
            'voice': 'af_bella',
            'language': 'en',
            'speed': 1.0,
            'pitch': 1.0,
            'kokoro_url': 'http://localhost:8880'
        }
        
        text = "Hello, this is a test from the backend function."
        
        print(f"Testando com texto: '{text}'")
        print(f"Configuração: {tts_config}")
        
        result = generate_tts_with_kokoro(text, tts_config)
        
        if result and 'success' in result:
            if result['success']:
                print("✅ Função TTS executou com sucesso")
                if 'file_path' in result:
                    file_path = result['file_path']
                    if os.path.exists(file_path):
                        file_size = os.path.getsize(file_path)
                        print(f"Arquivo criado: {file_path} ({file_size} bytes)")
                        
                        # Verificar conteúdo do arquivo
                        with open(file_path, 'rb') as f:
                            content = f.read(100)  # Primeiros 100 bytes
                            print(f"Primeiros 20 bytes do arquivo: {content[:20]}")
                            
                            if all(b == 0 for b in content[:50]):
                                print("⚠️  PROBLEMA: Arquivo contém apenas zeros!")
                                return False
                            else:
                                print("✅ Arquivo parece válido")
                                return True
                    else:
                        print(f"❌ Arquivo não foi criado: {file_path}")
                        return False
                else:
                    print("❌ Resultado não contém caminho do arquivo")
                    return False
            else:
                print(f"❌ Função TTS falhou: {result.get('error', 'Erro desconhecido')}")
                return False
        else:
            print(f"❌ Resultado inválido: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar função TTS: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_different_voices():
    """Testa diferentes vozes para ver se alguma funciona"""
    print("\n=== Testando diferentes vozes ===")
    
    voices = ['af_bella', 'af_sarah', 'am_adam', 'am_michael']
    
    for voice in voices:
        print(f"\nTestando voz: {voice}")
        
        payload = {
            "model": "kokoro",
            "input": "Test voice",
            "voice": voice,
            "response_format": "wav",
            "speed": 1.0
        }
        
        try:
            response = requests.post(
                "http://localhost:8880/v1/audio/speech",
                json=payload,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'audio' in data:
                    audio_data = base64.b64decode(data['audio'])
                    if not all(b == 0 for b in audio_data[:50]):
                        print(f"✅ Voz {voice} funciona!")
                        return voice
                    else:
                        print(f"❌ Voz {voice} retorna zeros")
                else:
                    print(f"❌ Voz {voice} - sem campo audio")
            else:
                print(f"❌ Voz {voice} - erro {response.status_code}")
                
        except Exception as e:
            print(f"❌ Voz {voice} - erro: {e}")
    
    return None

def check_docker_container():
    """Verifica se o container Docker do Kokoro está rodando"""
    print("\n=== Verificando container Docker ===")
    
    try:
        import subprocess
        result = subprocess.run(['docker', 'ps'], capture_output=True, text=True)
        
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            kokoro_containers = [line for line in lines if 'kokoro' in line.lower()]
            
            if kokoro_containers:
                print("✅ Container Kokoro encontrado:")
                for container in kokoro_containers:
                    print(f"  {container}")
                return True
            else:
                print("❌ Nenhum container Kokoro encontrado")
                return False
        else:
            print(f"❌ Erro ao executar docker ps: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ Docker não encontrado no sistema")
        return False
    except Exception as e:
        print(f"❌ Erro ao verificar Docker: {e}")
        return False

def main():
    """Função principal de diagnóstico"""
    print("🔍 DIAGNÓSTICO DETALHADO DO KOKORO TTS\n")
    
    # Verificar Docker primeiro
    docker_ok = check_docker_container()
    
    # Teste 1: Saúde do servidor
    if not test_kokoro_server_health():
        print("\n❌ FALHA CRÍTICA: Servidor Kokoro não está respondendo")
        if not docker_ok:
            print("\n🔧 SOLUÇÃO: Iniciar o container Docker do Kokoro")
            print("Comando: docker run -d -p 8880:8880 kokoro-tts")
        return False
    
    # Teste 2: API direta
    api_ok = test_kokoro_direct_api()
    if not api_ok:
        print("\n⚠️  PROBLEMA: API direta retorna áudio inválido")
        
        # Teste 3: Diferentes vozes
        working_voice = test_different_voices()
        if working_voice:
            print(f"\n✅ Encontrada voz funcionando: {working_voice}")
            api_ok = True
        else:
            print("\n❌ PROBLEMA CRÍTICO: Nenhuma voz funciona")
            print("\n🔧 POSSÍVEIS SOLUÇÕES:")
            print("1. Reiniciar o container Docker do Kokoro")
            print("2. Verificar se os modelos estão carregados corretamente")
            print("3. Verificar logs do container: docker logs <container_id>")
            print("4. Testar com um servidor Kokoro diferente")
            return False
    
    # Teste 4: Função do backend
    if api_ok:
        if test_backend_tts_function():
            print("\n✅ SUCESSO: Pipeline TTS está funcionando completamente!")
            return True
        else:
            print("\n❌ PROBLEMA: Função do backend falha mesmo com API funcionando")
            print("\n🔧 Verificar:")
            print("1. Configuração da URL do Kokoro no backend")
            print("2. Processamento do áudio base64")
            print("3. Salvamento do arquivo WAV")
            return False
    
    return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 DIAGNÓSTICO CONCLUÍDO: Sistema funcionando!")
    else:
        print("\n🚨 DIAGNÓSTICO CONCLUÍDO: Problemas identificados!")