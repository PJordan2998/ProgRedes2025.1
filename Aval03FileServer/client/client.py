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

# Função para solicitar o cálculo do MD5 parcial
def calcular_md5(conexao, arquivo):     
# Solicita ao usuário o byte inicial                   
    inicio = input("Informe o byte inicial: ")   
# Solicita ao usuário a quantidade de bytes          
    quantidade = input("Informe a quantidade de bytes: ")  
# Envia comando ao servidor
    conexao.sendall(f'MD5 {arquivo} {inicio} {quantidade}\n'.encode()) 
# Exibe o resultado recebido
    print(conexao.recv(TAM_BUFFER).decode())               

# Função para baixar arquivos por padrão/máscara
def baixar_por_mascara(conexao, filtro):     
# Envia comando com o filtro              
    conexao.sendall(f'DMA {filtro}\n'.encode())    
# Loop para receber múltiplos arquivos        
    while True:     
# Recebe resposta do servidor                                       
        resposta = conexao.recv(TAM_BUFFER).decode()  
# Se for o fim da transferência, sai do loop     
        if resposta.startswith("FIM"):                     
            break
# Se for início de um arquivo
        elif resposta.startswith("ARQUIVO"):    
# Divide a resposta em partes           
            partes = resposta.strip().split()      
# Pega o nome do arquivo        
            nome_arq = partes[1]             
# Pega o tamanho do arquivo              
            tam_arq = int(partes[3])               
# Abre o arquivo para escrita        
            with open(nome_arq, 'wb') as destino:   
# Inicializa o total recebido       
                recebido = 0              
# Continua até receber tudo                 
                while recebido < tam_arq:                  
# Recebe bloco de dados
                    dados = conexao.recv(min(TAM_BUFFER, tam_arq - recebido)) 
# Escreve no arquivo
                    destino.write(dados)  
# Atualiza o total recebido                 
                    recebido += len(dados)           
# Informa que o arquivo foi transferido      
            print(f"{nome_arq} transferido.")              
        else:
# Exibe mensagens diversas do servidor
            print(resposta)                                

# Função para exibir o menu de opções ao usuário
def exibir_menu(conexao):      
# Dicionário de opções e funções correspondentes                            
    opcoes = {                                             
        '1': lambda: mostrar_lista(conexao),
        '2': lambda: baixar_arquivo(conexao, input("Nome do arquivo: ")),
        '3': lambda: continuar_download(conexao, input("Nome do arquivo: ")),
        '4': lambda: calcular_md5(conexao, input("Nome do arquivo: ")),
        '5': lambda: baixar_por_mascara(conexao, input("Padrão (*.txt, etc): "))
    }
# Loop principal do menu
    while True:          
# Exibe as opções                                  
        print("\n1 - Listar arquivos")                     
        print("2 - Baixar arquivo")
        print("3 - Retomar download")
        print("4 - MD5 parcial")
        print("5 - Baixar por padrão")
        print("6 - Sair")
# Solicita a escolha do usuário
        escolha = input("Opção: ")                         

# Se escolher sair, encerra o loop
        if escolha == '6':                                 
            break
# Busca a função correspondente à escolha
        acao = opcoes.get(escolha)                         
        if acao:
# Executa a função escolhida
            acao()                                         
        else:
# Informa se a opção for inválida
            print("Escolha inválida.")                     

# Função principal para iniciar o cliente
def iniciar():                         
# Cria o socket TCP                    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conexao: 
        try:
# Tenta conectar ao servidor
            conexao.connect((HOST, PORTA))             
# Exibe o menu de opções    
            exibir_menu(conexao)        
# Captura erros de conexão                   
        except Exception as erro:       
# Exibe mensagem de erro                   
            print(f"Falha na conexão: {erro}")             

if __name__ == '__main__':                                 
    iniciar()                                                