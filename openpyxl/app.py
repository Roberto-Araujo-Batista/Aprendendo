import openpyxl

#criando arquivo excel
planilha = openpyxl.Workbook()

#como visualizar pastas existentes
print(planilha.sheetnames)

#como criar uma página
planilha.create_sheet('Enviar')

#como selecionar uma página
enviar = planilha['Enviar']

enviar.append(['NOME', 'IDADE', 'CARGO'])
enviar.append(['roberto', '22', 'suporte ti'])
enviar.append(['gabriel', '5', 'estudante'])
enviar.append(['william', '9', 'estudante'])
enviar.append(['clarice', '0', 'bebe'])

#salvar planilha e fecha arquivo.
planilha.save('dados.xlsx')

arquivo = openpyxl.load_workbook('dados.xlsx')

enviar = arquivo['Enviar']

for linha in enviar.iter_rows(): #o openpyxl retorna sempre linha em tuplas com ponteiros para a celula
    for celula in linha:
        print(celula.value) #celula é uma referencia a celula da planilha