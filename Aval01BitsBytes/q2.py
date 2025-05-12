# Importa as bibliotecas que vamos precisar para executar o programa #
import time, hashlib, struct

# Função principal que executa mostra os resultados #
def principal():
    tabela = [("Esse um texto elementar", 8),
        ("Esse um texto elementar", 10),
        ("Esse um texto elementar", 15),
        ("Textinho", 8),
        ("Textinho", 18),
        ("Textinho", 22),
        ("Meu texto médio", 18),
        ("Meu texto médio", 19),
        ("Meu texto médio", 20)]
    
# Cabeçalho da tabela #
    print(f"{'Texto a validar':<25} {'Bits em zero':<10} {'Nonce':<15} {'Tempo (em s)':<12}")

# Laço que percorre cada par (texto, bits) da tabela #    
    for texto, bits in tabela:

# Transforma o texto em bytes usando UTF-8 #
        dados = texto.encode('utf-8')

# função findNonce retorna o inteiro do noce encontrado que satisfaz, o hash em formato hexadecimal e o tempo total da busca #
        nonce, hash_hex, tempo = findNonce(dados, bits)
        
# Formata o texto #
        texto_tabela = texto if len(texto) <= 30 else texto[:17] + "..."
        print(f"{texto_tabela:<25} {bits:<10} {nonce:<15} {tempo:.6f}")

# Função que conta quantos bits zero existem no início do hash #
def contar_bits_zero_iniciais(bytes_hash):

# Inicializa o contador de bits zero #
    contador = 0
    for byte in bytes_hash:
    
# Se o byte for 0x00, então todos os 8 bits são zero → soma 8 ao contador #
        if byte == 0:
            contador += 8
        else:

# Conta os bits zero no primeiro byte não-zero #
            for i in range(7, -1, -1):
                if (byte >> i) and 1:
                    break
                contador += 1
            break

# Retorna o número total de bits zero consecutivos no início do hash #
    return contador

# Encontra um nonce que faz o hash começar com a quantidade especificada de bits zero #
def findNonce(dataToHash, bitsToBeZero):

# Marca o tempo de início da busca #
    tempo_inicial = time.time()
    nonce = 0

# Laço infinito até encontrar um nonce válido #
    while True:
# Prepara os nonce de 4 bytes big-endian + dados #
        dados_nonce = struct.pack('>I', nonce) + dataToHash
        
# Calcula o hash #
        result_hash = hashlib.sha256(dados_nonce).digest()
        
# Verificação dos bits zero iniciais #
        if contar_bits_zero_iniciais(result_hash) >= bitsToBeZero:
            tempo_de_execucao = time.time() - tempo_inicial
            return (nonce, result_hash.hex(), tempo_de_execucao)
        nonce += 1

# Inicia a função principal, caso o programa seja exacutado corretamente #
if __name__ == "__main__":
    principal()
