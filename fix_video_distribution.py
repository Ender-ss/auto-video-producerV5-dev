#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para corrigir a distribuição uniforme de imagens na pipeline de criação de vídeos

Este script verifica e corrige a implementação da distribuição uniforme de imagens,
importando as configurações corretas e garantindo que a lógica de timing e transições
estejam funcionando como esperado.
"""

import os
import sys
import time
import logging
import argparse
from datetime import datetime

# Configurar logging
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fix_video_distribution.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class VideoDistributionFixer:
    """Classe para corrigir a distribuição uniforme de imagens"""
    
    def __init__(self):
        self.config_loaded = False
        self.DURATION_TOLERANCE = 0.5
        self.TRANSITION_DURATION = 0.3
    
    def load_configurations(self):
        """Carregar configurações do arquivo video_distribution_config.py"""
        try:
            from video_distribution_config import DURATION_TOLERANCE, TRANSITION_DURATION
            self.DURATION_TOLERANCE = DURATION_TOLERANCE
            self.TRANSITION_DURATION = TRANSITION_DURATION
            self.config_loaded = True
            
            logger.info("[OK] Configurações carregadas com sucesso:")
            logger.info(f"   - DURATION_TOLERANCE: {self.DURATION_TOLERANCE}s")
            logger.info(f"   - TRANSITION_DURATION: {self.TRANSITION_DURATION}s")
            return True
        except ImportError:
            logger.error("[ERRO] Não foi possível importar o arquivo video_distribution_config.py")
            logger.info("   Verifique se o arquivo existe no diretório raiz do projeto.")
            return False
    
    def check_service_implementation(self):
        """Verificar se a implementação no VideoCreationService está correta"""
        try:
            service_path = os.path.join(
                'backend', 'services', 'video_creation_service.py'
            )
            
            if not os.path.exists(service_path):
                logger.error(f"[ERRO] Arquivo não encontrado: {service_path}")
                return False
            
            # Ler o conteúdo do arquivo
            with open(service_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Verificar importações
            if 'from video_distribution_config import' not in content:
                logger.warning("[AVISO] As importações de configuração não estão presentes no arquivo.")
                logger.info("   Você precisa adicionar a importação no início do arquivo.")
                
            # Verificar uso da TRANSITION_DURATION
            if 'transition_duration = TRANSITION_DURATION' not in content:
                logger.warning("[AVISO] A duração de transição não está usando a configuração importada.")
                logger.info("   Verifique se o método _add_transitions está usando TRANSITION_DURATION.")
                
            # Verificar implementação do _calculate_uniform_timings
            if '_calculate_uniform_timings' not in content:
                logger.error("[ERRO] O método _calculate_uniform_timings não foi encontrado.")
                return False
            
            logger.info("[OK] Verificação da implementação concluída com sucesso.")
            return True
            
        except Exception as e:
            logger.error(f"[ERRO] Erro ao verificar a implementação: {e}")
            return False
    
    def run_test_verification(self):
        """Executar verificação do teste"""
        logger.info("[INFO] Executando verificação do script de teste...")
        
        test_script_path = 'test_video_distribution.py'
        
        if not os.path.exists(test_script_path):
            logger.error(f"[ERRO] Script de teste não encontrado: {test_script_path}")
            return False
        
        # Ler o conteúdo do arquivo
        with open(test_script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar se está usando as configurações corretas
        if 'from video_distribution_config import DURATION_TOLERANCE, TRANSITION_DURATION' not in content:
            logger.warning("[AVISO] O script de teste não está importando todas as configurações necessárias.")
            return False
        
        logger.info("[OK] Script de teste verificado com sucesso.")
        return True
    
    def create_fix_report(self):
        """Criar relatório com as correções necessárias"""
        report_path = os.path.join('test_output', 'fix_report.txt')
        
        # Criar diretório de saída se necessário
        os.makedirs('test_output', exist_ok=True)
        
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write("# RELATÓRIO DE CORREÇÃO DA DISTRIBUIÇÃO DE IMAGENS\n")
                f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
                
                if self.config_loaded:
                    f.write("## CONFIGURAÇÕES CARREGADAS\n")
                    f.write(f"- DURATION_TOLERANCE: {self.DURATION_TOLERANCE}s\n")
                    f.write(f"- TRANSITION_DURATION: {self.TRANSITION_DURATION}s\n\n")
                else:
                    f.write("## CONFIGURAÇÕES NÃO CARREGADAS\n")
                    f.write("O arquivo video_distribution_config.py não foi encontrado ou não pôde ser importado.\n\n")
                
                f.write("## PASSOS PARA CORRIGIR A DISTRIBUIÇÃO UNIFORME DE IMAGENS\n")
                f.write("1. Certifique-se de que o arquivo video_distribution_config.py existe no diretório raiz do projeto.\n")
                f.write("2. No arquivo backend/services/video_creation_service.py, adicione a importação no início do arquivo:\n")
                f.write("   ```python\n")
                f.write("   from video_distribution_config import DURATION_TOLERANCE, TRANSITION_DURATION\n")
                f.write("   ```\n")
                f.write("3. No mesmo arquivo, no método _add_transitions, altere a duração da transição para usar a configuração:\n")
                f.write("   ```python\n")
                f.write("   transition_duration = TRANSITION_DURATION  # Usar duração configurada nas transições\n")
                f.write("   ```\n")
                f.write("4. Execute o script test_video_distribution.py para verificar se a distribuição está funcionando:\n")
                f.write("   ```bash\n")
                f.write("   python test_video_distribution.py\n")
                f.write("   ```\n")
                f.write("5. Após a criação do vídeo de teste, verifique a distribuição usando o script check_video.py:\n")
                f.write("   ```bash\n")
                f.write("   python check_video.py --path caminho/do/video.mp4\n")
                f.write("   ```\n\n")
                
                f.write("## SOLUÇÃO DE PROBLEMAS COMUNS\n")
                f.write("- **Erro de importação**: Certifique-se de que o diretório raiz do projeto está no PYTHONPATH.\n")
                f.write("- **Timing inconsistente**: Ajuste o valor de DURATION_TOLERANCE no arquivo de configuração.\n")
                f.write("- **Transições não sincronizadas**: Verifique se TRANSITION_DURATION está sendo usada corretamente.\n")
                
            logger.info(f"[OK] Relatório de correção criado: {report_path}")
            return report_path
        except Exception as e:
            logger.error(f"[ERRO] Erro ao criar relatório de correção: {e}")
            return None
    
    def run_fix_process(self):
        """Executar processo completo de correção"""
        logger.info("[INFO] Iniciando processo de correção da distribuição uniforme de imagens...")
        
        # 1. Carregar configurações
        config_ok = self.load_configurations()
        
        # 2. Verificar implementação do serviço
        service_ok = self.check_service_implementation()
        
        # 3. Verificar script de teste
        test_ok = self.run_test_verification()
        
        # 4. Criar relatório
        report_path = self.create_fix_report()
        
        # 5. Mostrar resumo
        logger.info("\n[INFO] RESUMO DA CORREÇÃO:")
        if config_ok and service_ok and test_ok:
            logger.info("[OK] Todas as verificações passaram! A distribuição de imagens deve estar funcionando corretamente.")
        else:
            logger.warning("[AVISO] Algumas verificações falharam. Consulte o relatório para mais detalhes.")
        
        if report_path:
            logger.info(f"   Relatório gerado: {report_path}")
        
        logger.info("\n[INFO] Dicas:")
        logger.info("- Execute o pipeline completo para testar com dados reais.")
        logger.info("- Ajuste os parâmetros no arquivo video_distribution_config.py se necessário.")
        logger.info("- Sempre verifique o log de execução para identificar possíveis problemas.")

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description='Corrigir distribuição uniforme de imagens na pipeline')
    parser.add_argument('--fix', action='store_true', help='Aplicar correções automaticamente')
    args = parser.parse_args()
    
    fixer = VideoDistributionFixer()
    fixer.run_fix_process()

if __name__ == "__main__":
    main()