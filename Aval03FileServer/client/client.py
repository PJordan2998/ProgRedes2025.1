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