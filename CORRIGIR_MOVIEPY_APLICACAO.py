#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 CORREÇÃO DEFINITIVA DO MOVIEPY 2.2.1
Script para corrigir os problemas de importação do MoviePy na aplicação
"""

import os
import sys
import re
import shutil
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def backup_file(file_path):
    """Criar backup do arquivo original"""
    if os.path.exists(file_path):
        backup_path = f"{file_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(file_path, backup_path)
        logger.info(f"Backup criado: {backup_path}")
        return backup_path
    return None

def fix_moviepy_imports_in_file(file_path):
    """Corrigir importações do MoviePy em um arquivo específico"""
    if not os.path.exists(file_path):
        logger.warning(f"Arquivo não encontrado: {file_path}")
        return False
    
    try:
        # Ler o conteúdo do arquivo
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = []
        
        # 1. Corrigir importação direta do submódulo 'editor'
        # from moviepy import editor -> from moviepy import VideoFileClip, ImageClip, etc.
        if re.search(r'from\s+moviepy\s+import\s+editor', content):
            logger.info(f"Corrigindo importação de editor em: {file_path}")
            
            # Encontrar todas as referências a editor. no arquivo
            editor_usages = re.findall(r'editor\.(\w+)', content)
            unique_usages = list(set(editor_usages))
            
            if unique_usages:
                # Criar nova importação com os componentes específicos
                new_import = f"from moviepy import {', '.join(unique_usages)}"
                content = re.sub(
                    r'from\s+moviepy\s+import\s+editor',
                    new_import,
                    content
                )
                
                # Substituir todas as referências editor.componente por componente direto
                for usage in unique_usages:
                    content = re.sub(
                        rf'editor\.{usage}',
                        usage,
                        content
                    )
                
                changes_made.append(f"Importação de editor substituída por componentes específicos: {', '.join(unique_usages)}")
        
        # 2. Corrigir importação específica do editor
        # from moviepy.editor import ... -> from moviepy import ...
        if re.search(r'from\s+moviepy\.editor\s+import', content):
            logger.info(f"Corrigindo importação de moviepy.editor em: {file_path}")
            
            # Substituir from moviepy.editor import por from moviepy import
            content = re.sub(
                r'from\s+moviepy\.editor\s+import',
                'from moviepy import',
                content
            )
            
            changes_made.append("Importação de moviepy.editor corrigida para moviepy")
        
        # 3. Verificar se há referências a editor.py ou caminhos relacionados
        if 'editor.py' in content:
            logger.info(f"Removendo referências a editor.py em: {file_path}")
            
            # Remover ou comentar linhas que verificam a existência de editor.py
            content = re.sub(
                r'([^\n]*editor\.py[^\n]*)',
                r'# \1  # Removido - MoviePy 2.2.1 não possui arquivo editor.py',
                content
            )
            
            changes_made.append("Referências a editor.py removidas ou comentadas")
        
        # 4. Adicionar tratamento de erro para importações do MoviePy
        moviepy_import_pattern = r'from\s+moviepy(?:\.\w+)?\s+import'
        if re.search(moviepy_import_pattern, content) and 'try:' not in content[:500]:
            logger.info(f"Adicionando tratamento de erro para importações MoviePy em: {file_path}")
            
            # Encontrar a primeira importação do MoviePy
            first_import_match = re.search(moviepy_import_pattern, content)
            if first_import_match:
                # Extrair a linha de importação completa
                import_start = first_import_match.start()
                import_end = content.find('\n', import_start)
                import_line = content[import_start:import_end]
                
                # Criar bloco try-except
                try_except_block = f"""try:
    {import_line}
    MOVIEPY_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ MoviePy não disponível: {{e}}")
    MOVIEPY_AVAILABLE = False
    # Definir classes vazias para evitar erros
    VideoFileClip = ImageClip = AudioFileClip = CompositeVideoClip = None
    TextClip = concatenate_videoclips = ColorClip = None
"""
                
                # Substituir a linha de importação pelo bloco try-except
                content = content[:import_start] + try_except_block + content[import_end:]
                
                changes_made.append("Adicionado tratamento de erro para importações do MoviePy")
        
        # Se houve alterações, salvar o arquivo
        if changes_made and content != original_content:
            backup_path = backup_file(file_path)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"Arquivo corrigido: {file_path}")
            for change in changes_made:
                logger.info(f"  - {change}")
            
            return True
        else:
            logger.info(f"Nenhuma alteração necessária em: {file_path}")
            return False
            
    except Exception as e:
        logger.error(f"Erro ao processar arquivo {file_path}: {str(e)}")
        return False

def fix_application_files():
    """Corrigir todos os arquivos da aplicação que usam MoviePy"""
    logger.info("Iniciando correção dos arquivos da aplicação para MoviePy 2.2.1")
    
    # Arquivos principais da aplicação que precisam de correção
    app_files = [
        'backend/routes/videos.py',
        'backend/services/video_creation_service.py',
        'backend/check_moviepy_functions.py',
        'backend/log_moviepy_test.py',
        'backend/simple_moviepy_test.py',
        'backend/test_moviepy.py',
        'backend/ultra_simple_test.py',
        'backend/ultra_simple_test_v2.py',
        'backend/verify_moviepy_installation.py',
        'backend/very_simple_test.py'
    ]
    
    fixed_files = []
    failed_files = []
    
    for file_path in app_files:
        full_path = os.path.join(os.getcwd(), file_path)
        if fix_moviepy_imports_in_file(full_path):
            fixed_files.append(file_path)
        else:
            failed_files.append(file_path)
    
    # Resumo
    logger.info("=" * 60)
    logger.info("RESUMO DA CORREÇÃO")
    logger.info("=" * 60)
    logger.info(f"Arquivos corrigidos: {len(fixed_files)}")
    for file in fixed_files:
        logger.info(f"  ✓ {file}")
    
    if failed_files:
        logger.info(f"Arquivos não precisaram de correção: {len(failed_files)}")
        for file in failed_files:
            logger.info(f"  - {file}")
    
    logger.info("=" * 60)
    
    return len(fixed_files) > 0

def create_test_script():
    """Criar script para testar as correções"""
    test_script_content = '''#!/usr/bin/env python3
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
'''
    
    test_script_path = os.path.join(os.getcwd(), 'testar_correcoes_moviepy.py')
    with open(test_script_path, 'w', encoding='utf-8') as f:
        f.write(test_script_content)
    
    logger.info(f"Script de teste criado: {test_script_path}")
    return test_script_path

if __name__ == "__main__":
    try:
        # Corrigir arquivos da aplicação
        success = fix_application_files()
        
        if success:
            # Criar script de teste
            test_script = create_test_script()
            
            logger.info("🎉 CORREÇÕES CONCLUÍDAS COM SUCESSO!")
            logger.info(f"Execute o script de teste para verificar: python {os.path.basename(test_script)}")
        else:
            logger.info("ℹ️ Nenhum arquivo precisou de correção.")
        
    except Exception as e:
        logger.error(f"Erro durante a execução: {str(e)}")
        sys.exit(1)