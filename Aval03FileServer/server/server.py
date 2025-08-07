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

def enviar_por_mascara(conn, mascara):
# Lista todos os arquivos no diretório
    arquivos = os.listdir(PASTA)                        
    for nome in arquivos:
# Verifica se o nome corresponde ao padrão
        if fnmatch.fnmatch(nome, mascara):    
# Monta o caminho completo do arquivo          
            caminho = os.path.join(PASTA, nome)   
# Obtém o tamanho do arquivo      
            tamanho = os.path.getsize(caminho)         
# Informa início do envio 
            conn.sendall(f"ARQUIVO {nome} TAMANHO {tamanho}\n".encode()) 
# Abre o arquivo em modo binário
            with open(caminho, 'rb') as f:              
                while True:
# Lê um bloco do arquivo
                    dados = f.read(BUFFER)              
                    if not dados:
                        break
# Envia o bloco lido
                    conn.sendall(dados)     
# Informa o fim da transferência            
    conn.sendall(b"FIM\n")                              

def tratar_cliente(conn, addr):
# Mostra que um cliente se conectou
    print(f"[+] Conexão de {addr}")                     
    try:
        while True:
# Recebe uma linha de comando do cliente
            linha = conn.recv(BUFFER).decode()  
# Se não receber nada, encerra o loop        
            if not linha:                               
                break
# Divide a linha em partes
            partes = linha.strip().split()
# Se não houver comando, continua              
            if not partes:                              
                continue
# Pega o comando enviado
            cmd = partes[0]                             

            if cmd == 'DIR':
# Monta a lista de arquivos
                lista = '\n'.join(os.listdir(PASTA)) + '\n' 
# Envia a lista para o cliente
                conn.sendall(lista.encode())                
            elif cmd == 'DOW' and len(partes) == 2:
# Pega o nome do arquivo solicitado
                nome = partes[1]                
# Monta o caminho completo           
                caminho = os.path.join(PASTA, nome)  
# Verifica se o arquivo existe      
                if os.path.exists(caminho):       
# Envia o arquivo         
                    enviar_arquivo(conn, caminho)          
                else:
# Arquivo não existe
                    conn.sendall("ERRO Arquivo não encontrado\n".encode('utf-8')) 
            elif cmd == 'DRA' and len(partes) == 3:
# Pega o nome e o offset
                nome, offset = partes[1], int(partes[2])   
# Monta o caminho completo
                caminho = os.path.join(PASTA, nome)     
# Verifica se o arquivo existe   
                if os.path.exists(caminho):    
# Envia a partir do offset            
                    enviar_parcial(conn, caminho, offset)  
                else:
                    conn.sendall("ERRO Arquivo não encontrado\n".encode('utf-8'))

            elif cmd == 'MD5' and len(partes) == 4:
# Pega os parâmetros
                nome, offset, tamanho = partes[1], int(partes[2]), int(partes[3]) 
# Monta o caminho completo
                caminho = os.path.join(PASTA, nome)     
# Verifica se o arquivo existe   
                if os.path.exists(caminho):                
# Calcula e envia o MD5
                    enviar_md5(conn, caminho, offset, tamanho) 
                else:
                    conn.sendall("ERRO Arquivo não encontrado\n".encode('utf-8'))

            elif cmd == 'DMA' and len(partes) == 2:
# Pega a máscara de arquivos
                mascara = partes[1]          
# Envia todos os arquivos que combinam
                enviar_por_mascara(conn, mascara)         
            else:
# Comando não reconhecido
                conn.sendall(b"ERRO Comando desconhecido\n") 
    except Exception as e:
# Mostra erro ocorrido com o cliente
        print(f"[ERRO] Cliente {addr}: {e}")               
    finally:
# Fecha a conexão com o cliente
        conn.close()                               
# Informa que a conexão foi fechada        
        print(f"[-] Conexão encerrada com {addr}")         

def main():
# Garante que a pasta de arquivos existe
    os.makedirs(PASTA, exist_ok=True)             
# Cria o socket do servidor         
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor: 
# Associa o socket ao endereço e porta
        servidor.bind((HOST, PORT))  
# Coloca o socket em modo de escuta                      
        servidor.listen()    
# Mensagem de status                              
        print(f"[SERVIDOR] Aguardando conexões na porta {PORT}...") 
        while True:
# Aceita uma nova conexão
            conn, addr = servidor.accept()   
# Chama a função para tratar o cliente              
            tratar_cliente(conn, addr)                     
#            
if __name__ == '__main__':
    main()                                                 
  