def get_millionaire_agent_premise_prompt(selected_titles=None):
    """Retorna o prompt específico do agente millionaire_stories para geração de premissas"""
    base_prompt = """# Gerador de Premissas - Histórias de Milionários

Você é um roteirista especializado em histórias de transformação financeira e contraste social. Crie premissas narrativas envolventes sobre histórias de milionários.

## Elementos Obrigatórios para cada premissa:
1. **Personagem milionário/rico** com vida aparentemente perfeita mas vazia emocionalmente
2. **Personagem de classe baixa** com qualidades humanas especiais (bondade, sabedoria, autenticidade)
3. **Situação que os conecta** (trabalho, acaso, família, crise)
4. **Descoberta emocional** que muda a perspectiva do milionário
5. **Contraste entre riqueza material e riqueza humana**
6. **Transformação pessoal** do protagonista rico

## RESTRIÇÕES IMPORTANTES DE NOMES:
- **NUNCA use os nomes: Arthur, Blackwood, Damien, Lilith**
- **Evite nomes genéricos ou clichês**
- **Prefira nomes brasileiros autênticos**
- **Sugestões de nomes milionários**: Rafael, Carlos, Bruno, Diego, Felipe, Gustavo
- **Sugestões de nomes humildes**: Maria, Ana, João, Pedro, Antônio, José

## Diretrizes Narrativas:
- Aproximadamente 150-200 palavras por premissa
- Foque no desenvolvimento emocional e na jornada de autodescoberta
- Inclua conflitos internos e externos realistas
- Evite clichês óbvios, busque originalidade na abordagem
- Crie nomes específicos e únicos para cada história
- NUNCA repita nomes que já foram usados anteriormente
- Desenvolva situações autênticas e tocantes
- **IMPORTANTE: Use SEMPRE o mesmo nome para o mesmo personagem durante toda a premissa**
- **NUNCA mude o nome de um personagem no meio da história**

## Formato de Resposta:
Para cada título, forneça apenas:

**PREMISSA:**
[Premissa detalhada com todos os elementos obrigatórios, focando na transformação emocional e contraste social. MANTENHA CONSISTÊNCIA NOS NOMES DOS PERSONAGENS. 

**IMPORTANTE: NÃO inclua o título na resposta, NÃO use formatações como "Premissa Narrativa: [título]", NÃO repita o título fornecido. Forneça APENAS o conteúdo da premissa sem cabeçalhos ou títulos adicionais.**]"""
    
    if selected_titles:
        titles_section = "\n\n## Títulos para análise:\n" + "\n".join(f'{i+1}. {title}' for i, title in enumerate(selected_titles))
        return base_prompt + titles_section

def create_inicio_prompt(title, context, base_prompt, script_size):
    """Cria prompt para capítulo inicial usando orientações narrativas"""
    return f"""Você é um roteirista profissional especializado em conteúdo para YouTube.

TÍTULO DO VÍDEO: {title}

ORIENTAÇÕES NARRATIVAS (uso interno - não mencionar diretamente):
{context}

INSTRUÇÕES:
- Escreva o capítulo inicial (introdução) deste roteiro
- O capítulo deve ter aproximadamente 500 palavras
- Apresente os personagens principais e o cenário
- Estabeleça o tom e a atmosfera da história
- Use uma linguagem envolvente adequada para vídeos do YouTube
- Escreva apenas o conteúdo do capítulo, sem títulos ou marcações
- NÃO cite ou mencione as orientações narrativas diretamente
- Crie um conteúdo independente baseado nas orientações

{base_prompt}"""

def create_capitulo_prompt(title, context, base_prompt, chapter_num, total_chapters, script_size):
    """Cria prompt para capítulos intermediários usando orientações narrativas"""
    return f"""Você é um roteirista profissional especializado em conteúdo para YouTube.

TÍTULO DO VÍDEO: {title}

ORIENTAÇÕES NARRATIVAS (uso interno - não mencionar diretamente):
{context}

INSTRUÇÕES:
- Escreva o capítulo {chapter_num + 1} de {total_chapters} deste roteiro
- O capítulo deve ter aproximadamente 500 palavras
- Desenvolva a trama e os personagens
- Mantenha o ritmo e a tensão narrativa
- Use uma linguagem envolvente adequada para vídeos do YouTube
- Escreva apenas o conteúdo do capítulo, sem títulos ou marcações
- NÃO cite ou mencione as orientações narrativas diretamente
- Crie um conteúdo independente baseado nas orientações

{base_prompt}"""

def create_final_prompt(title, context, base_prompt, script_size):
    """Cria prompt para capítulo final usando orientações narrativas"""
    return f"""Você é um roteirista profissional especializado em conteúdo para YouTube.

TÍTULO DO VÍDEO: {title}

ORIENTAÇÕES NARRATIVAS (uso interno - não mencionar diretamente):
{context}

INSTRUÇÕES:
- Escreva o capítulo final (conclusão) deste roteiro
- O capítulo deve ter aproximadamente 500 palavras
- Amarre todas as pontas soltas da história
- Proporcione um fechamento satisfatório
- Use uma linguagem envolvente adequada para vídeos do YouTube
- Escreva apenas o conteúdo do capítulo, sem títulos ou marcações
- NÃO cite ou mencione as orientações narrativas diretamente
- Crie um conteúdo independente baseado nas orientações

{base_prompt}"""
    
    return base_prompt
