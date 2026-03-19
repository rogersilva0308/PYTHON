#!/bin/bash
# Script para instalar e executar o projeto Python

echo "================================================"
echo "   Setup Completo - Projeto Python"
echo "================================================"
echo

# Verificar se Python está instalado
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Python não encontrado no seu sistema!"
    echo "   Por favor, instale Python 3.8 ou superior"
    exit 1
fi

echo "✓ Python encontrado: $($PYTHON_CMD --version)"
echo

# Criar ambiente virtual
echo "Criando ambiente virtual..."
$PYTHON_CMD -m venv .venv
echo "✓ Ambiente virtual criado"
echo

# Ativar ambiente virtual
echo "Ativando ambiente virtual..."
source .venv/bin/activate
echo "✓ Ambiente virtual ativado"
echo

# Instalar dependências
echo "Instalando dependências..."
pip install --upgrade pip
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
    echo "✓ Dependências instaladas"
else
    echo "⚠ Arquivo requirements.txt não encontrado"
fi
echo

# Executar o projeto
echo "================================================"
echo "   Executando o Projeto"
echo "================================================"
echo
$PYTHON_CMD main.py
