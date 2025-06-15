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

inicio_dados_exif = conteudo.find(b'Exif') + 6
dados_exif = conteudo[inicio_dados_exif:]

# Define a ordem dos bytes #
cabecalho = dados_exif[:2]
modo_little_endian = cabecalho == b'II'

# Função para leitura de inteiros #
if modo_little_endian:
    ler_16bits = lambda b, o: b[o] + (b[o+1] << 8)
    ler_32bits = lambda b, o: b[o] + (b[o+1] << 8) + (b[o+2] << 16) + (b[o+3] << 24)
else:
    ler_16bits = lambda b, o: (b[o] << 8) + b[o+1]
    ler_32bits = lambda b, o: (b[o] << 24) + (b[o+1] << 16) + (b[o+2] << 8) + b[o+3]
