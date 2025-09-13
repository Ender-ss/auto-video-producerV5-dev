# Makefile para MoviePy Documentation Manager
# Este Makefile facilita a execução dos scripts de documentação e testes do MoviePy

# Variáveis
PYTHON := python
PYTHON_FLAGS := 
DOCS_DIR := docs/moviepy
SCRIPTS_DIR := $(DOCS_DIR)
CONFIG_FILE := $(DOCS_DIR)/CONFIG.json
REQUIREMENTS_FILE := $(DOCS_DIR)/requirements.txt
SETUP_SCRIPT := $(DOCS_DIR)/setup.py
MAIN_SCRIPT := $(DOCS_DIR)/SCRIPT_MAIN.py

# Cores para output
RED := \033[91m
GREEN := \033[92m
YELLOW := \033[93m
BLUE := \033[94m
MAGENTA := \033[95m
CYAN := \033[96m
WHITE := \033[97m
ENDC := \033[0m
BOLD := \033[1m

# Funções
define color_print
	@echo "$(2)$(1)$(ENDC)"
endef

define print_header
	@echo "$(CYAN)==============================================================$(ENDC)"
	@echo "$(CYAN)$(1)$(ENDC)"
	@echo "$(CYAN)==============================================================$(ENDC)"
	@echo ""
endef

define print_section
	@echo "$(BLUE)----------------------------------------$(ENDC)"
	@echo "$(BLUE)$(1)$(ENDC)"
	@echo "$(BLUE)----------------------------------------$(ENDC)"
	@echo ""
endef

# Alvos padrão
.PHONY: help all install diagnose test examples report clean update setup

# Ajuda
help:
	@$(call print_header,Makefile para MoviePy Documentation Manager)
	@$(call color_print,"Uso:",$(WHITE))
	@$(call color_print,"  make [alvo]",$(CYAN))
	@$(call color_print,"",$(WHITE))
	@$(call color_print,"Alvos disponíveis:",$(WHITE))
	@$(call color_print,"  help          Mostra esta ajuda",$(CYAN))
	@$(call color_print,"  all           Executa todos os scripts",$(CYAN))
	@$(call color_print,"  install       Executa o script de instalação",$(CYAN))
	@$(call color_print,"  diagnose      Executa o script de diagnóstico",$(CYAN))
	@$(call color_print,"  diagnose-simple Executa o script de diagnóstico simplificado",$(CYAN))
	@$(call color_print,"  test          Executa os testes do MoviePy",$(CYAN))
	@$(call color_print,"  examples      Executa os exemplos do MoviePy",$(CYAN))
	@$(call color_print,"  report        Gera um relatório completo",$(CYAN))
	@$(call color_print,"  clean         Limpa arquivos temporários",$(CYAN))
	@$(call color_print,"  update        Atualiza a documentação",$(CYAN))
	@$(call color_print,"  setup         Configura o ambiente do MoviePy",$(CYAN))
	@$(call color_print,"  check         Verifica o ambiente",$(CYAN))
	@$(call color_print,"  run           Executa o script principal",$(CYAN))
	@$(call color_print,"",$(WHITE))

# Executar todos os scripts
all:
	@$(call print_header,Executar Todos os Scripts)
	@$(PYTHON) $(MAIN_SCRIPT) --all

# Instalação
install:
	@$(call print_header,Instalar e Configurar MoviePy)
	@$(PYTHON) $(MAIN_SCRIPT) --install

# Diagnóstico
diagnose:
	@$(call print_header,Diagnóstico do MoviePy)
	@$(PYTHON) $(MAIN_SCRIPT) --diagnose

# Diagnóstico simplificado
diagnose-simple:
	@$(call print_header,Diagnóstico Simplificado do MoviePy)
	@$(PYTHON) $(DOCS_DIR)/solucoes/SCRIPT_DIAGNOSTICO_SIMPLIFICADO.py

# Testes
test:
	@$(call print_header,Testes do MoviePy)
	@$(PYTHON) $(MAIN_SCRIPT) --test

# Exemplos
examples:
	@$(call print_header,Exemplos do MoviePy)
	@$(PYTHON) $(MAIN_SCRIPT) --examples

# Relatório
report:
	@$(call print_header,Relatório do MoviePy)
	@$(PYTHON) $(MAIN_SCRIPT) --report

# Limpar
clean:
	@$(call print_header,Limpar Arquivos Temporários)
	@$(PYTHON) $(MAIN_SCRIPT) --clean

# Atualizar
update:
	@$(call print_header,Atualizar Documentação)
	@$(PYTHON) $(MAIN_SCRIPT) --update

# Setup
setup:
	@$(call print_header,Configurar Ambiente do MoviePy)
	@$(PYTHON) $(SETUP_SCRIPT)

# Verificar ambiente
check:
	@$(call print_header,Verificar Ambiente)
	@if [ ! -f "$(CONFIG_FILE)" ]; then \
		$(call color_print,"Arquivo de configuração não encontrado: $(CONFIG_FILE)",$(RED)); \
		exit 1; \
	fi
	@if [ ! -f "$(REQUIREMENTS_FILE)" ]; then \
		$(call color_print,"Arquivo requirements.txt não encontrado: $(REQUIREMENTS_FILE)",$(RED)); \
		exit 1; \
	fi
	@if [ ! -f "$(SETUP_SCRIPT)" ]; then \
		$(call color_print,"Script setup.py não encontrado: $(SETUP_SCRIPT)",$(RED)); \
		exit 1; \
	fi
	@if [ ! -f "$(MAIN_SCRIPT)" ]; then \
		$(call color_print,"Script principal não encontrado: $(MAIN_SCRIPT)",$(RED)); \
		exit 1; \
	fi
	@$(call color_print,"Todos os arquivos necessários estão presentes!",$(GREEN))

# Executar script principal
run:
	@$(call print_header,Executar Script Principal)
	@$(PYTHON) $(MAIN_SCRIPT)

# Instalar dependências
install-deps:
	@$(call print_header,Instalar Dependências)
	@$(call color_print,"Instalando dependências do requirements.txt...",$(YELLOW))
	@$(PYTHON) -m pip install -r $(REQUIREMENTS_FILE)
	@$(call color_print,"Dependências instaladas com sucesso!",$(GREEN))

# Verificar Python
check-python:
	@$(call print_section,Verificar Python)
	@$(PYTHON) --version

# Verificar FFmpeg
check-ffmpeg:
	@$(call print_section,Verificar FFmpeg)
	@ffmpeg -version

# Verificar ImageMagick
check-imagemagick:
	@$(call print_section,Verificar ImageMagick)
	@magick -version

# Testar MoviePy
test-moviepy:
	@$(call print_section,Testar MoviePy)
	@$(PYTHON) -c "import moviepy.editor as mpy; print('MoviePy está funcionando!')"

# Criar diretórios
create-dirs:
	@$(call print_section,Criar Diretórios)
	@mkdir -p $(DOCS_DIR)/temp
	@mkdir -p $(DOCS_DIR)/output
	@mkdir -p $(DOCS_DIR)/logs
	@mkdir -p $(DOCS_DIR)/cache
	@mkdir -p $(DOCS_DIR)/examples_output
	@$(call color_print,"Diretórios criados com sucesso!",$(GREEN))

# Limpar diretórios
clean-dirs:
	@$(call print_section,Limpar Diretórios)
	@rm -rf $(DOCS_DIR)/temp/*
	@rm -rf $(DOCS_DIR)/output/*
	@rm -rf $(DOCS_DIR)/logs/*
	@rm -rf $(DOCS_DIR)/cache/*
	@rm -rf $(DOCS_DIR)/examples_output/*
	@$(call color_print,"Diretórios limpos com sucesso!",$(GREEN))

# Verificar estrutura
check-structure:
	@$(call print_section,Verificar Estrutura)
	@ls -la $(DOCS_DIR)
	@ls -la $(DOCS_DIR)/documentacao
	@ls -la $(DOCS_DIR)/exemplos
	@ls -la $(DOCS_DIR)/guias
	@ls -la $(DOCS_DIR)/solucoes
	@ls -la $(DOCS_DIR)/testes

# Executar diagnóstico completo
full-diagnose:
	@$(call print_header,Diagnóstico Completo)
	@make check
	@make check-python
	@make check-ffmpeg
	@make check-imagemagick
	@make test-moviepy
	@make check-structure
	@make diagnose-simple
	@make diagnose

# Executar workflow completo
full-workflow:
	@$(call print_header,Workflow Completo)
	@make setup
	@make install-deps
	@make create-dirs
	@make full-diagnose
	@make test
	@make examples
	@make report
	@$(call color_print,"Workflow completo executado com sucesso!",$(GREEN))

# Alvo padrão
.DEFAULT_GOAL := help