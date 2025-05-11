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
