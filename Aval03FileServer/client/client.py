import socket, os
# endereço do servidor
HOST = 'localhost'    
# porta do servidor       
PORTA = 50000     
# tamanho do buffer           
TAM_BUFFER = 4096            

# Função para baixar um arquivo do servidor
def baixar_arquivo(conexao, arquivo):      
# Envia comando para solicitar o arquivo                
    conexao.sendall(f'DOW {arquivo}\n'.encode())       
# Recebe a resposta do servidor    
    resposta = conexao.recv(TAM_BUFFER).decode()    
# Verifica se a resposta é positiva       
    if resposta.startswith("OK"):   
# Pega o tamanho do arquivo informado pelo servidor                      
        tam = int(resposta.split()[1])      
# Abre o arquivo local para escrita em modo binário         
        with open(arquivo, 'wb') as destino: 
# Inicializa o total de bytes recebidos              
            total = 0           
# Continua até receber todo o arquivo                           
            while total < tam:                             
# Recebe um bloco de dados
                bloco = conexao.recv(min(TAM_BUFFER, tam - total))  
# Se não receber nada, interrompe
                if not bloco:                              
                    break
# Escreve o bloco no arquivo
                destino.write(bloco)     
# Atualiza o total de bytes recebidos                 
                total += len(bloco)     
# Informa que o download foi concluído                   
        print("Arquivo baixado com sucesso.")      
# Exibe mensagem de erro recebida do servidor        
    else:
        print(resposta)  

# Função para retomar o download de um arquivo
def continuar_download(conexao, arquivo):           
# Verifica o tamanho já baixado       
    inicio = os.path.getsize(arquivo) if os.path.exists(arquivo) else 0  
# Solicita ao servidor o restante do arquivo
    conexao.sendall(f'DRA {arquivo} {inicio}\n'.encode()) 
# Recebe a resposta do servidor
    resposta = conexao.recv(TAM_BUFFER).decode()        
# Se a resposta for positiva     
    if resposta.startswith("OK"):    
# Pega o tamanho restante a ser baixado               
        restante = int(resposta.split()[1])  
# Abre o arquivo para acrescentar dados              
        with open(arquivo, 'ab') as destino:      
# Inicializa o total de bytes recebidos nesta etapa         
            recebido = 0                        
# Continua até receber tudo               
            while recebido < restante:      
# Recebe um bloco de dados               
                dados = conexao.recv(min(TAM_BUFFER, restante - recebido)) 
# Se não receber nada, interrompe
                if not dados:                              
                    break
# Escreve o bloco no arquivo
                destino.write(dados)    
# Atualiza o total recebido                  
                recebido += len(dados)     
# Informa que o download foi concluído                
        print("Download retomado e finalizado.")           
    else:
# Exibe mensagem de erro recebida do servidor                                  
        print(resposta)                                    

# Função para listar arquivos disponíveis no servidor
def mostrar_lista(conexao):          
# Envia comando de listagem                      
    conexao.sendall(b'DIR\n')           
# Recebe a lista de arquivos                   
    lista = conexao.recv(TAM_BUFFER).decode()       
# Exibe a lista       
    print(lista)                                           
