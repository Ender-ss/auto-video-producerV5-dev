#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug passo a passo do processamento de script
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.script_processing_service import ScriptProcessingService

def debug_step_by_step():
    """Debug detalhado passo a passo"""
    
    print("🔍 DEBUG PASSO A PASSO DO PROCESSAMENTO")
    print("=" * 50)
    
    # Script de teste
    test_script = """
**PREMISSA:** Era uma vez um jovem empreendedor que sonhava em construir um império digital.

Capítulo 1: O Início

João sempre teve o sonho de ser um empresário de sucesso.

Premissa: O sucesso vem para aqueles que persistem.

Ele começou vendendo doces na escola.

*PREMISSA*: A determinação é a chave para o sucesso.

Capítulo 2: Os Desafios
"""
    
    print(f"📝 Script original ({len(test_script)} caracteres):")
    print(repr(test_script))
    
    processor = ScriptProcessingService()
    
    # Configuração de teste
    config = {
        "enabled": True,
        "remove_chapter_headers": True,
        "remove_markdown": True,
        "remove_premise": True
    }
    
    print(f"\n🔧 Configuração:")
    for key, value in config.items():
        print(f"   {key}: {value}")
    
    # Simular o fluxo do process_script
    print(f"\n⚙️ Simulando fluxo do process_script...")
    
    try:
        # Mesclar configuração
        processing_config = {**processor.default_config, **config}
        
        print(f"\n📋 Configuração final:")
        relevant_keys = ['remove_premise', 'remove_chapter_headers', 'remove_markdown']
        for key in relevant_keys:
            print(f"   {key}: {processing_config.get(key)}")
        
        # Simular _apply_processing passo a passo
        print(f"\n🔄 Executando _apply_processing...")
        
        step_result = test_script
        print(f"\n📝 Passo 0 (original): {len(step_result)} chars")
        print(f"   Contém 'premissa': {'premissa' in step_result.lower()}")
        print(f"   Primeiros 100 chars: {repr(step_result[:100])}")
        
        # Passo 1: Filtro de premissa (PRIMEIRO)
        if processing_config.get('remove_premise', True):
            print(f"\n🎯 Passo 1: Aplicando filtro de premissa...")
            step_result = processor._remove_premise_from_script(step_result)
            print(f"   Resultado: {len(step_result)} chars")
            print(f"   Contém 'premissa': {'premissa' in step_result.lower()}")
            print(f"   Primeiros 100 chars: {repr(step_result[:100])}")
        
        # Passo 2: Remoção de cabeçalhos
        if processing_config.get('remove_chapter_headers', True):
            print(f"\n📑 Passo 2: Removendo cabeçalhos...")
            step_result = processor.header_remover.remove_headers_advanced(step_result)
            print(f"   Resultado: {len(step_result)} chars")
            print(f"   Contém 'premissa': {'premissa' in step_result.lower()}")
            print(f"   Primeiros 100 chars: {repr(step_result[:100])}")
        
        # Passo 3: Remoção de markdown
        if processing_config.get('remove_markdown', True):
            print(f"\n🔤 Passo 3: Removendo markdown...")
            step_result = processor._remove_additional_markdown(step_result)
            print(f"   Resultado: {len(step_result)} chars")
            print(f"   Contém 'premissa': {'premissa' in step_result.lower()}")
            print(f"   Primeiros 100 chars: {repr(step_result[:100])}")
        
        print(f"\n📝 Resultado final:")
        print(repr(step_result))
        
        # Verificar se premissas foram removidas
        premise_check = 'premissa' in step_result.lower()
        if premise_check:
            print(f"\n❌ FALHA: Premissas ainda encontradas no resultado final")
            
            # Encontrar onde estão as premissas
            lines = step_result.split('\n')
            for i, line in enumerate(lines):
                if 'premissa' in line.lower():
                    print(f"   Linha {i+1}: {repr(line)}")
            
            return False
        else:
            print(f"\n✅ SUCESSO: Todas as premissas foram removidas!")
            return True
    
    except Exception as e:
        print(f"\n❌ ERRO: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_process_script_directly():
    """Testar o método process_script diretamente"""
    
    print(f"\n\n🧪 TESTE DIRETO DO MÉTODO process_script")
    print("=" * 50)
    
    test_script = "**PREMISSA:** Teste simples.\n\nCapítulo 1: Conteúdo."
    
    processor = ScriptProcessingService()
    
    config = {
        "enabled": True,
        "remove_premise": True
    }
    
    print(f"📝 Script: {repr(test_script)}")
    print(f"🔧 Config: {config}")
    
    try:
        result = processor.process_script(
            pipeline_id="test-debug",
            raw_script=test_script,
            config=config
        )
        
        if result.get('success'):
            processed = result.get('processed_script', '')
            print(f"\n✅ Sucesso: {repr(processed)}")
            
            if 'premissa' in processed.lower():
                print(f"❌ FALHA: Premissa ainda presente")
                return False
            else:
                print(f"✅ SUCESSO: Premissa removida")
                return True
        else:
            print(f"❌ Erro: {result.get('error')}")
            return False
    
    except Exception as e:
        print(f"❌ ERRO: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success1 = debug_step_by_step()
    success2 = test_process_script_directly()
    
    print("\n" + "=" * 50)
    if success1 and success2:
        print("🎉 RESULTADO FINAL: Filtro funcionando corretamente!")
        sys.exit(0)
    else:
        print("💥 RESULTADO FINAL: Problema no filtro!")
        sys.exit(1)