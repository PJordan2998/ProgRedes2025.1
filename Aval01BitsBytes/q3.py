Imagem = ''

try:
    with open(imagem, 'rb') as f:
        leitura = f.read(6)
      
        if leitura [0] != 0xFF or leitura [1] != 0xD8:
            print("Erro: Arquivo não é um JPEG válido")
            exit()
