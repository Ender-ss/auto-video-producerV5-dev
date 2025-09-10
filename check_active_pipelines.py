import requests
import json

url = "http://localhost:5000/api/pipelines/"

try:
    response = requests.get(url)
    response.raise_for_status()
    
    result = response.json()
    
    if result.get('success'):
        pipelines = result['data']['pipelines']
        print(f"Total de pipelines encontradas: {len(pipelines)}")
        
        if pipelines:
            print("\nPipelines ativas:")
            for pipeline in pipelines:
                print(f"ID: {pipeline['pipeline_id']}")
                print(f"Título: {pipeline['title']}")
                print(f"Status: {pipeline['status']}")
                print(f"Etapa atual: {pipeline['current_step']}")
                print(f"Progresso: {pipeline['progress']}%")
                print("-" * 50)
        else:
            print("Nenhuma pipeline encontrada.")
    else:
        print(f"Erro na resposta: {result}")

except requests.exceptions.RequestException as e:
    print(f"Erro na requisição: {e}")
except json.JSONDecodeError:
    print(f"Erro ao decodificar JSON: {response.text}")