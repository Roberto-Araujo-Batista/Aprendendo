import openpyxl

arquivo = openpyxl.load_workbook('dados.xlsx')

enviar = arquivo['Enviar']

for linha in enviar.iter_rows(): #o openpyxl retorna sempre linha em tuplas com ponteiros para a celula
    for celula in linha:
        print(celula)
