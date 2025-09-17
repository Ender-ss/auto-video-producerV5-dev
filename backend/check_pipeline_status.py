import requests
import json

# ID do pipeline retornado na criação
pipeline_id = "5a4600a3-cc34-4f42-ae18-44e1ffd0fc9f"

# URL do backend
url = f"http://localhost:5000/api/pipeline/status/{pipeline_id}"

# Headers
headers = {
    "Content-Type": "application/json"
}

# Enviar requisição
response = requests.get(url, headers=headers)

# Verificar resposta
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")

if response.status_code == 200:
    try:
        response_json = json.loads(response.text)
        print("\nResponse JSON:")
        print(json.dumps(response_json, indent=2))
    except:
        print("\nResponse is not valid JSON")
else:
    print("\nHeaders:")
    print(response.headers)