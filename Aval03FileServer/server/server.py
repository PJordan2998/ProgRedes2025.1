import socket, os, fnmatch, hashlib 

# endereço IP para escutar conexões
HOST = '0.0.0.0'   
# porta para escutar conexões      
PORT = 50000        
# tamanho do buffer de leitura e escrita     
BUFFER = 4096        
# diretório onde os arquivos estão armazenados    
PASTA = 'arquivos'       

def enviar_arquivo(conn, caminho):
# Obtém o tamanho do arquivo
    tamanho = os.path.getsize(caminho)                  
# Envia confirmação e tamanho do arquivo    
    conn.sendall(f"OK {tamanho}\n".encode())            
# Abre o arquivo em modo binário
    with open(caminho, 'rb') as f:                      
        while True:
# Lê um bloco do arquivo
            dados = f.read(BUFFER)                      
            if not dados:                               
                break
# Envia o bloco lido para o cliente
            conn.sendall(dados)                         