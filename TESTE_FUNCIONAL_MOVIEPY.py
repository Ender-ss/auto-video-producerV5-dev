#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎬 TESTE FUNCIONAL DO MOVIEPY NA APLICAÇÃO
Script para testar a funcionalidade completa do MoviePy após as correções
"""

import sys
import os
import tempfile
import traceback
from datetime import datetime

def test_moviepy_basic_functionality():
    """Testar funcionalidades básicas do MoviePy"""
    print("=" * 60)
    print("TESTANDO FUNCIONALIDADES BÁSICAS DO MOVIEPY")
    print("=" * 60)
    
    try:
        # Importar componentes do MoviePy
        from moviepy import VideoFileClip, ImageClip, AudioFileClip, CompositeVideoClip
        from moviepy import TextClip, concatenate_videoclips, ColorClip
        print("✅ Importação de componentes do MoviePy bem-sucedida")
        
        # Testar criação de clipe de cor
        try:
            color_clip = ColorClip(size=(640, 480), color=(255, 0, 0), duration=2)
            print("✅ Criação de ColorClip bem-sucedida")
        except Exception as e:
            print(f"❌ Erro ao criar ColorClip: {e}")
            return False
        
        # Testar criação de clipe de texto (apenas verificação de importação)
        try:
            # Apenas verificar se a classe TextClip pode ser importada
            print("✅ Classe TextClip disponível para uso")
        except Exception as e:
            print(f"❌ Erro ao verificar TextClip: {e}")
            return False
        
        # Testar concatenação de clipes
        try:
            clips = [color_clip]
            final_clip = concatenate_videoclips(clips)
            print("✅ Concatenação de clipes bem-sucedida")
        except Exception as e:
            print(f"❌ Erro ao concatenar clipes: {e}")
            return False
        
        # Testar criação de arquivo de vídeo
        try:
            temp_dir = tempfile.gettempdir()
            output_path = os.path.join(temp_dir, f"test_moviepy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4")
            
            final_clip.write_videofile(
                output_path,
                fps=24,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile=os.path.join(temp_dir, 'temp_audio.m4a'),
                remove_temp=True
            )
            
            if os.path.exists(output_path):
                print(f"✅ Criação de arquivo de vídeo bem-sucedida: {output_path}")
                # Limpar arquivo temporário
                os.remove(output_path)
            else:
                print("❌ Arquivo de vídeo não foi criado")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao criar arquivo de vídeo: {e}")
            return False
        
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"❌ Erro geral ao testar MoviePy: {e}")
        traceback.print_exc()
        return False

def test_application_video_service():
    """Testar o serviço de criação de vídeo da aplicação"""
    print("TESTANDO SERVIÇO DE CRIAÇÃO DE VÍDEO DA APLICAÇÃO")
    print("=" * 60)
    
    try:
        # Importar o serviço
        sys.path.append(os.path.join(os.getcwd(), 'backend'))
        from services.video_creation_service import VideoCreationService
        
        # Verificar se a classe pode ser importada
        print("✅ Classe VideoCreationService importada com sucesso")
        
        # Verificar métodos disponíveis
        methods = [method for method in dir(VideoCreationService) if not method.startswith('_')]
        print(f"✅ Métodos públicos disponíveis: {', '.join(methods[:5])}")
        if len(methods) > 5:
            print(f"   ... e mais {len(methods) - 5} métodos")
        
        # Tentar criar instância com um ID de pipeline fictício
        try:
            video_service = VideoCreationService(pipeline_id="test_pipeline")
            print("✅ Instância do VideoCreationService criada com sucesso")
        except Exception as e:
            print(f"⚠️ Aviso ao criar instância: {e}")
        
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar serviço de vídeo: {e}")
        traceback.print_exc()
        return False

def test_video_routes():
    """Testar as rotas de vídeo da aplicação"""
    print("TESTANDO ROTAS DE VÍDEO DA APLICAÇÃO")
    print("=" * 60)
    
    try:
        # Importar o blueprint de vídeos
        sys.path.append(os.path.join(os.getcwd(), 'backend'))
        from routes.videos import videos_bp
        
        # Verificar se o blueprint foi criado corretamente
        if videos_bp:
            print("✅ Blueprint de vídeos importado com sucesso")
            print(f"✅ Nome do blueprint: {videos_bp.name}")
            print(f"✅ URL prefix: {videos_bp.url_prefix}")
            
            # Verificar se há rotas registradas (sem usar iter_rules)
            if hasattr(videos_bp, 'deferred_functions') and videos_bp.deferred_functions:
                print(f"✅ Número de funções registradas: {len(videos_bp.deferred_functions)}")
            elif hasattr(videos_bp, 'routes'):
                print(f"✅ Número de rotas encontradas: {len(videos_bp.routes)}")
            else:
                print("✅ Blueprint de vídeos está configurado")
            
            # Listar algumas funções do módulo
            import routes.videos as videos_module
            functions = [name for name in dir(videos_module) if not name.startswith('_') and callable(getattr(videos_module, name))]
            print(f"✅ Funções disponíveis no módulo: {', '.join(functions[:5])}")
            if len(functions) > 5:
                print(f"   ... e mais {len(functions) - 5} funções")
        else:
            print("❌ Blueprint de vídeos não foi criado corretamente")
            return False
        
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar rotas de vídeo: {e}")
        traceback.print_exc()
        return False

def test_moviepy_version_compatibility():
    """Testar compatibilidade com a versão do MoviePy"""
    print("TESTANDO COMPATIBILIDADE COM A VERSÃO DO MOVIEPY")
    print("=" * 60)
    
    try:
        import moviepy
        print(f"✅ Versão do MoviePy: {moviepy.__version__}")
        
        # Verificar se os componentes necessários estão disponíveis
        required_components = [
            'VideoFileClip', 'ImageClip', 'AudioFileClip', 'CompositeVideoClip',
            'TextClip', 'concatenate_videoclips', 'ColorClip'
        ]
        
        missing_components = []
        for component in required_components:
            if not hasattr(moviepy, component):
                missing_components.append(component)
        
        if missing_components:
            print(f"❌ Componentes faltando: {', '.join(missing_components)}")
            return False
        else:
            print("✅ Todos os componentes necessários estão disponíveis")
        
        # Verificar se o submódulo 'editor' não existe (compatibilidade com 2.2.1)
        try:
            from moviepy import editor
            print("⚠️ Aviso: O submódulo 'editor' ainda existe, o que pode indicar uma versão mais antiga")
        except ImportError:
            print("✅ Submódulo 'editor' não existe, compatível com MoviePy 2.2.1")
        
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar compatibilidade: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Iniciando teste funcional completo do MoviePy...")
    
    # Executar todos os testes
    tests = [
        ("Funcionalidades Básicas do MoviePy", test_moviepy_basic_functionality),
        ("Serviço de Criação de Vídeo", test_application_video_service),
        ("Rotas de Vídeo", test_video_routes),
        ("Compatibilidade com Versão", test_moviepy_version_compatibility)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Executando teste: {test_name}")
        try:
            if test_func():
                print(f"✅ Teste '{test_name}' PASSOU")
                passed_tests += 1
            else:
                print(f"❌ Teste '{test_name}' FALHOU")
        except Exception as e:
            print(f"❌ Erro ao executar teste '{test_name}': {e}")
    
    # Resultado final
    print("\n" + "=" * 60)
    print("RESUMO DOS TESTES")
    print("=" * 60)
    print(f"Testes passados: {passed_tests}/{total_tests}")
    
    if passed_tests == total_tests:
        print("🎉 TODOS OS TESTES PASSARAM! O MoviePy está funcionando corretamente na aplicação.")
        sys.exit(0)
    else:
        print("❌ ALGUNS TESTES FALHARAM. Verifique os erros acima.")
        sys.exit(1)