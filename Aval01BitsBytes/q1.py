# Solicita o ip da rede e dos bits da máscara de rede, além de separar os espaços em branco, com a função strip #
ip = input("Digite o endereço IPv4: ").strip()
bits = int(input("Digite a máscara em bits: ").strip())

# Conversão do IP da rede para número inteiro, através de laço for, separando os quatro octetos por pontos #
ip_num = 0
for parte in ip.split('.'):
    ip_num = (ip_num << 8) + int(parte)

# Calcula a máscara de rede a partir dos bits #
mascara = (0xFFFFFFFF << (32 - bits)) & 0xFFFFFFFF if bits > 0 else 0

# Calcula os endereços da rede #
rede = ip_num & mascara
broadcast = rede | (~mascara & 0xFFFFFFFF)
gateway = broadcast - 1 if bits < 31 else broadcast

# Calcula o número de hosts da rede, se a máscara for bits 32, apenas 1 host é possível, já se for 31 bits 2 IPs possíveis #
# Para máscaras menores tira a rede e o broadcast #
if bits == 32:
    hosts = 1
elif bits == 31:
    hosts = 2
else:
    hosts = (1 << (32 - bits)) - 2

# Função para converter um número inteiro de volta para IPv4, através de deslocamento de bits, para obter cada octeto #
def num_para_ip(num):
    return '.'.join(str((num >> shift) & 0xFF) for shift in (24, 16, 8, 0))

# Apresenta o Endereço de rede, broadcast, gateway e hosts #
print(f"Rede:       {num_para_ip(rede)}")
print(f"Broadcast:  {num_para_ip(broadcast)}")
print(f"Gateway:    {num_para_ip(gateway)}")
print(f"Hosts:      {hosts}")

