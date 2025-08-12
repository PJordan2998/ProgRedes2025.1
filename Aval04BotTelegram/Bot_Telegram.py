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

def obter_atualizacoes(token, offset=None):
    url = f'https://api.telegram.org/bot{token}/getUpdates'
    parametros = {'timeout': 3, 'offset': offset}
    try:
        resposta = requests.get(url, params=parametros, timeout=3)
        resposta.raise_for_status()
        return resposta.json()
    except Exception as erro:
        print(f"Erro ao obter atualizações: {erro}")
        return {}

def enviar_mensagem(token, id_chat, texto):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    dados = {'chat_id': id_chat, 'text': texto}
    try:
        requests.post(url, data=dados, timeout=3)
    except Exception as erro:
        print(f"Erro ao enviar mensagem: {erro}")
