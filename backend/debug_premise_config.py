#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug da configuração do filtro de premissa
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.script_processing_service import ScriptProcessingService

def debug_config_flow():
    """Debug do fluxo de configuração"""
    
    print("🔍 DEBUG DA CONFIGURAÇÃO DO FILTRO DE PREMISSA")
    print("=" * 60)
    
    processor = ScriptProcessingService()
    
    # Verificar configuração padrão
    print("📋 Configuração padrão:")
    for key, value in processor.default_config.items():
        print(f"   {key}: {value}")
    
    # Teste com configuração explícita
    test_config = {
        "enabled": True,
        "remove_chapter_headers": False,
        "remove_markdown": False,
        "remove_premise": True
    }
    
    print(f"\n🧪 Configuração de teste:")
    for key, value in test_config.items():
        print(f"   {key}: {value}")
    
    # Script de teste simples
    test_script = "**PREMISSA:** Teste de premissa.\n\nCapítulo 1: Conteúdo do roteiro."
    
    print(f"\n📝 Script de teste:")
    print(f'   "{test_script}"')
    
    # Testar método _apply_processing diretamente
    print(f"\n⚙️ Testando _apply_processing diretamente...")
    
    try:
        # Simular o que acontece no process_script
        processing_config = {**processor.default_config, **test_config}
        
        print(f"\n🔧 Configuração final mesclada:")
        for key, value in processing_config.items():
            if 'remove' in key:
                print(f"   {key}: {value}")
        
        # Aplicar processamento
        result = processor._apply_processing(test_script, processing_config)
        
        print(f"\n📝 Resultado do _apply_processing:")
        print(f'   "{result}"')
        
        # Verificar se premissa foi removida
        if 'premissa' in result.lower():
            print("❌ FALHA: Premissa ainda presente no resultado")
            
            # Debug passo a passo
            print("\n🔍 Debug passo a passo:")
            
            step1 = test_script
            print(f"   Passo 0 (original): \"{step1}\"")
            
            if processing_config.get('remove_chapter_headers', True):
                step1 = processor.header_remover.remove_headers_advanced(step1)
                print(f"   Passo 1 (headers): \"{step1}\"")
            
            if processing_config.get('remove_markdown', True):
                step1 = processor._remove_additional_markdown(step1)
                print(f"   Passo 2 (markdown): \"{step1}\"")
            
            if processing_config.get('remove_premise', True):
                print(f"   Aplicando filtro de premissa...")
                step1 = processor._remove_premise_from_script(step1)
                print(f"   Passo 3 (premise): \"{step1}\"")
            else:
                print(f"   ⚠️ Filtro de premissa DESABILITADO na configuração!")
            
            return False
        else:
            print("✅ SUCESSO: Premissa removida corretamente")
            return True
    
    except Exception as e:
        print(f"❌ ERRO: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_method_isolation():
    """Testar o método isoladamente"""
    
    print(f"\n\n🧪 TESTE ISOLADO DO MÉTODO _remove_premise_from_script")
    print("=" * 60)
    
    processor = ScriptProcessingService()
    
    test_cases = [
        "**PREMISSA:** Teste 1",
        "*PREMISSA*: Teste 2",
        "Premissa: Teste 3",
        "PREMISSA: Teste 4",
        "**Premissa:** Teste 5",
        "Normal text without premise"
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Caso {i}: \"{test_case}\"")
        result = processor._remove_premise_from_script(test_case)
        print(f"   Resultado: \"{result}\"")
        
        if 'premissa' in result.lower() and 'premissa' in test_case.lower():
            print(f"   ❌ FALHA: Premissa não removida")
        elif 'premissa' not in result.lower() and 'premissa' in test_case.lower():
            print(f"   ✅ SUCESSO: Premissa removida")
        else:
            print(f"   ✅ OK: Texto sem premissa preservado")

if __name__ == "__main__":
    success = debug_config_flow()
    test_method_isolation()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 RESULTADO: Configuração funcionando corretamente!")
    else:
        print("💥 RESULTADO: Problema na configuração ou fluxo!")