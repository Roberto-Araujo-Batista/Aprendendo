import pyautogui

try:
    x = pyautogui.locateOnScreen('setaFirefox.PNG')
    print(x)
    raise pyautogui.ImageNotFoundException('não encontrou')
except pyautogui.ImageNotFoundException:
    print('não encontrou')