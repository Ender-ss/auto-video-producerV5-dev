# -*- coding: utf-8 -*-
"""
🎯 Sistema de Cache de Premissas

Este módulo implementa um sistema de cache para evitar a regeneração de premissas
idênticas, melhorando a performance e reduzindo custos de API.

Autor: Sistema de IA
Data: 2024
"""

import hashlib
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from pathlib import Path

class PremiseCache:
    """
    Sistema de cache para premissas geradas.
    
    Armazena premissas baseadas em hash do título, configurações e prompt,
    permitindo reutilização quando os mesmos parâmetros são usados.
    """
    
    def __init__(self, cache_dir: str = None, max_age_days: int = 30):
        """
        Inicializar o sistema de cache.
        
        Args:
            cache_dir: Diretório para armazenar o cache (padrão: backend/cache/premises)
            max_age_days: Idade máxima do cache em dias (padrão: 30)
        """
        if cache_dir is None:
            # Usar diretório padrão relativo ao backend
            backend_dir = Path(__file__).parent.parent
            cache_dir = backend_dir / "cache" / "premises"
        
        self.cache_dir = Path(cache_dir)
        self.max_age_days = max_age_days
        
        # Criar diretório se não existir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Arquivo de índice para metadados
        self.index_file = self.cache_dir / "index.json"
        self._load_index()
    
    def _load_index(self):
        """Carregar índice de cache."""
        try:
            if self.index_file.exists():
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    self.index = json.load(f)
            else:
                self.index = {}
        except Exception:
            self.index = {}
    
    def _save_index(self):
        """Salvar índice de cache."""
        try:
            with open(self.index_file, 'w', encoding='utf-8') as f:
                json.dump(self.index, f, indent=2, ensure_ascii=False)
        except Exception:
            pass  # Falha silenciosa para não quebrar o fluxo
    
    def _generate_cache_key(self, title: str, config: Dict[str, Any], 
                           prompt_source: str, instructions: str) -> str:
        """
        Gerar chave única para o cache baseada nos parâmetros.
        
        Args:
            title: Título do vídeo
            config: Configurações da premissa
            prompt_source: Origem do prompt (custom_user, agent_specialized, system_default)
            instructions: Instruções/prompt usado
            
        Returns:
            Hash MD5 como chave do cache
        """
        # Criar string única com todos os parâmetros relevantes
        cache_data = {
            'title': title.lower().strip(),
            'word_count': config.get('word_count', 200),
            'style': config.get('style', 'educational'),
            'prompt_source': prompt_source,
            'instructions_hash': hashlib.md5(instructions.encode('utf-8')).hexdigest()[:16]
        }
        
        # Incluir informações do agente se for especializado
        if prompt_source == 'agent_specialized':
            agent_info = config.get('agent_info', {})
            cache_data['agent_type'] = agent_info.get('type', '')
            cache_data['agent_name'] = agent_info.get('name', '')
        
        # Gerar hash da combinação
        cache_string = json.dumps(cache_data, sort_keys=True)
        return hashlib.md5(cache_string.encode('utf-8')).hexdigest()
    
    def get_cached_premise(self, title: str, config: Dict[str, Any], 
                          prompt_source: str, instructions: str) -> Optional[Dict[str, Any]]:
        """
        Buscar premissa no cache.
        
        Args:
            title: Título do vídeo
            config: Configurações da premissa
            prompt_source: Origem do prompt
            instructions: Instruções/prompt usado
            
        Returns:
            Dados da premissa se encontrada e válida, None caso contrário
        """
        try:
            cache_key = self._generate_cache_key(title, config, prompt_source, instructions)
            
            # Verificar se existe no índice
            if cache_key not in self.index:
                return None
            
            cache_info = self.index[cache_key]
            
            # Verificar se não expirou
            created_date = datetime.fromisoformat(cache_info['created_at'])
            if datetime.now() - created_date > timedelta(days=self.max_age_days):
                # Cache expirado, remover
                self._remove_cache_entry(cache_key)
                return None
            
            # Carregar dados do arquivo
            cache_file = self.cache_dir / f"{cache_key}.json"
            if not cache_file.exists():
                # Arquivo não existe, remover do índice
                self._remove_cache_entry(cache_key)
                return None
            
            with open(cache_file, 'r', encoding='utf-8') as f:
                cached_data = json.load(f)
            
            # Atualizar último acesso
            self.index[cache_key]['last_accessed'] = datetime.now().isoformat()
            self._save_index()
            
            return cached_data
            
        except Exception:
            return None  # Falha silenciosa
    
    def cache_premise(self, title: str, config: Dict[str, Any], 
                     prompt_source: str, instructions: str, 
                     premise_data: Dict[str, Any]) -> bool:
        """
        Armazenar premissa no cache.
        
        Args:
            title: Título do vídeo
            config: Configurações da premissa
            prompt_source: Origem do prompt
            instructions: Instruções/prompt usado
            premise_data: Dados da premissa gerada
            
        Returns:
            True se armazenado com sucesso, False caso contrário
        """
        try:
            cache_key = self._generate_cache_key(title, config, prompt_source, instructions)
            
            # Preparar dados para cache
            cache_data = {
                'title': title,
                'word_count': premise_data.get('word_count', 0),
                'provider_used': premise_data.get('provider_used', ''),
                'style': premise_data.get('style', ''),
                'prompt_source': prompt_source,
                'cached_at': datetime.now().isoformat(),
                'config_used': {
                    'word_count': config.get('word_count', 200),
                    'style': config.get('style', 'educational')
                }
            }
            
            # Salvar arquivo de cache
            cache_file = self.cache_dir / f"{cache_key}.json"
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)
            
            # Atualizar índice
            self.index[cache_key] = {
                'title': title,
                'created_at': datetime.now().isoformat(),
                'last_accessed': datetime.now().isoformat(),
                'word_count': cache_data['word_count'],
                'style': cache_data['style'],
                'prompt_source': prompt_source
            }
            
            self._save_index()
            return True
            
        except Exception:
            return False  # Falha silenciosa
    
    def _remove_cache_entry(self, cache_key: str):
        """Remover entrada do cache."""
        try:
            # Remover arquivo
            cache_file = self.cache_dir / f"{cache_key}.json"
            if cache_file.exists():
                cache_file.unlink()
            
            # Remover do índice
            if cache_key in self.index:
                del self.index[cache_key]
                self._save_index()
        except Exception:
            pass
    
    def cleanup_expired(self) -> int:
        """
        Limpar entradas expiradas do cache.
        
        Returns:
            Número de entradas removidas
        """
        removed_count = 0
        expired_keys = []
        
        try:
            for cache_key, cache_info in self.index.items():
                created_date = datetime.fromisoformat(cache_info['created_at'])
                if datetime.now() - created_date > timedelta(days=self.max_age_days):
                    expired_keys.append(cache_key)
            
            for cache_key in expired_keys:
                self._remove_cache_entry(cache_key)
                removed_count += 1
                
        except Exception:
            pass
        
        return removed_count
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Obter estatísticas do cache.
        
        Returns:
            Dicionário com estatísticas do cache
        """
        try:
            total_entries = len(self.index)
            total_size = 0
            
            # Calcular tamanho total
            for cache_file in self.cache_dir.glob("*.json"):
                if cache_file.name != "index.json":
                    total_size += cache_file.stat().st_size
            
            # Contar por origem de prompt
            by_source = {}
            for cache_info in self.index.values():
                source = cache_info.get('prompt_source', 'unknown')
                by_source[source] = by_source.get(source, 0) + 1
            
            return {
                'total_entries': total_entries,
                'total_size_bytes': total_size,
                'total_size_mb': round(total_size / (1024 * 1024), 2),
                'by_prompt_source': by_source,
                'cache_dir': str(self.cache_dir),
                'max_age_days': self.max_age_days
            }
            
        except Exception:
            return {
                'total_entries': 0,
                'total_size_bytes': 0,
                'total_size_mb': 0,
                'by_prompt_source': {},
                'cache_dir': str(self.cache_dir),
                'max_age_days': self.max_age_days
            }
    
    def clear_cache(self) -> bool:
        """
        Limpar todo o cache.
        
        Returns:
            True se limpeza foi bem-sucedida
        """
        try:
            # Remover todos os arquivos de cache
            for cache_file in self.cache_dir.glob("*.json"):
                cache_file.unlink()
            
            # Resetar índice
            self.index = {}
            self._save_index()
            
            return True
            
        except Exception:
            return False