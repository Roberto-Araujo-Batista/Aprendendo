import socket, os, json

def enviar_arquivos():
    print('ainda não foi feito')

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
        print('-------------- ESPERANDO SOLICITAÇÕES ----------------')
        con, cliente = tcp_socket.accept()
        print(f'conectado a {cliente}')

        operacao = con.recv(2)
        operacao = int.from_bytes(operacao)
        print(operacao)
        
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
            enviar_arquivos()
        if operacao == 50:
            #solicita uma lista de arquivos para download
            enviar_arquivos()
        else:
            print('Essa operação não existe!')

main()

