#!/usr/bin/python3

# scraping gallito

import platform
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

# Obtener el nombre del sistema operativo
sistema_operativo = platform.system()

if sistema_operativo == "Linux":
    driver = webdriver.Remote(command_executor='http://127.0.0.1:4444', options=webdriver.ChromeOptions())
elif sistema_operativo == 'Windows':
    driver = webdriver.Chrome()

# website en alquiler de inmuebles
website = "https://www.gallito.com.uy"

driver.get(website)
driver.maximize_window()

time.sleep(2)

# elemento del menu
elemento = driver.find_element(By.XPATH, '//*[@id="cat_inmuebles_li"]/a')

# Mueve el mouse sobre el elemento para desplegar menu
action = ActionChains(driver)
action.move_to_element(elemento).perform()

time.sleep(3)

# click en el menu de alquileres
menu_alquileres = driver.find_element(By.XPATH, '//div[@id="cat_inmuebles"]/div[2]/ul/li[2]/h3/a')
menu_alquileres.click()

time.sleep(1)

seleccionarDep = driver.find_element(By.XPATH, '//*[@id="Div_Departamentos"]/li[1]/a')
seleccionarDep.click()

time.sleep(1)

# lista en la que se van a guardar los datos de cada publicacion
lst_data = []

# capturar en rango desde la pagina 0 hasta la que determine range()
for i in range(2):

    if i > 0:
        # avanzo a la siguiente pagina
        avanzar_pag = driver.find_element(By.XPATH, '//div[@id="paginador"]/ul/li[6]/a')
        avanzar_pag.click()
        time.sleep(4)

    time.sleep(4)
    # captura la lista de elementos de alquiler
    lst_alquiler = driver.find_elements(By.XPATH, '//div[3]/div[1]/div/div[1]/a')

    # creo una lista con las urls para que no pierda la informacion al hacer el back()
    urls_alquiler = []
    for alquiler in lst_alquiler:
        url_alquiler = alquiler.get_attribute('href')
        urls_alquiler.append(url_alquiler)

    # abre cada uno de los url de alquileres
    for url_alquiler in urls_alquiler:

        # abrir enlace
        driver.get(url_alquiler)
        time.sleep(2)

        # capturar informacion de url abierta
        try:
            id = "gallito_{}".format(url_alquiler.split("-")[-1])
            precioString = driver.find_element(By.XPATH, '//div[@id="div_datosBasicos"]/div[2]/span').text
            precio = float(precioString.split(" ")[-1].replace(".",""))
            moneda = precioString.split(" ")[0]
        except Exception:
            pass
        try:
            departamento = driver.find_element(By.XPATH, '//*[@id="ol_breadcrumb"]/li[5]/a').text
            zona = driver.find_element(By.XPATH, '//*[@id="ol_breadcrumb"]/li[6]/a').text
        except Exception:
            pass
        try:
            tipo_propiedad = driver.find_element(By.XPATH, '//div[@id="div_datosOperacion"]/div[1]/p').text
        except:
            tipo_propiedad = ""
        try:
            banos = driver.find_element(By.XPATH, '//div[@id="div_datosOperacion"]/div[5]/p').text.split()[0]
        except Exception:
            banos = 0
            pass
        try:
            metros = driver.find_element(By.XPATH, '//div[@id="div_datosOperacion"]/div[6]/p').text.split()[0]
        except Exception:
            metros = 0
            pass
        try:
            dormitorios = driver.find_element(By.XPATH, '//div[@id="div_datosOperacion"]/div[4]/p').text.split()[0]
        except Exception:
            dormitorios = 0
            pass
        try:
            time.sleep(1)
            # capturar informacion de galeria de imagenes
            lst_imgs = driver.find_elements(By.XPATH, '//*[@id="divInner_Galeria"]/div/a/picture/img')
            img_urls = [img.get_attribute("src") for img in lst_imgs]
        except Exception:
            img_urls = []
            pass
        try:
            # voy a seccion de ubicacion
            place_map = driver.find_element(By.XPATH, '//*[@id="ulNavGaleria"]/li[4]/a')
            place_map.click()
            time.sleep(2)

            url_map = driver.find_element(By.XPATH, '//*[@id="iframeMapa"]')
            src = url_map.get_attribute('src')
            lat = src.split("=")[2].split(",")[0][:11]
            lon = src.split("=")[2].split(",")[-1][:11]
        except Exception:
            lat = 0
            lon = 0
            pass

        # guardar informacion en diccionario
        try:
            dic_alquiler = {
                "id": id,
                "url_link": url_alquiler,
                "origin": "gallito",
                "operation_type": "Alquiler",
                "price": precio,
                "currency": str(moneda),
                "state_name": departamento,
                "city_name": zona,
                "property_type": tipo_propiedad,
                "total_area": int(metros),
                "bathrooms": int(banos),
                "bedrooms": int(dormitorios),
                "location": {
                    "latitude": float(lat),
                    "longitude": float(lon)
                },
                "images": img_urls
            }
            lst_data.append(dic_alquiler)
        except Exception:
            pass

        # volver a la pagina anterior
        driver.back()
        time.sleep(2)

#---------------------------------------------------------------
#---------------------------------------------------------------


# exportar JSON
json_data = json.dumps(lst_data, indent=4, ensure_ascii=False)
with open('gallito.json', 'w', encoding='utf-8') as json_file:
    json_file.write(json_data)

# input("Enter para salir..")

# cerrar driver
driver.quit()
