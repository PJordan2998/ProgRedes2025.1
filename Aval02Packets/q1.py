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

# Abre o arquivo pcap em modo leitura binária #
with open(nome_arquivo, 'rb') as arquivo_pcap:
# Lê e descarta o cabeçalho global do pcap 24 bytes #
    arquivo_pcap.read(24)  

    while True:
# Lê o cabeçalho de cada pacote 16 bytes #
        cabecalho_pacote = arquivo_pcap.read(16)  
        if len(cabecalho_pacote) < 16:
            break 

# retira informações do cabeçalho do pacote timestamp e tamanho #
        tempo_seg, tempo_usec, tam_incluido, tam_original = struct.unpack('=IIII', cabecalho_pacote)

# Lê os dados do pacote #
        dados_pacote = arquivo_pcap.read(tam_incluido)

        if len(dados_pacote) < 14:
# Ignora pacotes menores que o cabeçalho Ethernet #
            continue  

        print("\n" + "=" * 70)
        print("Pacote lido ({} bytes)".format(len(dados_pacote)))

# Lê mac de destino e origem 6 bytes #
        mac_destino = ':'.join('{:02x}'.format(b) for b in dados_pacote[0:6])   
        mac_origem = ':'.join('{:02x}'.format(b) for b in dados_pacote[6:12])  
# Extrai o tipo do protocolo 2 bytes # 
        tipo_ethernet = struct.unpack('!H', dados_pacote[12:14])[0]     
# Separa o restante para a camada de rede #        
        dados_rede = dados_pacote[14:]                                          

        print("[Camada Enlace - Ethernet]")
        print(f"  ➜ MAC de Origem : {mac_origem}")
        print(f"  ➜ MAC de Destino: {mac_destino}")
        print(f"  ➜ Tipo Ethernet : {tipo_ethernet:#06x}")