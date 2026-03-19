#!/usr/bin/env python3
"""
Script de teste - Valida se o site está responsivo e se os seletores HTML funcionam.
"""

import asyncio
from playwright.async_api import async_playwright
from src.config import TARGET_URL, FORM_SELECTORS
from src.logger import setup_logger

logger = setup_logger(__name__)


async def test_site_connectivity():
    """Testa conectividade com o site e valida seletores HTML."""
    
    async with async_playwright() as p:
        logger.info("Iniciando teste de conectividade...")
        
        # Abrir navegador
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            # Navegar para o site
            logger.info(f"Conectando em: {TARGET_URL}")
            await page.goto(TARGET_URL, wait_until="networkidle", timeout=10000)
            logger.info("[OK] Site carregado com sucesso")
            
            # Verificar seletores
            teste_seletores = {
                "campo1": FORM_SELECTORS["campo1"],
                "campo2": FORM_SELECTORS["campo2"],
                "campo3": FORM_SELECTORS["campo3"],
                "campo4": FORM_SELECTORS["campo4"],
                "radiob1": FORM_SELECTORS["radiob1"],
                "radiob2": FORM_SELECTORS["radiob2"],
                "submit": FORM_SELECTORS["submit_button"],
            }
            
            logger.info("\nValidando seletores HTML:")
            for nome, seletor in teste_seletores.items():
                try:
                    elemento = await page.query_selector(seletor)
                    if elemento:
                        logger.info(f"  [OK] {nome}: {seletor} - encontrado")
                    else:
                        logger.warning(f"  [FALLO] {nome}: {seletor} - NAO encontrado")
                except Exception as e:
                    logger.error(f"  [ERRO] {nome}: {seletor} - erro: {e}")
            
            logger.info("\n[OK] Teste de conectividade concluido com sucesso!")
            return True
        
        except Exception as e:
            logger.error(f"[ERRO] Erro ao conectar no site: {e}")
            return False
        
        finally:
            await browser.close()


if __name__ == "__main__":
    logger.info("=" * 80)
    logger.info("TESTE DE CONECTIVIDADE")
    logger.info("=" * 80)
    
    sucesso = asyncio.run(test_site_connectivity())
    
    exit(0 if sucesso else 1)
