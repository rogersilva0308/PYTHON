"""
Validadores para dados da planilha antes de enviar ao formulário.
"""

from typing import Dict, List, Tuple
from src.config import VALIDATION_RULES, FIELD_MAPPING
from src.logger import setup_logger

logger = setup_logger(__name__)


class ValidationError(Exception):
    """Exceção customizada para erros de validação."""
    pass


def validate_field(field_name: str, value: any) -> Tuple[bool, str]:
    """
    Valida um campo individual de acordo com as regras.
    
    Args:
        field_name: Nome do campo
        value: Valor a validar
    
    Returns:
        Tupla (is_valid, error_message)
    """
    if field_name not in VALIDATION_RULES:
        return True, ""
    
    rules = VALIDATION_RULES[field_name]
    
    # Validar campo obrigatório
    if value is None or (isinstance(value, str) and value.strip() == ""):
        if FIELD_MAPPING.get(field_name, {}).get("required", False):
            return False, f"{field_name} é obrigatório"
        return True, ""
    
    # Validar string
    if "min_length" in rules and isinstance(value, str):
        if len(value.strip()) < rules["min_length"]:
            return False, f"{field_name} deve ter pelo menos {rules['min_length']} caracteres"
    
    if "max_length" in rules and isinstance(value, str):
        if len(value.strip()) > rules["max_length"]:
            return False, f"{field_name} não pode exceder {rules['max_length']} caracteres"
    
    # Validar número
    if "min_value" in rules:
        try:
            numeric_value = float(value)
            if numeric_value < rules["min_value"]:
                return False, f"{field_name} deve ser >= {rules['min_value']}"
        except (ValueError, TypeError):
            return False, f"{field_name} deve ser um número válido"
    
    if "max_value" in rules:
        try:
            numeric_value = float(value)
            if numeric_value > rules["max_value"]:
                return False, f"{field_name} deve ser <= {rules['max_value']}"
        except (ValueError, TypeError):
            return False, f"{field_name} deve ser um número válido"
    
    # Validar valores permitidos
    if "allowed_values" in rules:
        if value not in rules["allowed_values"]:
            allowed = ", ".join(rules["allowed_values"])
            return False, f"{field_name} deve ser um de: {allowed}"
    
    return True, ""


def validate_row(row: Dict[str, any]) -> Tuple[bool, List[str]]:
    """
    Valida uma linha completa de dados.
    
    Args:
        row: Dicionário com os dados da linha
    
    Returns:
        Tupla (is_valid, list_of_errors)
    """
    errors = []
    
    for field_name in FIELD_MAPPING.keys():
        value = row.get(field_name)
        is_valid, error_msg = validate_field(field_name, value)
        
        if not is_valid:
            errors.append(error_msg)
    
    return len(errors) == 0, errors


def validate_all_rows(rows: List[Dict[str, any]]) -> Tuple[List[Dict], List[Tuple[int, List[str]]]]:
    """
    Valida múltiplas linhas e retorna as válidas e inválidas.
    
    Args:
        rows: Lista de dicionários (cada um é uma linha)
    
    Returns:
        Tupla (rows_valid, rows_invalid) onde rows_invalid contém (row_index, errors)
    """
    valid_rows = []
    invalid_rows = []
    
    for idx, row in enumerate(rows, start=1):
        is_valid, errors = validate_row(row)
        
        if is_valid:
            valid_rows.append(row)
            logger.debug(f"Linha {idx}: [OK] Válida")
        else:
            invalid_rows.append((idx, errors))
            logger.warning(f"Linha {idx}: ✗ Inválida - {'; '.join(errors)}")
    
    logger.info(f"Validação concluída: {len(valid_rows)} válidos, {len(invalid_rows)} inválidos")
    
    return valid_rows, invalid_rows
