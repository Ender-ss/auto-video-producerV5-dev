#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import glob
from datetime import datetime

def debug_audio_paths():
    print("🔍 DIAGNÓSTICO DE CAMINHOS DE ÁUDIO")
    print("=" * 50)
    
    # Diretórios para verificar
    base_dir = os.path.dirname(__file__)
    temp_dir = os.path.join(base_dir, 'temp')
    output_dir = os.path.join(base_dir, 'output', 'audio')
    
    print(f"📁 Diretório base: {base_dir}")
    print(f"📁 Diretório temp: {temp_dir}")
    print(f"📁 Diretório output: {output_dir}")
    print()
    
    # Verificar diretório temp
    print("🔍 VERIFICANDO DIRETÓRIO TEMP:")
    if os.path.exists(temp_dir):
        print(f"✅ Diretório temp existe: {temp_dir}")
        
        # Listar arquivos de áudio no temp
        audio_files = []
        for ext in ['*.wav', '*.mp3', '*.ogg']:
            audio_files.extend(glob.glob(os.path.join(temp_dir, ext)))
        
        if audio_files:
            print(f"✅ {len(audio_files)} arquivo(s) de áudio encontrado(s) no temp:")
            for i, file_path in enumerate(sorted(audio_files, key=os.path.getmtime, reverse=True)[:10], 1):
                filename = os.path.basename(file_path)
                size = os.path.getsize(file_path)
                mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                print(f"  {i:2d}. {filename} ({size} bytes, {mod_time.strftime('%H:%M:%S')})")
        else:
            print("❌ Nenhum arquivo de áudio encontrado no temp")
    else:
        print(f"❌ Diretório temp não existe: {temp_dir}")
    
    print()
    
    # Verificar diretório output
    print("🔍 VERIFICANDO DIRETÓRIO OUTPUT:")
    if os.path.exists(output_dir):
        print(f"✅ Diretório output existe: {output_dir}")
        
        # Listar arquivos de áudio no output
        audio_files = []
        for ext in ['*.wav', '*.mp3', '*.ogg']:
            audio_files.extend(glob.glob(os.path.join(output_dir, ext)))
        
        if audio_files:
            print(f"✅ {len(audio_files)} arquivo(s) de áudio encontrado(s) no output:")
            for i, file_path in enumerate(sorted(audio_files, key=os.path.getmtime, reverse=True)[:10], 1):
                filename = os.path.basename(file_path)
                size = os.path.getsize(file_path)
                mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                print(f"  {i:2d}. {filename} ({size} bytes, {mod_time.strftime('%H:%M:%S')})")
        else:
            print("❌ Nenhum arquivo de áudio encontrado no output")
    else:
        print(f"❌ Diretório output não existe: {output_dir}")
        print("🔧 Criando diretório output...")
        os.makedirs(output_dir, exist_ok=True)
        print(f"✅ Diretório output criado: {output_dir}")
    
    print()
    
    # Verificar arquivos recentes de TTS
    print("🔍 VERIFICANDO ARQUIVOS TTS RECENTES:")
    all_audio_files = []
    
    # Buscar em ambos os diretórios
    for search_dir in [temp_dir, output_dir]:
        if os.path.exists(search_dir):
            for ext in ['*.wav', '*.mp3', '*.ogg']:
                files = glob.glob(os.path.join(search_dir, ext))
                for file_path in files:
                    if any(keyword in os.path.basename(file_path).lower() for keyword in ['tts', 'kokoro', 'elevenlabs', 'gemini', 'pipeline']):
                        all_audio_files.append(file_path)
    
    if all_audio_files:
        print(f"✅ {len(all_audio_files)} arquivo(s) TTS encontrado(s):")
        # Ordenar por data de modificação (mais recente primeiro)
        all_audio_files.sort(key=os.path.getmtime, reverse=True)
        
        for i, file_path in enumerate(all_audio_files[:15], 1):
            filename = os.path.basename(file_path)
            size = os.path.getsize(file_path)
            mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            directory = "temp" if "temp" in file_path else "output"
            print(f"  {i:2d}. [{directory}] {filename} ({size} bytes, {mod_time.strftime('%H:%M:%S')})")
    else:
        print("❌ Nenhum arquivo TTS encontrado")
    
    print()
    print("🔍 DIAGNÓSTICO COMPLETO!")
    print("💡 PROBLEMA IDENTIFICADO:")
    print("   - Arquivos TTS são salvos no diretório 'temp'")
    print("   - Concatenação procura no diretório 'output/audio'")
    print("   - Isso causa o erro 'Arquivo não encontrado'")
    print()
    print("🔧 SOLUÇÕES POSSÍVEIS:")
    print("   1. Corrigir o TTS Service para salvar no diretório correto")
    print("   2. Corrigir a concatenação para procurar no diretório correto")
    print("   3. Mover arquivos do temp para output antes da concatenação")

if __name__ == '__main__':
    debug_audio_paths()