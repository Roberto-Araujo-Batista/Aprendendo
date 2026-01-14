import socket, os, json
import threading

DEBUG = True    

def enviar_arquivos():
    print('------ Download de arquivos -----')
    print('operação: 10')

    #recebendo tamanho do nome do arquivo e nome do arquivo para procurar na pasta
    tamanho_nome = con.recv(4)
    tamanho_nome = int.from_bytes(tamanho_nome)

    nome_arquivo = con.recv(tamanho_nome)
    nome_arquivo = nome_arquivo.decode()
    print(f'Nome do arquivo solicitado: {nome_arquivo}')
    
    #criando caminho para encontrar o arquivo na pasta
    caminho_arquivo = f'arquivos/{nome_arquivo}'

    lista_arquivos = os.listdir('arquivos')
    #verificando se arquivo existe para enviá-lo
    if nome_arquivo in lista_arquivos:
        print('esse aquivo existe! Preparar para enviar')

        #enviando status para dizer que arquivo existe
        status = int.to_bytes(0)
        con.send(status)

        #enviando tamanho do arquivo
        tamanho_arquivo = os.path.getsize(caminho_arquivo)
        tamanho_arquivoe = int.to_bytes(tamanho_arquivo, 4)
        con.send(tamanho_arquivoe)

        #enviando arquivo
        arquivo = open(caminho_arquivo, 'rb')
        while tamanho_arquivo > 0:
            dados = arquivo.read(1024)
            con.send(dados)
            tamanho_arquivo = tamanho_arquivo - 1024
        arquivo.close()


    else:
        status = int.to_bytes(1)
        con.send(status)
        print('arquivo não encontrado')


def listar_arquivos():
    try: #deu certo, enviar 0 
        
        print('-'*10 +' listar Arquivos ' + '-' *10)
        
        lista = os.listdir('arquivos')
        lista_json  = []

        arquivo = 0
        while arquivo < len(lista):
            dic_lista = {}
            tamanho_aquivo       = os.path.getsize(f'arquivos/{lista[arquivo]}')
            dic_lista['nome']    = lista[arquivo] 
            dic_lista['tamanho'] = tamanho_aquivo
            
            lista_json = lista_json + [dic_lista]
            arquivo = arquivo + 1
        
        #exibindo a lista
        pos = 0
        while pos < len(lista_json):
            dic = lista_json[pos]
            print(f"Arquivo: {dic['nome']} \nTamanho: {dic['tamanho']}")
            print('-'*10)
            pos = pos +1

        #enviando código de confirmação:
        status = int.to_bytes(0)
        con.send(status)


        #transformando em uma str formato json para enviar
        lista_json = json.dumps(lista_json)
        lista_json = lista_json.encode()

        #enviando tamanho do json antes do json
        tamanho_json = len(lista_json)
        tamanho_json = tamanho_json.to_bytes(4, 'big')
        con.send(tamanho_json)

        #enviando json
        con.send(lista_json)

    except:
        #enviando status: 
        print('deu erro enviar 1')    
        status = int.to_bytes(1)
        con.send(status)


def receber_arquivos():
    print('----- Recebendo Arquivos -----')
    
    tamanho_nome = con.recv(4)
    tamanho_nome = int.from_bytes(tamanho_nome)
    
    nome_arquivo = con.recv(tamanho_nome)
    nome_arquivo = nome_arquivo.decode()
    
    print(f'Foi solicitado o upload do arquivo chamado: {nome_arquivo}\n1.sim\n0.não')
    opcao = int(input('Você deseja permitir o upload desse arquivo?'))

    if opcao == 1:
        print('Operação aceita, baixando arquivo...')
        status = int.to_bytes(0)
        con.send(status)
        
        #recebendo arquivo
        arquivo = open(nome_arquivo, 'wb')
        while tamanho_arquivo > 0:
            dados = con.recv(10240)
            arquivo.write(dados)
            tamanho_arquivo -= 1024
        arquivo.close()

    else:
        print('Operação negada, infomando ao cliente...')
        status = int.to_bytes(1)
        con.send(status)










def enviar_partes_arquivos():
    #recebendo tamanho do nome e nome do arquvio
    tamanho_nome = con.recv(4)
    nome_arquivo = con.recv(int.from_bytes(tamanho_nome))
    nome_arquivo = nome_arquivo.decode()

    if DEBUG: print(tamanho_nome, nome_arquivo)

    if os.path.isfile(f'arquivos/{nome_arquivo}'): #verifica se o arquivo existe
        print('arquivo existe!!')


    print(f'{cliente} está fazendo o download do arquivo: {nome_arquivo}')    















def enviar_varios_arquivos():
    print('ainda não foi feito')


#estabelecendo conexão
def main():
    global con, cliente

    host = ''
    port = 20000

    #configurando para ser um socket tcp
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #configurando para deixar em modo passivo(modo de servidor)
    tcp_socket.bind((host, port))
    tcp_socket.listen(1)

    while True:
        try:
            print('-------------- ESPERANDO SOLICITAÇÕES ----------------')
            con, cliente = tcp_socket.accept()
            print(f'conectado a {cliente}')

            operacao = con.recv(1)
            operacao = int.from_bytes(operacao)
            
            if operacao == 10:
                #solicita o download de um arquivo
                enviar_arquivos()
            if operacao == 20:
                #lista arquivos
                listar_arquivos()
            if operacao == 30:
                #solicita upload de arquivos
                receber_arquivos()
            if operacao == 40:
                #solicita download de um aquivo, especificando até onde enviar
                enviar_partes_arquivos()
            if operacao == 50:
                #solicita uma lista de arquivos para download
                enviar_varios_arquivos()
            else:
                raise ModuleNotFoundError

        except:
            print('Essa operação não existe')

main()
