# coding: utf-8
import re
from ftplib import FTP
import tarfile
import os, os.path
from os import remove
import shutil
import glob
import pandas as pd
import datetime
import requests
import smtplib
import time
from bs4 import BeautifulSoup as bs
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def waves():
    titulo_boya = ('        ALTURA OLAS BOYAS - CANTABRIA\n'.upper())

    # Hora, día y mes actual
    b1 = time.strftime("%H")
    d1 = time.strftime("%Y/%m/%d")[8:]
    f1 = time.strftime("%Y/%m/%d")[5:7]
    
    # BOYA ODAS BILBAO-VIZCAYA & GIJON-PEÑAS

    # Crear directorio en el caso de que no exista.
    nuevaruta = r'/Datos_Boyas/'
    if not os.path.exists(nuevaruta): os.makedirs(nuevaruta)

    # Crear directorio en el caso de que no exista.
    nuevaruta = r'/Datos_Boyas1/'
    if not os.path.exists(nuevaruta): os.makedirs(nuevaruta)

    # Borra ficheros del directorio
    folder_path = '/Datos_Boyas/'
    for file_object in os.listdir(folder_path):
        file_object_path = os.path.join(folder_path, file_object)
        if os.path.isfile(file_object_path):
            os.unlink(file_object_path)
        else:
            shutil.rmtree(file_object_path)

    # Borra ficheros del directorio
    folder_path = '/Datos_Boyas1/'
    for file_object in os.listdir(folder_path):
        file_object_path = os.path.join(folder_path, file_object)
        if os.path.isfile(file_object_path):
            os.unlink(file_object_path)
        else:
            shutil.rmtree(file_object_path)

    # Descargar fichero del FTP
    ftp = FTP('cain.puertos.es')
    ftp.login("", "")
    ftp.cwd('incoming/PdE_RealTime_Data/')
    ftp.retrbinary('RETR PdE_RealTime_Data.tar.gz', open('PdE_RealTime_Data.tar.gz', 'wb').write)
    ftp.quit()

    # Extraer fichero comprimido tar.gz
    tar = tarfile.open("PdE_RealTime_Data.tar.gz", "r:gz")
    tar.getmembers()
    for tarinfo in tar:

        tar.extractall('/Datos_Boyas')

    tar.close

    # Cambia el nombre del fichero de Bilbao

    def main():

            dire = '/Datos_Boyas/'
            os.chdir(dire)
            archivos = glob.glob('Parbilbo*.txt')
            for dirlist in archivos:
                    os.rename(dirlist, 'Parbilbo.txt')
    main()

    shutil.move('/Datos_Boyas/parbilbo.txt', '/Datos_Boyas1/parbilbo.txt')

    # Cambia el nombre del fichero de Gijon

    def main1():
        dire = '/Datos_Boyas/'
        os.chdir(dire)
        archivos = glob.glob('parpenas*.txt')
        for dirlist in archivos:
            os.rename(dirlist, 'parpenas.txt')
    main1()

    shutil.move('/Datos_Boyas/parpenas.txt', '/Datos_Boyas1/parpenas.txt')
    '''
    # Borra ficheros del directorio
    folder_path = '/Datos_Boyas/'
    for file_object in os.listdir(folder_path):
        file_object_path = os.path.join(folder_path, file_object)
        if os.path.isfile(file_object_path):
            os.unlink(file_object_path)
        else:
            shutil.rmtree(file_object_path)
    '''
    shutil.move('/Datos_Boyas1/parbilbo.txt', '/Datos_Boyas/Datos_Boya_Bilbao.txt')
    shutil.move('/Datos_Boyas1/parpenas.txt', '/Datos_Boyas/Datos_Boya_Gijon.txt')

    # Borra directorio Datos_Boyas1
    os.rmdir('/Datos_Boyas1/')

    # Extrae datos del fichero Bilbao
    df = pd.read_csv("/Datos_Boyas/Datos_Boya_Bilbao.txt",  delimiter=r"\s+")
    altura_ola_bilbao = df.loc[0, 'WaHs']
    hora_ola_bilbao = df.loc[0, 'Time']
    dia_ola_bilbao = df.loc[0, 'Date']
    dia_ola_bilbao = str(dia_ola_bilbao)
    dia_ola_bilbao_2 = str(dia_ola_bilbao)[6:]
    mes_ola_bilbao = str(dia_ola_bilbao)[4:6]
    #print(mes_ola_bilbao)
    a1 = hora_ola_bilbao
    c1 = dia_ola_bilbao_2
    e1 = mes_ola_bilbao
    Dif_Hora = (int(b1) - int(a1))
    Dif_Dia = (int(d1) - int(c1))
    Dif_Mes = (int(f1) - int(e1))

    # Pasa a formato YYYY-MM-DD
    dt = datetime.datetime.strptime(dia_ola_bilbao, '%Y%m%d')
    dt = str(dt)
    dt = (dt[0:10])

    try:

        mensaje_bilbao = '\n* Boya Bilbao (ODAS) -> Altura ola registrada el ' + str(dt) + ' a las ' + str(hora_ola_bilbao) + ':00 UTC es de ' + str(altura_ola_bilbao) + ' metros.\n'
        mensaje_bilbao_1 = mensaje_bilbao
        if (int(b1) - int(a1)) < 0:
            Dif_Hora = (int(b1) + 24 - int(a1))
        else:
            Dif_Hora = (int(b1) - int(a1))
            # print('Dif_Hora: ', Dif_Hora)
        if (Dif_Dia == 0 and Dif_Hora <= 6 and Dif_Mes == 0) or (Dif_Dia == 1 and Dif_Hora <= 6 and int(b1) < int(a1) and Dif_Mes == 0):
            str(mensaje_bilbao)
        else:
            mensaje_bilbao = '\n* Boya Bilbao (ODAS) -> SIN COMUNICACION.\n'
            ultima_altura = 0

    except:

        mensaje_bilbao = '\n* Boya Bilbao (ODAS) -> NO OPERATIVA.\n'
        ultima_altura = 0
    #print(mensaje_bilbao)

    # Extrae datos del fichero Gijón
    df1 = pd.read_csv("/Datos_Boyas/Datos_Boya_Gijon.txt",  delimiter=r"\s+")
    altura_ola_gijon = df1.loc[0, 'WaHs']
    hora_ola_gijon = df1.loc[0, 'Time']
    dia_ola_gijon = df1.loc[0, 'Date']
    dia_ola_gijon = str(dia_ola_gijon)
    dia_ola_gijon = str(dia_ola_gijon)
    dia_ola_gijon_1 = str(dia_ola_gijon)[6:]
    mes_ola_gijon = str(dia_ola_gijon)[4:6]

    a1 = hora_ola_gijon
    c1 = dia_ola_gijon_1
    e1 = mes_ola_gijon
    Dif_Hora = (int(b1) - int(a1))
    Dif_Dia = (int(d1) - int(c1))
    Dif_Mes = (int(f1) - int(e1))

    # Pasa a formato YYYY-MM-DD
    dt1 = datetime.datetime.strptime(dia_ola_gijon, '%Y%m%d')
    dt1 = str(dt1)
    dt1 = (dt1[0:10])

    try:

        mensaje_gijon = '\n* Boya Peñas (ODAS) -> Altura ola registrada el ' + str(dt1) + ' a las ' + str(hora_ola_gijon) + ':00 UTC es de ' + str(altura_ola_gijon) + ' metros.\n'
        mensaje_gijon_1 = mensaje_gijon
        if (int(b1) - int(a1)) < 0:
            Dif_Hora = (int(b1) + 24 - int(a1))
        else:
            Dif_Hora = (int(b1) - int(a1))
            # print('Dif_Hora: ', Dif_Hora)
        if (Dif_Dia == 0 and Dif_Hora <= 6 and Dif_Mes == 0) or (Dif_Dia == 1 and Dif_Hora <= 6 and int(b1) < int(a1) and Dif_Mes == 0):
            str(mensaje_gijon)
        else:
            mensaje_gijon = '\n* Boya Peñas (ODAS) -> SIN COMUNICACION.\n'
            ultima_altura = 0

    except:

        mensaje_gijon = '\n* Boya Peñas (ODAS) -> NO OPERATIVA.\n'
        ultima_altura = 0
    

    # BOYA DEL IEO --> AGL

    try:

        # Extracción de datos de la página del IEO para la boya AGL
        request_boya_agl = requests.get('http://www.boya-agl.st.ieo.es/boya_agl/ultimos.php?var=hm0_table', timeout=5)
        soup_boya_agl = bs(request_boya_agl.content, "html.parser")
        busca_altura = soup_boya_agl.find_all('table')
        texto_busca_altura = re.search(r'Valor(.*)', busca_altura[0].text, re.DOTALL)
        lista_lecturas = texto_busca_altura.group(1).strip().split('\n')
        ultima_altura = float(lista_lecturas[3])

        mensaje_boya_agl = '* Boya AGL (ODAS) -> Altura ola registrada el ' + str(lista_lecturas[0]) + ' a las ' + str(lista_lecturas[1]) + ' UTC es de ' + str(lista_lecturas[3]) + ' metros.\n'
        mensaje_boya_agl_1 = mensaje_boya_agl
        a1 = lista_lecturas[1]  # Ultima hora boya
        a1 = a1[0:2]
        lista_lecturas = lista_lecturas[0]
        c1 = lista_lecturas[8:]
        e1 = lista_lecturas[5:7]
        #print(e1)
        Dif_Hora = (int(b1) - int(a1))
        Dif_Dia = (int(d1) - int(c1))
        Dif_Mes = (int(f1) - int(e1))

        if (int(b1) - int(a1)) < 0:
            Dif_Hora = (int(b1) + 24 - int(a1))
        else:
            Dif_Hora = (int(b1) - int(a1))

        if (Dif_Dia == 0 and Dif_Hora <= 6 and Dif_Mes == 0) or (Dif_Dia == 1 and Dif_Hora <= 6 and int(b1) < int(a1) and Dif_Mes == 0):
            str(mensaje_boya_agl)
        else:
            mensaje_boya_agl = '* Boya AGL (ODAS) -> SIN COMUNICACION.\n'
            ultima_altura = 0

    except:

        mensaje_boya_agl = '* Boya AGL (ODAS) -> NO OPERATIVA.\n'
        ultima_altura = 0

    # CREACION DEL MENSAJE A ENVIAR POR EMAIL
    #remove ("/Datos_Boyas/PdE_RealTime_Data.tar.gz")
    mensaje_boya2 = '\n'
    
    mensaje_boyas = titulo_boya + mensaje_boya2 + mensaje_boya_agl + mensaje_bilbao + mensaje_gijon
    #print(mensaje_boyas)
    return mensaje_boyas 
    
    '''
    # Crea cuadro de texto
    with open('boya_agl.txt', 'w') as archivo_texto:
        print(mensaje_boyas.strip(), file=archivo_texto)
    os.startfile('boya_agl.txt')
    


    if ultima_altura > 3.85 or altura_ola_gijon > 8.00 or altura_ola_bilbao > 8.00:
        
        # Crea cuadro de texto
        with open('boya_agl.txt', 'w') as archivo_texto:
            print(mensaje_boyas.strip(), file=archivo_texto)
        os.startfile('boya_agl.txt')
        
        
        # Modulo para enviar lo anterior por email, cuando cumpla la condición anterior.
        print("***** Enviar email con Sasemar.es *****")
        user = 'controlsantander'
        password = 'santander'

        # Para las cabeceras del email
        remitente = 'santander@sasemar.es'
        destinatario = ['jefecentro.santande@sasemar.es','cdherrera@fomento.es','ampereda@mfom.es','santander@sasemar.es']
        Cc = ['cesainzl@gmail.com']
        Bcc = ['sbonis57@yahoo.es','carlos_vallar@yahoo.es']
        destinatarios = destinatario + Cc + Bcc
        asunto = 'Boyas ODAS (AGL, Peñas y Bilbao)'
        mensaje = mensaje_boyas

        # Host y puerto SMTP de Gmail
        gmail = smtplib.SMTP('smtp.sasemar.es', 587)

        # protocolo de cifrado de datos utilizado por gmail
        gmail.starttls()

        # muestra la depuración de la operacion de envío 1=true
        gmail.set_debuglevel(1)

        msg = MIMEMultipart()
        header = MIMEMultipart()
        header['Subject'] = asunto
        header['From'] = remitente
        header['To'] = ", ".join(destinatario)
        header['Cc'] = ", ".join(Cc)
        body = mensaje
        header.attach(MIMEText(body, 'plain'))
        text = header.as_string()

        # Enviar email
        gmail.login(user, password)
        gmail.sendmail(remitente, destinatarios, text)

        # Cerrar la conexión SMTP
        gmail.quit()
    

    else:
        pass
'''

if __name__ == "__main__":   
    pass
