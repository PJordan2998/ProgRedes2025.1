#Entrada do número ip e máscara da rede#
ip = input("Digite o IPv4 (ex: 192.168.1.100): ").strip()
bits = int(input("Digite a máscara em bits (ex: 24): ").strip())

ip_num = 0
for parte in ip.split('.'):
    ip_num = (ip_num << 8) + int(parte)

