# Gerador de Capa

Gerador de capas com IA a partir de um título e de um tema visual.

## Sobre o projeto

Este projeto é uma aplicação Python originalmente desenvolvida para gerar
capas com auxílio de inteligência artificial.

Atualmente, o projeto está sendo utilizado como laboratório de modernização
de código legado, aplicando práticas de Engenharia de Software de forma
incremental.

## Funcionalidades atuais

- Geração de prompt a partir de título e tema visual.
- Geração de imagem por meio da API da OpenAI.
- Decodificação da imagem recebida em Base64.
- Salvamento da imagem em formato PNG.
- Tratamento de falhas esperadas durante a geração e o salvamento da imagem.
- Testes automatizados dos principais fluxos da aplicação.

## Estrutura do projeto

```text
gerador_capa/
├── src/
│   └── gerador_capa/
│       ├── __init__.py
│       └── app.py
├── tests/
│   └── test_app.py
├── pyproject.toml
└── README.md
```

## Requisitos

- Python 3.10 ou superior

## Instalação

Crie e ative um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instale o projeto com as dependências de desenvolvimento:

```powershell
python -m pip install -e ".[dev]"
```
