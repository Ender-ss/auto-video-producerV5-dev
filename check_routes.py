#!/usr/bin/env python3
"""
Script para verificar as rotas registradas no servidor em execução
"""

import requests
import json

def check_routes():
    """Verificar rotas disponíveis no servidor"""
    try:
        # Testar rota principal
        response = requests.get('/')
        print(f"Rota principal (/): {response.status_code}")
        if response.status_code == 200:
            print(f"Resposta: {response.json()}")
        
        # Testar rota de status do sistema
        response = requests.get('/api/system/status')
        print(f"\nRota /api/system/status: {response.status_code}")
        if response.status_code == 200:
            print(f"Resposta: {response.json()}")
        
        # Testar rota de pipelines
        response = requests.get('/api/pipelines')
        print(f"\nRota /api/pipelines: {response.status_code}")
        if response.status_code == 200:
            print(f"Resposta: {response.json()}")
        
        # Testar rota de pipeline active
        response = requests.get('/api/pipeline/active')
        print(f"\nRota /api/pipeline/active: {response.status_code}")
        if response.status_code == 200:
            print(f"Resposta: {response.json()}")
        else:
            print(f"Erro: {response.text}")
            
    except Exception as e:
        print(f"Erro ao verificar rotas: {e}")

if __name__ == "__main__":
    check_routes()