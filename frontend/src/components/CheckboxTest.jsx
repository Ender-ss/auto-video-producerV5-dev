import React, { useState } from 'react'

const CheckboxTest = () => {
  const [formData, setFormData] = useState({
    config: {
      tts: {
        enabled: true,
        provider: 'openai',
        voice: 'alloy',
        language: 'pt-BR',
        speed: 1.0,
        pitch: 1.0
      },
      extraction: { enabled: true },
      titles: { enabled: true },
      premises: { enabled: true },
      scripts: { enabled: true },
      images: { enabled: true },
      video: { enabled: true }
    }
  })

  const [testResult, setTestResult] = useState(null)

  const handleInputChange = (path, value) => {
    console.log('🔧 handleInputChange chamado:', { path, value })
    
    setFormData(prevData => {
      const newData = { ...prevData }
      const keys = (path || '').split('.')
      let current = newData
      
      for (let i = 0; i < keys.length - 1; i++) {
        if (!current[keys[i]]) {
          current[keys[i]] = {}
        }
        current = current[keys[i]]
      }
      
      current[keys[keys.length - 1]] = value
      
      console.log('📊 Novo estado do formulário:', newData)
      return newData
    })
  }

  const testConfiguration = async () => {
    try {
      console.log('🧪 Enviando configuração para teste:', formData)
      
      const response = await fetch('/api/test-config', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      })
      
      const result = await response.json()
      console.log('📋 Resultado do teste:', result)
      setTestResult(result)
      
    } catch (error) {
      console.error('❌ Erro no teste:', error)
      setTestResult({ success: false, error: error.message })
    }
  }

  return (
    <div className="p-8 bg-gray-900 min-h-screen">
      <h1 className="text-white text-2xl mb-6">Teste de Checkboxes</h1>
      
      <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
        <h4 className="text-lg font-medium text-white mb-3">Controle de Etapas</h4>
        <div className="grid grid-cols-2 gap-4">
          {[
            { key: 'extraction', label: 'Extração' },
            { key: 'titles', label: 'Títulos' },
            { key: 'premises', label: 'Premissas' },
            { key: 'scripts', label: 'Roteiros' },
            { key: 'tts', label: 'TTS' },
            { key: 'images', label: 'Imagens' },
            { key: 'video', label: 'Vídeo' }
          ].map((step) => (
            <label key={step.key} className="flex items-center space-x-2">
              <input
                type="checkbox"
                checked={formData.config[step.key].enabled}
                onChange={(e) => handleInputChange(`config.${step.key}.enabled`, e.target.checked)}
                className="rounded border-gray-600 bg-gray-700 text-purple-600"
              />
              <span className="text-sm text-gray-300">{step.label}</span>
            </label>
          ))}
        </div>
      </div>

      <div className="mt-6 bg-gray-800 rounded-lg p-4 border border-gray-700">
        <h4 className="text-lg font-medium text-white mb-3">Estado Atual</h4>
        <pre className="text-green-400 text-sm overflow-auto">
          {JSON.stringify(formData, null, 2)}
        </pre>
        
        <div className="mt-6">
          <button 
            onClick={testConfiguration}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
          >
            🧪 Testar Configuração
          </button>
        </div>
        
        {testResult && (
          <div className="mt-4 p-4 border rounded">
            <h3 className="font-bold mb-2">Resultado do Teste:</h3>
            <pre className="bg-gray-100 p-2 rounded text-sm overflow-auto">
              {JSON.stringify(testResult, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  )
}

export default CheckboxTest