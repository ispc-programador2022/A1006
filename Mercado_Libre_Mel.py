from ast import Break
import requests
from bs4 import BeautifulSoup
import pandas as pd
from lxml import etree

#url: https://listado.mercadolibre.com.ar/autos-usados
pagina=requests.get('https://listado.mercadolibre.com.ar/autos-usados')
#status code, es la respuesta del prog, deberia ser 200.
pagina.status_code
pagina.text

soup = BeautifulSoup(pagina.content, 'html.parser')

#Nombre h2, ui-search-item__title ui-search-item__group__element shops__items-group-details shops__item-title

nombres= soup.find_all('h2', attrs={"class":"ui-search-item__title ui-search-item__group__element shops__items-group-details shops__item-title"})
nombres=[i.text for i in nombres]


#Precio  
#//li[@class="ui-search-layout__item"]//div[@class="ui-search-result__content-wrapper shops__result-content-wrapper"]//div[@class="ui-search-price ui-search-price--size-medium shops__price"]
dom= etree.HTML(str(soup))
precios= dom.xpath('//li[@class="ui-search-layout__item"]//div[@class="ui-search-result__content-wrapper shops__result-content-wrapper"]//div[@class="ui-search-price ui-search-price--size-medium shops__price"]//span[@class="price-tag-amount"]/span[2]')
precios = [i.text for i in precios]

#Ubicacion //li[@class="ui-search-layout__item"]//div[@class="ui-search-item__group ui-search-item__group--location shops__items-group"]//span[@class="ui-search-item__group__element ui-search-item__location shops__items-group-details"]
ubicacion=dom.xpath('//li[@class="ui-search-layout__item"]//div[@class="ui-search-item__group ui-search-item__group--location shops__items-group"]//span[@class="ui-search-item__group__element ui-search-item__location shops__items-group-details"]')
ubicacion=[i.text for i in ubicacion]


#df = pd.DataFrame({"Nombre":nombres, "Precio":precios, "Ubicacion":ubicacion})

#Exportar 
#df.to_csv('Autos_usados_ML.csv')

#Encontrar siguiente //div[@class="ui-search-pagination shops__pagination-content"]//ul/li[contains(@class,"--next")]/a
siguiente = dom.xpath('//div[@class="ui-search-pagination shops__pagination-content"]//ul/li[contains(@class,"--next")]/a')[0].get('href')

#pagina 1 //span[@class="andes-pagination__link"]
pagina_inicial= soup.find('span',attrs={"class":"andes-pagination__link"}).text
pagina_inicial=int(pagina_inicial)

#pagina 42 //li[@class="andes-pagination__page-count"]
pagina_final= soup.find("li", attrs={"class":"andes-pagination__page-count"})
pagina_final = int(pagina_final.text.split(" ")[1])

#hacer hile para que saque info de todas las pag
lista_nombres = []
lista_precios = []
lista_ubicacion = []

siguiente = 'https://listado.mercadolibre.com.ar/autos-usados'

while True:
    pagina=requests.get(siguiente)
    if pagina.status_code ==200:
        soup = BeautifulSoup(pagina.content, 'html.parser')
        #Nombres
        nombres= soup.find_all('h2', attrs={"class":"ui-search-item__title ui-search-item__group__element shops__items-group-details shops__item-title"})
        nombres=[i.text for i in nombres]
        lista_nombres.extend(nombres)
        #Precios
        dom= etree.HTML(str(soup))
        precios= dom.xpath('//li[@class="ui-search-layout__item"]//div[@class="ui-search-result__content-wrapper shops__result-content-wrapper"]//div[@class="ui-search-price ui-search-price--size-medium shops__price"]//span[@class="price-tag-amount"]/span[2]')
        precios = [i.text for i in precios]
        lista_precios.extend(precios)
        #Ubicacion
        ubicacion=dom.xpath('//li[@class="ui-search-layout__item"]//div[@class="ui-search-item__group ui-search-item__group--location shops__items-group"]//span[@class="ui-search-item__group__element ui-search-item__location shops__items-group-details"]')
        ubicacion=[i.text for i in ubicacion]
        lista_ubicacion.extend(ubicacion)
        pagina_inicial= soup.find('span',attrs={"class":"andes-pagination__link"}).text
        pagina_inicial=int(pagina_inicial)
        pagina_final= soup.find("li", attrs={"class":"andes-pagination__page-count"})
        pagina_final = int(pagina_final.text.split(" ")[1])

    else:
        break
    #print(pagina_inicial)



    if pagina_inicial == 4:
        break
    siguiente = dom.xpath('//div[@class="ui-search-pagination shops__pagination-content"]//ul/li[contains(@class,"--next")]/a')[0].get('href')
#Validar longitud de lista, deberian ser iguales.  
#print(len(lista_nombres))
#print(len(lista_precios))
#print(len(lista_ubicacion))

#Convertir
df = pd.DataFrame({"Nombre":lista_nombres, "Precio":lista_precios, "Ubicacion":lista_ubicacion})
#Exportar 
#df.to_csv('Autos_usados_ML.csv')
