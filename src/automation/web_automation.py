"""
Automação web com Playwright para preencher e submeter formulários.
"""

import asyncio
import time
from typing import Dict, Optional
from playwright.async_api import async_playwright, Browser, Page, BrowserContext
from src.config import (
    TARGET_URL, BROWSER_TYPE, HEADLESS_MODE, TIMEOUT_MS,
    WAIT_AFTER_SUBMIT, MAX_RETRIES, RETRY_DELAY_MS, FORM_SELECTORS
)
from src.logger import setup_logger

logger = setup_logger(__name__)


class WebAutomationError(Exception):
    """Exceção customizada para erros de automação web."""
    pass


class FormAutomation:
    """
    Classe responsável por automatizar o preenchimento e submissão do formulário.
    Utiliza Playwright para interação com o navegador.
    """
    
    def __init__(self, headless: bool = HEADLESS_MODE):
        """
        Inicializa a automação web.
        
        Args:
            headless: Se True, navegador roda em background sem interface
        """
        self.headless = headless
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.playwright = None
    
    async def init_browser(self):
        """Inicializa o navegador e contexto."""
        try:
            logger.info(f"Inicializando navegador: {BROWSER_TYPE} (headless={self.headless})")
            self.playwright = await async_playwright().start()
            
            # Selecionar browser
            if BROWSER_TYPE == "firefox":
                self.browser = await self.playwright.firefox.launch(headless=self.headless)
            elif BROWSER_TYPE == "webkit":
                self.browser = await self.playwright.webkit.launch(headless=self.headless)
            else:  # chromium (default)
                self.browser = await self.playwright.chromium.launch(headless=self.headless)
            
            self.context = await self.browser.new_context()
            self.page = await self.context.new_page()
            self.page.set_default_timeout(TIMEOUT_MS)
            
            logger.info("Navegador inicializado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao inicializar navegador: {str(e)}")
            raise WebAutomationError(f"Falha ao inicializar navegador: {str(e)}")
    
    async def close_browser(self):
        """Fecha o navegador e libera recursos."""
        try:
            if self.page:
                await self.page.close()
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
            logger.info("Navegador fechado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao fechar navegador: {str(e)}")
    
    async def navigate_to_form(self):
        """Navega para a URL do formulário."""
        try:
            logger.info(f"Navegando para: {TARGET_URL}")
            await self.page.goto(TARGET_URL, wait_until="networkidle")
            logger.info("Página carregada com sucesso")
        except Exception as e:
            logger.error(f"Erro ao navegar: {str(e)}")
            raise WebAutomationError(f"Falha ao carregar página: {str(e)}")
    
    async def fill_field_with_retry(self, field_id: str, value: str, retry_count: int = 0) -> bool:
        """
        Preenche um campo com retry automático em caso de falha.
        
        Args:
            field_id: ID do campo HTML
            value: Valor a preencher
            retry_count: Contador interno de tentativas
        
        Returns:
            True se preencheu com sucesso
        """
        try:
            selector = f"#{field_id}"
            
            # Esperar elemento estar visível
            await self.page.wait_for_selector(selector, timeout=TIMEOUT_MS)
            
            # Limpar campo
            await self.page.fill(selector, "")
            
            # Preencher com valor
            await self.page.fill(selector, str(value))
            
            # Verificar se valor foi preenchido
            filled_value = await self.page.input_value(selector)
            if filled_value != str(value):
                raise ValueError(f"Valor não foi preenchido corretamente em {field_id}")
            
            logger.debug(f"Campo {field_id} preenchido com: {value}")
            return True
        
        except Exception as e:
            if retry_count < MAX_RETRIES:
                logger.warning(f"Tentativa {retry_count + 1}/{MAX_RETRIES} falhou para {field_id}. Aguardando...")
                await asyncio.sleep(RETRY_DELAY_MS / 1000)
                return await self.fill_field_with_retry(field_id, value, retry_count + 1)
            
            logger.error(f"Erro ao preencher {field_id}: {str(e)}")
            raise WebAutomationError(f"Falha ao preencher campo {field_id}: {str(e)}")
    
    async def select_radio_button(self, option: str) -> bool:
        """
        Seleciona um botão de rádio (Sim ou Não).
        
        Args:
            option: "Sim" ou "Não"
        
        Returns:
            True se selecionado com sucesso
        """
        try:
            if option.lower() == "sim":
                selector = FORM_SELECTORS['radiob1']
            else:
                selector = FORM_SELECTORS['radiob2']
            
            await self.page.wait_for_selector(selector, timeout=TIMEOUT_MS)
            await self.page.click(selector)
            
            logger.debug(f"Radio button '{option}' selecionado")
            return True
        
        except Exception as e:
            logger.error(f"Erro ao selecionar radio button: {str(e)}")
            raise WebAutomationError(f"Falha ao selecionar opção '{option}': {str(e)}")
    
    async def fill_form(self, data: Dict[str, any]) -> bool:
        """
        Preenche todos os campos do formulário com os dados fornecidos.
        
        Args:
            data: Dicionário com os dados {campo: valor}
        
        Returns:
            True se preenchimento foi bem-sucedido
        """
        try:
            logger.info("Iniciando preenchimento do formulário...")
            
            # Preencher campo Produto
            if "Produto" in data:
                await self.fill_field_with_retry("campo1", data["Produto"])
            
            # Preencher campo Fornecedor
            if "Fornecedor" in data:
                await self.fill_field_with_retry("campo2", data["Fornecedor"])
            
            # Preencher campo Categoria
            if "Categoria" in data:
                await self.fill_field_with_retry("campo3", data["Categoria"])
            
            # Preencher campo Valor Unitário
            if "Valor Unitário" in data:
                await self.fill_field_with_retry("campo4", str(data["Valor Unitário"]))
            
            # Selecionar radio button Notificar
            if "Notificar a Cada Venda?" in data:
                await self.select_radio_button(str(data["Notificar a Cada Venda?"]))
            
            logger.info("Formulário preenchido com sucesso")
            return True
        
        except Exception as e:
            logger.error(f"Erro ao preencher formulário: {str(e)}")
            raise WebAutomationError(f"Falha ao preencher formulário: {str(e)}")
    
    async def submit_form(self) -> bool:
        """
        Clica no botão de submissão e aguarda o resultado.
        
        Returns:
            True se submissão foi bem-sucedida
        """
        try:
            logger.info("Submetendo formulário...")
            
            # Esperar botão estar disponível
            submit_button = FORM_SELECTORS["submit_button"]
            await self.page.wait_for_selector(submit_button, timeout=TIMEOUT_MS)
            
            # Clicar no botão
            await self.page.click(submit_button)
            
            # Aguardar processamento
            await asyncio.sleep(WAIT_AFTER_SUBMIT / 1000)
            
            logger.info("Formulário submetido com sucesso")
            return True
        
        except Exception as e:
            logger.error(f"Erro ao submeter formulário: {str(e)}")
            raise WebAutomationError(f"Falha ao submeter formulário: {str(e)}")
    
    async def process_row(self, row_data: Dict[str, any]) -> bool:
        """
        Processa uma linha completa: navega, preenche e submete.
        
        Args:
            row_data: Dicionário com os dados da linha
        
        Returns:
            True se processamento foi bem-sucedido
        """
        try:
            # Preencher formulário
            await self.fill_form(row_data)
            
            # Submeter
            await self.submit_form()
            
            return True
        
        except WebAutomationError:
            raise
        except Exception as e:
            logger.error(f"Erro ao processar linha: {str(e)}")
            raise WebAutomationError(f"Erro ao processar linha: {str(e)}")


async def run_automation(rows: list) -> tuple:
    """
    Função wrapper para executar automação com context manager.
    
    Args:
        rows: Lista de dicionários com dados a processar
    
    Returns:
        Tupla (total_processed, total_success, total_failed)
    """
    automation = FormAutomation()
    total_success = 0
    total_failed = 0
    
    try:
        # Inicializar navegador
        await automation.init_browser()
        
        # Navegar para página
        await automation.navigate_to_form()
        
        # Processar cada linha
        for idx, row in enumerate(rows, start=1):
            try:
                logger.info(f"Processando linha {idx}/{len(rows)}...")
                await automation.process_row(row)
                total_success += 1
                logger.info(f"[OK] Linha {idx} processada com sucesso")
            
            except WebAutomationError as e:
                total_failed += 1
                logger.error(f"✗ Linha {idx} falhou: {str(e)}")
    
    finally:
        await automation.close_browser()
    
    return len(rows), total_success, total_failed
