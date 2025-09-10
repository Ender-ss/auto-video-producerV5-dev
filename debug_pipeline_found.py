#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 Debug Pipeline Encontrada
Script para investigar a Pipeline #2025-09-09-009 encontrada no banco
"""

import sys
import os
import json
from datetime import datetime

# Adicionar o diretório backend ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def debug_pipeline_found():
    """Debugar a pipeline específica encontrada"""
    print("🔍 [DEBUG] Investigando Pipeline #2025-09-09-009...")
    print("=" * 60)
    
    try:
        # Importar app e criar contexto
        from app import app, db, Pipeline, PipelineLog
        
        with app.app_context():
            if Pipeline:
                # Buscar pipeline específica por display_name
                pipeline = Pipeline.query.filter(
                    Pipeline.display_name.like('%2025-09-09-009%')
                ).first()
                
                if pipeline:
                    print(f"📋 PIPELINE ENCONTRADA NO BANCO:")
                    print(f"   ID (UUID): {pipeline.pipeline_id}")
                    print(f"   Display Name: {pipeline.display_name}")
                    print(f"   Título: {pipeline.title}")
                    print(f"   Status: {pipeline.status}")
                    print(f"   Progresso: {pipeline.progress}%")
                    print(f"   Etapa atual: {pipeline.current_step}")
                    print(f"   Canal URL: {pipeline.channel_url}")
                    print(f"   Estilo de vídeo: {pipeline.video_style}")
                    print(f"   Duração alvo: {pipeline.target_duration}s")
                    print()
                    
                    # Verificar configuração
                    if pipeline.config_json:
                        try:
                            config = json.loads(pipeline.config_json)
                            print(f"📄 CONFIGURAÇÃO:")
                            print(json.dumps(config, indent=2, ensure_ascii=False))
                            print()
                        except Exception as e:
                            print(f"   ❌ Erro ao decodificar config_json: {e}")
                    
                    # Verificar configuração do agente
                    if pipeline.agent_config:
                        try:
                            agent_config = json.loads(pipeline.agent_config)
                            print(f"🤖 CONFIGURAÇÃO DO AGENTE:")
                            print(json.dumps(agent_config, indent=2, ensure_ascii=False))
                            print()
                        except Exception as e:
                            print(f"   ❌ Erro ao decodificar agent_config: {e}")
                    
                    # Verificar resultados de cada etapa
                    print(f"📊 RESULTADOS DAS ETAPAS:")
                    if pipeline.extraction_results:
                        print(f"   ✅ Extraction: {len(pipeline.extraction_results)} chars")
                    else:
                        print(f"   ❌ Extraction: Não executado")
                    
                    if pipeline.titles_results:
                        print(f"   ✅ Titles: {len(pipeline.titles_results)} chars")
                    else:
                        print(f"   ❌ Titles: Não executado")
                    
                    if pipeline.premises_results:
                        print(f"   ✅ Premises: {len(pipeline.premises_results)} chars")
                    else:
                        print(f"   ❌ Premises: Não executado")
                    
                    if hasattr(pipeline, 'scripts_results') and pipeline.scripts_results:
                        print(f"   ✅ Scripts: {len(pipeline.scripts_results)} chars")
                    else:
                        print(f"   ❌ Scripts: Não executado")
                    
                    if hasattr(pipeline, 'tts_results') and pipeline.tts_results:
                        print(f"   ✅ TTS: {len(pipeline.tts_results)} chars")
                    else:
                        print(f"   ❌ TTS: Não executado")
                    
                    if hasattr(pipeline, 'images_results') and pipeline.images_results:
                        print(f"   ✅ Images: {len(pipeline.images_results)} chars")
                    else:
                        print(f"   ❌ Images: Não executado")
                    
                    if hasattr(pipeline, 'video_results') and pipeline.video_results:
                        print(f"   ✅ Video: {len(pipeline.video_results)} chars")
                    else:
                        print(f"   ❌ Video: Não executado")
                    
                    print()
                    
                    # Buscar logs da pipeline
                    if PipelineLog:
                        logs = PipelineLog.query.filter_by(
                            pipeline_id=pipeline.pipeline_id
                        ).order_by(PipelineLog.timestamp.desc()).limit(10).all()
                        
                        if logs:
                            print(f"📝 ÚLTIMOS 10 LOGS:")
                            for log in logs:
                                print(f"   [{log.timestamp}] {log.level.upper()}: {log.message}")
                                if log.step:
                                    print(f"      Etapa: {log.step}")
                                if log.data:
                                    try:
                                        data = json.loads(log.data)
                                        print(f"      Dados: {json.dumps(data, ensure_ascii=False)}")
                                    except:
                                        print(f"      Dados: {log.data}")
                                print()
                        else:
                            print(f"📝 Nenhum log encontrado para esta pipeline")
                    
                    print()
                    print(f"🔍 ANÁLISE:")
                    
                    # Verificar por que está no polling
                    if pipeline.status in ['queued', 'processing']:
                        print(f"   ⚠️  Pipeline está com status '{pipeline.status}' - por isso aparece no polling")
                        print(f"   📊 Progresso atual: {pipeline.progress}%")
                        
                        if pipeline.status == 'queued':
                            print(f"   💡 SOLUÇÃO: Pipeline está na fila mas não está sendo processada")
                            print(f"      - Verifique se há threads de processamento ativas")
                            print(f"      - Considere cancelar ou reiniciar a pipeline")
                        
                        elif pipeline.status == 'processing':
                            print(f"   💡 SOLUÇÃO: Pipeline está sendo processada")
                            print(f"      - Verifique logs do backend para ver o progresso")
                            print(f"      - Se travou, considere reiniciar")
                    
                    elif pipeline.status in ['completed', 'failed', 'cancelled']:
                        print(f"   ✅ Pipeline já foi finalizada com status '{pipeline.status}'")
                        print(f"   💡 SOLUÇÃO: Remover do polling ou limpar do banco")
                    
                    else:
                        print(f"   ❓ Status desconhecido: '{pipeline.status}'")
                    
                    return pipeline
                
                else:
                    print("❌ Pipeline #2025-09-09-009 não encontrada no banco")
                    return None
            
            else:
                print("❌ Modelo Pipeline não disponível")
                return None
    
    except Exception as e:
        print(f"❌ Erro ao verificar pipeline: {e}")
        import traceback
        traceback.print_exc()
        return None

def check_memory_state():
    """Verificar estado em memória"""
    print("\n🧠 Verificando estado em memória...")
    
    try:
        from routes.pipeline_complete import active_pipelines, pipeline_logs
        
        print(f"📊 Pipelines ativos em memória: {len(active_pipelines)}")
        
        # Procurar pela pipeline específica
        found_in_memory = False
        for pipeline_id, pipeline_data in active_pipelines.items():
            if '2025-09-09-009' in pipeline_id or '2025-09-09-009' in str(pipeline_data):
                print(f"   ⚠️  PIPELINE ENCONTRADA EM MEMÓRIA: {pipeline_id}")
                print(f"   📄 Dados: {json.dumps(pipeline_data, indent=2, default=str, ensure_ascii=False)}")
                found_in_memory = True
        
        if not found_in_memory:
            print(f"   ✅ Pipeline não encontrada em memória")
            print(f"   💡 Isso explica por que o polling busca do banco")
    
    except Exception as e:
        print(f"❌ Erro ao verificar memória: {e}")

def suggest_solutions(pipeline):
    """Sugerir soluções baseadas no estado da pipeline"""
    print("\n💡 SOLUÇÕES RECOMENDADAS:")
    print("=" * 40)
    
    if not pipeline:
        print("1. Pipeline não encontrada - verificar se foi removida")
        return
    
    if pipeline.status == 'queued':
        print("1. 🔄 REINICIAR PROCESSAMENTO:")
        print("   - Parar o backend (Ctrl+C)")
        print("   - Reiniciar o backend")
        print("   - A pipeline será retomada automaticamente")
        print()
        print("2. ❌ CANCELAR PIPELINE:")
        print("   - Usar endpoint DELETE /api/pipeline/{pipeline_id}")
        print("   - Ou atualizar status no banco para 'cancelled'")
        print()
        print("3. 🧹 LIMPAR BANCO:")
        print("   - Remover pipelines antigas com status 'queued'")
        print("   - Implementar limpeza automática")
    
    elif pipeline.status == 'processing':
        print("1. ⏱️  AGUARDAR CONCLUSÃO:")
        print("   - Pipeline pode estar processando normalmente")
        print("   - Verificar logs do backend para progresso")
        print()
        print("2. 🔄 REINICIAR SE TRAVOU:")
        print("   - Se não há progresso há muito tempo")
        print("   - Reiniciar backend para retomar")
    
    elif pipeline.status in ['completed', 'failed', 'cancelled']:
        print("1. 🧹 REMOVER DO POLLING:")
        print("   - Pipeline já foi finalizada")
        print("   - Não deveria aparecer no polling")
        print("   - Verificar lógica de filtragem no frontend")
        print()
        print("2. 🗑️  LIMPAR BANCO:")
        print("   - Remover pipelines antigas finalizadas")
        print("   - Manter apenas as ativas")

if __name__ == "__main__":
    print(f"🚀 Iniciando debug detalhado em {datetime.now()}")
    pipeline = debug_pipeline_found()
    check_memory_state()
    suggest_solutions(pipeline)
    print("\n✅ Debug detalhado concluído")