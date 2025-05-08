import hashlib
import time

testes = [
    ("Texto curto", 8),
    ("Texto curto", 16),
    ("Texto médio com mais caracteres", 12),
    ("Texto médio com mais caracteres", 18),
    ("Texto grande para teste de performance com nonce difícil", 20),
    ("Texto grande para teste de performance com nonce difícil", 22)
]

print(f"{'TEXTO':<40} {'BITS':<6} {'NONCE':<10} {'TEMPO(s)':<8}")
print("-" * 70)

for texto, bits in testes:
    alvo = 1 << (256 - bits)
    inicio = time.time()
    nonce = 0

 while True:
        dados = nonce.to_bytes(4, 'big') + texto.encode()
        hash_resultado = hashlib.sha256(dados).digest()
        valor_hash = int.from_bytes(hash_resultado, 'big')
        
