#Entrada do número ip e máscara da rede#
ip = input("Digite o endereço IPv4 ").strip()
bits = int(input("Digite a máscara em bits (ex: 24): ").strip())

ip_num = 0
for parte in ip.split('.'):
    ip_num = (ip_num << 8) + int(parte)

mascara = (0xFFFFFFFF << (32 - bits)) & 0xFFFFFFFF if bits > 0 else 0

rede = ip_num & mascara
broadcast = rede | (~mascara & 0xFFFFFFFF)
gateway = broadcast - 1 if bits < 31 else broadcast

if bits == 32:
    hosts = 1
elif bits == 31:
    hosts = 2
else:
    hosts = (1 << (32 - bits)) - 2

def num_para_ip(num):
    return '.'.join(str((num >> shift) & 0xFF) for shift in (24, 16, 8, 0))

print("\nResultados:")
print(f"Rede:       {num_para_ip(rede)}")
print(f"Broadcast:  {num_para_ip(broadcast)}")
print(f"Gateway:    {num_para_ip(gateway)}")
print(f"Hosts:      {hosts}")

