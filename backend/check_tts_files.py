#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from datetime import datetime

def check_tts_files():
    print("🎵 VERIFICANDO ARQUIVOS DE ÁUDIO TTS")
    print("=" * 50)
    
    tts_dir = 'outputs/tts'
    
    if not os.path.exists(tts_dir):
        print(f"❌ Diretório {tts_dir} não existe")
        return
    
    print(f"✅ Diretório {tts_dir} existe")
    
    # Listar todos os arquivos de áudio
    audio_files = []
    for file in os.listdir(tts_dir):
        if file.endswith(('.wav', '.mp3', '.ogg')):
            file_path = os.path.join(tts_dir, file)
            file_size = os.path.getsize(file_path)
            file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            audio_files.append((file, file_size, file_time))
    
    if not audio_files:
        print("❌ Nenhum arquivo de áudio encontrado")
        return
    
    print(f"✅ {len(audio_files)} arquivo(s) de áudio encontrado(s)")
    print("\n📁 ARQUIVOS ENCONTRADOS:")
    
    # Ordenar por data de modificação (mais recente primeiro)
    audio_files.sort(key=lambda x: x[2], reverse=True)
    
    for i, (filename, size, mod_time) in enumerate(audio_files[:10], 1):
        size_mb = size / (1024 * 1024)
        print(f"{i:2d}. {filename}")
        print(f"    📏 Tamanho: {size_mb:.2f} MB")
        print(f"    🕒 Modificado: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
    
    if len(audio_files) > 10:
        print(f"... e mais {len(audio_files) - 10} arquivo(s)")

if __name__ == '__main__':
    check_tts_files()