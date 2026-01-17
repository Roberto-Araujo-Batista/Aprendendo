#testando expressões regulares com arquivos
import os, re

padrao = r'*.jpeg'

nome_arquivo = r'arquivos/gato.jpeg'

print(re.match(padrao, nome_arquivo))
