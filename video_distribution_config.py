# Configurações para distribuição uniforme de imagens no vídeo

# Tolerância para diferenças de duração (em segundos)
# Valores menores que isso não acionarão um recálculo completo dos timings
DURATION_TOLERANCE = 0.5

# Método preferido para concatenação de clipes
# Opções: 'chain', 'compose'
CONCATENATION_METHOD = 'chain'

# Duração das transições (em segundos)
# Nota: Isso afeta a duração total do vídeo, por isso é importante manter a lógica de recálculo
TRANSITION_DURATION = 0.3

# Debug: ativar logs mais detalhados
enable_debug_logs = True

# Caminho padrão para salvar vídeos de teste
TEST_VIDEO_PATH = r'c:\Users\Enderson\Documents\APP 2\auto-video-producerV5-dev\test_output'  # Usando string raw para evitar erros de escape