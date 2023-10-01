# este script corre sobre windows

# scraping infocasas
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import json


website = "https://www.infocasas.com.uy"

# navegador
driver = webdriver.Chrome()
driver.get(website)
driver.maximize_window()


time.sleep(5)
try:
    btnpopup = driver.find_element(By.XPATH, '//*[@id="bodyTag"]//div[3]/div/div[1]/button')
    btnpopup.click()
except Exception as e:
    pass


# ir a los alquileres del website
alquileres = driver.find_element(By.XPATH, '//div[@id="__next"]/div/header/nav/a[2]')
alquileres.click()

# limpiar filtros
limpiar_filtros = driver.find_element(By.XPATH, '//div[@id="__next"]/div[1]/div[1]/button')
limpiar_filtros.click()

#esperar que cargue pagina
time.sleep(4)

lst_data = []

# capturar en rango desde la pagina 0 hasta la que determine range()
for i in range(1):

    if i == 0:
        lst_divs1 = driver.find_elements(By.XPATH, '//div[@id="__next"]/div[2]/div/section/div[contains(@class,"listingCard isSuperHighlighted UY")]')
        lst_article = driver.find_elements(By.XPATH, '//div[@id="__next"]/div[2]/div/section/div/a')
        main_window = driver.window_handles[0]

        for article in lst_article:
            # abre una pestaña nueva
            article.click()
            time.sleep(1)

            # cambia el enfoque a la nueva pestaña
            new_window = driver.window_handles[-1]
            driver.switch_to.window(new_window)
            time.sleep(2)

            # para capturar informacion de pestaña abierta
            precio = driver.find_elements(By.XPATH, '//div[@id="__next"]//span/strong')            
            departamento = driver.find_element(By.CLASS_NAME, 'property-location-tag')
            departamento_split = departamento.text.split(", ")
            lst_info = driver.find_elements(By.XPATH, '//div[@id="__next"]//div[3]/div/strong')

            # print para pruebas
            print(str(departamento_split[-1]))

            # guardar informacion en diccionario
            dic_alquiler = {
                "precio": str(precio[0].text),
                "zona": str(lst_info[2].text),
                "tipo": str(lst_info[1].text),
                "depart": str(departamento_split[-1]),
                "imagenes": [] 
            }
            lst_data.append(dic_alquiler)

            # cerrar pestaña abierta y volver a la principal
            driver.close()
            driver.switch_to.window(main_window)


        primer_pag = driver.find_element(By.XPATH, '//div[@id="__next"]/div[2]/div/ul/li[2]/a')
        primer_pag.click()
        time.sleep(2)

    if i > 0:

        avanzar_pag = driver.find_element(By.XPATH, '//div[@id="__next"]/div[2]/div/ul/li[11]/a')
        avanzar_pag.click()
        time.sleep(2)



#---------------------------------------------------------------
#---------------------------------------------------------------

# exportar JSON
json_data = json.dumps(lst_data, indent=4, ensure_ascii=False)
with open('infocasas.json', 'w', encoding='utf-8') as json_file:
    json_file.write(json_data)

# input("Enter para salir..")

# cerrar driver
driver.quit()
