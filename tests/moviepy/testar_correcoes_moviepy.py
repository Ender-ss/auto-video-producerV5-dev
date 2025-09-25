#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TESTE DAS CORREÇÕES DO MOVIEPY
Script para testar se as correções funcionaram corretamente
"""

import sys
import os
import traceback

def test_moviepy_imports():
    """Testar importações do MoviePy após as correções"""
    print("=" * 60)
    print("TESTANDO IMPORTAÇÕES DO MOVIEPY APÓS CORREÇÕES")
    print("=" * 60)
    
    # Testar importação direta dos componentes
    try:
        from moviepy import VideoFileClip, ImageClip, AudioFileClip, CompositeVideoClip
        print("✅ Importação direta de componentes do MoviePy bem-sucedida")
    except ImportError as e:
        print(f"❌ Falha na importação direta: {e}")
        return False
    
    # Testar importação com tratamento de erro
    try:
        try:
            from moviepy import TextClip, concatenate_videoclips, ColorClip
            MOVIEPY_AVAILABLE = True
            print("✅ Importação com tratamento de erro bem-sucedida")
        except ImportError as e:
            print(f"⚠️ MoviePy não disponível: {e}")
            MOVIEPY_AVAILABLE = False
            TextClip = concatenate_videoclips = ColorClip = None
    except Exception as e:
        print(f"❌ Erro no tratamento de importação: {e}")
        return False
    
    # Testar importação dos módulos principais
    try:
        import moviepy
        print(f"✅ MoviePy importado com sucesso - versão: {moviepy.__version__}")
    except ImportError as e:
        print(f"❌ Falha ao importar moviepy: {e}")
        return False
    
    # Testar componentes específicos
    components_to_test = [
        'VideoFileClip', 'ImageClip', 'AudioFileClip', 'CompositeVideoClip',
        'TextClip', 'concatenate_videoclips', 'ColorClip'
    ]
    
    for component in components_to_test:
        try:
            module = __import__('moviepy', fromlist=[component])
            if hasattr(module, component):
                print(f"✅ Componente {component} disponível")
            else:
                print(f"❌ Componente {component} não disponível")
        except Exception as e:
            print(f"❌ Erro ao verificar componente {component}: {e}")
    
    print("=" * 60)
    return True

def test_application_files():
    """Testar se os arquivos da aplicação podem ser importados sem erros"""
    print("TESTANDO ARQUIVOS DA APLICAÇÃO")
    print("=" * 60)
    
    files_to_test = [
        'backend.routes.videos',
        'backend.services.video_creation_service'
    ]
    
    success_count = 0
    
    for module_name in files_to_test:
        try:
            __import__(module_name)
            print(f"✅ {module_name} importado com sucesso")
            success_count += 1
        except Exception as e:
            print(f"❌ Erro ao importar {module_name}: {e}")
            traceback.print_exc()
    
    print("=" * 60)
    print(f"Arquivos importados com sucesso: {success_count}/{len(files_to_test)}")
    print("=" * 60)
    
    return success_count == len(files_to_test)

if __name__ == "__main__":
    print("Iniciando testes das correções do MoviePy...")
    
    # Testar importações do MoviePy
    moviepy_ok = test_moviepy_imports()
    
    # Testar arquivos da aplicação
    app_ok = test_application_files()
    
    # Resultado final
    if moviepy_ok and app_ok:
        print("🎉 TODOS OS TESTES PASSARAM! As correções foram bem-sucedidas.")
        sys.exit(0)
    else:
        print("❌ ALGUNS TESTES FALHARAM. Verifique os erros acima.")
        sys.exit(1)
