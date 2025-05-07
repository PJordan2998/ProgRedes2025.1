#Entrada do número ip e máscara da rede#
ip = input("Digite o endereço IPv4 ").strip()
bits = int(input("Digite a máscara em bits (ex: 24): ").strip())

ip_num = 0
for parte in ip.split('.'):
    ip_num = (ip_num << 8) + int(parte)

<<<<<<< HEAD
mascara = (0xFFFFFFFF << (32 - bits)) & 0xFFFFFFFF if bits > 0 else 0


=======
>>>>>>> 6025364beef561228aa5ddba4c34976bf24f2d19
