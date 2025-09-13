import os
import re

# Definir o diretório raiz do projeto
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(PROJECT_ROOT, 'backend')

# Lista de diretórios e extensões de arquivo a serem processados
TARGET_DIRS = [BACKEND_DIR]
TARGET_EXTENSIONS = ['.py']

# Expressão regular para encontrar as importações do moviepy.editor
IMPORT_PATTERN = re.compile(r'from\s+moviepy\.editor\s+import\s+(.+)')

# Função para corrigir as importações em um arquivo
def fix_file_imports(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Encontrar todas as correspondências
        matches = IMPORT_PATTERN.findall(content)
        if not matches:
            return False  # Nenhuma correspondência encontrada
        
        # Criar novo conteúdo com as importações corrigidas
        new_content = IMPORT_PATTERN.sub(r'from moviepy import \1', content)
        
        # Salvar o arquivo corrigido
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✓ Corrigido: {file_path}")
        return True
    except Exception as e:
        print(f"✗ Erro ao corrigir {file_path}: {e}")
        return False

# Função principal
if __name__ == "__main__":
    print("🔧 Iniciando correção das importações do MoviePy nos arquivos do backend...")
    print(f"Diretórios alvo: {TARGET_DIRS}")
    print(f"Extensões alvo: {TARGET_EXTENSIONS}")
    print("=" * 80)
    
    total_files = 0
    fixed_files = 0
    
    # Percorrer todos os diretórios e subdiretórios
    for dir_path in TARGET_DIRS:
        for root, _, files in os.walk(dir_path):
            for file in files:
                # Verificar se a extensão do arquivo é uma das alvo
                if any(file.endswith(ext) for ext in TARGET_EXTENSIONS):
                    file_path = os.path.join(root, file)
                    total_files += 1
                    if fix_file_imports(file_path):
                        fixed_files += 1
    
    print("=" * 80)
    print(f"✅ Processamento concluído!")
    print(f"Total de arquivos verificados: {total_files}")
    print(f"Total de arquivos corrigidos: {fixed_files}")
    print("\n📝 Próximos passos:")
    print("1. Execute pip install moviepy==2.1.2 --force-reinstall --no-cache-dir")
    print("2. Reinicie o backend")
    print("3. Teste as funcionalidades do MoviePy")