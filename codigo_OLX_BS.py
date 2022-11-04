
from bs4 import BeautifulSoup
import requests
import pandas as pd
import xlrd

url= 'https://www.olx.com.ar/autos_c378'
page=requests.get(url)
soup=BeautifulSoup(page.content, 'html.parser')

#Fecha de Publicacion
Fecha =soup.find_all('span', class_='_2jcGx')
Fec_autos_usados= list()
count=0
for i in Fecha:
    if count <40:
        Fec_autos_usados.append(i.text)
    else:
         break
    count+=1

#Precios de los autos en venta
precio=soup.find_all('span', class_='_2Ks63')
prc_autos_usados= list()
count=0
for i in precio:
    if count <40:
         prc_autos_usados.append(i.text)
    else:
         break
    count+=1

#Modelo
mod=soup.find_all('span', class_='_2poNJ')
mod_autos_usados= list()
count=0
for i in mod:
    if count <40:
         mod_autos_usados.append(i.text)
    else:
         break
    count+=1

año=soup.find_all('span', class_='YBbhy')
año_autos_usados= list()
count=0
for i in año:
    if count <40:
         año_autos_usados.append(i.text)
    else:
         break
    count+=1


#Esta guardado en CSV y Excel para trabajar mejor en estadisticas

df=pd.DataFrame({'Fecha de Publicacion':Fec_autos_usados, 'Precios':prc_autos_usados, 'Modelo':mod_autos_usados, 'Año y Km':año_autos_usados},index=list(range(1,41)))
df.to_csv('autos_enVenta_olx.cvs', index='False')
df2= df.to_dict('records')
print(df2)

df.to_excel('autos_enVenta_olx.xlsx', index='False')
df3 = df.to_dict('list')
print(df3)
