import urllib.request
import os

try:
    # URL do script get-pip.py oficial
    url = 'https://bootstrap.pypa.io/get-pip.py'
    # Nome do arquivo de destino
    filename = 'get-pip.py'
    
    print(f'Baixando {url} para {filename}...')
    # Baixar o arquivo
    urllib.request.urlretrieve(url, filename)
    print(f'Arquivo baixado com sucesso!')
    
    print('Executando o script get-pip.py...')
    # Executar o script
    os.system(f'python {filename}')
    
    print('Instalação do pip concluída com sucesso!')
except Exception as e:
    print(f'Ocorreu um erro: {str(e)}')