import socket, os

print('-' * 20 + ' SERVIDOR DISPONÍVEL ' + '-' * 20)

host = ''
port = 60000

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.bind((host, port))  # especifica qual porta e ip da máquina receber as solicitações

tcp_socket.listen(1)

continuar = 1

while continuar:

    print('Aguardando solicitação...')

    # recebe primeiro byte(tamanho do nome do arquivo)
    # recvfrom sempre recebe os bytes e o adrress do solicitante
    # adress = ip e porta do solicitante

    con, cliente = tcp_socket.accept()

    tamanho_arquivo = con.recv(1)

    tamanho_arquivo = int.from_bytes(tamanho_arquivo)

    nome_arquivo = con.recv(tamanho_arquivo)
    nome_arquivo = nome_arquivo.decode('utf-8') 

    print('-' * 20 + ' INFORMAÇÕES DA SOLICITAÇÃO ' + '-' * 20)

    print(f'''
    nome:               {nome_arquivo}
    ip cliente:         {cliente[0]}
    porta cliente:      {cliente[1]}
    ''')

    status = 0
    status = status.to_bytes()

    if os.path.isfile(nome_arquivo):
        status = 1
        status = status.to_bytes()
        con.send(status)
        print('Arquivo encontrado')

        # mandar tamanho do arquivo, no máximo 4 bytes
        tamanho_arquivo = os.path.getsize(nome_arquivo).to_bytes(4)
        con.send(tamanho_arquivo)
        tamanho_arquivo = int.from_bytes(tamanho_arquivo)

        print(f'Tamanho do arquivo: {tamanho_arquivo}')
        # ler o arquivo para mandar
        try:
            arquivo = open(nome_arquivo, 'rb')
            while tamanho_arquivo > 0:
                enviar = arquivo.read(4096)
                con.send(enviar)
                tamanho_arquivo = tamanho_arquivo - 4096
            arquivo.close()

        except:
            print('erro ao abrir arquivo para enviar')


    else:
        con.send(status)
        print('Arquivo não encontrado')


con.close()
print('Fim da execução')
