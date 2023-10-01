# este script corre sobre windows
# scraping infocasas

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
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

time.sleep(4)

lst_data = []

# capturar en rango desde la pagina 0 hasta la que determine range()
for i in range(2):

    if i == 0:
        lst_article = driver.find_elements(By.XPATH, '//div[@id="__next"]/div[2]/div/section/div/a')
        """
        # esta parte abre una pestaña nueva y devuelve el enfoque a pestaña principal
        main_window = driver.window_handles[0]
        for article in lst_article:
            article.click()
            time.sleep(1)
            # cambia el enfoque a la nueva pestaña
            new_window = driver.window_handles[-1]
            driver.switch_to.window(new_window)
            # cerrar pestaña abierta y volver a la principal
            driver.close()
            driver.switch_to.window(main_window)
        """
        # esta parte actua como si pasara el mouse el articulo iterado
        actions = ActionChains(driver)
        for article in lst_article:
            # realiza el efecto de pasar el mouse sobre el articulo
            actions.move_to_element(article).perform()
            time.sleep(2)
            lst_img = driver.find_elements(By.XPATH, '//div[@id="__next"]/div[2]/div/section/div[1]/a/div[1]/div/div[2]/div/img')
            # iterar los elementos img y obtener el atributo src
            image_src_list = []
            for img_element in lst_img:
                src = img_element.get_attribute("src")
                image_src_list.append(src)
            print(image_src_list)
            actions.reset_actions()


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
                "descripcion": str(descripcion.text),
                "imagenes": []
            }
            lst_data.append(dic_alquiler)
        primer_pag = driver.find_element(By.XPATH, '//div[@id="__next"]/div[2]/div/ul/li[2]/a')
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
                "descripcion": str(descripcion.text),
                "imagenes": []
            }
            lst_data.append(dic_alquiler)
        avanzar_pag = driver.find_element(By.XPATH, '//div[@id="__next"]/div[2]/div/ul/li[11]/a')
        avanzar_pag.click()
        time.sleep(2)


# exportar JSON
json_data = json.dumps(lst_data, indent=4, ensure_ascii=False)
with open('infocasas.json', 'w', encoding='utf-8') as json_file:
    json_file.write(json_data)


# input("Enter para salir..")

# cerrar driver
driver.quit()