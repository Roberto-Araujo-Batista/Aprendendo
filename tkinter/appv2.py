from tkinter import *

#criando janela
janela = Tk()
janela.title('testando label')
janela.geometry('250x250')
janela.iconphoto(False, PhotoImage(file='monstroAlienigena.png'))


#crianção de label, sintaxe Label(janela, text='nome')
label_nome = Label(janela,width='10', height=' 10', text='Nome: ')
#adicionando label a tela do programa
label_nome.grid(row = 0, column= 0)

label_idade = Label(janela, width='10', height='10', text= 'Idade: ')
label_idade.grid(row=0, column=1)

label_pais = Label(janela, width='10', height='10', text='Pais: ')
label_pais.grid(row=0, column=2)

janela.mainloop()