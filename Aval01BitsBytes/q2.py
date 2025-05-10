import time, hashlib, struct

def contar_bits_zero_iniciais(bytes_hash):
    contador = 0
    for byte in bytes_hash:
        if byte == 0:
            contador += 8
        else:
            
            for i in range(7, -1, -1):
                if (byte >> i) & 1:
                    break
                contador += 1
            break
    return contador
