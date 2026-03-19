"""
Configurações e mapeamentos para a automação de cadastro de produtos.
Define constantes, URLs, seletores e mapeamento de campos Excel → formulário HTML.
"""

# ============================================================================
# URLS E CONFIGURAÇÕES DO SITE
# ============================================================================
TARGET_URL = "https://produtize.netlify.app/"
BROWSER_TYPE = "chromium"  # ou "firefox", "webkit"
HEADLESS_MODE = False  # Mudar para True se quiser executar em background
TIMEOUT_MS = 10000  # Timeout para operações Playwright
WAIT_AFTER_SUBMIT = 2000  # Tempo de espera após submissão (ms)

# ============================================================================
# MAPEAMENTO: COLUNAS EXCEL → CAMPOS HTML
# ============================================================================
# Este dicionário mapeia os nomes de colunas do Excel para os IDs/names dos campos HTML
# Permite reutilização da solução para diferentes arquivos com mesma estrutura
FIELD_MAPPING = {
    "Produto": {
        "html_id": "campo1",
        "html_name": "campo_produto",
        "type": "text",
        "required": True,
    },
    "Fornecedor": {
        "html_id": "campo2",
        "html_name": "campo_fornecedor",
        "type": "text",
        "required": True,
    },
    "Categoria": {
        "html_id": "campo3",
        "html_name": "campo_categoria",
        "type": "text",
        "required": True,
    },
    "Valor Unitário": {
        "html_id": "campo4",
        "html_name": "campo_valor_unitario",
        "type": "float",
        "required": True,
    },
    "Notificar a Cada Venda?": {
        "html_yes_id": "radiob1",
        "html_no_id": "radiob2",
        "type": "radio",
        "required": False,
        "default": "Sim",
    },
}

# ============================================================================
# SELETORES HTML DO FORMULÁRIO
# ============================================================================
FORM_SELECTORS = {
    "form": "form",
    "submit_button": "#btn_registrar",
    "campo1": "#campo1",
    "campo2": "#campo2",
    "campo3": "#campo3",
    "campo4": "#campo4",
    "radiob1": "#radiob1",  # Sim
    "radiob2": "#radiob2",  # Não
}

# ============================================================================
# CONFIGURAÇÕES DE LOGGING
# ============================================================================
LOG_FILE = "logs/automation.log"
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# ============================================================================
# CONFIGURAÇÕES DE VALIDAÇÃO
# ============================================================================
VALIDATION_RULES = {
    "Produto": {"min_length": 1, "max_length": 255},
    "Fornecedor": {"min_length": 1, "max_length": 255},
    "Categoria": {"min_length": 1, "max_length": 255},
    "Valor Unitário": {"min_value": 0.0, "max_value": 999999.99},
    "Notificar a Cada Venda?": {"allowed_values": ["Sim", "Não"]},
}

# ============================================================================
# CONFIGURAÇÕES DE RETRY
# ============================================================================
MAX_RETRIES = 3
RETRY_DELAY_MS = 1000  # Delay entre tentativas em ms

# ============================================================================
# MENSAGENS
# ============================================================================
MESSAGES = {
    "success": "[OK] Produto cadastrado com sucesso!",
    "error_validation": "✗ Erro de validação nos dados",
    "error_network": "✗ Erro de conexão com o site",
    "error_timeout": "✗ Timeout durante operação",
}
