from bs4 import BeautifulSoup
import requests
import pandas as pd

def Codigo_CarOneZ(z):
  url= "https://www.carone.com.ar/categoria-producto/usados/page/"+z+"/"
  page=requests.get(url)
  soup=BeautifulSoup(page.content, "html.parser")
  
  # Nombres de autos usados en venta
  aut=soup.find_all("h2", class_="p-marca")
  autos_usados=list()
  count=0
  for i in aut:
    if count <11:
      autos_usados.append(i.text) 
    else:
      break
    count+=1
  
  #detalle de los autos en venta
  detalle=soup.find_all("p", class_="p-price")
  detalles=list()
  count=0
  for i in detalle:
    if count <11:
      detalles.append(i.text)
    else:
      break
    count+=1
  
  #precio de los autos usados en venta
  precio=soup.find_all("p", class_="p-cuotas-2")
  precios=list()
  count=0
  for i in precio:
    if count <11:
      precios.append(i.text)
    else:
      break
    count+=1
  
  df=pd.DataFrame({"Nombre":autos_usados, "Precio": precios, "Detalle": detalles}, index=list(range(1,12)))
  y = input("¿Como se llamara el archivo?: ")
  df.to_csv(y, index=False)

print("Cuando el programa le indique ingrese el nombre del archivo con la extension .csv")
for i in range(2):
  a=i+1
  z=str(a)
  Codigo_CarOneZ(z)
