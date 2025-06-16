# módulo para manipulação de argumentos #
# módulo para processar #

import sys
import subprocess

# Analiza argumentos #
if len(sys.argv) < 2:
    print("Uso correto: python localizar_imagem.py imagem.jpg")
    sys.exit()

# Armazena o nome do arquivo JPEG passado como argumento #
caminho_imagem = sys.argv[1]

# Faz a leitura da imagem em binário #
with open(caminho_imagem, 'rb') as arquivo_imagem:
# Lê todo o conteúdo do arquivo JPEG #
    conteudo = arquivo_imagem.read()

# Verifica se o cabeçalho EXIF está presente no conteúdo#
if b'Exif' not in conteudo:
    print("Erro: Dados EXIF não encontrados na imagem.")
    sys.exit()

# Encontra o início efetivo dos dados EXIF, pulando "Exif\0\0" #
inicio_dados_exif = conteudo.find(b'Exif') + 6
# Extrai somente os dados EXIF da imagem #
dados_exif = conteudo[inicio_dados_exif:]

# Os dois primeiros bytes do EXIF indicam o endianness ordem dos bytes#
cabecalho = dados_exif[:2]
# 'II' indica little endian, caso contrário é big endian #
modo_little_endian = cabecalho == b'II'

# Funções para leitura de inteiros de 16 e 32 bits com base no endianness #
if modo_little_endian:
    ler_16bits = lambda b, o: b[o] + (b[o+1] << 8)
    ler_32bits = lambda b, o: b[o] + (b[o+1] << 8) + (b[o+2] << 16) + (b[o+3] << 24)
else:
    ler_16bits = lambda b, o: (b[o] << 8) + b[o+1]
    ler_32bits = lambda b, o: (b[o] << 24) + (b[o+1] << 16) + (b[o+2] << 8) + b[o+3]


# Encontra o primeiro diretório da imagem#
# Lê o deslocamento (offset) para o primeiro diretório IFD0 #
offset_ifd0 = ler_32bits(dados_exif, 4)
 # Extrai os dados IFD0 #
dados_ifd0 = dados_exif[offset_ifd0:]
# Lê o número de entradas (tags) no IFD0 #
quantidade_tags = ler_16bits(dados_ifd0, 0)
# Inicializa a variável que guardará o deslocamento da seção GPS #
offset_gps_info = None

# Procura a entrada com ID 0x8825, que contém informações GPS #
for i in range(quantidade_tags):
# Cada tag tem 12 bytes; os 2 primeiros bytes são o número total de tags #
    pos = 2 + i * 12
# Lê o ID da tag #
    identificador_tag = ler_16bits(dados_ifd0, pos)
# Se for a tag GPSInfo #
    if identificador_tag == 0x8825:
# Pega o valor do offset para a IFD GPS #
        offset_gps_info = ler_32bits(dados_ifd0, pos + 8)
        break
# Se não encontrou a tag de GPS, exibe erro e sai #
if offset_gps_info is None:
    print("Erro: A imagem não contém informações de localização GPS.")
    sys.exit()

#  Extrai os dados do diretório GPS #
dados_gps = dados_exif[offset_gps_info:]
# Lê o número de entradas GPS #
quantidade_tags_gps = ler_16bits(dados_gps, 0)

# Inicializa variáveis que armazenarão os dados de coordenadas #
latitude = longitude = None
referencia_lat = referencia_lon = None

# Percorre todas as entradas GPS procurando latitude, longitude e suas referências #
for i in range(quantidade_tags_gps):
    pos = 2 + i * 12
    id_tag = ler_16bits(dados_gps, pos)
    tipo_dado = ler_16bits(dados_gps, pos + 2)
    total_valores = ler_32bits(dados_gps, pos + 4)
    offset_valores = ler_32bits(dados_gps, pos + 8)