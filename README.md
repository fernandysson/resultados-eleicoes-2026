# Instruções para execução

## Requisitos
- uv
- wget
- JSON com chaves para fazer upload no Google Spreadsheets

## Sincroniziar projeto

`uv sync`

## Gerar arquivos com dados dos locais de votação 

`bash scripts/download-eleitorado-dataaset-local-votacao.sh`

## Executar para um estado:

`uf=pe python3 main.py`

## Diretórios

- tse_bu: diretório com scripts para decodificação dos BUs
