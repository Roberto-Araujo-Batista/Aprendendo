#aprendendo a ler imagens com python em vídeos da hashtag.

import pytesseract
import cv2 #opencv é um programa usado para analisar e identificar imagens




#passo 1: ler a imagem
imagem = cv2.imread('certidao.jpg')
print(imagem)

caminho = r"C:\Program Files\Tesseract-OCR"

#passo 2: pedir para o tesseract extrair o texto da imagem  
pytesseract.pytesseract.tesseract_cmd = caminho + r'\tesseract.exe'
texto = pytesseract.image_to_string(imagem, lang='por') #separa a leitura da imagem pelos quadrados que tem na certidão

print(texto)
