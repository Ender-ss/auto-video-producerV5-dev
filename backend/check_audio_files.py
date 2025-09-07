#!/usr/bin/env python3

import os
import soundfile as sf
from pathlib import Path

def check_audio_files():
    """Verificar arquivos de áudio gerados pelo Kokoro TTS"""
    temp_dir = Path('temp')
    
    print("🔍 Verificando arquivos de áudio no diretório temp...")
    
    # Listar todos os arquivos de áudio
    audio_files = list(temp_dir.glob('tts_kokoro_*.wav'))
    
    if not audio_files:
        print("❌ Nenhum arquivo de áudio encontrado")
        return
    
    print(f"✅ Encontrados {len(audio_files)} arquivos de áudio")
    
    for audio_file in audio_files[:5]:  # Verificar apenas os primeiros 5
        print(f"\n📁 Arquivo: {audio_file.name}")
        print(f"📏 Tamanho: {audio_file.stat().st_size} bytes")
        
        try:
            # Tentar ler com soundfile
            data, samplerate = sf.read(str(audio_file))
            print(f"✅ Formato válido - Sample rate: {samplerate}Hz, Duração: {len(data)/samplerate:.2f}s")
            
        except Exception as e:
            print(f"❌ Erro ao ler arquivo: {e}")
            
            # Verificar se é um arquivo vazio ou corrompido
            if audio_file.stat().st_size == 0:
                print("⚠️  Arquivo vazio")
            else:
                # Tentar ler os primeiros bytes para verificar o cabeçalho
                with open(audio_file, 'rb') as f:
                    header = f.read(12)
                    print(f"🔍 Cabeçalho (hex): {header.hex()}")
                    print(f"🔍 Cabeçalho (ascii): {header}")

if __name__ == "__main__":
    check_audio_files()