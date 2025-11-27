import socket, os 

host = ''
port = 60000

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((host, port)) #especifica qual porta e ip da máquina receber as solicitações

enviado = False
while not enviado:

    
    print('Esperando solicitação...')

    #recebe primeiro byte(tamanho do nome do arquivo)
    #recvfrom sempre recebe os bytes e o adrress do solicitante
    #adress = ip e porta do solicitante
    tamanho_arquivo , cliente = udp_socket.recvfrom(1) 
    tamanho_arquivo = int.from_bytes(tamanho_arquivo)
    
    print('-' *30)
    print(f'''
    Tamanho do arquivo: {tamanho_arquivo}
    ip cliente:         {cliente[0]}
    porta cliente:      {cliente[1]}
    ''')

    nome_arquivo, cliente = udp_socket.recvfrom(tamanho_arquivo)
    print('-' *30)
    
    print(f'''
    nome:               {nome_arquivo}
    ip cliente:         {cliente[0]}
    porta cliente:      {cliente[1]}
    ''')


    
    if os.path.isfile(nome_arquivo):
        udp_socket.sendto(b'1', cliente)
        print('Arquivo encontrado')

        enviado = True

    else:
        udp_socket.sendto(b'0', cliente)        
        print('Arquivo não encontrado')

        enviado = True  

    print('Fim da execução')