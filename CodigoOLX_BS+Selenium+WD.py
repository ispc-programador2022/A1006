#Para utilizar este codigo deberá descargar el archivo chromedriver.exe
# de esta página https://chromedriver.chromium.org/downloads
# descargarlo en la carpeta en la que esté trabajando

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import pandas as pd
from datetime import date
from time import sleep
from selenium.webdriver.common.by import By

ubicacion = "./chromedriver.exe" #Ruta del driver
driver = webdriver.Chrome(ubicacion)

driver.get("https://www.olx.com.ar/autos_c378")

precio_lista=[]
km_lista =[]
mod_lista=[]

page = BeautifulSoup(driver.page_source,'html.parser')


for i in range(2):
    for auto in page.findAll('li', attrs={'data-aut-id':'itemBox', 'data-aut-category-id':'378', 'class':'_1DNjI'}):
        precio = auto.find('span', attrs ={'class':"_2Ks63", 'data-aut-id':'itemPrice'})
        if precio:
            precio_lista.append(precio.text)
        else:precio_lista.append('')

        km= auto.find('span', class_="YBbhy")
        if km:
            km_lista.append(km.text)
        else:
            km_lista.append('')

        mod=auto.find('span', class_= '_2poNJ')
        if mod:
            mod_lista.append(mod.text)
        else:
            mod_lista.append('')
  
    next_btn=driver.find_element(By.XPATH,'//li/div/button')
    next_btn.click
    sleep(2)

#print(precio_lista)
df= pd.DataFrame({'Precio': precio_lista, 'Kilometraje': km_lista, 'Modelo':mod_lista})
df.to_excel('OLX_autos_venta.xlsx', index=False)
print(df)
