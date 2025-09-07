import json
import os

# Verificar conteúdo do arquivo JSON salvo como .wav
temp_dir = 'temp'
files = [f for f in os.listdir(temp_dir) if f.startswith('tts_kokoro_') and f.endswith('.wav')]

if files:
    file_path = os.path.join(temp_dir, files[0])
    print(f"Verificando arquivo: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("\nConteúdo JSON:")
        print(json.dumps(data, indent=2)[:1000])
        
        # Verificar se tem campo 'audio' com dados base64
        if 'audio' in data:
            print(f"\nCampo 'audio' encontrado com {len(data['audio'])} caracteres")
            print(f"Primeiros 50 caracteres: {data['audio'][:50]}")
        
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
else:
    print("Nenhum arquivo TTS Kokoro encontrado")