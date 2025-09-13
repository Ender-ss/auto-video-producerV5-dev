import os
import re

# Definir o diretório raiz do projeto
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(PROJECT_ROOT, 'backend')

# Lista de diretórios a serem processados
TARGET_DIRS = [BACKEND_DIR]

# Extensões de arquivo a serem processadas
TARGET_EXTENSIONS = ['.py']

# Diretórios a serem ignorados
IGNORE_DIRS = [
    '__pycache__',
    '.venv',
    'venv',
    'node_modules',
    'dist',
    'build',
    'backup',
    '.git'
]

# Padrões de arquivo a serem ignorados
IGNORE_FILE_PATTERNS = [
    r'\.backup_',
    r'_backup\.',
    r'~'
]

# Expressão regular para encontrar as importações do moviepy.editor
IMPORT_PATTERN = re.compile(r'from\s+moviepy\.editor\s+import\s+(.+)')

# Função para verificar se um diretório deve ser ignorado
def should_ignore_dir(dir_path):
    for ignore in IGNORE_DIRS:
        if ignore in dir_path.split(os.sep):
            return True
    return False

# Função para verificar se um arquivo deve ser ignorado
def should_ignore_file(file_name):
    for pattern in IGNORE_FILE_PATTERNS:
        if re.search(pattern, file_name):
            return True
    return False

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
    print("🔧 Iniciando correção das importações do MoviePy nos arquivos do projeto...")
    print(f"Diretórios alvo: {TARGET_DIRS}")
    print(f"Extensões alvo: {TARGET_EXTENSIONS}")
    print(f"Diretórios ignorados: {IGNORE_DIRS}")
    print("=" * 80)
    
    total_files = 0
    fixed_files = 0
    
    # Percorrer todos os diretórios e subdiretórios
    for dir_path in TARGET_DIRS:
        for root, dirs, files in os.walk(dir_path):
            # Filtrar diretórios a serem ignorados
            dirs[:] = [d for d in dirs if not should_ignore_dir(os.path.join(root, d))]
            
            for file in files:
                # Verificar se a extensão do arquivo é uma das alvo e se não deve ser ignorado
                if any(file.endswith(ext) for ext in TARGET_EXTENSIONS) and not should_ignore_file(file):
                    file_path = os.path.join(root, file)
                    total_files += 1
                    if fix_file_imports(file_path):
                        fixed_files += 1
    
    print("=" * 80)
    print(f"✅ Processamento concluído!")
    print(f"Total de arquivos verificados: {total_files}")
    print(f"Total de arquivos corrigidos: {fixed_files}")
    print("\n📝 Próximos passos:")
    print("1. Reinicie o backend")
    print("2. Execute o script de teste para verificar se as importações estão funcionando")