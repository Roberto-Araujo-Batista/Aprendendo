#ALUNOS:
#ROBERTO ARAUJO BATISTA, MATRICULA 20251014050041
#RYAN GUILHERME COSTA DE MOURA, MATRICULA 20242014050039

import os #ter acesso ao prompt de comando
import string

#import próprio
from exibicao import *

global alfabeto
alfabeto = list(string.ascii_lowercase)

#criar inicializaRAID:
'''inicializaRAID: Pergunta ao usuário quantos discos serão utilizados em RAID, o tamanho dos discos (o mesmo para todos) 
e o tamanho do bloco. Os arquivos devem ser criados em uma pasta que o usuário também deve informar.

Essa função deve criar um arquivo para cada um dos discos (disco0.bin, disco1.bin, disco2.bin, .... discoX.bin). 
O arquivo discoX.bin representa o disco de paridade (X é antecessor do número de discos informado pelo usuário). 
Cada arquivo representando discos de dados deve ter todo o seu conteúdo zerado, enquanto o arquivo que guarda o disco de 
paridade deve ter os dados calculados pela aplicação do xor dos arquivos de dados;
'''
    
def inicializaRAID():
    #perguntar quantos discos, quantos blocos, e nome da pasta onde serão salvos os discos
    #verificar se pasta já existe e perguntar se quer regravar por cima dela
    global pasta, discos, tamanho_bloco, blocos, total_bytes

    pastaCriada = False
    while not pastaCriada: #enquanto pasta não foi criada
        try:
            discos        = int(input('Quantos discos serão usados? '))
            tamanho       = int(input('Qual o tamanho dos discos(bytes)? '))
            blocos        = int(input('Em quantos blocos cada disco será dividido? '))
            pasta         = input('Qual nome da pasta serão salvos os arquivos? ')
            tamanho_bloco = tamanho // blocos
            total_bytes = discos * tamanho
            criar_pasta()
            pastaCriada = True
    
        except FileExistsError:
            opcao = input('Já existe uma pasta com esse nome, você deseja substituir a pasta? (isso excluirá todos os arquivos de dentro dela)\n(S/N)\n')
            if opcao.lower() == 's':
                pastaRemovida = False
                while not pastaRemovida:
                    try:
                        os.rmdir(pasta)
                        pastaRemovida = True
                        criar_pasta()
                        pastaCriada = True
                    except OSError: #apagar todos os arquivos da pasta antes de excluir
                        for arquivo in os.listdir(pasta):
                            os.remove(f'{pasta}/{arquivo}')
        except Exception as e:
            erro = type(e).__name__
            erro(f'houve um erro na função inicializaRAID, \nErro: {erro}')
            break

def criar_pasta():
    os.mkdir(pasta)
    
    formato = []
    for _ in range(tamanho_bloco):
        formato += [0]
    
    #criar aquivo .bin para cada disco, quantidade de disco + 1 discos chamado discox.bin que será o RAID x=nésimo
    for conta_disco in range(discos+1):
        open(f'{pasta}/disco{conta_disco}.bin', 'x')

    try:
        if discos == 1:
            RAID = 'PRECISA SER FEITO UM RAID1 com redundância'
            print(RAID)


        elif discos > 1: #criar os dados zerados com os identificadores de cada bloco
            conta_disco = 0
            while conta_disco <= discos: #tirando o disco de paridade
                header = []
                #tamaho_header, tamanho_bloco, discos, id_blocos
                #por enquanto os dados que tem
                header = [tamanho_bloco, discos]

                for b in range(blocos):                
                    id_blocos = ord(alfabeto[b]) #será uma letra seguido por número: a0,b0,c0...
                    header += [id_blocos] #já inclui como byte

                #calcular tamanho total do header
                tamanho_header = len(header)
                header.insert(0,tamanho_header+1) #+1 para contar com o tamanho também
                
                #dados completos header + formato
                dados_formatados = header + formato
                dados_formatados = bytes(dados_formatados)

                #formatando os discos:
                arquivo = open(f'{pasta}/disco{conta_disco}.bin', 'wb')
                arquivo.write(dados_formatados)
                arquivo.close()
                conta_disco += 1
            correto('RAID criado com sucesso')

        elif discos < 1:
            raise ValueError

    except ValueError:
        errado('Não é possível criar um RAID com esse número de discos!')
    except Exception as e:
        erro_funcao('criar_pasta', e)

    #formtar o disco de paridade
    atualiza_paridade()


#0. para apenas obterRAID
#1. para construir paridade
#2. para construir disco
#3. para fazer o xor do disco removido
def atualiza_paridade(disco_removido = -1, paridade = 1, posicao = 0):
    global tamanho_header, tamanho_bloco, discos, id_blocos, blocos, total_bytes
    try:
        disco = open(f'{pasta}/disco0.bin', 'rb')
        disco_padrao = 0
        if disco_removido == 0:
            raise FileNotFoundError
    except FileNotFoundError:
        disco = open(f'{pasta}/disco1.bin', 'rb')
        disco_padrao = 1
    except:
        errado('Não é possível atualizar paridade, sem disco padrão encontrado')
        return 0

    #extraindo blocos dos discos
    #lendo cabeçalho
    tamanho_header = int.from_bytes(disco.read(1))
    tamanho_bloco  = int.from_bytes(disco.read(1))
    discos         = int.from_bytes(disco.read(1))
    id_blocos      = disco.read(tamanho_header-3)
    blocos         = len(id_blocos)
    total_bytes = discos * tamanho_bloco * blocos

    disco.seek(0)
    dados_formatados = disco.read(tamanho_header)

    if paridade > 0: #apenas obterRAID será barrado
        try:
            #fazendo primeiro xor para criar lista
            disco.seek(tamanho_header,0)
            xor_list = []
            for b in range(blocos):
                bloco = disco.read(tamanho_bloco)
                bloco_int = int.from_bytes(bloco)
                #acumular todos os xor em uma lista, em que cada elemento é o xor de um bloco
                xor_list += [bloco_int]
            disco.close()

            conta_disco = 1
            while conta_disco < discos:
                if (conta_disco != disco_removido) and (conta_disco != disco_padrao):
                    disco = open(f'{pasta}/disco{conta_disco}.bin', 'rb')
                    disco.seek(tamanho_header)
                    for b in range(blocos):
                        bloco = disco.read(tamanho_bloco)
                        bloco_int = int.from_bytes(bloco)
                        #acumular todos os xor em uma lista, em que cada elemento é o xor de um bloco
                        xor_list[b] = xor_list[b] ^ bloco_int

                    disco.close()
                conta_disco += 1
        except FileNotFoundError:
            errado('Arquivo não encontrado ao extrair dados na função atualiza_paridade')
            return 0
        except Exception as e:
            errado(f'erro ao extrair dados dos discos, {erro_funcao("atualiza_paridade", e)}')
            return 0        

    if paridade == 1: #construir paridade
        try:
            #atualizando a paridade
            disco_par = open(f'{pasta}/disco{discos}.bin', 'wb') #disco paridade = quantidade de discos
            disco_par.write(dados_formatados)
            inicio_bloco = tamanho_header

            for b in range(blocos):
                disco_par.seek(inicio_bloco) #pular o header
                bloco = xor_list[b].to_bytes(tamanho_bloco)
                disco_par.write(bloco)
                inicio_bloco += tamanho_bloco #inicio do próximo bloco 
            
            disco_par.close()
            correto('PARIDADE ATUALIZADA', cls = False)
        
        except FileNotFoundError:
            errado('Arquivo não encontrado ao atualizar paridade na função atualiza_paridade')
            return 0
        except Exception as e:
            errado('Erro ao atualizar paridade')
            erro_funcao('atualiza_paridade', e)
            return 0

    if paridade >= 2: #outras opções para ler o disco de paridade também
        #ler mais o disco de paridade
        disco_par = open(f'{pasta}/disco{discos}.bin', 'r+b') #disco paridade = quantidade de discos
        inicio_bloco = tamanho_header
        for b in range(blocos):
            disco_par.seek(inicio_bloco)
            bloco = disco_par.read(tamanho_bloco)
            bloco_int = int.from_bytes(bloco)
            #acumular todos os xor em uma lista, em que cada elemento é o xor de um bloco
            xor_list[b] = xor_list[b] ^ bloco_int
            inicio_bloco += tamanho_bloco
        disco_par.close()
    if paridade == 2: #reconstruir disco, constroiDiscoRAID
        try:
            #reconstruindo disco
            disco_construir = open(f'{pasta}/disco{disco_removido}.bin', 'wb') #disco paridade = quantidade de discos
            disco_construir.write(dados_formatados)
            inicio_bloco = tamanho_header

            for b in range(blocos):
                disco_construir.seek(inicio_bloco,0) #pular o header
                bloco = xor_list[b].to_bytes(tamanho_bloco)
                disco_construir.write(bloco)
                inicio_bloco += tamanho_bloco #inicio do próximo bloco 
            
            disco_construir.close()
            correto(f'Disco{disco_removido}.bin RECONSTRUÍDO')
        
        except FileNotFoundError:
            errado('Arquivo não encontrado ao atualizar paridade na função atualiza_paridade')
            return 0
        except Exception as e:
            errado('Erro ao atualizar paridade')
            erro_funcao('atualiza_paridade', e)
            return 0
        
    if paridade == 3: #exibe o xor_list para um disco removido
        bloco = xor_list[posicao].to_bytes(tamanho_bloco)
        bloco = bloco.decode(encoding='utf-8')
        output(bloco)

'''obtemRAID: Essa operação pergunta ao usuário as mesmas informações de InicializaRAID, mas em vez criar os arquivos, 
busca os arquivos criados anteriormente com inicializaRAID;
'''
def obtemRAID():
    global pasta
    try:
        pasta = input('Qual nome da pasta que foram salvos os arquivos? ')
        pasta = pasta.strip()
        atualiza_paridade(paridade=0)
        correto('RAID encontrado com sucesso')
    except FileNotFoundError:
        errado(f'{pasta} ainda não foi criado.\n Para criar um RAID do zero use a função {certo('incializaRAID')}')
    except Exception as e:
        erro_funcao('obtemRAID', e)

'''
escreveRAID: Pergunta ao usuário um conjunto de dados a gravar no RAID e a posição onde iniciar a gravação. 
Essa posição pode ser qualquer valor entre zero e o tamanho lógico do RAID -1. Por exemplo, 
se o RAID tem cinco discos (quatro de dados e um de paridade) e o tamanho dos discos é 10000 bytes,
então a posição pode ser qualquer valor entre 0 e 39999. O programa deve identificar em que arquivo(s) gravar os dados e que posição dentro do(s) arquivo(s).

pós a escrita no arquivo correto, o disco de paridade deve ser atualizado;
'''
def escreveRAID():
    try:
        dados           = input('Digite os dados da gravação: ').encode()
        posicao         = 1+int(input(f'Em qual posição você quer iniciar a gravação(0..{(blocos*discos)-1}): '))
        disco, posicao  = encontra_disco(posicao, discos)

        inicio_bloco    = tamanho_header + posicao * tamanho_bloco #inicio do bloco referente aos bytes

        escreve_dados(dados, disco, inicio_bloco)
        correto('Dados gravados com sucesso!')
        atualiza_paridade()

    except NameError:
        errado('Você precisa criar um RAID ou abrir um já pronto para que essa função funcione corretamente.')
    except Exception as e:
        erro = type(e).__name__
        errado(f'Erro na entrada de dados na função escreveRAID.\nErro:{erro}')

def encontra_disco(n, divisor):
    if n < divisor:
        posicao = 0
        return n -1, posicao #sempre disco -1
    elif n >= divisor:
        disco = n% divisor
        posicao = n//divisor
        if disco == 0:
            return discos-1, posicao-1  #gravar no último disco útil
        else:
            return disco-1, posicao
    else:
        return 'a conta não bate'
    
    
def escreve_dados(dados, conta_disco, inicio_bloco):
    try:
        disco = open(f'{pasta}/disco{conta_disco}.bin', 'r+b')
        #verificar se já há dados gravados, se sim, perguntar se quer realmente prosseguir

        disco.seek(inicio_bloco)
        if len(dados) <= tamanho_bloco: #se os dados couberem em um bloco, simplesmente grave-os
            disco.write(dados)
            disco.close()
            return True
        else:
            primeira_parte = dados[:tamanho_bloco]
            disco.write(primeira_parte)
            resto = dados[tamanho_bloco:]
            disco.close()

            if conta_disco == discos-1: #se for ultimo disco útil, volte o disco com bloco diferente
                conta_disco = 0
                inicio_bloco += tamanho_bloco
            else:  #se ainda não for último disco, prossiga no mesmo bloco em discos diferentes
                conta_disco += 1
            escreve_dados(resto, conta_disco, inicio_bloco)

    except Exception as e:
        erro_funcao('criar_pasta', e)
'''
leRAID: Pergunta ao usuário informações sobre dados a ler do RAID. O usuário informa a posição e quantos bytes ler. 
A lógica para encontrar o arquivo de onde ler é a mesma da escrita.
A paridade não necessita ser atualizada;
'''
def leRAID():
    global disco_removido
    try:
        posicao        = 1+int(input(f'Em qual posição, você quer iniciar a leitura(0..{(blocos*discos)-1})? '))
        disco, posicao = encontra_disco(posicao,discos)
        inicio_bloco   = tamanho_header + posicao * tamanho_bloco #inicio do bloco referente aos bytes
        tamanho        = int(input('Quantos bytes você quer ler? '))

        disco_removido = encontra_discoremovido()        
        correto('RETORNO DOS DADOS: \n')
        le_dados(tamanho, disco, inicio_bloco)
        input(f'\n\nPressione {certo('Enter')} para voltar ao menu')
    except NameError:
        errado('Você precisa criar um RAID ou abrir um já pronto para que essa função funcione corretamente.')
    except RecursionError: #caso digite mais bytes que o tamanho do disco
        input(f'\n\nPressione {certo('Enter')} para voltar ao menu')
        return 0
    except Exception as e:
        erro = type(e).__name__
        print('Erro na entrada de dados, na função leRAID.\nErro:', erro)
        
def encontra_discoremovido():
    #primeiro saber se tem algum disco removido
    diretorio = os.listdir(f'{pasta}')
    #procurar disco_removido
    if len(diretorio) < discos +1: #verificando se tem disco_removido
        for conta_disco in range(discos+1): #vamos ter que procurar qual disco foi removido
            if not f'disco{conta_disco}.bin' in diretorio:
                disco_removido = conta_disco
                return disco_removido
    else:
        return -1


def le_dados(tamanho, conta_disco, inicio_bloco):
    if tamanho > total_bytes:  #caso ele queira ler o arquivo todo, basta digitar um número maior que o arquivo
        tamanho = total_bytes
    try:
        disco = open(f'{pasta}/disco{conta_disco}.bin', 'rb')
        disco.seek(inicio_bloco)        
        if tamanho <= tamanho_bloco:
            leitura = disco.read(tamanho_bloco)
            leitura = leitura.decode(encoding='utf-8') #"traduzindo" o que foi lido
            output(leitura)
            return True
        elif tamanho > tamanho_bloco:
            leitura = disco.read(tamanho_bloco)
            leitura = leitura.decode(encoding='utf-8') #"traduzindo" o que foi lido
            output(leitura)
            novo_tamanho = tamanho - tamanho_bloco

    except FileNotFoundError: #esse except funciona parecido com o elif de cima
        #abrir os discos e criar um xor do disco removido
        posicao = int((inicio_bloco - tamanho_header) /tamanho_bloco) #contrário da formula inicio_bloco, obs: assim ela fica calculando sempre
        atualiza_paridade(disco_removido, 3, posicao= posicao)
        novo_tamanho = tamanho - tamanho_bloco 

    #passar para o próximo disco ou bloco
    if conta_disco == discos-1: #se for ultimo disco útil, volte o disco com bloco diferente
        conta_disco = 0
        inicio_bloco += tamanho_bloco
    else:  #se ainda não for último disco, prossiga no mesmo bloco em discos diferentes
        conta_disco += 1
    le_dados(novo_tamanho, conta_disco, inicio_bloco)




'''
removeDiscoRAID: O usuário indica um disco a remover do RAID4 (simulando um defeito). O arquivo que representa o disco deve ser apagado pelo programa. 
Ainda assim, as operações seguintes de leitura e escrita devem operar normalmente, mesmo quando envolvem o disco removido.

Quando a leitura envolve o disco removido, os dados devem ser obtidos mediante xor nos demais discos e no disco de paridade. 
A operação de escrita no disco removido gera efeitos apenas no disco de paridade, a fim de permitir (indiretamente) que os dados sendo gravados possam ser 
recuperados em futuras leituras;
'''

def removeDiscoRAID():
    try: 
        lista_dir = os.listdir(pasta)

        lista_dir.sort(key=lambda x:len(x)) #organiza pelo tamanho da string e por padrão pelo valor de cada caracter

        if len(lista_dir) > discos:
            for bin in lista_dir:
                exibicao(bin)
            
            disco_removido = int(input('Digite o número do disco que deseja remover: '))

            os.remove(f'{pasta}/disco{disco_removido}.bin')
            correto(f'Disco{disco_removido}.bin removido com sucesso')
        else:
            errado('Não é possível remover dois discos de um RAID 4, isso acabaria com o RAID')
            return 0

    except NameError:
        errado('Você precisa criar um RAID ou abrir um já pronto para que essa função funcione corretamente.')

    except Exception as e:
        erro = type(e).__name__
        erro (f'Erro na entrada de dados, na função removeDiscoRAID.\nErro: {erro}')

'''
constroiDiscoRAID: O usuário pede para reconstruir o disco defeituoso. 
Um novo arquivo deve ser criado e ter seu conteúdo gerado a partir dos discos remanescentes e o disco de paridade.
'''
def constroiDiscoRAID():
    try:
        disco_removido = encontra_discoremovido()
        if disco_removido != -1:
            print('Esse disco foi removido: ')
            exibicao(f'disco{disco_removido}.bin')

        print(f'Escolha um disco entre 0..{discos}')
        disco_construir = int(input('qual disco você deseja recuperar? '))
        
        if disco_construir not in range(discos+1):
            raise ValueError
        if discos == disco_construir:
            input(disco_construir)

            atualiza_paridade()
        else:
            atualiza_paridade(disco_construir, 2)

    except ValueError:
        errado(f'Não há disco{disco_construir}.bin nesse RAID')
    except Exception as e:
        erro_funcao('constroiDiscoRAID', e)

def main():

    while True:
        print(f'''
        1. inicializaRAID
        2. obtemRAID
        3. escreveRAID
        4. leRAID
        5. removeDiscoRAID
        6. constroiDiscoRAID

        0. Sair
        
                        {legenda("Atalho: crtl+c para voltar a esse menu")}
        ''')
        
        try:
            opcao = int(input('Digite uma opção: '))
            if opcao == 0: # Deixei assim que fica mais legível
                break #se for 0 ele para o código 
            
            if opcao == 1:
                inicializaRAID()
            elif opcao == 2:
                obtemRAID()
            elif opcao == 3:
                escreveRAID()
            elif opcao == 4:
                leRAID()
            elif opcao == 5:
                removeDiscoRAID()
            elif opcao == 6:
                constroiDiscoRAID()
            else:
                raise ValueError
        except:
            errado('\nPor favor, escolha uma opção válida!')  

if __name__ == "__main__":
    main()
