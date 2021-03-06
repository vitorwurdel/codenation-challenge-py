import requests
import json
import hashlib

# Faz o request para receber as informações e formata o request para JSON
req = requests.get('https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token=MEU_TOKEN')
r = req.json()

#Cria o arquivo "answer.json" e popula o arquivo com as informações do request
with open('answer.json', 'w') as arquivo :
    json.dump(r, arquivo, indent=4)

# Funções que Descriptografa ou Criptografa 
def Criptografa(texto, ncasas):
    return ''.join([char if char in ' ,.' else chr((ord(char) + ncasas - 97) % 26 + 97) for char in texto.lower()])

def Descriptografa(texto, ncasas):
    return ''.join([char if char in ' ,.' else chr((ord(char) - ncasas - 97) % 26 + 97) for char in texto.lower()])

# Seleciona os campos a serem utilizados para realizar a descriptografia
descriptografado = Descriptografa(r['cifrado'], r['numero_casas'])

# Faz o resumo 
resumocripto = hashlib.sha1(descriptografado.encode())

r['decifrado'] = descriptografado
r['resumo_criptografico'] = resumocripto.hexdigest()


#Abre o arquivo e salva com os novos dados
with open('answer.json', 'w') as arquivo :
    json.dump(r, arquivo, indent=4)

#Envia resposta via POST

token = ''
params = {'token' : token}

url = 'https://api.codenation.dev/v1/challenge/dev-ps/submit-solution'
answer = {'answer': open('answer.json', 'rb')}
env = requests.post(url, files=answer, params=params)
print(env.status_code)
print(env.text)

