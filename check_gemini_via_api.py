import requests
import json

# URL do endpoint para verificar status das chaves Gemini
url = "http://127.0.0.1:5000/api/settings/gemini-quota-status"

try:
    # Fazer requisição para o endpoint
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print("Status das Chaves Gemini:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        # Adicionar informações de depuração
        if data.get('success'):
            keys_data = data.get('data', {}).get('keys', [])
            print(f"\n=== DEBUG ===")
            print(f"Número de chaves encontradas: {len(keys_data)}")
            for key in keys_data:
                print(f"Chave {key.get('key_id')}: Uso={key.get('usage_current')}, Status={key.get('status')}")
            
            summary = data.get('data', {}).get('summary', {})
            print(f"\nResumo:")
            print(f"Total de chaves: {summary.get('total_keys')}")
            print(f"Chaves ativas: {summary.get('active_keys')}")
            print(f"Chaves exauridas: {summary.get('exhausted_keys')}")
            print(f"Requisições hoje: {summary.get('total_requests_today')}")
    else:
        print(f"Erro na requisição: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"Erro ao conectar ao servidor: {e}")
    print("Verifique se o backend está rodando em http://127.0.0.1:5000")