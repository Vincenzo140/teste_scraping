import requests

#TODO verificar como a consulta é feita manualmente na busca de paciente e tentar implementar isso
#TODO possivelmente login não é feito  com sucesso pois 'lumIsLoggedUser': 'false' e cookie não altera


# Criar uma sessão para manter os cookies entre requisições
session = requests.Session()

# Headers para simular um navegador real
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Referer": "https://saude.sulamericaseguros.com.br/prestador/login/"
}

# URL base  da página de login 
login_url = "https://saude.sulamericaseguros.com.br/prestador/login/"

# 1. Acessar a página de login para capturar cookies iniciais
print("Acessando a página de login...")
response = session.get(login_url, headers=headers)

# Verificar os cookies iniciais
cookies_before_login = session.cookies.get_dict()
print("Cookies iniciais:", cookies_before_login)

# Dados com informação  de login
payload = {
    "user": "master",
    "senha": "837543",
    "code": "100000009361"
}

# 3. Enviar a requisição POST com as credenciais
print("Enviando credenciais...")
response = session.post(login_url, data=payload, headers=headers)

#verificar oque aparece apos o login
print("Resposta do login:", response.text[:5000])


# 4. Verificar se o login foi bem-sucedido
cookies_after_login = session.cookies.get_dict()
print("Cookies após login:", cookies_after_login)

if response.status_code == 200 or response.status_code == 302:
    print("Requisição de login deu certo", response.status_code)
else:
    print(f'Falha no login. Status code: {response.status_code}')
    print("Resposta:", response.text)
    exit()

#  Busca do paciente
consulta_url = "https://saude.sulamericaseguros.com.br/prestador/servicos-medicos/contas-medicas/faturamento-tiss-3/faturamento/guia-de-consulta/"
headers["Referer"] = login_url
carteira_number = "55788888485177660015"

# Acessar a página de consulta
response = session.get(consulta_url, headers=headers)
if response.status_code != 200:
    print(f"Falha ao acessar a página de consulta. Status code: {response.status_code}")
    exit()

"""
o Site é separado por 5 input boxes e são separados por numeros limites de numeros, por exemplo o primeiro só aceita 
3 digitos o segundo apenas 5 e por ai vai
"""
search_payload = {
    "tipo-guia": "consulta",
    "validaCampoVermelho": "",
    "codigo-beneficiario-1": carteira_number[:3],
    "codigo-beneficiario-2": carteira_number[3:8],
    "codigo-beneficiario-3": carteira_number[8:12],
    "codigo-beneficiario-4": carteira_number[12:16],
    "codigo-beneficiario-5": carteira_number[16:]
}

headers["Referer"] = consulta_url
response = session.post(consulta_url, data=search_payload, headers=headers)



# Verificar resultado
if response.status_code == 200:
    print("Consulta realizada com sucesso.")
    if carteira_number in response.text:
        print(f"Paciente com carteira '{carteira_number}' encontrado.")
    else:
        print("Paciente não encontrado na resposta.")
else:
    print(f"Falha na consulta. Status code: {response.status_code}")