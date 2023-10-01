# este script corre sobre windows
# scraping infocasas

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

# from selenium.webdriver.chrome.service import Service
# s = Service("C:\chromedriver_win32\chromedriver.exe")

website = "https://www.infocasas.com.uy"

# opciones
# from selenium.webdriver.chrome.options import Options
# opts = Options()
# opts.add_argument("--headless")

# navegador
# driver = webdriver.Chrome(options=opts)
driver = webdriver.Chrome()
driver.get(website)
driver.maximize_window()

# ir a los alquileres
alquileres = driver.find_element(By.XPATH, '//div[@id="__next"]/div/header/nav/a[2]')
alquileres.click()

# limpiar filtros
limpiar_filtros = driver.find_element(By.XPATH, '//div[@id="__next"]/div[1]/div[1]/button')
limpiar_filtros.click()

time.sleep(5)
primer_pag = driver.find_element(By.XPATH, '//div[@id="__next"]/div[2]/div/ul/li[2]/a')

lst_data = []

for i in range(5):

    if i == 0:
        lst_divs1 = driver.find_elements(By.XPATH, '//div[@id="__next"]/div[2]/div/section/div[contains(@class,"listingCard isSuperHighlighted UY")]')
        for div in lst_divs1:
            precio = div.find_element(By.CLASS_NAME, 'lc-price')
            lugar = div.find_element(By.CLASS_NAME, 'lc-location')
            lst_lugar = lugar.text.split(", ")
            descripcion = div.find_element(By.CLASS_NAME, 'lc-description')

            dic_alquiler = {
                "precio": str(precio.text),
                "zona": str(lst_lugar[0]),
                "depart": str(lst_lugar[1]),
                "descripcion": str(descripcion.text)
            }
            lst_data.append(dic_alquiler)
        primer_pag.click()
        time.sleep(2)

    if i > 0:
        lst_divs2 = driver.find_elements(By.XPATH, '//div[@id="__next"]/div[2]/div/section/div[contains(@class,"listingCard isSuperHighlighted UY")]')   
        for div in lst_divs2:
            precio = div.find_element(By.CLASS_NAME, 'lc-price')
            lugar = div.find_element(By.CLASS_NAME, 'lc-location')
            lst_lugar = lugar.text.split(", ")
            descripcion = div.find_element(By.CLASS_NAME, 'lc-description')

            dic_alquiler = {
                "precio": str(precio.text),
                "zona": str(lst_lugar[0]),
                "depart": str(lst_lugar[1]),
                "descripcion": str(descripcion.text)
            }
            lst_data.append(dic_alquiler)

        avanzar_pag = driver.find_element(By.XPATH, '//div[@id="__next"]/div[2]/div/ul/li[11]/a')
        avanzar_pag.click()
        time.sleep(2)


# exportar
json_data = json.dumps(lst_data, indent=4, ensure_ascii=False)
with open('infocasas.json', 'w', encoding='utf-8') as json_file:
    json_file.write(json_data)


# input("Enter para salir..")
driver.quit()