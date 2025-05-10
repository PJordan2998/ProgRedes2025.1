# Solicitação do ip da rede e dos bits da máscara de rede ao usuário #
ip = input("Digite o endereço IPv4 ").strip()
bits = int(input("Digite a máscara em bits: ").strip())

# Conversão do IP da rede para número inteiro #
ip_num = 0
for parte in ip.split('.'):
    ip_num = (ip_num << 8) + int(parte)

# Calcula a máscara da rede #
mascara = (0xFFFFFFFF << (32 - bits)) & 0xFFFFFFFF if bits > 0 else 0

# Calcula os endereços da rede #
rede = ip_num & mascara
broadcast = rede | (~mascara & 0xFFFFFFFF)
gateway = broadcast - 1 if bits < 31 else broadcast

# Calcula o número de hosts da rede #
if bits == 32:
    hosts = 1
elif bits == 31:
    hosts = 2
else:
    hosts = (1 << (32 - bits)) - 2

# Função para converter número para IP #
def num_para_ip(num):
    return '.'.join(str((num >> shift) & 0xFF) for shift in (24, 16, 8, 0))

# Apresenta o Endereço de rede, broadcast, gateway e hosts #
print(f"Rede:       {num_para_ip(rede)}")
print(f"Broadcast:  {num_para_ip(broadcast)}")
print(f"Gateway:    {num_para_ip(gateway)}")
print(f"Hosts:      {hosts}")

