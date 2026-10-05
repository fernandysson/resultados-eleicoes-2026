#!/usr/bin/env sh

set -exu

echo "=== Baixa arquivo do TSE com dados dos locais de votação ==="
echo ""
echo "Com eles vocês conseguem identificar  os locais de cada seção eleitoral"

DEST="datasets"
mkdir -p $DEST
cd $DEST
wget https://cdn.tse.jus.br/estatistica/sead/odsele/eleitorado_locais_votacao/eleitorado_local_votacao_2026.zip
unzip eleitorado_local_votacao_2026.zip
rm eleitorado_local_votacao_2026.zip
