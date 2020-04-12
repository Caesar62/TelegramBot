from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint
import requests
import json

api_key  = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJjZXNhaW56bEBnbWFpbC5jb20iLCJqdGkiOiIyYjFiNjkxYS1iOTk4LTRiNzgtOTYwMS1lMGViMTcwNjEwYWUiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTU4NjEyMjM1MiwidXNlcklkIjoiMmIxYjY5MWEtYjk5OC00Yjc4LTk2MDEtZTBlYjE3MDYxMGFlIiwicm9sZSI6IiJ9.fb-wFsTLg-EthXoOjSwJ32o0WlcGTpZEJE5rYyHLf9U'

# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['api_key'] = api_key
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['api_key'] = 'Bearer'

def wxlei():
    # create an instance of the API class
    api_instance = swagger_client.PrediccionMaritimaApi(swagger_client.ApiClient(configuration))
    costa = '41' # str |  | Código | Área Costera | |----------|----------| | 42 | Costa de Andalucía Occidental y Ceuta   | | 47  | Costa de Andalucía Oriental y Melilla   | | 41  | Costa de Asturias, Cantabria y País Vasco  | | 45  | Costa de Cataluña   | | 40  | Costa de Galicia   | | 44  | Costa de Illes Balears   | | 43  | Costa de las Islas Canarias  | | 46  | Costa de Valencia y Murcia

    try:
        # Predicción marítima costera.
        api_response = api_instance.prediccin_martima_costera_(costa)
        #pprint(api_response)
    except ApiException as e:
        print("Exception when calling PrediccionMaritimaApi->prediccin_martima_costera_: %s\n" % e)

    #aguas_costeras
    response = requests.get(api_response.datos)
    #response.content
    aguas_costeras = response.content.decode(encoding="windows-1252")
    boletin_costero = json.loads(aguas_costeras)[0]
    

    # create an instance of the API class
    api_instance = swagger_client.PrediccionMaritimaApi(swagger_client.ApiClient(configuration))
    area1 = '1' # str |  | Código | Área de Alta Mar | |----------|----------| | 0 | Océano Atlántico al sur de 35º N   | | 1  | Océano Atlántico al norte de 30º N   | | 2  | Mar Mediterráneo

    try:
        # Predicción marítima de alta mar.
        api_response1 = api_instance.prediccin_martima_de_alta_mar_(area1)
        #pprint(api_response)
    except ApiException as e:
        print("Exception when calling PrediccionMaritimaApi->prediccin_martima_de_alta_mar_: %s\n" % e)

    #alta mar
    response1 = requests.get(api_response1.datos)
    #response.content
    alta_mar = response1.content.decode(encoding="windows-1252")
    boletin_alta_mar = json.loads(alta_mar)[0]

    prediccion_meteorologica="""
BOLETÍN METEOROLÓGICO PARA ALTA MAR
INICIO : {}
FIN    : {}
{}: {}
BOLETÍN METEOROLÓGICO PARA AGUAS COSTERAS
INICIO : {}
FIN    : {}
{}: {}
""".format(
    boletin_alta_mar["situacion"]["inicio"],
    boletin_alta_mar["situacion"]["fin"],
    boletin_alta_mar["prediccion"]["zona"][8]["nombre"].upper(),
    boletin_alta_mar["prediccion"]["zona"][8]["texto"].upper(),
    boletin_costero["situacion"]["inicio"],
    boletin_costero["situacion"]["fin"],
    boletin_costero["prediccion"]["zona"][1]["subzona"]["nombre"].upper(),
    boletin_costero["prediccion"]["zona"][1]["subzona"]["texto"].upper()
)
   
    return (prediccion_meteorologica)
    #print(prediccion_meteorologica)

if __name__ == "__main__":   
    pass
