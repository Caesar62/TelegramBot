import datetime
import os
import re
import time
import urllib
import urllib.request
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

def wxlei ():
    # ALTA MAR CANTABRICO
    #http://www.aemet.es/es/eltiempo/prediccion/maritima?opc1=1&opc2=martot&opc3=1&area=atl1&zona=9109_Cantabrico

    #Extraccion de datos altamar Cantabrico
    request_altmar_cantabrico = requests.get('http://www.aemet.es/es/eltiempo/prediccion/maritima?opc1=1&opc2=martot&opc3=1&area=atl1&zona=9109_Cantabrico')
    soup_altamar_cantabrico = BeautifulSoup(request_altmar_cantabrico.content)
    busca_cantabrico_fecha= soup_altamar_cantabrico.find_all('h3',{'class':"texto_entradilla"})

    #Fecha elaboración aviso altamar
    #texto_cantabrico_fecha = busca_cantabrico_fecha[0].text
    busca_fecha_inicio_altaMar = soup_altamar_cantabrico.find_all('div',{'class':'contenedor_central marginbottom35px'})
    texto_cantabrico_fecha = re.search(r'Fecha de inicio:(.*)\nFec',(busca_fecha_inicio_altaMar[1].text),re.DOTALL)

    #Texto aviso altamar
    busca_cantabrico= soup_altamar_cantabrico.find_all('div',{'class':"texto_normal"})
    texto_aviso_cantabrico = re.search(r'Fecha de fin:(.*)',(busca_cantabrico[1].text),re.DOTALL)
    aviso_cantabrico = busca_cantabrico[0].text  # texto

    #Fecha de prediccion altamar
    busca_fecha_fin_altaMar = soup_altamar_cantabrico.find_all('div',{'class':'contenedor_central marginbottom35px'})
    texto_fecha_fin_altaMar = re.search(r'Fecha de fin:(.*)',busca_fecha_fin_altaMar[1].text)

    #Texto prediccion altamar
    altaMarCantabrico = busca_cantabrico[1].text # texto


    # AGUAS COSTERAS CANTABRICO
    # http://www.aemet.es/es/eltiempo/prediccion/maritima?opc1=0&opc2=martot&opc3=1&area=can1
    rCostCantabrico = requests.get('http://www.aemet.es/es/eltiempo/prediccion/maritima?opc1=0&opc2=martot&opc3=1&area=can1')
    soup_costeras_cantabrico = BeautifulSoup(rCostCantabrico.content)
    busca_cantabria_fecha= soup_costeras_cantabrico.find_all('div',{'class':"notas_tabla"})

    #Fecha elaboración aviso costero
    texto_cantabria_fecha = re.search(r'Fecha de inicio:(.*)\nFec',(busca_cantabria_fecha[1].text),re.DOTALL)

    #Texto aviso costero
    busca_cantabria= soup_costeras_cantabrico.find_all('div',{'class':"texto_normal"})
    texto_aviso_cantabria = re.search(r'Fecha de fin:(.*)',(busca_cantabria[1].text),re.DOTALL)
    aviso_cantabria = busca_cantabria[0].text  # texto

    #Prediccion costera valida hasta
    busca_fecha_fin_costeras =soup_costeras_cantabrico.find_all('div',{'class':'notas_tabla'})
    texto_fecha_fin_costeras = re.search(r'Fecha de fin:(.*)',busca_fecha_fin_costeras[1].text)
    # fomateado  ::    texto_fecha_fin_costeras.group(1).replace('\xa0',' ')

    #TEXTO AGUAS COSTERAS CANTABRIA
    busca_costeras_cantabrico = soup_costeras_cantabrico.find_all('div',{'class':"contenedor_central"})
    texto_costera_cantabria = re.search(r'Aguas costeras de Cantabria(.*)Aguas costeras de B',(busca_costeras_cantabrico[1].text),re.DOTALL)

    meteo_sdr = """
ALTA MAR  CANTABRICO {}
AVISO PARA ALTA MAR:  {}
PREDICCIÓN PARA ALTA MAR: 
{}
{}
AGUAS COSTERAS DE CANTABRIA:
{}
PREDICCION: {}
{}
""".format(
    texto_cantabrico_fecha[0].replace("\xa0","").replace("\nFec","").replace("FECHA DE ","").upper(),
    aviso_cantabrico.upper(),
    altaMarCantabrico.upper().strip(),
    texto_fecha_fin_altaMar[0].replace("\xa0"," ").upper().replace("FECHA DE FIN:","HASTA : "),
    texto_cantabria_fecha[0].replace("\xa0"," ").replace("\nFec"," ").upper(),
    texto_costera_cantabria[0].replace("\xa0"," ").replace("\n"," ").upper().replace("Aguas costeras de B",""),
    texto_fecha_fin_costeras[0].replace("\xa0"," ").replace("\nFec","").upper().replace("FECHA DE FIN","HASTA "),

)

    return meteo_sdr
    #print(meteo_sdr)


if __name__ == "__main__":   
    pass
