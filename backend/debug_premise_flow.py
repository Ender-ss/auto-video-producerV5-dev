#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.script_processing_service import ScriptProcessingService
import re

def count_premises(text):
    """Conta quantas premissas existem no texto"""
    patterns = [
        r'\*\*PREMISSA:\*\*.*?(?=\n\n|\n[A-Z]|$)',
        r'Premissa:.*?(?=\n\n|\n[A-Z]|$)',
        r'\*PREMISSA\*:.*?(?=\n\n|\n[A-Z]|$)',
        r'\*\*PREMISSA\*\*:.*?(?=\n\n|\n[A-Z]|$)'
    ]
    
    total = 0
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
        total += len(matches)
        if matches:
            print(f"   Padrão '{pattern}' encontrou {len(matches)} ocorrências")
    
    return total

def debug_process_script():
    print("🔍 DEBUG DETALHADO DO PROCESS_SCRIPT")
    print("=" * 60)
    
    # Script de teste
    test_script = """
**PREMISSA:** Era uma vez um jovem empreendedor que sonhava em construir um império digital.

Capítulo 1: O Início

João sempre teve o sonho de ser um empresário de sucesso. Desde pequeno, ele observava os grandes nomes do mundo dos negócios e imaginava como seria estar no lugar deles.

Premissa: O sucesso vem para aqueles que persistem.

Ele começou vendendo doces na escola, depois passou a vender produtos online. A cada dia que passava, ele se aproximava mais do seu objetivo.

*PREMISSA*: A determinação é a chave para o sucesso.

Capítulo 2: Os Desafios

Nem tudo foram flores no caminho de João.
"""
    
    print(f"📝 Script original tem {count_premises(test_script)} premissas")
    
    # Inicializar serviço
    service = ScriptProcessingService()
    
    # Configuração de teste
    config = {
        'remove_premise': True,
        'remove_chapter_headers': True,
        'remove_markdown': True
    }
    
    print(f"⚙️ Configuração: {config}")
    
    # Simular o fluxo interno do process_script
    print("\n🔄 SIMULANDO FLUXO INTERNO:")
    print("-" * 40)
    
    # 1. Validação
    print("1️⃣ Validação de entrada...")
    try:
        validation_result = service.validate_input(test_script, config)
        if not validation_result:
            print("❌ Validação falhou")
            return
        print("✅ Validação passou")
    except Exception as e:
        print(f"❌ Erro na validação: {e}")
    
    # 2. Mesclagem de configuração
    print("\n2️⃣ Mesclagem de configuração...")
    merged_config = {**service.default_config, **config}
    print(f"📋 Configuração mesclada: {merged_config}")
    
    # 3. Aplicar processamento
    print("\n3️⃣ Aplicando processamento...")
    try:
        processed_script = service._apply_processing(test_script, merged_config)
        print(f"✅ Processamento concluído")
        print(f"📊 Script processado tem {count_premises(processed_script)} premissas")
        
        # Mostrar resultado
        print("\n📄 RESULTADO FINAL:")
        print("-" * 40)
        print(processed_script[:500] + "..." if len(processed_script) > 500 else processed_script)
        
    except Exception as e:
        print(f"❌ Erro no processamento: {e}")
        import traceback
        traceback.print_exc()
    
    # 4. Teste direto do método process_script
    print("\n\n🧪 TESTE DIRETO DO PROCESS_SCRIPT")
    print("=" * 60)
    
    try:
        result = service.process_script('test-pipeline', test_script, config)
        
        if result['success']:
            final_script = result['processed_script']
            final_count = count_premises(final_script)
            print(f"✅ Process_script executado com sucesso")
            print(f"📊 Script final tem {final_count} premissas")
            
            if final_count == 0:
                print("🎉 SUCESSO: Filtro funcionando!")
            else:
                print("❌ FALHA: Premissas ainda presentes")
                print("\n📄 Script final:")
                print("-" * 40)
                print(final_script[:500] + "..." if len(final_script) > 500 else final_script)
        else:
            print(f"❌ Process_script falhou: {result.get('error', 'Erro desconhecido')}")
            
    except Exception as e:
        print(f"❌ Erro no process_script: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_process_script()