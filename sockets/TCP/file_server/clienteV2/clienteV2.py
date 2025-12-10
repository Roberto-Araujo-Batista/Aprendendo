import socket

host = '127.0.0.1'
port = 20000


#estabelecendo conexão
def main():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((host, port))

    opcao = input('digite uma opção: ')  
    opcao = opcao.encode()

    print(opcao)
    tcp_socket.send(opcao)

    lista_json = tcp_socket.recv(4096)
    lista_json = lista_json.decode()
    
    print(lista_json)


    tcp_socket.close()

main()