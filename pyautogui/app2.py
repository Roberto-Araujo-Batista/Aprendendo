#programa para abrir o notepad e escrever "feito" automatizando teclado

from time import sleep
import pyautogui

#para pressionar várias teclas
pyautogui.hotkey('win', 'd')
pyautogui.hotkey('win', 'r')
#para digitar
pyautogui.write('notepad')
#pressionar uma tecla
pyautogui.press('Enter')

sleep(1) #sleep para carregar o notepad
pyautogui.write('feito :)')