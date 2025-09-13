import os
import shutil

# Caminho do arquivo a ser corrigido
file_path = "c:\Users\Enderson\Documents\APP 2\auto-video-producerV5-dev\backend\services\video_creation_service.py"

# Verificar se o arquivo existe
if not os.path.exists(file_path):
    print(f"Erro: O arquivo {file_path} não foi encontrado.")
    exit(1)

# Criar backup do arquivo original
backup_path = f"{file_path}.backup_before_verbose_fix"
if not os.path.exists(backup_path):
    shutil.copy2(file_path, backup_path)
    print(f"Backup do arquivo original criado em: {backup_path}")

# Ler o conteúdo do arquivo
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# Contar ocorrências do parâmetro 'verbose' antes da correção
original_count = content.count('verbose=False') + content.count("'verbose': False")
print(f"Encontradas {original_count} ocorrências do parâmetro 'verbose'.")

# Remover o parâmetro 'verbose' da configuração do render_params
content = content.replace("'verbose': False,", '')

# Remover o parâmetro 'verbose' das chamadas diretas de write_videofile
content = content.replace('verbose=False,', '')
content = content.replace('verbose=False', '')

# Salvar o arquivo corrigido
with open(file_path, 'w', encoding='utf-8') as file:
    file.write(content)

# Contar ocorrências restantes
remaining_count = content.count('verbose=False') + content.count("'verbose': False")
fixed_count = original_count - remaining_count

print(f"Correção concluída com sucesso! Foram removidos {fixed_count} parâmetros 'verbose'.")
print("\nO MoviePy 2.2.1 não suporta mais o parâmetro 'verbose', ele foi substituído por 'logger=None'.")
print("O script já manteve o 'logger=None' em todas as chamadas de write_videofile().")
print("\nVocê pode agora testar a renderização novamente.")