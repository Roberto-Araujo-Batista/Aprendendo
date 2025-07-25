import openpyxl

#criando arquivo excel
planilha = openpyxl.Workbook()

#como visualizar pastas existentes
print(planilha.sheetnames)

#como criar uma página
planilha.create_sheet('Enviar')

#como selecionar uma página
enviar = planilha['Enviar']



#salvar planilha
planilha.save('dados.xlsx')
