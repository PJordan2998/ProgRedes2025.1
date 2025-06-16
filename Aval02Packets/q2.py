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


# Encontra o primeiro diretório da imagem#
offset_ifd0 = ler_32bits(dados_exif, 4)
dados_ifd0 = dados_exif[offset_ifd0:]
quantidade_tags = ler_16bits(dados_ifd0, 0)

offset_gps_info = None

# Localiza a localização do GPS #
for i in range(quantidade_tags):
    pos = 2 + i * 12
    identificador_tag = ler_16bits(dados_ifd0, pos)
    if identificador_tag == 0x8825:
        offset_gps_info = ler_32bits(dados_ifd0, pos + 8)
        break

if offset_gps_info is None:
    print("Erro: A imagem não contém informações de localização GPS.")
    sys.exit()

dados_gps = dados_exif[offset_gps_info:]
quantidade_tags_gps = ler_16bits(dados_gps, 0)

# Inicializa dados de coordenadas
latitude = longitude = None
referencia_lat = referencia_lon = None