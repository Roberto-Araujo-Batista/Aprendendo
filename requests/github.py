#requests com github.com
import requests, base64

#trazendo o arquivo readme.md do diretório "Aprendendo"
link = 'https://api.github.com/repos/roberto-araujo-batista/Aprendendo/contents/readme.md'
entrada = requests.get(link).json()
sha = entrada['sha']  #será usado para fazer o post
conteudo = entrada['content']

#por padrão o github utiliza base64 para transferir os dados
convertido = base64.b64decode(conteudo.encode('ascii'))
print(convertido.decode('utf-8'))



#agora aprendendo a fazer o post para o mesmo diretório lido

'''
    "message": "Uma mensagem de commit",
    "content": "O conteúdo do arquivo em base64",
    "branch": "O nome do branch onde fazer o commit",
    "sha": "o hash do arquivo (se já existente)"
'''

arquivo = open('readme.md', 'r')
content = arquivo.read()
arquivo.close()

content = base64.b64encode(content.encode())

authorization = input('authorization para fazer o post: ')

headers = {
           'authorization' : authorization, 
           'message' : 'testando o post',
           'content' : content,
           'branch'  : 'main',
           'sha'     : sha
           }

#formato do post:
#PUT /repos/{owner}/{repo}/contents/{path}

owner = 'roberto-araujo-batista'
repo  = 'Aprendendo'
path  = 'requests/'
link_post = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'

response = requests.post(link_post, headers=headers)


print(f"Status Code: {response.status_code}")
