"""
Configuração de logging estruturado para a automação.
"""

import logging
import os
from datetime import datetime
from src.config import LOG_FILE, LOG_LEVEL, LOG_FORMAT


def setup_logger(name: str) -> logging.Logger:
    """
    Configura e retorna um logger com handlers para arquivo e console.
    
    Args:
        name: Nome do logger (geralmente __name__ do módulo)
    
    Returns:
        logging.Logger: Logger configurado
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL))
    
    # Criar diretório de logs se não existir
    log_dir = os.path.dirname(LOG_FILE)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Handler para arquivo
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(getattr(logging, LOG_LEVEL))
    file_formatter = logging.Formatter(LOG_FORMAT)
    file_handler.setFormatter(file_formatter)
    
    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, LOG_LEVEL))
    console_formatter = logging.Formatter(LOG_FORMAT)
    console_handler.setFormatter(console_formatter)
    
    # Adicionar handlers ao logger
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger


def log_execution_start(logger: logging.Logger, filename: str, total_rows: int):
    """Log de início de execução."""
    logger.info("=" * 80)
    logger.info(f"INICIANDO AUTOMAÇÃO - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    logger.info(f"Arquivo: {filename}")
    logger.info(f"Total de registros: {total_rows}")
    logger.info("=" * 80)


def log_execution_end(logger: logging.Logger, total_processed: int, total_success: int, total_failed: int):
    """Log de fim de execução."""
    logger.info("=" * 80)
    logger.info(f"EXECUÇÃO FINALIZADA - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    logger.info(f"Total processado: {total_processed}")
    logger.info(f"Sucessos: {total_success}")
    logger.info(f"Falhas: {total_failed}")
    logger.info("=" * 80)
