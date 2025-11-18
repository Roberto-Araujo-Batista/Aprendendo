from tkinter import *

#criar janela
janela = Tk()
#definir título
janela.title('olá, mundo!')

#configurar o tamanho da janela
janela.geometry('600x600')

#alterar cor de fundo da janela
janela.config(background= '#242323')

#alterar logo da janela
janela.iconphoto(False, PhotoImage(file='monstroAlienigena.png'))

#prender janela em um tamanho só
janela.resizable(width=False, height=False)

janela.mainloop()