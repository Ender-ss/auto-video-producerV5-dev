import requests
import json

url = "http://localhost:5000/api/pipelines/?status=running"

try:
    response = requests.get(url)
    response.raise_for_status()
    
    result = response.json()
    
    if result.get('success'):
        pipelines = result['data']['pipelines']
        print(f"Pipelines em execução: {len(pipelines)}")
        
        if pipelines:
            for pipeline in pipelines:
                print(f"\nID: {pipeline['pipeline_id']}")
                print(f"Título: {pipeline['title']}")
                print(f"Status: {pipeline['status']}")
                print(f"Etapa atual: {pipeline['current_step']}")
                print(f"Progresso: {pipeline['progress']}%")
                
                # Verificar se há erros específicos
                if 'video_step_error' in pipeline and pipeline['video_step_error']:
                    print(f"Erro na etapa de vídeo: {pipeline['video_step_error']}")
                
                print("-" * 50)
        else:
            print("Nenhuma pipeline em execução encontrada.")
            
            # Verificar pipelines com outros status
            print("\nVerificando pipelines com status 'processing'...")
            url_processing = "http://localhost:5000/api/pipelines/?status=processing"
            response_processing = requests.get(url_processing)
            
            if response_processing.status_code == 200:
                result_processing = response_processing.json()
                if result_processing.get('success'):
                    processing_pipelines = result_processing['data']['pipelines']
                    print(f"Pipelines processando: {len(processing_pipelines)}")
                    
                    for pipeline in processing_pipelines:
                        print(f"\nID: {pipeline['pipeline_id']}")
                        print(f"Título: {pipeline['title']}")
                        print(f"Status: {pipeline['status']}")
                        print(f"Etapa atual: {pipeline['current_step']}")
                        print(f"Progresso: {pipeline['progress']}%")
                        
                        if 'video_step_error' in pipeline and pipeline['video_step_error']:
                            print(f"Erro na etapa de vídeo: {pipeline['video_step_error']}")
    else:
        print(f"Erro na resposta: {result}")

except requests.exceptions.RequestException as e:
    print(f"Erro na requisição: {e}")
except json.JSONDecodeError:
    print(f"Erro ao decodificar JSON: {response.text}")