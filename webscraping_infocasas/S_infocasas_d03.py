#!/usr/bin/python3

# scraping infocasas

import platform
import time
import json
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By

# Obtener el nombre del sistema operativo
sistema_operativo = platform.system()

if sistema_operativo == "Linux":
    # instancia del webdriver en Linux
    driver = webdriver.Remote(command_executor='http://127.0.0.1:4444', options=webdriver.ChromeOptions())
    print("OS: Linux")

elif sistema_operativo == 'Windows':
    # instancia del webdriver en windows
    driver = webdriver.Chrome();
    print("OS: Windows")

website = "https://www.infocasas.com.uy"

driver.get(website)
driver.maximize_window()

time.sleep(4)

# pop up publicidad
try:                                          
    btnpopup = driver.find_element(By.XPATH, '//body/div[2]/div//button')
    btnpopup.click()
except Exception as e:
    pass

# ir a los alquileres del website
alquileres = driver.find_element(By.XPATH, '//div[@id="__next"]/div/header/nav/a[2]')
alquileres.click()

# el filtro usa montevideo por defecto
# limpiar filtros
# limpiar_filtros = driver.find_element(By.CLASS_NAME, 'clean-filters')
# limpiar_filtros.click()

#esperar que cargue pagina
time.sleep(4)

lst_data = []

# capturar en rango desde la pagina 0 hasta la que determine range()
# for i in range(4):
for i in tqdm(range(4)):

    # avanzar de pagina
    if i == 1:
        primer_pag = driver.find_element(By.XPATH, '//div[@id="__next"]//ul/li[2]/a')
        primer_pag.click()
        time.sleep(2)
    if i > 1:
        avanzar_pag = driver.find_element(By.XPATH, '//div[@id="__next"]//ul/li[11]/a')
        avanzar_pag.click()
        time.sleep(2)

    # capturar articles de alquileres
    lst_article = driver.find_elements(By.XPATH, '//div[@id="__next"]//section//div/a[@class="lc-data"]')

    # guardar instancia de la pagina principal
    main_window = driver.window_handles[0]

    # pop up publicidad
    try:
        btnpopup = driver.find_element(By.XPATH, '//body/div[2]/div//button')
        btnpopup.click()
    except Exception as e:
        pass

    # creo una lista con los article de las urls para que no pierda la informacion al abrir un nuevo tab
    urls_alquiler = []
    for alquiler in lst_article:
        url_alquiler = alquiler.get_attribute('href')
        urls_alquiler.append(url_alquiler)

    for i, article in enumerate(lst_article):

        # abre una pestaña nueva
        article.click()
        time.sleep(1)

        # cambia el enfoque a la nueva pestaña
        new_window = driver.window_handles[-1]
        driver.switch_to.window(new_window)

        # para capturar informacion de pestaña abierta
        try:
            url_link = urls_alquiler[i]
        except Exception:
            url_link = ""
            pass
        try:
            id = "infocasas_{}".format(url_link.split("/")[-1])
        except Exception:
            id = ""
            print("error en id")
            pass
        try:  
            lst_precio = driver.find_elements(By.XPATH, '//div[@id="__next"]//span/strong')
            # obtener precio y convertir a flotante
            precio = lst_precio[0].text.split(" ")[-1]
            precio_float = float(precio.replace(".", ""))
            # obtener tipo de moneda
            moneda = lst_precio[0].text.split(" ")[0]
        except Exception:
            lst_precio = []
            precio = 0
            moneda = ""
            pass
        try:           
            departamento = driver.find_element(By.CLASS_NAME, 'property-location-tag')
            departamento_split = departamento.text.split(", ")
        except Exception:
            departamento_split = []
            pass
        try:
            lst_info_zona = driver.find_elements(By.XPATH, '//div[@id="__next"]//div[3]/div/strong')
        except Exception:
            lst_info_zona = []
            pass
        try:
            lst_info = driver.find_elements(By.XPATH, '//div[@id="__next"]//div[1]//div[2]/span')
        except Exception:
            lst_info = []
            pass
        try:
            banos = str(lst_info[1].text).split()[0]
        except Exception:
            banos = 0
            pass
        try:
            area = str(lst_info[2].text).split()[0]
        except Exception:
            area = 0
            pass
        try:
            cuartos = str(lst_info[0].text).split()[0]
        except Exception:
            cuartos = 0
            pass
        try:
            # abrir galeria
            time.sleep(1)
            btn_galeria_abrir = driver.find_element(By.XPATH, '//div[@id="__next"]//div[3]/div/div/button[1]')
            btn_galeria_abrir.click()
            time.sleep(1)
            # capturar informacion de galeria de imagenes
            lst_imgs = driver.find_elements(By.XPATH, '//div[@class="pmp-image"]//img')
            img_urls = [img.get_attribute("src") for img in lst_imgs]
        except Exception:
            img_urls = ""
            pass
        try:
            # ir a street view
            time.sleep(1)
            div_street_view = driver.find_element(By.XPATH, '//div[text()="Street View"]')
            div_street_view.click()
            time.sleep(2)
            # capturar url de mapa
            url_google_map = driver.find_element(By.XPATH, '//div[@id="rc-tabs-2-panel-streetView"]//div[1]/div[2]/a')
            url_map = url_google_map.get_attribute('href')
            # capturar latitud y longitud
            parts = url_map.split(',')
            lat = parts[0].split("@")[1]
            lon = parts[1]
        except Exception:
            url_map = ""
            lat = 0
            lon = 0
            pass
        try:
            # cerrar galeria
            btn_galeria_cerrar = driver.find_element(By.XPATH, '//button[@class="ant-modal-close"]')
            btn_galeria_cerrar.click()
        except Exception:
            pass

        # guardar informacion en diccionario
        try:
            dic_alquiler = {
                "id": id,
                "url_link": url_link,
                "origin": "infocasas",
                "operation_type": "Alquiler",
                "price": precio_float,
                "currency": str(moneda),
                "state_name": str(departamento_split[-1]),
                "zone_name": str(lst_info_zona[2].text),
                "property_type": str(lst_info_zona[1].text),
                "total_area": int(area),
                "bathrooms": int(banos),
                "bedrooms": int(cuartos),
                "location": {
                    "latitude": float(lat),
                    "longitude": float(lon)
                    },
                "imagenes": img_urls
                }
            lst_data.append(dic_alquiler)
        except Exception:
            pass

        # cerrar pestaña abierta y volver a la principal
        driver.close()
        driver.switch_to.window(main_window)

#---------------------------------------------------------------
#---------------------------------------------------------------

# exportar JSON
json_data = json.dumps(lst_data, indent=4, ensure_ascii=False)
with open('infocasas.json', 'w', encoding='utf-8') as json_file:
    json_file.write(json_data)

# cerrar driver
driver.quit()
