# Abre a imagem JPEG e lê os primeiros 6 bytes #
with open('IMG_20250509_184205.jpg', 'rb') as imagem:
    leia = imagem.read(6)

# Extrai o app1DataSize das posições 4 e 5 (2 bytes) #
app1DataSize = (leia[4] << 8) + leia[5]

# Fecha #
imagem.close()

# Reabre a imagem e ignora os primeiros 4 bytes #
with open('IMG_20250509_184205.jpg', 'rb') as imagem:
    imagem.read(4) 
# Lê app1DataSize bytes para app1Data #
    app1Data = imagem.read(app1DataSize)
