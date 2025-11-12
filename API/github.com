#requests com github.com
import requests, base64

#trazendo o arquivo readme.md do diretório "Aprendendo"
link = 'https://api.github.com/repos/roberto-araujo-batista/Aprendendo/contents/readme.md'
entrada = requests.get(link).json()
conteudo = entrada['content']

#por padrão o github utiliza base64 para transferir os dados
convertido = base64.b64decode(conteudo.encode('ascii'))
print(convertido.decode('utf-8'))
