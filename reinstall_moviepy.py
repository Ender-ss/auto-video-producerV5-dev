# coding: utf-8
import os
import sys

print("Iniciando reinstalação do MoviePy e dependências...")

# Tentar atualizar o pip usando python -m pip
print("Atualizando o pip...")
os.system(f"python -m pip install --upgrade pip")

# Tentar reinstalar o MoviePy e todas as dependências
print("Reinstalando o MoviePy e dependências...")
os.system(f"python -m pip install --upgrade moviepy imageio imageio-ffmpeg numpy pillow proglog")

# Tentar instalar o MoviePy em modo usuário
print("Tentando instalar o MoviePy em modo usuário...")
os.system(f"python -m pip install --user --upgrade moviepy")

print("\nVerificando instalação básica do MoviePy...")
try:
    # Tentar importar o MoviePy
    import moviepy
    print(f"MoviePy importado com sucesso! Versão: {moviepy.__version__}")
    
    # Tentar importar componentes básicos
    try:
        import imageio
        print(f"Imageio importado com sucesso! Versão: {imageio.__version__}")
    except ImportError:
        print("Erro: Não foi possível importar o imageio.")
        
    try:
        import numpy
        print(f"NumPy importado com sucesso! Versão: {numpy.__version__}")
    except ImportError:
        print("Erro: Não foi possível importar o NumPy.")
        
    try:
        import pillow
        print(f"Pillow importado com sucesso! Versão: {pillow.__version__}")
    except ImportError:
        try:
            # Pillow às vezes é importado como PIL
            import PIL
            print(f"Pillow/PIL importado com sucesso! Versão: {PIL.__version__}")
        except ImportError:
            print("Erro: Não foi possível importar o Pillow/PIL.")
            
    print("\nInstruções para prosseguir:")
    print("1. Verifique se o Python está corretamente instalado no sistema")
    print("2. Certifique-se de que o caminho do Python e do Scripts está no PATH do sistema")
    print("3. Instale o ffmpeg e adicione-o ao PATH (necessário para o MoviePy funcionar)")
    print("4. Após resolver esses problemas, execute novamente a pipeline")
    
    # Salvar informações em um arquivo
    with open('moviepy_reinstall_log.txt', 'w', encoding='utf-8') as f:
        f.write("Relatório de reinstalação do MoviePy\n")
        f.write(f"MoviePy versão: {moviepy.__version__}\n")
        try:
            f.write(f"Imageio versão: {imageio.__version__}\n")
        except:
            f.write("Imageio não importado\n")
        try:
            f.write(f"NumPy versão: {numpy.__version__}\n")
        except:
            f.write("NumPy não importado\n")
        f.write("Reinstalação concluída\n")
    
except ImportError as e:
    print(f"Erro: Não foi possível importar o MoviePy após reinstalação. Erro: {str(e)}")
    print("\nSugestões:")
    print("1. Verifique se o Python está corretamente instalado")
    print("2. Tente reinstalar o Python do zero")
    print("3. Certifique-se de ter permissões administrativas")
    print("4. Considere usar um ambiente virtual Python")
    
    with open('moviepy_reinstall_log.txt', 'w', encoding='utf-8') as f:
        f.write("Falha na reinstalação do MoviePy\n")
        f.write(f"Erro: {str(e)}\n")
except Exception as e:
    print(f"Ocorreu um erro durante a reinstalação: {str(e)}")
    with open('moviepy_reinstall_log.txt', 'w', encoding='utf-8') as f:
        f.write("Erro desconhecido durante reinstalação\n")
        f.write(f"Erro: {str(e)}\n")