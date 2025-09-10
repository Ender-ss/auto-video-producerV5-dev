#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Investigação do padrão Arthur Blackwood
Testa diferentes variações para entender por que a IA usa esse nome
"""

import sys
import os
import requests
import json
from datetime import datetime

# Adicionar o diretório backend ao path
sys.path.insert(0, 'backend')

print('=== INVESTIGAÇÃO DO PADRÃO ARTHUR BLACKWOOD ===')
print(f'Data/Hora: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print()

url = 'http://localhost:5000/api/premise/generate'
headers = {'Content-Type': 'application/json'}

# Teste 1: Prompt original do agente milionário
prompt_original = """Crie uma premissa narrativa para história de milionário sobre: {title}.
A premissa deve incluir:
- Personagem milionário/rico com vida aparentemente perfeita
- Personagem de classe baixa com qualidades humanas especiais
- Situação que os conecta (trabalho, acaso, família)
- Descoberta emocional que muda perspectivas
- Contraste entre riqueza material e riqueza humana
- Aproximadamente 200 palavras"""

# Teste 2: Prompt modificado com instrução específica de nomes
prompt_com_instrucao_nomes = """Crie uma premissa narrativa para história de milionário sobre: {title}.
A premissa deve incluir:
- Personagem milionário/rico com vida aparentemente perfeita (use nomes BRASILEIROS variados)
- Personagem de classe baixa com qualidades humanas especiais
- Situação que os conecta (trabalho, acaso, família)
- Descoberta emocional que muda perspectivas
- Contraste entre riqueza material e riqueza humana
- Aproximadamente 200 palavras

IMPORTANTE: Use nomes brasileiros únicos e variados. Evite repetir nomes de exemplos anteriores."""

# Teste 3: Prompt completamente diferente
prompt_alternativo = """Crie uma história sobre contraste social envolvendo: {title}.
Elementos necessários:
- Protagonista rico com problemas emocionais
- Personagem humilde com sabedoria de vida
- Encontro que muda ambas as vidas
- Lição sobre valores verdadeiros
- Aproximadamente 200 palavras

Use nomes brasileiros únicos para os personagens."""

# Teste 4: Prompt em inglês
prompt_ingles = """Create a narrative premise for a millionaire story about: {title}.
The premise should include:
- Rich character with apparently perfect but empty life
- Poor character with special human qualities
- Situation that connects them
- Emotional discovery that changes perspectives
- Contrast between material and human wealth
- Approximately 200 words

Use diverse Brazilian names for characters."""

testes = [
    {
        'nome': 'PROMPT ORIGINAL (Agente Milionário)',
        'prompt': prompt_original,
        'titulo': 'A Transformação do Magnata Solitário'
    },
    {
        'nome': 'PROMPT COM INSTRUÇÃO DE NOMES',
        'prompt': prompt_com_instrucao_nomes,
        'titulo': 'A Transformação do Magnata Solitário'
    },
    {
        'nome': 'PROMPT ALTERNATIVO',
        'prompt': prompt_alternativo,
        'titulo': 'A Transformação do Magnata Solitário'
    },
    {
        'nome': 'PROMPT EM INGLÊS',
        'prompt': prompt_ingles,
        'titulo': 'A Transformação do Magnata Solitário'
    },
    {
        'nome': 'TÍTULO DIFERENTE + PROMPT ORIGINAL',
        'prompt': prompt_original,
        'titulo': 'O Empresário que Mudou de Vida'
    }
]

resultados = []

for i, teste in enumerate(testes, 1):
    print(f'\n🧪 TESTE {i}: {teste["nome"]}')
    print(f'Título: {teste["titulo"]}')
    print('='*50)
    
    # Preparar prompt
    prompt_final = teste['prompt'].replace('{title}', teste['titulo'])
    
    data = {
        'titles': [teste['titulo']],
        'prompt': prompt_final,
        'ai_provider': 'gemini',
        'script_size': 'medio',
        'use_custom_prompt': True,
        'custom_prompt': prompt_final
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get('success'):
                premises = result.get('premises', [])
                
                if premises:
                    premise = premises[0]
                    content = premise.get('premise', 'Sem conteúdo')
                    
                    print(f'✅ Premissa gerada')
                    print(f'Palavras: {len(content.split())}')
                    
                    # Analisar nomes usados
                    content_lower = content.lower()
                    
                    # Verificar Arthur Blackwood
                    if 'arthur blackwood' in content_lower:
                        print('❌ CONTÉM "Arthur Blackwood"')
                        resultado = 'ARTHUR_BLACKWOOD'
                    elif 'arthur' in content_lower:
                        print('⚠️ Contém "Arthur" (sem Blackwood)')
                        resultado = 'ARTHUR_APENAS'
                    elif 'blackwood' in content_lower:
                        print('⚠️ Contém "Blackwood" (sem Arthur)')
                        resultado = 'BLACKWOOD_APENAS'
                    else:
                        print('✅ Não contém nomes problemáticos')
                        resultado = 'LIMPO'
                    
                    # Extrair nomes mencionados
                    import re
                    nomes_encontrados = re.findall(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', content)
                    print(f'Nomes encontrados: {nomes_encontrados}')
                    
                    resultados.append({
                        'teste': teste['nome'],
                        'resultado': resultado,
                        'nomes': nomes_encontrados,
                        'conteudo': content[:200] + '...'
                    })
                    
                    print(f'\n📄 TRECHO DA PREMISSA:')
                    print(content[:300] + '...')
                    
                else:
                    print('❌ Nenhuma premissa retornada')
                    resultados.append({
                        'teste': teste['nome'],
                        'resultado': 'ERRO_SEM_PREMISSA',
                        'nomes': [],
                        'conteudo': ''
                    })
            else:
                error = result.get('error', 'Erro desconhecido')
                print(f'❌ Erro na geração: {error}')
                resultados.append({
                    'teste': teste['nome'],
                    'resultado': 'ERRO_GERACAO',
                    'nomes': [],
                    'conteudo': error
                })
        else:
            print(f'❌ Erro HTTP: {response.status_code}')
            resultados.append({
                'teste': teste['nome'],
                'resultado': 'ERRO_HTTP',
                'nomes': [],
                'conteudo': f'HTTP {response.status_code}'
            })
            
    except Exception as e:
        print(f'❌ Erro: {e}')
        resultados.append({
            'teste': teste['nome'],
            'resultado': 'ERRO_EXCECAO',
            'nomes': [],
            'conteudo': str(e)
        })
    
    print('\n⏳ Aguardando 2 segundos...')
    import time
    time.sleep(2)

# Resumo final
print('\n' + '='*60)
print('📊 RESUMO DA INVESTIGAÇÃO')
print('='*60)

arthur_blackwood_count = 0
arthur_apenas_count = 0
limpo_count = 0

for resultado in resultados:
    print(f'\n🧪 {resultado["teste"]}')
    print(f'   Resultado: {resultado["resultado"]}')
    print(f'   Nomes: {resultado["nomes"]}')
    
    if resultado['resultado'] == 'ARTHUR_BLACKWOOD':
        arthur_blackwood_count += 1
    elif resultado['resultado'] == 'ARTHUR_APENAS':
        arthur_apenas_count += 1
    elif resultado['resultado'] == 'LIMPO':
        limpo_count += 1

print(f'\n📈 ESTATÍSTICAS:')
print(f'   Arthur Blackwood: {arthur_blackwood_count}/{len(resultados)}')
print(f'   Apenas Arthur: {arthur_apenas_count}/{len(resultados)}')
print(f'   Limpo: {limpo_count}/{len(resultados)}')

print(f'\n🔍 CONCLUSÕES:')
if arthur_blackwood_count > 0:
    print('   ❌ O problema persiste mesmo com modificações no prompt')
    print('   📝 Isso indica que pode ser um padrão da IA Gemini para esse tipo de história')
else:
    print('   ✅ As modificações no prompt resolveram o problema')
    print('   📝 O problema estava relacionado ao prompt específico')

print(f'\n✅ INVESTIGAÇÃO CONCLUÍDA!')
print(f'Hora de término: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')