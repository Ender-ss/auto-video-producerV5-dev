import React, { useState, useEffect } from 'react';

const ImageGeneration = () => {
    const [script, setScript] = useState('');
    const [customPrompt, setCustomPrompt] = useState('');
    const [useCustomPrompt, setUseCustomPrompt] = useState(false);
    const [savedScripts, setSavedScripts] = useState([]);
    const [selectedSavedScript, setSelectedSavedScript] = useState('');
    const [useSavedScript, setUseSavedScript] = useState(false);
    const [pastedText, setPastedText] = useState('');
    const [usePastedText, setUsePastedText] = useState(false);
    const [useAiAgent, setUseAiAgent] = useState(false);
    const [aiAgentPrompt, setAiAgentPrompt] = useState('Crie uma descrição visual detalhada para uma imagem baseada no seguinte conteúdo:');
    const [style, setStyle] = useState('cinematic');
    const [images, setImages] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [apiKey, setApiKey] = useState('');
    const [provider, setProvider] = useState('together'); // together, gemini, gemini-reddit ou pollinations
    const [format, setFormat] = useState('1024x1024'); // formato da imagem
    const [quality, setQuality] = useState('standard'); // qualidade da imagem
    const [batchCount, setBatchCount] = useState(1);
    const [delayBetweenImages, setDelayBetweenImages] = useState(3);
    const [currentBatch, setCurrentBatch] = useState(0);
    const [isGeneratingBatch, setIsGeneratingBatch] = useState(false);
    const [pollinationsModel, setPollinationsModel] = useState('gpt'); // flux ou gpt
    const [isCancelled, setIsCancelled] = useState(false);
    const [abortController, setAbortController] = useState(null);
    const [googleCookies, setGoogleCookies] = useState('');

    useEffect(() => {
        const fetchApiKey = async () => {
            // Não precisa de chave de API para gemini-reddit, pollinations, gemini-imagen3 ou gemini-imagen3-rohitaryal
            if (provider === 'gemini-reddit' || provider === 'pollinations' || provider === 'gemini-imagen3' || provider === 'gemini-imagen3-rohitaryal') {
                setApiKey('');
                setError(null);
                return;
            }
            
            try {
                const apiEndpoint = provider === 'gemini' ? 'gemini_1' : 'together';
                const response = await fetch(`/api/settings/api-keys/${apiEndpoint}`);
                const data = await response.json();
                if (data.success) {
                    setApiKey(data.api_key);
                    setError(null);
                } else {
                    setError(`Chave da API ${provider === 'gemini' ? 'Gemini' : 'Together.ai'} não encontrada. Por favor, configure-a nas Configurações.`);
                }
            } catch (err) {
                setError('Não foi possível buscar a chave da API. Verifique a conexão com o backend.');
            }
        };

        fetchApiKey();
    }, [provider]);

    // Carregar roteiros salvos do localStorage
    useEffect(() => {
        const loadSavedScripts = () => {
            try {
                const saved = localStorage.getItem('generated_scripts');
                if (saved) {
                    const parsed = JSON.parse(saved);
                    if (parsed && parsed.chapters) {
                        setSavedScripts([{
                            id: 'current',
                            title: parsed.title || 'Roteiro Atual',
                            content: parsed.chapters.map(ch => ch.content).join('\n\n')
                        }]);
                    }
                }
            } catch (err) {
                console.error('Erro ao carregar roteiros salvos:', err);
            }
        };

        loadSavedScripts();
    }, []);

    const handleGenerateImages = async () => {
        // Verificar se a chave de API é necessária (não é necessária para Pollinations.ai, Gemini Reddit, Gemini Imagen3 ou Gemini Imagen3-rohitaryal)
        if (!apiKey && provider !== 'pollinations' && provider !== 'gemini-reddit' && provider !== 'gemini-imagen3' && provider !== 'gemini-imagen3-rohitaryal') {
            const providerName = provider === 'gemini' ? 'Gemini' : 'Together.ai';
            setError(`A chave da API do ${providerName} não está configurada.`);
            return;
        }

        let promptToUse = '';
        
        // Determinar qual fonte de conteúdo usar
        if (useCustomPrompt) {
            promptToUse = customPrompt;
        } else if (useSavedScript && selectedSavedScript) {
            const savedScript = savedScripts.find(s => s.id === selectedSavedScript);
            promptToUse = savedScript ? savedScript.content : '';
        } else if (usePastedText) {
            promptToUse = pastedText;
        } else {
            promptToUse = script;
        }

        if (!promptToUse) {
            setError('Por favor, forneça um conteúdo para gerar as imagens.');
            return;
        }

        // Resetar estado de cancelamento
        setIsCancelled(false);
        
        // Criar novo AbortController
        const controller = new AbortController();
        setAbortController(controller);

        // Se usar agente IA, processar o conteúdo primeiro
        if (useAiAgent) {
            promptToUse = await processWithAiAgent(promptToUse);
            if (!promptToUse || isCancelled) {
                setError('Falha ao processar conteúdo com o agente IA.');
                return;
            }
        }

        if (batchCount > 1) {
            await handleBatchGeneration(promptToUse, controller);
        } else {
            await generateSingleImage(promptToUse, controller);
        }
    };

    const handleCancelGeneration = () => {
        setIsCancelled(true);
        if (abortController) {
            abortController.abort();
        }
        setIsLoading(false);
        setIsGeneratingBatch(false);
        setCurrentBatch(0);
        setError('Geração cancelada pelo usuário.');
    };

    const processWithAiAgent = async (content) => {
        try {
            setError(null);
            
            // Buscar chaves de API para o agente IA
            const keysResponse = await fetch('/api/settings/api-keys');
            const keysData = await keysResponse.json();
            
            if (!keysData.success) {
                throw new Error('Não foi possível carregar as chaves de API');
            }
            
            const apiKeys = keysData.keys || {};
            
            // Usar OpenAI como padrão para o agente IA
            if (!apiKeys.openai) {
                throw new Error('Chave da API OpenAI não encontrada para o agente IA');
            }
            
            const fullPrompt = `${aiAgentPrompt}\n\n${content}`;
            
            const response = await fetch('/api/premise/generate-agent-script', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    title: 'Geração de Prompt para Imagem',
                    premise: content,
                    custom_prompt: aiAgentPrompt,
                    ai_provider: 'openai',
                    openrouter_model: 'auto',
                    num_chapters: 1,
                    api_keys: apiKeys
                }),
            });
            
            const data = await response.json();
            
            if (data.success && data.script) {
                return data.script;
            } else {
                throw new Error(data.error || 'Falha ao processar com agente IA');
            }
        } catch (err) {
            console.error('Erro no agente IA:', err);
            setError(`Erro no agente IA: ${err.message}`);
            return null;
        }
    };

    const generateSingleImage = async (promptText, controller) => {
        setIsLoading(true);
        setError(null);
        setImages([]);
        
        try {
            const response = await fetch('/api/images/generate-enhanced', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    script: promptText,
                    api_key: apiKey,
                    style: style,
                    provider: provider,
                    format: format,
                    quality: quality,
                    pollinations_model: pollinationsModel,
                    image_count: 1,
                    google_cookies: (provider === 'gemini-imagen3-rohitaryal' || provider === 'gemini-imagen3') ? googleCookies : undefined
                }),
                signal: controller.signal
            });

            const data = await response.json();

            if (data.success) {
                const newImages = data.images || [];
                setImages(prev => [...prev, ...newImages]);
                
                // Salvar imagens no localStorage para uso na criação de vídeos
                const existingImages = JSON.parse(localStorage.getItem('generated_images') || '[]');
                const imagesToSave = newImages.map((img, index) => ({
                    id: Date.now() + index,
                    url: img.url,
                    filename: `imagem_gerada_${Date.now()}_${index + 1}.png`,
                    prompt: img.prompt || promptText.substring(0, 100) + (promptText.length > 100 ? '...' : ''),
                    style: style,
                    provider: img.provider || provider,
                    format: format,
                    quality: quality,
                    timestamp: new Date().toISOString(),
                    size: 'unknown' // Será atualizado quando a imagem for carregada
                }));
                
                const updatedImages = [...existingImages, ...imagesToSave];
                localStorage.setItem('generated_images', JSON.stringify(updatedImages));
                
                console.log('✅ Imagens salvas no localStorage:', imagesToSave);
            } else {
                setError(data.error);
            }
        } catch (err) {
            if (err.name === 'AbortError') {
                setError('Geração cancelada pelo usuário.');
            } else {
                setError('Falha ao conectar com o servidor. Verifique se o backend está rodando.');
            }
        }

        setIsLoading(false);
    };

    const handleBatchGeneration = async (promptText, controller) => {
        setIsGeneratingBatch(true);
        setIsLoading(true);
        setError(null);
        setImages([]);
        setCurrentBatch(1);

        try {
            setIsLoading(true);
            const response = await fetch('/api/images/generate-enhanced', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    script: promptText,
                    api_key: apiKey,
                    style: style,
                    provider: provider,
                    format: format,
                    quality: quality,
                    pollinations_model: pollinationsModel,
                    image_count: batchCount,
                    google_cookies: (provider === 'gemini-imagen3-rohitaryal' || provider === 'gemini-imagen3') ? googleCookies : undefined
                }),
                signal: controller.signal
            });

            const data = await response.json();

            if (data.success) {
                const newImages = data.images || [];
                setImages(prev => [...prev, ...newImages]);
                
                // Salvar imagens no localStorage para uso na criação de vídeos
                const existingImages = JSON.parse(localStorage.getItem('generated_images') || '[]');
                const imagesToSave = newImages.map((url, index) => ({
                    id: Date.now() + index,
                    url: url,
                    filename: `imagem_lote_${Date.now()}_${index + 1}.png`,
                    prompt: promptText.substring(0, 100) + (promptText.length > 100 ? '...' : ''),
                    style: style,
                    provider: provider,
                    format: format,
                    quality: quality,
                    timestamp: new Date().toISOString(),
                    batch: 1,
                    size: 'unknown'
                }));
                
                const updatedImages = [...existingImages, ...imagesToSave];
                localStorage.setItem('generated_images', JSON.stringify(updatedImages));
                
                console.log(`✅ ${batchCount} imagens geradas e salvas no localStorage:`, imagesToSave);
            } else {
                setError(data.error);
            }
        } catch (err) {
            if (err.name === 'AbortError') {
                setError('Geração cancelada pelo usuário.');
            } else {
                setError('Falha ao conectar com o servidor. Verifique se o backend está rodando.');
            }
        }

        setIsLoading(false);
        setIsGeneratingBatch(false);
        setCurrentBatch(0);
    };

    const downloadImage = async (image, index) => {
        try {
            const imageUrl = typeof image === 'string' ? image : image.url;
            const response = await fetch(imageUrl);
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = `imagem_gerada_${index + 1}.png`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            window.URL.revokeObjectURL(url);
        } catch (err) {
            setError('Erro ao baixar a imagem.');
        }
    };

    const downloadAllImages = async () => {
        for (let i = 0; i < images.length; i++) {
            await downloadImage(images[i], i);
            // Pequeno delay entre downloads
            await new Promise(resolve => setTimeout(resolve, 500));
        }
    };

    return (
        <div className="p-6 bg-gray-900 text-white min-h-screen">
            <h1 className="text-3xl font-bold mb-6">Geração de Imagens com IA</h1>

            <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
                {/* Opções de Fonte de Conteúdo */}
                <div className="mb-6 p-4 bg-gray-800 rounded-lg border border-gray-600">
                    <h3 className="text-lg font-semibold mb-4 text-blue-400">📝 Fonte do Conteúdo</h3>
                    
                    <div className="space-y-3">
                        <label className="flex items-center gap-3 cursor-pointer">
                            <input
                                type="radio"
                                name="contentSource"
                                checked={!useCustomPrompt && !useSavedScript && !usePastedText}
                                onChange={() => {
                                    setUseCustomPrompt(false);
                                    setUseSavedScript(false);
                                    setUsePastedText(false);
                                }}
                                className="w-4 h-4 text-blue-600 bg-gray-700 border-gray-600 focus:ring-blue-500"
                            />
                            <span className="text-lg font-medium">Roteiro Manual</span>
                        </label>

                        <label className="flex items-center gap-3 cursor-pointer">
                            <input
                                type="radio"
                                name="contentSource"
                                checked={useSavedScript}
                                onChange={(e) => {
                                    setUseSavedScript(e.target.checked);
                                    setUseCustomPrompt(false);
                                    setUsePastedText(false);
                                }}
                                className="w-4 h-4 text-blue-600 bg-gray-700 border-gray-600 focus:ring-blue-500"
                            />
                            <span className="text-lg font-medium">Roteiro Salvo</span>
                        </label>

                        <label className="flex items-center gap-3 cursor-pointer">
                            <input
                                type="radio"
                                name="contentSource"
                                checked={usePastedText}
                                onChange={(e) => {
                                    setUsePastedText(e.target.checked);
                                    setUseCustomPrompt(false);
                                    setUseSavedScript(false);
                                }}
                                className="w-4 h-4 text-blue-600 bg-gray-700 border-gray-600 focus:ring-blue-500"
                            />
                            <span className="text-lg font-medium">Colar Texto</span>
                        </label>

                        <label className="flex items-center gap-3 cursor-pointer">
                            <input
                                type="radio"
                                name="contentSource"
                                checked={useCustomPrompt}
                                onChange={(e) => {
                                    setUseCustomPrompt(e.target.checked);
                                    setUseSavedScript(false);
                                    setUsePastedText(false);
                                }}
                                className="w-4 h-4 text-blue-600 bg-gray-700 border-gray-600 focus:ring-blue-500"
                            />
                            <span className="text-lg font-medium">Prompt Personalizado</span>
                        </label>
                    </div>
                </div>

                {/* Opção de Agente IA */}
                <div className="mb-6 p-4 bg-gray-800 rounded-lg border border-gray-600">
                    <label className="flex items-center gap-3 cursor-pointer mb-4">
                        <input
                            type="checkbox"
                            checked={useAiAgent}
                            onChange={(e) => setUseAiAgent(e.target.checked)}
                            className="w-4 h-4 text-blue-600 bg-gray-700 border-gray-600 rounded focus:ring-blue-500"
                        />
                        <span className="text-lg font-medium text-purple-400">🤖 Usar Agente IA para Otimizar Prompts</span>
                    </label>
                    
                    {useAiAgent && (
                        <div>
                            <label htmlFor="aiAgentPrompt" className="block text-sm font-medium mb-2 text-gray-300">
                                Instruções para o Agente IA:
                            </label>
                            <textarea
                                id="aiAgentPrompt"
                                rows="3"
                                className="w-full p-3 bg-gray-700 rounded-md border border-gray-600 focus:ring-2 focus:ring-purple-500 text-sm"
                                placeholder="Ex: Crie uma descrição visual detalhada e cinematográfica..."
                                value={aiAgentPrompt}
                                onChange={(e) => setAiAgentPrompt(e.target.value)}
                            />
                        </div>
                    )}
                </div>

                {/* Campos de entrada baseados na seleção */}
                {useCustomPrompt && (
                    <div className="mb-4">
                        <label htmlFor="customPrompt" className="block text-lg font-medium mb-2">Prompt Personalizado</label>
                        <textarea
                            id="customPrompt"
                            rows="6"
                            className="w-full p-3 bg-gray-700 rounded-md border border-gray-600 focus:ring-2 focus:ring-blue-500"
                            placeholder="Descreva detalhadamente a imagem que você quer gerar..."
                            value={customPrompt}
                            onChange={(e) => setCustomPrompt(e.target.value)}
                        />
                    </div>
                )}

                {useSavedScript && (
                    <div className="mb-4">
                        <label htmlFor="savedScript" className="block text-lg font-medium mb-2">Roteiro Salvo</label>
                        <select
                            id="savedScript"
                            className="w-full p-3 bg-gray-700 rounded-md border border-gray-600 focus:ring-2 focus:ring-blue-500"
                            value={selectedSavedScript}
                            onChange={(e) => setSelectedSavedScript(e.target.value)}
                        >
                            <option value="">Selecione um roteiro salvo...</option>
                            {savedScripts.map((script) => (
                                <option key={script.id} value={script.id}>
                                    {script.title}
                                </option>
                            ))}
                        </select>
                        {selectedSavedScript && (
                            <div className="mt-2 p-3 bg-gray-900 rounded border text-sm text-gray-300 max-h-32 overflow-y-auto">
                                {savedScripts.find(s => s.id === selectedSavedScript)?.content.substring(0, 200)}...
                            </div>
                        )}
                    </div>
                )}

                {usePastedText && (
                    <div className="mb-4">
                        <label htmlFor="pastedText" className="block text-lg font-medium mb-2">Texto Colado</label>
                        <textarea
                            id="pastedText"
                            rows="8"
                            className="w-full p-3 bg-gray-700 rounded-md border border-gray-600 focus:ring-2 focus:ring-blue-500"
                            placeholder="Cole aqui o texto que você quer usar para gerar as imagens..."
                            value={pastedText}
                            onChange={(e) => setPastedText(e.target.value)}
                        />
                    </div>
                )}

                {!useCustomPrompt && !useSavedScript && !usePastedText && (
                    <div className="mb-4">
                        <label htmlFor="script" className="block text-lg font-medium mb-2">Roteiro Manual</label>
                        <textarea
                            id="script"
                            rows="10"
                            className="w-full p-3 bg-gray-700 rounded-md border border-gray-600 focus:ring-2 focus:ring-blue-500"
                            placeholder="Digite ou cole o roteiro aqui..."
                            value={script}
                            onChange={(e) => setScript(e.target.value)}
                        />
                    </div>
                )}

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                    <div>
                        <label htmlFor="provider" className="block text-lg font-medium mb-2">Provedor de IA</label>
                        <select 
                            id="provider"
                            className="w-full p-3 bg-gray-700 rounded-md border border-gray-600 focus:ring-2 focus:ring-blue-500"
                            value={provider}
                            onChange={(e) => setProvider(e.target.value)}
                        >
                            <option value="together">Together.ai (GPT)</option>
                            <option value="gemini">Google Gemini</option>
                            <option value="gemini-imagen3">Google Imagen 3 (ImageFX) - Novo!</option>
                            <option value="gemini-imagen3-rohitaryal">Google Imagen 3 (ImageFX-api by rohitaryal) - Com suporte a cookies</option>
                            <option value="gemini-reddit">Google Gemini (via Reddit - Sem API Key)</option>
                            <option value="pollinations">Pollinations.ai (Gratuito)</option>
                        </select>
                        {provider === 'pollinations' && (
                            <div className="mt-3 space-y-3">
                                <div className="p-3 bg-green-900/30 border border-green-600 rounded-lg">
                                    <h4 className="text-green-400 font-semibold mb-2">🌟 Pollinations.ai - Vantagens</h4>
                                    <ul className="text-sm text-green-300 space-y-1">
                                        <li>• ✅ Completamente gratuito</li>
                                        <li>• 🚀 Sem necessidade de API key</li>
                                        <li>• 🎨 Múltiplos modelos de IA (GPT, Flux)</li>
                                        <li>• ⚡ Geração rápida e de alta qualidade</li>
                                        <li>• 🔄 Sistema de fallback inteligente</li>
                                    </ul>
                                </div>
                                
                                <div className="p-3 bg-blue-900/30 border border-blue-600 rounded-lg">
                                    <label htmlFor="pollinationsModel" className="block text-blue-400 font-semibold mb-2">🤖 Modelo de IA</label>
                                    <select 
                                        id="pollinationsModel"
                                        className="w-full p-2 bg-gray-700 rounded-md border border-gray-600 focus:ring-2 focus:ring-blue-500 text-sm"
                                        value={pollinationsModel}
                                        onChange={(e) => setPollinationsModel(e.target.value)}
                                    >
                                        <option value="gpt">🖼️ GPT Image - Melhor para realismo</option>
                                        <option value="flux">🎨 Flux - Melhor para arte e criatividade</option>
                                    </select>
                                    <p className="text-xs text-blue-300 mt-1">
                                        {pollinationsModel === 'flux' ? 
                                            '✨ Flux: Ideal para arte digital, fantasia e estilos criativos' : 
                                            '📸 GPT Image: Ideal para fotos realistas e cenários do mundo real'
                                        }
                                    </p>
                                </div>
                            </div>
                        )}
                        {provider === 'gemini-imagen3' && (
                            <div className="mt-4 space-y-4">
                                <div className="p-3 bg-indigo-900/30 border border-indigo-600 rounded-lg">
                                    <h4 className="text-indigo-400 font-semibold mb-2">🚀 Google Imagen 3 (ImageFX) - Vantagens</h4>
                                    <ul className="text-sm text-indigo-300 space-y-1">
                                        <li>• ✅ Última tecnologia de geração de imagens do Google</li>
                                        <li>• 🎨 Qualidade superior com o modelo Imagen 3</li>
                                        <li>• 🚀 Modo gratuito disponível</li>
                                        <li>• 🔗 Acesso via API do Gemini</li>
                                        <li>• 🔄 Sistema de fallback automático</li>
                                        <li>• 🍪 Suporte para cookies do Google (opcional)</li>
                                    </ul>
                                </div>
                                
                                <div>
                                    <label className="block text-sm font-medium text-gray-300 mb-2">Cookies do Google (Opcional)</label>
                                    <textarea 
                                        id="googleCookies"
                                        className="w-full p-3 bg-gray-700 rounded-md border border-gray-600 focus:ring-2 focus:ring-blue-500 h-32"
                                        placeholder="Cole aqui os cookies do Google para autenticação...\n\nExemplo:\n__Secure-1PSID=...; __Secure-1PSIDTS=...; __Secure-1PSIDCC=..." 
                                        value={googleCookies}
                                        onChange={(e) => setGoogleCookies(e.target.value)}
                                    />
                                    <p className="text-xs text-gray-400 mt-1">Para obter os cookies, acesse o site do Google Imagen 3, faça login e copie os cookies usando a ferramenta de desenvolvedor do navegador.</p>
                                </div>
                                
                                <div>
                                    <label className="block text-sm font-medium text-gray-300 mb-2">Estilo da Imagem</label>
                                    <select 
                                        id="style"
                                        className="w-full p-3 bg-gray-700 rounded-md border border-gray-600 focus:ring-2 focus:ring-blue-500"
                                        value={style}
                                        onChange={(e) => setStyle(e.target.value)}
                                    >
                                        <option value="">Padrão</option>
                                        <option value="fotorealista">Fotorealista</option>
                                        <option value="desenho">Desenho</option>
                                        <option value="pintura">Pintura</option>
                                        <option value="anime">Anime</option>
                                        <option value="cartoon">Cartoon</option>
                                        <option value="pixel-art">Pixel Art</option>
                                        <option value="cyberpunk">Cyberpunk</option>
                                        <option value="steampunk">Steampunk</option>
                                        <option value="fantasia">Fantasia</option>
                                        <option value="ficcao-cientifica">Ficção Científica</option>
                                        <option value="abstracto">Abstracto</option>
                                    </select>
                                </div>
                            </div>
                        )}
                        {provider === 'gemini-imagen3-rohitaryal' && (
                            <div className="mt-4 space-y-4">
                                <div className="p-3 bg-indigo-900/30 border border-indigo-600 rounded-lg">
                                    <h4 className="text-indigo-400 font-semibold mb-2">🚀 Google Imagen 3 (ImageFX-api by rohitaryal) - Vantagens</h4>
                                    <ul className="text-sm text-indigo-300 space-y-1">
                                        <li>• ✅ Implementação baseada no repositório GitHub rohitaryal/imageFX-api</li>
                                        <li>• 🍪 Suporte completo para cookies do Google</li>
                                        <li>• 🎨 Qualidade superior com o modelo Imagen 3</li>
                                        <li>• 🔄 Sistema de fallback automático</li>
                                        <li>• ⚡ Geração rápida de imagens em alta resolução</li>
                                    </ul>
                                </div>
                                
                                {/* Mensagem de aviso sobre prompt necessário */}
                                {(!script && !customPrompt && !pastedText && !selectedSavedScript) && (
                                    <div className="p-3 bg-yellow-900/30 border border-yellow-600 rounded-lg">
                                        <h4 className="text-yellow-400 font-semibold mb-2">⚠️ Aviso Importante</h4>
                                        <p className="text-sm text-yellow-300">
                                            O botão "Gerar Imagem" permanecerá desativado até que você preencha um dos campos de prompt (Roteiro Manual, Prompt Personalizado, Texto Colado ou Roteiro Salvo).
                                        </p>
                                    </div>
                                )}
                                <div>
                                    <label className="block text-sm font-medium text-gray-300 mb-2">Cookies do Google (Opcional)</label>
                                    <textarea 
                                        id="googleCookies"
                                        className="w-full p-3 bg-gray-700 rounded-md border border-gray-600 focus:ring-2 focus:ring-blue-500 h-32"
                                        placeholder="Cole aqui os cookies do Google para autenticação...\n\nExemplo:\n__Secure-1PSID=...; __Secure-1PSIDTS=...; __Secure-1PSIDCC=..." 
                                        value={googleCookies}
                                        onChange={(e) => setGoogleCookies(e.target.value)}
                                    />
                                    <p className="text-xs text-gray-400 mt-1">Para obter os cookies, acesse o site do Google Imagen 3, faça login e copie os cookies usando a ferramenta de desenvolvedor do navegador.</p>
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-300 mb-2">Estilo da Imagem</label>
                                    <select 
                                        id="style"
                                        className="w-full p-3 bg-gray-700 rounded-md border border-gray-600 focus:ring-2 focus:ring-blue-500"
                                        value={style}
                                        onChange={(e) => setStyle(e.target.value)}
                                    >
                                        <option value="">Padrão</option>
                                        <option value="fotorealista">Fotorealista</option>
                                        <option value="desenho">Desenho</option>
                                        <option value="pintura">Pintura</option>
                                        <option value="anime">Anime</option>
                                        <option value="cartoon">Cartoon</option>
                                        <option value="pixel-art">Pixel Art</option>
                                        <option value="cyberpunk">Cyberpunk</option>
                                        <option value="steampunk">Steampunk</option>
                                        <option value="fantasia">Fantasia</option>
                                        <option value="ficcao-cientifica">Ficção Científica</option>
                                        <option value="abstracto">Abstracto</option>
                                    </select>
                                </div>
                            </div>
                        )}
                        {provider === 'gemini-reddit' && (
                            <div className="mt-3 space-y-3">
                                <div className="p-3 bg-purple-900/30 border border-purple-600 rounded-lg">
                                    <h4 className="text-purple-400 font-semibold mb-2">🔮 Gemini via Reddit - Vantagens</h4>
                                    <ul className="text-sm text-purple-300 space-y-1">
                                        <li>• ✅ Acesso ao Google Gemini 2.5 Flash</li>
                                        <li>• 🚀 Sem necessidade de API key</li>
                                        <li>• 🎨 Alta qualidade de imagem</li>
                                        <li>• 🔗 Método alternativo via endpoint do Reddit</li>
                                        <li>• 🔄 Sistema de retry automático</li>
                                    </ul>
                                </div>
                            </div>
                        )}
                    </div>

                    <div>
                        <label htmlFor="style" className="block text-lg font-medium mb-2">Estilo da Imagem</label>
                        <select 
                            id="style"
                            className="w-full p-3 bg-gray-700 rounded-md border border-gray-600 focus:ring-2 focus:ring-blue-500"
                            value={style}
                            onChange={(e) => setStyle(e.target.value)}
                        >
                            <option value="cinematic, high detail, 4k">Cinemático</option>
                            <option value="photorealistic, sharp focus, f/1.8">Fotorealista</option>
                            <option value="fantasy, epic, detailed, vibrant colors">Fantasia</option>
                            <option value="documentary, natural lighting, realistic">Documental</option>
                            <option value="anime, ghibli style, detailed background">Anime (Ghibli)</option>
                            {provider === 'pollinations' && (
                                <>
                                    <option value="digital art, trending on artstation, highly detailed">Arte Digital</option>
                                    <option value="oil painting, classical art, masterpiece">Pintura Clássica</option>
                                    <option value="cyberpunk, neon lights, futuristic, sci-fi">Cyberpunk</option>
                                    <option value="watercolor, soft colors, artistic, painting">Aquarela</option>
                                    <option value="minimalist, clean, simple, modern design">Minimalista</option>
                                </>
                            )}
                        </select>
                        {provider === 'pollinations' && (
                            <p className="text-sm text-green-400 mt-1">✨ Estilos otimizados para Pollinations.ai</p>
                        )}
                    </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                    <div>
                        <label htmlFor="format" className="block text-lg font-medium mb-2">Formato da Imagem</label>
                        <select 
                            id="format"
                            className="w-full p-3 bg-gray-700 rounded-md border border-gray-600 focus:ring-2 focus:ring-blue-500"
                            value={format}
                            onChange={(e) => setFormat(e.target.value)}
                        >
                            <option value="1024x1024">Quadrado (1024x1024)</option>
                            <option value="1024x768">Paisagem (1024x768)</option>
                            <option value="768x1024">Retrato (768x1024)</option>
                            <option value="1280x720">HD Paisagem (1280x720)</option>
                            <option value="720x1280">HD Retrato (720x1280)</option>
                        </select>
                    </div>

                    <div>
                        <label htmlFor="quality" className="block text-lg font-medium mb-2">Qualidade</label>
                        <select 
                            id="quality"
                            className="w-full p-3 bg-gray-700 rounded-md border border-gray-600 focus:ring-2 focus:ring-blue-500"
                            value={quality}
                            onChange={(e) => setQuality(e.target.value)}
                        >
                            <option value="standard">Padrão</option>
                            <option value="hd">Alta Definição</option>
                        </select>
                    </div>
                </div>

                {/* Controles de geração em lote */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                    <div>
                        <label htmlFor="batchCount" className="block text-lg font-medium mb-2">Quantidade de Imagens</label>
                        <select 
                            id="batchCount"
                            className="w-full p-3 bg-gray-700 rounded-md border border-gray-600 focus:ring-2 focus:ring-blue-500"
                            value={batchCount}
                            onChange={(e) => setBatchCount(parseInt(e.target.value))}
                        >
                            <option value={1}>1 imagem</option>
                            <option value={2}>2 imagens</option>
                            <option value={3}>3 imagens</option>
                            <option value={4}>4 imagens</option>
                            <option value={5}>5 imagens</option>
                            <option value={10}>10 imagens</option>
                        </select>
                    </div>

                    <div>
                        <label htmlFor="delay" className="block text-lg font-medium mb-2">Delay entre Gerações (segundos)</label>
                        <select 
                            id="delay"
                            className="w-full p-3 bg-gray-700 rounded-md border border-gray-600 focus:ring-2 focus:ring-blue-500"
                            value={delayBetweenImages}
                            onChange={(e) => setDelayBetweenImages(parseInt(e.target.value))}
                            disabled={batchCount <= 1}
                        >
                            <option value={1}>1 segundo</option>
                            <option value={3}>3 segundos</option>
                            <option value={5}>5 segundos</option>
                            <option value={10}>10 segundos</option>
                            <option value={15}>15 segundos</option>
                            <option value={30}>30 segundos</option>
                        </select>
                        {batchCount <= 1 && (
                            <p className="text-sm text-gray-400 mt-1">💡 Disponível apenas para múltiplas imagens</p>
                        )}
                    </div>
                </div>

                <div className="space-y-3">
                    <button 
                        onClick={handleGenerateImages}
                        disabled={isLoading || isGeneratingBatch || (!script && !customPrompt && !pastedText && !selectedSavedScript) || (!apiKey && provider !== 'pollinations' && provider !== 'gemini-reddit' && provider !== 'gemini-imagen3' && provider !== 'gemini-imagen3-rohitaryal')}
                        className="w-full py-3 px-4 bg-blue-600 hover:bg-blue-700 rounded-md text-lg font-semibold disabled:bg-gray-500 disabled:cursor-not-allowed transition-colors"
                    >
                        {isGeneratingBatch ? 
                            `Gerando ${currentBatch}/${batchCount} imagens...` : 
                            isLoading ? 'Gerando Imagem...' : 
                            `Gerar ${batchCount > 1 ? `${batchCount} Imagens` : 'Imagem'}`
                        }
                    </button>
                    
                    {(isLoading || isGeneratingBatch) && (
                        <button 
                            onClick={handleCancelGeneration}
                            className="w-full py-2 px-4 bg-red-600 hover:bg-red-700 rounded-md text-sm font-semibold transition-colors"
                        >
                            ❌ Cancelar Geração
                        </button>
                    )}
                </div>

                {/* Barra de progresso para geração em lote */}
                {isGeneratingBatch && (
                    <div className="mt-4">
                        <div className="flex justify-between text-sm text-gray-300 mb-2">
                            <span>Progresso da Geração</span>
                            <span>{currentBatch}/{batchCount}</span>
                        </div>
                        <div className="w-full bg-gray-700 rounded-full h-2">
                            <div 
                                className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                                style={{ width: `${(currentBatch / batchCount) * 100}%` }}
                            ></div>
                        </div>
                    </div>
                )}

                {error && <p className="text-red-400 mt-4">{error}</p>}
            </div>

            {images.length > 0 && (
                <div className="mt-8">
                    <div className="flex justify-between items-center mb-4">
                        <h2 className="text-2xl font-bold">Imagens Geradas ({images.length})</h2>
                        <button
                            onClick={downloadAllImages}
                            className="px-4 py-2 bg-green-600 hover:bg-green-700 rounded-md text-sm font-semibold transition-colors"
                        >
                            📥 Baixar Todas
                        </button>
                    </div>
                    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                        {images.map((image, index) => (
                            <div key={index} className="bg-gray-800 rounded-lg overflow-hidden shadow-lg group relative">
                                <img 
                                    src={image.url} 
                                    alt={`Imagem gerada ${index + 1}`} 
                                    className="w-full h-auto object-cover" 
                                />
                                <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-50 transition-all duration-300 flex items-center justify-center">
                                    <button
                                        onClick={() => downloadImage(image.url, index)}
                                        className="opacity-0 group-hover:opacity-100 px-3 py-2 bg-blue-600 hover:bg-blue-700 rounded-md text-sm font-semibold transition-all duration-300 transform scale-90 group-hover:scale-100"
                                    >
                                        📥 Baixar
                                    </button>
                                </div>
                                <div className="p-2 text-center text-sm text-gray-400">
                                    Imagem {index + 1}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default ImageGeneration;