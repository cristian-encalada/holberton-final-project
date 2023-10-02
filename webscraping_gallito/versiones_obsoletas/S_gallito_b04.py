from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

website = "https://www.gallito.com.uy/"

driver = webdriver.Chrome()
driver.get(website)
driver.maximize_window()


alquileres = driver.find_element(By.XPATH, '//*[@id="inmuebles"]/ul/li[1]/a')
alquileres.click()

time.sleep(4)

lst_data = []

for _ in range(1):
    # for para recuperar las URLs de los distintos alquileres
    lst_articles = driver.find_elements(By.XPATH, f'//*[@id="grillaavisos"]/div/section/article/div[2]/img')
    main_window = driver.window_handles[0]
    articles_links = [i.get_attribute('alt') for i in lst_articles]
    
    
    for article in articles_links:
        driver.get(article)
        
        precio = driver.find_element(By.XPATH, '//*[@id="div_datosBasicos"]/div[2]/span')
        tipo = driver.find_element(By.XPATH, '//*[@id="div_datosOperacion"]/div[1]/p')
        zona = driver.find_element(By.XPATH, '//*[@id="div_datosOperacion"]/div[3]/p')
        lst_imgs = driver.find_elements(By.XPATH, '//*[@id="divInner_Galeria"]/div[1]/a/picture/img')
        img_urls = [img.get_attribute('src') for img in lst_imgs]
        try:
            space = driver.find_element(By.XPATH, '//*[@id="div_datosOperacion"]/div[6]/p')
        except Exception:
            pass
        try: 
            n_bedrooms = driver.find_element(By.XPATH, '//*[@id="div_datosOperacion"]/div[4]/p')
        except Exception:
            pass
        try:
            n_bathrooms = driver.find_element(By.XPATH, '//*[@id="div_datosOperacion"]/div[5]/p')
        except Exception:
            pass
        try:
            ubi = driver.find_element(By.XPATH, '//*[@id="ulNavGaleria"]/li[4]/a').click()
        except Exception:
            pass
        try:
            url_map = WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.XPATH, '//*[@id="iframeMapa"]')))
        except Exception:
            pass
        try:
            dic_alquiler = {
                'precio': str(precio.text),
                'zona': str(zona.text),
                'tipo' : str(tipo.text),
                'imagen': img_urls,
                'url_map': str(url_map.get_attribute('src')),
                'number_of_bedrooms': str(n_bedrooms.text),
                'number_of_bathrooms': str(n_bathrooms.text),
                'area': str(space.text)
            }
        except Exception as e:
            pass
        lst_data.append(dic_alquiler)
        
        
        
json_data = json.dumps(lst_data, indent=4, ensure_ascii=False)
with open('gallito.json', 'w', encoding='utf-8') as json_file:
    json_file.write(json_data)
    
    
driver.quit()