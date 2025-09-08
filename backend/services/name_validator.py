# -*- coding: utf-8 -*-
"""
🚫 Sistema de Validação de Nomes

Este módulo implementa um sistema para detectar e evitar nomes repetidos
nas premissas geradas, garantindo diversidade de personagens.

Autor: Sistema de IA
Data: 2024
"""

import re
import json
import os
from typing import List, Dict, Set, Optional
from pathlib import Path
from datetime import datetime, timedelta

class NameValidator:
    """
    Sistema de validação de nomes para evitar repetições.
    
    Detecta nomes proibidos, mantém histórico de nomes usados
    e sugere alternativas quando necessário.
    """
    
    def __init__(self, history_file: str = None, max_history_days: int = 30):
        """
        Inicializar o validador de nomes.
        
        Args:
            history_file: Arquivo para armazenar histórico de nomes
            max_history_days: Dias para manter histórico de nomes
        """
        if history_file is None:
            backend_dir = Path(__file__).parent.parent
            cache_dir = backend_dir / "cache" / "names"
            cache_dir.mkdir(parents=True, exist_ok=True)
            history_file = cache_dir / "name_history.json"
        
        self.history_file = Path(history_file)
        self.max_history_days = max_history_days
        
        # Nomes proibidos (sempre bloqueados)
        self.forbidden_names = {
            'blackwood', 'arthur blackwood', 'damien blackwood', 'lilith blackwood',
            'johnson', 'smith', 'williams', 'brown', 'jones', 'davis',
            'miller', 'wilson', 'moore', 'taylor', 'anderson', 'thomas'
        }
        
        # Padrões de nomes genéricos
        self.generic_patterns = [
            r'\b(mr|mrs|miss|ms)\.?\s+[a-z]+\b',  # Mr. Smith, Mrs. Johnson
            r'\b[a-z]+\s+(ceo|boss|manager|executive)\b',  # John CEO
            r'\b(the|a)\s+(rich|wealthy|millionaire)\s+(man|woman|person)\b'  # The rich man
        ]
        
        # Carregar histórico
        self.name_history = self._load_history()
    
    def _load_history(self) -> Dict[str, List[Dict]]:
        """Carregar histórico de nomes usados."""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
                    # Limpar entradas antigas
                    return self._clean_old_entries(history)
            return {}
        except Exception:
            return {}
    
    def _save_history(self):
        """Salvar histórico de nomes."""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.name_history, f, indent=2, ensure_ascii=False)
        except Exception:
            pass  # Falha silenciosa
    
    def _clean_old_entries(self, history: Dict) -> Dict:
        """Remover entradas antigas do histórico."""
        cutoff_date = datetime.now() - timedelta(days=self.max_history_days)
        cleaned_history = {}
        
        for name, entries in history.items():
            valid_entries = []
            for entry in entries:
                try:
                    entry_date = datetime.fromisoformat(entry['timestamp'])
                    if entry_date > cutoff_date:
                        valid_entries.append(entry)
                except:
                    continue
            
            if valid_entries:
                cleaned_history[name] = valid_entries
        
        return cleaned_history
    
    def extract_names_from_text(self, text: str) -> Set[str]:
        """Extrair nomes de personagens do texto."""
        names = set()
        
        # Padrões para detectar nomes
        patterns = [
            r'\b([A-Z][a-z]+)\s+([A-Z][a-z]+)\b',  # Nome Sobrenome
            r'\b([A-Z][a-z]{2,})\b(?=\s*[,.]|\s+[a-z])',  # Nome seguido de vírgula ou palavra minúscula
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if isinstance(match, tuple):
                    full_name = ' '.join(match).strip()
                else:
                    full_name = match.strip()
                
                # Filtrar nomes válidos (não são palavras comuns)
                if self._is_valid_name(full_name):
                    names.add(full_name.lower())
        
        return names
    
    def _is_valid_name(self, name: str) -> bool:
        """Verificar se é um nome válido (não palavra comum)."""
        name_lower = name.lower()
        
        # Palavras comuns que não são nomes
        common_words = {
            'the', 'and', 'but', 'for', 'with', 'from', 'into', 'during',
            'before', 'after', 'above', 'below', 'between', 'through',
            'casa', 'vida', 'mundo', 'tempo', 'pessoa', 'lugar', 'coisa',
            'trabalho', 'empresa', 'dinheiro', 'história', 'problema'
        }
        
        # Verificar se não é palavra comum
        if name_lower in common_words:
            return False
        
        # Verificar se tem pelo menos 3 caracteres
        if len(name) < 3:
            return False
        
        # Verificar se contém apenas letras e espaços
        if not re.match(r'^[a-zA-ZÀ-ÿ\s]+$', name):
            return False
        
        return True
    
    def is_name_forbidden(self, name: str) -> bool:
        """Verificar se o nome está na lista de proibidos."""
        name_lower = name.lower().strip()
        
        # Verificar lista de nomes proibidos
        if name_lower in self.forbidden_names:
            return True
        
        # Verificar padrões genéricos
        for pattern in self.generic_patterns:
            if re.search(pattern, name_lower, re.IGNORECASE):
                return True
        
        return False
    
    def is_name_overused(self, name: str, threshold: int = 3) -> bool:
        """Verificar se o nome foi usado muitas vezes recentemente."""
        name_lower = name.lower().strip()
        
        if name_lower not in self.name_history:
            return False
        
        # Contar usos recentes (últimos 7 dias)
        recent_cutoff = datetime.now() - timedelta(days=7)
        recent_uses = 0
        
        for entry in self.name_history[name_lower]:
            try:
                entry_date = datetime.fromisoformat(entry['timestamp'])
                if entry_date > recent_cutoff:
                    recent_uses += 1
            except:
                continue
        
        return recent_uses >= threshold
    
    def validate_premise(self, premise_text: str, agent_context: str = None) -> Dict[str, any]:
        """Validar premissa quanto a nomes repetidos ou proibidos."""
        names_found = self.extract_names_from_text(premise_text)
        
        validation_result = {
            'is_valid': True,
            'issues': [],
            'names_found': list(names_found),
            'forbidden_names': [],
            'overused_names': [],
            'suggestions': []
        }
        
        # Nomes proibidos específicos por agente
        if agent_context == 'millionaire_stories':
            agent_forbidden = {'arthur', 'blackwood', 'damien', 'lilith'}
        else:
            agent_forbidden = self.forbidden_names
        
        for name in names_found:
            name_lower = name.lower().strip()
            
            # Verificar se é proibido (considerando contexto do agente)
            if any(forbidden in name_lower for forbidden in agent_forbidden):
                validation_result['is_valid'] = False
                validation_result['forbidden_names'].append(name)
                validation_result['issues'].append(f"Nome proibido detectado: {name}")
            
            # Verificar se está sendo usado demais
            elif self.is_name_overused(name):
                validation_result['is_valid'] = False
                validation_result['overused_names'].append(name)
                validation_result['issues'].append(f"Nome usado recentemente: {name}")
        
        # Gerar sugestões se há problemas
        if not validation_result['is_valid']:
            validation_result['suggestions'] = self._generate_name_suggestions(
                validation_result['forbidden_names'] + validation_result['overused_names']
            )
        
        return validation_result
    
    def _generate_name_suggestions(self, problematic_names: List[str]) -> List[str]:
        """Gerar sugestões de nomes alternativos."""
        suggestions = []
        
        # Nomes brasileiros alternativos
        male_names = [
            'Rafael Mendes', 'Carlos Silva', 'Bruno Santos', 'Diego Costa',
            'Felipe Oliveira', 'Gustavo Lima', 'Henrique Alves', 'Igor Pereira',
            'João Rodrigues', 'Leonardo Ferreira', 'Marcelo Ribeiro', 'Nicolas Barbosa'
        ]
        
        female_names = [
            'Ana Clara', 'Beatriz Santos', 'Camila Oliveira', 'Daniela Costa',
            'Eduarda Silva', 'Fernanda Lima', 'Gabriela Alves', 'Helena Pereira',
            'Isabela Rodrigues', 'Juliana Ferreira', 'Larissa Ribeiro', 'Mariana Barbosa'
        ]
        
        # Selecionar sugestões que não estão no histórico recente
        all_suggestions = male_names + female_names
        
        for suggestion in all_suggestions:
            if not self.is_name_overused(suggestion, threshold=1):
                suggestions.append(suggestion)
                if len(suggestions) >= 6:  # Limitar a 6 sugestões
                    break
        
        return suggestions
    
    def record_name_usage(self, name: str, context: str = ""):
        """Registrar uso de um nome no histórico."""
        name_lower = name.lower().strip()
        
        if name_lower not in self.name_history:
            self.name_history[name_lower] = []
        
        # Adicionar nova entrada
        entry = {
            'timestamp': datetime.now().isoformat(),
            'context': context,
            'original_case': name
        }
        
        self.name_history[name_lower].append(entry)
        
        # Manter apenas as últimas 10 entradas por nome
        if len(self.name_history[name_lower]) > 10:
            self.name_history[name_lower] = self.name_history[name_lower][-10:]
        
        self._save_history()
    
    def get_name_statistics(self) -> Dict[str, any]:
        """Obter estatísticas de uso de nomes."""
        total_names = len(self.name_history)
        total_uses = sum(len(entries) for entries in self.name_history.values())
        
        # Nomes mais usados
        most_used = sorted(
            [(name, len(entries)) for name, entries in self.name_history.items()],
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        return {
            'total_unique_names': total_names,
            'total_uses': total_uses,
            'forbidden_names_count': len(self.forbidden_names),
            'most_used_names': most_used,
            'history_file': str(self.history_file)
        }
    
    def clean_premise_text(self, premise_text: str, problematic_names: List[str], 
                          suggestions: List[str]) -> str:
        """Limpar texto da premissa substituindo nomes problemáticos."""
        return self.clean_text_content(premise_text, problematic_names, suggestions)
    
    def clean_text_content(self, text: str, problematic_names: List[str], 
                          suggestions: List[str]) -> str:
        """Limpar qualquer texto (premissa ou script) substituindo nomes problemáticos."""
        cleaned_text = text
        
        # Primeiro, remover todas as ocorrências de nomes proibidos conhecidos
        forbidden_patterns = [
            r'\bArthur\s+Blackwood\b',
            r'\bArthur\b(?=\s+[A-Z][a-z]+)',  # Arthur seguido de qualquer sobrenome
            r'\bBlackwood\b',
            r'\bDamien\s+Blackwood\b',
            r'\bLilith\s+Blackwood\b'
        ]
        
        # Substituir padrões proibidos por nomes alternativos
        replacement_names = [
            'Rafael Mendes', 'Carlos Silva', 'Bruno Santos', 'Diego Costa',
            'Felipe Oliveira', 'Gustavo Lima', 'Henrique Alves', 'Igor Pereira'
        ]
        
        replacement_index = 0
        for pattern in forbidden_patterns:
            matches = re.findall(pattern, cleaned_text, flags=re.IGNORECASE)
            if matches:
                replacement = replacement_names[replacement_index % len(replacement_names)]
                cleaned_text = re.sub(pattern, replacement, cleaned_text, flags=re.IGNORECASE)
                replacement_index += 1
        
        # Depois, substituir nomes problemáticos específicos por sugestões
        for i, problematic_name in enumerate(problematic_names):
            if i < len(suggestions):
                suggestion = suggestions[i]
                # Criar padrão mais robusto para o nome
                pattern = r'\b' + re.escape(problematic_name.replace(' ', r'\s+')) + r'\b'
                cleaned_text = re.sub(pattern, suggestion, cleaned_text, flags=re.IGNORECASE)
        
        return cleaned_text