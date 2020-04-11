# coding: utf-8


from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint
import requests
import json


def wxlei ():
    api_key = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJjZXNhaW56bEBnbWFpbC5jb20iLCJqdGkiOiIyYjFiNjkxYS1iOTk4LTRiNzgtOTYwMS1lMGViMTcwNjEwYWUiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTU4NjEyMjM1MiwidXNlcklkIjoiMmIxYjY5MWEtYjk5OC00Yjc4LTk2MDEtZTBlYjE3MDYxMGFlIiwicm9sZSI6IiJ9.fb-wFsTLg-EthXoOjSwJ32o0WlcGTpZEJE5rYyHLf9U"
    # Configure API key authorization: api_key
    configuration = swagger_client.Configuration()
    configuration.api_key['api_key'] = api_key
    # Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
    # configuration.api_key_prefix['api_key'] = 'Bearer'

    # create an instance of the API class
    api_instance = swagger_client.PrediccionMaritimaApi(swagger_client.ApiClient(configuration))
    costa = '41' # str |  | Código | Área Costera | |----------|----------| | 42 | Costa de Andalucía Occidental y Ceuta   | | 47  | Costa de Andalucía Oriental y Melilla   | | 41  | Costa de Asturias, Cantabria y País Vasco  | | 45  | Costa de Cataluña   | | 40  | Costa de Galicia   | | 44  | Costa de Illes Balears   | | 43  | Costa de las Islas Canarias  | | 46  | Costa de Valencia y Murcia


    try:
        # Predicción marítima costera.
        api_response = api_instance.prediccin_martima_costera_(costa)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling PrediccionMaritimaApi->prediccin_martima_costera_: %s\n" % e)


    response = requests.get(api_response.datos)
    #response.content
    aguas_costeras = response.content.decode(encoding="windows-1252")



    #aguas_costeras


    boletin_costero = json.loads(aguas_costeras)[0]



    prediccion_cantabrico="""
    BOLETÍN METEOROLÓGICO PARA AGUAS COSTERAS
    INICIO :{}
    FIN    :{}
    {}
    {}
    """.format(
        boletin_costero["situacion"]["inicio"],
        boletin_costero["situacion"]["fin"],
        boletin_costero["prediccion"]["zona"][1]["subzona"]["nombre"].upper(),
        boletin_costero["prediccion"]["zona"][1]["subzona"]["texto"].upper()
    )


    #print(prediccion_cantabrico)
    return prediccion_cantabrico

if __name__ == "__main__":   
    pass




