import sqlite3
import requests
import time

pipeline_id = '52877cd3-b105-4263-b556-a99f57d33b22'

# Aguardar processamento
print('Aguardando 30 segundos para processamento...')
time.sleep(30)

# Verificar status via API
response = requests.get(f'http://localhost:5000/api/pipeline/{pipeline_id}/status')
if response.status_code == 200:
    status = response.json()
    print(f'\nStatus da pipeline: {status.get("status")}')
    print(f'Progresso: {status.get("progress", 0)}%')
    print(f'Etapas: {status.get("steps", {})}')
    
    # Verificar se há resultados de títulos
    if 'titles' in status.get('steps', {}):
        titles_step = status['steps']['titles']
        print(f'\nEtapa Titles:')
        print(f'  Status: {titles_step.get("status")}')
        print(f'  Progresso: {titles_step.get("progress", 0)}%')
        if titles_step.get('result'):
            print(f'  Resultado: {titles_step["result"]}')
    
    # Verificar se há resultados de premissas
    if 'premises' in status.get('steps', {}):
        premises_step = status['steps']['premises']
        print(f'\nEtapa Premises:')
        print(f'  Status: {premises_step.get("status")}')
        print(f'  Progresso: {premises_step.get("progress", 0)}%')
        if premises_step.get('result'):
            print(f'  Resultado: {premises_step["result"]}')
else:
    print(f'\nErro ao verificar status: {response.status_code}')