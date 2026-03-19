# Projeto Python para Automação

Um projeto Python moderno e bem estruturado, pronto para desenvolvimento.

## 🚀 Início Rápido

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. **Crie um ambiente virtual:**
   ```bash
   python -m venv .venv
   ```

2. **Ative o ambiente virtual:**
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source .venv/bin/activate
     ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

### Execução

Execute o projeto com:
```bash
python main.py
```

## 📁 Estrutura do Projeto

```
.
├── main.py              # Arquivo principal da aplicação
├── requirements.txt     # Dependências do projeto
├── README.md            # Este arquivo
├── .gitignore           # Arquivos ignorados pelo Git
└── .github/
    └── copilot-instructions.md  # Instruções para Copilot
```

## 🔧 Desenvolvimento

Para adicionar novas dependências:

1. Instale a biblioteca desejada:
   ```bash
   pip install nome-da-biblioteca
   ```

2. Atualize o arquivo `requirements.txt`:
   ```bash
   pip freeze > requirements.txt
   ```

3. Commit as alterações:
   ```bash
   git add requirements.txt
   git commit -m "Add novo pacote"
   ```

## 📝 Licença

Este projeto é fornecido como template e pode ser usado livremente.

## 👨‍💻 Desenvolvimento

Modificue `main.py` para iniciar seu desenvolvimento!
