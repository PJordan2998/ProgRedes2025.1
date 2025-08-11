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
        resposta = requests.get(url, params=parametros, timeout=15)
        resposta.raise_for_status()
        return resposta.json()
    except Exception as erro:
        print(f"Erro ao obter atualizações: {erro}")
        return {}