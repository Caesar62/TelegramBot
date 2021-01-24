
import folium
from folium import plugins
from folium.plugins import Draw
from folium.plugins import MeasureControl
from folium import features
import json
import math
import os
import webbrowser
import swagger_client
from swagger_client.rest import ApiException

api_key  = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJjZXNhaW56bEBnbWFpbC5jb20iLCJqdGkiOiIyYjFiNjkxYS1iOTk4LTRiNzgtOTYwMS1lMGViMTcwNjEwYWUiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTU4NjEyMjM1MiwidXNlcklkIjoiMmIxYjY5MWEtYjk5OC00Yjc4LTk2MDEtZTBlYjE3MDYxMGFlIiwicm9sZSI6IiJ9.fb-wFsTLg-EthXoOjSwJ32o0WlcGTpZEJE5rYyHLf9U'

# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['api_key'] = api_key
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['api_key'] = 'Bearer'

try:
    os.stat("./SPReport")
except:
    os.mkdir("./SPReport")

def patterns():
    # MENU OPCIONES

    opcion = True
    while opcion:
        print("""
        +----------------------------------------------------+
        |                  Centro Jovellanos                 |
        |               IAMSAR PATTERN DESIGNER              |
        |                                                    |
        |                      OPTION MENU                   |
        +----------------------------------------------------+


        1- PARALLEL SEARCH
            CSP in a corner of the search area
        2- PARALLEL SEARCH 
            CSP at the center point on the side of the search area
        3- EXPANDING SQUARE SEARCH
        4- EXPANDING RECTANGLE SEARCH
        5- SECTOR SEARCH
        6- HELP
        7- EXIT

        """)
        opcion = input("""
        SELECT OPTION : 
        """)
        if opcion == "1":
            print("""
            +-----------------------------------------------------------------+
            |           PATRON DE BUSQUEDA.PARALLEL LADDER SEARCH             |
            |           CSP IN A CORNER OF THE SEARCH AREA                    |
            +-----------------------------------------------------------------+
            """)
            lat0 = str(input("\n\tLATITUD PUNTO COMIENZO BUSQUEDA  GGMM.M(N/S)\t:  ").replace(',','.')).upper()
            lon0 = str(input("\n\tLONGITUD PUNTO COMIENZO BUSQUEDA  GGGMM.M(E/W)\t:  ").replace(',','.')).upper()
            rumbo0 = float(input("\n\tRUMBO INICIAL\t\t\t\t\t:  ").replace(',','.'))
            leg_length = float(input("\n\tLARGO DEL PATRON DE BUSQUEDA\t:  "))
            pattern_width = float(input("\n\tANCHO DEL PATRON DE BUSQUEDA\t:  "))
            leg_spacing = float(input("\n\tLEG SPACING\t\t\t:  ").replace(',','.'))
            giro = input("\n\tSENSE (GIRO) L OR R\t\t:  ")
            pattern_name = input("\n\tPATTERN NAME\t\t\t:  ")

            num_legs = int(pattern_width//leg_spacing+1)

            # Pasar la latitud de ggmm.mN/S a gg.ggg
            latg=lat0[0:2]
            latm=lat0[2:6]
            latf=lat0[6:7]
            lat0=(float(latg)+float(latm)/60)
            if latf != "N":
                lat0 = 0 - lat0
            # Pasar la Longitud de gggmm.mE/W a gg.ggg
            long=lon0[0:3]
            lonm=lon0[3:7]
            lonf=lon0[7:8]
            lon0=(float(long)+float(lonm)/60)
            if lonf != "E":
                lon0 = 0 - lon0

            num_wps = num_legs*2
            num_tracks = num_legs*2-1
            rumboDistancia = []
            wpList = [[lat0, lon0]]
            wpListReverse = [[lon0, lat0]]

            def quita360(x): return x if x <= 360 else x-360

            def deg_to_rad(degree): return degree*math.pi/180

            def rad_to_deg(radian): return radian*180/math.pi

            def formalat(lat):
                if lat >= 0:
                    signolat = 'N'
                else:
                    signolat = 'S'
                return "{:02} {:06.3f} {}".format(int(abs(lat)), (abs(lat) - abs(int(lat)))*60, signolat)

            def formalon(lon):
                if lon >= 0:
                    signolon = 'E'
                else:
                    signolon = 'W'
                return "{:03} {:06.3f} {}".format(int(abs(lon)), (abs(lon) - abs(int(lon)))*60, signolon)
            # ESTIMA DIRECTA CON RETURN EN [lat,lon]

            def Directa(lat0, lon0, rumbo, distancia):
                diferencia_latitud = distancia * math.cos(deg_to_rad(rumbo))
                lat1 = lat0 + (diferencia_latitud/60)
                apartamiento = distancia * math.sin(deg_to_rad(rumbo))
                latitud_media = (lat0+lat1)/2
                diferencia_longitud = apartamiento / \
                    (math.cos(deg_to_rad(latitud_media)))
                lon1 = lon0 + (diferencia_longitud / 60)
                return [lat1, lon1]
            # ESTIMA DIRECTA CON RETURN EN [lon,lat]

            def DirectaReverse(lat0, lon0, rumbo, distancia):
                diferencia_latitud = distancia * math.cos(deg_to_rad(rumbo))
                lat1 = lat0 + (diferencia_latitud/60)
                apartamiento = distancia * math.sin(deg_to_rad(rumbo))
                latitud_media = (lat0+lat1)/2
                diferencia_longitud = apartamiento / \
                    (math.cos(deg_to_rad(latitud_media)))
                lon1 = lon0 + (diferencia_longitud / 60)
                return [lon1, lat1]
            j = 1
            if giro.upper() == "R":
                while j <= num_legs*2-1:
                    rumboDistancia.extend(([quita360(rumbo0), leg_length], ([quita360(rumbo0 + 90), leg_spacing]),
                                        ([quita360(rumbo0+180), leg_length]),
                                        ([quita360(rumbo0 + 90), leg_spacing])
                                        ))
                    j = j+4
                    rumboDistancia = rumboDistancia[0:num_tracks]
            else:
                while j <= num_legs*2-1:
                    rumboDistancia.extend(([quita360(rumbo0), leg_length], ([quita360(rumbo0 + 270), leg_spacing]),
                                        ([quita360(rumbo0+180), leg_length]),
                                        ([quita360(rumbo0 + 270), leg_spacing])
                                        ))
                    j = j+4
                    rumboDistancia = rumboDistancia[0:num_tracks]
                    #print(rumboDistancia)
            # LISTA DE WAYPOINTS [lat, lon]   wpList
            for w in range(num_wps-1):
                wpList.append(
                    Directa(wpList[w][0], wpList[w][1], rumboDistancia[w][0], rumboDistancia[w][1]))
            # LISTA DE WAYPOINTS [lon,lat] wpListReverse
            for z in range(num_wps-1):
                wpListReverse.append(DirectaReverse(
                    wpList[z][0], wpList[z][1], rumboDistancia[z][0], rumboDistancia[z][1]))
            ################## SALIDA CONSOLA ##########################

            def giro_fms(giro): return 'RIGHT'if giro.upper() == 'R' else 'LEFT'
            patternTrack = rumbo0+90 if giro.upper() == "R" else rumbo0-90
            patternTrack = patternTrack if patternTrack <= 360 else patternTrack-360
            patternTrack = patternTrack if patternTrack > 0 else patternTrack+360

            longitudTotalPattern = 0
            for elemento in rumboDistancia:
                longitudTotalPattern = longitudTotalPattern+elemento[1]

            ################## NMEA .CSV ##########################
            with open("./SPReport/{}_SPReportNMEA.csv".format(pattern_name.upper()), "w") as text_file:
                for d in range(len(wpList)):
                    print('$IIWPL,{},{},{},{},Pt.{}'.format(
                        (formalat(wpList[d][0]).replace(" ", "")[:-1]),
                        (formalat(wpList[d][0])[-1]),
                        (formalon(wpList[d][1]).replace(" ", "")[:-1]),
                        (formalon(wpList[d][1])[-1]),
                        d
                    ), file=text_file)

            ################## SALIDA .TXT ##########################
            with open("./SPReport/{}_SPReport.txt".format(pattern_name.upper()), "w") as text_file:
                print("""
    +-----------------------+
    |    SEARCH PATTERN     |
    +-----------------------+
    CSP\t\t\t:  {0}  {1}
    CSC\t\t\t:  {2}
    LENGHT\t\t\t:  {3}
    SPACING\t\t\t:  {4}
    TURN\t\t\t:  {5}
    LEGS\t\t\t:  {6}
    PATT. TOTAL LENGTH\t:  {7} NM
    ESP\t\t\t:  {8}  {9}""".format(
                    formalat(wpList[0][0]),
                    formalon(wpList[0][1]),
                    rumboDistancia[0][0],
                    leg_length,
                    leg_spacing,
                    giro_fms(giro),
                    num_legs,
                    longitudTotalPattern,
                    formalat(wpList[-1][0]),
                    formalon(wpList[-1][1])
                ), file=text_file)

                print("""
    +-----------------------+
    |AW 139 FMS PARAMETERS  |
    +-----------------------+
    SEARCH TYPE\t\t:  LADDER SEARCH
    1L\tSTART POSICION\t:  {0} {1}
    2L\tTURN DIRECTION\t:  {2}
    2R\tPATTERN TRACK\t:  {3}
    3L\tLEG SPACE\t:  {4}
    3R\tPATTERN WIDTH\t:  {5}
    4L\tSPEED\t\t:  {6}
    4R\tPATTERN LENGTH\t:  {7}""".format(  # {7:05.2f}
                    formalat((wpList[0][0]+wpList[1][0])/2),
                    formalon((wpList[0][1]+wpList[1][1])/2),
                    giro_fms(giro),
                    patternTrack,
                    leg_spacing,
                    leg_length,
                    "DEFAULT 90 KIAS",
                    num_legs*leg_spacing
                ), file=text_file)

            ############  CN 235   ############################

            # 235 CAM

                print("""
    +-----------------------+
    | CN 235 CAM PARAMETERS |
    +-----------------------+
    SEARCH PATTERN TYPE\t:  PARALLELOGRAM (PS)
    CSP \t\t\t:  {0} {1}
    ORIENTATION\t\t:  {2}
    TRACK LENGHT\t\t:  {3}
    NUMBER OF TRACKS\t:  {4}
    SENSE\t\t\t:  {5}
    TRACK SPACE METHOD\t: {6}
    TRACK SPACE\t\t:  {7}
            """.format(
                    formalat(wpList[0][0]),
                    formalon(wpList[0][1]),
                    rumbo0,
                    leg_length,
                    num_legs,
                    giro_fms(giro),
                    " MANUALLY",
                    leg_spacing
                ), file=text_file)

            # 235 FMS
                print("""
    +-----------------------+
    |CN 235 FMS PARAMETERS  |
    +-----------------------+
    PATTERN TYPE\t\t:  PARALLEL RISING LADDER
    IWPT INITIAL WAYPOINT\t:  {0} {1}
    ITRK INITIAL TRACK\t:  {2}
    IRTN INITIAL TURN DIR\t:  {3}
    LNTH LEG LEGHT\t\t:  {4}
    LSPC LEG SEPARATION\t:  {5}
    SEARCH SPEED\t\t:  {6}

    CSP COMMENCE SEARCH P\t:  {7} {8}
    ESP END SEARCH P\t:  {9} {10}""".format(
                    formalat(wpList[0][0]),
                    formalon(wpList[0][1]),
                    rumbo0,
                    giro_fms(giro),
                    leg_length,
                    leg_spacing,
                    "DEFAULT 148 KIAS",
                    formalat(wpList[0][0]),
                    formalon(wpList[0][1]),
                    formalat(wpList[-1][0]),
                    formalon(wpList[-1][1])
                ), file=text_file)

            # 235 FITS
                print("""
    +-----------------------+
    |CN 235 FITS PARAMETERS |
    +-----------------------+
    PATTERN TYPE\t\t:  PARALLEL SEARCH
    CSP COMMENCE SEARCH P\t:  {0} {1}
    ORIENTATION\t\t:  {2}
    SENSE\t\t\t:  {3}
    NUMBER OF TRACKS\t:  {4}
    TRACK SPACE\t\t:  {5}
    SEARCH SPEED\t\t:  {6}
    ESP END SEARCH P\t:  {7} {8}""".format(
                    formalat(wpList[0][0]),
                    formalon(wpList[0][1]),
                    rumbo0,
                    giro_fms(giro),
                    num_legs,
                    leg_spacing,
                    "DEFAULT ",
                    formalat(wpList[-1][0]),
                    formalon(wpList[-1][1])
                ), file=text_file)


    # PATTERN
                print("""
    +---------------------+
    |PATTERN WAYPOINTS    |
    +---------------------+""", file=text_file)
                for d in range(len(wpList)):
                    print('WP{:02}\t\t:  {}  {}'.format(d, formalat(
                        wpList[d][0]), formalon(wpList[d][1])), file=text_file)

                print("""
    +---------------------+
    |PATTERN TRACKS       |
    +---------------------+""", file=text_file)
                for e in range(len(rumboDistancia)):
                    print('TRK{:02}\t\t:  {:06.2f}  {:05.2f} NM'.format(
                        e+1, rumboDistancia[e][0], rumboDistancia[e][1]), file=text_file)

            ################## SALIDA GEOJSON ##########################
            # CREAR DATOS PARA ARCHIVO
            data = {}
            data["type"] = "FeatureCollection"
            data["features"] = [{
                "type": "Feature",
                "properties": {},
                "geometry": {
                        "type": "Point",
                        "coordinates": wpListReverse[0]
                },
                "properties": {
                    "name": "CSP"
                }
            },
                {
                "type": "Feature",
                "properties": {},
                "geometry": {
                        "type": "Point",
                        "coordinates": wpListReverse[-1]
                },
                "properties": {
                    "name": "ESP"
                }
            },
                {"type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "LineString",
                    "coordinates": wpListReverse
                }
                }]
            # VOLCAR DATOS A ARCHIVO
            # with open("C:\\SPRreport\SPReport.geojson", "w") as outfile:
            with open("./SPReport/{}_SPReport.geojson".format(pattern_name.upper()), "w") as outfile:
                json.dump(data, outfile)

            # MAPA

            map = folium.Map(
                location=[lat0, lon0],
                tiles='cartodbpositron',
                zoom_start=9
            )

            # MAT TOOLS PLUGIN
            draw = Draw()
            draw.add_to(map)

            folium.GeoJson("SPReport/{}_SPReport.geojson".format(pattern_name.upper()),
                        name=pattern_name.upper()).add_to(map)

            # WMOP MODEL
            wompWMS = "http://thredds.socib.es/thredds/wms/operational_models/oceanographical/hydrodynamics/wmop/latest.nc?"

            folium.WmsTileLayer(
                wompWMS,
                name="womp last",
                layers="sea_surface_velocity",
                styles="linevec/occam",
                fmt="image/png",
                transparent=True,
                opaciy=0.4
            ).add_to(map)

            # PdE IBI
            IBIWMS = "http://puertos2.cesga.es:8080/thredds/wms/dataset-ibi-analysis-forecast-phys-005-001-daily"
            folium.WmsTileLayer(
                IBIWMS,
                name="IBI",
                layers="sea_water_velocity",
                # styles="barb/redblue",
                styles="linevec/ferret",
                fmt="image/png",
                transparent=True,
                opaciy=0.4
            ).add_to(map)

            plugins.Fullscreen(
                position="topright",
                force_separate_button=True).add_to(map)

            folium.LayerControl().add_to(map)

            map.add_child(MeasureControl())

            map.save("pattern.html")
            webbrowser.open("pattern.html")
            map

        elif opcion == "2":
            print("""
            +-----------------------------------------------------------------+
            |           PATRON DE BUSQUEDA.PARALLEL                           |
            |           CSP AT THE CENTER POINN OF THE SEARCH AREA SIDE       |
            +-----------------------------------------------------------------+
            """)
            lat0 = str(input("\n\tLATITUD PUNTO COMIENZO BUSQUEDA  GGMM.M(N/S)\t:  ").replace(',','.')).upper()
            lon0 = str(input("\n\tLONGITUD PUNTO COMIENZO BUSQUEDA  GGGMM.M(E/W)\t:  ").replace(',','.')).upper()
            rumbo0 = float(input("\n\tRUMBO INICIAL\t\t\t\t\t:  "))
            leg_length = float(input("\n\tLARGO DEL PATRON DE BUSQUEDA\t:  "))
            pattern_width = float(input("\n\tANCHO DEL PATRON DE BUSQUEDA\t:  "))
            leg_spacing = float(input("\n\tLEG SPACING\t\t\t:  "))
            giro = input("\n\tSENSE (GIRO) L OR R\t\t:  ")
            pattern_name = input("\n\tPATTERN NAME\t\t\t:  ")

            num_legs = int(pattern_width//leg_spacing+1)
            #wpList = [[lat0, lon0]]
            #wpListReverse = [[lon0, lat0]]

            # Pasar la latitud de ggmm.mN/S a gg.ggg
            latg=lat0[0:2]
            latm=lat0[2:6]
            latf=lat0[6:7]
            lat0=(float(latg)+float(latm)/60)
            if latf != "N":
                lat0 = 0 - lat0
            # Pasar la Longitud de gggmm.mE/W a gg.ggg
            long=lon0[0:3]
            lonm=lon0[3:7]
            lonf=lon0[7:8]
            lon0=(float(long)+float(lonm)/60)
            if lonf != "E":
                lon0 = 0 - lon0

            wpList = [[lat0, lon0]]
            wpListReverse = [[lon0, lat0]]

            # FUNCIONES
            def quita360(x): return x if x <= 360 else x-360

            def deg_to_rad(degree): return degree*math.pi/180

            def rad_to_deg(radian): return radian*180/math.pi

            def formalat(lat):
                if lat >= 0:
                    signolat = 'N'
                else:
                    signolat = 'S'
            #    return str(int(abs(lat)))+' '+str(round((abs(lat) - abs(int(lat)))*60,1))+ signolat
                return "{:02} {:06.3f} {}".format(int(abs(lat)), (abs(lat) - abs(int(lat)))*60, signolat)

            def formalon(lon):
                if lon >= 0:
                    signolon = 'E'
                else:
                    signolon = 'W'
            #    return str(int(abs(lon)))+' '+str(round((abs(lon) - abs(int(lon)))*60,1))+ signolon
                return "{:03} {:06.3f} {}".format(int(abs(lon)), (abs(lon) - abs(int(lon)))*60, signolon)
            # ESTIMA DIRECTA CON RETURN EN [lat,lon]

            def Directa(lat0, lon0, rumbo, distancia):
                diferencia_latitud = distancia * math.cos(deg_to_rad(rumbo))
                lat1 = lat0 + (diferencia_latitud/60)
                apartamiento = distancia * math.sin(deg_to_rad(rumbo))
                latitud_media = (lat0+lat1)/2
                diferencia_longitud = apartamiento / \
                    (math.cos(deg_to_rad(latitud_media)))
                lon1 = lon0 + (diferencia_longitud / 60)
                return [lat1, lon1]
            # ESTIMA DIRECTA CON RETURN EN [lon,lat]

            def DirectaReverse(lat0, lon0, rumbo, distancia):
                diferencia_latitud = distancia * math.cos(deg_to_rad(rumbo))
                lat1 = lat0 + (diferencia_latitud/60)
                apartamiento = distancia * math.sin(deg_to_rad(rumbo))
                latitud_media = (lat0+lat1)/2
                diferencia_longitud = apartamiento / \
                    (math.cos(deg_to_rad(latitud_media)))
                lon1 = lon0 + (diferencia_longitud / 60)
                return [lon1, lat1]

            lista_distancias = []
            for i in range(1, int(num_legs)+1):
                lista_distancias.append(leg_length)
                lista_distancias.append(i*leg_spacing)
                lista_distancias = lista_distancias[0:(num_legs*2)]

            lista_rumbos = []
            for j in range(int(num_legs)):
                lista_rumbos.append(quita360(rumbo0))
                lista_rumbos.append(quita360(rumbo0+90))
                lista_rumbos.append(quita360(rumbo0+180))
                lista_rumbos.append(quita360(rumbo0+270))
                lista_rumbos = lista_rumbos[0:((num_legs*2))]

            rumboDistancia = []
            for k in range(len(lista_rumbos)):
                rumboDistancia.append([lista_rumbos[k], lista_distancias[k]])

            # LISTA DE WAYPOINTS [lat, lon]   wpList

            for w in range((len(rumboDistancia)-1)):
                # for w in range(num_wps-1):
                wpList.append(
                    Directa(wpList[w][0], wpList[w][1], rumboDistancia[w][0], rumboDistancia[w][1]))
            # LISTA DE WAYPOINTS [lon,lat] wpListReverse
            for z in range(len(rumboDistancia)-1):
                # for z in range(num_wps-1):
                wpListReverse.append(DirectaReverse(
                    wpList[z][0], wpList[z][1], rumboDistancia[z][0], rumboDistancia[z][1]))

            longitudTotalPattern = 0
            for elemento in rumboDistancia:
                longitudTotalPattern = longitudTotalPattern+elemento[1]

            #################  GEOJSON ##########################
            data = {}
            data["type"] = "FeatureCollection"
            data["features"] = [{
                "type": "Feature",
                "properties": {},
                "geometry": {
                        "type": "Point",
                        "coordinates": wpListReverse[0]
                },
                "properties": {
                    "name": "CSP"
                }
            },
                {
                "type": "Feature",
                "properties": {},
                "geometry": {
                        "type": "Point",
                        "coordinates": wpListReverse[-1]
                },
                "properties": {
                    "name": "ESP"
                }
            },
                {"type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "LineString",
                    "coordinates": wpListReverse
                }
                }]

            # VOLCAR DATOS A ARCHIVO
            # with open("C:\\SPRreport\SPReport.geojson", "w") as outfile:
            with open("./SPReport/{}_SPReport.geojson".format(pattern_name.upper()), "w") as outfile:
                json.dump(data, outfile)

            ################## NMEA .CSV ##########################
            with open("./SPReport/{}_SPReportNMEA.csv".format(pattern_name.upper()), "w") as text_file:
                for d in range(len(wpList)):
                    print('$IIWPL,{},{},{},{},Pt.{}'.format(
                        (formalat(wpList[d][0]).replace(" ", "")[:-1]),
                        (formalat(wpList[d][0])[-1]),
                        (formalon(wpList[d][1]).replace(" ", "")[:-1]),
                        (formalon(wpList[d][1])[-1]),
                        d
                    ), file=text_file)

            ################## SALIDA .TXT ##########################
            with open("./SPReport/{}_SPReport.txt".format(pattern_name.upper()), "w") as text_file:
                print("""
    +-----------------------+
    |    SEARCH PATTERN     |
    +-----------------------+
    CSP\t\t\t:  {0}  {1}
    CSC\t\t\t:  {2}
    LENGHT\t\t\t:  {3}
    SPACING\t\t\t:  {4}
    TURN\t\t\t:  {5}
    LEGS\t\t\t:  {6}
    PATTERN TOTAL LENGTH\t:  {7} NM
    ESP\t\t\t:  {8}  {9}""".format(
                    formalat(wpList[0][0]),
                    formalon(wpList[0][1]),
                    rumboDistancia[0][0],
                    leg_length,
                    leg_spacing,
                    "DEFAULT RIGHT",
                    num_legs,
                    longitudTotalPattern,
                    formalat(wpList[-1][0]),
                    formalon(wpList[-1][1])
                ), file=text_file)

                print("""
    +-----------------------+
    |AW 139 FMS PARAMETERS  |
    +-----------------------+
    SEARCH TYPE\t\t:  PARALLEL PATTERN SEARCH
    1L\tSTART POSICION\t:  {0} {1}
    2L\tTURN DIRECTION\t:  {2}  
    2R\tINITIAL TRACK\t:  {3}
    3L\tLEG SPACE\t:  {4}
    3R\tPATTERN WIDTH\t:  {5}
    4L\tSPEED\t\t:  {6}
    4R\tPATTERN LENGTH\t:  {7}""".format(  # {7:05.2f}
                    formalat(wpList[0][0]),
                    formalon(wpList[0][1]),
                    'DEFAULT (RIGHT)',
                    rumboDistancia[0][0],
                    leg_spacing,
                    num_legs*leg_spacing,
                    "DEFAULT 90 KIAS",
                    leg_length
                ), file=text_file)

                print("""
    +---------------------+
    |PATTERN WAYPOINTS    |
    +---------------------+""", file=text_file)
                for d in range(len(wpList)):
                    print('WP{:02}\t\t:  {}  {}'.format(d, formalat(
                        wpList[d][0]), formalon(wpList[d][1])), file=text_file)

                print("""
    +---------------------+
    PATTERN TRACKS        |
    +---------------------+""", file=text_file)
                for e in range(len(rumboDistancia)):
                    print('TRK{:02}\t\t:  {:06.2f}  {:05.2f} NM'.format(
                        e+1, rumboDistancia[e][0], rumboDistancia[e][1]), file=text_file)

            map = folium.Map(
                location=[lat0, lon0],
                tiles='cartodbpositron',
                zoom_start=7
            )

            # MAT TOOLS PLUGIN
            draw = Draw()
            draw.add_to(map)

            folium.GeoJson("SPReport/{}_SPReport.geojson".format(pattern_name.upper()),
                        name=pattern_name.upper()).add_to(map)

            # WMOP MODEL
            wompWMS = "http://thredds.socib.es/thredds/wms/operational_models/oceanographical/hydrodynamics/wmop/latest.nc?"

            folium.WmsTileLayer(
                wompWMS,
                name="womp last",
                layers="sea_surface_velocity",
                styles="linevec/occam",
                fmt="image/png",
                transparent=True,
                opaciy=0.4
            ).add_to(map)

            # PdE IBI
            IBIWMS = "http://puertos2.cesga.es:8080/thredds/wms/dataset-ibi-analysis-forecast-phys-005-001-daily"
            folium.WmsTileLayer(
                IBIWMS,
                name="IBI",
                layers="sea_water_velocity",
                # styles="barb/redblue",
                styles="linevec/ferret",
                fmt="image/png",
                transparent=True,
                opaciy=0.4
            ).add_to(map)

            plugins.Fullscreen(
                position="topright",
                force_separate_button=True).add_to(map)

            folium.LayerControl().add_to(map)

            map.add_child(MeasureControl())

            map.save("pattern.html")
            webbrowser.open("pattern.html")
            map

        elif opcion == "3":
            print("""
            +-----------------------------------------------------------------+
            |           PATRON DE BUSQUEDA.EXPANDING SQUARE SEARCH            |                             
            +-----------------------------------------------------------------+
            """)
            lat0 = str(input("\n\tLATITUD PUNTO COMIENZO BUSQUEDA  GGMM.M(N/S)\t:  ").replace(',','.')).upper()
            lon0 = str(input("\n\tLONGITUD PUNTO COMIENZO BUSQUEDA  GGGMM.M(E/W)\t:  ").replace(',','.')).upper()
            rumbo0 = float(input("\n\tRUMBO INICIAL\t\t\t:  "))
            leg_spacing = float(input("\n\tLEG SPACING\t\t\t:  "))
            giro = input("\n\tSENSE (GIRO) L OR R\t\t:  ")
            max_radius = float(input("\n\tMAXIMUN RADIUS (NM)\t\t:  "))
            pattern_name = input("\n\tPATTERN NAME\t\t\t:  ")

            # Pasar la latitud de ggmm.mN/S a gg.ggg
            latg=lat0[0:2]
            latm=lat0[2:6]
            latf=lat0[6:7]
            lat0=(float(latg)+float(latm)/60)
            if latf != "N":
                lat0 = 0 - lat0
            # Pasar la Longitud de gggmm.mE/W a gg.ggg
            long=lon0[0:3]
            lonm=lon0[3:7]
            lonf=lon0[7:8]
            lon0=(float(long)+float(lonm)/60)
            if lonf != "E":
                lon0 = 0 - lon0

            def giro_fms(giro): return 'RIGHT'if giro.upper() == 'R' else 'LEFT'

            def quita360(x): return x if x <= 360 else x-360

            def deg_to_rad(degree): return degree*math.pi/180

            def rad_to_deg(radian): return radian*180/math.pi

            def formalat(lat):
                if lat >= 0:
                    signolat = 'N'
                else:
                    signolat = 'S'
            #    return str(int(abs(lat)))+' '+str(round((abs(lat) - abs(int(lat)))*60,1))+ signolat
                return "{:02} {:06.3f} {}".format(int(abs(lat)), (abs(lat) - abs(int(lat)))*60, signolat)

            def formalon(lon):
                if lon >= 0:
                    signolon = 'E'
                else:
                    signolon = 'W'
            #    return str(int(abs(lon)))+' '+str(round((abs(lon) - abs(int(lon)))*60,1))+ signolon
                return "{:03} {:06.3f} {}".format(int(abs(lon)), (abs(lon) - abs(int(lon)))*60, signolon)

            rumboDistancia = []
            wpList = [[lat0, lon0]]
            wpListReverse = [[lon0, lat0]]
            num_tracks = int((max_radius//leg_spacing)*4+1)

            # ESTIMA DIRECTA CON RETURN EN [lat,lon]
            def Directa(lat0, lon0, rumbo, distancia):
                diferencia_latitud = distancia * math.cos(deg_to_rad(rumbo))
                lat1 = lat0 + (diferencia_latitud/60)
                apartamiento = distancia * math.sin(deg_to_rad(rumbo))
                latitud_media = (lat0+lat1)/2
                diferencia_longitud = apartamiento / \
                    (math.cos(deg_to_rad(latitud_media)))
                lon1 = lon0 + (diferencia_longitud / 60)
                return [lat1, lon1]
            # ESTIMA DIRECTA CON RETURN EN [lon,lat]

            def DirectaReverse(lat0, lon0, rumbo, distancia):
                diferencia_latitud = distancia * math.cos(deg_to_rad(rumbo))
                lat1 = lat0 + (diferencia_latitud/60)
                apartamiento = distancia * math.sin(deg_to_rad(rumbo))
                latitud_media = (lat0+lat1)/2
                diferencia_longitud = apartamiento / \
                    (math.cos(deg_to_rad(latitud_media)))
                lon1 = lon0 + (diferencia_longitud / 60)
                return [lon1, lat1]

            if giro.upper() == "R":
                lista_rumbos = []
                for j in range(int(num_tracks)):
                    lista_rumbos.append(quita360(rumbo0))
                    lista_rumbos.append(quita360(rumbo0+90))
                    lista_rumbos.append(quita360(rumbo0+180))
                    lista_rumbos.append(quita360(rumbo0+270))
                    lista_rumbos = lista_rumbos[0:((num_tracks))]

                lista_distancias = []
                for i in range(1, 100):
                    lista_distancias.extend([leg_spacing*i, leg_spacing*i])
                    lista_distancias = lista_distancias[0:((num_tracks))]
            else:
                lista_rumbos = []
                for j in range(int(num_tracks)):
                    lista_rumbos.append(quita360(rumbo0))
                    lista_rumbos.append(quita360(rumbo0+270))
                    lista_rumbos.append(quita360(rumbo0+180))
                    lista_rumbos.append(quita360(rumbo0+90))
                    lista_rumbos = lista_rumbos[0:((num_tracks))]

                lista_distancias = []
                for i in range(1, 100):
                    lista_distancias.extend([leg_spacing*i, leg_spacing*i])
                    lista_distancias = lista_distancias[0:((num_tracks))]

            rumboDistancia = []
            for k in range(len(lista_rumbos)):
                rumboDistancia.append([lista_rumbos[k], lista_distancias[k]])
            num_wps = len(rumboDistancia)

            # LISTA DE WAYPOINTS [lat, lon]   wpList
            for w in range(num_wps):
                wpList.append(
                    Directa(wpList[w][0], wpList[w][1], rumboDistancia[w][0], rumboDistancia[w][1]))
            # LISTA DE WAYPOINTS [lon,lat] wpListReverse

            for z in range(num_wps):
                wpListReverse.append(DirectaReverse(
                    wpList[z][0], wpList[z][1], rumboDistancia[z][0], rumboDistancia[z][1]))

            longitudTotalPattern = 0
            for elemento in rumboDistancia:
                longitudTotalPattern = longitudTotalPattern+elemento[1]

            # ################## SALIDA .TXT ##########################
            with open("./SPReport/{}_SPReport.txt".format(pattern_name.upper()), "w") as text_file:

                print("""
    +-----------------------+
    |AW 139 FMS PARAMETERS  |
    +-----------------------+
    SEARCH TYPE\t\t:  EXPANDING SQUARE SEARCH
    1L\tSTART POSICION\t:  {0} {1}
    2L\tTURN DIRECTION\t:  {2}
    2R\tINITIAL TRACK\t:  {3}
    3L\tLEG SPACE\t:  {4}
    3R\tINITIAL LEG L\t:  {5}
    4L\tSPEED\t\t:  {6}
    4R\tMAXIMUN RADIUS\t:  {7}""".format(  # {7:05.2f}
                    formalat(wpList[0][0]),
                    formalon(wpList[0][1]),
                    giro_fms(giro),
                    rumbo0,
                    leg_spacing,
                    leg_spacing,
                    "DEFAULT 90 KIAS- MINIMUN 60KT",
                    max_radius
                ), file=text_file)

            # PATTERN
                print("""
    +---------------------+
    |PATTERN WAYPOINTS    |
    +---------------------+""", file=text_file)
                for d in range(len(wpList)):
                    print('WP{:02}\t\t:  {}  {}'.format(d, formalat(
                        wpList[d][0]), formalon(wpList[d][1])), file=text_file)

                print("""
    +---------------------+
    |PATTERN TRACKS       |
    +---------------------+""", file=text_file)
                for e in range(len(rumboDistancia)):
                    print('TRK{:02}\t\t:  {:06.2f}  {:05.2f} NM'.format(
                        e+1, rumboDistancia[e][0], rumboDistancia[e][1]), file=text_file)

            ################## SALIDA GEOJSON ##########################
            # CREAR DATOS PARA ARCHIVO
            data = {}
            data["type"] = "FeatureCollection"
            data["features"] = [{
                "type": "Feature",
                "properties": {},
                "geometry": {
                        "type": "Point",
                        "coordinates": wpListReverse[0]
                },
                "properties": {
                    "name": "CSP"
                }
            },
                {
                "type": "Feature",
                "properties": {},
                "geometry": {
                        "type": "Point",
                        "coordinates": wpListReverse[-1]
                },
                "properties": {
                    "name": "ESP"
                }
            },
                {"type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "LineString",
                    "coordinates": wpListReverse
                }
                }]
            # VOLCAR DATOS A ARCHIVO
            # with open("C:\\SPRreport\SPReport.geojson", "w") as outfile:
            with open("./SPReport/{}_SPReport.geojson".format(pattern_name.upper()), "w") as outfile:
                json.dump(data, outfile)
            map = folium.Map(
                location=[lat0, lon0],
                tiles='cartodbpositron',
                zoom_start=7
            )
            draw = Draw()
            draw.add_to(map)
            folium.GeoJson("SPReport/{}_SPReport.geojson".format(pattern_name.upper()),
                        name=pattern_name.upper()).add_to(map)

            # WMOP MODEL
            wompWMS = "http://thredds.socib.es/thredds/wms/operational_models/oceanographical/hydrodynamics/wmop/latest.nc?"
            folium.WmsTileLayer(
                wompWMS,
                name="womp last",
                layers="sea_surface_velocity",
                styles="linevec/occam",
                fmt="image/png",
                transparent=True,
                opaciy=0.4
            ).add_to(map)

            # PdE IBI
            IBIWMS = "http://puertos2.cesga.es:8080/thredds/wms/dataset-ibi-analysis-forecast-phys-005-001-daily"
            folium.WmsTileLayer(
                IBIWMS,
                name="IBI",
                layers="sea_water_velocity",
                # styles="barb/redblue",
                styles="linevec/ferret",
                fmt="image/png",
                transparent=True,
                opaciy=0.4
            ).add_to(map)

            plugins.Fullscreen(
                position="topright",
                force_separate_button=True).add_to(map)

            folium.LayerControl().add_to(map)

            map.add_child(MeasureControl())

            map.save("pattern.html")
            webbrowser.open("pattern.html")
            map

        elif opcion == "4":
            print("""
            +-----------------------------------------------------------------+
            |           PATRON DE BUSQUEDA.EXPANDING. EXPANDING RECTANGLE     |                             
            +-----------------------------------------------------------------+
            """)
            lat0 = str(input("\n\tLATITUD PUNTO COMIENZO BUSQUEDA  GGMM.M(N/S)\t:  ").replace(',','.')).upper()
            lon0 = str(input("\n\tLONGITUD PUNTO COMIENZO BUSQUEDA  GGGMM.M(E/W)\t:  ").replace(',','.')).upper()
            rumbo0 = float(input("\n\tRUMBO INICIAL\t\t\t:  "))
            leg_spacing = float(input("\n\tLEG SPACING\t\t\t:  "))
            initial_track = float(input("\n\tINITIAL TRACK\t\t\t:  "))
            giro = input("\n\tSENSE (GIRO) L OR R\t\t:  ")
            pattern_width = float(input("\n\tPATTERN WIDTH (NM)\t\t:  "))
            pattern_name = input("\n\tPATTERN NAME\t\t\t:  ")

            # Pasar la latitud de ggmm.mN/S a gg.ggg
            latg=lat0[0:2]
            latm=lat0[2:6]
            latf=lat0[6:7]
            lat0=(float(latg)+float(latm)/60)
            if latf != "N":
                lat0 = 0 - lat0
            # Pasar la Longitud de gggmm.mE/W a gg.ggg
            long=lon0[0:3]
            lonm=lon0[3:7]
            lonf=lon0[7:8]
            lon0=(float(long)+float(lonm)/60)
            if lonf != "E":
                lon0 = 0 - lon0


            def giro_fms(giro): return 'RIGHT'if giro.upper() == 'R' else 'LEFT'

            def quita360(x): return x if x <= 360 else x-360

            def deg_to_rad(degree): return degree*math.pi/180

            def rad_to_deg(radian): return radian*180/math.pi

            def formalat(lat):
                if lat >= 0:
                    signolat = 'N'
                else:
                    signolat = 'S'
            #    return str(int(abs(lat)))+' '+str(round((abs(lat) - abs(int(lat)))*60,1))+ signolat
                return "{:02} {:06.3f} {}".format(int(abs(lat)), (abs(lat) - abs(int(lat)))*60, signolat)

            def formalon(lon):
                if lon >= 0:
                    signolon = 'E'
                else:
                    signolon = 'W'
            #    return str(int(abs(lon)))+' '+str(round((abs(lon) - abs(int(lon)))*60,1))+ signolon
                return "{:03} {:06.3f} {}".format(int(abs(lon)), (abs(lon) - abs(int(lon)))*60, signolon)

            rumboDistancia = []
            wpList = [[lat0, lon0]]
            wpListReverse = [[lon0, lat0]]

            num_tracks = int((pattern_width//leg_spacing)*2+1)

            # ESTIMA DIRECTA CON RETURN EN [lat,lon]
            def Directa(lat0, lon0, rumbo, distancia):
                diferencia_latitud = distancia * math.cos(deg_to_rad(rumbo))
                lat1 = lat0 + (diferencia_latitud/60)
                apartamiento = distancia * math.sin(deg_to_rad(rumbo))
                latitud_media = (lat0+lat1)/2
                diferencia_longitud = apartamiento / \
                    (math.cos(deg_to_rad(latitud_media)))
                lon1 = lon0 + (diferencia_longitud / 60)
                return [lat1, lon1]
            # ESTIMA DIRECTA CON RETURN EN [lon,lat]

            def DirectaReverse(lat0, lon0, rumbo, distancia):
                diferencia_latitud = distancia * math.cos(deg_to_rad(rumbo))
                lat1 = lat0 + (diferencia_latitud/60)
                apartamiento = distancia * math.sin(deg_to_rad(rumbo))
                latitud_media = (lat0+lat1)/2
                diferencia_longitud = apartamiento / \
                    (math.cos(deg_to_rad(latitud_media)))
                lon1 = lon0 + (diferencia_longitud / 60)
                return [lon1, lat1]
            ################# fin funciones

            if giro.upper() == "R":
                lista_rumbos = []
                for j in range(int(num_tracks)):
                    lista_rumbos.append(quita360(rumbo0))
                    lista_rumbos.append(quita360(rumbo0+90))
                    lista_rumbos.append(quita360(rumbo0+180))
                    lista_rumbos.append(quita360(rumbo0+270))
                lista_rumbos = lista_rumbos[0:((num_tracks))]

                lista_distancias = [initial_track]
                for i in range(1, 50):
                    lista_distancias.extend(
                        [leg_spacing*i, leg_spacing*i+initial_track])
                lista_distancias = lista_distancias[0:((num_tracks))]

            else:
                lista_rumbos = []
                for j in range(int(num_tracks)):
                    lista_rumbos.append(quita360(rumbo0))
                    lista_rumbos.append(quita360(rumbo0+270))
                    lista_rumbos.append(quita360(rumbo0+180))
                    lista_rumbos.append(quita360(rumbo0+90))
                    lista_rumbos = lista_rumbos[0:((num_tracks))]

                lista_distancias = [initial_track]
                for i in range(1, 50):
                    lista_distancias.extend(
                        [leg_spacing*i, leg_spacing*i+initial_track])
                    lista_distancias = lista_distancias[0:((num_tracks))]

            rumboDistancia = []
            for k in range(len(lista_rumbos)):
                rumboDistancia.append([lista_rumbos[k], lista_distancias[k]])

            num_wps = len(rumboDistancia)

            #LISTA DE WAYPOINTS [lat, lon]   wpList
            for w in range(num_wps):
                wpList.append(
                    Directa(wpList[w][0], wpList[w][1], rumboDistancia[w][0], rumboDistancia[w][1]))
            #LISTA DE WAYPOINTS [lon,lat] wpListReverse

            for z in range(num_wps):
                wpListReverse.append(DirectaReverse(
                    wpList[z][0], wpList[z][1], rumboDistancia[z][0], rumboDistancia[z][1]))

            longitudTotalPattern = 0
            for elemento in rumboDistancia:
                longitudTotalPattern = longitudTotalPattern+elemento[1]

            # ################## SALIDA .TXT ##########################
            with open("./SPReport/{}_SPReport.txt".format(pattern_name.upper()), "w") as text_file:
                print("""
    +-----------------------+
    |    SEARCH PATTERN     |
    +-----------------------+
    CSP\t\t\t:  {0}  {1}
    CSC\t\t\t:  {2}
    INITIAL LENGTH\t\t:  {3}
    SPACING\t\t\t:  {4}
    TURN\t\t\t:  {5}
    LEGS\t\t\t:  {6}
    PATTERN TOTAL LENGTH\t:  {7} NM
    ESP\t\t\t:  {8}  {9}""".format(
                    formalat(wpList[0][0]),
                    formalon(wpList[0][1]),
                    rumboDistancia[0][0],
                    leg_spacing,
                    leg_spacing,
                    giro_fms(giro),
                    len(rumboDistancia),
                    longitudTotalPattern,
                    formalat(wpList[-1][0]),
                    formalon(wpList[-1][1])
                ), file=text_file)

                print("""
    +-----------------------+
    |AW 139 FMS PARAMETERS  |
    +-----------------------+
    SEARCH TYPE\t\t:  EXPANDING RECTANGLE
    1L\tSTART POSICION\t:  {0} {1}
    2L\tTURN DIRECTION\t:  {2}
    2R\tINITIAL TRACK\t:  {3}
    3L\tLEG SPACE\t:  {4}
    3R\tINITIAL LEG L\t:  {5}
    4L\tSPEED\t\t:  {6}
    4R\tCAMBIAR\t:  {7}""".format(  # {7:05.2f}
                    formalat((wpList[0][0]+wpList[1][0])/2),
                    formalon((wpList[0][1]+wpList[1][1])/2),
                    giro_fms(giro),
                    rumbo0,
                    leg_spacing,
                    leg_spacing,
                    "DEFAULT 90 KIAS- MINIMUN 60KT",
                    "CAMBIAR"
                ), file=text_file)

            ######################## PATTERN
                print("""
    +---------------------+
    |PATTERN WAYPOINTS    |
    +---------------------+""", file=text_file)
                for d in range(len(wpList)):
                    print('WP{:02}\t\t:  {}  {}'.format(d, formalat(
                        wpList[d][0]), formalon(wpList[d][1])), file=text_file)

                print("""
    +---------------------+
    PATTERN TRACKS        |
    +---------------------+""", file=text_file)
                for e in range(len(rumboDistancia)):
                    print('TRK{:02}\t\t:  {:06.2f}  {:05.2f} NM'.format(
                        e+1, rumboDistancia[e][0], rumboDistancia[e][1]), file=text_file)

            ################## SALIDA GEOJSON ##########################
            ### CREAR DATOS PARA ARCHIVO
            data = {}
            data["type"] = "FeatureCollection"
            data["features"] = [{
                "type": "Feature",
                "properties": {},
                "geometry": {
                        "type": "Point",
                        "coordinates": wpListReverse[0]
                },
                "properties": {
                    "name": "CSP"
                }
            },
                {
                "type": "Feature",
                "properties": {},
                "geometry": {
                        "type": "Point",
                        "coordinates": wpListReverse[-1]
                },
                "properties": {
                    "name": "ESP"
                }
            },
                {"type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "LineString",
                    "coordinates": wpListReverse
                }
                }]
            ### VOLCAR DATOS A ARCHIVO
            #with open("C:\\SPRreport\SPReport.geojson", "w") as outfile:
            with open("./SPReport/{}_SPReport.geojson".format(pattern_name.upper()), "w") as outfile:
                json.dump(data, outfile)

            map = folium.Map(
                location=[lat0, lon0],
                tiles='cartodbpositron',
                zoom_start=7
            )

            # MAT TOOLS PLUGIN
            draw = Draw()
            draw.add_to(map)

            folium.GeoJson("SPReport/{}_SPReport.geojson".format(pattern_name.upper()),
                        name=pattern_name.upper()).add_to(map)

            #WOMP
            wompWMS = "http://thredds.socib.es/thredds/wms/operational_models/oceanographical/hydrodynamics/wmop/latest.nc?"
            folium.WmsTileLayer(
                wompWMS,
                name="womp last",
                layers="sea_surface_velocity",
                #styles="linevec/gmt_ocean",
                styles="linevec/occam",
                #styles="stumpvec/temp_diff_1lev",
                fmt="image/png",
                transparent=True,
                opaciy=0.4
            ).add_to(map)

            # PdE IBI
            IBIWMS = "http://puertos2.cesga.es:8080/thredds/wms/dataset-ibi-analysis-forecast-phys-005-001-daily"
            folium.WmsTileLayer(
                IBIWMS,
                name="IBI",
                layers="sea_water_velocity",
                #styles="barb/redblue",
                styles="linevec/ferret",
                fmt="image/png",
                transparent=True,
                opaciy=0.4
            ).add_to(map)

            plugins.Fullscreen(
                position="topright",
                force_separate_button=True).add_to(map)

            folium.LayerControl().add_to(map)

            map.add_child(MeasureControl())

            map.save("pattern.html")
            webbrowser.open("pattern.html")
            map


    ##########################################################

        elif opcion == "5":
            print("""
            +-----------------------------------------------------------------+
            |           PATRON DE BUSQUEDA.SECTOR SEARCH                      |                             
            |           60 DEGREES SECTOR                                     |                             
            +-----------------------------------------------------------------+
            """)
            lat0 = str(input("\n\tLATITUD PUNTO COMIENZO BUSQUEDA  GGMM.M(N/S)\t:  ").replace(',','.')).upper()
            lon0 = str(input("\n\tLONGITUD PUNTO COMIENZO BUSQUEDA  GGGMM.M(E/W)\t:  ").replace(',','.')).upper()
            rumbo0 = float(input("\n\tRUMBO INICIAL\t\t\t:  "))
            radial_space = float(input("\n\tINITIAL TRACK (NM)\t\t:  "))
            giro = input("\n\tSENSE (GIRO) L OR R\t\t:  ")
            pattern_name = input("\n\tPATTERN NAME\t\t\t:  ")

            radius = radial_space*0.866

            # Pasar la latitud de ggmm.mN/S a gg.ggg
            latg=lat0[0:2]
            latm=lat0[2:6]
            latf=lat0[6:7]
            lat0=(float(latg)+float(latm)/60)
            if latf != "N":
                lat0 = 0 - lat0
            # Pasar la Longitud de gggmm.mE/W a gg.ggg
            long=lon0[0:3]
            lonm=lon0[3:7]
            lonf=lon0[7:8]
            lon0=(float(long)+float(lonm)/60)
            if lonf != "E":
                lon0 = 0 - lon0


            def giro_fms(giro): return 'RIGHT'if giro.upper() == 'R' else 'LEFT'

            def quita360(x): return x if x <= 360 else x-360

            def deg_to_rad(degree): return degree*math.pi/180

            def rad_to_deg(radian): return radian*180/math.pi

            def formalat(lat):
                if lat >= 0:
                    signolat = 'N'
                else:
                    signolat = 'S'
            #    return str(int(abs(lat)))+' '+str(round((abs(lat) - abs(int(lat)))*60,1))+ signolat
                return "{:02} {:06.3f} {}".format(int(abs(lat)), (abs(lat) - abs(int(lat)))*60, signolat)

            def formalon(lon):
                if lon >= 0:
                    signolon = 'E'
                else:
                    signolon = 'W'
            #    return str(int(abs(lon)))+' '+str(round((abs(lon) - abs(int(lon)))*60,1))+ signolon
                return "{:03} {:06.3f} {}".format(int(abs(lon)), (abs(lon) - abs(int(lon)))*60, signolon)

            rumboDistancia = []
            wpList = [[lat0, lon0]]
            wpListReverse = [[lon0, lat0]]

            #num_tracks=int((max_radius//leg_spacing)*4+1)

            # ESTIMA DIRECTA CON RETURN EN [lat,lon]
            def Directa(lat0, lon0, rumbo, distancia):
                diferencia_latitud = distancia * math.cos(deg_to_rad(rumbo))
                lat1 = lat0 + (diferencia_latitud/60)
                apartamiento = distancia * math.sin(deg_to_rad(rumbo))
                latitud_media = (lat0+lat1)/2
                diferencia_longitud = apartamiento / \
                    (math.cos(deg_to_rad(latitud_media)))
                lon1 = lon0 + (diferencia_longitud / 60)
                return [lat1, lon1]
            # ESTIMA DIRECTA CON RETURN EN [lon,lat]

            def DirectaReverse(lat0, lon0, rumbo, distancia):
                diferencia_latitud = distancia * math.cos(deg_to_rad(rumbo))
                lat1 = lat0 + (diferencia_latitud/60)
                apartamiento = distancia * math.sin(deg_to_rad(rumbo))
                latitud_media = (lat0+lat1)/2
                diferencia_longitud = apartamiento / \
                    (math.cos(deg_to_rad(latitud_media)))
                lon1 = lon0 + (diferencia_longitud / 60)
                return [lon1, lat1]
            ################# fin funciones

            rumboDistancia = []
            if giro.upper() == "R":
                rumboDistancia = [
                    [quita360(rumbo0), radial_space],
                    [quita360(rumbo0+120), radial_space],
                    [quita360(rumbo0+240), 2*radial_space],
                    [quita360(rumbo0), radial_space],
                    [quita360(rumbo0+120), 2*radial_space],
                    [quita360(rumbo0+240), radial_space],
                    [quita360(rumbo0), radial_space],
                    [quita360((rumbo0+30)), radial_space],
                    [quita360((rumbo0+150)), radial_space],
                    [quita360((rumbo0+270)), 2*radial_space],
                    [quita360((rumbo0+30)), radial_space],
                    [quita360((rumbo0+150)), 2*radial_space],
                    [quita360((rumbo0+270)), radial_space],
                    [quita360((rumbo0+30)), radial_space]
                ]
            else:
                    rumboDistancia = [
                        [quita360(rumbo0), radial_space],
                        [quita360(rumbo0+240), radial_space],
                        [quita360(rumbo0+120), 2*radial_space],
                        [quita360(rumbo0), radial_space],
                        [quita360(rumbo0+240), 2*radial_space],
                        [quita360(rumbo0+120), radial_space],
                        [quita360(rumbo0), radial_space],
                        [quita360((rumbo0-30)), radial_space],
                        [quita360((rumbo0+210)), radial_space],
                        [quita360((rumbo0+90)), 2*radial_space],
                        [quita360((rumbo0-30)), radial_space],
                        [quita360((rumbo0+210)), 2*radial_space],
                        [quita360((rumbo0+90)), radial_space],
                        [quita360((rumbo0-30)), radial_space]
                    ]

            num_wps = len(rumboDistancia)

            #LISTA DE WAYPOINTS [lat, lon]   wpList
            for w in range(num_wps):
                wpList.append(
                    Directa(wpList[w][0], wpList[w][1], rumboDistancia[w][0], rumboDistancia[w][1]))
            #LISTA DE WAYPOINTS [lon,lat] wpListReverse

            for z in range(num_wps):
                wpListReverse.append(DirectaReverse(
                    wpList[z][0], wpList[z][1], rumboDistancia[z][0], rumboDistancia[z][1]))

            longitudTotalPattern = 0
            for elemento in rumboDistancia:
                longitudTotalPattern = longitudTotalPattern+elemento[1]

            # ################## SALIDA .TXT ##########################
            with open("./SPReport/{}_SPReport.txt".format(pattern_name.upper()), "w") as text_file:
                print("""
    +-----------------------+
    |    SEARCH PATTERN     |
    +-----------------------+
    SEARCH TYPE\t\t:  SECTOR SEARCH
    SECTOR\t\t\t:  60 DEGREES
    SECOND SEARCH\t\t:  +30 DEGREES

    DATUM\t\t\t:  {0}  {1}
    CSC\t\t\t:  {2}
    INITIAL TRACK (S)\t:  {3}
    TURN\t\t\t:  {4}
    PATTERN TOTAL LENGTH\t:  {5} NM
    ESP\t\t\t:  {6}  {7}""".format(
                    formalat(wpList[0][0]),
                    formalon(wpList[0][1]),
                    rumboDistancia[0][0],
                    radial_space,
                    giro_fms(giro),
                    longitudTotalPattern,
                    formalat(wpList[0][0]),
                    formalon(wpList[0][1])
                ), file=text_file)

                print("""
    +-----------------------+
    |AW 139 FMS PARAMETERS  |
    +-----------------------+
    SEARCH TYPE\t\t:  EXPANDING SQUARE SEARCH
    1L\tSTART POSICION\t:  {0} {1}
    2L\tTURN DIRECTION\t:  {2}
    2R\tINITIAL TRACK\t:  {3}
    3L\tRADIAL SPACE\t:  {4}
    3R\tSECTOR ANGLE L\t:  {5}
    4L\tSPEED\t\t:  {6}
    4R\tPATTERN RADIUS\t:  {7}""".format(  # {7:05.2f}
                    formalat((wpList[0][0]+wpList[1][0])/2),
                    formalon((wpList[0][1]+wpList[1][1])/2),
                    giro_fms(giro),
                    rumbo0,
                    radial_space,
                    "60 DEGREES",
                    "DEFAULT 90 KIAS- MINIMUN 60KT",
                    round(radius, 2)
                ), file=text_file)

            ######################## PATTERN
                print("""
    +---------------------+
    |PATTERN WAYPOINTS    |
    +---------------------+""", file=text_file)
                for d in range(len(wpList)):
                    print('WP{:02}\t\t:  {}  {}'.format(d, formalat(
                        wpList[d][0]), formalon(wpList[d][1])), file=text_file)

                print("""
    +---------------------+
    PATTERN TRACKS        |
    +---------------------+""", file=text_file)
                for e in range(len(rumboDistancia)):
                    print('TRK{:02}\t\t:  {:06.2f}  {:05.2f} NM'.format(
                        e+1, rumboDistancia[e][0], rumboDistancia[e][1]), file=text_file)

    ############################# SALIDA GEOJSON ##########################
            data = {}
            data["type"] = "FeatureCollection"
            data["features"] = [{
                "type": "Feature",
                "properties": {},
                "geometry": {
                        "type": "Point",
                        "coordinates": wpListReverse[0]
                },
                "properties": {
                    "name": "CSP"
                }
            },
                {
                "type": "Feature",
                "properties": {},
                "geometry": {
                        "type": "Point",
                        "coordinates": wpListReverse[-1]
                },
                "properties": {
                    "name": "ESP"
                }
            },
                {"type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "LineString",
                    "coordinates": wpListReverse
                }
                }]
            with open("./SPReport/{}_SPReport.geojson".format(pattern_name.upper()), "w") as outfile:
                json.dump(data, outfile)

            map = folium.Map(
                location=[lat0, lon0],
                tiles='cartodbpositron',
                zoom_start=7
            )

            # MAT TOOLS PLUGIN
            draw = Draw()
            draw.add_to(map)

            folium.GeoJson("SPReport/{}_SPReport.geojson".format(pattern_name.upper()),
                        name=pattern_name.upper()).add_to(map)

            #WOMP
            wompWMS = "http://thredds.socib.es/thredds/wms/operational_models/oceanographical/hydrodynamics/wmop/latest.nc?"
            folium.WmsTileLayer(
                wompWMS,
                name="womp last",
                layers="sea_surface_velocity",
                #styles="linevec/gmt_ocean",
                styles="linevec/occam",
                #styles="stumpvec/temp_diff_1lev",
                fmt="image/png",
                transparent=True,
                opaciy=0.4
            ).add_to(map)

            # PdE IBI
            IBIWMS = "http://puertos2.cesga.es:8080/thredds/wms/dataset-ibi-analysis-forecast-phys-005-001-daily"
            folium.WmsTileLayer(
                IBIWMS,
                name="IBI",
                layers="sea_water_velocity",
                #styles="barb/redblue",
                styles="linevec/ferret",
                fmt="image/png",
                transparent=True,
                opaciy=0.4
            ).add_to(map)

            plugins.Fullscreen(
                position="topright",
                force_separate_button=True).add_to(map)

            folium.LayerControl().add_to(map)

            map.add_child(MeasureControl())

            map.save("pattern.html")
            webbrowser.open("pattern.html")
            map

        elif opcion == '6':
            print('''
            SCRIPT PARA CONSTRUIR PATTERN DE BÚSQUEDA. 
        __________________________________________

            Opciones:
                1- PARALLEL SEARCH
                CSP in a corner of the search area 
                2- PARALLEL SEARCH 
                CSP at the center point on the side of the search area
                3- EXPANDING SQUARE SEARCH
                4- EXPANDING RECTANGLE SEARCH
                5- SECTOR SEARCH
                6- HELP
                7- EXIT
            
            Si no existe el directorio SPRerport, lo crea con los siguientes 
            archivos:
                .geojson    Archivo con la información geográfica del pattern. 
                            Válido para su visualización en GIS
                .txt        Contiene la información del pattern y los wps,así 
                            como los rumbos y distancias de cada uno de los 
                            tracks que conforman el pattern.
                .csv        opcionalmente archivo con la informacion 
                            geográfica del pattern en formato NMEA

            Crea un archivo HTML con un visor para el pattern y herramientas 
            de dibujo.

            Muestra capas con la información on-line de los modelos hidródinámicos 
            SOCIB WOMP y MyO IBI
        
        Enter para continuar.

            ''')
            input()

        elif opcion == "7":
            print('''
            Goodbye
            ''')
            opcion = None
        else:
            print("\n Not Valid Choice Try again")

if __name__ == "__main__":   
    pass