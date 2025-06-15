# módulo para manipulação de argumentos #
# módulo para interpretar dados binários pcap #
import sys 
import struct 

# Dicionário com os principais tipos ICMP #
tipos_icmp = {
    0: "Echo Reply",
    3: "Destination Unreachable",
    5: "Redirect",
    8: "Echo Request",
    11: "Time Exceeded"
}

# Analiza se o usuário forneceu o nome do arquivo pcap na linha de comando #
if len(sys.argv) < 2:
    print("Modo de uso: python3 analisador_pcap.py <arquivo.pcap>")
# Encerra o programa se não for pcap #
    sys.exit(1) 

# pega o arquivo informado #
nome_arquivo = sys.argv[1]