"""
🖼️ Image Generation Routes
Rotas para geração de imagens com IA
"""

from flask import Blueprint, request, jsonify
import os
import requests
import base64
import time
import datetime
import json
from utils.error_messages import auto_format_error, format_error_response
from routes.prompts_config import load_prompts_config

images_bp = Blueprint('images', __name__)

# Diretório para salvar as imagens geradas
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'output', 'images')
os.makedirs(OUTPUT_DIR, exist_ok=True)

@images_bp.route('/generate-enhanced', methods=['POST'])
def generate_images_enhanced_route():
    """
    Gera imagens a partir de um roteiro usando divisão inteligente e opções avançadas.
    """
    try:
        data = request.get_json()
        
        # Parâmetros básicos
        script = data.get('script', '').strip()
        api_key = data.get('api_key', '').strip()
        provider = data.get('provider', 'pollinations')  # pollinations, together, gemini
        model = data.get('model', 'gpt')
        style_prompt = data.get('style', 'cinematic, high detail, 4k')
        format_size = data.get('format', '1024x1024')
        quality = data.get('quality', 'standard')
        pollinations_model = data.get('pollinations_model', 'gpt')  # gpt ou flux
        
        # Parâmetros avançados
        use_ai_agent = data.get('use_ai_agent', False)
        ai_agent_prompt = data.get('ai_agent_prompt', '')
        use_custom_prompt = data.get('use_custom_prompt', False)
        custom_prompt = data.get('custom_prompt', '').strip()
        use_custom_image_prompt = data.get('use_custom_image_prompt', False)
        custom_image_prompt = data.get('custom_image_prompt', '').strip()
        image_count = data.get('image_count', 1)
        selected_agent = data.get('selected_agent', None)
        
        # Novos parâmetros para divisão inteligente
        split_strategy = data.get('split_strategy', 'intelligent')  # intelligent ou traditional
        enable_variations = data.get('enable_variations', False)
        variation_intensity = data.get('variation_intensity', 1.0)
        target_scenes = data.get('target_scenes', None)
        
        # Validações
        if use_custom_prompt:
            if not custom_prompt:
                error_response = format_error_response('validation_error', 'Prompt personalizado é obrigatório quando selecionado', 'Geração de Imagens')
                return jsonify(error_response), 400
        else:
            if not script:
                error_response = format_error_response('validation_error', 'Roteiro é obrigatório para gerar imagens baseadas no conteúdo', 'Geração de Imagens')
                return jsonify(error_response), 400

        # Pollinations.ai e Gemini Reddit não requerem chave de API (são gratuitos)
        if not api_key and provider not in ['pollinations', 'gemini-reddit', 'gemini-imagen3', 'gemini-imagen3-rohitaryal']:
            error_response = format_error_response('api_key_missing', f'Chave da API ({provider}) é obrigatória', 'Geração de Imagens')
            return jsonify(error_response), 400

        # Validar cookies para provedores que exigem autenticação
        if provider == 'gemini-imagen3-rohitaryal':
            google_cookies = data.get('google_cookies', '')
            if not google_cookies:
                error_response = format_error_response('cookies_missing', 'Cookies de autenticação do Google são obrigatórios para o provedor gemini-imagen3-rohitaryal', 'Geração de Imagens')
                return jsonify(error_response), 400

        # Validar cookies para provedores que exigem autenticação
        if provider == 'gemini-imagen3-rohitaryal':
            google_cookies = data.get('google_cookies', '')
            if not google_cookies:
                error_response = format_error_response('cookies_missing', 'Cookies de autenticação do Google são obrigatórios para o provedor gemini-imagen3-rohitaryal', 'Geração de Imagens')
                return jsonify(error_response), 400

        # Processar formato da imagem
        try:
            width, height = map(int, format_size.split('x'))
        except ValueError:
            width, height = 1024, 1024

        generated_images = []
        prompts_to_generate = []

        # Determinar prompts baseado no modo selecionado
        if use_custom_prompt:
            # Modo: Prompt personalizado
            for i in range(image_count):
                final_prompt = f"{custom_prompt}, {style_prompt}"
                prompts_to_generate.append(final_prompt)
        else:
            # Modo: Baseado em roteiro
            if use_ai_agent and ai_agent_prompt:
                # Usar IA Agent para criar prompts específicos
                scene_prompts = generate_scene_prompts_with_ai(script, ai_agent_prompt, api_key, provider, image_count, use_custom_image_prompt, custom_image_prompt, selected_agent)
                if not scene_prompts:
                    error_response = format_error_response('internal_error', 'Não foi possível gerar prompts automaticamente com IA', 'IA Agent para Imagens')
                    return jsonify(error_response), 500
                
                for scene_prompt in scene_prompts:
                    final_prompt = f"{scene_prompt}, {style_prompt}"
                    prompts_to_generate.append(final_prompt)
            else:
                # Dividir roteiro em cenas usando a estratégia selecionada
                if split_strategy == 'intelligent':
                    scenes = split_script_intelligently(script, target_scenes or image_count)
                else:
                    # Modo tradicional
                    scenes = [scene.strip() for scene in script.split('\n\n') if scene.strip()]
                
                if not scenes:
                    error_response = format_error_response('content_too_long', 'Não foi possível dividir o roteiro em cenas', 'Análise de Roteiro')
                    return jsonify(error_response), 400
                
                # Distribuir cenas uniformemente ao longo do roteiro completo
                scenes_to_use = distribute_scenes_evenly(scenes, image_count, enable_variations, variation_intensity)
                
                for scene_text in scenes_to_use:
                    final_prompt = f"{scene_text}, {style_prompt}"
                    prompts_to_generate.append(final_prompt)

        # Gerar imagens para cada prompt
        for i, prompt in enumerate(prompts_to_generate):
            try:
                # Gerar imagem baseado no provedor
                if provider == 'gemini':
                    image_bytes = generate_image_gemini(prompt, api_key, width, height, quality)
                elif provider == 'gemini-imagen3':
                    # Extrair cookies do provedor da requisição (se houver)
                    google_cookies = data.get('google_cookies', '')
                    image_bytes = generate_image_gemini_imagen3(prompt, api_key, width, height, quality, google_cookies)
                elif provider == 'gemini-imagen3-rohitaryal':
                    # Extrair cookies do provedor da requisição (se houver)
                    google_cookies = data.get('google_cookies', '')
                    image_bytes = generate_image_gemini_imagen3_rohitaryal(prompt, width, height, quality, google_cookies)
                elif provider == 'gemini-reddit':
                    image_bytes = generate_image_gemini_reddit(prompt, width, height, quality)
                elif provider == 'pollinations':
                    image_bytes = generate_image_pollinations(prompt, width, height, quality, pollinations_model)
                else:  # together
                    image_bytes = generate_image_together(prompt, api_key, width, height, quality, model)
                
                if image_bytes is None:
                    print(f"Erro ao gerar imagem {i+1}: {prompt[:50]}...")
                    continue

                # Salvar a imagem
                timestamp = int(time.time() * 1000)
                filename = f"image_{timestamp}_{i+1}.png"
                filepath = os.path.join(OUTPUT_DIR, filename)

                with open(filepath, 'wb') as f:
                    f.write(image_bytes)

                # URL para acessar a imagem
                image_url = f"/api/images/view/{filename}"
                generated_images.append({
                    'prompt': prompt,
                    'url': image_url,
                    'provider': provider
                })
                
                # Delay entre gerações para respeitar limites de taxa
                if i < len(prompts_to_generate) - 1:  # Não aguardar após a última imagem
                    if provider == 'pollinations':
                        time.sleep(5)  # 5 segundos para Pollinations
                    else:
                        time.sleep(2)  # 2 segundos para outras APIs
                        
            except Exception as e:
                print(f"Erro ao processar imagem {i+1}: {str(e)}")
                generated_images.append({
                    'prompt': prompt,
                    'url': None,
                    'provider': provider,
                    'error': str(e)
                })
                continue

        if not generated_images:
            error_response = format_error_response('internal_error', 'Todas as tentativas de geração de imagem falharam', 'Geração de Imagens')
            return jsonify(error_response), 500

        return jsonify({
            'success': True,
            'message': f'{len([img for img in generated_images if img.get("url")])} imagens geradas com sucesso!',
            'images': generated_images,
            'total_requested': len(prompts_to_generate),
            'total_generated': len([img for img in generated_images if img.get("url")]),
            'split_strategy': split_strategy,
            'enable_variations': enable_variations,
            'variation_intensity': variation_intensity
        })

    except Exception as e:
        error_response = auto_format_error(str(e), 'Geração de Imagens')
        return jsonify(error_response), 500

@images_bp.route('/generate', methods=['POST'])
def generate_images_route():
    """
    Gera imagens a partir de um roteiro usando uma API de IA com suporte a IA Agent e processamento em fila.
    
    Provedores suportados:
    - pollinations: Gratuito, não requer API key
    - gemini-reddit: Gratuito, não requer API key
    - gemini: Requer API key do Google Gemini
    - together: Requer API key do Together AI
    - gemini-imagen3: Usa ImageFX do Google, opcionalmente com cookies para melhor acesso
    - gemini-imagen3-rohitaryal: Usa ImageFX do Google via API não oficial (REQUER cookies de autenticação)
    
    Parâmetros obrigatórios:
    - script: Roteiro para gerar imagens (ou custom_prompt se use_custom_prompt=True)
    
    Parâmetros opcionais:
    - api_key: Chave da API (não obrigatório para pollinations, gemini-reddit, gemini-imagen3 e gemini-imagen3-rohitaryal)
    - provider: Provedor de IA (padrão: 'pollinations')
    - model: Modelo a ser usado (padrão: 'gpt')
    - style: Estilo da imagem (padrão: 'cinematic, high detail, 4k')
    - format: Formato da imagem (padrão: '1024x1024')
    - quality: Qualidade da imagem (padrão: 'standard')
    - pollinations_model: Modelo do Pollinations (padrão: 'gpt')
    - use_ai_agent: Usar IA Agent para criar prompts (padrão: False)
    - ai_agent_prompt: Prompt para o IA Agent
    - use_custom_prompt: Usar prompt personalizado (padrão: False)
    - custom_prompt: Prompt personalizado
    - use_custom_image_prompt: Usar prompt de imagem personalizado (padrão: False)
    - custom_image_prompt: Prompt de imagem personalizado
    - image_count: Número de imagens a gerar (padrão: 1)
    - selected_agent: Agente selecionado
    - split_strategy: Estratégia de divisão do roteiro (padrão: 'intelligent')
    - enable_variations: Habilitar variações (padrão: False)
    - variation_intensity: Intensidade das variações (padrão: 1.0)
    - target_scenes: Número alvo de cenas
    - google_cookies: Cookies de autenticação do Google (OBRIGATÓRIO para provider gemini-imagen3-rohitaryal)
    
    Importante:
    - Para usar o provider gemini-imagen3-rohitaryal, é essencial fornecer cookies válidos de uma sessão
      autenticada do Google através do parâmetro google_cookies. Sem cookies, a geração falhará.
    - Os cookies podem ser obtidos fazendo login no Google ImageFX e copiando os cookies do navegador.
    """
    try:
        data = request.get_json()
        
        # Parâmetros básicos
        script = data.get('script', '').strip()
        api_key = data.get('api_key', '').strip()
        provider = data.get('provider', 'pollinations')  # pollinations, together, gemini
        model = data.get('model', 'gpt')
        style_prompt = data.get('style', 'cinematic, high detail, 4k')
        format_size = data.get('format', '1024x1024')
        quality = data.get('quality', 'standard')
        pollinations_model = data.get('pollinations_model', 'gpt')  # gpt ou flux
        
        # Novos parâmetros
        use_ai_agent = data.get('use_ai_agent', False)
        ai_agent_prompt = data.get('ai_agent_prompt', '')
        use_custom_prompt = data.get('use_custom_prompt', False)
        custom_prompt = data.get('custom_prompt', '').strip()
        use_custom_image_prompt = data.get('use_custom_image_prompt', False)
        custom_image_prompt = data.get('custom_image_prompt', '').strip()
        image_count = data.get('image_count', 1)
        selected_agent = data.get('selected_agent', None)
        
        # Validações
        if use_custom_prompt:
            if not custom_prompt:
                error_response = format_error_response('validation_error', 'Prompt personalizado é obrigatório quando selecionado', 'Geração de Imagens')
                return jsonify(error_response), 400
        else:
            if not script:
                error_response = format_error_response('validation_error', 'Roteiro é obrigatório para gerar imagens baseadas no conteúdo', 'Geração de Imagens')
                return jsonify(error_response), 400

        # Pollinations.ai e Gemini Reddit não requerem chave de API (são gratuitos)
        if not api_key and provider not in ['pollinations', 'gemini-reddit', 'gemini-imagen3', 'gemini-imagen3-rohitaryal']:
            error_response = format_error_response('api_key_missing', f'Chave da API ({provider}) é obrigatória', 'Geração de Imagens')
            return jsonify(error_response), 400

        # Processar formato da imagem
        try:
            width, height = map(int, format_size.split('x'))
        except ValueError:
            width, height = 1024, 1024

        generated_images = []
        prompts_to_generate = []

        # Determinar prompts baseado no modo selecionado
        if use_custom_prompt:
            # Modo: Prompt personalizado
            for i in range(image_count):
                final_prompt = f"{custom_prompt}, {style_prompt}"
                prompts_to_generate.append(final_prompt)
        else:
            # Modo: Baseado em roteiro
            if use_ai_agent and ai_agent_prompt:
                # Usar IA Agent para criar prompts específicos
                scene_prompts = generate_scene_prompts_with_ai(script, ai_agent_prompt, api_key, provider, image_count, use_custom_image_prompt, custom_image_prompt, selected_agent)
                if not scene_prompts:
                    error_response = format_error_response('internal_error', 'Não foi possível gerar prompts automaticamente com IA', 'IA Agent para Imagens')
                    return jsonify(error_response), 500
                
                for scene_prompt in scene_prompts:
                    final_prompt = f"{scene_prompt}, {style_prompt}"
                    prompts_to_generate.append(final_prompt)
            else:
                # Dividir roteiro em cenas usando divisão inteligente
                scenes = split_script_intelligently(script, image_count)
                
                if not scenes:
                    error_response = format_error_response('content_too_long', 'Não foi possível dividir o roteiro em cenas', 'Análise de Roteiro')
                    return jsonify(error_response), 400
                
                # Distribuir cenas uniformemente ao longo do roteiro completo
                scenes_to_use = distribute_scenes_evenly(scenes, image_count)
                
                for scene_text in scenes_to_use:
                    final_prompt = f"{scene_text}, {style_prompt}"
                    prompts_to_generate.append(final_prompt)

        # Gerar imagens para cada prompt
        for i, prompt in enumerate(prompts_to_generate):
            try:
                # Gerar imagem baseado no provedor
                if provider == 'gemini':
                    image_bytes = generate_image_gemini(prompt, api_key, width, height, quality)
                elif provider == 'gemini-imagen3':
                    # Extrair cookies do provedor da requisição (se houver)
                    google_cookies = data.get('google_cookies', '')
                    image_bytes = generate_image_gemini_imagen3(prompt, api_key, width, height, quality, google_cookies)
                elif provider == 'gemini-imagen3-rohitaryal':
                    # Extrair cookies do provedor da requisição (se houver)
                    google_cookies = data.get('google_cookies', '')
                    image_bytes = generate_image_gemini_imagen3_rohitaryal(prompt, width, height, quality, google_cookies)
                elif provider == 'gemini-reddit':
                    image_bytes = generate_image_gemini_reddit(prompt, width, height, quality)
                elif provider == 'pollinations':
                    image_bytes = generate_image_pollinations(prompt, width, height, quality, pollinations_model)
                else:  # together
                    image_bytes = generate_image_together(prompt, api_key, width, height, quality, model)
                
                if image_bytes is None:
                    print(f"Erro ao gerar imagem {i+1}: {prompt[:50]}...")
                    continue

                # Salvar a imagem
                timestamp = int(time.time() * 1000)
                filename = f"image_{timestamp}_{i+1}.png"
                filepath = os.path.join(OUTPUT_DIR, filename)

                with open(filepath, 'wb') as f:
                    f.write(image_bytes)

                # URL para acessar a imagem
                image_url = f"/api/images/view/{filename}"
                generated_images.append(image_url)
                
                # Delay entre gerações para respeitar limites de taxa
                if i < len(prompts_to_generate) - 1:  # Não aguardar após a última imagem
                    if provider == 'pollinations':
                        time.sleep(5)  # 5 segundos para Pollinations
                    else:
                        time.sleep(2)  # 2 segundos para outras APIs
                        
            except ValueError as e:
                # Tratar especificamente o erro de cookies ausentes
                print(f"🔍 ValueError capturado: {str(e)}")
                if "Cookies de autenticação do Google são obrigatórios para o provedor gemini-imagen3-rohitaryal" in str(e):
                    print("✅ Erro de cookies detectado, retornando resposta 400")
                    error_response = format_error_response('cookies_missing', 'Cookies de autenticação do Google são obrigatórios para o provedor gemini-imagen3-rohitaryal', 'Geração de Imagens')
                    return jsonify(error_response), 400
                else:
                    print(f"Erro ao processar imagem {i+1}: {str(e)}")
                    continue
            except Exception as e:
                print(f"Erro ao processar imagem {i+1}: {str(e)}")
                continue

        if not generated_images:
            error_response = format_error_response('internal_error', 'Todas as tentativas de geração de imagem falharam', 'Geração de Imagens')
            return jsonify(error_response), 500

        return jsonify({
            'success': True,
            'message': f'{len(generated_images)} imagens geradas com sucesso!',
            'image_urls': generated_images,
            'total_requested': len(prompts_to_generate),
            'total_generated': len(generated_images),
            'split_strategy': 'intelligent'
        })

    except Exception as e:
        error_response = auto_format_error(str(e), 'Geração de Imagens')
        return jsonify(error_response), 500

def split_script_intelligently(script, target_scenes=None):
    """
    Divide o roteiro de forma inteligente, identificando cenas significativas.
    
    Args:
        script (str): O roteiro completo
        target_scenes (int, optional): Número desejado de cenas. Se None, usa divisão automática.
    
    Returns:
        list: Lista de cenas divididas inteligentemente
    """
    # Dividir inicialmente por parágrafos duplos
    initial_scenes = [scene.strip() for scene in script.split('\n\n') if scene.strip()]
    
    if not initial_scenes:
        return []
    
    # Se não temos um alvo específico, retornar as cenas iniciais
    if target_scenes is None or len(initial_scenes) <= target_scenes:
        return initial_scenes
    
    # Se precisamos de mais cenas que as iniciais, tentar dividir parágrafos longos
    if len(initial_scenes) < target_scenes:
        enhanced_scenes = []
        
        for scene in initial_scenes:
            # Se o parágrafo é longo (mais de 3 frases), tentar dividir
            sentences = [s.strip() for s in scene.split('.') if s.strip()]
            
            if len(sentences) > 3:
                # Dividir em duas partes: primeira metade e segunda metade das frases
                mid_point = len(sentences) // 2
                first_part = '. '.join(sentences[:mid_point]) + '.'
                second_part = '. '.join(sentences[mid_point:]) + '.'
                
                enhanced_scenes.append(first_part)
                enhanced_scenes.append(second_part)
            else:
                enhanced_scenes.append(scene)
        
        # Se ainda não temos cenas suficientes, dividir por frases
        if len(enhanced_scenes) < target_scenes:
            final_scenes = []
            for scene in enhanced_scenes:
                if len(final_scenes) >= target_scenes:
                    break
                    
                # Dividir por frases se ainda precisamos de mais cenas
                sentences = [s.strip() for s in scene.split('.') if s.strip()]
                if len(sentences) > 1 and len(final_scenes) + len(sentences) <= target_scenes:
                    for sentence in sentences:
                        final_scenes.append(sentence + '.')
                else:
                    final_scenes.append(scene)
            
            return final_scenes[:target_scenes]
        
        return enhanced_scenes[:target_scenes]
    
    # Se temos mais cenas que o alvo, selecionar as mais importantes
    # Algoritmo simples: selecionar cenas uniformemente distribuídas
    step = len(initial_scenes) / target_scenes
    selected_scenes = []
    
    for i in range(target_scenes):
        scene_index = int(i * step)
        scene_index = min(scene_index, len(initial_scenes) - 1)
        selected_scenes.append(initial_scenes[scene_index])
    
    return selected_scenes

def distribute_scenes_evenly(scenes, image_count, enable_variations=False, intensity=1.0):
    """
    Distribui cenas uniformemente ao longo do roteiro completo.
    Evita repetições desnecessárias e garante distribuição inteligente.
    
    Args:
        scenes (list): Lista de cenas disponíveis
        image_count (int): Número de imagens desejadas
        enable_variations (bool): Se deve habilitar variações nas cenas
        intensity (float): Intensidade das variações (0.0 a 1.0)
    
    Returns:
        list: Lista de cenas selecionadas para geração de imagens
    """
    total_scenes = len(scenes)
    
    if image_count <= 0:
        return []
    
    if image_count <= total_scenes:
        # Se queremos menos ou igual imagens que cenas, selecionar uniformemente
        selected_scenes = []
        step = total_scenes / image_count
        
        for i in range(image_count):
            scene_index = int(i * step)
            # Garantir que não exceda o índice
            scene_index = min(scene_index, total_scenes - 1)
            selected_scenes.append(scenes[scene_index])
        
        return selected_scenes
    else:
        # Se queremos mais imagens que cenas, usar estratégia inteligente
        selected_scenes = []
        
        # Primeiro, incluir todas as cenas originais
        for scene in scenes:
            selected_scenes.append(scene)
        
        # Calcular quantas imagens extras precisamos
        remaining_images = image_count - total_scenes
        
        # Distribuir as imagens extras uniformemente entre as cenas
        if remaining_images > 0 and enable_variations:
            # Lista de variações para tornar cada prompt único
            variations = [
                "different angle and perspective",
                "close-up shot", 
                "wide angle view",
                "dramatic lighting",
                "soft lighting",
                "from above perspective",
                "from below perspective",
                "side view",
                "detailed focus",
                "atmospheric mood",
                "golden hour lighting",
                "blue hour ambiance",
                "high contrast",
                "soft focus background",
                "dynamic composition"
            ]
            
            # Ajustar a intensidade das variações
            if intensity < 1.0:
                # Usar apenas uma parte das variações com base na intensidade
                variations_count = max(1, int(len(variations) * intensity))
                variations = variations[:variations_count]
            
            for i in range(remaining_images):
                scene_index = i % total_scenes
                variation_index = i % len(variations)
                
                # Adicionar variação ao prompt para evitar imagens idênticas
                original_scene = scenes[scene_index]
                variation = variations[variation_index]
                varied_scene = f"{original_scene}, {variation}"
                selected_scenes.append(varied_scene)
        elif remaining_images > 0:
            # Se variações não estão habilitadas, apenas repetir as cenas
            for i in range(remaining_images):
                scene_index = i % total_scenes
                selected_scenes.append(scenes[scene_index])
        
        return selected_scenes

def generate_scene_prompts_with_ai(script, ai_agent_prompt, api_key, provider, image_count, use_custom_image_prompt=False, custom_image_prompt=None, selected_agent=None):
    """
    Usa IA para gerar prompts específicos de imagem baseados no roteiro.
    """
    try:
        # Carregar prompt personalizado se solicitado
        if use_custom_image_prompt and custom_image_prompt:
            base_prompt = custom_image_prompt
        elif use_custom_image_prompt:
            # Carregar prompt personalizado do arquivo de configuração
            try:
                prompts_config = load_prompts_config()
                image_config = prompts_config.get('image_prompts', {})
                
                # Verificar se há um prompt específico para o agente selecionado
                if selected_agent and 'agent_specific_prompts' in image_config and selected_agent in image_config['agent_specific_prompts']:
                    base_prompt = image_config['agent_specific_prompts'][selected_agent]
                    print(f"Usando prompt específico do agente {selected_agent}: {base_prompt[:100]}...")
                else:
                    # Usar prompt padrão
                    base_prompt = image_config.get('default_prompt', ai_agent_prompt)
                    print(f"Usando prompt padrão de imagem: {base_prompt[:100]}...")
            except Exception as e:
                print(f"Erro ao carregar prompt personalizado de imagem: {e}")
                base_prompt = ai_agent_prompt
        else:
            base_prompt = ai_agent_prompt
        
        # Prompt para o IA Agent
        system_prompt = f"""
{base_prompt}

Roteiro:
{script}

Gere exatamente {image_count} prompts de imagem baseados neste roteiro. Cada prompt deve:
1. Descrever uma cena visual específica
2. Ser detalhado e cinematográfico
3. Incluir elementos visuais importantes
4. Ser adequado para geração de imagem por IA

Retorne apenas os prompts, um por linha, sem numeração ou formatação extra.
        """
        
        if provider == 'together' and api_key:
            # Usar Together.ai para gerar os prompts
            import requests
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo",
                "messages": [
                    {"role": "system", "content": "You are an expert in creating prompts for AI image generation."},
                    {"role": "user", "content": system_prompt}
                ],
                "max_tokens": 1000,
                "temperature": 0.7
            }
            
            response = requests.post("https://api.together.xyz/v1/chat/completions", headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                response_data = response.json()
                if 'choices' in response_data and len(response_data['choices']) > 0:
                    content = response_data['choices'][0]['message']['content']
                    # Dividir em linhas e limpar
                    prompts = [line.strip() for line in content.split('\n') if line.strip()]
                    return prompts[:image_count]  # Garantir que não exceda o número solicitado
        
        # Fallback: dividir roteiro em partes e distribuir uniformemente
        scenes = split_script_intelligently(script, image_count)
        if scenes:
            return distribute_scenes_evenly(scenes, image_count)
        else:
            return [script] * min(image_count, 1)
        
    except Exception as e:
        print(f"Erro ao gerar prompts com IA Agent: {str(e)}")
        # Fallback: dividir roteiro em partes e distribuir uniformemente
        scenes = split_script_intelligently(script, image_count)
        if scenes:
            return distribute_scenes_evenly(scenes, image_count)
        else:
            return [script] * min(image_count, 1)

@images_bp.route('/view/<filename>')
def serve_image(filename):
    """
    Serve uma imagem gerada a partir do diretório de output.
    """
    try:
        from flask import send_from_directory
        return send_from_directory(OUTPUT_DIR, filename)
    except Exception as e:
        error_response = auto_format_error(str(e), 'Visualização de Imagem')
        return jsonify(error_response), 404

@images_bp.route('/download/<filename>')
def download_image(filename):
    """
    Faz o download de uma imagem gerada a partir do diretório de output.
    """
    try:
        from flask import send_from_directory
        return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)
    except Exception as e:
        error_response = auto_format_error(str(e), 'Download de Imagem')
        return jsonify(error_response), 404

@images_bp.route('/download/text/<filename>')
def download_text_file(filename):
    """
    Faz o download de um arquivo de texto gerado a partir do diretório de output.
    """
    try:
        from flask import send_from_directory
        text_dir = os.path.join(os.path.dirname(__file__), '..', 'output', 'text')
        return send_from_directory(text_dir, filename, as_attachment=True)
    except Exception as e:
        error_response = auto_format_error(str(e), 'Download de Texto')
        return jsonify(error_response), 404

@images_bp.route('/list-pipelines', methods=['GET'])
def list_pipelines_content():
    """
    Lista todos os pipelines com seus conteúdos gerados organizados por tipo
    """
    try:
        import glob
        from datetime import datetime
        from app import Pipeline
        
        # Diretórios de conteúdo
        base_dir = os.path.join(os.path.dirname(__file__), '..')
        images_dir = os.path.join(base_dir, 'output', 'images')
        audio_dir = os.path.join(base_dir, 'output', 'audio')
        videos_dir = os.path.join(base_dir, 'output', 'videos')
        outputs_dir = os.path.join(base_dir, 'outputs')
        temp_dir = os.path.join(base_dir, 'temp')
        
        # Obter todas as pipelines
        pipelines = Pipeline.query.order_by(Pipeline.started_at.desc()).all()
        
        # Listar todos os arquivos para associar às pipelines
        all_files = {
            'images': [],
            'audios': [],
            'videos': []
        }
        
        # Listar imagens
        if os.path.exists(images_dir):
            for ext in ['*.png', '*.jpg', '*.jpeg', '*.gif', '*.webp']:
                for filepath in glob.glob(os.path.join(images_dir, ext)):
                    filename = os.path.basename(filepath)
                    file_stats = os.stat(filepath)
                    all_files['images'].append({
                        'filename': filename,
                        'path': filepath,
                        'url': f'/api/images/view/{filename}',
                        'size': file_stats.st_size,
                        'created_at': datetime.datetime.fromtimestamp(file_stats.st_ctime).isoformat(),
                'modified_at': datetime.datetime.fromtimestamp(file_stats.st_mtime).isoformat()
                    })
        
        # Listar áudios (verificar múltiplos diretórios)
        audio_dirs = [audio_dir, temp_dir]
        audio_files_seen = set()  # Para evitar duplicatas
        
        for audio_search_dir in audio_dirs:
            if os.path.exists(audio_search_dir):
                for ext in ['*.wav', '*.mp3', '*.m4a', '*.ogg', '*.flac']:
                    for filepath in glob.glob(os.path.join(audio_search_dir, ext)):
                        filename = os.path.basename(filepath)
                        
                        # Evitar duplicatas baseadas no nome do arquivo
                        if filename not in audio_files_seen:
                            audio_files_seen.add(filename)
                            file_stats = os.stat(filepath)
                            all_files['audios'].append({
                                'filename': filename,
                                'path': filepath,
                                'directory': os.path.basename(audio_search_dir),
                                'size': file_stats.st_size,
                                'created_at': datetime.datetime.fromtimestamp(file_stats.st_ctime).isoformat(),
                'modified_at': datetime.datetime.fromtimestamp(file_stats.st_mtime).isoformat(),
                                'url': f'/api/automations/audio/{filename}'
                            })
        
        # Listar vídeos (verificar múltiplos diretórios)
        video_dirs = [videos_dir, outputs_dir]
        for video_search_dir in video_dirs:
            if os.path.exists(video_search_dir):
                for ext in ['*.mp4', '*.avi', '*.mov', '*.mkv', '*.webm']:
                    for filepath in glob.glob(os.path.join(video_search_dir, ext)):
                        filename = os.path.basename(filepath)
                        file_stats = os.stat(filepath)
                        all_files['videos'].append({
                            'filename': filename,
                            'path': filepath,
                            'directory': os.path.basename(video_search_dir),
                            'size': file_stats.st_size,
                            'created_at': datetime.datetime.fromtimestamp(file_stats.st_ctime).isoformat(),
                'modified_at': datetime.datetime.fromtimestamp(file_stats.st_mtime).isoformat(),
                            'url': f'/api/automations/video/{filename}'
                        })
        
        # Organizar pipelines com seus conteúdos
        pipelines_content = []
        
        for pipeline in pipelines:
            pipeline_dict = pipeline.to_dict()
            pipeline_id = pipeline_dict['pipeline_id']
            display_name = pipeline_dict['display_name']
            
            # Formatar o nome da pipeline como solicitado: "Pipeline #2025-09-13-015"
            pipeline_name = f"Pipeline #{display_name}"
            
            # Inicializar conteúdo da pipeline
            pipeline_content = {
                'id': pipeline_id,
                'name': pipeline_name,
                'display_name': display_name,
                'status': pipeline_dict['status'],
                'created_at': pipeline_dict['started_at'],
                'content': {
                    'text': [],
                    'audio': [],
                    'image': [],
                    'video': []
                }
            }
            
            # Adicionar conteúdo de texto (script)
            if pipeline_dict.get('script_content'):
                pipeline_content['content']['text'].append({
                    'type': 'text',
                    'content': pipeline_dict['script_content'],
                    'created_at': pipeline_dict['started_at']
                })
            
            # Associar arquivos à pipeline baseado no nome do arquivo
            # Verificar se o nome do arquivo contém o ID da pipeline ou o display_name
            for image in all_files['images']:
                if pipeline_id in image['filename'] or display_name in image['filename']:
                    image_copy = image.copy()
                    image_copy['type'] = 'image'
                    pipeline_content['content']['image'].append(image_copy)
            
            for audio in all_files['audios']:
                if pipeline_id in audio['filename'] or display_name in audio['filename']:
                    audio_copy = audio.copy()
                    audio_copy['type'] = 'audio'
                    pipeline_content['content']['audio'].append(audio_copy)
            
            for video in all_files['videos']:
                if pipeline_id in video['filename'] or display_name in video['filename']:
                    video_copy = video.copy()
                    video_copy['type'] = 'video'
                    pipeline_content['content']['video'].append(video_copy)
            
            # Adicionar arquivos específicos da pipeline se existirem nos campos do modelo
            if pipeline_dict.get('audio_file_path'):
                audio_filename = os.path.basename(pipeline_dict['audio_file_path'])
                pipeline_content['content']['audio'].append({
                    'filename': audio_filename,
                    'path': pipeline_dict['audio_file_path'],
                    'url': f'/api/automations/audio/{audio_filename}',
                    'type': 'audio',
                    'created_at': pipeline_dict['started_at']
                })
            
            if pipeline_dict.get('video_file_path'):
                video_filename = os.path.basename(pipeline_dict['video_file_path'])
                pipeline_content['content']['video'].append({
                    'filename': video_filename,
                    'path': pipeline_dict['video_file_path'],
                    'url': f'/api/automations/video/{video_filename}',
                    'type': 'video',
                    'created_at': pipeline_dict['started_at']
                })
            
            pipelines_content.append(pipeline_content)
        
        # Calcular totais
        total_pipelines = len(pipelines_content)
        total_files = sum(
            len(p['content']['text']) + 
            len(p['content']['audio']) + 
            len(p['content']['image']) + 
            len(p['content']['video']) 
            for p in pipelines_content
        )
        
        # Calcular totais por tipo de mídia
        total_text = sum(len(p['content']['text']) for p in pipelines_content)
        total_audio = sum(len(p['content']['audio']) for p in pipelines_content)
        total_image = sum(len(p['content']['image']) for p in pipelines_content)
        total_video = sum(len(p['content']['video']) for p in pipelines_content)
        
        return jsonify({
            'success': True,
            'pipelines': pipelines_content,
            'summary': {
                'total_pipelines': total_pipelines,
                'total_files': total_files,
                'total_text': total_text,
                'total_audio': total_audio,
                'total_image': total_image,
                'total_video': total_video
            }
        })
        
    except Exception as e:
        error_response = auto_format_error(str(e), 'Listagem de Pipelines')
        return jsonify(error_response), 500

@images_bp.route('/list-generated', methods=['GET'])
def list_generated_content():
    """
    Lista todos os conteúdos gerados (imagens, áudios, vídeos)
    """
    try:
        import glob
        from datetime import datetime
        
        # Diretórios de conteúdo
        base_dir = os.path.join(os.path.dirname(__file__), '..')
        images_dir = os.path.join(base_dir, 'output', 'images')
        audio_dir = os.path.join(base_dir, 'output', 'audio')
        videos_dir = os.path.join(base_dir, 'output', 'videos')
        outputs_dir = os.path.join(base_dir, 'outputs')
        temp_dir = os.path.join(base_dir, 'temp')
        
        content = {
            'images': [],
            'audios': [],
            'videos': [],
            'total_files': 0
        }
        
        # Listar imagens
        if os.path.exists(images_dir):
            for ext in ['*.png', '*.jpg', '*.jpeg', '*.gif', '*.webp']:
                for filepath in glob.glob(os.path.join(images_dir, ext)):
                    filename = os.path.basename(filepath)
                    file_stats = os.stat(filepath)
                    content['images'].append({
                        'filename': filename,
                        'path': filepath,
                        'url': f'/api/images/view/{filename}',
                        'size': file_stats.st_size,
                        'created_at': datetime.datetime.fromtimestamp(file_stats.st_ctime).isoformat(),
                'modified_at': datetime.datetime.fromtimestamp(file_stats.st_mtime).isoformat()
                    })
        
        # Listar áudios (verificar múltiplos diretórios)
        audio_dirs = [audio_dir, temp_dir]
        audio_files_seen = set()  # Para evitar duplicatas
        
        for audio_search_dir in audio_dirs:
            if os.path.exists(audio_search_dir):
                for ext in ['*.wav', '*.mp3', '*.m4a', '*.ogg', '*.flac']:
                    for filepath in glob.glob(os.path.join(audio_search_dir, ext)):
                        filename = os.path.basename(filepath)
                        
                        # Evitar duplicatas baseadas no nome do arquivo
                        if filename not in audio_files_seen:
                            audio_files_seen.add(filename)
                            file_stats = os.stat(filepath)
                            content['audios'].append({
                                'filename': filename,
                                'path': filepath,
                                'directory': os.path.basename(audio_search_dir),
                                'size': file_stats.st_size,
                                'created_at': datetime.datetime.fromtimestamp(file_stats.st_ctime).isoformat(),
                'modified_at': datetime.datetime.fromtimestamp(file_stats.st_mtime).isoformat()
                            })
        
        # Listar vídeos (verificar múltiplos diretórios)
        video_dirs = [videos_dir, outputs_dir]
        for video_search_dir in video_dirs:
            if os.path.exists(video_search_dir):
                for ext in ['*.mp4', '*.avi', '*.mov', '*.mkv', '*.webm']:
                    for filepath in glob.glob(os.path.join(video_search_dir, ext)):
                        filename = os.path.basename(filepath)
                        file_stats = os.stat(filepath)
                        content['videos'].append({
                            'filename': filename,
                            'path': filepath,
                            'directory': os.path.basename(video_search_dir),
                            'size': file_stats.st_size,
                            'created_at': datetime.datetime.fromtimestamp(file_stats.st_ctime).isoformat(),
                'modified_at': datetime.datetime.fromtimestamp(file_stats.st_mtime).isoformat()
                        })
        
        # Ordenar por data de criação (mais recentes primeiro)
        content['images'].sort(key=lambda x: x['created_at'], reverse=True)
        content['audios'].sort(key=lambda x: x['created_at'], reverse=True)
        content['videos'].sort(key=lambda x: x['created_at'], reverse=True)
        
        # Calcular total
        content['total_files'] = len(content['images']) + len(content['audios']) + len(content['videos'])
        
        return jsonify({
            'success': True,
            'content': content,
            'summary': {
                'total_images': len(content['images']),
                'total_audios': len(content['audios']),
                'total_videos': len(content['videos']),
                'total_files': content['total_files']
            }
        })
        
    except Exception as e:
        error_response = auto_format_error(str(e), 'Listagem de Conteúdos')
        return jsonify(error_response), 500

def generate_image_together(prompt, api_key, width, height, quality, model):
    """
    Gera imagem usando a API Together.ai
    """
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model,
            "prompt": prompt,
            "width": width,
            "height": height
        }

        response = requests.post("https://api.together.xyz/v1/images/generations", headers=headers, json=payload, timeout=120)

        if response.status_code != 200:
            return None

        # A API Together.ai retorna uma URL para a imagem
        response_data = response.json()
        
        if 'data' in response_data and len(response_data['data']) > 0:
            image_item = response_data['data'][0]
            if 'url' in image_item:
                # Baixar a imagem da URL fornecida
                img_response = requests.get(image_item['url'])
                if img_response.status_code == 200:
                    return img_response.content
        
        return None
    except Exception as e:
        print(f"Erro na API Together.ai: {str(e)}")
        return None

def generate_image_gemini(prompt, api_key, width, height, quality):
    """
    Generate image using Gemini 2.0 Flash Preview Image Generation with automatic retry system
    """
    from routes.automations import get_next_gemini_key, handle_gemini_429_error, get_gemini_keys_count
    
    # Usar a quantidade real de chaves disponíveis
    max_retries = get_gemini_keys_count() if get_gemini_keys_count() > 0 else 1
    print(f"🔑 Usando {max_retries} chaves Gemini para imagens")
    current_api_key = api_key
    
    for attempt in range(max_retries):
        try:
            import google.generativeai as genai
            from google.generativeai import types
            import base64
            from io import BytesIO
            
            print(f"🎨 Tentativa {attempt + 1}/{max_retries} - Gerando imagem com Gemini")
            
            # Configurar Gemini
            genai.configure(api_key=current_api_key)
            model = genai.GenerativeModel('gemini-2.0-flash-preview-image-generation')
            
            # Prepare the prompt with size specifications
            enhanced_prompt = f"{prompt}. Generate a {width}x{height} image."
            if quality == "hd":
                enhanced_prompt += " High quality, detailed, professional."
            
            # Generate content with image output
            print(f"🔄 Enviando requisição para Gemini com prompt: {enhanced_prompt}")
            response = model.generate_content(enhanced_prompt)
            print(f"✅ Resposta recebida do Gemini")
            print(f"📊 Status da resposta: {response}")
            print(f"📊 Número de candidatos: {len(response.candidates)}")
            print(f"📊 Partes no primeiro candidato: {len(response.candidates[0].content.parts)}")
            
            # Extract image from response
            for i, part in enumerate(response.candidates[0].content.parts):
                print(f"🔍 Verificando parte {i+1}: {part}")
                if part.inline_data is not None:
                    print(f"✅ Dados de imagem encontrados na parte {i+1}")
                    # Get image data
                    image_data = part.inline_data.data
                    print(f"📊 Tamanho dos dados da imagem: {len(image_data)} bytes")
                    
                    # Convert to bytes if needed
                    if isinstance(image_data, str):
                        image_bytes = base64.b64decode(image_data)
                    else:
                        image_bytes = image_data
                    
                    print(f"✅ Sucesso! Imagem gerada com Gemini na tentativa {attempt + 1}")
                    return image_bytes
            
            raise Exception("No image data found in Gemini response")
            
        except Exception as e:
            error_str = str(e)
            print(f"❌ Erro na tentativa {attempt + 1}: {error_str}")
            
            # Check if it's a quota error (429)
            if "429" in error_str or "quota" in error_str.lower() or "rate limit" in error_str.lower():
                if attempt < max_retries - 1:  # Not the last attempt
                    print(f"🔄 Erro de quota detectado, tentando próxima chave Gemini...")
                    handle_gemini_429_error(error_str, current_api_key)
                    current_api_key = get_next_gemini_key()
                    if current_api_key:
                        print(f"🔑 Nova chave Gemini obtida para tentativa {attempt + 2}")
                        continue
                    else:
                        print("❌ Nenhuma chave Gemini disponível")
                        break
                else:
                    print("❌ Todas as tentativas de retry falharam")
                    handle_gemini_429_error(error_str, current_api_key)
            else:
                # For non-quota errors, don't retry
                print(f"❌ Erro não relacionado à quota, parando tentativas: {error_str}")
                break
    
    print("❌ Falha na geração de imagem com Gemini após todas as tentativas")
    return None

def generate_image_gemini_imagen3(prompt, api_key=None, width=1024, height=1024, quality="standard", cookies=None):
    """
    Gera imagem usando o Imagen 3 (ImageFX) do Google através da API do Gemini
    Utiliza o modo gratuito do Google Gemini
    
    Esta função tenta múltiplos métodos em ordem de prioridade:
    1. Método rohitaryal (imageFX-api) - REQUER cookies de autenticação do Google
    2. Método oficial com API key do Gemini
    3. Método não oficial (sem autenticação)
    4. API oficial do Gemini (generateContent)
    5. Método Reddit
    
    Args:
        prompt (str): Texto descritivo da imagem
        api_key (str, optional): Chave da API do Gemini
        width (int): Largura da imagem
        height (int): Altura da imagem
        quality (str): Qualidade da imagem ("standard" ou "hd")
        cookies (str, optional): Cookies de autenticação do Google (OBRIGATÓRIO para método rohitaryal)
    
    Returns:
        bytes: Imagem gerada em formato PNG ou None se falhar
    
    Note:
        Para usar o método rohitaryal (imageFX-api), é essencial fornecer cookies válidos
        de uma sessão autenticada do Google. Sem cookies, a função tentará outros métodos.
    """
    try:
        print(f"🎨 Gerando imagem com Imagen 3 (ImageFX) do Google")
        print(f"📝 Prompt: {prompt}")
        print(f"📏 Dimensões: {width}x{height}")
        print(f"🎯 Qualidade: {quality}")
        print(f"🍪 Cookies fornecidos: {'Sim' if cookies else 'Não'}")
        
        # PRIORIDADE 1: Usar o método rohitaryal (imageFX-api)
        print("🔒 Tentando método rohitaryal (imageFX-api)...")
        rohitaryal_result = generate_image_gemini_imagen3_rohitaryal(prompt, width, height, quality, cookies)
        
        if rohitaryal_result is not None:
            return rohitaryal_result
        
        # PRIORIDADE 2: Se tiver cookies, tentar novamente com o método rohitaryal (já tentado acima, mas mantido para clareza)
        if cookies:
            print("🔒 Usando método com cookies para autenticação...")
            return generate_image_gemini_imagen3_rohitaryal(prompt, width, height, quality, cookies)
        
        # PRIORIDADE 3: Se tiver API key, tentar método oficial
        if api_key:
            print("🔑 Tentando com chave de API do Gemini...")
            try:
                # Configurar o cliente Gemini
                genai.configure(api_key=api_key)
                
                # Selecionar o modelo Imagen 3
                model = genai.ImageGenerationModel("imagen-3.0-generate-001")
                
                # Configurar parâmetros de geração
                generation_config = {
                    "number_of_images": 1,
                    "aspect_ratio": f"{width}:{height}",
                    "safety_filter_level": "block_none",
                    "person_generation": "allow_adult"
                }
                
                # Ajustar configuração baseado na qualidade
                if quality == "hd":
                    generation_config["sample_count"] = 1
                    generation_config["quality"] = "hd"
                
                # Gerar a imagem
                response = model.generate_images(
                    prompt=prompt,
                    **generation_config
                )
                
                # Verificar se a imagem foi gerada com sucesso
                if response and response.generated_images and len(response.generated_images) > 0:
                    generated_image = response.generated_images[0]
                    
                    # Converter para bytes
                    image_bytes = generated_image.image_bytes
                    
                    print(f"✅ Imagem gerada com sucesso usando Imagen 3!")
                    print(f"📊 Tamanho: {len(image_bytes)} bytes")
                    
                    return image_bytes
                else:
                    print("❌ Nenhuma imagem foi gerada")
            except Exception as e:
                print(f"❌ Erro ao gerar imagem com API key do Gemini: {str(e)}")
        
        # PRIORIDADE 4: Tentar método não oficial
        print("🔑 Tentando método não oficial...")
        unofficial_result = generate_image_gemini_imagen3_unofficial(prompt, width, height, quality)
        
        if unofficial_result is not None:
            return unofficial_result
        
        # PRIORIDADE 5: Tentar com a API oficial do Gemini (generateContent)
        print("🔄 Tentando com API oficial do Gemini (generateContent)...")
        official_result = generate_image_gemini_official(prompt, width, height, quality)
        
        if official_result is not None:
            return official_result
        
        # PRIORIDADE 6: Tentar com o método Reddit
        print("🔄 Tentando com método Reddit...")
        return generate_image_gemini_reddit(prompt, width, height, quality)
            
    except Exception as e:
        print(f"❌ Erro crítico ao gerar imagem com Imagen 3: {str(e)}")
        
        # Tentar fallback para o método não oficial
        print("🔄 Tentando fallback para método não oficial...")
        unofficial_result = generate_image_gemini_imagen3_unofficial(prompt, width, height, quality)
        
        if unofficial_result is not None:
            return unofficial_result
        
        # Se o método não oficial também falhar, tentar com a API oficial do Gemini
        print("🔄 Método não oficial falhou, tentando com API oficial do Gemini...")
        official_result = generate_image_gemini_official(prompt, width, height, quality)
        
        if official_result is not None:
            return official_result
        
        # Se tudo falhar, tentar com o método Reddit
        print("🔄 API oficial do Gemini falhou, tentando com método Reddit...")
        return generate_image_gemini_reddit(prompt, width, height, quality)

def generate_image_gemini_imagen3_unofficial(prompt, width=1024, height=1024, quality="standard"):
    """
    Gera imagem usando o Imagen 3 (ImageFX) do Google através de método não oficial
    Não requer chave de API, utiliza endpoints públicos do Google
    
    Args:
        prompt (str): Texto descritivo da imagem
        width (int): Largura da imagem
        height (int): Altura da imagem
        quality (str): Qualidade da imagem ("standard" ou "hd")
    
    Returns:
        bytes: Imagem gerada em formato PNG ou None se falhar
    """
    try:
        print(f"🎨 Gerando imagem com Imagen 3 (ImageFX) - Método não oficial")
        print(f"📝 Prompt: {prompt}")
        print(f"📏 Dimensões: {width}x{height}")
        print(f"🎯 Qualidade: {quality}")
        
        # Headers para simular um navegador real
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'
        }
        
        # Configurar sessão
        session = requests.Session()
        session.headers.update(headers)
        
        # URL do ImageFX do Google
        base_url = "https://imagen.research.google"
        
        # Payload para a requisição
        payload = {
            "prompt": prompt,
            "aspectRatio": f"{width}:{height}",
            "outputFormat": "png",
            "quality": quality,
            "safetyFilterLevel": "block_none",
            "personGeneration": "allow_adult"
        }
        
        # Tentar gerar a imagem
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"🔄 Tentativa {attempt + 1}/{max_retries}")
                
                # Fazer a requisição para o endpoint do ImageFX
                response = session.post(
                    f"{base_url}/_/ImageFxGenerateService/generate",
                    json=payload,
                    timeout=60
                )
                
                if response.status_code == 200:
                    # Verificar se a resposta contém dados de imagem
                    content_type = response.headers.get('content-type', '').lower()
                    
                    if 'image' in content_type:
                        print(f"✅ Imagem gerada com sucesso!")
                        print(f"📊 Tamanho: {len(response.content)} bytes")
                        return response.content
                    else:
                        # Tentar extrair imagem da resposta JSON
                        try:
                            json_response = response.json()
                            if 'imageData' in json_response:
                                import base64
                                image_data = base64.b64decode(json_response['imageData'])
                                print(f"✅ Imagem extraída da resposta JSON!")
                                print(f"📊 Tamanho: {len(image_data)} bytes")
                                return image_data
                        except:
                            pass
                        
                        print(f"⚠️ Resposta não contém imagem válida")
                        print(f"🔍 Content-Type: {content_type}")
                        continue
                else:
                    print(f"❌ Erro HTTP {response.status_code}")
                    if response.status_code == 429:
                        print("⚠️ Limite de taxa excedido, aguardando...")
                        time.sleep(5)
                    continue
                    
            except requests.exceptions.Timeout:
                print(f"⏰ Timeout na tentativa {attempt + 1}")
                continue
            except Exception as e:
                print(f"❌ Erro na tentativa {attempt + 1}: {str(e)}")
                continue
        
        # Se todas as tentativas falharem, tentar fallback para o método Gemini Reddit
        print("🔄 Todas as tentativas falharam, tentando fallback para Gemini Reddit...")
        return generate_image_gemini_reddit(prompt, width, height, quality)
        
    except Exception as e:
        print(f"❌ Erro crítico ao gerar imagem com Imagen 3 não oficial: {str(e)}")
        return None
        

def generate_image_gemini_imagen3_rohitaryal(prompt, width=1024, height=1024, quality="standard", cookies=None):
    """
    Gera imagem usando a API imageFX-api do GitHub (rohitaryal/imageFX-api)
    Utiliza cookies para autenticação e acesso ao serviço
    
    Esta implementação segue o padrão do repositório imageFX-api, que inclui:
    - Autenticação via sessão do Google com cookies
    - Obtenção de token de acesso via endpoint /auth/session
    - Uso do endpoint https://aisandbox-pa.googleapis.com/v1:runImageFx
    - Formato de payload específico com userInput, clientContext, modelInput e aspectRatio
    
    Args:
        prompt (str): Texto descritivo da imagem
        width (int): Largura da imagem
        height (int): Altura da imagem
        quality (str): Qualidade da imagem ("standard" ou "hd")
        cookies (str, optional): Cookies de autenticação do Google (obrigatório)
    
    Returns:
        bytes: Imagem gerada em formato PNG ou None se falhar
    
    Raises:
        ValueError: Se cookies não forem fornecidos
        requests.exceptions.RequestException: Se houver erro na requisição
    """
    print(f"🎨 Gerando imagem com ImageFX API (rohitaryal)")
    print(f"📝 Prompt: {prompt}")
    print(f"📏 Dimensões: {width}x{height}")
    print(f"🎯 Qualidade: {quality}")
    print(f"🍪 Cookies fornecidos: {'Sim' if cookies else 'Não'}")
    
    # Verificar se temos cookies de autenticação (fora do try-catch principal)
    if not cookies or cookies.strip() == "":
        print("❌ Nenhum cookie fornecido")
        print(f"🍪 Valor dos cookies: '{cookies}'")
        raise ValueError("Cookies de autenticação do Google são obrigatórios para o provedor gemini-imagen3-rohitaryal")
    
    try:
        
        # Configurar headers baseados no repositório imageFX-api
        headers = {
            'Origin': 'https://labs.google',
            'content-type': 'application/json',
            'Referer': 'https://labs.google/fx/tools/image-fx',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }
        
        # Configurar sessão
        session = requests.Session()
        session.headers.update(headers)
        
        # Processar cookies
        if isinstance(cookies, str):
            # Separar cookies por ; e processar cada um
            cookie_pairs = cookies.split(';')
            for cookie in cookie_pairs:
                if '=' in cookie:
                    key, value = cookie.strip().split('=', 1)
                    session.cookies.set(key, value)
                    print(f"🍪 Cookie adicionado: {key}")
        elif isinstance(cookies, dict):
            for key, value in cookies.items():
                session.cookies.set(key, value)
                print(f"🍪 Cookie adicionado: {key}")
        
        # Obter token de autenticação
        print("🔑 Obtendo token de autenticação...")
        auth_response = session.get("https://labs.google/fx/api/auth/session")
        
        if auth_response.status_code != 200:
            print(f"❌ Falha na autenticação: {auth_response.status_code}")
            print(f"📤 Resposta: {auth_response.text[:500]}...")
            return None
        
        auth_data = auth_response.json()
        if not auth_data.get('access_token'):
            print("❌ Token de acesso não encontrado na resposta")
            return None
        
        access_token = auth_data['access_token']
        print("✅ Token de autenticação obtido com sucesso")
        
        # Atualizar headers com o token de acesso
        session.headers.update({
            'Authorization': f'Bearer {access_token}'
        })
        
        # Determinar o modelo com base na qualidade
        if quality == "hd":
            model = "IMAGEN_3_5"  # Modelo mais avançado para alta qualidade
        else:
            model = "IMAGEN_3"    # Modelo padrão
        
        # Determinar a proporção de aspecto
        if width == height:
            aspect_ratio = "IMAGE_ASPECT_RATIO_SQUARE"
        elif width > height:
            aspect_ratio = "IMAGE_ASPECT_RATIO_LANDSCAPE"
        else:
            aspect_ratio = "IMAGE_ASPECT_RATIO_PORTRAIT"
        
        # Preparar payload no formato correto baseado no repositório imageFX-api
        payload = {
            "userInput": {
                "candidatesCount": 1,
                "prompts": [prompt],
                "seed": 0
            },
            "clientContext": {
                "sessionId": ";1757113025397",
                "tool": "IMAGE_FX"
            },
            "modelInput": {
                "modelNameType": model
            },
            "aspectRatio": aspect_ratio
        }
        
        print(f"📤 Enviando requisição para: https://aisandbox-pa.googleapis.com/v1:runImageFx")
        print(f"📋 Payload: {json.dumps(payload, indent=2)}")
        
        # Tentar gerar a imagem
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"🔄 Tentativa {attempt + 1}/{max_retries}")
                
                # Fazer a requisição para o endpoint correto do ImageFX
                response = session.post(
                    "https://aisandbox-pa.googleapis.com/v1:runImageFx",
                    json=payload,
                    timeout=90  # Timeout mais longo para lidar com processamento
                )
                
                print(f"📊 Status da resposta: {response.status_code}")
                
                # Tratar diferentes tipos de respostas
                if response.status_code == 200:
                    try:
                        json_response = response.json()
                        print(f"📋 Resposta JSON recebida")
                        
                        # Extrair imagem da resposta JSON
                        generated_images = json_response.get('imagePanels', [])
                        if generated_images and len(generated_images) > 0:
                            panel = generated_images[0]
                            images = panel.get('generatedImages', [])
                            if images and len(images) > 0:
                                image_data = images[0]
                                encoded_image = image_data.get('encodedImage')
                                
                                if encoded_image:
                                    import base64
                                    image_bytes = base64.b64decode(encoded_image)
                                    print(f"✅ Imagem gerada com sucesso usando ImageFX API!")
                                    print(f"📊 Tamanho: {len(image_bytes)} bytes")
                                    return image_bytes
                        
                        print("❌ Nenhuma imagem encontrada na resposta")
                        print(f"📋 Estrutura da resposta: {json.dumps(json_response, indent=2)[:500]}...")
                        
                    except Exception as json_err:
                        print(f"❌ Erro ao processar JSON: {str(json_err)}")
                        print(f"📤 Resposta bruta: {response.text[:500]}...")
                        continue
                        
                else:
                    print(f"❌ Erro HTTP {response.status_code}")
                    print(f"📤 Mensagem: {response.text[:500]}...")
                    
                    # Tratamento especial para erros comuns
                    if response.status_code == 403:
                        print("🚫 Acesso negado - verifique os cookies de autenticação")
                    elif response.status_code == 429:
                        print("⚠️ Limite de taxa excedido, aguardando...")
                        time.sleep(10)  # Pausa mais longa para este tipo de erro
                    elif response.status_code == 500:
                        print("⚠️ Erro interno do servidor, tentando novamente...")
                    
                    continue
                    
            except requests.exceptions.Timeout:
                print(f"⏰ Timeout na tentativa {attempt + 1}")
                time.sleep(3)
                continue
            except requests.exceptions.ConnectionError:
                print(f"🔌 Erro de conexão na tentativa {attempt + 1}")
                time.sleep(3)
                continue
            except Exception as e:
                print(f"❌ Erro na tentativa {attempt + 1}: {str(e)}")
                continue
        
        # Se todas as tentativas falharem, tentar fallback para o método Gemini não oficial
        print("🔄 Todas as tentativas falharam, tentando fallback para Imagen 3 não oficial...")
        return generate_image_gemini_imagen3_unofficial(prompt, width, height, quality)
        
    except ValueError as e:
        # Não fazer fallback para erros de validação (como cookies ausentes)
        print(f"❌ Erro de validação: {str(e)}")
        raise e
    except Exception as e:
        print(f"❌ Erro crítico ao gerar imagem com ImageFX API (rohitaryal): {str(e)}")
        # Tentar fallback em caso de erro crítico
        try:
            return generate_image_gemini_imagen3_unofficial(prompt, width, height, quality)
        except:
            return None

def generate_image_gemini_official(prompt, width, height, quality='standard'):
    """
    Gera imagem usando a API oficial do Google Gemini com o modelo gemini-1.5-flash
    Esta é uma alternativa funcional ao Imagen 3 que utiliza a API oficial do Google
    
    Args:
        prompt (str): Texto descritivo da imagem
        width (int): Largura da imagem
        height (int): Altura da imagem
        quality (str): Qualidade da imagem ("standard" ou "hd")
    
    Returns:
        bytes: Imagem gerada em formato PNG ou None se falhar
    """
    try:
        import json
        import base64
        import os
        from pathlib import Path
        
        print(f"🎨 Iniciando geração com API oficial do Gemini")
        print(f"📝 Prompt: {prompt[:50]}...")
        print(f"📏 Dimensões: {width}x{height}")
        
        # Melhorar o prompt com instruções de tamanho e qualidade
        enhanced_prompt = f"{prompt}. Generate a {width}x{height} image."
        if quality == "hd":
            enhanced_prompt += " High quality, detailed, professional, 4K resolution."
        
        # Preparar o payload para a requisição
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {
                            "text": enhanced_prompt
                        }
                    ]
                }
            ],
            "generationConfig": {
                "responseModalities": [
                    "Text",
                    "Image"
                ],
                "temperature": 1.0,
                "topK": 32,
                "topP": 1.0
            },
            "safetySettings": [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_NONE"
                }
            ]
        }
        
        # Headers para a requisição
        headers = {
            "Content-Type": "application/json"
        }
        
        # Tentar carregar uma API key de Gemini
        config_path = Path(__file__).parent.parent / "config" / "api_keys.json"
        
        if not config_path.exists():
            print("❌ Arquivo de configuração de API keys não encontrado")
            return None
        
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Verificar se há alguma chave de Gemini disponível
        gemini_keys = [key for key in config.keys() if key.startswith('gemini_') and config[key]]
        
        if not gemini_keys:
            print("❌ Nenhuma API key de Gemini encontrada no arquivo de configuração")
            return None
        
        # Tentar com cada chave disponível até encontrar uma que funcione
        for key_name in gemini_keys:
            try:
                api_key = config[key_name]
                print(f"🔑 Tentando com API key: {key_name}")
                
                # URL do endpoint do Gemini 1.5 Flash
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                
                # Fazer a requisição
                response = requests.post(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=60
                )
                
                print(f"📊 Status da resposta: {response.status_code}")
                
                if response.status_code == 200:
                    # Processar a resposta
                    response_data = response.json()
                    
                    # Verificar se há candidatos na resposta
                    if "candidates" not in response_data or not response_data["candidates"]:
                        print("❌ Nenhum candidato encontrado na resposta")
                        continue
                    
                    # Extrair a imagem da resposta
                    for candidate in response_data["candidates"]:
                        if "content" in candidate and "parts" in candidate["content"]:
                            for part in candidate["content"]["parts"]:
                                if "inlineData" in part and "data" in part["inlineData"]:
                                    # Obter os dados da imagem em base64
                                    image_data_base64 = part["inlineData"]["data"]
                                    
                                    # Decodificar de base64 para bytes
                                    image_bytes = base64.b64decode(image_data_base64)
                                    
                                    print(f"✅ Sucesso! Imagem gerada com API oficial do Gemini")
                                    print(f"📊 Tamanho dos dados da imagem: {len(image_bytes)} bytes")
                                    
                                    return image_bytes
                    
                    print("❌ Nenhum dado de imagem encontrado na resposta")
                elif response.status_code == 429:
                    print("⚠️ Limite de taxa excedido, tentando próxima chave...")
                    continue
                elif response.status_code == 403:
                    print("⚠️ Chave de API inválida ou sem permissão, tentando próxima chave...")
                    continue
                else:
                    print(f"❌ Erro na resposta: {response.text}")
                    continue
                    
            except Exception as e:
                print(f"❌ Erro ao tentar com chave {key_name}: {str(e)}")
                continue
        
        print("❌ Todas as chaves de API falharam")
        return None
        
    except Exception as e:
        print(f"❌ Erro ao gerar imagem com API oficial do Gemini: {str(e)}")
        return None

def generate_image_gemini_reddit(prompt, width, height, quality='standard'):
    """
    Gera imagem usando o método do Reddit para acessar o Gemini 2.5 Flash sem chaves de API ou cookies
    Baseado no comando curl encontrado em: https://www.reddit.com/r/GeminiAI/comments/1n42e14/found_trick_to_access_gemini_only_25_flash/
    
    NOTA: Este método pode não funcionar mais devido a mudanças nas políticas do Google.
    Se falhar, tentará usar uma API key de Gemini se disponível.
    """
    try:
        import json
        import base64
        import re
        
        print(f"🎨 Iniciando geração com método Reddit do Gemini 2.5 Flash")
        print(f"📝 Prompt: {prompt[:50]}...")
        print(f"📏 Dimensões: {width}x{height}")
        
        # Melhorar o prompt com instruções de tamanho
        enhanced_prompt = f"{prompt}. Generate a {width}x{height} image."
        if quality == "hd":
            enhanced_prompt += " High quality, detailed, professional."
        
        # Preparar o payload para a requisição
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {
                            "text": enhanced_prompt
                        }
                    ]
                }
            ],
            "generationConfig": {
                "responseModalities": [
                    "Text",
                    "Image"
                ]
            },
            "safetySettings": [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_NONE"
                }
            ]
        }
        
        # Headers para a requisição
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        # URL do endpoint do Gemini 2.5 Flash
        # NOTA: O modelo gemini-2.5-flash-exp pode não estar mais disponível
        # Vamos tentar com gemini-1.5-flash que é o modelo atual para geração de imagens
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        
        print(f"🔄 Enviando requisição para Gemini 2.5 Flash via método Reddit")
        
        # Fazer a requisição
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=60
        )
        
        print(f"📊 Status da resposta: {response.status_code}")
        
        # Se o método Reddit falhar com erro 403, tentar com API key se disponível
        if response.status_code == 403:
            print("⚠️ Método Reddit sem autenticação falhou, tentando com API key se disponível...")
            
            # Tentar carregar uma API key de Gemini
            try:
                import os
                from pathlib import Path
                
                # Caminho para o arquivo de configuração
                config_path = Path(__file__).parent.parent / "config" / "api_keys.json"
                
                if config_path.exists():
                    with open(config_path, 'r') as f:
                        config = json.load(f)
                    
                    # Verificar se há alguma chave de Gemini disponível
                    gemini_keys = [key for key in config.keys() if key.startswith('gemini_') and config[key]]
                    
                    if gemini_keys:
                        # Usar a primeira chave disponível
                        api_key = config[gemini_keys[0]]
                        print(f"🔑 Usando API key de Gemini: {gemini_keys[0]}")
                        
                        # Adicionar a API key à URL
                        url_with_key = f"{url}?key={api_key}"
                        
                        # Fazer a requisição com API key
                        response = requests.post(
                            url_with_key,
                            headers=headers,
                            json=payload,
                            timeout=60
                        )
                        
                        print(f"📊 Status da resposta com API key: {response.status_code}")
                    else:
                        print("❌ Nenhuma API key de Gemini encontrada no arquivo de configuração")
                else:
                    print("❌ Arquivo de configuração de API keys não encontrado")
                    
            except Exception as e:
                print(f"❌ Erro ao tentar usar API key: {str(e)}")
        
        if response.status_code != 200:
            print(f"❌ Erro na resposta: {response.text}")
            return None
        
        # Processar a resposta
        response_data = response.json()
        
        # Verificar se há candidatos na resposta
        if "candidates" not in response_data or not response_data["candidates"]:
            print("❌ Nenhum candidato encontrado na resposta")
            return None
        
        # Extrair a imagem da resposta
        for candidate in response_data["candidates"]:
            if "content" in candidate and "parts" in candidate["content"]:
                for part in candidate["content"]["parts"]:
                    if "inlineData" in part and "data" in part["inlineData"]:
                        # Obter os dados da imagem em base64
                        image_data_base64 = part["inlineData"]["data"]
                        
                        # Decodificar de base64 para bytes
                        image_bytes = base64.b64decode(image_data_base64)
                        
                        print(f"✅ Sucesso! Imagem gerada com método Reddit do Gemini 2.5 Flash")
                        print(f"📊 Tamanho dos dados da imagem: {len(image_bytes)} bytes")
                        
                        return image_bytes
        
        print("❌ Nenhum dado de imagem encontrado na resposta")
        return None
        
    except Exception as e:
        print(f"❌ Erro ao gerar imagem com método Reddit do Gemini: {str(e)}")
        return None

def generate_image_pollinations(prompt, width, height, quality, model='gpt'):
    """
    Gera imagem usando Pollinations.ai com implementação melhorada e múltiplas estratégias
    Suporta modelos Flux, GPT e FLUX Kontext para diferentes tipos de imagem
    """
    try:
        import urllib.parse
        import time
        import random
        
        print(f"🎨 Iniciando geração com Pollinations.ai")
        print(f"📝 Prompt: {prompt[:50]}...")
        print(f"📏 Dimensões: {width}x{height}")
        print(f"🤖 Modelo: {model}")
        
        # Melhorar o prompt baseado no modelo
        if model == 'gpt':
            enhanced_prompt = f"{prompt}, photorealistic, high quality, detailed, realistic"
        elif model == 'flux-kontext':
            enhanced_prompt = f"{prompt}, context-aware, detailed, high quality, cinematic"
        else:  # flux
            enhanced_prompt = f"{prompt}, artistic, creative, high quality"
        
        # Codificar o prompt para URL
        encoded_prompt = urllib.parse.quote(enhanced_prompt, safe='')
        
        # Headers melhorados com rotação de User-Agent
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        
        headers = {
            'User-Agent': random.choice(user_agents),
            'Accept': 'image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        # Estratégias de URL melhoradas
        base_urls = [
            "https://image.pollinations.ai/prompt",
            "https://pollinations.ai/p"
        ]
        
        # Parâmetros otimizados por modelo - PRIORIDADE PARA NOLOGO
        if model == 'gpt':
            param_sets = [
                f"?width={width}&height={height}&nologo=true&model=openai&enhance=true",
                f"?width={width}&height={height}&nologo=true&model=dalle&quality=hd",
                f"?width={width}&height={height}&nologo=true&enhance=true&realistic=true",
                f"?width={width}&height={height}&model=openai&enhance=true",
                f"?width={width}&height={height}&model=dalle&quality=hd",
                f"?width={width}&height={height}&enhance=true&realistic=true",
                f"?width={width}&height={height}&model=openai",
                f"?width={width}&height={height}"
            ]
        elif model == 'flux-kontext':
            param_sets = [
                f"?width={width}&height={height}&nologo=true&model=flux-kontext&enhance=true",
                f"?width={width}&height={height}&nologo=true&model=flux-kontext",
                f"?width={width}&height={height}&model=flux-kontext&enhance=true",
                f"?width={width}&height={height}&model=flux-kontext",
                f"?width={width}&height={height}&nologo=true&model=flux&enhance=true",
                f"?width={width}&height={height}&nologo=true&model=flux",
                f"?width={width}&height={height}&model=flux&enhance=true",
                f"?width={width}&height={height}&model=flux"
            ]
        else:  # flux
            param_sets = [
                f"?width={width}&height={height}&nologo=true&model=flux&enhance=true",
                f"?width={width}&height={height}&nologo=true&model=flux-dev&quality=hd",
                f"?width={width}&height={height}&nologo=true&enhance=true",
                f"?width={width}&height={height}&nologo=true&model=flux",
                f"?width={width}&height={height}&model=flux&enhance=true",
                f"?width={width}&height={height}&model=flux-dev&quality=hd",
                f"?width={width}&height={height}&model=flux",
                f"?width={width}&height={height}"
            ]
        
        # Gerar todas as combinações de URLs
        urls_to_try = []
        for base_url in base_urls:
            for params in param_sets:
                urls_to_try.append(f"{base_url}/{encoded_prompt}{params}")
        
        # Tentar cada URL com estratégia melhorada
        for i, url in enumerate(urls_to_try, 1):
            try:
                print(f"🎨 Tentativa {i}/{len(urls_to_try)} - Pollinations.ai")
                print(f"🔗 URL: {url[:80]}...")
                
                # Timeout progressivo (mais tempo para tentativas posteriores)
                timeout = min(30 + (i * 5), 60)
                
                response = requests.get(
                    url, 
                    headers=headers, 
                    timeout=timeout,
                    allow_redirects=True,
                    stream=False,  # Não usar stream para evitar problemas
                    verify=True
                )
                
                print(f"📊 Status: {response.status_code} | Tamanho: {len(response.content)} bytes")
                
                if response.status_code == 200:
                    content_type = response.headers.get('content-type', '').lower()
                    content_length = len(response.content)
                    
                    # Validação melhorada de imagem
                    is_valid_image = (
                        content_length > 2000 and  # Limite mínimo reduzido
                        (
                            'image' in content_type or
                            response.content.startswith(b'\x89PNG') or  # PNG
                            response.content.startswith(b'\xff\xd8\xff') or  # JPEG
                            response.content.startswith(b'GIF8') or  # GIF
                            (response.content.startswith(b'RIFF') and b'WEBP' in response.content[:20]) or  # WebP
                            response.content.startswith(b'\x00\x00\x01\x00')  # ICO
                        )
                    )
                    
                    # Verificação anti-HTML melhorada
                    is_html = (
                        'text/html' in content_type or
                        b'<html' in response.content[:200].lower() or
                        b'<!doctype' in response.content[:200].lower() or
                        b'<body' in response.content[:500].lower()
                    )
                    
                    if is_valid_image and not is_html:
                        print(f"✅ Sucesso! Imagem gerada com Pollinations.ai")
                        print(f"📏 Dimensões solicitadas: {width}x{height}")
                        print(f"💾 Tamanho do arquivo: {content_length:,} bytes")
                        print(f"🤖 Modelo usado: {model}")
                        print(f"📝 Prompt final: {enhanced_prompt[:100]}...")
                        print(f"🔗 URL bem-sucedida: {url[:100]}...")
                        
                        # Tentar remover marca d'água por pós-processamento se necessário
                        processed_content = remove_watermark_if_needed(response.content, width, height)
                        return processed_content
                    else:
                        print(f"❌ Resposta inválida na tentativa {i}")
                        print(f"🔍 Content-Type: {content_type}")
                        print(f"📊 Tamanho: {content_length} bytes")
                        if is_html:
                            print("⚠️ Detectada resposta HTML")
                            html_preview = response.content[:300].decode('utf-8', errors='ignore')
                            print(f"🔍 HTML Preview: {html_preview}")
                        else:
                            print(f"⚠️ Imagem muito pequena ou formato inválido")
                        continue
                        
                elif response.status_code == 502:
                    print(f"🔄 Erro 502 (Bad Gateway) - Servidor sobrecarregado")
                    # Aguardar um pouco antes da próxima tentativa
                    time.sleep(2)
                    continue
                elif response.status_code == 503:
                    print(f"🔄 Erro 503 (Service Unavailable) - Serviço temporariamente indisponível")
                    time.sleep(3)
                    continue
                else:
                    print(f"❌ Erro HTTP {response.status_code}")
                    continue
                    
            except requests.exceptions.Timeout:
                print(f"⏰ Timeout na tentativa {i} (após {timeout}s)")
                continue
            except requests.exceptions.ConnectionError:
                print(f"🔌 Erro de conexão na tentativa {i}")
                time.sleep(1)  # Pequena pausa antes da próxima tentativa
                continue
            except Exception as e:
                print(f"❌ Erro na tentativa {i}: {str(e)}")
                continue
        
        # Fallbacks melhorados
        print(f"🔄 Tentando fallbacks...")
        
        # Fallback 1: Lorem Picsum (mais confiável)
        fallback_urls = [
            f"https://picsum.photos/{width}/{height}?random={int(time.time())}",
            f"https://picsum.photos/{width}/{height}",
            f"https://source.unsplash.com/{width}x{height}/?nature"
        ]
        
        for fallback_url in fallback_urls:
            try:
                print(f"🔄 Tentando fallback: {fallback_url}")
                response = requests.get(fallback_url, timeout=20, headers={'User-Agent': headers['User-Agent']})
                if response.status_code == 200 and len(response.content) > 1000:
                    print(f"✅ Fallback bem-sucedido: {len(response.content)} bytes")
                    return response.content
            except Exception as e:
                print(f"❌ Fallback falhou: {str(e)}")
                continue
        
        # Placeholder final melhorado
        print(f"⚠️ Gerando placeholder personalizado...")
        return generate_placeholder_image(width, height, prompt)
        
    except Exception as e:
        print(f"❌ Erro crítico: {str(e)}")
        return generate_placeholder_image(width, height, prompt)

def remove_watermark_if_needed(image_content, width, height):
    """
    Remove marca d'água cortando os últimos 45 pixels da parte inferior da imagem
    se detectar possível marca d'água do Pollinations.ai
    """
    try:
        from PIL import Image
        import io
        
        # Carregar a imagem
        img = Image.open(io.BytesIO(image_content))
        img_width, img_height = img.size
        
        # Verificar se a imagem tem dimensões que podem conter marca d'água
        # Pollinations.ai adiciona marca d'água principalmente em imagens menores
        if img_height > 100 and img_width >= 512:  # Só processar se for grande o suficiente
            # Cortar os últimos 45 pixels da parte inferior
            watermark_height = min(45, img_height // 10)  # Máximo 10% da altura
            cropped_img = img.crop((0, 0, img_width, img_height - watermark_height))
            
            # Redimensionar de volta para as dimensões originais se necessário
            if width and height and (cropped_img.width != width or cropped_img.height != height):
                cropped_img = cropped_img.resize((width, height), Image.Resampling.LANCZOS)
            
            # Converter de volta para bytes
            output = io.BytesIO()
            cropped_img.save(output, format='PNG', optimize=True)
            
            print(f"🔧 Marca d'água removida: cortados {watermark_height}px da parte inferior")
            return output.getvalue()
        
        # Se não precisar de processamento, retornar original
        return image_content
        
    except Exception as e:
        print(f"⚠️ Erro ao processar remoção de marca d'água: {str(e)}")
        # Em caso de erro, retornar imagem original
        return image_content

def generate_placeholder_image(width, height, prompt):
    """
    Gera uma imagem placeholder quando todas as APIs falham
    """
    try:
        from PIL import Image, ImageDraw, ImageFont
        import io
        
        # Criar imagem placeholder
        img = Image.new('RGB', (width, height), color='#2D3748')
        draw = ImageDraw.Draw(img)
        
        # Tentar usar fonte padrão
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        # Texto do placeholder
        text_lines = [
            "🖼️ Imagem Placeholder",
            f"Prompt: {prompt[:50]}...",
            f"Tamanho: {width}x{height}",
            "APIs temporariamente indisponíveis"
        ]
        
        # Desenhar texto centralizado
        y_offset = height // 2 - (len(text_lines) * 30) // 2
        for line in text_lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            draw.text((x, y_offset), line, fill='white', font=font)
            y_offset += 35
        
        # Converter para bytes
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        return img_bytes.getvalue()
        
    except Exception as e:
        print(f"❌ Erro ao gerar placeholder: {str(e)}")
        # Retornar uma imagem mínima se tudo falhar
        return b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x04\x00\x00\x00\x04\x00\x08\x02\x00\x00\x00\x91\x5c\xef\x1f\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xdd\x8d\xb4\x1c\x00\x00\x00\x00IEND\xaeB`\x82'

# Endpoints para servir arquivos de áudio e vídeo

@images_bp.route('/audio/<filename>', methods=['GET'])
def serve_audio(filename):
    """Serve arquivos de áudio do diretório output/audio"""
    try:
        audio_dir = os.path.join(OUTPUT_DIR, 'audio')
        if not os.path.exists(audio_dir):
            return jsonify({'error': 'Diretório de áudio não encontrado'}), 404
        
        return send_from_directory(audio_dir, filename)
    except FileNotFoundError:
        return jsonify({'error': 'Arquivo de áudio não encontrado'}), 404
    except Exception as e:
        return jsonify({'error': f'Erro ao servir áudio: {str(e)}'}), 500

@images_bp.route('/video/<filename>', methods=['GET'])
def serve_video(filename):
    """Serve arquivos de vídeo do diretório output/videos"""
    try:
        video_dir = os.path.join(OUTPUT_DIR, 'videos')
        if not os.path.exists(video_dir):
            return jsonify({'error': 'Diretório de vídeo não encontrado'}), 404
        
        return send_from_directory(video_dir, filename)
    except FileNotFoundError:
        return jsonify({'error': 'Arquivo de vídeo não encontrado'}), 404
    except Exception as e:
        return jsonify({'error': f'Erro ao servir vídeo: {str(e)}'}), 500

@images_bp.route('/text/<filename>', methods=['GET'])
def serve_text(filename):
    """Serve arquivos de texto do diretório output"""
    try:
        text_dir = OUTPUT_DIR
        if not os.path.exists(text_dir):
            return jsonify({'error': 'Diretório de texto não encontrado'}), 404
        
        # Verificar se é um arquivo de texto
        if not filename.endswith('.txt'):
            return jsonify({'error': 'Formato de arquivo inválido'}), 400
        
        file_path = os.path.join(text_dir, filename)
        if not os.path.exists(file_path):
            return jsonify({'error': 'Arquivo de texto não encontrado'}), 404
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return jsonify({
            'filename': filename,
            'content': content
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro ao servir texto: {str(e)}'}), 500

@images_bp.route('/list-all-content', methods=['GET'])
def list_all_content():
    """Lista todos os conteúdos gerados (texto, imagem, áudio, vídeo)"""
    try:
        contents = {
            'text': [],
            'images': [],
            'audio': [],
            'videos': [],
            'projects': []
        }
        
        # Diretórios a serem verificados
        directories = {
            'text': OUTPUT_DIR,
            'images': os.path.join(OUTPUT_DIR, 'images'),
            'audio': os.path.join(OUTPUT_DIR, 'audio'),
            'videos': os.path.join(OUTPUT_DIR, 'videos')
        }
        
        for content_type, directory in directories.items():
            if os.path.exists(directory):
                files = []
                for filename in os.listdir(directory):
                    file_path = os.path.join(directory, filename)
                    if os.path.isfile(file_path):
                        stat = os.stat(file_path)
                        
                        # Determinar URL baseado no tipo
                        if content_type == 'text':
                            url = f"/api/images/text/{filename}"
                        elif content_type == 'images':
                            url = f"/api/images/view/{filename}"
                        elif content_type == 'audio':
                            url = f"/api/images/audio/{filename}"
                        elif content_type == 'videos':
                            url = f"/api/images/video/{filename}"
                        
                        files.append({
                            'filename': filename,
                            'url': url,
                            'size': stat.st_size,
                            'created': datetime.datetime.fromtimestamp(stat.st_ctime).isoformat(),
                            'modified': datetime.datetime.fromtimestamp(stat.st_mtime).isoformat()
                        })
                
                # Ordenar por data de criação (mais recente primeiro)
                files.sort(key=lambda x: x['created'], reverse=True)
                contents[content_type] = files
        
        # Adicionar conteúdo do diretório outputs (vídeos finais)
        outputs_dir = os.path.join(os.path.dirname(OUTPUT_DIR), 'outputs')
        if os.path.exists(outputs_dir):
            video_files = []
            for filename in os.listdir(outputs_dir):
                file_path = os.path.join(outputs_dir, filename)
                if os.path.isfile(file_path) and filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                    stat = os.stat(file_path)
                    video_files.append({
                        'filename': filename,
                        'url': f"/api/images/video/{filename}",
                        'size': stat.st_size,
                        'created': datetime.datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        'modified': datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        'source': 'final_output'
                    })
            
            video_files.sort(key=lambda x: x['created'], reverse=True)
            contents['videos'].extend(video_files)
        
        # Adicionar conteúdo da pasta projects (organizado por pipeline)
        projects_dir = os.path.join(os.path.dirname(OUTPUT_DIR), 'projects')
        if os.path.exists(projects_dir):
            projects = []
            for project_id in os.listdir(projects_dir):
                project_path = os.path.join(projects_dir, project_id)
                if os.path.isdir(project_path):
                    project_data = {
                        'project_id': project_id,
                        'contents': {
                            'text': [],
                            'images': [],
                            'audio': [],
                            'videos': []
                        }
                    }
                    
                    # Verificar cada subdiretório do projeto
                    subdirs = {
                        'text': os.path.join(project_path, 'texts'),
                        'images': os.path.join(project_path, 'images'),
                        'audio': os.path.join(project_path, 'audio'),
                        'videos': os.path.join(project_path, 'video')
                    }
                    
                    for content_type, subdir in subdirs.items():
                        if os.path.exists(subdir):
                            files = []
                            for filename in os.listdir(subdir):
                                file_path = os.path.join(subdir, filename)
                                if os.path.isfile(file_path):
                                    stat = os.stat(file_path)
                                    
                                    # Determinar URL baseado no tipo e projeto
                                    if content_type == 'text':
                                        url = f"/api/images/project/{project_id}/text/{filename}"
                                    elif content_type == 'images':
                                        url = f"/api/images/project/{project_id}/image/{filename}"
                                    elif content_type == 'audio':
                                        url = f"/api/images/project/{project_id}/audio/{filename}"
                                    elif content_type == 'videos':
                                        url = f"/api/images/project/{project_id}/video/{filename}"
                                    
                                    files.append({
                                        'filename': filename,
                                        'url': url,
                                        'size': stat.st_size,
                                        'created': datetime.datetime.fromtimestamp(stat.st_ctime).isoformat(),
                                    'modified': datetime.datetime.fromtimestamp(stat.st_mtime).isoformat()
                                    })
                            
                            # Ordenar por data de criação
                            files.sort(key=lambda x: x['created'], reverse=True)
                            project_data['contents'][content_type] = files
                    
                    projects.append(project_data)
            
            # Ordenar projetos pelo ID (assumindo que o ID contém timestamp)
            projects.sort(key=lambda x: x['project_id'], reverse=True)
            contents['projects'] = projects
        
        return jsonify({
            'success': True,
            'contents': contents,
            'summary': {
                'total_text': len(contents['text']),
                'total_images': len(contents['images']),
                'total_audio': len(contents['audio']),
                'total_videos': len(contents['videos']),
                'total_projects': len(contents['projects'])
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao listar conteúdos: {str(e)}'
        }), 500

# Endpoints para servir arquivos de projetos

@images_bp.route('/project/<project_id>/image/<filename>', methods=['GET'])
def serve_project_image(project_id, filename):
    """Serve arquivos de imagem de um projeto específico"""
    try:
        project_image_dir = os.path.join(os.path.dirname(OUTPUT_DIR), 'projects', project_id, 'images')
        if not os.path.exists(project_image_dir):
            return jsonify({'error': 'Diretório de imagens do projeto não encontrado'}), 404
        
        return send_from_directory(project_image_dir, filename)
    except FileNotFoundError:
        return jsonify({'error': 'Arquivo de imagem do projeto não encontrado'}), 404
    except Exception as e:
        return jsonify({'error': f'Erro ao servir imagem do projeto: {str(e)}'}), 500

@images_bp.route('/project/<project_id>/audio/<filename>', methods=['GET'])
def serve_project_audio(project_id, filename):
    """Serve arquivos de áudio de um projeto específico"""
    try:
        project_audio_dir = os.path.join(os.path.dirname(OUTPUT_DIR), 'projects', project_id, 'audio')
        if not os.path.exists(project_audio_dir):
            return jsonify({'error': 'Diretório de áudio do projeto não encontrado'}), 404
        
        return send_from_directory(project_audio_dir, filename)
    except FileNotFoundError:
        return jsonify({'error': 'Arquivo de áudio do projeto não encontrado'}), 404
    except Exception as e:
        return jsonify({'error': f'Erro ao servir áudio do projeto: {str(e)}'}), 500

@images_bp.route('/project/<project_id>/video/<filename>', methods=['GET'])
def serve_project_video(project_id, filename):
    """Serve arquivos de vídeo de um projeto específico"""
    try:
        project_video_dir = os.path.join(os.path.dirname(OUTPUT_DIR), 'projects', project_id, 'video')
        if not os.path.exists(project_video_dir):
            return jsonify({'error': 'Diretório de vídeo do projeto não encontrado'}), 404
        
        return send_from_directory(project_video_dir, filename)
    except FileNotFoundError:
        return jsonify({'error': 'Arquivo de vídeo do projeto não encontrado'}), 404
    except Exception as e:
        return jsonify({'error': f'Erro ao servir vídeo do projeto: {str(e)}'}), 500

@images_bp.route('/project/<project_id>/text/<filename>', methods=['GET'])
def serve_project_text(project_id, filename):
    """Serve arquivos de texto de um projeto específico"""
    try:
        project_text_dir = os.path.join(os.path.dirname(OUTPUT_DIR), 'projects', project_id, 'texts')
        if not os.path.exists(project_text_dir):
            return jsonify({'error': 'Diretório de textos do projeto não encontrado'}), 404
        
        # Verificar se é um arquivo de texto
        if not filename.endswith('.txt'):
            return jsonify({'error': 'Formato de arquivo inválido'}), 400
        
        file_path = os.path.join(project_text_dir, filename)
        if not os.path.exists(file_path):
            return jsonify({'error': 'Arquivo de texto do projeto não encontrado'}), 404
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return jsonify({
            'filename': filename,
            'project_id': project_id,
            'content': content
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro ao servir texto do projeto: {str(e)}'}), 500

@images_bp.route('/delete/<file_type>/<filename>', methods=['DELETE'])
def delete_file(file_type, filename):
    """
    Exclui um arquivo baseado no tipo (text, image, audio, video)
    """
    try:
        # Determinar o diretório baseado no tipo de arquivo
        base_dir = os.path.dirname(os.path.dirname(__file__))
        
        if file_type == 'text':
            file_dir = OUTPUT_DIR  # Os arquivos de texto estão no mesmo diretório das imagens
        elif file_type == 'image':
            file_dir = os.path.join(base_dir, 'output', 'images')
        elif file_type == 'audio':
            # Verificar em múltiplos diretórios possíveis
            possible_dirs = [
                os.path.join(base_dir, 'output', 'audio'),
                os.path.join(base_dir, 'temp')
            ]
            file_path = None
            for dir_path in possible_dirs:
                if os.path.exists(os.path.join(dir_path, filename)):
                    file_path = os.path.join(dir_path, filename)
                    break
            
            if not file_path:
                return jsonify({'error': 'Arquivo de áudio não encontrado'}), 404
                
            os.remove(file_path)
            return jsonify({
                'success': True,
                'message': f'Arquivo de áudio "{filename}" excluído com sucesso'
            })
            
        elif file_type == 'video':
            # Verificar em múltiplos diretórios possíveis
            possible_dirs = [
                os.path.join(base_dir, 'output', 'videos'),
                os.path.join(base_dir, 'outputs')
            ]
            file_path = None
            for dir_path in possible_dirs:
                if os.path.exists(os.path.join(dir_path, filename)):
                    file_path = os.path.join(dir_path, filename)
                    break
            
            if not file_path:
                return jsonify({'error': 'Arquivo de vídeo não encontrado'}), 404
                
            os.remove(file_path)
            return jsonify({
                'success': True,
                'message': f'Arquivo de vídeo "{filename}" excluído com sucesso'
            })
        else:
            return jsonify({'error': 'Tipo de arquivo inválido'}), 400
        
        # Para texto e imagem, usar o diretório específico
        file_path = os.path.join(file_dir, filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': f'Arquivo de {file_type} não encontrado'}), 404
        
        os.remove(file_path)
        
        return jsonify({
            'success': True,
            'message': f'Arquivo de {file_type} "{filename}" excluído com sucesso'
        })
        
    except Exception as e:
        error_response = auto_format_error(str(e), f'Exclusão de Arquivo ({file_type})')
        return jsonify(error_response), 500

@images_bp.route('/delete/project/<project_id>/<file_type>/<filename>', methods=['DELETE'])
def delete_project_file(project_id, file_type, filename):
    """
    Exclui um arquivo de um projeto específico baseado no tipo (text, image, audio, video)
    """
    try:
        base_dir = os.path.dirname(os.path.dirname(__file__))
        projects_dir = os.path.join(base_dir, 'projects')
        
        # Verificar se o projeto existe
        project_path = os.path.join(projects_dir, project_id)
        if not os.path.exists(project_path):
            return jsonify({'error': 'Projeto não encontrado'}), 404
        
        # Determinar o subdiretório baseado no tipo de arquivo
        if file_type == 'text':
            file_dir = os.path.join(project_path, 'texts')
        elif file_type == 'image':
            file_dir = os.path.join(project_path, 'images')
        elif file_type == 'audio':
            file_dir = os.path.join(project_path, 'audio')
        elif file_type == 'video':
            file_dir = os.path.join(project_path, 'video')
        else:
            return jsonify({'error': 'Tipo de arquivo inválido'}), 400
        
        file_path = os.path.join(file_dir, filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': f'Arquivo de {file_type} não encontrado no projeto'}), 404
        
        os.remove(file_path)
        
        return jsonify({
            'success': True,
            'message': f'Arquivo de {file_type} "{filename}" do projeto "{project_id}" excluído com sucesso'
        })
        
    except Exception as e:
        error_response = auto_format_error(str(e), f'Exclusão de Arquivo do Projeto ({file_type})')
        return jsonify(error_response), 500

@images_bp.route('/test-gemini', methods=['POST'])
def test_gemini_image_generation():
    """
    Endpoint de teste para geração de imagens com a API do Google Gemini.
    Permite testar diferentes prompts, configurações e chaves de API.
    """
    try:
        data = request.get_json()
        
        # Parâmetros básicos
        prompt = data.get('prompt', 'A beautiful landscape with mountains and a lake').strip()
        width = data.get('width', 1024)
        height = data.get('height', 1024)
        quality = data.get('quality', 'standard')
        test_mode = data.get('test_mode', 'single')  # single, multiple, stress
        
        # Validações
        if not prompt:
            return jsonify({
                'success': False,
                'error': 'Prompt é obrigatório'
            }), 400
        
        # Validar dimensões
        try:
            width = int(width)
            height = int(height)
        except ValueError:
            width, height = 1024, 1024
        
        # Limites de dimensões
        if width < 256 or width > 2048 or height < 256 or height > 2048:
            return jsonify({
                'success': False,
                'error': 'Dimensões devem estar entre 256x256 e 2048x2048'
            }), 400
        
        # Obter uma chave Gemini do sistema
        from routes.automations import get_next_gemini_key
        api_key = get_next_gemini_key()
        
        if not api_key:
            return jsonify({
                'success': False,
                'error': 'Nenhuma chave Gemini disponível'
            }), 400
        
        # Criar diretório para imagens de teste
        test_dir = os.path.join(os.path.dirname(__file__), '..', 'output', 'test_images')
        os.makedirs(test_dir, exist_ok=True)
        
        results = []
        start_time = time.time()
        
        # Modo de teste único
        if test_mode == 'single':
            try:
                print(f"🧪 Teste único: Gerando imagem com Gemini")
                print(f"📝 Prompt: {prompt}")
                print(f"📏 Dimensões: {width}x{height}")
                print(f"🎯 Qualidade: {quality}")
                
                # Gerar imagem
                image_bytes = generate_image_gemini(prompt, api_key, width, height, quality)
                
                if image_bytes:
                    # Salvar a imagem
                    timestamp = int(time.time() * 1000)
                    filename = f"gemini_test_{timestamp}.png"
                    filepath = os.path.join(test_dir, filename)
                    
                    with open(filepath, 'wb') as f:
                        f.write(image_bytes)
                    
                    # URL para acessar a imagem
                    image_url = f"/api/images/test/{filename}"
                    
                    # Calcular tamanho e tempo
                    file_size = len(image_bytes) / 1024  # KB
                    elapsed_time = time.time() - start_time
                    
                    results.append({
                        'test_id': 1,
                        'success': True,
                        'prompt': prompt,
                        'url': image_url,
                        'width': width,
                        'height': height,
                        'quality': quality,
                        'file_size_kb': round(file_size, 2),
                        'elapsed_time': round(elapsed_time, 2),
                        'message': 'Imagem gerada com sucesso'
                    })
                else:
                    results.append({
                        'test_id': 1,
                        'success': False,
                        'prompt': prompt,
                        'width': width,
                        'height': height,
                        'quality': quality,
                        'error': 'Falha ao gerar imagem',
                        'message': 'A API do Gemini não retornou uma imagem válida'
                    })
                    
            except Exception as e:
                elapsed_time = time.time() - start_time
                results.append({
                    'test_id': 1,
                    'success': False,
                    'prompt': prompt,
                    'width': width,
                    'height': height,
                    'quality': quality,
                    'error': str(e),
                    'elapsed_time': round(elapsed_time, 2),
                    'message': 'Erro durante a geração da imagem'
                })
        
        # Modo de teste múltiplo
        elif test_mode == 'multiple':
            test_prompts = [
                "A beautiful landscape with mountains and a lake",
                "A futuristic city with flying cars",
                "A cute cat sitting on a windowsill",
                "A delicious plate of food with vibrant colors",
                "An abstract painting with geometric shapes"
            ]
            
            for i, test_prompt in enumerate(test_prompts):
                try:
                    print(f"🧪 Teste múltiplo {i+1}/5: Gerando imagem com Gemini")
                    print(f"📝 Prompt: {test_prompt}")
                    
                    # Gerar imagem
                    image_bytes = generate_image_gemini(test_prompt, api_key, width, height, quality)
                    
                    if image_bytes:
                        # Salvar a imagem
                        timestamp = int(time.time() * 1000)
                        filename = f"gemini_test_{timestamp}_{i+1}.png"
                        filepath = os.path.join(test_dir, filename)
                        
                        with open(filepath, 'wb') as f:
                            f.write(image_bytes)
                        
                        # URL para acessar a imagem
                        image_url = f"/api/images/test/{filename}"
                        
                        # Calcular tamanho e tempo
                        file_size = len(image_bytes) / 1024  # KB
                        elapsed_time = time.time() - start_time
                        
                        results.append({
                            'test_id': i+1,
                            'success': True,
                            'prompt': test_prompt,
                            'url': image_url,
                            'width': width,
                            'height': height,
                            'quality': quality,
                            'file_size_kb': round(file_size, 2),
                            'elapsed_time': round(elapsed_time, 2),
                            'message': 'Imagem gerada com sucesso'
                        })
                    else:
                        results.append({
                            'test_id': i+1,
                            'success': False,
                            'prompt': test_prompt,
                            'width': width,
                            'height': height,
                            'quality': quality,
                            'error': 'Falha ao gerar imagem',
                            'message': 'A API do Gemini não retornou uma imagem válida'
                        })
                        
                except Exception as e:
                    elapsed_time = time.time() - start_time
                    results.append({
                        'test_id': i+1,
                        'success': False,
                        'prompt': test_prompt,
                        'width': width,
                        'height': height,
                        'quality': quality,
                        'error': str(e),
                        'elapsed_time': round(elapsed_time, 2),
                        'message': 'Erro durante a geração da imagem'
                    })
                    
                    # Pequeno delay entre tentativas
                    time.sleep(2)
        
        # Modo de teste de estresse
        elif test_mode == 'stress':
            max_tests = min(10, data.get('max_tests', 5))
            success_count = 0
            error_count = 0
            
            for i in range(max_tests):
                try:
                    print(f"🧪 Teste de estresse {i+1}/{max_tests}: Gerando imagem com Gemini")
                    
                    # Gerar imagem
                    image_bytes = generate_image_gemini(prompt, api_key, width, height, quality)
                    
                    if image_bytes:
                        # Salvar a imagem
                        timestamp = int(time.time() * 1000)
                        filename = f"gemini_stress_{timestamp}_{i+1}.png"
                        filepath = os.path.join(test_dir, filename)
                        
                        with open(filepath, 'wb') as f:
                            f.write(image_bytes)
                        
                        # URL para acessar a imagem
                        image_url = f"/api/images/test/{filename}"
                        
                        # Calcular tamanho
                        file_size = len(image_bytes) / 1024  # KB
                        
                        results.append({
                            'test_id': i+1,
                            'success': True,
                            'prompt': prompt,
                            'url': image_url,
                            'width': width,
                            'height': height,
                            'quality': quality,
                            'file_size_kb': round(file_size, 2),
                            'message': 'Imagem gerada com sucesso'
                        })
                        
                        success_count += 1
                    else:
                        results.append({
                            'test_id': i+1,
                            'success': False,
                            'prompt': prompt,
                            'width': width,
                            'height': height,
                            'quality': quality,
                            'error': 'Falha ao gerar imagem',
                            'message': 'A API do Gemini não retornou uma imagem válida'
                        })
                        
                        error_count += 1
                        
                except Exception as e:
                    results.append({
                        'test_id': i+1,
                        'success': False,
                        'prompt': prompt,
                        'width': width,
                        'height': height,
                        'quality': quality,
                        'error': str(e),
                        'message': 'Erro durante a geração da imagem'
                    })
                    
                    error_count += 1
                
                # Delay entre tentativas para evitar limites de taxa
                time.sleep(3)
            
            # Adicionar resumo do teste de estresse
            total_elapsed_time = time.time() - start_time
            success_rate = (success_count / max_tests) * 100
            
            results.append({
                'test_id': 'summary',
                'success': success_count > 0,
                'total_tests': max_tests,
                'success_count': success_count,
                'error_count': error_count,
                'success_rate': round(success_rate, 2),
                'total_elapsed_time': round(total_elapsed_time, 2),
                'average_time_per_test': round(total_elapsed_time / max_tests, 2),
                'message': f'Teste de estresse concluído: {success_count}/{max_tests} imagens geradas com sucesso'
            })
        
        # Calcular estatísticas gerais
        total_elapsed_time = time.time() - start_time
        successful_tests = [r for r in results if r.get('success', False)]
        failed_tests = [r for r in results if not r.get('success', False)]
        
        return jsonify({
            'success': True,
            'test_mode': test_mode,
            'total_tests': len(results),
            'successful_tests': len(successful_tests),
            'failed_tests': len(failed_tests),
            'success_rate': round((len(successful_tests) / len(results)) * 100, 2) if results else 0,
            'total_elapsed_time': round(total_elapsed_time, 2),
            'results': results,
            'message': f'Teste de geração de imagens com Gemini concluído: {len(successful_tests)}/{len(results)} imagens geradas com sucesso'
        })
        
    except Exception as e:
        error_response = auto_format_error(str(e), 'Teste de Geração de Imagens com Gemini')
        return jsonify(error_response), 500

@images_bp.route('/test/<filename>', methods=['GET'])
def serve_test_image(filename):
    """
    Serve imagens de teste geradas pelo endpoint /test-gemini
    """
    try:
        test_dir = os.path.join(os.path.dirname(__file__), '..', 'output', 'test_images')
        
        if not os.path.exists(test_dir):
            return jsonify({'error': 'Diretório de imagens de teste não encontrado'}), 404
        
        return send_from_directory(test_dir, filename)
    except FileNotFoundError:
        return jsonify({'error': 'Arquivo de imagem de teste não encontrado'}), 404
    except Exception as e:
        return jsonify({'error': f'Erro ao servir imagem de teste: {str(e)}'}), 500
