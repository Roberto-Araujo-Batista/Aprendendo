vermelho = '\033[1;31m' 
verde    = '\033[1;32m' 
amarelo  = '\033[1;33m'
azul     = '\033[1;34m'
f_azul   = '\033[1;44m'
padrao   = '\033[0m'  # Resetar

import os

def correto(mensagem, cls = True):
    if cls: 
        os.system('cls')
    print(verde, mensagem, padrao)

def certo(mensagem):
    resultado = f'{verde}{mensagem}{padrao}'
    return resultado

def errado(mensagem):
    os.system('cls')
    print(vermelho, mensagem, padrao)

def erro_funcao(mensagem, e):
    erro = type(e).__name__
    print(vermelho,f'Erro na função {mensagem}\nErro: {erro}', padrao)

def exibicao(mensagem):
    print(azul, mensagem, padrao)

def output(mensagem):
    mensagem = mensagem
    print(azul, mensagem, padrao,end='', sep='')

def legenda(mensagem):
    resultado = f'{amarelo}{mensagem}{padrao}'
    return resultado