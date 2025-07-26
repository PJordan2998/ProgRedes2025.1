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

def enviar_parcial(conn, caminho, offset):
# Calcula o tamanho restante a ser enviado
    tamanho = os.path.getsize(caminho) - offset   
# Envia confirmação e tamanho restante      
    conn.sendall(f"OK {tamanho}\n".encode())   
# Abre o arquivo em modo binário         
    with open(caminho, 'rb') as f:    
# Move o ponteiro para o offset informado                  
        f.seek(offset)                                  
        while True:
# Lê um bloco a partir do offset
            dados = f.read(BUFFER)                      
            if not dados:
                break
# Envia o bloco lido  
            conn.sendall(dados)     

def enviar_md5(conn, caminho, offset, qtd_bytes):
    try:
# Abre o arquivo em modo binário
        with open(caminho, 'rb') as f:    
# Move o ponteiro para o offset              
            f.seek(offset)   
# Lê a quantidade de bytes solicitada                            
            dados = f.read(qtd_bytes)    
# Calcula o hash MD5 dos dados lidos             
        md5 = hashlib.md5(dados).hexdigest()    
 # Envia o resultado para o cliente       
        conn.sendall(f"MD5 {md5}\n".encode())   
# Em caso de erro, envia mensagem de erro                                            
    except Exception as e:
        conn.sendall(f"ERRO {str(e)}\n".encode())       