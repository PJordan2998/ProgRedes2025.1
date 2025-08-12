import requests, subprocess, time, threading

TOKENS = [
    '',
    '',
    '',
    '',
    ''
]

USUARIOS_CADASTRADOS = {}
USUARIOS_LOCK = threading.Lock()

# busca atualizações das mensagens do bot, através da URL da API, realiza requisições GET
def obter_atualizacoes(token, offset=None):
    url = f'https://api.telegram.org/bot{token}/getUpdates'
    parametros = {'timeout': 3, 'offset': offset}
    try:
        resposta = requests.get(url, params=parametros, timeout=4)
        resposta.raise_for_status()
        return resposta.json()
    except Exception as erro:
        print(f"Erro ao obter atualizações: {erro}")
        return {}

# Envia mensagens ao chat, através da URL da API
def enviar_mensagem(token, id_chat, texto):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    dados = {'chat_id': id_chat, 'text': texto}
    try:
        requests.post(url, data=dados, timeout=3)
    except Exception as erro:
        print(f"Erro ao enviar mensagem: {erro}")

# Comandos para teste de redes, ping, netstat, route, ipconfig e tracert
def executar_comando(comando, argumentos):
    if comando == '/ping':
        host = argumentos[0] if argumentos else '8.8.8.8'
        try:
            saida = subprocess.check_output(['ping', '-n', '4', host], text=True)
            return saida
        except Exception as erro:
            return f'Erro ao executar ping: {erro}'
    elif comando == '/netstat':
        try:
            saida = subprocess.check_output(['netstat', '-an'], text=True)
            return saida[:3000]
        except Exception as erro:
            return f'Erro ao executar netstat: {erro}'
    elif comando == '/route':
        try:
            saida = subprocess.check_output(['route', 'print'], text=True)
            return saida[:3000]
        except Exception as erro:
            return f'Erro ao executar route: {erro}'
    elif comando == '/ipconfig':
        try:
            saida = subprocess.check_output(['ipconfig'], text=True)
            return saida[:3000]
        except Exception as erro:
            return f'Erro ao executar ipconfig: {erro}'
    elif comando == '/tracert':
        host = argumentos[0] if argumentos else '8.8.8.8'
        try:
            saida = subprocess.check_output(['tracert', host], text=True)
            return saida[:3000]
        except Exception as erro:
            return f'Erro ao executar tracert: {erro}'
    else:
        return 'Comando não reconhecido.'

# Manda mensagem de boas-vindas para usuários que já interagiram com o bot mas ainda não estão cadastrados.
def enviar_boas_vindas_para_chats_ativos():
    for token in TOKENS:
        atualizacoes = obter_atualizacoes(token)
        if 'result' in atualizacoes:
            for item in atualizacoes['result']:
                mensagem = item.get('message')
                if not mensagem:
                    continue
                id_chat = mensagem['chat']['id']
                id_usuario = mensagem['from']['id']
                chave_usuario = (token, id_usuario)
                with USUARIOS_LOCK:
                    if chave_usuario not in USUARIOS_CADASTRADOS:
                        enviar_mensagem(token, id_chat, "Bem-vindo! Por favor, envie seu nome para cadastro.")

#Tratamento de cada usuário/bot, com threads
def bot_thread(token):
    ultimos_id = None
    while True:
        atualizacoes = obter_atualizacoes(token, ultimos_id)
        if 'result' in atualizacoes:
            for item in atualizacoes['result']:
                ultimos_id = item['update_id'] + 1
                mensagem = item.get('message')
                if not mensagem:
                    continue
                id_chat = mensagem['chat']['id']
                texto = mensagem.get('text', '')
                id_usuario = mensagem['from']['id']

                chave_usuario = (token, id_usuario)
                with USUARIOS_LOCK:
                    if chave_usuario not in USUARIOS_CADASTRADOS:
                        if texto.startswith('/start'):
                            enviar_mensagem(token, id_chat, "Bem-vindo! Por favor, envie seu nome para cadastro.")
                        elif texto:
                            USUARIOS_CADASTRADOS[chave_usuario] = texto.strip()
                            enviar_mensagem(token, id_chat, f"Usuário {texto.strip()} cadastrado com sucesso!\nDigite /help para ver os comandos.")
                        continue

                if texto.startswith('/help'):
                    texto_ajuda = (
                        "Comandos disponíveis:\n"
                        "/ping [host] - Testa conectividade\n"
                        "/netstat - Mostra conexões de rede\n"
                        "/route - Mostra tabela de rotas\n"
                        "/ipconfig - Mostra interfaces de rede\n"
                        "/tracert [host] - Mostra rota até o destino"
                        )
                    enviar_mensagem(token, id_chat, texto_ajuda)
                elif texto.startswith('/'):
                    partes = texto.split()
                    comando = partes[0]
                    argumentos = partes[1:]
                    resultado = executar_comando(comando, argumentos)
                    enviar_mensagem(token, id_chat, resultado)
                else:
                    enviar_mensagem(token, id_chat, "Comando não reconhecido. Digite /help para ver os comandos.")
        time.sleep(0.5)

# inicialização dos bots
def principal():
    print("Bots iniciados...")
    enviar_boas_vindas_para_chats_ativos()
    threads = []
    for token in TOKENS:
        t = threading.Thread(target=bot_thread, args=(token,), daemon=True)
        t.start()
        threads.append(t)
    while True:
        time.sleep(0.4)

if __name__ == '__main__':
    principal()
