import time, hashlib, struct

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
    
    print(f"{'Texto a validar':<25} {'Bits em zero':<10} {'Nonce':<15} {'Tempo (em s)':<12}")
    
    for texto, bits in tabela:
        dados = texto.encode('utf-8')
        nonce, hash_hex, tempo = findNonce(dados, bits)
        
        texto_tabela = texto if len(texto) <= 30 else texto[:17] + "..."
        print(f"{texto_tabela:<25} {bits:<10} {nonce:<15} {tempo:.6f}")
