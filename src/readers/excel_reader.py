"""
Leitor dinâmico de arquivos Excel que suporta múltiplos formatos.
Converte dados da planilha para formato de dicionário para fácil manipulação.
"""

import os
from typing import List, Dict, Tuple
import pandas as pd
from src.logger import setup_logger
from src.config import FIELD_MAPPING

logger = setup_logger(__name__)


class ExcelReaderError(Exception):
    """Exceção customizada para erros de leitura Excel."""
    pass


def validate_file_exists(filepath: str) -> bool:
    """
    Valida se o arquivo Excel existe.
    
    Args:
        filepath: Caminho do arquivo
    
    Returns:
        True se existe, False caso contrário
    """
    if not os.path.exists(filepath):
        raise ExcelReaderError(f"Arquivo não encontrado: {filepath}")
    return True


def validate_file_format(filepath: str) -> bool:
    """
    Valida se o arquivo tem extensão Excel suportada.
    
    Args:
        filepath: Caminho do arquivo
    
    Returns:
        True se é Excel válido
    """
    valid_extensions = [".xlsx", ".xls", ".xlsm", ".ods"]
    _, ext = os.path.splitext(filepath)
    
    if ext.lower() not in valid_extensions:
        raise ExcelReaderError(
            f"Formato não suportado: {ext}. Suportados: {', '.join(valid_extensions)}"
        )
    return True


def read_excel_dynamic(filepath: str, sheet_name: int = 0) -> Tuple[List[Dict[str, any]], List[str]]:
    """
    Lê um arquivo Excel de forma dinâmica e retorna os dados como lista de dicionários.
    Suporta automaticamente .xlsx, .xls, .xlsm, .ods
    
    Args:
        filepath: Caminho do arquivo Excel
        sheet_name: Índice da aba a ler (default: 0 = primeira aba)
    
    Returns:
        Tupla (rows, columns) onde:
        - rows: Lista de dicionários, cada dict é uma linha
        - columns: Lista de nomes de colunas encontradas
    
    Raises:
        ExcelReaderError: Se houver problemas na leitura
    """
    try:
        # Validações
        validate_file_exists(filepath)
        validate_file_format(filepath)
        
        logger.info(f"Lendo arquivo: {filepath}")
        
        # Ler Excel com pandas
        df = pd.read_excel(filepath, sheet_name=sheet_name)
        
        # Log de informações
        logger.info(f"Colunas encontradas: {list(df.columns)}")
        logger.info(f"Total de linhas: {len(df)}")
        
        # Remover linhas completamente vazias
        df = df.dropna(how="all")
        
        # Converter para lista de dicionários
        rows = df.to_dict("records")
        
        # Limpar NaN values para None
        rows = [
            {k: (None if pd.isna(v) else v) for k, v in row.items()}
            for row in rows
        ]
        
        columns = list(df.columns)
        
        logger.info(f"Dados lidos com sucesso: {len(rows)} linhas")
        
        return rows, columns
    
    except ExcelReaderError as e:
        logger.error(f"Erro ao ler Excel: {str(e)}")
        raise
    except pd.errors.ParserError as e:
        logger.error(f"Erro ao fazer parse do arquivo Excel: {str(e)}")
        raise ExcelReaderError(f"Erro ao fazer parse do arquivo: {str(e)}")
    except Exception as e:
        logger.error(f"Erro inesperado ao ler Excel: {str(e)}")
        raise ExcelReaderError(f"Erro inesperado: {str(e)}")


def validate_columns(columns: List[str]) -> Tuple[bool, List[str]]:
    """
    Valida se as colunas do Excel correspondem aos campos esperados.
    
    Args:
        columns: Lista de nomes de colunas do Excel
    
    Returns:
        Tupla (is_valid, missing_columns) onde missing_columns é lista de campos não encontrados
    """
    expected_columns = set(FIELD_MAPPING.keys())
    found_columns = set(columns)
    
    missing = expected_columns - found_columns
    extra = found_columns - expected_columns
    
    if missing:
        logger.warning(f"Colunas obrigatórias não encontradas: {missing}")
    
    if extra:
        logger.debug(f"Colunas extras encontradas (serão ignoradas): {extra}")
    
    return len(missing) == 0, list(missing)


def read_and_validate(filepath: str) -> Tuple[List[Dict[str, any]], List[str]]:
    """
    Lê Excel, valida colunas e retorna dados prontos para processamento.
    
    Args:
        filepath: Caminho do arquivo Excel
    
    Returns:
        Tupla (rows, validation_errors)
    
    Raises:
        ExcelReaderError: Se arquivo não existir ou formato inválido
    """
    rows, columns = read_excel_dynamic(filepath)
    is_valid, missing = validate_columns(columns)
    
    if not is_valid:
        error_msg = f"Colunas obrigatórias faltando: {', '.join(missing)}"
        logger.error(error_msg)
        raise ExcelReaderError(error_msg)
    
    return rows, columns
