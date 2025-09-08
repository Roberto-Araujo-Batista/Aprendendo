from selenium import webdriver
from time import sleep

navegador = webdriver.Edge()
navegador.get('https://www.google.com/?hl=pt_BR')
sleep(4)