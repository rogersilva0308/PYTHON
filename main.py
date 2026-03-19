#!/usr/bin/env python3
"""
Aplicação Principal - Automação de Cadastro de Produtos
Orquestra toda a automação: lê Excel, valida dados e preenche formulário.
"""

import asyncio
import argparse
import sys
from pathlib import Path

from src.logger import setup_logger, log_execution_start, log_execution_end
from src.readers.excel_reader import read_and_validate, ExcelReaderError
from src.validators import validate_all_rows
from src.automation.web_automation import run_automation, WebAutomationError

logger = setup_logger(__name__)


def parse_arguments():
    """Parse argumentos de linha de comando."""
    parser = argparse.ArgumentParser(
        description="Automação de Cadastro de Produtos - Preenche formulário via Playwright"
    )
    
    parser.add_argument(
        "--file", "-f",
        type=str,
        required=True,
        help="Caminho para arquivo Excel (.xlsx, .xls, .xlsm, .ods)"
    )
    
    parser.add_argument(
        "--headless",
        action="store_true",
        default=False,
        help="Executar navegador em modo headless (background)"
    )
    
    parser.add_argument(
        "--skip-validation",
        action="store_true",
        default=False,
        help="Pular validação e processar todos os dados"
    )
    
    return parser.parse_args()


def validate_file_argument(filepath):
    """Valida se o arquivo informado existe e tem formato válido."""
    path = Path(filepath)
    
    if not path.exists():
        logger.error(f"Arquivo não encontrado: {filepath}")
        sys.exit(1)
    
    valid_extensions = {".xlsx", ".xls", ".xlsm", ".ods"}
    if path.suffix.lower() not in valid_extensions:
        logger.error(f"Formato não suportado: {path.suffix}")
        sys.exit(1)
    
    return str(path)


def print_validation_report(valid_rows, invalid_rows):
    """Exibe relatório de validação."""
    print("\n" + "=" * 80)
    print("RELATÓRIO DE VALIDAÇÃO")
    print("=" * 80)
    print(f"[OK] Linhas válidas: {len(valid_rows)}")
    print(f"✗ Linhas inválidas: {len(invalid_rows)}")
    
    if invalid_rows:
        print("\nDetalhes das linhas inválidas:")
        for row_idx, errors in invalid_rows:
            print(f"  Linha {row_idx}:")
            for error in errors:
                print(f"    - {error}")
    
    print("=" * 80 + "\n")


def print_execution_report(total_processed, total_success, total_failed):
    """Exibe relatório final de execução."""
    print("\n" + "=" * 80)
    print("RELATÓRIO FINAL DE EXECUÇÃO")
    print("=" * 80)
    print(f"Total de registros processados: {total_processed}")
    print(f"[OK] Sucessos: {total_success}")
    print(f"✗ Falhas: {total_failed}")
    print(f"Taxa de sucesso: {(total_success/total_processed*100):.1f}%" if total_processed > 0 else "N/A")
    print("=" * 80 + "\n")


async def main_async(filepath, headless=False, skip_validation=False):
    """Função principal assíncrona."""
    try:
        # 1. Ler e validar arquivo Excel
        logger.info("PASSO 1: Lendo arquivo Excel...")
        rows, columns = read_and_validate(filepath)
        log_execution_start(logger, filepath, len(rows))
        
        # 2. Validar dados
        logger.info("PASSO 2: Validando dados...")
        if skip_validation:
            valid_rows = rows
            invalid_rows = []
            logger.warning("Validação pulada (skip-validation ativado)")
        else:
            valid_rows, invalid_rows = validate_all_rows(rows)
        
        print_validation_report(valid_rows, invalid_rows)
        
        # Se não há linhas válidas, parar
        if not valid_rows:
            logger.error("Nenhuma linha válida para processar. Abortando.")
            sys.exit(1)
        
        # Perguntar confirmação se há linhas inválidas
        if invalid_rows and not skip_validation:
            response = input(f"\n{len(invalid_rows)} linhas inválidas serão ignoradas. Continuar? (s/n): ")
            if response.lower() != "s":
                logger.info("Execução cancelada pelo usuário.")
                sys.exit(0)
        
        # 3. Executar automação
        logger.info(f"PASSO 3: Iniciando automação (processarão {len(valid_rows)} linhas)...")
        total_processed, total_success, total_failed = await run_automation(valid_rows)
        
        # 4. Exibir relatório
        print_execution_report(total_processed, total_success, total_failed)
        log_execution_end(logger, total_processed, total_success, total_failed)
        
        return 0 if total_failed == 0 else 1
    
    except ExcelReaderError as e:
        logger.error(f"Erro ao ler Excel: {str(e)}")
        sys.exit(1)
    
    except WebAutomationError as e:
        logger.error(f"Erro de automação web: {str(e)}")
        sys.exit(1)
    
    except KeyboardInterrupt:
        logger.warning("Execução interrompida pelo usuário (Ctrl+C)")
        sys.exit(130)
    
    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}", exc_info=True)
        sys.exit(1)


def main():
    """Função principal - entry point."""
    print("=" * 80)
    print("AUTOMAÇÃO DE CADASTRO DE PRODUTOS")
    print("Preenchimento automático de formulário com Playwright")
    print("=" * 80 + "\n")
    
    # Parse argumentos
    args = parse_arguments()
    
    # Validar arquivo
    filepath = validate_file_argument(args.file)
    
    # Executar automação assíncrona
    exit_code = asyncio.run(main_async(filepath, args.headless, args.skip_validation))
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
