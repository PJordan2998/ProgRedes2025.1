# módulo para manipulação de argumentos #
# módulo para processar #

import sys
import subprocess

# Analiza argumentos #
if len(sys.argv) < 2:
    print("Uso correto: python localizar_imagem.py imagem.jpg")
    sys.exit()

caminho_imagem = sys.argv[1]

# Faz a leitura da imagem em binário #
with open(caminho_imagem, 'rb') as arquivo_imagem:
    conteudo = arquivo_imagem.read()

if b'Exif' not in conteudo:
    print("Erro: Dados EXIF não encontrados na imagem.")
    sys.exit()
