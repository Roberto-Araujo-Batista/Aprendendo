import pyautogui

pyautogui.alert('essa mensagem é um teste')
 
x = pyautogui.confirm(text='prosseguir com o programa?', title ='teste', buttons=['Sim', 'Não'])
print(x)
if x == 'sim':
    print('continuar código')
else:
    print('parar código')


try:
    x = pyautogui.locateOnScreen('image.png')
    print(x)
    print('encontrou imagem')
except:
    print('não encontrou')
