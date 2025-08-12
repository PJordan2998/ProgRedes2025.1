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
def obter_atualizacoes_CHAT(token, offset=None):
    url = f'https://api.telegram.org/bot{token}/getUpdates'
    parametros = {'timeout': 3, 'offset': offset}
    try:
        resposta = requests.get(url, params=parametros, timeout=3)
        resposta.raise_for_status()
        return resposta.json()
    except Exception as erro:
        print(f"Erro ao obter atualizações: {erro}")
        return {}

# Envia mensagens ao chat, através da URL da API
def enviar_mensagens(token, id_chat, texto):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    dados = {'chat_id': id_chat, 'text': texto}
    try:
        requests.post(url, data=dados, timeout=3)
    except Exception as erro:
        print(f"Erro ao enviar mensagem: {erro}")

# Comandos para teste de redes, ping, netstat, route, ipconfig e tracert
def executar_comando_redes(comando, argumentos):
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
            return saida[:300]
        except Exception as erro:
            return f'Erro ao executar netstat: {erro}'
    elif comando == '/route':
        try:
            saida = subprocess.check_output(['route', 'print'], text=True)
            return saida[:300]
        except Exception as erro:
            return f'Erro ao executar route: {erro}'
    elif comando == '/ipconfig':
        try:
            saida = subprocess.check_output(['ipconfig'], text=True)
            return saida[:300]
        except Exception as erro:
            return f'Erro ao executar ipconfig: {erro}'
    elif comando == '/tracert':
        host = argumentos[0] if argumentos else '8.8.8.8'
        try:
            saida = subprocess.check_output(['tracert', host], text=True)
            return saida[:300]
        except Exception as erro:
            return f'Erro ao executar tracert: {erro}'
    else:
        return 'Comando não reconhecido.'

# Manda mensagem de boas-vindas para usuários que já interagiram com o bot mas ainda não estão cadastrados.
def enviar_mensagem_inicial_chats_():
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
                        enviar_mensagem(token, id_chat, "Bem-vindo novo usuário! Envie seu nome para cadastro.")
