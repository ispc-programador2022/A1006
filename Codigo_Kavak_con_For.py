from bs4 import BeautifulSoup
import requests
import pandas as pd

def codigo_YaninaZ(z):
    url= 'https://www.kavak.com/ar/page-'+z+'/autos-usados'
    page=requests.get(url)
    soup=BeautifulSoup(page.content, 'html.parser')

    #Nombres autos en venta
    aut=soup.find_all('h2', class_='car-name')
    autos_usados= list()
    count=0
    for i in aut:
        if count <35:
            autos_usados.append(i.text)
        else:
            break
        count+=1

    #Precios
    precio=soup.find_all('span', class_='payment-total payment-highlight')
    precios= list()
    count=0
    for i in precio:
        if count <35:
            precios.append(i.text)
        else:
            break
        count+=1

    #DETALLE
    detalle=soup.find_all('p', class_='car-details')
    detalles= list()
    count=0
    for i in detalle:
        if count <35:
         detalles.append(i.text)
        else:
         break
        count+=1

    df=pd.DataFrame({'Nombre':autos_usados, 'Precio': precios, 'Detalle': detalles},index=list(range(1,36)))
    y = input('¿Como se llamara el archivo? : ')
    df.to_excel(y, index=False)


print('Cuando el programa le indique ingrese el nombre del archivo con la extension .xlsx')
for i in range(4):
    a=i+1
    z=str(a)
    codigo_YaninaZ(z)
        