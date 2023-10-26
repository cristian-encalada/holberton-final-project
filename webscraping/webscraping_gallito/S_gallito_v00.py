# scraping gallito

import platform
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


# Obtener el nombre del sistema operativo
sistema_operativo = platform.system()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-notifications")

if sistema_operativo == "Linux":
    driver = webdriver.Remote(command_executor='http://127.0.0.1:4444', options=chrome_options)
elif sistema_operativo == 'Windows':
    driver = webdriver.Chrome()

# website en alquiler de inmuebles
website = "https://www.gallito.com.uy"
time.sleep(2)

driver.get(website)
driver.maximize_window()

time.sleep(4)

# elemento del menu
elemento = driver.find_element(By.XPATH, '//*[@id="cat_inmuebles_li"]/a')
# Mueve el mouse sobre el elemento para desplegar menu
action = ActionChains(driver)
action.move_to_element(elemento).perform()

time.sleep(2)

# click en el menu de alquileres
menu_alquileres = driver.find_element(By.XPATH, '//div[@id="cat_inmuebles"]/div[2]/ul/li[2]/h3/a')
urlalquileres = menu_alquileres.get_attribute("href")
driver.get(urlalquileres)

time.sleep(2)

# un clic en las coordenadas x y para quitar el anuncio
action.move_to_element_with_offset(driver.find_element(By.TAG_NAME, 'body'), 300, 200)
action.click()
action.perform()

time.sleep(2)

# seleccionar zona
seleccionarDep = driver.find_element(By.XPATH, '//*[@id="Div_Departamentos"]/li[1]/a')
selecDepart = seleccionarDep.get_attribute("href")
driver.get(selecDepart)

time.sleep(2)

# boton avanzar de pagina con zona filtrada
avanzar_pag = driver.find_element(By.XPATH, '//*[@id="paginador"]/ul/li[6]/a')
custom_avanzar = avanzar_pag.get_attribute("href")

# lista en la que se van a guardar los datos de cada publicacion
lst_data = []

# capturar en rango desde la pagina 0 hasta la que determine range()
for i in range(2):

    if i > 0:
        # se crea url cambiando el ultimo char de la url
        custom_url_avanzando = f"{custom_avanzar[:-1]}{i + 1}"
        driver.get(custom_url_avanzando)
        time.sleep(2)
    
    # captura la lista de elementos de alquiler
    lst_alquiler = driver.find_elements(By.XPATH, '//div[3]/div[1]/div/div[1]/a')

    # creo una lista con las urls para que no pierda la informacion al hacer el back()
    urls_alquiler = []
    for alquiler in lst_alquiler:
        url_alquiler = alquiler.get_attribute('href')
        urls_alquiler.append(url_alquiler)

    # abre cada uno de los url de alquileres
    for j, url_alquiler in enumerate(urls_alquiler):

        driver.get(url_alquiler)
        time.sleep(2)

        print(f"pagina: {i} alquiler: {j}")

        # capturar informacion de url abierta
        try:
            id = "gallito_{}".format(url_alquiler.split("-")[-1])
            precioString = driver.find_element(By.XPATH, '//div[@id="div_datosBasicos"]/div[2]/span').text
            precio = float(precioString.split(" ")[-1].replace(".",""))
            moneda = precioString.split(" ")[0]
            if moneda == '$U':
                moneda = 'UYU'
            elif moneda == 'U$S':
                moneda = 'USD'
        except Exception:
            pass
        try:
            title = driver.find_element(By.XPATH, '//div[@id="div_datosBasicos"]/h1').text
        except Exception:
            title = ""
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
            elementos = driver.find_elements(By.XPATH, '//div[@id="div_datosOperacion"]/div//p')
            for e in elementos:
                lst_e = e.text.split()
                if 'Baños' in lst_e:
                    banos = lst_e[0]
                elif 'Mts' in lst_e:
                    metros = lst_e[0]
        except Exception:
            banos = 0
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
                "title": str(title),
                "url_link": url_alquiler,
                "origin": "gallito",
                "operation_type": "Alquiler",
                "price": precio,
                "currency": str(moneda),
                "state_name": departamento,
                "zone_name": zona,
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

        # abrir enlace
        if i == 0:
            # volver pagina 0 de alquileres
            driver.get(selecDepart)
        else:
            # volver pagina distinta a 0
            driver.get(custom_url_avanzando)

        time.sleep(2)

#---------------------------------------------------------------
#---------------------------------------------------------------

# directorio de guardado
if sistema_operativo == "Linux":
    jsonPath = 'gallito.json'
else:
    jsonPath = 'gallito.json'

# exportar JSON
json_data = json.dumps(lst_data, indent=4, ensure_ascii=False)
with open(jsonPath, 'w', encoding='utf-8') as json_file:
    json_file.write(json_data)

# input("Enter para salir..")

# cerrar driver
driver.quit()
