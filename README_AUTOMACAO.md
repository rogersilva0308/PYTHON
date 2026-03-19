# Automação de Cadastro de Produtos - Documentação Completa

## 📋 Visão Geral

Sistema de automação que lê dados de arquivo Excel e preenche automaticamente um formulário web em **https://produtize.netlify.app/** usando Playwright.

**Características principais:**
- ✅ Leitura dinâmica de arquivos Excel (.xlsx, .xls, .xlsm, .ods)
- ✅ Validação inteligente de dados antes de enviar
- ✅ Preenchimento automático com retry em caso de falhas
- ✅ Suporte a múltiplos formatos de arquivo sem alteração de código
- ✅ Logging estruturado e relatórios detalhados
- ✅ Tratamento robusto de erros

---

## 🚀 Início Rápido

### 1. **Instalação de Dependências**

```bash
# Instalar dependências Python
.venv\Scripts\pip.exe install -r requirements.txt

# Instalar navegador Playwright
.venv\Scripts\playwright.exe install chromium
```

### 2. **Usar o Sistema**

```bash
# Ejecutar com arquivo padrão
python main.py --file produtos_teste.xlsx

# Sem validação (processar tudo)
python main.py --file seu_arquivo.xlsx --skip-validation

# Modo headless (sem interface visual)
python main.py --file seu_arquivo.xlsx --headless
```

---

## 📂 Estrutura do Projeto

```
PYTHON/
├── main.py                           # Entry point - orquestrador principal
├── requirements.txt                  # Dependências do projeto
├── produtos_teste.xlsx               # Arquivo de exemplo
├── test_connectivity.py              # Script de teste do site
├── README.md                         # Esta documentação
├── logs/                            # Diretório de logs (criado automaticamente)
│   └── automation.log
└── src/
    ├── __init__.py
    ├── config.py                    # Configurações, mapeamento de campos, seletores
    ├── logger.py                    # Sistema de logging
    ├── validators.py                # Validação de dados
    ├── readers/
    │   ├── __init__.py
    │   └── excel_reader.py          # Leitor dinâmico de Excel
    └── automation/
        ├── __init__.py
        └── web_automation.py        # Automação com Playwright
```

---

## 🔧 Configuração

### Arquivo: `src/config.py`

**Importante**: Se você trocar as colunas do Excel ou os IDs/names do formulário HTML, edite este arquivo:

```python
# Mapeamento atual (CUSTOMIZE AQUI se necessário)
FIELD_MAPPING = {
    "Produto": {
        "html_id": "campo1",
        "html_name": "campo_produto",
        "type": "text",
        "required": True,
    },
    "Fornecedor": { ... },
    "Categoria": { ... },
    "Valor Unitário": { ... },
    "Notificar a Cada Venda?": { ... },
}
```

**Mudou o nome de uma coluna?** Só edite o dicionário e pronto! Não precisa mudar nenhum outro código.

---

## 📊 Formatos de Arquivo Suportados

| Formato | Extensão | Suportado |
|---------|----------|-----------|
| Excel 2007+ | .xlsx | ✅ |
| Excel 97-2003 | .xls | ✅ |
| Excel com Macros | .xlsm | ✅ |
| OpenDocument | .ods | ✅ |
| CSV | .csv | ❌ |

---

## 🔍 Campos da Planilha (Excel)

A planilha **DEVE** conter estas colunas (nomes exatamente iguais):

| Coluna | Tipo | Obrigatório | Exemplo |
|--------|------|-----------|---------|
| **Produto** | Texto | Sim | "Água Tradicional 250g" |
| **Fornecedor** | Texto | Sim | "Suprimentos Itajaí" |
| **Categoria** | Texto | Sim | "Limpeza" |
| **Valor Unitário** | Número | Sim | 48.43 |
| **Notificar a Cada Venda?** | Texto | Não | "Sim" ou "Não" |

**Notas:**
- Valores vazios em colunas obrigatórias causarão erro
- Linhas inválidas serão puladas (com relatório)
- A automação está preparada para 100 linhas de dados

---

## 🛠️ Uso e Exemplos

### Executar Automação

```bash
# Básico
python main.py --file produtos_teste.xlsx

# Com mais opções
python main.py -f /caminho/completo/para/dados.xlsx --headless --skip-validation
```

### Argumentos CLI

```
--file, -f          : Caminho do arquivo Excel (OBRIGATÓRIO)
--headless          : Executar sem interface visual
--skip-validation   : Ignorar validação e processar tudo
```

---

## 📋 Validação de Dados

A automação valida automaticamente cada linha contra estas regras:

| Campo | Regra |
|-------|-------|
| Produto | 1-255 caracteres |
| Fornecedor | 1-255 caracteres |
| Categoria | 1-255 caracteres |
| Valor Unitário | 0.00 - 999999.99 |
| Notificar | "Sim" ou "Não" |

**Se houver erros:**
1. Serão listados no console
2. Você poderá confirmar se quer continuar
3. Linhas inválidas serão puladas
4. Tudo será registrado em `logs/automation.log`

---

## 📝 Fluxo de Execução

```
1. Validar argumentos CLI
↓
2. Ler arquivo Excel
↓
3. Validar colunas do Excel
↓
4. Validar cada linha (dados)
↓
5. Mostrar relatório de validação
↓
6. Pedir confirmação (se há inválidos)
↓
7. Inicializar navegador Playwright
↓
8. Navegar para site
↓
9. Para cada linha válida:
   - Preencher campos
   - Submeter formulário
   - Aguardar resposta
↓
10. Gerar relatório final
↓
11. Fechar navegador
```

---

## 🔍 Testando o Sistema

### Teste de Conectividade

Antes de executar a automação completa, teste se o site está respondendo:

```bash
python test_connectivity.py
```

**Saída esperada:**
```
[OK] Site carregado com sucesso
[OK] campo1: #campo1 - encontrado
[OK] campo2: #campo2 - encontrado
... (etc)
[OK] Teste de conectividade concluido com sucesso!
```

### Teste de Leitura de Excel

```bash
python -c "from src.readers.excel_reader import read_and_validate; rows, cols = read_and_validate('produtos_teste.xlsx'); print(f'Linhas: {len(rows)}'); print(f'Primeira: {rows[0]}')"
```

---

## 📊 Relatórios e Logs

### Arquivo de Log: `logs/automation.log`

Contém histórico completo de:
- Tentativas de leitura
- Erros de validação
- Preenchimentos de formulário
- Submissões
- Erros de rede/timeout

**Localização:** `c:\Users\m908789\Desktop\SISTEMAS\PYTHON\logs\automation.log`

---

## ⚙️ Personalização Avançada

### Mudar Mapeamento de Campos

Se o formulário do site mudar (novos campos, IDs diferentes):

1. Abra [src/config.py](src/config.py)
2. Edite `FIELD_MAPPING` com novos mapeamentos
3. Execute normalmente

### Mudar Validação

Para mudar regras de validação:

1. Abra [src/validators.py](src/validators.py)
2. Edite `VALIDATION_RULES` em [src/config.py](src/config.py)
3. Execute novamente

### Modo Debug

Para ativar logs mais detalhados:

```python
# Em src/config.py, mude:
LOG_LEVEL = "DEBUG"  # ao invés de "INFO"
```

---

## 🚨 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'pandas'"

```bash
# Reinstale dependências
pip install -r requirements.txt
```

### Erro: "Arquivo não encontrado"

```bash
# Verifique o caminho
python main.py --file ./produtos_teste.xlsx
```

### Navegador não abre / Timeout

```bash
# Teste conectividade primeiro
python test_connectivity.py

# Se falhar, site pode estar offline
```

### Linhas sendo puladas

```bash
# Verifique o relatório de validação
# Procure por mensagens como "Coluna X inválida"
# Corrija os dados no Excel
```

---

## 📌 Notas Importantes

1. **Colunas do Excel**: Devem ter nomes **exatamente** como mapeados em `config.py`
2. **Dados válidos**: Valores vazios em campos obrigatórios causam erro
3. **Performance**: Para 100+ linhas, considere usar `--headless`
4. **Timeout**: Site com lentidão pode gerar timeouts (configurável em `config.py`)
5. **Segurança**: Não exponha credenciais em argumentos CLI

---

## 🔄 Reutilização com Outros Arquivos

A solução é **100% reutilizável** para qualquer arquivo Excel com mesma estrutura:

```bash
# Mesmo arquivo, dados diferentes = funciona automaticamente
python main.py --file vendas_janeiro.xlsx
python main.py --file vendas_fevereiro.xlsx
python main.py --file novos_produtos.xlsx
```

Se a estrutura de colunas mudar, apenas edite `src/config.py` e execute novamente.

---

## 📞 Support

Para questões, verifique:
1. Logs em `logs/automation.log`
2. Relatório de validação no console
3. Teste de conectividade com `test_connectivity.py`

---

**Versão**: 1.0.0  
**Data**: 18 de março de 2026  
**Status**: ✅ Pronto para produção
