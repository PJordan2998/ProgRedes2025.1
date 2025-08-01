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

#  ARP / RARP #
# Se for protocolo ARP (0x0806), extrai: Operação (1 = request, 2 = reply) e MAC e IP do remetente e destinatário #
        if tipo_ethernet == 0x0806 and len(dados_rede) >= 28:
# Código ARP ou RARP #
            codigo_operacao = struct.unpack('!H', dados_rede[6:8])[0]  
            remetente_mac = ':'.join('{:02x}'.format(b) for b in dados_rede[8:14])
            remetente_ip = '.'.join(str(b) for b in dados_rede[14:18])
            destinatario_mac = ':'.join('{:02x}'.format(b) for b in dados_rede[18:24])
            destinatario_ip = '.'.join(str(b) for b in dados_rede[24:28])

            print("[Camada Rede - ARP/RARP]")
            print(f"  ➜ Código de operação: {codigo_operacao} ({'ARP' if codigo_operacao in [1, 2] else 'RARP'})")
            print(f"  ➜ Remetente         : MAC {remetente_mac}, IP {remetente_ip}")
            print(f"  ➜ Destinatário      : MAC {destinatario_mac}, IP {destinatario_ip}")

#  IPv4 #
# Se for protocolo IPv4 (0x0800), extrai dados #
        elif tipo_ethernet == 0x0800 and len(dados_rede) >= 20:
# Versão e tamanho do cabeçalho #
            versao_ihl = dados_rede[0]
# Extrai tamanho do cabeçalho #                            
            tamanho_cabecalho = (versao_ihl & 0x0F) * 4
# TTL #          
            tempo_de_vida = dados_rede[8]
# Protocolo (1 = ICMP, 6 = TCP, 17 = UDP) #                         
            protocolo = dados_rede[9]                             
            ip_origem = '.'.join(str(b) for b in dados_rede[12:16])
            ip_destino = '.'.join(str(b) for b in dados_rede[16:20])
# Tamanho total do pacote #
            tamanho_total = struct.unpack('!H', dados_rede[2:4])[0]
# Dados da camada de transporte #  
            dados_transporte = dados_rede[tamanho_cabecalho:]        

            print("[Camada Rede - IPv4]")
            print(f"  ➜ IP de Origem : {ip_origem}")
            print(f"  ➜ IP de Destino: {ip_destino}")
            print(f"  ➜ TTL          : {tempo_de_vida}")
            print(f"  ➜ Protocolo    : {protocolo}")
            print(f"  ➜ Tamanho Total: {tamanho_total} bytes | Cabeçalho: {tamanho_cabecalho} bytes")

#  ICMP #
# Se for ICMP, extrai dados #
            if protocolo == 1 and len(dados_transporte) >= 8:
# Tipo do ICMP #
                tipo_icmp = dados_transporte[0]     
# Código ICMP #                           
                codigo_icmp = dados_transporte[1]         
# ID #                     
                identificador = struct.unpack('!H', dados_transporte[4:6])[0]  
# Sequência #
                sequencia = struct.unpack('!H', dados_transporte[6:8])[0] 
# Nome legível #     
                nome_icmp = tipos_icmp.get(tipo_icmp, f"Tipo {tipo_icmp}")     

                print("[Camada Transporte - ICMP]")
                print(f"  ➜ Tipo        : {nome_icmp} ({tipo_icmp})")
                print(f"  ➜ Código      : {codigo_icmp}")
# Echo Request ou Reply #
                if tipo_icmp in [0, 8]:  
                    print(f"  ➜ Identificador: {identificador}")
                    print(f"  ➜ Sequência    : {sequencia}")

#  UDP #
# Extrai portas de origem e destino do cabeçalho UDP #
            elif protocolo == 17 and len(dados_transporte) >= 8:
# Portas #
                porta_origem, porta_destino = struct.unpack('!HH', dados_transporte[:4])  
                print("[Camada Transporte - UDP]")
                print(f"  ➜ Porta de Origem : {porta_origem}")
                print(f"  ➜ Porta de Destino: {porta_destino}")

#  TCP #
# Extrai dados #
            elif protocolo == 6 and len(dados_transporte) >= 20:
                porta_origem, porta_destino, numero_seq, numero_ack, dados_flags = struct.unpack('!HHIIH', dados_transporte[:14])
# Tamanho do cabeçalho TCP #
                tamanho_tcp = (dados_flags >> 12) * 4   
# Flags (SYN, ACK) #                    
                flags_tcp = dados_flags & 0x01FF                
#  Tamanho da janela #           
                janela_tcp = struct.unpack('!H', dados_transporte[14:16])[0] 
# Dados da camada de aplicação #
 
                dados_aplicacao = dados_transporte[tamanho_tcp:]              
                print("[Camada Transporte - TCP]")
                print(f"  ➜ Porta de Origem : {porta_origem}")
                print(f"  ➜ Porta de Destino: {porta_destino}")
                print(f"  ➜ Número Seq      : {numero_seq}")
                print(f"  ➜ Número ACK      : {numero_ack}")
                print(f"  ➜ Flags           : {flags_tcp:#04x}")
                print(f"  ➜ Janela          : {janela_tcp}")

# Se flag ACK estiver e tiver carga de dados #
                if flags_tcp & 0x10 and dados_aplicacao:
                    print("[Camada Aplicação - Dados]")
                    print(f"  ➜ Dados (máx. 200 bytes): {dados_aplicacao[:200]}")

